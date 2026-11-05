"""Offline source-bound negative probe: no host, network, credentials, or live IPC.

Supply paths to exact-revision public source files in VERA_E2E_SOURCE_DIR.
The probe checks six expected Git blob hashes before executing any code.
Source checks are limited to selected classes and static contract shape.
"""
from __future__ import annotations

import ast
import hashlib
import os
from contextlib import contextmanager
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import json
import re
import shutil
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
import uuid


PINNED_REFS = {
    "portal": "a27db806c064248cba5cf109aa8a4866df4fb8d1",
    "project-runner": "44da26e02c39591118bf1fdfe7ec01bd1103fc66",
    "executor": "9838c0f840e3bcf946d7ed6b767b00b89d5a5d86",
}
PINNED_BLOBS = {
    "portal_desktop_ipc.py": "330028c1d0c63b77836a63c8a94a0a6c51423427",
    "portal_capability_admission.py": "0fc7067807aa5a5f16716f01f87e706d6102d958",
    "projectrunner_sqlite_state.py": "c829398d6cfa31d0fbffa54cf072f7f3c36af35c",
    "executor_effect_ledger.ts": "09b09790ffbefe209c1dc81b92e92321c9540b54",
    "executor_server.ts": "e2fc19872fbbc5315249500c16771bb7f5257cf9",
    "executor_device_registry.ts": "9f8421891134f0f9794cf4184fa3f29c4714acab",
}
if not os.environ.get("VERA_E2E_SOURCE_DIR"):
    raise SystemExit("VERA_E2E_SOURCE_DIR must name an isolated directory of exact pinned source files")
SNAP = Path(os.environ["VERA_E2E_SOURCE_DIR"]).resolve()
for filename, expected in PINNED_BLOBS.items():
    path = SNAP / filename
    raw = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if actual != expected:
        raise SystemExit(f"source blob mismatch for {filename}: got {actual}, expected {expected}")


def _extract_python_source(filename: str, names: set[str], namespace: dict) -> dict:
    tree = ast.parse((SNAP / filename).read_text(encoding="utf-8"))
    body = [node for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.Assign))
            and (getattr(node, "name", None) in names or
                 (isinstance(node, ast.Assign) and
                  any(isinstance(t, ast.Name) and t.id in names for t in node.targets)))]
    code = compile(ast.fix_missing_locations(ast.Module(body=body, type_ignores=[])), filename, "exec")
    exec(code, namespace)
    return namespace


@dataclass
class Lease:
    work_fingerprint: str
    holder: str
    fencing_token: int
    expires_at: float


bridge_ns = _extract_python_source(
    "portal_desktop_ipc.py",
    {"_REQUEST_ID_RE", "BridgeTimeoutError", "BridgeOutcomeUnknownError", "FileBridgeClient"},
    {"Path": Path, "json": json, "re": re, "time": time, "uuid": uuid},
)
FileBridgeClient = bridge_ns["FileBridgeClient"]
BridgeOutcomeUnknownError = bridge_ns["BridgeOutcomeUnknownError"]
runner_ns = _extract_python_source(
    "projectrunner_sqlite_state.py",
    {"_connect", "_managed_connection", "SQLiteLeaseStore"},
    {"Path": Path, "sqlite3": sqlite3, "contextmanager": contextmanager, "Lease": Lease},
)
SQLiteLeaseStore = runner_ns["SQLiteLeaseStore"]


