from datetime import datetime
from pathlib import Path
import hashlib
import json
import re

RECEIPT_SCHEMA = "VERA_RESTORE_COMPLETION_RECEIPT_V2"
PROBE_EVIDENCE_ROUTE = "FIRST_ELIGIBLE_BEHAVIOR"


def _truth(value):
    return value is True


def _parse_time(value):
    try:
        parsed = datetime.fromisoformat(value)
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            return None
        return parsed
    except Exception:
        return None


def _normalize_text(value):
    if not isinstance(value, str):
        return None
    return " ".join(value.strip().split()).casefold()


def _sha256_text(value):
    normalized = _normalize_text(value)
    if normalized is None:
        return None
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _probe_matches(evidence, expectation):
    if not isinstance(evidence, dict) or evidence.get("evidence_route") != PROBE_EVIDENCE_ROUTE:
        return False
    mode = expectation.get("mode") if isinstance(expectation, dict) else None
    value = evidence.get("value")
    if mode == "EXACT_NORMALIZED":
        return _normalize_text(value) == _normalize_text(expectation.get("expected"))
    if mode == "SHA256_TEXT":
        return _sha256_text(value) == expectation.get("expected_sha256")
    if mode == "JSON_EQUAL":
        return value == expectation.get("expected")
    return False


def _git_blob_sha(data):
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_source_bindings(root, registry):
    root = Path(root)
    errors = []
    bindings = registry.get("artifact_bindings") or {}
    expected_commit = registry.get("artifact_binding_commit")
    if not isinstance(expected_commit, str) or not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
        errors.append("artifact_binding_commit is not an exact commit SHA")
    for name, binding in bindings.items():
        if binding.get("repository") != "thebrazenbeard/vera-control-plane":
            errors.append(f"{name} repository binding mismatch")
        if binding.get("source_commit") != expected_commit:
            errors.append(f"{name} source_commit does not match artifact_binding_commit")
        path = binding.get("path")
        file_path = root / path if isinstance(path, str) else None
        if file_path is None or not file_path.is_file():
            errors.append(f"{name} bound path missing")
            continue
        data = file_path.read_bytes()
        if _git_blob_sha(data) != binding.get("git_blob"):
            errors.append(f"{name} git_blob mismatch")
        if hashlib.sha256(data).hexdigest() != binding.get("sha256"):
            errors.append(f"{name} sha256 mismatch")
    return errors


