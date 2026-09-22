import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "VERAPORT_MACHINE_ACCEPTANCE_SEQUENCE_V1.json"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_machine_acceptance_sequence_is_strictly_ordered_and_non_skippable():
    value = load()
    assert value["ordered_steps"] == [
        "CONTROLLER_IDENTITY",
        "READ_ONLY_TRUST",
        "SERVICE_RESTART_AND_READBACK",
        "DIRECT_APPLICATION_AUTH",
        "EDGE_APPLICATION_AUTH",
        "LANE_LIST",
        "READ_ONLY_LANE_OPEN",
        "BOUNDED_READ",
        "DRAINED_CLOSE",
    ]
    assert value["non_skippable"] is True


def test_entry_gate_requires_exact_head_and_distinct_durable_reviews():
    value = load()
    subject = value["implementation_subject"]
    assert subject == {
        "repository": "thebrazenbeard/vera-mesh",
        "pull_request": 12,
        "exact_head": "9bffc57930587bf74a12657bbeaa913474ab5574",
        "current_review_state": "PENDING_EXACT_HEAD_REVIEW",
    }
    gate = value["entry_gate"]
    assert gate["vera_mesh_pr12_exact_head_review"] == (
        "TWO_DISTINCT_DURABLE_PASS_REVIEWS_REQUIRED"
    )
    assert gate["independent_reviewer"] == (
        "DISTINCT_INDEPENDENT_REVIEW_IDENTITY_AND_EVIDENCE_REQUIRED"
    )
    assert gate["review_provenance"] == (
        "VCP_AND_INDEPENDENT_REVIEWS_MUST_BIND_EXACT_IMPLEMENTATION_HEAD"
    )
    assert gate["self_attested_review_pass"] == "FORBIDDEN"
    assert gate["vcp_control_contract"] == "PASS_REQUIRED"

def test_initial_trust_is_read_only():
    trust = load()["steps"]["READ_ONLY_TRUST"]
    required = set(trust["success_requires"])
    assert "CAPABILITY_CEILING_EXACTLY_FS_READ" in required
    assert "NO_FS_WRITE" in required
    assert "NO_PROCESS_EXEC" in required


def test_direct_and_edge_require_application_auth_not_transport_only():
    value = load()
    route = value["route_acceptance"]
    assert route["direct_and_edge_must_both_pass_application_auth"] is True
    assert route["transport_only_is_insufficient"] is True
    assert route["same_workstation_identity_required"] is True
    assert route["same_controller_identity_required"] is True


def test_lane_open_is_session_bounded_and_fenced():
    opened = load()["steps"]["READ_ONLY_LANE_OPEN"]["success_requires"]
    assert "TTL_NOT_GREATER_THAN_REMAINING_SESSION_LIFETIME" in opened
    assert "NONREUSABLE_FENCE_IDENTITY" in opened
    assert "NO_WRITE_CLAIM" in opened


def test_bounded_read_is_bounded_on_wire_and_time():
    required = set(load()["steps"]["BOUNDED_READ"]["success_requires"])
    assert "READ_WITHIN_DECLARED_BYTE_LIMIT" in required
    assert "WIRE_RESPONSE_WITHIN_FRAME_POLICY_OR_CHUNKED_POLICY" in required
    assert "OPERATION_DEADLINE_OBSERVED" in required


def test_close_is_a_drained_authority_boundary():
    required = set(load()["steps"]["DRAINED_CLOSE"]["success_requires"])
    assert "NO_INFLIGHT_LANE_OPERATION_REMAINS" in required
    assert "NO_POST_CLOSE_REMOTE_OPERATION" in required
    assert "NO_POST_CLOSE_CONTENT_RETURN" in required
    assert "RESOURCE_CLAIM_RELEASED" in required
    assert "REOPEN_REQUIRES_NEW_NONREUSED_FENCE" in required


def test_read_only_machine_acceptance_does_not_promote_write_or_process():
    completion = load()["completion_state"]
    assert completion["name"] == "LIVE_READ_ONLY_MACHINE_ACCEPTANCE_PASS"
    assert "FS_WRITE_PASS" in completion["does_not_establish"]
    assert "PROCESS_EXEC_PASS" in completion["does_not_establish"]
    assert "CHATGPT_PLUGIN_REGISTERED" in completion["does_not_establish"]


def test_source_contract_does_not_authorize_machine_effects():
    forbidden = set(load()["protected_effects_not_authorized_by_this_contract"])
    assert {
        "CREDENTIAL_ROTATION",
        "TRUST_MUTATION",
        "SERVICE_RESTART",
        "FS_WRITE",
        "PROCESS_POLICY_ENABLE",
        "PROCESS_EXECUTION",
        "MCP_TUNNEL_CREATION",
        "CHATGPT_APP_REGISTRATION",
        "MERGE",
        "DEPLOY",
    }.issubset(forbidden)
