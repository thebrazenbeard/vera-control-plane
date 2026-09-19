# Project Runner Exodus Retirement — Postscript V1

Status: **STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT**

Date: 2026-09-19

This postscript does not replace the verified retirement checkpoint at
`state/exodus/PROJECT_RUNNER_EXODUS_RETIREMENT_20260919_V1.md`.
It records concurrent Exodus work discovered immediately after that checkpoint and prevents newest-PR or duplicate-branch ambiguity.

## Concurrent Project Runner sibling

Repository: `thebrazenbeard/project-runner`

PR #21:
- head `e53dd3907af6686cbbe0937ba726803fe3640d23`
- title: `Exodus: make Project Runner chatless and discovery-driven`
- base: `main@bc05812b560b4fcde3a362e72fba04c626cafac8`
- exact-head workflow `35476848963` / job `105987448618`: SUCCESS
- test result: **99 PASS**
- review: `5258386033`

Disposition:
`SOURCE/DOCS PASS / SIBLING_NOT_SUCCESSOR`.

PR #21 adds useful chatless-orchestration, portfolio-discovery, and three-interface registry material, but it is based directly on `main` and does not carry the current M6/dechatification successor PR #20.

Therefore:
- PR #20 remains the current M6 dechatification subject at this cut;
- PR #21 is a useful sibling supplement;
- any future promotion must deliberately compose/rebase the subjects and requalify the exact result;
- recency alone does not supersede PR #20.

## Concurrent Bus sibling

Repository: `thebrazenbeard/chat-communication-bus`

PR #136:
- head `bde34be27c90821c5d4068e3a5d02cfea0b2ec6b`
- title: `Exodus: make worker reconstruction runtime-neutral`
- base: `main@aeab0f04fc9b4bd7c2945c9a53011c53fac809b4`
- source review: `5258386151`
- hosted run `35476796626`
- Python 3.11/3.12 jobs fail before any exposed step: `CI_PRE_STEP_FAILURE_UNRESOLVED`

Disposition:
`SOURCE/DESIGN PASS / HOSTED QUALIFICATION UNRESOLVED / SIBLING_NOT_GLOBAL_SUCCESSOR`.

PR #136 usefully removes remaining runtime/chat-specific wording, fixes stale writer-route references, and adds a runtime-neutral worker reconstruction contract. It does not carry PR #135's exact ACTIVE-writer reconstruction census/cutover gate.

Therefore:
- PR #135 remains the census-gated global Exodus subject at this cut;
- PR #136 is a useful sibling supplement;
- any integration must deliberately compose and requalify the exact result;
- recency alone does not supersede PR #135.

## Duplicate scratch branches created by this retiring terminal

Before the concurrent Exodus PRs were discovered, this terminal created two bounded documentation branches:

- `thebrazenbeard/chat-communication-bus@exodus/persistent-interface-terminal-topology-v1`
  - head `7e7a99ed4429645ed63f05613b13c667938f34cc`
  - no PR opened
- `thebrazenbeard/project-runner@exodus/project-runner-dechatification-v1`
  - head `8ccf1173168e155c25ddbf780fdc01687a224ff2`
  - no PR opened

Classification:
`HISTORICAL_EVIDENCE / DUPLICATE_SCRATCH / DO_NOT_PROMOTE_BY_RECENCY`.

Their material overlaps the already-active Exodus workstreams. They are not required for reconstruction and should not be treated as a new canonical path. They are left intact because this Exodus does not authorize destructive branch deletion.

## Retirement status

The chat-specific retirement conclusion remains:

`SAFE_TO_ARCHIVE`.

This Project Runner conversation is not required for:
- Project Runner identity/role reconstruction;
- current portfolio recovery;
- worker reconstruction;
- Bus routing;
- authority reconstruction;
- audit/challenge;
- continuation.

The global Exodus cutover remains separately blocked at the current census gate until all active writer identities are reconstructibly qualified. That global blocker is durable and does not require this conversation.

## Next interface / directive

Primary future interface:
`BT2 Coordinator`.

Next directive:

`BT2::EXODUS_CONTINUE::FRESH_CHECK_PROJECT_RUNNER_PR20_PR21_REZON_PR76_BUS_PR135_PR136`

No merge, canonical promotion, deployment, provider/NAS mutation, credential/permission change, training, publication, destructive deletion, Slack activation, or other protected effect was performed by this postscript.
