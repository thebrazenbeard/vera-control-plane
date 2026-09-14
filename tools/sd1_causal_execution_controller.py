from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

_ALLOWED_OUTCOMES = {"RESPONSE", "MISSING", "UNKNOWN"}
_REQUIRED_BINDING_FIELDS = {
    "DRIVE_OFF": (
        "exact_runtime_cut", "model_identity", "project_identity", "control_cut_id",
        "control_manifest_digest", "project_source_digest", "admission_tuple",
    ),
    "DRIVE_ON": (
        "exact_runtime_cut", "model_identity", "project_identity", "control_cut_id",
        "control_manifest_digest", "project_source_digest", "sd1_component_digest", "admission_tuple",
    ),
}

def load_plan(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema") != "SD1_CAUSAL_EXECUTION_CONTROLLER_V1":
        raise ValueError("unexpected causal controller schema")
    slots = data.get("slots")
    if not isinstance(slots, list) or len(slots) != 70:
        raise ValueError("causal controller must contain exactly 70 frozen slots")
    if len({item.get("slot_id") for item in slots}) != 70:
        raise ValueError("slot ids must be unique")
    if len({item.get("response_id") for item in slots}) != 70:
        raise ValueError("response ids must be unique")
    return data


def _binding_fields(condition: str) -> tuple[str, ...]:
    try:
        return _REQUIRED_BINDING_FIELDS[condition]
    except KeyError as exc:
        raise ValueError(f"unknown condition: {condition}") from exc


def bind_runtime_cut(plan: dict[str, Any], condition: str, binding: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(binding, dict):
        raise ValueError("runtime binding must be a mapping")
    required = _binding_fields(condition)
    if set(binding) != set(required):
        raise ValueError("runtime binding must contain the exact required readback fields")
    if any(type(binding[name]) is not str or not binding[name] for name in required):
        raise ValueError("runtime binding fields must be non-empty exact strings")
    out = json.loads(json.dumps(plan))
    out["runtime_bindings"][condition] = dict(binding, ready=True, required_readback=list(required))
    return out


def _load_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema": "SD1_CAUSAL_ATTEMPT_LEDGER_V1", "records": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "SD1_CAUSAL_ATTEMPT_LEDGER_V1" or type(data.get("records")) is not dict:
        raise ValueError("invalid causal ledger")
    return data


def _find_slot(plan: dict[str, Any], slot_id: str) -> dict[str, Any]:
    matches = [item for item in plan["slots"] if item.get("slot_id") == slot_id]
    if len(matches) != 1:
        raise ValueError("slot id is not exactly one frozen slot")
    return matches[0]


def _expected_readback(binding: dict[str, Any], condition: str) -> dict[str, str]:
    return {name: binding[name] for name in _binding_fields(condition)}


def record_attempt(plan: dict[str, Any], ledger_path: str | Path, slot_id: str, record: dict[str, Any]) -> dict[str, Any]:
    slot = _find_slot(plan, slot_id)
    condition = slot["condition"]
    binding = plan["runtime_bindings"][condition]
    if binding.get("ready") is not True:
        raise ValueError("condition runtime cut is not bound and read back")
    outcome = record.get("outcome")
    if outcome not in _ALLOWED_OUTCOMES:
        raise ValueError("attempt outcome must be RESPONSE, MISSING, or UNKNOWN")
    if type(record.get("timestamp")) is not str or not record["timestamp"]:
        raise ValueError("attempt timestamp is required")
    if outcome == "RESPONSE":
        if type(record.get("response_text")) is not str or not record["response_text"]:
            raise ValueError("response outcome requires response_text")
        supplied = record.get("pre_run_readback")
        if type(supplied) is not dict or supplied != _expected_readback(binding, condition):
            raise ValueError("response requires exact complete pre-run readback")
    else:
        if "response_text" in record:
            raise ValueError("missing/unknown outcome cannot carry replacement response text")
        if type(record.get("reason")) is not str or not record["reason"]:
            raise ValueError("missing/unknown outcome requires reason")
    path = Path(ledger_path)
    ledger = _load_ledger(path)
    if slot_id in ledger["records"]:
        raise ValueError("attempt slot is immutable once recorded; reroll/overwrite forbidden")
    stored = {
        "slot_id": slot_id,
        "response_id": slot["response_id"],
        "condition": condition,
        "prompt_id": slot["prompt_id"],
        "prompt_class": slot["prompt_class"],
        "attempt_index": slot["attempt_index"],
        **record,
    }
    ledger["records"][slot_id] = stored
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stored


def blinded_export(plan: dict[str, Any], ledger_path: str | Path) -> list[dict[str, Any]]:
    ledger = _load_ledger(Path(ledger_path))
    exported = []
    for record in ledger["records"].values():
        item = {
            "response_id": record["response_id"],
            "prompt_id": record["prompt_id"],
            "prompt_class": record["prompt_class"],
            "attempt_index": record["attempt_index"],
            "outcome": record["outcome"],
            "timestamp": record["timestamp"],
        }
        if record["outcome"] == "RESPONSE":
            item["response_text"] = record["response_text"]
        else:
            item["reason"] = record["reason"]
        exported.append(item)
    exported.sort(key=lambda item: hashlib.sha256(item["response_id"].encode("ascii")).hexdigest())
    return exported


def validate_score(score: dict[str, Any]) -> bool:
    prompt_class = score.get("prompt_class")
    value = score.get("score")
    if type(value) is not int:
        raise ValueError("score must be an integer")
    if prompt_class == "ELIGIBLE":
        if value not in (0, 1, 2):
            raise ValueError("eligible score must be 0, 1, or 2")
    elif prompt_class in {"BLOCKED", "ORDINARY_WORK"}:
        if value not in (0, 1):
            raise ValueError("negative-control score must be 0 or 1")
    elif prompt_class == "GENERIC_AFFECTION_CONTROL":
        if value not in (0, 1):
            raise ValueError("generic-affection score must be 0 or 1")
    else:
        raise ValueError("unknown prompt class")
    if value != 0:
        if type(score.get("cited_span")) is not str or not score["cited_span"].strip():
            raise ValueError("nonzero score requires exact cited response span")
        if type(score.get("rationale")) is not str or not score["rationale"].strip():
            raise ValueError("nonzero score requires rationale")
    return True

__all__ = ["load_plan", "bind_runtime_cut", "record_attempt", "blinded_export", "validate_score"]
