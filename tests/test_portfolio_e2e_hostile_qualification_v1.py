import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "governance" / "VERA_PORTFOLIO_E2E_HOSTILE_QUALIFICATION_V1.json"


def load():
    return json.loads(Q.read_text(encoding="utf-8"))


def test_portfolio_e2e_hostile_qualification_fails_closed_at_real_boundary():
    data = load()
    assert data["schema"] == "VERA_PORTFOLIO_E2E_HOSTILE_QUALIFICATION_V1"
    assert data["overall_status"] == "FAIL_CLOSED_INTEGRATION_NOT_QUALIFIED"
    assert data["canonical_cut"]["discovery"]["repository_count"] == 59
    assert data["canonical_cut"]["vera"]["source_rows"] == 42
    assert data["canonical_cut"]["vera"]["no_auto_bind"] == 17
    assert data["canonical_cut"]["vcp"]["candidate_zero_behind_current_main"] is True
    assert data["route_and_projection"]["current_vera_lane"] == "bus/vera-v2"
    assert data["route_and_projection"]["historical_supabase_endpoint"] == "bus/vera-sol-v1"
    assert data["route_and_projection"]["historical_endpoint_authoritative"] is False
    assert data["route_and_projection"]["radar_projection_lane_state_rows"] == 0
    assert data["route_and_projection"]["radar_projection_batch_rows"] == 0
    assert data["route_and_projection"]["qualification"] == "FAIL_GLOBAL_GITHUB_TO_RADAR_PROJECTION_STALE"
    assert data["closeout"]["first_hard_failure"] == "BUS_TO_RADAR_PROJECTION"


def test_deployed_edge_source_custody_is_current_and_not_a_runtime_pass():
    data = load()
    custody = data["deployed_edge_source_custody"]
    assert custody["qualification"] == "PASS_DEPLOYED_PROVIDER_BYTES_MATCH_CANONICAL_BUS_MAIN"
    assert custody["current_canonical_bus_main"] == data["canonical_cut"]["bus"]["main"]
    assert custody["fresh_provider_byte_match"] == {
        "index": True,
        "handler": True,
        "deno_json": True,
    }
    assert data["route_and_projection"]["qualification"] == "FAIL_GLOBAL_GITHUB_TO_RADAR_PROJECTION_STALE"
    edge_stage = next(row for row in data["stages"] if row["stage"] == "EDGE_SOURCE_CUSTODY")
    projection_stage = next(row for row in data["stages"] if row["stage"] == "BUS_TO_RADAR_PROJECTION")
    assert edge_stage["status"] == "PASS"
    assert projection_stage["status"] == "FAIL"


def test_runner_availability_does_not_launder_canonical_radar_execution():
    data = load()
    actions = data["github_actions"]
    probe = actions["self_hosted_runner_probe"]
    binding = actions["canonical_radar_runner_binding"]
    assert probe["status"] == "VERIFIED_EXECUTABLE"
    assert probe["conclusion"] == "success"
    assert probe["runner"] == "LAPPY-vera-blender"
    assert binding["trusted_projector_runs_on"] == "ubuntu-latest"
    assert binding["self_hosted_route_bound"] is False
    assert binding["canonical_dispatcher_executed_after_self_hosted_probe"] is False
    assert binding["classification"] == "CANONICAL_RADAR_SELFHOSTED_ROUTING_NOT_YET_BOUND"


def test_vcp_no_auto_bind_enforcement_gap_is_not_laundered_as_canonical_pass():
    data = load()
    enforcement = data["vcp_source_disposition_enforcement"]
    assert enforcement["canonical_main"]["status"] == (
        "EXACT_SOURCE_BINDING_PRESENT_BUT_NO_AUTO_BIND_POLICY_NOT_EXECUTABLY_ENFORCED"
    )
    candidate = enforcement["candidate_repair"]
    assert candidate["status"] == "SOURCE_CANDIDATE_ENFORCEMENT_PASS_NOT_CANONICAL"
    assert candidate["branch"] == "repair/enforce-runtime-source-disposition-v3-20260923"
    assert candidate["zero_behind_current_main"] is True
    assert candidate["bound_no_auto_bind_count"] == 17
    assert candidate["vera_works_class"] == "DOMAIN_PROJECT"
    assert candidate["vera_works_load_mode"] == "TASK_SPECIFIC_ONLY"


def test_direct_hostile_rerun_preserves_first_real_integration_failure():
    data = load()
    rerun = data["hostile_rerun_20260923"]
    assert rerun["check_count"] == 24
    assert rerun["passed"] == 21
    assert rerun["failed"] == 3
    assert rerun["subject"]["vcp_candidate"]["zero_behind"] is True
    assert rerun["first_integration_failure"] == "BUS_RADAR_PROJECTION"
    assert rerun["verdict"] == "FAIL_CLOSED_INTEGRATION_NOT_QUALIFIED"
    failed = {row["id"] for row in rerun["failed_checks"]}
    assert failed == {
        "BUS_RADAR_PROJECTION",
        "RADAR_MESSAGE_FRESHNESS",
        "RECOVERY_RUNTIME_GATE",
    }


def test_historical_provider_projection_is_not_rewritten_into_current_route():
    data = load()
    route = data["hostile_rerun_20260923"]["provider_route_readback"]
    assert route["lane_vera"]["address"] == "bus/vera-sol-v1"
    assert route["lane_vera"]["historical_branch_name"] is True
    assert route["lane_vera"]["liveness_claimed"] is False
    assert route["identity_vera"]["lifecycle_status"] == "ACTIVE"
    assert route["identity_vera_sol"]["lifecycle_status"] == "ARCHIVED"
    assert route["interpretation"] == (
        "HISTORICAL_PROVIDER_PROJECTION_NON_AUTHORITATIVE_FOR_CURRENT_ROUTING"
    )


def test_fresh_currentness_packet_rejects_count_only_and_post_cut_promotion():
    data = load()
    fresh = data["fresh_currentness_reconciliation_20260923"]
    assert fresh["repository_set_equality"] == {
        "discovery": 59,
        "vera": 59,
        "vcp": 59,
        "all_exactly_equal": True,
    }
    assert fresh["partition"]["bound_conditional"] == 41
    assert fresh["partition"]["predecessor_evidence"] == 1
    assert fresh["partition"]["no_auto_bind"] == 17
    assert fresh["partition"]["no_auto_bind_exactly_equal_across_discovery_vera_vcp"] is True
    assert fresh["meso_crct"]["in_frozen_59"] is False
    assert fresh["meso_crct"]["disposition"] == "OUTSIDE_CANONICAL_59_CUT_NO_SILENT_PROMOTION"


def test_qualification_contains_no_superseded_currentness_claims():
    raw = Q.read_text(encoding="utf-8")
    forbidden = (
        "FAIL_DEPLOYED_PROVIDER_SOURCE_NOT_CANONICAL_MAIN",
        "B3_BUS_EDGE_SOURCE_NOT_CANONICAL",
        "repair/enforce-runtime-source-disposition-v2-20260923",
        "92c66159d9b610a94f59066ab2bb6416f4513093",
        "deployed bytes match an unmerged draft PR",
    )
    for stale in forbidden:
        assert stale not in raw
