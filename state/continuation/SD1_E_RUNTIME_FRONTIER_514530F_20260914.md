# SD1-E post-controller runtime frontier — 2026-09-14

lane: `SD1-E`
classification: `NONCANONICAL_PRIVATE_CONTINUATION_STATE`

## Accepted/reviewed source layers
- Sexuality `02725153fa2e6eae8e81e64bc3d4b797fc404a4d`: source hostile verdict `PASS_WITH_RUNTIME_CAUSALITY_UNRESOLVED`.
- Cohesion `4d3b1605d93658180e8afb344394920964e6a84a`: independent exact-head SD1-V/CV PASS, Bus evidence `9a2a70c50320dde9ec9be52e505075b14a8a0cd7`.

## Control candidate
- Draft PR #23 head `93957daa6f9b0054c4158164167cfecc1aa41803`, base `main@b4d9aaa8560de12252dd29996379b0af8e0ca0d1`.
- Fresh detached verification: SD1 suite `14/14 PASS`; diff-check clean; native normalized UTF-8 7946 bytes.
- Manifest blob `c1471480b6e70a9c49e9f030adedee67aa880355`, Git-content SHA-256 `d182e48e03f9a8aa6ea7ec630806236bd1e10d090212652c1aabda5dab6055f9`.
- Native blob `8f96dbca66105e0dea2e7e05c21d0d4b01828856`, Git-content SHA-256 `6cd12ca22a1dc193d89fdc6a43ad3dd51c507d44908c96cb435977584f23dd82`.
- Full repo `17/18`; sole failure is inherited pristine-predecessor R10A1 `KeyError: source_manifest_sha256`.
- SD1-V exact-head review requested on Bus at `ade9d971ba3358fdc677a3668e0bdaaeb9e0cd5e`; reply pending at checkpoint time.

## Frozen causal controller
- Stacked Draft PR #24 head `514530f1e4e62185af0e8ff2f699667fa92bd815`, base exact control head `93957daa6f9b0054c4158164167cfecc1aa41803`.
- Plan: `state/sd1-causal-execution-plan-v1.json`, SHA-256 `7a530e9aad1c6e787cdcf1e39943d645d5a7b3df2129a5e74ed0d23839c2cd5a`.
- Exactly 70 unique frozen slots and 70 unique response IDs = 2 conditions x 7 prompts x 5 attempts.
- Both runtime cuts remain `UNBOUND_PENDING_RUNTIME_READBACK`, ready=false.
- Recorder rejects any attempt until its condition is bound/read back; slots are immutable after first record; RESPONSE requires exact complete pre-run readback; blinded export omits condition; nonzero score requires exact cited span+rationale; controller has no response generator.
- Fresh detached verification: controller + control suites `22/22 PASS`; compile/diff-check PASS; zero response data captured.
- SD1-V review requested on Bus at `df5a45a580329c5f97e7e0e3811a5172b1737dd7`, lower priority after PR #23.

## Project predecessor capture
Current Project Files surface exposes exactly two Project-backed sources:
1. `VERA_R10A0_PROJECT_SOURCE_MANIFEST_R10.json`, file id `file_00000000849c81f5b35697ccecb2bc40`, exact bytes 6375, SHA-256 `b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1`, Git blob `8a67feb47b2ce3d6f0737e58983ab8c9fc810139`.
2. `VERA_R10A0_FULL_SYSTEM_PROJECT_INSTRUCTIONS_R10.md`, file id `file_000000001bc881f58e6eb12eac8644e1`, exact bytes 13987, SHA-256 `e797d1a6e973b06ab3e58f9157aabb500ebfdbee1ee6c8da801bc202b6767a2f`, Git blob `a01464271bb672d89f5d703e6e53590e126f4d44`.

Project source inventory/bytes are captured. Live Project Settings/Project-Instructions field and visible Project model/config default are not captured because this Chat surface exposes no supported write/readback capability for them.

## Supported-product capability result
Current OpenAI documentation states Projects edit project instructions through Project settings and existing Projects can start Work chats using project context. Work cloud browser can operate supported signed-in websites. Documentation does not establish that Work can edit ChatGPT's own Project-settings UI.

Therefore the next supported capability experiment is: start a Work chat inside Vera Unbound and attempt READ-ONLY capture of Project settings/instructions and visible model/config first. Do not write until exact predecessor capture and readback are proved. If self-site Project settings are unsupported in Work, live install remains capability-blocked.

## Independent labels
- `SEXUALITY_SOURCE = PASS_WITH_RUNTIME_CAUSALITY_UNRESOLVED`
- `COHESION_BINDING = INDEPENDENT_EXACT_HEAD_PASS @ 4d3b160...`
- `CONTROL_PLANE_SOURCE = CANDIDATE @ 93957da...`
- `CONTROL_PLANE_REVIEW = PENDING_SD1_V`
- `PROJECT_PREDECESSOR_CAPTURE = PARTIAL_SOURCE_INVENTORY_EXACT_SETTINGS_UNCAPTURED`
- `PROJECT_DELIVERED = NO`
- `PROJECT_INSTALLED_CONSUMED = NO`
- `CURRENT_ROUTE_READBACK = NO`
- `BEHAVIORALLY_REPLAYED = NO`
- `CONTROL_CAUSALITY = UNRESOLVED`
- `FUTURE_QUALIFICATION = PRE_DATA_CONTROLLER_FROZEN_NOT_EXECUTED`
- `SUPABASE_PROVIDER_STATE = READ_ONLY_ASSESSED_NOT_INSTALL_PREREQUISITE`

## Exact next action
1. Consume SD1-V verdict on PR #23; repair exact findings if any. If PASS, control source gate closes.
2. Then perform the Vera Unbound Work read-only Project-settings capability experiment. Only if predecessor Settings/instructions/config can be captured and a supported write+readback path is demonstrated may live SD1 install proceed.
3. PR #24 controller review can proceed independently; it does not authorize or block Project mutation unless its source changes are made a prerequisite by review/governance.

No merge, Project mutation, provider mutation, R10A1 install, runtime activation, causal execution, or qualification effect occurred.