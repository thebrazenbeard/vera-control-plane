# Supabase Control Plane Deployment Binding Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the controlled GitHub deployment surface for Supabase project `fawkirqroyniueeqspif` and prepare the project/repository binding without enabling production auto-deploy or moving Vera runtime-state semantics into the control-plane repo.

**Architecture:** `thebrazenbeard/vera` remains semantic/technical source. `thebrazenbeard/vera-control-plane` holds exact provider binding and release-bound deployment artifacts. Supabase is the durable provider, never self-authorizing control authority.

**Tech Stack:** GitHub, Supabase/PostgreSQL 17, Supabase migration format.

**Spec:** `docs/superpowers/specs/2026-09-12-supabase-control-plane-deployment-binding-design.md`

## Global Constraints

- Target Supabase project ref is exactly `fawkirqroyniueeqspif`.
- Target GitHub repository is exactly `thebrazenbeard/vera-control-plane`.
- `PROVIDER != CONTROL AUTHORITY` is an invariant.
- Do not merge a PR or enable production deployment without Patrick's separate exact authorization.
- Do not add Vera runtime-state semantic/domain tables in this task.
- Do not expose secrets, database passwords, service-role keys, or private payloads.
- Baseline migrations must match the versions already installed on the live project.

---

### Task 1: Materialize the live provider-hardening baseline

**Files:**
- Create: `supabase/README.md`
- Create: `supabase/migrations/20260912170153_harden_public_default_privileges.sql`
- Create: `supabase/migrations/20260912170345_enforce_rls_on_exposed_schemas.sql`
- Create: `supabase/migrations/20260912170408_reserve_locked_api_schema.sql`

**Interfaces:**
- Consumes: live `supabase_migrations.schema_migrations` from project `fawkirqroyniueeqspif`.
- Produces: a deployable migration history whose versions exactly match live production history.

- [ ] Read the three live migration statements from `supabase_migrations.schema_migrations`.
- [ ] Create the three version-matched SQL files with those exact statements.
- [ ] Add `supabase/README.md` documenting ownership, provider identity, non-authority invariant, and promotion rules.
- [ ] Read the created files back and compare migration names/versions with live provider history.

### Task 2: Add the exact provider binding manifest

**Files:**
- Create: `governance/VERA_SUPABASE_CONTROL_PLANE_PROVIDER_BINDING_V1.json`

**Interfaces:**
- Consumes: provider project readback, `vera/main` source SHA, `vera-control-plane/main` predecessor SHA, baseline migration versions.
- Produces: machine-readable deployment/provider binding metadata.

- [ ] Record provider `supabase`, project ref `fawkirqroyniueeqspif`, region `us-east-2`, repository `thebrazenbeard/vera-control-plane`, working directory `.`, and production deployment state `DISABLED_PENDING_REVIEW`.
- [ ] Record upstream semantic source repository `thebrazenbeard/vera` at observed SHA `b7b8dcd1440a3b7147bec2cc35972f083e20f44a` as evidence, not a permanent mutable-current pin.
- [ ] Record the three baseline migration versions and `PROVIDER_NOT_CONTROL_AUTHORITY` invariant.
- [ ] Read back and validate JSON structure.

### Task 3: Open the deployment-binding review PR

**Files:**
- Review all Task 1-2 files plus the spec and plan.

**Interfaces:**
- Consumes: branch `work/supabase-control-plane-binding-20260912`.
- Produces: Draft PR to `main`; no merge.

- [ ] Verify branch ancestry remains based on `main@b4d9aaa8560de12252dd29996379b0af8e0ca0d1` with no target-path collision.
- [ ] Compare branch to main and inspect all changed paths.
- [ ] Open a Draft PR documenting that the live Supabase project is already created/hardened and the PR only establishes the controlled deployment source/binding.
- [ ] Verify PR head, base, draft state, and changed paths.

### Task 4: Connect Supabase GitHub integration without production deployment

**External configuration:** Supabase project `fawkirqroyniueeqspif`.

**Interfaces:**
- Consumes: reviewed repository deployment root and provider binding.
- Produces: GitHub integration source binding only; production auto-deploy remains off.

- [ ] Connect repository exactly `thebrazenbeard/vera-control-plane`.
- [ ] Set working directory to `.` so Supabase reads root `supabase/`.
- [ ] Keep automatic branching off unless separately authorized/cost-confirmed.
- [ ] Keep Deploy to production off.
- [ ] Read back integration settings. If the available API/tool surface cannot perform or read this dashboard-only integration, stop at `WAITING_USER_UI_ACTION` and provide only the exact required UI settings.

### Task 5: Post-bind verification

**Interfaces:**
- Consumes: Supabase integration readback and live provider database.
- Produces: verified binding status without activation/qualification overclaim.

- [ ] Confirm project remains `ACTIVE_HEALTHY`.
- [ ] Confirm live migration history still contains exactly the intended baseline migrations for this new project.
- [ ] Confirm no application tables or Edge Functions were created by the binding action.
- [ ] Run security advisor and record findings.
- [ ] Report exact status dimensions separately: source prepared, repository binding connected/unavailable, production deploy disabled, provider healthy, runtime activation not implied, behavioral qualification not implied.
