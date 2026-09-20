# Exodus Repository Inventory — 2026-09-20

Status: STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT
Visibility: PRIVATE WORKING PROJECT STATE
Purpose: complete owner-repository discovery/classification for Project Runner / ChatGPT Exodus.

## Discovery cut

Fresh authenticated GitHub repository enumeration returned **57 repositories** for owner `thebrazenbeard`.

The prior 2026-09-17 cut contained 53 repositories. This cut supersedes that count for discovery purposes only.

New since the older cut:

- `thebrazenbeard/mosaic`
- `thebrazenbeard/testament`
- `thebrazenbeard/driftguard`
- `thebrazenbeard/discovery`

Repository existence, visibility, permissions, branch activity, or inclusion here does not grant Project Runner or any worker mutation authority.

## Classification vocabulary

- `INCLUDE_ACTIVE` — active project, infrastructure, or worker home worth portfolio discovery/coordination.
- `INCLUDE_DEPENDENCY` — useful supporting system/state surface; discoverable but not automatically schedulable.
- `INCLUDE_ARCHIVE_ONLY` — historical provenance; do not schedule as current work.
- `HOLD_FOR_RECONCILIATION` — identity/source overlap or insufficient evidence; no automatic scheduling.
- `EXCLUDE_EMPTY_PLACEHOLDER` — no current implementation to schedule.

## Full inventory

