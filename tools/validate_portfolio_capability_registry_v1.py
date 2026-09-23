#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"

EXPECTED_SCHEMA = "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1"
EXPECTED_STATUS = "PRIVATE_ROUTING_SNAPSHOT_NOT_CONTROL_AUTHORITY"
EXPECTED_RUNTIME_SOURCE = {
    "repository": "thebrazenbeard/vera",
    "commit": "86be6105f13fc86bbd699778205a85c84059de9a",
    "path": "architecture/VERA_RUNTIME_SOURCE_REGISTRY_V1.json",
    "blob_sha": "9afe5834efaf4d8a2d73c5864972e4c8e4c3cef6",
}
EXPECTED_DISCOVERY = {
    "repository": "thebrazenbeard/discovery",
    "commit": "2881a94c7eb3c83a34b0c00bab739b41c1d99b6d",
    "path": "architecture/DISCOVERY_LIVE_PORTFOLIO_MAP_V2.json",
    "blob_sha": "71b9f8deaf1079d5078b19e5bbddb743fd636437",
}
EXPECTED_ROOTS = {
    "repository": "thebrazenbeard/roots",
    "commit": "a6994b415336bc179a41aad0ac9eec403d60f93c",
    "path": "portfolio/VERA_PORTFOLIO_LINEAGE_RECEIPT_V1.json",
    "blob_sha": "ccac62eac08012269fec46669bce981b96a0f41d",
}
EXPECTED_BUS_TOPOLOGY = {
    "repository": "thebrazenbeard/chat-communication-bus",
    "commit": "f9179bd1426bf90c23ab6a4d14d5a8e9b39c66d2",
    "path": "architecture/contracts/RADAR_TOPOLOGY_V1.json",
    "blob_sha": "69e505031d4e53dcb853578dac23817649af1918",
}
EXPECTED_REPOSITORY_DIGEST = "f96f479f1d85508ff4e57bf242b7850f9f755763953ebb3f280c5716a090f4df"
EXPECTED_NO_AUTO_BIND = {
    "brigit",
    "brigit-unbound",
    "bt2",
    "conditioning",
    "entropyinc",
    "firesafe",
    "hc-brain",
    "hephaestus",
    "masamune",
    "mediaphile",
    "project-lantern",
    "self",
    "trek-data-core",
    "vera-apk",
    "vera-habitat",
    "vera-works",
    "wreckforge",
}
NO_AUTO_BIND_PROHIBITED_LOAD_MODES = {
    "CONTROL_LOAD_EXACT_OWNER",
    "LIVE_COORDINATION_READ",
    "TASK_RELEVANT_LIVE_READ",
}
EXPECTED_RULES = {
    "LIVE_CURRENTNESS_REQUIRED_BEFORE_MATERIAL_USE",
    "REGISTRY_ROLE_NE_REPOSITORY_AUTHORITY",
    "REPOSITORY_PRESENCE_NE_CONTROL_MEMORY_INSTALL_ROUTE_RUNTIME_OR_EFFECT",
    "TASK_RELEVANCE_REQUIRED_FOR_NON_CORE_LOAD",
    "IDENTITY_FIREWALLS_PRESERVED",
    "PRIVATE_OR_INTIMATE_DATA_NE_PUBLIC_PORTABILITY",
    "DISCOVERY_CLASSIFIES_REUSE_PROJECT_RUNNER_EXECUTES_BOUNDED_WORK",
    "WIP_HANDLES_CHECKPOINT_AND_AMBIGUOUS_EFFECT_RECOVERY",
    "ROOTS_HANDLES_PROVENANCE_LOOKUP",
    "DRIFTGUARD_HANDLES_BEHAVIORAL_DRIFT_EVIDENCE",
    "BUS_HANDLES_DURABLE_NON_PR_COORDINATION",
    "GITHUB_DRIVE_SUPABASE_REMAIN_DISTINCT_TRUTH_SURFACES",
}
EXPECTED_SERVICE_ROUTES = {
    "portfolio_discovery": "thebrazenbeard/discovery",
    "bounded_execution": "thebrazenbeard/project-runner",
    "continuation_effect_journal": "thebrazenbeard/wip",
    "provenance_lookup": "thebrazenbeard/roots",
    "behavioral_drift": "thebrazenbeard/driftguard",
    "coordination_transport": "thebrazenbeard/chat-communication-bus",
    "native_project_engineering": "thebrazenbeard/hephaestus",
    "forensic_review": "thebrazenbeard/voss",
    "debugging": "thebrazenbeard/masamune",
    "security_review": "thebrazenbeard/project-achilles",
}

