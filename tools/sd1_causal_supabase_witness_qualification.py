"""Source-controlled pin for the independently reviewed provider qualification.

This module is intentionally excluded from the implementation-subject digest:
pinning an artifact must not change the witness bytes that artifact attests.
Changing this pin remains a separate source change and grants no provider or
causal-collection authority.
"""

QUALIFICATION_ARTIFACT_SHA256: str | None = None

__all__ = ["QUALIFICATION_ARTIFACT_SHA256"]
