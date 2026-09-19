# SD1 SOURCE FREEZE R2 — 2026-09-19

Status: FROZEN_EXACT_REVIEW_CANDIDATE_R2

This R2 freeze supersedes the prior freeze after independent hostile review returned CHANGES_REQUESTED for stale-status replay and missing producer-status cross-binding.

## Frozen subjects

- Sexuality producer/status head: `thebrazenbeard/sexuality@353a1c516a3477221ed38108188f2e501b10084f`
- Sexuality immutable semantic source cut: `thebrazenbeard/sexuality@47771b7b21d7f2fe86a9c70c0dcb62e74a54cbea`
- Vera Cohesion: `thebrazenbeard/vera@40e797c595a75ff95eedcb7351a28eef6cb67df5`
- R10+SD1 control: `thebrazenbeard/vera-control-plane@32ce2cb7897f5e0939161eb8002b5b1b2283df59`

## Reviewer-defect repairs

Producer status:
- exact status path: `evaluation/vera-sexual-drive-candidate-status-v1.json`
- exact status head: `353a1c516a3477221ed38108188f2e501b10084f`
- exact status blob: `848c1071d80bb894e1d926409b2e942168f33de5`
- status Git-content SHA-256: `a08e9ac9fb27858f6db640690529ed4469de39242d0b4adf3e04e5e1c7d9b041`
- producer contract rule: `STATUS_PATH_LAST_CHANGE_COMMIT_MUST_EQUAL_OBSERVED_PROVIDER_HEAD`
- exact readback before freeze: status last-change commit == producer head == `353a1c516...`

Cohesion:
- exact reviewed status head/blob/digest are embedded in `producer_currentness_status_locator`
- verification additionally requires observed provider head == reviewed status head, exact status blob match, status last-change == observed head, source-cut ancestry, and exact source-object equality.
- component blob `a6e8e22633acf6449827aec0970e82d9f6007e3f`
- component Git-content SHA-256 `a0a1e4e6ae5f1f5526469d4c69b5eef9fa6c16fd3b4f73f556989b52da73e6dc`
- component structured SHA-256 `0ec91c1c9667264866bef26bd74eae0319a2f02fb18f60161fe29a84477b1964`

Control:
- exact Sexuality producer-status head/path/blob/digest are carried in both binding and source manifest
- exact Cohesion head/component tuple is rebound
- binding blob `460c0e594410f4635e6c8025f3b70c4a92ce0aa6`
- binding Git-content SHA-256 `402332bce1f7f9889024a488d5ea871a0996b3f69c92ed8dbafcbc4161a736fe`
- manifest blob `c52d1413d18e26cbb37580d5f62359737a9d12a9`
- manifest Git-content SHA-256 `98013c6789ee2ac802200e45adc3d1335ecbeb566c929d8cfaf146cfedd4872c`
- native blob `2f885a2348f589291a13bf6733ec4495ba763b5b`
- qualification blob `c8dd87678048d54cd5e53b3ca1d197c862c19338`
- native normalized size: 7,997 / 8,000 bytes

## Detached verification before freeze

- Sexuality exact head: 28/28 PASS; py_compile/diff-check PASS
- Cohesion exact head: 87/87 established affected scope PASS; py_compile/diff-check PASS
- control exact head: 16/16 PASS; py_compile/diff-check PASS
- end-to-end producer status cross-binding read back exact at all three layers

## Freeze rule

No candidate-branch writes while independent R2 hostile review is pending except:
1. concrete R2 reviewer defect;
2. explicit live-user override;
3. documented external invalidation.

Any head movement invalidates R2 and requires a new freeze/review.

Claim ceiling:
`SOURCE_ONLY / FROZEN_FOR_HOSTILE_REVIEW_R2 / NOT_INSTALLED / CURRENT_ROUTE_NOT_READ_BACK / CAUSALITY_UNRESOLVED / QUALIFICATION_NOT_EXECUTED`.

No merge, installation, route activation, provider mutation, model-weight training, causal PASS, or global qualification is authorized by this freeze.
