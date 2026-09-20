import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUT = (
    ROOT / "evidence" / "qualification"
    / "SD1_WITNESS_QUALIFICATION_EVIDENCE_CUT_20260920.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_evidence_cut_binds_exact_restaked_acceptance_subject():
    cut = load(CUT)
    subject = cut["acceptance_subject"]
    assert subject["draft_pr"] == 72
    assert subject["exact_head"] == (
        "d5e39d8fee4d6b37aedf11085b3aec66b9a33759"
    )
    assert subject["parent_pr"] == 64
    assert subject["parent_head"] == (
        "c15c426d8578372474f677593387e7bf43b7e18c"
    )
    assert cut["historical_predecessor"] == {
        "pr": 65,
        "head": "4c63a5771ace947b4c02fd1376b87fb95e9035a0",
        "disposition":
            "HISTORICAL_FAILED_PARENT_LINEAGE_NOT_CURRENT_QUALIFICATION_EVIDENCE",
    }


def test_evidence_cut_preserves_partial_gate_state():
    cut = load(CUT)
    assert cut["schema"] == "SD1_WITNESS_QUALIFICATION_EVIDENCE_CUT_V1"
    assert cut["gate_summary"] == {
        "required": 5,
        "pass": 3,
        "not_executed": 2,
    }
    assert cut["gates"]["independent_exact_head_source_review"]["result"] == (
        "NOT_EXECUTED"
    )
    assert cut["gates"]["disposable_postgres_semantics"]["result"] == (
        "NOT_EXECUTED"
    )
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
        assert hashlib.sha256(path.read_bytes()).hexdigest() == (
            gate["evidence_sha256"]
        )
        evidence = load(path)
        assert evidence["schema"] == "SD1_WITNESS_QUALIFICATION_EVIDENCE_V1"
        assert evidence["gate"] == gate_name
        assert evidence["result"] == "PASS"


def test_controller_replay_evidence_is_exact_pr72_subject():
    evidence = load(
        ROOT / "evidence" / "qualification"
        / "SD1_CONTROLLER_INTEGRATION_REPLAY_20260920.json"
    )
    assert evidence["subject"]["draft_pr"] == 72
    assert evidence["subject"]["exact_head"] == (
        "d5e39d8fee4d6b37aedf11085b3aec66b9a33759"
    )
    assert evidence["subject"]["parent_head"] == (
        "c15c426d8578372474f677593387e7bf43b7e18c"
    )


def test_provider_readbacks_remain_non_effect_evidence():
    for name in (
        "SD1_PRODUCTION_PERMISSION_READBACK_20260920.json",
        "SD1_PROVIDER_SOURCE_BINDING_READBACK_20260920.json",
    ):
        evidence = load(ROOT / "evidence" / "qualification" / name)
        assert evidence["result"] == "PASS"
        assert "NOT_PROVIDER_MUTATION" in evidence["non_effects"]
        assert "NOT_CAUSAL_DATA_COLLECTION" in evidence["non_effects"]
        assert "NOT_MERGE_AUTHORITY" in evidence["non_effects"]


def test_evidence_cut_cannot_claim_qualification_completion():
    cut = load(CUT)
    assert cut["gate_summary"]["pass"] < cut["gate_summary"]["required"]
    assert "NOT_PROVIDER_MUTATION" in cut["non_effects"]
    assert "NOT_CAUSAL_DATA_COLLECTION" in cut["non_effects"]
    assert "NOT_CONTROL_CAUSALITY_PASS" in cut["non_effects"]
