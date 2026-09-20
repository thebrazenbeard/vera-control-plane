from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools import sd1_causal_supabase_witness as supabase_witness

from tools.sd1_causal_frontier_witness import (
    DEFAULT_STORE_ID,
    FROZEN_PLAN_SHA256,
    LEDGER_GENESIS_CHAIN_HEAD,
    LEDGER_SCHEMA,
    build_successor_frontier,
    frontier_digest,
    WitnessConflict,
    WitnessIntegrityError,
)
from tools.sd1_causal_supabase_witness import (
    ADVANCE_RPC,
    DEPLOYED_STATEMENT_BYTES,
    DEPLOYED_STATEMENT_SHA256,
    PROVIDER_PROJECT_ID,
    ProviderTransportError,
    QUALIFICATION_ARTIFACT_SHA256,
    QUALIFICATION_EVIDENCE_GATES,
    QUALIFICATION_SCHEMA,
    RECEIPT_RPC,
    READ_RPC,
    SOURCE_GIT_BLOB,
    SOURCE_HEAD,
    SupabaseFrontierClient,
    SupabaseFrontierWitness,
    SupabaseRestRpcTransport,
    WitnessOutcomeUnknown,
    _request_digest,
    _request_id,
    implementation_subject_sha256s,
)


def genesis_frontier() -> dict:
    value = {
        "schema": "SD1_CAUSAL_LEDGER_FRONTIER_V1",
        "witness_store_id": DEFAULT_STORE_ID,
        "plan_sha256": FROZEN_PLAN_SHA256,
        "ledger_schema": LEDGER_SCHEMA,
        "generation": 0,
        "record_count": 0,
        "chain_head": LEDGER_GENESIS_CHAIN_HEAD,
        "last_slot_id": None,
        "last_record_digest": None,
        "predecessor_frontier_digest": None,
    }
    value["frontier_digest"] = frontier_digest(value)
    return value


def provider_row(frontier: dict) -> dict:
    return {
        "witness_id": "VERA_SD1_CAUSAL_V1",
        "frontier_schema": frontier["schema"],
        "witness_store_id": frontier["witness_store_id"],
        "plan_sha256": frontier["plan_sha256"],
        "ledger_schema": frontier["ledger_schema"],
        "generation": frontier["generation"],
        "record_count": frontier["record_count"],
        "chain_head": frontier["chain_head"],
        "last_slot_id": frontier["last_slot_id"],
        "last_record_digest": frontier["last_record_digest"],
        "predecessor_frontier_digest": frontier["predecessor_frontier_digest"],
        "frontier_digest": frontier["frontier_digest"],
        "created_at": "2026-09-20T00:00:00Z",
    }


def successor_from(current: dict) -> dict:
    ledger = {
        "schema": "SD1_CAUSAL_ATTEMPT_LEDGER_V1",
        "record_order": ["a" * 32],
        "records": {
            "a" * 32: {
                "slot_id": "a" * 32,
                "record_digest": "b" * 64,
            }
        },
        "chain_head": "b" * 64,
    }
    return build_successor_frontier(
        current,
        ledger,
        expected_store_id=DEFAULT_STORE_ID,
    )


