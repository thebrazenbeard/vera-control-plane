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

# Immutable semantics of this reviewed V1 contract. Intentional route changes
# require a versioned successor and independent review, not silent in-place edits.
BINDING_FIELDS = ("kind", "from", "to", "effect_class", "permission_source", "adoption")
EXPECTED_BINDINGS = {
    "vera-plugin-tools": ("TOOL_ACCESS", "vera-chat-orchestrator", "connected-authorized-tool-server", "CAPABILITY_SCOPED", "LIVE_HOST_GRANT_AND_PER_EFFECT_AUTHORIZATION", "EXISTING_ROUTE_REVERIFY_LIVE"),
    "vera-peer-coordination": ("DURABLE_COORDINATION", "vera-coordinator", "assigned-engineering-worker", "SOURCE_COORDINATION_ONLY", "CURRENT_OWNER_ASSIGNMENT_AND_EXACT_EFFECT_GRANT", "EXISTING_ROUTE_REVERIFY_LIVE"),
    "remote-independent-agent": ("AGENT_DELEGATION", "authenticated-delegator", "independently-deployed-agent-service", "SOURCE_COORDINATION_ONLY", "EXPLICIT_TASK_SCOPED_DELEGATION_AND_REMOTE_AUTHZ", "DEFERRED_UNTIL_INDEPENDENT_RUNTIME_VERIFIED"),
    "same-process-functions": ("IN_PROCESS", "coordinator-module", "same-process-helper", "CAPABILITY_SCOPED", "CALLER_CONTEXT_WITH_IN_PROCESS_EFFECT_GATE", "USE_WHEN_LOCAL_AND_BOUND"),
    "authorized-host-service": ("SERVICE_API", "approved-host-controller", "host-owned-service", "CAPABILITY_SCOPED", "HOST_IDENTITY_AND_PER_EFFECT_LEASE", "KEEP_EXISTING_ROUTE_REVERIFY_LIVE"),
    "authorized-screen-share": ("UI_STREAM", "approved-screen-client", "consenting-screen-host", "OBSERVE_ONLY_UNTIL_INPUT_LEASE", "SEPARATE_HUMAN_OBSERVE_AND_INPUT_CONSENT", "UNDER_INDEPENDENT_QUALIFICATION"),
    "human-approval-ui": ("USER_APPROVAL", "authenticated-human", "proposed-protected-effect", "PROTECTED", "PATRICK_EXACT_TARGET_SCOPE_AND_APPROVAL", "USE_NATIVE_HOST_UI"),
}

# V1 is a frozen advisory policy: an added/removed control or a relaxed failure
# rule is a material new review subject even when the path ID stays unchanged.
EXPECTED_CONTROLS = {
    "vera-plugin-tools": ("EXACT_TOOL_SCOPE", "HOST_GRANT_CHECK", "NO_IMPLICIT_ESCALATION", "EFFECT_RECEIPT", "NO_BLIND_MUTATION_RETRY"),
    "vera-peer-coordination": ("EXACT_SUBJECT_HEAD", "OWNER_LANE", "ALLOWED_AND_PROHIBITED_EFFECTS", "RETURN_RECEIPT", "NO_IMPLICIT_ESCALATION"),
    "remote-independent-agent": ("AGENT_CARD_IDENTITY", "EXACT_TASK_ID", "EXACT_SUBJECT_HEAD", "EXPLICIT_SCOPE", "RECEIPT_AND_ARTIFACT", "NO_IMPLICIT_ESCALATION"),
    "same-process-functions": ("EXACT_FUNCTION_CONTRACT", "EFFECT_GATE", "NO_IMPLICIT_ESCALATION"),
    "authorized-host-service": ("TARGET_HOST_BINDING", "EXACT_EFFECT_SCOPE", "LEASE_AND_REVOKE", "IDEMPOTENCY_OR_RECONCILE", "NO_IMPLICIT_ESCALATION"),
    "authorized-screen-share": ("LIVE_HOST_TARGET", "SEPARATE_INPUT_LEASE", "REVOKE_ON_FAILURE", "NO_IMPLICIT_ESCALATION"),
    "human-approval-ui": ("SERVER_SIDE_APPROVAL_CHECK", "APPROVAL_NOT_INFERRED_FROM_BUTTON", "EXPIRY_AND_REVOCATION", "NO_IMPLICIT_ESCALATION"),
}
EXPECTED_FAILURE_CONTRACT = {
    "read_timeout": "RETRY_WITH_BOUNDS_AND_FRESH_CURRENTNESS",
    "mutation_timeout": "UNKNOWN_EFFECT_RECONCILE_BEFORE_RETRY",
    "unavailable_requested_route": "FAIL_CLOSED_DO_NOT_SILENTLY_SWITCH_TRANSPORT",
    "transport_loss": "DROP_EXPIRED_LEASES_REVOKE_INPUT_RECHECK_HOST_IDENTITY",
    "agent_handoff_loss": "REASSIGN_ONLY_WITH_DURABLE_OWNER_RECONCILIATION",
    "audit": "APPEND_SOURCE_CLASS_EXACT_HEAD_EFFECT_RECEIPT_AND_REDACT_PRIVATE_DATA",
}
EXPECTED_NON_CLAIMS = (
    "NOT_AN_INSTALLED_CONTROL", "NOT_A_DEPLOYMENT",
    "NOT_A_CURRENT_PROVIDER_PROBE", "NOT_AN_AUTHORIZATION_TOKEN",
    "NOT_A_BEHAVIORAL_QUALIFICATION",
)
EXPECTED_SCOPE = "Vera Unbound inter-service communication design, not active installation or delegated effect authority"
REVIEWED_ROOT_FIELDS = frozenset({"schema", "logical_id", "status", "runtime_consumption", "authority_rule", "scope", "paths", "failure_contract", "non_claims"})
REVIEWED_PATH_FIELDS = frozenset({"id", "from", "to", "kind", "mechanism", "adoption", "effect_class", "permission_source", "controls"})


