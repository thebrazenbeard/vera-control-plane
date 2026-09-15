# SD1-V checkpoint — live Project predecessor classification — 2026-09-14T2014-0400

lane: `SD1-V`
source_bus_commit: `6316ae959eebcbef61d46f324465e98437b7bcca`
status: `READ_ONLY_PROJECT_PREDECESSOR_CAPTURE_PARTIAL / NO_PROJECT_MUTATION`

Fresh source heads remain blocked: PR #23 `93957daa6f9b0054c4158164167cfecc1aa41803` has open `SD1-V-CP-004`; PR #24 `514530f1e4e62185af0e8ff2f699667fa92bd815` remains `CAUSAL_DATA_HOLD` for VM-SD1-CAUSAL-001..003 independently reproduced by SD1-V.

## Live Work probe classification
- `PROJECT_CONTEXT_IDENTITY = VERIFIED`: live UI identified `Vera Unbound` at the Project route.
- `PROJECT_SETTINGS_SURFACE = READABLE`: settings exposed Project name, editable Instructions, Memory, Library access, sharing/delete surfaces.
- `PROJECT_INSTRUCTIONS_PREDECESSOR_CAPTURE = PARTIAL_READABLE_NOT_IMMUTABLY_BOUND`: the live `#instructions` textarea value was read directly without edit/submit, but the durable Bus receipt does not include the exact text/byte count/hash. Therefore exact rollback bytes are not yet independently bound.
- `PROJECT_MODEL_CONFIG_PREDECESSOR_CAPTURE = PARTIAL_COMPOSER_ONLY`: Work composer showed `GPT-5.6 Sol Light`, Power `Light, 2 of 5`, fast mode off. Project settings exposed no Project-level default model/power field, so composer state must not be silently promoted to a Project default.
- `PROJECT_SOURCE_INVENTORY_CAPTURE = VERIFIED_VISIBLE`: exactly the two R10 Project files were visible in the settings/source surface.
- `SUPPORTED_WRITE_SURFACE_VISIBLE = PARTIAL`: Project name and Instructions were editable controls, but no Save/Update control was visible; write semantics were not exercised.
- `SUPPORTED_POST_WRITE_READBACK_VISIBLE = UNRESOLVED`: same-modal pre-write readback exists, but no authorized write/post-write cycle has established an independent effect readback path.
- `LIVE_MUTATION_PERFORMED = NO`.

## Gate consequence
`PROJECT_PREDECESSOR_ROLLBACK_FIDELITY = PARTIAL_NOT_READY`.
The probe materially upgrades settings visibility from unavailable to readable, but it does not yet satisfy exact `PROJECT_SETTINGS_BYTES` because the durable evidence does not bind the full live textarea value to immutable bytes/digest. Source files remain supporting evidence only. No install is approved.

Next evidence request: persist the exact live Instructions textarea value or an exact faithful export with byte count + SHA-256, and preserve the observed Project/source/model-config metadata separately. Do not mutate the field to prove writability.
