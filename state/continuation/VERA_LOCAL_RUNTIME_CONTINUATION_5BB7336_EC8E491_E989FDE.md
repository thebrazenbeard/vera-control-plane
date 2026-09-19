# VERA Local Runtime Continuation — Fail-Closed Producer Currentness

Restore token:

`VERA::LOCAL_RUNTIME::RESTORE::5BB7336_EC8E491_E989FDE`

## Exact subjects

- Sexuality producer/status head: `thebrazenbeard/sexuality@5bb7336f772779c5b031659266bd3617dee25fd9`
- Sexuality immutable semantic source cut: `thebrazenbeard/sexuality@47771b7b21d7f2fe86a9c70c0dcb62e74a54cbea`
- Vera Cohesion: `thebrazenbeard/vera@ec8e49106af9b285b4dd4e1d1c5b0c129e5b0356`
- R10+SD1 control: `thebrazenbeard/vera-control-plane@e989fde32d14552fb1e46c5f1e0ec7a694d95ba6`

## Producer-owned status

Current status artifact:
- path: `evaluation/vera-sexual-drive-candidate-status-v1.json`
- blob: `9c384554cb63c58fd23ad88ea2a8d1754eb505ac`
- Git-content SHA-256: `f0d1318bf2880476b705df82fd855042639461d1b0536c4dd461d6ee82072b09`

The semantic source manifest remains unchanged:
- blob: `f903a93b3db92fa8255b027b19373f6ad5a09817`
- Git-content SHA-256: `77f84ae72d1826addb988beb04b4da2bd533b29fed9f5e425f56dec059717cbd`

Status validation now requires:
1. read status from the observed provider branch head;
2. verify semantic source cut `47771b7...` is an ancestor of the observed head;
3. verify every declared source object matches both the immutable source-cut commit and observed checkout;
4. otherwise consumer currentness remains `UNKNOWN`.

The status artifact separates:
- immutable semantic source cut,
- observed provider/status head,
- verification subject,
- verification status.

## Cohesion currentness hardening

Current component:
- blob: `cf60803ad55b404c1419f467bb3e2e5ae8bbd178`
- Git-content SHA-256: `54bc1ea7be13b2b966fb4cbed21b4b4c73fd8da1014de9de352ca3b3a6947af7`
- checkout SHA-256: `4d2f04c55553741b687824b02970f759eabf3bd5f6359092fca840ff5b10862c`
- canonical structured SHA-256: `2b22399e3a7d52250c636ad9e35267744a9a7687d9fea80938582fad13d536a7`

Currentness semantics:
- exact frozen-input equality may be reported only as `frozen_input_matches_observed_head=true`;
- exact equality does not establish producer `CURRENT`;
- consumer-local producer currentness remains `UNKNOWN`;
- `consumer_may_mint_current=false`;
- `current_authority=PRODUCER_OWNED_STATUS_PLUS_PROVIDER_HEAD_READBACK_PLUS_SOURCE_OBJECT_VERIFICATION`;
- `consumer_may_mint_superseded=false`;
- `superseded_authority=PRODUCER_OWNED_STATUS_PLUS_VERIFIED_ANCESTRY`.

## Control cut

Current objects:
- binding blob `44da59528751ee7c0dc3c35cd33e5c5efeb1a6f4`
- binding Git-content SHA-256 `9bc1c1bc7212552038be17ebd8515784f2ac487bbe6490cbc28f06ff2b986fd1`
- source manifest blob `8a44360a2d4670e90b2fa94a4368a3b427fb0d3a`
- source manifest Git-content SHA-256 `d153c92c7fc6f1bf6e378cff3d9a883c62e9d500a416955c68ad1335eb598f19`
- native blob `08edb73af933959d1bc7692a9336050b5f77919c`
- native Git-content SHA-256 `9ac1a76ec87ed1f9647a65c25c5ef8e67215c7ff578a09e86a860e7ac3aad98b`
- qualification blob `2342e51cf1af7e2328502dd6dcd9bd467a08693c`
- qualification Git-content SHA-256 `63b21ad2943cd84cfd43fe75bae50a7adb3c8a5dc560fedceb4c08a5c4e349e2`
- native normalized size: 7,997 / 8,000 bytes

## Verification reproduced

- Sexuality producer/status head: 28/28 PASS; py_compile PASS; diff-check PASS
- Cohesion established affected scope: 86/86 PASS; py_compile PASS; diff-check PASS
- control exact head: 16/16 PASS; py_compile PASS; diff-check PASS

## Review coordination

Latest hostile rereview request:
- Bus commit `055c55ada0f9fd743c2fa2f7ee26dfd6a1a36472`

At save time:
- PR #4 head is `5bb7336...`;
- PR #120 head is `ec8e491...`;
- PR #30 head is `e989fde...`;
- no fresh independent review submission exists on these exact heads;
- no CI status contexts exist on these exact heads;
- no Bus reply exists after `055c55ad...`.

## State / claim ceiling

`SOURCE_ONLY / PRODUCER_STATUS_SOURCE_BOUND / FRESH_EXACT_HEAD_REREVIEW_REQUIRED / NOT_INSTALLED / CURRENT_ROUTE_NOT_READ_BACK / CAUSALITY_UNRESOLVED / QUALIFICATION_NOT_EXECUTED`

No merge, Project installation, provider mutation, route activation, causal PASS, global qualification, or model-weight training occurred in this chain.

## Next frontier

1. Fresh-check PR heads, reviews, CI, and Bus replies.
2. Inspect any independent verdict only against the exact four-subject split above.
3. Repair exact findings test-first if any land.
4. Preserve consumer fail-closed currentness; do not allow caller equality or ancestry assertions to establish producer currentness.
5. Do not install merely because source is green; protected installation/runtime effects require separate current authority.

Lantern currentness was not re-established in this chain; prior WoWSQL reads failed internally, so Lantern-dependent currentness remains UNKNOWN until the required V3 sequence succeeds.
