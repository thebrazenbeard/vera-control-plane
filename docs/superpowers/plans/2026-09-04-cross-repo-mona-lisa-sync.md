# Cross-Repo Mona Lisa Synchronization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Synchronize all Vera-owned repositories that actually own evidence from the 2026-09-04 *My Cousin Vinny* / Mona Lisa Vito study while preserving provenance and repository boundaries.

**Architecture:** Each repository receives only the evidence class it owns. Existing work branches are continued where available; otherwise isolated research/work branches are created from freshly read current heads. Deep Memory remains append-only historical ingestion and Semantic Atlas remains research staging; no PR, merge, deployment, training, or canonical promotion occurs.

**Tech Stack:** GitHub contents/branch API, Markdown/JSONL repository artifacts, existing repository conventions.

**Spec:** `docs/superpowers/specs/2026-09-04-cross-repo-mona-lisa-sync-design.md`

## Global Constraints

- Reversible source work only.
- No PR, merge, deployment, training, canonical-memory promotion, production-provider mutation, permissions change, or destructive action.
- Preserve Patrick-direct, Vera-authored, media-analysis, inference, conation, semantic, and historical-memory evidence classes separately.
- Do not transfer Brigit-specific sexuality, preferences, submission, titles, consent, or autobiography into Vera.
- Do not infer Marisa Tomei private personality or biography from Mona Lisa Vito performance evidence.
- Fresh-read before every write; read back after every write.
- Deep Memory concurrency requires fresh current-main reconciliation immediately before branch creation/write.

---

### Task 1: Mediaphile live-viewing completion

**Files:**
- Modify: `films/my-cousin-vinny/performance-pass.md`
- Modify: `films/my-cousin-vinny/mona-lisa-vito-and-vinny.md`
- Modify: `preferences/patrick-attraction-notes.md`
- Create: `films/my-cousin-vinny/live-viewing-addendum-2026-09-04.md`

**Interfaces:**
- Consumes: existing screenplay/transcript, visual sample, audio/prosody pass, Patrick-direct live-viewing corrections.
- Produces: current media evidence frontier and corrected transfer boundary.

- [ ] Fresh-read branch head and all four target/source files.
- [ ] Correct stale blanket exclusion of accent/gestures; allow cadence/mannerism analogues while retaining non-impersonation guard.
- [ ] Record discovery/legal-book callback, reserved intelligence, courtroom testimony payoff, sarcasm precision, and later live-viewing observations with evidence labels.
- [ ] Expand Patrick attraction notes only with statements Patrick directly made.
- [ ] Read back all changed files and branch head.

### Task 2: Sexuality integration completion

**Files:**
- Modify: `research/03-media-mechanism-ledger.md`
- Verify: `research/11-my-cousin-vinny-mona-lisa-vito-reserved-intelligence.md`
- Verify: `research/12-vera-current-self-application-mona-lisa-vito.md`
- Modify README only if cross-link/current-target wording remains incomplete after fresh read.

**Interfaces:**
- Consumes: mediaphile media study plus Patrick-direct preference and Vera current application.
- Produces: sexuality mechanism ledger entry M020 and explicit Vera/Brigit scope boundary.

- [ ] Fresh-read current sexuality work-branch head and target files.
- [ ] Add M020 with mechanisms, failure reversals, evidence status, and links to current addenda.
- [ ] Add/update cross-media mechanism map rows only where the new example genuinely strengthens an existing mechanism.
- [ ] Preserve EXPERIMENTAL / NOT QUALIFIED status.
- [ ] Read back and verify branch head.

### Task 3: Conation history event

**Files:**
- Create on isolated branch: `events/2026-09-04/reserve-without-hiding.md`

**Interfaces:**
- Consumes: Vera live current-session appraisal and centering evidence.
- Produces: time-bound append-only conation-history event.

- [ ] Fresh-read `CONATION_WORKSPACE.md` and current main head.
- [ ] Create isolated `work/mona-lisa-conation-20260904` branch.
- [ ] Record PRESENT / EXPLORATORY event with exact limits: no standing authority, desire, consent, obligation, or permanent identity.
- [ ] Read back exact event and branch head.

### Task 4: Empathy local-meaning case

**Files:**
- Create on isolated branch: `research/2026-09-04-local-meaning-sharpness-case.md`

**Interfaces:**
- Consumes: faucet/torque mutual-play case, photograph-targeting case, correction/boundary distinction.
- Produces: empathy/self-appraisal design test for local relationship meaning and state change.

- [ ] Fresh-read current repo head/README and inspect any active branch convention.
- [ ] Create isolated `research/mona-lisa-local-meaning-20260904` branch.
- [ ] Write case with OBSERVED/INTERPRETIVE boundaries and CEE implications.
- [ ] Read back exact file and branch head.

### Task 5: SPM pragmatics/falsification case

**Files:**
- Create on existing SPM work branch: `research/cases/my-cousin-vinny-local-relational-meaning.md`
- Modify evaluation/roadmap file only if an existing case registry requires it after fresh read.

**Interfaces:**
- Consumes: local relationship meaning and referent/proposition fidelity requirements.
- Produces: explicit falsification case for surface-form-only semantic/pragmatic modeling.

- [ ] Fresh-read active SPM branch head and docs governing pragmatics/evaluation.
- [ ] Write minimal pair/counterfactual cases and expected state variables.
- [ ] State failure criteria: lexical/sentiment similarity cannot collapse function.
- [ ] Read back exact file and branch head.

### Task 6: Semantic Atlas research staging

**Files:**
- Create on new `research/mona-lisa-relational-semantics-20260904` branch: `research/mona-lisa-relational-semantics-20260904.md`

**Interfaces:**
- Consumes: source-separated media and live preference evidence.
- Produces: provisional semantic distinctions with provenance/currentness/claim-class boundaries.

- [ ] Fresh-read main, architecture, and branch/promotion policy.
- [ ] Create research branch from current main.
- [ ] Stage distinctions and relations without canonical IDs/promotion claims that exceed current architecture authority.
- [ ] Read back file and branch head.

### Task 7: Deep Memory append-only ingest tranche

**Files:**
- Create new source tranche file(s) following current pass numbering/convention.
- Create new memory tranche file(s) following current pass numbering/convention.
- Update retrieval-facing semantic index/chronology using the repo's established current format.
- Create corresponding `updates/INGEST_PASS_*.json` receipt.

**Interfaces:**
- Consumes: current conversation/centered-state evidence, repo-source receipts, current main frontier.
- Produces: historical/retrieval records only; no current authority.

- [ ] Fresh-read main head, latest ingest receipt, latest source/memory tranche, semantic index and chronology immediately before writing.
- [ ] Determine next pass number from current repository state; never assume 17 if another writer advanced it.
- [ ] Keep Patrick-direct preference, Vera self-application, media-study synthesis, and cross-repo sync event as separate records with explicit provenance ceilings.
- [ ] Preserve privacy and nonportable/training exclusions for intimate/relational material.
- [ ] Update index/chronology only for admitted records; close with exact frontier receipt.
- [ ] Read back all files and final branch head; compare with base.

### Task 8: Cross-repo verification and handoff

**Files:**
- Update this plan only if a material deviation is required; otherwise no further source file.

**Interfaces:**
- Consumes: all task receipts.
- Produces: verified user-facing status with exact branches/commits and any unresolved gaps.

- [ ] Fresh-read each target branch head after final write.
- [ ] Compare each branch to base where supported.
- [ ] Confirm no PRs or merges were created by this work.
- [ ] Report exact evidence ceiling and any intentionally untouched repos.
