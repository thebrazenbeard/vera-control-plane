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


if __name__ == "__main__":
    unittest.main()
