# Lifecycle, termination and receipt acceptance contract

Date: 2026-11-12
Status: acceptance contract addendum; not implemented, not a canonical specification amendment.
Scope: evidence projection across coordinator lifecycle, child/wrapper/interpreter observations, termination, cleanup, collection and receipt publication.
Authority: preserve PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md, LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13 without modification.

## 1. Ranked gap and verified implementation boundary

Rank 4 for this pass: a report must not convert a wrapper code, timeout signal, embedded Python exception or missing termination acknowledgement into a confident program verdict. It must preserve the raw evidence and separately resolve execution, job/evidence and artifact disposition.

VERIFIED from active-branch code:
- scripts/execution_projection.py is a pure helper. Its module docstring requires callers to authenticate producers, authorize attempts, deduplicate events, validate policy and persist observations before projection.
- It binds typed lifecycle, exit and program-failure observations to one attempt and requires coordinator lifecycle plus direct-child natural exit for PASS.
- It treats wrapper exit, signal termination, embedded SystemExit and embedded exception as distinct observations, not child natural exit.
- scripts/report_contract.py is a pure formatter. Its classify_verdict() currently checks any integer nonzero exit first and returns FAIL before considering timeout/cancelled/infrastructure lifecycle. Therefore a timeout status combined with wrapper code 137 can become FAIL. The formatter explicitly says it does not verify the trustworthiness of input.
- scripts/result_receipts.py is an in-memory store and its Receipt model already separates execution_outcome, collection_state, lifecycle_disposition, cleanup_state, evidence references, artifacts and uncertainty. It is not durable or an authenticated release service.
- AI_COLLAB/EXIT_PROVENANCE_RESOLUTION_20261108.md already records the formatter compatibility limitation and prohibits a precedence-only patch. This document adds an acceptance crosswalk; it does not replace that earlier resolution.

## 2. Evidence identity and authority

Preserve the existing identity chain:
CommandId -> EffectId -> DispatchAttemptId -> ExecutionId -> ObservationSequence -> ResultReceiptId + immutable revision.

These identities are different:
- CommandId is the accepted logical user command.
- EffectId is one intended externally observable effect.
- DispatchAttemptId is one authorized dispatch attempt.
- ExecutionId identifies the actual execution instance when the boundary supplies one.
- ObservationSequence is coordinator-assigned accepted evidence order.
- ResultReceiptId and revision identify an immutable projection snapshot.
- PublicationAttemptId identifies copying/sharing a receipt; it is not execution or artifact identity.

Authority rules:
- Only an authenticated coordinator may author lifecycle transitions.
- A direct-child natural exit requires a trusted wait/status source bound to the exact ExecutionId and DispatchAttemptId.
- A wrapper/supervisor exit is a separate fact and cannot substitute for child exit.
- An embedded interpreter result is a task observation, not a native child wait status.
- A provider or worker message is not authoritative merely because its schema is typed. The adapter must authenticate its producer and bind it to tenant, effect, attempt, execution, policy and fence before persistence.
- Sequence is the accepted observation order. Caller timestamps are metadata and must not reorder the event stream.
- A missing producer proof, identity binding, policy barrier, sequence or required collection result is UNKNOWN/INCOMPLETE, not PASS or FAIL by inference.

## 3. Separate raw facts and projections

The system must retain all raw observations and compute at least three distinct projections.

| Projection | Inputs | May establish | Must not establish |
|---|---|---|---|
| Execution evidence/verdict | trusted coordinator lifecycle, direct-child natural wait, typed runtime failure, contradictions | whether the exact execution has sufficient evidence for PASS/FAIL/INCOMPLETE | artifact collection, cleanup, transfer or client receipt |
| Overall job/evidence disposition | execution projection, policy/egress barriers, observation completeness, wrapper/supervisor, collection and cleanup | whether the requested operation is complete and safe to report | rewriting raw child or wrapper observations |
| Artifact disposition | exact staged bytes, parent read-back digest, receipt binding, quarantine, current authorization and release evidence | whether an exact immutable artifact may be offered/released | program correctness, child exit or client acknowledgement |

