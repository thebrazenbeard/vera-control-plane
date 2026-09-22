from __future__ import annotations

from typing import Any


IMPLEMENTATION_REPOSITORY = "thebrazenbeard/vera-mesh"
IMPLEMENTATION_PR = 12
IMPLEMENTATION_HEAD = "9bffc57930587bf74a12657bbeaa913474ab5574"
REVIEW_CLASSES = {
    "vcp": "VCP_SOURCE_REVIEW",
    "independent": "INDEPENDENT_SOURCE_REVIEW",
}


class VeraPortAcceptanceError(ValueError):
    pass


def _exact_nonempty_str(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise VeraPortAcceptanceError(f"{field} must be an exact non-empty string")
    return value


def validate_review_evidence_binding(receipt: dict[str, Any]) -> None:
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
        raise VeraPortAcceptanceError("implementation subject is not the exact current review subject")

    reviews = receipt.get("review_evidence")
    if type(reviews) is not dict or set(reviews) != set(REVIEW_CLASSES):
        raise VeraPortAcceptanceError("review_evidence must contain exactly vcp and independent")

    identities: list[str] = []
    evidence_ids: list[str] = []
    for slot, expected_class in REVIEW_CLASSES.items():
        review = reviews.get(slot)
        if type(review) is not dict:
            raise VeraPortAcceptanceError(f"{slot} review must be an exact object")
        required = {
            "review_class",
            "target_repository",
            "pull_request",
            "reviewed_head",
            "reviewer_identity",
            "evidence_id",
            "verdict",
        }
        if set(review) != required:
            raise VeraPortAcceptanceError(f"{slot} review fields are not exact")
        if review["review_class"] != expected_class:
            raise VeraPortAcceptanceError(f"{slot} review class mismatch")
        if review["target_repository"] != IMPLEMENTATION_REPOSITORY:
            raise VeraPortAcceptanceError(f"{slot} review target repository mismatch")
        if review["pull_request"] != IMPLEMENTATION_PR:
            raise VeraPortAcceptanceError(f"{slot} review target PR mismatch")
        if review["reviewed_head"] != subject["exact_head"]:
            raise VeraPortAcceptanceError(f"{slot} review is bound to a stale/different head")
        if review["verdict"] != "PASS":
            raise VeraPortAcceptanceError(f"{slot} review has not passed")
        identities.append(_exact_nonempty_str(review["reviewer_identity"], f"{slot}.reviewer_identity"))
        evidence_ids.append(_exact_nonempty_str(review["evidence_id"], f"{slot}.evidence_id"))

    if identities[0] == identities[1]:
        raise VeraPortAcceptanceError("one reviewer identity cannot satisfy both review classes")
    if evidence_ids[0] == evidence_ids[1]:
        raise VeraPortAcceptanceError("one evidence object cannot satisfy both review classes")

    lane_open = receipt.get("lane_open")
    if type(lane_open) is not dict:
        raise VeraPortAcceptanceError("lane_open must be an exact object")
    fence = lane_open.get("fencing_token")
    if type(fence) is not int or fence <= 0:
        raise VeraPortAcceptanceError("lane_open.fencing_token must be a positive exact integer")


__all__ = [
    "IMPLEMENTATION_HEAD",
    "VeraPortAcceptanceError",
    "validate_review_evidence_binding",
]
