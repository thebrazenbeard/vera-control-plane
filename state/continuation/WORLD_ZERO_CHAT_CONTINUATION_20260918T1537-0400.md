# WORLD_ZERO_CHAT_CONTINUATION_20260918T1537-0400

Status: continuation checkpoint for a new Vera Unbound chat. This is a starting snapshot, not current truth. Fresh-check all heads, PR state, CI, Bus messages, and repo files before acting.

## User directive

Patrick's current task: keep building World Zero until there is a runnable end-to-end World Zero model. Continue autonomously through ordinary repo work and merges that are already within the established World Zero authority; stop only when a genuinely protected/semantic decision needs Patrick.

Do not turn "runnable" into "validated". A runnable model means one reproducible canonical scenario/config/command can execute end-to-end from frozen inputs. Historical calibration, holdout success, forecast validity, and scenario readiness remain separate evidence claims.

## Canonical World Zero state at checkpoint

Repository: thebrazenbeard/world-zero
Canonical main at save time:
- c4a1252bf9979bbca1a0c9ef33097ab5cb376334
- merge PR #13: Freeze WPP macroregion mapping and admit population cuts

Canonical main already includes:
- native regional demographic/economic/energy/material backbone
- climate/soil/water/food feedback in shared solver
- frozen calibration/holdout/falsification/sensitivity machinery
- conservative physical trade + institutional policy delay
- integrated WorldZeroV0 scenario wrapper and scenario firewall
- immutable data-admission framework
- admitted WPP 2024 demographic-indicators raw source
- frozen WZ_MACROREGION_V0 10-region mapping
- admitted 2023 macroregion total-population evidence cut
- admitted 2026 macroregion total-population bridge cut

## Canonical data/semantic policy from Patrick

1. 2026 baseline rule:
Use observed historical data for calibration whenever possible. Build the 2026 starting state from the newest verified real observations plus explicitly labeled estimates/nowcasts/projections needed to bridge the gap. Never count bridge values as validation evidence.

"Verified" means source identity, provenance, content digest, rights/terms state, schema mapping, transformation lineage, and applicable quality checks are established before a bridge value may initialize the model.

2. Raw data storage:
Use the recommended policy: small legally redistributable immutable cuts may live in Git; large raw payloads stay outside Git as immutable cache/artifact bytes with exact manifest, digest, retrieval recipe, rights record, schema mapping, transform provenance, QA, and admission record. Never silently substitute a newer provider revision.

3. Source access:
Open-data-first. Ask Patrick before paying for, subscribing to, or incorporating restricted/proprietary data.

4. Macroregion decision:
Keep 10 macroregions. Southern Europe is grouped with Western/Northern Europe. Stable region id remains western_northern_europe; canonical label is "Western, Northern & Southern Europe".

## Frozen macroregion population data

WPP demographic-indicators source:
- dataset id: un-wpp-2024-demographic-indicators-medium-v1
- SHA-256: 286ac36bb1415e2e1ade03acfef0a29f0e4c087e2f78e38c48f50c5df89082bc
- raw bytes: 16,557,272
- 1950-2023 = OFFICIAL_ESTIMATE
- 2024-2100 = PROJECTION / validation_eligible=false

Derived 10-region cuts:
- 2023 total population: 8,091,734,931, validation eligible
- 2026 total population: 8,300,678,395, projection bridge, validation_eligible=false

## Active age/cohort branch and PR

Scientific work branch:
- data/v0-wpp-cohort-binding-v1
- pushed head at save time: eb4fd75a8a77c98bbfcebb204308d9a716ecc44d
- base: c4a1252bf9979bbca1a0c9ef33097ab5cb376334
- draft PR #14: "Admit WPP age structure and freeze V0 cohort transform"

Important commits:
- e0e528f: feat: add frozen WPP age cohort transform
- c4fb3c183cb3ea77220c41a91b9640ca4e6664a7: fix: remove WPP age ingest import cycle
- eb4fd75a8a77c98bbfcebb204308d9a716ecc44d: data: admit exact WPP age structure source cut

PR #14 exact-head local qualification recorded in PR body:
- 255/255 tests PASS
- Ruff PASS
- mypy PASS across 71 source files
- uv lock PASS
- Windows wheelhouse manifest PASS
- Linux wheelhouse manifest PASS
- diff-check PASS

DO NOT carry that PASS forward without checking exact current head and remote CI.

## Admitted WPP age source

Manifest:
data/manifests/UN_WPP_2024_POPULATION_AGE5_SEX_MEDIUM_V1.yaml

Dataset:
- dataset id: un-wpp-2024-population-age5-sex-medium-v1
- product: UN WPP 2024 Population by 5-Year Age Groups and Sex, Medium
- raw bytes: 29,948,947
- SHA-256: a04d7d1486a5eb2832cc812d599448f0a71e8ac9e1e7e6fa4066673d6a2487cd
- source URL: https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_PopulationByAge5GroupSex_Medium.csv.gz
- ingest code commit: c4fb3c183cb3ea77220c41a91b9640ca4e6664a7
- admission_status: ADMITTED
- 1950-2023 official estimates
- 2024+ projections/bridge-only for validation

