# Shared Contract Readiness and State-Domain Crosswalk

**Date:** 2026-11-01  
**Status:** Provisional architecture analysis. Not a frozen schema, API, implementation plan, or adoption approval.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Reconcile the existing PocketCode shared-core and execution-contract proposals with RevDev's mission/publication/recovery authorities before drafting any common contract.

## 1. Executive finding

The projects should not begin by defining one universal `status` field. The existing authorities describe at least three independently evolving state domains:

1. **Execution outcome:** what happened to the work itself, based on trusted execution evidence.
2. **Coordination disposition:** where the task/job/attempt sits in the coordinator's lifecycle, including dispatch uncertainty, retry, cancellation and reconciliation.
3. **Publication and delivery state:** whether a result/evidence bundle has been durably recorded, authorized for disclosure, transferred, and verifiably received where such proof exists.

A fourth concept, **user-facing verdict**, is a derived presentation of execution evidence and must not be used as the storage authority for the other domains.

This is not a new claim that all fields are already implemented. It is a design distinction supported by the current PocketCode proposals and RevDev P8U acceptance specification.

## 2. Exact authority set reviewed

### PocketCode

- `PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md`, blob `35344d54cd7864862797c424686de885a217c70d`: proposed shared result contract with PASS/FAIL/INCOMPLETE, execution status, run identity, runtime/version, exit code when available, duration, bounded stdout/stderr and output metadata. It explicitly states current prototype is static/simulated and RevDev compatibility is not verified.
- `PRODUCT/EXECUTION_CONTRACT.md`, blob `128a00a9b2a335514814cab76fb5781fe8f9f858`: proposed provider-neutral execution lifecycle with accepted/queued as nonterminal and succeeded/program_failed/timed_out/cancelled/rejected/infrastructure_failed as terminal states. It distinguishes client disconnect from execution completion and requires idempotency and uncertainty handling.
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`: LOOP-01..14; explicitly separates user-facing verdict from lifecycle status and requires that PASS be backed by trusted terminal evidence plus exit code 0.
- `AI_COLLAB/UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md`, blob `51edbb9bd1e3f3518b0e80620be9c0ebe88f49ab`: proposed durable coordinator lifecycle and separate identities for job, attempt, reservation version, fencing epoch, provider token, events, report, publication and transfer. New tests NOT RUN.
- `AI_COLLAB/LIFECYCLE_ORDERING_AND_EVIDENCE_PRESERVATION_REVIEW_20261101.md`, blob `a163b72cf2dc802e272bfe38edd3910bac7d585e`: calls out that release authorization and transfer completion must not be conflated, and that cleanup must not destroy evidence before durable capture.

### RevDev

- `resume/revdev/P8U_PUBLICATION_RECOVERY_ACCEPTANCE_2026-09-30.json`, blob `e60c506d00e6ef6e1f1279b40e124a5cff354a6b`: explicitly separates `eventsVocabulary.execution` (`NOT_RUN`, `RUNNING`, `PASS`, `FAIL`) from `eventsVocabulary.publication` (`NOT_ATTEMPTED`, `PENDING_RETRY`, `PUBLISHED`, `PERMANENT_ERROR`) and remediation. P8U-01 requires product PASS to remain PASS while publication is pending retry, retaining exact local result identity and forbidding second execution/audio.
- `resume/revdev/SHARED_INFRA_RELIABILITY_HARDENING_PLAN_2026-09-30.md`, blob `6a0c804e1ad75edf1022af960acbb143ba1430b6`: describes queue ingestion, per-project bulkheads, dependency-light finalization, publication context, transactional/idempotent queue state and recovery requirements. This is a plan, not current runtime proof.
- `resume/revdev/POCKETCODE_REVDEV_ACCEPTANCE_TRACEABILITY_SUPPLEMENT_2026-10-29.md`, blob `d56da68bdc5414cf518d97abc63445f26c6af1fa`: preserves separate canonical suites and explicitly classifies conceptual relationships rather than claiming acceptance equivalence.

All referenced RevDev host/runtime behavior remains UNKNOWN until PC access returns. P8U implementation state is `SPEC_ONLY_NOT_IMPLEMENTED`; P8U scenarios remain NOT RUN in the required Windows/runtime shape. PocketCode execution and coordinator cases are proposals; no provider or device execution was run in this analysis.

## 3. State domains and invariants

### 3.1 Execution outcome

This answers: *what did the execution attempt actually do?*

Candidate shared concepts:
- `execution_outcome`: `SUCCEEDED`, `PROGRAM_FAILED`, `TIMED_OUT`, `CANCELLED`, `REJECTED`, `INFRASTRUCTURE_FAILED`, `UNKNOWN`.
- `exit_code`: nullable; include only when observed from an authoritative process/provider source.
- `termination_source`: source that confirms completion or termination, if known.
- `execution_evidence_ref`: immutable evidence references supporting the outcome.

Important qualification: PocketCode currently calls some of these lifecycle statuses, while RevDev P8U uses `PASS`/`FAIL` for its execution vocabulary. This table is a normalization proposal only. It must not silently rename or reinterpret existing canonical acceptance values. `REJECTED` may occur before an execution attempt exists, so the final schema may represent it as a request/attempt disposition rather than force a fictitious process execution record.

Invariants:
- `PASS` is a presentation verdict, not a substitute for the authoritative execution record.
- Missing or ambiguous terminal evidence is `UNKNOWN`/incomplete, never success.
- Client timeout or disconnect does not prove worker termination.
- A script's own printed PASS/FAIL lines remain untrusted program output unless independently validated.

### 3.2 Coordination disposition

This answers: *what is the system currently doing with the task and its attempts?*

Candidate shared concepts:
- `job_disposition`: `RECEIVED`, `VALIDATED`, `QUEUED`, `CLAIMED`, `DISPATCH_INTENT_RECORDED`, `START_CONFIRMED`, `RUNNING`, `CANCEL_REQUESTED`, `RECONCILIATION_REQUIRED`, `RETRY_WAIT`, `TERMINAL`, `MANUAL_REVIEW`.
- Stable `task_id`/`job_id` and separate `attempt_id`.
- Operation identity, request fingerprint, reservation/version and fencing data where the adapter supports them.
- Causal links from job to attempts and events.

Invariants:
- Job disposition is not execution outcome. A job may be in reconciliation while the actual attempt outcome is unknown.
- A retry is a new attempt or a formally defined continuation, never an implicit overwrite of the old attempt.
- Lease expiry or worker reassignment does not prove an old process/provider request stopped.
- Cancellation request and confirmed termination remain distinct.
- Same epoch alone is not enough for concurrent ownership; atomic expected-version/CAS semantics are required where concurrent coordinator mutations are possible.

### 3.3 Publication, authorization and delivery

This answers: *what happened to the result after execution?*

Candidate shared concepts:
- `evidence_persistence_state`: `NOT_CAPTURED`, `CAPTURE_PENDING`, `CAPTURED`, `INTEGRITY_VERIFIED`, `CAPTURE_FAILED`, `UNKNOWN`.
- `publication_state`: `NOT_ATTEMPTED`, `PENDING_RETRY`, `PUBLISHED`, `PERMANENT_ERROR`, `UNKNOWN`.
- `release_decision`: separate authorization identity, policy revision, scope and time.
- `transfer_state`: `NOT_STARTED`, `STARTED`, `PARTIAL`, `ABORTED`, `SERVER_COMPLETE`, `CLIENT_VERIFIED`, `UNKNOWN`.
- Artifact identity, digest, size, expectedness and retention reference.

Invariants:
- Execution success does not automatically authorize publication or disclosure.
- Publication failure must not rewrite a valid execution outcome or cause duplicate execution.
- Release authorization does not prove transfer started or completed.
- Transfer completion does not prove client-side integrity unless a verifiable receipt exists.
- Revoking a release decision cannot recall bytes already sent.
- Destructive cleanup must not occur until required evidence is durably captured or an explicitly approved evidence-loss state is recorded.
- Artifact-free success is valid when the trusted task definition says artifacts are not required; an empty artifact list alone does not prove that.

### 3.4 User-facing verdict

This answers: *what can the user safely be told?*

PocketCode's current canonical presentation is:
- `PASS`: trusted terminal success and exit code 0.
- `FAIL`: confirmed program/runtime failure or non-zero exit.
- `INCOMPLETE`: timeout, cancellation, rejection, infrastructure uncertainty, missing or ambiguous terminal evidence.

This verdict should be derived from authoritative execution evidence plus task-specific acceptance policy. It must not be derived from publication state, UI timer expiry, client disconnect, queue acceptance, or an agent-generated status string.

RevDev's P8U `execution` PASS/FAIL vocabulary remains its own acceptance authority. Do not directly replace it with PocketCode verdicts. The cross-project contract can carry an explicit mapping/projection only after each product owner approves its semantics.

## 4. Minimal shared identity model

Names below are proposed identifiers for a future contract, not accepted field names.

| Identity | Purpose | Why it must be distinct |
|---|---|---|
| `task_id` | User-intended unit of work across the product | Can span multiple attempts or platform handoffs |
| `job_id` | Coordinator's durable work record | A task may be decomposed or scheduled as multiple jobs |
| `attempt_id` | One execution attempt | Retry must not overwrite prior execution evidence |
| `operation_id` | One externally visible side effect such as provider start, publication or transfer | Stable across retries of the same operation |
| `event_id` | One source event | Duplicate delivery must be distinguishable from a new event |
| `evidence_id` | One immutable evidence record/object | Report history and raw evidence are not the same thing |
| `artifact_id` | One generated or transferred artifact | Artifact may be optional, staged, published or partially transferred |
| `release_decision_id` | One authorization decision | Authorization is separate from artifact identity and transfer |
| `transfer_id` | One delivery attempt | Partial/retried transfers must be independently observable |

Do not force RevDev's existing MissionId/RunId or PocketCode's current runId into a common field without a precise mapping and a compatibility review. Keep source-native identifiers and add explicit cross-references. No identity value itself grants permission.

## 5. Proposed minimum shared envelope, not a schema yet

A first portable envelope should likely carry:

- `contract_version` and `producer_product`.
- `task_id` plus source-native `job_id`/`mission_id`/`run_id` references.
- `attempt_id` where execution was attempted.
- `execution_outcome` with provenance and optional authoritative exit code.
- `job_disposition` as a separate axis.
- `evidence_refs[]` with digest, capture source, completeness and truncation state.
- `artifact_refs[]` with explicit required/optional/not-applicable/unknown expectation.
- `publication_state` and `release_decision_ref` as separate concepts.
- `transfer_refs[]` if a transfer occurred.
- `acceptance_refs[]` preserving the original product-specific suite and test IDs.

Avoid embedding raw secrets, full prompts, arbitrary environment variables, private paths, unrestricted stdout/stderr, or unbounded diffs by default. Evidence references should be bounded and access-controlled; report text is a projection, not the evidence store.

## 6. Existing contract gaps to resolve before schema freeze

| Gap | Current source tension | Required resolution |
|---|---|---|
| G-01 State axes | PocketCode's execution contract uses one run lifecycle; coordinator spec adds job/attempt/reconciliation; RevDev P8U separates execution and publication | Approve distinct `execution_outcome`, `job_disposition`, `publication_state` and derived verdict |
| G-02 Identity | PocketCode runId vs coordinator job/attempt/provider/operation IDs; RevDev MissionId/RunId/exact result path | Define source-native IDs and explicit cross-reference rules; never collapse mission/task/job/attempt |
| G-03 Terminal authority | Client timer/disconnect vs server/provider/process confirmation | Define trusted sources and UNKNOWN handling per execution adapter |
| G-04 Cancellation | Requested cancellation vs provider/process termination; detached process may continue | Model request and confirmed termination separately; adapter-specific proof |
| G-05 Retry/idempotency | Queue retry vs external start/publication side effect; same key with changed request | Define operation key scope, fingerprint, retention and ambiguous-call reconciliation |
| G-06 Evidence capture | Output may be destroyed by cleanup; collector/display truncation differs from runtime truncation | Capture required evidence before destructive cleanup; preserve completeness and truncation dimensions |
| G-07 Artifact expectation | Successful task may legitimately produce no files | Carry trusted artifact expectation, including `NOT_REQUIRED`; do not infer from empty list |
| G-08 Publication/release/transfer | RevDev publication retry; PocketCode release and transfer semantics | Keep persistence, publication, authorization and byte transfer distinct |
| G-09 Acceptance equivalence | AWC/AEC vs LOOP/CASE vs P8U/P0-D | Preserve native IDs; share fixtures only where exact semantics match |
| G-10 Trust and policy | Task packet, AI output, MCP tool call or client field could be mistaken for authority | Every execution adapter enforces its own policy; contract fields are evidence/context, never permission |

## 7. Cross-project mapping: where shared concepts stop

| Concern | PocketCode meaning | RevDev meaning | Safe shared boundary |
|---|---|---|---|
| Work identity | Phone-prepared task/run and future local/remote execution | Mission plus one or more operation/run results | Correlation contract only; preserve native IDs |
| Execution | Browser/WASM, future user-owned remote host or future provider | Windows PowerShell/process runner and mission operations | Common outcome vocabulary with adapter-specific evidence |
| Queue | No durable local queue selected for MVP; coordinator persistence unresolved | Existing queue/runtime state UNKNOWN; P0 reliability plan exists | Requirements and test fixtures only until real store is known |
| Retry | Provider start and ambiguous remote execution; do not duplicate billable run | Publisher retry must republish exact result without rerunning product mission | Separate execution retry from publication retry |
| Cancellation | Future remote process/provider cancellation | Windows process-tree termination and mission-level cancellation | Shared intent vocabulary; separate termination proof |
| Evidence | Run output, checks, files, runtime/version, provider events | Exact local terminal result, stdout/stderr, mission metadata, publisher/recovery traces | Common metadata envelope; separate collectors and trust roots |
| Artifact delivery | Download/share to phone, transfer authorization and client receipt | Local result path, GitHub publication, exact-result identity | Shared artifact metadata; distinct delivery adapters |
| Security | Browser origin, mobile storage, remote host trust and possible provider boundary | Windows host guard, RelayRef, mission authorization and queue isolation | Shared threat vocabulary; no shared authorization engine by assumption |
| Acceptance | LOOP/CASE/AEC/AWC as applicable | P8U/P0-D/RelayRef and product suites | Preserve all namespaces; no automatic test equivalence |

## 8. Recommended design order

1. Approve terminology and state axes only; do not pick field names prematurely.
2. Build a source-to-field traceability table preserving native identifiers and acceptance IDs.
3. Define a versioned minimal JSON Schema only for the portable envelope, with `additionalProperties` policy and explicit unknown/null semantics.
4. Create golden valid/invalid fixtures for: accepted-not-started; provider-start-unknown; cancellation-requested-but-running; duplicate event; stale worker; execution PASS with publication pending; execution FAIL with publication retry; artifact-not-required; missing terminal evidence; output collector truncation; runtime output limit; report-display truncation; release authorized but transfer not started; partial transfer; cleanup before evidence persistence.
5. Have Claude review implementation feasibility and Gemini red-team the state/identity/security semantics independently.
6. Only after those reviews, consider a dependency-light shared library or code generation. The first implementation may be two independent validators consuming the same schema and fixtures.

## 9. Open decisions and unresolved evidence

- Which existing PocketCode run contract fields are mandatory in the first bounded task, and which remain optional/unknown?
- Which RevDev MissionId/RunId/result fields are authoritative in the current source/runtime? UNKNOWN until PC access.
- Does the shared envelope represent a task, a job, an attempt, or a report? Recommendation: it is a task-linked **result/evidence envelope** referencing separate job/attempt records, not a universal mutable state object.
- Which publication concepts should RevDev export to PocketCode in the first integration? Do not assume GitHub publication is PocketCode's artifact-delivery mechanism.
- How will acceptance references be serialized without falsely claiming equivalence across product suites?
- Which evidence fields can be shared safely without leaking secrets or proprietary content?
- How are retention, deletion, redaction, access and transfer receipts handled by each product?

## 10. Non-actions and status

This is a documentation-only crosswalk. No code, schema, test, acceptance suite, PR #2/#3, provider, account, workload, Actions, billing, merge, deployment, queue, local host or PC state was changed or exercised. No tests were run. No open-source candidate is approved by this document. The proposed field names and state values remain subject to owner, Claude and Gemini review.
