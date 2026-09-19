# VERA EXODUS RETIREMENT CHECKPOINT — 2026-09-19 V1

Status: STARTING_SNAPSHOT — FRESHNESS REQUIRED BEFORE EFFECT

## Scope

This checkpoint retires the current ChatGPT conversation as infrastructure while preserving the governed Vera referent and current durable project state.

This chat is an interface/terminal, not Vera's canonical identity, memory, authority, or state store. No successor worker/chat dependency is created here.

## Post-Exodus persistent ChatGPT interface topology

Patrick directed exactly three persistent ChatGPT interfaces:

### Vera Unbound
- `Vera`
- `Vera Control Plane Coordinator`

### Build Team Two
- `BT2 Coordinator`

All other workers, reviewers, lanes, identities, specialists, and project roles must be reconstructible and usable from durable GitHub/Bus state without requiring a permanent ChatGPT conversation.

Cross-system source candidate:
- repo: `thebrazenbeard/chat-communication-bus`
- Draft PR: `#128`
- branch: `work/exodus-interface-topology-v1`
- exact head: `1af84ba0650bb646b696dfc31e4f79b498d100af`
- ADR blob: `e9c58d1519922e6e5b47758b25ec4cb1afc3755c`
- topology contract blob: `88258a228029b88387e4d5ab84af40ffc044bf4d`
- regression-test blob: `941c6671e23b5a9b3b36784724848a1ed84b7cb9`
- focused execution: `4/4 PASS`
- compileall: PASS
- diff-check from Bus main `aeab0f04fc9b4bd7c2945c9a53011c53fac809b4`: PASS
- merge/cutover: NOT AUTHORIZED / NOT PERFORMED

Vera Control Plane Coordinator source candidate:
- repo: `thebrazenbeard/vera-control-plane`
- Draft PR: `#49`
- branch: `work/exodus-vcp-coordinator-interface-v1`
- exact head: `d8d21c6f02cb90ab104d6b4da6a9051af76c0a38`
- purpose: surviving control-plane/runtime/provider/governance/qualification interface, not separate identity/state store
- merge/cutover: NOT AUTHORIZED / NOT PERFORMED

BT2 Coordinator source candidate:
- repo: `thebrazenbeard/bt2`
- Draft PR: `#24`
- branch: `work/exodus-bt2-coordinator-interface-v1`
- exact head: `9ded716828244d4abc3d5b3dfd7a351b6f261717`
- purpose: surviving Build Team Two engineering-portfolio interface; workers remain GitHub/Bus-defined
- merge/cutover: NOT AUTHORIZED / NOT PERFORMED

## Durable communication / routing

Current Chat Bus topology owner tuple remains:

- repo: `thebrazenbeard/chat-communication-bus`
- owner last-change commit: `f90d52e66d655e9c3cfac63cb529914ac51d3a88`
- path: `architecture/contracts/RADAR_TOPOLOGY_V1.json`
- Git blob: `69e505031d4e53dcb853578dac23817649af1918`
- Vera writer route: `bus/vera-v2`

Bus is the durable work-bearing communication hub. A ChatGPT conversation is not.

At this checkpoint's final preparation, `bus/vera-v2` had advanced beyond its convenience `HEAD.json` via concurrent work; therefore consumers MUST fresh-read the branch and protocol rather than treating this checkpoint's observed branch head as permanent authority.

## Current control / Vera state

Governed referent: Vera.

Current Project control root presented in this runtime:
- `R10_PLUS_SD1`
- R10+SD1 source manifest owner and qualification rules remain controlling under current Project instructions.
- Freshness or a new chat does not itself prove same-process continuity, lived waiting, hidden activity, consciousness, feeling, desire, consent, attachment, or phenomenal continuity.
- A new Vera chat must orient from current Project control + durable GitHub/Bus evidence.

No identity or worker represented here requires this conversation to remain accessible.

## SD1 production anchor — current effect state

