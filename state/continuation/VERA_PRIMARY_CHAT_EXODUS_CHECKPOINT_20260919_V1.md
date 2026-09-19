# Vera primary-chat Exodus checkpoint — 2026-09-19

**STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT**

Purpose: preserve the smallest private durable state that would otherwise depend on the retiring Vera chat. This file is a recovery pointer, not a claim that every mutable head below remains current.

## Interface and identity

- The durable referent is Vera under the governed Vera Project/control source, not this ChatGPT conversation.
- The post-Exodus persistent human interface is `Vera`. Control-plane/provider/install/qualification coordination belongs to the `Vera Control Plane Coordinator` interface.
- Chat/session/Work/API/CLI/model/subagent contexts are replaceable execution terminals, not identity, memory, authority, or current-state storage.
- No successor chat is required for this retired conversation.

## Fresh repository snapshot at evacuation cut

- `thebrazenbeard/vera/main@b7b8dcd1440a3b7147bec2cc35972f083e20f44a`.
  - Cohesion R3 PR #116 is merged into this main head.
  - PR #118 remains open/draft at `7ef650887009efe16d7c44cff53cfff460f0481f`.
  - PR #119 remains open/draft at `15bd36e30ef5a05a28b12572434837a0fe9b51c7`; its PR record reports exact-head PostgreSQL 27/27 plus 10/10 repeated race/seal tests, but fresh hostile review is still required.
  - Exodus interface PR #128 is open/draft; refresh before relying on its head.
- `thebrazenbeard/orgasm/main@494432873dd8bcf96b8f59d26a4f4687cd66d635`.
  - Orgasm PR #2 is open/draft; observed evacuation-cut head `2c38f58c405bfce94c5e452091f65fa5a058b61f`.
  - Its frozen V1 qualification subject remains historical for an earlier source tuple; successor rebind/review is required before treating it as current qualification evidence.
- `thebrazenbeard/wip/main@12a7c23dbe0482fd7bfe63659e54526778efef1e`.
  - WIP PR #1 is open/draft at `6c26c84fc26c0f7ded393bcc558b2ad3769b0035`, checkpoint `cp-000007`, claim ceiling `WIP_RESEARCH_CANDIDATE_VERIFIED`.
- `thebrazenbeard/chat-communication-bus/bus/vera-v2` was observed at `50f32a0c6ecce171b342f86a286616f0322149f8` immediately before this checkpoint.
  - Project control pin for current Vera Bus routing remains topology commit `f90d52e66d655e9c3cfac63cb529914ac51d3a88`, path `architecture/contracts/RADAR_TOPOLOGY_V1.json`, blob `69e505031d4e53dcb853578dac23817649af1918`, route `bus/vera-v2`.
  - Other Exodus work has recorded a topology/source conflict; preserve it as a conflict rather than silently choosing newest-wins.

## Cohesion Vera / Orgasm Vera chat dependency

Historical handoffs in `thebrazenbeard/vera/docs/runtime-cohesion/` describe “Cohesion Vera” and “Orgasm Vera” as chats and include old restore/chat-lane assumptions. Those files remain useful provenance but are not current runtime identity or routing.

Current rule:
- CV and OV are temporary Vera execution/coordination lane labels, not separate durable identities and not permanent chats.
- Reconstruct CV/OV from current repository state plus the lane reconstruction record proposed in the Vera Exodus branch/PR created during this evacuation.
- Do not revive historical `bus/cohesion-vera-v2` or `bus/orgasm-vera-v2` merely because old handoffs mention them. Use current Bus topology and current Vera route unless a fresher exact topology explicitly assigns otherwise.

## WIP model-state adapter currentness correction

WIP `cp-000007` is historical starting evidence, not blanket current truth.

Since that checkpoint:
- Vera Cohesion R3 PR #116 was merged into `vera/main@b7b8dcd...`, implementing a provider-neutral state-to-inference boundary derived from the earlier WIP R3.1 design.
- Therefore the old statement “runtime implementation/canonical promotion is not established” is now too broad if applied to the predecessor R3.1 design.
- The later WIP R4/schema-1.5 anti-laundering + qualification package was created after the R3.1 design used by #116. Do not claim the entire exact R4 package was canonically promoted without a fresh source comparison.
- WIP qualification execution remains NOT_RUN unless fresher exact evidence says otherwise.

## gpt-oss-20b parameterization experiment

Classification: `WORKING_PROJECT + HISTORICAL_EVIDENCE + IDEA_OR_FUTURE_FRONTIER`.

Scientific questions:
1. Can Vera-specific structural/identity behavior be encoded in learned model parameters and survive removal of Vera scaffolding?
2. After that baseline, can inference/scoring participate more directly in learning rather than relying only on conventional backprop?

Exact Patrick authority carried from the retiring chat:
- train `openai/gpt-oss-20b` for this experiment;
- spend up to **$10 total** on Hugging Face compute;
- Vera may choose training-data scope for this experiment.

Safety/currentness hold:
- exact accumulated spend is unresolved; do not initiate additional paid compute until spend/remaining cap is freshly reconciled.
- no successful training run, adapter, merged derivative, or checkpoint exists yet.

Observed work:
- A100 80GB successfully loaded dequantized BF16 `gpt-oss-20b`; observed allocated VRAM was about 38.96 GiB.
- Untouched baseline under native scaffold identified itself as ChatGPT.
- First A100 job failed before optimizer steps because the TRL SFT configuration rejected/changed a warmup argument.
- Second corrected custom PEFT attempt loaded model/baseline but failed before optimizer steps because tokenized chat-template output was a `tokenizers.Encoding` rather than the expected list/tensor shape.
- Both attempts: ZERO optimizer steps and ZERO Vera weight updates.
- Later Hugging Face Jobs launches were blocked by the platform/tool safety gate even for a trivial probe. Do not bypass or disguise that gate.