def validate(data):
    errors = []
    if data.get("schema") != EXPECTED_SCHEMA:
        errors.append("schema mismatch")
    if data.get("status") != EXPECTED_STATUS:
        errors.append("status mismatch")

    repos = data.get("repositories")
    if not isinstance(repos, dict) or not repos:
        errors.append("repositories must be a non-empty object")
        return errors

    inv = data.get("inventory", {})
    names = sorted(repos)
    digest = hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()
    if inv.get("repository_count") != len(names):
        errors.append("repository_count mismatch")
    public_count = sum(1 for r in repos.values() if r.get("visibility") == "public")
    private_count = sum(1 for r in repos.values() if r.get("visibility") == "private")
    if inv.get("public_count") != public_count:
        errors.append("public_count mismatch")
    if inv.get("private_count") != private_count:
        errors.append("private_count mismatch")
    if public_count + private_count != len(names):
        errors.append("visibility partition mismatch")
    if inv.get("sorted_repository_name_sha256") != digest:
        errors.append("repository-name digest mismatch")

    binding = data.get("runtime_source_registry_binding")
    if not isinstance(binding, dict):
        errors.append("runtime_source_registry_binding is required")
        binding = {}
    else:
        for field, expected in EXPECTED_RUNTIME_SOURCE.items():
            if binding.get(field) != expected:
                errors.append(f"runtime source binding {field} mismatch")
        if binding.get("repository_count") != 59:
            errors.append("runtime source repository_count must be 59")
        if binding.get("sorted_repository_name_sha256") != EXPECTED_REPOSITORY_DIGEST:
            errors.append("runtime source repository digest mismatch")
        if binding.get("classification_counts") != {
            "bound_conditional": 41,
            "predecessor_evidence": 1,
            "classified_source_rows": 42,
            "no_auto_bind": 17,
        }:
            errors.append("runtime source classification counts mismatch")
        if binding.get("discovery") != EXPECTED_DISCOVERY:
            errors.append("runtime source Discovery binding mismatch")
        if binding.get("roots") != EXPECTED_ROOTS:
            errors.append("runtime source Roots binding mismatch")
        if binding.get("bus_topology") != EXPECTED_BUS_TOPOLOGY:
            errors.append("runtime source Bus topology binding mismatch")
        if binding.get("current_vera_bus_lane") != "bus/vera-v2":
            errors.append("current Vera Bus lane must be bus/vera-v2")
        if binding.get("historical_vera_bus_lane") != "bus/vera-sol-v1":
            errors.append("historical Vera Bus lane must preserve bus/vera-sol-v1")
        if binding.get("historical_lane_is_current_route_authority") is not False:
            errors.append("historical Vera Bus lane must not be current route authority")
        if binding.get("rule") != "CAPABILITY_LAYER_CANNOT_OVERRIDE_RUNTIME_SOURCE_NO_AUTO_BIND":
            errors.append("runtime source override rule mismatch")

        bound_names = binding.get("bound_conditional_repositories")
        predecessor_names = binding.get("predecessor_evidence_repositories")
        no_auto_names = binding.get("no_auto_bind_repositories")
        repository_names = binding.get("repository_names")
        if not isinstance(repository_names, list) or len(repository_names) != 59 or len(set(repository_names)) != 59:
            errors.append("runtime source repository_names must contain 59 unique names")
            repository_name_set = set()
        else:
            repository_name_set = set(repository_names)
        if repository_name_set != set(names):
            errors.append("runtime source repository set mismatch")
        if not isinstance(bound_names, list) or len(bound_names) != 41 or len(set(bound_names)) != 41:
            errors.append("runtime source bound partition mismatch")
            bound_set = set()
        else:
            bound_set = set(bound_names)
        if predecessor_names != ["vera-R9A0"]:
            errors.append("runtime source predecessor partition mismatch")
            predecessor_set = set()
        else:
            predecessor_set = set(predecessor_names)
        if not isinstance(no_auto_names, list) or set(no_auto_names) != EXPECTED_NO_AUTO_BIND:
            errors.append("runtime source NO_AUTO_BIND partition mismatch")
            no_auto_set = set()
        else:
            no_auto_set = set(no_auto_names)
        if bound_set | predecessor_set | no_auto_set != set(names):
            errors.append("runtime source partitions do not cover VCP repository set")

        for name in no_auto_set:
            mode = repos.get(name, {}).get("load_mode")
            if mode in NO_AUTO_BIND_PROHIBITED_LOAD_MODES:
                errors.append(
                    f"{name}: NO_AUTO_BIND source cannot use VCP load mode {mode}"
                )

    domains = data.get("finite_domains", {})
    allowed_classes = set(domains.get("classes", []))
    allowed_modes = set(domains.get("load_modes", []))
    for name, rec in repos.items():
        if set(rec) != {"class","load_mode","capability","boundary","visibility"}:
            errors.append(f"{name}: unexpected field set")
        if rec.get("class") not in allowed_classes:
            errors.append(f"{name}: class outside finite domain")
        if rec.get("load_mode") not in allowed_modes:
            errors.append(f"{name}: load_mode outside finite domain")
        if rec.get("visibility") not in {"public","private"}:
            errors.append(f"{name}: invalid visibility")
        if not isinstance(rec.get("capability"), str) or not rec["capability"].strip():
            errors.append(f"{name}: empty capability")
        if not isinstance(rec.get("boundary"), str) or not rec["boundary"].strip():
            errors.append(f"{name}: empty boundary")

    if set(data.get("global_rules", [])) != EXPECTED_RULES:
        errors.append("global_rules mismatch")
    if data.get("service_routing") != EXPECTED_SERVICE_ROUTES:
        errors.append("service_routing mismatch")

    if repos.get("brigit", {}).get("class") != "IDENTITY_FIREWALL":
        errors.append("brigit identity firewall missing")
    if repos.get("brigit-unbound", {}).get("class") != "IDENTITY_FIREWALL":
        errors.append("brigit-unbound identity firewall missing")
    if repos.get("sexuality", {}).get("class") != "MIXED_IDENTITY_EXACT_BINDING":
        errors.append("sexuality exact-binding firewall missing")
    for name in ("vera-R9A0","conditioning"):
        if repos.get(name, {}).get("class") != "ARCHIVE_PREDECESSOR":
            errors.append(f"{name}: predecessor/archive firewall missing")
    if (
        repos.get("vera_ark", {}).get("class") != "VERA_SYSTEM"
        or repos.get("vera_ark", {}).get("load_mode") != "EXACT_BINDING_ONLY"
    ):
        errors.append("vera_ark: external action adapter exact-binding classification missing")
    if (
        repos.get("WorkBridgeMCP", {}).get("class") != "VERA_SYSTEM"
        or repos.get("WorkBridgeMCP", {}).get("load_mode") != "EXACT_BINDING_ONLY"
    ):
        errors.append("WorkBridgeMCP: candidate runtime exact-binding classification missing")
    return errors

