from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_SUPABASE_CONTROL_PLANE_PROVIDER_BINDING_V1.json"


def test_moving_upstream_frontier_blocks_installable_currentness() -> None:
    binding = json.loads(BINDING.read_text(encoding="utf-8"))
    frontier = binding["upstream_source_frontier"]

    assert frontier["repository"] == "thebrazenbeard/vera"
    assert frontier["canonical_main_sha"] == "b7b8dcd1440a3b7147bec2cc35972f083e20f44a"
    assert frontier["predecessor_hardening_pr"] == 119
    assert frontier["observed_branch"] == "work/predecessor-import-readback-hardening-20260913"
    assert frontier["last_observed_head"] == "15bd36e30ef5a05a28b12572434837a0fe9b51c7"
    assert frontier["status"] == "MOVING_UNACCEPTED"
    assert frontier["binding_semantics"] == "OBSERVED_FRONTIER_ONLY_NOT_INSTALLABLE_CURRENTNESS_PIN"
    assert frontier["refresh_required"] is True
    assert frontier["deployment_copy_refresh"] == "BLOCKED_UNTIL_EXACT_HEAD_HOSTILE_POSTGRESQL_ACCEPTANCE"
    assert frontier["provider_install_authority"] == "NOT_GRANTED_BY_SOURCE_BINDING"

    assert binding["effect_status"]["runtime_plane_substrate_migration"] == "SOURCE_BOUND_NOT_APPLIED"
    assert binding["effect_status"]["predecessor_import_staging_migration"] == "SOURCE_BOUND_NOT_APPLIED"
