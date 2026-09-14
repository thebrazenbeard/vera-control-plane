# SD1-V Project install gate — read-only assessment

lane: `SD1-V`
status: `PREDECESSOR_SOURCE_CAPTURE_PARTIAL_LIVE_SETTINGS_READBACK_UNAVAILABLE`

## Independently observable in this runtime
- Project identity/context: Vera Unbound is the current governed Project context, but this is conversational/runtime context rather than an independent provider Settings receipt.
- model identity exposed to this lane: GPT-5.6 Sol.
- Project-backed file surface currently exposes exactly two R10 files:
  - `VERA_R10A0_FULL_SYSTEM_PROJECT_INSTRUCTIONS_R10.md` — local SHA-256 `e797d1a6e973b06ab3e58f9157aabb500ebfdbee1ee6c8da801bc202b6767a2f`, 13,987 bytes;
  - `VERA_R10A0_PROJECT_SOURCE_MANIFEST_R10.json` — SHA-256 `b7c70b1ad2c3bc533c7560320fb9a03b827f3eafad6296894216d75281b8dca1`, 6,375 bytes.
- R10 source manifest binds owner/registry/qualification/rollback/topology provenance, but its own status is a frozen source-candidate artifact; source bytes do not prove live Settings equality.
- frozen R10 rollback subject exact blob `b08be49d3f3a17aa0723a54356f4c95cbc1cb70b` states `PARTIAL_PRE_CUT_CAPTURE_NOT_EXECUTABLE_ROLLBACK` and requires provider-live Project Settings bytes plus complete provider-live Project Source inventory/bytes/digests before cutover.

## Not independently observable / not available to this lane
- exact machine-readable ChatGPT Project Settings/Instructions bytes immediately before an SD1 mutation;
- a provider-generated Project source inventory distinct from the Files surface;
- provider-native activation/current-routing state;
- a supported in-chat Project Settings mutation primitive with deterministic post-save byte readback;
- independent automated restoration primitive.

## Gate state
`PROJECT_PREDECESSOR_ROLLBACK_FIDELITY = PARTIAL_SOURCE_CAPTURE_ONLY / NOT_INSTALL_READY`
`PROJECT_INSTALL_READBACK = UNAVAILABLE_IN_SD1-V_CURRENT_TOOLING / NOT_ATTEMPTED`
`UNRELATED_SETTING_PRESERVATION = NOT_VERIFIABLE_BEFORE_SUPPORTED_MUTATION_READBACK_PATH`

No live mutation is approved from this evidence. Before cutover, SD1-E or another authorized executor must demonstrate a supported mutation/readback path and capture the exact live predecessor surface. If exact restoration remains technically unavailable, rollback fidelity stays PARTIAL/UNKNOWN and Patrick must explicitly accept that risk before cutover. Source files, commits, screenshots without byte-equivalent readback, or a worker statement that Save was clicked do not satisfy this gate.