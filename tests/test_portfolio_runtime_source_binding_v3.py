import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance/VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3.json"
CAPABILITY = ROOT / "governance/VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"
VALIDATOR = ROOT / "tools/validate_portfolio_runtime_source_binding_v3.py"
BUILDER = ROOT / "tools/build_portfolio_runtime_source_binding_v3.py"

spec = importlib.util.spec_from_file_location("binding_v3", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PortfolioRuntimeSourceBindingV3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(BINDING.read_text(encoding="utf-8"))
        cls.capability = json.loads(CAPABILITY.read_text(encoding="utf-8"))

    def row(self, repository):
        return next(row for row in self.data["public_sources"] if row["repository"] == repository)

    def test_exact_subject_validates(self):
        self.assertEqual([], mod.validate(copy.deepcopy(self.data), self.capability))
        self.assertEqual(self.data["upstream"]["pull_request"], 206)
        self.assertEqual(self.data["upstream"]["head"], "dff171a8cee0b2dd3c6fd4627499330800499fdd")
        self.assertEqual(self.data["qualification"]["pull_request"], 95)
    def test_builder_is_deterministic(self):
        before = BINDING.read_bytes()
        subprocess.run([sys.executable, str(BUILDER)], cwd=ROOT, check=True, capture_output=True)
        self.assertEqual(before, BINDING.read_bytes())

    def test_private_membership_is_count_only(self):
        private = self.data["private_inventory"]
        self.assertEqual(private["public_commitment_scheme"], "COUNT_ONLY_PUBLIC_V1")
        self.assertFalse(private["exact_membership_publicly_committed"])
        self.assertFalse(private["membership_names_present"])
        for key in ("repositories", "members", "names"):
            self.assertNotIn(key, private)

    def test_public_membership_matches_exact_vendored_cut(self):
        cut = json.loads(mod.CUT.read_text(encoding="utf-8"))
        expected = {row["repository"] for row in cut["public_records"]}
        actual = {row["repository"] for row in self.data["public_sources"]}
        self.assertEqual(expected, actual)
        self.assertEqual(len(actual), self.data["cut_counts"]["public"])

    def test_explicit_pr206_no_auto_bind_is_enforced(self):
        row = self.row("thebrazenbeard/vera-mono")
        self.assertEqual(row["source_activation_mode"], "NO_AUTO_BIND")
        self.assertEqual(row["runtime_source_disposition"], "NO_AUTO_BIND")
        self.assertFalse(mod.runtime_source_disposition(self.data, row["repository"])["auto_bind_allowed"])
    def test_predecessor_no_auto_bind_is_fail_closed_floor(self):
        row = self.row("thebrazenbeard/freerowcochkar")
        self.assertEqual(row["source_activation_mode"], "MECHANISM_RESEARCH_ONLY")
        self.assertEqual(row["predecessor_v2_disposition"], "NO_AUTO_BIND")
        self.assertEqual(row["runtime_source_disposition"], "NO_AUTO_BIND")

    def test_predecessor_evidence_never_becomes_current_control(self):
        row = self.row("thebrazenbeard/vera-R9A0")
        self.assertEqual(row["runtime_source_disposition"], "PREDECESSOR_EVIDENCE_ONLY")
        result = mod.runtime_source_disposition(self.data, row["repository"])
        self.assertEqual(result["status"], "PREDECESSOR_EVIDENCE_ONLY")
        self.assertFalse(result["auto_bind_allowed"])

    def test_no_auto_bind_blocks_live_capability_modes(self):
        mutant = copy.deepcopy(self.capability)
        mutant["repositories"]["vera-mono"] = {
            "class": "VERA_SYSTEM",
            "load_mode": "TASK_RELEVANT_LIVE_READ",
            "capability": "mutant",
            "boundary": "mutant",
            "visibility": "public",
        }
        errors = mod.validate(self.data, mutant)
        self.assertTrue(any("NO_AUTO_BIND source cannot use VCP load mode" in e for e in errors))

    def test_outside_cut_and_private_fail_closed(self):
        outside = mod.runtime_source_disposition(self.data, "thebrazenbeard/post-cut-repository")
        self.assertEqual(outside["status"], "UNRESOLVED")
        self.assertFalse(outside["auto_bind_allowed"])
        private = mod.runtime_source_disposition(self.data, "opaque-private", private_source=True)
        self.assertEqual(private["status"], "PRIVATE_EXACT_BINDING_REQUIRED")
        self.assertFalse(private["auto_bind_allowed"])
    def test_head_drift_is_currentness_failure_not_cut_corruption(self):
        row = self.row("thebrazenbeard/discovery")
        result = mod.runtime_source_disposition(self.data, row["repository"], current_head="f" * 40)
        self.assertEqual(result["status"], "STALE_CURRENTNESS")
        self.assertFalse(result["auto_bind_allowed"])
        self.assertEqual(result["source_disposition"], row["runtime_source_disposition"])

    def test_capability_registry_routes_activation_through_v3_binding(self):
        rules = self.capability["global_rules"]
        self.assertIn(
            "VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3_GOVERNS_ACTIVATION_DISPOSITION",
            rules,
        )
        self.assertNotIn(
            "VERA_RUNTIME_SOURCE_REGISTRY_GOVERNS_ACTIVATION_DISPOSITION",
            rules,
        )

    def test_no_fixed_legacy_partition_constants_drive_policy(self):
        raw = VALIDATOR.read_text(encoding="utf-8")
        self.assertNotIn("EXPECTED_NO_AUTO_BIND", raw)
        self.assertNotIn('"total":59', raw)
        self.assertNotIn('"no_auto_bind":17', raw)
        self.assertEqual(self.data["cardinality_semantics"], "CUT_LOCAL_FACTS_ONLY_NOT_PERMANENT_POLICY_INVARIANTS")

if __name__ == "__main__":
    unittest.main()
