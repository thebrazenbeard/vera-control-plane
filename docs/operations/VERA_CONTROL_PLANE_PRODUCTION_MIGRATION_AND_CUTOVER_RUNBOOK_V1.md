# Vera Control Plane Production Migration and Cutover Runbook V1

Status: `PREPARED / NO_PROVIDER_MUTATION`
Target provider: `fawkirqroyniueeqspif`
Predecessor provider: `klmbpaigzeguvnpccqzz`
Deployment source: `thebrazenbeard/vera-control-plane`
Semantic source: `thebrazenbeard/vera`

## Purpose

This runbook begins only after the predecessor-import and provider-gate source work has a reviewed exact Vera source head. It converts that reviewed source into a controlled production migration without collapsing source, installation, admission, current route, or qualification into one event.

The goal is to land the smallest trustworthy provider cut: install the reviewed schema, stage the frozen predecessor payload as evidence, verify exact readback, and stop before semantic admission or runtime cutover unless Patrick separately authorizes those effects.

## Non-negotiable invariants

- `PROVIDER != CONTROL AUTHORITY`.
- `PERSISTENCE != ADMISSION`.
- `SOURCE != INSTALLATION`.
- `INSTALLATION != CURRENT_ROUTE`.
- `CURRENT_ROUTE != BEHAVIORAL_QUALIFICATION`.
- A reviewed PR, migration file, receipt, or passing test does not authorize a protected production effect.
- Never delete, retire, truncate, or make `klmbpaigzeguvnpccqzz` unavailable during this runbook.
- Never place private predecessor payload in Git, PR text, Bus messages, or public logs.
- Every shared mutation uses an exact target and fresh preflight/readback; ambiguous effects stop for reconciliation.

## Gate A — reviewed source cut

Do not refresh deployment bytes until all of the following are true:

1. The final predecessor-import/provider-gate source head in `thebrazenbeard/vera` is exact and immutable for this release cut.
2. OV hostile review has returned PASS for that exact head, or Patrick has explicitly accepted a named residual risk.
3. The two pending provider migrations are identified by exact source commit, path, Git blob, and SHA-256.
4. The frozen predecessor cargo snapshot remains bound to the same source cut or has been deliberately superseded with an exact replacement receipt.
5. Any parallel Work Chat result has been reconciled against the actual Git head; chat prose alone is not release evidence.

If any item is unresolved, status is `WAITING_REVIEWED_SOURCE_HEAD` and no deployment-copy refresh occurs.

## Gate B — refresh PR #20 deployment custody

After Gate A passes:

1. Refresh `work/supabase-control-plane-binding-20260912` and confirm no unexpected target-path changes.
2. Replace only the deployment copies that changed in the reviewed Vera source cut.
3. Update `governance/VERA_SUPABASE_CONTROL_PLANE_PROVIDER_BINDING_V1.json` with the exact reviewed source commit/blob/SHA-256 values.
4. Keep `payload_migration_authority` and equivalent protected-effect fields explicitly non-granting.
5. Run all control-plane binding tests and byte-identity checks.
6. Read back PR #20 head/base/draft/mergeability and record the exact release candidate head.

A GREEN PR #20 establishes `SOURCE_BOUND_NOT_APPLIED`, not installation.

## Gate C — protected production authority

Before any mutation of `fawkirqroyniueeqspif`, obtain Patrick's exact authority for the specific phase being executed.

The minimal installation/staging authority should name:

- target provider `fawkirqroyniueeqspif`;
- the exact reviewed PR #20/source head;
- permission to apply the pending runtime-plane and predecessor-staging migrations;
- permission to transfer only the classified frozen predecessor payload into the locked evidence staging plane;
- explicit exclusion of semantic admission, runtime-route cutover, deletion, retirement, and merge unless separately authorized.

Without that authority, stop at `SOURCE_READY / WAITING_PRODUCTION_AUTHORITY`.

## Phase 1 — read-only production preflight

Immediately before mutation, refresh both providers.

For `fawkirqroyniueeqspif`, verify:

- project is healthy and reachable;
- installed migration history still matches the known hardened baseline;
- pending migration versions are not already applied under an unobserved route;
- expected schema/role names do not conflict with unexpected owners or memberships;
- no unexpected runtime/predecessor application tables have appeared;
- security/advisor findings are captured before the cut.

For `klmbpaigzeguvnpccqzz`, re-read the frozen source-cut counts/digests and confirm the migration corpus has not drifted from the reviewed snapshot. Drift stops the run before writes.

## Phase 2 — install reviewed provider schema

Apply only the exact reviewed migration bytes, in order:

1. `20260912183000_initialize_runtime_planes.sql`
2. `20260912193000_create_predecessor_import_staging.sql`

After each migration, perform exact readback before continuing. Verify migration history, schema ownership, role membership graph, grants/default ACL behavior, RLS enablement/forcing, required functions, and absence of unintended PUBLIC/anon/authenticated/service-role capability.

