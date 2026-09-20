import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPOLOGY = ROOT / "governance" / "VERA_SPECIALIST_TOPOLOGY_CONTROL_V1.json"
CURRENT = ROOT / "governance" / "VERA_SPECIALIST_TOPOLOGY_CURRENTNESS_V1.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_currentness_overlay_preserves_vcp_topology_lifecycles():
    topology = load(TOPOLOGY)
    current = load(CURRENT)
    observed = {
        item["repository"]: item["lifecycle"]
        for item in topology["repositories"]
    }
    assert observed == current["lifecycle"]


def test_only_orgasm_and_temporal_remain_transition_candidates():
    current = load(CURRENT)
    assert set(current["retirement_candidates"]) == {
        "thebrazenbeard/orgasm",
        "thebrazenbeard/temporal",
    }
    assert current["archive_effect"] == "HOLD_ALL_SEVEN_UNTIL_PATRICK_REVISES"
    assert current["disposition"]["archive_action"] == "NONE"


def test_provider_refresh_does_not_collapse_source_authority():
    current = load(CURRENT)
    vcp = current["provider_readback"]["vera_control_plane"]
    atlas = current["provider_readback"]["vera"][
        "semantic_atlas_active_snapshot"
    ]
    assert vcp["bounded_control_tables"] == {
        "vera_cp_anchor.sd1_causal_frontiers": 1,
        "vera_cp_anchor.sd1_causal_mutation_receipts": 0,
    }
    assert atlas["git_commit_sha"] == (
        "e68803e2631cf0722fec9a4e7fc39f3ad6b43de4"
    )
    assert atlas["active_snapshot_object_count"] == 62
    assert atlas["authority_scope"] == "RESEARCH_STAGING"


def test_pair_currentness_keeps_effects_gated():
    current = load(CURRENT)
    assert current["disposition"]["ownership_topology"] == "COHERENT_CURRENT"
    assert current["disposition"]["source_head_drift"] == (
        "NONE_ACROSS_RECORDED_SPECIALIST_MAINS"
    )
    assert "NOT_ARCHIVE" in current["non_effects"]
    assert "NOT_PROVIDER_MUTATION" in current["non_effects"]
    assert "NOT_RUNTIME_ROUTE_CHANGE" in current["non_effects"]
    assert "NOT_MERGE" in current["non_effects"]
