import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUT = ROOT / "evidence" / "qualification" / "SD1_WITNESS_QUALIFICATION_EVIDENCE_CUT_20260920.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_evidence_cut_preserves_partial_gate_state():
    cut = load(CUT)
    assert cut["schema"] == "SD1_WITNESS_QUALIFICATION_EVIDENCE_CUT_V1"
    assert cut["acceptance_subject"]["exact_head"] == (
        "a98309513e137b03989f12c30c97c17a78ae2b67"
    )
    assert cut["gate_summary"] == {"required": 5, "pass": 3, "not_executed": 2}
    assert cut["gates"]["independent_exact_head_source_review"]["result"] == "NOT_EXECUTED"
    assert cut["gates"]["disposable_postgres_semantics"]["result"] == "NOT_EXECUTED"
    assert cut["qualification_artifact"] == "UNBOUND"
    assert cut["production_witness"] == "NOT_CONSTRUCTIBLE"
    assert cut["causal_data_collection"] == "HOLD"
    assert cut["control_causality"] == "UNRESOLVED"


def test_pass_gate_digests_match_exact_evidence_files():
    cut = load(CUT)
    for gate_name, gate in cut["gates"].items():
        if gate["result"] != "PASS":
            continue
        path = ROOT / gate["path"]
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == gate["evidence_sha256"]
        evidence = load(path)
        assert evidence["schema"] == "SD1_WITNESS_QUALIFICATION_EVIDENCE_V1"
        assert evidence["gate"] == gate_name
        assert evidence["result"] == "PASS"


def test_evidence_cut_cannot_claim_qualification_completion():
    cut = load(CUT)
    assert cut["gate_summary"]["pass"] < cut["gate_summary"]["required"]
    assert "NOT_PROVIDER_MUTATION" in cut["non_effects"]
    assert "NOT_CAUSAL_DATA_COLLECTION" in cut["non_effects"]
    assert "NOT_CONTROL_CAUSALITY_PASS" in cut["non_effects"]
