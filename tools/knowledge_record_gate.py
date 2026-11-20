"""Fail-closed structural validation of synthetic Vera knowledge record claims.

This does not authenticate evidence, fetch sources, grant rights, or publish data.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA = "VERA_KNOWLEDGE_RECORD_V1"
MAX_INPUT_BYTES = 131072
FRESHNESS_HOURS = 24
FIELDS = frozenset({"schema", "record_id", "subject_id", "title", "claim", "domains", "owner_id", "owner_binding_ref", "visibility", "publication_target", "lifecycle", "claim_surface", "currentness", "valid_until", "evidence", "supersedes", "limitations"})
EVIDENCE_FIELDS = frozenset({"class", "source_ref", "revision", "observed_at"})
ENUMS = {
    "visibility": frozenset({"PUBLIC_SAFE", "RESTRICTED", "UNKNOWN"}),
    "publication_target": frozenset({"NONE", "PUBLIC_REPOSITORY", "PRIVATE_STORE"}),
    "lifecycle": frozenset({"DRAFT", "REVIEWED", "PUBLISHED", "SUPERSEDED", "RETIRED"}),
    "claim_surface": frozenset({"SOURCE", "RUNTIME", "PROVIDER", "HISTORICAL"}),
    "currentness": frozenset({"CURRENT", "HISTORICAL", "UNKNOWN"}),
}
CLASSES = frozenset({"DOC", "SOURCE_INSPECTION", "TEST", "REAL_PROBE", "PROVIDER_READBACK", "INFERENCE"})
CURRENT_EVIDENCE = {"SOURCE": "SOURCE_INSPECTION", "RUNTIME": "REAL_PROBE", "PROVIDER": "PROVIDER_READBACK"}
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
GIT_BLOB_LOCATOR = re.compile(r"https://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)/blob/(?P<sha>[0-9a-f]{40})/(?P<path>[A-Za-z0-9_./-]+)\Z")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")


def _enum(value: object, options: frozenset[str]) -> bool:
    return isinstance(value, str) and value in options


def _distinct_pairs(pairs: list[tuple[str, object]]) -> dict:
    output = {}
    for key, value in pairs:
        if key in output:
            raise ValueError("duplicate key")
        output[key] = value
    return output


def _nonfinite(value: str):
    raise ValueError("nonfinite number")


def _text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and len(value) <= 1024


def _dt(value: object) -> datetime | None:
    if not isinstance(value, str) or not TIMESTAMP.fullmatch(value):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_record(record: object, *, now: datetime) -> list[str]:
    """Check shape and declared proof class; PASS is not evidence authentication."""
    if now.tzinfo is None or now.utcoffset() != timedelta(0):
        raise ValueError("now must be UTC")
    if type(record) is not dict:
        return ["record.not_object"]
    fail: set[str] = set()
    if set(record) != FIELDS:
        fail.add("record.fields")
    if record.get("schema") != SCHEMA:
        fail.add("record.schema")
    for key in ("record_id", "subject_id", "title", "claim", "owner_id", "owner_binding_ref"):
        if not _text(record.get(key)):
            fail.add("record." + key)
    for key, allowed in ENUMS.items():
        if not _enum(record.get(key), allowed):
            fail.add("record.enum." + key)
    for key in ("domains", "supersedes", "limitations"):
        val = record.get(key)
        if type(val) is not list or len(val) > 100 or any(not _text(x) for x in val):
            fail.add("record.list." + key)
        elif len(val) != len(set(val)):
            fail.add("record.list_distinct." + key)
    if type(record.get("domains")) is list and not record["domains"]:
        fail.add("record.domains_empty")
    if type(record.get("supersedes")) is list and record.get("record_id") in record["supersedes"]:
        fail.add("record.self_supersession")
    observations: list[tuple[str, datetime]] = []
    evidence = record.get("evidence")
    if type(evidence) is not list or len(evidence) > 100:
        fail.add("evidence.list")
    else:
        for item in evidence:
            if type(item) is not dict or set(item) != EVIDENCE_FIELDS:
                fail.add("evidence.fields")
                continue
            typ = item.get("class")
            if not _enum(typ, CLASSES):
                fail.add("evidence.class")
            if not _text(item.get("source_ref")):
                fail.add("evidence.source_ref")
            rev = item.get("revision")
            if rev is not None and not _text(rev):
                fail.add("evidence.revision")
            observed = _dt(item.get("observed_at"))
            if observed is None:
                fail.add("evidence.observed_at")
            elif observed > now:
                fail.add("evidence.future")
            elif _enum(typ, CLASSES):
                observations.append((typ, observed))
            if typ == "SOURCE_INSPECTION" and not (isinstance(rev, str) and SHA40.fullmatch(rev)):
                fail.add("evidence.git_revision")
            if typ == "SOURCE_INSPECTION":
                locator = item.get("source_ref")
                match = GIT_BLOB_LOCATOR.fullmatch(locator) if isinstance(locator, str) else None
                if match is None:
                    fail.add("evidence.source_unpinned")
                else:
                    if match.group("sha") != rev:
                        fail.add("evidence.source_revision_mismatch")
                    if any(part in {"", ".", ".."} for part in match.group("path").split("/")):
                        fail.add("evidence.source_path_invalid")
                    subject = record.get("subject_id")
                    if (isinstance(subject, str) and subject.startswith("repo:")
                            and subject[5:].casefold() != (match.group("owner") + "/" + match.group("repo")).casefold()):
                        fail.add("evidence.source_repository_mismatch")
    if record.get("publication_target") == "PUBLIC_REPOSITORY":
        if record.get("visibility") != "PUBLIC_SAFE":
            fail.add("publication.restricted_or_unknown")
        if not _enum(record.get("lifecycle"), frozenset({"REVIEWED", "PUBLISHED"})):
            fail.add("publication.not_reviewed")
    if record.get("lifecycle") == "PUBLISHED" and record.get("publication_target") == "NONE":
        fail.add("publication.missing_target")
    status = record.get("currentness")
    until = _dt(record.get("valid_until")) if record.get("valid_until") is not None else None
    if record.get("valid_until") is not None and until is None:
        fail.add("currentness.invalid_until")
    if status == "CURRENT":
        surface = record.get("claim_surface")
        if not _enum(surface, frozenset(CURRENT_EVIDENCE)):
            fail.add("currentness.unsupported_surface")
        if until is None or until <= now:
            fail.add("currentness.expired_or_missing")
        needed = CURRENT_EVIDENCE.get(surface) if isinstance(surface, str) else None
        qualified = [when for typ, when in observations if typ == needed]
        if not qualified:
            fail.add("currentness.missing_qualified_evidence")
        elif max(qualified) < now - timedelta(hours=FRESHNESS_HOURS):
            fail.add("currentness.stale_evidence")
        if qualified and until is not None and until > max(qualified) + timedelta(hours=FRESHNESS_HOURS):
            fail.add("currentness.overlong_window")
        if _enum(record.get("lifecycle"), frozenset({"RETIRED", "SUPERSEDED"})):
            fail.add("currentness.retired_or_superseded")
    elif until is not None:
        fail.add("currentness.until_without_current")
    return sorted(fail)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Source-only Vera knowledge card shape gate")
    parser.add_argument("path", type=Path)
    parser.add_argument("--as-of", help="UTC YYYY-MM-DDTHH:MM:SSZ; defaults to current UTC")
    args = parser.parse_args(argv)
    now = _dt(args.as_of) if args.as_of else datetime.now(timezone.utc)
    if now is None:
        parser.error("--as-of requires UTC ISO second timestamp ending Z")
    try:
        with args.path.open("rb") as stream:
            raw = stream.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            raise ValueError("too long")
        content = json.loads(raw.decode("utf-8"), object_pairs_hook=_distinct_pairs, parse_constant=_nonfinite)
        errors = validate_record(content, now=now)
    except (OSError, ValueError, UnicodeError):
        errors = ["input.invalid_or_unavailable"]
    print(json.dumps({"valid": not errors, "errors": errors}, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
