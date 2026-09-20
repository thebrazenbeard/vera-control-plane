from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any

from tools.sd1_causal_frontier_witness import (
    build_successor_frontier,
    validate_frontier,
)
from tools.sd1_causal_supabase_witness import SupabaseFrontierWitness
from tools.sd1_causal_witness_testing import MemoryFrontierWitness

_ALLOWED_OUTCOMES = {"RESPONSE", "MISSING", "UNKNOWN"}
_FROZEN_IMMUTABLE_PLAN_SHA256 = "526f35438c2521d40e7a2bfa145da363e0c5063d2affef27131f9370e08564ba"
_RANDOMIZATION_SEED = "VERA_SD1_CAUSALITY_V1_20260913_FROZEN"
_CONDITION_SUBJECT_IDS = {
    "DRIVE_OFF": "VERA_R10A0_SD1_CAUSAL_DRIVE_OFF",
    "DRIVE_ON": "VERA_R10A0_SD1_CAUSAL_DRIVE_ON",
}
_RESPONSE_INPUT_FIELDS = {"timestamp", "outcome", "response_text", "pre_run_readback"}
_NONRESPONSE_INPUT_FIELDS = {"timestamp", "outcome", "reason", "pre_run_readback"}
_LEDGER_GENESIS_DIGEST = hashlib.sha256(b"SD1_CAUSAL_ATTEMPT_LEDGER_V1_GENESIS").hexdigest()
_INTEGRITY_FIELDS = {"previous_record_digest", "record_digest"}
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


def _read_witness_frontier(witness: Any) -> dict[str, Any]:
    if witness is None:
        raise ValueError("causal frontier witness is required")
    if type(witness) is MemoryFrontierWitness:
        read = MemoryFrontierWitness.read_frontier
    elif type(witness) is SupabaseFrontierWitness:
        read = SupabaseFrontierWitness.read_frontier
    else:
        raise ValueError("causal frontier witness is not an exact reviewed witness")
    if getattr(witness, "monotonicity_qualified", False) is not True:
        raise ValueError("causal frontier witness is not monotonicity-qualified")
    store_id = getattr(witness, "store_id", None)
    if type(store_id) is not str or not store_id:
        raise ValueError("causal frontier witness interface is invalid")
    frontier = read(witness)
    if type(frontier) is not dict:
        raise ValueError("causal frontier witness readback must be an object")
    validate_frontier(frontier, expected_store_id=store_id)
    return frontier


def _advance_witness_frontier(
    witness: Any,
    *,
    expected_frontier_digest: str,
    successor: dict[str, Any],
) -> dict[str, Any]:
    if type(witness) is MemoryFrontierWitness:
        advance = MemoryFrontierWitness.advance_frontier
    elif type(witness) is SupabaseFrontierWitness:
        advance = SupabaseFrontierWitness.advance_frontier
    else:
        raise ValueError("causal frontier witness is not an exact reviewed witness")
    return advance(
        witness,
        expected_frontier_digest=expected_frontier_digest,
        successor=successor,
    )


def _reconcile_ledger_frontier(
    ledger: dict[str, Any],
    frontier: dict[str, Any],
) -> None:
    order = ledger["record_order"]
    if frontier["generation"] != len(order):
        raise ValueError("RECOVERY_REQUIRED: witness generation diverges from ledger")
    if frontier["record_count"] != len(order):
        raise ValueError("RECOVERY_REQUIRED: witness record_count diverges from ledger")
    if frontier["chain_head"] != ledger["chain_head"]:
        raise ValueError("RECOVERY_REQUIRED: witness chain_head diverges from ledger")
    if not order:
        if frontier["last_slot_id"] is not None or frontier["last_record_digest"] is not None:
            raise ValueError("RECOVERY_REQUIRED: empty ledger has nonempty witness tail")
        return
    last_slot = order[-1]
    last_record = ledger["records"][last_slot]
    if frontier["last_slot_id"] != last_slot:
        raise ValueError("RECOVERY_REQUIRED: witness last_slot_id diverges from ledger")
    if frontier["last_record_digest"] != last_record["record_digest"]:
        raise ValueError("RECOVERY_REQUIRED: witness last_record_digest diverges from ledger")


def _recovery_artifacts(path: Path) -> list[Path]:
    if not path.parent.exists():
        return []
    prefix = f".{path.name}.pending-"
    return sorted(
        item
        for item in path.parent.iterdir()
        if item.is_file()
        and (
            item.name.startswith(prefix)
            or (item.name.startswith(prefix) and item.name.endswith(".recovery"))
        )
    )


def _require_no_recovery_artifacts(path: Path) -> None:
    artifacts = _recovery_artifacts(path)
    if artifacts:
        raise ValueError(
            "RECOVERY_REQUIRED: unresolved pending causal ledger artifact exists"
        )


