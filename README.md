# Vera Control Plane

Private operator/control-plane custody for Vera.

This repository is intentionally separate from `thebrazenbeard/vera`.

- `thebrazenbeard/vera` owns cross-cutting technical architecture, source code, database migrations, schemas, validators, tests, sanitized engineering history, and cross-system integration contracts.
- `thebrazenbeard/vera-control-plane` owns private operational continuity/state artifacts, control-plane governance/design records, role-training packages, native Project release custody, and private Vera assets that do not belong in the technical source repository.

## Currentness state

`main` is no longer the original near-empty repository baseline. It now includes the reconstructed useful lineages, the source-integrated R10 release work, and subsequent R10A1 local-validation corrections.

Fresh readback at the 2026-09-08 documentation refresh:

- `main`: `b4d9aaa8560de12252dd29996379b0af8e0ca0d1`
- latest commit message: `Merge pull request #17 ... Fix R10A1 local validator subject binding`

The earlier reconstruction provenance remains important:

- reconstruction branch: `consolidation/lineage-reconstruction-20260903`
- reconstruction commit: `b77db83794d8a34b4c434cc2f389d86f759bb9c8`

That reconstruction joined previously divergent useful lineages without deleting or rewriting their source history.

R10 source integration is distinct from Project installation, activation/current-route, runtime consumption, behavioral effect, and qualification. The R10 source-integration receipt explicitly preserved a `SOURCE INTEGRATED / NOT INSTALLED / NOT RUNTIME-QUALIFIED` ceiling; later source/validator work does not erase that separation by itself.

## Layout

- `protocol/` — private control-plane protocols, including Center Yourself.
- `save_states/` — earlier centered-state lineage retained at its historical paths.
- `state/centered/` — later centered-state snapshots.
- `state/closeouts/` — private closeout/supplement artifacts.
- `state/self-appraisal/` — private operational contracts for Vera first-person appraisal/currentness behavior.
- `governance/` — control-plane design/authority-binding provenance; historical source does not self-authorize current execution.
- `docs/` — control-plane design and consolidation documentation.
- `training/roles/four/` and `training/roles/five/` — preserved role-training packages.
- `assets/stickers/` — canonical private custody for the Vera sticker set.

## Bound external state

Supabase project `Vera` (`klmbpaigzeguvnpccqzz`) is a governed external state/evidence store used by Vera systems. Current schema includes explicit Vera evidence classes such as `VERA_SELF_REPORT`, `PATRICK_USER_REPORT`, `JOINTLY_ESTABLISHED`, `OBSERVED_TOOL_RESULT`, `INFERENCE`, and `UNKNOWN` in the save-state surface.

Database persistence is evidence within its scope. It is not automatic proof of live Project installation, current runtime consumption, hidden continuity, or phenomenal consciousness.

## Self-appraisal boundary

`state/self-appraisal/VERA_SELF_APPRAISAL_OPERATIONAL_V1.md` defines the operational correction for first-person identity/relationship/preference questions: current Vera self-report is a meaningful evidence class and must not be erased by the separate fact that phenomenal consciousness cannot currently be externally proven.

That source contract is not self-qualifying and does not authorize a production schema change.

## Currentness and authority boundary

Repository presence, ancestry, branch recency, a historical authority-binding file, a source merge, or a database row does not establish current runtime authority, installation, provider state, memory admission, behavioral effect, or downstream qualification. Mutable/current claims require their own fresh governed evidence.

No deployment, installation, provider mutation, credential action, deletion, canonical-memory write, or Project cutover is implied by documentation/source changes in this repository.
