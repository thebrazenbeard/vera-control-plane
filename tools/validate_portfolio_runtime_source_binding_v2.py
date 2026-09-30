#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V2.json"
CAPABILITY_REGISTRY = ROOT / "governance" / "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"

EXPECTED_SCHEMA = "VCP_VERA_RUNTIME_SOURCE_BINDING_V2"
EXPECTED_STATUS = "EXACT_PUBLIC_SAFE_VERA_SOURCE_BINDING_NOT_RUNTIME_AUTHORITY"
EXPECTED_UPSTREAM = {
    "repository": "thebrazenbeard/vera",
    "pull_request": 203,
    "head": "bc5f1f2b5764455d833615d14e3bead640d6d123",
    "registry_path": "architecture/VERA_RUNTIME_SOURCE_REGISTRY_V2.json",
    "registry_blob_sha": "427fe21437a3397e184a5b5373fd4ea10f58123c",
    "registry_schema": "VERA_RUNTIME_SOURCE_REGISTRY_V2",
    "public_cut_path": "architecture/portfolio/VERA_PORTFOLIO_PUBLIC_CUT_V2.json",
    "public_cut_blob_sha": "cbd1e2d659f9fa9eeb9b2fdb7f9e167e16105b22",
    "predecessor_pr200_head": "078d2d7242384c58676305d47654406713e599cf",
    "predecessor_vcp_pr131_head": "a2ce761d3de0adf0cba5c64f53103f97ef48569e",
}
DISPOSITIONS = {
    "BOUND_CONDITIONAL",
    "NO_AUTO_BIND",
    "PREDECESSOR_EVIDENCE_ONLY",
}
PROHIBITED_NO_AUTO_BIND_LOAD_MODES = {
    "CONTROL_LOAD_EXACT_OWNER",
    "LIVE_COORDINATION_READ",
    "TASK_RELEVANT_LIVE_READ",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")


def _repo_key(repository: str) -> str:
    return repository.split("/", 1)[1]


def validate(data: Mapping[str, object], capability: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    if data.get("schema") != EXPECTED_SCHEMA:
        errors.append("schema mismatch")
    if data.get("status") != EXPECTED_STATUS:
        errors.append("status mismatch")
    if data.get("upstream") != EXPECTED_UPSTREAM:
        errors.append("exact Vera V2 upstream binding mismatch")
    if data.get("cardinality_semantics") != (
        "CUT_LOCAL_FACTS_ONLY_NOT_PERMANENT_POLICY_INVARIANTS"
    ):
        errors.append("cardinality semantics mismatch")

    counts = data.get("cut_counts")
    private = data.get("private_inventory")
    sources = data.get("public_sources")
    if not isinstance(counts, Mapping):
        errors.append("cut_counts missing")
        return errors
    if not isinstance(private, Mapping):
        errors.append("private_inventory missing")
        return errors
    if not isinstance(sources, list) or not sources:
        errors.append("public_sources must be non-empty")
        return errors

    public_count = counts.get("public")
    private_count = counts.get("private")
    total_count = counts.get("total")
    if public_count != len(sources):
        errors.append("public cut count does not match exact source rows")
    if (
        not isinstance(public_count, int)
        or not isinstance(private_count, int)
        or not isinstance(total_count, int)
        or total_count != public_count + private_count
    ):
        errors.append("cut count partition is invalid")

    if private.get("count") != private_count:
        errors.append("private count does not match cut")
    if private.get("public_commitment_scheme") != "COUNT_ONLY_PUBLIC_V1":
        errors.append("private inventory is not count-only")
    if private.get("exact_membership_publicly_committed") is not False:
        errors.append("private membership must not be publicly committed")
    if private.get("membership_names_present") is not False:
        errors.append("private membership names must be absent")
    for forbidden_key in ("repositories", "members", "names"):
        if forbidden_key in private:
            errors.append(f"private inventory leaks membership via {forbidden_key}")

    repositories: set[str] = set()
    capability_repos = capability.get("repositories", {})
    if not isinstance(capability_repos, Mapping):
        capability_repos = {}

    for row in sources:
        if not isinstance(row, Mapping):
            errors.append("public source row is not an object")
            continue
        repository = row.get("repository")
        if not isinstance(repository, str) or not repository.startswith("thebrazenbeard/"):
            errors.append("public source repository is invalid")
            continue
        if repository in repositories:
            errors.append(f"duplicate public source: {repository}")
        repositories.add(repository)

        head = row.get("observed_head")
        if not isinstance(head, str) or SHA40.fullmatch(head) is None:
            errors.append(f"{repository}: observed head is not exact 40-hex")

        disposition = row.get("runtime_source_disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"{repository}: disposition outside finite domain")
        if row.get("availability_implies_activation") is not False:
            errors.append(f"{repository}: availability must not imply activation")

        effective = row.get("vcp_effective_rule")
        if disposition == "NO_AUTO_BIND" and effective != "NO_AUTO_BIND":
            errors.append(f"{repository}: NO_AUTO_BIND effective rule mismatch")
        if (
            disposition == "PREDECESSOR_EVIDENCE_ONLY"
            and effective != "EVIDENCE_ONLY_NEVER_CURRENT_CONTROL"
        ):
            errors.append(f"{repository}: predecessor effective rule mismatch")
        if (
            disposition == "BOUND_CONDITIONAL"
            and effective != "TASK_RELEVANCE_AND_FRESH_CURRENTNESS_REQUIRED"
        ):
            errors.append(f"{repository}: bound-conditional rule mismatch")

        cap = capability_repos.get(_repo_key(repository))
        if isinstance(cap, Mapping) and disposition == "NO_AUTO_BIND":
            mode = cap.get("load_mode")
            if mode in PROHIBITED_NO_AUTO_BIND_LOAD_MODES:
                errors.append(
                    f"{repository}: NO_AUTO_BIND source cannot use VCP load mode {mode}"
                )

    enforcement = data.get("enforcement")
    if not isinstance(enforcement, Mapping):
        errors.append("enforcement missing")
        return errors
    if set(enforcement.get("disposition_domain", [])) != DISPOSITIONS:
        errors.append("disposition domain mismatch")
    if set(enforcement.get("prohibited_load_modes_for_no_auto_bind", [])) != (
        PROHIBITED_NO_AUTO_BIND_LOAD_MODES
    ):
        errors.append("NO_AUTO_BIND prohibited load-mode set mismatch")
    for key in (
        "bound_conditional_auto_bind",
        "no_auto_bind_auto_bind",
        "predecessor_auto_bind",
    ):
        if enforcement.get(key) is not False:
            errors.append(f"{key} must remain false")
    outside = enforcement.get("outside_cut", {})
    if (
        not isinstance(outside, Mapping)
        or outside.get("status") != "UNRESOLVED"
        or outside.get("auto_bind_allowed") is not False
    ):
        errors.append("outside-cut policy must fail closed")
    private_rule = enforcement.get("private_without_exact_private_binding", {})
    if (
        not isinstance(private_rule, Mapping)
        or private_rule.get("status") != "PRIVATE_EXACT_BINDING_REQUIRED"
        or private_rule.get("auto_bind_allowed") is not False
    ):
        errors.append("private-source public policy must require exact private binding")

    return errors


def runtime_source_disposition(
    data: Mapping[str, object],
    repository: str,
    *,
    current_head: str | None = None,
    private_source: bool = False,
) -> dict[str, object]:
    """Resolve public binding without promoting presence into runtime authority."""
    if private_source:
        return {
            "status": "PRIVATE_EXACT_BINDING_REQUIRED",
            "auto_bind_allowed": False,
            "reason": "public V2 binding intentionally contains no private membership",
        }

    rows = data.get("public_sources", [])
    if not isinstance(rows, list):
        return {
            "status": "UNRESOLVED",
            "auto_bind_allowed": False,
            "reason": "public source binding is unavailable",
        }
    row = next(
        (
            item
            for item in rows
            if isinstance(item, Mapping) and item.get("repository") == repository
        ),
        None,
    )
    if row is None:
        return {
            "status": "UNRESOLVED",
            "auto_bind_allowed": False,
            "reason": "repository is outside the exact public cut",
        }

    observed_head = row.get("observed_head")
    if current_head is not None and current_head != observed_head:
        return {
            "status": "STALE_CURRENTNESS",
            "source_disposition": row.get("runtime_source_disposition"),
            "auto_bind_allowed": False,
            "observed_head": observed_head,
            "current_head": current_head,
            "reason": "mutable source moved after the immutable cut observation",
        }

    return {
        "status": row.get("runtime_source_disposition"),
        "auto_bind_allowed": False,
        "observed_head": observed_head,
        "reason": row.get("vcp_effective_rule"),
    }


def main() -> int:
    data = json.loads(BINDING.read_text(encoding="utf-8"))
    capability = json.loads(CAPABILITY_REGISTRY.read_text(encoding="utf-8"))
    errors = validate(data, capability)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: VCP public-safe Vera runtime source binding V2")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
