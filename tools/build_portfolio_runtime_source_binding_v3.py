#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERA_CUT = ROOT / "governance/vendor/vera/VERA_PORTFOLIO_PUBLIC_CUT_V2.json"
VERA_ABSORPTION = ROOT / "governance/vendor/vera/VERA_PORTFOLIO_ABSORPTION_V2.json"
PREDECESSOR_V2 = ROOT / "governance/vendor/vcp/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V2.json"
OUTPUT = ROOT / "governance/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3.json"

VERA_PR = 206
VERA_HEAD = "be3d11a5b4d3a9880c18e03522f0d4e341b71f99"
CUT_BLOB = "19c20a5fceae81f3324d477317f1ec79062cd9f2"
ABSORPTION_BLOB = "15499b3a8f3b4d5033a4cf8e0d6a1953c2826cb9"
PREDECESSOR_VCP_PR = 134
PREDECESSOR_VCP_HEAD = "eb96ff92f6aadd158124a7d20fa81a594e2ae87a"
PREDECESSOR_V2_BLOB = "9e6cf5244898e0a6fb85ffabbd52df6fdef8bc65"
REVIEW_PR = 95
REVIEW_HEAD = "c8d97b14b20b653178dbc079c8f2943fecbc3c34"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def disposition(module, predecessor):
    old = predecessor.get(module["source_repository"])
    activation = module["source_activation_mode"]
    if module["source_role"] == "PREDECESSOR_SOURCE" or old == "PREDECESSOR_EVIDENCE_ONLY":
        return "PREDECESSOR_EVIDENCE_ONLY"
    if activation in {"NO_AUTO_BIND", "NO_IDENTITY_TRANSFER"} or old == "NO_AUTO_BIND":
        return "NO_AUTO_BIND"
    return "BOUND_CONDITIONAL"

def effective_rule(value: str) -> str:
    if value == "NO_AUTO_BIND":
        return "NO_AUTO_BIND"
    if value == "PREDECESSOR_EVIDENCE_ONLY":
        return "EVIDENCE_ONLY_NEVER_CURRENT_CONTROL"
    return "TASK_RELEVANCE_AND_FRESH_CURRENTNESS_REQUIRED"

cut = load(VERA_CUT)
absorption = load(VERA_ABSORPTION)
predecessor = load(PREDECESSOR_V2)
old = {row["repository"]: row["runtime_source_disposition"] for row in predecessor["public_sources"]}
refresh = {row["repository"]: row["observed_head"] for row in cut["public_head_refresh"]["heads"]}
records = {row["repository"]: row for row in cut["public_records"]}

assert cut["cut_counts"]["public"] == len(records) == 49
assert absorption["portfolio_cut"]["public_modules"] == len(absorption["modules"]) == 49
assert set(records) == {row["source_repository"] for row in absorption["modules"]}
assert set(records) == set(refresh)
public_sources = []
for module in absorption["modules"]:
    repo = module["source_repository"]
    assert module["source_evidence_commit"] == refresh[repo]
    value = disposition(module, old)
    public_sources.append({
        "repository": repo,
        "observed_head": module["source_evidence_commit"],
        "source_activation_mode": module["source_activation_mode"],
        "runtime_source_disposition": value,
        "predecessor_v2_disposition": old.get(repo),
        "availability_implies_activation": False,
        "source_authority_ceiling": module["source_authority_ceiling"],
        "vcp_effective_rule": effective_rule(value),
    })

