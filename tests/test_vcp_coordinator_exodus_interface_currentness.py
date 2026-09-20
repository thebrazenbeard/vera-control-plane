import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTERFACE = ROOT / "governance" / "VERA_CONTROL_PLANE_COORDINATOR_INTERFACE_V1.json"
DOC = ROOT / "docs" / "VERA_CONTROL_PLANE_COORDINATOR_EXODUS_V1.md"

def load() -> dict:
    return json.loads(INTERFACE.read_text(encoding="utf-8"))

def test_exodus_topology_locator_is_exact_and_reconstructible():
    source = load()["durable_sources"]["exodus_topology_contract"]
    assert source == {
        "repository": "thebrazenbeard/chat-communication-bus",
        "branch": "architecture/chatgpt-exodus-interface-topology-v1-20260919",
        "head": "54f3fe558f69a44220f5ce43a33a09cbc6e39183",
        "path": "architecture/contracts/CHATGPT_EXODUS_INTERFACE_TOPOLOGY_V1.md",
        "git_blob": "71c4336b127e9a0bb9c3ccbd5cebeae4b585b031",
        "status": "SOURCE_DESIGN_EXACT_BINDING_NOT_BUS_MAIN",
    }

def test_interface_does_not_depend_on_dead_bus_main_locator():
    raw = INTERFACE.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    assert "architecture/contracts/EXODUS_INTERFACE_TOPOLOGY_V1.json" not in raw
    assert "not a JSON contract on Bus main" in doc

def test_coordinator_interface_preserves_authority_and_chat_independence():
    data = load()
    assert data["interface_not_identity"] is True
    assert data["worker_model"]["permanent_worker_chats_required"] is False
    assert data["worker_model"]["retired_chat_url_dependency_forbidden"] is True
    assert data["authority"]["inherits_no_protected_effect_authority_from_interface_role"] is True
    assert "project_settings" in data["authority"]["patrick_exact_authority_required_for"]