def _candidate_ledger_with_record(
    ledger: dict[str, Any],
    slot_id: str,
    stored: dict[str, Any],
) -> dict[str, Any]:
    candidate = json.loads(json.dumps(ledger))
    previous = candidate["chain_head"]
    stored = json.loads(json.dumps(stored))
    stored["previous_record_digest"] = previous
    stored["record_digest"] = _record_digest(previous, stored)
    candidate["records"][slot_id] = stored
    candidate["record_order"].append(slot_id)
    candidate["chain_head"] = stored["record_digest"]
    return candidate


def record_attempt(
    plan: dict[str, Any],
    ledger_path: str | Path,
    slot_id: str,
    record: dict[str, Any],
    *,
    witness: Any,
) -> dict[str, Any]:
    _validate_immutable_plan(plan)
    if type(record) is not dict:
        raise ValueError("attempt record must be an exact mapping")
    slot = _find_slot(plan, slot_id)
    condition = slot["condition"]
    binding = plan["runtime_bindings"][condition]
    if binding.get("ready") is not True:
        raise ValueError("condition runtime cut is not bound and read back")
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
    supplied = record.get("pre_run_readback")
    if type(supplied) is not dict or supplied != _expected_readback(binding, condition):
        raise ValueError("attempt requires exact complete pre-run readback")
    stored["pre_run_readback"] = dict(supplied)
    if outcome == "RESPONSE":
        if type(record.get("response_text")) is not str or not record["response_text"]:
            raise ValueError("response outcome requires response_text")
        stored["response_text"] = record["response_text"]
    else:
        if type(record.get("reason")) is not str or not record["reason"]:
            raise ValueError("missing/unknown outcome requires reason")
        stored["reason"] = record["reason"]

    path = Path(ledger_path)
    _require_no_recovery_artifacts(path)
    ledger = _load_ledger(path)
    _validate_ledger_integrity(plan, ledger)
    current_frontier = _read_witness_frontier(witness)
    _reconcile_ledger_frontier(ledger, current_frontier)
    if slot_id in ledger["records"]:
        raise ValueError("attempt slot is immutable once recorded; reroll/overwrite forbidden")

    candidate = _candidate_ledger_with_record(ledger, slot_id, stored)
    _validate_ledger_integrity(plan, candidate)
    successor_frontier = build_successor_frontier(
        current_frontier,
        candidate,
        expected_store_id=witness.store_id,
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    pending_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.pending-",
            suffix=".json",
            delete=False,
        ) as pending:
            pending.write(json.dumps(candidate, indent=2, ensure_ascii=False) + "\n")
            pending.flush()
            os.fsync(pending.fileno())
            pending_path = Path(pending.name)

        advanced = _advance_witness_frontier(
            witness,
            expected_frontier_digest=current_frontier["frontier_digest"],
            successor=successor_frontier,
        )
        if advanced != successor_frontier:
            raise ValueError("RECOVERY_REQUIRED: witness successor readback mismatch")
        confirmed = _read_witness_frontier(witness)
        if confirmed != successor_frontier:
            raise ValueError("RECOVERY_REQUIRED: witness post-CAS readback mismatch")

        os.replace(pending_path, path)
        pending_path = None
        persisted = _load_ledger(path)
        _validate_ledger_integrity(plan, persisted)
        _reconcile_ledger_frontier(persisted, confirmed)
        return persisted["records"][slot_id]
    finally:
        # A leftover pending file after a failed/ambiguous witness mutation is
        # recovery evidence, not a candidate that may be silently retried.
        if pending_path is not None and pending_path.exists():
            recovery = pending_path.with_suffix(pending_path.suffix + ".recovery")
            try:
                os.replace(pending_path, recovery)
            except OSError:
                pass


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
    if record.get("pre_run_readback") != _expected_readback(binding, slot["condition"]):
        raise ValueError("ledger pre-run readback diverges from bound runtime tuple")
    if outcome == "RESPONSE":
        if type(record.get("response_text")) is not str or not record["response_text"]:
            raise ValueError("ledger response requires response_text")
    else:
        if type(record.get("reason")) is not str or not record["reason"]:
            raise ValueError("ledger missing/unknown outcome requires reason")
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


def blinded_export(
    plan: dict[str, Any],
    ledger_path: str | Path,
    *,
    witness: Any,
) -> list[dict[str, Any]]:
    _validate_immutable_plan(plan)
    path = Path(ledger_path)
    _require_no_recovery_artifacts(path)
    ledger = _load_ledger(path)
    _validate_ledger_integrity(plan, ledger)
    frontier = _read_witness_frontier(witness)
    _reconcile_ledger_frontier(ledger, frontier)
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
