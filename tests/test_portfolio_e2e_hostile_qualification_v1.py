import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "governance" / "VERA_PORTFOLIO_E2E_HOSTILE_QUALIFICATION_V1.json"


def test_portfolio_e2e_hostile_qualification_fails_closed_at_real_boundary():
    data = json.loads(Q.read_text(encoding="utf-8"))
    assert data["schema"] == "VERA_PORTFOLIO_E2E_HOSTILE_QUALIFICATION_V1"
    assert data["overall_status"] == "FAIL_CLOSED_INTEGRATION_NOT_QUALIFIED"
    assert data["canonical_cut"]["discovery"]["repository_count"] == 59
    assert data["canonical_cut"]["vera"]["source_rows"] == 42
    assert data["canonical_cut"]["vera"]["no_auto_bind"] == 17
    assert data["route_and_projection"]["current_vera_lane"] == "bus/vera-v2"
    assert data["route_and_projection"]["historical_supabase_endpoint"] == "bus/vera-sol-v1"
    assert data["route_and_projection"]["historical_endpoint_authoritative"] is False
    assert data["route_and_projection"]["radar_projection_lane_state_rows"] == 0
    assert data["route_and_projection"]["radar_projection_batch_rows"] == 0
    assert data["route_and_projection"]["qualification"] == "FAIL_GLOBAL_GITHUB_TO_RADAR_PROJECTION_STALE"
    assert data["deployed_edge_source_custody"]["matching_git_subject"]["state"] == "OPEN_DRAFT_UNMERGED"
    assert data["workbridge"]["current_head_ci_runs"][0]["conclusion"] == "success"
    assert data["workbridge"]["installed_or_registered"] is False
    assert data["closeout"]["first_hard_failure"] == "BUS_TO_RADAR_PROJECTION"


def test_no_runner_failures_are_not_test_failures_or_passes():
    data = json.loads(Q.read_text(encoding="utf-8"))
    actions = data["github_actions"]
    assert actions["vera_pr198"]["classification"] == "PRIVATE_HOSTED_RUNNER_NO_EXECUTION"
    assert actions["vcp_pr127"]["classification"] == "PRIVATE_HOSTED_RUNNER_NO_EXECUTION"
    assert actions["bus_pr325"]["classification"] == "PRIVATE_HOSTED_RUNNER_NO_EXECUTION"
    assert actions["vera_pr198"]["all_failed_jobs_had_steps_null"] is True
    assert actions["vcp_pr127"]["all_failed_jobs_had_steps_null"] is True
    assert actions["bus_pr325"]["all_failed_jobs_had_steps_null"] is True



def test_vcp_no_auto_bind_enforcement_gap_is_not_laundered_as_canonical_pass():
    data = json.loads(Q.read_text(encoding="utf-8"))
    enforcement = data["vcp_source_disposition_enforcement"]
    assert enforcement["canonical_main"]["status"] == (
        "EXACT_SOURCE_BINDING_PRESENT_BUT_NO_AUTO_BIND_POLICY_NOT_EXECUTABLY_ENFORCED"
    )
    assert enforcement["candidate_repair"]["status"] == (
        "SOURCE_CANDIDATE_ENFORCEMENT_PASS_NOT_CANONICAL"
    )
    assert enforcement["candidate_repair"]["bound_no_auto_bind_count"] == 17
    assert enforcement["candidate_repair"]["vera_works_class"] == "DOMAIN_PROJECT"
    assert enforcement["candidate_repair"]["vera_works_load_mode"] == "TASK_SPECIFIC_ONLY"


def test_direct_hostile_rerun_preserves_first_real_integration_failure():
    data = json.loads(Q.read_text(encoding="utf-8"))
    rerun = data["hostile_rerun_20260923"]
    assert rerun["check_count"] == 24
    assert rerun["passed"] == 21
    assert rerun["failed"] == 3
    assert rerun["first_integration_failure"] == "BUS_RADAR_PROJECTION"
    assert rerun["verdict"] == "FAIL_CLOSED_INTEGRATION_NOT_QUALIFIED"
    failed = {row["id"] for row in rerun["failed_checks"]}
    assert failed == {
        "BUS_RADAR_PROJECTION",
        "RADAR_MESSAGE_FRESHNESS",
        "RECOVERY_RUNTIME_GATE",
    }


def test_historical_provider_projection_is_not_rewritten_into_current_route():
    data = json.loads(Q.read_text(encoding="utf-8"))
    route = data["hostile_rerun_20260923"]["provider_route_readback"]
    assert route["lane_vera"]["address"] == "bus/vera-sol-v1"
    assert route["lane_vera"]["historical_branch_name"] is True
    assert route["lane_vera"]["liveness_claimed"] is False
    assert route["identity_vera"]["lifecycle_status"] == "ACTIVE"
    assert route["identity_vera_sol"]["lifecycle_status"] == "ARCHIVED"
    assert route["interpretation"] == (
        "HISTORICAL_PROVIDER_PROJECTION_NON_AUTHORITATIVE_FOR_CURRENT_ROUTING"
    )