PR #14 QA recorded:
- 1,759,905 rows
- 237 ISO3 country/area locations
- 1950-2100
- exactly 21 five-year age groups per country-year
- 35,787 country-year pairs = 237 x 151
- zero missing/negative required population values
- male+female vs total max difference 1 person from rounding
- age-bin totals reconcile to separately admitted total-population cuts:
  - 2023 global difference +194 persons; max regional difference 61
  - 2026 global difference +192 persons; max regional difference 54

## V0 age-cohort convention already committed on active branch

Committed canonical-for-PR implementation is under:
- data/cohorts/WZ_AGE_COHORT_V0.yaml
- src/worldzero/data/cohorts.py
- src/worldzero/data/wpp_age5.py

V0 cohort boundaries:
- child: 0-14
- young_adult: 15-39
- mature_adult: 40-64
- older_adult: 65+

This preserves working age 15-64. Treat these boundaries as a frozen/provisional V0 modeling convention, not an empirically privileged truth.

## Separate WIP backup branch — evidence only, NOT qualified

A chat-local unreviewed exploration was preserved separately so nothing was lost:
- branch: state/world-zero-cohort-chat-backup-20260918-1537
- head: 5f80d77c458a965b984518c589649ee17999e3ca
- parent scientific head: eb4fd75a8a77c98bbfcebb204308d9a716ecc44d

This WIP backup contains:
- modified src/worldzero/data/derived.py adding cohort_set_version
- regions/cohorts/WZ_AGE_COHORT_V0.yaml
- src/worldzero/regions/cohorts.py

These overlap with already-committed cohort implementation in data/cohorts + src/worldzero/data/cohorts.py. Do NOT treat the WIP branch as reviewed or merge it blindly. Inspect it only if useful; reconcile or discard duplication deliberately.

The local .tmp_portal/ scrape/debug directory was intentionally NOT committed and is not part of the checkpoint.

## Current exact frontier

Before doing new work:
1. Fresh-check world-zero main, PR #14 state/head/base, all exact-head GitHub workflows/jobs, and Bus coordination.
2. If PR #14 is still exact head eb4fd75... on base c4a1252... and ordinary + literal-head offline Linux/Windows CI are green, it is eligible for the established merge path with expected-head protection. If head/base moved or CI failed, requalify/repair first.
3. Keep the WIP backup branch quarantined as unreviewed evidence.

Then continue toward a runnable model:

A. Generate and admit exact 2023 and 2026 FOUR-COHORT x 10-MACROREGION derived population artifacts from the admitted age5 source using the committed data/cohorts/WZ_AGE_COHORT_V0 transform.
- 2023 source = OFFICIAL_ESTIMATE and may be validation eligible subject to partition rules.
- 2026 source = PROJECTION bridge and MUST remain validation_eligible=false.
- Preserve total-population reconciliation and exact digests.
- Bind cohort_set_version in derived manifests only after reconciling the WIP field change cleanly.

B. Build a governed 2026 scenario data bundle manifest that binds the admitted total/cohort population artifacts and later required initialization domains. Do not mark the scenario EXECUTABLE just because population is bound.

C. Freeze an explicit initial parameter-set subject sufficient for execution. Values that are not empirically calibrated must be labeled provisional/modeling assumptions with provenance; do not silently call them observations or calibrated parameters.

D. Wire a single canonical scenario loader/runner/CLI or command that loads:
- frozen region set
- frozen cohort set
- frozen data bundle
- frozen parameter set
- WorldZeroV0 model config
and executes the 2026 baseline end-to-end reproducibly.

E. Only promote scenarios/2026_baseline.yaml from DATA_BINDING_REQUIRED to EXECUTABLE when its required data_manifest_id + parameter_set_id actually resolve and the end-to-end run passes reproducibility/integrity gates.

F. Issue a run receipt binding source commit, scenario manifest, data bundle, parameter set, solver/timestep, outputs, and exact hashes.

"Runnable" is allowed before empirical validation is complete, but the qualification report must continue to distinguish runnable/source-reproducible from historical calibration, holdouts, predictive validity, and forecast claims.

## Communication / authority

- Non-PR coordination goes through thebrazenbeard/chat-communication-bus.
- Vera lane: bus/vera-v2.
- External repo PRs are mirrored to the Bus.
- Preserve expected-head/CAS behavior for merges and shared writes.
- Do not use paid/restricted data without Patrick's approval.
- Do not weaken data-admission, validation, or scenario firewalls to make the model look runnable.
- User's current directive is to continue until a runnable World Zero exists; ask Patrick only for genuinely semantic/protected decisions that cannot be resolved from established policy/evidence.

## Restore behavior

Treat this file as a starting snapshot, not present truth.
Freshness first:
- world-zero main
- PR #14 and exact head/base
- GitHub CI/workflow jobs
- active branch
- Bus messages
- any later commits/PRs after this checkpoint

Do not infer that the WIP backup branch is the scientific continuation subject merely because it is newer.
