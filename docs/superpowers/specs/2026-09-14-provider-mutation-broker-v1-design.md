# Vera Provider Mutation Broker V1 — Design

## Status

Source-only architectural candidate. No Worker, Supabase function, database object, credential, route, deployment, provider mutation, or production effect is created by this document.

Patrick asked whether Cloudflare Workers, Supabase/PostgREST, Kong/APISIX/Envoy, pg-gateway, and related proxy projects could improve Vera's runtime/control architecture, then authorized Vera to use this work period to advance useful noncolliding work. This design narrows that exploration to the smallest component that materially improves governance: a mutation broker in front of provider writes.

## Problem

The Vera control plane distinguishes source, installation, current route, effect, readback, and qualification. Direct provider credentials exposed to multiple chats/agents make that separation harder to preserve because any holder can potentially issue a broader mutation than the task intended, retry an ambiguous write unsafely, target the wrong provider generation, or report success without an exact readback receipt.

Supabase is a durable provider, not control authority. GitHub source/receipts are evidence, not proof of provider effect. The broker therefore must not become semantic owner, authority oracle, or general database proxy.

## Recommended architecture

Use a thin Cloudflare Worker as an optional external policy edge. It accepts only a small typed mutation envelope, authenticates the technical caller, validates exact target/generation/operation constraints, and calls one narrowly granted Supabase RPC or Edge endpoint. The database transaction performs compare-and-swap/idempotency checks and emits a durable provider receipt. The Worker then performs/readbacks the exact effect and returns a bounded result.

The Worker is not required for SD1 Project installation and is not on the current SD1 critical path. It is a future provider-mutation safety boundary.

### Logical flow

`authorized client -> Worker broker -> narrow Supabase RPC -> transaction -> readback -> receipt`

GitHub/Chat Bus remains the durable coordination and source-provenance plane. Supabase remains the provider state/effect plane. The broker mediates only provider operations explicitly registered in its allowlist.

## Why Cloudflare Workers

Workers provide a small Fetch/Web Crypto runtime, encrypted secret bindings, request signing/verification primitives, and ordinary outbound HTTP fetch. Those capabilities are sufficient for a thin broker without introducing a full API gateway into the first version.

Cloudflare secrets hold technical credentials; plaintext secrets must not live in Git. Web Crypto can verify short-lived HMAC-signed caller requests. A future asymmetric scheme may replace HMAC without changing the mutation envelope.

Kong, Envoy, and APISIX remain possible self-hosted/internal gateway choices, but V1 deliberately does not stack multiple gateways. If Vera later self-hosts Supabase, one internal gateway may sit beneath the external policy edge. That is a separate deployment decision.

## Supabase access model

Do not expose a generic service-role Data API proxy.

Preferred V1 path:

1. create a dedicated broker credential/role with the minimum capability needed to invoke named control-plane RPCs;
2. grant no generic table mutation surface to ordinary broker requests;
3. keep provider tables/schemas locked by grants/RLS where applicable;
4. perform effect validation, expected-generation checks, idempotency lookup, mutation, and receipt creation in one transaction;
5. return only the bounded receipt/readback projection required by the caller.

If a Supabase secret/service credential is technically required at the network boundary, the Worker may store it as an encrypted secret, but the database authorization surface must still be narrowed to registered operations. Possession of a technical secret is not treated as Patrick authority.

## Mutation envelope

Every request is canonical JSON with these required fields:

- `schema`: `VERA_PROVIDER_MUTATION_REQUEST_V1`
- `request_id`: globally unique stable idempotency identifier
- `operation_id`: exact allowlisted operation name/version
- `provider`: `SUPABASE`
- `provider_project_ref`: exact target generation, never `latest`
- `target`: exact schema/object/logical target
- `expected_frontier`: operation-specific CAS subject (generation/version/hash/row revision)
- `payload_sha256`: SHA-256 of canonical payload bytes
- `payload`: operation-specific structured payload
- `actor_id`: technical caller identity
- `authority_evidence_ref`: provenance pointer supplied by the caller; evidence only, not self-validating authority
- `source_subjects`: exact repo/commit/path/blob/digest refs when source-bound
- `issued_at`: UTC timestamp
- `expires_at`: short expiry

