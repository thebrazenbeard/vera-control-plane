# Vera Control Plane — Supabase deployment surface

This directory is the release-bound deployment surface for Supabase project `fawkirqroyniueeqspif` (`Vera Control Plane`, `us-east-2`).

## Critical boundary

**PROVIDER != CONTROL AUTHORITY.**

Supabase persists provider state and receipts. Persistence, co-location, a database row, a migration record, or a provider-stored receipt does not by itself establish semantic currentness, operational authority, installation, current route, behavioral qualification, or inference admission.

## Repository ownership

- `thebrazenbeard/vera` owns provider-neutral state semantics, Vera runtime/domain schema definitions, provider adapters, Cohesion admission/composition logic, and conformance tests.
- `thebrazenbeard/vera-control-plane` owns exact provider binding, promotion/deployment manifests, installed migration-set receipts, route/install/readback/qualification evidence, and genuinely control-plane-only provider migrations.

Future Vera runtime/domain migrations must be authored and reviewed in `thebrazenbeard/vera`, then promoted here as exact release artifacts with source identity/digest. A promoted copy here is deployable custody, not an independent semantic source of truth.

## Initial baseline

The initial migration files mirror the three provider-hardening migrations already installed on the live project:

- `20260912170153_harden_public_default_privileges.sql`
- `20260912170345_enforce_rls_on_exposed_schemas.sql`
- `20260912170408_reserve_locked_api_schema.sql`

They create no Vera runtime-state domain tables.

The runtime-plane substrate migration `20260912183000_initialize_runtime_planes.sql` is a byte-identical promoted copy from `thebrazenbeard/vera@50c155f9715183b48ddcb404a53bb16c148b323e`. It is `SOURCE_BOUND_NOT_APPLIED`: present for controlled deployment custody, not evidence of installation or current-route activation.

## Deployment policy

GitHub integration may bind this repository to the Supabase project, using repository root `.` as the working directory. `Deploy to production` remains disabled until Patrick separately authorizes activation after review. Supabase branching is not enabled by this baseline.

Do not commit database passwords, secret/service-role keys, private payloads, raw conversation archives, or connector credentials here.
