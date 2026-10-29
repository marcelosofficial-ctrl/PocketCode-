# PocketCode — owner decision register

**Status:** Research proposals only; not canonical, not implemented, NOT RUN. Recommendations require owner review.

## D-01 — Confirmed execution limit verdict

Canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (main blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`) defines FAIL as confirmed program/runtime failure and INCOMPLETE as no confirmed success or failure.

Earlier versions of the semantic and transition matrices leaned toward INCOMPLETE for enforced limits without distinguishing the terminal cause. The latest research pass now separates limit-caused termination, collection-only truncation with independently confirmed EXIT_ZERO, and display-only truncation. The exact verdict mapping for limit-caused termination remains OPEN under D-01 because the owner has not approved an interpretation of the canonical failure definition.

**Three cases must not be conflated:** (1) trusted evidence confirms the limit caused termination/failure: candidate FAIL if this qualifies as a confirmed program/runtime failure under canonical wording, with `LIMIT_EXCEEDED` disposition; exact verdict mapping remains OPEN for owner review. (2) A collector/retention cap truncates captured bytes while independent trusted process evidence confirms EXIT_ZERO: derive the verdict from terminal facts and the acceptance case's explicit collection requirements; PASS remains possible only if partial collection is accepted for that case and all other gates pass. (3) The report renderer alone truncates presentation: preserve the execution verdict and do not infer a runtime limit. If terminal outcome is unknown or contradictory, use INCOMPLETE. The limit event and cleanup state remain separate.

Tests: confirmed limit termination, collector truncation with exit zero, ambiguous limit evidence, display-only truncation. **OPEN; owner confirmation required.**

## D-02 — Provider failure without child exit evidence

Proposed default: user verdict INCOMPLETE; execution outcome UNKNOWN; disposition `PROVIDER_ERROR` only if the infrastructure cause is confirmed. Never invent an exit code. A separately confirmed nonzero child exit remains FAIL when cleanup is unknown. Test before-start failure, partial output then lost exit evidence, and nonzero exit with cleanup failure. **Proposed default.**

## D-03 — Is complete output mandatory for PASS?

Canonical PASS wording requires trusted completion and exit zero but does not explicitly make every output stream complete a universal gate. Proposed default: define required streams and accepted partial-capture behavior per acceptance case/runtime; optional diagnostics being unavailable or capped must not become an accidental universal PASS failure. A stream explicitly required by that case must satisfy its stated collection rule; if it does not, PASS is withheld while the raw terminal outcome is preserved. Keep COMPLETE, PARTIAL, UNAVAILABLE, EMPTY, RUNTIME_LIMIT, and DISPLAY_TRUNCATED distinct; artifact-specific release gates remain independent. **OPEN pending owner confirmation before gate/schema freeze.**

## D-04 — Event identity scope

**Proposed default for owner review:** assign each accepted canonical event a coordinator-owned unique `event_id`; retain any external/provider event ID separately with a documented source namespace. Deduplicate source replays using a scoped key such as `(source_namespace, tenant_ref, job_id, attempt_id, source_event_id)`. Bind and validate tenant/job/attempt/source (and policy revision where relevant) before reduction. A coordinator sequence is unique and monotonic within the attempt/event stream; provider timestamps do not establish ordering. A replay is identical only when its scoped source identity and all immutable observation fields match (event kind, sequence, canonical payload/schema version, binding and relevant policy revision). Only explicitly designated transport-delivery metadata may differ. Changed identity, sequence, kind or payload is a conflict, not an idempotent retry. Keep accepted payloads immutable; distinct events sharing a coordinator sequence must appear in conflict diagnostics. This is a proposed contract, not a frozen schema. Tests: exact replay; changed attempt/job/tenant/source/policy; changed payload; same sequence under different event IDs; nested-payload mutation. **OPEN.**

## D-05..D-08 — Other blocking choices

- **D-05 Policy binding:** require an enforceable immutable per-attempt policy or atomic/conditional dispatch revision barrier; read-then-act is insufficient. PBR-01..07 test revision race/binding behavior; PF-01..05 separately test fingerprint-schema determinism/idempotency and linkage to the actually applied policy. Both checklists are in `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md`. A request fingerprint is not proof of applied-policy binding. Provider/runtime enforcement remains unselected and BLOCKED/NOT RUN until verified at the actual boundary.
- **D-06 Idempotency and ambiguous dispatch:** atomic durable tenant-scoped reservation + versioned semantic fingerprint; same key/same fingerprint resolves to the original job/attempt; same key/changed fingerprint conflicts before dispatch. Persist dispatch intent before external start; after acknowledgement loss, restart or uncertain dispatch, reconcile the same original identity. UNKNOWN/unavailable lookup means no automatic redispatch. A lease timeout is not proof the first start did not happen. Full DR-01..DR-12 crash/concurrency/retention checklist: `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md`. Exactly-once provider execution remains unclaimable without provider idempotent-start semantics or authoritative lookup. **Proposed default; owner review required.**
- **D-07 Artifact release:** treat download as a separate current authorization decision, not a permanent consequence of execution PASS. Revalidate tenant/job/attempt, trusted manifest, quarantine, safe object identity/path/type/size and the exact immutable bytes immediately before returning them; deny stale/mismatched/unknown states without cross-tenant disclosure. Full AR-01..AR-14 checklist: `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md`. **Proposed default; store/API boundary unselected and NOT RUN.**
- **D-08 Report history:** immutable issued versions; atomic monotonic per-job version allocation; idempotent append identity; immutable evidence references; crash-safe publication; concurrent writers cannot lose events; late/contradictory evidence creates a new version rather than rewriting history. Cross-store report/artifact publication must be atomic or reconciled without exposing inconsistent PASS/download states. Full RH-01..RH-14 checklist: `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md`. In-memory `ReportHistory` is not durable proof. **Proposed default; store and transaction guarantees unselected and NOT RUN.**

These require tests at the actual chosen boundary; fake tests alone cannot establish provider, storage, or device guarantees.

## Order and stop rule

Resolve D-01..D-04 before freezing verdict/event tests; D-05 before execution-boundary safety claims; D-06/D-08 before durable recovery/history claims; D-07 before artifact-release claims. Keep all proposals unapproved until the owner confirms them. Do not change canonical acceptance or implementation merely to make tests pass.

**Evidence:** research note only; no tests or implementation changes. No provider/runtime, account, billing, workload, merge, or deployment action. Canonical acceptance and PR #2/#3 remain unchanged.


## Cross-decision consistency and implementation sequencing — 2026-10-29
See [CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md) for the read-only D-06/D-07/D-08 contradiction audit, residual ambiguities A-G, and proposed G0-G7 evidence gates. No direct logical contradiction was found; provider/store/HTTP/device guarantees remain SPECIFIED ONLY / NOT RUN. D-01..D-04 remain owner-open; D-05 remains BLOCKED pending actual boundary proof. The audit does not approve a provider, store, or implementation.


## Provider-neutral boundary contract sketch — 2026-10-29
See [PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md). It defines proposed operations and typed outcomes for atomic reservation, dispatch-intent/reconciliation, trusted evidence acceptance, append-only report publication, artifact publication/release, retention, and hard stops. It is a review sketch only: not a frozen schema, implementation, provider/store selection, or proof of any guarantee. All integration evidence remains NOT RUN.


## Implementation-readiness backlog — 2026-10-29

See [IMPLEMENTATION_READINESS_BACKLOG_20261029.md](IMPLEMENTATION_READINESS_BACKLOG_20261029.md) for a dependency-ordered plan from independent review and D-01..D-04 owner decisions through pure tests, policy barrier, durable recovery/history, artifact release, and device acceptance. It is a planning aid only and does not close or approve any decision.


## Owner decision packet — 2026-10-29

See [OWNER_DECISION_PACKET_D01_D04_20261029.md](OWNER_DECISION_PACKET_D01_D04_20261029.md) for a compact review of D-01..D-04, proposed defaults, counterexample tests, canonical traceability and a copy-ready response template. It is decision support only: no owner choice is implied or approved.


## Consolidated owner decision and patch gate — 2026-10-29

See [CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md](CONSOLIDATED_OWNER_DECISION_AND_PATCH_GATE_20261029.md) for one review surface covering D-01..D-04 and G-01/G-02/G-03/G-07/G-08. Existing decisions remain OPEN/proposed until the owner explicitly responds. The patch grouping and suggested behaviors are recommendations, not authorizations.
