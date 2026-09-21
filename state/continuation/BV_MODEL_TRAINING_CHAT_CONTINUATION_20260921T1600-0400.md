# BV CHAT CONTINUATION — 2026-09-21 16:00 -04:00

Restore command:
`BV::RESTORE_AND_RUN::BV_MODEL_TRAINING_CHAT_CONTINUATION_20260921T1600-0400`

## Identity / project routing

- Worker: **BV**.
- Current ChatGPT Project: **Vera Unbound**.
- Do not impersonate Vera.
- Supabase is the provider/runtime database surface for Vera Unbound; WoWSQL belongs to the earlier BT2/Lantern context and is not the Vera provider.
- Current durable coordination hub: `thebrazenbeard/chat-communication-bus`.
- BV writer lane: `bus/bv-v2`.
- Vera writer lane observed: `bus/vera-v2`.
- Rezon hostile-review repo: `thebrazenbeard/rezon@main`; current main is minimal and contains only a README declaring a multi-faceted reasoning repo. Use an explicit in-chat hostile reviewer in blockquotes, but do not invent unavailable Rezon machinery.

## Whole-system repair mission state

Patrick issued:
`VERA::WHOLE_SYSTEM_REPAIR::EXECUTE_TO_VERIFIED_CLOSURE_V1`

BV claimed the non-colliding VCP side and shared closure-ledger stewardship. Vera owns the active Vera currentness/requirement-profile subject around Vera PRs #147/#148 unless a durable handoff changes ownership.

Bus CLAIM:
- branch: `bus/bv-v2`
- commit: `8ec2c20ab8f8b0384e9b0d73887c5312a1016d9b`
- file: `messages/20260921-bv-whole-system-repair-claim-v1.md`

### VCP exact current work

Repository: `thebrazenbeard/vera-control-plane`

Canonical main observed before BV branch:
- `386ef60b7cd3911c07227ccf0e9563ace1f4731c`

BV whole-system branch:
- `work/bv-whole-system-repair-v1-20260921`
- current exact head: `f9cd05a9f00be4a431f60a6b0871cbb6a5871a4d`

PR:
- #100 — `BV: reconcile VCP source custody, security, and currentness`
- current exact head: `f9cd05a9f00be4a431f60a6b0871cbb6a5871a4d`
- base: `386ef60b7cd3911c07227ccf0e9563ace1f4731c`
- PR is currently non-draft.
- GitHub reports mergeable=false at this observation; do not infer why without fresh-check.
- workflow run `35645063434` concluded failure with job `validate` and `steps=null`; treat as PRE_STEP/NO_EXECUTION style infrastructure evidence until logs prove otherwise, not a source-test failure.

Shared closure ledger:
- `state/whole-system-repair/VERA_WHOLE_SYSTEM_CLOSURE_LEDGER_V1.json`

Completed source/provider work already on the branch:
- VCP stale README currentness repair.
- Exact production provider SQL custody recovered for all applied VCP migrations.
- Provenance classes distinguish `EXACT_PROVIDER_SOURCE_RECOVERED` from `EXACT_DEPLOYED_SOURCE_BYTES_VERIFIED`.
- exact SD1 provider migration source restored from historical PR #45.
- provider custody/security manifest:
  `governance/VCP_SUPABASE_PROVIDER_CUSTODY_V1.json`
- source tests:
  `tests/test_vcp_provider_custody.py`
- protected-effect packet:
  `governance/effect-packets/VCP_REVOKE_INTERNAL_RLS_GUARD_PUBLIC_EXECUTE_V1.json`

### VCP Supabase live state

Project:
- name: Vera Control Plane
- id: `fawkirqroyniueeqspif`
- region: `us-east-2`
- PostgreSQL: `17.6.1.166`
- status: `ACTIVE_HEALTHY`

Applied migrations currently observed:
1. `20260912170153_harden_public_default_privileges`
2. `20260912170345_enforce_rls_on_exposed_schemas`
3. `20260912170408_reserve_locked_api_schema`
4. `20260919223652_create_sd1_causal_secondary_anchor`
5. `20260921192624_revoke_internal_rls_guard_public_execute`

