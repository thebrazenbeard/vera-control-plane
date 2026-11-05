# Portal → ProjectRunner → Executor: source-only negative contract probe

Status: **DRAFT / HOLD / NOT INSTALLED / NO EXECUTION AUTHORITY**. Event `project_unfuck_runtime_coordination`.

This public-source document and standalone regression probe bind specific **published source code**, not a user's installed runtime, current credentials, private consent, or execution history. No actual workstation IPC, Executor MCP call, protected effect, credential, service launch, paid provider, or public Bus write is performed.

## Exact source subjects

| Component | Pinned repository commit | Relevant source | Git blob ID |
| --- | --- | --- | --- |
| Portal | `a27db806c064248cba5cf109aa8a4866df4fb8d1` | `portal/desktop_ipc.py` | `330028c1d0c63b77836a63c8a94a0a6c51423427` |
| Portal | same | `portal/capability_admission.py` | `0fc7067807aa5a5f16716f01f87e706d6102d958` |
| ProjectRunner | `44da26e02c39591118bf1fdfe7ec01bd1103fc66` | `runner/sqlite_state.py` | `c829398d6cfa31d0fbffa54cf072f7f3c36af35c` |
| Executor | `9838c0f840e3bcf946d7ed6b767b00b89d5a5d86` | `src/effect-ledger.ts` | `09b09790ffbefe209c1dc81b92e92321c9540b54` |
| Executor | same | `src/server.ts` | `e2fc19872fbbc5315249500c16771bb7f5257cf9` |
| Executor | same | `src/device-registry.ts` | `9f8421891134f0f9794cf4184fa3f29c4714acab` |

No source blobs are vendored into VCP. An operator can fetch those six **public, exact-commit** files with their own preferred Git tooling and place copies in a disposable directory under the filenames `portal_desktop_ipc.py`, `portal_capability_admission.py`, `projectrunner_sqlite_state.py`, `executor_effect_ledger.ts`, `executor_server.ts`, `executor_device_registry.ts`. No secrets or local runtime state are required. Then run:

```bash
VERA_E2E_SOURCE_DIR=/path/to/disposable/pinned-source-files \
  python tools/contract_probes/portal_runner_executor_probe.py -v
```

The standalone probe verifies Git blob SHA-1 (which binds exact file bytes) **before loading source**, and fails when a source is missing or differs. The repository commits above are separate provenance claims; the operator must fetch from those exact refs. This probe does not automatically fetch live default branches, call host APIs, or start a bridge. Python AST extraction executes the exact selected Portal/Runner class and function bodies using only synthetic dependencies and temporary local files; Executor static tests bind the exact source text. A negative-test PASS is a reproducible finding, not evidence of a safe integrated executor.

## Actual-source negative evidence

1. **Claimed request / lost response:** Portal `FileBridgeClient.request` raises `BridgeOutcomeUnknownError` when a synthetic temp-file claimant moves the request but no response arrives. Retrying that ID raises `FileExistsError`, and no exact receipt readback operation is exposed. Retrying under a **new** request ID could duplicate a real action if a live protected bridge were later wired.
2. **Response consumed:** successful synthetic bridge response is read and then deleted, so the file bridge response alone is not an immutable, independently recoverable receipt.
3. **Holder spoof:** fresh ProjectRunner `SQLiteLeaseStore.claim` accepts an arbitrary nonblank holder string; equality in subsequent lease operations does not authenticate the original principal.
4. **SQLite rollback fork:** after token 1, a SQLite backup is taken. The active branch and the restored branch separately issue the same fencing token 2 to different holders. Thus a SQLite-only monotone counter is not rollback-resistant host authority.
5. **Executor lineage mismatch:** `server.ts` allocates fresh `effectId = randomUUID()` for every dispatched client request, while `device-registry.ts` allocates a separate downstream request UUID. `effect-ledger.ts` stores outcomes in a volatile capped Map. Authenticated `GET /effects` returns `recent()` state; it does not supply an immutable exact-ID receipt contract. An MCP JSON-RPC ID is not a host-owned idempotency/receipt key.
6. **Capability source gate:** Portal `admit_capability` v0 explicitly rejects protected effects as `PROTECTED_EFFECT_NOT_IMPLEMENTED`, returning `NOT_EXECUTED` / `SOURCE_GATE_DECISION`. Source admission does not establish dispatch.

**Route disclosure:** `thebrazenbeard/chat-communication-bus` is currently **public** (live GitHub visibility). Its issue/comment/branch history is unsuitable for intent payloads, private consent, holder secrets, execution receipts, or protected operation routes. Public-safe hashes and pointers only.

## Contract for a future no-effect adapter qualification

This is a proposed future contract, **not** a capability available to Portal or Executor today:

```text
EffectIntentV1:
  operation_id          caller-independent stable opaque ID, minted once
  payload_digest        canonical exact intent+effect+scope digest
  protected_effect      never inferred from an ordinary text prompt
  expected_host         exact host/device identity
  source_identity       exact repository commit and installed artifact digest
  holder_evidence_ref   host-verified principal, not caller-supplied holder text
  capability_grant_ref  independently current scoped grant, not a model claim
  fence_epoch           host-owned durable monotone lease epoch
  private_route         bound authenticated adapter; never public Bus

EffectReceiptV1:
  operation_id          equal to admitted operation ID
  payload_digest        immutable expected digest; conflict on mismatch
  installed_identity    observed dispatching process/artifact identity
  disposition          RECEIVED / ADMITTED / DISPATCHED / COMPLETED /
                       FAILED / OUTCOME_UNKNOWN
  effect_result_digest  exact outcome digest if independently witnessed
  private_readback      authenticated same-ID durable receipt retrieval
```

Producer requirements:

- Portal may mint an intent and carry its ID through Runner but must not treat the read-only capability gate, model output, or file bridge as an authority issuer.
- Runner's local SQLite work budget/lease is scheduling data, not an independently authenticated or rollback-proof host execution grant.
- A separately authorized, host-owned verifier must bind principal, current scoped consent/grant, fencing epoch, actual installed process/package digest, and intended operation before Executor dispatch.
- Executor's **optional adapter-specific** boundary must persist an atomic `(operation_id, payload_digest)` admission record before dispatch, return the exact prior receipt for repeated identical calls, reject same-ID/different-digest calls, and never replay `OUTCOME_UNKNOWN` automatically. Do not change or mischaracterize Executor's generic full-authority MCP surface as a restricted command runner.
- The private receipt store must survive process restarts; its authenticity and monotonic lease epoch must survive local SQLite restore. A state value in a rollbackable DB is insufficient by itself.
- Separate follow-up release evidence must bind installed process bytes, route, device principal, host-owned lease, restart/failure injection, exact receipt readback, safe rollback, and effects authority. CI/source success is not deployment.

> **Hostile review:** Carrying the same UUID through three layers does not create exactly-once delivery. A forged holder string, old SQLite fencing token after backup restore, ambiguous device send, mismatched installed code, or public coordination route can each invalidate the contract while source unit tests remain green. Any protected operation remains HOLD until independent installed-host evidence and Patrick's exact scope authority are present.

## Ownership / persistence boundary

This addition is isolated to `docs/integration/PORTAL_RUNNER_EXECUTOR_SOURCE_CONTRACT_PROBE_20261105.md` and `tools/contract_probes/portal_runner_executor_probe.py`. It does not alter `project-instructions/native-v2/`, a release manifest, `tools/validate_vcp_integrity.py`, active Portal or Executor modules, services, devices, and other current PR owners' files. A Draft PR does not itself authorize merge, provider changes, installed Project updates, financial actions, canonical memory, or protected execution.
