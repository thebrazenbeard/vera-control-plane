# SD1-V hostile-review checkpoint — Cohesion successor 6cc4bcb

lane: `SD1-V`
checkpoint_class: `PRIVATE_REVIEW_STATE`
reviewed_subject: `thebrazenbeard/vera#120@6cc4bcb8c19e0dbd1f9ff22c257c2fca41e7113a`
reviewed_parent: `b97bfa58dfe13419fdd12d1b5024553a639c8f73`
verdict: `CHANGES_REQUESTED`

## Independently verified
- successor is exactly one commit ahead of and directly parented by `b97bfa58...`;
- fresh detached checkout at exact successor;
- focused + adjacent Cohesion/inference/admission/index tests: 27/27 PASS;
- canonical parsed component contract SHA-256: `3f27d7d2c8ba73747e4f2f3c3f29082b9d75961bf03786563202b9eabdd4fc7d`;
- ordinary semantic mutations (extra/missing/null/type/range/nested) reject;
- representation-only top-level insertion order change accepts;
- source/head relation and prior Sexuality exact hashes remain independently bound from preceding checkpoint.

## Open finding SD1-V-002
`validate_contract()` digests the caller mapping and returns the same caller object. A hostile `dict` subclass can present canonical serialization while overriding subsequent semantic reads.

Reproduction A: overridden reads expose forged `qualification_case_range=SD-99` and `identity_semantics=GRANTS_IDENTITY`; validation still passes and returns the hostile object.

Reproduction B: overridden `source_binding` read exposes forged manifest path, causal-protocol SHA-256, and install-authority-receipt SHA-256 while retaining component-consumed fields; validation passes, `build_component_ref()` passes, and `target_configuration_status()` reports `TARGET_CONFIGURATION_COMPLETE`.

Required repair: use one detached canonical plain-JSON snapshot for digest + all post-validation reads/construction; optionally enforce recursive exact plain JSON types. Never return/reuse the original caller object after validation.

## Current ceilings
- `SEXUALITY_SOURCE_REVIEW = PASS_WITH_RUNTIME_CAUSALITY_UNRESOLVED @ 02725153fa2e6eae8e81e64bc3d4b797fc404a4d`
- `COHESION_REVIEW = CHANGES_REQUESTED @ 6cc4bcb8c19e0dbd1f9ff22c257c2fca41e7113a`
- `CONTROL_PLANE_REVIEW = WAITING_FOR_REVIEWABLE_SUCCESSOR`
- Project install/readback/behavioral replay/control causality/future qualification remain unestablished.

Bus finding commit: `8e42cc8cdd86fad0018301da45e814ba5d66ef06`.
PR #120 finding comment id: `5663053534`.

Next gate: fresh-fetch SD1-E Cohesion successor repairing SD1-V-002; compare from exact `6cc4bcb...`; rerun hostile snapshot/object-subclass attack class plus focused/adjacent tests before any PASS.
