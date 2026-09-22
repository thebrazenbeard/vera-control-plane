from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_DISCOVERY_PORTFOLIO_CONTROL_SUPPORT_INTAKE_V1.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")

EXPECTED_DESTINATIONS = {
    "VCP_PORTFOLIO_INTAKE_GOVERNANCE",
    "VCP_RECOVERY_QUALIFICATION_RESEARCH",
    "VCP_EXECUTION_GOVERNANCE_RESEARCH",
    "VCP_PROVENANCE_CURRENTNESS_RESEARCH",
    "VCP_ROUTING_CONNECTIVITY_RESEARCH",
    "VCP_INSTALL_DEPLOYMENT_RESEARCH",
    "VCP_HOSTILE_REVIEW_AUDIT_RESEARCH",
    "VCP_AMBIGUOUS_EFFECT_RECOVERY_RESEARCH",
}
EXPECTED_SOURCES = {
    "thebrazenbeard/discovery",
    "thebrazenbeard/driftguard",
    "thebrazenbeard/project-runner",
    "thebrazenbeard/roots",
    "thebrazenbeard/vera-mesh",
    "thebrazenbeard/vera-synology",
    "thebrazenbeard/voss",
    "thebrazenbeard/wip",
}
FORBIDDEN = {
    "CONTROL_OWNERSHIP",
    "PROJECT_INSTALL",
    "RUNTIME_ACTIVATION",
    "PROVIDER_MUTATION",
    "CREDENTIAL_OR_PERMISSION_CHANGE",
    "NETWORK_DEPLOYMENT",
    "MERGE_AUTHORITY",
    "MEMORY_OR_IDENTITY_ADMISSION",
}


class ValidationError(ValueError):
    pass


def validate(data: dict[str, Any]) -> None:
    if data.get("schema") != "VERA_DISCOVERY_PORTFOLIO_CONTROL_SUPPORT_INTAKE_V1":
        raise ValidationError("schema mismatch")
    if data.get("status") != "SOURCE_SUPPORT_INTAKE_ONLY_NOT_CONTROL_NOT_INSTALLED_NOT_RUNTIME_QUALIFIED":
        raise ValidationError("status promoted beyond source-support intake")
    if data.get("observed_date") != "2026-09-22":
        raise ValidationError("observed_date changed")

    binding = data.get("discovery_binding")
    if not isinstance(binding, dict):
        raise ValidationError("discovery binding missing")
    if binding.get("repository") != "thebrazenbeard/discovery":
        raise ValidationError("discovery repository mismatch")
    if binding.get("pr") != 39:
        raise ValidationError("discovery PR binding mismatch")
    if not HEX40.fullmatch(str(binding.get("exact_head", ""))):
        raise ValidationError("discovery exact head invalid")

    rules = data.get("guard_rules")
    if not isinstance(rules, dict) or not rules or any(value is not True for value in rules.values()):
        raise ValidationError("all guard rules must remain exact true")

    domains = data.get("domains")
    if not isinstance(domains, dict):
        raise ValidationError("domains missing")
    if set(domains.get("destination", [])) != EXPECTED_DESTINATIONS:
        raise ValidationError("destination domain changed")
    if domains.get("disposition") != ["CONTROL_SUPPORT_SOURCE_CANDIDATE"]:
        raise ValidationError("disposition domain changed")
    allowed_modes = {"EVIDENCE_ONLY", "MECHANISM_RESEARCH_ONLY", "EXACT_TASK_AND_TARGET_AUTHORITY_REQUIRED", "REVIEW_ONLY"}
    if set(domains.get("activation_mode", [])) != allowed_modes:
        raise ValidationError("activation mode domain changed")

    sources = data.get("sources")
    if not isinstance(sources, list) or len(sources) != 8:
        raise ValidationError("exact eight-source support intake required")
    seen: set[str] = set()
    seen_destinations: set[str] = set()
    for item in sources:
        if not isinstance(item, dict):
            raise ValidationError("source entry invalid")
        repo = item.get("repository")
        if repo not in EXPECTED_SOURCES or repo in seen:
            raise ValidationError("source repository set changed")
        seen.add(repo)
        if not HEX40.fullmatch(str(item.get("head", ""))):
            raise ValidationError(f"{repo}: exact head invalid")
        if item.get("disposition") != "CONTROL_SUPPORT_SOURCE_CANDIDATE":
            raise ValidationError(f"{repo}: disposition promoted")
        destination = item.get("destination")
        if destination not in EXPECTED_DESTINATIONS:
            raise ValidationError(f"{repo}: destination outside finite domain")
        if destination in seen_destinations:
            raise ValidationError("each support source must retain a distinct destination")
        seen_destinations.add(destination)
        if item.get("activation_mode") not in allowed_modes:
            raise ValidationError(f"{repo}: activation mode outside finite domain")
        ceiling = item.get("authority_ceiling")
        if not isinstance(ceiling, str) or not ceiling.strip():
            raise ValidationError(f"{repo}: authority ceiling missing")

    if seen != EXPECTED_SOURCES:
        raise ValidationError("source repository set incomplete")
    if seen_destinations != EXPECTED_DESTINATIONS:
        raise ValidationError("destination coverage incomplete")

    forbidden = data.get("global_forbidden_effects")
    if not isinstance(forbidden, list) or set(forbidden) != FORBIDDEN or len(forbidden) != len(FORBIDDEN):
        raise ValidationError("forbidden effect set changed")

    ceiling = data.get("claim_ceiling")
    if ceiling != "VCP_CONTROL_SUPPORT_SOURCE_INTAKE_ONLY_NO_RELEASE_BINDING_NO_INSTALL_NO_RUNTIME_ACTIVATION":
        raise ValidationError("claim ceiling changed")


def load_and_validate(path: Path = CONTRACT) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValidationError("contract must be an object")
    validate(data)
    return data


if __name__ == "__main__":
    load_and_validate()
    print("VERA_DISCOVERY_PORTFOLIO_CONTROL_SUPPORT_INTAKE_V1: VALID")
