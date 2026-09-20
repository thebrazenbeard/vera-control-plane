import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1.json"


def load_contract():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_controller_contract_requires_qualified_witness_everywhere():
    rules = load_contract()["controller_rules"]
    assert rules["witness_required_for_record_attempt"] is True
    assert rules["witness_required_for_blinded_export"] is True
    assert rules["witness_monotonicity_qualified_capability_required"] is True
    assert rules["ledger_witness_reconcile_before_write"] is True
    assert rules["ledger_witness_reconcile_before_export"] is True


def test_controller_contract_preserves_all_outcome_readback_binding():
    rules = load_contract()["controller_rules"]
    assert rules["exact_pre_run_readback_required_for_all_outcomes"] is True


def test_controller_contract_blocks_crash_reroll_paths():
    rules = load_contract()["controller_rules"]
    assert rules["candidate_ledger_written_to_pending_recovery_file_before_witness_cas"] is True
    assert rules["witness_cas_before_active_ledger_replace"] is True
    assert rules["witness_post_cas_readback_required"] is True
    assert rules["post_replace_ledger_witness_reconcile_required"] is True
    assert rules["orphan_pending_or_recovery_artifact_blocks_new_write"] is True
    assert rules["orphan_pending_or_recovery_artifact_blocks_export"] is True
    assert rules["exact_reviewed_witness_type_required"] is True
    assert rules["instance_method_shadowing_forbidden"] is True


def test_valid_prefix_rollback_fails_closed_but_unprotected_witness_is_not_accepted():
    attack = load_contract()["rollback_attack_rule"]
    assert "RECOVERY_REQUIRED" in attack["valid_prefix_ledger_rollback"]
    assert attack["unprotected_git_witness"] == "REJECT_AS_UNQUALIFIED"
    assert attack["synthetic_memory_witness"] == "TEST_ONLY"


def test_production_binding_has_source_path_but_still_blocks_real_collection():
    binding = load_contract()["production_binding"]
    ceiling = load_contract()["claim_ceiling"]
    assert (
        binding["implementation"]
        == "tools.sd1_causal_supabase_witness.SupabaseFrontierWitness"
    )
    assert (
        binding["client_implementation"]
        == "tools.sd1_causal_supabase_witness.SupabaseFrontierClient"
    )
    assert (
        binding["binding_contract"]
        == "protocol/SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json"
    )
    assert binding["provider_project_id"] == "fawkirqroyniueeqspif"
    assert binding["qualification_artifact_sha256"] is None
    assert binding["monotonicity_qualification"] == "NOT_EXECUTED"
    assert binding["runtime_constructible"] is False
    assert binding["exact_reviewed_implementation_required"] is True
    assert binding["git_transport_alone_allowed"] is False
    assert binding["status"].startswith("SOURCE_BOUND_BLOCKS_CAUSAL_COLLECTION")
    assert ceiling["production_witness"] == "SOURCE_IMPLEMENTATION_PRESENT_NOT_QUALIFIED"
    assert ceiling["provider_deployed_source"] == "EXACT_BYTES_VERIFIED"
    assert ceiling["controller_provider_path"] == "SOURCE_PRESENT_RUNTIME_BLOCKED"
    assert ceiling["causal_data_collection"] == "HOLD"
    assert ceiling["control_causality"] == "UNRESOLVED"
