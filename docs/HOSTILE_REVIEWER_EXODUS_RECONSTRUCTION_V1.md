# Hostile Reviewer — Exodus Reconstruction V1

Status: **STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT**

Hostile Reviewer is a Vera runtime feature, not a permanent worker identity and not a ChatGPT conversation.

## Durable ownership

Runtime source:
- repository: `thebrazenbeard/vera`
- Draft PR: `#127`
- branch: `work/hostile-reviewer-runtime-v1-20260919`

Control source:
- repository: `thebrazenbeard/vera-control-plane`
- Draft PR: `#47`
- branch: `work/hostile-reviewer-toggle-v1-20260919`

Future persistent interface for control/install/qualification coordination:
`Vera Control Plane Coordinator`

That interface is not the Hostile Reviewer and does not own its truth. It coordinates the durable source/control state.

## Feature identity

The feature is a response-stage adversarial second pass.

It is:
- toggleable `OFF|ON`;
- advisory only;
- exact-primary-answer bound;
- externally visible as a concise `HOSTILE REVIEWER` blockquote;
- ineligible to promote authority, evidence, effects, memory, identity, preference, desire, consent, installation, or qualification.

It is not:
- a second Vera identity;
- a standing persona;
- a durable autonomous agent;
- a permanent chat;
- a provider selector;
- a source of effect authority.

## Fresh-runtime reconstruction

A fresh runtime should:

1. Fresh-check PR #127 and PR #47 exact heads.
2. Read `governance/VERA_HOSTILE_REVIEWER_BINDING_V1.json`.
3. Verify the runtime/control blobs named by that binding still exist on the claimed commits.
4. Read `governance/VERA_HOSTILE_REVIEWER_CONTROL_V1.json`.
5. Read `state/features/hostile-reviewer-v1.json`.
6. Read the R10 Hostile Reviewer behavior patch.
7. Run the focused runtime and control tests.
8. Read current hosted workflow state separately from focused-test state.
9. Before any installation/activation claim, obtain actual native Project/runtime install + current-route + readback evidence.
10. Before changing project-wide mode, establish the currently installed control source and current generation; source Git state alone is not live activation.

No retired chat, chat URL, conversation ID, or browser-tab continuity is part of this reconstruction sequence.

## Current evidence ceiling

Source implementation and focused tests are distinct from:
- merge;
- Project installation;
- current runtime consumption;
- all-chat propagation;
- observed cross-chat behavior;
- causal qualification.

Do not collapse those labels.

## Authority

The Exodus authorizes source/reconstruction/checkpoint work only.

Merge, native Project installation/settings mutation, provider mutation, and project-wide live activation remain protected effects requiring Patrick's exact authority.

## Current source default

The durable source state defaults to `OFF`.

That is not evidence that a live installed runtime is currently OFF; live mode requires current installed-source/readback evidence.

## Next safe frontier

The next source-level work is hostile/independent review of the exact bound source cut and reconciliation of branch-wide CI failures.

The next operational frontier—native installation plus fresh-chat ON/OFF replay—is protected and must not execute without exact authority.
