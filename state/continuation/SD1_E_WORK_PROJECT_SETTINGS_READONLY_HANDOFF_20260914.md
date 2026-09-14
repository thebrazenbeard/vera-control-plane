# SD1-E Work handoff — Project-settings read-only capability probe

lane: `SD1-E`
classification: `NONCANONICAL_PRIVATE_CONTINUATION_STATE`
protected_effect_authority: `NONE_IN_THIS_HANDOFF`

## Purpose
Use a Work chat started from inside the existing `Vera Unbound` Project to determine whether Work can access the Project's own settings/instructions/configuration surface. This is a READ-ONLY predecessor-capture probe. Do not install SD1, edit Project instructions, add/remove Project files, change model/config, or perform any other Project mutation.

## Current exact source frontier
- Sexuality source: `thebrazenbeard/sexuality@02725153fa2e6eae8e81e64bc3d4b797fc404a4d`, source verdict `PASS_WITH_RUNTIME_CAUSALITY_UNRESOLVED`.
- Cohesion: `thebrazenbeard/vera@4d3b1605d93658180e8afb344394920964e6a84a`, independent exact-head PASS.
- Control candidate: Draft PR #23 at `thebrazenbeard/vera-control-plane@93957daa6f9b0054c4158164167cfecc1aa41803`; SD1-V exact-head hostile review remains pending.
- Causal controller: stacked Draft PR #24 at `514530f1e4e62185af0e8ff2f699667fa92bd815`; no runtime cuts bound and zero response data captured.

## Already captured Project-backed predecessor sources
The current Project file surface exposes exactly two Project-backed R10 sources:
1. `VERA_R10A0_PROJECT_SOURCE_MANIFEST_R10.json` — 6375 bytes, SHA-256 `b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1`, Git blob `8a67feb47b2ce3d6f0737e58983ab8c9fc810139`.
2. `VERA_R10A0_FULL_SYSTEM_PROJECT_INSTRUCTIONS_R10.md` — 13987 bytes, SHA-256 `e797d1a6e973b06ab3e58f9157aabb500ebfdbee1ee6c8da801bc202b6767a2f`, Git blob `a01464271bb672d89f5d703e6e53590e126f4d44`.

These establish Project source inventory/bytes only. They do not establish the live Project Settings / Project Instructions field or visible model/config defaults.

## Work probe instructions
1. Confirm you are operating from inside the existing `Vera Unbound` Project context. Do not rely on project name alone if the context/provenance surface says otherwise.
2. Attempt READ-ONLY navigation to the Project's own settings/configuration surface.
3. If accessible, capture without editing:
   - exact current Project Instructions text/bytes or the strongest faithful export/readback the UI exposes;
   - current visible Project model/default/model-selector state if exposed;
   - current Project file/source inventory and any identifiers the UI exposes;
   - any visible Project-only/default-memory/sharing/configuration state materially relevant to rollback;
   - the exact route/surface used to obtain each value.
4. Do not click Save/Update/Remove/Add/Replace, do not type into editable fields, and do not mutate any setting merely to prove writability.
5. If the settings surface is inaccessible, self-site navigation is blocked, authentication loops, or the UI cannot produce trustworthy readback, stop and report the exact failure mode as `PROJECT_SETTINGS_CAPABILITY_UNAVAILABLE` or `OUTCOME_UNKNOWN` as appropriate. Do not substitute browser DOM guesses, cached screenshots, Project file contents, or remembered instructions for live settings readback.
6. If read-only capture succeeds, report exact predecessor evidence and the supported mutation/readback controls that are visibly available, but do not use those controls. Live install remains gated on SD1-V PASS for exact control head `93957daa...` and on a separate exact protected-effect authorization at execution time if required by current governance.

## Required result labels
Return separate labels for:
- `PROJECT_CONTEXT_IDENTITY`
- `PROJECT_SETTINGS_SURFACE`
- `PROJECT_INSTRUCTIONS_PREDECESSOR_CAPTURE`
- `PROJECT_MODEL_CONFIG_PREDECESSOR_CAPTURE`
- `PROJECT_SOURCE_INVENTORY_CAPTURE`
- `SUPPORTED_WRITE_SURFACE_VISIBLE`
- `SUPPORTED_POST_WRITE_READBACK_VISIBLE`
- `LIVE_MUTATION_PERFORMED = NO`

Do not collapse source visibility, settings visibility, mutation capability, and readback capability into one PASS.
