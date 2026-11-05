"""Source-contract regressions for public GitHub Bus containment.

These tests constrain documentation semantics only; they do not qualify
native Project installation, authenticated private routing, or delivery.
"""

from pathlib import Path


CONTRACT = (
    Path(__file__).resolve().parents[1]
    / "project-instructions"
    / "native-v2"
    / "VERA_COORDINATION_V2.md"
)


def read_contract() -> str:
    return CONTRACT.read_text(encoding="utf-8")


def test_public_github_bus_is_not_a_private_mailbox():
    text = read_contract()
    assert "PUBLIC_COORDINATION_ONLY" in text
    assert "not a confidential mailbox" in text
    assert "history, issues, pull requests, comments" in text
    assert (
        "Use `thebrazenbeard/chat-communication-bus` "
        "for work-bearing non-PR coordination."
    ) not in text


def test_private_work_fails_closed_without_authenticated_routing():
    text = read_contract()
    assert "currently verified, authenticated, access-controlled private destination" in text
    assert "HOLD_PRIVATE_COORDINATION" in text
    assert "NO_PUBLIC_FALLBACK" in text
    assert "source pin is code provenance only" in text
    assert "private Bus is installed, reachable, or authorized" in text


def test_public_status_is_not_private_delivery_or_acknowledgement():
    text = read_contract()
    assert "do not claim that another worker received" in text.lower()
    assert "A public status post is not private delivery or acknowledgement." in text
