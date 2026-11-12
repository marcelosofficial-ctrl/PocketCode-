# Report projection v2 migration and acceptance plan

Date: 2026-11-12  
Status: proposed compatibility and acceptance plan; NOT IMPLEMENTED / NOT RUN.  
Authority: preserve PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md, LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. This note does not amend canonical acceptance or authorize source/test changes.

## 1. Purpose and verified baseline

The report path has two different helpers with different responsibilities:

- `scripts/execution_projection.py` is a pure typed-observation helper. It distinguishes coordinator lifecycle, direct-child natural exit, wrapper exit, signal termination and embedded-interpreter observations. Its docstring requires callers to authenticate producers, authorize attempts, deduplicate events, validate policy and persist observations first. It is not an authenticated coordinator.
- `scripts/report_contract.py` is a bounded plain-text renderer and explicitly does not verify input trust. It emits `Report format: 1` and currently calls `classify_verdict(status, exit_code)`.
- `scripts/result_receipts.py` is an in-memory model, not durable storage or a production release service.

Pinned source blobs rechecked from the active branch:
- `scripts/report_contract.py`: `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`
- `scripts/test_report_contract.py`: `85109f056009d65a274e9306deb39b68e1fefbd2`
- `scripts/execution_projection.py`: `f32237c8c5ee5d62b0416b3dd867515ce567c21b`
- `scripts/test_execution_projection.py`: `cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1`

**Confirmed formatter defect:** any non-bool integer nonzero `exit_code` returns FAIL before lifecycle is considered. Thus `timed_out + wrapper 137`, `cancelled + wrapper 143`, nonterminal + stale code, or `succeeded + nonzero` all become FAIL. The generic integer does not say whether it came from a natural child wait, wrapper, signal convention, embedded `SystemExit`, or stale/misbound observation.

**Important boundary:** the typed `execution_projection` helper already prevents wrapper/signal/embedded observations from becoming a child exit and makes timeout/cancel/rejection/infrastructure states INCOMPLETE. It is still a pure helper, not authenticated ingress, durable reduction, an overall job projection or an artifact-release authority. It is not wired into `format_report()`.

## 2. Migration decision

Do not patch the current formatter by swapping condition order or changing only verdict precedence. That would preserve an ambiguous two-field interface and still trust caller-supplied metadata.

Keep format 1 available as a legacy renderer for compatibility. Do not silently reinterpret its fields or claim it is safe for newly integrated execution evidence. Any future format-1 bug fix requires an explicit compatibility decision and regression evidence.

Propose a separate format-2 boundary only after an explicit owner implementation/test gate:

1. **Trusted evidence ingress:** authenticate producer/channel, authorize tenant and operation, bind CommandId, EffectId, DispatchAttemptId and ExecutionId where known, validate policy/fence, deduplicate identity and persist immutable observations. A typed object or field named `trusted` is not authentication.
2. **Execution projection:** derive PASS / FAIL / INCOMPLETE from accepted, attempt-bound lifecycle and child/runtime observations. A natural child exit is distinct from wrapper exit, signal termination and embedded interpreter result. Preserve contradictory observations as INCOMPLETE pending reconciliation.
3. **Overall job/evidence disposition:** separately account for required policy/egress barriers, observation completeness, collection and cleanup. Missing required evidence is INCOMPLETE, not an inferred success or failure.
4. **Artifact disposition:** separately account for staged bytes, parent read-back integrity, manifest/receipt binding, quarantine, fresh authorization, release, transport emission and client acknowledgement. Execution PASS does not authorize artifact release.
5. **Versioned renderer:** consume an already resolved, immutable projection and display its provenance and uncertainty. It must not authenticate, repair, infer or reclassify raw observations.

The version-2 schema, serialization, persistence and public report layout remain proposals. Do not add redundant identity fields or freeze a schema until the execution boundary and owner gate are approved.

## 3. Non-negotiable projection rules

