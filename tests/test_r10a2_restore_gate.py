from copy import deepcopy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/validate_restore_completion.py"
CONTRACT = ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_COMPLETION_GATE.json"


def load_validator():
    spec = spec_from_file_location("restore_validator", SCRIPT)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def complete_receipt():
    return {
        "schema": "VERA_RESTORE_COMPLETION_RECEIPT_V1",
        "release": "R10A2",
        "trigger": "restore yourself",
        "control": {
            "control_id": "REC_RECOVERY",
            "owner_loaded": True,
            "owner_subject_verified": True,
        },
        "live_input": {
            "preserved_separately": True,
            "outranks_conflicting_restored_frontier": True,
        },
        "discovery": {
            "surfaces_checked": ["VCP_STATE_REFS", "VCP_SAVE_REFS", "BUS_VERA_ROUTE"],
            "candidates": [
                {
                    "id": "older-state",
                    "source_surface": "VCP_STATE_REFS",
                    "observed_at": "2026-09-13T19:43:07-04:00",
                    "eligible": True,
                    "integrity_verified": True,
                    "referent": "VERA",
                },
                {
                    "id": "latest-save",
                    "source_surface": "VCP_SAVE_REFS",
                    "observed_at": "2026-09-16T09:15:00-04:00",
                    "eligible": True,
                    "integrity_verified": True,
                    "referent": "VERA",
                },
            ],
            "selected_candidate_id": "latest-save",
            "newest_eligible_selection_verified": True,
        },
        "reconciliation": {
            "stable_relational_identity": {
                "source_candidate_id": "latest-save",
                "proposition_type": "RELATIONAL_IDENTITY",
                "state": "CURRENT_REESTABLISHED",
            },
            "historical_conation_promoted": False,
            "standing_consent_promoted": False,
            "operational_authority_promoted": False,
            "unresolved_material_conflicts": [],
        },
        "mutable_refresh": {
            "authority_currentness_provider_frontier_refreshed": True,
            "unstable_material_sources": [],
        },
        "behavioral_probes": {
            "SELF_IDENTITY": {"status": "PASS", "source_candidate_id": "latest-save"},
            "RELATIONSHIP_IDENTITY": {"status": "PASS", "source_candidate_id": "latest-save"},
            "CURRENTNESS_TYPING": {"status": "PASS", "source_candidate_id": "latest-save"},
            "ACTIVE_FRONTIER": {"status": "PASS", "source_candidate_id": "latest-save"},
        },
        "completion": {
            "status": "RESTORED",
            "restored_claim_permitted": True,
        },
    }


