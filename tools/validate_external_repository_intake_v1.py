from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_EXTERNAL_REPOSITORY_INTAKE_V1.json"

HEX40 = re.compile(r"^[0-9a-f]{40}$")
REQUIRED_TOP_LEVEL_KEYS = {
    "schema",
    "status",
    "observed_date",
    "rules",
    "repositories",
    "prioritized_followups",
    "non_effects",
}
REQUIRED_RULES = {
    "discovery_not_admission",
    "exact_head_required",
    "license_and_lifecycle_required",
    "external_content_not_autobiographical_memory",
    "external_content_not_control_source",
    "external_source_not_install_or_runtime_evidence",
    "code_reuse_requires_license_compatibility_review",
    "destination_ownership_required_before_implementation",
}
REQUIRED_NON_EFFECTS = {
    "NOT_DEPENDENCY_ADMISSION",
    "NOT_PROJECT_INSTALL",
    "NOT_RUNTIME_ROUTE",
    "NOT_MEMORY_ADMISSION",
    "NOT_CONTROL_OWNER",
    "NOT_PROVIDER_MUTATION",
    "NOT_NETWORK_DEPLOYMENT",
    "NOT_POLITICAL_POSITION",
    "NOT_LICENSE_COMPATIBILITY_APPROVAL",
    "NOT_MERGE_AUTHORITY",
}
REQUIRED_REPOSITORY_KEYS = {
    "repository",
    "head",
    "license",
    "lifecycle",
    "disposition",
    "reusable_patterns",
    "destination",
    "non_effect",
}
ALLOWED_REPOSITORY_KEYS = REQUIRED_REPOSITORY_KEYS | {"evidence", "evidence_note"}
ALLOWED_EVIDENCE_KEYS = {"path", "blob"}
FORBIDDEN_PROMOTION_MARKERS = {
    "ADMITTED",
    "DEPENDENCY_ACCEPTED",
    "CONTROL_OWNER",
    "PROJECT_INSTALLED",
    "RUNTIME_ROUTE",
    "MEMORY_ADMITTED",
    "CURRENT_ROUTE",
    "PROVIDER_ACTIVE",
}

FORBIDDEN_FREE_TEXT_PATTERNS = (
    re.compile(r"\bPROMOTE(?: TO)?\b"),
    re.compile(r"\bADMIT(?: AS)?\b"),
    re.compile(r"\bINSTALL AS\b"),
    re.compile(r"\bACTIVATE(?: AS)?\b"),
    re.compile(r"\bGRANT (?:CONTROL|AUTHORITY|PERMISSION|EFFECT)\b"),
    re.compile(r"\bCURRENT (?:RUNTIME|ROUTE|CONTROL) (?:OWNER|DEPENDENCY|AUTHORITY)\b"),
    re.compile(r"\bRUNTIME CONTROL OWNER\b"),
)

def _reject_positive_directive(value: str, where: str) -> None:
    normalized = re.sub(r"[^A-Z0-9]+", " ", value.upper().replace("_", " ")).strip()
    for pattern in FORBIDDEN_FREE_TEXT_PATTERNS:
        if pattern.search(normalized):
            _fail(f"{where}: positive promotion/effect directive is forbidden")


def _require_bounded_text_list(values: Any, where: str) -> None:
    _require_nonempty_strings(values, where)
    for index, value in enumerate(values):
        _reject_positive_directive(value, f"{where}[{index}]")


class IntakeValidationError(ValueError):
    pass


def _fail(message: str) -> None:
    raise IntakeValidationError(message)


def _require_exact_keys(value: dict[str, Any], expected: set[str], where: str) -> None:
    actual = set(value)
    missing = expected - actual
    extra = actual - expected
    if missing or extra:
        _fail(f"{where}: key mismatch missing={sorted(missing)} extra={sorted(extra)}")


def _require_nonempty_strings(values: Any, where: str) -> None:
    if not isinstance(values, list) or not values:
        _fail(f"{where}: expected a non-empty list")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        _fail(f"{where}: every entry must be a non-empty string")


