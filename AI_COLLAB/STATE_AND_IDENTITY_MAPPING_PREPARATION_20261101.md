# RevDev + PocketCode — State and Identity Mapping Preparation

**Date:** 2026-11-01  
**Status:** Provisional reconciliation aid. NOT OWNER-APPROVED, NOT A SCHEMA, NOT A FIELD/ENUM FREEZE, NOT IMPLEMENTED, NOT RUN.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Make the state and identity decisions explicit enough for Claude/Gemini review and owner decisions, without collapsing native product semantics or pretending unresolved mappings are settled.

## 1. Executive finding

The existing shared-contract readiness crosswalk correctly rejects a universal `status` field. This note sharpens it into **seven independently reportable state axes**, plus a separate artifact-expectation fact and operation-specific records:

1. execution outcome;
2. coordination/job disposition;
3. evidence persistence/integrity;
4. publication;
5. release authorization;
6. transfer/delivery/receipt;
7. user-facing verdict.

These axes are related by explicit, versioned projections. They are not a single ordered enum and must not be inferred from one another.

This is a semantic decomposition for review, not a proposal to create one mutable shared object. A portable result/evidence envelope may reference source-native records, but each product remains authoritative for its own execution, authorization, persistence and acceptance.

## 2. Important correction: not every terminal-looking lifecycle value is an execution outcome

PocketCode's proposed `PRODUCT/EXECUTION_CONTRACT.md` includes accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected and infrastructure_failed in a run-lifecycle vocabulary. The shared mapping must preserve that source contract while avoiding false process claims:

| Native lifecycle observation | Safe cross-domain interpretation | What it does NOT prove |
|---|---|---|
| accepted / queued | Coordination disposition before execution | No process has necessarily started unless dispatch boundary evidence says so |
| running | Coordination observation that execution is believed active | A UI timer or stale worker heartbeat is not authoritative process liveness |
| succeeded | Candidate successful execution observation only when trusted terminal source and exit 0 are established | HTTP acceptance, worker disappearance or printed PASS is not sufficient |
| program_failed | Candidate confirmed execution failure when supported by trusted child/runtime evidence | Wrapper/provider error alone is not a program failure |
| timed_out | A timeout/limit observation with provenance; verdict follows canonical CASE-04 | Client timeout or lost connection does not prove runtime termination |
| cancelled | Confirmed cancellation outcome only if authoritative termination is established | Cancel request/acknowledgement alone is not termination |
| rejected | Request/admission/coordination disposition if no execution attempt exists | Do not fabricate an execution attempt or process outcome |
| infrastructure_failed | Infrastructure/coordination failure classification; execution outcome may remain UNKNOWN | Does not prove child failure, child exit code, or whether execution started |

The PocketCode canonical acceptance currently states that a trusted timeout maps to `INCOMPLETE / timed_out` (CASE-04). Do not change this to FAIL by adopting a generic shared enum. The owner decision register D-01 explicitly preserves that working default unless canonical acceptance is deliberately revised.

Likewise, D-02's working default is user-facing INCOMPLETE and execution outcome UNKNOWN when provider failure leaves child terminal evidence unavailable. A confirmed infrastructure cause may be recorded as disposition `PROVIDER_ERROR`; it does not manufacture a child outcome.

## 3. Seven state axes

| Axis | Question answered | Candidate values / observations | Authority and hard boundary |
|---|---|---|---|
| Execution outcome | What happened to this execution attempt? | Trusted success, confirmed program failure, confirmed timeout, confirmed cancellation, unknown/not established | Execution adapter/host/provider evidence. No attempt means no execution outcome. Preserve source-native result. |
| Coordination disposition | What is the coordinator doing with the task/job/attempt? | Received, validated, queued, claimed, dispatch intent recorded, start uncertain/confirmed, running, cancel requested, reconciliation required, retry wait, terminal, manual review, rejected/provider error | Product-specific coordinator. A disposition never substitutes for process evidence. |
| Evidence persistence/integrity | Was required evidence captured durably and checked? | Not captured, capture pending, captured, integrity verified, capture failed, unknown | Evidence store/collector and its durable acknowledgement. Captured is not the same as published. |
| Publication | Was the exact result/evidence object published to its intended store? | Not attempted, pending retry, published, permanent error, unknown | Product-specific publisher and immutable object/result identity. Publication retry must not rerun execution. |
| Release authorization | Is this principal currently authorized to disclose this exact object? | Not requested, denied, authorized, expired/revoked, unknown | Product-specific authorization decision at release boundary. Authorization is scoped and time/policy bound; it is not a transfer. |
| Transfer/delivery/receipt | What happened to bytes delivered to a client/consumer? | Not started, started, partial, aborted, server complete, client receipt unverified, client verified, unknown | Transfer service plus client-side receipt/integrity proof where available. Server completion is not client verification. |
| User-facing verdict | What can safely be told to the user under the applicable acceptance policy? | PASS, FAIL, INCOMPLETE (PocketCode native vocabulary) | Derived projection from trusted execution facts plus case-specific requirements. Never a storage authority for other axes. |

