from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.validate_veraport_machine_acceptance_receipt import (
    IMPLEMENTATION_HEAD,
    VeraPortAcceptanceError,
    validate_review_evidence_binding,
)


def receipt() -> dict:
    return {
        "implementation_subject": {
            "repository": "thebrazenbeard/vera-mesh",
            "pull_request": 12,
            "exact_head": IMPLEMENTATION_HEAD,
        },
        "review_evidence": {
            "vcp": {
                "review_class": "VCP_SOURCE_REVIEW",
                "target_repository": "thebrazenbeard/vera-mesh",
                "pull_request": 12,
                "reviewed_head": IMPLEMENTATION_HEAD,
                "reviewer_identity": "VCP_REVIEWER",
                "evidence_id": "github:review:123",
                "verdict": "PASS",
            },
            "independent": {
                "review_class": "INDEPENDENT_SOURCE_REVIEW",
                "target_repository": "thebrazenbeard/vera-mesh",
                "pull_request": 12,
                "reviewed_head": IMPLEMENTATION_HEAD,
                "reviewer_identity": "BT2_REVIEWER",
                "evidence_id": "bus:" + "a" * 40,
                "verdict": "PASS",
            },
        },
        "lane_open": {"fencing_token": 1},
    }


def test_valid_distinct_exact_head_review_evidence_passes():
    validate_review_evidence_binding(receipt())


def test_plain_self_attested_pass_strings_cannot_replace_review_evidence():
    value = receipt()
    value.pop("review_evidence")
    value["implementation_subject"]["vcp_review"] = "PASS"
    value["implementation_subject"]["independent_review"] = "PASS"
    with pytest.raises(VeraPortAcceptanceError, match="implementation subject"):
        validate_review_evidence_binding(value)


def test_stale_review_head_fails_closed():
    value = receipt()
    value["review_evidence"]["independent"]["reviewed_head"] = "0" * 40
    with pytest.raises(VeraPortAcceptanceError, match="stale/different head"):
        validate_review_evidence_binding(value)


def test_one_reviewer_cannot_satisfy_both_review_classes():
    value = receipt()
    value["review_evidence"]["independent"]["reviewer_identity"] = "VCP_REVIEWER"
    with pytest.raises(VeraPortAcceptanceError, match="one reviewer identity"):
        validate_review_evidence_binding(value)


def test_one_evidence_object_cannot_be_double_counted():
    value = receipt()
    value["review_evidence"]["independent"]["evidence_id"] = "github:review:123"
    with pytest.raises(VeraPortAcceptanceError, match="one evidence object"):
        validate_review_evidence_binding(value)


@pytest.mark.parametrize("fence", [0, -1, "", "1", True, None])
def test_fencing_token_must_be_positive_exact_integer(fence):
    value = receipt()
    value["lane_open"]["fencing_token"] = fence
    with pytest.raises(VeraPortAcceptanceError, match="positive exact integer"):
        validate_review_evidence_binding(value)


def test_review_class_cannot_be_swapped():
    value = receipt()
    value["review_evidence"]["independent"]["review_class"] = "VCP_SOURCE_REVIEW"
    with pytest.raises(VeraPortAcceptanceError, match="review class mismatch"):
        validate_review_evidence_binding(value)


def test_review_target_cannot_point_at_different_pr():
    value = receipt()
    value["review_evidence"]["vcp"]["pull_request"] = 11
    with pytest.raises(VeraPortAcceptanceError, match="target PR mismatch"):
        validate_review_evidence_binding(value)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("reviewer_identity", "bad reviewer", "invalid shape"),
        ("evidence_id", "PASS", "durable evidence shape"),
        ("evidence_id", "github:review:", "durable evidence shape"),
        ("evidence_id", "bus:not-a-sha", "durable evidence shape"),
    ],
)
def test_review_provenance_identifier_shapes_fail_closed(field, value, message):
    candidate = receipt()
    candidate["review_evidence"]["vcp"][field] = value
    with pytest.raises(VeraPortAcceptanceError, match=message):
        validate_review_evidence_binding(candidate)
