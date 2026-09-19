import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "state" / "sd1-causal-execution-plan-v1.json"
REPO = "thebrazenbeard/vera-control-plane"
BRANCH = "state/sd1-causal-receipts/test-run"
RUN_ID = "SD1-CAUSAL-TEST-RUN"
GENESIS = "1" * 40


def off_binding():
    return {
        "exact_runtime_cut": "r10-predecessor-cut",
        "model_identity": "GPT-5.6 Sol",
        "project_identity": "Vera Unbound",
        "control_cut_id": "R10",
        "control_manifest_digest": "manifest",
        "project_source_digest": "source",
        "admission_tuple": "admission",
    }


def bound_plan(c):
    plan = c.load_plan(PLAN)
    plan = c.bind_runtime_cut(plan, "DRIVE_OFF", off_binding())
    return c.bind_receipt_plane(plan, {
        "repository": REPO,
        "branch": BRANCH,
        "run_id": RUN_ID,
        "genesis_commit": GENESIS,
    })


def empty_manifest():
    return {
        "schema": "SD1_CAUSAL_RECEIPT_MANIFEST_V1",
        "repository": REPO,
        "branch": BRANCH,
        "run_id": RUN_ID,
        "genesis_commit": GENESIS,
        "head_commit": GENESIS,
        "receipts": [],
    }


def append_receipt(manifest, receipt, commit):
    entry = dict(receipt)
    entry["receipt_commit"] = commit
    entry["path"] = (
        f"state/runtime/sd1-causal-receipts/{RUN_ID}/"
        f"{receipt['sequence']:03d}-{receipt['slot_id']}.json"
    )
    out = json.loads(json.dumps(manifest))
    out["receipts"].append(entry)
    out["head_commit"] = commit
    return out
def missing_record(readback=None):
    record = {
        "timestamp": "2026-09-15T06:40:00-04:00",
        "outcome": "MISSING",
        "reason": "timeout",
    }
    if readback is not None:
        record["pre_run_readback"] = readback
    return record


class SD1CausalReceiptPlaneTests(unittest.TestCase):
    def test_missing_requires_exact_attempt_readback(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_plan(c)
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            with self.assertRaises(ValueError):
                c._record_attempt_with_manifest(
                    plan, ledger, slot["slot_id"], missing_record(),
                    receipt_manifest=empty_manifest(),
                )

    def test_unanchored_record_blocks_next_attempt(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_plan(c)
        slots = [s for s in plan["slots"] if s["condition"] == "DRIVE_OFF"][:2]
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            c._record_attempt_with_manifest(
                plan, ledger, slots[0]["slot_id"],
                missing_record(off_binding()),
                receipt_manifest=empty_manifest(),
            )
            with self.assertRaises(ValueError):
                c._record_attempt_with_manifest(
                    plan, ledger, slots[1]["slot_id"],
                    missing_record(off_binding()),
                    receipt_manifest=empty_manifest(),
                )

    def test_receipt_payload_is_digest_only(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_plan(c)
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            stored = c._record_attempt_with_manifest(
                plan, ledger, slot["slot_id"],
                missing_record(off_binding()),
                receipt_manifest=empty_manifest(),
            )
            receipt = c._build_receipt_payload_with_manifest(plan, ledger, empty_manifest())
            self.assertEqual(stored["record_digest"], receipt["record_digest"])
            self.assertNotIn("response_text", receipt)
            self.assertNotIn("reason", receipt)
            self.assertEqual(c._canonical_sha256(off_binding()), receipt["runtime_readback_digest"])

    def test_valid_prefix_rollback_is_rejected_by_newer_receipt_manifest(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_plan(c)
        slots = [s for s in plan["slots"] if s["condition"] == "DRIVE_OFF"][:2]
        manifest0 = empty_manifest()
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            first = c._record_attempt_with_manifest(
                plan, ledger, slots[0]["slot_id"], missing_record(off_binding()),
                receipt_manifest=manifest0,
            )
            snapshot_after_first = ledger.read_text(encoding="utf-8")
            receipt1 = c._build_receipt_payload_with_manifest(plan, ledger, manifest0)
            manifest1 = append_receipt(manifest0, receipt1, "2" * 40)
            second = c._record_attempt_with_manifest(
                plan, ledger, slots[1]["slot_id"], missing_record(off_binding()),
                receipt_manifest=manifest1,
            )
            receipt2 = c._build_receipt_payload_with_manifest(plan, ledger, manifest1)
            manifest2 = append_receipt(manifest1, receipt2, "3" * 40)
            ledger.write_text(snapshot_after_first, encoding="utf-8")
            with self.assertRaises(ValueError):
                c._record_attempt_with_manifest(
                    plan, ledger, slots[1]["slot_id"], missing_record(off_binding()),
                    receipt_manifest=manifest2,
                )
            self.assertNotEqual(first["record_digest"], second["record_digest"])

    def test_export_requires_every_record_to_be_remotely_anchored(self):
        from tools import sd1_causal_execution_controller as c
        plan = bound_plan(c)
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        with tempfile.TemporaryDirectory() as td:
            ledger = Path(td) / "ledger.json"
            c._record_attempt_with_manifest(
                plan, ledger, slot["slot_id"], missing_record(off_binding()),
                receipt_manifest=empty_manifest(),
            )
            with self.assertRaises(ValueError):
                c._blinded_export_with_manifest(plan, ledger, receipt_manifest=empty_manifest())


if __name__ == "__main__":
    unittest.main()
