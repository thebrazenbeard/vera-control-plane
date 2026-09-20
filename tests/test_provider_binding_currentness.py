import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_CONTROL_PLANE_PROVIDER_BINDING_V1.json"


class ProviderBindingTests(unittest.TestCase):
    def setUp(self):
        self.binding = json.loads(BINDING.read_text(encoding="utf-8"))

    def test_binding_is_exact_and_readback_only(self):
        self.assertEqual(self.binding["schema"], "VERA_CONTROL_PLANE_PROVIDER_BINDING_V1")
        provider = self.binding["provider"]
        self.assertEqual(provider["project_id"], "fawkirqroyniueeqspif")
        self.assertEqual(provider["project_name"], "Vera Control Plane")
        self.assertEqual(provider["activation_mode"], "PROVIDER_READBACK_ONLY")
        self.assertFalse(provider["availability_implies_activation"])

    def test_sd1_anchor_is_genesis_not_causal_activation(self):
        anchor = self.binding["sd1_anchor_readback"]
        self.assertEqual(anchor["witness_id"], "VERA_SD1_CAUSAL_V1")
        self.assertEqual(anchor["generation"], 0)
        self.assertEqual(anchor["record_count"], 0)
        self.assertEqual(anchor["mutation_receipts"], 0)
        self.assertIn("CONTROLLER_BINDING_UNESTABLISHED", anchor["classification"])
        self.assertIn("REAL_CAUSAL_COLLECTION_UNESTABLISHED", anchor["classification"])

    def test_binding_does_not_self_authorize_provider_mutation(self):
        boundary = " ".join(self.binding["effect_boundary"])
        self.assertIn("separate exact Patrick authority", boundary)
        self.assertIn("does not rewrite frozen/native R10", boundary)


if __name__ == "__main__":
    unittest.main()