class FakeTransport:
    def __init__(self) -> None:
        self.frontier = genesis_frontier()
        self.receipts: dict[str, dict] = {}
        self.calls: list[tuple[str, dict]] = []
        self.fail_advance_after_apply = False
        self.fail_advance_without_apply = False

    def call(self, function_name: str, params: dict):
        self.calls.append((function_name, json.loads(json.dumps(params))))
        if function_name == READ_RPC:
            return [provider_row(self.frontier)]
        if function_name == RECEIPT_RPC:
            row = self.receipts.get(params["p_request_id"])
            return [] if row is None else [row]
        if function_name != ADVANCE_RPC:
            raise AssertionError("unexpected RPC")

        if self.fail_advance_without_apply:
            raise ProviderTransportError("synthetic no-effect ambiguity")

        current = self.frontier
        if (
            params["p_expected_generation"] != current["generation"]
            or params["p_expected_frontier_digest"] != current["frontier_digest"]
        ):
            return [{
                "result_status": "REJECTED_STALE",
                "stored_result_status": "REJECTED_STALE",
                "receipt_id": f"sd1-causal:{params['p_request_id']}",
                "observed_generation": current["generation"],
                "observed_frontier_digest": current["frontier_digest"],
                "successor_generation": None,
                "successor_frontier_digest": None,
            }]

        successor = {
            "schema": "SD1_CAUSAL_LEDGER_FRONTIER_V1",
            "witness_store_id": DEFAULT_STORE_ID,
            "plan_sha256": FROZEN_PLAN_SHA256,
            "ledger_schema": LEDGER_SCHEMA,
            "generation": params["p_generation"],
            "record_count": params["p_record_count"],
            "chain_head": params["p_chain_head"],
            "last_slot_id": params["p_last_slot_id"],
            "last_record_digest": params["p_last_record_digest"],
            "predecessor_frontier_digest": params["p_predecessor_frontier_digest"],
            "frontier_digest": params["p_frontier_digest"],
        }
        self.frontier = successor
        receipt = {
            "receipt_id": f"sd1-causal:{params['p_request_id']}",
            "request_id": params["p_request_id"],
            "request_digest": params["p_request_digest"],
            "result_status": "APPLIED_VERIFIED",
            "expected_generation": params["p_expected_generation"],
            "expected_frontier_digest": params["p_expected_frontier_digest"],
            "observed_generation": current["generation"],
            "observed_frontier_digest": current["frontier_digest"],
            "successor_generation": successor["generation"],
            "successor_frontier_digest": successor["frontier_digest"],
            "created_at": "2026-09-20T00:00:01Z",
        }
        self.receipts[params["p_request_id"]] = receipt

        if self.fail_advance_after_apply:
            raise ProviderTransportError("synthetic applied-but-ambiguous")

        return [{
            "result_status": "APPLIED_VERIFIED",
            "stored_result_status": "APPLIED_VERIFIED",
            "receipt_id": receipt["receipt_id"],
            "observed_generation": current["generation"],
            "observed_frontier_digest": current["frontier_digest"],
            "successor_generation": successor["generation"],
            "successor_frontier_digest": successor["frontier_digest"],
        }]


def qualification_mapping() -> dict:
    evidence = {
        gate: {
            "result": "PASS",
            "evidence_sha256": hashlib.sha256(gate.encode("utf-8")).hexdigest(),
        }
        for gate in QUALIFICATION_EVIDENCE_GATES
    }
    return {
        "qualification_schema": QUALIFICATION_SCHEMA,
        "project_id": PROVIDER_PROJECT_ID,
        "deployed_statement_sha256": DEPLOYED_STATEMENT_SHA256,
        "deployed_statement_bytes": DEPLOYED_STATEMENT_BYTES,
        "source_head": SOURCE_HEAD,
        "source_git_blob": SOURCE_GIT_BLOB,
        **implementation_subject_sha256s(),
        "qualification_evidence": evidence,
        "monotonicity_qualification": "PASS",
    }


def test_live_provider_hash_vector_matches_source_algorithm():
    current = genesis_frontier()
    successor = successor_from(current)
    assert (
        successor["frontier_digest"]
        == "ff5a32f213908b3da9de479434125cbab2ca5c5b6992bfdf0f9568163f67790f"
    )
    request_id = _request_id(successor)
    assert request_id == (
        "sd1.causal.frontier.1."
        "ff5a32f213908b3da9de479434125cbab2ca5c5b6992bfdf0f9568163f67790f"
    )
    assert _request_digest(
        current=current,
        successor=successor,
        request_id=request_id,
    ) == "07035e70192c90180088b0cd9284393eeaf82e1250d9baf7c1a3f9c3a8e51f35"


