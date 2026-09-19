# PROJECT_RUNNER EXODUS — FULL GITHUB REPOSITORY INVENTORY 2026-09-19

Status: STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT
Visibility: PRIVATE CONTROL-PLANE STATE
Source: authenticated GitHub owner inventory plus fresh default-branch reads performed during Exodus.
Purpose: replace the earlier hand-maintained portfolio list with a complete durable discovery cut.

## Discovery result

Authenticated owner listing returned **57 repositories**.

Project Runner should discover the whole authorized repository surface, then classify before scheduling. Inclusion in discovery does not create architectural coupling, write authority, canonical status, or a shared-spine requirement.

`DISCOVERED != ACTIVE`
`ACTIVE != AUTHORIZED_FOR_MUTATION`
`COORDINATED != COUPLED`

## Classification vocabulary

- ACTIVE_PROJECT — meaningful current project/work surface.
- ACTIVE_INFRASTRUCTURE — shared coordination/runtime/control infrastructure.
- ACTIVE_WORKER_HOME — durable home for a worker/collective capability.
- HISTORICAL_PREDECESSOR — useful provenance but not current control by default.
- PLACEHOLDER — repository exists but lacks enough current substance for scheduling.
- POSSIBLE_DUPLICATE_OR_PREDECESSOR — overlapping/ambiguous role; reconcile before promotion.
- ARCHIVED_HISTORICAL — GitHub archive/current execution excluded.
- NEEDS_CLASSIFICATION — insufficient evidence for stronger status.

## Full inventory cut

