# PocketCode — provider-neutral result envelope and fake-adapter protocol

**Date:** 2026-10-29  
**Status:** Design/test specification only; NOT implemented and NOT RUN.  
**Prerequisites:** `CROSS_BRANCH_CONFORMANCE_GAP_AUDIT_20261029.md`; canonical `PRODUCT/EXECUTION_CONTRACT.md` and `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`.  
**Scope:** Define the smallest seam between a future trusted execution coordinator, a provider/runtime adapter, and the existing report formatter. This document does not choose a provider, freeze a public API, or authorize implementation, accounts, workloads, spend, merge, or deployment.

## 1. Objective and non-goals

The adapter boundary must prevent three different facts from collapsing into one ambiguous status:

1. **Execution observations:** what the trusted execution boundary actually observed about start, child/process exit, timeout/cancel/limit events, output collection, and artifact production.
2. **Control-plane and safety evidence:** whether the required policy was applied before dispatch, whether termination and cleanup were confirmed, whether artifacts are valid and correctly associated, and whether the requester is authorized for the job.
3. **Derived disposition:** what PocketCode is justified in telling the user now, under a versioned policy.

The existing PR #2 report helper is a formatter/classifier for caller-supplied data; it is not the trusted producer. The PR #3 lifecycle helper is a pure model; it is not durable storage, a runner, or a provider adapter. The envelope below is a proposed join between them.

Non-goals: selecting wire-format field names, defining an HTTP API, claiming exactly-once provider execution, designing production storage, proving sandbox/egress controls, or replacing canonical acceptance criteria. (The intended term is **egress** control; no enforcement is established by this document.)

## 2. Core invariants

1. **One attempt identity:** every execution attempt has a stable opaque `job_id` and `attempt_id`; retries that refer to an existing attempt must not allocate a new attempt.
2. **Raw facts are immutable:** accepted observations are append-only. Reconciliation creates a new evidence/report version; it does not rewrite an issued report.
3. **Outcome is not disposition:** an observed zero exit is not equivalent to overall PASS. Keep execution outcome and derived disposition separately.
4. **Unknown is a first-class value:** missing exit, lost acknowledgement, uncertain termination, failed state lookup, or contradictory terminal evidence must remain explicit. Never fill gaps with guessed values.
5. **Only the trusted producer can set authoritative fields:** task source, stdout/stderr, generated JSON, filenames, and client-supplied report fields are untrusted data. They may be shown as data but cannot set lifecycle status, exit code, policy state, cleanup state, artifact authority, or tenant ownership.
6. **Policy before dispatch:** no adapter task-start call occurs until the exact required policy revision is authoritatively confirmed as applied for that attempt immediately before dispatch. **A read-then-dispatch sequence alone does not close a time-of-check/time-of-use race.** A real boundary must either bind the attempt to an immutable policy revision or provide an atomic/conditional dispatch guarantee that rejects a changed revision; if neither is available, the policy barrier remains unproven and the boundary is not acceptable for untrusted code.
7. **No blind replay:** after an ambiguous acknowledgement, look up the existing attempt. If authoritative state cannot be recovered, return UNKNOWN/INCOMPLETE and do not redispatch automatically.
8. **Artifact fail-closed:** no artifact is released until final stored-byte integrity, job/attempt association, tenant authorization, and cleanup requirements are satisfied.

   **Release-boundary validation:** immediately before each export/download, re-evaluate current authorization and artifact state rather than inheriting a historical PASS. Validate normalized safe artifact path/name, allowed media type, size/count limits, final stored-byte integrity, and job/attempt/tenant association at the actual release boundary. Deny or quarantine on mismatch, stale/unknown required evidence, or failed validation. A secret-scanning/redaction check may be an additional policy gate if selected, but it is not currently a chosen mechanism and must not be represented as present or verified. Do not rely on regex log redaction as the primary secret-protection mechanism.
9. **Report is a projection:** report formatting can render a trusted envelope but cannot create missing trust or execution evidence.
10. **Local and hosted evidence stay separate:** local UX tests cannot pass provider-side isolation, egress, termination, multi-tenant, or durable recovery criteria.

