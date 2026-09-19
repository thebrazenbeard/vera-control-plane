from __future__ import annotations

import json
from typing import Any

from tools.sd1_causal_frontier_witness import (
    FRONTIER_SCHEMA,
    FROZEN_PLAN_SHA256,
    LEDGER_GENESIS_CHAIN_HEAD,
    LEDGER_SCHEMA,
    validate_frontier,
)


class MemoryFrontierWitness:
    """Test-only monotonic witness.

    It models the exact controller interface without implying any production
    provider deployment or qualification.
    """

    monotonicity_qualified = True

    def __init__(self, store_id: str = "test:sd1-causal-frontier") -> None:
        self.store_id = store_id
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
        from tools.sd1_causal_frontier_witness import frontier_digest

        genesis["frontier_digest"] = frontier_digest(genesis)
        self._frontier = genesis

    def read_frontier(self) -> dict[str, Any]:
        return json.loads(json.dumps(self._frontier))

    def advance_frontier(
        self,
        *,
        expected_frontier_digest: str,
        successor: dict[str, Any],
    ) -> dict[str, Any]:
        current = self._frontier
        if expected_frontier_digest != current["frontier_digest"]:
            raise ValueError("synthetic witness CAS conflict")
        validate_frontier(successor, expected_store_id=self.store_id)
        if successor["generation"] != current["generation"] + 1:
            raise ValueError("synthetic witness generation jump")
        if successor["record_count"] != current["record_count"] + 1:
            raise ValueError("synthetic witness record-count jump")
        if successor["predecessor_frontier_digest"] != current["frontier_digest"]:
            raise ValueError("synthetic witness predecessor mismatch")
        self._frontier = json.loads(json.dumps(successor))
        return self.read_frontier()

    def force_set_for_hostile_test(self, frontier: dict[str, Any]) -> None:
        validate_frontier(frontier, expected_store_id=self.store_id)
        self._frontier = json.loads(json.dumps(frontier))
