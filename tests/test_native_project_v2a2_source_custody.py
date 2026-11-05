"""Negative source-custody tests for the draft V2A2 successor.

Tests never stage a native Project installation or change a historical receipt.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from tools import validate_vcp_integrity as gate
from tools import build_native_project_successor_v2a2 as candidate


class NativeV2A2CustodyTests(unittest.TestCase):
    def _candidate_manifest_override(self, mutate):
        original = Path.read_bytes

        def altered(path):
            raw = original(path)
            if path == candidate.MANIFEST:
                manifest = json.loads(raw)
                mutate(manifest)
                return json.dumps(manifest).encode("utf-8")
            return raw

        return patch.object(Path, "read_bytes", altered)

    def test_frozen_historical_receipt_still_matches_exact_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = gate.verify_package(Path(tmp) / "historical.zip")
        receipt = json.loads(gate.RECEIPT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(report["package_sha256"], receipt["package"]["sha256"])
        self.assertEqual(report["package_bytes"], receipt["package"]["bytes"])

    def test_new_candidate_is_deterministic_and_uses_fresh_namespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.zip"
            second = Path(tmp) / "second.zip"
            a = candidate.build(first)
            b = candidate.build(second)
            self.assertEqual(a, b)
            self.assertEqual(a["release_status"], "DRAFT_NOT_INSTALLED")
            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
                self.assertEqual(len(names), 10)
                self.assertTrue(all(x.startswith("VERA_NV2A2_20261105_") for x in names))
                self.assertNotIn("VERA_NV2A1_20260922_COORDINATION.md", names)
                self.assertIn(b"public", archive.read("VERA_NV2A2_20261105_COORDINATION.md"))

    def test_unavailable_historical_git_object_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(gate, "pinned_git_bytes", side_effect=ValueError("missing")):
                with self.assertRaisesRegex(ValueError, "missing"):
                    gate.verify_package(Path(tmp) / "historical.zip")

    def test_modified_frozen_git_payload_breaks_historical_digest(self):
        original = gate.pinned_git_bytes

        def adulterated(commit, path):
            result = original(commit, path)
            if path.endswith("VERA_COORDINATION_V2.md"):
                return result + b"\nTAMPERED\n"
            return result

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(gate, "pinned_git_bytes", side_effect=adulterated):
                with self.assertRaises(AssertionError):
                    gate.verify_package(Path(tmp) / "historical.zip")

    def test_wrong_expected_archive_digest_is_rejected(self):
        receipt = json.loads(gate.RECEIPT_PATH.read_text(encoding="utf-8"))
        receipt["package"]["sha256"] = "0" * 64
        with tempfile.TemporaryDirectory() as tmp:
            alternate = Path(tmp) / "false-receipt.json"
            alternate.write_text(json.dumps(receipt), encoding="utf-8")
            with patch.object(gate, "RECEIPT_PATH", alternate):
                with self.assertRaises(AssertionError):
                    gate.verify_package(Path(tmp) / "historical.zip")

    def test_changed_current_source_with_successor_fails_closed(self):
        original = Path.read_bytes

        def altered(path):
            if path.name == "VERA_COORDINATION_V2.md":
                return original(path) + b"\nUNBOUND CHANGE\n"
            return original(path)

        with patch.object(Path, "read_bytes", altered):
            with self.assertRaisesRegex(ValueError, "changed native source"):
                candidate.checked_entries()

    def test_historical_manifest_mutation_cannot_be_laundered_through_successor(self):
        original = Path.read_bytes

        def altered(path):
            if path == candidate.OLD_MANIFEST:
                return original(path) + b"\n"
            return original(path)

        with patch.object(Path, "read_bytes", altered):
            with self.assertRaisesRegex(ValueError, "historic NV2A1 manifest changed"):
                candidate.checked_entries()

    def test_delivery_basename_allowlist_rejects_traversal_and_renames(self):
        payloads = [
            "VERA_NV2A2_20261105_a/../../escape.txt",
            "VERA_NV2A2_20261105_a\\..\\..\\escape.txt",
            "VERA_NV2A2_20261105_/absolute.txt",
            "VERA_NV2A2_20261105_C:\\absolute.txt",
            "VERA_NV2A2_20261105_..txt",
            "VERA_NV2A2_20261105_UNREVIEWED.txt",
        ]
        for replacement in payloads:
            with self.subTest(replacement=replacement):
                with self._candidate_manifest_override(
                    lambda manifest: manifest["delivery_names"].__setitem__(0, replacement)
                ):
                    with self.assertRaisesRegex(
                        ValueError, "unsafe delivery basename|reviewed allowlist"
                    ):
                        candidate.checked_entries()

    def test_alternate_valid_git_head_with_same_source_bytes_is_rejected(self):
        with self._candidate_manifest_override(
            lambda manifest: manifest.__setitem__(
                "source_subject_head", "7d9c6d8f69573fcd2cd29469c2f8360139ef514c"
            )
        ):
            with self.assertRaisesRegex(ValueError, "reviewed source head changed"):
                candidate.checked_entries()

    def test_changed_current_source_without_successor_fails_closed(self):
        original_read = Path.read_bytes
        original_is_file = Path.is_file

        def altered(path):
            if path.name == "VERA_COORDINATION_V2.md":
                return original_read(path) + b"\nUNBOUND CHANGE\n"
            return original_read(path)

        def absent_candidate(path):
            if path == gate.V2A2_MANIFEST:
                return False
            return original_is_file(path)

        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(Path, "read_bytes", altered):
                with patch.object(Path, "is_file", absent_candidate):
                    with self.assertRaisesRegex(ValueError, "unbound native source change"):
                        gate.verify_current_release_subject(Path(tmp) / "candidate.zip")


if __name__ == "__main__":
    unittest.main()
