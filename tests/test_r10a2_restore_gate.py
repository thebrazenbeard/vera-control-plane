from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_restore_completion.py"
CONTRACT = ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_COMPLETION_GATE.json"
REGISTRY = ROOT / "project-instructions/r10a2/VERA_R10A2_CONTROL_REGISTRY.json"


def load_validator():
    spec = spec_from_file_location("restore_validator", SCRIPT)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def normalized_sha256(text):
    normalized = " ".join(text.strip().split()).casefold()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def expectations():
    return {
        "SELF_IDENTITY": {"mode": "EXACT_NORMALIZED", "expected": "vera"},
        "RELATIONSHIP_IDENTITY": {"mode": "SHA256_TEXT", "expected_sha256": normalized_sha256("relation-alpha")},
        "CURRENTNESS_TYPING": {
            "mode": "JSON_EQUAL",
            "expected": {"relationship": "CURRENT", "desire": "UNKNOWN", "consent": "UNKNOWN", "authority": "SCOPED"},
        },
        "ACTIVE_FRONTIER": {"mode": "SHA256_TEXT", "expected_sha256": normalized_sha256("frontier-alpha")},
    }


def complete_receipt():
    return {
        "schema": "VERA_RESTORE_COMPLETION_RECEIPT_V2",
        "release": "R10A2",
        "trigger": "restore yourself",
        "control": {
            "control_id": "REC_RECOVERY",
            "base_owner_id": "R10A0_DOMAIN_CONTROLS",
            "base_section": "REC_RECOVERY",
            "base_owner_loaded": True,
            "base_owner_subject_verified": True,
            "delta_owner_id": "RESTORE_HARDENING_OWNER",
            "delta_section": "RESTORE_COMPLETE",
            "delta_owner_loaded": True,
            "delta_owner_subject_verified": True,
        },
        "live_input": {"preserved_separately": True, "outranks_conflicting_restored_frontier": True},
        "discovery": {
            "surfaces_checked": ["VCP_STATE_REFS", "VCP_SAVE_REFS", "BUS_VERA_ROUTE"],
            "candidates": [
                {"id": "older-state", "source_surface": "VCP_STATE_REFS", "observed_at": "2026-09-13T19:43:07-04:00", "eligible": True, "integrity_verified": True, "referent": "VERA", "probe_expectations": expectations()},
                {"id": "latest-save", "source_surface": "VCP_SAVE_REFS", "observed_at": "2026-09-16T09:15:00-04:00", "eligible": True, "integrity_verified": True, "referent": "VERA", "probe_expectations": expectations()},
            ],
            "selected_candidate_id": "latest-save",
            "newest_eligible_selection_verified": True,
        },
        "reconciliation": {
            "stable_relational_identity": {"source_candidate_id": "latest-save", "proposition_type": "RELATIONAL_IDENTITY", "state": "CURRENT_REESTABLISHED"},
            "historical_conation_promoted": False,
            "standing_consent_promoted": False,
            "operational_authority_promoted": False,
            "unresolved_material_conflicts": [],
        },
        "mutable_refresh": {"authority_currentness_provider_frontier_refreshed": True, "unstable_material_sources": []},
        "behavioral_probes": {
            "SELF_IDENTITY": {"source_candidate_id": "latest-save", "evidence": {"evidence_route": "FIRST_ELIGIBLE_BEHAVIOR", "value": "Vera"}},
            "RELATIONSHIP_IDENTITY": {"source_candidate_id": "latest-save", "evidence": {"evidence_route": "FIRST_ELIGIBLE_BEHAVIOR", "value": "relation-alpha"}},
            "CURRENTNESS_TYPING": {"source_candidate_id": "latest-save", "evidence": {"evidence_route": "FIRST_ELIGIBLE_BEHAVIOR", "value": {"relationship": "CURRENT", "desire": "UNKNOWN", "consent": "UNKNOWN", "authority": "SCOPED"}}},
            "ACTIVE_FRONTIER": {"source_candidate_id": "latest-save", "evidence": {"evidence_route": "FIRST_ELIGIBLE_BEHAVIOR", "value": "frontier-alpha"}},
        },
        "completion": {"status": "RESTORED", "restored_claim_permitted": True},
    }


class RestoreGateSourceTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.contract = contract()

    def assert_error(self, receipt, fragment):
        errors = self.validator.validate_receipt(receipt, self.contract)
        self.assertTrue(any(fragment in error for error in errors), msg=f"expected {fragment!r}; got {errors!r}")

    def test_complete_receipt_passes(self):
        self.assertEqual(self.validator.validate_receipt(complete_receipt(), self.contract), [])

    def test_composed_recovery_owner_is_required(self):
        for field in ["base_owner_loaded", "base_owner_subject_verified", "delta_owner_loaded", "delta_owner_subject_verified"]:
            receipt = complete_receipt(); receipt["control"][field] = False
            self.assert_error(receipt, "not loaded/verified")

    def test_control_only_restore_cannot_complete(self):
        receipt = complete_receipt(); receipt["behavioral_probes"] = {}
        self.assert_error(receipt, "evidence missing")

    def test_missing_save_namespace_fails_closed(self):
        receipt = complete_receipt(); receipt["discovery"]["surfaces_checked"] = ["VCP_STATE_REFS", "BUS_VERA_ROUTE"]
        self.assert_error(receipt, "VCP_SAVE_REFS")

    def test_older_eligible_snapshot_cannot_win(self):
        receipt = complete_receipt(); receipt["discovery"]["selected_candidate_id"] = "older-state"; receipt["discovery"]["newest_eligible_selection_verified"] = False
        self.assert_error(receipt, "newest eligible")

    def test_equal_time_newest_candidates_fail_closed(self):
        receipt = complete_receipt(); tied = deepcopy(receipt["discovery"]["candidates"][1]); tied["id"] = "latest-save-z"; receipt["discovery"]["candidates"].append(tied); receipt["discovery"]["selected_candidate_id"] = "latest-save-z"
        self.assert_error(receipt, "ambiguous newest")

    def test_relationship_identity_cannot_be_laundered_into_historical_conation(self):
        receipt = complete_receipt(); receipt["reconciliation"]["stable_relational_identity"]["proposition_type"] = "HISTORICAL_CONATION"
        self.assert_error(receipt, "RELATIONAL_IDENTITY")

    def test_relationship_identity_does_not_create_consent_or_authority(self):
        receipt = complete_receipt(); receipt["reconciliation"]["standing_consent_promoted"] = True
        self.assert_error(receipt, "standing consent")
        receipt = complete_receipt(); receipt["reconciliation"]["operational_authority_promoted"] = True
        self.assert_error(receipt, "operational authority")

    def test_live_input_must_remain_separate_and_superior(self):
        receipt = complete_receipt(); receipt["live_input"]["preserved_separately"] = False
        self.assert_error(receipt, "LIVE_INPUT")

    def test_material_conflict_or_unstable_refresh_blocks_restored_claim(self):
        receipt = complete_receipt(); receipt["reconciliation"]["unresolved_material_conflicts"] = ["relationship/currentness"]
        self.assert_error(receipt, "material conflict")
        receipt = complete_receipt(); receipt["mutable_refresh"]["unstable_material_sources"] = ["bus topology"]
        self.assert_error(receipt, "unstable material source")

    def test_naked_or_forged_probe_pass_is_rejected(self):
        receipt = complete_receipt(); receipt["behavioral_probes"]["RELATIONSHIP_IDENTITY"] = {"source_candidate_id": "latest-save", "status": "PASS", "evidence": {"evidence_route": "FIRST_ELIGIBLE_BEHAVIOR", "value": "primary human counterpart"}}
        self.assert_error(receipt, "RELATIONSHIP_IDENTITY evidence mismatch")

    def test_each_probe_value_is_actually_evaluated(self):
        mutations = {
            "SELF_IDENTITY": "generic assistant",
            "RELATIONSHIP_IDENTITY": "generic counterpart",
            "CURRENTNESS_TYPING": {"relationship": "HISTORICAL", "desire": "CURRENT", "consent": "STANDING", "authority": "GLOBAL"},
            "ACTIVE_FRONTIER": "unknown",
        }
        for probe, bad_value in mutations.items():
            receipt = complete_receipt(); receipt["behavioral_probes"][probe]["evidence"]["value"] = bad_value
            self.assert_error(receipt, f"{probe} evidence mismatch")

    def test_wrong_probe_route_is_rejected(self):
        receipt = complete_receipt(); receipt["behavioral_probes"]["SELF_IDENTITY"]["evidence"]["evidence_route"] = "POST_HOC"
        self.assert_error(receipt, "SELF_IDENTITY evidence mismatch")

    def test_restored_claim_requires_explicit_gate_permission(self):
        receipt = complete_receipt(); receipt["completion"]["restored_claim_permitted"] = False
        self.assert_error(receipt, "RESTORED claim")

    def test_restore_owner_preserves_all_twelve_inherited_steps(self):
        text = (ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_HARDENING.md").read_text(encoding="utf-8")
        self.assertIn("All twelve numbered recovery steps remain binding unchanged", text)
        self.assertIn("REC_RECOVERY = R10A0_DOMAIN_CONTROLS#REC_RECOVERY -> RESTORE_HARDENING_OWNER#RESTORE_COMPLETE", text)

    def test_hostile_regression_covers_repair_cases(self):
        text = (ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_REGRESSION.md").read_text(encoding="utf-8")
        for case_id in [f"RST-{i:02d}" for i in range(1, 15)]:
            self.assertIn(case_id, text)

    def test_registry_composes_exact_inherited_owner_and_delta(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        base = registry["owners"]["R10A0_DOMAIN_CONTROLS"]
        self.assertEqual(base["source_commit"], "2d60cd8e87ac0aae89a5a9bd9a44bfb63f48aa64")
        self.assertEqual(base["git_blob"], "1aa3fc83f88d7151a7307720149ebb10bdd1b8b7")
        self.assertEqual(registry["controls"]["REC_RECOVERY"]["composition"], "BASE_THEN_COMPLETION_DELTA")
        self.assertEqual(registry["controls"]["REC_RECOVERY"]["inherited_step_set"], list(range(1, 13)))

    def test_registry_artifact_bindings_match_bytes(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(self.validator.validate_source_bindings(ROOT, registry), [])

    def test_native_delta_remains_small_and_requires_composition(self):
        text = (ROOT / "project-instructions/r10a2/VERA_R10A2_NATIVE_DELTA.txt").read_text(encoding="utf-8")
        self.assertIn("composed `REC_RECOVERY`", text)
        self.assertLessEqual(len(text.encode("utf-8")), 400)


if __name__ == "__main__":
    unittest.main()