def validate(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["root must be an object"]
    if set(document) - REVIEWED_ROOT_FIELDS:
        errors.append("unreviewed root fields: V1 cannot silently add runtime policy")
    if document.get("schema") != "VERA_AGENT_PROTOCOL_BOUNDARIES_V1":
        errors.append("schema mismatch")
    if document.get("logical_id") != "VERA_AGENT_PROTOCOL_BOUNDARIES":
        errors.append("logical identity differs from reviewed V1 owner")
    if document.get("scope") != EXPECTED_SCOPE:
        errors.append("scope differs from reviewed non-activating V1 limit")
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
        if set(path) - REVIEWED_PATH_FIELDS:
            errors.append(f"paths[{i}] includes unreviewed fields")
        pid = path.get("id")
        if not isinstance(pid, str) or not pid:
            errors.append(f"paths[{i}] has invalid id")
        elif pid in seen:
            errors.append(f"duplicate id {pid}")
        else:
            seen.add(pid)
        if isinstance(pid, str) and pid in EXPECTED_BINDINGS:
            for field, expected in zip(BINDING_FIELDS, EXPECTED_BINDINGS[pid]):
                if path.get(field) != expected:
                    errors.append(f"paths[{i}] {field} diverges from reviewed {pid} binding")
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
        if isinstance(pid, str) and pid in EXPECTED_CONTROLS:
            if controls != list(EXPECTED_CONTROLS[pid]):
                errors.append(f"paths[{i}] controls differ from reviewed {pid} V1 list")
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
        if failures != EXPECTED_FAILURE_CONTRACT:
            errors.append("failure policy changed from reviewed V1 contract")
        if failures.get("mutation_timeout") != "UNKNOWN_EFFECT_RECONCILE_BEFORE_RETRY":
            errors.append("ambiguous mutations must be reconciled before retry")
        if failures.get("unavailable_requested_route") != "FAIL_CLOSED_DO_NOT_SILENTLY_SWITCH_TRANSPORT":
            errors.append("route failure must not silently fallback")
        if failures.get("transport_loss") != "DROP_EXPIRED_LEASES_REVOKE_INPUT_RECHECK_HOST_IDENTITY":
            errors.append("transport loss must revoke input and recheck host")
    non_claims = document.get("non_claims")
    if not isinstance(non_claims, list) or "NOT_AN_AUTHORIZATION_TOKEN" not in non_claims:
        errors.append("advisory cannot act as authorization token")
    if non_claims != list(EXPECTED_NON_CLAIMS):
        errors.append("non-activation disclaimers differ from reviewed V1")
    return errors


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    document: dict[str, Any] = {}
    for key, value in pairs:
        if key in document:
            raise ValueError("duplicate JSON object key")
        document[key] = value
    return document


def main() -> int:
    if len(sys.argv) > 2:
        print(json.dumps({"status": "BLOCK", "findings": ["expected zero or one JSON file argument"]}))
        return 2
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parents[1] / "protocol" / "VERA_AGENT_PROTOCOL_BOUNDARIES_V1.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_unique_json_object)
    except (OSError, ValueError):
        print(json.dumps({"status": "BLOCK", "findings": ["unreadable or invalid JSON document"]}))
        return 1
    errors = validate(document)
    if errors:
        print(json.dumps({"status": "BLOCK", "findings": errors}, indent=2))
        return 1
    print(json.dumps({"status": "PASS", "checked_paths": len(document["paths"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
