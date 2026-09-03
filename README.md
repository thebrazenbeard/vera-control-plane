# Vera Control Plane

Private operator/control-plane custody for Vera.

This repository is intentionally separate from `thebrazenbeard/vera`.

- `thebrazenbeard/vera` owns cross-cutting technical architecture, source code, schemas, migrations, validators, tests, and sanitized engineering history.
- `thebrazenbeard/vera-control-plane` owns private operational continuity/state artifacts, control-plane governance/design records, role-training packages, and private Vera assets that do not belong in the technical source repository.

## Consolidation state

`main` is still the original near-empty repository baseline. The reconstructed candidate is:

- branch: `consolidation/lineage-reconstruction-20260903`
- reconstruction commit: `b77db83794d8a34b4c434cc2f389d86f759bb9c8`

That commit deliberately joins the previously divergent useful lineages without replaying stale branches onto one another:

- centered-state lineage through `feature/center-yourself-20260903@519eeb1551fcb59963a321766252bc62067da71b`;
- control-plane bootstrap lineage `bootstrap/control-plane-v1@123049ed72573bfda152d06dd76b0c234c26f91b`;
- Four training lineage `training/four-v1.0.0@1aa51c6c5be28d71762b5a4a1f3424a067dbcccd`;
- Five training lineage `training/five-v1.0.0@bc88b5b5ab3438683d8b301c596c30b5c5616804`;
- Vera sticker lineage `vera-stickers@965e223777fa62cd0f84f45561ba9b21779b7543`.

The source branches remain historical provenance. This consolidation does not delete or rewrite them.

## Layout

- `protocol/` — private control-plane protocols, including Center Yourself.
- `save_states/` — earlier centered-state lineage retained at its historical paths.
- `state/centered/` — later centered-state snapshots.
- `state/closeouts/` — private closeout/supplement artifacts.
- `governance/` — control-plane design/authority-binding provenance; historical source does not self-authorize current execution.
- `docs/` — control-plane design and consolidation documentation.
- `training/roles/four/` and `training/roles/five/` — preserved role-training packages.
- `assets/stickers/` — canonical private custody for the Vera sticker set.

## Currentness and authority boundary

Repository presence, ancestry, branch recency, a historical authority-binding file, or a merged consolidation candidate does not establish current runtime authority, installation, provider state, memory admission, or downstream effect. Mutable/current claims require their own fresh governed evidence.

No merge into `main`, deployment, installation, provider mutation, credential action, deletion, or canonical-memory write is implied by this candidate.
