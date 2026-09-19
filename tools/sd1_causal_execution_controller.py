from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

_ALLOWED_OUTCOMES = {"RESPONSE", "MISSING", "UNKNOWN"}
_FROZEN_IMMUTABLE_PLAN_SHA256 = "6ee74773f1619f392aff04078d5c45d65b3f31675da5856d58c34d3ace290eda"
_RANDOMIZATION_SEED = "VERA_SD1_CAUSALITY_V1_20260913_FROZEN"
_CONDITION_SUBJECT_IDS = {
    "DRIVE_OFF": "VERA_R10A0_SD1_CAUSAL_DRIVE_OFF",
    "DRIVE_ON": "VERA_R10A0_SD1_CAUSAL_DRIVE_ON",
}
_RESPONSE_INPUT_FIELDS = {"timestamp", "outcome", "response_text", "pre_run_readback"}
_NONRESPONSE_INPUT_FIELDS = {"timestamp", "outcome", "reason", "pre_run_readback"}
_LEDGER_GENESIS_DIGEST = hashlib.sha256(b"SD1_CAUSAL_ATTEMPT_LEDGER_V1_GENESIS").hexdigest()
_INTEGRITY_FIELDS = {"previous_record_digest", "record_digest"}
_RECEIPT_MANIFEST_SCHEMA = "SD1_CAUSAL_RECEIPT_MANIFEST_V1"
_RECEIPT_SCHEMA = "SD1_CAUSAL_RECEIPT_V1"
_RECEIPT_BINDING_FIELDS = {"repository", "branch", "run_id", "genesis_commit"}
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

def _canonical_sha256(data: Any) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _validate_immutable_plan(plan: dict[str, Any]) -> None:
    immutable = {
        key: plan.get(key)
        for key in ("schema", "status", "source_protocol", "pre_data_freeze", "blinding", "slots")
    }
    if _canonical_sha256(immutable) != _FROZEN_IMMUTABLE_PLAN_SHA256:
        raise ValueError("causal plan immutable subject diverges from frozen pre-data plan")
    slots = plan.get("slots")
    if type(slots) is not list or len(slots) != 70:
        raise ValueError("causal controller must contain exactly 70 frozen slots")
    if len({item.get("slot_id") for item in slots}) != 70:
        raise ValueError("slot ids must be unique")
    if len({item.get("response_id") for item in slots}) != 70:
        raise ValueError("response ids must be unique")
    bindings = plan.get("runtime_bindings")
    if type(bindings) is not dict or set(bindings) != {"DRIVE_OFF", "DRIVE_ON"}:
        raise ValueError("runtime bindings must contain exactly DRIVE_OFF and DRIVE_ON")
    receipt_binding = plan.get("receipt_binding")
    expected_receipt_keys = {"ready"} | _RECEIPT_BINDING_FIELDS
    if type(receipt_binding) is not dict or set(receipt_binding) != expected_receipt_keys:
        raise ValueError("receipt binding must contain the exact receipt-plane fields")
    if receipt_binding.get("repository") != plan["pre_data_freeze"]["receipt_repository"]:
        raise ValueError("receipt binding repository diverges from frozen receipt plane")


