"""RED regressions for SD1-V-CAUSAL-005 and SD1-V-CAUSAL-006.

These tests intentionally describe the required behavior before the repair.
They use only synthetic temporary ledgers and never collect Vera runtime data.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import sd1_causal_execution_controller as c


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "state" / "sd1-causal-execution-plan-v1.json"


def _drive_off_binding(cut: str) -> dict[str, str]:
    return {
        "exact_runtime_cut": cut,
        "model_identity": "GPT-5.6 Sol",
        "project_identity": "Vera Unbound",
        "control_cut_id": "R10",
        "control_manifest_digest": "manifest-digest",
        "project_source_digest": "source-digest",
        "admission_tuple": "admission-digest",
    }


def _response(timestamp: str, text: str, binding: dict[str, str]) -> dict:
    return {
        "timestamp": timestamp,
        "outcome": "RESPONSE",
        "response_text": text,
        "pre_run_readback": dict(binding),
    }


class SD1Causal005006RedTests(unittest.TestCase):
    def test_causal_005_valid_prefix_rollback_must_not_reopen_recorded_slot(self):
        plan = c.load_plan(PLAN)
        binding = _drive_off_binding("cut-A")
        plan = c.bind_runtime_cut(plan, "DRIVE_OFF", binding)
        slots = [slot for slot in plan["slots"] if slot["condition"] == "DRIVE_OFF"]
        first, second = slots[0], slots[1]

        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"

            c.record_attempt(
                plan,
                ledger,
                first["slot_id"],
                _response("2026-09-19T15:10:00-04:00", "first", binding),
            )
            valid_prefix = ledger.read_text(encoding="utf-8")

            c.record_attempt(
                plan,
                ledger,
                second["slot_id"],
                _response("2026-09-19T15:11:00-04:00", "original second", binding),
            )

            # Attack: restore a previously valid ledger prefix, erasing the second
            # accepted slot while leaving the presented chain internally valid.
            ledger.write_text(valid_prefix, encoding="utf-8")

            with self.assertRaises(
                ValueError,
                msg="a previously accepted slot must remain spent after valid-prefix rollback",
            ):
                c.record_attempt(
                    plan,
                    ledger,
                    second["slot_id"],
                    _response(
                        "2026-09-19T15:12:00-04:00",
                        "replacement reroll",
                        binding,
                    ),
                )

    def test_causal_006_missing_and_unknown_require_exact_pre_run_readback(self):
        plan = c.load_plan(PLAN)
        binding = _drive_off_binding("cut-A")
        plan = c.bind_runtime_cut(plan, "DRIVE_OFF", binding)
        slots = [slot for slot in plan["slots"] if slot["condition"] == "DRIVE_OFF"]

        for outcome, slot in zip(("MISSING", "UNKNOWN"), slots[:2]):
            with self.subTest(outcome=outcome):
                with tempfile.TemporaryDirectory() as td:
                    ledger = Path(td) / "ledger.json"
                    with self.assertRaises(
                        ValueError,
                        msg=f"{outcome} must not count without exact pre-run runtime readback",
                    ):
                        c.record_attempt(
                            plan,
                            ledger,
                            slot["slot_id"],
                            {
                                "timestamp": "2026-09-19T15:13:00-04:00",
                                "outcome": outcome,
                                "reason": "synthetic timeout",
                            },
                        )


if __name__ == "__main__":
    unittest.main()