binding = {
    "schema": "VCP_VERA_RUNTIME_SOURCE_BINDING_V3",
    "status": "EXACT_PR206_PUBLIC_SAFE_BINDING_NOT_RUNTIME_AUTHORITY",
    "vcp_repository": "thebrazenbeard/vera-control-plane",
    "upstream": {
        "repository": "thebrazenbeard/vera",
        "pull_request": VERA_PR,
        "head": VERA_HEAD,
        "public_cut_path": "architecture/portfolio/VERA_PORTFOLIO_PUBLIC_CUT_V2.json",
        "public_cut_blob_sha": CUT_BLOB,
        "absorption_path": "architecture/portfolio/VERA_PORTFOLIO_ABSORPTION_V2.json",
        "absorption_blob_sha": ABSORPTION_BLOB,
    },
    "qualification": {
        "repository": "thebrazenbeard/rezon",
        "pull_request": REVIEW_PR,
        "head": REVIEW_HEAD,
        "review_path": "docs/assurance/VERA_PR206_PUBLIC_SUCCESSOR_HOSTILE_REVIEW.md",
        "disposition": "SURVIVES_NARROWED_PUBLIC_SAFE_SUCCESSOR",
    },
    "predecessor_vcp": {
        "pull_request": PREDECESSOR_VCP_PR,
        "head": PREDECESSOR_VCP_HEAD,
        "binding_blob_sha": PREDECESSOR_V2_BLOB,
        "rule": "NO_AUTO_BIND and predecessor restrictions are a fail-closed floor; PR206 may make a source more restrictive but never less restrictive by packaging alone.",
    },
    "cut_counts": cut["cut_counts"],
    "cardinality_semantics": "CUT_LOCAL_FACTS_ONLY_NOT_PERMANENT_POLICY_INVARIANTS",
    "private_inventory": {
        "count": cut["private_inventory"]["count"],
        "public_commitment_scheme": cut["private_inventory"]["public_commitment_scheme"],
        "exact_membership_publicly_committed": False,
        "membership_names_present": False,
        "public_runtime_rule": "NO_AUTO_BIND_FROM_PUBLIC_INVENTORY; PRIVATE_EXACT_BINDING_REQUIRED_ON_A_PRIVATE_AUTHORIZED_SURFACE",
    },
    "public_sources": public_sources,
    "enforcement": {
        "disposition_domain": ["BOUND_CONDITIONAL", "NO_AUTO_BIND", "PREDECESSOR_EVIDENCE_ONLY"],
        "prohibited_load_modes_for_no_auto_bind": ["CONTROL_LOAD_EXACT_OWNER", "LIVE_COORDINATION_READ", "TASK_RELEVANT_LIVE_READ"],
        "bound_conditional_auto_bind": False,
        "no_auto_bind_auto_bind": False,
        "predecessor_auto_bind": False,
        "outside_cut": {"status": "UNRESOLVED", "auto_bind_allowed": False, "rule": "NO_AUTO_BIND_UNTIL_NEWER_EXACT_PUBLIC_CUT_OR_EXPLICIT_AUTHORIZED_BINDING"},
        "private_without_exact_private_binding": {"status": "PRIVATE_EXACT_BINDING_REQUIRED", "auto_bind_allowed": False},
        "freshness": {"mutable_head_use": "REFRESH_REQUIRED_BEFORE_MATERIAL_RUNTIME_USE", "head_drift": "INVALIDATES_UNREFRESHED_CURRENTNESS_CLAIM_NOT_IMMUTABLE_CUT", "membership_drift": "REQUIRES_NEWER_EXACT_CUT"},
    },
    "non_implications": ["EXACT_SOURCE_BINDING_NE_RUNTIME_ACTIVATION", "BOUND_CONDITIONAL_NE_AUTO_BIND", "REPOSITORY_PRESENCE_NE_AUTHORITY", "PUBLIC_CUT_NE_PRIVATE_MEMBERSHIP_DISCLOSURE", "SOURCE_QUALIFICATION_NE_PROJECT_INSTALL", "SOURCE_QUALIFICATION_NE_PROTECTED_EFFECT_AUTHORITY"],
}
OUTPUT.write_text(json.dumps(binding, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"public_sources": len(public_sources), "no_auto_bind": sum(1 for r in public_sources if r["runtime_source_disposition"] == "NO_AUTO_BIND"), "predecessor": sum(1 for r in public_sources if r["runtime_source_disposition"] == "PREDECESSOR_EVIDENCE_ONLY")}, indent=2))
