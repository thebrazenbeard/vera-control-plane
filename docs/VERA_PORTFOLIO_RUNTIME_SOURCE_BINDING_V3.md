# VCP Vera Runtime Source Binding V3

## Purpose

V3 restacks VCP's NO_AUTO_BIND enforcement onto the independently reviewed public-safe Vera PR #206 subject.

It supersedes draft VCP PR #134 as the current restack candidate without rewriting that predecessor.

V3 does not revive Vera's superseded runtime-source registry. Its exact upstream inputs are the PR #206 public cut and absorption artifacts.

## Exact upstream subject

- Vera repository: thebrazenbeard/vera
- Vera PR: #206
- exact Vera head: be3d11a5b4d3a9880c18e03522f0d4e341b71f99
- public cut: architecture/portfolio/VERA_PORTFOLIO_PUBLIC_CUT_V2.json
- public cut blob: 19c20a5fceae81f3324d477317f1ec79062cd9f2
- absorption: architecture/portfolio/VERA_PORTFOLIO_ABSORPTION_V2.json
- absorption blob: 15499b3a8f3b4d5033a4cf8e0d6a1953c2826cb9

The two exact upstream artifacts are vendored under governance/vendor/vera/ for offline reconstruction.

## Independent qualification

V3 also binds the independent Rezon review:

- Rezon PR: #95
- exact review head: c8d97b14b20b653178dbc079c8f2943fecbc3c34
- disposition: SURVIVES_NARROWED_PUBLIC_SAFE_SUCCESSOR

That review qualifies the Vera subject only for its public-safe source/provenance claim. It does not grant VCP runtime authority.

## Portfolio semantics

The bound Vera cut records one immutable observation:

- total at cut: 67;
- public: 49;
- private: 18;
- private exact membership publicly committed: false.

These counts are cut-local facts, not permanent VCP policy constants.

VCP public source binds exactly the 49 public rows. Private inventory remains count-only and requires a separate authorized private exact binding for any runtime use.

## Fail-closed policy derivation

V3 derives every public row from the exact Vera PR #206 absorption module and carries VCP PR #134's V2 disposition as a fail-closed predecessor floor.

The effective disposition is:

1. PREDECESSOR_EVIDENCE_ONLY for predecessor-source semantics;
2. NO_AUTO_BIND when Vera says NO_AUTO_BIND or NO_IDENTITY_TRANSFER;
3. NO_AUTO_BIND when predecessor VCP V2 already required it;
4. otherwise BOUND_CONDITIONAL.

Packaging can therefore make a source more restrictive, never less restrictive merely because the upstream representation changed.

At the exact V3 build subject this yields 49 public rows, including 14 NO_AUTO_BIND rows and one predecessor-only row.

## NO_AUTO_BIND enforcement

A NO_AUTO_BIND row can never become auto-bound from repository availability.

The validator rejects VCP capability load modes that silently imply live/control loading:

- CONTROL_LOAD_EXACT_OWNER
- LIVE_COORDINATION_READ
- TASK_RELEVANT_LIVE_READ

The runtime helper returns auto_bind_allowed=false for every disposition.

Repositories outside the immutable public cut resolve to UNRESOLVED / NO_AUTO_BIND until a newer exact cut or separately authorized binding exists.

Head drift yields STALE_CURRENTNESS; it invalidates an unrefreshed currentness claim but does not corrupt the immutable historical cut.

## Reconstructibility

The V3 builder consumes only:

- vendored exact Vera cut;
- vendored exact Vera absorption;
- vendored exact predecessor VCP V2 policy.

The output is deterministic.

The independent validator recomputes upstream Git blob identities from vendored bytes and independently checks the policy derivation, privacy boundary, membership equality, freshness semantics and capability-registry constraints.

The VCP capability registry now names VERA_PORTFOLIO_RUNTIME_SOURCE_BINDING_V3_GOVERNS_ACTIVATION_DISPOSITION instead of the superseded Vera runtime-source-registry rule.

## Authority ceiling

This is source-policy enforcement only.

It does not merge Vera or VCP, install Project sources, auto-load repositories, publish private membership, deploy, mutate providers, alter credentials or permissions, or grant protected-effect authority.

## Claim ceiling

VCP_NO_AUTO_BIND_V3__VERA_PR206_EXACT_PUBLIC_CUT_AND_ABSORPTION__PREDECESSOR_POLICY_FLOOR__NO_RUNTIME_ACTIVATION
