from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FRONTIER_SCHEMA = "SD1_CAUSAL_LEDGER_FRONTIER_V1"
LEDGER_SCHEMA = "SD1_CAUSAL_ATTEMPT_LEDGER_V1"
FROZEN_PLAN_SHA256 = "526f35438c2521d40e7a2bfa145da363e0c5063d2affef27131f9370e08564ba"
LEDGER_GENESIS_CHAIN_HEAD = hashlib.sha256(
    b"SD1_CAUSAL_ATTEMPT_LEDGER_V1_GENESIS"
).hexdigest()
DEFAULT_STORE_ID = (
    "github:thebrazenbeard/vera-control-plane:state/sd1-causal-witness-v1"
)
DEFAULT_BRANCH = "state/sd1-causal-witness-v1"
DEFAULT_PREFIX = "state/sd1-causal-witness/frontiers/"
DEFAULT_GENESIS_COMMIT = "cecf8d2ec6cf031c714e9f6c0972c4882101c16f"
_FRONTIER_PATH_RE = re.compile(r"^(?P<generation>[0-9]{6})-(?P<suffix>[^/]+)\.json$")


class WitnessError(RuntimeError):
    pass


class WitnessIntegrityError(WitnessError):
    pass


class WitnessConflict(WitnessError):
    pass


class WitnessNotQualified(WitnessError):
    pass


@dataclass(frozen=True)
class ObservedFrontier:
    branch_head: str
    path: str
    frontier: dict[str, Any]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def frontier_digest(frontier: dict[str, Any]) -> str:
    payload = {key: value for key, value in frontier.items() if key != "frontier_digest"}
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value)
    )


def validate_frontier(
    frontier: dict[str, Any],
    *,
    expected_store_id: str,
    expected_plan_sha256: str = FROZEN_PLAN_SHA256,
) -> None:
    if not isinstance(frontier, dict):
        raise WitnessIntegrityError("frontier must be an object")
    required = {
        "schema",
        "witness_store_id",
        "plan_sha256",
        "ledger_schema",
        "generation",
        "record_count",
        "chain_head",
        "last_slot_id",
        "last_record_digest",
        "predecessor_frontier_digest",
        "frontier_digest",
    }
    if set(frontier) != required:
        raise WitnessIntegrityError("frontier fields do not match exact schema")
    if frontier["schema"] != FRONTIER_SCHEMA:
        raise WitnessIntegrityError("frontier schema mismatch")
    if frontier["witness_store_id"] != expected_store_id:
        raise WitnessIntegrityError("witness store id mismatch")
    if frontier["plan_sha256"] != expected_plan_sha256:
        raise WitnessIntegrityError("frozen plan digest mismatch")
    if frontier["ledger_schema"] != LEDGER_SCHEMA:
        raise WitnessIntegrityError("ledger schema mismatch")

    generation = frontier["generation"]
    count = frontier["record_count"]
    if type(generation) is not int or generation < 0:
        raise WitnessIntegrityError("frontier generation must be a nonnegative integer")
    if type(count) is not int or count < 0:
        raise WitnessIntegrityError("frontier record_count must be a nonnegative integer")
    if generation != count:
        raise WitnessIntegrityError("frontier generation must equal record_count")
    if not _is_sha256(frontier["chain_head"]):
        raise WitnessIntegrityError("frontier chain_head must be SHA-256")

    if generation == 0:
        if frontier["chain_head"] != LEDGER_GENESIS_CHAIN_HEAD:
            raise WitnessIntegrityError("genesis frontier chain head mismatch")
        if any(
            frontier[name] is not None
            for name in (
                "last_slot_id",
                "last_record_digest",
                "predecessor_frontier_digest",
            )
        ):
            raise WitnessIntegrityError("genesis frontier must not name predecessor/record")
    else:
        if not isinstance(frontier["last_slot_id"], str) or not frontier["last_slot_id"]:
            raise WitnessIntegrityError("non-genesis frontier requires last_slot_id")
        if not _is_sha256(frontier["last_record_digest"]):
            raise WitnessIntegrityError("non-genesis frontier requires last_record_digest")
        if not _is_sha256(frontier["predecessor_frontier_digest"]):
            raise WitnessIntegrityError(
                "non-genesis frontier requires predecessor_frontier_digest"
            )

    if not _is_sha256(frontier["frontier_digest"]):
        raise WitnessIntegrityError("frontier_digest must be SHA-256")
    if frontier_digest(frontier) != frontier["frontier_digest"]:
        raise WitnessIntegrityError("frontier canonical digest mismatch")