Retain the raw event, producer class, source identity, signature/adapter verification result, attempt and execution binding, ObservationSequence, source occurrence time, coordinator observation time and exact payload digest. A projection is a deterministic view, not a replacement for those facts.

## 4. Typed observation rules

Lifecycle:
- accepted, queued and running are non-terminal.
- succeeded and program_failed are coordinator-resolved terminal program states.
- timed_out, cancelled, rejected and infrastructure_failed are non-success terminal dispositions. They do not become child exit codes.
- A late event after a terminal disposition must be reconciled against the same attempt and sequence. It cannot silently rewrite terminal history.

Natural child exit:
- Requires a trusted direct_child_wait or provider_child_wait observation bound to the exact attempt and ExecutionId.
- Stores a natural integer exit code. A zero code is only one prerequisite for success; it is not proof of policy compliance, artifact integrity, cleanup or client receipt.
- A signal-terminated observation stores signal/cause separately and has no natural exit_code.
- Never translate a shell convention such as 128+signal into a natural child exit.

Wrapper/supervisor:
- Store wrapper exit separately with its own producer, execution binding and sequence.
- Wrapper exit zero with missing child wait is INCOMPLETE.
- Wrapper exit nonzero does not prove child program failure.
- Wrapper/supervisor cleanup or collection failure can make the overall job/artifact INCOMPLETE even when a natural child exit zero is proven.

Embedded interpreter:
- Store Python exception, SystemExit request, bridge failure and host-observed return as interpreter observations.
- Never put an embedded SystemExit request in the native child exit_code field.
- Pyodide worker messages or app UI errors do not prove native process termination. When there is no OS child process, record the execution model and report task completion only at the strength the host can verify.

Termination and cleanup:
- Record request_sent, controller_action, same-attempt termination_acknowledged and observation source as separate facts.
- For the opaque-origin browser Worker protocol, `worker_termination_action_acknowledged` means only that the trusted supervisor invoked `terminate()` on its exact Worker and closed the task channel. It is a controller-action acknowledgement, not by itself the broader `termination_acknowledged` required by OD-12. Keep both facts separate; only an execution-model-specific, independently accepted authority rule may promote the narrower action fact to the termination/cleanup evidence needed for release.
- A request to cancel/kill, timeout event, disconnect, process signal request, wrapper exit or iframe removal is not termination acknowledgement.
- Confirmation must bind DispatchAttemptId and ExecutionId and come from the authoritative process/transport controller for that execution model.
- Missing, late, contradictory, wrong-attempt or unauthenticated acknowledgement leaves termination UNKNOWN and cleanup UNKNOWN. Artifact release stays blocked where containment/cleanup is required.
- A child may have stopped while the acknowledgement was lost. The correct result is UNKNOWN until reconciled, not a guessed FAIL or PASS.

## 5. Verdict and disposition mapping

| Accepted evidence | Execution evidence result | Overall job/evidence disposition |
|---|---|---|
| Coordinator succeeded + direct-child natural exit 0 + required security barrier verified + no contradiction | PASS candidate | COMPLETE only if collection and required cleanup are also complete |
| Coordinator program_failed + trusted natural nonzero child exit, no contradictory success | FAIL | COMPLETE evidence only if collection/cleanup are complete; otherwise INCOMPLETE overall |
| Trusted runtime confirms program failure without a native child exit, under an approved runtime contract | FAIL candidate | Depends on collection, barrier and lifecycle completeness |
| timed_out, cancelled, rejected or infrastructure_failed | INCOMPLETE | INCOMPLETE |
| Wrapper exits 0, child wait missing | INCOMPLETE | INCOMPLETE |
| Wrapper reports 137/143 after timeout or signal request | INCOMPLETE unless an independent trusted natural child result exists | INCOMPLETE |
| Child natural exit 0 but required policy/egress barrier is missing, mismatched or unverified | INCOMPLETE for product acceptance; preserve raw child exit 0 | INCOMPLETE; artifact blocked/quarantined |
| Coordinator succeeded but child exit is absent, signal-only, wrapper-only or embedded-only | INCOMPLETE | INCOMPLETE |
| succeeded + natural child nonzero, or program_failed + natural child zero | INCOMPLETE contradiction | INCOMPLETE; reconcile, do not choose precedence |
| Execution PASS candidate but required collection/integrity/cleanup is unknown | preserve execution facts; overall acceptance not PASS | INCOMPLETE |
| Artifact has correct bytes but current policy/receipt binding is missing | execution facts unchanged | artifact blocked; job cannot claim releasable result |
| Server emitted bytes without exact client acknowledgement | execution/artifact facts unchanged | transport_emitted only; not client_received |