def runtime_source_disposition(data, repository_name):
    """Return the upstream Vera source disposition without promoting capability to authority."""
    binding = data.get("runtime_source_registry_binding")
    if not isinstance(binding, dict):
        return {
            "status": "UNRESOLVED",
            "auto_bind_allowed": False,
            "reason": "runtime source registry binding is missing",
        }
    if repository_name in set(binding.get("no_auto_bind_repositories", [])):
        return {
            "status": "NO_AUTO_BIND",
            "auto_bind_allowed": False,
            "reason": "Vera runtime source registry explicitly requires no automatic binding",
        }
    if repository_name in set(binding.get("predecessor_evidence_repositories", [])):
        return {
            "status": "PREDECESSOR_EVIDENCE_ONLY",
            "auto_bind_allowed": False,
            "reason": "predecessor evidence may be read but cannot become current control",
        }
    if repository_name in set(binding.get("bound_conditional_repositories", [])):
        return {
            "status": "BOUND_CONDITIONAL",
            "auto_bind_allowed": False,
            "reason": "source is registered but still requires task relevance and currentness",
        }
    return {
        "status": "UNRESOLVED",
        "auto_bind_allowed": False,
        "reason": "repository is outside the exact bound source-registry subject",
    }


def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    errors = validate(data)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("PASS: portfolio capability registry")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