def require_qualified_binding(contract: dict[str, Any]) -> dict[str, Any]:
    try:
        storage = contract["storage_requirements"]
        binding = contract["provider_binding"]
    except (KeyError, TypeError) as exc:
        raise WitnessNotQualified("witness contract is missing binding state") from exc
    if storage.get("independently_durable_from_ledger") is not True:
        raise WitnessNotQualified("witness durability requirement is absent")
    if (
        storage.get("enforceable_no_rewind_or_independent_secondary_anchor_required")
        is not True
    ):
        raise WitnessNotQualified("anti-rewind qualification requirement is absent")
    if binding.get("monotonicity_qualification") != "PASS":
        raise WitnessNotQualified(
            "bound witness lacks independently verified monotonicity"
        )
    return binding


def build_successor_frontier(
    current: dict[str, Any],
    ledger: dict[str, Any],
    *,
    expected_store_id: str,
) -> dict[str, Any]:
    validate_frontier(current, expected_store_id=expected_store_id)
    if not isinstance(ledger, dict) or ledger.get("schema") != LEDGER_SCHEMA:
        raise WitnessIntegrityError("candidate ledger schema mismatch")
    order = ledger.get("record_order")
    records = ledger.get("records")
    chain_head = ledger.get("chain_head")
    if not isinstance(order, list) or not isinstance(records, dict):
        raise WitnessIntegrityError("candidate ledger structure is invalid")
    if len(order) != current["record_count"] + 1:
        raise WitnessIntegrityError(
            "candidate ledger must advance witness by exactly one record"
        )
    if set(order) != set(records) or len(order) != len(set(order)):
        raise WitnessIntegrityError("candidate ledger record order diverges")
    if not _is_sha256(chain_head):
        raise WitnessIntegrityError("candidate ledger chain head is invalid")
    last_slot = order[-1]
    last_record = records.get(last_slot)
    if not isinstance(last_record, dict):
        raise WitnessIntegrityError("candidate ledger final record is missing")
    last_digest = last_record.get("record_digest")
    if not _is_sha256(last_digest) or last_digest != chain_head:
        raise WitnessIntegrityError(
            "candidate ledger final record digest must equal chain head"
        )

    successor = {
        "schema": FRONTIER_SCHEMA,
        "witness_store_id": expected_store_id,
        "plan_sha256": FROZEN_PLAN_SHA256,
        "ledger_schema": LEDGER_SCHEMA,
        "generation": current["generation"] + 1,
        "record_count": len(order),
        "chain_head": chain_head,
        "last_slot_id": last_slot,
        "last_record_digest": last_digest,
        "predecessor_frontier_digest": current["frontier_digest"],
    }
    successor["frontier_digest"] = frontier_digest(successor)
    validate_frontier(successor, expected_store_id=expected_store_id)
    return successor