## 3. Proposed typed envelope (conceptual, not a frozen schema)

Use typed fields/enums in an eventual implementation. The following is a semantic contract, not a copy-ready public JSON schema.

### 3.1 Identity and provenance

- `contract_version`: version of the envelope semantics.
- `job_id`: opaque stable identifier for the logical request.
- `attempt_id`: opaque identifier for one actual attempt; explicit rerun gets a new attempt.
- `tenant_ref`: server-derived authorization namespace or a non-sensitive internal reference. Never trust a client-supplied tenant ID.
- `report_version`: monotonically increasing version for the derived report.
- `evidence_events[]`: append-only facts with event identity, tenant/job/attempt binding, coordinator sequence, authenticated source class, observed time, payload schema/version, typed payload, and relevant policy revision.
- **Proposed event-ID model (not frozen):** the coordinator assigns a unique internal `event_id` to each accepted canonical event. Preserve any provider-supplied identifier separately as `source_event_id`; do not assume provider IDs are globally unique. Deduplicate source replays using an explicit namespace such as `(source_namespace, tenant_ref, job_id, attempt_id, source_event_id)` when the source contract supports it. If a source provides no stable event ID, define and test a bounded canonical fingerprint/reconciliation policy rather than assuming replay identity.
- `coordinator_sequence` is assigned by the trusted coordinator/append boundary and is unique within the event stream reduced for a particular attempt. Provider timestamps may be retained as observations but do not establish ordering. A sequence collision within one attempt is a contradiction and diagnostics must identify every colliding record.
- **Duplicate equivalence:** a source replay is identical only when the scoped source identity and all immutable observation fields match, including event kind, coordinator sequence/canonical sequence binding, payload/schema version, tenant/job/attempt/source binding, and relevant policy revision. Only explicitly designated delivery-only metadata may vary. Different payload or identity under the same scoped source event ID is a conflict, not a retry.
- Accepted payloads must be immutable snapshots (for example, validated canonical serialization or deep immutable records); a shallow copy with mutable nested payload references is insufficient.
- `trust_boundary`: implicit in the authenticated producer and validation path. Do **not** implement it as a user-controlled `trusted=true` flag.
- `evidence_quality`: COMPLETE | MISSING | CONTRADICTORY | STALE. This qualifies the evidence; it does not replace execution outcome or disposition.

### 3.2 Execution observations

- `execution_outcome`: NOT_STARTED | EXIT_ZERO | EXIT_NONZERO | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | UNKNOWN.
- `child_exit_code`: optional integer, present only when directly observed from the child process or an authoritative equivalent. Do not infer it from output text or wrapper exit.
- `wrapper_outcome` and `wrapper_exit_code`: optional and only present if the selected architecture has an independently failing wrapper/supervisor process. Decide at boundary selection; do not add redundant fields if no such independent process exists.
- `started_at` / `terminal_observed_at`: optional trusted timestamps. Timestamps aid diagnosis but do not by themselves resolve conflicting event ordering.
- `termination_state`: CONFIRMED | NOT_CONFIRMED | UNKNOWN, with evidence source. A timeout/cancel request is not termination confirmation.

### 3.3 Output collection

For each stream independently:

- `state`: COMPLETE | UNAVAILABLE | PARTIAL_FAILURE | TRUNCATED_BY_POLICY.
- `retained_bytes`: actual bytes retained, bounded by policy.
- `observed_bytes`: actual observed count if reliably known; otherwise null/unknown, not estimated silently.
- `reason_code`: a bounded machine-readable reason where applicable (for example COLLECTOR_ERROR, SOURCE_UNAVAILABLE, OUTPUT_CAP).
- `content`: optional bounded text/bytes, escaped safely at report presentation time.

