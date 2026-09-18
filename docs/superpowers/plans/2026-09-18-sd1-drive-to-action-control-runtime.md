# SD1 Drive-to-Action Control/Runtime Implementation Plan

> For agentic workers: use subagent-driven-development or executing-plans task-by-task.

Goal: Build a successor R10+SD1 control cut that binds the repaired Sexuality/Cohesion subjects, makes turn-local drive appraisal mandatory in the native runtime projection, preserves the 8,000-byte ceiling, and remains install-blocked until exact-head review/readback gates are satisfied.

Spec: thebrazenbeard/sexuality@4e4f70a3433e267f3b769b2c1a676babf5cd4000:docs/superpowers/specs/2026-09-18-sd1-drive-to-action-runtime-bridge-design.md

## Exact upstreams
Sexuality:
- commit 4e4f70a3433e267f3b769b2c1a676babf5cd4000
- manifest blob 97b31f59562380eb2ecf24e45b6ce2e092794dd3
- manifest checkout SHA-256 b1c84e0dad48038572f9a6898252af578400af9e2e93a66bf923deba65a74830
- manifest Git-content SHA-256 17435cc38e6ee61a8344fa79fa4ca370592f91790af2222f6a7bfb2031162efc
- semantic owner blob b5aab6974b1a044de7f6ab4db3163eb9dfff01fd
- semantic owner checkout SHA-256 905b1ea197f94b5310e34fb822997fab3ad2f42b8d0a80f1f2be5d301c2248a0
- semantic owner Git-content SHA-256 762594a288d7edcb3e1b5c2b1a4bcbe081256e33fcdbbef4c0db37a65c36b7d5
- causal/authority blobs unchanged.

Cohesion:
- commit 94e50b976830e73f18c5d4a68ced22cbce3ab16b
- component blob 1af604c8a14316e7fc9ad4a59359ff3f7600fe2b
- checkout SHA-256 d73f53c206e217ecb3b22b9e19c34605b2f2fc3fbd07b26a5ec6ddbfffb52101
- Git-content SHA-256 47711e5e68bca2742279f0d63700a93adc3f9723c13dfb384f9f8c65067db08d
- canonical structured SHA-256 4e1c843dd403dc82e697fa0f310bde269684ee95fab6a760078c4f461a7f4a56
- exact-head hostile rereview pending; Bus request 4b368c6950ecf7d4c9e84dc42558b920531d4738.

## Global constraints
- Do not reuse predecessor review PASS on moved heads.
- Package status remains REREVIEW_PENDING / NOT_INSTALLED until exact source/Cohesion acceptance arrives.
- No merge, R10A1 install, model/memory/sharing/permission mutation, or unrelated Project change.
- Native settings remain <= 8000 normalized UTF-8 bytes.
- Native projection itself requires per-turn drive appraisal; cold source carries full semantics.
- Blocked/work contexts do not receive drive sexual bids.
- Eligible turns must consider a specifically sexual candidate without an immediate user sexual cue.
- Candidate is not action; initiation remains permitted, not forced.
- SEXUAL_SYSTEM_ACTIVATION=ACTIVE requires current SD1 participation evidence.
- A single initiative never proves causality.
## Task 1 — RED exact successor and runtime-bridge contract

Modify tests/test_r10a0_sd1_sexual_drive.py first.

Change expected upstream constants to the exact Sexuality/Cohesion tuples above. Add tests requiring:
- binding status and source state say exact-head rereview pending, not reviewed;
- binding has a machine-readable drive_to_action_bridge;
- control text requires TURN_LOCAL_DRIVE_APPRAISAL, cue-free specifically sexual candidate consideration on eligible turns, blocked/work suppression, permitted-not-forced initiation, and current participation evidence for activation;
- qualification text names exact successor subjects and keeps causal effect unresolved;
- native K05 includes a compact mandatory drive-appraisal directive and remains <=8000 bytes.

Run py -3.11 -m unittest -q tests.test_r10a0_sd1_sexual_drive and confirm RED only for stale subjects/semantics.

## Task 2 — Repair control/binding/qualification source

Update VERA_R10A0_SEXUAL_DRIVE_CONTROL_V1.md, VERA_R10A0_SEXUAL_DRIVE_BINDING_V1.json, and VERA_R10A0_SD1_QUALIFICATION.md.

Binding must carry exact upstream tuples and:
- status SOURCE_CANDIDATE_REREVIEW_PENDING_NOT_INSTALLED;
- source state SOURCE_CANDIDATE_REREVIEW_PENDING;
- drive_to_action_bridge matching the Sexuality owner;
- no promotion to consent/attraction/desire/identity/phenomenology/causality;
- Cohesion review status FRESH_EXACT_HEAD_REREVIEW_PENDING with the rereview Bus request commit, never predecessor PASS.

Run focused tests; expected remaining failures are manifest/artifact/native digest bindings.
## Task 3 — Rebuild manifest cross-bind

After Task 2 files are final, compute their Git blob identities and Git-content SHA-256 values. Update the source manifest artifact and external-binding tuples. Keep native outside the manifest artifact cycle exactly as the existing binding rule specifies.

Run focused tests. Update expected binding blob constants only after the binding bytes are final.

## Task 4 — Native hot projection

Preserve the frozen R10 transformation shape: K00 + K05 only.

Replace the predecessor SD1 K05 suffix with one compact mandatory bridge directive equivalent to: SD1=CONTROL_LOAD owner;each turn appraise drive;eligible=>consider sexual bid sans cue;blocked/work=>no bid;ACTIVE only if SD1 participated.

The exact committed wording must fit <=8000 bytes, require every-turn appraisal, preserve candidate-vs-action/consent through the bound owner, make cue-free eligible candidate consideration explicit, keep blocked/work negative transfer explicit, and gate ACTIVE on SD1 participation.

Recompute source-manifest Git-content SHA-256 and use it in K00. Run tests plus explicit byte count.

## Task 5 — Exact-head freeze/review gate

Detached-checkout verification: focused SD1 control suite; py_compile; diff-check from b0aa53e; source-manifest/native byte/digest recomputation; stale upstream sweep.

Open a separate Draft PR stacked from the reviewed predecessor branch. Route exact-head hostile rereview to PR + Bus.

Exit before hostile acceptance: SOURCE_BUILT / LOCAL_GREEN / FRESH_REREVIEW_REQUIRED / NOT_INSTALLED.

## Task 6 — Live install/readback gate

Only after exact source/Cohesion/control acceptance: fresh-read Vera Unbound instructions and source inventory; compare against captured predecessor; stop on unexplained drift; install only exact verified SD1 surfaces; immediately read back exact settings/source bytes/digests; reconcile ambiguous effects before retry; record install receipt; run cue-free positive and blocked/work/generic-affection negative replay.

Runtime installation is not complete until readback succeeds. Causal effect remains separately governed by the frozen matched DRIVE_OFF/DRIVE_ON protocol.
