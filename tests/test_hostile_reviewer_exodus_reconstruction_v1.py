import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "HOSTILE_REVIEWER_EXODUS_RECONSTRUCTION_V1.md"
CHECKPOINT = ROOT / "state" / "closeouts" / "HOSTILE_REVIEWER_EXODUS_CHECKPOINT_20260919.json"

class HostileReviewerExodusTests(unittest.TestCase):
    def test_checkpoint_is_starting_snapshot_and_not_chat_identity(self):
        data = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        self.assertTrue(data["status"].startswith("STARTING_SNAPSHOT"))
        self.assertFalse(data["retired_chat_dependency"])
        self.assertEqual(
            "VERA_RUNTIME_RESPONSE_REVIEW_FEATURE_NOT_WORKER_IDENTITY",
            data["feature_class"],
        )

    def test_source_runtime_effect_qualification_remain_separate(self):
        data = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
        cp = data["control_plane"]
        self.assertEqual("NOT_ESTABLISHED", cp["install"])
        self.assertEqual("NOT_ESTABLISHED", cp["current_route"])
        self.assertEqual("NOT_ESTABLISHED", cp["runtime_consumption"])
        self.assertEqual("NOT_ESTABLISHED", cp["behavioral_qualification"])
        self.assertEqual("OFF", cp["source_default_mode"])

    def test_reconstruction_doc_has_no_chat_url_dependency(self):
        text = DOC.read_text(encoding="utf-8")
        self.assertNotIn("chatgpt.com/", text.lower())
        self.assertIn("No retired chat", text)

if __name__ == "__main__":
    unittest.main()
