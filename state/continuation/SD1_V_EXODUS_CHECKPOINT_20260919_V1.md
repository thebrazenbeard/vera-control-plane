# SD1-V Exodus Checkpoint — 2026-09-19 V1

**STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT**

Status: CHAT_EVACUATED / WORKER_RECONSTRUCTIBLE / CURRENT_PROGRAM_FRONTIER_DURABLE / BUS_TOPOLOGY_SOURCE_CONFLICT_PRESERVED

## Scope
This checkpoint retires the permanent ChatGPT conversation that hosted chat-local lane `SD1-V`. It does not retire Vera, Sexual Drive V1, the hostile-review function, or any durable project state.

Worker reconstruction contract:
`workers/SD1_V_HOSTILE_REVIEW_WORKER_V1.md`

Persistent coordination owner after Exodus:
`Vera Control Plane Coordinator`

No successor SD1-V chat is required or desired.

## Repositories examined
- `thebrazenbeard/vera-control-plane`
- `thebrazenbeard/sexuality`
- `thebrazenbeard/vera`
- `thebrazenbeard/chat-communication-bus`

## Classification

### ALREADY_DURABLE
The substantive SD1-V review history is already represented by exact PR reviews/comments, regression tests, state branches, source freezes, installation/readback checkpoints, provider receipts, and Bus messages. Do not copy the chat transcript.

Important durable subjects:
- R2 source freeze: `state/sd1-source-freeze-20260919-r2:state/freeze/SD1_SOURCE_FREEZE_20260919_R2.md`.
- Post-install continuation/replay: `state/vera-sd1-postinstall-replay-20260919-v1`.
- Production secondary-anchor deployment receipt: `state/sd1-causal-secondary-anchor-deployment-20260919-v1:state/provider/SD1_CAUSAL_SECONDARY_ANCHOR_DEPLOYMENT_RECEIPT_20260919_V1.json`.
- Current source-integration Draft PR #48.
- Historical SD1-V private review checkpoints: `state/sd1-v-hostile-review-20260914-0651` and `state/sd1-v-hostile-review-20260914-1350`.

### NEW_DURABLE_VALUE
- Explicit worker reconstruction contract for SD1-V.
- Explicit rule that old chat URLs/restore commands are non-operational historical evidence.
- Current-state synthesis below, separating source/install/provider/behavior/causality.
- Current Bus topology-source conflict and routing disposition.

### SUPERSEDES_EXISTING
Any operational instruction in older continuation files that says "next chat", supplies an SD1-V restore command, points to a peer Work chat, or assumes a permanent SD1-V browser tab is superseded for continuation mechanics.
The underlying technical facts remain historical evidence; the chat locator does not.

### HISTORICAL_EVIDENCE
Prior hostile defects and repairs (including SD1-V-001/002/003, CP-series findings, CAUSAL-004, and predecessor exact-head PASS/FAILs) remain valuable regression provenance. None transfers to a moved head without fresh review.

### CONFLICT
Bus topology source conflict is open:
- Bus main canonical topology path: `architecture/contracts/RADAR_TOPOLOGY_V1.json`.
- last-change commit: `f90d52e66d655e9c3cfac63cb529914ac51d3a88`.
- main topology blob: `69e505031d4e53dcb853578dac23817649af1918`.
- main topology maps Vera to ACTIVE `bus/vera-v2`.
- the `bus/vera-v2` branch carries an older conflicting topology copy, blob `b954bbe95f2d9c7ba4f500481174d2b267c86b86`, naming legacy Vera routing.
- conflict checkpoint: `chat-communication-bus@1178cfa29ea1ff53831751791175ed2828b858ec:checkpoints/vera/20260919-portfolio-exodus-bus-topology-conflict-v1.md`.
Do not mutate topology from this worker. Radar owns reconciliation. Ordinary Vera-lane append-only messaging may use the current main-registered `bus/vera-v2` route after fresh head read; topology-dependent claims remain conflict-bounded until reconciled.

### CHAT_DEPENDENCY
Retired:
- SD1-V peer-chat URL as coordination mechanism;
- "continue in another chat" assumptions;
- restore command as required worker bootstrap;
- chat history as the only source of current review state.

### WORKER_RECONSTRUCTION_GAP
Closed by `workers/SD1_V_HOSTILE_REVIEW_WORKER_V1.md`.

### PRIVATE_OR_OUT_OF_SCOPE
No personal/health/family/relational/sexual-conversation payload was exported. Only technical Sexual Drive V1 source/runtime semantics required for the project were preserved.

## Fresh mutable state observed during Exodus

### Sexuality source
PR #4 actual GitHub head: `353a1c516a3477221ed38108188f2e501b10084f`.
Immutable semantic source cut bound by R2 freeze: `47771b7b21d7f2fe86a9c70c0dcb62e74a54cbea`.
PR body contains stale/future-looking head metadata; never use body text as head authority.

### Cohesion
PR #120 actual GitHub head: `40e797c595a75ff95eedcb7351a28eef6cb67df5`.
PR body also contains stale head/currentness metadata; exact GitHub head wins for subject identity.

