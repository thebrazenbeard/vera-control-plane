# Provider Mutation Broker V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a source-only, credential-free reference implementation of the Vera Provider Mutation Broker contract with a fake provider so its policy/CAS/idempotency/readback semantics can be hostile-tested before any Cloudflare or Supabase deployment work.

**Architecture:** Keep the first executable unit provider-neutral and dependency-light. A small ESM module validates/canonicalizes request envelopes, verifies technical HMAC signatures through Web Crypto-compatible primitives, dispatches only registered operations, and coordinates a fake transactional provider implementing CAS/idempotency/receipt behavior. A Worker/Supabase adapter is deliberately deferred until the contract passes source review.

**Tech Stack:** Node.js 20+ built-in ESM, `node:test`, Web Crypto API, JSON/SHA-256. No production credentials or network calls.

**Spec:** `docs/superpowers/specs/2026-09-14-provider-mutation-broker-v1-design.md`

## Global Constraints

- Source-only: no Cloudflare deployment, Supabase mutation, provider secret provisioning, route activation, or production call.
- No generic SQL/table/function proxy.
- Exact provider target only; initial allowed provider ref in fixtures is `fawkirqroyniueeqspif`.
- Technical authentication does not create governance authority.
- Every mutation requires exact expected frontier, stable request ID, canonical payload digest, bounded operation, readback, and typed receipt.
- Historical `klmbpaigzeguvnpccqzz` must never be chosen by fallback.
- Secrets and private payloads never appear in committed fixtures/log snapshots.

---

### Task 1: Freeze the request/receipt and operation registry contract

**Files:**
- Create: `provider-broker/package.json`
- Create: `provider-broker/src/canonical.mjs`
- Create: `provider-broker/src/contracts.mjs`
- Create: `provider-broker/test/contracts.test.mjs`

**Interfaces:**
- `canonicalJson(value) -> string`
- `sha256Hex(bytesOrString) -> Promise<string>`
- `validateMutationRequest(value, registry) -> normalized plain object`
- `validateOperationDefinition(value) -> normalized definition`

- [ ] Write failing tests proving canonical object-key order stability and semantic-change sensitivity.
- [ ] Write failing tests for required fields, unknown-field rejection, wrong provider ref, floating provider target, unknown operation version, missing frontier, malformed timestamps, and payload digest mismatch.
- [ ] Implement strict plain-JSON detachment/canonicalization so hostile object/prototype behavior is not consumed after validation.
- [ ] Implement exact schema/type checks with no truthy/coercive acceptance.
- [ ] Run `node --test provider-broker/test/contracts.test.mjs` and require PASS.
- [ ] Commit the independently testable contract unit.

### Task 2: Implement technical request authentication without authority promotion

**Files:**
- Create: `provider-broker/src/auth.mjs`
- Create: `provider-broker/test/auth.test.mjs`

**Interfaces:**
- `signRequest(secret, canonicalRequest, timestamp) -> Promise<string>` test helper
- `verifyRequestSignature({secret, canonicalRequest, timestamp, signature, now, maxSkewSeconds}) -> Promise<void>`

- [ ] Write RED tests for missing/invalid signature, modified payload, expired timestamp, and future-skewed timestamp.
- [ ] Write a PASS test for exact HMAC-SHA256 signature over the canonical request subject.
- [ ] Implement using `crypto.subtle` only; never log the secret or signature key material.
- [ ] Add a test proving a valid signature does not add/change `authority_evidence_ref` or operation authorization.
- [ ] Run auth + contract tests and require PASS.
- [ ] Commit.

### Task 3: Build a fake transactional provider and idempotency/CAS engine

**Files:**
- Create: `provider-broker/src/fake-provider.mjs`
- Create: `provider-broker/src/engine.mjs`
- Create: `provider-broker/test/engine.test.mjs`

**Interfaces:**
- `FakeProvider.apply(request, operation) -> Promise<providerResult>`
- `executeMutation({request, registry, provider, actor, authorityEvidence}) -> Promise<receipt>`

