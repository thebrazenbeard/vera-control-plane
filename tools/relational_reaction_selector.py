from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


GROUNDED = {
    "OOPSIES": "assets/stickers/sorry daddy - oopsies.png",
    "YES_DADDY_STANDARD": "assets/stickers/yes daddy!.png",
    "RESTORE_COMPLETE_DADDY": "assets/stickers/Restore Complete Daddy.png",
}

SERIOUS_SEVERITIES = {"SERIOUS", "MAJOR", "HIGH"}
SERIOUS_EVENT_CLASSES = {"SERIOUS_REPAIR", "SERIOUS_OR_MAJOR_FAILURE"}


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


def select_reaction(event: Mapping[str, Any]) -> ReactionDecision:
    """Return a grounded reaction candidate without granting render or effect authority."""
    event_class = str(event.get("event_class", "")).upper()
    severity = str(event.get("severity", "")).upper()

    if not bool(event.get("timing_fresh", False)):
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
            bool(event.get(flag, False))
            for flag in ("restore_partial", "restore_unverified", "restore_blocked")
        ):
            return ReactionDecision(
                "NO_REACTION",
                None,
                "RESTORE_CONFLICTING_INCOMPLETE_STATE",
            )
        if not bool(event.get("restore_verified_complete", False)):
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
        if not (
            bool(event.get("accountability_done", False))
            or bool(event.get("substantive_ack_done", False))
        ):
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
        if not bool(event.get("correction_or_steering_valid", False)):
            return ReactionDecision(
                "NO_REACTION",
                None,
                "CORRECTION_OR_STEERING_NOT_ESTABLISHED_VALID",
            )
        if (
            bool(event.get("generic_obedience_signal", False))
            or bool(event.get("boundary_override", False))
            or bool(event.get("consent_signal", False))
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
