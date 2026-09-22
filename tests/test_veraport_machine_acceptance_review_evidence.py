from __future__ import annotations

from dataclasses import replace
import hashlib
import json

import pytest

from scripts.validate_veraport_machine_acceptance_receipt import (
    IMPLEMENTATION_HEAD,
    REVIEW_ADMISSION_SCHEMA,
    ResolvedReviewEvidence,
    ReviewEvidencePending,
    VeraPortAcceptanceError,
    validate_review_evidence_binding,
)


VCP_ID = "github:review:123"
INDEPENDENT_ID = "bus:" + "a" * 40


def admission_payload(
    *,
    evidence_id: str,
    review_class: str,
    reviewer_identity: str,
    reviewed_head: str = IMPLEMENTATION_HEAD,
    target_repository: str = "thebrazenbeard/vera-mesh",
    pull_request: int = 12,
    verdict: str = "PASS",
) -> bytes:
    value = {
        "schema": REVIEW_ADMISSION_SCHEMA,
        "evidence_id": evidence_id,
        "review_class": review_class,
        "target_repository": target_repository,
        "pull_request": pull_request,
        "reviewed_head": reviewed_head,
        "reviewer_identity": reviewer_identity,
        "verdict": verdict,
    }
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def resolved_reviews() -> dict[str, ResolvedReviewEvidence]:
    return {
        VCP_ID: ResolvedReviewEvidence(
            evidence_id=VCP_ID,
            canonical_payload=admission_payload(
                evidence_id=VCP_ID,
                review_class="VCP_SOURCE_REVIEW",
                reviewer_identity="VCP_REVIEWER",
            ),
        ),
        INDEPENDENT_ID: ResolvedReviewEvidence(
            evidence_id=INDEPENDENT_ID,
            canonical_payload=admission_payload(
                evidence_id=INDEPENDENT_ID,
                review_class="INDEPENDENT_SOURCE_REVIEW",
                reviewer_identity="BT2_REVIEWER",
            ),
        ),
    }


def rewrite_admission(
    evidence: ResolvedReviewEvidence,
    **updates,
) -> ResolvedReviewEvidence:
    value = json.loads(evidence.canonical_payload.decode("utf-8"))
    value.update(updates)
    return replace(
        evidence,
        canonical_payload=json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
    )


def resolver(mapping=None):
    evidence = resolved_reviews() if mapping is None else mapping
    return lambda evidence_id: evidence.get(evidence_id)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def receipt(evidence=None) -> dict:
    evidence = resolved_reviews() if evidence is None else evidence
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
    evidence = resolved_reviews()
    validate_review_evidence_binding(receipt(evidence), resolver(evidence))


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


def test_duplicate_evidence_reference_is_rejected_before_lookup():
    value = receipt()
    value["review_evidence"]["independent"] = dict(value["review_evidence"]["vcp"])
    with pytest.raises(VeraPortAcceptanceError, match="one evidence reference"):
        validate_review_evidence_binding(value, resolver())


def test_duplicate_evidence_digest_is_rejected_before_lookup():
    value = receipt()
    value["review_evidence"]["independent"]["evidence_content_sha256"] = (
        value["review_evidence"]["vcp"]["evidence_content_sha256"]
    )
    with pytest.raises(VeraPortAcceptanceError, match="one evidence content digest"):
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


def test_admission_identity_inside_digest_bound_payload_must_match_reference():
    evidence = resolved_reviews()
    evidence[VCP_ID] = rewrite_admission(
        evidence[VCP_ID],
        evidence_id="github:review:456",
    )
    with pytest.raises(VeraPortAcceptanceError, match="admission evidence identity"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_stale_review_head_fails_closed_from_digest_bound_admission():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = rewrite_admission(
        evidence[INDEPENDENT_ID],
        reviewed_head="0" * 40,
    )
    with pytest.raises(VeraPortAcceptanceError, match="stale/different head"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_one_authenticated_reviewer_cannot_satisfy_both_review_classes():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = rewrite_admission(
        evidence[INDEPENDENT_ID],
        reviewer_identity="VCP_REVIEWER",
    )
    with pytest.raises(VeraPortAcceptanceError, match="one authenticated reviewer"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


@pytest.mark.parametrize("fence", [0, -1, "", "1", True, None])
def test_fencing_token_must_be_positive_exact_integer(fence):
    evidence = resolved_reviews()
    value = receipt(evidence)
    value["lane_open"]["fencing_token"] = fence
    with pytest.raises(VeraPortAcceptanceError, match="positive exact integer"):
        validate_review_evidence_binding(value, resolver(evidence))


def test_resolved_review_class_cannot_be_swapped():
    evidence = resolved_reviews()
    evidence[INDEPENDENT_ID] = rewrite_admission(
        evidence[INDEPENDENT_ID],
        review_class="VCP_SOURCE_REVIEW",
    )
    with pytest.raises(VeraPortAcceptanceError, match="review class mismatch"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_resolved_review_target_cannot_point_at_different_pr():
    evidence = resolved_reviews()
    evidence[VCP_ID] = rewrite_admission(evidence[VCP_ID], pull_request=11)
    with pytest.raises(VeraPortAcceptanceError, match="target PR mismatch"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_resolved_nonpass_verdict_fails_closed():
    evidence = resolved_reviews()
    evidence[VCP_ID] = rewrite_admission(
        evidence[VCP_ID],
        verdict="CHANGES_REQUIRED",
    )
    with pytest.raises(VeraPortAcceptanceError, match="has not passed"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_resolved_admission_field_injection_fails_closed():
    evidence = resolved_reviews()
    value = json.loads(evidence[VCP_ID].canonical_payload.decode("utf-8"))
    value["authority"] = "DEPLOY"
    evidence[VCP_ID] = replace(
        evidence[VCP_ID],
        canonical_payload=json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8"),
    )
    with pytest.raises(VeraPortAcceptanceError, match="admission fields are not exact"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_boolean_pull_request_cannot_alias_integer_subject():
    evidence = resolved_reviews()
    evidence[VCP_ID] = rewrite_admission(evidence[VCP_ID], pull_request=True)
    with pytest.raises(VeraPortAcceptanceError, match="target PR mismatch"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


def test_duplicate_json_key_in_authenticated_admission_fails_closed():
    evidence = resolved_reviews()
    payload = evidence[VCP_ID].canonical_payload.decode("utf-8")
    payload = payload.replace(
        '"verdict":"PASS"',
        '"verdict":"PASS","verdict":"PASS"',
    )
    evidence[VCP_ID] = replace(
        evidence[VCP_ID],
        canonical_payload=payload.encode("utf-8"),
    )
    with pytest.raises(VeraPortAcceptanceError, match="duplicate key"):
        validate_review_evidence_binding(receipt(evidence), resolver(evidence))


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
