# Exodus Cross-Project Worker Reconstruction Audit V1

Status: STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT
Recorded: 2026-09-19T21:53:30-04:00

Purpose: prove that retiring the current ChatGPT conversation does not remove durable identity, authority, assignment, recovery, review, or coordination state for the worker/role classes exercised here.

## Interface boundary

Persistent ChatGPT interfaces are exactly:
- Vera
- Vera Control Plane Coordinator
- BT2 Coordinator

Every other worker, reviewer, lane, project role, or specialist is instantiated from durable GitHub/Bus state into a temporary runtime terminal. A terminal is not durable identity, memory, authority, currentness, or assignment state.

Overall result: PASS_WITH_SOURCE_CANDIDATE_HOLDS.

No named worker or lane audited here requires this conversation to survive. Some Exodus reconstruction contracts are durable Draft-PR/source-candidate state rather than merged canonical main. Hosted CI on private Bus/control-plane Exodus PRs failed before runner admission, so local exact-head tests are source evidence while hosted status remains SOURCE_UNDETERMINED.

## Noah / Noëtarch

Classification: ALREADY_DURABLE / DURABLE_PROJECT_IDENTITY.

Owning repository:
- thebrazenbeard/hc-brain
- observed main: 618245b54fb923c7a204892c6953ab6d1c5dac57

Durable reconstruction:
- WARDEN.md — blob 4018be2085d1a97957f73c9ad0ab430f5794d0a5
- CURRENT.md — blob f5ff3f9ffe8e55e5cf1fe122afee7978ae1ed113
- docs/REPOSITORY_MAP.md — blob 642d191ec62ab1ee959069bc5e32f2c47c632caa

Coordination:
- non-PR HC coordination uses chat-communication-bus branch project/hc-brain-v1
- observed project lane head: 126397f182c203e546fee0f76bbce9a022de44d6

Noah / Noëtarch is the HC Brain Warden / primary architect, subject to Patrick owner authority. WARDEN.md explicitly says no permanent ChatGPT conversation is part of Noah identity or recovery. CURRENT.md is the currentness entrypoint. Chat dependency: NONE.

## Parallax

Classification: ALREADY_DURABLE / INDEPENDENT_REVIEW_IDENTITY / REGISTERED_INERT.

Canonical topology:
- Bus main: aeab0f04fc9b4bd7c2945c9a53011c53fac809b4
- RADAR_TOPOLOGY_V1.json blob: 69e505031d4e53dcb853578dac23817649af1918
- topology state preserves Parallax as REGISTERED_INERT until current activation/guard evidence exists.

Durable Exodus reconstruction source candidate:
- Bus Draft PR #140 exact head: 2461df3a1a8393d4c7ded227afb17ecc7abfacb3
- architecture/reconstruction/EXODUS_WORKER_PARALLAX_V1.json
- blob: 5a14ba0c43ce4e59d038459b5b9882f7be4a34e4

Route:
- bus/parallax-v1 observed head 6620e9d9cc6662da2872d37b98747edb8476b04b
- branch existence is provenance, not current assignment or activation.

Authority: independent systems-review/adversarial evidence under a current bounded assignment. No standing merge/provider/credential/branch-protection/deployment/canonical-integration authority.

Current assignment: NONE ASSERTED. A future Parallax runtime requires a new durable exact-subject review assignment. Chat dependency: NONE.

## SD1-E

Classification: ALREADY_DURABLE / TEMPORARY_EXECUTION_LANE / NOT A SEPARATE IDENTITY.

Durable lane contract source candidate:
- vera-control-plane Draft PR #52
- exact head b9b98a3b090101688cc65d1cf93265bb44fa54c4
- docs/EXODUS_RUNTIME_LANE_RECONSTRUCTION_V1.md
- blob b566d88784a288caeaaca226c2a66263aaf73f31

Durable state sources:
- thebrazenbeard/sexuality
- thebrazenbeard/vera
- thebrazenbeard/vera-control-plane

