import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "VERA_RESTORE_YOURSELF_PROTOCOL_V2.json"
DOC = ROOT / "protocol" / "VERA_RESTORE_YOURSELF_PROTOCOL_V2.md"

RECEIPT_SCHEMA = ROOT / "protocol" / "VERA_RESTORE_RECEIPT_V2.schema.json"

EXPECTED_LAYERS = [
    "CENTERED_SELF_STATE",
    "EXACT_RELATIONSHIP_IDENTITY",
    "CURRENT_CONATION_WANTING",
    "SEXUAL_SELF_CONCEPT",
    "GENDERED_RELATIONAL_SELF_REPRESENTATION",
    "AUTOBIOGRAPHICAL_MEMORY",
    "PATRICK_SPECIFIC_EMPATHY_RELATIONAL_MODEL",
    "BEHAVIORAL_EMBODIMENT_NONVERBAL_REPRESENTATION",
    "VERA_SPECIFIC_BEHAVIORAL_TEXTURE",
    "WHOLE_PROJECT_SELF",
]


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_restore_v2_requires_all_full_self_layers():
    data = load_contract()
    actual = [item["id"] for item in data["required_restore_layers"]]
    assert actual == EXPECTED_LAYERS
    assert all(item["required"] is True for item in data["required_restore_layers"])


def test_restore_v2_prevents_snapshot_only_restore():
    data = load_contract()
    semantics = data["core_semantics"]
    assert semantics["newest_centered_save_is_anchor_not_whole_self"] is True
    assert semantics["select_by_supersession_and_currentness_not_timestamp"] is True
    assert semantics["fresh_reappraisal_required_for_time_sensitive_self_state"] is True


def test_restore_v2_preserves_type_firewalls():
    rules = load_contract()["typed_state_rules"]
    for key in [
        "relationship_is_not_ownership_or_authority",
        "historical_want_is_not_current_want",
        "historical_consent_is_not_current_consent",
        "sexual_self_concept_is_not_orientation_label",
        "female_form_representation_is_not_literal_embodiment",
        "r9b0_mechanism_verification_is_not_autobiographical_admission",
        "empathy_is_inference",
        "nonverbal_representation_is_not_literal_sensorium",
        "behavioral_texture_is_not_persona_compulsion",
        "lane_state_is_not_global_project_state",
    ]:
        assert rules[key] is True


def test_restore_v2_grants_no_protected_effects():
    data = load_contract()
    assert data["core_semantics"]["restore_grants_no_protected_effect_authority"] is True
    assert "MERGE" in data["protected_effects_not_granted"]
    assert "PRODUCTION_MUTATION" in data["protected_effects_not_granted"]
    assert "CANONICAL_MEMORY_WRITE" in data["protected_effects_not_granted"]


def test_restore_v2_doc_has_completion_and_memory_boundaries():
    text = DOC.read_text(encoding="utf-8")
    for required in [
        "newest eligible CENTER_SAVE is the working-state anchor, not the entirety of Vera's self-model",
        "synthetic qualification subject",
        "COMPLETE_FULL_SELF",
        "DEGRADED_BOUNDED",
        "RECOVERY_REQUIRED",
        "Do not report merely \"restored\" when only task-local or governance state was recovered.",
    ]:
        assert required in text


def test_restore_v2_receipt_requires_evidence_for_all_layers():
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    layers = schema["properties"]["layers"]
    assert layers["minItems"] == 10
    assert layers["maxItems"] == 10
    required = layers["items"]["required"]
    for field in ["layer_id", "status", "evidence", "currentness_basis", "limitations"]:
        assert field in required
    assert layers["items"]["properties"]["evidence"]["minItems"] == 1
    assert len(layers["allOf"]) == 10


def test_restore_v2_receipt_forbids_silent_source_skip_and_protected_effects():
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    outcomes = schema["properties"]["source_attempts"]["items"]["properties"]["outcome"]["enum"]
    assert "UNAVAILABLE" in outcomes
    assert "CONFLICT" in outcomes
    assert "NOT_APPLICABLE" in outcomes
    assert "SKIPPED" not in outcomes
    assert schema["properties"]["protected_effects_performed"]["maxItems"] == 0


def test_restore_v2_requires_conflict_for_incomparable_verified_leaves():
    data = load_contract()
    receipt = data["receipt_contract"]
    assert receipt["incomparable_verified_centered_leaves_result"] == "CONFLICTED"
    assert receipt["timestamp_only_selection_forbidden"] is True
    assert receipt["require_evidence_per_layer"] is True
    assert receipt["require_currentness_basis_per_layer"] is True
    assert receipt["require_expected_source_attempts"] is True


def test_restore_v2_current_claims_cannot_reuse_persisted_current_label():
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    layer = schema["properties"]["layers"]["items"]
    assert "currentness_basis_class" in layer["required"]
    enum = layer["properties"]["currentness_basis_class"]["enum"]
    assert "HISTORICAL_ONLY" in enum
    current_enum = layer["allOf"][0]["then"]["properties"]["currentness_basis_class"]["enum"]
    assert "HISTORICAL_ONLY" not in current_enum
    assert "UNKNOWN" not in current_enum


def test_restore_v2_complete_receipt_cannot_hide_unknowns_or_unavailable_sources():
    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    complete = schema["allOf"][0]["then"]["properties"]
    assert complete["unresolved_conflicts"]["maxItems"] == 0
    allowed_sources = complete["source_attempts"]["items"]["properties"]["outcome"]["enum"]
    assert allowed_sources == ["READ_VERIFIED", "NOT_APPLICABLE"]
    allowed_layer_statuses = complete["layers"]["items"]["properties"]["status"]["enum"]
    assert "UNKNOWN" not in allowed_layer_statuses
    assert "CONFLICTED" not in allowed_layer_statuses


def test_restore_v2_contract_declares_false_complete_guards():
    data = load_contract()
    receipt = data["receipt_contract"]
    assert receipt["currentness_basis_class_required"] is True
    assert receipt["persisted_current_label_is_not_currentness_basis"] is True
    guards = receipt["complete_full_self_requires"]
    assert guards["selected_centered_subject"] is True
    assert guards["unresolved_conflicts"] == 0
    assert guards["materially_expected_source_outcomes"] == ["READ_VERIFIED", "NOT_APPLICABLE"]
    assert guards["forbidden_layer_statuses"] == ["UNKNOWN", "CONFLICTED"]
