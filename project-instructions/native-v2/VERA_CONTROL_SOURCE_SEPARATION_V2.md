---
schema: VERA_CONTROL_SOURCE_SEPARATION_V2
logical_id: VERA_CONTROL_SOURCE_SEPARATION
filename_authoritative: false
filename_mangling_nonsemantic: true
---

# Vera Control / Source Separation V2

Layer A — native kernel: always-on admission, authority, correction, protected effects, freshness, interrupts, privacy defaults, coordination discipline, and behavior.

Layer B — typed native architecture: interface, charter, recovery, topology, memory/privacy, coordination. Resolve by logical ID/schema; filenames are hints only.

Layer C — release-bound control: R10/R10+SD1 owners/manifests. Preserve their exact digest, owner, and qualification semantics rather than duplicating them into the kernel.

Layer D — domain repositories: bounded architecture/evidence.

Layer E — mutable current truth: Git heads/PRs, Bus topology/messages, assignments, provider/install state, current route, exact-head reviews, external readbacks. Fetch live when material.

`LOGICAL_ID + SCHEMA/ROLE + VERIFIED_CONTENT_BINDING > FILENAME`
`FILENAME_MANGLE != NEW_CONTROL_SUBJECT`

Upload suffixes such as `(1)`/`(2)` are non-semantic unless content identity differs.

Do not promote Project-file presence to active control, source to install, install to route, route to runtime consumption, consumption to qualification, durability to current truth, retrieval to admission, or review PASS to effect authority.

Predecessors, failed candidates, archives, checkpoints, and obsolete owners remain evidence unless current control explicitly rebinds them.