class GitFrontierTransport:
    """Git CAS transport only.

    This class proves freshness/CAS mechanics. It is NOT sufficient causal witness
    qualification by itself. Call require_qualified_binding() on the separately
    reviewed witness contract before causal collection.
    """

    def __init__(
        self,
        repo_root: str | Path,
        *,
        remote: str = "origin",
        branch: str = DEFAULT_BRANCH,
        prefix: str = DEFAULT_PREFIX,
        store_id: str = DEFAULT_STORE_ID,
        genesis_commit: str = DEFAULT_GENESIS_COMMIT,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.remote = remote
        self.branch = branch
        self.prefix = prefix
        self.store_id = store_id
        self.genesis_commit = genesis_commit

    def _git(
        self,
        *args: str,
        input_bytes: bytes | None = None,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[bytes]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        proc = subprocess.run(
            ["git", *args],
            cwd=self.repo_root,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=merged_env,
            check=False,
        )
        if check and proc.returncode != 0:
            detail = proc.stderr.decode("utf-8", errors="replace").strip()
            raise WitnessError(f"git {' '.join(args)} failed: {detail}")
        return proc

    def _git_text(
        self,
        *args: str,
        input_bytes: bytes | None = None,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> str:
        return self._git(
            *args,
            input_bytes=input_bytes,
            env=env,
            check=check,
        ).stdout.decode("utf-8").strip()

    def fresh_read(self) -> ObservedFrontier:
        self._git(
            "fetch",
            "--quiet",
            "--no-tags",
            self.remote,
            f"refs/heads/{self.branch}",
        )
        head = self._git_text("rev-parse", "FETCH_HEAD")
        ancestor = self._git(
            "merge-base",
            "--is-ancestor",
            self.genesis_commit,
            head,
            check=False,
        )
        if ancestor.returncode != 0:
            raise WitnessIntegrityError(
                "witness branch head does not descend from bound genesis"
            )

        names = self._git_text("ls-tree", "-r", "--name-only", head, "--", self.prefix)
        paths = [name for name in names.splitlines() if name]
        by_generation: dict[int, str] = {}
        for path in paths:
            if not path.startswith(self.prefix):
                continue
            basename = path[len(self.prefix):]
            match = _FRONTIER_PATH_RE.match(basename)
            if not match:
                continue
            generation = int(match.group("generation"))
            if generation in by_generation:
                raise WitnessIntegrityError("duplicate frontier generation")
            by_generation[generation] = path
        if not by_generation or 0 not in by_generation:
            raise WitnessIntegrityError("witness frontier genesis is missing")
        latest = max(by_generation)
        if set(by_generation) != set(range(latest + 1)):
            raise WitnessIntegrityError("witness frontier generation gap")

        previous_digest: str | None = None
        latest_frontier: dict[str, Any] | None = None
        for generation in range(latest + 1):
            path = by_generation[generation]
            raw = self._git("show", f"{head}:{path}").stdout
            try:
                frontier = json.loads(raw.decode("utf-8"))
            except Exception as exc:
                raise WitnessIntegrityError(
                    f"witness frontier generation {generation} is not valid JSON"
                ) from exc
            validate_frontier(frontier, expected_store_id=self.store_id)
            if frontier["generation"] != generation:
                raise WitnessIntegrityError(
                    "frontier path generation disagrees with content"
                )
            basename = path[len(self.prefix):]
            suffix = _FRONTIER_PATH_RE.match(basename).group("suffix")
            if generation == 0:
                if suffix != "genesis":
                    raise WitnessIntegrityError("generation-zero frontier must be genesis")
                if frontier["predecessor_frontier_digest"] is not None:
                    raise WitnessIntegrityError(
                        "genesis frontier may not name a predecessor"
                    )
            else:
                if suffix != frontier["frontier_digest"][:16]:
                    raise WitnessIntegrityError(
                        "frontier path digest suffix disagrees with content"
                    )
                if frontier["predecessor_frontier_digest"] != previous_digest:
                    raise WitnessIntegrityError(
                        "frontier predecessor digest chain mismatch"
                    )
            previous_digest = frontier["frontier_digest"]
            latest_frontier = frontier

        assert latest_frontier is not None
        return ObservedFrontier(head, by_generation[latest], latest_frontier)

    def compare_and_swap(
        self,
        *,
        expected_head: str,
        expected_frontier_digest: str,
        successor: dict[str, Any],
    ) -> ObservedFrontier:
        current = self.fresh_read()
        if current.branch_head != expected_head:
            raise WitnessConflict("witness branch head changed before CAS")
        if current.frontier["frontier_digest"] != expected_frontier_digest:
            raise WitnessConflict("witness frontier changed before CAS")

        validate_frontier(successor, expected_store_id=self.store_id)
        if successor["generation"] != current.frontier["generation"] + 1:
            raise WitnessIntegrityError("successor generation must advance exactly once")
        if successor["record_count"] != current.frontier["record_count"] + 1:
            raise WitnessIntegrityError("successor record count must advance exactly once")
        if (
            successor["predecessor_frontier_digest"]
            != current.frontier["frontier_digest"]
        ):
            raise WitnessIntegrityError("successor predecessor frontier mismatch")

        path = (
            f"{self.prefix}{successor['generation']:06d}-"
            f"{successor['frontier_digest'][:16]}.json"
        )
        payload = json.dumps(successor, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        blob = self._git_text("hash-object", "-w", "--stdin", input_bytes=payload)

        with tempfile.TemporaryDirectory() as td:
            index = str(Path(td) / "index")
            env = {"GIT_INDEX_FILE": index}
            self._git("read-tree", expected_head, env=env)
            self._git(
                "update-index",
                "--add",
                "--cacheinfo",
                "100644",
                blob,
                path,
                env=env,
            )
            tree = self._git_text("write-tree", env=env)
            commit = self._git_text(
                "commit-tree",
                tree,
                "-p",
                expected_head,
                "-m",
                f"state: advance SD1 causal witness generation {successor['generation']}",
            )

        push = self._git(
            "push",
            "--porcelain",
            self.remote,
            f"{commit}:refs/heads/{self.branch}",
            check=False,
        )
        if push.returncode != 0:
            # Reconcile instead of force/retrying the same mutation blindly.
            observed = self.fresh_read()
            if (
                observed.branch_head == commit
                and observed.frontier["frontier_digest"]
                == successor["frontier_digest"]
            ):
                return observed
            raise WitnessConflict(
                "witness CAS failed or raced; fresh state differs from proposed successor"
            )

        observed = self.fresh_read()
        if observed.branch_head != commit:
            raise WitnessIntegrityError("post-CAS witness head readback mismatch")
        if observed.frontier != successor:
            raise WitnessIntegrityError("post-CAS witness frontier readback mismatch")
        return observed
