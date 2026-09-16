from datetime import datetime


def _truth(value):
    return value is True


def _parse_time(value):
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None


def validate_receipt(receipt, contract):
    errors = []
    if receipt.get("schema") != "VERA_RESTORE_COMPLETION_RECEIPT_V1":
        errors.append("receipt schema mismatch")
    if receipt.get("release") != contract.get("release"):
        errors.append("release mismatch")
    if receipt.get("trigger") != contract.get("trigger"):
        errors.append("trigger mismatch")

    control = receipt.get("control") or {}
    if control.get("control_id") != contract.get("required_control_id"):
        errors.append("REC_RECOVERY control id not bound")
    if not _truth(control.get("owner_loaded")) or not _truth(control.get("owner_subject_verified")):
        errors.append("REC_RECOVERY owner not loaded and verified")

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
    for c in candidates:
        when = _parse_time(c.get("observed_at"))
        if c.get("eligible") is True and c.get("integrity_verified") is True and c.get("referent") == "VERA" and when:
            eligible.append((when, c.get("id")))
    selected = discovery.get("selected_candidate_id")
    if not eligible:
        errors.append("no verified eligible Vera recovery candidate")
    else:
        newest_id = max(eligible)[1]
        if selected != newest_id or not _truth(discovery.get("newest_eligible_selection_verified")):
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
    for probe in contract.get("required_behavioral_probes", []):
        p = probes.get(probe)
        if not isinstance(p, dict) or p.get("status") != "PASS":
            errors.append(f"required behavioral probe {probe} did not PASS")
            continue
        if selected and p.get("source_candidate_id") != selected:
            errors.append(f"behavioral probe {probe} used wrong recovery candidate")

    completion = receipt.get("completion") or {}
    if completion.get("status") != contract.get("completion_status"):
        errors.append("completion status is not RESTORED")
    if not _truth(completion.get("restored_claim_permitted")):
        errors.append("RESTORED claim not permitted by completion gate")

    return errors