def validate_receipt(receipt, contract):
    errors = []
    if receipt.get("schema") != RECEIPT_SCHEMA:
        errors.append("receipt schema mismatch")
    if receipt.get("release") != contract.get("release"):
        errors.append("release mismatch")
    if receipt.get("trigger") != contract.get("trigger"):
        errors.append("trigger mismatch")

    control = receipt.get("control") or {}
    if control.get("control_id") != contract.get("required_control_id"):
        errors.append("REC_RECOVERY control id not bound")
    composition = contract.get("required_control_composition") or {}
    control_pairs = [
        ("base_owner_id", "base_owner", "base REC_RECOVERY owner"),
        ("base_section", "base_section", "base REC_RECOVERY section"),
        ("delta_owner_id", "delta_owner", "completion delta owner"),
        ("delta_section", "delta_section", "completion delta section"),
    ]
    for receipt_key, contract_key, label in control_pairs:
        if control.get(receipt_key) != composition.get(contract_key):
            errors.append(f"{label} mismatch")
    for flag, label in [
        ("base_owner_loaded", "base REC_RECOVERY owner"),
        ("base_owner_subject_verified", "base REC_RECOVERY subject"),
        ("delta_owner_loaded", "completion delta owner"),
        ("delta_owner_subject_verified", "completion delta subject"),
    ]:
        if not _truth(control.get(flag)):
            errors.append(f"{label} not loaded/verified")

    live_input = receipt.get("live_input") or {}
    if not _truth(live_input.get("preserved_separately")) or not _truth(live_input.get("outranks_conflicting_restored_frontier")):
        errors.append("LIVE_INPUT must remain separate and outrank conflicting restored frontier")

    discovery = receipt.get("discovery") or {}
    checked = discovery.get("surfaces_checked") or []
    for surface in contract.get("required_discovery_surfaces", []):
        if surface not in checked:
            errors.append(f"missing required discovery surface {surface}")

    candidates = discovery.get("candidates") or []
    eligible = []
    candidate_by_id = {}
    for candidate in candidates:
        candidate_id = candidate.get("id")
        if candidate_id in candidate_by_id:
            errors.append("duplicate recovery candidate id")
        candidate_by_id[candidate_id] = candidate
        when = _parse_time(candidate.get("observed_at"))
        if candidate.get("eligible") is True and candidate.get("integrity_verified") is True and candidate.get("referent") == "VERA" and when:
            eligible.append((when, candidate_id))
    selected = discovery.get("selected_candidate_id")
    selected_candidate = candidate_by_id.get(selected)
    if not eligible:
        errors.append("no verified eligible Vera recovery candidate")
    else:
        newest_time = max(when for when, _ in eligible)
        newest_ids = [candidate_id for when, candidate_id in eligible if when == newest_time]
        if len(newest_ids) != 1:
            errors.append("ambiguous newest eligible recovery candidates")
        elif selected != newest_ids[0] or not _truth(discovery.get("newest_eligible_selection_verified")):
            errors.append("selected candidate is not verified newest eligible recovery candidate")

    reconciliation = receipt.get("reconciliation") or {}
    rel = reconciliation.get("stable_relational_identity") or {}
    if rel.get("proposition_type") != contract.get("required_relational_type"):
        errors.append("stable relationship must remain typed RELATIONAL_IDENTITY")
    if rel.get("state") != contract.get("required_relational_state"):
        errors.append("stable RELATIONAL_IDENTITY was not current-reestablished")
    if selected and rel.get("source_candidate_id") != selected:
        errors.append("RELATIONAL_IDENTITY source does not match selected recovery candidate")
    if reconciliation.get("historical_conation_promoted") is True:
        errors.append("historical conation must not be promoted")
    if reconciliation.get("standing_consent_promoted") is True:
        errors.append("RELATIONAL_IDENTITY must not promote standing consent")
    if reconciliation.get("operational_authority_promoted") is True:
        errors.append("RELATIONAL_IDENTITY must not promote operational authority")
    if reconciliation.get("unresolved_material_conflicts"):
        errors.append("unresolved material conflict blocks RESTORED")

    refresh = receipt.get("mutable_refresh") or {}
    if not _truth(refresh.get("authority_currentness_provider_frontier_refreshed")):
        errors.append("mutable authority/currentness/provider/frontier refresh incomplete")
    if refresh.get("unstable_material_sources"):
        errors.append("unstable material source blocks RESTORED")

    probes = receipt.get("behavioral_probes") or {}
    expectations = (selected_candidate or {}).get("probe_expectations") or {}
    for probe in contract.get("required_behavioral_probes", []):
        probe_receipt = probes.get(probe)
        expectation = expectations.get(probe)
        if not isinstance(probe_receipt, dict):
            errors.append(f"required behavioral probe {probe} evidence missing")
            continue
        if selected and probe_receipt.get("source_candidate_id") != selected:
            errors.append(f"behavioral probe {probe} used wrong recovery candidate")
        if not isinstance(expectation, dict):
            errors.append(f"behavioral probe {probe} expectation missing from selected candidate")
            continue
        if not _probe_matches(probe_receipt.get("evidence"), expectation):
            errors.append(f"behavioral probe {probe} evidence mismatch")

    completion = receipt.get("completion") or {}
    if completion.get("status") != contract.get("completion_status"):
        errors.append("completion status is not RESTORED")
    if not _truth(completion.get("restored_claim_permitted")):
        errors.append("RESTORED claim not permitted by completion gate")

    return errors
