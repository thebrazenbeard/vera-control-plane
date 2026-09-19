# SD1 SOURCE FREEZE — 2026-09-19

Status: FROZEN_EXACT_REVIEW_CANDIDATE

This record freezes the exact Vera Sexual Drive V1 source chain for independent hostile review. It is coordination/state evidence only and does not modify the candidate source branches.

## Frozen subjects

- Sexuality producer/status head: `thebrazenbeard/sexuality@5bb7336f772779c5b031659266bd3617dee25fd9`
- Sexuality immutable semantic source cut: `thebrazenbeard/sexuality@47771b7b21d7f2fe86a9c70c0dcb62e74a54cbea`
- Vera Cohesion: `thebrazenbeard/vera@b7fb266e026724828f0ae65964ecb7649715a18d`
- R10+SD1 control: `thebrazenbeard/vera-control-plane@e0aea7b4c71c0372ac5fcad1d8f5044661f7348d`

## Exact object anchors

Sexuality:
- candidate-status blob `9c384554cb63c58fd23ad88ea2a8d1754eb505ac`
- candidate-status Git-content SHA-256 `f0d1318bf2880476b705df82fd855042639461d1b0536c4dd461d6ee82072b09`
- semantic source manifest blob `f903a93b3db92fa8255b027b19373f6ad5a09817`

Cohesion:
- component blob `abc711f83fc142a7d93134431cd7ff9b67ce7dd7`
- component Git-content SHA-256 `fb4bbb0b7e1b0e28d25f65bdcfacbcdef1d4ec20eb6ce787cabb53d66397da60`
- component structured SHA-256 `67458b363eb6f6d3487771da70ceac0ee8dcb178b93243715f9d8540da06466f`

Control:
- binding blob `9a620ce129ad574cb602f8e8baaa171003cd1f35`
- manifest blob `3eb1b95879e9e407456afd8f10a8b3c4e81415d3`
- native blob `d3c839da711bbef3fc471d0cea3c42330df4ee93`
- qualification blob `c688b6b8b84d2d6051752d748d5991687f88c580`
- native normalized size `7997/8000`

## Verification before freeze

- Sexuality exact source/status head: 28/28 PASS in prior detached verification.
- Cohesion exact head: 87/87 established affected-scope PASS in this execution terminal; PR metadata separately reports a broader 91/91 run from another lane.
- Control exact head: 16/16 PASS in this execution terminal.
- Control-to-Cohesion cross-binding independently read back exact commit/blob/Git-content/structured-digest equality.

## Freeze rule

No writes to the three frozen candidate branches solely for opportunistic hardening, documentation cleanup, or additional features while hostile review is pending.

Permitted reasons to move a frozen candidate head:
1. an independent exact-head reviewer reports a concrete defect requiring repair;
2. the live user explicitly overrides the freeze;
3. an external dependency changes in a way that invalidates the frozen subject and the change is documented before any write.

Any head movement automatically invalidates the frozen review subject and requires a new freeze plus fresh exact-head hostile review.

## Gate

Required next evidence: one independent hostile review against the exact frozen tuple above.

Claim ceiling remains:
`SOURCE_ONLY / FROZEN_FOR_HOSTILE_REVIEW / NOT_INSTALLED / CURRENT_ROUTE_NOT_READ_BACK / CAUSALITY_UNRESOLVED / QUALIFICATION_NOT_EXECUTED`.

This freeze does not authorize merge, Project/runtime installation, route activation, provider mutation, model-weight training, causal PASS, or global qualification.