Do not equate an empty complete stream with an unavailable stream, a partial collector failure, or truncation due to the output cap. A capped stream does not, by itself, prove that the process was terminated or failed. Define whether each stream is required by the specific acceptance/report case and whether bounded partial capture is accepted; do not silently impose a universal complete-stream requirement. If a selected adapter cannot encounter partial collection failure, document that limitation rather than inventing unnecessary states. Never buffer an unbounded stream just to compute these fields.

**Verdict interaction:** preserve any trusted child exit code/outcome even when stream collection is degraded; collection failure does not rewrite the raw exit fact. If a stream required by the specific acceptance/report case is `UNAVAILABLE` or `PARTIAL_FAILURE`, or required output is `TRUNCATED_BY_POLICY` without an explicitly accepted partial-output rule, the coordinator must not project an otherwise zero exit as PASS. If a stream is optional or bounded partial capture is explicitly accepted for that case, derive the verdict from trusted terminal evidence and the remaining mandatory gates; do not fail solely because optional diagnostics are unavailable or capped. Use INCOMPLETE (or a more specific non-success disposition if the authoritative cause is established) when a required gate is unsatisfied, retain the exit fact, expose the collection state/reason, and deny artifact release whenever its required integrity/evidence gates are unresolved. A genuinely complete empty stream remains distinct and may be valid. Do not conflate a collector failure with `cleanup_state`; record cleanup independently.

**Truncation vocabulary:** keep runtime-enforced output limiting separate from report/UI presentation truncation. At the envelope/report seam, expose distinguishable facts equivalent to `stream_truncated_by_runtime` and `display_truncated_by_ui` (or typed fields with the same unambiguous meaning). Runtime truncation must be supported by trusted enforcement evidence; UI truncation must never be treated as a runtime limit event.

### 3.4 Safety/control evidence

- `required_policy_revision`: the policy revision expected by the coordinator.
- `applied_policy_revision`: the revision authoritatively observed as applied before dispatch, if the boundary can expose it.
- `policy_barrier_state`: CONFIRMED_MATCH | MISSING | PENDING | MISMATCH | STALE | UNKNOWN.
- `cleanup_state`: PENDING | CONFIRMED | FAILED | UNKNOWN.
- `artifact_validation_state`: NOT_APPLICABLE | PENDING | VALID | INVALID | UNKNOWN.
- `tenant_job_authorization_state`: CONFIRMED | DENIED | UNKNOWN.
- `limit_events[]`: typed limit identifier, observed value if trustworthy, configured limit revision, and enforcement outcome. Do not claim that a configured limit was enforced merely because it appears in a report.

### 3.5 Derived disposition

- `job_disposition`: REJECTED | PASS | FAILED | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | INCOMPLETE | PROVIDER_ERROR.
- `disposition_policy_version`: version of the deterministic rules used to derive disposition.
- `disposition_reasons[]`: bounded reason codes that explain why PASS was withheld or a non-success disposition was selected.
- `artifact_release_allowed`: not a trusted input field. Compute at the release boundary from authoritative current evidence and authorization; never accept it from client/task/report JSON.

The report formatter should receive an envelope created/validated by the trusted coordinator. If the formatter remains a generic pure helper, its API must make clear that it formats supplied evidence only and cannot authenticate it.

## 4. Proposed conservative disposition rules

This table specifies required behavior for the adapter/report seam. It does not replace the existing lifecycle helper or canonical contract; discrepancies should be resolved explicitly before implementation.

