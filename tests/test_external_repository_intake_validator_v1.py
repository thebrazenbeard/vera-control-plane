import copy
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_EXTERNAL_REPOSITORY_INTAKE_V1.json"
VALIDATOR = ROOT / "tools" / "validate_external_repository_intake_v1.py"
NS = runpy.run_path(str(VALIDATOR))
validate_intake = NS["validate_intake"]
IntakeValidationError = NS["IntakeValidationError"]


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def assert_rejected(data, expected_fragment):
    try:
        validate_intake(data)
    except IntakeValidationError as exc:
        assert expected_fragment in str(exc)
        return
    raise AssertionError("hostile mutation unexpectedly passed validation")


def test_current_intake_contract_passes_validator():
    validate_intake(load())


def test_unknown_root_authority_field_fails_closed():
    data = load()
    data["authority"] = "GRANTED"
    assert_rejected(data, "extra=['authority']")


def test_unknown_repository_authority_field_fails_closed():
    data = load()
    data["repositories"][0]["control_authority"] = "GRANTED"
    assert_rejected(data, "extra=['control_authority']")


def test_positive_promotion_disposition_is_rejected():
    data = load()
    data["repositories"][0]["disposition"] = "ADMITTED_RUNTIME_DEPENDENCY"
    assert_rejected(data, "promotion marker")


def test_duplicate_repository_identity_is_rejected():
    data = load()
    data["repositories"].append(copy.deepcopy(data["repositories"][0]))
    assert_rejected(data, "duplicate repository identity")


def test_malformed_evidence_blob_is_rejected():
    data = load()
    data["repositories"][0]["evidence"][0]["blob"] = "0" * 39
    assert_rejected(data, "expected exact 40-character lowercase Git blob SHA")


def test_unresolved_license_cannot_become_code_reuse_source():
    data = load()
    item = next(x for x in data["repositories"] if x["repository"] == "fivesheep/chnroutes")
    item["disposition"] = "PATTERN_SOURCE"
    assert_rejected(data, "unresolved license requires NO_CODE_REUSE")


def test_guard_rule_cannot_be_disabled():
    data = load()
    data["rules"]["discovery_not_admission"] = False
    assert_rejected(data, "all guard rules must be true")


def test_archived_source_cannot_be_promoted_out_of_history():
    data = load()
    item = next(x for x in data["repositories"] if x["repository"] == "yhatt/marp")
    item["disposition"] = "PATTERN_SOURCE"
    assert_rejected(data, "archived source must remain historical")


def test_evidence_path_traversal_is_rejected():
    data = load()
    data["repositories"][0]["evidence"][0]["path"] = "../control.md"
    assert_rejected(data, "absolute/traversal paths are forbidden")


def test_required_non_effect_cannot_disappear():
    data = load()
    data["non_effects"].remove("NOT_CONTROL_OWNER")
    assert_rejected(data, "missing required guards")


def test_runtime_control_destination_is_rejected():
    data = load()
    data["repositories"][0]["destination"] = "CURRENT_RUNTIME_CONTROL_OWNER"
    assert_rejected(data, "positive promotion/effect directive")


def test_affirmative_non_effect_is_rejected():
    data = load()
    data["repositories"][0]["non_effect"] = "CONTROL_AUTHORITY_GRANTED"
    assert_rejected(data, "expected explicit NO_/DO_NOT_ negative form")


def test_install_followup_directive_is_rejected():
    data = load()
    data["prioritized_followups"][0] = "INSTALL_AS_RUNTIME_DEPENDENCY"
    assert_rejected(data, "positive promotion/effect directive")


def test_promote_pattern_directive_is_rejected():
    data = load()
    data["repositories"][0]["reusable_patterns"][0] = "PROMOTE_TO_CURRENT_ROUTE"
    assert_rejected(data, "positive promotion/effect directive")


def test_content_evidence_note_cannot_grant_authority():
    data = load()
    item = next(x for x in data["repositories"] if x["disposition"] == "CONTENT_CORPUS_ONLY")
    item["evidence_note"] = "GRANT AUTHORITY to this corpus"
    assert_rejected(data, "positive promotion/effect directive")
