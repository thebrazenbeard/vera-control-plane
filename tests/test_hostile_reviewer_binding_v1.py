import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_HOSTILE_REVIEWER_BINDING_V1.json"

class HostileReviewerBindingTests(unittest.TestCase):
    def test_binding_keeps_source_and_runtime_lifecycle_separate(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        self.assertEqual("IMPLEMENTED_AND_EXACT_BOUND", data["lifecycle"]["source"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["install"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["runtime_consumption"])
        self.assertEqual("NOT_ESTABLISHED", data["lifecycle"]["behavioral_qualification"])

    def test_binding_records_focused_pass_and_hosted_ci_red_separately(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        self.assertEqual("PASS", data["focused_validation"]["runtime"]["result"])
        self.assertEqual("8/8", data["focused_validation"]["runtime"]["assertions"])
        self.assertEqual("PASS", data["focused_validation"]["control_plane"]["result"])
        self.assertEqual("6/6", data["focused_validation"]["control_plane"]["assertions"])
        self.assertEqual("BRANCH_WIDE_RED", data["hosted_ci"]["status"])

    def test_binding_pins_exact_runtime_and_control_blobs(self):
        data = json.loads(BINDING.read_text(encoding="utf-8"))
        self.assertEqual(
            "fe63a265ed6f5da695f0f4d6dc197f3529c0b037",
            data["runtime"]["runtime_module"]["blob"],
        )
        self.assertEqual(
            "71fa08d2221744a139eb854af549ace2997b58b0",
            data["control_plane"]["control_contract"]["blob"],
        )

if __name__ == "__main__":
    unittest.main()
