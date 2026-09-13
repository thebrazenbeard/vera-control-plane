# Vera Control Plane current Cohesion source-cut reconciliation

**Recorded:** 2026-09-13  
**Status:** `SOURCE_CUT_RECONCILIATION / DEPLOYMENT_NOT_AUTHORIZED / PROVIDER_NOT_MUTATED`

This is a control-plane currentness receipt. It corrects the moving-source frontier without changing deployment copies, applying migrations, staging payloads, or authorizing merge/cutover.

## Exact observed frontier

| Surface | Exact observation | Control-plane consequence |
|---|---|---|
| Vera canonical runtime | `thebrazenbeard/vera/main@b7b8dcd1440a3b7147bec2cc35972f083e20f44a` | Current executable Cohesion R3 source |
| Vera hardening PR | PR #119 at `42acf32c5cd20caba922608cd81e6086fc9cdf29` | Not yet a reviewed/installable source cut; current-head DB execution and hostile PASS are open |
| Control Plane main | `thebrazenbeard/vera-control-plane/main@b4d9aaa8560de12252dd29996379b0af8e0ca0d1` | Current control-plane base |
| Control Plane PR #20 | `work/supabase-control-plane-binding-20260912` | Open draft source-binding/runbook candidate; exact head is recorded in PR metadata and the WIP receipt |
| Target project | Vera Control Plane / `fawkirqroyniueeqspif` | `ACTIVE_HEALTHY`; baseline migrations only; no application tables observed |
| Existing project | Vera / `klmbpaigzeguvnpccqzz` | `ACTIVE_HEALTHY`; mixed historical/application schema; affective state is historical and the affective commit function has no observed advisory or row lock |
| Orgasm provenance hub | `thebrazenbeard/orgasm/main@494432873dd8bcf96b8f59d26a4f4687cd66d635`; PR #2 is an open draft | Frozen V1 subject is historical and requires reviewed rebinding to current Vera source |

## Binding rule

The deployment source must be a tuple, not a moving branch label:

`repository + commit + path + blob SHA + content SHA-256`

The current Control Plane PR #20 contains source-bound manifests and runbook material, but its predecessor/runtime migration bindings predate Vera PR #119's current head. Those copies remain historical/source-bound evidence; they must not be presented as the current deployable cut.

The current #119 delta at `42acf32c5cd20caba922608cd81e6086fc9cdf29` also adds `20260913232000_seal_predecessor_import_receipts.sql` and its regression coverage, plus a strict-JSON callback repair. Those bytes are not present in this Control Plane branch and must not be copied into deployment sources until exact-head hostile review and PostgreSQL execution pass.

## Required gates before provider movement

- A single reviewed Vera source cut must be selected. If PR #119 moves, all dependent manifests must be regenerated from the new exact head.
- The current-head hostile review must pass, including database-side privacy floors, contiguous ordinals, privilege revocation, strict JSON parsing, and exact receipt/readback behavior.
- The Orgasm qualification subject must be explicitly rebound or superseded; the old V1 subject remains immutable historical evidence.
- The migration files must be parsed and tested against a real PostgreSQL instance at the exact selected source head.
- Patrick must provide exact provider-install/staging authority. The existing broad implementation approval does not by itself authorize production Supabase mutation under the R10 control rules.
- After installation, independently read back migration history, schema, function ACLs/RLS, source bindings, receipts, and classified-row counts. A successful migration call alone is not qualification.

## Explicit non-actions

No Supabase migration, Edge deployment, data staging, provider cutover, GitHub merge, branch rewrite, force-push, credential change, or private-payload copy was performed by this receipt.