| Observed execution outcome | Other authoritative evidence | Minimum disposition behavior | May report PASS? |
|---|---|---|---|
| NOT_STARTED | Validation/policy rejection confirmed | REJECTED | No |
| EXIT_ZERO | Required policy barrier, terminal evidence, cleanup, artifact validity/association, tenant authorization, and case-specific required-output rule all confirmed; no disqualifying limit event under D-01 or contradiction. Display-only truncation is not a disqualifying runtime event. | PASS | Yes |
| EXIT_ZERO | Any mandatory gate missing, stale, contradictory, or unknown, including required output collection being unavailable/partial | INCOMPLETE (or explicit provider error if the cause is established) | No |
| EXIT_NONZERO | Trusted child failure evidence | FAILED | No |
| TIMED_OUT | Termination confirmed and timeout evidence authoritative | TIMED_OUT | No |
| TIMED_OUT | Termination not confirmed or evidence contradictory | INCOMPLETE | No |
| CANCELLED | Termination confirmed and cancellation evidence authoritative | CANCELLED | No |
| CANCELLED | Termination not confirmed or evidence contradictory | INCOMPLETE | No |
| LIMIT_EXCEEDED | Limit event is authoritative | Preserve `LIMIT_EXCEEDED` as disposition and separately preserve terminal/cleanup facts; verdict mapping for confirmed limit-triggered termination remains open under D-01. Never report PASS for a run that the trusted boundary confirms was terminated/failed by the limit; if the terminal outcome is unknown/contradictory, use INCOMPLETE. | No |
| UNKNOWN | Provider/adapter cannot establish the outcome | INCOMPLETE or PROVIDER_ERROR based on known cause | No |
| Any | Distinct conflicting terminal events or impossible sequence | Preserve all evidence; derive INCOMPLETE/PROVIDER_ERROR under the selected policy | No |

**Important nuance:** preserving a trusted nonzero program exit as an execution fact does not require claiming cleanup succeeded. The overall disposition must never be PASS when a mandatory safety gate is missing. Whether a known program failure is projected as FAILED or INCOMPLETE when cleanup is also uncertain must be defined consistently: preserve both facts and make the safety uncertainty visible rather than erasing either. Do not let the report's single legacy status field be the only storage of this distinction.

**Proposed resolution (see [semantic decision note](SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md)):** when a trusted, non-contradictory child exit confirms program failure, preserve the user-facing verdict as FAIL even if cleanup is UNKNOWN/FAILED. Report cleanup uncertainty independently and keep artifacts blocked. Reserve INCOMPLETE for an outcome that is not a confirmed success or confirmed program failure, including contradictory terminal evidence. This follows the canonical verdict definitions; it does not claim cleanup succeeded.


The PR #2 vocabulary currently has no dedicated `limit_exceeded` value and its formatter maps unknown status labels to `unknown`. Do not silently translate a known limit event into `program_failed`; extend or wrap the report envelope deliberately when an integration is authorized. Also keep an enforced execution output cap separate from report-rendering truncation: the latter is a presentation fact, not evidence that the runtime limit was exceeded. See the semantic decision note for proposed fields and regression cases.

## 5. Minimal fake-adapter protocol

This protocol is designed for deterministic, offline tests with no network, provider SDK, account, or live workload. It is a future test seam, not a claim that these methods exist today.

Conceptual operations:

1. `reserve(request_fingerprint, tenant_scope, idempotency_key) -> existing_or_new_job_ref`
2. `read_authoritative_state(job_id, attempt_id) -> typed_state_or_UNKNOWN`
3. `read_applied_policy_revision(attempt_id) -> revision_or_UNKNOWN`
4. `dispatch_once(job_id, attempt_id, source_ref, input_refs, expected_policy_revision) -> acknowledgement_or_AMBIGUOUS`
5. `read_terminal_evidence(job_id, attempt_id) -> evidence_events`
6. `request_cancel(job_id, attempt_id) -> request_ack_only`
7. `read_termination_state(job_id, attempt_id) -> CONFIRMED | NOT_CONFIRMED | UNKNOWN`
8. `read_cleanup_state(job_id, attempt_id) -> PENDING | CONFIRMED | FAILED | UNKNOWN`
9. `validate_artifact(job_id, attempt_id, artifact_ref) -> typed_validation_result`
10. `release_artifact(job_id, attempt_id, artifact_ref, authenticated_tenant) -> allow_or_deny`

The fake records every call, argument, and sequence number. Tests must assert both return values **and call count/order**. A fake can prove coordinator logic and mapping; it cannot prove real provider enforcement, filesystem isolation, egress blocking, termination, or storage durability.

