from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from tools import sd1_causal_execution_controller as controller

RECEIPT_PAYLOAD_KEYS = {
    "schema", "run_id", "sequence", "slot_id", "response_id",
    "record_digest", "previous_record_digest", "runtime_readback_digest", "plan_subject_digest",
}
_HEX40 = re.compile(r"^[0-9a-f]{40}$")
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True
    )
    if check and proc.returncode != 0:
        raise ValueError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc


def _git(repo: Path, *args: str, check: bool = True) -> str:
    return _run_git(repo, *args, check=check).stdout.strip()


def _normalize_github_repo(url: str) -> str | None:
    value = url.strip()
    if value.startswith("git@github.com:"):
        value = value[len("git@github.com:"):]
    elif value.startswith("ssh://git@github.com/"):
        value = value[len("ssh://git@github.com/"):]
    elif value.startswith("https://github.com/"):
        value = value[len("https://github.com/"):]
    elif value.startswith("http://github.com/"):
        value = value[len("http://github.com/"):]
    else:
        return None
    if value.endswith(".git"):
        value = value[:-4]
    return value.strip("/")


def _receipt_path(run_id: str, sequence: int, slot_id: str) -> str:
    return (
        f"state/runtime/sd1-causal-receipts/{run_id}/"
        f"{sequence:03d}-{slot_id}.json"
    )


def _require_hex(value: Any, regex: re.Pattern[str], label: str) -> str:
    if type(value) is not str or regex.fullmatch(value) is None:
        raise ValueError(f"{label} must be exact lowercase hex")
    return value

_HEX32 = re.compile(r"^[0-9a-f]{32}$")


def read_verified_manifest(plan: dict[str, Any], repo_path: str | Path) -> dict[str, Any]:
    controller._validate_immutable_plan(plan)
    binding = plan["receipt_binding"]
    if binding.get("ready") is not True:
        raise ValueError("receipt plane must be bound before Git reconciliation")
    repo = Path(repo_path)
    expected_repo = binding["repository"]
    origin = _normalize_github_repo(_git(repo, "config", "--get", "remote.origin.url"))
    if origin != expected_repo:
        raise ValueError("receipt Git origin does not match the frozen private repository")
    branch = binding["branch"]
    remote_ref = f"refs/remotes/origin/{branch}"
    fetch = _run_git(
        repo, "fetch", "--no-tags", "origin",
        f"refs/heads/{branch}:{remote_ref}", check=False,
    )
    if fetch.returncode != 0:
        raise ValueError(f"fresh receipt branch fetch failed: {fetch.stderr.strip()}")
    head = _git(repo, "rev-parse", remote_ref)
    genesis = _require_hex(binding["genesis_commit"], _HEX40, "receipt genesis commit")
    if _run_git(repo, "cat-file", "-e", f"{genesis}^{{commit}}", check=False).returncode != 0:
        raise ValueError("receipt genesis commit is unavailable in the fresh Git view")
    if _run_git(repo, "merge-base", "--is-ancestor", genesis, head, check=False).returncode != 0:
        raise ValueError("receipt branch head is not a descendant of the bound genesis")

    manifest = {
        "schema": "SD1_CAUSAL_RECEIPT_MANIFEST_V1",
        "repository": expected_repo,
        "branch": branch,
        "run_id": binding["run_id"],
        "genesis_commit": genesis,
        "head_commit": head,
        "receipts": [],
    }
    if head == genesis:
        return manifest
    commits = _git(
        repo, "rev-list", "--reverse", "--first-parent", f"{genesis}..{head}"
    ).splitlines()
    previous_commit = genesis
    previous_record_digest = controller._LEDGER_GENESIS_DIGEST
    for sequence, commit in enumerate(commits, start=1):
        _require_hex(commit, _HEX40, "receipt commit")
        parents = _git(repo, "rev-list", "--parents", "-n", "1", commit).split()
        if len(parents) != 2 or parents[1] != previous_commit:
            raise ValueError("receipt branch must be a strict single-parent append chain")
        changes = [line for line in _git(
            repo, "diff-tree", "--no-commit-id", "--name-status", "-r",
            previous_commit, commit,
        ).splitlines() if line]
        if len(changes) != 1:
            raise ValueError("each receipt commit must add exactly one receipt file")
        status, path = changes[0].split("\t", 1)
        if status != "A":
            raise ValueError("receipt commits may only append new receipt files")

        raw = _git(repo, "show", f"{commit}:{path}")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError("receipt file is not valid JSON") from exc
        if type(payload) is not dict or set(payload) != RECEIPT_PAYLOAD_KEYS:
            raise ValueError("receipt file diverges from the digest-only schema")
        if payload.get("schema") != "SD1_CAUSAL_RECEIPT_V1":
            raise ValueError("receipt schema mismatch")
        if payload.get("run_id") != binding["run_id"]:
            raise ValueError("receipt run id mismatch")
        if payload.get("sequence") != sequence:
            raise ValueError("receipt sequence is not monotonic")
        slot_id = _require_hex(payload.get("slot_id"), _HEX32, "slot id")
        _require_hex(payload.get("response_id"), _HEX32, "response id")
        record_digest = _require_hex(payload.get("record_digest"), _HEX64, "record digest")
        _require_hex(payload.get("runtime_readback_digest"), _HEX64, "runtime readback digest")
        if _require_hex(payload.get("plan_subject_digest"), _HEX64, "plan subject digest") != controller._FROZEN_IMMUTABLE_PLAN_SHA256:
            raise ValueError("receipt plan subject diverges from frozen causal plan")
        previous_digest = _require_hex(
            payload.get("previous_record_digest"), _HEX64, "previous record digest"
        )
        if previous_digest != previous_record_digest:
            raise ValueError("receipt record-digest chain is discontinuous")
        expected_path = _receipt_path(binding["run_id"], sequence, slot_id)
        if path != expected_path:
            raise ValueError("receipt path does not match sequence and slot")
        manifest["receipts"].append(dict(payload, receipt_commit=commit, path=path))
        previous_commit = commit
        previous_record_digest = record_digest
    if previous_commit != head:
        raise ValueError("verified receipt history does not terminate at fetched head")
    return manifest


