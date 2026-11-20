"""Synthetic fixtures; no private source locators or user memory."""
import copy
import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from knowledge_record_gate import validate_record, main

NOW = datetime(2026, 11, 20, 20, 0, tzinfo=timezone.utc)


def card():
    return {
        "schema": "VERA_KNOWLEDGE_RECORD_V1",
        "record_id": "synthetic:repo-42-readme",
        "subject_id": "repo:synthetic/example",
        "title": "Synthetic source branch is inspected",
        "claim": "Synthetic test source at exact commit is inspected; no runtime asserted",
        "domains": ["source", "verification"],
        "owner_id": "owner:synthetic-reviewer",
        "owner_binding_ref": "synthetic:owner-map-v1",
        "visibility": "PUBLIC_SAFE",
        "publication_target": "PUBLIC_REPOSITORY",
        "lifecycle": "REVIEWED",
        "claim_surface": "SOURCE",
        "currentness": "CURRENT",
        "valid_until": "2026-11-20T22:00:00Z",
        "evidence": [{"class": "SOURCE_INSPECTION", "source_ref": "https://github.com/synthetic/example/blob/" + "a" * 40 + "/docs/README.md", "revision": "a" * 40, "observed_at": "2026-11-20T19:00:00Z"}],
        "supersedes": [],
        "limitations": ["Structural check, source inspection not independently executed by the validator"],
    }