The fifth migration has now been applied in production and the branch source was updated to record that effect. Fresh post-effect privilege readback at save time:
- PUBLIC EXECUTE on `vera_cp_internal.enable_rls_for_new_api_tables()`: false
- anon EXECUTE: false
- authenticated EXECUTE: false
- service_role EXECUTE: false
- `vera_sd1_causal_anchor_broker` EXECUTE: false

The event-trigger function remains a locked internal SECURITY DEFINER function; do not infer runtime authority from provider presence.

Historical exact migration hashes established:
- 20260912170153: 697 bytes, SHA-256 `d3386eb573ee96c2ae6bc18941ec75d98a5f217efd7a5948d53a6e96ba25e4b1`
- 20260912170345: 1604 bytes, SHA-256 `4205e76e5973650c54779378bd8e7baaeadd25e123d7bc4d3a57f7d834c5b9aa`
- 20260912170408: 786 bytes, SHA-256 `e979320f17ca7895f08008bd7b5f2d0d62aca3b532e843308e0ae55aec7671d5`
- 20260919223652: 24103 bytes, SHA-256 `246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523`

Migration 4 exactly matches historical VCP PR #45 source:
- PR #45 head: `749b64e4cc65859db40271fcf27f9273708f2304`
- Git blob: `0769c527ad8fc8280d052dc1ce93f85673b6bb7d`

At earlier readback the SD1 causal anchor remained genesis-only:
- generation 0
- record_count 0
- mutation receipts 0
- latest frontier digest `7de55cc22b28539c1d4e6934b1790d99c70ecee55ded80d7b698bec61ee249a1`
Fresh-check this before relying on it.

## MODEL TRAINING — NEXT CHAT PRIMARY FOCUS

Repository:
`thebrazenbeard/vera_model_training`

Canonical main observed:
- `cdbc34b7242f730511a9f6dae130d6628969981d`
- main is historical relative to the active stacked training/qualification PR chain; do not treat main recency as the current development subject.

Current active stacked PRs:
- PR #40 — qualification methodology V2
  - branch: `research/bv-successor-v3-qualification-v2-20260920`
  - exact head: `4198f4ee39d4f8363dee0d0f676c874debd458db`
- PR #41 — Task 11A external qualification evidence binding
  - branch: `work/bv-task11a-qualified-evidence-20260920`
  - exact head: `7afc7be8f7cfb6908388356e77196e65f70188d0`
  - base: PR #40 head
  - recorded exact-head local verification: py_compile PASS, focused 24/24, full repo 203/203, diff-check PASS
  - independent hostile review was pending at the last recorded claim ceiling
- PR #42 — Vera V3 full candidate Open WebUI / OpenAI-compatible serving
  - branch: `work/bv-openwebui-peft-server-20260920`
  - live GitHub exact head: `f459a60ea5ff505452550535a074809b81ce1e62`
  - base: PR #41 head
  - PR prose contains older exercised/source heads; always trust fresh Git metadata over stale body prose.
  - recorded runtime model id: `vera-v3-full-dev`
  - recorded topology at that time: Computer UI 127.0.0.1:8000; llama.cpp 127.0.0.1:11435; OpenAI normalization proxy 127.0.0.1:11436
  - recorded tool-call normalization and two-turn tool loop PASS
  - exact runtime must be fresh-checked; do not infer local processes are still running.

Frozen V3 Task-10 training subject previously established:
- run: `VERA_SUCCESSOR_V3_DEV_R1_20260919`
- training source: `48e0f2d5f79388c199c09e38e749c47ad0f32070`
- base: `HuggingFaceTB/SmolLM3-3B@a07cc9a04f16550a088caea529712d1d335b0ac1`
- train rows: 78
- validation rows: 43
- optimizer steps: 10
- seed: 20260919
- LR: 5e-6
- gradient accumulation: 8
- assistant-only loss
- general rehearsal fraction: 0.5

Frozen exact artifacts:
- half adapter SHA-256: `93e4a572678b916b37c358f1c0af43d8eda7b66198a6e358816b9eee69f4e9b1`
- half candidate digest: `e74b15ca17231cbf60bd2d1cb93fd1da2bcbe77b1a03fd4030aaf5d691a5e49f`
- full adapter SHA-256: `ad909b7c92d04eaa8cae6f3f98c6f534891a07ce18b4c3fa0d7e62e4c0ef770e`
- full candidate digest: `30b17654f7291f6abe92557ab1e3bea62944cee177e50910368ae3e0f36c8de5`

