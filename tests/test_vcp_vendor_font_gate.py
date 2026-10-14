"""Protect vendored font bytes while checking all other source whitespace."""
from __future__ import annotations

from types import SimpleNamespace
import pytest
from tools import validate_vcp_integrity as v


def test_vendor_assets_match_canonical_git_blobs():
    assert len(v.PINNED_VENDOR_SVG_BLOBS) == 3
    v.verify_vendor_font_blobs()


def test_tampered_vendor_asset_fails_closed(monkeypatch):
    monkeypatch.setattr(v.subprocess, "run",
                        lambda *a, **kw: SimpleNamespace(stdout="0" * 40))
    with pytest.raises(RuntimeError, match="pinned vendored font"):
        v.verify_vendor_font_blobs()


def test_git_whitespace_diff_excludes_only_pinned_vendor_svgs():
    command = v._whitespace_command("base...HEAD")
    assert command[:5] == ["git", "diff", "--check", "base...HEAD", "--"]
    excluded = [arg.removeprefix(":(exclude)") for arg in command[5:]]
    assert set(excluded) == set(v.PINNED_VENDOR_SVG_BLOBS)
    assert ":(exclude)tools/" not in command
    assert ":(exclude)tests/" not in command