class KnowledgeGateTests(unittest.TestCase):
    def assert_bad(self, record, code):
        self.assertIn(code, validate_record(record, now=NOW))

    def test_qualified_source_passes_shape_only(self):
        self.assertEqual(validate_record(card(), now=NOW), [])

    def test_document_not_runtime_proof(self):
        record = card(); record["claim_surface"] = "RUNTIME"
        self.assert_bad(record, "currentness.missing_qualified_evidence")

    def test_test_result_not_runtime_proof(self):
        record = card(); record["claim_surface"] = "RUNTIME"
        record["evidence"][0]["class"] = "TEST"
        record["evidence"][0]["revision"] = "synthetic:test"
        self.assert_bad(record, "currentness.missing_qualified_evidence")

    def test_provider_readback_required(self):
        record = card(); record["claim_surface"] = "PROVIDER"
        self.assert_bad(record, "currentness.missing_qualified_evidence")

    def test_genuine_runtime_evidence_type_can_pass_shape(self):
        record = card(); record["claim_surface"] = "RUNTIME"
        record["evidence"][0]["class"] = "REAL_PROBE"
        record["evidence"][0]["revision"] = "synthetic:probe-receipt"
        self.assertEqual(validate_record(record, now=NOW), [])

    def test_historical_record_cannot_be_current(self):
        record = card(); record["claim_surface"] = "HISTORICAL"
        self.assert_bad(record, "currentness.unsupported_surface")

    def test_stale_evidence_rejected(self):
        record = card(); record["evidence"][0]["observed_at"] = "2026-11-18T19:00:00Z"
        self.assert_bad(record, "currentness.stale_evidence")

    def test_future_evidence_rejected(self):
        record = card(); record["evidence"][0]["observed_at"] = "2026-11-21T19:00:00Z"
        self.assert_bad(record, "evidence.future")

    def test_expired_currentness_rejected(self):
        record = card(); record["valid_until"] = "2026-11-20T19:59:59Z"
        self.assert_bad(record, "currentness.expired_or_missing")

    def test_overlong_currentness_window_rejected(self):
        record = card(); record["valid_until"] = "2026-11-23T12:00:00Z"
        self.assert_bad(record, "currentness.overlong_window")

    def test_retired_claim_cannot_be_current(self):
        record = card(); record["lifecycle"] = "RETIRED"
        self.assert_bad(record, "currentness.retired_or_superseded")

    def test_private_public_leak_flag_rejected(self):
        record = card(); record["visibility"] = "RESTRICTED"
        self.assert_bad(record, "publication.restricted_or_unknown")

    def test_public_requires_review(self):
        record = card(); record["lifecycle"] = "DRAFT"
        self.assert_bad(record, "publication.not_reviewed")

    def test_missing_owner_binding_rejected(self):
        record = card(); record["owner_binding_ref"] = ""
        self.assert_bad(record, "record.owner_binding_ref")

    def test_rejected_bare_timestamp(self):
        record = card(); record["evidence"][0]["observed_at"] = "2026-11-20T19:00:00"
        self.assert_bad(record, "evidence.observed_at")

    def test_no_unreviewed_extra_fields(self):
        record = card(); record["authorization"] = True
        self.assert_bad(record, "record.fields")

    def test_no_self_supersession(self):
        record = card(); record["supersedes"] = [record["record_id"]]
        self.assert_bad(record, "record.self_supersession")

    def test_no_boolean_strings_for_enums(self):
        record = card(); record["visibility"] = True
        self.assert_bad(record, "record.enum.visibility")

    def test_cli_duplicate_key_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "record.json"
            s = json.dumps(card()).replace('"schema":', '"schema": "JUNK", "schema":', 1)
            p.write_text(s, encoding="utf-8")
            with redirect_stdout(io.StringIO()) as stream:
                code = main([str(p), "--as-of", "2026-11-20T20:00:00Z"])
            self.assertEqual(code, 1)
            self.assertIn("input.invalid_or_unavailable", stream.getvalue())

    def test_cli_bad_argument_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "record.json"
            p.write_text(json.dumps(card()), encoding="utf-8")
            with redirect_stdout(io.StringIO()) as stream:
                code = main([str(p), "--as-of", "2026-11-20T20:00:00Z"])
            self.assertEqual(code, 0)
            self.assertIn('"valid": true', stream.getvalue())

    def test_restricted_private_store_allowed_structurally(self):
        record = card(); record["publication_target"] = "PRIVATE_STORE"
        record["visibility"] = "RESTRICTED"
        self.assertEqual(validate_record(record, now=NOW), [])

    def test_malformed_nested_json_does_not_crash_gate(self):
        record = card()
        for field in ("visibility", "lifecycle", "claim_surface", "currentness"):
            corrupt = copy.deepcopy(record)
            corrupt[field] = []
            errors = validate_record(corrupt, now=NOW)
            self.assertTrue(errors, field)
        corrupt = copy.deepcopy(record)
        corrupt["evidence"][0]["class"] = {"fake": True}
        self.assertIn("evidence.class", validate_record(corrupt, now=NOW))

    def test_invalid_valid_until_is_not_accepted(self):
        record = card(); record["valid_until"] = "2026-11-20T22:00:00+00:00"
        self.assert_bad(record, "currentness.invalid_until")

    def test_source_inspection_requires_exact_git_sha(self):
        record = card(); record["evidence"][0]["revision"] = "latest"
        self.assert_bad(record, "evidence.git_revision")

    def test_duplicate_domain_tags_rejected(self):
        record = card(); record["domains"] = ["source", "source"]
        self.assert_bad(record, "record.list_distinct.domains")

    def test_until_without_current_rejected(self):
        record = card(); record["currentness"] = "HISTORICAL"
        self.assert_bad(record, "currentness.until_without_current")


    def test_source_branch_reference_cannot_pass_currentness(self):
        record = card()
        record["evidence"][0]["source_ref"] = "https://github.com/synthetic/example/blob/main/docs/README.md"
        self.assert_bad(record, "evidence.source_unpinned")

    def test_source_revision_must_match_pinned_url(self):
        record = card()
        record["evidence"][0]["source_ref"] = "https://github.com/synthetic/example/blob/" + "b" * 40 + "/docs/README.md"
        self.assert_bad(record, "evidence.source_revision_mismatch")

    def test_source_path_traversal_cannot_pass_currentness(self):
        record = card()
        record["evidence"][0]["source_ref"] = "https://github.com/synthetic/example/blob/" + "a" * 40 + "/docs/../secrets.txt"
        self.assert_bad(record, "evidence.source_path_invalid")

    def test_source_repository_must_match_repo_subject(self):
        record = card()
        record["evidence"][0]["source_ref"] = "https://github.com/synthetic/other/blob/" + "a" * 40 + "/docs/README.md"
        self.assert_bad(record, "evidence.source_repository_mismatch")

if __name__ == "__main__":
    unittest.main()