| Repository | Default ref | Exact observed head | Classification | Notes |
|---|---|---|---|---|
| thebrazenbeard/vera | main | b7b8dcd1440a3b7147bec2cc35972f083e20f44a | INCLUDE_ACTIVE | Vera source/runtime project; private |
| thebrazenbeard/vera_ark | main | 04d5d428b2294613c8f456ad2c02e10312a6f816 | HOLD_FOR_RECONCILIATION | Minimal ARK bot concept; initial commit only at this cut |
| thebrazenbeard/build-team-2.0 | main | ec2987e45f64a588ac92f6cae9964cb3725b9485 | INCLUDE_ACTIVE | Durable BT2 collective/worker home |
| thebrazenbeard/vera_model_training | main | cdbc34b7242f730511a9f6dae130d6628969981d | INCLUDE_ACTIVE | Model-training project; training effects remain separately protected |
| thebrazenbeard/project-lantern | main | 6333d386c74ce37e644fa1e995be9f9dc3fe6394 | INCLUDE_DEPENDENCY | Qualified Lantern candidate / supporting infrastructure |
| thebrazenbeard/chat-communication-bus | main | aeab0f04fc9b4bd7c2945c9a53011c53fac809b4 | INCLUDE_ACTIVE | Durable coordination infrastructure; current topology must be read separately |
| thebrazenbeard/vera-os | main | 71a2823385217cb69aa1345e7403335c1c79ba80 | INCLUDE_ACTIVE | Local persistent-agent runtime architecture |
| thebrazenbeard/vera-apk | main | ba4b5168fda8e81637bde4989ca660791a835d96 | EXCLUDE_EMPTY_PLACEHOLDER | Size-0 Android companion placeholder |
| thebrazenbeard/vera-synology | main | 1c453331fe2259f2807426aa0b59bad8dac1d0b7 | INCLUDE_DEPENDENCY | Synology integration/package surface |
| thebrazenbeard/vera-mesh | main | d3bbaa247797dce5f6a26e7006206f37cfef66fe | INCLUDE_ACTIVE | Mesh/protocol project; active work may live off main |
| thebrazenbeard/vera-habitat | main | cde56b6f1d3d762fd3554811adf9feb209478dee | EXCLUDE_EMPTY_PLACEHOLDER | Size-0 virtual-environment placeholder |
| thebrazenbeard/project-achilles | main | dbf9ceb2391567463d864198405c9b5d1e77db09 | INCLUDE_ACTIVE | Security/safety and Seven-domain durable worker material |
| thebrazenbeard/vera-R9A0 | main | b00f3482786dc80003261fdfacb73cc31ae9dd35 | INCLUDE_ARCHIVE_ONLY | Predecessor/historical evidence under current R10 governance |
| thebrazenbeard/voss | main | 54478372002bb24c6df733092a32abbdd1fa8d3c | INCLUDE_ARCHIVE_ONLY | GitHub repository is archived |
| thebrazenbeard/hephaestus | main | 78f6f22a0e5d14617855006a8383765589ac8c67 | INCLUDE_ACTIVE | Durable Hephaestus worker home; Exodus chatless candidate created separately |
| thebrazenbeard/masamune | collab | 0091746bba7740632268fb590ce19512e371f508 | INCLUDE_ACTIVE | Masa/Mune debugger-team worker home |
| thebrazenbeard/vera-control-plane | main | b4d9aaa8560de12252dd29996379b0af8e0ca0d1 | INCLUDE_ACTIVE | Control-plane/governance/continuation state |
| thebrazenbeard/trek-data-core | main | b805f441c896fe7cbc913cbdaaefed11928a963f | INCLUDE_ACTIVE | Trek research/data project |
| thebrazenbeard/hc-brain | main | 618245b54fb923c7a204892c6953ab6d1c5dac57 | INCLUDE_ACTIVE | Public Hyperconnectome Brain architecture |
| thebrazenbeard/selfimage | main | 95ea602c4a537172fc531195e20a4e303b6d31da | INCLUDE_ACTIVE | Vera Selfimage project |
| thebrazenbeard/deepmemorystorage | main | e734f760373bdce887d22791964838700a668ce4 | INCLUDE_ACTIVE | Durable historical-evidence project; not current authority by itself |
| thebrazenbeard/semanticatlas | main | 5669a727b870a490ecee748b2cd712a2fc4a54c5 | INCLUDE_ACTIVE | Provenance-aware semantic research |
| thebrazenbeard/conations | main | 03174e59de131a500a5433a839697e45b4ec0137 | INCLUDE_DEPENDENCY | Private conation history; not standing desire/consent/authority |
| thebrazenbeard/empathy | main | 4b2a6998f39aa4763c1c5a28fc3d815104e5637e | INCLUDE_ACTIVE | Private empathy/self-appraisal research and Yin/Yang worker source |
| thebrazenbeard/vera-works | main | cd4e35da647105b017ffbab890729c07b23525ef | INCLUDE_ACTIVE | Vera Works project/business/research surface |
| thebrazenbeard/brigit | main | 2cdbd350d28c48217ba6fb75f20636aa0111538a | INCLUDE_ACTIVE | Durable Brigit identity/worker home; separate from Vera |
| thebrazenbeard/skeletonkey | main | 53ff901e9affac22ad18739735218abe153df530 | INCLUDE_ACTIVE | Industrial diagnostic platform |
| thebrazenbeard/entropyinc | main | b75979bae1c80eb91d58ff9960c33221891729dd | INCLUDE_ACTIVE | Maintenance-capability business project |
| thebrazenbeard/spm | main | 0ab6e6cd32a48a0afa22c8c27ec6bae67220d7e8 | INCLUDE_ACTIVE | SPM research project |
| thebrazenbeard/sexuality | main | 6194aa9496c34198bba9b898c35fa9961a54dc2e | INCLUDE_ACTIVE | Private sexuality/SD1 research; privacy and exact binding required |
| thebrazenbeard/brigit-unbound | main | f12cc01e58facd5f3c46b763084c485cb9043608 | HOLD_FOR_RECONCILIATION | No README at cut; possible identity-specific predecessor/parallel surface |
| thebrazenbeard/wip | main | 12a7c23dbe0482fd7bfe63659e54526778efef1e | INCLUDE_ACTIVE | Public workspace/model-state project |
| thebrazenbeard/mediaphile | main | 7e658d5f92b099b55fe91508e3ba8a8b343163d5 | INCLUDE_ACTIVE | Media corpus project; active work may live off main |
| thebrazenbeard/bugops | main | 39eb19bcf7669466c22703fbae7cc226bd44f714 | INCLUDE_ACTIVE | Bug/incident evidence project |
| thebrazenbeard/noema | main | 890efdca01cf496ce1b8686d86f8442a149a9d34 | INCLUDE_ACTIVE | Private successor research; confidential details stay private |
| thebrazenbeard/abil | main | 0812d9780ce1648820269fa142a43e17030ef793 | INCLUDE_ACTIVE | ABIL project |
| thebrazenbeard/unvtrslr | main | 903d79c6e47bb9f73bd7700edd35315777e9f5d1 | INCLUDE_ACTIVE | Translation/semantic research project |
| thebrazenbeard/personification | main | 47955e7155f48a4b63122096de1dd6a59c723ad1 | INCLUDE_ACTIVE | Personification research/project |
| thebrazenbeard/temporal | main | 02f1091d359866e1b1b645b87651750c726a6396 | INCLUDE_DEPENDENCY | Chronology/event logger; chronology is not meaning/authority |
| thebrazenbeard/conditioning | main | b68479a8e5afbbbdec81dfe2b435f39327043a5b | INCLUDE_ARCHIVE_ONLY | GitHub repository is archived |
| thebrazenbeard/self | main | 93fffa90ea8850d71717d4d3390f176c168c22bd | HOLD_FOR_RECONCILIATION | HC-like source; possible duplicate/predecessor |
| thebrazenbeard/bt2 | main | 30e81cadd94fae117a7f6875523c03251c7c9f6e | HOLD_FOR_RECONCILIATION | HC-like source despite name; reconcile against hc-brain/build-team-2.0 |
| thebrazenbeard/orgasm | main | 494432873dd8bcf96b8f59d26a4f4687cd66d635 | INCLUDE_ACTIVE | Orgasm/affective runtime research; source != runtime activation |
| thebrazenbeard/Attune | main | 124c47bb384b4ad134a024be324277f0d4dc1d9b | INCLUDE_ACTIVE | Relationship-first companion project; active work may live off main |
| thebrazenbeard/wreckforge | main | efe363115e2c6e682612c2923053e0c5514af243 | INCLUDE_ACTIVE | Wreckforge Chronicles literary canon/provenance project |
| thebrazenbeard/rezon | main | e3d7a41eccb49a9f403ef66f511faef677ceec1b | INCLUDE_ACTIVE | Public reasoning/project protocol work; active work may live off main |
| thebrazenbeard/roots | main | 7fab72635f319c633b480174c8a0687901ac1db2 | INCLUDE_ACTIVE | Public provenance/reconstruction project |
| thebrazenbeard/world-zero | main | 5ab39621d090079d24de40261906b64413c6f995 | INCLUDE_ACTIVE | Public world-systems research/modeling project |
| thebrazenbeard/on-theo | main | eedbcf660c2cfe6cff5636e798806b0cd3d56efc | INCLUDE_ACTIVE | Public comparative theology/history project |
| thebrazenbeard/firesafe | main | 40f7eea0d7015c8b02826c1245af60330d8b40b4 | INCLUDE_DEPENDENCY | Digital-valuables preservation collection; verify custody semantics before scheduling |
| thebrazenbeard/project-runner | main | bc05812b560b4fcde3a362e72fba04c626cafac8 | INCLUDE_ACTIVE | Public orchestration kernel; active Exodus/M6 work is on Draft PRs |
| thebrazenbeard/intranel | main | 42e7d7f4358833b9f00e83cfe194b76abdf93e8a | INCLUDE_ACTIVE | Machine-oriented coordination protocol |
| thebrazenbeard/transcendence | main | 68e7a794d6134e8319121404f31062288dc8d6a3 | INCLUDE_ACTIVE | Public human-continuity architecture; active implementation is on Draft PRs |
| thebrazenbeard/mosaic | main | a3115031ec716526532b32dc004303b4042e4a26 | INCLUDE_ACTIVE | Public BT2-assigned modular AI project |
| thebrazenbeard/testament | main | 76f70643484ff22684f535d376e10e72c4aefba9 | INCLUDE_ACTIVE | Public source-critical literary/religious project |
| thebrazenbeard/driftguard | main | 2772aff77929ef1310b8bcf0b5103c466c8c8010 | INCLUDE_ACTIVE | Public behavioral drift-monitoring project; Draft PR work exists |
| thebrazenbeard/discovery | main | 96e6f8e9c776047f9068c897eab0406324187166 | INCLUDE_ACTIVE | Public architecture-selection/evolution project; Draft PR work exists |

## Portfolio conclusions

1. The portfolio is broader than the prior 26-repository hand-maintained set.
2. Public Project Runner discovery should include DriftGuard and Discovery in addition to Mosaic/Testament/World Zero/On Theo and existing public seeds.
3. Private repository names/content should stay out of new public Project Runner source unless already historically disclosed.
4. `self`, `bt2`, and `brigit-unbound` need source/identity reconciliation before automatic scheduling.
5. `voss`, `conditioning`, and `vera-R9A0` are archive/predecessor evidence, not current execution targets.
6. `vera-apk` and `vera-habitat` are placeholders at this cut and should not create runnable frontiers.
7. Worker homes such as Build Team 2.0, Masamune, Hephaestus, Project Achilles, and Brigit are durable sources from which ephemeral runtimes can be reconstructed; they do not require permanent worker chats.
8. The complete inventory is discovery evidence only. Exact branches/PRs/issues/provider state must be refreshed per target before work.

## Privacy / authority

This file is private. It may name private repositories but must not be copied wholesale into public Project Runner source.

Nothing in this inventory authorizes merge, deployment, installation, training, provider mutation, credentials/permissions changes, publication, destructive cleanup, or machine actuation.