def record_attempt(
    plan: dict[str, Any], ledger_path: str | Path, slot_id: str,
    record: dict[str, Any], repo_path: str | Path,
) -> dict[str, Any]:
    manifest = read_verified_manifest(plan, repo_path)
    return controller._record_attempt_with_manifest(
        plan, ledger_path, slot_id, record, receipt_manifest=manifest
    )


def append_receipt(
    plan: dict[str, Any], ledger_path: str | Path, repo_path: str | Path,
) -> dict[str, Any]:
    repo = Path(repo_path)
    manifest = read_verified_manifest(plan, repo)
    payload = controller._build_receipt_payload_with_manifest(plan, ledger_path, manifest)
    binding = plan["receipt_binding"]
    path = _receipt_path(binding["run_id"], payload["sequence"], payload["slot_id"])
    with tempfile.TemporaryDirectory() as td:
        worktree = Path(td) / "receipt-worktree"
        _run_git(repo, "worktree", "add", "--detach", str(worktree), manifest["head_commit"])
        try:
            target = worktree / Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
            _run_git(worktree, "add", "--", path)
            staged = _git(worktree, "diff", "--cached", "--name-status").splitlines()
            if staged != [f"A\t{path}"]:
                raise ValueError("receipt worktree contains changes outside the one append")
            _run_git(
                worktree,
                "-c", "user.name=Vera SD1 Causal Receipt",
                "-c", "user.email=vera-sd1-causal@local.invalid",
                "commit", "--no-gpg-sign", "-m",
                f"SD1 causal receipt {payload['sequence']:03d}",
            )
            commit = _git(worktree, "rev-parse", "HEAD")
            parent = _git(worktree, "rev-parse", "HEAD^")
            if parent != manifest["head_commit"]:
                raise ValueError("receipt commit parent moved before publish")
            push = _run_git(
                worktree, "push", "origin",
                f"HEAD:refs/heads/{binding['branch']}", check=False,
            )
            if push.returncode != 0:
                raise ValueError(
                    "non-force receipt publish rejected; reconcile remote frontier before retry"
                )
        finally:
            _run_git(repo, "worktree", "remove", "--force", str(worktree), check=False)
    verified = read_verified_manifest(plan, repo)
    if not verified["receipts"]:
        raise ValueError("receipt publish produced no verified remote receipt")
    last = verified["receipts"][-1]
    for key, value in payload.items():
        if last.get(key) != value:
            raise ValueError("remote receipt readback diverges from the published payload")
    if last.get("receipt_commit") != commit:
        raise ValueError("remote receipt head does not match the published commit")
    return verified


def blinded_export(
    plan: dict[str, Any], ledger_path: str | Path, repo_path: str | Path,
) -> list[dict[str, Any]]:
    manifest = read_verified_manifest(plan, repo_path)
    return controller._blinded_export_with_manifest(
        plan, ledger_path, receipt_manifest=manifest
    )


__all__ = [
    "RECEIPT_PAYLOAD_KEYS",
    "read_verified_manifest",
    "record_attempt",
    "append_receipt",
    "blinded_export",
]