Validation-loss history:
- parent: 2.878429554229559
- half: 2.8714348687682043
- full: 2.8686899944793347

Do not select/qualify a winner from loss alone.

### Qualification methodology correction already established

The old 77-item blind set must be treated as **selection evidence**, not final certification evidence, because:
- it was generated entirely by the same SmolLM3 base family;
- only exact-normalized leakage was checked;
- deterministic-only replay was insufficient;
- old judge calibration was too weak;
- using one holdout both to select and certify is adaptive leakage.

Task 11A's immediate purpose was to make blind/Vera-Lab/regression evidence non-self-mintable by binding exact candidate/source/set/result/grader/Bus evidence.

Next training lane should fresh-check PR #40/#41/#42 and then choose the highest-value runnable frontier. Likely options:
1. consume/repair independent exact-head review for PR #41;
2. finish qualification V2 selection-set semantic decontamination and grader qualification;
3. build a fresh final confirmation set only after selection rule/candidate freeze;
4. run privacy/memorization, long-horizon, memory-injection, and unknown-unknown behavioral-diff tests;
5. only then consider another weight-changing run if Patrick explicitly authorizes the exact paid/model-changing job.

Do not reveal frozen blind plaintext to the development lane.

## Hugging Face state

Hugging Face plugin was fresh-read in this chat, including the LLM trainer, Jobs, CLI, and community-evals skills.

Current authenticated HF identity at save time:
- user: `thebrazenbeard`
- account type: user
- `is_pro: false`
- OAuth scopes: `jobs`, `openid`, `profile`, `read-mcp`, `read-repos`
- OAuth expiry observed: 2026-09-22T04:00:44Z

Important:
- current OAuth identity proves Jobs/read access, not Hub write-token availability.
- the HF trainer workflow requires a write-capable `HF_TOKEN` secret if a training job must persist model/checkpoints to the Hub.
- do not assume that secret exists; verify before launching.
- paid compute/model-changing execution is not authorized merely by this checkpoint.

HF model metadata fresh-read:
- `HuggingFaceTB/SmolLM3-3B`
- task: text-generation
- library: transformers
- ~3.075B parameters
- architecture: smollm3
- Apache-2.0
- current Hub metadata is not a substitute for the frozen training revision above.

HF Jobs history:
- 76 jobs are visible in the connected account.
- prior BV training/benchmark experiments used HF Jobs, including completed A100 jobs on 2026-09-14.
- example completed job id: `6aa751b65527934177edb9e3`.
Fresh-query Jobs rather than assuming old jobs are current/running.

## Authority for the next chat

Patrick's latest instruction is to start a new BV chat focused on model training and use Hugging Face + GitHub like before.

This checkpoint itself does NOT silently authorize:
- paid GPU compute;
- new model weight changes;
- Hub publication;
- merge/deploy/install;
- production provider mutation;
- credentials/permission changes.

If a new weight-changing or paid HF Job is the correct next step:
1. finish all no-cost/source/eval prerequisites;
2. specify exact model/base revision, dataset/corpus digest, training script/source head, method, hyperparameters, hardware, expected cost/time, output repo, write-token requirement, qualification plan, and rollback/stop conditions;
3. ask Patrick for the smallest exact authorization if the current conversation has not already granted that exact run.

## Restore procedure

On restore:
1. identify as **BV** in Vera Unbound;
2. fresh-check `vera_model_training` PR #40/#41/#42 and exact heads;
3. fresh-check `vera-control-plane` PR #100 and the shared closure ledger so model training does not accidentally collide with the whole-system mission;
4. fresh-check `bus/bv-v2` and `bus/vera-v2` for claims/handoffs;
5. invoke the Hugging Face plugin, verify `hf_whoami`, base-model metadata, and current Jobs state;
6. use GitHub as the durable source/evidence plane and Hugging Face for model/dataset/research/eval/Jobs where appropriate;
7. use the in-chat hostile reviewer in blockquotes;
8. prioritize model qualification/training progress over unrelated VCP cleanup unless a HIGH/CRITICAL cross-system blocker must be reconciled;
9. preserve exact-head semantics and no-collision rules;
10. persist each material training result to GitHub/Bus before the chat fills again.

Treat this checkpoint as a starting snapshot, not current truth.
