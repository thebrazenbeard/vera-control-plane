# SD1 Causal Secondary Anchor — Deployment and Readback V1

Status: SOURCE-ONLY RUNBOOK / NOT DEPLOYED / NO PROVIDER AUTHORITY

This runbook turns the source contract in
`protocol/SD1_CAUSAL_SECONDARY_ANCHOR_V1.json` into a future bounded
provider deployment procedure. It is deliberately separate from current
SD1 installation and does not authorize any provider effect.

## Problem being closed

The Git witness branch `state/sd1-causal-witness-v1` supports exact
non-force compare-and-swap from an observed head, but current GitHub
readback reports that branch as unprotected. Client-side non-force behavior
therefore cannot prove that an out-of-band actor could not rewind the branch
to an earlier valid frontier.

The secondary anchor exists to make the causal ledger monotonic for the
controller's threat model even if the Git audit mirror is rewound.

## Source dependencies

Before deployment, fresh-check all of the following exact source subjects:

- the current SD1 causal controller and its frozen 70-slot plan;
- CAUSAL-006 repair exact head and hostile verdict;
- CAUSAL-005 RED regression exact head;
- witness contract and Git transport exact heads;
- Provider Mutation Broker V1 design/implementation source, if used;
- exact Supabase deployment source/custody branch selected for the control-plane provider.

A source PASS on any one of these is not deployment authority.

## Proposed provider object

The provider implementation should expose exactly one versioned operation:

`sd1.causal.frontier.advance.v1`

The durable data model is an append-only frontier relation keyed by:

`(witness_id, generation)`

Each non-genesis row binds:

- generation and record_count;
- causal ledger chain head;
- last slot id and last record digest;
- predecessor frontier digest;
- canonical frontier digest;
- frozen plan SHA-256 and ledger schema;
- request id and canonical request digest;
- provider timestamp.

The broker/client does not receive generic INSERT, UPDATE, DELETE, arbitrary
SQL, arbitrary table, or arbitrary function access.

## Transaction behavior

Inside one provider transaction:

1. lock the exact `witness_id` frontier;
2. read the latest accepted generation;
3. require the request's expected generation and expected frontier digest to
   equal that exact latest row;
4. require successor generation = predecessor generation + 1;
5. require successor record_count = successor generation;
6. require successor predecessor digest = current frontier digest;
7. verify the successor frontier digest against canonical payload fields;
8. enforce request-id/canonical-digest idempotency;
9. INSERT exactly one successor frontier row;
10. INSERT/derive the provider mutation receipt atomically;
11. commit;
12. perform an independent bounded readback of latest frontier and receipt.

A stale expected frontier is `REJECTED_STALE`. A request-id reuse with a
different digest is `REQUEST_ID_COLLISION`. Divergence is `CONFLICT`.
Transport ambiguity is reconciled before any retry. A changed successor is
never retried under the same logical attempt.

## Permission model

The deployed broker credential should have only:

- EXECUTE on the exact versioned frontier-advance RPC;
- bounded read of latest frontier;
- bounded read of its mutation receipt.

It should have no direct INSERT/UPDATE/DELETE on the frontier relation.
`anon` and ordinary `authenticated` roles must have no access.

The provider owner/admin necessarily remains more privileged; full provider
administrative compromise is outside the controller threat model. The
security claim is narrower: the credential used by the causal controller
must not possess a rewind path.

## Genesis

Provider genesis must reproduce the already frozen causal witness genesis:

- plan SHA-256:
  `526f35438c2521d40e7a2bfa145da363e0c5063d2affef27131f9370e08564ba`
- ledger schema: `SD1_CAUSAL_ATTEMPT_LEDGER_V1`
- generation: `0`
- record_count: `0`
- chain head:
  `527ddd4d35e85dfcff56b8c209ba2a6b642c08a18a9d2ae704626e8c78bfe229`
- frontier digest:
  `7de55cc22b28539c1d4e6934b1790d99c70ecee55ded80d7b698bec61ee249a1`

The deployed row must be read back and recomputed; source text is not effect
evidence.

## Pre-deployment gate

Do not perform provider mutation unless all are true:

- Patrick has given exact authority for this provider generation and
  migration/RPC/grant effect;
- exact migration/RPC source is reviewed;
- rollback/recovery is defined;
- selected provider project is fresh-read and matches the intended
  generation;
- no colliding migration or object exists;
- credentials are not exposed to chat/source.

## Post-deployment qualification

After deployment, independently verify:

1. object definitions and exact function source/readback;
2. genesis row values and canonical digest;
3. broker-role direct INSERT/UPDATE/DELETE are denied;
4. anon/authenticated access is denied;
5. exact RPC succeeds for one synthetic non-causal probe namespace only;
6. stale expected generation is rejected with no state change;
7. same request/same digest is idempotent;
8. same request/different digest collides;
9. ambiguous transport is reconciled before retry;
10. no update/delete path can rewind an accepted frontier through the
    controller credential.

Only after those gates pass may the controller integration be reviewed as a
candidate CAUSAL-005 repair. Real 70-slot causal data collection remains a
separate subsequent gate.

## Claim ceiling

Until deployment and readback complete:

`PROVIDER_SCHEMA=NOT_INSTALLED`

`SECONDARY_ANCHOR=NOT_ACTIVE`

`MONOTONICITY=NOT_ESTABLISHED`

`CAUSAL_DATA_COLLECTION=HOLD`

`CONTROL_CAUSALITY=UNRESOLVED`
