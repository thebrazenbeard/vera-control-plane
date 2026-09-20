# SD1 Supabase Witness Client — Source Integration 2026-09-20

Status: **SOURCE IMPLEMENTATION PRESENT / PROVIDER BYTES VERIFIED / QUALIFICATION UNBOUND / CAUSAL COLLECTION HOLD**

Parent integration subject: PR #48 exact head `e141968fbac172b72d4c5f027b8b367fd9085855`.

## What this source unit closes

The VCP provider already contains the SD1 secondary monotonic anchor, but PR #48 deliberately leaves the controller production witness implementation unbound.

This source unit adds the bounded provider client and wires an exact production witness type into the controller without making it constructible.

Implementation:

- `tools/sd1_causal_supabase_witness.py`
- client: `SupabaseFrontierClient`
- controller-eligible type: `SupabaseFrontierWitness`
- binding contract: `protocol/SD1_CAUSAL_SUPABASE_WITNESS_BINDING_V1.json`

The client exposes only:

- `sd1_causal_frontier_read_v1`
- `sd1_causal_receipt_read_v1`
- `sd1_causal_frontier_advance_v1`

There is no generic SQL proxy or direct table mutation path.

## Exact provider/source binding

Fresh provider readback established the deployed migration statement itself:

- provider: `fawkirqroyniueeqspif`
- migration version: `20260919223652`
- migration name: `create_sd1_causal_secondary_anchor`
- statement count: 1
- bytes: 24,103
- SHA-256: `246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523`

That exactly matches PR #45 head `749b64e4cc65859db40271fcf27f9273708f2304`, source path `supabase/migrations/20260919195000_create_sd1_causal_secondary_anchor.sql`, Git blob `0769c527ad8fc8280d052dc1ce93f85673b6bb7d`.

Classification: `EXACT_DEPLOYED_SOURCE_BYTES_VERIFIED`.

## Canonical hash compatibility

A read-only synthetic generation-1 vector was computed independently by the Python client algorithm and by the deployed immutable provider digest functions.

Synthetic fields:

- last slot: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- chain/last-record digest: 64 × `b`
- predecessor: provider genesis frontier digest

Exact matches:

- frontier digest: `ff5a32f213908b3da9de479434125cbab2ca5c5b6992bfdf0f9568163f67790f`
- request digest: `07035e70192c90180088b0cd9284393eeaf82e1250d9baf7c1a3f9c3a8e51f35`

Effect: **read-only immutable digest function calls only**.

## Ambiguity and idempotency

The client derives a deterministic request id from successor generation + frontier digest.

If the mutation transport is ambiguous:

1. it does not blind-retry the mutation;
2. it reads the exact request receipt;
3. if the receipt proves `APPLIED_VERIFIED`, it reads the frontier and requires exact successor equality;
4. if the receipt proves stale rejection, it fails conflict;
5. if no exact receipt/readback resolves the attempt, it returns outcome-unknown and the controller's pending-recovery gate remains in force.

A changed successor after ambiguity is not retried under the same attempt.

## Qualification fail-close

`SupabaseFrontierWitness` is intentionally not constructible in this source cut.

The source-controlled pin QUALIFICATION_ARTIFACT_SHA256 is None in
tools/sd1_causal_supabase_witness_qualification.py. Even a caller-supplied
mapping that says monotonicity_qualification=PASS is rejected.

The pin lives outside the implementation-subject digest. This is deliberate:
pinning an artifact must not change the witness bytes that the same artifact is
required to qualify.

A qualification artifact is also implementation-subject-bound. It must carry
canonical SHA-256 digests for the witness source, controller source, provider
binding contract, controller binding contract, and qualification acceptance
contract. Construction rehashes those current subjects and rejects an otherwise
correctly pinned PASS artifact when any subject digest is stale.

The exact acceptance semantics are frozen in
protocol/SD1_CAUSAL_SUPABASE_WITNESS_QUALIFICATION_V1.json. Its mutable status
and current-frontier fields are excluded from the semantic digest; evidence-gate
definitions, artifact shape, state separation, and non-effects remain bound.
monotonicity_qualification=PASS is not accepted as a standalone assertion.
The pinned artifact must contain PASS evidence digests for all five required
evidence gates.

A later source change may make the production witness constructible only after:

- all five acceptance-contract evidence gates are independently satisfied;
- a durable qualification artifact binds those evidence digests and all five exact implementation subjects;
- exact SHA-256 pinning of that artifact in source.

That later source change is itself separate from causal collection authority.

## Claim ceiling

Established:

- exact deployed provider source bytes;
- provider client source;
- controller source path;
- canonical digest compatibility;
- fail-closed qualification gate.

Not established:

- production witness qualification;
- production runtime binding;
- credential provisioning;
- real causal frontier advance;
- response collection;
- `CONTROL_CAUSALITY`;
- global qualification;
- Project install;
- merge authority.

No provider mutation was performed by this source unit.