- PASS requires trusted coordinator success, a direct-child natural exit of zero, all applicable mandatory security/evidence gates, and no contradiction.
- A trusted program/runtime failure or direct-child natural nonzero exit may establish FAIL only under the approved provenance and lifecycle rules.
- CASE-04 timeout remains INCOMPLETE / timed_out. A wrapper code such as 137 or 143, signal termination, cancellation request or worker self-report is not a natural child failure.
- succeeded + natural child nonzero, program_failed + natural child zero, or nonterminal lifecycle + terminal child evidence are contradictions. Preserve both facts; do not choose a winner by field precedence.
- Wrapper exit zero with no child wait is INCOMPLETE. Embedded Python exception/SystemExit is an interpreter observation, not native child exit.
- Missing, unauthenticated, stale, wrong-attempt or contradictory evidence is UNKNOWN/INCOMPLETE.
- Keep CommandId, EffectId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceiptId/revision and PublicationAttemptId distinct.
- A renderer's displayed evidence source, run ID, runtime, checks or output are not proof of producer identity.

## 4. Required future regression matrix

A future authorized format-2 implementation must include at least:

| Case | Input/evidence | Required result |
|---|---|---|
| R2-01 | succeeded + authenticated child natural exit 0 + required gates | PASS candidate |
| R2-02 | trusted program_failed + natural child nonzero | FAIL |
| R2-03 | timed_out + wrapper 137 or signal termination | INCOMPLETE / timed_out |
| R2-04 | cancelled + wrapper 143 | INCOMPLETE / cancelled |
| R2-05 | wrapper exit 0, child wait absent | INCOMPLETE |
| R2-06 | succeeded + natural child nonzero | INCOMPLETE contradiction |
| R2-07 | program_failed + natural child zero | INCOMPLETE contradiction |
| R2-08 | accepted/queued/running + purported terminal child exit | INCOMPLETE pending reconciliation |
| R2-09 | embedded SystemExit/exception without native child wait | INCOMPLETE unless trusted runtime contract independently resolves it |
| R2-10 | wrong attempt, producer, tenant, sequence or policy binding | reject/quarantine; no PASS/FAIL inference |
| R2-11 | child exit zero but required policy/egress barrier missing | INCOMPLETE; artifact blocked |
| R2-12 | execution PASS candidate but collection/cleanup/integrity missing | overall INCOMPLETE; artifact blocked |
| R2-13 | bytes emitted but no exact client acknowledgement | transport_emitted only; not client_received |
| R2-14 | legacy format-1 golden inputs | byte/field compatibility retained unless separately approved |

Tests must assert both the projection and retained raw evidence, provenance, attempt identity and uncertainty. Pure helper tests cannot prove authentication, persistence, provider behavior, process-tree termination, browser storage or client receipt. Adapter and canonical CASE acceptance remain separate gates.

## 5. Migration sequence and stop conditions

1. Reconcile the canonical execution acceptance, owner decision register, exit-provenance resolution and lifecycle/receipt contract. Keep CASE-04 and all canonical IDs unchanged.
2. Obtain explicit owner approval for the exact source/test scope. The P39 implementation/adapter conformance gate is currently CLOSED.
3. Have independent architecture/security review identify counterexamples before implementation.
4. Pin exact source/test SHA; add deterministic pure projection tests first, then formatter compatibility tests. Do not add dependencies or select runtime/provider/database/transport/storage.
5. Only after a separate adapter gate, prove authenticated ingress, durable event/receipt persistence, restart/replay, concurrency, real termination and artifact/client acknowledgement.

Stop if the caller cannot supply authoritative producer and attempt provenance, if child/wrapper semantics are unavailable, if a required security barrier is unknown, or if the proposed change would alter canonical LOOP/CASE meanings.

## 6. Evidence status

- VERIFIED: source behavior and helper separation above are present at the pinned blobs.
- VERIFIED: the pure execution projection already distinguishes child, wrapper, signal and embedded observations, but is not authenticated or integrated.
- INFERRED: a versioned renderer over three resolved projections is the lowest-risk migration direction while preserving format 1.
- UNKNOWN: production ingress, durable adapter, actual runtime termination semantics and artifact/client receipt integration.
- NOT RUN: this document's regression matrix; no tests were executed for this documentation unit.
- No application source, tests, canonical acceptance IDs, provider, runtime, database, transport, storage engine, host, deployment, PR or budget decisions changed.