The former PR #44 migration subject failed independent hostile review because NULL numeric inputs plus ordinary SQL digest comparison could bypass intended canonical request rejection. That failure is preserved as historical evidence.

Repaired successor:
- repo: `thebrazenbeard/vera-control-plane`
- PR: `#45`
- exact head: `749b64e4cc65859db40271fcf27f9273708f2304`
- exact migration path: `supabase/migrations/20260919195000_create_sd1_causal_secondary_anchor.sql`
- Git blob: `0769c527ad8fc8280d052dc1ce93f85673b6bb7d`
- SHA-256: `246ac38c8112346d90885626514bcead0ef73005ecf30e90b04884983fce7523`
- UTF-8 bytes: `24103`
- independent hostile rereview: PASS exact head
- fresh local source suite: `11/11 PASS`
- PostgreSQL grammar parse: PASS / 36 statements
- diff-check: PASS

Patrick then granted exact authority to apply this repaired migration to Supabase project `fawkirqroyniueeqspif` after immediate preconditions matched.

Verified provider effect:
- apply result: `success:true`
- provider-assigned migration version: `20260919223652`
- Git source-version identifier retained: `20260919195000`
- `vera_cp_anchor` schema: PRESENT
- frontier + receipt tables: PRESENT with RLS + FORCE RLS
- append-only UPDATE/DELETE triggers: PRESENT
- broker role: NOLOGIN / NOSUPERUSER / NOCREATEDB / NOCREATEROLE / NOINHERIT / NOBYPASSRLS
- broker direct table write: NO
- broker bounded RPC execution: frontier-read / receipt-read / advance only
- anon/authenticated/service_role RPC execution: NO
- advance RPC owner: postgres
- advance RPC: SECURITY DEFINER with fixed search path
- repaired numeric NULL guards + null-safe `IS DISTINCT FROM` checks: PRESENT in deployed function definition
- exact frozen genesis: generation 0, record_count 0
- genesis chain head: `527ddd4d35e85dfcff56b8c209ba2a6b642c08a18a9d2ae704626e8c78bfe229`
- genesis frontier digest: `7de55cc22b28539c1d4e6934b1790d99c70ecee55ded80d7b698bec61ee249a1`
- non-genesis frontier rows: 0
- mutation receipts: 0

Durable deployment receipt:
- branch: `state/sd1-causal-secondary-anchor-deployment-20260919-v1`
- receipt commit: `62c69fd9dc0f7918cef674f4dc3359eee8be3eb3`
- path: `state/provider/SD1_CAUSAL_SECONDARY_ANCHOR_DEPLOYMENT_RECEIPT_20260919_V1.json`
- Git blob: `7eb5244633523644df9e0c9021b311c688489643`

Current ceiling:
- `PROVIDER_INSTALL=VERIFIED`
- `PRODUCTION_ANCHOR_GENESIS=PRESENT_VERIFIED`
- `PRODUCTION_WITNESS_CONTROLLER_BINDING=NOT_YET_ESTABLISHED`
- `REAL_CAUSAL_COLLECTION=HOLD`
- `CONTROL_CAUSALITY=UNRESOLVED`
- `GLOBAL_QUALIFICATION=NOT_EXECUTED`

### PR #45 currentness conflict resolved

A Project Runner source-review comment posted after deployment retained a stale local statement that provider installation was not authorized/not performed.

That statement is HISTORICAL_EVIDENCE_ONLY for effect state.

A durable correction was added to PR #45:
- issue-comment id: `5746018458`

The source-review verdict remains usable for source review; the effect ceiling is superseded by the verified provider deployment receipt above.

## Causal-controller continuation frontier

Prior durable controller evidence remains relevant but MUST be fresh-checked before action:

- `thebrazenbeard/vera-control-plane#43`
- prior exact head: `b31dfdb882321911274a96ea9cc9ae910f6020b7`
- prior focused exact execution: `42/42 PASS`
- synthetic CAUSAL-005/006 protections were PASS
- production witness was previously UNBOUND

