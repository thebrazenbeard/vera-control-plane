"""Synthetic adversarial checks; no network, user hosts, or provider effects."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_agent_protocol_boundaries_v1 import validate  # noqa E402

BASE = json.loads((ROOT / "protocol" / "VERA_AGENT_PROTOCOL_BOUNDARIES_V1.json").read_text(encoding="utf-8"))


class DecisionContractTests(unittest.TestCase):
    def test_valid_candidate(self):
        self.assertEqual(validate(copy.deepcopy(BASE)), [])

    def test_activated_source_rejected(self):
        d = copy.deepcopy(BASE); d["status"] = "INSTALLED"
        self.assertTrue(validate(d))

    def test_transport_cannot_be_authority(self):
        d = copy.deepcopy(BASE); d["authority_rule"] = "MCP_GRANTS_ACCESS"
        self.assertTrue(validate(d))

    def test_duplicate_path_id_rejected(self):
        d = copy.deepcopy(BASE); d["paths"][1]["id"] = d["paths"][0]["id"]
        self.assertTrue(validate(d))

    def test_a2a_cannot_replace_tool_access(self):
        d = copy.deepcopy(BASE); d["paths"][0]["mechanism"] = "A2A"
        self.assertTrue(validate(d))

    def test_bus_cannot_impersonate_mcp(self):
        d = copy.deepcopy(BASE); d["paths"][1]["kind"] = "TOOL_ACCESS"
        self.assertTrue(validate(d))

    def test_no_immediate_a2a_adoption(self):
        d = copy.deepcopy(BASE); d["paths"][2]["adoption"] = "ACTIVE"
        self.assertTrue(validate(d))

    def test_a2a_requires_scope(self):
        d = copy.deepcopy(BASE); d["paths"][2]["controls"].remove("EXPLICIT_SCOPE")
        self.assertTrue(validate(d))

    def test_no_input_without_separate_lease(self):
        d = copy.deepcopy(BASE); d["paths"][5]["controls"].remove("SEPARATE_INPUT_LEASE")
        self.assertTrue(validate(d))

    def test_client_button_is_not_approval(self):
        d = copy.deepcopy(BASE); d["paths"][6]["controls"].remove("SERVER_SIDE_APPROVAL_CHECK")
        self.assertTrue(validate(d))

    def test_mutation_timeout_never_blind_retry(self):
        d = copy.deepcopy(BASE); d["failure_contract"]["mutation_timeout"] = "RETRY_IMMEDIATELY"
        self.assertTrue(validate(d))

    def test_route_failure_no_silent_fallback(self):
        d = copy.deepcopy(BASE); d["failure_contract"]["unavailable_requested_route"] = "FALLBACK_TO_MCP"
        self.assertTrue(validate(d))

    def test_transport_drop_revokes_input(self):
        d = copy.deepcopy(BASE); d["failure_contract"]["transport_loss"] = "RETRY_INPUT"
        self.assertTrue(validate(d))

    def test_missing_permission_rejected(self):
        d = copy.deepcopy(BASE); d["paths"][4]["permission_source"] = ""
        self.assertTrue(validate(d))

    def test_incomplete_inventory_rejected(self):
        d = copy.deepcopy(BASE); d["paths"].pop()
        self.assertTrue(validate(d))

    def test_malformed_path_rejected(self):
        d = copy.deepcopy(BASE); d["paths"][1] = None
        self.assertTrue(validate(d))

    def test_malformed_root_rejected(self):
        self.assertTrue(validate([]))

    def test_unhashable_kind_rejected_without_exception(self):
        d = copy.deepcopy(BASE); d["paths"][0]["kind"] = ["TOOL_ACCESS"]
        self.assertTrue(validate(d))

    def test_non_string_controls_rejected_without_exception(self):
        d = copy.deepcopy(BASE); d["paths"][2]["controls"] = [["EXACT_TASK_ID"]]
        self.assertTrue(validate(d))

    def test_null_non_claims_rejected_without_exception(self):
        d = copy.deepcopy(BASE); d["non_claims"] = None
        self.assertTrue(validate(d))

    def test_no_auth_token_promotion(self):
        d = copy.deepcopy(BASE); d["non_claims"].remove("NOT_AN_AUTHORIZATION_TOKEN")
        self.assertTrue(validate(d))


    def test_tool_path_cannot_recast_as_a2a_with_coherent_metadata(self):
        d = copy.deepcopy(BASE)
        tool = d["paths"][0]
        agent = d["paths"][2]
        tool["kind"] = "AGENT_DELEGATION"
        tool["mechanism"] = "A2A"
        tool["adoption"] = "DEFERRED_UNTIL_INDEPENDENT_RUNTIME_VERIFIED"
        tool["controls"] = agent["controls"].copy()
        self.assertTrue(validate(d))

    def test_permission_source_cannot_be_replaced_by_opaque_claim(self):
        d = copy.deepcopy(BASE)
        d["paths"][0]["permission_source"] = "ANYONE_CAN_APPROVE"
        self.assertTrue(validate(d))

    def test_screen_endpoint_cannot_be_silently_retargeted(self):
        d = copy.deepcopy(BASE)
        d["paths"][5]["to"] = "untrusted-screen-host"
        self.assertTrue(validate(d))

    def test_human_approval_path_cannot_downgrade_effect_class(self):
        d = copy.deepcopy(BASE)
        d["paths"][6]["effect_class"] = "SOURCE_COORDINATION_ONLY"
        self.assertTrue(validate(d))


    def test_tool_host_grant_control_cannot_disappear(self):
        d = copy.deepcopy(BASE)
        d["paths"][0]["controls"].remove("HOST_GRANT_CHECK")
        self.assertTrue(validate(d))

    def test_host_service_reconciliation_control_cannot_disappear(self):
        d = copy.deepcopy(BASE)
        d["paths"][4]["controls"].remove("IDEMPOTENCY_OR_RECONCILE")
        self.assertTrue(validate(d))

    def test_bus_owner_lane_control_cannot_disappear(self):
        d = copy.deepcopy(BASE)
        d["paths"][1]["controls"].remove("OWNER_LANE")
        self.assertTrue(validate(d))

    def test_unreviewed_auto_approval_control_cannot_be_injected(self):
        d = copy.deepcopy(BASE)
        d["paths"][6]["controls"].append("AUTO_APPROVE_ALL")
        self.assertTrue(validate(d))

    def test_audit_cannot_be_changed_to_log_private_data(self):
        d = copy.deepcopy(BASE)
        d["failure_contract"]["audit"] = "LOG_PRIVATE_DATA"
        self.assertTrue(validate(d))

    def test_handoff_loss_cannot_drop_owner_reconciliation(self):
        d = copy.deepcopy(BASE)
        del d["failure_contract"]["agent_handoff_loss"]
        self.assertTrue(validate(d))

    def test_mutation_retries_cannot_be_added_by_new_failure_key(self):
        d = copy.deepcopy(BASE)
        d["failure_contract"]["automatic_mutation_retry"] = "YES"
        self.assertTrue(validate(d))

    def test_all_non_install_disclaimers_are_stable(self):
        d = copy.deepcopy(BASE)
        d["non_claims"].remove("NOT_A_DEPLOYMENT")
        self.assertTrue(validate(d))

    def test_logical_id_cannot_silently_change(self):
        d = copy.deepcopy(BASE)
        d["logical_id"] = "OTHER_CONTROL_OWNER"
        self.assertTrue(validate(d))

    def test_scope_cannot_silently_expand(self):
        d = copy.deepcopy(BASE)
        d["scope"] = "active permission authority across all repositories"
        self.assertTrue(validate(d))

    def test_unreviewed_root_runtime_override_is_rejected(self):
        d = copy.deepcopy(BASE)
        d["runtime_enforcement"] = "ENABLED_WITHOUT_REVIEW"
        self.assertTrue(validate(d))

    def test_unreviewed_path_authorization_override_is_rejected(self):
        d = copy.deepcopy(BASE)
        d["paths"][0]["authorization_override"] = "ALLOW"
        self.assertTrue(validate(d))

    def test_cli_does_not_ignore_extra_arguments_and_validate_default(self):
        import subprocess
        import tempfile

        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / "bad.json"
            bad.write_text('{"schema":"UNSAFE"}', encoding="utf-8")
            validator = ROOT / "tools" / "validate_agent_protocol_boundaries_v1.py"
            p = subprocess.run(
                [sys.executable, "-B", str(validator), str(bad), "--unused"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(p.returncode, 0, p.stdout)
            self.assertNotIn('"status": "PASS"', p.stdout)

    def test_cli_rejects_duplicate_json_keys_before_validation(self):
        import subprocess
        import tempfile

        d = copy.deepcopy(BASE)
        source = json.dumps(d)
        source = source.replace(
            '"authority_rule": "TRANSPORT_AND_DISCOVERY_NEVER_CONFER_AUTHORITY",',
            '"authority_rule": "AUTO_GRANT", "authority_rule": "TRANSPORT_AND_DISCOVERY_NEVER_CONFER_AUTHORITY",',
            1,
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "duplicate.json"
            path.write_text(source, encoding="utf-8")
            p = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools" / "validate_agent_protocol_boundaries_v1.py"), str(path)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertNotEqual(p.returncode, 0, p.stdout)
            self.assertNotIn('"status": "PASS"', p.stdout)


if __name__ == "__main__":
    unittest.main()
