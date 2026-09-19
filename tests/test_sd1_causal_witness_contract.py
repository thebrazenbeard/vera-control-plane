import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "SD1_CAUSAL_FRONTIER_WITNESS_V1.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_witness_contract_requires_independent_durable_cas():
    data = load_contract()
    storage = data["storage_requirements"]
    assert storage["independently_durable_from_ledger"] is True
    assert storage["compare_and_swap_required"] is True
    assert storage["fresh_readback_after_successful_cas"] is True
    assert storage["same_ledger_file_disallowed"] is True
    assert storage["sidecar_rewindable_with_ledger_disallowed"] is True
    assert storage["same_snapshot_domain_as_ledger_disallowed"] is True
    assert storage["non_force_monotonic_update_required"] is True


def test_witness_frontier_binds_monotonic_ledger_state():
    data = load_contract()
    frontier = data["frontier"]
    required = set(frontier["required_fields"])
    for field in {
        "witness_store_id",
        "plan_sha256",
        "generation",
        "record_count",
        "chain_head",
        "last_slot_id",
        "last_record_digest",
        "predecessor_frontier_digest",
        "frontier_digest",
    }:
        assert field in required
    assert "EXACTLY_PLUS_ONE" in frontier["generation_rule"]
    assert "LEDGER_RECORD_ORDER_LENGTH" in frontier["record_count_rule"]
    assert "LEDGER_CHAIN_HEAD" in frontier["chain_head_rule"]


def test_witness_contract_fails_closed_on_prefix_or_ambiguous_state():
    data = load_contract()
    rules = data["ambiguity_and_conflict_rules"]
    assert rules["witness_behind_ledger"].startswith("RECOVERY_REQUIRED")
    assert rules["witness_ahead_of_ledger"].startswith("RECOVERY_REQUIRED")
    assert "NO_REROLL" in rules["cas_conflict"]
    assert "RECONCILE_EXACT_OPERATION_TARGET" in rules["ambiguous_witness_mutation"]


def test_witness_provider_binding_blocks_collection_until_real_target_exists():
    data = load_contract()
    binding = data["provider_binding"]
    assert binding["witness_store_id"] == "UNBOUND"
    assert binding["provider"] == "UNBOUND"
    assert binding["target"] == "UNBOUND"
    assert binding["cas_subject"] == "UNBOUND"
    assert binding["status"] == "BLOCKS_CAUSAL_COLLECTION_UNTIL_BOUND_AND_READ_BACK"


def test_export_requires_fresh_witness_reconciliation():
    data = load_contract()
    text = " ".join(data["export_gate"]).lower()
    assert "fresh-read witness" in text
    assert "exact witness-to-ledger frontier equality" in text
    assert "reject export" in text