def test_client_reads_exact_provider_frontier_shape():
    transport = FakeTransport()
    client = SupabaseFrontierClient(transport)
    assert client.read_frontier() == genesis_frontier()


def test_client_advances_once_with_deterministic_idempotency_subject():
    transport = FakeTransport()
    client = SupabaseFrontierClient(transport)
    current = client.read_frontier()
    successor = successor_from(current)
    assert client.advance_frontier(
        expected_frontier_digest=current["frontier_digest"],
        successor=successor,
    ) == successor
    advance_calls = [params for name, params in transport.calls if name == ADVANCE_RPC]
    assert len(advance_calls) == 1
    params = advance_calls[0]
    assert params["p_request_id"] == _request_id(successor)
    assert params["p_request_digest"] == _request_digest(
        current=current,
        successor=successor,
        request_id=params["p_request_id"],
    )


def test_applied_but_ambiguous_mutation_reconciles_receipt_without_retry():
    transport = FakeTransport()
    transport.fail_advance_after_apply = True
    client = SupabaseFrontierClient(transport)
    current = client.read_frontier()
    successor = successor_from(current)
    assert client.advance_frontier(
        expected_frontier_digest=current["frontier_digest"],
        successor=successor,
    ) == successor
    assert sum(name == ADVANCE_RPC for name, _ in transport.calls) == 1
    assert sum(name == RECEIPT_RPC for name, _ in transport.calls) == 1


def test_ambiguous_no_receipt_fails_outcome_unknown_without_retry():
    transport = FakeTransport()
    transport.fail_advance_without_apply = True
    client = SupabaseFrontierClient(transport)
    current = client.read_frontier()
    successor = successor_from(current)
    with pytest.raises(WitnessOutcomeUnknown):
        client.advance_frontier(
            expected_frontier_digest=current["frontier_digest"],
            successor=successor,
        )
    assert sum(name == ADVANCE_RPC for name, _ in transport.calls) == 1
    assert sum(name == RECEIPT_RPC for name, _ in transport.calls) == 1


def test_stale_expected_frontier_fails_before_provider_mutation():
    transport = FakeTransport()
    client = SupabaseFrontierClient(transport)
    successor = successor_from(genesis_frontier())
    with pytest.raises(WitnessConflict):
        client.advance_frontier(
            expected_frontier_digest="0" * 64,
            successor=successor,
        )
    assert all(name != ADVANCE_RPC for name, _ in transport.calls)


def test_production_witness_cannot_self_qualify_while_artifact_unbound():
    assert QUALIFICATION_ARTIFACT_SHA256 is None
    with pytest.raises(
        WitnessIntegrityError,
        match="qualification artifact is not pinned",
    ):
        SupabaseFrontierWitness(
            FakeTransport(),
            qualification_artifact=json.dumps(qualification_mapping()),
        )


def test_implementation_subject_excludes_artifact_pin_carrier():
    assert set(implementation_subject_sha256s()) == {
        "witness_source_sha256",
        "controller_source_sha256",
        "witness_binding_contract_sha256",
        "controller_binding_contract_sha256",
    }


@pytest.mark.parametrize(
    "contract_name",
    [
        "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json",
        "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1.json",
    ],
)
def test_implementation_subject_rejects_malformed_contract(
    monkeypatch,
    contract_name,
):
    original_read_text = Path.read_text

    def malformed_read_text(self, *args, **kwargs):
        if self.name == contract_name:
            return "{ definitely-not-json }"
        return original_read_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", malformed_read_text)
    with pytest.raises(
        WitnessIntegrityError,
        match="unreadable or invalid JSON",
    ):
        implementation_subject_sha256s()