**Separate fact, not another state axis:** artifact expectation, bound to the trusted task/acceptance definition: REQUIRED, OPTIONAL, NOT_REQUIRED, NOT_APPLICABLE, UNKNOWN (candidate vocabulary only). An empty artifact list does not prove NOT_REQUIRED.

**Operation records:** start, cancel, report append, publication, release decision and transfer are distinct side effects. Each operation needs its own identity, status, idempotency scope and reconciliation rules. Do not use one generic operation status to represent the whole job.

## 4. Derived-state rules and non-implications

The following are hard semantic rules for any future mapping:

- `PASS` requires trusted terminal success and exit code zero, plus the evidence explicitly required by that native acceptance case.
- `FAIL` requires confirmed program/runtime failure or trusted nonzero child exit. A wrapper/provider/coordinator error is not enough.
- `INCOMPLETE` covers timeout under current CASE-04, cancellation/termination uncertainty, rejection, infrastructure uncertainty, missing or contradictory terminal evidence.
- A job may be in `RECONCILIATION_REQUIRED` while execution outcome is UNKNOWN or while a trusted execution outcome is already known.
- A job can have execution PASS while evidence persistence or publication is pending. This is central to RevDev P8U-01.
- A report/artifact may be durably captured but not published; published but not authorized for release; authorized but not transferred; transferred but not client-verified.
- A transfer may be partial while the underlying execution and publication remain successful.
- Release denial, expiry, quarantine or transfer failure must not rewrite historical execution outcome/verdict.
- Evidence cleanup is prohibited until required evidence is durably captured or an explicit approved evidence-loss record exists.
- UNKNOWN is not false, empty, failed, not-started, or safe-to-retry. It remains a first-class uncertainty.
- Retry of an external side effect reuses the original operation identity where the contract requires idempotency. A new execution attempt is a new attempt identity and must not overwrite the previous attempt.

## 5. Identity domains: candidate map, not a universal ID

| Identity | Scope | Distinct from | Existing native anchors / limits |
|---|---|---|---|
| User task / intent ID | User's intended unit of work across handoffs | Mission, coordinator job, execution attempt | Product concept only; no approved shared field |
| RevDev MissionId | RevDev mission envelope / mission lineage | Individual operation or exact run result | P8U recovery references mission ID and run ID; current PC source/runtime remains UNKNOWN |
| PocketCode runId | PocketCode's current proposed run/report identity | User task, future coordinator job, provider operation | Appears in proposed PocketCode execution/report contract; exact mapping to a future attempt ID is not frozen |
| Coordinator jobId | Durable coordinator work record | Task, attempt, provider operation | Proposed in coordinator spec; not established as a current production identity |
| attemptId | One execution attempt | Job, mission, retry operation | Proposed shared/coordinator concept; mapping to RevDev MissionId/RunId and PocketCode runId remains unresolved |
| operationId | One externally visible side effect (start, cancel, append, publish, release, transfer) | Job/attempt and provider token | Proposed; must be stable across retries of that same operation |
| provider idempotency token | Provider-specific deduplication namespace | Internal operationId and attemptId | Provider not selected; token scope/retention UNKNOWN |
| source event identity | One producer's event in its own namespace | Coordinator event ID and coordinator sequence | D-04 OPEN; source namespace, tenant/job/attempt binding and immutable fields unresolved |
| coordinator event ID/sequence | Durable accepted observation and coordinator ordering | Provider event ID/sequence/timestamp | Proposed; ingress authentication and durable atomicity NOT RUN |
| evidence/result identity | One immutable evidence bundle or exact terminal result | Job/attempt, report version, artifact | RevDev P8U explicitly preserves exact local result path/hash; PocketCode evidence identity not implemented |
| artifact identity | One immutable output object/version | Evidence bundle and transfer | PocketCode D-07 boundary unselected; RevDev local result/publication is not automatically same as a PocketCode downloadable artifact |
| report identity/version | One immutable user/report projection | Raw evidence and latest pointer | D-08 OPEN; in-memory ReportHistory is not durable proof |
| releaseDecisionId | One authorization decision for principal + exact object + scope + policy/time | Artifact ID and transfer ID | D-07 proposed only; store/API boundary NOT RUN |
| transferId / receipt ID | One delivery attempt and optional client receipt | Release decision and artifact | Proposed only; no PocketCode delivery implementation established |

