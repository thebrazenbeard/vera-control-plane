from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_exodus_lane_contract_is_chat_independent():
    text = (ROOT / "docs" / "EXODUS_RUNTIME_LANE_RECONSTRUCTION_V1.md").read_text(encoding="utf-8")
    assert "TEMPORARY_EXECUTION_LANE" in text
    assert "TEMPORARY_HOSTILE_REVIEW_LANE" in text
    assert "bus/bv-v2" in text
    assert "bus/vw-v1" in text
    assert "NOT A SEPARATE IDENTITY" in text
    assert "Project Runner conversation is not required" in text
    assert "Vera Control Plane Coordinator" in text
    assert "BT2 Coordinator" in text
    assert "WORKER_RECONSTRUCTION_GAP" in text
    assert "chatgpt.com/" not in text.lower()


def test_lane_contract_does_not_self_authorize_protected_effects():
    text = (ROOT / "docs" / "EXODUS_RUNTIME_LANE_RECONSTRUCTION_V1.md").read_text(encoding="utf-8")
    assert "no standing protected-effect authority" in text
    assert "This contract grants no merge" in text


def test_permanent_role_training_is_terminal_agnostic():
    role_files = [
        ROOT / "training" / "roles" / "four" / "v1.0.0" / "BOOTSTRAP.md",
        ROOT / "training" / "roles" / "four" / "v1.0.0" / "06-checkpoint-reorientation.md",
        ROOT / "training" / "roles" / "four" / "v1.0.0" / "manifest.yaml",
        ROOT / "training" / "roles" / "five" / "v1.0.0" / "BOOTSTRAP.md",
        ROOT / "training" / "roles" / "five" / "v1.0.0" / "README.md",
        ROOT / "training" / "roles" / "five" / "v1.0.0" / "references" / "AUTHORITY_EVIDENCE_MODEL.md",
    ]
    for path in role_files:
        text = path.read_text(encoding="utf-8").lower()
        assert "fresh chat" not in text, path
        assert "runtime terminal" in text, path
