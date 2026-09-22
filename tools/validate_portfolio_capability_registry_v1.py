#!/usr/bin/env python3
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "governance" / "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"

EXPECTED_SCHEMA = "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1"
EXPECTED_STATUS = "PRIVATE_ROUTING_SNAPSHOT_NOT_CONTROL_AUTHORITY"
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
    for name in ("vera-R9A0","vera_ark","conditioning"):
        if repos.get(name, {}).get("class") != "ARCHIVE_PREDECESSOR":
            errors.append(f"{name}: predecessor/archive firewall missing")
    return errors

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
