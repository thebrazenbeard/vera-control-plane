import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "state" / "sd1-causal-execution-plan-v1.json"
BRANCH = "state/sd1-causal-receipts/git-tests"
RUN_ID = "SD1-GIT-RECEIPT-TEST"


def git(cwd, *args, check=True):
    proc = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True)
    if check and proc.returncode:
        raise AssertionError(proc.stderr)
    return proc.stdout.strip()


def make_remote(root):
    bare = root / "remote.git"
    work = root / "work"
    git(root, "init", "--bare", str(bare))
    git(root, "clone", str(bare), str(work))
    git(work, "config", "user.name", "Receipt Test")
    git(work, "config", "user.email", "receipt-test@local.invalid")
    (work / "GENESIS").write_text("sd1 receipt genesis\n", encoding="utf-8")
    git(work, "add", "GENESIS")
    git(work, "commit", "-m", "receipt genesis")
    genesis = git(work, "rev-parse", "HEAD")
    git(work, "push", "origin", f"HEAD:refs/heads/{BRANCH}")
    expected = "https://github.com/thebrazenbeard/vera-control-plane.git"
    git(work, "config", f"url.{bare.as_uri()}.insteadOf", expected)
    git(work, "remote", "set-url", "origin", expected)
    return bare, work, genesis


def bound_plan(c, genesis):
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
    return c.bind_receipt_plane(plan, {
        "repository": "thebrazenbeard/vera-control-plane",
        "branch": BRANCH,
        "run_id": RUN_ID,
        "genesis_commit": genesis,
    })


def missing(binding):
    return {
        "timestamp": "2026-09-15T09:30:00-04:00",
        "outcome": "MISSING",
        "reason": "timeout",
        "pre_run_readback": dict(binding),
    }


class SD1CausalGitReceiptTests(unittest.TestCase):
    def test_git_receipt_round_trip_rejects_valid_prefix_rollback(self):
        from tools import sd1_causal_execution_controller as c
        from tools import sd1_causal_receipt_git as g
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, work, genesis = make_remote(root)
            plan = bound_plan(c, genesis)
            ledger = root / "ledger.json"
            slots = [s for s in plan["slots"] if s["condition"] == "DRIVE_OFF"][:2]
            binding = {k: v for k, v in plan["runtime_bindings"]["DRIVE_OFF"].items()
                       if k not in {"ready", "required_readback"}}
            g.record_attempt(plan, ledger, slots[0]["slot_id"], missing(binding), work)
            g.append_receipt(plan, ledger, work)
            snapshot = ledger.read_text(encoding="utf-8")
            g.record_attempt(plan, ledger, slots[1]["slot_id"], missing(binding), work)
            g.append_receipt(plan, ledger, work)
            ledger.write_text(snapshot, encoding="utf-8")
            with self.assertRaises(ValueError):
                g.record_attempt(plan, ledger, slots[1]["slot_id"], missing(binding), work)

    def test_receipt_commit_contains_only_digest_payload(self):
        from tools import sd1_causal_execution_controller as c
        from tools import sd1_causal_receipt_git as g
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, work, genesis = make_remote(root)
            plan = bound_plan(c, genesis)
            ledger = root / "ledger.json"
            slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
            binding = {k: v for k, v in plan["runtime_bindings"]["DRIVE_OFF"].items()
                       if k not in {"ready", "required_readback"}}
            g.record_attempt(plan, ledger, slot["slot_id"], missing(binding), work)
            manifest = g.append_receipt(plan, ledger, work)
            entry = manifest["receipts"][0]
            payload = json.loads(git(work, "show", f"{entry['receipt_commit']}:{entry['path']}"))
            self.assertEqual(set(payload), g.RECEIPT_PAYLOAD_KEYS)
            self.assertNotIn("reason", payload)
            self.assertNotIn("response_text", payload)

    def test_receipt_branch_rejects_nonreceipt_commit(self):
        from tools import sd1_causal_execution_controller as c
        from tools import sd1_causal_receipt_git as g
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, work, genesis = make_remote(root)
            plan = bound_plan(c, genesis)
            (work / "UNRELATED").write_text("pollution\n", encoding="utf-8")
            git(work, "add", "UNRELATED")
            git(work, "commit", "-m", "pollute receipt branch")
            git(work, "push", "origin", f"HEAD:refs/heads/{BRANCH}")
            with self.assertRaises(ValueError):
                g.read_verified_manifest(plan, work)


if __name__ == "__main__":
    unittest.main()

# Public controller entry points must not accept caller-forged receipt manifests.
def _test_public_controller_rejects_manifest_injection(self):
    from tools import sd1_causal_execution_controller as c
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _, work, genesis = make_remote(root)
        plan = bound_plan(c, genesis)
        slot = next(s for s in plan["slots"] if s["condition"] == "DRIVE_OFF")
        binding = {k: v for k, v in plan["runtime_bindings"]["DRIVE_OFF"].items()
                   if k not in {"ready", "required_readback"}}
        fake = {
            "schema": "SD1_CAUSAL_RECEIPT_MANIFEST_V1",
            "repository": "thebrazenbeard/vera-control-plane",
            "branch": BRANCH, "run_id": RUN_ID, "genesis_commit": genesis,
            "head_commit": genesis, "receipts": [],
        }
        with self.assertRaises(TypeError):
            c.record_attempt(plan, root / "ledger.json", slot["slot_id"],
                             missing(binding), receipt_manifest=fake)

SD1CausalGitReceiptTests.test_public_controller_rejects_manifest_injection = _test_public_controller_rejects_manifest_injection