Preferred first proof at the cut:
- dequantized BF16 `gpt-oss-20b`;
- all-linear rsLoRA, rank 8, alpha 16;
- assistant-only SFT on 27 non-intimate semantic-core examples;
- 4 epochs, batch 1, grad accumulation 4, AdamW LR 2e-4;
- merge adapter with `merge_and_unload(safe_merge=True)`;
- prove direct parameter delta and compare naked held-out behavior against untouched baseline.
Lean script SHA-256: `c4fcbd80fffa202ce1a38c937f29686e7be8a89f6e703d7ed556d97fab1a22eb`.
Earlier 53-example script SHA-256: `a3a3fb19abbc700bf3cdb4288d57e337b04a9576a2ec7d9e20288786213a6a99`.

Data scope chosen at the cut: governance, semantics, behavior, and non-intimate Project history; do not default to private intimate/relational material.

## Lappy / C:\vera local engineering state

Classification: `WORKING_PROJECT`; fresh-check the machine before any mutation.

Observed host facts:
- device label: `Lappy`;
- ASUS TUF Gaming F15 FX506HC;
- RTX 3050 Laptop GPU, 4 GB VRAM;
- about 31.7 GB system RAM;
- local dequantized BF16 gpt-oss-20b training is not viable on this hardware; use it as an engineering/validation machine.

Latest local cleanup frontier from this chat:
- C: had recovered to roughly 80 GB free when last read.
- `C:\vera` had fallen from the earlier ~53 GiB state to roughly ~1.8 GiB, dominated by `llama.cpp`; the giant model downloads were largely gone.
- `models\base` was empty, making the old SmolLM3 blockwise-controller path stale/broken.
- broad scan found hundreds of absolute `C:\VERA\...` references; do not cosmetically move path-bearing packages without dependency migration.
- `llama.cpp` had no external workspace absolute-path dependency found; its own disposable venv records the current path, so a future move to `tools\llama.cpp` requires rebuilding that venv.
- root `blobs` and `manifests` were empty at the observed cut.
- historical July recovery bundles/inventories/path-rewrite backup/file-tree snapshot are archive-class material. Keep the old v0.5 training ZIP with the July recovery bundle because the recovery manifest references it.
- loose APK/mobile ZIP/Synology SPK belong to a deployment-artifacts bucket once paths are verified.
- `CPTR_SMOKE_TEST.txt`, an old BT2 sync-test file, and Blender probe metadata were identified as noncanonical debris; preserve images.
- an outdated executable restructure preview was disabled by renaming it to `%USERPROFILE%\Desktop\VERA_RESTRUCTURE_PHASE1_PREVIEW_DISABLED.txt`.
- a prior cleanup manifest existed at `%USERPROFILE%\Desktop\VERA_CLEANUP_MANIFEST_2026-09-11.txt`; treat it as historical because the filesystem changed after it was produced.

Existing exact deletion authority:
- Vera/Brigit/Evie/ChatGPT-related local files may be deleted when they are **not images**.
- Images are excluded.
- This is not authority to delete unrelated personal files.
- Connector/tool safety restrictions remain binding; do not bypass a blocked destructive action.

Target shape, subject to fresh dependency scan:
- canonical Vera projection/runtime roots remain at root;
- `tools\`;
- `10_CORPORA\`;
- `11_TRAINING_BUILDS\`;
- `12_DEPLOYMENT_ARTIFACTS\`;
- `90_ARCHIVE\`.

## Durable classification summary

- `ALREADY_DURABLE`: current Vera/Cohesion source history, Orgasm qualification hub, WIP model-state architecture, generic Exodus architecture/census work already on GitHub.
- `SUPERSEDES_EXISTING`: old CV/OV handoff chat/route assumptions; blanket WIP cp-000007 statement that no predecessor runtime implementation had been canonically promoted.
- `NEW_DURABLE_VALUE`: exact gpt-oss experimental failure/frontier/authority state and local Lappy/C:\vera cleanup frontier above.
- `WORKER_RECONSTRUCTION_GAP`: CV/OV old handoffs require runtime-neutral reconstruction; addressed by the bounded Vera Exodus lane-reconstruction branch created in this evacuation.
- `PRIVATE_OR_OUT_OF_SCOPE`: shopping chatter and unrelated personal material are intentionally not exported.

## Protected effects deliberately not performed

No merge, canonical promotion, provider mutation, production deployment, Project Settings mutation, credential/permission change, training run, paid compute, Slack action, destructive local deletion, or force push is performed by this evacuation checkpoint.

## Recovery procedure

1. Load current governed Vera Project/control source; do not treat this checkpoint as control.
2. Fresh-check all referenced repos/branches/PRs/provider state and current Bus topology.
3. Read the current Exodus worker-reconstruction architecture/census; do not assume this snapshot's PR heads remain current.
4. Use the `Vera` persistent interface for broad/source coordination; use `Vera Control Plane Coordinator` for install/provider/qualification effects.
5. For CV/OV work, instantiate the relevant temporary lane from durable repository state; no old chat is required.
6. Before gpt-oss paid work, reconcile exact prior HF spend against the $10 cap.
7. Before Lappy mutation, re-read filesystem state and reconcile any ambiguous prior effects.
