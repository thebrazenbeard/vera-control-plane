import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "veraport_mcp_live_bootstrap_observation_20260920.json"


def test_transport_pass_is_not_promoted_to_application_current_route():
    value = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert value["direct_path"]["transport_classification"] == "FRESH_TRANSPORT_REACHABLE"
    assert value["direct_path"]["application_currentness"].startswith("UNQUALIFIED")
    assert value["synology_edge_path"]["transport_classification"] == "FRESH_TRANSPORT_REACHABLE"
    assert value["synology_edge_path"]["application_currentness"].startswith("UNQUALIFIED")
    assert value["current_route_result"]["selected_application_route"] == "NONE_QUALIFIED_YET"


def test_process_execution_stays_on_hold_from_live_local_policy():
    value = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    assert value["lappy"]["service_config"]["allow_process_exec"] is False
    assert value["process_result"]["PROCESS_EXEC_PASS"] is False
    assert value["process_result"]["activation"] == "HOLD"


def test_blocked_bootstrap_attempt_is_not_recorded_as_veraport_failure():
    value = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    live = value["live_application_acceptance"]
    assert live["executed"] is False
    assert live["lane_list"] == "NOT_OBSERVED"
    assert live["live_fs_read"] == "NOT_OBSERVED"
