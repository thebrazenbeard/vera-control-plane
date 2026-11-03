# VCP Supabase provider composition

`supabase/migrations/` is the executable **historical reconstruction
baseline** for the stable Vera Control Plane Supabase project identity.
The source-only validator checks the six local SQL files against the frozen
provider custody snapshot dated 2026-09-22, not against a current provider
connection. A PASS for the historical byte checks does **not** mean the full
live migration ledger or deployed SQL bodies were checked.

The read-only provider observation on 2026-11-03 listed those six VCP
migration versions plus two later Masamune-named migrations in the **same
stable project**, now displayed under a different project name. A display
name is not a provider identity. This observation establishes version/name
presence only; it does not independently establish current SQL-body bytes,
cross-owner migration custody, service behavior, or deployment qualification.
It must be refreshed before any protected change.

`tools/validate_vcp_supabase_provider_composition.py` consequently returns
`HISTORICAL_BASELINE_ONLY`, with `live_full_ledger_parity =
UNVERIFIED_NOT_QUERIED`. Any operator requiring live parity must obtain
separate authenticated exact-project provider readback and byte/provenance
evidence; the static validator always refuses live promotion.

The JSON report is explicitly `VCP_PROVIDER_COMPOSITION_REPORT_V2` and sets
`legacy_v1_pass_compatible=false`. The old generic `status=PASS` and ambiguous
`provider_migrations`, `pending_migrations`, and `last_provider_version` keys
are deliberately not emitted: recreating them as a v1 compatibility facade
would let an unmodified caller mistake a frozen 2026-09-22 source snapshot for
live parity. In-repository source inspection found no consumer beyond the
validator's own tests, but external consumers are not proven absent. A
downstream caller must explicitly adopt the v2 contract or hold; this source
change is not a verified portfolio-wide migration.

The three pre-repair alternate-timestamp sources are preserved under
`supabase/drafts/pre-provider-composition-20260922/` for audit only.

Future migrations must advance the bound provider cut and be declared before
they enter the executable directory. Git source, provider application, and
provider readback remain separate evidence/effect domains.
