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
        self.assertEqual(58, self.data["inventory"]["repository_count"])
        self.assertEqual(23, self.data["inventory"]["public_count"])
        self.assertEqual(35, self.data["inventory"]["private_count"])

    def test_digest_binds_exact_repository_set(self):
        names = sorted(self.data["repositories"])
        digest = hashlib.sha256("\n".join(names).encode()).hexdigest()
        self.assertEqual(digest, self.data["inventory"]["sorted_repository_name_sha256"])
        mutant = copy.deepcopy(self.data)
        mutant["repositories"].pop("god-brain")
        self.assertTrue(any("repository_count" in e or "digest" in e for e in mod.validate(mutant)))

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
