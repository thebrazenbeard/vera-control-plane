# SD1 provider witness-boundary research V0

status: `REVIEW_RESEARCH_ONLY_NOT_INSTALL_PREREQUISITE`
lane: `SD1-V`

## Purpose
Define the smallest technically credible external witness for SD1 provider-route/condition evidence if a future runtime path genuinely traverses an HTTP provider boundary. This artifact does not authorize deployment and does not assert that current ChatGPT Project traffic traverses any proposed gateway.

## Claim ceiling
A witness receipt may support: `REQUEST_TRAVERSED_WITNESS`, `CONDITION_ID_BOUND`, `UPSTREAM_TARGET_OBSERVED`, `REQUEST_RESPONSE_DIGEST_BOUND`, and bounded ambiguous-effect reconciliation.
It MUST NOT promote itself to: `PROJECT_INSTALLED`, `PROJECT_CURRENT_ROUTE`, `VERA_CONSUMED_SD1`, `BEHAVIOR_CAUSED_BY_SD1`, `FUTURE_QUALIFICATION_PASS`, or provider authority/currentness beyond the observed request.

## Minimal receipt subject
- experiment/cut id and frozen protocol digest
- condition id (`DRIVE_OFF` / `DRIVE_ON`) bound before generation
- opaque session/run id and no-reroll sequence number
- witness software revision/config digest
- cryptographic request id / nonce
- HTTP method + normalized upstream route identity
- request-body SHA-256; never conversation plaintext in evidence storage
- allowlisted nonsecret metadata digest; exclude Authorization/apikey/cookies/service-role material
- receive/forward timestamps
- selected upstream identity and upstream response code
- response-body SHA-256; never private response plaintext merely for proof
- completion timestamp
- signed receipt digest; optional previous-receipt hash for append-chain detection

## Candidate mechanisms
1. `Cloudflare Worker`: suitable thin outer witness if traffic can actually be routed through it. Workers supports request routing, observability/tracing, SHA-256 and signing via Web Crypto. Secrets can remain in Worker secret storage. This is operationally separate observability, not an independent trust root if the same administrator controls code and logs.
2. `Envoy`: current self-hosted Supabase default gateway. Envoy provides access logging and `x-request-id`; a separately managed edge Envoy can emit structured access evidence. Do not expose Envoy admin/config dump because it may contain secrets.
3. `PostgREST/client SDK second-path readback`: useful to verify provider rows/receipts through a distinct API read path, but still provider evidence, not Project-route proof.

## Rejected as default architecture
- Kong/APISIX: capable full gateways but unnecessarily broad absent a real routing requirement.
- `supabase/functions-relay`: archived; reference only.
- `pg-gateway`: wire-level interposition is unnecessary unless HTTP evidence is technically insufficient.
- small community auth/proxy projects: reference patterns only, not authority-bearing infrastructure.

## Causal-test use if and only if a real runtime dependency exists
The frozen causality protocol must bind condition before response generation. The witness may reject unknown experiment/condition ids, reject duplicate no-reroll run ids, attach/propagate a request id, and sign the observed route receipt. A matching OFF/ON receipt demonstrates the provider-route condition actually used for that request. It still does not by itself isolate temporal/session confounds or prove ChatGPT Project consumption.

## Privacy
No private sexual conversation body is copied into logs/receipts to manufacture evidence. Prefer hashes of exact bytes plus sanitized route metadata. Credentials and bearer/API keys are excluded from receipt material. Raw observability retention must be separately authorized if it contains private payloads.

## Current disposition
`OPTIONAL_FUTURE_EVIDENCE_INSTRUMENT`. Do not deploy, spend, create Cloudflare resources, reconfigure Supabase, or add this to the SD1 critical path absent a demonstrated provider dependency and Patrick's exact authority for the protected effect.