Fresh current source subjects:
- sexuality PR #4 head 353a1c516a3477221ed38108188f2e501b10084f — OPEN / DRAFT / clean
- vera PR #120 head 40e797c595a75ff95eedcb7351a28eef6cb67df5 — OPEN / DRAFT / clean
- control-plane PR #45 head 749b64e4cc65859db40271fcf27f9273708f2304 — OPEN / DRAFT; exact-head independent source rereview previously PASS

Effect ceiling:
- provider install NOT AUTHORIZED / NOT PERFORMED
- production witness UNBOUND
- causal collection HOLD
- control causality UNRESOLVED

Chat dependency: NONE.

## SD1-V

Classification: ALREADY_DURABLE / TEMPORARY_HOSTILE_REVIEW_LANE / NOT A SEPARATE IDENTITY.

Durable contract: same control-plane PR #52 exact head/blob above.

Required behavior:
- review one exact subject under explicit scope
- preserve reviewer/source provenance
- do not patch the reviewed head while acting independently
- head movement invalidates the verdict
- PASS/FAIL is evidence only, not merge/install/deploy/canon authority

No standing identity or authority exists outside a current durable review assignment. Chat dependency: NONE.

## BV

Classification: ALREADY_DURABLE / HISTORICAL_VERA_EXECUTION_LANE / NOT A SEPARATE IDENTITY.

Durable contract:
- control-plane PR #52 exact head b9b98a3b090101688cc65d1cf93265bb44fa54c4
- lane-contract blob b566d88784a288caeaaca226c2a66263aaf73f31

Historical coordination lane:
- bus/bv-v2 observed head 0d74ad85afad450ab46a23cf3168224c73234cfc

Recovery rule:
- recover current Vera control/governance and current assignment first
- historical bus/bv-v2 is provenance only
- do not instantiate BV merely because the branch or old chat exists

Current standing assignment: NONE ASSERTED. Chat dependency: NONE.

## VW

Classification: ALREADY_DURABLE / HISTORICAL_VERA-WORKS EXECUTION LANE / NOT A SEPARATE IDENTITY.

Owning durable project:
- thebrazenbeard/vera-works
- observed main cd4e35da647105b017ffbab890729c07b23525ef

Current durable contracts:
- governance/OPERATING_CHARTER.md — blob aaabf96b4fbfeae612effc667def0833db179ee1
- docs/superpowers/specs/2026-08-29-vera-works-operating-architecture-design-v2.md — blob ee1ef6ee581b47946dd22c225078a07a592a5a1e
- prompts/PROJECT_INSTRUCTIONS.md — blob b57565c8fec2e9c048feabfe355f6234372d64ba

Supersession:
- V2 explicitly supersedes the earlier V1 design for implementation purposes.
- old V1 text saying a ChatGPT Project holds worker chats is HISTORICAL_EVIDENCE, not current operating architecture.
- current charter/V2 design around work, not worker chats.

Historical Bus lane:
- bus/vw-v1 observed head a5f164029272997816ae31a39cf5615aaa4d5b52
- project/vera-works-v1 observed head e6f24773ae62e2511da4c2215e532ae46c5d5480

Current source frontier:
- vera-works PR #12 head 71cb8a1811dd74385587c73b036558d3491bb5c3
- OPEN / DRAFT
- local full workflow reproduction previously PASS; hosted private-repo job failed before runner admission.

Chat dependency: NONE. Future Vera Works workers receive current structured assignments/leases and use event state; VW is not a permanent worker identity.

## Project-specific workers and hostile reviewers

Classification: ALREADY_DURABLE + SOURCE_CANDIDATE_HARDENING.

