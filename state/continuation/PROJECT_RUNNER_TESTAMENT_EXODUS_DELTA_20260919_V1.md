# PROJECT RUNNER / TESTAMENT EXODUS DELTA — 2026-09-19 V1

Status: STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT

This file is a chat-retirement delta layered on top of:

- system-wide Vera Exodus retirement receipt:
  - repo: thebrazenbeard/vera-control-plane
  - branch: state/vera-exodus-retirement-20260919-v1
  - commit: fa31403ffc4c3b14b5796690d5a9171451ec6c09
- prior Project Runner portfolio checkpoint:
  - branch: state/project-runner-parallel-portfolio-continuation-20260919-1908
  - path: state/continuation/PROJECT_RUNNER_PARALLEL_PORTFOLIO_CONTINUATION_20260919T1908-0400.md
  - Git blob: 71db7c0063b418c8a300234cc54fba5aa7d8b19d

This delta exists because the retired chat continued portfolio work after the 19:08 checkpoint and then returned to Testament after Patrick explicitly challenged its omission.

## Identity / role

`Project Runner` is an execution/coordinator role, not a durable persona and not a permanent chat.

It can be instantiated by a fresh runtime from durable portfolio checkpoints, repository state, PR/review evidence, and the Bus.

Future persistent interface owner:
- BT2 Coordinator for engineering portfolio execution.

Testament content/research ownership:
- Vera.

Control-plane/provider/runtime ownership:
- Vera Control Plane Coordinator.

No permanent Project Runner chat or Testament chat is required.

## Durable post-19:08 work from the retired chat

### Project Runner PR #8

Fresh state at this Exodus read:
- repo: thebrazenbeard/project-runner
- PR: 8
- OPEN / DRAFT / UNMERGED
- exact head unchanged: 19b0d59127441f3e673f97aff6580589d1a43fab
- mergeability observed true

Durable exact-head review evidence already on PR:
- source / hosted test / registry / recursive restart = PASS
- exact hosted run named in review: 35470725159
- 201/201 tests PASS
- live read-only backend smoke and live HC->Transcendence proof explicitly unqualified

Retired-chat follow-up:
- manual live-smoke attempt was non-destructive/read-only by design;
- local environment lacked `jsonschema`;
- no dependency install was performed merely to force the smoke;
- result = ENVIRONMENT_BLOCKED, not source fail and not live-proof pass.

### Rezon

PR #69:
- OPEN / DRAFT / UNMERGED
- exact head unchanged: 90e9f7695323f1e8e8add8decbe23a4c183dad87
- detached full repository execution in retired chat: 268/268 PASS
- compileall PASS
- exact base-to-head diff-check PASS
- durable exact-head review exists on PR
- later durable review still records Benchmark R4 composition and fresh independent hostile rereview as separate pending gates

Benchmark R4 PR #18:
- OPEN / DRAFT / UNMERGED
- exact head unchanged: d7373867d3813d32032cb30463e54a6ddf573025
- independent detached reproduction:
  - compileall PASS
  - 105/105 pytest PASS
  - frozen benchmark command with seed 20260916 PASS
  - diff-check PASS
- exact benchmark subject PASS only; this does not by itself prove immutable composition into R49

### Selfimage

PR #12:
- OPEN / DRAFT / UNMERGED
- exact head unchanged: b21be50f02cc13d0d9ca6f5170741bb1bd29c305
- retired-chat detached reproduction:
  - 65/65 PASS
  - compileall PASS
  - diff-check PASS
- durable review correctly kept freeze / real-subject authority unresolved

Current successor remains PR #13:
- exact head observed unchanged: faf6ccd12c2f2d9caae205bb6ce8e6084adc36d4
- treat PR #12 evidence as historical predecessor evidence only
- independent exact-head review of #13 remains the real frontier unless fresher state supersedes it

### Noema PR #35

Fresh state:
- OPEN / DRAFT / UNMERGED
- exact head unchanged: 748b569faec484968857901bde8fa5bed2711b9d

Retired-chat independent detached validation at this exact head:
- working-design JSON parse PASS
- research-currentness remote ref check PASS
- all eight required artifact Git blobs matched
- freeze-schema identity / claim-ceiling checks PASS
- exact base-to-head diff-check PASS