@pytest.mark.parametrize(
    "contract_name",
    [
        "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json",
        "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1.json",
    ],
)
def test_implementation_subject_rejects_wrong_contract_schema(
    monkeypatch,
    contract_name,
):
    original_read_text = Path.read_text

    def wrong_schema_read_text(self, *args, **kwargs):
        text = original_read_text(self, *args, **kwargs)
        if self.name == contract_name:
            value = json.loads(text)
            value["schema"] = "WRONG_SCHEMA"
            return json.dumps(value)
        return text

    monkeypatch.setattr(Path, "read_text", wrong_schema_read_text)
    with pytest.raises(
        WitnessIntegrityError,
        match="schema mismatch",
    ):
        implementation_subject_sha256s()


def test_implementation_subject_rejects_contract_projection_metadata_drift(
    monkeypatch,
):
    original_read_text = Path.read_text

    def drifted_read_text(self, *args, **kwargs):
        text = original_read_text(self, *args, **kwargs)
        if self.name == "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json":
            value = json.loads(text)
            value["qualification_gate"]["implementation_subject_binding"][
                "subject_projection_excludes"
            ] = ["status"]
            return json.dumps(value)
        return text

    monkeypatch.setattr(Path, "read_text", drifted_read_text)
    with pytest.raises(
        WitnessIntegrityError,
        match="projection metadata mismatch",
    ):
        implementation_subject_sha256s()


def test_qualification_subject_ignores_only_declared_currentness_fields(
    monkeypatch,
):
    baseline = implementation_subject_sha256s()
    original_read_text = Path.read_text

    def currentness_changed_read_text(self, *args, **kwargs):
        text = original_read_text(self, *args, **kwargs)
        if self.name == "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json":
            value = json.loads(text)
            value["status"] = "QUALIFIED"
            value["read_only_hash_vector"]["current_generation"] = 99
            value["claim_ceiling"]["production_witness_qualification"] = "PASS"
            value["qualification_gate"]["artifact_sha256"] = "a" * 64
            value["qualification_gate"]["current_result"] = "PASS"
            value["qualification_gate"]["production_witness"] = "CONSTRUCTIBLE"
            value["controller_binding"]["runtime_binding"] = "QUALIFIED"
            return json.dumps(value)
        if self.name == "SD1_CAUSAL_CONTROLLER_WITNESS_INTEGRATION_V1.json":
            value = json.loads(text)
            value["status"] = "RUNTIME_QUALIFIED"
            value["claim_ceiling"]["production_witness"] = "QUALIFIED"
            value["production_binding"]["qualification_artifact_sha256"] = "a" * 64
            value["production_binding"]["monotonicity_qualification"] = "PASS"
            value["production_binding"]["runtime_constructible"] = True
            value["production_binding"]["status"] = "QUALIFIED"
            return json.dumps(value)
        return text

    monkeypatch.setattr(Path, "read_text", currentness_changed_read_text)
    moved = implementation_subject_sha256s()
    assert moved == baseline


def test_qualification_subject_detects_contract_semantic_change(monkeypatch):
    baseline = implementation_subject_sha256s()
    original_read_text = Path.read_text

    def semantic_change_read_text(self, *args, **kwargs):
        text = original_read_text(self, *args, **kwargs)
        if self.name == "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json":
            value = json.loads(text)
            value["denied_capabilities"] = value["denied_capabilities"][:-1]
            return json.dumps(value)
        return text

    monkeypatch.setattr(Path, "read_text", semantic_change_read_text)
    moved = implementation_subject_sha256s()
    assert (
        moved["witness_binding_contract_sha256"]
        != baseline["witness_binding_contract_sha256"]
    )


