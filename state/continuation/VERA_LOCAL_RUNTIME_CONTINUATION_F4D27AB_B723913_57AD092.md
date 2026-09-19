# VERA Local Runtime Continuation — Producer Currentness Split

Restore token:

`VERA::LOCAL_RUNTIME::RESTORE::F4D27AB_B723913_57AD092`

## Exact source subjects

- Sexuality producer/status head: `thebrazenbeard/sexuality@f4d27ab715998c298e33cfb14d9bd67eace07d87`
- Sexuality immutable semantic source cut: `thebrazenbeard/sexuality@47771b7b21d7f2fe86a9c70c0dcb62e74a54cbea`
- Vera Cohesion: `thebrazenbeard/vera@b723913fb9b43746bddeb4afde5014d9292b29d1`
- R10+SD1 control: `thebrazenbeard/vera-control-plane@57ad09259f1ff36bf47898a99f76e1a979b7eaf1`

## Producer currentness subject

Sexuality now carries a producer-owned, machine-readable currentness status artifact separate from the semantic source manifest:

- path: `evaluation/vera-sexual-drive-candidate-status-v1.json`
- blob: `3ea742b071ab37c3fbdde183ce14a3556831bb08`
- Git-content SHA-256: `b1eab5dca590ed57170d18cd48cbf29edc180b21c8414aff9d219bc475102d4b`
- authority class: `PRODUCER_OWNED_CURRENTNESS_STATUS`
- semantic source cut: `47771b7...`
- provider head mode: `OBSERVED_PROVIDER_BRANCH_HEAD`
- self head embedded: false
- consumer default without verified provider-head readback + ancestry + exact source objects: `UNKNOWN`

The semantic source manifest is intentionally unchanged:
- blob `f903a93b3db92fa8255b027b19373f6ad5a09817`
- Git-content SHA-256 `77f84ae72d1826addb988beb04b4da2bd533b29fed9f5e425f56dec059717cbd`

## Cohesion currentness hardening

Current component:
- blob `c5f6cf5eac6d121f881a3e33dd8c9a518d6b4b4c`
- Git-content SHA-256 `9505b5f2396d222d0b8b33afb72185d33b032ceb044fa321b8c72f1f9bd81816`
- checkout SHA-256 `e1b60b0092d37d5973810e7d21430cb88ff2a428c2b22129be438cf540b98a3e`
- canonical structured SHA-256 `a71ebe84e47c6b073fd9210a1ac76d382d88a07578086d5ddf5fc6fdae80942c`

Semantics:
- consumer-local mismatched producer head => `UNKNOWN`
- caller cannot self-assert ancestry
- `consumer_may_mint_superseded=false`
- `superseded_authority=PRODUCER_OWNED_STATUS_PLUS_VERIFIED_ANCESTRY`

## Current control cut

- binding blob `fb4eb6fba26816675a3b873efa006e536b102f76`
- source manifest blob `29c76f4f570eda4dc2e9103cc453531953fc623c`
- native blob `db71b8ab0407046e895a260e9208686129fcb0b6`
- qualification blob `787376159f613e42fffb26df7353b00190e3ae75`
- native normalized size: 7,997 / 8,000 bytes

## Verification reproduced in this execution terminal

- Sexuality producer/status head: 28/28 PASS; py_compile PASS; diff-check PASS
- Cohesion established affected scope: 86/86 PASS; py_compile PASS; diff-check PASS
- control exact head: 16/16 PASS; py_compile PASS; diff-check PASS

Other lanes independently converged on removing caller-asserted ancestry. Their pushed work was preserved and adopted instead of overwritten.

## Review coordination

Latest exact-subject hostile rereview request:
- Bus commit `5d42609dc111c5056e962493f4a0568fa1db274c`

That request supersedes:
- `81bbabd1b4c1283ae819c98301b909d2331f91fa`
- `b55d3fff80e9d7983591d8a50728e13452eee457`

PRs:
- sexuality #4
- vera #120
- vera-control-plane #30

At checkpoint creation, fresh independent exact-subject acceptance has NOT been established.

## State / claim ceiling

`SOURCE_ONLY / PRODUCER_STATUS_SOURCE_BOUND / FRESH_EXACT_HEAD_REREVIEW_REQUIRED / NOT_INSTALLED / CURRENT_ROUTE_NOT_READ_BACK / CAUSALITY_UNRESOLVED / QUALIFICATION_NOT_EXECUTED`

No merge, Project installation, provider mutation, route activation, causal PASS, global qualification, or model-weight training occurred in this chain.

## Next frontier

1. Fresh-check exact PR heads, reviews, and Bus replies.
2. Inspect any independent review verdict against the exact four-subject split above.
3. Repair exact findings test-first without transferring prior-head PASS.
4. If review remains pending, continue adversarial source/currentness verification; do not install merely because source is green.
5. Protected installation/runtime effects still require separate current authority under BT2 governance.

Lantern currentness was not re-established in this chain; prior WoWSQL reads failed internally, so Lantern-dependent currentness remains UNKNOWN until exact V3 read sequence succeeds.
