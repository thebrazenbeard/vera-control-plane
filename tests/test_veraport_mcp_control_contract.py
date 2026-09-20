import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "VERAPORT_MCP_CONTROL_CONTRACT_V1.json"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_state_machine_keeps_effect_states_separate():
    value = load()
    assert value["state_model"] == [
        "SOURCE_CREATED",
        "BUILD_PASS",
        "MCP_SERVER_RUNNING",
        "PLUGIN_REGISTERED",
        "CURRENT_ROUTE",
        "LIVE_READ_PASS",
        "LIVE_WRITE_PASS",
        "PROCESS_EXEC_PASS",
        "RDC_EQUIVALENCE_BOUNDARY_PASS",
    ]
    assert len(value["state_non_implications"]) == 8


def test_tool_discoverability_and_edge_transport_do_not_grant_authority():
    ceiling = load()["authority_ceiling"]
    assert ceiling["tool_discoverability"] == "NO_AUTHORITY"
    assert ceiling["edge_reachability"] == "NO_APPLICATION_AUTHORITY"
    assert ceiling["source_presence"] == "NO_INSTALL_OR_CURRENT_ROUTE_AUTHORITY"


def test_unknown_mutation_delivery_never_crosses_application_session():
    failover = load()["mutation_failover"]
    assert failover["unknown_delivery"] == "NO_CROSS_SESSION_RETRY"
    assert failover["same_request_id_required"] is True
    assert failover["same_application_session_required"] is True
    assert failover["durable_idempotency_required"] is True
    assert failover["no_compatible_same_session_path"] == "AMBIGUOUS_DELIVERY_STOP"


def test_current_route_requires_application_auth_and_readback():
    routes = load()["routes"]
    required = set(routes["current_requires"])
    assert "VERAPORT_APPLICATION_AUTH_PASS" in required
    assert "LIVE_APPLICATION_READBACK" in required
    assert routes["edge_tls_only"] == "TRANSPORT_REACHABLE_NOT_CURRENT_APPLICATION_ROUTE"
    assert routes["DURABLE_RELAY"] == "FUTURE_NOT_IMPLEMENTED_NOT_CURRENT"


def test_process_activation_requires_local_policy_and_exact_head_review():
    process = load()["process_activation"]
    required = set(process["required_all"])
    assert "VCP_EXACT_HEAD_SOURCE_REVIEW_PASS" in required
    assert "LIVE_WORKSTATION_ALLOW_PROCESS_EXEC_TRUE" in required
    assert "PATRICK_EXACT_PROCESS_EFFECT_AUTHORITY_WHEN_ACTIVATING_OR_EXECUTING" in required
    assert process["pid_only_termination"] == "FORBIDDEN"
    assert process["managed_process_handle_required"] is True


def test_mcp_transport_reconnect_does_not_promote_session_resume_claim():
    reconnect = load()["mcp_reconnect"]
    assert reconnect["client_transport_reconnect"] == (
        "MUST_REUSE_EXISTING_CONTROLLER_RUNTIME_WHERE_RUNNING"
    )
    assert reconnect["controller_process_restart"] == (
        "APPLICATION_SESSION_RECREATION_CURRENTLY_REQUIRED"
    )
    assert reconnect["session_resume_across_controller_restart"] == "NOT_IMPLEMENTED"


def test_required_hostile_regressions_are_frozen():
    attacks = set(load()["hostile_regressions"])
    for required in {
        "TOOL_DISCOVERABILITY_AUTHORITY",
        "MUTATION_REPLAY_CROSS_SESSION",
        "PID_REUSE",
        "SESSION_EXPIRY_RACE",
        "LANE_FENCING_RACE",
        "CONTROLLER_KEY_MISMATCH",
        "WORKSTATION_KEY_MISMATCH",
        "SOURCE_AS_INSTALL_OR_CURRENT_ROUTE",
    }:
        assert required in attacks


def test_local_mcp_server_does_not_equal_chatgpt_registration():
    exposure = load()["chatgpt_exposure"]
    assert exposure["local_mcp_server"] == "NOT_DIRECTLY_REACHABLE_BY_CHATGPT"
    assert exposure["preferred_private_mode"] == "SECURE_MCP_TUNNEL"
    assert exposure["tunnel_effect_class"] == (
        "ADMINISTRATIVE_PROVIDER_AND_CREDENTIAL_EFFECT"
    )
    assert exposure["local_server_non_implication"] == (
        "MCP_SERVER_RUNNING_NE_PLUGIN_REGISTERED"
    )
    assert "PRODUCT_SIDE_REGISTRATION_READBACK" in (
        exposure["plugin_registered_requires"]
    )
