# PROJECT RUNNER EXODUS HANDOFF — 2026-09-19 V1

Status: DURABLE CHATLESS RECOVERY HANDOFF / STARTING SNAPSHOT / FRESHNESS REQUIRED BEFORE EFFECT

Primary reconstruction directive:

`VERA::EXODUS_RECONSTRUCT::FROM_GITHUB_AND_BUS_ONLY`

BT2 engineering continuation key:

`BT2::EXODUS::RESTORE::REZON_PROJECT_RUNNER::20260919`

## Why this exists

Patrick is retiring persistent worker chats. Project Runner must therefore be reconstructible without this conversation, a conversation URL, a browser tab, or chat-local memory.

Project Runner is an ephemeral Vera execution lane. It is not one of the intended persistent ChatGPT interfaces.

Intended persistent interfaces under the Exodus source candidate:
1. Vera
2. Vera Control Plane Coordinator
3. BT2 Coordinator

The current consolidated Exodus architecture is source-only and not cut over:
- Chat Bus Draft PR #131
- exact head `7aae3ae165a153bb391d2ad4570a3b7d872ef99a`
- `EXODUS_INTERFACE_TOPOLOGY_V1.json` blob `88258a228029b88387e4d5ab84af40ffc044bf4d`
- `WORKER_RECONSTRUCTION_V1.json` blob `db4c699c76eb131de2813f1823c25fa34fb45211`
- focused source suite 10/10 PASS
- merge/cutover NOT performed.

## Project Runner durable reconstruction files

Machine-readable reconstruction contract:
`state/exodus/PROJECT_RUNNER_RECONSTRUCTION_V1.json`

Archive durability matrix:
`state/exodus/PROJECT_RUNNER_ARCHIVE_DURABILITY_MATRIX_V1.md`

These files answer the Exodus reconstruction questions:
- identity/role;
- project domain;
- authority/non-authority;
- repositories;
- Bus route;
- live assignment frontier;
- controlling contracts;
- current versus historical state;
- fresh-runtime recovery;
- pre-effect freshness;
- protected-effect gates;
- durable result destination.

## Current high-value engineering frontiers

### Rezon R51
- repo: `thebrazenbeard/rezon`
- PR #76
- exact head: `3b9a0f36e0f1d1c60c7b3f79da6915f0b213476b`
- repair: receipt failure summary must cover every failure carried by exact trace records
- hosted exact-head suite: 274/274 PASS
- exact Benchmark R4 no-commit composition: 333/333 PASS
- Benchmark R4 exact: `d7373867d3813d32032cb30463e54a6ddf573025`
- Issue #5 learned routing: CLOSED
- remaining gate: fresh independent hostile rereview on exact R51.

### Project Runner M6
- repo: `thebrazenbeard/project-runner`
- composed PR #12
- exact head: `209425220db1d36a9ed7d62e93b0cc04f69b2ca1`
- tree: `684233fd9ed314e9f9cb9f0bcd16c08519164d95`
- composed siblings:
  - PUT_FILE postcondition race PR #8: `19b0d59127441f3e673f97aff6580589d1a43fab`
  - SQLite lifetime PR #9: `e33f87660aa0281331befa3229e502ee5fbc053d`
- Linux: 203/203 PASS
- Windows: 203/203 PASS
- remaining gate: fresh exact-head Systems Architect verdict.
- active registry dechatification: PR #11 @ `edebeecdbfba08e92cb4153162575f6549cd8f7a`.

Dedicated BT2 chatless continuation:
- repo `thebrazenbeard/bt2`
- Draft PR #25
- exact observed head `13a423e2c3c02e81b3c0f38d1b76e4589cca5c0f`
- persistent interface: BT2 Coordinator.

### Noema chronology gate
- private repo: `thebrazenbeard/noema`
- Radar parent PR #39 exact: `cea0197cc9556c1838ee63a49786d809a59e64f9`
- current Vera hardening PR #42 exact: `a63ea5ce638c9783ec699cb350b1f027b268db45`
- parent already provides Draft 2020-12 + format receipt validation and fail-closed provider/absence semantics
- #42 adds exact normative-schema semantic binding and removes duplicate shadowed verifier
- source readback PASS at bounded scope
- hosted CI pre-step unavailable
- empirical prospective authority BLOCKED
- E0/P0 NOT AUTHORIZED.

