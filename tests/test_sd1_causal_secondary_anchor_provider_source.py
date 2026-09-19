import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (
    ROOT
    / "supabase"
    / "migrations"
    / "20260919195000_create_sd1_causal_secondary_anchor.sql"
)

EXPECTED_PROVIDER = "fawkirqroyniueeqspif"
EXPECTED_PLAN_SHA256 = (
    "526f35438c2521d40e7a2bfa145da363e0c5063d2affef27131f9370e08564ba"
)
EXPECTED_STORE_ID = (
    "github:thebrazenbeard/vera-control-plane:state/sd1-causal-witness-v1"
)
EXPECTED_GENESIS_CHAIN = (
    "527ddd4d35e85dfcff56b8c209ba2a6b642c08a18a9d2ae704626e8c78bfe229"
)
EXPECTED_GENESIS_FRONTIER = (
    "7de55cc22b28539c1d4e6934b1790d99c70ecee55ded80d7b698bec61ee249a1"
)


def source() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def canonical_frontier_digest(frontier: dict) -> str:
    payload = {key: value for key, value in frontier.items() if key != "frontier_digest"}
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def test_genesis_constants_match_frozen_frontier_algorithm():
    frontier = {
        "schema": "SD1_CAUSAL_LEDGER_FRONTIER_V1",
        "witness_store_id": EXPECTED_STORE_ID,
        "plan_sha256": EXPECTED_PLAN_SHA256,
        "ledger_schema": "SD1_CAUSAL_ATTEMPT_LEDGER_V1",
        "generation": 0,
        "record_count": 0,
        "chain_head": EXPECTED_GENESIS_CHAIN,
        "last_slot_id": None,
        "last_record_digest": None,
        "predecessor_frontier_digest": None,
        "frontier_digest": EXPECTED_GENESIS_FRONTIER,
    }
    assert canonical_frontier_digest(frontier) == EXPECTED_GENESIS_FRONTIER


def test_migration_is_exact_provider_bound_and_source_only():
    text = source()
    assert EXPECTED_PROVIDER in text
    assert "SOURCE ONLY" in text
    assert "PROVIDER != CONTROL AUTHORITY" in text
    assert "CREATE SCHEMA vera_cp_anchor AUTHORIZATION postgres;" in text


def test_broker_has_only_bounded_rpc_surface():
    text = source()
    assert "CREATE ROLE vera_sd1_causal_anchor_broker" in text
    assert "NOLOGIN" in text
    assert "NOBYPASSRLS" in text
    assert "sd1_causal_frontier_read_v1" in text
    assert "sd1_causal_receipt_read_v1" in text
    assert "sd1_causal_frontier_advance_v1" in text
    assert "REVOKE ALL ON TABLE vera_cp_anchor.sd1_causal_frontiers" in text
    assert "REVOKE ALL ON TABLE vera_cp_anchor.sd1_causal_mutation_receipts" in text
    assert "FROM vera_sd1_causal_anchor_broker" in text
    assert "GRANT INSERT" not in text
    assert "GRANT UPDATE" not in text
    assert "GRANT DELETE" not in text


def test_advance_rpc_is_serialized_exact_cas_and_idempotent():
    text = source()
    assert "pg_advisory_xact_lock" in text
    assert "p_generation <> p_expected_generation + 1" in text
    assert "p_predecessor_frontier_digest <> p_expected_frontier_digest" in text
    assert "'REJECTED_STALE'::text" in text
    assert "'IDEMPOTENT_REPLAY'::text" in text
    assert "'REQUEST_ID_COLLISION'::text" in text
    assert "'APPLIED_VERIFIED'::text" in text
    assert "canonical request digest mismatch" in text
    assert "successor frontier digest mismatch" in text


def test_anchor_tables_are_append_only_and_receipt_is_atomic_with_successor():
    text = source()
    assert "BEFORE UPDATE OR DELETE ON vera_cp_anchor.sd1_causal_frontiers" in text
    assert "BEFORE UPDATE OR DELETE ON vera_cp_anchor.sd1_causal_mutation_receipts" in text

    frontier_insert = text.index("INSERT INTO vera_cp_anchor.sd1_causal_frontiers (", text.index("CREATE FUNCTION vera_cp_api.sd1_causal_frontier_advance_v1"))
    receipt_insert = text.index("INSERT INTO vera_cp_anchor.sd1_causal_mutation_receipts (", frontier_insert)
    assert frontier_insert < receipt_insert


def test_public_client_roles_receive_no_anchor_capability():
    text = source()
    assert "FROM PUBLIC, anon, authenticated, service_role" in text
    assert "GRANT USAGE ON SCHEMA vera_cp_api\n  TO vera_sd1_causal_anchor_broker;" in text
    assert "GRANT EXECUTE ON FUNCTION vera_cp_api.sd1_causal_frontier_read_v1()" in text
    assert "GRANT EXECUTE ON FUNCTION vera_cp_api.sd1_causal_receipt_read_v1(text)" in text


def test_sql_frontier_canonicalization_uses_same_sorted_key_order_as_python():
    text = source()
    ordered_fragments = [
        '{"chain_head":',
        ',"generation":',
        ',"last_record_digest":',
        ',"last_slot_id":',
        ',"ledger_schema":',
        ',"plan_sha256":',
        ',"predecessor_frontier_digest":',
        ',"record_count":',
        ',"schema":',
        ',"witness_store_id":',
    ]
    start = text.index("CREATE FUNCTION vera_cp_anchor.sd1_causal_frontier_digest_v1")
    end = text.index("$fn$;", start)
    helper = text[start:end]
    positions = [helper.index(fragment) for fragment in ordered_fragments]
    assert positions == sorted(positions)


def test_migration_fails_if_genesis_or_direct_write_ceiling_is_wrong():
    text = source()
    assert "SD1 causal genesis exact readback failed" in text
    assert "SD1 causal broker unexpectedly has direct table write privilege" in text
    assert "has_table_privilege(" in text
