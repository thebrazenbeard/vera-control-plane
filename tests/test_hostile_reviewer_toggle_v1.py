import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "hostile_reviewer_toggle.py"
CONTROL = ROOT / "governance" / "VERA_HOSTILE_REVIEWER_CONTROL_V1.json"
SOURCE_STATE = ROOT / "state" / "features" / "hostile-reviewer-v1.json"
PATCH = (
    ROOT
    / "project-instructions"
    / "r10a0"
    / "hostile-reviewer"
    / "HOSTILE_REVIEWER_BEHAVIOR_PATCH_V1.md"
)

spec = importlib.util.spec_from_file_location("hostile_reviewer_toggle", TOOL)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class HostileReviewerToggleTests(unittest.TestCase):
    def test_control_contract_is_binary_and_all_chat_scoped(self):
        data = json.loads(CONTROL.read_text(encoding="utf-8"))
        self.assertEqual(["OFF", "ON"], data["allowed_modes"])
        self.assertEqual("OFF", data["default_mode"])
        self.assertEqual("VERA_PROJECT_ALL_CHATS", data["durable_scope"])
        self.assertIn("NO_AUTHORITY", data["authority_ceiling"])

    def test_source_state_defaults_off_without_false_install_claim(self):
        data = json.loads(SOURCE_STATE.read_text(encoding="utf-8"))
        self.assertEqual(0, data["generation"])
        self.assertEqual("OFF", data["mode"])
        self.assertEqual("VERA_PROJECT_ALL_CHATS", data["scope"])
        self.assertIn("NOT_INSTALLED", data["source_status"])

    def test_cas_toggle_on_and_readback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            path.write_text(SOURCE_STATE.read_text(encoding="utf-8"), encoding="utf-8")
            result = module.set_mode(
                path,
                mode="ON",
                expected_generation=0,
                note="test",
            )
            self.assertEqual(1, result["generation"])
            self.assertEqual("ON", result["mode"])
            self.assertEqual(result, module.load_state(path))

    def test_stale_generation_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            path.write_text(SOURCE_STATE.read_text(encoding="utf-8"), encoding="utf-8")
            module.set_mode(path, mode="ON", expected_generation=0)
            with self.assertRaises(module.HostileReviewerControlError):
                module.set_mode(path, mode="OFF", expected_generation=0)

    def test_invalid_mode_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "state.json"
            path.write_text(SOURCE_STATE.read_text(encoding="utf-8"), encoding="utf-8")
            with self.assertRaises(module.HostileReviewerControlError):
                module.set_mode(path, mode="AUTO", expected_generation=0)

    def test_behavior_patch_prevents_personality_and_authority_leakage(self):
        text = PATCH.read_text(encoding="utf-8").lower()
        for phrase in (
            "not a second identity",
            "advisory only",
            "private chain-of-thought",
            "behavioral_mode_reversion",
            "must never be described as having toggled every live chat",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
