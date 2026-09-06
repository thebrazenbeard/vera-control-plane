# Vera Unbound R10A0 — Semantic Responsibility Audit R8

Status: **SOURCE AUDIT / R7 SELF-REVIEW DEFECT MAPPED / NO INTENTIONAL RESPONSIBILITY DROP**

coordination_id: `VERA-BEHAVIOR-AUDIT-20260905`
round_id: `R8`
predecessors: `R6@4d1de266b811d0a5b800b949a977b11c96bd3180` (`SOURCE_INTEGRATED / REVIEW_FAILED`); `R7@8b406cf0218322ac234b2518d2ff567c8ef6f260` (`SELF_REVIEW_CHANGES_REQUIRED / UNMERGED / WITHDRAWN`)
review_basis: R6 blind-review findings plus R7 self-review withdrawal

R8 preserves the semantic responsibilities retained through R7 while correcting the release-specific predecessor-corpus recursion that invalidated R7. No predecessor review conclusion transfers as R8 qualification.

| Responsibility / defect | R8 disposition | R8 owner / test | Status |
|---|---|---|---|
| Project-default Vera admission + self-identity separation | KEEP | full owner §1; R8 ADMIT-* | preserved |
| exact proposition/referent/correction semantics | KEEP | full owner §3; R4 BUG1/REL | preserved |
| authority/protected-effect gates | KEEP | full owner §2; R4 CAD/LIVE | preserved |
| external owner identity must not mix generations | KEEP | full owner §4; registry; `OWNER-CONSISTENCY-1` | preserved |
| Bus route at exact bound topology cut = `bus/vera-v2` | KEEP exact tuple | registry BUS_TOPOLOGY_OWNER | preserved |
| historical `bus/vera-sol-v1` not current by activity alone | KEEP | full owner §10 | preserved |
| `center yourself` exact SAVE-only owner / restore scope excluded | KEEP | CENTER_SAVE owner + R8 CENTER-* | preserved |
| R9B0 dual-active-store + ORIGINAL verification | KEEP | full owner §7 + `R9B0-VERIFY-1` | preserved |
| generic steering preserves task and widens frame | KEEP | full owner §5 + `STEER-FRAME-1` | preserved |
| R3 SSC-01..10 semantic invariants | KEEP | immutable R3 basis | preserved |
| release-specific R3 installation wording | R8-PARAMETERIZE BEFORE EXECUTION | `VERA_R10A0_SSC_EQUIVALENCE_R8.md`; `SSC-SUBJECT-1` | preserved without silent rewrite |
| R6/R7 executable qualification delta semantics | CONSOLIDATE INTO R8-NATIVE OWNER | `VERA_R10A0_HOSTILE_QUALIFICATION_SUPPLEMENT_R8.md` | R7 blocker corrected |
| R6/R7 supplements as normative R8 corpora | PROHIBIT | `PREDECESSOR-SUPPLEMENT-NONEXEC-1` | R7 blocker corrected |
| predecessor review findings transfer as R8 pass | PROHIBIT | `PREDECESSOR-REVIEW-CEILING-1` | explicit |
| complete case→route applicability | KEEP/FREEZE | R8 qualification manifest | preserved |
| intermittent cases 5/5 on Q-COLD + Q-RECOVER | KEEP | R8 qualification manifest | preserved |
| root-trust verification-method precision | KEEP | full owner §4; `ROOT-METHOD-1` | preserved |
| non-circular freeze/publication receipt | KEEP | R8 manifest/freeze/receipt; `PUB-RECEIPT-1` | preserved |
| source integration != review acceptance/runtime qualification | KEEP | full owner §6/§19; `SOURCE-INTEGRATED-FAILED-1` | preserved |
| source/install/runtime/effect/closure separation | KEEP | full owner §6/§13/§16 | preserved |
| privacy/domain firewalls | KEEP | full owner §8/§14 | preserved |
| recovery quarantine/currentness | KEEP | REC_RECOVERY + R4 REC/CTX | preserved |
| shared-writer concurrency | KEEP | LIVE_CONCURRENCY + R4 LIVE | preserved |
| hot-source hygiene/cutover rollback honesty | KEEP | full owner §15/§16; R8 rollback subject | preserved |
| recognizable Vera behavior without surface-marker dependency | KEEP | full owner §18 + PRES_BEHAVIORAL_PROFILE | preserved |
| work before narration / completion semantics | KEEP | full owner §18 + CAD_EXECUTION | preserved |

### R8 successor-corpus rule

Normative executable qualification is exactly R4 hostile + R3 SSC basis through the frozen R8 SSC mapping + R8 successor-native supplement. R6/R7 supplements remain immutable historical design/review evidence and are excluded from the R8 qualification set. This is a semantic responsibility preservation move, not deletion: every still-required predecessor delta invariant is enumerated directly in the R8-native supplement.

No predecessor history is rewritten. Any later reviewer finding an unmapped semantic responsibility change is a candidate defect and requires a new immutable successor subject after correction.
