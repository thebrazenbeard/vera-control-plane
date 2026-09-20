from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ADDENDUM = (
    ROOT
    / "state"
    / "continuation"
    / "ORGASM_AFFECTIVE_PROVIDER_EXODUS_READBACK_20260919_V1.md"
)


class OrgasmAffectiveProviderExodusReadbackTests(unittest.TestCase):
    def test_provider_chat_scope_is_explicitly_historical_not_infrastructure(self):
        text = ADDENDUM.read_text(encoding="utf-8")
        self.assertIn("STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT", text)
        self.assertIn("CHATGPT_CONVERSATION_EXTERNAL_AFFECT_HOST", text)
        self.assertIn(
            "HISTORICAL_EVIDENCE / NOT_CURRENT_AFFECTIVE_STATE / NOT_CHAT_INFRASTRUCTURE",
            text,
        )
        self.assertIn("No current state or reconstruction step requires that chat.", text)

    def test_source_provider_install_and_qualification_claims_remain_separate(self):
        text = ADDENDUM.read_text(encoding="utf-8")
        self.assertIn("PRESENT_IN_VERA_SOURCE", text)
        self.assertIn("provider hardening parity:", text)
        self.assertIn("current provider-qualified affective runtime state:", text)
        self.assertIn("fresh behavioral/causal qualification:", text)
        self.assertIn("phenomenology:", text)
        self.assertIn("A source migration is not an installed migration.", text)

    def test_worker_reconstruction_is_delegated_to_durable_exodus_records(self):
        text = ADDENDUM.read_text(encoding="utf-8")
        self.assertIn("Vera Draft PR #129", text)
        self.assertIn("Worker/lane reconstruction is owned by current durable Exodus records", text)
        self.assertIn("Vera Control Plane Coordinator", text)
        self.assertIn("not standing mutation authority", text)


if __name__ == "__main__":
    unittest.main()