If the provider returns an ambiguous mutation outcome, do not blindly retry. Reconcile the migration version and resulting database objects first; reuse the exact effect if present, otherwise remain `ATTEMPTED_UNKNOWN` unless an idempotent retry is proven safe.

Successful schema installation establishes `INSTALLED_NOT_ADMITTED / NOT_CURRENT_ROUTE`.

## Phase 3 — stage frozen predecessor evidence

Transfer only the reviewed MIGRATE corpus into the locked predecessor evidence plane. Do not write directly to admitted runtime-state domain tables.

For each supported source table:

- use the reviewed staging interface rather than raw table INSERT;
- preserve exact source provider/schema/table identity, primary key, source ordinal, source JSON representation, row digest, source-cut digest, and privacy floor;
- require the full one-table batch to match the frozen row count/PK set/order/table digest;
- reject dropped, added, mutated, duplicate, malformed, or cross-table batches;
- keep memory-epoch material at `PRIVATE_AUTOBIOGRAPHICAL` or a stricter compatible scope;
- treat predecessor sequence state as bounded non-MVCC evidence, not an operational sequence value to apply blindly.

## Phase 4 — database-derived verification

After each table batch, invoke only the reviewed database verifier and require a terminal receipt derived from staged rows, not caller-attested metadata.

Verification must bind at minimum:

- source cut;
- source table;
- exact row count;
- exact deterministic table digest;
- staged row identities/order;
- receipt status and immutable receipt identity.

A mismatch remains a mismatch. Do not rewrite evidence until it agrees. Repeated verification of an unchanged exact batch should be idempotent and must not invent a contradictory lifecycle.

When all reviewed tables pass, independently compare the new provider's staged counts/digests with the predecessor frozen snapshot. Preserve the per-table and aggregate verification receipt outside private payload bytes.

Successful staging establishes `PERSISTED_EXACT / NOT_ADMITTED / NOT_CURRENT_ROUTE`.

## Phase 5 — semantic shadow/readback gate

Before any current-state admission, exercise the new provider through read-only/shadow paths that consume the staged evidence and reviewed runtime substrate without making it authoritative.

Verify that source, provider, timestamps, semantic currentness, privacy, supersession/conflict handling, authority/effect ceilings, and receipt provenance remain distinguishable under real reads. Recency alone must not promote stale predecessor state.

Any semantic mismatch returns the cut to source repair or migration repair. Do not compensate by hand-editing provider rows.

## Phase 6 — admission and runtime cutover are separate effects

Do not perform semantic admission or route activation under installation/staging authority.

A later cutover authorization must separately identify:

- what exact state/evidence is being admitted as current;
- the reviewed admission procedure and supersession/conflict frontier;
- the runtime/service whose route will change;
- predecessor and rollback route;
- exact qualification suite required after route activation.

After authorized admission, verify exact provider readback before route mutation. After authorized route mutation, verify the current route independently before behavioral qualification.

## Phase 7 — qualification and rollback

Qualification must run against the actual activated route/configuration/source tuple. Source tests or shadow reads do not substitute for post-activation qualification.

If qualification fails, classify the failure without rewriting history: source defect, provider-install defect, admission/currentness defect, route defect, or behavioral defect. Roll back only the affected stage using its captured predecessor frontier.

Keep `klmbpaigzeguvnpccqzz` readable throughout qualification and rollback. Its retirement is a later protected operation requiring separate authority and a verified successor/rollback boundary.

## Hard stop conditions

Stop immediately on source-head drift, deployment-byte mismatch, provider-history drift, unexpected role/schema ownership, privacy broadening, digest/count mismatch, ambiguous mutation not reconciled by readback, semantic-currentness disagreement, route uncertainty, or qualification failure.

Do not transform a hard stop into a broader redesign. Fix the exact blocker or report the exact `WAITING` frontier.

## Current frontier at publication

- PR #119 exact head `42acf32c5cd20caba922608cd81e6086fc9cdf29` includes the strict-JSON and terminal-receipt-seal source repairs; PostgreSQL staging/seal execution and OV hostile review for this exact head remain `UNVERIFIED`. The earlier `ceca583b9f888794a9b2b70a7b32e616b4f0e8f1` execution receipt does not transfer.
- PR #20 remains `SOURCE_BOUND_NOT_APPLIED` for the runtime-plane and predecessor-import migrations.
- The deployment binding must not be refreshed from #119 until the exact reviewed head is frozen; execution GREEN alone is not hostile-review PASS.
- No mutation of `fawkirqroyniueeqspif` is performed by publishing this runbook.
- Next executable transition: receive the exact reviewed Vera source head, refresh only the bound deployment bytes/manifest in PR #20, run custody tests, and stop at `SOURCE_READY / WAITING_PRODUCTION_AUTHORITY` unless Patrick has granted the next protected phase.
