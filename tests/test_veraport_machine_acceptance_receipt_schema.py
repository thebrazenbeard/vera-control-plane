import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "protocol" / "VERAPORT_MACHINE_ACCEPTANCE_RECEIPT_V1.schema.json"


def load():
    return json.loads(SCHEMA.read_text(encoding="utf-8"))


def test_receipt_requires_exact_subject_and_durable_review_objects():
    value = load()
    subject = value["properties"]["implementation_subject"]
    assert subject["required"] == ["repository", "pull_request", "exact_head"]
    assert subject["properties"]["repository"]["const"] == "thebrazenbeard/vera-mesh"
    assert subject["properties"]["pull_request"]["const"] == 12
    assert subject["properties"]["exact_head"]["const"] == "9bffc57930587bf74a12657bbeaa913474ab5574"

    reviews = value["properties"]["review_evidence"]
    assert reviews["required"] == ["vcp", "independent"]
    assert reviews["properties"]["vcp"]["allOf"][1]["properties"]["review_class"]["const"] == (
        "VCP_SOURCE_REVIEW"
    )
    assert reviews["properties"]["independent"]["allOf"][1]["properties"]["review_class"]["const"] == (
        "INDEPENDENT_SOURCE_REVIEW"
    )

    evidence = value["$defs"]["reviewEvidence"]
    assert evidence["properties"]["reviewed_head"]["const"] == "9bffc57930587bf74a12657bbeaa913474ab5574"
    assert evidence["properties"]["verdict"]["const"] == "PASS"
    assert "reviewer_identity" in evidence["required"]
    assert "evidence_id" in evidence["required"]


def test_fencing_token_is_positive_integer():
    value = load()
    fence = value["properties"]["lane_open"]["properties"]["fencing_token"]
    assert fence == {"type": "integer", "minimum": 1}

def test_receipt_cannot_encode_write_or_process_capability():
    value = load()
    trust = value["properties"]["trust"]["properties"]
    assert trust["fs_write_granted"]["const"] is False
    assert trust["process_exec_granted"]["const"] is False
    assert trust["capabilities"]["prefixItems"][0]["const"] == "fs.read"
    assert trust["capabilities"]["maxItems"] == 1


def test_routes_require_application_auth_and_exact_identity_shapes():
    route = load()["$defs"]["applicationRoute"]["properties"]
    assert route["tls"]["const"] == "TLSv1.3"
    assert route["alpn"]["const"] == "veraport/1"
    assert route["application_auth"]["const"] == "PASS"
    assert route["controller_principal"]["pattern"].startswith("^controller:")
    assert route["workstation_principal"]["pattern"].startswith("^workstation:")


def test_read_receipt_proves_rdc_did_not_perform_workstation_operation():
    bounded = load()["properties"]["bounded_read"]["properties"]
    assert bounded["rdc_performed_workstation_operation"]["const"] is False
    assert bounded["wire_bound_pass"]["const"] is True
    assert bounded["deadline_pass"]["const"] is True


def test_close_receipt_requires_zero_inflight_and_no_post_close_effect():
    close = load()["properties"]["drained_close"]["properties"]
    assert close["inflight_after_close"]["const"] == 0
    assert close["post_close_remote_operation_observed"]["const"] is False
    assert close["post_close_content_return_observed"]["const"] is False
    assert close["resource_claim_released"]["const"] is True
    assert close["reopen_fence_nonreused"]["const"] is True


def test_claim_ceiling_remains_read_only():
    value = load()
    assert value["properties"]["claim_ceiling"]["const"] == (
        "LIVE_READ_ONLY_MACHINE_ACCEPTANCE_PASS"
    )
    neg = value["properties"]["negative_assertions"]["properties"]
    assert neg["fs_write_performed"]["const"] is False
    assert neg["process_exec_performed"]["const"] is False
    assert neg["chatgpt_app_registered"]["const"] is False
