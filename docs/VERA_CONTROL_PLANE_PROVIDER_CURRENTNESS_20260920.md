# Vera Control Plane Provider Binding — 2026-09-20

Status: `OBSERVED_PROVIDER_BINDING / READBACK_ONLY / NO_PROVIDER_EFFECT`

This record gives the Vera Control Plane repository a durable locator for the live control-plane Supabase project without treating provider presence as runtime/control authority.

The observed project is `Vera Control Plane` / `fawkirqroyniueeqspif`, healthy in `us-east-2` on PostgreSQL 17.6.1.166. The provider currently exposes the narrow `vera_cp_anchor` state plus reserved `vera_cp_api` and `vera_cp_internal` schemas.

Fresh readback observed the SD1 causal witness at generation 0 with record_count 0 and zero mutation receipts. That establishes the installed genesis anchor only. It does not establish a bound production controller, causal collection, behavior/causal qualification, current route, phenomenology, or authority for a new provider mutation.

This source record deliberately does not modify R10/R10+SD1 control artifacts, Supabase, Project Settings, credentials, permissions, or runtime state.

Companion Vera-side currentness source: `thebrazenbeard/vera#136`.

## Exact deployed-source binding

The Supabase migration ledger retains the exact applied SQL statement. Fresh read-only hashing established:

- provider migration version: `20260919223652`
- provider migration name: `create_sd1_causal_secondary_anchor`
- statement count: 1
- applied SQL bytes: 24,103
- applied SQL SHA-256: `246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523`

Git source at PR #45 head `749b64e4cc65859db40271fcf27f9273708f2304`, path `supabase/migrations/20260919195000_create_sd1_causal_secondary_anchor.sql`, is also 24,103 bytes with the exact same SHA-256. Git blob: `0769c527ad8fc8280d052dc1ce93f85673b6bb7d`.

Classification: `EXACT_DEPLOYED_SOURCE_BYTES_VERIFIED`.

The provider migration version differs from the source filename timestamp, but the applied SQL bytes themselves match exactly, so provenance is bound by content rather than inferred from the version string.

Current integration candidate PR #48 head `e141968fbac172b72d4c5f027b8b367fd9085855` composes the deployed anchor source with the hardened controller source. That remains source integration only: provider-backed controller binding and real causal collection are still unestablished.
