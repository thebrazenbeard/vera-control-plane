from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Any, Callable


IMPLEMENTATION_REPOSITORY = "thebrazenbeard/vera-mesh"
IMPLEMENTATION_PR = 12
IMPLEMENTATION_HEAD = "9bffc57930587bf74a12657bbeaa913474ab5574"
REVIEW_CLASSES = {
    "vcp": "VCP_SOURCE_REVIEW",
    "independent": "INDEPENDENT_SOURCE_REVIEW",
}


class VeraPortAcceptanceError(ValueError):
    pass


class ReviewEvidencePending(VeraPortAcceptanceError):
    status = "PENDING_REVIEW_EVIDENCE"


@dataclass(frozen=True)
class ResolvedReviewEvidence:
    evidence_id: str
    canonical_payload: bytes
    review_class: str
    target_repository: str
    pull_request: int
    reviewed_head: str
    reviewer_identity: str
    verdict: str


ReviewEvidenceResolver = Callable[[str], ResolvedReviewEvidence | None]


_REVIEWER_RE = re.compile(r"^[A-Za-z0-9._:/@-]+$")
_EVIDENCE_RE = re.compile(
    r"^(?:github:(?:review|comment):[A-Za-z0-9._:/@-]+|bus:[0-9a-f]{40})$"
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _exact_nonempty_str(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise VeraPortAcceptanceError(f"{field} must be an exact non-empty string")
    return value


def _reviewer_identity(value: Any, field: str) -> str:
    value = _exact_nonempty_str(value, field)
    if _REVIEWER_RE.fullmatch(value) is None:
        raise VeraPortAcceptanceError(f"{field} has invalid shape")
    return value


def _evidence_id(value: Any, field: str) -> str:
    value = _exact_nonempty_str(value, field)
    if _EVIDENCE_RE.fullmatch(value) is None:
        raise VeraPortAcceptanceError(f"{field} has invalid durable evidence shape")
    return value


def _sha256(value: Any, field: str) -> str:
    value = _exact_nonempty_str(value, field)
    if _SHA256_RE.fullmatch(value) is None:
        raise VeraPortAcceptanceError(f"{field} must be lowercase SHA-256 hex")
    return value


def _resolve_review(
    *,
    slot: str,
    expected_class: str,
    reference: dict[str, Any],
    subject: dict[str, Any],
    resolver: ReviewEvidenceResolver | None,
) -> ResolvedReviewEvidence:
    if type(reference) is not dict or set(reference) != {
        "evidence_id",
        "evidence_content_sha256",
    }:
        raise VeraPortAcceptanceError(
            f"{slot} review reference must contain only evidence_id and evidence_content_sha256"
        )

    evidence_id = _evidence_id(reference["evidence_id"], f"{slot}.evidence_id")
    expected_digest = _sha256(
        reference["evidence_content_sha256"],
        f"{slot}.evidence_content_sha256",
    )

    if resolver is None:
        raise ReviewEvidencePending(
            f"{slot} review evidence cannot be authenticated without a resolver"
        )

    try:
        resolved = resolver(evidence_id)
    except (LookupError, OSError, TimeoutError, ConnectionError) as exc:
        raise ReviewEvidencePending(
            f"{slot} review evidence lookup is unavailable"
        ) from exc

    if resolved is None:
        raise ReviewEvidencePending(
            f"{slot} review evidence is unresolved or nonexistent"
        )
    if type(resolved) is not ResolvedReviewEvidence:
        raise VeraPortAcceptanceError(
            f"{slot} resolver returned an invalid evidence object"
        )
    if resolved.evidence_id != evidence_id:
        raise VeraPortAcceptanceError(
            f"{slot} resolved evidence identity does not match the receipt reference"
        )
    if type(resolved.canonical_payload) is not bytes:
        raise VeraPortAcceptanceError(
            f"{slot} resolved evidence canonical_payload must be exact bytes"
        )

    actual_digest = hashlib.sha256(resolved.canonical_payload).hexdigest()
    if actual_digest != expected_digest:
        raise VeraPortAcceptanceError(
            f"{slot} resolved evidence content digest mismatch"
        )
    if resolved.review_class != expected_class:
        raise VeraPortAcceptanceError(f"{slot} resolved review class mismatch")
    if resolved.target_repository != IMPLEMENTATION_REPOSITORY:
        raise VeraPortAcceptanceError(
            f"{slot} resolved review target repository mismatch"
        )
    if resolved.pull_request != IMPLEMENTATION_PR:
        raise VeraPortAcceptanceError(f"{slot} resolved review target PR mismatch")
    if resolved.reviewed_head != subject["exact_head"]:
        raise VeraPortAcceptanceError(
            f"{slot} resolved review is bound to a stale/different head"
        )
    if resolved.verdict != "PASS":
        raise VeraPortAcceptanceError(
            f"{slot} resolved review has not passed"
        )
    _reviewer_identity(
        resolved.reviewer_identity,
        f"{slot}.resolved_reviewer_identity",
    )
    return resolved


def validate_review_evidence_binding(
    receipt: dict[str, Any],
    evidence_resolver: ReviewEvidenceResolver | None = None,
) -> None:
    if type(receipt) is not dict:
        raise VeraPortAcceptanceError("receipt must be an exact object")

    subject = receipt.get("implementation_subject")
    if type(subject) is not dict:
        raise VeraPortAcceptanceError("implementation_subject must be an exact object")
    if subject != {
        "repository": IMPLEMENTATION_REPOSITORY,
        "pull_request": IMPLEMENTATION_PR,
        "exact_head": IMPLEMENTATION_HEAD,
    }:
        raise VeraPortAcceptanceError(
            "implementation subject is not the exact current review subject"
        )

    reviews = receipt.get("review_evidence")
    if type(reviews) is not dict or set(reviews) != set(REVIEW_CLASSES):
        raise VeraPortAcceptanceError(
            "review_evidence must contain exactly vcp and independent"
        )

    resolved_reviews = []
    for slot, expected_class in REVIEW_CLASSES.items():
        resolved_reviews.append(
            _resolve_review(
                slot=slot,
                expected_class=expected_class,
                reference=reviews[slot],
                subject=subject,
                resolver=evidence_resolver,
            )
        )

    identities = [review.reviewer_identity for review in resolved_reviews]
    evidence_ids = [review.evidence_id for review in resolved_reviews]
    evidence_digests = [
        hashlib.sha256(review.canonical_payload).hexdigest()
        for review in resolved_reviews
    ]
    if identities[0] == identities[1]:
        raise VeraPortAcceptanceError(
            "one authenticated reviewer identity cannot satisfy both review classes"
        )
    if evidence_ids[0] == evidence_ids[1]:
        raise VeraPortAcceptanceError(
            "one authenticated evidence object cannot satisfy both review classes"
        )
    if evidence_digests[0] == evidence_digests[1]:
        raise VeraPortAcceptanceError(
            "one authenticated evidence payload cannot satisfy both review classes"
        )

    lane_open = receipt.get("lane_open")
    if type(lane_open) is not dict:
        raise VeraPortAcceptanceError("lane_open must be an exact object")
    fence = lane_open.get("fencing_token")
    if type(fence) is not int or fence <= 0:
        raise VeraPortAcceptanceError(
            "lane_open.fencing_token must be a positive exact integer"
        )


__all__ = [
    "IMPLEMENTATION_HEAD",
    "ResolvedReviewEvidence",
    "ReviewEvidencePending",
    "ReviewEvidenceResolver",
    "VeraPortAcceptanceError",
    "validate_review_evidence_binding",
]
