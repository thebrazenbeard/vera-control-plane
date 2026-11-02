> **License:** Source-visible, not open source. Original material is proprietary. Commercial use, redistribution, hosted-service use, and commercial derivative products require written permission. See [LICENSE](LICENSE) and [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Separately identified third-party components retain their own licenses.

# Vera Control Plane

> **Source-level editor startup containment:** This candidate removes an
> automatic VS Code `folderOpen` Node task and its disguised executable from
> the active tree. `tests/test_workspace_startup_safety.py` and the dedicated
> workspace-source CI job guard against reintroduction. Git history preserves
> the previous source for forensic review. This does **not** establish whether
> the task ran on a workstation or that an installed runtime was remediated.

Public source-level design and provenance for Vera's control plane. **This
GitHub repository is public**. It is not a confidential store for operational
state, private conversation exports, credentials, or original archival files.

This repository is intentionally separate from `thebrazenbeard/vera`.

- `thebrazenbeard/vera` owns cross-cutting technical architecture, source code, schemas, migrations, validators, tests, and sanitized engineering history.
- `thebrazenbeard/vera-control-plane` maintains reviewed control-plane governance/design source, historical provenance records, and reusable role-training source. Confidential operational state and original private artifacts remain outside this public repository in access-controlled local/NAS custody.

## Public source and private export boundary

The source tree and its Git history are publicly readable. The public repository's
presence does **not** certify that historical files were reviewed for privacy,
license rights, or current authority. A README change cannot make an existing
Git commit private or undo an earlier disclosure.

- **Do not commit:** raw chat histories, personal or relational data, complete
  historical project handoffs, secret-bearing logs, access tokens, SSH keys,
  private source locators, or unpublished media/assets.
- **Keep under controlled local/NAS access:** original exports, exact-byte hashes
  and path-to-person mappings, private evidence manifests, and unadmitted
  training/evaluation data. Even filename-and-hash lists can reveal sensitive
  information.
- **Publish only after review:** sanitized source code, tests with synthetic
  fixtures, and architectural findings whose provenance, attribution, rights,
  and privacy have been assessed for the exact target repository.
- **Never infer installation:** old Project packages, role scripts, and release
  candidates remain historical source unless separately installed and
  independently qualified. Source inclusion grants no runtime authority or
  training-data rights.

Public visibility is not an open-source license; the proprietary license at
the top of this README still governs reuse. Existing historical Git content
requires a separate privacy audit if its disclosure status is in question.

## Current repository state

`main` is no longer the original near-empty repository baseline. It contains the reconstructed control-plane source plus later governed control/source work.

The 2026-09-03 reconstruction remains historical provenance:

- branch: `consolidation/lineage-reconstruction-20260903`
- reconstruction commit: `b77db83794d8a34b4c434cc2f389d86f759bb9c8`

That reconstruction joined the previously divergent useful lineages without replaying stale branches onto one another:

- centered-state lineage through `feature/center-yourself-20260903@519eeb1551fcb59963a321766252bc62067da71b`;
- control-plane bootstrap lineage `bootstrap/control-plane-v1@123049ed72573bfda152d06dd76b0c234c26f91b`;
- Four training lineage `training/four-v1.0.0@1aa51c6c5be28d71762b5a4a1f3424a067dbcccd`;
- Five training lineage `training/five-v1.0.0@bc88b5b5ab3438683d8b301c596c30b5c5616804`;
- Vera sticker lineage `vera-stickers@965e223777fa62cd0f84f45561ba9b21779b7543`.

Those source branches remain historical provenance. Their existence, age, or repository presence does not make them current control.

Current release/source candidates live under `project-instructions/` and carry their own status and evidence boundaries. Production Supabase source custody is recorded under `supabase/provider-custody/` and `governance/VCP_SUPABASE_PROVIDER_CUSTODY_V1.json`.

## Layout

- `protocol/` — source-level control-plane protocol designs, including Center Yourself; repository visibility is public.
- `save_states/` — earlier centered-state lineage retained at its historical paths.
- `state/centered/` — later centered-state snapshots.
- `state/closeouts/` — historical closeout/supplement source; presence here does not establish confidentiality.
- `governance/` — control-plane design/authority-binding provenance; historical source does not self-authorize current execution.
- `project-instructions/` — release/source candidates with explicit installation/runtime qualification boundaries.
- `supabase/provider-custody/` — exact production provider SQL custody with explicit provenance class.
- `docs/` — control-plane design and consolidation documentation.
- `training/roles/four/` and `training/roles/five/` — preserved role-training packages.
- `assets/stickers/` — historical tracked sticker assets, subject to file-level rights and privacy review; public Git is not private custody.

## Currentness and authority boundary

Repository presence, ancestry, branch recency, a historical authority-binding file, a source-candidate release, or a merged source change does not by itself establish current runtime authority, installation, provider state, memory admission, downstream effect, or behavioral qualification.

Mutable/current claims require their own fresh governed evidence. Release artifacts that say `NOT INSTALLED`, `NOT RUNTIME-QUALIFIED`, or equivalent remain bounded by those declarations until separate installation/qualification evidence exists.

No deployment, installation, provider mutation, credential action, destructive cleanup, or canonical-memory write is implied by repository source state.