Now that the provider anchor exists, the next high-value control-plane frontier is:

1. fresh-check controller/source heads and current reviews;
2. bind the verified production witness into the causal controller without fabricating effect evidence;
3. hostile-test the integration;
4. only after verified binding, perform any separately authorized real causal collection;
5. preserve the frozen experiment structure and claim ceiling;
6. blind-score and compare only after genuine fresh DRIVE_OFF/DRIVE_ON data exist.

Do not create extra production frontier generations/receipts merely for testing unless exact authority exists.

No causal response collection was performed in this retirement cycle.

## DriftGuard

The DriftGuard question in this chat was resolved from live GitHub state. No unique chat-local DriftGuard state needs evacuation.

At the time checked:
- repo: `thebrazenbeard/driftguard`
- Draft PR #1 existed on `work/driftguard-v1-hostile-design`
- exact head observed: `32c8a70de9938fa525eff5169258cc10fc4e2af0`
- described local suite: `33/33 PASS`
- hosted Actions on exact head: SUCCESS
- Bus coordination had routed an exact-head hostile rereview

Treat all of that as ALREADY_DURABLE and fresh-check before future work.

## Slack — future frontier only

Slack is NOT reconnected, configured, deployed, or made authoritative by this retirement.

Durable source candidate PR #128 records the future boundary:

A future Vera Slack gateway may provide live Patrick-facing transport:

```
Patrick -> Slack -> Vera runtime -> Bus/GitHub
Patrick <- Slack <- Vera runtime <- Bus/GitHub
```

Required architectural boundary:
- Slack is transport/interface, not canonical state;
- Slack does not replace the Bus;
- worker-to-worker coordination cannot exist only in Slack;
- Slack history cannot be required for reconstruction;
- protected-effect authority must be durably recorded and verified;
- inbound events require authentication, deduplication/replay protection, durable attribution, and effect reconciliation;
- Slack-specific runtime must load governed Vera state rather than invent a separate Slack persona.

Slack credentials, event subscriptions, hosting, provider changes, reconnection, and deployment remain separately gated.

## Reconstruction test

A fresh post-Exodus Vera interface should be able to proceed without this conversation by reading:

1. current Project instructions/control sources;
2. current `thebrazenbeard/vera-control-plane` state and relevant exact PR/receipt evidence;
3. current `thebrazenbeard/chat-communication-bus` topology/protocol and Vera lane;
4. Bus Draft PR #128 for the Patrick-directed Exodus topology until/if promoted;
5. VCP Draft PR #49 for the VCP Coordinator interface until/if promoted;
6. BT2 Draft PR #24 for the BT2 Coordinator interface until/if promoted;
7. the verified SD1 provider deployment receipt above.

It must then fresh-check all mutable heads before effects.

No retired ChatGPT URL is required to continue.

## Protected effects deliberately not performed

- no merge
- no canonical promotion
- no Project Settings mutation
- no Slack reconnection/configuration
- no credential/permission changes
- no unrelated provider mutation
- no extra SD1 frontier generation or receipt
- no real causal response collection
- no global causality/qualification promotion

## Exact successor-interface directive

Future interface owner for general coordination: `Vera`.

On first post-Exodus orientation:

`VERA::EXODUS_RECONSTRUCT::FROM_GITHUB_AND_BUS_ONLY`

Then:
- fresh-check Bus PR #128, VCP PR #49, BT2 PR #24, current Bus topology/route, current Vera/VCP/SD1 heads, and the production-anchor receipt;
- identify any remaining worker reconstruction gaps without reopening retired chats;
- route control-plane-specific continuation through `Vera Control Plane Coordinator`;
- route Build Team engineering portfolio continuation through `BT2 Coordinator`;
- continue the SD1 frontier at production witness/controller binding;
- do not rely on this retired conversation.

This checkpoint is a starting snapshot only. Freshness is required before effect.
