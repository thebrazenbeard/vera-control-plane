from tools.validate_vcp_supabase_provider_composition import (
    LiveProviderQualificationRequired,
    require_live_provider_parity,
    validate,
)


def assert_live_qualification_rejected(report: dict) -> None:
    try:
        require_live_provider_parity(report)
    except LiveProviderQualificationRequired:
        return
    raise AssertionError("frozen baseline falsely promoted live provider parity")


def test_vcp_supabase_provider_composition_is_exact() -> None:
    report = validate()
    assert report["status"] == "HISTORICAL_BASELINE_ONLY"
    assert report["historical_source_byte_check"] == "PASS"
    assert report["historical_inventory_observed_date"] == "2026-09-22"
    assert report["historical_provider_migrations"] == 6
    assert report["pending_source_migrations"] == 0
    assert report["historical_last_provider_version"] == "20260921200623"
    assert report["live_provider_queried"] is False
    assert report["live_full_ledger_parity"] == "UNVERIFIED_NOT_QUERIED"
    assert report["live_sql_bytes_attested"] is False
    assert report["provider_apply_or_install_authorized"] is False


def test_frozen_six_version_match_cannot_promote_live_eight_row_ledger() -> None:
    report = validate()
    # This is the exact class of the 2026-11-03 read-only provider result:
    # six historical VCP versions and two later Masamune-owned versions.
    observed_eight_versions = [
        "20260912170153", "20260912170345", "20260912170408",
        "20260919223652", "20260921192624", "20260921200623",
        "20260930205855", "20260930210018",
    ]
    assert len(observed_eight_versions) == 8
    assert report["historical_provider_migrations"] == 6
    assert report["live_full_ledger_parity"] != "PASS"
    assert_live_qualification_rejected(report)


def test_version_only_byte_substitution_is_not_live_attestation() -> None:
    # Versions alone can remain equal while SQL bodies differ; the historical
    # local-byte checks cannot inspect today's provider SQL bodies.
    report = validate()
    tampered_live_sql = {
        "version": "20260912170153",
        "body": "SELECT 'different live SQL with unchanged version';",
    }
    assert tampered_live_sql["version"] == "20260912170153"
    assert report["live_sql_bytes_attested"] is False
    assert_live_qualification_rejected(report)