- [ ] RED: stale expected frontier -> `REJECTED_STALE`, no state change.
- [ ] RED: same request ID + same digest -> exactly one effect, second receipt `IDEMPOTENT_REPLAY`.
- [ ] RED: same request ID + different canonical digest -> `REQUEST_ID_COLLISION`, no second effect.
- [ ] RED: wrong/historical provider ref -> `REJECTED_POLICY`, no fallback.
- [ ] RED: simulated ambiguous provider result with no reconcilable receipt -> `ATTEMPTED_UNKNOWN`.
- [ ] RED: post-write readback mismatch -> never `APPLIED_VERIFIED`.
- [ ] Implement transaction model that records predecessor/successor frontier and canonical request digest atomically.
- [ ] Implement typed receipt with explicit claim ceiling.
- [ ] Run tests and commit.

### Task 4: Enforce registered operations and deny generic pass-through

**Files:**
- Create: `provider-broker/src/registry.mjs`
- Create: `provider-broker/test/registry.test.mjs`

**Interfaces:**
- `createRegistry(definitions) -> immutable registry`
- `registry.resolve(operationId, providerRef) -> exact operation definition`

- [ ] Define one harmless fixture operation (`control.receipt.probe.v1`) against the fake provider only.
- [ ] RED tests for arbitrary SQL, arbitrary URL, unknown function, unknown target class, oversized payload, and alternate provider ref.
- [ ] Verify operation definitions bind retry class, protected-effect class, privacy/egress ceiling, request schema, CAS rule, readback projection, and receipt schema.
- [ ] Implement deny-by-default registry and freeze/detach definitions.
- [ ] Run tests and commit.

### Task 5: Add privacy-safe logging and reconciliation behavior

**Files:**
- Create: `provider-broker/src/logging.mjs`
- Create: `provider-broker/test/logging.test.mjs`
- Modify: `provider-broker/src/engine.mjs`

**Interfaces:**
- `auditProjection(request, receipt) -> bounded object`
- `reconcileRequest(provider, requestId, requestDigest) -> Promise<receipt|status>`

- [ ] RED test proving payload bodies, secrets, and private fields never enter the audit projection.
- [ ] RED tests for `IN_PROGRESS`, completed exact replay, divergent digest, and unresolved provider state.
- [ ] Implement bounded audit fields only: IDs, operation, provider ref, target class, result code, latency placeholder, digests.
- [ ] Implement reconciliation-first rule for ambiguous outcomes.
- [ ] Run tests and commit.

### Task 6: Add a local Worker-shaped handler without network/provider effects

**Files:**
- Create: `provider-broker/src/worker.mjs`
- Create: `provider-broker/test/worker.test.mjs`
- Create: `provider-broker/README.md`

**Interfaces:**
- default Worker-style `{ fetch(request, env, ctx) }`
- environment requires only fake/test bindings in committed tests.

- [ ] RED tests: methods other than POST rejected; invalid JSON rejected; auth failure 403; policy/schema failures bounded 4xx; provider ambiguity bounded 409/503; exact fake success returns typed receipt.
- [ ] Implement handler without outbound network calls or committed secrets.
- [ ] Document that real Supabase/Cloudflare adapters are `NOT_IMPLEMENTED` and `NOT_DEPLOYED`.
- [ ] Verify repository search contains no service-role keys, Cloudflare API tokens, or real mutation endpoints.
- [ ] Run all broker tests and commit.

### Task 7: Whole-source hostile verification and handoff

**Files:**
- Modify only tests/docs if hostile findings require source repairs.

- [ ] Run full `node --test provider-broker/test/*.test.mjs` from a clean checkout.
- [ ] Run `git diff --check` against the branch base.
- [ ] Search for generic SQL/function pass-through and secret literals.
- [ ] Hostile tests: prototype/subclass objects, duplicate keys after parsing where applicable, Unicode/key-order canonicalization edges, stale CAS, request-ID collision, wrong generation, contradictory receipt/effect claims, provider readback mismatch.
- [ ] Record exact branch head and test counts in the Draft PR.
- [ ] Request independent review.
- [ ] Do not deploy, provision secrets, create Supabase RPCs/tables/functions, or mark provider route active without Patrick's separate exact authority.
