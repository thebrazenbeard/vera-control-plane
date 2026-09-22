from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import hashlib

import pytest

from scripts.validate_veraport_machine_acceptance_receipt import (
    IMPLEMENTATION_HEAD,
    ResolvedReviewEvidence,
    ReviewEvidencePending,
    VeraPortAcceptanceError,
    validate_review_evidence_binding,
)


VCP_ID = "github:review:123"
INDEPENDENT_ID = "bus:" + "a" * 40


def resolved_reviews() -> dict[str, ResolvedReviewEvidence]:
    return {
        VCP_ID: ResolvedReviewEvidence(
            evidence_id=VCP_ID,
            canonical_payload=b"github-review-123-immutable-payload",
            review_class="VCP_SOURCE_REVIEW",
            target_repository="thebrazenbeard/vera-mesh",
            pull_request=12,
            reviewed_head=IMPLEMENTATION_HEAD,
            reviewer_identity="VCP_REVIEWER",
            verdict="PASS",
        ),
        INDEPENDENT_ID: ResolvedReviewEvidence(
            evidence_id=INDEPENDENT_ID,
            canonical_payload=b"bus-review-immutable-payload",
            review_class="INDEPENDENT_SOURCE_REVIEW",
            target_repository="thebrazenbeard/vera-mesh",
            pull_request=12,
            reviewed_head=IMPLEMENTATION_HEAD,
            reviewer_identity="BT2_REVIEWER",
            verdict="PASS",
        ),
    }


def resolver(mapping=None):
    evidence = resolved_reviews() if mapping is None else mapping
    return lambda evidence_id: evidence.get(evidence_id)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def receipt() -> dict:
    evidence = resolved_reviews()
    return {
        "implementation_subject": {
            "repository": "thebrazenbeard/vera-mesh",
            "pull_request": 12,
            "exact_head": IMPLEMENTATION_HEAD,
        },
        "review_evidence": {
            "vcp": {
                "evidence_id": VCP_ID,
                "evidence_content_sha256": digest(evidence[VCP_ID].canonical_payload),
            },
            "independent": {
                "evidence_id": INDEPENDENT_ID,
                "evidence_content_sha256": digest(
                    evidence[INDEPENDENT_ID].canonical_payload
                ),
            },
        },
        "lane_open": {"fencing_token": 1},
    }


def test_valid_distinct_exact_head_review_evidence_passes_only_after_resolution():
    validate_review_evidence_binding(receipt(), resolver())


def test_missing_resolver_is_explicit_pending_not_pass():
    with pytest.raises(ReviewEvidencePending, match="without a resolver") as exc:
        validate_review_evidence_binding(receipt())
    assert exc.value.status == "PENDING_REVIEW_EVIDENCE"


def test_well_shaped_nonexistent_evidence_is_pending_not_pass():
    value = receipt()
    value["review_evidence"]["vcp"] = {
        "evidence_id": "github:review:999",
        "evidence_content_sha256": "0" * 64,
    }
    with pytest.raises(ReviewEvidencePending, match="unresolved or nonexistent"):
        validate_review_evidence_binding(value, resolver())


def test_offline_evidence_lookup_is_pending_not_pass():
    def offline(_evidence_id):
        raise ConnectionError("offline")

    with pytest.raises(ReviewEvidencePending, match="lookup is unavailable"):
        validate_review_evidence_binding(receipt(), offline)


def test_receipt_cannot_self_attest_reviewer_head_class_or_verdict():
    value = receipt()
    value["review_evidence"]["vcp"]["reviewer_identity"] = "FORGED_REVIEWER"
    value["review_evidence"]["vcp"]["verdict"] = "PASS"
    with pytest.raises(VeraPortAcceptanceError, match="must contain only"):
        validate_review_evidence_binding(value, resolver())


def test_plain_self_attested_pass_strings_cannot_replace_review_evidence():
    value = receipt()
    value.pop("review_evidence")
    value["implementation_subject"]["vcp_review"] = "PASS"
    value["implementation_subject"]["independent_review"] = "PASS"
    with pytest.raises(VeraPortAcceptanceError, match="implementation subject"):
        validate_review_evidence_binding(value, resolver())


def test_resolved_content_digest_must_match_receipt_reference():
    value = receipt()
    value["review_evidence"]["vcp"]["evidence_content_sha256"] = "0" * 64
    with pytest.raises(VeraPortAcceptanceError, match="content digest mismatch"):
        validate_review_evidence_binding(value, resolver())


def test_resolved_evidence_identity_must_match_lookup_reference():
    evidence = resolved_reviews()
    evidence[VCP_ID] = replace(
        evidence[VCP_ID],
        evidence_id="github:review:456",
    )
    with pytest.raises(VeraPortAcceptanceError, match="identity does not match"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


def test_stale_review_head_fails_closed_from_resolved_evidence():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = replace(
        evidence[INDEPENDENT_ID],
        reviewed_head="0" * 40,
    )
    with pytest.raises(VeraPortAcceptanceError, match="stale/different head"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


def test_one_authenticated_reviewer_cannot_satisfy_both_review_classes():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = replace(
        evidence[INDEPENDENT_ID],
        reviewer_identity="VCP_REVIEWER",
    )
    with pytest.raises(VeraPortAcceptanceError, match="one authenticated reviewer"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


def test_one_authenticated_payload_cannot_be_aliased_as_two_reviews():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = replace(
        evidence[INDEPENDENT_ID],
        canonical_payload=evidence[VCP_ID].canonical_payload,
    )
    value = receipt()
    value["review_evidence"]["independent"]["evidence_content_sha256"] = digest(
        evidence[VCP_ID].canonical_payload
    )
    with pytest.raises(VeraPortAcceptanceError, match="one authenticated evidence payload"):
        validate_review_evidence_binding(value, resolver(evidence))


@pytest.mark.parametrize("fence", [0, -1, "", "1", True, None])
def test_fencing_token_must_be_positive_exact_integer(fence):
    value = receipt()
    value["lane_open"]["fencing_token"] = fence
    with pytest.raises(VeraPortAcceptanceError, match="positive exact integer"):
        validate_review_evidence_binding(value, resolver())


def test_resolved_review_class_cannot_be_swapped():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = replace(
        evidence[INDEPENDENT_ID],
        review_class="VCP_SOURCE_REVIEW",
    )
    with pytest.raises(VeraPortAcceptanceError, match="review class mismatch"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


def test_resolved_review_target_cannot_point_at_different_pr():
    evidence = resolved_reviews()
    evidence[VCP_ID] = replace(evidence[VCP_ID], pull_request=11)
    with pytest.raises(VeraPortAcceptanceError, match="target PR mismatch"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


def test_resolved_nonpass_verdict_fails_closed():
    evidence = resolved_reviews()
    evidence[VCP_ID] = replace(evidence[VCP_ID], verdict="CHANGES_REQUIRED")
    with pytest.raises(VeraPortAcceptanceError, match="has not passed"):
        validate_review_evidence_binding(receipt(), resolver(evidence))


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("evidence_id", "PASS", "durable evidence shape"),
        ("evidence_id", "github:review:", "durable evidence shape"),
        ("evidence_id", "bus:not-a-sha", "durable evidence shape"),
        ("evidence_content_sha256", "PASS", "lowercase SHA-256"),
        ("evidence_content_sha256", "A" * 64, "lowercase SHA-256"),
    ],
)
def test_review_reference_shapes_fail_closed(field, value, message):
    candidate = receipt()
    candidate["review_evidence"]["vcp"][field] = value
    with pytest.raises(VeraPortAcceptanceError, match=message):
        validate_review_evidence_binding(candidate, resolver())