OD-09..OD-13 remain controlling policy. Keep child execution evidence, overall job disposition and artifact disposition separate, but do not show a public PASS for a run whose required security barrier is missing.

## 6. Receipt snapshot and publication contract

An immutable ResultReceipt revision must bind:
- ResultReceiptId, revision, predecessor receipt and revision reason.
- CommandId, EffectId, DispatchAttemptId and ExecutionId where known.
- Exact accepted ObservationSequence high-water and immutable evidence references/digests.
- Resolved execution result/reason, overall lifecycle disposition, collection state, cleanup state and explicit uncertainties.
- Artifact manifest with ArtifactId, immutable object version, byte length, SHA-256, exact attempt binding, integrity and quarantine state.
- Policy/egress barrier references and their verification result.
- The receipt's own canonical bytes and digest, with a versioned contract schema.

Receipt update rules:
- A new accepted observation creates a new immutable receipt revision when it changes the projection.
- Same revision key and same canonical content returns the same receipt; same key with changed content conflicts.
- Never mutate an earlier receipt to hide uncertainty or contradiction.
- A renderer consumes the already-resolved projection and displays raw facts; it must not authenticate, repair or reclassify them.
- A receipt does not itself authorize artifact release. New download/share requires the latest receipt head, fresh policy and the exact artifact/object version under OD-02..OD-08.
- Report publication/copy has a separate PublicationAttemptId and retries the same receipt; it never reruns execution.

## 7. Current implementation defects and prohibited shortcut

VERIFIED current code issue: report_contract.classify_verdict() evaluates a nonzero exit code before timeout/cancelled lifecycle. A caller that passes wrapper code 137 for a timed_out execution can receive FAIL. This contradicts the typed projection contract where timeout is INCOMPLETE and wrapper exit is not child exit.

Do not patch this by swapping two if-statements or changing only verdict precedence. That would still leave the formatter's raw input unauthenticated and unable to distinguish:
- natural child nonzero exit from wrapper exit;
- signal termination from natural exit;
- embedded SystemExit from OS child exit;
- missing termination acknowledgement from actual termination;
- execution verdict from collection/cleanup/artifact disposition.

Required future change after an implementation gate:
1. Define a versioned report input containing a typed, already-authenticated, coordinator-resolved projection plus preserved raw observations.
2. Make the formatter a pure renderer of that projection. It must never accept caller-supplied arbitrary verdict as authority.
3. Add migration/compatibility tests proving legacy format remains bounded and does not silently reinterpret old reports.
4. Test contradiction and timeout precedence from typed provenance, not a bare integer exit code.
5. Keep the legacy two-field report contract unchanged until this versioned contract is reviewed and authorized.

## 8. Acceptance matrix for CASE-04 and adjacent evidence

