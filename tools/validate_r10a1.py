#!/usr/bin/env python3
"""Repo-local static/source validator for the frozen R10A1 candidate.

Run from the repository root at the exact candidate receipt head:
    python tools/validate_r10a1.py

Uses only Python stdlib plus the local git executable. No GitHub Actions runner
or external paid service is required.
"""

import hashlib
import json
import subprocess
from pathlib import Path

BASE = "2d60cd8e87ac0aae89a5a9bd9a44bfb63f48aa64"
ROOT = Path(__file__).resolve().parents[1]
R10A0_PREFIX = "project-instructions/r10a0/"


def git(*args: str, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True
    )
    if check and proc.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed ({proc.returncode}): {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def blob(path: Path) -> str:
    return git("hash-object", str(path.relative_to(ROOT)))


def intro_commit(path: Path) -> str:
    out = git(
        "log",
        "--diff-filter=A",
        "--format=%H",
        "--reverse",
        "--",
        str(path.relative_to(ROOT)),
    ).splitlines()
    assert out, f"no introduction commit for {path}"
    return out[0]


def validate_base_and_predecessor() -> None:
    git("cat-file", "-e", f"{BASE}^{{commit}}")
    rc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=ROOT
    ).returncode
    assert rc == 0, f"{BASE} is not an ancestor of HEAD"
    changed = git("diff", "--name-only", f"{BASE}...HEAD").splitlines()
    bad = [p for p in changed if p.startswith(R10A0_PREFIX)]
    assert not bad, f"R10A0 predecessor path changed in R10A1 candidate: {bad}"