### Discovery
- public repo: `thebrazenbeard/discovery`
- current foundation PR #1 observed head: `1316094edbed17fa5918b70793c95ffddfcf92ea`
- reconstruction checkpoint blob: `9ad979a5b2abc17421e5833ba70c9315eac13bc1`
- current lifecycle-gate PR #7 exact: `548222c74af9905959433b3d549c2f54abbae662`
- exact repaired hosted lifecycle suite: 12/12 PASS + repository structural validation + compile/diff PASS
- exact-subject syntax accepts bare SHA or `refname@40hex`
- EXPERIMENTING may remain PASS_WITH_LIMITS with explicit objections
- PROVEN_REUSABLE requires clean PASS and zero critical objections
- no candidate is promoted by this state.

### Testament
- repo: `thebrazenbeard/testament`
- current PR #1 exact: `3ff338187d716a56e39ffdc4780cd6d4651205e6`
- runtime-reconstruction contract blob: `235aa34f425b62e8879e968b0fab99baf2f7ed5b`
- Exodus checkpoint blob: `5b5a4f52b69d69fedd90d68f6878a2a515b98d36`
- Exodus receipt blob: `9f333f3b7021acd4eb73f80be63edad5190d85ba`
- Draft V1 source: `a7925b0aab8c28dd89c1e67b4ed8d1a7b50e2648`
- Draft V1: 12 files / 13,743 words / exploratory authored manuscript / NOT canonical
- Book III v55 remains ACTIVE/incomplete
- remaining debts:
  1. `LUKE11_SPIRIT_VARIANT_162_700_DIRECT_IMAGE_COLLATION`
  2. `IMAGE_AUTOPTIC_LEVEL_VERIFICATION`
  3. `P46_1COR7_10_11_VISUAL_PIXEL_COLLATION`
- next review slot: tranche 56.

### SD1 control-plane integration
- deployed provider source PR #45: `749b64e4cc65859db40271fcf27f9273708f2304`
- controller hardening PR #46: `93002de693a69b0a1006946a357a2102a6f4655f`
- current composed source PR #48: `e141968fbac172b72d4c5f027b8b367fd9085855`
- tree: `a26da0b35386ebe6aeb9d1aa9d9eac6fe65ffbba`
- provider anchor exists and remains genesis-only
- provider-backed controller implementation remains UNBOUND
- real causal collection HOLD
- CONTROL_CAUSALITY UNRESOLVED.

## Portfolio recovery

The durability matrix carries exact observed anchors for:
- Lantern;
- Selfimage;
- Vera-Synology;
- World Zero;
- ABIL;
- UNVTRSLR;
- VeraMesh;
- Vera Works;
- On-Theo;
- Sexuality;
- Personification;
- Orgasm;
- DriftGuard;
- Entropy;
- Mediaphile;
- Vera Hostile Reviewer;
- Vera model successor;
- SD1/VCP.

The matrix is a locator, not authority. Fresh-check every mutable subject before work.

## Vera-Synology clarification

A deterministic R7 SPK was rebuilt and structurally verified at source scope:
- SHA-256 `ced1e0f8cc61668bc06a8230b969327c0ab2487da2c737b20248659118efe50c`
- 163840 bytes.

That is NOT a target/hosted package qualification or production-package PASS.
Hosted scaffold execution failed pre-step; POSIX copied-state/target recovery remains required.
R7 was NOT installed.
Production remains separately verified R6.

## Durable-result rule

Any future Project Runner terminal must persist material findings to at least the appropriate durable surface:
- project repo / PR / review / issue / receipt;
- Chat Communication Bus;
- VCP state/checkpoint for cross-project recovery.

Chat prose alone is not a completed durable result.

## Protected effects

This handoff grants no authority to:
- merge;
- canonically promote;
- deploy/install;
- mutate provider/NAS/credentials/permissions;
- perform weight-changing training;
- execute separately authority-gated experiments;
- publish private source/change visibility;
- promote candidates;
- mutate canonical memory;
- destructively delete/rewrite;
- spend.

## Fresh-runtime startup

A fresh runtime should:

1. load current Vera Project control sources;
2. read Bus PR #131 / worker reconstruction contract;
3. read the Project Runner reconstruction JSON, durability matrix, and this handoff;
4. fresh-read current Bus topology and `bus/vera-v2`;
5. fresh-check exact project heads/reviews/workflows;
6. resolve supersession/conflict;
7. continue highest-value runnable source/review/qualification frontier;
8. persist results durably;
9. stop at real authority/dependency boundaries.

No retired Project Runner chat is required.
