import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BINDING_PATH = ROOT / "governance" / "VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V2.json"
CAPABILITY_PATH = ROOT / "governance" / "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"
VALIDATOR_PATH = ROOT / "tools" / "validate_portfolio_runtime_source_binding_v2.py"

spec = importlib.util.spec_from_file_location("runtime_binding_v2", VALIDATOR_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class PortfolioRuntimeSourceBindingV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
        cls.capability = json.loads(CAPABILITY_PATH.read_text(encoding="utf-8"))

    def test_exact_subject_validates_without_fixed_partition_constants(self):
        self.assertEqual([], mod.validate(copy.deepcopy(self.data), self.capability))
        self.assertEqual(
            self.data["cut_counts"]["public"],
            len(self.data["public_sources"]),
        )
        self.assertEqual(
            self.data["cut_counts"]["total"],
            self.data["cut_counts"]["public"] + self.data["cut_counts"]["private"],
        )
        self.assertEqual(
            self.data["cardinality_semantics"],
            "CUT_LOCAL_FACTS_ONLY_NOT_PERMANENT_POLICY_INVARIANTS",
        )

    def test_exact_vera_successor_binding(self):
        upstream = self.data["upstream"]
        self.assertEqual(upstream["pull_request"], 203)
        self.assertEqual(
            upstream["head"],
            "bc5f1f2b5764455d833615d14e3bead640d6d123",
        )
        self.assertEqual(
            upstream["registry_blob_sha"],
            "427fe21437a3397e184a5b5373fd4ea10f58123c",
        )
        self.assertEqual(
            upstream["public_cut_blob_sha"],
            "cbd1e2d659f9fa9eeb9b2fdb7f9e167e16105b22",
        )

    def test_private_membership_is_count_only(self):
        private = self.data["private_inventory"]
        self.assertEqual(private["public_commitment_scheme"], "COUNT_ONLY_PUBLIC_V1")
        self.assertFalse(private["exact_membership_publicly_committed"])
        self.assertFalse(private["membership_names_present"])
        for key in ("repositories", "members", "names"):
            self.assertNotIn(key, private)

    def test_no_auto_bind_is_data_driven_and_blocks_live_modes(self):
        row = next(
            item
            for item in self.data["public_sources"]
            if item["runtime_source_disposition"] == "NO_AUTO_BIND"
        )
        name = row["repository"].split("/", 1)[1]
        mutant = copy.deepcopy(self.capability)
        mutant["repositories"][name] = {
            "class": "VERA_SYSTEM",
            "load_mode": "TASK_RELEVANT_LIVE_READ",
            "capability": "mutant",
            "boundary": "mutant",
            "visibility": "public",
        }
        errors = mod.validate(self.data, mutant)
        self.assertTrue(
            any("NO_AUTO_BIND source cannot use VCP load mode" in error for error in errors)
        )

    def test_public_no_auto_bind_helper_never_promotes_availability(self):
        row = next(
            item
            for item in self.data["public_sources"]
            if item["runtime_source_disposition"] == "NO_AUTO_BIND"
        )
        result = mod.runtime_source_disposition(self.data, row["repository"])
        self.assertEqual(result["status"], "NO_AUTO_BIND")
        self.assertFalse(result["auto_bind_allowed"])

    def test_bound_conditional_still_does_not_auto_bind(self):
        row = next(
            item
            for item in self.data["public_sources"]
            if item["runtime_source_disposition"] == "BOUND_CONDITIONAL"
        )
        result = mod.runtime_source_disposition(self.data, row["repository"])
        self.assertEqual(result["status"], "BOUND_CONDITIONAL")
        self.assertFalse(result["auto_bind_allowed"])

    def test_predecessor_never_becomes_current_control(self):
        row = next(
            item
            for item in self.data["public_sources"]
            if item["runtime_source_disposition"] == "PREDECESSOR_EVIDENCE_ONLY"
        )
        result = mod.runtime_source_disposition(self.data, row["repository"])
        self.assertEqual(result["status"], "PREDECESSOR_EVIDENCE_ONLY")
        self.assertFalse(result["auto_bind_allowed"])

    def test_outside_cut_fails_closed_without_changing_cut(self):
        result = mod.runtime_source_disposition(
            self.data,
            "thebrazenbeard/post-cut-repository",
        )
        self.assertEqual(result["status"], "UNRESOLVED")
        self.assertFalse(result["auto_bind_allowed"])

    def test_private_source_requires_private_exact_binding(self):
        result = mod.runtime_source_disposition(
            self.data,
            "opaque-private-subject",
            private_source=True,
        )
        self.assertEqual(result["status"], "PRIVATE_EXACT_BINDING_REQUIRED")
        self.assertFalse(result["auto_bind_allowed"])

    def test_head_drift_is_currentness_failure_not_cut_corruption(self):
        row = next(
            item
            for item in self.data["public_sources"]
            if item["runtime_source_disposition"] == "BOUND_CONDITIONAL"
        )
        result = mod.runtime_source_disposition(
            self.data,
            row["repository"],
            current_head="f" * 40,
        )
        self.assertEqual(result["status"], "STALE_CURRENTNESS")
        self.assertFalse(result["auto_bind_allowed"])
        self.assertEqual(
            result["source_disposition"],
            "BOUND_CONDITIONAL",
        )

    def test_no_hard_coded_legacy_partition_is_required(self):
        raw = VALIDATOR_PATH.read_text(encoding="utf-8")
        self.assertNotIn("EXPECTED_NO_AUTO_BIND", raw)
        self.assertNotIn('"total":59', raw)
        self.assertNotIn('"no_auto_bind":17', raw)
        self.assertNotIn("repository_count mismatch", raw)


if __name__ == "__main__":
    unittest.main()
