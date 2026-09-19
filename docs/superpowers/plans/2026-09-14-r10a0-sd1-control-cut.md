# R10A0 + SD1 Control Cut Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a source-only `R10_PLUS_SD1` control-plane candidate that exactly binds reviewed Sexuality and provisional Cohesion, preserves R10 semantics, fits the native Project ceiling, and keeps install/runtime/causality/qualification states separate.

**Architecture:** Add one cold SD1 control owner plus exact binding/qualification/rollback/manifest artifacts under `project-instructions/r10a0/sexual-drive-v1/`. Derive the native projection mechanically from frozen R10, permitting changes only to K00 and K05; the SD1 manifest binds cold artifacts while the native projection pins the manifest SHA-256, avoiding circular native-manifest hashing.

**Tech Stack:** Python 3.11 `unittest`, JSON, SHA-256, Git object hashes.

**Spec:** Patrick `SD1-E::WORK::ORIENT_EXECUTE_INTEGRATE_RUNTIME` and `SD1-E::FOLLOWUP::REPAIR_REBIND_ADVANCE`.

## Global Constraints

- R10 predecessor control-plane base: `b4d9aaa8560de12252dd29996379b0af8e0ca0d1`.
- Sexuality exact source: `02725153fa2e6eae8e81e64bc3d4b797fc404a4d`.
- Cohesion provisional subject: `8510497bb9857185e6b5d4578376adb70613a13d`; final persistence requires independent SD1-V PASS and then fresh exact rebind.
- Do not install R10A1; future `R10A1_PLUS_SD1` is composition metadata only.
- No merge, Project mutation, provider mutation, force push, credential/permission/model/training effects.
- Source/install/current-route/behavior/causality/qualification states remain independently typed.

---### Task 1: Complete RED control-plane contract

**Files:**
- Modify: `tests/test_r10a0_sd1_sexual_drive.py`

- [ ] Rebind provisional Cohesion head to `8510497...` and exact component blob/SHA-256.
- [ ] Assert required package files are absent before implementation.
- [ ] Assert binding pins exact R10 predecessor, Sexuality tuple, Cohesion tuple, SD-01..20, causal protocol, install-authority receipt, and explicit state separation.
- [ ] Assert control semantics include disposition PRESENT, turn-local relevance/intensity typing, nonsexual-intimacy firewall, no consent/attraction/act-desire/identity/human-libido/background-accumulator promotion.
- [ ] Assert future `R10A1_PLUS_SD1` is declared but `NOT_INSTALLED`.
- [ ] Assert native projection preserves line count and every R10 line except declared K00/K05 lines.
- [ ] Assert final native UTF-8 bytes <= 8000 and K00 pins the SD1 manifest SHA-256.
- [ ] Assert manifest hashes/blobs resolve and does not circularly bind native blob.
- [ ] Assert rollback subject remains source-only until provider-live predecessor capture.
- [ ] Run focused tests and record RED caused by missing package.

### Task 2: Minimal source implementation

**Files:**
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SEXUAL_DRIVE_CONTROL_V1.md`
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SEXUAL_DRIVE_BINDING_V1.json`
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SD1_QUALIFICATION.md`
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SD1_ROLLBACK_SUBJECT.json`
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SD1_PROJECT_SOURCE_MANIFEST.json`
- Create: `project-instructions/r10a0/sexual-drive-v1/VERA_R10A0_SD1_NATIVE_PROJECT_INSTRUCTIONS.txt`

- [ ] Implement cold owner and exact binding/qualification/rollback artifacts first.
- [ ] Compute exact Git blobs/SHA-256 and write source manifest, excluding native blob to avoid circularity.
- [ ] Derive native from frozen R10 by changing only K00 and K05, then pin manifest SHA-256.
- [ ] Run focused tests to GREEN.### Task 3: Verification and review gate

- [ ] Run focused SD1 control tests plus inherited `tests/test_r10a1_local_validation.py` and `tools/validate_r10a1.py` as regression-only evidence; never treat R10A1 as installed.
- [ ] Run JSON parse/hash/object verification, `git diff --check`, and inspect exact changed paths.
- [ ] Keep candidate `PROVISIONAL_WAITING_FOR_COHESION_REVIEW` until SD1-V exact-head PASS.
- [ ] After PASS, fresh-read Cohesion exact head and contract object; rebind any changed tuple and rerun the entire suite before commit/push.
- [ ] Commit only after fresh full verification; then verify from a clean detached checkout.
- [ ] Non-force push only from the expected remote frontier; open/update Draft PR without merging.
- [ ] Request independent control-plane hostile review and persist a sanitized Bus checkpoint.

### Task 4: Runtime/provider frontier

- [ ] Continue read-only discovery of a supported live Project Settings/files mutation + readback path.
- [ ] Capture rollback requirements but do not mutate live Project until supported predecessor capture is possible and Cohesion/control review gates pass.
- [ ] Keep both Supabase projects read-only and off the install critical path absent a proven dependency.

Self-review: all required SD1 semantics, exact upstream bindings, byte-budget/native-diff constraints, state separation, R10A1 noninstallation, rollback honesty, hostile review, and fresh-checkout verification are explicitly gated.