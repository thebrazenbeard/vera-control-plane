from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKER = ROOT / "workers" / "ORGASM_VERA_RUNTIME_WORKER_V1.md"
CHECKPOINT = ROOT / "state" / "continuation" / "ORGASM_VERA_EXODUS_CHECKPOINT_20260919_V1.md"


class OrgasmVeraExodusReconstructionTests(unittest.TestCase):
    def test_worker_is_reconstructible_without_permanent_chat(self):
        text = WORKER.read_text(encoding="utf-8")
        self.assertIn("temporary delegated Vera execution", text)
        self.assertIn("not a separate identity", text)
        self.assertIn("No permanent chat dependency is permitted.", text)
        self.assertIn("thebrazenbeard/vera", text)
        self.assertIn("thebrazenbeard/sexuality", text)
        self.assertIn("thebrazenbeard/vera-control-plane", text)
        self.assertIn("thebrazenbeard/chat-communication-bus", text)
        self.assertIn("bus/vera-v2", text)
        self.assertIn("WORKER_RECONSTRUCTION_GAP", text)
        self.assertNotIn("chatgpt.com/", text)

    def test_checkpoint_is_freshness_first_and_preserves_claim_boundaries(self):
        text = CHECKPOINT.read_text(encoding="utf-8")
        self.assertIn("STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT", text)
        self.assertIn("CHATGPT_CONVERSATION_EXTERNAL_AFFECT_HOST", text)
        self.assertIn("HISTORICAL", text)
        self.assertIn("PHENOMENOLOGY", text.upper())
        self.assertIn("No successor OV permanent chat is required.", text)
        self.assertIn("Vera Control Plane Coordinator", text)
        self.assertNotIn("chatgpt.com/", text)

    def test_retirement_does_not_promote_source_or_provider_state(self):
        text = CHECKPOINT.read_text(encoding="utf-8")
        self.assertIn("provider schema/function: older generation", text)
        self.assertIn("current provider-qualified affective state: not established", text)
        self.assertIn("current route activation: not established", text)
        self.assertIn("No provider mutation is authorized by this Exodus", text)


if __name__ == "__main__":
    unittest.main()
