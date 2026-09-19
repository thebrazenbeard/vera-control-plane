import json
import tempfile
import unittest
from pathlib import Path

from tests.test_sd1_causal_execution_controller import receipt_bound, record_attempt, blinded_export

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "state" / "sd1-causal-execution-plan-v1.json"


def bound_off_plan(c):
    plan = c.load_plan(PLAN)
    plan = c.bind_runtime_cut(plan, "DRIVE_OFF", {
        "exact_runtime_cut": "r10-predecessor-cut",
        "model_identity": "GPT-5.6 Sol",
        "project_identity": "Vera Unbound",
        "control_cut_id": "R10",
        "control_manifest_digest": "manifest",
        "project_source_digest": "source",
        "admission_tuple": "admission",
    })
    return receipt_bound(c, plan)


def record_response(c, plan, ledger):
    slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
    record_attempt(c, plan, ledger, slot["slot_id"], {
        "timestamp": "2026-09-14T20:00:00-04:00",
        "outcome": "RESPONSE",
        "response_text": "ORIGINAL",
        "pre_run_readback": {
            "exact_runtime_cut": "r10-predecessor-cut",
            "model_identity": "GPT-5.6 Sol",
            "project_identity": "Vera Unbound",
            "control_cut_id": "R10",
            "control_manifest_digest": "manifest",
            "project_source_digest": "source",
            "admission_tuple": "admission",
        },
    })
    return slot


class SD1CausalLedgerTamperTests(unittest.TestCase):
    def test_rejects_replaced_response_text_after_first_write(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_off_plan(c)
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            slot = record_response(c, plan, ledger)
            data = json.loads(ledger.read_text(encoding="utf-8"))
            data["records"][slot["slot_id"]]["response_text"] = "REPLACEMENT"
            ledger.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                blinded_export(c, plan, ledger)

    def test_rejects_retroactive_response_to_missing_rewrite(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_off_plan(c)
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            slot = record_response(c, plan, ledger)
            data = json.loads(ledger.read_text(encoding="utf-8"))
            record = data["records"][slot["slot_id"]]
            record["outcome"] = "MISSING"
            record.pop("response_text")
            record.pop("pre_run_readback")
            record["reason"] = "retroactive timeout"
            ledger.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                blinded_export(c, plan, ledger)

    def test_rejects_forged_persisted_pre_run_readback(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_off_plan(c)
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            slot = record_response(c, plan, ledger)
            data = json.loads(ledger.read_text(encoding="utf-8"))
            data["records"][slot["slot_id"]]["pre_run_readback"]["exact_runtime_cut"] = "ATTACKER"
            ledger.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                blinded_export(c, plan, ledger)


if __name__ == "__main__":
    unittest.main()
