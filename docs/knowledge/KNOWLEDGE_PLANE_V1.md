# Vera knowledge plane — evidence-gated claim cards (candidate V1)

**Status: DRAFT / SOURCE-ONLY / NOT INSTALLED / NOT A LIVE KNOWLEDGE BASE.** This is public-safe architectural source, not a new private memory writer, deployed search service, or proof of authority.

## Problem and decision

The ecosystem already contains Git source, PR reviews, tests, Blotter events, coordination threads, memory records, model artifacts and host receipts. More undifferentiated documents will worsen findability. The missing piece is a consistent, **bounded and evidence-sensitive way to discover a claim and ask whether it is the right claim, about the right entity, with proof appropriate to the requested question**.

Decision: do not create a competing database. Define a small interoperable claim-card contract with a source-only validator first; test its false-promotion behavior. Index references to governed source systems, never copy private primary content into a public search index.

## Reuse and ownership

| Existing source | Knowledge role | Limit |
| --- | --- | --- |
| GitHub repos, branches and PRs | Versioned source, code and reviews | A passing source test does not prove runtime effect |
| Shared Blotter and Bus #423 | Observations, coordination, review leads | A claimed actor or event label is not authenticated authority |
| Roots | Candidate discovery, temporal and historical provenance | A retrieval hit does not prove origin |
| Deep Memory Storage | Historical ledger union with correction overlays | Historical canonicity is not current identity, consent or admission; public Git cannot receive private transcripts |
| STM and separately governed memory | Bounded session retention and reviewed mutable memory | Historical records cannot self-admit or override current instructions |
| Vera Mono and hosts | Runtime capabilities and installed behavior | Must be checked against actual machine/provider state and independent receipts |
| Vera Control Plane | Reviewed control-plane source policies and verification boundaries | This proposal does not change any production permission |

The owner of an artifact must be resolved using logical ID, schema role, and verified binding; filenames, suffixes and a repository's stated purpose alone are not enough. Active security and protocol PRs must retain their own independent writer lanes.

## Information architecture

Use three complementary structures, not a single sprawling taxonomy.

- **Taxonomy:** repositories, services, models, agents, tests, decisions, incidents, recovery records and historical relationships. Hierarchical ownership is *one facet*, not a source of authority.
- **Facets:** claim surface, epistemic class, evidence time, freshness, owner binding, visibility, source revision, lifecycle, domain and affected dependency. Missing metadata remains UNKNOWN.
- **Graph:** REFERENCES, DEPENDS_ON, OBSERVED_IN, TESTED_BY, SUPERSEDES, CONTRADICTS and OWNED_BY_CANDIDATE. A graph edge is a query lead, not permission, chronology proof or semantic identity.

A knowledge card has one atomic claim and these V1 fields: schema, record_id, subject_id, title, claim, domains, owner_id, owner_binding_ref, visibility, publication_target, lifecycle, claim_surface, currentness, valid_until, evidence, supersedes and limitations.

Each evidence element contains a class, source_ref, revision and observed_at (UTC). Source classes include DOC, SOURCE_INSPECTION, TEST, REAL_PROBE, PROVIDER_READBACK and INFERENCE. The source-only validator is at tools/knowledge_record_gate.py; tests use only synthetic data.

**Critical distinction:** source CURRENT claims require a fresh SOURCE_INSPECTION referencing an exact 40-hex Git SHA. Runtime CURRENT claims require a fresh REAL_PROBE. Provider CURRENT claims require a fresh PROVIDER_READBACK. Historical claims cannot be CURRENT. The demonstrator's currentness lease is capped at 24 hours after matching evidence, not a universal policy. A document, synthetic test receipt or model-generated statement cannot grant runtime authority.

The validator checks internal shape and declared evidence class only. It neither authenticates a caller, fetches the referenced source, proves a probe happened, reviews private data, nor grants effects. A validator PASS must not be described as an authenticated source verification.

## Retrieval and search

