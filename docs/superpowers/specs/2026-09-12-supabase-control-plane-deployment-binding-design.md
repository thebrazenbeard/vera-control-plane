# Supabase Control Plane Deployment Binding Design

## Purpose

Bind Supabase project `fawkirqroyniueeqspif` (`Vera Control Plane`, `us-east-2`) to `thebrazenbeard/vera-control-plane` as the deployment/promotion surface without moving Vera runtime-state semantics out of `thebrazenbeard/vera` and without allowing provider persistence to self-authorize control/currentness.

## Ownership boundary

- `thebrazenbeard/vera` remains the semantic/technical source for provider-neutral state contracts, runtime-state schemas, provider adapters, Cohesion admission/composition logic, and conformance tests.
- `thebrazenbeard/vera-control-plane` owns exact provider binding, promotion/deployment manifests, installed migration-set receipts, route/install/readback/qualification evidence, and genuinely control-plane-only provider migrations.
- Supabase is a durable provider. It is not itself control authority. A row, receipt, or migration present in Supabase does not self-prove currentness, authority, installation, route, qualification, or inference admission.

## GitHub deployment surface

The repository receives a root `supabase/` deployment surface because the Supabase GitHub integration expects a working directory containing `supabase/`.

The initial deployment surface contains only the three provider-hardening migrations already installed in `fawkirqroyniueeqspif`:

1. `20260912170153_harden_public_default_privileges.sql`
2. `20260912170345_enforce_rls_on_exposed_schemas.sql`
3. `20260912170408_reserve_locked_api_schema.sql`

No Vera runtime-state domain tables are introduced by this change.

## Promotion contract

Future Vera runtime/domain migrations are authored and reviewed in `thebrazenbeard/vera`. They become deployable only after an exact source generation is promoted into this repository with source repository, commit SHA, migration path/blob or digest, target provider generation, and review/readback metadata. A copied migration in `vera-control-plane` is a release-bound deployment artifact, not an independent semantic source.

## Provider baseline

Project binding:

- provider: Supabase
- project name: `Vera Control Plane`
- project ref: `fawkirqroyniueeqspif`
- region: `us-east-2`
- PostgreSQL: 17
- organization: `Vera`
- cost basis at creation: `$0/month`

Current provider hardening keeps `public` inert for `anon`, `authenticated`, and `service_role`; reserves `vera_cp_internal` and `vera_cp_api`; and enables RLS automatically on newly created tables in `public` or `vera_cp_api`.

## Deployment safety

The GitHub integration may be connected to this repository, but automatic production deployment remains disabled until the deployment root is reviewed and the repository branch containing it is merged by Patrick. No merge is authorized by this design.

The production provider must not consume `thebrazenbeard/vera` directly. This prevents technical source from self-installing merely by landing on `vera/main`.

## Verification

Before enabling production deployment:

- GitHub source repo is exactly `thebrazenbeard/vera-control-plane`.
- Working directory is repository root (`.`), containing `supabase/`.
- The three baseline migration versions exactly match live `supabase_migrations.schema_migrations`.
- No unexpected application tables or Edge Functions exist.
- Security advisor is clean.
- Provider binding manifest matches project ref and repository source.
- Any future semantic migration promotion cross-binds exact `vera` source identity.

## Non-goals

This change does not migrate predecessor Vera data, create runtime-state domain schemas, attach secrets, enable a public Data API surface, authorize Auth signup, cut over current runtime state, retire `klmbpaigzeguvnpccqzz`, merge any PR, or qualify a runtime/provider route.