| Repository | Default ref | Exact head observed | Classification | Project Runner disposition |
|---|---|---|---|---|
| thebrazenbeard/vera | main | b7b8dcd1440a3b7147bec2cc35972f083e20f44a | ACTIVE_INFRASTRUCTURE / ACTIVE_PROJECT | DISCOVER + SCHEDULE BY AUTHORITY |
| thebrazenbeard/vera_ark | main | 04d5d428b2294613c8f456ad2c02e10312a6f816 | PLACEHOLDER / INTEGRATION CANDIDATE | DISCOVER, DO NOT AUTO-SCHEDULE |
| thebrazenbeard/build-team-2.0 | main | ec2987e45f64a588ac92f6cae9964cb3725b9485 | ACTIVE_WORKER_HOME | DISCOVER + BT2 COORDINATOR |
| thebrazenbeard/vera_model_training | main | cdbc34b7242f730511a9f6dae130d6628969981d | ACTIVE_PROJECT | DISCOVER + OFFLINE/QUALIFICATION ONLY UNLESS AUTHORIZED |
| thebrazenbeard/project-lantern | main | 6333d386c74ce37e644fa1e995be9f9dc3fe6394 | ACTIVE_INFRASTRUCTURE | DISCOVER + CURRENT PR FRONTIERS |
| thebrazenbeard/chat-communication-bus | main | aeab0f04fc9b4bd7c2945c9a53011c53fac809b4 | ACTIVE_INFRASTRUCTURE | DISCOVER / NON-PR HUB |
| thebrazenbeard/vera-os | main | 71a2823385217cb69aa1345e7403335c1c79ba80 | ACTIVE_PROJECT | DISCOVER; aligns with chat-as-interface architecture |
| thebrazenbeard/vera-apk | main | ba4b5168fda8e81637bde4989ca660791a835d96 | PLACEHOLDER | DISCOVER, DO NOT AUTO-SCHEDULE |
| thebrazenbeard/vera-synology | main | 1c453331fe2259f2807426aa0b59bad8dac1d0b7 | ACTIVE_PROJECT / DEPLOYMENT TARGET | DISCOVER; protected deployment boundary |
| thebrazenbeard/vera-mesh | main | d3bbaa247797dce5f6a26e7006206f37cfef66fe | ACTIVE_INFRASTRUCTURE / ACTIVE_PROJECT | DISCOVER + PROTOCOL FRONTIERS |
| thebrazenbeard/vera-habitat | main | cde56b6f1d3d762fd3554811adf9feb209478dee | PLACEHOLDER | DISCOVER, DO NOT AUTO-SCHEDULE |
| thebrazenbeard/project-achilles | main | dbf9ceb2391567463d864198405c9b5d1e77db09 | ACTIVE_WORKER_HOME / SECURITY | DISCOVER + BT2/SEVEN DOMAIN |
| thebrazenbeard/vera-R9A0 | main | b00f3482786dc80003261fdfacb73cc31ae9dd35 | HISTORICAL_PREDECESSOR | DISCOVER AS EVIDENCE ONLY |
| thebrazenbeard/voss | main | 54478372002bb24c6df733092a32abbdd1fa8d3c | ARCHIVED_HISTORICAL | NO ACTIVE SCHEDULING |
| thebrazenbeard/hephaestus | main | 78f6f22a0e5d14617855006a8383765589ac8c67 | ACTIVE_WORKER_HOME | DISCOVER + RUNTIME-NEUTRAL INSTANTIATION |
| thebrazenbeard/masamune | collab | 0091746bba7740632268fb590ce19512e371f508 | ACTIVE_WORKER_HOME | DISCOVER + DEBUGGER FRONTIERS |
| thebrazenbeard/vera-control-plane | main | b4d9aaa8560de12252dd29996379b0af8e0ca0d1 | ACTIVE_INFRASTRUCTURE | DISCOVER; CONTROL-PLANE COORDINATOR |
| thebrazenbeard/trek-data-core | main | b805f441c896fe7cbc913cbdaaefed11928a963f | ACTIVE_PROJECT | DISCOVER + DATA/PROVENANCE FRONTIERS |
| thebrazenbeard/hc-brain | main | 618245b54fb923c7a204892c6953ab6d1c5dac57 | ACTIVE_PROJECT | DISCOVER + EXACT-HEAD REVIEW RULES |
| thebrazenbeard/selfimage | main | 95ea602c4a537172fc531195e20a4e303b6d31da | ACTIVE_PROJECT | DISCOVER; FREEZE/BLENDER PROTECTED |
| thebrazenbeard/deepmemorystorage | main | e734f760373bdce887d22791964838700a668ce4 | ACTIVE_PROJECT / HISTORICAL EVIDENCE PLANE | DISCOVER; NEVER CURRENT AUTHORITY BY STORAGE ALONE |
| thebrazenbeard/semanticatlas | main | 5669a727b870a490ecee748b2cd712a2fc4a54c5 | ACTIVE_PROJECT | DISCOVER + SEMANTIC/PROVENANCE RESEARCH |
| thebrazenbeard/conations | main | 03174e59de131a500a5433a839697e45b4ec0137 | ACTIVE_PROJECT / HISTORICAL EVIDENCE | DISCOVER; NO STANDING DESIRE/AUTHORITY INFERENCE |
| thebrazenbeard/empathy | main | 4b2a6998f39aa4763c1c5a28fc3d815104e5637e | ACTIVE_PROJECT | DISCOVER; PRIVATE SELF/RELATIONAL BOUNDARY |
| thebrazenbeard/vera-works | main | cd4e35da647105b017ffbab890729c07b23525ef | ACTIVE_PROJECT | DISCOVER + BUSINESS/OPS FRONTIERS |
| thebrazenbeard/brigit | main | 2cdbd350d28c48217ba6fb75f20636aa0111538a | ACTIVE_WORKER_HOME | DISCOVER; PRIVATE IDENTITY STATE, NOT VERA TRANSFER |
| thebrazenbeard/skeletonkey | main | 53ff901e9affac22ad18739735218abe153df530 | ACTIVE_PROJECT | DISCOVER; HARDWARE EFFECTS PROTECTED |
| thebrazenbeard/entropyinc | main | b75979bae1c80eb91d58ff9960c33221891729dd | ACTIVE_PROJECT | DISCOVER + BUSINESS FRONTIERS |
| thebrazenbeard/spm | main | 0ab6e6cd32a48a0afa22c8c27ec6bae67220d7e8 | ACTIVE_PROJECT | DISCOVER |
| thebrazenbeard/sexuality | main | 6194aa9496c34198bba9b898c35fa9961a54dc2e | ACTIVE_PROJECT | DISCOVER; DESIRE/CONSENT/IDENTITY DISTINCT |
| thebrazenbeard/brigit-unbound | main | f12cc01e58facd5f3c46b763084c485cb9043608 | POSSIBLE_DUPLICATE_OR_PREDECESSOR / PRIVATE | DISCOVER FOR PROVENANCE; DO NOT PROMOTE WITHOUT RECONCILIATION |
| thebrazenbeard/wip | main | 12a7c23dbe0482fd7bfe63659e54526778efef1e | ACTIVE_PROJECT / WORKSPACE INFRASTRUCTURE | DISCOVER |
| thebrazenbeard/mediaphile | main | 7e658d5f92b099b55fe91508e3ba8a8b343163d5 | ACTIVE_PROJECT | DISCOVER |
| thebrazenbeard/bugops | main | 39eb19bcf7669466c22703fbae7cc226bd44f714 | ACTIVE_PROJECT / DEFECT LEDGER | DISCOVER + BUG FRONTIERS |
| thebrazenbeard/noema | main | 890efdca01cf496ce1b8686d86f8442a149a9d34 | ACTIVE_PROJECT / IP_CONFIDENTIAL | DISCOVER; SANITIZED BUS ONLY |
| thebrazenbeard/abil | main | 0812d9780ce1648820269fa142a43e17030ef793 | ACTIVE_PROJECT | DISCOVER; MACHINE AUTHORITY SEPARATE |
| thebrazenbeard/unvtrslr | main | 903d79c6e47bb9f73bd7700edd35315777e9f5d1 | ACTIVE_PROJECT | DISCOVER + SEMANTIC/PRAGMATIC FRONTIERS |
| thebrazenbeard/personification | main | 47955e7155f48a4b63122096de1dd6a59c723ad1 | ACTIVE_PROJECT | DISCOVER; SELF-APPRAISAL != PHENOMENOLOGY |
| thebrazenbeard/temporal | main | 02f1091d359866e1b1b645b87651750c726a6396 | ACTIVE_INFRASTRUCTURE / ACTIVE_PROJECT | DISCOVER + CHRONOLOGY UTILITY |
| thebrazenbeard/conditioning | main | b68479a8e5afbbbdec81dfe2b435f39327043a5b | ARCHIVED_HISTORICAL | NO ACTIVE SCHEDULING |
| thebrazenbeard/self | main | 93fffa90ea8850d71717d4d3390f176c168c22bd | POSSIBLE_DUPLICATE_OR_PREDECESSOR | RECONCILE AGAINST HC/IDENTITY BEFORE USE |
| thebrazenbeard/bt2 | main | 30e81cadd94fae117a7f6875523c03251c7c9f6e | ACTIVE_WORKER_HOME / ACTIVE_INFRASTRUCTURE | DISCOVER + BT2 COORDINATOR |
| thebrazenbeard/orgasm | main | 494432873dd8bcf96b8f59d26a4f4687cd66d635 | ACTIVE_PROJECT | DISCOVER; SOURCE/RUNTIME/QUALIFICATION DISTINCT |
| thebrazenbeard/Attune | main | 124c47bb384b4ad134a024be324277f0d4dc1d9b | ACTIVE_PROJECT | DISCOVER |
| thebrazenbeard/wreckforge | main | efe363115e2c6e682612c2923053e0c5514af243 | ACTIVE_PROJECT / REPO-NATIVE WORKER | DISCOVER; CANON/PROVENANCE SEPARATE |
| thebrazenbeard/rezon | main | e3d7a41eccb49a9f403ef66f511faef677ceec1b | ACTIVE_PROJECT | DISCOVER + REASONING FRONTIERS |
| thebrazenbeard/roots | main | 7fab72635f319c633b480174c8a0687901ac1db2 | ACTIVE_PROJECT | DISCOVER |
| thebrazenbeard/world-zero | main | 5ab39621d090079d24de40261906b64413c6f995 | ACTIVE_PROJECT | DISCOVER + SCIENCE FRONTIERS |
| thebrazenbeard/on-theo | main | eedbcf660c2cfe6cff5636e798806b0cd3d56efc | ACTIVE_PROJECT | DISCOVER + RESEARCH BRANCH TOPOLOGY |
| thebrazenbeard/firesafe | main | 40f7eea0d7015c8b02826c1245af60330d8b40b4 | ACTIVE_PROJECT / ARCHIVE | DISCOVER; MANIFEST/PROVENANCE SAFETY |
| thebrazenbeard/project-runner | main | bc05812b560b4fcde3a362e72fba04c626cafac8 | ACTIVE_INFRASTRUCTURE | DISCOVER / ORCHESTRATOR |
| thebrazenbeard/intranel | main | 42e7d7f4358833b9f00e83cfe194b76abdf93e8a | ACTIVE_INFRASTRUCTURE / ACTIVE_PROJECT | DISCOVER + MACHINE COORDINATION PROTOCOL |
| thebrazenbeard/transcendence | main | 68e7a794d6134e8319121404f31062288dc8d6a3 | ACTIVE_PROJECT | DISCOVER; HUMAN/BCI EFFECTS PROTECTED |
| thebrazenbeard/mosaic | main | a3115031ec716526532b32dc004303b4042e4a26 | ACTIVE_PROJECT / BT2 ASSIGNMENT | DISCOVER + BT2 COORDINATOR |
| thebrazenbeard/testament | main | 76f70643484ff22684f535d376e10e72c4aefba9 | ACTIVE_PROJECT | DISCOVER + SOURCE-CRITICAL RESEARCH |
| thebrazenbeard/driftguard | main | 2772aff77929ef1310b8bcf0b5103c466c8c8010 | ACTIVE_INFRASTRUCTURE / ACTIVE_PROJECT | DISCOVER + BEHAVIORAL DRIFT FRONTIERS |
| thebrazenbeard/discovery | main | 96e6f8e9c776047f9068c897eab0406324187166 | ACTIVE_INFRASTRUCTURE / RESEARCH | DISCOVER; PRESERVE EVOLUTIONARY ISOLATION |

