# PocketCode — owner decision register

**Status:** Research proposals only; not canonical, not implemented, NOT RUN. Recommendations require owner review.

## D-01 — Confirmed execution limit verdict

**Canonical trace:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (LOOP-03–05) and CASE-04/CASE-07. The current canonical CASE-04 wording explicitly maps a trusted enforced timeout to `INCOMPLETE / timed_out`; LOOP-05 says timeout/cancellation/rejection/uncertain infrastructure outcome cannot be shown as success. These existing acceptance meanings are not changed by this research note.

**Working default for this branch:** retain `INCOMPLETE` for a confirmed deadline/timeout termination with terminal status `timed_out`, and record the limit cause separately (candidate disposition `LIMIT_EXCEEDED`). A confirmed non-zero program exit or confirmed program/runtime failure may be `FAIL` under LOOP-04. Do not reclassify a timeout as FAIL merely because a trusted limit caused termination; that would conflict with CASE-04 unless the owner explicitly revises canonical acceptance first. If cause or terminal state is unknown/contradictory, use INCOMPLETE.

Keep three cases distinct:
1. Trusted execution control confirms the run was terminated by a deadline/resource limit: follow CASE-04/LOOP-05 (INCOMPLETE / timed_out) under the current contract; preserve the cause/disposition separately.
2. A collector/retention cap truncates captured bytes while independent trusted process evidence confirms exit zero: verdict depends on the case-specific evidence requirements and whether partial capture is explicitly accepted; this is not a runtime timeout.
3. The report renderer truncates presentation only: preserve the execution verdict and label the presentation truncation; do not infer runtime termination.

**Status:** Owner decision remains OPEN for any future canonical change. Until then, use the canonical CASE-04 working default above; do not freeze conflicting expectations or silently change acceptance text. Proposed checks: trusted timeout, actual non-zero exit, collector-only truncation with exit zero, display-only truncation, ambiguous terminal evidence.

## D-02 — Provider failure without child exit evidence

**Working default:** user-facing verdict INCOMPLETE; execution outcome UNKNOWN; candidate disposition `PROVIDER_ERROR` only when the infrastructure cause itself is confirmed. Never invent an exit code or infer program failure from provider loss alone. If a non-zero child exit is independently and authoritatively confirmed, preserve FAIL even when cleanup is unknown; record cleanup separately.

**Canonical trace:** LOOP-05 and CASE-06 require infrastructure uncertainty without trustworthy program result to remain INCOMPLETE. CASE-11 additionally prohibits inferring completion from a browser disconnect; CASE-13 requires ambiguous retry state to remain unknown rather than creating a duplicate execution.

**Status:** Working default selected for research consistency; owner decision remains OPEN before schema/test expectations are frozen. Proposed checks: provider failure before start, partial output then loss of terminal evidence, independently confirmed non-zero exit plus cleanup uncertainty.

## D-03 — Is complete output mandatory for PASS?

**Working default:** no universal complete-output or artifact-presence gate. PASS requires trusted terminal success and exit code zero plus any evidence explicitly required by that acceptance case. Missing/capped optional diagnostics do not automatically invalidate execution PASS. If a stream is explicitly required by a case and its collection rule is not met, withhold that case's PASS while preserving the raw terminal outcome and stating the evidence gap.

Keep these states distinct: COMPLETE, PARTIAL, UNAVAILABLE, EMPTY, RUNTIME_LIMIT, and DISPLAY_TRUNCATED. An empty stream is not an unavailable stream. A collector cap is not the same as a runtime limit. A task that does not produce files can still PASS; an empty output-file list is not a universal failure. Conversely, execution PASS is not artifact-release authorization: when an artifact exists and a release/download is requested, apply the separate current release decision and its D-07 checks. A historical PASS must not bypass quarantine, authorization, identity, integrity, or release-time checks.

**Canonical trace:** LOOP-03/04/05 define verdict semantics; LOOP-07 asks for bounded diagnostics; LOOP-10 covers generated files when present; CASE-01/02/03/06/07/09/10/12/14 cover success, failures, limits, output, and reports. CASE-09 explicitly permits process execution PASS while retaining a program-reported failed check; process success does not prove the broader task is correct. CASE-07 requires a configured output limit to be enforced and truncation/rejection disclosed, not that every task produce output files.

**Status:** Working default selected for research consistency; D-03 remains OPEN before schema/gate freeze. Define required streams/artifacts per case/runtime; do not impose a universal artifact gate on artifact-free tasks.

## D-04 — Event identity scope

**Working default:** every accepted canonical event should eventually have a coordinator-owned unique event ID; retain any external/provider event ID separately with a source namespace. Candidate replay key: `(source_namespace, tenant_ref, job_id, attempt_id, source_event_id)`. Bind tenant/job/attempt/source (and relevant policy revision) before reduction. Coordinator ordering, not provider timestamps alone, should establish event order. A replay is identical only if scoped identity and immutable observation fields match; changed payload/identity/sequence is a conflict. These are proposed semantics, not a frozen schema.

**Canonical trace:** LOOP-07 requires a stable run identity in useful diagnostics; LOOP-09 requires separate run identities across repeatable correction cycles; CASE-13 addresses ambiguous retry/idempotency; CASE-16 requires out-of-order concurrent completions to remain tied to the correct run. These cases support identity preservation and correlation but do not define a complete canonical event envelope, sequence algorithm, or deduplication key.

**Status:** D-04 remains OPEN. Preserve the proposed default for crosswalk/research only. Do not freeze event schema or exact replay assertions until the event source, authority boundary, immutable fields, and conflict semantics are reviewed. Proposed checks: exact replay; changed tenant/job/attempt/source/policy; changed payload; same sequence with different event IDs; nested-payload mutation.

## Canonical alignment note — do not confuse the two D-01..D-04 registers

This section refers to execution/lifecycle decisions D-01..D-04 in this owner decision register. The separate AI Workflow Director builder register `AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md` also has D-01..D-04 for input normalization, serialization, character counting, and oversized context; those IDs are a different namespace and are not changed here.

The canonical LOOP/CASE criteria remain authoritative. This reconciliation chooses conservative **working defaults** for research consistency but does not close owner decisions, freeze a schema, create tests, or change canonical acceptance.

See [Execution Verdict and Artifact-Release Reconciliation](EXECUTION_VERDICT_ARTIFACT_RELEASE_RECONCILIATION_20261029.md) for the current CASE-04 timeout crosswalk, artifact-free task analysis, the read-only `report_contract.py` review, and the finding that `scripts/lifecycle_contract.py` was absent from the inspected research branch and `main`.

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