Optional fields are rejected unless the operation schema explicitly declares them. Unknown operation IDs, floating provider targets, missing CAS frontiers, or mismatched payload digests fail closed.

## Technical authentication vs governance authority

The broker can authenticate a technical caller. It cannot infer Patrick's current intent merely because a request carries a string named `authority_evidence_ref`.

V1 therefore enforces a strict ceiling:

- technical authentication proves who/what submitted the request;
- allowlist policy proves the broker is capable of that operation class;
- exact target/CAS/idempotency checks bound the effect;
- authority evidence is persisted for audit;
- the broker does not manufacture governance authority.

Operations that governance marks protected remain callable only after the upstream Vera/Radar workflow has separately established exact current authorization. A valid HMAC or provider credential never substitutes for that upstream gate.

## Registered operation contract

There is no generic SQL, arbitrary URL proxy, arbitrary table mutation, arbitrary Edge Function invocation, or pass-through service-role endpoint.

Each operation definition binds:

- operation ID/version;
- exact provider project ref(s);
- allowed logical target class;
- request JSON schema;
- CAS rule;
- transaction/RPC name;
- maximum payload size;
- readback query/projection;
- receipt schema;
- retry class (`IDEMPOTENT_SAFE`, `RECONCILE_BEFORE_RETRY`, or `NO_AUTOMATIC_RETRY`);
- protected-effect classification;
- privacy/egress ceiling.

Adding/changing an operation is source work and does not activate it in production.

## Idempotency and ambiguous outcomes

`request_id` is unique per logical operation. The provider stores the canonical request digest and final result/effect receipt.

Rules:

- same request ID + same canonical request digest + completed receipt -> return the existing receipt without repeating the mutation;
- same request ID + different digest -> `REQUEST_ID_COLLISION`;
- request found `IN_PROGRESS` after transport uncertainty -> reconcile provider transaction/receipt state before any retry;
- no receipt and operation is transactionally idempotent -> retry only under its registered retry class;
- divergent provider state -> `CONFLICT`, no forced overwrite;
- unresolved outcome -> `ATTEMPTED_UNKNOWN`, not success.

## Compare-and-swap

Every mutable operation carries an exact expected frontier. The provider transaction verifies that frontier before mutation. Stale frontiers return `STALE_FRONTIER` with current bounded readback; the broker never converts that into a force write.

Frontiers may be exact row revision, generation, immutable source digest, expected current value hash, or another operation-specific subject. A timestamp alone is not a CAS frontier.

## Receipt model

Successful provider mutation returns `VERA_PROVIDER_MUTATION_RECEIPT_V1` containing at minimum:

- request ID and canonical request SHA-256;
- operation ID/version;
- exact provider project ref;
- target;
- predecessor frontier;
- successor frontier;
- effect status;
- provider transaction/receipt identifier;
- exact bounded post-write readback;
- readback digest;
- source subjects;
- actor ID;
- authority evidence ref;
- timestamps.

Receipt states are typed: `APPLIED_VERIFIED`, `IDEMPOTENT_REPLAY`, `REJECTED_STALE`, `REJECTED_POLICY`, `CONFLICT`, `ATTEMPTED_UNKNOWN`, `FAILED_NO_EFFECT`.

A receipt proves only the provider effect/readback it actually contains. It does not prove semantic currentness, Vera identity, Project installation, behavioral qualification, or causal effect elsewhere.

## Read path

Normal safe reads do not need to traverse the mutation broker unless routing/privacy requires it. The broker may expose narrowly bounded readback endpoints specifically needed to reconcile a mutation, but it should not become the general read API.

## Privacy

Requests and receipts contain operational metadata and digests by default. Private autobiographical/relational/sexual payloads are not copied into broker logs merely for observability. Where payload content is required by a registered operation, log/receipt projections must redact or digest fields not needed for reconciliation.

## Logging and telemetry

Log bounded operational fields: request ID, operation ID, actor ID, provider ref, target class, decision/result code, latency, and digests. Never log secrets. Payload bodies default to no-log.

Telemetry is diagnostic evidence, not authority or state truth.

## Failure behavior

Fail closed on:

