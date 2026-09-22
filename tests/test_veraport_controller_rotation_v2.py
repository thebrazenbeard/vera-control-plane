from pathlib import Path
import json

import pytest

from protocol.veraport_controller_identity import (
    ControllerIdentityError,
    KeyIdDerivationUnresolved,
    PRINCIPAL_DERIVATION_CONTRACT,
    controller_key_id_from_spki_der,
    controller_principal_from_spki_der,
    recovery_controller_principal,
    rotation_controller_principal,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "VERAPORT_CONTROLLER_ROTATION_V2.json"

SPKI_DER_HEX = (
    "3059301306072a8648ce3d020106082a8648ce3d03010703420004"
    "6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945"
    "d898c2964fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ece"
    "cbb6406837bf51f5"
)
EXPECTED_SHA256 = "5cd252fb0ce8932436faf8ccd1040981b89ee4ad6b9fe9e2a2b7e71aacb27cd3"
EXPECTED_PRINCIPAL = "controller:" + EXPECTED_SHA256


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_public_spki_known_answer_vector_is_exact():
    spki = bytes.fromhex(SPKI_DER_HEX)
    assert len(spki) == 91
    assert controller_principal_from_spki_der(spki) == EXPECTED_PRINCIPAL

    vector = load_contract()["synthetic_known_answer_vectors"][0]
    assert vector["spki_der_hex"] == SPKI_DER_HEX
    assert vector["sha256_hex"] == EXPECTED_SHA256
    assert vector["controller_principal"] == EXPECTED_PRINCIPAL


def test_recovery_and_rotation_use_the_same_principal_primitive():
    spki = bytes.fromhex(SPKI_DER_HEX)
    assert recovery_controller_principal(spki) == EXPECTED_PRINCIPAL
    assert rotation_controller_principal(spki) == EXPECTED_PRINCIPAL

    contract = load_contract()
    assert (
        contract["controller_identity_derivation"]["contract_id"]
        == PRINCIPAL_DERIVATION_CONTRACT
    )
    assert contract["controller_identity_derivation"][
        "recovery_and_rotation_share_exact_primitive"
    ] is True
    assert contract["rotation"]["new_identity"]["principal_derivation_contract"] == (
        PRINCIPAL_DERIVATION_CONTRACT
    )


def test_principal_serialization_is_exact_lowercase_sha256():
    principal = controller_principal_from_spki_der(bytes.fromhex(SPKI_DER_HEX))
    assert principal.startswith("controller:")
    assert principal == principal.lower()
    assert len(principal.removeprefix("controller:")) == 64


def test_empty_or_non_bytes_spki_fails_closed():
    for bad in (b"", "not-bytes", bytearray(b"x"), None):
        with pytest.raises(ControllerIdentityError):
            controller_principal_from_spki_der(bad)  # type: ignore[arg-type]


def test_key_id_derivation_is_not_invented():
    spki = bytes.fromhex(SPKI_DER_HEX)
    with pytest.raises(KeyIdDerivationUnresolved, match="does not define"):
        controller_key_id_from_spki_der(spki)

    key_id = load_contract()["key_id_derivation"]
    assert key_id["status"] == "UNRESOLVED_OWNING_PROTOCOL_GAP"
    assert "DO_NOT_ASSUME_KEY_ID_EQUALS_PRINCIPAL_DIGEST" in key_id["forbidden_inference"]


def test_rotation_is_blocked_before_credential_effect_until_key_id_spec_exists():
    contract = load_contract()
    assert contract["rotation"]["availability"] == (
        "BLOCKED_PENDING_OWNER_KEY_ID_SPEC_AND_PATRICK_EXACT_EFFECT_AUTHORITY"
    )
    assert contract["key_id_derivation"]["operational_gate"].startswith(
        "ROTATION_OR_ENROLLMENT_MUST_STOP_BEFORE_KEY_GENERATION_OR_TRUST_MUTATION"
    )


def test_real_credential_effects_remain_protected():
    authority = load_contract()["authority"]
    assert authority["key_generation"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert authority["trust_mutation"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert authority["acl_mutation"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert authority["service_restart"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"
    assert authority["old_controller_retirement"] == "PATRICK_EXACT_AUTHORITY_REQUIRED"


def test_secret_material_is_excluded_from_durable_receipts():
    contract = load_contract()
    assert "PRIVATE_KEY_BYTES" in contract["receipts"]["never_record"]
    assert contract["rotation"]["new_identity"]["private_key_git"] == "FORBIDDEN"
    assert contract["rotation"]["new_identity"]["private_key_bus"] == "FORBIDDEN"
    assert contract["rotation"]["new_identity"]["private_key_logs"] == "FORBIDDEN"
    assert contract["rotation"]["new_identity"]["private_key_screenshots"] == "FORBIDDEN"