Do not map identities by similar names. In particular:
- `MissionId` is not automatically `task_id`, `job_id` or `attempt_id`.
- RevDev `RunId` is not automatically PocketCode `runId` or a provider operation token.
- PocketCode `runId` must not be assumed to be both coordinator job and execution attempt.
- A source provider event ID is not a globally unique event ID.
- Exact result identity/hash is not a mutable `LATEST_RESULT` pointer.
- Evidence ID, artifact ID, report version and transfer ID are different things.
- No identifier grants execution or release permission.

## 6. Native acceptance authorities remain distinct

| Product / suite | Native vocabulary or identity | What it proves / tests | Must not be relabelled as |
|---|---|---|---|
| PocketCode LOOP-01..14 | User-facing execution-loop requirements and verdict rules | Product-level loop behavior when actually accepted | RevDev P8U |
| PocketCode CASE-01..16 | Canonical synthetic scenarios; CASE-04 timeout semantics, CASE-13 ambiguous retry, CASE-16 out-of-order attempts | Specific PocketCode acceptance behavior | Shared SCF pass |
| PocketCode AEC / AWC | Separate additional acceptance/evaluation namespaces | Their own exact fixtures and assertions | LOOP/CASE or RevDev P8U |
| PocketCode COORD/DR and proposed supplemental labels | Coordinator/failure-injection research | Design/fake/persistence/provider gates according to proof level | Canonical acceptance unless explicitly adopted |
| Shared SCF-001..018 | Provisional shared semantic fixtures | Cross-project vocabulary and counterexamples | Native acceptance or schema approval |
| RevDev P8U-01..12 | RevDev execution/publication/recovery specification | Exact result preservation, publication retry and no rerun when implemented and run in required environment | PocketCode LOOP/CASE |
| RevDev P0-D items 1..10 | RevDev reliability hardening acceptance/planning | Original numbered reliability gates | New SCF or PocketCode cases |
| RevDev RelayRef | Parser/reference protocol and its own versioned tests | Only the exact tested reference implementation/environment | Windows/installed product acceptance |
| RevDev AWC-001..018 | AI Work Coach synthetic evaluation fixtures | Model/evaluation behavior for that distinct lane | P8U or PocketCode execution acceptance |

P8U's exact source vocabulary is:
- execution: NOT_RUN, RUNNING, PASS, FAIL;
- publication: NOT_ATTEMPTED, PENDING_RETRY, PUBLISHED, PERMANENT_ERROR;
- remediation: REPUBLISH_EXISTING, RECOVER_NO_LOCAL_TERMINAL_ONLY, ESCALATE_WITH_ORIGINAL_ERROR.

P8U is `SPEC_ONLY_NOT_IMPLEMENTED`. It is a useful native example of execution/publication separation, not proof of current RevDev runtime behavior. Current PC state remains UNKNOWN.

## 7. Owner decision dependencies

| Decision | Mapping affected | Current status | Stop rule |
|---|---|---|---|
| Lifecycle D-01 | Runtime timeout/limit and verdict projection | OPEN; CASE-04 INCOMPLETE/timed_out remains working default | Do not encode a different verdict |
| Lifecycle D-02 | Provider failure, execution UNKNOWN, provider-error disposition | Proposed default; OPEN | No invented child exit or FAIL |
| Lifecycle D-03 | Evidence completeness and per-case PASS gates | OPEN | No universal output/artifact completeness gate |
| Lifecycle D-04 | Source event identity, replay, ordering, immutable observations | OPEN | No frozen event envelope/reducer identity |
| D-05 | Applied policy revision before execution | BLOCKED | No execution-boundary security claim without actual enforceable barrier |
| D-06 | Reservation, provider token, dispatch intent and ambiguous-start recovery | Proposed; owner review required | No exactly-once or safe redispatch claim |
| D-07 | Artifact identity, quarantine, release authorization and transfer | Proposed; store/API unselected | No artifact release claim |
| D-08 | Durable report history, versions, tombstones and retention | Proposed; store unselected | No durable append/recovery claim |

The D-01..D-04 above are the lifecycle owner-decision namespace in `OWNER_DECISION_REGISTER_20261029.md`. Do not confuse them with the separate AI Workflow Director D-01..D-04 namespace.

## 8. Reviewer questions before schema work

### Claude — architecture and implementation feasibility

