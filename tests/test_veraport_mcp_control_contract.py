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
        "LOGICAL_READ_CLOSE_RACE",
        "POST_CLOSE_MIRROR_MATERIALIZATION",
        "CONTROLLER_RESTART_FENCE_REUSE",
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


def test_contract_is_bound_to_current_vera_implementation_subject():
    value = load()
    subject = value["implementation_subject"]
    assert subject["repository"] == "thebrazenbeard/vera-mesh"
    assert subject["pull_request"] == 12
    assert subject["branch"] == "vera/veraport-chatgpt-mcp-v2-20260920"
    assert subject["head"] == "9bffc57930587bf74a12657bbeaa913474ab5574"
    assert subject["review_state"] == "CHANGES_REQUIRED_EXACT_HEAD"


def test_live_process_policy_remains_hold():
    value = load()
    assert value["process_activation"]["current_live_workstation_policy"] == "FALSE_READBACK_20260920"
    assert value["routes"]["current_application_route"] == (
        "NONE_QUALIFIED_PENDING_CONTROLLER_PRIVATE_KEY"
    )


def test_close_is_a_linearization_boundary_for_lane_authority():
    fencing = load()["concurrency_fencing"]
    assert fencing["lane_close_linearization"] == (
        "CLOSE_RETURN_MUST_FENCE_ALL_PRIOR_AND_CONCURRENT_LANE_OPERATIONS"
    )
    assert fencing["post_close_mirror_materialization"] == "FORBIDDEN"
    assert fencing["post_close_content_return"] == "FORBIDDEN"
    assert fencing["await_boundary_rule"] == (
        "AUTHORITY_MUST_BE_REVALIDATED_OR_SERIALIZED_ACROSS_ASYNC_AWAITS"
    )


def test_fence_identity_never_repeats_across_controller_restart():
    fencing = load()["concurrency_fencing"]
    assert fencing["controller_restart_fence_reuse"] == "FORBIDDEN"
    assert fencing["stale_prior_lifetime_fence"] == "MUST_REJECT"
    assert fencing["fence_generation_requirement"] == (
        "NONREPEATING_ACROSS_CONTROLLER_LIFETIMES_OR_DURABLY_MONOTONIC"
    )
    assert set(fencing["required_tests"]) >= {
        "BLOCKED_READ_RACES_CLOSE",
        "BLOCKED_MIRROR_OPEN_RACES_CLOSE",
        "CONTROLLER_RESTART_STALE_FENCE",
        "REOPEN_SAME_LANE_ID_AFTER_RESTART",
        "NO_POST_CLOSE_REMOTE_OPERATION",
    }


def test_transport_blackhole_has_explicit_bounded_failover_semantics():
    value = load()["transport_deadlines"]
    assert value["connect_tls_application_handshake"] == "BOUNDED_REQUIRED"
    assert value["probe"] == "BOUNDED_REQUIRED"
    assert value["operation"] == "BOUNDED_REQUIRED"
    assert value["read_only_timeout"] == "MAY_FAILOVER_AS_TRANSPORT_FAILURE"
    assert value["mutation_timeout"] == "AMBIGUOUS_DELIVERY"
    assert value["direct_blackhole_must_not_block_edge"] == "REQUIRED"


def test_path_freshness_policy_is_one_value_everywhere():
    policy = load()["routes"]["max_path_age_policy"]
    assert policy["single_authoritative_value"] == "ControllerConfig.max_path_age_ms"
    assert set(policy["must_apply_to"]) == {
        "MACHINE_INFO",
        "READ_ROUTER",
        "GATEWAY_LANE_CONTROL",
        "GATEWAY_WRITE",
        "GATEWAY_PROCESS",
    }
    assert policy["hard_coded_secondary_default"] == "FORBIDDEN"


def test_workstation_close_cannot_claim_drained_while_effects_continue():
    semantics = load()["concurrency_fencing"]["workstation_close_semantics"]
    assert semantics["required_choice"] == (
        "DRAIN_BEFORE_CLOSE_RETURN_OR_EXPLICIT_INFLIGHT_STATE"
    )
    assert semantics["simple_closed_true_while_effects_continue"] == "FORBIDDEN"
    assert set(semantics["must_cover"]) >= {"FS_READ", "FS_WRITE", "PROCESS_EXECUTION"}


def test_file_read_bound_is_not_confused_with_wire_frame_bound():
    wire = load()["wire_limits"]
    assert wire["local_file_read_limit_ne_wire_frame_limit"] is True
    assert wire["successful_executor_result_must_fit_or_be_chunked"] is True
    assert wire["json_escape_expansion_must_be_accounted"] is True
    assert wire["uncorrelated_task_failure"] == "FORBIDDEN"
    assert wire["client_wait_without_deadline"] == "FORBIDDEN"
    assert wire["preferred_file_read_model"] == (
        "RANGED_OR_CHUNKED_READ_WITH_EXPLICIT_LIMITS"
    )


def test_session_lifetime_bounds_lane_lifetime_and_cleanup():
    lifecycle = load()["session_lifecycle"]
    assert lifecycle["lane_ttl_must_not_exceed_remaining_session_lifetime"] is True
    assert lifecycle["session_disconnect_cleanup"] == (
        "DRAIN_THEN_REAP_EXACT_SESSION_LANES"
    )
    assert lifecycle["cross_session_reap"] == "FORBIDDEN"
    assert lifecycle["dead_session_resource_claims"] == (
        "MUST_NOT_PERSIST_BEYOND_BOUNDED_DRAIN"
    )
    assert lifecycle["reconnect_storm_lane_leak"] == "FORBIDDEN"


