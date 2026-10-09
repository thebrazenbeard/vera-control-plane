#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3.json"
CUT = ROOT / "governance/vendor/vera/VERA_PORTFOLIO_PUBLIC_CUT_V2.json"
ABSORPTION = ROOT / "governance/vendor/vera/VERA_PORTFOLIO_ABSORPTION_V2.json"
PREDECESSOR = ROOT / "governance/vendor/vcp/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V2.json"
CAPABILITY = ROOT / "governance/VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"

SHA40 = re.compile(r"^[0-9a-f]{40}$")
DISPOSITIONS = {"BOUND_CONDITIONAL", "NO_AUTO_BIND", "PREDECESSOR_EVIDENCE_ONLY"}
PROHIBITED = {"CONTROL_LOAD_EXACT_OWNER", "LIVE_COORDINATION_READ", "TASK_RELEVANT_LIVE_READ"}
VERA_HEAD = "dff171a8cee0b2dd3c6fd4627499330800499fdd"
REVIEW_HEAD = "d22abc8f7b4649ca0b9e21e77673f263283d98bf"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()

def expected_disposition(module, predecessor: str | None) -> str:
    if module["source_role"] == "PREDECESSOR_SOURCE" or predecessor == "PREDECESSOR_EVIDENCE_ONLY":
        return "PREDECESSOR_EVIDENCE_ONLY"
    if module["source_activation_mode"] in {"NO_AUTO_BIND", "NO_IDENTITY_TRANSFER"}:
        return "NO_AUTO_BIND"
    if predecessor == "NO_AUTO_BIND":
        return "NO_AUTO_BIND"
    return "BOUND_CONDITIONAL"

def effective_rule(value: str) -> str:
    if value == "NO_AUTO_BIND":
        return "NO_AUTO_BIND"
    if value == "PREDECESSOR_EVIDENCE_ONLY":
        return "EVIDENCE_ONLY_NEVER_CURRENT_CONTROL"
    return "TASK_RELEVANCE_AND_FRESH_CURRENTNESS_REQUIRED"

