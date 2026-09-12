from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_SUPABASE_CONTROL_PLANE_PROVIDER_BINDING_V1.json"
SOURCE_COMMIT = "719658fb75d783b34fb884ae707a6bee6b2c63b6"
SOURCE_PATH = "providers/vera_control_plane/migrations/20260912193000_create_predecessor_import_staging.sql"
SOURCE_BLOB = "0f486c7af34b3346380e3249d49d551499388d44"
SOURCE_SHA256 = "daf6f99e26f828cfc2a583bb498564112dfacec4c78d362617594360e3e81351"
DEPLOYMENT_PATH = "supabase/migrations/20260912193000_create_predecessor_import_staging.sql"


def load_binding() -> dict:
    return json.loads(BINDING.read_text(encoding="utf-8"))


def test_predecessor_import_source_is_exactly_bound() -> None:
    source = load_binding()["predecessor_import_schema_source"]
    assert source["repository"] == "thebrazenbeard/vera"
    assert source["commit"] == SOURCE_COMMIT
    assert source["path"] == SOURCE_PATH
    assert source["git_blob"] == SOURCE_BLOB
    assert source["sha256"] == SOURCE_SHA256
    assert source["deployment_copy_path"] == DEPLOYMENT_PATH

def test_deployment_copy_is_byte_identical() -> None:
    deployment = ROOT / DEPLOYMENT_PATH
    assert hashlib.sha256(deployment.read_bytes()).hexdigest() == SOURCE_SHA256


def test_predecessor_import_migration_is_pending_not_installed() -> None:
    binding = load_binding()
    installed = {entry["version"] for entry in binding["installed_baseline_migrations"]}
    pending = {entry["version"]: entry for entry in binding["pending_source_migrations"]}
    assert "20260912193000" not in installed
    assert pending["20260912193000"]["status"] == "SOURCE_BOUND_NOT_APPLIED"
    assert binding["effect_status"]["predecessor_import_staging_migration"] == "SOURCE_BOUND_NOT_APPLIED"


def test_import_copy_does_not_admit_or_migrate_payload() -> None:
    source = load_binding()["predecessor_import_schema_source"]
    assert source["semantic_owner"] == "thebrazenbeard/vera"
    assert source["custody_semantics"] == "BYTE_IDENTICAL_DEPLOYMENT_COPY_NOT_SEMANTIC_REAUTHORING"
    assert source["payload_migration_authority"] == "NOT_GRANTED_BY_SOURCE_BINDING"


def test_predecessor_cargo_snapshot_is_exactly_bound() -> None:
    snapshot = load_binding()["predecessor_cargo_snapshot"]
    assert snapshot["repository"] == "thebrazenbeard/vera"
    assert snapshot["commit"] == "d56666c558da24587dc3d11f39b0f177971cb5e3"
    assert snapshot["path"] == "architecture/VERA_PREDECESSOR_MIGRATION_CARGO_SNAPSHOT_20260912.json"
    assert snapshot["git_blob"] == "39311906abf8536a0ddb0baff21d996e28e9255f"
    assert snapshot["sha256"] == "b098d08b81187b7063836ff789fafff1c9cdcd96cbc7cbf9cd6e1f43a45a6647"
    assert snapshot["total_rows"] == 294
    assert snapshot["payload_in_repository"] is False
    assert snapshot["migration_authority"] == "NOT_GRANTED_BY_SNAPSHOT"