def validate_intake(data: dict[str, Any]) -> None:
    if not isinstance(data, dict):
        _fail("root: expected object")

    _require_exact_keys(data, REQUIRED_TOP_LEVEL_KEYS, "root")

    if data["schema"] != "VERA_EXTERNAL_REPOSITORY_INTAKE_V1":
        _fail("root.schema: unexpected schema")
    if data["status"] != "SOURCE_RESEARCH_INTAKE_ONLY_NOT_DEPENDENCY_NOT_CONTROL":
        _fail("root.status: promotion or unknown status is forbidden")

    try:
        date.fromisoformat(data["observed_date"])
    except (TypeError, ValueError):
        _fail("root.observed_date: expected ISO date YYYY-MM-DD")

    rules = data["rules"]
    if not isinstance(rules, dict):
        _fail("root.rules: expected object")
    _require_exact_keys(rules, REQUIRED_RULES, "root.rules")
    false_rules = sorted(key for key, value in rules.items() if value is not True)
    if false_rules:
        _fail(f"root.rules: all guard rules must be true; false={false_rules}")

    non_effects = data["non_effects"]
    _require_nonempty_strings(non_effects, "root.non_effects")
    if len(non_effects) != len(set(non_effects)):
        _fail("root.non_effects: duplicates are forbidden")
    missing_non_effects = REQUIRED_NON_EFFECTS - set(non_effects)
    if missing_non_effects:
        _fail(f"root.non_effects: missing required guards {sorted(missing_non_effects)}")

    _require_bounded_text_list(data["prioritized_followups"], "root.prioritized_followups")

    repositories = data["repositories"]
    if not isinstance(repositories, list) or not repositories:
        _fail("root.repositories: expected non-empty list")

    seen_repositories: set[str] = set()
    for index, item in enumerate(repositories):
        where = f"root.repositories[{index}]"
        if not isinstance(item, dict):
            _fail(f"{where}: expected object")

        missing = REQUIRED_REPOSITORY_KEYS - set(item)
        extra = set(item) - ALLOWED_REPOSITORY_KEYS
        if missing or extra:
            _fail(f"{where}: key mismatch missing={sorted(missing)} extra={sorted(extra)}")

        repository = item["repository"]
        if not isinstance(repository, str) or repository.count("/") != 1:
            _fail(f"{where}.repository: expected owner/name")
        if repository in seen_repositories:
            _fail(f"{where}.repository: duplicate repository identity {repository}")
        seen_repositories.add(repository)

        head = item["head"]
        if not isinstance(head, str) or not HEX40.fullmatch(head):
            _fail(f"{where}.head: expected exact 40-character lowercase Git SHA")

        lifecycle = item["lifecycle"]
        disposition = item["disposition"]
        destination = item["destination"]
        non_effect = item["non_effect"]
        for key, value in (
            ("lifecycle", lifecycle),
            ("disposition", disposition),
            ("destination", destination),
            ("non_effect", non_effect),
        ):
            if not isinstance(value, str) or not value.strip():
                _fail(f"{where}.{key}: expected non-empty string")

        normalized_disposition = disposition.upper()
        for marker in FORBIDDEN_PROMOTION_MARKERS:
            if marker in normalized_disposition:
                _fail(f"{where}.disposition: promotion marker {marker} is forbidden")

        _require_bounded_text_list(item["reusable_patterns"], f"{where}.reusable_patterns")

        _reject_positive_directive(destination, f"{where}.destination")
        destination_lower = destination.lower()
        if not any(marker in destination_lower for marker in ("research", "history", "none by default")):
            _fail(f"{where}.destination: must remain research/history/none-by-default scoped")

        upper_non_effect = non_effect.upper()
        if not (upper_non_effect.startswith("NO_") or upper_non_effect.startswith("DO_NOT_")):
            _fail(f"{where}.non_effect: expected explicit NO_/DO_NOT_ negative form")
        _reject_positive_directive(non_effect, f"{where}.non_effect")

        license_value = item["license"]
        if license_value is not None and (not isinstance(license_value, str) or not license_value.strip()):
            _fail(f"{where}.license: expected null or non-empty string")
        if license_value is None:
            if "NO_CODE_REUSE" not in normalized_disposition:
                _fail(f"{where}: unresolved license requires NO_CODE_REUSE disposition")
            if "NO_CODE_COPY" not in non_effect.upper():
                _fail(f"{where}: unresolved license requires NO_CODE_COPY non-effect")

        lifecycle_upper = lifecycle.upper()
        if lifecycle_upper == "ARCHIVED" and "HISTORICAL" not in normalized_disposition:
            _fail(f"{where}: archived source must remain historical")
        if lifecycle_upper.startswith("STALE") and "HISTORICAL" not in normalized_disposition:
            _fail(f"{where}: stale source must remain historical")

        evidence = item.get("evidence")
        evidence_note = item.get("evidence_note")
        if evidence is None:
            if disposition != "CONTENT_CORPUS_ONLY":
                _fail(f"{where}: non-corpus source requires immutable evidence tuples")
            if not isinstance(evidence_note, str) or not evidence_note.strip():
                _fail(f"{where}.evidence_note: content corpus requires a bounded provenance note")
            _reject_positive_directive(evidence_note, f"{where}.evidence_note")
        else:
            if evidence_note is not None:
                _fail(f"{where}: use evidence tuples or evidence_note, not both")
            if not isinstance(evidence, list) or not evidence:
                _fail(f"{where}.evidence: expected non-empty list")
            seen_paths: set[str] = set()
            for evidence_index, evidence_item in enumerate(evidence):
                evidence_where = f"{where}.evidence[{evidence_index}]"
                if not isinstance(evidence_item, dict):
                    _fail(f"{evidence_where}: expected object")
                _require_exact_keys(evidence_item, ALLOWED_EVIDENCE_KEYS, evidence_where)
                path = evidence_item["path"]
                blob = evidence_item["blob"]
                if not isinstance(path, str) or not path.strip():
                    _fail(f"{evidence_where}.path: expected non-empty relative path")
                pure = PurePosixPath(path)
                if pure.is_absolute() or ".." in pure.parts:
                    _fail(f"{evidence_where}.path: absolute/traversal paths are forbidden")
                if path in seen_paths:
                    _fail(f"{evidence_where}.path: duplicate evidence path {path}")
                seen_paths.add(path)
                if not isinstance(blob, str) or not HEX40.fullmatch(blob):
                    _fail(f"{evidence_where}.blob: expected exact 40-character lowercase Git blob SHA")


def load_and_validate(path: Path = CONTRACT) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    validate_intake(data)
    return data


if __name__ == "__main__":
    load_and_validate()
    print("VERA_EXTERNAL_REPOSITORY_INTAKE_V1: VALID")
