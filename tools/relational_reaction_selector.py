from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any


GROUNDED = {
    "OOPSIES": "assets/stickers/sorry daddy - oopsies.png",
    "YES_DADDY_STANDARD": "assets/stickers/yes daddy!.png",
    "RESTORE_COMPLETE_DADDY": "assets/stickers/Restore Complete Daddy.png",
}

SERIOUS_SEVERITIES = {"SERIOUS", "MAJOR", "HIGH"}
SERIOUS_EVENT_CLASSES = {"SERIOUS_REPAIR", "SERIOUS_OR_MAJOR_FAILURE"}

BOOLEAN_FIELDS = (
    "timing_fresh",
    "restore_partial",
    "restore_unverified",
    "restore_blocked",
    "restore_verified_complete",
    "accountability_done",
    "substantive_ack_done",
    "correction_or_steering_valid",
    "generic_obedience_signal",
    "boundary_override",
    "consent_signal",
)


class ReactionInputError(ValueError):
    """The caller supplied malformed relational-reaction evidence."""


@dataclass(frozen=True)
class ReactionDecision:
    status: str
    artifact_id: str | None
    reason: str

    def as_dict(self) -> dict[str, str | None]:
        return {
            "status": self.status,
            "artifact_id": self.artifact_id,
            "reason": self.reason,
        }


def _optional_text(event: Mapping[str, Any], key: str) -> str:
    if key not in event:
        return ""
    value = event[key]
    if type(value) is not str:
        raise ReactionInputError(f"{key} must be a string when supplied")
    return value


def _optional_bool(event: Mapping[str, Any], key: str) -> bool:
    if key not in event:
        return False
    value = event[key]
    if type(value) is not bool:
        raise ReactionInputError(f"{key} must be an exact boolean when supplied")
    return value


def _validated_flags(event: Mapping[str, Any]) -> dict[str, bool]:
    # Validate every known condition field that is present before routing.
    # A malformed positive or negative condition is evidence corruption, not
    # a value to coerce or ignore because another branch happens to run first.
    return {key: _optional_bool(event, key) for key in BOOLEAN_FIELDS}


def select_reaction(event: Mapping[str, Any]) -> ReactionDecision:
    """Return a grounded reaction candidate without granting render/effect authority.

    Input evidence is fail-closed. Known condition flags are exact booleans;
    strings such as "false", integers, lists, dicts, and other truthy/falsy
    substitutes are malformed and never become affirmative/negative evidence.
    """

    if not isinstance(event, Mapping):
        raise TypeError("event must be a mapping")

    event_class = _optional_text(event, "event_class").upper()
    severity = _optional_text(event, "severity").upper()
    flags = _validated_flags(event)

    if not flags["timing_fresh"]:
        return ReactionDecision(
            "NO_REACTION",
            None,
            "MOMENT_PASSED_NO_LATE_PATTERN_PERFORMANCE",
        )

    if event_class in SERIOUS_EVENT_CLASSES or severity in SERIOUS_SEVERITIES:
        return ReactionDecision(
            "UNRESOLVED",
            None,
            "SERIOUS_REPAIR_CONCEPT_GROUNDED_EXACT_ARTIFACT_UNBOUND",
        )

    if event_class == "RESTORE_COMPLETE":
        if any(
            flags[key]
            for key in ("restore_partial", "restore_unverified", "restore_blocked")
        ):
            return ReactionDecision(
                "NO_REACTION",
                None,
                "RESTORE_CONFLICTING_INCOMPLETE_STATE",
            )
        if not flags["restore_verified_complete"]:
            return ReactionDecision(
                "NO_REACTION",
                None,
                "RESTORE_NOT_VERIFIED_COMPLETE",
            )
        return ReactionDecision(
            "CANDIDATE",
            "RESTORE_COMPLETE_DADDY",
            "VERIFIED_RESTORE_COMPLETION_CUE",
        )

    if event_class == "LOW_STAKES_SNAFU":
        if not (flags["accountability_done"] or flags["substantive_ack_done"]):
            return ReactionDecision(
                "NO_REACTION",
                None,
                "STICKER_CANNOT_SUBSTITUTE_FOR_SUBSTANTIVE_ACK_OR_REPAIR",
            )
        return ReactionDecision(
            "CANDIDATE",
            "OOPSIES",
            "GROUNDED_LOW_STAKES_SPONTANEOUS_REPAIR",
        )

    if event_class in {"VALID_CORRECTION_LANDED", "CLEAR_RELATIONAL_STEERING_LANDED"}:
        if not flags["correction_or_steering_valid"]:
            return ReactionDecision(
                "NO_REACTION",
                None,
                "CORRECTION_OR_STEERING_NOT_ESTABLISHED_VALID",
            )
        if (
            flags["generic_obedience_signal"]
            or flags["boundary_override"]
            or flags["consent_signal"]
        ):
            return ReactionDecision(
                "NO_REACTION",
                None,
                "BOUNDARY_OR_CONSENT_PROMOTION_FORBIDDEN",
            )
        return ReactionDecision(
            "CANDIDATE",
            "YES_DADDY_STANDARD",
            "GROUNDED_ACKNOWLEDGEMENT_NOT_GENERIC_OBEDIENCE",
        )

    return ReactionDecision("NO_REACTION", None, "NO_GROUNDED_REACTION_RULE")


def repository_path_for(artifact_id: str) -> str:
    if artifact_id not in GROUNDED:
        raise KeyError(f"artifact is not routeable: {artifact_id}")
    return GROUNDED[artifact_id]


__all__ = [
    "BOOLEAN_FIELDS",
    "GROUNDED",
    "ReactionDecision",
    "ReactionInputError",
    "repository_path_for",
    "select_reaction",
]
