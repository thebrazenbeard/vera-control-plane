-- Defense-in-depth hardening for the internal RLS event-trigger function.
-- Source only until Patrick explicitly authorizes application to
-- Supabase project fawkirqroyniueeqspif.
--
-- Live readback on 2026-09-21 showed:
-- - PUBLIC/anon/authenticated/service_role/broker inherited EXECUTE;
-- - none of those roles had USAGE on schema vera_cp_internal;
-- - therefore the function was not ordinarily reachable, but EXECUTE was
--   unnecessarily broad and should be explicitly revoked.

REVOKE EXECUTE ON FUNCTION vera_cp_internal.enable_rls_for_new_api_tables()
  FROM PUBLIC, anon, authenticated, service_role, vera_sd1_causal_anchor_broker;
