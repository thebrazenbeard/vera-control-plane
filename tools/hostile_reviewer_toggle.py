from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Mapping


SCHEMA = "VERA_HOSTILE_REVIEWER_STATE_V1"
VALID_MODES = {"OFF", "ON"}
REQUIRED_SCOPE = "VERA_PROJECT_ALL_CHATS"


class HostileReviewerControlError(RuntimeError):
    pass


def _validate_state(value: Mapping[str, Any]) -> None:
    if value.get("schema") != SCHEMA:
        raise HostileReviewerControlError("unexpected hostile reviewer state schema")
    generation = value.get("generation")
    if not isinstance(generation, int) or generation < 0:
        raise HostileReviewerControlError("generation must be a non-negative integer")
    if value.get("mode") not in VALID_MODES:
        raise HostileReviewerControlError("state contains unsupported mode")
    if value.get("scope") != REQUIRED_SCOPE:
        raise HostileReviewerControlError("state is not bound to all-chat project scope")


def load_state(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise HostileReviewerControlError("state must be a JSON object")
    _validate_state(value)
    return value


def set_mode(
    path: Path,
    *,
    mode: str,
    expected_generation: int,
    change_kind: str = "EXPLICIT_CONTROL_CHANGE",
    note: str = "",
) -> dict[str, Any]:
    if mode not in VALID_MODES:
        raise HostileReviewerControlError(f"unsupported mode: {mode}")

    current = load_state(path)
    if current["generation"] != expected_generation:
        raise HostileReviewerControlError(
            f"stale generation: expected {expected_generation}, "
            f"observed {current['generation']}"
        )

    updated = dict(current)
    updated["generation"] = expected_generation + 1
    updated["mode"] = mode
    updated["last_change"] = {
        "kind": change_kind,
        "note": note,
    }

    payload = json.dumps(updated, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as tmp:
        tmp.write(payload)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_name = tmp.name

    try:
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)

    readback = load_state(path)
    if (
        readback["generation"] != expected_generation + 1
        or readback["mode"] != mode
    ):
        raise HostileReviewerControlError("post-write readback mismatch")
    return readback


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("state_path", type=Path)
    parser.add_argument("--mode", required=True, choices=sorted(VALID_MODES))
    parser.add_argument("--expected-generation", required=True, type=int)
    parser.add_argument("--note", default="")
    args = parser.parse_args()

    result = set_mode(
        args.state_path,
        mode=args.mode,
        expected_generation=args.expected_generation,
        note=args.note,
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
