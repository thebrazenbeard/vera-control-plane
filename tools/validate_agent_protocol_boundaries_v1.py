"""Offline, fail-closed validator for an advisory Vera protocol decision record.

No imports, requests, or execution from the inspected repository; not an effect gate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

MECHANISMS = {
    "TOOL_ACCESS": "MCP",
    "DURABLE_COORDINATION": "BUS",
    "AGENT_DELEGATION": "A2A",
    "IN_PROCESS": "DIRECT_CALL",
    "SERVICE_API": "HTTPS_OR_EXISTING_AUTHENTICATED_API",
    "UI_STREAM": "VNC_OR_APPROVED_SCREEN_CHANNEL",
    "USER_APPROVAL": "NATIVE_UI",
}
REQUIRED_CONTROL = "NO_IMPLICIT_ESCALATION"
REQUIRED_IDS = {
    "vera-plugin-tools", "vera-peer-coordination", "remote-independent-agent",
    "same-process-functions", "authorized-host-service",
    "authorized-screen-share", "human-approval-ui",
}


def validate(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["root must be an object"]
    if document.get("schema") != "VERA_AGENT_PROTOCOL_BOUNDARIES_V1":
        errors.append("schema mismatch")
    if document.get("status") != "ADVISORY_SOURCE_CANDIDATE_NON_ACTIVATING":
        errors.append("may not promote source to activated status")
    if document.get("runtime_consumption") != "UNVERIFIED_NOT_CLAIMED":
        errors.append("runtime consumption is unverified")
    if document.get("authority_rule") != "TRANSPORT_AND_DISCOVERY_NEVER_CONFER_AUTHORITY":
        errors.append("protocol transport may not grant authorization")
    paths = document.get("paths")
    if not isinstance(paths, list):
        return errors + ["paths must be an array"]
    seen: set[str] = set()
    for i, path in enumerate(paths):
        if not isinstance(path, dict):
            errors.append(f"paths[{i}] must be an object")
            continue
        pid = path.get("id")
        if not isinstance(pid, str) or not pid:
            errors.append(f"paths[{i}] has invalid id")
        elif pid in seen:
            errors.append(f"duplicate id {pid}")
        else:
            seen.add(pid)
        kind = path.get("kind")
        if not isinstance(kind, str) or kind not in MECHANISMS or path.get("mechanism") != MECHANISMS.get(kind):
            errors.append(f"paths[{i}] incompatible kind/mechanism")
        if not isinstance(path.get("permission_source"), str) or not path["permission_source"].strip():
            errors.append(f"paths[{i}] lacks permission source")
        if not isinstance(path.get("from"), str) or not isinstance(path.get("to"), str):
            errors.append(f"paths[{i}] lacks endpoints")
        controls = path.get("controls")
        if not isinstance(controls, list) or not all(isinstance(x, str) for x in controls):
            errors.append(f"paths[{i}] controls must be an array of strings")
            controls = []
        if REQUIRED_CONTROL not in controls:
            errors.append(f"paths[{i}] lacks no-escalation control")
        if kind == "AGENT_DELEGATION":
            if path.get("adoption") != "DEFERRED_UNTIL_INDEPENDENT_RUNTIME_VERIFIED":
                errors.append("A2A not qualified for current deployment")
            if not {"EXACT_TASK_ID", "EXPLICIT_SCOPE", "RECEIPT_AND_ARTIFACT"} <= set(controls):
                errors.append("A2A delegation missing task/permission/receipt controls")
        if kind == "UI_STREAM" and "SEPARATE_INPUT_LEASE" not in controls:
            errors.append("screen observation may not imply input authority")
        if kind == "USER_APPROVAL" and "SERVER_SIDE_APPROVAL_CHECK" not in controls:
            errors.append("approval must be verified server-side")
    if seen != REQUIRED_IDS:
        errors.append("path inventory differs from the seven explicitly reviewed paths")
    failures = document.get("failure_contract")
    if not isinstance(failures, dict):
        errors.append("missing failure contract")
    else:
        if failures.get("mutation_timeout") != "UNKNOWN_EFFECT_RECONCILE_BEFORE_RETRY":
            errors.append("ambiguous mutations must be reconciled before retry")
        if failures.get("unavailable_requested_route") != "FAIL_CLOSED_DO_NOT_SILENTLY_SWITCH_TRANSPORT":
            errors.append("route failure must not silently fallback")
        if failures.get("transport_loss") != "DROP_EXPIRED_LEASES_REVOKE_INPUT_RECHECK_HOST_IDENTITY":
            errors.append("transport loss must revoke input and recheck host")
    non_claims = document.get("non_claims")
    if not isinstance(non_claims, list) or "NOT_AN_AUTHORIZATION_TOKEN" not in non_claims:
        errors.append("advisory cannot act as authorization token")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1] / "protocol" / "VERA_AGENT_PROTOCOL_BOUNDARIES_V1.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    errors = validate(document)
    if errors:
        print(json.dumps({"status": "BLOCK", "findings": errors}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "checked_paths": len(document["paths"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
