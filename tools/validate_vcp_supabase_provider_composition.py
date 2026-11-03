from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUPABASE = ROOT / "supabase"
MIGRATIONS = SUPABASE / "migrations"
CUSTODY = SUPABASE / "provider-custody" / "fawkirqroyniueeqspif"
INVENTORY = CUSTODY / "VCP_PROVIDER_LEDGER_CUSTODY_V1.json"
COMPOSITION = SUPABASE / "composition" / "VCP_PROVIDER_COMPOSITION_V1.json"
PENDING = SUPABASE / "composition" / "PENDING_MIGRATIONS_V1.json"
REPORT_SCHEMA = "VCP_PROVIDER_COMPOSITION_REPORT_V2"


class LiveProviderQualificationRequired(ValueError):
    """The frozen source inventory is not current provider readback."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> dict[str, object]:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    composition = json.loads(COMPOSITION.read_text(encoding="utf-8"))
    pending = json.loads(PENDING.read_text(encoding="utf-8"))

    expected = {
        f'{item["version"]}_{item["name"]}.sql': item["provider_sha256"]
        for item in inventory["migrations"]
    }
    if len(expected) != inventory["migration_count"]:
        raise AssertionError("duplicate provider migration identity")
    if len(expected) != composition["baseline"]["provider_migration_count"]:
        raise AssertionError("composition migration count mismatch")

    declared = {item["filename"]: item for item in pending["pending"]}
    actual = {p.name for p in MIGRATIONS.glob("*.sql") if p.is_file()}
    allowed = set(expected) | set(declared)
    if actual != allowed:
        raise AssertionError(
            f"migration identity drift: missing={sorted(allowed-actual)} extra={sorted(actual-allowed)}"
        )

    for name, digest in expected.items():
        executable = MIGRATIONS / name
        custody = CUSTODY / "applied" / name
        if not custody.is_file():
            raise AssertionError(f"missing provider custody file: {name}")
        if sha256(custody) != digest:
            raise AssertionError(f"custody digest mismatch: {name}")
        if sha256(executable) != digest:
            raise AssertionError(f"executable digest mismatch: {name}")
        if executable.read_bytes() != custody.read_bytes():
            raise AssertionError(f"executable/custody byte mismatch: {name}")

    last = inventory["last_version"]
    for name, item in declared.items():
        version = name.split("_", 1)[0]
        if len(version) != 14 or not version.isdigit() or version <= last:
            raise AssertionError(f"invalid pending migration ordering: {name}")
        if not item.get("source_repository") or len(item.get("source_blob", "")) != 40:
            raise AssertionError(f"pending migration lacks exact source binding: {name}")

    return {
        "report_schema": REPORT_SCHEMA,
        "status": "HISTORICAL_BASELINE_ONLY",
        "historical_source_byte_check": "PASS",
        "historical_inventory_observed_date": inventory["observed_date"],
        "historical_provider_migrations": len(expected),
        "pending_source_migrations": len(declared),
        "historical_last_provider_version": last,
        "live_provider_queried": False,
        "live_full_ledger_parity": "UNVERIFIED_NOT_QUERIED",
        "live_sql_bytes_attested": False,
        "provider_apply_or_install_authorized": False,
        "legacy_v1_pass_compatible": False,
    }


def require_live_provider_parity(report: dict[str, object]) -> None:
    """Deliberately stop release promotion from this source-only validator.

    A separate host-bound operator must attest a fresh, exact stable provider
    identity; full current ledger including other owners; SQL-body custody;
    source/currentness, permissions, and approved effect scope. A supplied
    list of matching migration versions is not equivalent.
    """
    if report.get("status") == "HISTORICAL_BASELINE_ONLY":
        raise LiveProviderQualificationRequired(
            "frozen source-byte parity does not establish current provider parity"
        )
    raise LiveProviderQualificationRequired("this tool does not perform live provider qualification")


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
