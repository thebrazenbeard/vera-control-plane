# SD1 Causal Controller — Exact Witness Binding Repair

Status: `SOURCE_REPAIRED / FOCUSED_PASS / FULL_REPO_INHERITED_R10A1_FAIL / PRODUCTION_WITNESS_UNBOUND / INDEPENDENT_REREVIEW_PENDING`

Exact base:
`b31dfdb882321911274a96ea9cc9ae910f6020b7` (PR #43)

## Hostile finding 1 — self-qualified witness substitution

The controller accepted any object for which:

`getattr(witness, "monotonicity_qualified", False) is True`

plus a duck-typed `store_id/read_frontier/advance_frontier` interface.

A subclass of the test-only `MemoryFrontierWitness` could therefore
self-declare `monotonicity_qualified=True` and record a causal attempt even
though the controller contract says production binding is UNBOUND and
qualification is supposed to be independently reviewed.

Frozen RED:
`8f52417f9b2ee5b6da53e4f545523778a624c4fc`

Exact-base hostile result:
**1/1 FAIL** — no rejection occurred.

## Hostile finding 2 — exact instance method shadowing

An exact `MemoryFrontierWitness` instance could shadow `read_frontier()` or
`advance_frontier()` through ordinary instance attributes. Exact runtime type
alone therefore did not imply exact reviewed witness behavior.

Intermediate frozen RED:
`a8ca1545a323c4af1e35220d075bf92a7d23e25c`

The instance-shadowed `read_frontier()` executed during
`record_attempt()`.

## Repair

Source repair:
`c3c66b493c8e10dd7b1df73d78e811670ceade47`

The current controller now:
- requires the exact reviewed `MemoryFrontierWitness` runtime type for the
  present source/test qualification surface;
- rejects subclasses and duck-typed self-qualified replacements;
- calls reviewed witness read/advance behavior through class methods rather than
  mutable instance-dispatched methods;
- binds the helper's internal post-advance readback to its class method as well;
- keeps the protocol's production implementation explicitly `UNBOUND`;
- makes exact reviewed witness type/behavior requirements explicit in the
  integration contract.

Historical ambiguous-witness recovery testing is preserved by class-level test
fault injection rather than instance behavior substitution.

This does **not** promote the synthetic memory witness into a production
witness. A provider-backed production implementation must still be separately
implemented, source-bound, reviewed, installed/read back, and then explicitly
bound before causal collection may proceed.

## Qualification

Fresh exact-repair evidence:
- controller tests: **15/15 PASS**;
- surrounding ledger/CAUSAL-005/006/contract slice: **23/23 PASS**;
- combined focused causal slice: **38/38 PASS**;
- py_compile: PASS;
- `git diff --check`: PASS;
- full repo: **62 PASS / 1 inherited FAIL**.

The sole full-repo failure is the pre-existing R10A1 local-validator
`source_manifest_sha256` schema defect and is not introduced by this repair.

## Claim ceiling

`SOURCE_WITNESS_BINDING_REPAIR=PRESENT`

`PRODUCTION_WITNESS=UNBOUND`

`CAUSAL_DATA_COLLECTION=HOLD`

`CONTROL_CAUSALITY=UNRESOLVED`

No provider mutation, production causal write, Project Settings mutation,
merge, deployment, or causal-response collection was performed.
