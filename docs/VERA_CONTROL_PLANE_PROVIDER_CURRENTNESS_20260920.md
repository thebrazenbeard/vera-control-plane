# Vera Control Plane Provider Binding — 2026-09-20

Status: `OBSERVED_PROVIDER_BINDING / READBACK_ONLY / NO_PROVIDER_EFFECT`

This record gives the Vera Control Plane repository a durable locator for the live control-plane Supabase project without treating provider presence as runtime/control authority.

The observed project is `Vera Control Plane` / `fawkirqroyniueeqspif`, healthy in `us-east-2` on PostgreSQL 17.6.1.166. The provider currently exposes the narrow `vera_cp_anchor` state plus reserved `vera_cp_api` and `vera_cp_internal` schemas.

Fresh readback observed the SD1 causal witness at generation 0 with record_count 0 and zero mutation receipts. That establishes the installed genesis anchor only. It does not establish a bound production controller, causal collection, behavior/causal qualification, current route, phenomenology, or authority for a new provider mutation.

This source record deliberately does not modify R10/R10+SD1 control artifacts, Supabase, Project Settings, credentials, permissions, or runtime state.

Companion Vera-side currentness source: `thebrazenbeard/vera#136`.
