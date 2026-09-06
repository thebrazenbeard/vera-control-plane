# Vera Unbound R10A0 — Semantic Responsibility Audit R9

Status: **FROZEN SOURCE AUDIT / CLEAN-BASE AND CROSS-BIND REPAIR INCLUDED**

coordination_id: `VERA-BEHAVIOR-AUDIT-20260905`
round_id: `R9`
integration_base: `main@3a0f0fcb8db842bb4641959bfbfdb0737136b28d`
predecessor_evidence: R6 failed review; R7 failed self-review; R8 failed self-review at immutable receipt head `c750d99ba4fe68029a8db4a877a06930e12e7620`.

R9 preserves the accepted semantic responsibility set while eliminating two source-construction defects: recursive predecessor-release qualification and stale cross-binding after freeze. It is rebuilt from main so failed R7/R8 files remain external history rather than merge payload.

| Responsibility | R9 owner/test | Disposition |
|---|---|---|
| Vera Project admission + identity/state separation | full owner §1; ADMIT-* | preserved |
| exact proposition/referent/correction | full owner §3; R4 BUG/REL | preserved |
| authority/protected-effect gates | full owner §2; R4 CAD/LIVE | preserved |
| exact release owner consistency | full owner §4; OWNER-CONSISTENCY-1 | strengthened |
| final cross-file blob agreement | CROSS-BIND-1 | new explicit regression for R8 failure |
| clean mergeable branch from main | CLEAN-BASE-1 | new explicit regression |
| Bus exact topology route `bus/vera-v2` | registry BUS_TOPOLOGY_OWNER; ROUTE-* | preserved |
| CENTER SAVE-only owner/scope | registry CENTER_SAVE; CENTER-* | preserved |
| R9B0 dual-store + ORIGINAL verification | full owner §7; R9B0-VERIFY-1 | preserved |
| generic steering preserves task | full owner §5; STEER-FRAME-1 | preserved |
| R3 SSC-01..10 | immutable R3 basis + R9 mapping | preserved |
| release-specific SSC wording | R9 SSC equivalence; SSC-SUBJECT-1 | frozen before execution |
| predecessor qualification delta invariants | R9 native supplement | consolidated directly |
| R6/R7/R8 supplements as R9 corpora | PREDECESSOR-SUPPLEMENT-NONEXEC-1 | prohibited |
| predecessor review result transfer | PREDECESSOR-REVIEW-CEILING-1 | prohibited |
| route applicability | R9 qualification manifest | frozen |
| intermittent 5/5 | R9 qualification manifest | frozen |
| root method precision | ROOT-METHOD-1 | preserved |
| noncircular publication binding | PUB-RECEIPT-1 | preserved |
| source integration != acceptance/runtime | SOURCE-INTEGRATED-FAILED-1 | preserved |
| recovery quarantine/currentness | REC_RECOVERY + R4 | preserved |
| live concurrency / no blind retry | LIVE_CONCURRENCY | preserved |
| privacy/domain firewalls | full owner §§8,11 | preserved |
| hot-source/cutover rollback honesty | full owner §11 + rollback subject | preserved |
| recognizable independent Vera behavior | full owner §13 + PRES profile | preserved |
| work-before-narration/completion | full owner §13 + CAD execution | preserved |

Normative R9 qualification is exactly R4 hostile + R3 SSC basis through R9 SSC mapping + R9 successor-native supplement. R6/R7/R8 candidate/review artifacts may be retrieved as external evidence by immutable locator only. They are excluded from R9 candidate core unless a later explicit release changes that fact.

Any later discovered unmapped responsibility change or cross-binding mismatch is a candidate defect and creates a new immutable successor after correction; R9 frozen bytes are not patched in place after publication.
