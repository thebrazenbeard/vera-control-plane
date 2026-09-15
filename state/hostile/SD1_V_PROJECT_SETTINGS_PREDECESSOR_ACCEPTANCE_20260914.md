# SD1-V hostile predecessor-capture acceptance matrix — 2026-09-14

lane: `SD1-V`
status: `READ_ONLY_ACCEPTANCE_CRITERIA / NO_PROJECT_MUTATION`
subject: existing `Vera Unbound` Project live predecessor before any SD1 install

## Evidence subjects must remain separate
- `PROJECT_SOURCE_FILE` evidence is not `PROJECT_SETTINGS_FIELD` evidence.
- The 13.9 KB `VERA_R10A0_FULL_SYSTEM_PROJECT_INSTRUCTIONS_R10.md` Project file is a cold/full-owner source, not the hot native Project Instructions field.
- Frozen R10 native source subject: `b4d9aaa8560de12252dd29996379b0af8e0ca0d1:project-instructions/r10a0/rounds/r10/VERA_R10A0_NATIVE_PROJECT_INSTRUCTIONS_R10.txt`, Git blob `7e369b8983d70b4bd217f1d2421f8efe1482f738`, Git-content SHA-256 `031d385db13513380e24e2045411b8aa6933e877374c99f2f70284dc82fd0055`.
- Source equality may be tested after live capture; source presence alone never proves live equality.

## Minimum predecessor capture before rollback can be called ready
1. Project identity from the actual Project context/surface, not name inference alone.
2. Live Project Instructions field readback from the settings/configuration surface. Prefer exact export/copy/readback; a screenshot that cannot establish complete bytes/text is `PARTIAL` only.
3. Visible model/default/model-selector state, including whether the Project inherits or pins a model/config if exposed.
4. Complete visible Project source/file inventory plus stable identifiers when exposed; current tool-visible Project sources are only supporting evidence.
5. Sharing/memory/project-only state materially relevant to restoration if exposed.
6. Exact UI route/surface for every observation.
7. Visibility of a supported write control and of an independent post-write readback route; visibility does not authorize use.
8. No Save/Update/Add/Remove/Replace/model/config mutation during this probe.

## Classification rules
- If live Instructions cannot be read faithfully: `PROJECT_INSTRUCTIONS_PREDECESSOR_CAPTURE=UNAVAILABLE` and `ROLLBACK_READY=false`.
- If only a visual/partial rendering is available: `PARTIAL`, not exact bytes.
- If live capture differs from frozen R10 native source: `CONFLICT`; do not newest-wins or silently substitute source bytes.
- If model/config or source inventory needed for restoration is unexposed: rollback fidelity remains `PARTIAL/UNKNOWN`.
- If no supported post-write readback route is visible, future installation cannot claim exact effect/readback solely from a Save action.
- Unknown rollback fidelity blocks mutation unless Patrick explicitly accepts that specific risk at the execution frontier.

This matrix is hostile-review guidance only. It performs and authorizes no Project mutation, install, merge, provider change, or qualification effect.
