# Vera Agent Protocol Boundaries V1 — advisory source, not activation

Status: `ADVISORY_SOURCE_CANDIDATE_NON_ACTIVATING`. Scope: exact, inspectable communication decisions. No provider, native Project, host, service, permission, identity, or memory effect.

Sources checked: Google Developer’s Guide to AI Agent Protocols (March 18, 2026); MCP version 2025-11-25 specification; A2A current published specification (2026). Protocol versions must be negotiated with actual peers and must not be inferred from the guide. References: https://developers.googleblog.com/developers-guide-to-ai-agent-protocols/ ; https://modelcontextprotocol.io/specification/2025-11-25 ; https://a2a-protocol.org/latest/specification/

## Decisions

- Existing ChatGPT/host to tool/plugin integrations: **MCP** when actually exposed and authorized. Per-tool effect authority remains separately verified. Direct functions in one process do not need an MCP server.
- Current Vera, Engineer A/B and BT2 assignments: **shared Bus coordination** with owner lane, exact repo/ref/head, bounded allowed/prohibited effects, effect receipt and reply. The Bus is an evidence/coordination substrate, not a delegation credential or secret channel. Neither its issue text nor its presence gives a worker authority.
- Independently deployed external agent runtimes: **A2A only if justified** by actual discoverable agent service, interoperable task/artifact lifecycle, and authenticated scoped delegation. Existing chat identities do not prove such services. A2A task acceptance does not authorize protected operations. No production A2A deployment is claimed.
- Host machine controller: **existing authenticated API**, ideally direct local binding or HTTPS for remote requests. Check actual transport and host ownership before calling it current; never replace it with A2A merely because it makes an agent call.
- Screen observation: **VNC/approved screen channel**; an image or handshake cannot confer keyboard/mouse permission. Input needs separately attested, revocable human authorization and exact host/window/epoch binding.
- Native UI: presentation, consent capture and results; server-side service owns durable task/effect state. Client-side display state is not an effect receipt. Browser content and UI labels are untrusted inputs.

## Contract and failures

Machine-checkable companion: `protocol/VERA_AGENT_PROTOCOL_BOUNDARIES_V1.json`, validated with `python tools/validate_agent_protocol_boundaries_v1.py` and `python -m unittest discover -s tests -p 'test_agent_protocol_boundaries_v1.py'`.

This source validator checks that declared paths are not promoted into live authority and critical failure-policy guardrails do not disappear. It does **not** intercept actual MCP/A2A/HTTPS/VNC requests, verify server configuration, grant consent, prove credential scope, or show runtime use. It cannot replace host-side policy enforcement.

Before every mutation: verify authenticated principal, target identity, exact effect scope, current head/version and user approval where required. Append source/evidence classes and receipt; keep private bytes out of public Bus. On ambiguous mutation failures, query authoritative effect ledger and reconcile prior effects before retry; do not mint a new retry key blindly. On screen disconnection, revoke input until fresh target, lease, and identity verification. Unavailable user-selected route fails closed instead of silently choosing another.

## Migration without protocol proliferation

1. Reconcile active owners and the failing editor-startup security PRs first; never activate concealed `folderOpen` loaders.
2. Keep existing MCP tool servers, Bus assignments, and host APIs. Audit their declared vs actual capability/permission behavior.
3. Use this document as a reviewable **candidate contract**; bind to exact live owner only through the existing VCP governance process, with independent review and explicit promotion authority.
4. Add integration tests at actual effect boundaries before claiming runtime enforcement: wrong host, revoked input, stale head, double submission, timeout after an applied effect, wrong principal, A2A task that cannot authorize a mutation.
5. Pilot A2A with one genuinely independent deployed worker only if the Bus + direct API path demonstrably fails a real interoperability need. Do not migrate current chat workers just for branding.

Primary tradeoff: less glue and cleaner ownership with one additional contract to maintain; the cost is refusing to market a source policy as a deployed enforcement mechanism.
