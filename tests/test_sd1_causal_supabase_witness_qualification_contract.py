import json
from pathlib import Path

from tools.sd1_causal_supabase_witness import QUALIFICATION_EVIDENCE_GATES

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = (
    ROOT / "protocol" / "SD1_CAUSAL_SUPABASE_WITNESS_QUALIFICATION_V1.json"
)
BINDING_PATH = (
    ROOT / "protocol" / "SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_acceptance_contract_matches_executable_gate_set():
    contract = load(CONTRACT_PATH)
    assert contract["schema"] == "SD1_SUPABASE_WITNESS_QUALIFICATION_CONTRACT_V1"
    assert contract["artifact_schema"] == "SD1_SUPABASE_WITNESS_QUALIFICATION_V1"
    assert tuple(contract["required_evidence_gates"]) == QUALIFICATION_EVIDENCE_GATES


def test_binding_points_to_exact_acceptance_contract_and_gate_set():
    gate = load(BINDING_PATH)["qualification_gate"]
    assert (
        gate["acceptance_contract"]
        == "protocol/SD1_CAUSAL_SUPABASE_WITNESS_QUALIFICATION_V1.json"
    )
    assert tuple(gate["required_evidence_gates"]) == QUALIFICATION_EVIDENCE_GATES
    assert gate["pass_semantics"] == (
        "ALL_REQUIRED_EVIDENCE_GATES_EXACT_PASS_WITH_DURABLE_EVIDENCE_DIGESTS"
    )


def test_acceptance_contract_preserves_state_separation():
    contract = load(CONTRACT_PATH)
    separation = contract["state_separation"]
    frontier = contract["current_frontier"]
    assert separation["production_witness_constructible"] == (
        "DOES_NOT_AUTHORIZE_FIRST_CAUSAL_MUTATION"
    )
    assert separation["causal_collection"] == "SEPARATE_PROTECTED_EFFECT"
    assert frontier["qualification_artifact"] == "UNBOUND"
    assert frontier["production_witness"] == "NOT_CONSTRUCTIBLE"
    assert frontier["causal_data_collection"] == "HOLD"
    assert frontier["control_causality"] == "UNRESOLVED"
