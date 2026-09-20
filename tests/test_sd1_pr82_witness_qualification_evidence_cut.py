import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUT = (
    ROOT / "evidence" / "qualification"
    / "SD1_PR82_WITNESS_QUALIFICATION_EVIDENCE_CUT_20260920.json"
)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_cut_binds_exact_pr82_on_passed_pr73():
    cut = load(CUT)
    subject = cut["acceptance_subject"]
    assert subject["draft_pr"] == 82
    assert subject["exact_head"] == (
        "7b9877741df29b75cecdf99ba4d92c2fa09cecf8"
    )
    assert subject["parent_pr"] == 73
    assert subject["parent_head"] == (
        "7e894a72ca453a63a8e2f57d3162aa27962c3e06"
    )


def test_cut_remains_partial_and_fail_closed():
    cut = load(CUT)
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


def test_pass_gate_digests_match_exact_files():
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


def test_controller_replay_is_exact_pr82_subject():
    evidence = load(
        ROOT / "evidence" / "qualification"
        / "SD1_PR82_CONTROLLER_INTEGRATION_REPLAY_20260920.json"
    )
    assert evidence["subject"]["draft_pr"] == 82
    assert evidence["subject"]["exact_head"] == (
        "7b9877741df29b75cecdf99ba4d92c2fa09cecf8"
    )
    assert evidence["subject"]["parent_pr"] == 73


def test_superseded_pr72_pr75_are_not_current_evidence():
    cut = load(CUT)
    assert cut["superseded_predecessors"] == [
        {
            "pr": 72,
            "head": "d5e39d8fee4d6b37aedf11085b3aec66b9a33759",
            "disposition": "SUPERSEDED_WRONG_PROJECTION_LINEAGE",
        },
        {
            "pr": 75,
            "head": "05874fb243783602b5292738bb17510c4adf9e36",
            "disposition": "SUPERSEDED_EVIDENCE_FOR_WRONG_ACCEPTANCE_SUBJECT",
        },
    ]


def test_provider_evidence_preserves_non_effect_ceiling():
    for name in (
        "SD1_PR82_PRODUCTION_PERMISSION_READBACK_20260920.json",
        "SD1_PR82_PROVIDER_SOURCE_BINDING_READBACK_20260920.json",
    ):
        evidence = load(ROOT / "evidence" / "qualification" / name)
        assert "NOT_PROVIDER_MUTATION" in evidence["non_effects"]
        assert "NOT_CAUSAL_DATA_COLLECTION" in evidence["non_effects"]
        assert "NOT_MERGE_AUTHORITY" in evidence["non_effects"]