class SourceBackedE2ENegativeTests(unittest.TestCase):
    def test_portal_claim_then_response_loss_is_unknown_and_same_id_blocked(self):
        with tempfile.TemporaryDirectory(prefix="vera-contract-no-effect-") as temp:
            root = Path(temp)
            client = FileBridgeClient(root, timeout_seconds=0.12, poll_seconds=0.002)
            request_id = "synthetic_effect_001"
            claimed = root / "bridge" / "claimed" / f"{request_id}.json"

            def synthetic_claim_no_response():
                request = root / "bridge" / "requests" / f"{request_id}.json"
                limit = time.monotonic() + 1.0
                while not request.exists() and time.monotonic() < limit:
                    time.sleep(0.001)
                if request.exists():
                    request.replace(claimed)

            worker = threading.Thread(target=synthetic_claim_no_response, daemon=True)
            worker.start()
            with self.assertRaises(BridgeOutcomeUnknownError):
                client.request("synthetic_noop", request_id=request_id)
            worker.join(1)
            self.assertTrue(claimed.exists(), "fixture must actually claim request")
            with self.assertRaises(FileExistsError):
                client.request("synthetic_noop", request_id=request_id)
            self.assertFalse(hasattr(client, "read_receipt"))

    def test_portal_success_response_is_consumed_no_exact_readback(self):
        with tempfile.TemporaryDirectory(prefix="vera-contract-no-effect-") as temp:
            root = Path(temp)
            client = FileBridgeClient(root, timeout_seconds=0.3, poll_seconds=0.002)
            rid = "synthetic_result_001"
            output = root / "bridge" / "responses" / f"{rid}.json"

            def synthetic_response():
                request = root / "bridge" / "requests" / f"{rid}.json"
                limit = time.monotonic() + 1.0
                while not request.exists() and time.monotonic() < limit:
                    time.sleep(0.001)
                if request.exists():
                    output.write_text(json.dumps({"request_id": rid, "ok": True, "result": {"no_effect": True}}))

            worker = threading.Thread(target=synthetic_response, daemon=True)
            worker.start()
            self.assertEqual(client.request("synthetic_noop", request_id=rid), {"no_effect": True})
            worker.join(1)
            self.assertFalse(output.exists(), "actual Portal source deletes response after read")

    def test_runner_arbitrary_holder_can_self_claim(self):
        with tempfile.TemporaryDirectory(prefix="vera-contract-no-effect-") as temp:
            store = SQLiteLeaseStore(Path(temp) / "lease.db")
            unverified = store.claim("synthetic_work", holder="forged-holder", now=100.0, ttl=10.0)
            self.assertIsNotNone(unverified)
            self.assertEqual(unverified.holder, "forged-holder")
            self.assertEqual(unverified.fencing_token, 1)

    def test_runner_sqlite_rollback_mints_same_fence_again(self):
        with tempfile.TemporaryDirectory(prefix="vera-contract-no-effect-") as temp:
            root = Path(temp)
            live = root / "lease.db"
            backup = root / "snapshot.db"
            store = SQLiteLeaseStore(live)
            first = store.claim("synthetic_work", holder="holder-A", now=100.0, ttl=1.0)
            self.assertEqual(first.fencing_token, 1)
            with sqlite3.connect(live) as source, sqlite3.connect(backup) as dst:
                source.backup(dst)  # exact SQLite snapshot after token 1
            newer = store.claim("synthetic_work", holder="holder-B", now=102.0, ttl=1.0)
            self.assertEqual(newer.fencing_token, 2)
            restored = SQLiteLeaseStore(backup)
            forked = restored.claim("synthetic_work", holder="holder-C", now=102.0, ttl=1.0)
            self.assertEqual(forked.fencing_token, 2)
            self.assertNotEqual(forked.holder, newer.holder)
            # Both token 2 values exist in branches: local SQLite fencing alone
            # cannot prove a globally monotonic, host-authenticated authority.

    def test_executor_source_breaks_upstream_idempotency_chain(self):
        server = (SNAP / "executor_server.ts").read_text(encoding="utf-8")
        device = (SNAP / "executor_device_registry.ts").read_text(encoding="utf-8")
        ledger = (SNAP / "executor_effect_ledger.ts").read_text(encoding="utf-8")
        self.assertIn("const effectId = randomUUID();", server)
        self.assertIn("effects.create(effectId, deviceId, generation, false);", server)
        self.assertIn("const requestId = randomUUID();", device)
        self.assertIn("private records = new Map<string, EffectRecord>();", ledger)
        self.assertIn("this.records.set(requestId, record);", ledger)
        self.assertIn("while (this.records.size > this.maxRecords)", ledger)
        self.assertNotIn("idempotencyKey", server)
        self.assertNotIn("idempotencyKey", ledger)
        self.assertNotIn("idempotencyKey", device)
        self.assertNotIn("read_receipt", server)

    def test_portal_protected_effect_gate_is_not_bridge_or_executor_authority(self):
        module_name = "isolated_verified_portal_capability_admission"
        spec = importlib.util.spec_from_file_location(module_name, SNAP / "portal_capability_admission.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        namespace = vars(module)
        Definition = namespace["CapabilityDefinition"]
        Invocation = namespace["CapabilityInvocation"]
        admission = namespace["admit_capability"]
        d = Definition("cap.synthetic", "v1", "noop", "PROTECTED_EFFECT", "in.v1", "out.v1",
                       "thebrazenbeard/executor", "9838c0f840e3bcf946d7ed6b767b00b89d5a5d86",
                       "PRIVATE", "GENERAL_READ")
        req = Invocation("r1", "cap.synthetic", "v1", "noop", "PROTECTED_EFFECT", "model",
                         "participant", "context", "adapter", "host", "idem1")
        got = admission(req, definition=d, advertisement=None, grant=None,
                        verify_grant=None, verify_context=None, now=100.0)
        self.assertFalse(got.allowed)
        self.assertEqual(got.reason, "PROTECTED_EFFECT_NOT_IMPLEMENTED")
        self.assertEqual(got.receipt.effect_status, "NOT_EXECUTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
