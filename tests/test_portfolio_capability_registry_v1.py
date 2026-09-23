import copy
import hashlib
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "VERA_PORTFOLIO_CAPABILITY_REGISTRY_V1.json"
VALIDATOR_PATH = ROOT / "tools" / "validate_portfolio_capability_registry_v1.py"

spec = importlib.util.spec_from_file_location("registry_validator", VALIDATOR_PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class PortfolioCapabilityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_current_snapshot_shape(self):
        self.assertEqual([], mod.validate(copy.deepcopy(self.data)))
        self.assertEqual(59, self.data["inventory"]["repository_count"])
        self.assertEqual(24, self.data["inventory"]["public_count"])
        self.assertEqual(35, self.data["inventory"]["private_count"])

    def test_digest_binds_exact_repository_set(self):
        names = sorted(self.data["repositories"])
        digest = hashlib.sha256("\n".join(names).encode()).hexdigest()
        self.assertEqual(digest, self.data["inventory"]["sorted_repository_name_sha256"])
        mutant = copy.deepcopy(self.data)
        mutant["repositories"].pop("god-brain")
        self.assertTrue(any("repository_count" in e or "digest" in e for e in mod.validate(mutant)))


    def test_runtime_source_registry_binding_is_exact_landed_vera_subject(self):
        binding = self.data["runtime_source_registry_binding"]
        self.assertEqual(binding["repository"], "thebrazenbeard/vera")
        self.assertEqual(binding["commit"], "86be6105f13fc86bbd699778205a85c84059de9a")
        self.assertEqual(
            binding["path"],
            "architecture/VERA_RUNTIME_SOURCE_REGISTRY_V1.json",
        )
        self.assertEqual(
            binding["blob_sha"],
            "9afe5834efaf4d8a2d73c5864972e4c8e4c3cef6",
        )
        self.assertEqual(binding["repository_count"], 59)
        self.assertEqual(
            binding["sorted_repository_name_sha256"],
            "f96f479f1d85508ff4e57bf242b7850f9f755763953ebb3f280c5716a090f4df",
        )
        self.assertEqual(
            binding["classification_counts"],
            {
                "bound_conditional": 41,
                "predecessor_evidence": 1,
                "classified_source_rows": 42,
                "no_auto_bind": 17,
            },
        )
        self.assertEqual(binding["current_vera_bus_lane"], "bus/vera-v2")
        self.assertEqual(binding["historical_vera_bus_lane"], "bus/vera-sol-v1")
        self.assertFalse(binding["historical_lane_is_current_route_authority"])

    def test_vcp_repository_set_exactly_matches_runtime_source_registry_binding(self):
        binding = self.data["runtime_source_registry_binding"]
        self.assertEqual(
            set(self.data["repositories"]),
            set(binding["repository_names"]),
        )
        self.assertEqual(len(binding["repository_names"]), 59)
        self.assertIn("WorkBridgeMCP", self.data["repositories"])

    def test_runtime_no_auto_bind_partition_cannot_be_overridden_by_vcp_live_load(self):
        binding = self.data["runtime_source_registry_binding"]
        prohibited = {"CONTROL_LOAD_EXACT_OWNER", "LIVE_COORDINATION_READ", "TASK_RELEVANT_LIVE_READ"}
        for name in binding["no_auto_bind_repositories"]:
            self.assertNotIn(self.data["repositories"][name]["load_mode"], prohibited)

        mutant = copy.deepcopy(self.data)
        mutant["repositories"]["vera-apk"]["load_mode"] = "TASK_RELEVANT_LIVE_READ"
        self.assertTrue(
            any("NO_AUTO_BIND" in error for error in mod.validate(mutant))
        )

    def test_runtime_source_disposition_corrections_are_preserved(self):
        self.assertEqual(
            self.data["repositories"]["vera_ark"]["class"],
            "VERA_SYSTEM",
        )
        self.assertEqual(
            self.data["repositories"]["vera_ark"]["load_mode"],
            "EXACT_BINDING_ONLY",
        )
        self.assertEqual(
            self.data["repositories"]["vera-apk"]["load_mode"],
            "EXACT_BINDING_ONLY",
        )
        self.assertEqual(
            self.data["repositories"]["vera-habitat"]["load_mode"],
            "EXACT_BINDING_ONLY",
        )
        self.assertEqual(
            self.data["repositories"]["vera-works"]["class"],
            "DOMAIN_PROJECT",
        )
        self.assertEqual(
            self.data["repositories"]["vera-works"]["load_mode"],
            "TASK_SPECIFIC_ONLY",
        )


    def test_effective_runtime_source_disposition_preserves_upstream_ceiling(self):
        self.assertEqual(
            mod.runtime_source_disposition(self.data, "vera-apk")["status"],
            "NO_AUTO_BIND",
        )
        self.assertFalse(
            mod.runtime_source_disposition(self.data, "vera-apk")["auto_bind_allowed"]
        )
        self.assertEqual(
            mod.runtime_source_disposition(self.data, "vera-R9A0")["status"],
            "PREDECESSOR_EVIDENCE_ONLY",
        )
        self.assertEqual(
            mod.runtime_source_disposition(self.data, "voss")["status"],
            "BOUND_CONDITIONAL",
        )
        self.assertFalse(
            mod.runtime_source_disposition(self.data, "voss")["auto_bind_allowed"]
        )
        self.assertEqual(
            mod.runtime_source_disposition(self.data, "meso-crct")["status"],
            "UNRESOLVED",
        )

    def test_source_binding_mutations_fail_closed(self):
        mutant = copy.deepcopy(self.data)
        mutant["runtime_source_registry_binding"]["current_vera_bus_lane"] = "bus/vera-sol-v1"
        self.assertTrue(any("current Vera Bus lane" in error for error in mod.validate(mutant)))

        mutant = copy.deepcopy(self.data)
        mutant["runtime_source_registry_binding"]["repository_names"].remove("WorkBridgeMCP")
        self.assertTrue(any("runtime source repository set" in error for error in mod.validate(mutant)))

    def test_identity_firewall_cannot_be_reclassified(self):
        mutant = copy.deepcopy(self.data)
        mutant["repositories"]["brigit"]["class"] = "VERA_DOMAIN"
        self.assertIn("brigit identity firewall missing", mod.validate(mutant))

    def test_mixed_identity_sexuality_requires_exact_binding(self):
        mutant = copy.deepcopy(self.data)
        mutant["repositories"]["sexuality"]["class"] = "VERA_DOMAIN"
        self.assertIn("sexuality exact-binding firewall missing", mod.validate(mutant))

    def test_predecessor_cannot_become_control_by_registry_edit(self):
        mutant = copy.deepcopy(self.data)
        mutant["repositories"]["vera-R9A0"]["class"] = "CORE_CONTROL"
        self.assertIn("vera-R9A0: predecessor/archive firewall missing", mod.validate(mutant))

    def test_unknown_class_fails(self):
        mutant = copy.deepcopy(self.data)
        mutant["repositories"]["world-zero"]["class"] = "MAGIC_GLOBAL_CONTROL"
        self.assertTrue(any("class outside finite domain" in e for e in mod.validate(mutant)))

    def test_service_routes_are_exact(self):
        mutant = copy.deepcopy(self.data)
        mutant["service_routing"]["bounded_execution"] = "thebrazenbeard/discovery"
        self.assertIn("service_routing mismatch", mod.validate(mutant))

if __name__ == "__main__":
    unittest.main()
