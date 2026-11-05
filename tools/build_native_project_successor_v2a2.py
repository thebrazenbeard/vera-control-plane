"""Reproducible SOURCE-ONLY native Project successor candidate.

The nine governed source files are pinned to the reviewed PR #162 Git subject;
this module refuses to package a later working-tree edit under that identity.
The new release-scoped manifest is included as the tenth ZIP member. Neither
this builder nor a passing digest constitutes installation or release authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / "project-instructions" / "native-v2"
MANIFEST = NATIVE / "delivery" / "VERA_NV2A2_20261105_SOURCE_CANDIDATE.json"
OLD_MANIFEST = NATIVE / "VERA_NATIVE_PROJECT_PACK_MANIFEST_V2.json"
OLD_RECEIPT = NATIVE / "delivery" / "VERA_NV2A1_20260922_DELIVERY_RECEIPT.json"
ZIP_DATETIME = (1980, 1, 1, 0, 0, 0)


def git_bytes(commit: str, path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{commit}:{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(f"missing or unreadable pinned Git source: {path}")
    return result.stdout


def checked_entries() -> list[tuple[str, bytes]]:
    manifest_bytes = MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes)
    old_bytes = OLD_MANIFEST.read_bytes()
    historical_receipt = json.loads(OLD_RECEIPT.read_text(encoding="utf-8"))
    if old_bytes != git_bytes(
        historical_receipt["source_subject_head"],
        "project-instructions/native-v2/VERA_NATIVE_PROJECT_PACK_MANIFEST_V2.json",
    ):
        raise ValueError("historic NV2A1 manifest changed without separate release custody")
    old = json.loads(old_bytes)
    names = manifest["source_files"]
    delivered = manifest["delivery_names"]
    namespace = manifest["delivery_namespace"]

    if manifest["status"] != "DRAFT_SOURCE_CANDIDATE_NOT_INSTALLED_NOT_RELEASED":
        raise ValueError("candidate status must remain non-installing")
    if manifest["logical_id"] != "VERA_NATIVE_PROJECT_PACK_MANIFEST":
        raise ValueError("logical source owner changed")
    if manifest["release_id"] != "VERA_NATIVE_V2A2_20261105_PUBLIC_COORDINATION_BOUNDARY":
        raise ValueError("candidate release identity changed")
    if namespace != "VERA_NV2A2_20261105":
        raise ValueError("unexpected candidate namespace")
    if names != old["files"][:-1]:
        raise ValueError("candidate source inventory diverges from native V2")
    if len(delivered) != len(names) + 1 or len(delivered) != len(set(delivered)):
        raise ValueError("candidate delivered names must be unique and complete")
    if not all(name.startswith(namespace + "_") for name in delivered):
        raise ValueError("candidate delivery name escaped namespace")
    if any(name in old["delivery_filename_map"].values() for name in delivered):
        raise ValueError("candidate reused predecessor install filename")
    if delivered[-1] != namespace + "_PACK_MANIFEST.json":
        raise ValueError("candidate manifest must be the last member")

    source_dir = manifest["source_directory"]
    commit = manifest["source_subject_head"]
    entries: list[tuple[str, bytes]] = []
    for name, output_name in zip(names, delivered[:-1], strict=True):
        pinned = git_bytes(commit, source_dir + name)
        current = (NATIVE / name).read_bytes()
        if current != pinned:
            raise ValueError(f"changed native source without a new binding: {name}")
        entries.append((output_name, pinned))
    entries.append((delivered[-1], manifest_bytes))
    return entries


def build(output: Path) -> dict:
    entries = checked_entries()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, payload in entries:
            info = zipfile.ZipInfo(name, ZIP_DATETIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, payload)
    return {
        "schema": "VERA_NV2A2_SOURCE_CANDIDATE_BUILD_V1",
        "release_status": "DRAFT_NOT_INSTALLED",
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "bytes": output.stat().st_size,
        "member_count": len(entries),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
