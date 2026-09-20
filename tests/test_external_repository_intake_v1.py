import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_EXTERNAL_REPOSITORY_INTAKE_V1.json"
DOC = ROOT / "docs" / "research" / "EXTERNAL_REPOSITORY_INTAKE_20260920_V1.md"

def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))

def test_all_external_sources_are_exact_head_bound():
    data = load()
    assert len(data["repositories"]) == 8
    for item in data["repositories"]:
        assert len(item["head"]) == 40
        int(item["head"], 16)
        assert item["disposition"]
        assert item["non_effect"]

def test_discovery_cannot_promote_external_source():
    data = load()
    rules = data["rules"]
    assert rules["discovery_not_admission"] is True
    assert rules["external_content_not_autobiographical_memory"] is True
    assert rules["external_content_not_control_source"] is True
    assert rules["external_source_not_install_or_runtime_evidence"] is True
    assert "NOT_MEMORY_ADMISSION" in data["non_effects"]
    assert "NOT_CONTROL_OWNER" in data["non_effects"]

def test_stale_or_license_unresolved_sources_fail_closed():
    data = load()
    by_repo = {x["repository"]: x for x in data["repositories"]}
    chn = by_repo["fivesheep/chnroutes"]
    assert chn["license"] is None
    assert chn["disposition"] == "HISTORICAL_TECHNIQUE_ONLY_NO_CODE_REUSE"
    marp = by_repo["yhatt/marp"]
    assert marp["lifecycle"] == "ARCHIVED"
    assert marp["disposition"] == "HISTORICAL_ONLY_SUCCESSOR_REQUIRED"

def test_network_research_routes_out_of_vcp_implementation():
    data = load()
    by_repo = {x["repository"]: x for x in data["repositories"]}
    assert by_repo["encodeous/nylon"]["destination"].startswith("VeraMesh")
    assert by_repo["CluvexStudio/Aether"]["destination"].startswith("VeraMesh")
    assert "NO_VCP_ROUTING_IMPLEMENTATION_BY_DISCOVERY_ALONE" == by_repo["encodeous/nylon"]["non_effect"]
    assert "NO_VCP_NETWORK_STACK" in by_repo["CluvexStudio/Aether"]["non_effect"]

def test_political_content_is_not_admitted_as_vera_position():
    data = load()
    by_repo = {x["repository"]: x for x in data["repositories"]}
    item = by_repo["cirosantilli/china-dictatorship"]
    assert item["disposition"] == "CONTENT_CORPUS_ONLY"
    assert item["destination"] == "none by default"
    assert "NO_IDENTITY_MEMORY_CONTROL_OR_POLITICAL_POSITION_INGESTION" == item["non_effect"]
    assert "NOT_POLITICAL_POSITION" in data["non_effects"]

def test_document_preserves_state_separation():
    text = DOC.read_text(encoding="utf-8")
    assert "EXTERNAL_DISCOVERY != ADMISSION" in text
    assert "VeraMesh" in text
    assert "adopts none of its political claims" in text
