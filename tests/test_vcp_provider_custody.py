import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CUSTODY = ROOT / "governance" / "VCP_SUPABASE_PROVIDER_CUSTODY_V1.json"
PACKET = (
    ROOT
    / "governance"
    / "effect-packets"
    / "VCP_REVOKE_INTERNAL_RLS_GUARD_PUBLIC_EXECUTE_V1.json"
)

INCIDENT = (
    ROOT
    / "governance"
    / "incidents"
    / "VCP_PROTECTED_EFFECT_AUTHORITY_INCIDENT_20260921_V1.json"
)
CLASSIFICATION = ROOT / "governance" / "VCP_OPEN_PR_CLASSIFICATION_V2.json"
GITHUB_SECURITY = ROOT / "governance" / "VCP_GITHUB_SECURITY_CURRENTNESS_V1.json"
ISSUE1_CLOSURE = ROOT / "governance" / "VCP_ISSUE1_RUNTIME_CLOSURE_V1.json"

EXPECTED = {
    "20260912170153": (
        "supabase/provider-custody/fawkirqroyniueeqspif/applied/"
        "20260912170153_harden_public_default_privileges.sql",
        697,
        "d3386eb573ee96c2ae6bc18941ec75d98a5f217efd7a5948d53a6e96ba25e4b1",
    ),
    "20260912170345": (
        "supabase/provider-custody/fawkirqroyniueeqspif/applied/"
        "20260912170345_enforce_rls_on_exposed_schemas.sql",
        1604,
        "4205e76e5973650c54779378bd8e7baaeadd25e123d7bc4d3a57f7d834c5b9aa",
    ),
    "20260912170408": (
        "supabase/provider-custody/fawkirqroyniueeqspif/applied/"
        "20260912170408_reserve_locked_api_schema.sql",
        786,
        "e979320f17ca7895f08008bd7b5f2d0d62aca3b532e843308e0ae55aec7671d5",
    ),
    "20260919223652": (
        "supabase/migrations/20260919195000_create_sd1_causal_secondary_anchor.sql",
        24103,
        "246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523",
    ),
    "20260921192624": (
        "supabase/provider-custody/fawkirqroyniueeqspif/applied/"
        "20260921192624_revoke_internal_rls_guard_public_execute.sql",
        231,
        "b5f43de5a82cd8a2f4b068dcc213db0370d8ddd286c8487722aef6a59f48a698",
    ),
    "20260921200623": (
        "supabase/provider-custody/fawkirqroyniueeqspif/applied/"
        "20260921200623_make_anchor_deny_all_rls_explicit_v1.sql",
        636,
        "46132f28486afe4ee1ba9830fdf93d499b7b61a53e81b904a49a128579eda248",
    ),
}


