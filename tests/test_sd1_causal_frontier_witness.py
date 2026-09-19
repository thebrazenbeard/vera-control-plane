from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

from tools.sd1_causal_frontier_witness import (
    FRONTIER_SCHEMA,
    FROZEN_PLAN_SHA256,
    GitFrontierTransport,
    LEDGER_GENESIS_CHAIN_HEAD,
    LEDGER_SCHEMA,
    WitnessConflict,
    WitnessIntegrityError,
    WitnessNotQualified,
    build_successor_frontier,
    frontier_digest,
    require_qualified_binding,
    validate_frontier,
)


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "protocol" / "SD1_CAUSAL_FRONTIER_WITNESS_V1.json"


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise AssertionError(
            f"git {' '.join(args)} failed: {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def write_genesis(work: Path, store_id: str, prefix: str) -> tuple[str, dict]:
    genesis = {
        "schema": FRONTIER_SCHEMA,
        "witness_store_id": store_id,
        "plan_sha256": FROZEN_PLAN_SHA256,
        "ledger_schema": LEDGER_SCHEMA,
        "generation": 0,
        "record_count": 0,
        "chain_head": LEDGER_GENESIS_CHAIN_HEAD,
        "last_slot_id": None,
        "last_record_digest": None,
        "predecessor_frontier_digest": None,
    }
    genesis["frontier_digest"] = frontier_digest(genesis)
    path = work / prefix / "000000-genesis.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(genesis, indent=2) + "\n", encoding="utf-8")
    git(work, "add", str(path.relative_to(work)))
    git(work, "commit", "-m", "genesis")
    return git(work, "rev-parse", "HEAD"), genesis


def synthetic_one_record_ledger(record_digest: str) -> dict:
    slot = "synthetic-slot-1"
    return {
        "schema": LEDGER_SCHEMA,
        "record_order": [slot],
        "records": {
            slot: {
                "slot_id": slot,
                "record_digest": record_digest,
            }
        },
        "chain_head": record_digest,
    }


def make_remote_fixture(td: str):
    root = Path(td)
    remote = root / "remote.git"
    work = root / "work"
    git(root, "init", "--bare", str(remote))
    git(root, "init", str(work))
    git(work, "config", "user.name", "Witness Test")
    git(work, "config", "user.email", "witness-test@example.invalid")
    git(work, "remote", "add", "origin", str(remote))

    store_id = "test:sd1-causal-witness"
    branch = "state/test-sd1-witness"
    prefix = "witness/frontiers"
    git(work, "checkout", "-b", branch)
    genesis_commit, genesis = write_genesis(work, store_id, prefix)
    git(work, "push", "-u", "origin", branch)

    transport = GitFrontierTransport(
        work,
        remote="origin",
        branch=branch,
        prefix=prefix + "/",
        store_id=store_id,
        genesis_commit=genesis_commit,
    )
    return remote, work, transport, genesis_commit, genesis


def test_current_bound_contract_fails_closed_as_unqualified():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    with pytest.raises(WitnessNotQualified):
        require_qualified_binding(contract)


def test_frontier_digest_detects_tamper():
    store_id = "test:sd1-causal-witness"
    frontier = {
        "schema": FRONTIER_SCHEMA,
        "witness_store_id": store_id,
        "plan_sha256": FROZEN_PLAN_SHA256,
        "ledger_schema": LEDGER_SCHEMA,
        "generation": 0,
        "record_count": 0,
        "chain_head": LEDGER_GENESIS_CHAIN_HEAD,
        "last_slot_id": None,
        "last_record_digest": None,
        "predecessor_frontier_digest": None,
    }
    frontier["frontier_digest"] = frontier_digest(frontier)
    validate_frontier(frontier, expected_store_id=store_id)
    frontier["record_count"] = 1
    with pytest.raises(WitnessIntegrityError):
        validate_frontier(frontier, expected_store_id=store_id)


def test_git_transport_reads_and_advances_exact_frontier_by_nonforce_cas():
    with tempfile.TemporaryDirectory() as td:
        _remote, _work, transport, genesis_commit, genesis = make_remote_fixture(td)
        observed = transport.fresh_read()
        assert observed.branch_head == genesis_commit
        assert observed.frontier == genesis

        record_digest = "a" * 64
        successor = build_successor_frontier(
            observed.frontier,
            synthetic_one_record_ledger(record_digest),
            expected_store_id=observed.frontier["witness_store_id"],
        )
        advanced = transport.compare_and_swap(
            expected_head=observed.branch_head,
            expected_frontier_digest=observed.frontier["frontier_digest"],
            successor=successor,
        )
        assert advanced.frontier == successor
        assert advanced.frontier["generation"] == 1
        assert advanced.frontier["record_count"] == 1
        assert advanced.frontier["chain_head"] == record_digest
        assert advanced.branch_head != genesis_commit

        with pytest.raises(WitnessConflict):
            transport.compare_and_swap(
                expected_head=genesis_commit,
                expected_frontier_digest=genesis["frontier_digest"],
                successor=successor,
            )


def test_git_transport_detects_generation_gaps():
    with tempfile.TemporaryDirectory() as td:
        _remote, work, transport, _genesis_commit, _genesis = make_remote_fixture(td)
        bogus = {
            "schema": FRONTIER_SCHEMA,
            "witness_store_id": transport.store_id,
            "plan_sha256": FROZEN_PLAN_SHA256,
            "ledger_schema": LEDGER_SCHEMA,
            "generation": 2,
            "record_count": 2,
            "chain_head": "b" * 64,
            "last_slot_id": "slot-2",
            "last_record_digest": "b" * 64,
            "predecessor_frontier_digest": "c" * 64,
        }
        bogus["frontier_digest"] = frontier_digest(bogus)
        path = work / transport.prefix / (
            f"000002-{bogus['frontier_digest'][:16]}.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(bogus, indent=2) + "\n", encoding="utf-8")
        git(work, "add", str(path.relative_to(work)))
        git(work, "commit", "-m", "skip generation one")
        git(work, "push", "origin", transport.branch)

        with pytest.raises(WitnessIntegrityError):
            transport.fresh_read()


def test_unprotected_remote_can_be_force_rewound_so_transport_alone_is_not_monotonic():
    with tempfile.TemporaryDirectory() as td:
        _remote, work, transport, genesis_commit, _genesis = make_remote_fixture(td)
        observed = transport.fresh_read()
        successor = build_successor_frontier(
            observed.frontier,
            synthetic_one_record_ledger("d" * 64),
            expected_store_id=transport.store_id,
        )
        advanced = transport.compare_and_swap(
            expected_head=observed.branch_head,
            expected_frontier_digest=observed.frontier["frontier_digest"],
            successor=successor,
        )
        assert advanced.frontier["generation"] == 1

        # This is the exact external capability the current production binding
        # cannot rule out because the branch is unprotected.
        git(
            work,
            "push",
            "--force",
            "origin",
            f"{genesis_commit}:refs/heads/{transport.branch}",
        )
        rewound = transport.fresh_read()
        assert rewound.branch_head == genesis_commit
        assert rewound.frontier["generation"] == 0


def test_unprotected_git_transport_does_not_itself_claim_monotonic_qualification():
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["provider_binding"]["branch_protected"] is False
    assert contract["provider_binding"]["monotonicity_qualification"] == "FAIL"
    assert (
        contract["provider_binding"]["monotonicity_mechanism"]
        == "UNQUALIFIED_CLIENT_SIDE_NON_FORCE_ONLY"
    )