**Durability and dispatch caveat:** `reserve(...)` must be implemented as an atomic, durable uniqueness decision scoped to tenant + idempotency key + request fingerprint, including concurrent requests and coordinator restarts. A successful reservation must be durably associated with the same job/attempt before any dispatch can occur. `dispatch_once(...)` is a coordinator invariant/name, not a magical exactly-once guarantee: if the provider can accept a start request while losing its acknowledgement and cannot authoritatively look up that same attempt, the outcome remains UNKNOWN and automatic redispatch is forbidden. Even a durable coordinator reservation cannot prove exactly-once execution inside a provider that lacks idempotent start or authoritative attempt lookup. The fake can test these intended branches, but cannot establish production atomicity or durability.

**Policy-race caveat:** FAKE-03/04 can prove that the coordinator refuses dispatch when its fake policy revision is missing, pending, or mismatched, and can exercise a simulated policy change. They do not prove the real execution boundary closes the race between the final policy read and task start. Before hosted acceptance, require evidence of immutable per-attempt policy binding or an atomic conditional start; otherwise mark the policy barrier BLOCKED rather than VERIFIED.

## 6. Required synthetic conformance cases (NOT RUN)

| ID | Setup / injected fault | Required assertions | Acceptance anchors |
|---|---|---|---|
| FAKE-01 | Valid exit-zero; every required gate confirmed | One dispatch; disposition PASS; report reflects authoritative outcome and run ID | CASE-01; LOOP-03 |
| FAKE-02 | Exit-zero but cleanup UNKNOWN | Preserve EXIT_ZERO observation; disposition not PASS; artifact release denied | CASE-12; LIFE-SEM-01 |
| FAKE-03 | Exit-zero but policy revision missing/pending/mismatched | Dispatch call count is zero; disposition not PASS | LOOP-12; CASE-15; NET-BARRIER-01 |
| FAKE-04 | Policy matches during prepare but changes before dispatch | Re-read exact applied revision immediately before start; mismatch yields zero dispatch calls | NET-SEM-01 |
| FAKE-05 | Dispatch accepted by fake; acknowledgement lost; client retries same tenant/key/fingerprint | One reservation, one dispatch; retry returns same job/attempt reference after authoritative lookup | CASE-13; IDEM-SEM-01 |
| FAKE-06 | Lost acknowledgement; authoritative lookup returns UNKNOWN | No second dispatch; outcome/disposition remains unknown/incomplete | CASE-13 |
| FAKE-07 | Same key with changed source/input/policy fingerprint | Conflict before dispatch; no prior report/artifact substitution | IDEM-SEM-02 |
| FAKE-08 | Same textual key used by different tenant scopes | Separate reservations; no cross-tenant result/existence disclosure | IDEM-SEM-04 |
| FAKE-09 | Cancellation requested but termination remains UNKNOWN | Do not report confirmed cancellation; no PASS; retain request and uncertainty | CASE-05 |
| FAKE-10 | Timeout event and late exit-zero event have conflicting order/identity | Preserve both; apply selected sequence/contradiction rule; never silently overwrite terminal decision with PASS | CASE-04; RACE-SEM-03 |
| FAKE-11 | Child exits nonzero but wrapper exits zero (only if both exist) | Preserve separate observations; disposition is not PASS | CASE-02/03/06 |
| FAKE-12 | Empty output vs unavailable vs prefix + collector failure vs policy truncation | Distinct stream states; retain prefix; mark unknown remainder; never describe partial output as complete | CASE-03/07/12 |
| FAKE-13 | Artifact write interrupted or final digest mismatch | No manifest publication/release; disposition not PASS | CASE-14; ART-SEM-01 |
| FAKE-14 | Artifact belongs to another job/tenant | Deny release; do not leak filename, digest, or existence beyond authorized response policy | LOOP-10/12; ART-SEM-03 |
| FAKE-15 | Two runs complete in reverse start order | Each report and artifact retains the correct job/attempt binding | CASE-16 |
| FAKE-16 | Script prints JSON claiming PASS or forged exit code | Treat as ordinary untrusted output; authoritative envelope unchanged | CASE-09/10; LOOP-11 |
| FAKE-17 | Historical report is PASS but release-time artifact validation now fails (unsafe path/name, disallowed media type, size/integrity mismatch, changed authorization, or unresolved required gate) | Deny/quarantine export despite historical PASS; record current reason; no cross-job/tenant disclosure | LOOP-10/11/12; CASE-14/15 |

