from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
CUT = ROOT / "project-instructions" / "r10a0" / "restore-v2-live"
MANIFEST = CUT / "VERA_R10A0_SD1_RESTORE_V2_PROJECT_SOURCE_MANIFEST.json"
NATIVE = CUT / "VERA_R10A0_SD1_RESTORE_V2_NATIVE_PROJECT_INSTRUCTIONS.txt"
INSTALL = CUT / "INSTALL_RESTORE_V2.md"
QUALIFICATION = CUT / "VERA_R10A0_SD1_RESTORE_V2_QUALIFICATION.md"
RECEIPT = CUT / "VERA_R10A0_SD1_RESTORE_V2_SOURCE_RECEIPT.json"
CURRENTNESS = ROOT / "governance" / "VERA_RESTORE_V2_INSTALL_CURRENTNESS_V1.json"

FINAL_MANIFEST_SHA = "fb99689bd8e8efabf6b9612d7f1451ea9701fae3e655c6cf6dfab0f043a3aeac"
FINAL_NATIVE_SHA = "1cfc6708c4e64cebae0a4721d38eb59592239d2ba61e7c4196130162c6e5381b"
STALE_MANIFEST_SHA = "9c8cbda882f794b4237e7c447427123fcc3deb7513b2c17ec39ceb3bdd34439c"
STALE_NATIVE_SHA = "d08306e64848b55e83d5bd8dd8a258f68465812c8eddbb28670decc006858b53"


def canonical_lf_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_final_source_hashes_match_source_receipt():
    receipt = load(RECEIPT)
    manifest_bytes = canonical_lf_bytes(MANIFEST)
    native_bytes = canonical_lf_bytes(NATIVE)
    assert hashlib.sha256(manifest_bytes).hexdigest() == FINAL_MANIFEST_SHA
    assert hashlib.sha256(native_bytes).hexdigest() == FINAL_NATIVE_SHA
    assert len(manifest_bytes) == 8035
    assert len(native_bytes) == 7997
    assert receipt["manifest"]["sha256"] == FINAL_MANIFEST_SHA
    assert receipt["native"]["sha256"] == FINAL_NATIVE_SHA


def test_install_and_qualification_docs_reference_final_bytes_only():
    install = INSTALL.read_text(encoding="utf-8")
    qualification = QUALIFICATION.read_text(encoding="utf-8")
    assert FINAL_MANIFEST_SHA in install
    assert FINAL_NATIVE_SHA in install
    assert FINAL_MANIFEST_SHA in qualification
    assert STALE_MANIFEST_SHA not in install
    assert STALE_NATIVE_SHA not in install
    assert STALE_MANIFEST_SHA not in qualification


def test_currentness_contract_preserves_source_install_runtime_separation():
    current = load(CURRENTNESS)
    manifest = load(MANIFEST)
    receipt = load(RECEIPT)
    assert current["source_subject"]["main_commit"] == (
        "57bd2cd3e53bc112d7bf220ede82225f14e2e540"
    )
    assert current["source_classification"]["manifest_status"] == manifest["status"]
    assert current["source_classification"]["receipt_status"] == receipt["status"]
    assert current["source_classification"]["receipt_claim_ceiling"] == (
        receipt["claim_ceiling"]
    )
    runtime = current["runtime_currentness"]
    assert runtime["install_effect"] == "NOT_ESTABLISHED"
    assert runtime["current_route"] == "NOT_ESTABLISHED"
    assert runtime["q_recover"] == "NOT_EXECUTED_BY_THIS_EVIDENCE"
    assert runtime["user_facing_restored_claim"] == "NOT_ESTABLISHED"


def test_currentness_contract_does_not_manufacture_project_effects():
    current = load(CURRENTNESS)
    assert "NOT_PROJECT_SETTINGS_MUTATION" in current["non_effects"]
    assert "NOT_PROJECT_SOURCE_MUTATION" in current["non_effects"]
    assert "NOT_INSTALL_EFFECT" in current["non_effects"]
    assert "NOT_CURRENT_ROUTE_QUALIFICATION" in current["non_effects"]
    assert "NOT_Q_RECOVER_PASS" in current["non_effects"]