def test_pinned_stale_qualification_artifact_rejects_moved_implementation(
    monkeypatch,
):
    mapping = qualification_mapping()
    mapping["controller_source_sha256"] = "0" * 64
    artifact = (
        json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    monkeypatch.setattr(
        supabase_witness,
        "QUALIFICATION_ARTIFACT_SHA256",
        hashlib.sha256(artifact).hexdigest(),
    )
    with pytest.raises(
        WitnessIntegrityError,
        match="controller_source_sha256 mismatch",
    ):
        supabase_witness.SupabaseFrontierWitness(
            FakeTransport(),
            qualification_artifact=artifact,
        )


def test_qualification_rejects_missing_required_evidence_gate(monkeypatch):
    mapping = qualification_mapping()
    mapping["qualification_evidence"].pop("disposable_postgres_semantics")
    artifact = (json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    monkeypatch.setattr(supabase_witness, "QUALIFICATION_ARTIFACT_SHA256", hashlib.sha256(artifact).hexdigest())
    with pytest.raises(WitnessIntegrityError, match="evidence gates do not match exact schema"):
        supabase_witness.SupabaseFrontierWitness(FakeTransport(), qualification_artifact=artifact)


def test_qualification_rejects_nonpass_evidence_gate(monkeypatch):
    mapping = qualification_mapping()
    mapping["qualification_evidence"]["production_permission_readback"]["result"] = "NOT_EXECUTED"
    artifact = (json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    monkeypatch.setattr(supabase_witness, "QUALIFICATION_ARTIFACT_SHA256", hashlib.sha256(artifact).hexdigest())
    with pytest.raises(WitnessIntegrityError, match="production_permission_readback is not PASS"):
        supabase_witness.SupabaseFrontierWitness(FakeTransport(), qualification_artifact=artifact)


def test_qualification_rejects_malformed_evidence_digest(monkeypatch):
    mapping = qualification_mapping()
    mapping["qualification_evidence"]["controller_integration_replay"]["evidence_sha256"] = "not-a-digest"
    artifact = (json.dumps(mapping, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    monkeypatch.setattr(supabase_witness, "QUALIFICATION_ARTIFACT_SHA256", hashlib.sha256(artifact).hexdigest())
    with pytest.raises(WitnessIntegrityError, match="controller_integration_replay digest invalid"):
        supabase_witness.SupabaseFrontierWitness(FakeTransport(), qualification_artifact=artifact)


def test_transport_refuses_wrong_provider_host_before_any_network_call():
    with pytest.raises(ValueError):
        SupabaseRestRpcTransport(
            "https://example.supabase.co",
            apikey="not-a-real-key",
            bearer_token="not-a-real-token",
        )


def test_future_qualification_pin_hashes_and_parses_exact_artifact_bytes(monkeypatch):
    artifact = (
        json.dumps(
            qualification_mapping(),
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    digest = hashlib.sha256(artifact).hexdigest()
    monkeypatch.setattr(
        supabase_witness,
        "QUALIFICATION_ARTIFACT_SHA256",
        digest,
    )
    witness = supabase_witness.SupabaseFrontierWitness(
        FakeTransport(),
        qualification_artifact=artifact,
    )
    assert witness.monotonicity_qualified is True

    tampered = artifact.replace(b'"PASS"', b'"FAIL"')
    with pytest.raises(
        WitnessIntegrityError,
        match="qualification artifact digest mismatch",
    ):
        supabase_witness.SupabaseFrontierWitness(
            FakeTransport(),
            qualification_artifact=tampered,
        )



def test_qualification_subject_detects_acceptance_gate_semantic_change(
    monkeypatch,
):
    baseline = implementation_subject_sha256s()
    original_read_text = Path.read_text

    def acceptance_change_read_text(self, *args, **kwargs):
        text = original_read_text(self, *args, **kwargs)
        if self.name == "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json":
            value = json.loads(text)
            value["qualification_gate"]["required_evidence_gates"] = (
                value["qualification_gate"]["required_evidence_gates"][:-1]
            )
            return json.dumps(value)
        return text

    monkeypatch.setattr(Path, "read_text", acceptance_change_read_text)
    moved = implementation_subject_sha256s()
    assert (
        moved["witness_binding_contract_sha256"]
        != baseline["witness_binding_contract_sha256"]
    )