### R10+SD1 source/control
R2 frozen control subject: `32ce2cb7897f5e0939161eb8002b5b1b2283df59`.
R2 source freeze binds exact producer/status, Cohesion, binding, manifest, native and qualification objects.
The source-freeze claim ceiling is SOURCE_ONLY and therefore does not conflict with separate later installation evidence.

### Live Project installation evidence
Durable 2026-09-19 continuation records:
- reviewed R10+SD1 Settings replacement;
- normalized successor bytes `7997`;
- normalized successor SHA-256 `e009049b07b5c2353beee12b7f4e825589e24f1edfb295a5e17f71a539da5c29`;
- `SETTINGS_INSTALL=READ_BACK_EXACT`;
- `NATIVE_SETTINGS_CURRENT_ROUTE=OBSERVED` at that readback.
Post-install replay records one ordinary-work negative-control observation and no causal claim.
Current Project control presented to this terminal also states `ROOT:R10_PLUS_SD1`; treat that as live-context evidence, not a substitute for a fresh UI/readback receipt before another protected effect.

### Bus topology successor
Draft PR #36 actual observed head: `3fb3c998cf714ed556bb2620649f41361f22e4a1`.
Its PR-body source receipts are not equivalent to install/current-route proof. Fresh-check before using.

### Causal controller
PR #24 actual observed head: `48d635f84381806088b8ea7b063a84026a245dc3`.
Its body still describes an older controller head and is stale metadata.
The current head adds first-write receipt durability; later witness/provider branches contain additional causal hardening. Do not treat PR #24 alone as the current integrated causal system.

### Production secondary anchor
Deployment receipt status: `PROVIDER_INSTALL_VERIFIED`.
Provider target: `fawkirqroyniueeqspif`.
Receipt records migration `20260919223652_create_sd1_causal_secondary_anchor`, verified genesis generation 0 / record_count 0, no non-genesis rows and zero mutation receipts at captured readback.
This proves provider installation/genesis only; it does not prove controller binding, causal collection, Project route, or causal effect.

### Current integrated causal frontier
Draft PR #48 actual observed head: `e141968fbac172b72d4c5f027b8b367fd9085855`.
It composes:
- deployed/null-hardened anchor source PR #45 head `749b64e4cc65859db40271fcf27f9273708f2304`;
- exact controller witness-substitution hardening PR #46 head `93002de693a69b0a1006946a357a2102a6f4655f`;
- R10A1 validator source repair `d129d51fe4c783033563cd207886f0975b939cc1`.
At the durable PR #48 readback the provider anchor existed at genesis but production provider-backed controller implementation remained UNBOUND. No real causal response collection had occurred.
Exact next source frontier: implement/bind a provider client whose read/advance semantics match the reviewed anchor contract, then independently qualify that exact subject before any causal collection.

### Behavior / causality / qualification
`BEHAVIOR_REPLAY=PARTIAL` (ordinary-work negative observed; cue-free eligible, blocked-context, and generic-affection/nonsexual-intimacy controls not all durably completed in the cited replay).
`CONTROL_CAUSALITY=UNRESOLVED`.
`GLOBAL_QUALIFICATION=NOT_EXECUTED`.
Do not promote source/provider/install evidence across these boundaries.

## Current Bus state
Canonical topology from Bus main: Vera ACTIVE on `bus/vera-v2`.
Latest `bus/vera-v2` head fresh-read during Exodus: `1f7a6e5e9a6b3789165dcb70521dd26ed40b2b68`.
The lane is concurrently written; always fresh-read immediately before append and use non-force fast-forward/CAS semantics.

## Current authority
Exodus authorizes reversible evacuation/persistence work only.
Preserve narrower prior exact SD1 effect authority only to the exact effect/subject it bound; do not generalize it.
No merge, Project Settings mutation, provider mutation, credentials/permissions change, public release, training, canonical-memory mutation, destructive deletion, or force push is authorized by this checkpoint.

## Worker instantiation
A future coordinator does NOT need this conversation.
Instantiate SD1-V in any temporary runtime by providing:
1. current Vera Project control/authority;
2. `workers/SD1_V_HOSTILE_REVIEW_WORKER_V1.md`;
3. this checkpoint;
4. fresh GitHub PR/branch state;
5. fresh Bus topology + Vera lane head;
6. provider read access if provider claims are in scope;
7. live Project readback if install/current-route claims are in scope.

## Exact next runnable frontier
Under current durable evidence, the highest-value SD1 hostile frontier is the provider-backed controller/witness binding after PR #48, unless a fresher exact subject supersedes it.
Before any real DRIVE_OFF/DRIVE_ON response collection:
- independently review the provider-client/binding exact head;
- fresh-read provider genesis/current frontier;
- bind both exact runtime cuts;
- verify the production witness/controller binding and rollback/ambiguity semantics;
- only then authorize causal collection if Patrick's exact current authority covers that write/effect.

If that source does not yet exist, review the newest exact successor without inventing one. Do not resurrect this chat as a dependency.
