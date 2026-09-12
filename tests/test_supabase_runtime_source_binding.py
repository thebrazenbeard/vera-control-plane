from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BINDING = ROOT / "governance" / "VERA_SUPABASE_CONTROL_PLANE_PROVIDER_BINDING_V1.json"
SOURCE_COMMIT = "50c155f9715183b48ddcb404a53bb16c148b323e"
SOURCE_PATH = "providers/vera_control_plane/migrations/20260912183000_initialize_runtime_planes.sql"
SOURCE_BLOB = "8ae7aa8e9c27389e0c7a744e3a31316b70fcdc59"
SOURCE_SHA256 = "780e42b93484cee074902277c78b4b3076a7ef0bdc90d95e778cfc7308dbf553"
DEPLOYMENT_PATH = "supabase/migrations/20260912183000_initialize_runtime_planes.sql"


def load_binding() -> dict:
    return json.loads(BINDING.read_text(encoding="utf-8"))


def test_runtime_schema_source_is_exactly_bound() -> None:
    source = load_binding()["runtime_state_schema_source"]
    assert source["repository"] == "thebrazenbeard/vera"
    assert source["commit"] == SOURCE_COMMIT
    assert source["path"] == SOURCE_PATH
    assert source["git_blob"] == SOURCE_BLOB
    assert source["sha256"] == SOURCE_SHA256
    assert source["deployment_copy_path"] == DEPLOYMENT_PATH


def test_deployment_copy_is_byte_identical() -> None:
    deployment = ROOT / DEPLOYMENT_PATH
    digest = hashlib.sha256(deployment.read_bytes()).hexdigest()
    assert digest == SOURCE_SHA256


def test_runtime_plane_migration_is_pending_not_installed() -> None:
    binding = load_binding()
    installed = {entry["version"] for entry in binding["installed_baseline_migrations"]}
    pending = {entry["version"] for entry in binding["pending_source_migrations"]}
    assert "20260912183000" not in installed
    assert "20260912183000" in pending
    assert binding["effect_status"]["runtime_plane_substrate_migration"] == "SOURCE_BOUND_NOT_APPLIED"


def test_copy_does_not_transfer_semantic_ownership() -> None:
    source = load_binding()["runtime_state_schema_source"]
    assert source["semantic_owner"] == "thebrazenbeard/vera"
    assert source["custody_semantics"] == "BYTE_IDENTICAL_DEPLOYMENT_COPY_NOT_SEMANTIC_REAUTHORING"