Proposed read path:

1. Authenticate user/workload and determine exact source/subject access scope.
2. Retrieve from authorized keyword and metadata indexes; optionally broaden candidates with semantic/vector retrieval.
3. Resolve entity names against actual logical IDs and schema roles; preserve aliases and competing candidates rather than collapsing them prematurely.
4. Expand relevant links for dependencies, changes, contradictions, supersessions and attempted owners.
5. Independently re-read time-sensitive sources and verify live effects with an appropriate host/provider tool.
6. Present answer with claim provenance, currentness, uncertain or missing evidence, and permission-scoped citations.

No vector score can upgrade truth, chronological origin, access rights or runtime verification. ACLs must filter before ranking, autocomplete, snippets and answer generation. When source availability is incomplete, provide partial results and source gaps rather than fabricate coverage.

## Lifecycle, privacy and usability

Lifecycle is DRAFT → REVIEWED → PUBLISHED → SUPERSEDED/RETIRED. A publication label does not itself establish privacy clearance; a PUBLIC_REPOSITORY target needs a separate public-safe review. Historical corrections are append-only lineage, with an explicit supersession relation, not silent destructive overwrite. Retention must distinguish session expiration, evidence retention, private records and legal obligations.

User experience should support: "What is blocking this service?", "Who actually owns this?", "What changed since the last pass?", "Which historical meaning did this term have?", "Which source am I authorized to inspect?". Show filters for source type, date, owner, confidence and freshness. When no qualified record exists, show that it is unverified instead of inventing it.

Tacit knowledge is captured only through permitted interviews, reviewed Q&A or authorized recordings. An assistant must not infer consent from a meeting transcript or a developer's informal report. Local/on-prem custody should be preferred for protected evidence; cloud services are scoped connectors, not unconditional mirrors. Maintain accessibility with keyboard navigation, meaningful labels, visual hierarchy and WCAG-aligned design.

## Rollout without another uncontrolled subsystem

**Phase 1 — this candidate:** run structural and hostile source-only tests with synthetic claim cards. Publish only as a draft, independently review privacy and failure boundaries. No ingestion or runtime activation.

**Phase 2 — read-only owner inventory:** bind three representative subjects (one Git source, one real service, one historical correction) to current owners, exact sources and explicit currentness gaps. Do not import private payloads into the public repository.

**Phase 3 — retrieval pilot:** measure precision@k and recall@k, null-result rate, stale-answer rejection, correct source citations, contradiction preservation, latency and editorial review time. Private result leakage target is ZERO, including autocomplete and embedding influence. Test wrong-owner references and poisoned summaries.

**Phase 4 — optional authenticated integration:** require exact current source bindings, proof-specific verification and explicit scoped authorization for any memory writer, provider update or production search service. Do not add a second Bus, memory database or permission system by default.

**Phase 5 — governed content health:** flag stale records for review; verify archival retrieval and recovery; measure coverage, time-to-find, resolved user questions and observed expert burden. Review incentives should reward corrections and proven reuse, not raw document counts.

## Falsifiers and limits

> A synthetic REAL_PROBE label and plausible receipt string can pass the structural gate. That does **not** mean a probe occurred. Any design claiming otherwise is invalid.

> Two similarly named repositories may have different runtime consumers and authority lanes. Similarity is not proof of redundancy.

> A private document behind a valid ACL can still leak through a public vector index or query completion. Failure of access-first filtering blocks adoption.

> An older but primary record may disprove the origin described by a newer summary. Preserve chronology and contradiction.

Run local synthetic tests with:

    python -m unittest discover -s tests -p test_knowledge_record_gate.py -v

Run the source-only CLI against a single explicit UTF-8 JSON card:

    python tools/knowledge_record_gate.py card.json --as-of 2026-11-20T20:00:00Z

A successful exit asserts **only that the presented record passes this validator's local contract**. It is not a knowledge-service installation or a certified statement about the world.
