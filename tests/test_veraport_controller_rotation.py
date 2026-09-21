import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "VERAPORT_CONTROLLER_ROTATION_V1.json"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_rotation_is_protected_and_not_authorized_by_source():
    value = load()
    assert value["status"] == "SOURCE_CONTROL_CONTRACT_ONLY_NO_CREDENTIAL_EFFECT"
    assert value["authority"]["key_generation"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert value["authority"]["trust_mutation"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert value["authority"]["service_restart"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"


def test_recovery_requires_cryptographic_identity_not_filename():
    recovery = load()["recovery"]
    assert recovery["candidate_filename_is_identity"] is False
    assert set(recovery["required_match"]) >= {
        "EC_P256_PRIVATE_KEY",
        "DERIVED_PUBLIC_SPKI",
        "DERIVED_CONTROLLER_PRINCIPAL_EXACT",
        "DERIVED_KEY_ID_EXACT",
    }


def test_rotation_is_additive_before_retirement():
    rotation = load()["rotation"]
    assert rotation["strategy"] == "ADDITIVE_THEN_ACCEPT_THEN_OPTIONAL_RETIRE"
    assert rotation["initial_enrollment"]["mode"] == "ADD_WITHOUT_PREDECESSOR_DELETION"
    assert rotation["initial_enrollment"]["capabilities"] == ["fs.read"]
    assert rotation["initial_enrollment"]["fs.write"] == "NOT_GRANTED_IN_INITIAL_ACCEPTANCE"
    assert rotation["predecessor_retirement"]["requires_successor_acceptance"] is True


def test_new_trust_requires_deliberate_restart_and_rollback():
    reload = load()["rotation"]["reload"]
    assert reload["trust_loaded_at_host_prepare"] is True
    assert reload["service_restart_required_for_new_trust"] is True
    assert reload["restart_is_separate_effect"] is True
    assert reload["rollback_on_restart_failure"] is True


def test_read_acceptance_does_not_promote_mutating_authority():
    non = set(load()["rotation"]["post_acceptance_non_implications"])
    assert {
        "READ_PASS_NE_WRITE_AUTHORITY",
        "READ_PASS_NE_PROCESS_AUTHORITY",
        "READ_PASS_NE_PLUGIN_REGISTERED",
        "READ_PASS_NE_OLD_CONTROLLER_RETIREMENT_AUTHORITY",
    }.issubset(non)


def test_private_key_never_enters_durable_public_evidence():
    value = load()
    identity = value["rotation"]["new_identity"]
    assert identity["private_key_git"] == "FORBIDDEN"
    assert identity["private_key_bus"] == "FORBIDDEN"
    assert identity["private_key_logs"] == "FORBIDDEN"
    assert "PRIVATE_KEY_BYTES" in value["receipt"]["never_record"]


def test_empty_trust_and_pre_acceptance_retirement_are_forbidden():
    retirement = load()["rotation"]["predecessor_retirement"]
    assert retirement["empty_trust_forbidden"] is True
    assert retirement["requires_successor_acceptance"] is True
    attacks = set(load()["hostile_regressions"])
    assert "TRUST_OVERWRITE_REMOVES_ALL_CONTROLLERS" in attacks
    assert "OLD_CONTROLLER_REMOVED_PRE_ACCEPTANCE" in attacks