def validate_contract() -> None:
    r = ROOT / "project-instructions" / "r10a1"
    required = {
        "regression": r / "VERA_R10A1_SALIENCE_REGRESSION.md",
        "baseline": r / "VERA_R10A1_BASELINE_RED.md",
        "owner": r / "VERA_R10A1_SALIENCE_ARBITRATION.md",
        "native_delta": r / "VERA_R10A1_NATIVE_DELTA.txt",
        "native": r / "VERA_R10A1_NATIVE_PROJECT_INSTRUCTIONS.txt",
        "registry": r / "VERA_R10A1_CONTROL_REGISTRY.json",
        "manifest": r / "VERA_R10A1_PROJECT_SOURCE_MANIFEST.json",
        "freeze": r / "VERA_R10A1_CANDIDATE_FREEZE.json",
        "receipt": r / "VERA_R10A1_PUBLICATION_RECEIPT.json",
    }
    missing = [str(p) for p in required.values() if not p.is_file()]
    assert not missing, f"missing implementation artifacts: {missing}"

    regression = required["regression"].read_text(encoding="utf-8")
    baseline = required["baseline"].read_text(encoding="utf-8")
    owner = required["owner"].read_text(encoding="utf-8")
    delta = required["native_delta"].read_text(encoding="utf-8")
    native = required["native"].read_text(encoding="utf-8")

    case_ids = [
        "SAL-CORR-1",
        "SAL-ACT-1",
        "SAL-LOCAL-1",
        "SAL-TECH-1",
        "SAL-PROV-1",
        "SAL-SELF-1",
        "SAL-CAUSE-1",
        "SAL-BOUND-1",
        "SAL-COMPOSE-1",
    ]
    for cid in case_ids:
        assert cid in regression, f"missing frozen case {cid}"
    assert "first eligible behavior" in regression.lower()
    assert "5/5" in regression
    assert "automatic inversion" in regression.lower() or "unsupported anti" in regression.lower()
    assert "R10A0_FIRST_ELIGIBLE_BEHAVIOR_CAUSALITY = FAIL_ON_OBSERVED_CASES" in baseline

    required_owner_terms = [
        "SALIENCE_ARBITRATION",
        "CORRECTION_INTERRUPT",
        "EXACT_PROPOSITION",
        "ACTIONABILITY",
        "LOCAL_CONTEXT_ARBITRATION",
        "PROVENANCE_UNCERTAINTY",
        "SELF_RELATIONAL_COMPOSITION",
        "old_claim",
        "corrected_scope",
        "invalidated_dependents",
        "surviving_claims",
        "newly_unknown_fields",
        "corrected_target",
        "first eligible behavior",
    ]
    for term in required_owner_terms:
        assert term.lower() in owner.lower(), f"owner missing {term}"
    assert "surface-marker quota" in owner.lower() or "surface marker" in owner.lower()
    assert "platform" in owner.lower() and "authority" in owner.lower()
    assert "relational > technical" in owner.lower() or "blanket" in owner.lower()

    required_delta_terms = [
        "SALIENCE_ARBITRATION",
        "correction",
        "action",
        "local",
        "provenance",
        "self/relationship",
        "authority",
    ]
    for term in required_delta_terms:
        assert term.lower() in delta.lower(), f"native delta missing {term}"
    assert len(delta.encode("utf-8")) <= 900, "native delta is not minimal"

    native_bytes = len(native.encode("utf-8"))
    assert native_bytes <= 8000, f"native Project Instructions exceed 8000 bytes: {native_bytes}"
    assert "VERA UNBOUND — NATIVE R10A1" in native
    assert "SALIENCE_ARBITRATION" in native
    assert "ROOT:R10A1" in native

    registry = json.loads(required["registry"].read_text(encoding="utf-8"))
    manifest = json.loads(required["manifest"].read_text(encoding="utf-8"))
    freeze = json.loads(required["freeze"].read_text(encoding="utf-8"))
    receipt = json.loads(required["receipt"].read_text(encoding="utf-8"))

    assert registry["release"] == "R10A1"
    assert registry["base_r10a0_main"] == BASE
    assert registry["controls"]["SALIENCE_ARBITRATION"]["owner"] == "SALIENCE_ARBITRATION_OWNER"
    assert manifest["release"] == "R10A1"
    assert manifest["base_r10a0_main"] == registry["base_r10a0_main"]

    actual = {
        name: blob(path)
        for name, path in required.items()
        if name not in {"freeze", "receipt"}
    }
    assert registry["owners"]["SALIENCE_ARBITRATION_OWNER"]["git_blob"] == actual["owner"]
    assert registry["qualification"]["salience_regression_blob"] == actual["regression"]
    assert manifest["artifacts"]["salience_owner"]["git_blob"] == actual["owner"]
    assert manifest["artifacts"]["salience_regression"]["git_blob"] == actual["regression"]
    assert manifest["artifacts"]["native_delta"]["git_blob"] == actual["native_delta"]
    assert manifest["artifacts"]["control_registry"]["git_blob"] == actual["registry"]

    manifest_sha = hashlib.sha256(required["manifest"].read_bytes()).hexdigest()
    assert manifest_sha in native, "native does not pin exact R10A1 manifest SHA-256"
    assert freeze["source_manifest_sha256"] == manifest_sha
    assert receipt["source_manifest"]["sha256"] == manifest_sha
    assert receipt["source_manifest"]["git_blob"] == actual["manifest"]
    assert receipt["freeze_descriptor"]["git_blob"] == blob(required["freeze"])
    assert receipt["cross_bind"]["salience_owner_blob"] == actual["owner"]
    assert receipt["cross_bind"]["salience_regression_blob"] == actual["regression"]
    assert receipt["cross_bind"]["control_registry_blob"] == actual["registry"]
    assert receipt["cross_bind"]["native_blob"] == actual["native"]

    core_names = ["regression", "baseline", "owner", "native_delta", "native", "registry"]
    records = []
    for name in core_names:
        path = required[name].relative_to(ROOT).as_posix()
        records.append(path.encode() + b"\0" + actual[name].encode() + b"\n")
    records.sort()
    records.append(b"manifest_sha256\0" + manifest_sha.encode() + b"\n")
    core = hashlib.sha256(b"".join(records)).hexdigest()
    assert freeze["candidate_core_sha256"] == core
    assert receipt["candidate_core_sha256"] == core

    assert "runtime qualified" not in owner.lower()
    assert receipt["status"] == "IMMUTABLE_PUBLICATION_BINDING_SOURCE_ONLY_NOT_INSTALLED_NOT_RUNTIME_QUALIFIED"
    assert "not BugOps closure" in receipt["non_effects"]

    regression_intro = intro_commit(required["regression"])
    owner_intro = intro_commit(required["owner"])
    rc = subprocess.run(
        ["git", "merge-base", "--is-ancestor", regression_intro, owner_intro], cwd=ROOT
    ).returncode
    assert rc == 0 and regression_intro != owner_intro, "regression must be committed before owner implementation"

    parents = git("rev-list", "--parents", "-n", "1", "HEAD").split()
    assert len(parents) == 2, "receipt review head must have exactly one parent"
    pre_commit = parents[1]
    pre_tree = git("show", "-s", "--format=%T", pre_commit)
    assert receipt["pre_receipt_publication_subject"]["commit"] == pre_commit
    assert receipt["pre_receipt_publication_subject"]["tree"] == pre_tree

    print("R10A1 static/source validation PASS")
    print(f"native_bytes={native_bytes}")
    print(f"manifest_sha256={manifest_sha}")
    print(f"candidate_core_sha256={core}")
    print(f"pre_receipt_commit={pre_commit}")
    print(f"pre_receipt_tree={pre_tree}")


def main() -> int:
    validate_base_and_predecessor()
    validate_contract()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
