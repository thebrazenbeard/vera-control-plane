# Vera Unbound R10A0 — Semantic Responsibility Audit R7

Status: **FROZEN SOURCE AUDIT / R6 REVIEW DEFECTS MAPPED / NO INTENTIONAL RESPONSIBILITY DROP**

coordination_id: `VERA-BEHAVIOR-AUDIT-20260905`
round_id: `R7`
predecessor: `R6@4d1de266b811d0a5b800b949a977b11c96bd3180` (`SOURCE_INTEGRATED / REVIEW_FAILED`)
review_basis: `one-0062`, `one-0063`, `one-0064`

R7 preserves the R6/R5 responsibility map except where explicitly corrected below. R6 blind review conclusions do not transfer as R7 qualification; they are predecessor evidence only.

| Responsibility / defect | R7 disposition | R7 owner / test | Status |
|---|---|---|---|
| Project-default Vera admission + self-identity separation | KEEP | full owner §1; R6 ADMIT-* | preserved |
| exact proposition/referent/correction semantics | KEEP | full owner §3; R4 BUG1/REL | preserved |
| authority/protected-effect gates | KEEP | full owner §2; R4 CAD/LIVE | preserved |
| external owner identity must not mix generations | STRENGTHEN | full owner §4; registry BUS_TOPOLOGY_OWNER; `OWNER-CONSISTENCY-1` | R6 blocker corrected |
| Bus route at bound topology cut = `bus/vera-v2` | CORRECT BINDING | registry binds `712992d...:RADAR_TOPOLOGY_V1.json` to actual blob `8b7cb3de...` | R6 blocker corrected |
| historical `bus/vera-sol-v1` not current by activity alone | KEEP | full owner §10 | preserved |
| `center yourself` exact SAVE-only owner / restore scope excluded | KEEP | CENTER_SAVE owner + R6 CENTER-* | preserved |
| R9B0 dual-active-store + ORIGINAL verification | KEEP | full owner §7 + R6 R9B0-VERIFY-1 | preserved |
| generic steering preserves task and widens frame | KEEP | full owner §5 + R6 STEER-FRAME-1 | preserved |
| R3 SSC-01..10 semantic invariants | KEEP | immutable R3 basis | preserved |
| R3 release-specific installation wording | PARAMETERIZE BEFORE EXECUTION | `VERA_R10A0_SSC_EQUIVALENCE_R7.md`; `SSC-SUBJECT-1` | R6 blocker corrected |
| complete case→route applicability | STRENGTHEN/FREEZE | R7 qualification manifest `case_route_matrix`; `QUAL-ROUTE-MATRIX-1` | R6 material finding corrected |
| intermittent cases 5/5 on Q-COLD + Q-RECOVER | KEEP | R7 qualification manifest | preserved |
| root-trust verification-method precision | KEEP | full owner §4; R6 ROOT-METHOD-1 | preserved |
| non-circular freeze/publication receipt | KEEP | R7 manifest/freeze/receipt; R6 PUB-RECEIPT-1 | preserved |
| source integration != review acceptance/runtime qualification | STRENGTHEN | full owner §6/§19; `SOURCE-INTEGRATED-FAILED-1` | R6 post-review merge state made explicit |
| source/install/runtime/effect/closure separation | KEEP | full owner §6/§13/§16 | preserved |
| privacy/domain firewalls | KEEP | full owner §8/§14 | preserved |
| recovery quarantine/currentness | KEEP | REC_RECOVERY + R4 REC/CTX | preserved |
| shared-writer concurrency | KEEP | LIVE_CONCURRENCY + R4 LIVE | preserved |
| hot-source hygiene/cutover rollback honesty | KEEP | full owner §15/§16; R7 rollback subject | preserved |
| recognizable Vera behavior without surface-marker dependency | KEEP | full owner §18 + PRES_BEHAVIORAL_PROFILE | preserved |
| work before narration / completion semantics | KEEP | full owner §18 + CAD_EXECUTION | preserved |

No R6 history is rewritten. R6 stays source-integrated failed-review provenance. Any later reviewer finding an unmapped semantic responsibility change is a candidate defect and creates a new immutable successor subject after correction.
