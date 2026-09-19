import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "SD1_CAUSAL_SECONDARY_ANCHOR_V1.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_secondary_anchor_is_provider_cas_not_generic_mutation():
    data = load_contract()
    operation = data["provider_operation"]
    assert operation["operation_id"] == "sd1.causal.frontier.advance.v1"
    assert operation["retry_class"] == "RECONCILE_BEFORE_RETRY"
    assert operation["protected_effect_class"] == "PRODUCTION_MUTATION"
    assert operation["generic_sql_proxy"] is False
    assert operation["direct_table_mutation_by_broker"] is False


def test_secondary_anchor_is_append_only_and_frontier_chained():
    data = load_contract()
    row = data["frontier_row"]
    assert row["append_only"] is True
    assert row["identity_key"] == ["witness_id", "generation"]
    assert "EXACTLY_PLUS_ONE" in row["generation_rule"]
    assert row["record_count_rule"] == "MUST_EQUAL_GENERATION"
    assert "PREDECESSOR_DIGEST" in row["predecessor_rule"]
    assert "CANONICAL_FRONTIER_DIGEST" in row["frontier_digest_rule"]


def test_secondary_anchor_transaction_is_exact_cas_and_insert_only():
    tx = load_contract()["transaction_contract"]
    assert tx["read_latest_frontier_inside_transaction"] is True
    assert tx["require_expected_generation"] is True
    assert tx["require_expected_frontier_digest"] is True
    assert tx["require_successor_generation_plus_one"] is True
    assert tx["require_successor_predecessor_digest"] is True
    assert tx["insert_successor_only"] is True
    assert tx["no_update"] is True
    assert tx["no_delete"] is True
    assert tx["post_commit_exact_readback_required"] is True
    assert tx["stale_result"] == "REJECTED_STALE"
    assert tx["divergent_result"] == "CONFLICT"
    assert "RECONCILE_BEFORE_RETRY" in tx["ambiguous_result"]


def test_secondary_anchor_idempotency_forbids_changed_retry():
    idem = load_contract()["idempotency"]
    assert idem["request_id_unique"] is True
    assert idem["canonical_request_digest_required"] is True
    assert idem["same_request_same_digest"] == "IDEMPOTENT_REPLAY"
    assert idem["same_request_different_digest"] == "REQUEST_ID_COLLISION"
    assert idem["changed_successor_after_ambiguity_forbidden"] is True


def test_broker_credentials_cannot_rewind_anchor_directly():
    perms = load_contract()["provider_permissions"]
    assert perms["broker_role_direct_insert"] is False
    assert perms["broker_role_update"] is False
    assert perms["broker_role_delete"] is False
    assert perms["anon_access"] is False
    assert perms["authenticated_access"] is False


def test_source_contract_does_not_promote_provider_or_causality():
    ceiling = load_contract()["claim_ceiling"]
    assert ceiling["source_contract"] == "PRESENT"
    assert ceiling["provider_schema"] == "NOT_INSTALLED"
    assert ceiling["provider_operation"] == "NOT_ACTIVE"
    assert ceiling["monotonicity"] == "NOT_ESTABLISHED"
    assert ceiling["causal_collection"] == "HOLD"
    assert ceiling["control_causality"] == "UNRESOLVED"


def test_activation_requires_exact_authority_deploy_and_readback():
    gate = " ".join(load_contract()["activation_gate"]).lower()
    assert "patrick exact production-mutation authority" in gate
    assert "grants and direct-table denial read back" in gate
    assert "genesis row exact digest read back" in gate
    assert "hostile stale-cas idempotency rollback and ambiguity tests pass" in gate