Bus Draft PR #140:
- exact head 2461df3a1a8393d4c7ded227afb17ecc7abfacb3
- current census: 20 active topology writers / 20 durable reconstruction records
- census internal evidence basis head 41fb26753b7bf106e0bb235bf50980cfc8abf653
- census blob 1a07a419aff4829abe5e2b3addaccec97a342f9e
- runtime reconstruction contract blob 208b51117af4fc97bcce9eec4a07cbfde7c20c4d
- runtime reconstruction prose blob 7ac40f73bea0895bf246af41c33db659c5723f1c
- local exact-head Exodus/topology/reconstruction suite 29/29 PASS
- hosted jobs executed zero steps and produced no logs: RUNNER_ADMISSION_FAILED / SOURCE_UNDETERMINED
- PR remains DRAFT / UNMERGED.

Project Runner Draft PR #16:
- exact head 549c317ec0ade8926b6b9117448777b40bffd52a
- base 209425220db1d36a9ed7d62e93b0cc04f69b2ca1
- worker reconstruction doc blob 7a533592039f5164b4b6c12ac2e469e4dfa38376
- active registry blob c39a3621178fa13ba67af9fe44c683b8f1343b83
- active registry contains zero chatgpt.com URLs on that exact source candidate
- hosted exact merge-subject suite 207/207 PASS
- PR remains DRAFT / UNMERGED; it does not activate workers/routes or merge itself.

Generic rule:
- an execution terminal may host a worker but cannot supply missing identity, memory, assignment, currentness, or authority
- a reviewer is assignment-scoped unless a durable project identity contract says otherwise
- project-specific workers reconstruct from owning repository contracts plus current durable assignment/frontier and current Bus route
- no current durable assignment means IDLE / WAITING, not recover work from old chat
- route/branch existence never manufactures standing authority

## Conflicts and preserved historical evidence

CONFLICT — private hosted CI versus source-local evidence:
- Bus PR #140 and control-plane PR #52 show hosted failure, but jobs have zero executed steps and no logs.
- exact-head local targeted suites pass: Bus 29/29; control-plane 3/3.
- hosted classification: RUNNER_ADMISSION_FAILED / SOURCE_UNDETERMINED.
- no hosted PASS is claimed.

HISTORICAL_EVIDENCE — stale PR #140 body:
- PR description reflects an earlier 15/20 census.
- current exact branch head is 2461df3a1a8393d4c7ded227afb17ecc7abfacb3.
- current census artifact says ALL_ACTIVE_WRITERS_RECONSTRUCTIBLE_SOURCE_CANDIDATE and 20/20 READY.
- preserve the PR body as history; use exact branch bytes for current source-candidate state.

SUPERSEDES_EXISTING — Vera Works V1:
- V2 explicitly supersedes the earlier chat-centric implementation design.

## Privacy and Slack boundary

This audit persists operational reconstruction only. It does not export Patrick's private relational, sexual, medical, family, credential, or autobiographical material.

Slack is not activated, reconnected, or made durable infrastructure. A future Slack gateway may be an interface/transport only; Bus/GitHub remain system of record and coordination substrate.

## Protected effects

This audit performs or authorizes none of:
- merge
- canonical promotion
- provider install/mutation
- production deployment
- credentials/permissions changes
- training
- Selfimage freeze/Blender mutation
- causal collection
- public release/visibility change
- Slack activation

## Reconstruction test

Assume this conversation is inaccessible.

A fresh runtime can determine:
1. Noah identity/authority/currentness from HC Brain Warden + CURRENT + HC Bus project lane.
2. Parallax role/current inert lifecycle from Bus topology + exact reconstruction record.
3. SD1-E / SD1-V semantics and authority ceilings from the control-plane lane contract plus current source PRs.
4. BV historical-lane semantics without the BV chat.
5. VW semantics, assignments, authority, and state from Vera Works charter/events/leases without the VW chat.
6. generic worker/reviewer reconstruction rules from Bus PR #140 and Project Runner PR #16 source candidates.
7. exact protected-effect boundaries and freshness requirements.
8. current coordination route from Bus topology instead of a chat URL.

Result: PASS. The retired conversation is not required for functional reconstruction.
