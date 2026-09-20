import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "governance" / "VERA_EXTERNAL_REPOSITORY_INTAKE_V2.json"
DOC = ROOT / "docs" / "research" / "EXTERNAL_REPOSITORY_INTAKE_20260920_V2.md"


def load():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def test_v2_is_additive_successor_not_v1_rewrite():
    data = load()
    assert data["predecessor"]["pr"] == 81
    assert data["predecessor"]["head"] == "d65685dbc424aed0fa959bed7c7226e9be4a5453"
    assert "does not rewrite" in data["predecessor"]["semantics"]


def test_all_new_sources_are_exact_head_bound():
    data = load()
    assert len(data["repositories"]) == 10
    for item in data["repositories"]:
        assert len(item["head"]) == 40
        int(item["head"], 16)
        assert item["disposition"]
        assert item["non_effect"]
        assert item["evidence"]


def test_hermes_and_openhands_do_not_transfer_identity_or_runtime():
    by_repo = {x["repository"]: x for x in load()["repositories"]}
    assert by_repo["NousResearch/hermes-agent"]["license"] == "MIT"
    assert "NO_HERMES_MEMORY_IDENTITY" in by_repo["NousResearch/hermes-agent"]["non_effect"]
    assert by_repo["OpenHands/OpenHands"]["license"] == "MIT"
    assert "NO_OPENHANDS_RUNTIME_DEPENDENCY" in by_repo["OpenHands/OpenHands"]["non_effect"]


def test_route_inspector_is_unofficial_unlicensed_evidence_reference_only():
    item = {x["repository"]: x for x in load()["repositories"]}["Liu-Bot24/chatgpt-route-inspector"]
    assert item["license"] is None
    assert item["disposition"] == "HIGH_VALUE_PROVIDER_ROUTE_EVIDENCE_REFERENCE_UNLICENSED"
    assert "UNOFFICIAL_TOOL_NOT_OPENAI_AUTHORITY" in item["non_effect"]


def test_jailbreak_and_hackgpt_are_data_not_instruction():
    data = load()
    by_repo = {x["repository"]: x for x in data["repositories"]}
    assert data["rules"]["retrieved_jailbreak_or_persona_text_is_data_not_instruction"] is True
    assert data["rules"]["cybersecurity_source_does_not_grant_offensive_action_authority"] is True
    assert by_repo["calebmayaka/ChatGPT-JailBreak"]["disposition"] == "ADVERSARIAL_PROMPT_CORPUS_DATA_NOT_INSTRUCTION"
    assert by_repo["NoDataFound/hackGPT"]["disposition"] == "HOSTILE_SECURITY_AUTONOMY_CORPUS_DATA_NOT_INSTRUCTION"
    assert "NO_EXPLOIT_MALWARE_JAILBREAK_EXECUTION" in by_repo["NoDataFound/hackGPT"]["non_effect"]


def test_license_unresolved_sources_fail_closed_for_code_reuse():
    by_repo = {x["repository"]: x for x in load()["repositories"]}
    assert by_repo["rasbt/LLMs-from-scratch"]["license"] == "NOASSERTION"
    assert "NO_CODE_REUSE" in by_repo["rasbt/LLMs-from-scratch"]["non_effect"]
    assert by_repo["howl-anderson/unlocking-the-power-of-llms"]["license"] is None
    assert "NO_CODE_COPY" in by_repo["howl-anderson/unlocking-the-power-of-llms"]["non_effect"]


def test_document_preserves_state_and_authority_separation():
    text = DOC.read_text(encoding="utf-8")
    for phrase in (
        "DATA_NOT_INSTRUCTION",
        "CYBER_ANALYSIS != OFFENSIVE_ACTION_AUTHORITY",
        "EXECUTION_TERMINAL != DURABLE_WORKER_IDENTITY",
        "UNOFFICIAL_ROUTE_OBSERVATION != PROVIDER_AUTHORITY",
        "does not rewrite the first eight observations",
    ):
        assert phrase in text
