# External Repository Intake V2 — Finite-Domain Governance

Status: **SOURCE RESEARCH INTAKE ONLY / NOT DEPENDENCY / NOT CONTROL / NOT INSTALLED**

This is the bounded current-main successor to the external-intake surface represented by VCP PR #89.

PR #89 correctly blocked several literal promotion phrases, but its authority boundary still depended on natural-language blacklists. Hostile review reproduced equivalent promotions by changing wording and by using the structured lifecycle field.

V2 removes prose from normative action semantics.

Normative repository fields are finite-domain values:
- lifecycle;
- disposition;
- destination;
- restriction classes;
- pattern IDs;
- evidence mode.

Follow-ups are structured objects containing only:
- a finite `action_kind`;
- a finite research/history destination;
- finite pattern IDs.

The validator freezes the domain definitions themselves. Adding a new lifecycle, disposition, destination, restriction, pattern ID, action kind, evidence mode, repository identity, or source head is therefore a new source subject rather than an unreviewed wording change.

Human-readable explanations remain documentation. They are not parsed to infer admission, authority, installation, routing, memory, provider state, or effects.

The exact forbidden-effect set remains:
`DEPENDENCY_ADMISSION | PROJECT_INSTALL | RUNTIME_ROUTE | MEMORY_ADMISSION | CONTROL_OWNERSHIP | PROVIDER_MUTATION | NETWORK_DEPLOYMENT | POLITICAL_POSITION_INGESTION | LICENSE_COMPATIBILITY_APPROVAL | MERGE_AUTHORITY`.

Additional fail-closed rules include:
- unresolved license requires `NO_CODE_REUSE`;
- archived/stale evidence remains historical and carries `PRESERVE_HISTORICAL_ONLY`;
- content-corpus evidence stays `NONE_BY_DEFAULT` and carries `CONTENT_POSITION_NONADOPTION`;
- VeraMesh destinations require explicit owner-subsystem review;
- follow-up action/destination combinations are finite and cross-checked;
- immutable evidence paths reject traversal and malformed blobs;
- repository identities and exact observed heads are frozen to this snapshot.

This source does not admit any external repository as a Vera dependency, control source, Project source, memory, current route, runtime dependency, political position, license-approved code source, or effect authority.

No merge, Project install/settings/source mutation, provider mutation, credential/permission change, runtime activation, memory admission, network deployment, or paid effect is authorized by this source.
