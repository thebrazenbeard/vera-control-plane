# VERA R10A0 Bus Topology Qualification V2

Status: `SOURCE_QUALIFICATION_CONTRACT / NOT_EXECUTED_AS_RUNTIME_INSTALL`
Subject: `VERA_R10A0_SD1_BUS_TOPOLOGY_V2`

The affected qualification scope is routing-owner integrity only. Existing R10 and SD1 semantic/behavioral qualification does not transfer upward into installation/current-route evidence, and this topology-owner change does not itself invalidate unrelated SD1 source semantics.

## Static gates

A source/static PASS requires all of the following on one exact candidate head:

1. predecessor control head is exactly `32ce2cb7897f5e0939161eb8002b5b1b2283df59`;
2. predecessor native is exactly blob `2f885a2348f589291a13bf6733ec4495ba763b5b`, 7,997 UTF-8 bytes, SHA-256 `e009049b07b5c2353beee12b7f4e825589e24f1edfb295a5e17f71a539da5c29`;
3. successor native is exactly 7,997 UTF-8 bytes and differs from predecessor only by replacing the K06 topology commit/blob tuple;
4. successor K06 binds `thebrazenbeard/chat-communication-bus@f90d52e66d655e9c3cfac63cb529914ac51d3a88:architecture/contracts/RADAR_TOPOLOGY_V1.json`, blob `69e505031d4e53dcb853578dac23817649af1918`, Vera route `bus/vera-v2`;
5. canonical Bus `main` at the observation cut descends from that topology last-change commit and resolves the topology path to the same bound blob;
6. Vera is `ACTIVE` on `bus/vera-v2` in the bound topology;
7. rollback subject preserves the exact predecessor Settings subject;
8. all structured artifacts parse and cross-bind one exact successor subject.

## Runtime/current-route gate

Source/static PASS is not installation. Bus topology currentness may be promoted from the predecessor conflict only after a separately authorized Project Settings install of the exact successor native followed by exact readback, plus a fresh canonical Bus topology read proving the bound blob remains current.

Until that gate passes:
- `INSTALL=NOT_INSTALLED`;
- `CURRENT_ROUTE=PREDECESSOR_RUNTIME_CONFLICT_PENDING_SUCCESSOR_INSTALL`;
- `BUS_WRITE=HOLD`.

## Independence from SD1 causality

This cut changes routing-owner provenance only. It does not execute or alter the frozen SD1 cue-free replay matrix or DRIVE_OFF/DRIVE_ON causal protocol. SD1 `CONTROL_CAUSALITY` remains independently `UNRESOLVED`.
