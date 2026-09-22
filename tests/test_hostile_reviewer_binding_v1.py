import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_HOSTILE_REVIEWER_BINDING_V1.json"


class HostileReviewerBindingTests(unittest.TestCase):
    def test_binding_pins_repaired_runtime_exactly(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        runtime = data["runtime"]
        self.assertEqual("44bd82b07ced00cabf800c6ee36bf096a363b797", runtime["source_commit"])
        self.assertEqual("ecdf279a231e2469aa202098250fe30981aa900e", runtime["architecture_contract"]["blob"])
        self.assertEqual("da14b1f4fbfa587157dce1a7ce409313c7bda9a1", runtime["runtime_module"]["blob"])
        self.assertEqual("23b93c30a89bcd8002847a7a53d89eb145ef4e22", runtime["package_init"]["blob"])
        self.assertEqual("381d71150561b4fb28e6eec6cc454a335bef24cc", runtime["focused_test"]["blob"])

    def test_binding_pins_current_main_control_cut(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        control = data["control_plane"]
        self.assertEqual("47fb9175020d10c1d6a6e70ae81d7f971d32d578", control["source_commit"])
        self.assertEqual("4e763372d28c844d35373ded64d1a231bf54e411", control["control_contract"]["blob"])
        self.assertEqual("8b59faac8985c1bd237ee3f72a9ff466df80a097", control["source_state"]["blob"])
        self.assertEqual("ddfc2ee230c821d867ed3aa2ac72e96f57b3678c", control["toggle_tool"]["blob"])
        self.assertEqual("281dd03876c5c5b444fb4ccb3359954baee53239", control["focused_test"]["blob"])

    def test_typed_contract_and_lifecycle_ceiling_are_explicit(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        typed = data["runtime"]["typed_contract"]
        self.assertEqual("LiteralProposition", typed["input"])
        self.assertEqual("HostileReviewDecision", typed["output"])
        self.assertTrue(typed["proposition_digest_bound"])
        self.assertTrue(typed["primary_answer_digest_bound"])
        self.assertTrue(typed["zero_objection_survival_allowed"])
        self.assertTrue(typed["stronger_route_guarded"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["install"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["runtime_consumption"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["behavioral_qualification"])


if __name__ == "__main__":
    unittest.main()
