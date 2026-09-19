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


def test_witness_provider_binding_is_exact_genesis_subject():
    data = load_contract()
    binding = data["provider_binding"]
    assert binding["witness_store_id"] == "github:thebrazenbeard/vera-control-plane:state/sd1-causal-witness-v1"
    assert binding["provider"] == "GITHUB_PRIVATE_BRANCH"
    assert binding["repository"] == "thebrazenbeard/vera-control-plane"
    assert binding["branch"] == "state/sd1-causal-witness-v1"
    assert binding["genesis_commit"] == "cecf8d2ec6cf031c714e9f6c0972c4882101c16f"
    assert binding["genesis_frontier_git_blob"] == "5e6dcc7952ad1e6341a59bcd72c47613032dc326"
    assert binding["genesis_frontier_digest"] == "7de55cc22b28539c1d4e6934b1790d99c70ecee55ded80d7b698bec61ee249a1"
    assert binding["cas_subject"] == "NON_FORCE_BRANCH_HEAD_UPDATE_FROM_EXACT_OBSERVED_PARENT"
    assert binding["append_rule"] == "ONE_NEW_IMMUTABLE_FRONTIER_FILE_PER_GENERATION"
    assert binding["status"] == "GENESIS_BOUND_AND_READ_BACK_NO_CAUSAL_DATA"


def test_export_requires_fresh_witness_reconciliation():
    data = load_contract()
    text = " ".join(data["export_gate"]).lower()
    assert "fresh-read witness" in text
    assert "exact witness-to-ledger frontier equality" in text
    assert "reject export" in text