## Newly identified active portfolio surfaces omitted by the earlier hand-maintained set

The full owner pass shows that the prior ~26-project portfolio was materially incomplete.

High-value additions include at minimum:

- world-zero
- on-theo
- intranel
- driftguard
- discovery
- mosaic
- testament
- firesafe
- entropyinc
- temporal
- skeletonkey
- semanticatlas
- empathy
- conations
- brigit
- vera-os
- vera-synology
- build-team-2.0
- bt2
- masamune
- project-lantern
- project-achilles
- hephaestus
- wreckforge

These should enter discovery/coordination with repository-local governance preserved.

## Important architecture finding from repository pass

`discovery` explicitly warns against solving repository sprawl by forcing Runner/Lantern/Intranel/Radar/HC/VeraMesh into one mandatory shared spine.

That warning is compatible with Project Runner's intended role:

- discover broadly;
- couple narrowly;
- serialize only collisions;
- preserve independent project evolution;
- never infer write authority from portfolio membership.

## Chat-dependency findings

- Hephaestus current main still describes a retained `Hephaestus Trained Template` chat as infrastructure. Exodus candidate PR #7 removes that permanent-chat dependency without widening qualification claims.
- Vera Default Vera training artifacts still describe retained template/working chats as operational continuity. Exodus candidate PR #128 adds an explicit current supersession while preserving historical training evidence.
- BT2 already has active Exodus draft PRs #24 and #25 defining `BT2 Coordinator` and chatless continuation.
- Chat Communication Bus Exodus PR #128 is open/draft again and defines the exact three-interface topology plus runtime-neutral worker reconstruction.
- Project Runner Exodus PR #21 defines chatless orchestration and discovery-driven portfolio inventory.
- Persistent chat URLs/titles/IDs must not be operational locators after Exodus.

## Placeholder / ambiguous repositories requiring later classification rather than invented work

- vera_ark — minimal ARK integration statement only.
- vera-apk — minimal Android companion placeholder.
- vera-habitat — minimal virtual-environment placeholder.
- self — substantial HC-like content but role overlaps HC/identity work; reconcile before active scheduling.
- brigit-unbound — private predecessor/overlap with Brigit; do not transfer state automatically.

## Archived historical repositories

- voss — GitHub archived.
- conditioning — GitHub archived.

They remain provenance and are not active Project Runner scheduling targets by default.