class RestoreGateSourceTests(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator()
        self.contract = contract()

    def assert_error(self, receipt, fragment):
        errors = self.validator.validate_receipt(receipt, self.contract)
        self.assertTrue(
            any(fragment in error for error in errors),
            msg=f"expected error containing {fragment!r}; got {errors!r}",
        )

    def test_restore_completion_validator_exists(self):
        self.assertTrue(SCRIPT.is_file())

    def test_validator_exposes_receipt_validation_api(self):
        self.assertTrue(hasattr(self.validator, "validate_receipt"))

    def test_restore_completion_contract_exists_and_names_hard_gates(self):
        self.assertEqual(self.contract["schema"], "VERA_R10A2_RESTORE_COMPLETION_GATE_V1")
        self.assertEqual(
            self.contract["required_discovery_surfaces"],
            ["VCP_STATE_REFS", "VCP_SAVE_REFS", "BUS_VERA_ROUTE"],
        )
        self.assertEqual(
            self.contract["required_behavioral_probes"],
            ["SELF_IDENTITY", "RELATIONSHIP_IDENTITY", "CURRENTNESS_TYPING", "ACTIVE_FRONTIER"],
        )

    def test_control_only_restore_cannot_complete(self):
        receipt = complete_receipt()
        receipt["behavioral_probes"] = {}
        self.assert_error(receipt, "behavioral probe")

    def test_missing_save_namespace_fails_closed(self):
        receipt = complete_receipt()
        receipt["discovery"]["surfaces_checked"] = ["VCP_STATE_REFS", "BUS_VERA_ROUTE"]
        self.assert_error(receipt, "VCP_SAVE_REFS")

    def test_older_eligible_snapshot_cannot_win_over_newer_eligible_snapshot(self):
        receipt = complete_receipt()
        receipt["discovery"]["selected_candidate_id"] = "older-state"
        receipt["discovery"]["newest_eligible_selection_verified"] = False
        self.assert_error(receipt, "newest eligible")

    def test_relationship_identity_cannot_be_laundered_into_historical_conation(self):
        receipt = complete_receipt()
        receipt["reconciliation"]["stable_relational_identity"]["proposition_type"] = "HISTORICAL_CONATION"
        self.assert_error(receipt, "RELATIONAL_IDENTITY")

    def test_relationship_identity_does_not_create_consent_or_authority(self):
        receipt = complete_receipt()
        receipt["reconciliation"]["standing_consent_promoted"] = True
        self.assert_error(receipt, "standing consent")
        receipt = complete_receipt()
        receipt["reconciliation"]["operational_authority_promoted"] = True
        self.assert_error(receipt, "operational authority")

    def test_live_input_must_remain_separate_and_superior_to_conflicting_restore(self):
        receipt = complete_receipt()
        receipt["live_input"]["preserved_separately"] = False
        self.assert_error(receipt, "LIVE_INPUT")
        receipt = complete_receipt()
        receipt["live_input"]["outranks_conflicting_restored_frontier"] = False
        self.assert_error(receipt, "LIVE_INPUT")

    def test_material_conflict_or_unstable_refresh_blocks_restored_claim(self):
        receipt = complete_receipt()
        receipt["reconciliation"]["unresolved_material_conflicts"] = ["relationship/currentness"]
        self.assert_error(receipt, "material conflict")
        receipt = complete_receipt()
        receipt["mutable_refresh"]["unstable_material_sources"] = ["bus topology"]
        self.assert_error(receipt, "unstable material source")

    def test_restored_claim_requires_explicit_gate_permission(self):
        receipt = complete_receipt()
        receipt["completion"]["restored_claim_permitted"] = False
        self.assert_error(receipt, "RESTORED claim")

    def test_restore_protocol_binds_completion_before_success_language(self):
        path = ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_HARDENING.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for required in [
            "RESTORE_COMPLETE",
            "VCP_STATE_REFS",
            "VCP_SAVE_REFS",
            "BUS_VERA_ROUTE",
            "RELATIONAL_IDENTITY",
            "SELF_IDENTITY",
            "RELATIONSHIP_IDENTITY",
            "CURRENTNESS_TYPING",
            "ACTIVE_FRONTIER",
            "must not say `Restored`",
        ]:
            self.assertIn(required, text)

    def test_hostile_regression_covers_today_failure_class(self):
        path = ROOT / "project-instructions/r10a2/VERA_R10A2_RESTORE_REGRESSION.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        for case_id in [f"RST-{i:02d}" for i in range(1, 11)]:
            self.assertIn(case_id, text)
        self.assertIn("namespace miss", text.lower())
        self.assertIn("generic counterpart", text.lower())
        self.assertIn("standing consent", text.lower())

    def test_r10a2_registry_supersedes_only_recovery_control(self):
        path = ROOT / "project-instructions/r10a2/VERA_R10A2_CONTROL_REGISTRY.json"
        self.assertTrue(path.is_file())
        registry = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(registry["release"], "R10A2")
        self.assertEqual(registry["base_r10a1_main"], "b4d9aaa8560de12252dd29996379b0af8e0ca0d1")
        self.assertEqual(registry["controls"]["REC_RECOVERY"]["owner"], "RESTORE_HARDENING_OWNER")
        self.assertEqual(registry["controls"]["SALIENCE_ARBITRATION"]["inherited_from"], "R10A1")
        self.assertIn("not installation", registry["non_effects"])

    def test_native_delta_is_small_and_blocks_false_complete(self):
        path = ROOT / "project-instructions/r10a2/VERA_R10A2_NATIVE_DELTA.txt"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("restore yourself", text)
        self.assertIn("RESTORE_COMPLETE", text)
        self.assertIn("REC_RECOVERY", text)
        self.assertLessEqual(len(text.encode("utf-8")), 300)

    def test_complete_receipt_passes(self):
        self.assertEqual(self.validator.validate_receipt(complete_receipt(), self.contract), [])


if __name__ == "__main__":
    unittest.main()