For each axis and identity, identify:
- exact authoritative producer and native source record;
- whether identity is generated by client, coordinator, host, provider, store or consumer;
- atomicity/idempotency boundary and crash window;
- what can be proved by pure helper, fake adapter, persistence, provider/host, HTTP/store and device tests;
- compatibility/migration risks for RevDev MissionId/RunId and PocketCode runId;
- the minimum cross-reference needed without renaming native fields.

### Gemini — security/spec adversarial review

For each axis and identity, attempt:
- false PASS from stale/missing/contradictory evidence;
- cross-tenant or cross-attempt identity substitution;
- replay with same source ID but changed immutable content;
- stale worker or delayed external call after takeover;
- cancel acknowledgement treated as termination;
- captured/published/released/received state forged from a weaker acknowledgement;
- artifact/report pointer substitution, stale release and transfer receipt forgery;
- information disclosure through identifiers, reports, logs or filenames.

Both reviewers should identify exact existing canonical IDs that cover each finding and avoid duplicate test namespaces. Disagreements must remain visible. “No issue found” is acceptable if justified.

## 9. Claude research availability check

At the current refreshed snapshot:
- the active PocketCode research branch contains the handoff, Gemini architecture audit, shared-contract readiness/crosswalk, 18-fixture catalogue, coordinator adversarial review and this preliminary fixture review;
- all eight listed PocketCode branches were enumerated;
- no dedicated medium-sized Claude research report was present in the active branch tree or other listed PocketCode branches;
- branch search for Claude-specific research returned no branch;
- the only matching Claude commit found by repository commit search adds `CLAUDE.md` entry instructions, not a research report.

Therefore Claude's promised research is still **NOT RECEIVED in the checked GitHub snapshot**. This is not a claim that Claude has not written it elsewhere or that it cannot arrive later. Do not synthesize or attribute recommendations to Claude.

## 10. Current evidence and non-actions

- This document is a static semantic mapping preparation aid.
- No schema, field name, enum, owner decision or canonical acceptance was frozen or changed.
- No source/test file, PR #2/#3, main branch, provider/store, account, workflow, Actions, workload, billing, deployment or merge was changed or exercised.
- No tests, provider integration, persistence, Windows/host, iOS/Safari or device run occurred.
- RevDev PC source, binary, runtime, watcher, queue and publication state remain UNKNOWN.
- Claude's medium-sized research report remains NOT RECEIVED in the checked repository snapshot; Gemini's existing research remains distinct from the requested SCF-specific independent review.


## 11. Source-review identity and persistence clarifications — 2026-11-01

This section adds source observations without freezing any PocketCode identity or state contract.

### 11.1 OpenHands identity domains observed in source

OpenHands EventLog uses several distinct concepts:
- EventID: event identity and duplicate detection;
- on-disk event sequence: stable file-order cursor that is not reused after a lost file;
- in-memory dense index: current readable collection position, which can differ from the disk sequence after gaps;
- parent_id: event-tree relationship;
- leaf_event_id: persisted active branch HEAD;
- ConversationLease generation: owner epoch for guarded persistence writes.

These must not be collapsed into one PocketCode event sequence, job ID, attempt ID, operation ID, or policy revision. The lease generation is not a provider idempotency key and does not fence external side effects by itself.

### 11.2 Happy identity domains observed in source

Happy client pairing distinguishes:
- QR pairing token (32-byte bearer input);
- handshakeId (subsequent handshake credential);
- ephemeral phone/daemon public keys and nonces;
- transcript hash and role MACs;
- derived deviceToken (returned only after mutual proof);
- deviceId (server/daemon-issued display identity).

Account linking uses a separate ephemeral public key to seal the account master secret. None of these should be mapped to a PocketCode job/run/attempt ID. Server-side handshake enforcement was not source-verified.

### 11.3 D-04 and D-05/D-06 review implications

- D-04 remains OPEN: event identity, authenticated source, replay/order, immutable evidence and gap semantics need an owner decision and conformance fixtures.
- D-05 remains BLOCKED: a storage lease does not prove the policy revision was atomically applied at execution start.
- D-06 remains owner-open: a generation-guarded disk write does not make an external provider request idempotent or resolve ambiguous-start recovery.
- Event append and active-HEAD snapshot writes in OpenHands are separate. Treat crash-between-writes as a proposed fault-injection case, not a reproduced defect.

### 11.4 Claude report receipt clarification

Section 9 above is a historical GitHub branch-presence check, not the current report-receipt status. Since that check, Claude's master OSS research report was supplied to ChatGPT in the conversation and its independent reconciliation was committed in CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md. Claude's Windows sandbox source-audit follow-up was also supplied in the conversation and integrated into WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md. The original raw master report itself is not currently asserted to be committed as a standalone repo file. Keep these three evidence artifacts distinct.