def validate(data: Mapping[str, object], capability: Mapping[str, object]) -> list[str]:
    errors: list[str] = []
    cut = load(CUT)
    absorption = load(ABSORPTION)
    predecessor = load(PREDECESSOR)
    if data.get("schema") != "VCP_VERA_RUNTIME_SOURCE_BINDING_V3":
        errors.append("schema mismatch")
    if data.get("status") != "EXACT_PR206_PUBLIC_SAFE_BINDING_NOT_RUNTIME_AUTHORITY":
        errors.append("status mismatch")
    upstream = data.get("upstream")
    if not isinstance(upstream, Mapping) or upstream.get("pull_request") != 206 or upstream.get("head") != VERA_HEAD:
        errors.append("exact Vera PR206 binding mismatch")
    qualification = data.get("qualification")
    if not isinstance(qualification, Mapping) or qualification.get("pull_request") != 95 or qualification.get("head") != REVIEW_HEAD:
        errors.append("exact Rezon qualification binding mismatch")
    if not isinstance(upstream, Mapping) or upstream.get("public_cut_blob_sha") != git_blob_sha(CUT):
        errors.append("vendored Vera cut blob mismatch")
    if not isinstance(upstream, Mapping) or upstream.get("absorption_blob_sha") != git_blob_sha(ABSORPTION):
        errors.append("vendored Vera absorption blob mismatch")
    counts = data.get("cut_counts")
    sources = data.get("public_sources")
    private = data.get("private_inventory")
    if counts != cut.get("cut_counts"):
        errors.append("cut counts diverge from vendored Vera cut")
    if not isinstance(sources, list):
        return errors + ["public_sources missing"]
    cut_rows = {row["repository"]: row for row in cut["public_records"]}
    modules = {row["source_repository"]: row for row in absorption["modules"]}
    refresh = {row["repository"]: row["observed_head"] for row in cut["public_head_refresh"]["heads"]}
    if set(cut_rows) != set(modules) or set(cut_rows) != set(refresh):
        errors.append("vendored Vera cut/absorption membership mismatch")
    if {row.get("repository") for row in sources} != set(cut_rows):
        errors.append("VCP public source membership does not exactly match Vera cut")
    if not isinstance(private, Mapping):
        errors.append("private inventory missing")
    else:
        if private.get("count") != cut["private_inventory"]["count"]:
            errors.append("private count mismatch")
        if private.get("public_commitment_scheme") != "COUNT_ONLY_PUBLIC_V1":
            errors.append("private inventory is not count-only")
        if private.get("exact_membership_publicly_committed") is not False:
            errors.append("private exact membership must remain absent")
        if private.get("membership_names_present") is not False:
            errors.append("private membership names must remain absent")
        for key in ("repositories", "members", "names"):
            if key in private:
                errors.append(f"private inventory leaks membership via {key}")
    old = {row["repository"]: row["runtime_source_disposition"] for row in predecessor["public_sources"]}
    cap_repos = capability.get("repositories", {}) if isinstance(capability, Mapping) else {}
    legacy_binding = capability.get("runtime_source_registry_binding", {}) if isinstance(capability, Mapping) else {}
    if not isinstance(legacy_binding, Mapping):
        errors.append("capability legacy runtime source registry binding missing")
    else:
        if legacy_binding.get("status") != "SUPERSEDED_HISTORICAL_EVIDENCE_ONLY":
            errors.append("legacy runtime source registry remains activation authority")
        if legacy_binding.get("legacy_semantics") != "HISTORICAL_EVIDENCE_ONLY_NOT_ACTIVATION_AUTHORITY":
            errors.append("legacy runtime source registry semantics mismatch")
        activation = legacy_binding.get("activation_authority")
        if not isinstance(activation, Mapping):
            errors.append("capability V3 activation authority missing")
        else:
            if activation.get("status") != "CURRENT_V3_BINDING":
                errors.append("capability V3 activation status mismatch")
            if activation.get("repository") != "thebrazenbeard/vera-control-plane":
                errors.append("capability V3 activation repository mismatch")
            if activation.get("path") != "governance/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3.json":
                errors.append("capability V3 activation path mismatch")
            if activation.get("binding_blob_sha") != git_blob_sha(BINDING):
                errors.append("capability V3 activation blob mismatch")
            if activation.get("upstream_vera_head") != VERA_HEAD:
                errors.append("capability V3 activation Vera head mismatch")
            if activation.get("qualification_rezon_head") != REVIEW_HEAD:
                errors.append("capability V3 activation Rezon head mismatch")
            if activation.get("semantics") != "V3_GOVERNS_ACTIVATION; LEGACY_REGISTRY_HISTORICAL_ONLY":
                errors.append("capability V3 activation semantics mismatch")
    for row in sources:
        if not isinstance(row, Mapping):
            errors.append("public source row is not an object")
            continue
        repo = row.get("repository")
        module = modules.get(repo)
        if module is None:
            errors.append(f"{repo}: missing Vera absorption module")
            continue
        if row.get("observed_head") != module["source_evidence_commit"] or row.get("observed_head") != refresh[repo]:
            errors.append(f"{repo}: exact head mismatch")
        if not isinstance(row.get("observed_head"), str) or SHA40.fullmatch(row["observed_head"]) is None:
            errors.append(f"{repo}: observed head is not exact 40-hex")
        if row.get("source_activation_mode") != module["source_activation_mode"]:
            errors.append(f"{repo}: activation mode mismatch")
        expected = expected_disposition(module, old.get(repo))
        if row.get("runtime_source_disposition") != expected:
            errors.append(f"{repo}: fail-closed disposition mismatch")
        if row.get("vcp_effective_rule") != effective_rule(expected):
            errors.append(f"{repo}: effective rule mismatch")
        if row.get("availability_implies_activation") is not False:
            errors.append(f"{repo}: availability must not imply activation")
        key = repo.split("/", 1)[1]
        cap = cap_repos.get(key, {}) if isinstance(cap_repos, Mapping) else {}
        if expected == "NO_AUTO_BIND" and isinstance(cap, Mapping) and cap.get("load_mode") in PROHIBITED:
            errors.append(f"{repo}: NO_AUTO_BIND source cannot use VCP load mode {cap.get('load_mode')}")
    enforcement = data.get("enforcement")
    if not isinstance(enforcement, Mapping):
        errors.append("enforcement missing")
    else:
        if set(enforcement.get("disposition_domain", [])) != DISPOSITIONS:
            errors.append("disposition domain mismatch")
        if set(enforcement.get("prohibited_load_modes_for_no_auto_bind", [])) != PROHIBITED:
            errors.append("prohibited load-mode set mismatch")
        for key in ("bound_conditional_auto_bind", "no_auto_bind_auto_bind", "predecessor_auto_bind"):
            if enforcement.get(key) is not False:
                errors.append(f"{key} must remain false")
    return errors

def runtime_source_disposition(data: Mapping[str, object], repository: str, *, current_head: str | None = None, private_source: bool = False):
    if private_source:
        return {"status": "PRIVATE_EXACT_BINDING_REQUIRED", "auto_bind_allowed": False}
    rows = data.get("public_sources", [])
    row = next((item for item in rows if isinstance(item, Mapping) and item.get("repository") == repository), None) if isinstance(rows, list) else None
    if row is None:
        return {"status": "UNRESOLVED", "auto_bind_allowed": False}
    if current_head is not None and current_head != row.get("observed_head"):
        return {"status": "STALE_CURRENTNESS", "source_disposition": row.get("runtime_source_disposition"), "auto_bind_allowed": False}
    return {"status": row.get("runtime_source_disposition"), "auto_bind_allowed": False}

def main() -> int:
    data = load(BINDING)
    capability = load(CAPABILITY)
    errors = validate(data, capability)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(json.dumps({"status": "PASS", "public_sources": len(data["public_sources"]), "no_auto_bind": sum(1 for row in data["public_sources"] if row["runtime_source_disposition"] == "NO_AUTO_BIND")}, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
