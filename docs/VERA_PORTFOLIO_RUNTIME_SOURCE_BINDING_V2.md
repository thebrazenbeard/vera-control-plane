# VCP Vera Runtime Source Binding V2

## Purpose

This is the public-safe successor to the source-disposition enforcement mechanism
carried by VCP draft PR #131.

PR #131 remains predecessor evidence. Its frozen 59-repository / 17-member
NO_AUTO_BIND subject is not current portfolio policy.

V2 binds VCP to the qualified Vera PR #203 source subject instead.

## Exact upstream subject

- repository: `thebrazenbeard/vera`
- PR: `#203`
- exact head: `bc5f1f2b5764455d833615d14e3bead640d6d123`
- registry: `architecture/VERA_RUNTIME_SOURCE_REGISTRY_V2.json`
- registry blob: `427fe21437a3397e184a5b5373fd4ea10f58123c`
- public cut: `architecture/portfolio/VERA_PORTFOLIO_PUBLIC_CUT_V2.json`
- public-cut blob: `cbd1e2d659f9fa9eeb9b2fdb7f9e167e16105b22`

The upstream Vera subject was qualified by the dedicated automatic
`Vera Portfolio Public-Safe Successor V2` workflow with 17 successor regressions
passing.

## Cardinality and privacy

The bound cut records 67 total repositories, 49 public and 18 private.

Those values are properties of that immutable cut. They are not hard-coded VCP
policy constants.

VCP's public V2 binding names the public source rows only.

Private inventory is count-only:

```text
COUNT_ONLY_PUBLIC_V1
exact_membership_publicly_committed = false
membership_names_present = false
```

VCP public source therefore cannot decide that an opaque private repository is
safe to auto-bind. Private runtime use requires a separately authorized private
exact binding.

## NO_AUTO_BIND enforcement

The V2 validator does not contain an `EXPECTED_NO_AUTO_BIND` name set.

It reads each exact public row's
`runtime_source_disposition` from the bound Vera V2 subject.

For `NO_AUTO_BIND` rows, VCP rejects capability-registry load modes that would
silently promote availability into automatic/live hydration:

- `CONTROL_LOAD_EXACT_OWNER`
- `LIVE_COORDINATION_READ`
- `TASK_RELEVANT_LIVE_READ`

The effective helper always returns `auto_bind_allowed=false`, including for
`BOUND_CONDITIONAL`. Conditional binding still requires task relevance,
fresh currentness, and any separate authority/effect gates.

`PREDECESSOR_EVIDENCE_ONLY` can never become current control merely because it
is accessible.

## Open-world and freshness behavior

A repository absent from the immutable public cut is:

`UNRESOLVED / NO_AUTO_BIND`

until a newer exact cut or separately authorized binding is supplied.

If a public source's mutable head differs from the cut observation, VCP reports:

`STALE_CURRENTNESS`

That is not treated as corruption of the immutable historical cut. The cut
remains valid provenance; the currentness claim must be refreshed.

This replaces PR #131's permanent 59/17 equality assertions.

## Predecessor disposition

VCP PR #131 exact head
`a2ce761d3de0adf0cba5c64f53103f97ef48569e` remains useful evidence for the
enforcement idea and hostile-review history.

It is superseded as the runtime-source subject because it binds the older Vera
V1 registry and frozen cardinality/membership partition.

This branch does not close, modify, merge, or force-push PR #131.

## Authority ceiling

This is source-policy enforcement only.

It does not install Project instructions, activate repositories, expose private
membership, merge, deploy, mutate providers, alter credentials/permissions, or
grant protected-effect authority.
