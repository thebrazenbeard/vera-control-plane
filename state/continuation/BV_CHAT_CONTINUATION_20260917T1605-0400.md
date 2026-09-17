# BV Chat Continuation Pointer — 2026-09-17 16:05 -0400

Restore token:
`BV::RESTORE::BV_CHAT_CONTINUATION_20260917T1605-0400`

This is the BV-level durable pointer for the chat rollover. The detailed execution checkpoint is source-controlled in `thebrazenbeard/spm`.

Primary detailed save:
- repo: `thebrazenbeard/spm`
- branch: `state/bv-chat-continuation-20260917-1605`
- file: `state/continuation/BV_CHAT_CONTINUATION_20260917T1605-0400.md`
- commit: `4832a1d7ee20e19f5fb9c02ca06e2a628423c7b6`
- file SHA-256: `ca36352d2c803095246731a96894b586e13385829bb19df8e1816be0a0275cc1`

The SPM continuation commit deliberately captures the current RED TDD frontier plus baseline subject manifests. It does NOT move SPM PR #2, which remains draft/open/unmerged at remote head `be86721cd96f3f2b0f4ca2b43c3ee81dbf0d145b`.

Fresh SPM review updates at save require (1) a conventional persistent-memory/retrieval control separate from B* and (2) nuisance-matched intervention controls with evidence classes separated into state dependence, persistence dependence, representation-structure dependence, and semantic-relation specificity.

Current local next step is to implement `LocalHFAdapter.score_many_selected()` from the existing failing test, prove score equivalence to the prior balanced-semantic evaluator, then complete the full pinned SmolLM3-3B 36-case baseline before baseline readiness or learned B*/C training.

Rezon remains a candidate optional external continuity-of-inquiry substrate; the Rezon team is One, Masa, Mune, and Rezon. Preserve the guardrail `stored != admitted != current != true`. Fresh-check the Chat Bus on restore.

Do not treat this pointer as qualification authority. `CAUSAL_MODEL_VERIFIED = NO`; `SPM_VERIFIED = NO`.