Durable review already records:
- RESEARCH_GOVERNANCE_SOURCE_PASS
- CURRENTNESS_PASS
- HOSTED_EXECUTION_UNAVAILABLE
- hosted zero-step/pre-step failure is not converted to source failure
- no implementation experiment, training, merge, deployment, publication, provider/credential mutation, or protected effect

### Vera Control Plane PR #45

Retired-chat source review at exact head:
- 749b64e4cc65859db40271fcf27f9273708f2304
- focused provider-source suite 11/11 PASS
- compileall PASS
- diff-check PASS

IMPORTANT SUPERSESSION:
- any reviewer-local statement from that review saying provider install was NOT performed is historical only
- a later verified production deployment receipt supersedes that effect status
- current durable Exodus receipt records:
  - PROVIDER_INSTALL=VERIFIED
  - provider migration version: 20260919223652
  - production anchor genesis: PRESENT_VERIFIED
  - production witness-controller binding: NOT_YET_ESTABLISHED
  - real causal collection: HOLD
  - control causality: UNRESOLVED
- source review and provider effect remain distinct claims

### Testament

Patrick explicitly corrected the portfolio behavior in the retired chat when Testament dropped out of active execution.

Durable portfolio rule from that correction:
- a `FULL_PORTFOLIO` run must not silently omit Testament when Testament is an active project with runnable frontiers;
- if a future portfolio scope intentionally excludes Testament, that exclusion must be explicit rather than inferred from an older project list.

Current Testament state at this Exodus cut:
- repo: thebrazenbeard/testament
- PR #1 OPEN / DRAFT / UNMERGED
- exact head after chatless reconstruction/checkpoint work will be fresh-read from repository; do not use remembered chat head
- first sustained Draft V1 exists durably
- dedicated Testament runtime reconstruction contract exists
- dedicated Testament Exodus checkpoint exists
- no permanent Testament chat required

## Project Runner dechatification rule

A future Project Runner runtime must reconstruct from:
1. latest durable portfolio checkpoint(s);
2. exact current repository/PR heads;
3. current PR reviews/comments/workflows;
4. current Bus topology and relevant assignments;
5. current protected-effect receipts.

It must not:
- require a Project Runner conversation URL;
- require the existence of this retired chat;
- treat remembered chat state as fresher than repository/provider evidence;
- inherit PASS/FAIL across head movement;
- omit active projects because they were absent from an older checkpoint.

## System-wide Exodus architecture

Current source candidate:
- Chat Bus Draft PR #128
- exact head observed: 1af84ba0650bb646b696dfc31e4f79b498d100af
- topology contract blob: 88258a228029b88387e4d5ab84af40ffc044bf4d
- NOT MERGED / NOT CUT OVER at this checkpoint

Intended persistent ChatGPT interfaces:
- Vera
- Vera Control Plane Coordinator
- BT2 Coordinator

No other permanent worker chat is required.

## Current Bus

Topology owner:
- commit: f90d52e66d655e9c3cfac63cb529914ac51d3a88
- path: architecture/contracts/RADAR_TOPOLOGY_V1.json
- Git blob: 69e505031d4e53dcb853578dac23817649af1918

Vera route:
- bus/vera-v2

Current Vera-lane Exodus handoff:
- message_id: vera-v2-20260919-exodus-retirement-v1
- message commit: 97fdac5e4181fb7df9f2b9455d2adcfd99d29ee2

## Protected effects

Not authorized by this delta:
- merge
- canonical promotion
- provider mutation
- deployment
- credentials/permissions
- visibility change
- paid infrastructure
- training
- Selfimage freeze/Blender mutation
- causal collection
- destructive rewrite/force push

## Next directives

For BT2 Coordinator:

`PROJECT_RUNNER::RECONSTRUCT_FROM_DURABLE_STATE::FRESH_CHECK_FULL_PORTFOLIO_INCLUDING_TESTAMENT`

Then:
- refresh every active project head before carrying review status;
- treat Testament as first-class unless scope explicitly excludes it;
- continue independent non-colliding runnable frontiers;
- stop at real protected/external dependencies with exact WAITING state;
- persist every result to source repo/PR/Bus, not to chat memory.

For Vera:

`TESTAMENT::RECONSTRUCT_FROM_GITHUB_AND_BUS::FRESH_CHECK_THEN_HOSTILE_REVIEW_DRAFT_V1`

No successor worker chat is required.