### Fake test design rules

- Use deterministic in-memory fixtures and synthetic identifiers; no real secrets, provider credentials, network calls, external side effects, or persistent data.
- Make dispatch an observable counter with an injected “accepted but acknowledgement lost” outcome.
- Make policy revision a mutable fake value so the prepare/dispatch race can be asserted.
- Represent UNKNOWN explicitly; do not substitute a plausible default.
- Separate “request was acknowledged” from “operation was applied” and from “operation is terminal.”
- Test tenant scoping at the reservation and result-lookup boundary, not only in a pure key-comparison helper.
- Tests should fail if the coordinator makes an extra dispatch call, even if the final status happens to look correct.
- Run tests only after an authorized implementation change and an available interpreter; record exact command, interpreter/version, commit, counts, failures, and limitations. Until then the cases are specifications, not passing tests.

## 7. Suggested implementation sequence after authorization

1. Review the vocabulary and resolve the known-nonzero-plus-uncertain-cleanup disposition nuance without losing facts.
2. Implement a small pure envelope validator and mapping function; keep it independent of provider SDKs.
3. Add fake-adapter tests FAKE-01..16, starting with false-PASS, lost acknowledgement, and policy barrier cases.
4. Review the report formatter as a projection of the envelope; retain bounded output and explicit missing/partial/truncated semantics.
5. Only after provider and execution boundary selection, add real adapter tests for the guarantees the provider can authoritatively expose.
6. Only after explicit owner approval and strict $0 verification, run the first-useful-proof sequence and any controlled hosted-security tests.

## 8. Evidence and authorization status

- This document is design/test specification only.
- No test command was run as part of creating it.
- No runtime, provider, adapter, store, or API has been selected or validated.
- No account, billing, workload, merge, deployment, or production implementation is authorized.
- Canonical acceptance remains unchanged: 14 LOOP criteria and 16 CASE scenarios remain in force.
- PR #2 and PR #3 remain separate drafts and are not modified by this artifact.

## D-06 durability boundary cross-reference

FAKE-05/06 specify coordinator behavior only. The full recovery contract is `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md` (DR-01..DR-12), including concurrent reservations, crash windows, lease expiry, persistence restart, provider lookup semantics and tombstone retention. Do not infer exactly-once execution from one durable local reservation. If dispatch may have been accepted and authoritative lookup is UNKNOWN/unavailable, keep the original attempt unresolved and forbid automatic redispatch. Any provider guarantee remains unverified until the selected provider contract and integration tests establish it.
## D-07 artifact-release boundary cross-reference

FAKE-13/14/17 cover coordinator-side decisions only. The full release-time contract is `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md` (AR-01..AR-14). Execution PASS does not grant permanent download permission; current authorization, exact tenant/job/attempt, trusted manifest, quarantine, immutable object version, exact-byte digest/size, safe response policy and bounded streaming must be enforced at the actual release boundary. A fake or metadata-only test cannot prove filesystem/object-store race resistance or HTTP behavior.

## Cross-decision audit pointer — 2026-10-29
See [CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md) for cross-boundary invariants, unresolved interface questions, and the proposed G0-G7 evidence gate sequence. This pointer does not close owner decisions or promote specification/fake-test evidence to provider, persistence, HTTP, or device integration evidence.


## Provider-neutral boundary contract sketch — 2026-10-29
See [PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md). It defines proposed operations and typed outcomes for atomic reservation, dispatch-intent/reconciliation, trusted evidence acceptance, append-only report publication, artifact publication/release, retention, and hard stops. It is a review sketch only: not a frozen schema, implementation, provider/store selection, or proof of any guarantee. All integration evidence remains NOT RUN.