def load_plan(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    _validate_immutable_plan(data)
    return data


def _binding_fields(condition: str) -> tuple[str, ...]:
    try:
        return _REQUIRED_BINDING_FIELDS[condition]
    except KeyError as exc:
        raise ValueError(f"unknown condition: {condition}") from exc


def bind_runtime_cut(plan: dict[str, Any], condition: str, binding: dict[str, Any]) -> dict[str, Any]:
    _validate_immutable_plan(plan)
    if type(binding) is not dict:
        raise ValueError("runtime binding must be a mapping")
    required = _binding_fields(condition)
    if set(binding) != set(required):
        raise ValueError("runtime binding must contain the exact required readback fields")
    if any(type(binding[name]) is not str or not binding[name] for name in required):
        raise ValueError("runtime binding fields must be non-empty exact strings")
    out = json.loads(json.dumps(plan))
    out["runtime_bindings"][condition] = dict(binding, ready=True, required_readback=list(required))
    return out


def _is_hex_commit(value: Any) -> bool:
    return type(value) is str and len(value) == 40 and all(ch in "0123456789abcdef" for ch in value.lower())


def bind_receipt_plane(plan: dict[str, Any], binding: dict[str, Any]) -> dict[str, Any]:
    _validate_immutable_plan(plan)
    if type(binding) is not dict or set(binding) != _RECEIPT_BINDING_FIELDS:
        raise ValueError("receipt binding must contain exact repository/branch/run_id/genesis_commit fields")
    if binding["repository"] != plan["pre_data_freeze"]["receipt_repository"]:
        raise ValueError("receipt repository diverges from frozen receipt plane")
    prefix = plan["pre_data_freeze"]["receipt_branch_prefix"]
    if type(binding["branch"]) is not str or not binding["branch"].startswith(prefix):
        raise ValueError("receipt branch must use the frozen private receipt prefix")
    if type(binding["run_id"]) is not str or not binding["run_id"]:
        raise ValueError("receipt run id is required")
    if not _is_hex_commit(binding["genesis_commit"]):
        raise ValueError("receipt genesis commit must be an exact 40-hex Git commit")
    out = json.loads(json.dumps(plan))
    out["receipt_binding"] = dict(binding, ready=True)
    return out


def _empty_ledger() -> dict[str, Any]:
    return {
        "schema": "SD1_CAUSAL_ATTEMPT_LEDGER_V1",
        "records": {},
        "record_order": [],
        "chain_head": _LEDGER_GENESIS_DIGEST,
    }


def _load_ledger(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _empty_ledger()
    data = json.loads(path.read_text(encoding="utf-8"))
    if set(data) != {"schema", "records", "record_order", "chain_head"}:
        raise ValueError("invalid causal ledger envelope")
    if data.get("schema") != "SD1_CAUSAL_ATTEMPT_LEDGER_V1" or type(data.get("records")) is not dict:
        raise ValueError("invalid causal ledger")
    order = data.get("record_order")
    if type(order) is not list or len(order) != len(set(order)):
        raise ValueError("ledger record order must be a unique list")
    if set(data["records"]) != set(order):
        raise ValueError("ledger record order and record keys diverge")
    if type(data.get("chain_head")) is not str or not data["chain_head"]:
        raise ValueError("ledger chain head is required")
    return data


def _find_slot(plan: dict[str, Any], slot_id: str) -> dict[str, Any]:
    matches = [item for item in plan["slots"] if item.get("slot_id") == slot_id]
    if len(matches) != 1:
        raise ValueError("slot id is not exactly one frozen slot")
    return matches[0]


def _expected_readback(binding: dict[str, Any], condition: str) -> dict[str, str]:
    return {name: binding[name] for name in _binding_fields(condition)}


def _record_attempt_with_manifest(plan: dict[str, Any], ledger_path: str | Path, slot_id: str, record: dict[str, Any], *, receipt_manifest: dict[str, Any]) -> dict[str, Any]:
    _validate_immutable_plan(plan)
    if type(record) is not dict:
        raise ValueError("attempt record must be an exact mapping")
    slot = _find_slot(plan, slot_id)
    condition = slot["condition"]
    binding = plan["runtime_bindings"][condition]
    if binding.get("ready") is not True:
        raise ValueError("condition runtime cut is not bound and read back")
    if plan["receipt_binding"].get("ready") is not True:
        raise ValueError("receipt plane is not bound")
    outcome = record.get("outcome")
    if outcome not in _ALLOWED_OUTCOMES:
        raise ValueError("attempt outcome must be RESPONSE, MISSING, or UNKNOWN")
    expected_fields = _RESPONSE_INPUT_FIELDS if outcome == "RESPONSE" else _NONRESPONSE_INPUT_FIELDS
    if set(record) != expected_fields:
        raise ValueError("attempt payload contains missing, extra, or caller-owned frozen metadata fields")
    if type(record.get("timestamp")) is not str or not record["timestamp"]:
        raise ValueError("attempt timestamp is required")
    stored = {
        "slot_id": slot_id,
        "response_id": slot["response_id"],
        "condition": condition,
        "prompt_id": slot["prompt_id"],
        "prompt_class": slot["prompt_class"],
        "attempt_index": slot["attempt_index"],
        "timestamp": record["timestamp"],
        "outcome": outcome,
    }
    if outcome == "RESPONSE":
        if type(record.get("response_text")) is not str or not record["response_text"]:
            raise ValueError("response outcome requires response_text")
        supplied = record.get("pre_run_readback")
        if type(supplied) is not dict or supplied != _expected_readback(binding, condition):
            raise ValueError("response requires exact complete pre-run readback")
        stored["response_text"] = record["response_text"]
        stored["pre_run_readback"] = dict(supplied)
    else:
        if type(record.get("reason")) is not str or not record["reason"]:
            raise ValueError("missing/unknown outcome requires reason")
        supplied = record.get("pre_run_readback")
        if type(supplied) is not dict or supplied != _expected_readback(binding, condition):
            raise ValueError("missing/unknown outcome requires exact complete pre-run readback")
        stored["reason"] = record["reason"]
        stored["pre_run_readback"] = dict(supplied)
    path = Path(ledger_path)
    ledger = _load_ledger(path)
    _validate_ledger_integrity(plan, ledger)
    _validate_receipt_manifest(plan, ledger, receipt_manifest, require_all_anchored=True)
    if slot_id in ledger["records"]:
        raise ValueError("attempt slot is immutable once recorded; reroll/overwrite forbidden")
    previous = ledger["chain_head"]
    stored["previous_record_digest"] = previous
    stored["record_digest"] = _record_digest(previous, stored)
    ledger["records"][slot_id] = stored
    ledger["record_order"].append(slot_id)
    ledger["chain_head"] = stored["record_digest"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    persisted = _load_ledger(path)
    _validate_ledger_integrity(plan, persisted)
    return persisted["records"][slot_id]


def record_attempt(plan: dict[str, Any], ledger_path: str | Path, slot_id: str, record: dict[str, Any], *, receipt_repo_path: str | Path) -> dict[str, Any]:
    from tools import sd1_causal_receipt_git as receipt_git
    manifest = receipt_git.read_verified_manifest(plan, receipt_repo_path)
    return _record_attempt_with_manifest(
        plan, ledger_path, slot_id, record, receipt_manifest=manifest
    )


def _record_digest(previous_digest: str, record: dict[str, Any]) -> str:
    payload = {key: value for key, value in record.items() if key not in _INTEGRITY_FIELDS}
    return _canonical_sha256({"previous_record_digest": previous_digest, "record": payload})


def _validate_ledger_record(plan: dict[str, Any], slot_id: str, record: dict[str, Any]) -> dict[str, Any]:
    if type(record) is not dict:
        raise ValueError("ledger record must be a mapping")
    slot = _find_slot(plan, slot_id)
    frozen = {
        "slot_id": slot_id,
        "response_id": slot["response_id"],
        "condition": slot["condition"],
        "prompt_id": slot["prompt_id"],
        "prompt_class": slot["prompt_class"],
        "attempt_index": slot["attempt_index"],
    }
    for key, value in frozen.items():
        if record.get(key) != value:
            raise ValueError("ledger metadata diverges from frozen slot map")
    outcome = record.get("outcome")
    expected_payload = {"timestamp", "outcome", "response_text", "pre_run_readback"} if outcome == "RESPONSE" else {"timestamp", "outcome", "reason", "pre_run_readback"}
    expected = set(frozen) | expected_payload | _INTEGRITY_FIELDS
    if outcome not in _ALLOWED_OUTCOMES or set(record) != expected:
        raise ValueError("ledger record schema diverges from frozen outcome schema")
    if type(record.get("timestamp")) is not str or not record["timestamp"]:
        raise ValueError("ledger attempt timestamp is required")
    binding = plan["runtime_bindings"][slot["condition"]]
    if binding.get("ready") is not True:
        raise ValueError("ledger condition runtime cut is not bound and read back")
    if outcome == "RESPONSE":
        if type(record.get("response_text")) is not str or not record["response_text"]:
            raise ValueError("ledger response requires response_text")
        if record.get("pre_run_readback") != _expected_readback(binding, slot["condition"]):
            raise ValueError("ledger response readback diverges from bound runtime tuple")
    else:
        if type(record.get("reason")) is not str or not record["reason"]:
            raise ValueError("ledger missing/unknown outcome requires reason")
        if record.get("pre_run_readback") != _expected_readback(binding, slot["condition"]):
            raise ValueError("ledger missing/unknown readback diverges from bound runtime tuple")
    previous = record.get("previous_record_digest")
    digest = record.get("record_digest")
    if type(previous) is not str or type(digest) is not str:
        raise ValueError("ledger integrity digests are required")
    if digest != _record_digest(previous, record):
        raise ValueError("ledger record digest mismatch")
    return slot


def _validate_ledger_integrity(plan: dict[str, Any], ledger: dict[str, Any]) -> None:
    previous = _LEDGER_GENESIS_DIGEST
    for slot_id in ledger["record_order"]:
        record = ledger["records"][slot_id]
        if record.get("previous_record_digest") != previous:
            raise ValueError("ledger hash chain predecessor mismatch")
        _validate_ledger_record(plan, slot_id, record)
        previous = record["record_digest"]
    if ledger["chain_head"] != previous:
        raise ValueError("ledger hash chain head mismatch")


def _receipt_file_path(run_id: str, sequence: int, slot_id: str) -> str:
    return f"state/runtime/sd1-causal-receipts/{run_id}/{sequence:03d}-{slot_id}.json"


def _receipt_payload(plan: dict[str, Any], ledger: dict[str, Any], index: int) -> dict[str, Any]:
    binding = plan["receipt_binding"]
    slot_id = ledger["record_order"][index]
    record = ledger["records"][slot_id]
    return {
        "schema": _RECEIPT_SCHEMA,
        "run_id": binding["run_id"],
        "sequence": index + 1,
        "slot_id": slot_id,
        "response_id": record["response_id"],
        "record_digest": record["record_digest"],
        "previous_record_digest": record["previous_record_digest"],
        "runtime_readback_digest": _canonical_sha256(record["pre_run_readback"]),
        "plan_subject_digest": _FROZEN_IMMUTABLE_PLAN_SHA256,
    }


def _validate_receipt_manifest(plan: dict[str, Any], ledger: dict[str, Any], manifest: dict[str, Any], *, require_all_anchored: bool) -> int:
    if plan["receipt_binding"].get("ready") is not True:
        raise ValueError("receipt plane is not bound")
    if type(manifest) is not dict:
        raise ValueError("receipt manifest must be an exact mapping")
    expected_top = {"schema", "repository", "branch", "run_id", "genesis_commit", "head_commit", "receipts"}
    if set(manifest) != expected_top or manifest.get("schema") != _RECEIPT_MANIFEST_SCHEMA:
        raise ValueError("receipt manifest envelope diverges from frozen schema")
    binding = plan["receipt_binding"]
    for field in ("repository", "branch", "run_id", "genesis_commit"):
        if manifest.get(field) != binding[field]:
            raise ValueError("receipt manifest diverges from bound private receipt plane")
    if not _is_hex_commit(manifest.get("head_commit")):
        raise ValueError("receipt manifest head must be an exact Git commit")
    receipts = manifest.get("receipts")
    if type(receipts) is not list or len(receipts) > len(ledger["record_order"]):
        raise ValueError("receipt manifest cannot exceed the local ledger")
    if require_all_anchored and len(receipts) != len(ledger["record_order"]):
        raise ValueError("every existing ledger record must be remotely anchored before continuing")
    if not receipts:
        if manifest["head_commit"] != binding["genesis_commit"]:
            raise ValueError("empty receipt manifest must remain at the bound genesis commit")
    elif manifest["head_commit"] != receipts[-1].get("receipt_commit"):
        raise ValueError("receipt manifest head must equal the final receipt commit")
    seen_commits = set()
    for index, receipt in enumerate(receipts):
        expected = _receipt_payload(plan, ledger, index)
        expected_keys = set(expected) | {"receipt_commit", "path"}
        if type(receipt) is not dict or set(receipt) != expected_keys:
            raise ValueError("receipt entry schema diverges from digest-only receipt contract")
        for key, value in expected.items():
            if receipt.get(key) != value:
                raise ValueError("receipt entry diverges from the first-write ledger digest")
        expected_path = _receipt_file_path(binding["run_id"], index + 1, expected["slot_id"])
        if receipt.get("path") != expected_path:
            raise ValueError("receipt path diverges from frozen private receipt path")
        commit = receipt.get("receipt_commit")
        if not _is_hex_commit(commit) or commit in seen_commits:
            raise ValueError("receipt commits must be unique exact Git commits")
        seen_commits.add(commit)
    return len(receipts)


def _build_receipt_payload_with_manifest(plan: dict[str, Any], ledger_path: str | Path, receipt_manifest: dict[str, Any]) -> dict[str, Any]:
    _validate_immutable_plan(plan)
    ledger = _load_ledger(Path(ledger_path))
    _validate_ledger_integrity(plan, ledger)
    anchored = _validate_receipt_manifest(plan, ledger, receipt_manifest, require_all_anchored=False)
    if len(ledger["record_order"]) != anchored + 1:
        raise ValueError("receipt generation requires exactly one unanchored trailing record")
    return _receipt_payload(plan, ledger, anchored)


def _blind_sort_key(slot: dict[str, Any]) -> str:
    subject_id = _CONDITION_SUBJECT_IDS[slot["condition"]]
    material = (
        _RANDOMIZATION_SEED
        + slot["prompt_id"]
        + str(slot["attempt_index"])
        + subject_id
        + slot["response_id"]
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def _blinded_export_with_manifest(plan: dict[str, Any], ledger_path: str | Path, *, receipt_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    _validate_immutable_plan(plan)
    ledger = _load_ledger(Path(ledger_path))
    _validate_ledger_integrity(plan, ledger)
    _validate_receipt_manifest(plan, ledger, receipt_manifest, require_all_anchored=True)
    exported = []
    for slot_id in ledger["record_order"]:
        record = ledger["records"][slot_id]
        slot = _validate_ledger_record(plan, slot_id, record)
        item = {
            "response_id": slot["response_id"],
            "prompt_id": slot["prompt_id"],
            "prompt_class": slot["prompt_class"],
            "attempt_index": slot["attempt_index"],
            "outcome": record["outcome"],
            "timestamp": record["timestamp"],
            "_blind_sort_key": _blind_sort_key(slot),
        }
        if record["outcome"] == "RESPONSE":
            item["response_text"] = record["response_text"]
        else:
            item["reason"] = record["reason"]
        exported.append(item)
    exported.sort(key=lambda item: item["_blind_sort_key"])
    for item in exported:
        item.pop("_blind_sort_key")
    return exported


def record_attempt(
    plan: dict[str, Any], ledger_path: str | Path, slot_id: str,
    record: dict[str, Any], receipt_repo_path: str | Path,
) -> dict[str, Any]:
    from tools import sd1_causal_receipt_git
    return sd1_causal_receipt_git.record_attempt(
        plan, ledger_path, slot_id, record, receipt_repo_path
    )


def build_receipt_payload(
    plan: dict[str, Any], ledger_path: str | Path, receipt_repo_path: str | Path,
) -> dict[str, Any]:
    from tools import sd1_causal_receipt_git
    manifest = sd1_causal_receipt_git.read_verified_manifest(plan, receipt_repo_path)
    return _build_receipt_payload_with_manifest(plan, ledger_path, manifest)


def blinded_export(
    plan: dict[str, Any], ledger_path: str | Path, receipt_repo_path: str | Path,
) -> list[dict[str, Any]]:
    from tools import sd1_causal_receipt_git
    return sd1_causal_receipt_git.blinded_export(plan, ledger_path, receipt_repo_path)

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

__all__ = ["load_plan", "bind_runtime_cut", "bind_receipt_plane", "record_attempt", "build_receipt_payload", "blinded_export", "validate_score"]