| Scenario | Required result |
|---|---|
| Timeout requested, no authoritative same-attempt acknowledgement | INCOMPLETE / timed_out; termination UNKNOWN |
| Same-attempt controller acknowledges termination and cleanup | Preserve request + ack + cleanup facts; still require all other CASE criteria |
| Acknowledgement belongs to another attempt or ExecutionId | Reject; target attempt remains UNKNOWN |
| Wrapper exits 0 without child natural wait | INCOMPLETE |
| Wrapper exits 137 after timeout | INCOMPLETE; no inferred natural child code |
| Direct child naturally exits 137 while coordinator confirms succeeded | Contradiction/INCOMPLETE unless the execution contract explicitly makes 137 a natural program exit; do not infer signal |
| Direct child signal-terminated | Preserve signal; no natural exit code |
| Python raises exception inside same interpreter | Interpreter failure observation; not native child exit |
| Python calls SystemExit(0) inside embedded runtime | Embedded request; not OS child exit |
| Pyodide worker posts success then disappears | Task-reported result only; no native child exit or termination proof |
| Coordinator and child evidence contradict | INCOMPLETE and preserve both facts |
| Required policy/egress barrier absent or mismatched | INCOMPLETE; artifact blocked/quarantined |
| Child natural success, collector truncates output | Child fact retained; overall disposition INCOMPLETE |
| Cleanup is required but acknowledgement missing | Cleanup UNKNOWN; block release where containment requires it |
| Artifact digest differs on read-back | Quarantine artifact; no release |
| Client has not acknowledged exact artifact digest/object/range | Do not claim client-confirmed receipt |
| Late terminal event arrives after receipt creation | Append/reconcile; create successor receipt, never rewrite old receipt |

No CASE ID, LOOP ID, OD decision or verdict vocabulary is changed here. These cases refine evidence requirements; they do not declare CASE-04 passed.

## 9. Research, reuse and source boundary

Primary source set opened/re-read 2026-11-12:
- scripts/execution_projection.py: typed pure projection; explicitly not an authenticated coordinator.
- scripts/report_contract.py: pure formatter with caller-supplied evidence and existing nonzero-code precedence defect.
- scripts/result_receipts.py: immutable receipt and artifact model; in-memory only.
- AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md and AI_COLLAB/EXIT_PROVENANCE_RESOLUTION_20261108.md: current design and previous formatter red-team.
- AI_COLLAB/P39_OWNER_DELEGATED_DECISIONS_20261111.md: OD-09..OD-13 and CASE-04 guard.
- WHATWG/MDN/Pyodide references in OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md: browser Worker completion is not native child wait evidence.

Reuse decision: reuse current typed projection vocabulary and immutable receipt fields as design inputs. Do not copy a new framework, runtime, executor, provider or reporting library. No test code or application code changed.

## 10. Red-team corrections

1. Prior report code could turn timeout plus wrapper 137 into FAIL because nonzero exit is checked first. Fix: status/producer typing must be resolved before projection; this is documented as a prohibited shortcut, not silently patched.
2. Prior typed projection could be misread as authenticated because producer class strings are validated. Fix: producer authentication and attempt authorization must happen before this pure helper.
3. Prior receipts held execution outcome and cleanup/collection fields, but the renderer and persisted production authority were not integrated. Fix: separate three projections and bind the receipt to accepted evidence high-water.
4. Browser Worker completion could be mistaken for native child exit. Fix: browser task-reported completion stays distinct; no synthetic exit code.
5. Server-side export/transport progress could be mistaken for client receipt. Fix: OD-13's exact digest/object/range client acknowledgement is required for client-confirmed wording.

## 11. Gate and evidence boundary

VERIFIED: the cited PocketCode source and contract files were read from the active branch on 2026-11-12.
INFERRED: the acceptance matrix is a conservative bridge between OD-09..OD-13 and existing typed projection/receipt models.
UNKNOWN: production producer authentication, coordinator authority, process/worker topology, current report-contract integration, durable receipt adapter and actual same-attempt termination acknowledgements.
NOT RUN: lifecycle integration, formatter migration, crash/restart, device or production adapter tests.

No implementation, test, deployment or stack choice is authorized by this document. P39 implementation/adapter gate remains CLOSED. CASE-04 remains INCOMPLETE / timed_out.