class VcpProviderCustodyTests(unittest.TestCase):
    def setUp(self):
        self.custody = json.loads(CUSTODY.read_text(encoding="utf-8"))
        self.packet = json.loads(PACKET.read_text(encoding="utf-8"))
        self.incident = json.loads(INCIDENT.read_text(encoding="utf-8"))
        self.classification = json.loads(CLASSIFICATION.read_text(encoding="utf-8"))
        self.github_security = json.loads(
            GITHUB_SECURITY.read_text(encoding="utf-8")
        )
        self.issue1 = json.loads(ISSUE1_CLOSURE.read_text(encoding="utf-8"))

    def test_provider_identity_is_exact(self):
        provider = self.custody["provider"]
        self.assertEqual(provider["project_id"], "fawkirqroyniueeqspif")
        self.assertEqual(provider["project_name"], "Vera Control Plane")
        self.assertEqual(provider["status"], "ACTIVE_HEALTHY")

    def test_all_applied_migrations_have_exact_custody_bytes(self):
        by_version = {
            item["version"]: item for item in self.custody["applied_migrations"]
        }
        self.assertEqual(set(by_version), set(EXPECTED))
        for version, (path, expected_bytes, expected_sha) in EXPECTED.items():
            data = (ROOT / path).read_bytes()
            self.assertEqual(len(data), expected_bytes, version)
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected_sha, version)
            self.assertEqual(by_version[version]["provider_bytes"], expected_bytes)
            self.assertEqual(by_version[version]["provider_sha256"], expected_sha)

    def test_provider_recovery_does_not_fake_historical_git_source(self):
        rows = {
            item["version"]: item for item in self.custody["applied_migrations"]
        }
        for version in ("20260912170153", "20260912170345", "20260912170408"):
            self.assertEqual(
                rows[version]["custody_class"],
                "EXACT_PROVIDER_SOURCE_RECOVERED",
            )
            self.assertEqual(rows[version]["historical_git_source"], "UNRESOLVED")
        self.assertEqual(
            rows["20260919223652"]["custody_class"],
            "EXACT_DEPLOYED_SOURCE_BYTES_VERIFIED",
        )
        self.assertEqual(
            rows["20260919223652"]["source_git_blob"],
            "0769c527ad8fc8280d052dc1ce93f85673b6bb7d",
        )

    def test_supabase_advisor_is_clear_after_explicit_deny_policies(self):
        advisor = self.custody["security_readback"]["supabase_advisor"]["security"]
        self.assertEqual(advisor, [])
        explicit = self.custody["security_readback"]["explicit_deny_all_policies"]
        self.assertEqual(explicit["provider_readback"], "VERIFIED")
        self.assertEqual(len(explicit["policies"]), 2)
        self.assertTrue(all(policy["using"] is False for policy in explicit["policies"]))
        self.assertTrue(
            all(policy["with_check"] is False for policy in explicit["policies"])
        )

    def test_internal_guard_execute_revoke_is_readback_verified(self):
        guard = self.custody["security_readback"]["internal_rls_guard"]
        self.assertFalse(guard["public_execute"])
        self.assertFalse(guard["anon_execute"])
        self.assertFalse(guard["authenticated_execute"])
        self.assertFalse(guard["service_role_execute"])
        self.assertFalse(guard["broker_execute"])
        self.assertFalse(guard["public_schema_usage"])
        self.assertEqual(guard["defect_class"], "VERIFIED_FIXED")
        self.assertEqual(guard["provider_effect"], "APPLIED_VERIFIED")
        self.assertEqual(guard["provider_migration_version"], "20260921192624")

    def test_security_migration_revokes_all_unnecessary_execute_paths(self):
        path = (
            ROOT
            / "supabase"
            / "migrations"
            / "20260921173000_revoke_internal_rls_guard_public_execute.sql"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn(
            "REVOKE EXECUTE ON FUNCTION "
            "vera_cp_internal.enable_rls_for_new_api_tables()",
            text,
        )
        for role in (
            "PUBLIC",
            "anon",
            "authenticated",
            "service_role",
            "vera_sd1_causal_anchor_broker",
        ):
            self.assertIn(role, text)

    def test_issue1_source_fixed_does_not_promote_to_runtime(self):
        self.assertEqual(
            self.issue1["closure"]["source_defect"],
            "VERIFIED_FIXED",
        )
        self.assertEqual(
            self.issue1["closure"]["live_runtime_defect"],
            "BLOCKED_EXTERNAL",
        )
        self.assertEqual(
            self.issue1["runtime_boundary"]["live_router_consumption"],
            "NOT_ESTABLISHED",
        )
        self.assertFalse(
            self.issue1["runtime_boundary"]["repository_source_auto_consumption"]
        )
        identities = self.issue1["canonical_source"]["byte_identity"]
        self.assertEqual(len(identities), 3)
        self.assertTrue(all(row["identical"] for row in identities.values()))
        self.assertIsNone(
            self.issue1["closure"]["protected_effect_packet"]
        )

    def test_effect_packet_separates_verified_effect_from_unverified_authority(self):
        self.assertEqual(
            self.packet["status"],
            "READBACK_VERIFIED_AUTHORITY_INCIDENT_OPEN",
        )
        self.assertEqual(
            self.packet["provider"]["project_id"],
            "fawkirqroyniueeqspif",
        )
        authorization = self.packet["authorization"]
        self.assertEqual(
            authorization["current_classification"],
            "UNVERIFIED_PROTECTED_EFFECT_AUTHORITY",
        )
        self.assertEqual(
            authorization["current_verification"],
            "NO_SEPARATE_EXACT_PATRICK_AUTHORIZATION_LOCATED",
        )
        self.assertEqual(
            authorization["historical_recorded_claim"]["authority"],
            "Patrick current direct instruction",
        )
        self.assertIn(
            "is not accepted as sufficient exact authorization",
            authorization["reconciliation_note"],
        )
        self.assertEqual(
            self.packet["provider_effect"]["result"],
            "APPLIED_VERIFIED",
        )
        self.assertEqual(
            self.packet["provider_effect"]["migration_version"],
            "20260921192624",
        )
        self.assertIsNone(self.packet["exact_authorization_needed"])
        self.assertIn(
            "does not retroactively authorize",
            self.packet["retention_decision_needed"],
        )
        self.assertTrue(
            self.packet["rollback_recovery"][
                "emergency_regrant_requires_separate_authority"
            ]
        )


if __name__ == "__main__":
    unittest.main()
