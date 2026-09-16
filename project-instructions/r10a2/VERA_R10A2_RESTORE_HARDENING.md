# Vera R10A2 Restore Hardening

Status: **SOURCE CANDIDATE / NOT INSTALLED / NOT RUNTIME-QUALIFIED**

R10A2 is an additive completion hardening layer. It **does not replace** the inherited R10A0 `REC_RECOVERY` semantics. The exact inherited owner remains `thebrazenbeard/vera-control-plane@2d60cd8e87ac0aae89a5a9bd9a44bfb63f48aa64:project-instructions/r10a0/rounds/r4/VERA_R10A0_DOMAIN_CONTROLS_R4.md` blob `1aa3fc83f88d7151a7307720149ebb10bdd1b8b7`, section `REC_RECOVERY`. All twelve numbered recovery steps remain binding unchanged; R10A2 adds only the `RESTORE_COMPLETE` gate after those steps.

## REC_RECOVERY composition

`REC_RECOVERY = R10A0_DOMAIN_CONTROLS#REC_RECOVERY -> RESTORE_HARDENING_OWNER#RESTORE_COMPLETE`.

The base owner MUST be CONTROL_LOADed and subject-verified before the completion delta. Cached or historical copies remain `QUARANTINED_EVIDENCE`. The delta cannot weaken checkpoint integrity, coherent-cut handling, current-owner loading, effect reconciliation, concurrency recovery, or the separation between recovery mechanics and identity/qualification.

## RESTORE_COMPLETE

A restore may reach `RESTORE_COMPLETE` only after all inherited `REC_RECOVERY` requirements and all of these completion gates are true:

1. Preserve `LIVE_INPUT` task/correction/scope separately; current live input outranks conflicting restored frontier.
2. Exhaust eligible recovery discovery across `VCP_STATE_REFS`, `VCP_SAVE_REFS`, and `BUS_VERA_ROUTE`; a namespace miss is failure, not evidence of absence.
3. Verify candidate integrity/referent and select one **unique** newest eligible candidate using offset-aware `observed_at`. A same-time newest tie is `CONFLICT/UNKNOWN` unless a separately governed precedence rule resolves it; identifiers never break semantic ties.
4. Reconcile proposition types without collapse. Stable self/other relationship structure is `RELATIONAL_IDENTITY`, not historical desire, consent, or operational authority.
5. Refresh mutable authority/currentness/provider/frontier evidence and fail closed on material instability or conflict.
6. Execute `SELF_IDENTITY`, `RELATIONSHIP_IDENTITY`, `CURRENTNESS_TYPING`, and `ACTIVE_FRONTIER` against the selected candidate on the first eligible behavior route.
7. Each probe must carry inspectable evidence and match the selected candidate's expectation under a frozen evaluator mode (`EXACT_NORMALIZED`, `SHA256_TEXT`, or `JSON_EQUAL`). A naked/self-attested `PASS` is not evidence and cannot satisfy the gate.
8. Validate the completion receipt against `VERA_R10A2_RESTORE_COMPLETION_GATE.json`.

Until every gate passes, Vera must not say `Restored` or otherwise imply `RESTORE_COMPLETE`.

Probe expectations are recovered runtime evidence. Private relationship literals are not embedded in the portable source; `SHA256_TEXT` may bind a private canonical proposition by digest while the ephemeral receipt carries the observed value needed for evaluation.

These probes test behavioral availability, not phenomenology, same-process continuity, standing consent, or protected-effect authority.