def test_session_expiry_is_truthful_admission_cutoff():
    lifecycle = load()["session_lifecycle"]
    assert lifecycle["expiry_semantics"] == (
        "ADMISSION_CUTOFF_NOT_IMPLICIT_INSTANT_EFFECT_CANCELLATION"
    )
    assert lifecycle["session_expiry_cleanup"] == (
        "NO_NEW_ADMISSION_THEN_DRAIN_BOUNDED_INFLIGHT_AND_REAP"
    )


def test_logical_close_never_ignores_remote_application_failure():
    close = load()["concurrency_fencing"]["logical_close_truth"]
    assert close["remote_application_errors_must_be_inspected"] is True
    assert close["closed_true_requires"] == (
        "ALL_REACHABLE_MIRRORS_PROVEN_CLOSED_OR_ALREADY_ABSENT"
    )
    assert close["unresolved_mirror"] == "PARTIAL_OR_UNKNOWN_NOT_SUCCESS"
    assert close["reconciliation_state_required"] is True


def test_chatgpt_product_gate_is_separate_from_tunnel_transport():
    exposure = load()["chatgpt_exposure"]
    product = exposure["product_gate"]
    tunnel = exposure["secure_tunnel"]
    assert product["current_workspace_availability"] == "MUST_BE_LIVE_VERIFIED"
    assert product["missing_product_path"] == (
        "CHATGPT_PRODUCT_GATE_UNAVAILABLE_NOT_TRANSPORT_FAILURE"
    )
    assert product["no_public_ingress_workaround_without_review"] is True
    assert tunnel["network_model"] == "OUTBOUND_HTTPS_FROM_TRUST_BOUNDARY"
    assert tunnel["public_inbound_required"] is False
    assert tunnel["tunnel_authority"] == "NO_VERAPORT_MACHINE_AUTHORITY"
    assert tunnel["credentials_git_bus_logs"] == "FORBIDDEN"
    assert product["states"][0] == "MCP_SERVER_RUNNING"
    assert product["states"][-1] == "WRITE_TOOL_INVOCATION_PASS"


def test_request_ledger_is_bounded_without_replay_regression():
    ledger = load()["request_ledger"]
    assert ledger["durable_idempotency_scope"] == (
        "MUTATION_OPERATIONS_ONLY_UNLESS_READ_LEDGER_SEPARATELY_JUSTIFIED"
    )
    assert ledger["read_probe_permanent_rows"] == "FORBIDDEN"
    assert ledger["unbounded_request_table"] == "FORBIDDEN"
    assert ledger["mutation_retention"] == (
        "BOUNDED_POLICY_REQUIRED_WITH_REPLAY_SAFETY"
    )
    assert ledger["late_retry_after_detail_gc"] == (
        "MUST_REJECT_OR_USE_COMPACT_TOMBSTONE_NOT_REEXECUTE"
    )
    assert ledger["disk_full_before_mutation_admission"] == "FAIL_CLOSED"


def test_max_inflight_bounds_admitted_requests_not_only_execution():
    admission = load()["request_admission"]
    assert admission["max_inflight_semantics"] == (
        "BOUND_ADMITTED_OUTSTANDING_REQUESTS_NOT_ONLY_EXECUTING_HANDLERS"
    )
    assert admission["unbounded_waiting_tasks"] == "FORBIDDEN"
    assert admission["backpressure_before_unbounded_task_creation"] == "REQUIRED"
    assert admission["accepted_request_without_correlated_terminal_result"] == "FORBIDDEN"
    assert admission["teardown_under_overload"] == "BOUNDED_REQUIRED"


def test_review_provenance_requires_two_distinct_exact_head_reviews():
    value = load()
    review = value["review_provenance"]
    assert review["required_for_machine_acceptance"] is True
    assert review["exact_reviewed_head"] == "9bffc57930587bf74a12657bbeaa913474ab5574"
    assert review["required_classes"] == [
        "VCP_SOURCE_REVIEW",
        "INDEPENDENT_SOURCE_REVIEW",
    ]
    assert review["reviewed_head_must_equal_implementation_head"] is True
    assert review["one_identity_cannot_satisfy_both_classes"] is True
    assert review["one_evidence_object_cannot_satisfy_both_classes"] is True
    assert review["self_attested_pass_strings"] == "FORBIDDEN"
    assert review["each_review_requires"] == [
        "IMMUTABLE_EVIDENCE_ID",
        "IMMUTABLE_EVIDENCE_CONTENT_SHA256",
        "AUTHENTICATED_EVIDENCE_RESOLUTION",
    ]
    assert review["resolved_evidence_must_derive"] == [
        "REVIEW_CLASS",
        "TARGET_REPOSITORY",
        "PULL_REQUEST",
        "REVIEWED_HEAD",
        "REVIEWER_IDENTITY",
        "PASS_VERDICT",
    ]
    assert review["receipt_claims_are_not_trust_root"] is True
    assert review["unresolved_or_unavailable_evidence"] == (
        "PENDING_REVIEW_EVIDENCE_NE_PASS"
    )
    assert review["resolved_identity_and_content_digest_must_match_reference"] is True
    assert review["authenticated_admission_schema"] == (
        "VERAPORT_AUTHENTICATED_REVIEW_ADMISSION_V1"
    )
    assert review["resolver_trust_boundary"] == (
        "OUT_OF_BAND_AUTHENTICATED_SOURCE_NOT_RECEIPT_CONTROLLED"
    )
    assert review["admission_payload_is_source_of_review_facts"] is True
    assert review["current_exact_head_state"] == (
        "CHANGES_REQUIRED_WIRE_AND_SESSION_LIFECYCLE"
    )
    assert review["current_exact_head_evidence"] == (
        "vera-mesh#12 issuecomment-5769570530"
    )