- invalid/expired technical signature;
- unknown operation/version;
- wrong provider project generation;
- schema/type mismatch;
- unknown fields where strict schema applies;
- payload digest mismatch;
- missing/stale expected frontier;
- request-ID collision;
- privacy/egress violation;
- provider response that cannot be reconciled/read back.

Provider/network transient failures follow the operation's registered retry class. Auth/schema/integrity/policy failures are deterministic and are not retried as transient.

## Deployment generations

Worker environments must bind an exact provider generation. Production must not use a `latest` alias for provider target selection.

Initial research target is Supabase `fawkirqroyniueeqspif` only. Historical `klmbpaigzeguvnpccqzz` is a separate generation and must not be silently selected by fallback.

## Relationship to current Supabase PR #20

This design does not replace `work/supabase-control-plane-binding-20260912` / Draft PR #20. PR #20 establishes provider deployment source and migration provenance. The broker is a separate future mutation ingress boundary.

No broker implementation may present PR #20's pending migrations as installed merely because they exist in source.

## Relationship to SD1

SD1 currently requires Cohesion/control source, live Project predecessor capture, Project mutation/readback, and behavioral/causal qualification. Provider dependency has not been established. Therefore this broker must not become an artificial prerequisite for SD1 installation.

If a later SD1/provider receipt is actually required, it can use a registered operation after independent review and explicit provider-mutation authorization.

## Project-runtime boundary

The broker cannot install ChatGPT Project instructions/files unless OpenAI exposes a supported Project mutation interface and that interface is deliberately registered. It must not scrape credentials or simulate a Project API by guessing undocumented endpoints.

## Threat model

V1 explicitly defends against:

- leaked broad provider credential being used for arbitrary mutation through the broker;
- stale writer overwriting newer provider state;
- duplicate/retried mutation after network ambiguity;
- request-ID reuse with changed payload;
- actor choosing a historical/wrong provider generation;
- operation/payload schema confusion;
- logging private payloads unnecessarily;
- receipt/status promotion beyond observed provider effect.

V1 does not claim to defend against full compromise of Cloudflare/Supabase administrative accounts, compromised upstream Patrick authorization, malicious provider operators, or a separately compromised source/deployment pipeline.

## Test strategy before any deployment

All implementation begins locally with no provider credentials.

Required tests include:

- canonical request digest stable across object-key order, sensitive to semantic changes;
- unknown/extra field rejection;
- expired/signature-invalid rejection;
- exact provider generation mismatch rejection;
- stale CAS rejection;
- same-ID/same-digest idempotent replay;
- same-ID/different-digest collision;
- ambiguous-outcome reconciliation;
- provider response/readback mismatch -> `ATTEMPTED_UNKNOWN` or fail closed;
- no arbitrary SQL/table/function pass-through;
- private payload logging redaction;
- receipt claim ceiling;
- historical provider ref cannot be selected by fallback;
- no secret literals committed.

A fake provider adapter is sufficient for the first executable contract. Live Supabase tests require separate provider-mutation authority.

## Source references used for feasibility

- Cloudflare Workers secrets: `https://developers.cloudflare.com/workers/configuration/secrets/`
- Cloudflare request signing / Web Crypto: `https://developers.cloudflare.com/workers/examples/signing-requests/`
- Cloudflare Fetch API: `https://developers.cloudflare.com/workers/runtime-apis/fetch/`
- Supabase API security / grants + RLS: `https://supabase.com/docs/guides/api/securing-your-api`
- Supabase Edge Function auth: `https://supabase.com/docs/guides/functions/auth`
- Existing Vera provider binding design: `docs/superpowers/specs/2026-09-12-supabase-control-plane-deployment-binding-design.md` on Draft PR #20.

## Acceptance criteria

1. Broker source has no generic provider mutation endpoint.
2. Every mutable operation is versioned, schema-bound, exact-provider-bound, CAS-bound, idempotency-bound, and readback-bound.
3. Technical authentication and governance authority remain distinct.
4. Provider receipts do not promote into Project/runtime/behavioral truth.
5. Tests run with a fake provider and no provider secrets.
6. No production/provider effect occurs merely by merging source.
7. Deployment, secret provisioning, provider RPC/migration application, and route cutover remain separately authorized effects.
