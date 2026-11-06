# PocketCode execution evidence and recovery contract

**Date:** 2026-11-06  
**Status:** Design-stage implementation artifact. The projection helper and tests are isolated research deliverables, not integrated product code. This document is not a frozen public schema, provider decision, or change to canonical acceptance.

## 1. Scope and invariants

PocketCode owns the control-plane semantics that connect a user command to a bounded execution attempt, trusted observations, durable receipt, artifact publication, and user-mediated correction. A runtime/provider may execute the work, but its task ID or event history does not replace PocketCode's operation identity or receipt.

Preserve the identity chain:

**CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt**

- CommandId identifies the accepted logical command.
- EffectId identifies one intended externally observable effect and remains stable across reconciliation and delivery retries for that same effect.
- DispatchAttemptId identifies one actual dispatch attempt. Re-sending the same idempotent request as a transport retry keeps its original attempt identity. A genuinely new execution attempt gets a new DispatchAttemptId.
- ExecutionId is the identity assigned by the execution boundary, when available. It is not interchangeable with the command, dispatch attempt or provider task ID.
- ObservationSequence is assigned by the durable coordinator when an observation is accepted. It supplies deterministic per-attempt order.
- ResultReceipt is an immutable, versioned projection over accepted evidence. A later reconciliation creates a new receipt/report version; it does not silently rewrite a previously published receipt.

A changed source, input digest, entrypoint, runtime, resource limit or effective policy is a different semantic request. It must not reuse an old idempotency key as though it were the same request. Preserve prior attempts and evidence for comparison.

## 2. Evidence producers and exit types

Keep these facts separate. The producer labels below are semantic classes, not cryptographic proof. A real adapter must authenticate the producer and bind its observations to the authorized attempt before persisting them.

| Observation class | What it establishes | What it does not establish |
|---|---|---|
| Coordinator lifecycle | Accepted/queued/running/succeeded/program_failed/timed_out/cancelled/rejected/infrastructure_failed, according to the trusted coordinator | Child exit code, sandbox containment, cleanup or artifact release |
| Direct-child natural exit | The child process returned naturally with an integer code observed by a trusted wait/status mechanism | That the task succeeded, policy was enforced, cleanup completed, or artifact is releasable |
| Direct-child signal termination | The child was observed terminated by a signal, separate from natural exit | A natural exit code or automatically the cause of termination |
| Wrapper/supervisor exit | The wrapper or supervisor itself exited with a code | The child process exit code or program verdict |
| Embedded interpreter result | An in-process return value, Python exception, SystemExit request or bridge error | A native child-process exit status |
| Trusted runtime failure | A runtime boundary specifically confirmed a program/runtime failure | A complete child exit code if none was observed |
| Collection/transport | What bytes/events were observed, lost, truncated or delayed | Rewriting an independently observed child exit |

A wrapper's code 137 may represent a shell's signal convention, an application-selected exit value, or another wrapper condition. Preserve the raw wrapper code and a separate termination observation. Never infer that the child naturally exited 137. Preserve POSIX wait status as natural exit versus signal termination. For embedded Python, record SystemExit as a requested interpreter exit value, not as a child exit. Python 3.14 platform documentation says subprocess is unavailable on WebAssembly and iOS apps cannot use subprocesses, multiprocessing or IPC. Android subprocess support is officially unsupported. A Pyodide worker is a UI responsiveness mechanism, not a hostile-code sandbox or durable background worker.

## 3. Verdict projection matrix

The only valid product verdicts remain PASS, FAIL and INCOMPLETE. This table formalizes projection rules without changing LOOP or CASE acceptance text.

| Trusted evidence | Projection | Rule |
|---|---|---|
| Coordinator succeeded + natural direct-child exit 0 for the same attempt | PASS | Both facts must be trusted, attempt-bound, and non-contradictory |
| Coordinator program_failed, with no contradictory successful child result | FAIL | Failure classification is from the coordinator's authoritative lifecycle evidence, not a wrapper code |
| Natural direct-child nonzero exit, with no contradictory timeout/cancel/success state | FAIL | Retain the exact child code |
| Trusted runtime explicitly confirms program/runtime failure, with no contradictory lifecycle | FAIL | Keep the raw failure observation separately |
| timed_out, cancelled, rejected or infrastructure_failed | INCOMPLETE | These dispositions dominate numeric wrapper/child codes for verdict purposes |
| succeeded but child exit is missing, signal-only, wrapper-only, embedded SystemExit or exception-only | INCOMPLETE | Evidence is insufficient to assert native-child success |
| program_failed plus natural child exit 0, or succeeded plus natural child nonzero | INCOMPLETE | Contradiction requires reconciliation, not precedence |
| Nonterminal lifecycle plus a terminal-looking child observation | INCOMPLETE | Reconcile stale/out-of-order/contradictory event history |
| Attempt mismatch, malformed field, untrusted event, unknown status or missing terminal evidence | INCOMPLETE | Fail closed |

CASE-04 is unchanged: trusted timeout remains INCOMPLETE / timed_out. A UI timeout, lost connection, cancellation request, wrapper code, or request to kill is not proof that the worker stopped. The terminal timeout observation must come from the trusted execution-control boundary. A cancellation acknowledgement while work remains active must remain a requested cancellation, not termination-confirmed.

## 4. Projection helper delivered in this pass

New files:
- scripts/execution_projection.py
- scripts/test_execution_projection.py

The helper accepts three typed observations: lifecycle, exit and confirmed program failure. It binds each to one expected attempt and requires positive non-boolean sequence numbers. It distinguishes natural child exit, signal termination, wrapper exit, embedded SystemExit and embedded exceptions. The verdict is a pure projection.

Explicit limitations: checking the producer class string is not authentication. The caller must verify event signature/transport identity or trusted in-process boundary, authorize attempt/tenant, enforce sequence rules and deduplicate before the helper is called. The helper does not persist events, prove a kill, verify resource isolation, inspect output, verify artifacts, or authorize release. It is not imported by report_contract.py. Do not pass its verdict into production UI until the authenticated coordinator contract exists.

## 5. Dispatch and ambiguous acknowledgement recovery

Use a durable reservation/outbox around dispatch. Store the normalized semantic request, exact source/input digests, policy revision, stable EffectId, DispatchAttemptId, serialized provider request fingerprint and provider idempotency metadata before the external call.

1. Atomically reserve the intended effect and append dispatch_intent in one local transaction.
2. Submit using the exact persisted request body and stable provider idempotency token, if the target API documents one.
3. Persist acknowledgement and provider execution reference as a new observation.
4. If acknowledgement is lost or transport outcome is ambiguous, mark the attempt RECONCILING and query the same provider resource/attempt. Do not allocate a new attempt or resend with a new token.
5. Adopt only a result whose tenant/account, endpoint, request fingerprint, EffectId/attempt correlation and provider resource identity match.
6. If lookup is absent, stale, eventually consistent, outside retention, or otherwise non-authoritative, remain UNKNOWN/INCOMPLETE. Not found is not proof that no execution occurred unless the API contract expressly makes it authoritative for that exact scope and time.
7. Only dispatch a new attempt when authoritative evidence shows the prior effect was not accepted/started, or a documented provider idempotency contract safely deduplicates the exact same request. A changed request is a new EffectId and new attempt.

A provider idempotency record must pin: provider and API/version, endpoint/operation, authenticated account/tenant, region/zone if relevant, key, semantic payload fingerprint, provider retention window, lookup consistency/authority, and mismatch behavior. AWS EC2 documents region/zonal token scope and rejects reuse with mismatched parameters. Google AIP-155 allows an API to define how long it honors request IDs. Do not generalize either promise across providers.

A transactional outbox can atomically persist local state and intent to notify a dispatcher. Delivery can still be at-least-once, so the receiver needs deduplication/idempotent handling. Temporal's Activity model is explicitly at-least-once in ordinary failure cases; a worker can complete the side effect and crash before acknowledging completion. The correct portable design is reconciliation and idempotent effects, not an exactly-once claim.

## 6. Event history and projection

Accepted evidence is append-only. One coordinator append function allocates internal EventId and ObservationSequence, validates the attempt binding, and persists raw event bytes plus their digest before updating derived projections.

Retain both:
- event_id: PocketCode's internal unique ID for the accepted canonical event.
- (source, source_event_id): producer's original identity, retained as a namespace.

CloudEvents requires source plus ID to be unique within the producer's scope. It does not make a provider ID globally unique. An identical retransmission from the same source can be deduplicated. Reuse of the same source/ID with changed payload is a conflict to quarantine, not an overwrite.

Record source occurrence time and PocketCode observation time separately. Source Timestamp describes when the producer says an event occurred; ObservedTimestamp describes when the collector observed it. Neither replaces the durable per-attempt sequence. Do not sort events solely by client wall clock or provider timestamps. Reject or quarantine wrong-attempt, wrong-tenant, invalid-policy, stale-fence, malformed-sequence and conflicting-ID events.

Read models and UI progress are rebuildable projections from the event log. A provider's task history, an A2A stream, an MCP task handle or a UI cache is not the authoritative receipt. A disconnected stream may miss updates; reconnect by querying authoritative task state and reconciling, then append recovered evidence without mutating old events.

## 7. Receipt and artifact integrity

Keep these independent:
1. execution outcome;
2. observation completeness/collection health;
3. lifecycle disposition;
4. cleanup/teardown status;
5. artifact write completion and exact-byte integrity;
6. authorization/quarantine/release decision;
7. publication/share/copy result;
8. derived report and final acceptance.

A receipt records attempt identity, contract version, ordered evidence references, raw observation digests, status projection, uncertainty/contradictions, and artifact manifest. A later observation produces a new version with a reason and link to its predecessor. It must not replace historical bytes or change the earlier receipt silently.

For each artifact record safe logical name, size, media type, immutable object/version reference, exact-byte digest, producing attempt, write completion, integrity verification, quarantine, authorization and release observations. A partial write or digest mismatch is quarantined. Revalidate exact bytes and current authorization immediately before every download/share. A successful execution is not permission to release an artifact forever. A report-copy failure should retry publication/copy of the same receipt, not rerun the task.

A digest establishes byte identity/integrity relative to the recorded digest, not producer authenticity, execution correctness, malware safety or authorization. in-toto statement/envelope ideas can inform a future signed receipt, but unsigned JSON is not an authenticated attestation. Before signing, define producer identity, signing keys, key custody, rotation, revocation, verifier policy and trust roots. SLSA build provenance applies to trusted builds of PocketCode itself, not arbitrary user scripts.

## 8. Mobile lifecycle and runtime boundaries

Keep evidence type specific to the execution model:

| Model | Valid terminal evidence | Important limit |
|---|---|---|
| Embedded iOS Python | Host-observed return/exception/SystemExit request and app-owned persistence observations | No subprocess/multiprocessing/IPC; no native child exit to report |
| Pyodide in browser/WebView | Worker message and host-observed worker state, with explicit cancellation/termination observation if supported | Worker is not process-level containment or guaranteed after app termination |
| Android embedded Python | Host-observed in-process outcome | Subprocesses officially unsupported by Python mobile docs |
| Native/external child process | Trusted OS wait status: natural exit vs signal termination | Requires real child process and authoritative supervisor |
| Remote runner | Authenticated provider/supervisor task state, child observation if exposed, and cleanup receipt | Provider task ID is not PocketCode identity; APIs may have delayed/eventually consistent state |

Persist durable intent and progress before leaving the foreground. App lifecycle callbacks are a chance to checkpoint/flush, not a guarantee that arbitrary execution will finish in background. On app resume, reconstruct UI from durable events and reconcile in-flight attempts with their original IDs. Never equate app suspension, worker disappearance, browser timeout or lost connection with child termination.

## 9. Open-source reuse and license/maintenance review

These are pattern references, not new product dependencies.

| Project | Latest source inspected in this pass | License verified | Reuse decision |
|---|---|---|---|
| OpenHands software-agent-sdk | v1.60.1, published 2026-11-05 | MIT | Event append chokepoint, parent/sequence history, rebuildable projections, explicit persistence configuration. Not exactly-once or power-loss guarantee. |
| Cline | v4.1.26, published 2026-10-26 | Apache-2.0 | Task history, interruption resume, shadow-Git source snapshots, compare/restore. Snapshot is workspace state, not execution evidence. |
| Temporal Python SDK | 1.35.0, published 2026-10-28 | MIT | Treat external Activities as at-least-once and build idempotency/reconciliation. Workflow service and infrastructure are beyond $0 MVP assumptions. |
| MCP Tasks | 2025-11-25 extension baseline; experimental | Apache-2.0 | Adapter-level task handle/status/polling only. Not PocketCode identity or receipt. |
| CloudEvents | Core spec | Specification | Source-scoped ID deduplication semantics, not global identity. |
| OpenTelemetry Logs | Current data model | Specification | Separate source and observation timestamps; do not order by wall clock. |

No OpenHands, Cline or Temporal dependency/code was added to product runtime. The repository's existing isolated OpenHands atomic-write reference has an fsynced temporary file and atomic replace, but no parent-directory fsync, multi-writer lock, append-only journal or crash/power-loss proof. It is not a database or complete receipt store. The existing capability-gated OpenHands retry sample is research-only and was not tested in this pass. Retain upstream license/attribution when copying any code later.

## 10. Regression matrix for the next implementation boundary

### Pure projection
- Timed out + wrapper exit 137 → INCOMPLETE, child exit unavailable.
- Timed out + direct-child observation after timeout → preserve event; verdict remains INCOMPLETE pending lifecycle reconciliation.
- Succeeded + child natural zero → PASS only when authenticated coordinator lifecycle and direct child observation match attempt.
- Succeeded + missing child observation, embedded SystemExit 0 or wrapper zero → INCOMPLETE.
- Program_failed + child natural zero → INCOMPLETE conflict.
- Succeeded + child nonzero → INCOMPLETE conflict.
- Program_failed + direct natural nonzero → FAIL.
- Signal termination → retain signal separately, not child exit integer.
- Wrong/stale attempt, producer spoof, reused source event ID with changed payload, malformed bool-as-int, unknown state → reject/quarantine or INCOMPLETE.

### Dispatch/persistence fake adapter
- Crash before reservation.
- Crash after reservation before dispatch.
- Provider accepted request but acknowledgement lost.
- Provider lookup returns exact same attempt/resource.
- Lookup says not found while provider consistency is eventually consistent.
- Same idempotency key with different request fingerprint.
- Duplicate outbox delivery.
- Crash after side effect before local completion acknowledgement.
- New correction attempt while prior execution remains unresolved.
- Stale lease/fencing token attempts to append a terminal event.

### Artifacts and lifecycle
- Child exits zero, then collector fails or truncates.
- Child exits zero, then provider teardown times out or returns an ambiguous error.
- Artifact partial write, changed bytes, mismatched digest, wrong attempt, stale authorization, quarantine and failed copy/share.
- Mobile app suspends during embedded execution, after execution but before receipt commit, and during export.
- Reconnect finds provider task active, complete, absent or unqueryable.
- Every case preserves raw facts and separates execution from cleanup, publication and release.

A fake adapter validates deterministic orchestration only. Persistence/crash tests must run against the selected store; provider isolation, egress, child termination and cleanup require actual provider/runtime evidence. Do not claim higher-layer proof from lower-layer tests.

## 11. Primary-source register

- Python 3.14 platform constraints: https://docs.python.org/3.14/library/intro.html
- Python subprocess return-code semantics: https://docs.python.org/3.14/library/subprocess.html
- Python SystemExit: https://docs.python.org/3.14/library/exceptions.html#SystemExit
- Bash signal exit convention: https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html
- Linux wait status: https://man7.org/linux/man-pages/man2/wait.2.html
- Google AIP-155: https://google.aip.dev/155
- AWS EC2 client tokens: https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html
- AWS transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Temporal Activity execution: https://docs.temporal.io/develop/python/failure-detection
- CloudEvents core spec: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- Apple background lifecycle: https://developer.apple.com/documentation/uikit/about-the-background-execution-sequence
- Pyodide Web Worker guide: https://pyodide.org/en/stable/usage/webworker.html
- OpenHands: https://github.com/OpenHands/software-agent-sdk
- Cline: https://github.com/cline/cline
- in-toto Statement v1: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
- SLSA provenance v1.2: https://slsa.dev/spec/v1.2/provenance

## 12. Verification boundary

VERIFIED: exact PocketCode source/spec/test files inspected at branch HEAD f545974e5d76c8282968c3a86ae69d22cad81343; standalone projection helper compiled and its isolated 31-case test suite passed under CPython 3.13.5; relevant primary docs and upstream LICENSE/latest-release metadata inspected.

INFERRED: provider-neutral orchestration/recovery is a stronger PocketCode product differentiator than building a generic phone Python editor; local outbox plus attempt-bound event log is the best architecture direction to investigate.

UNKNOWN: authenticated producer channels, durable store, runtime/provider, actual cancellation/termination semantics, mobile forced-termination durability, provider idempotency windows, owner Pyodios bridge root cause.

NOT RUN: exact repository unittest suite, GitHub Actions for this branch, iOS/Android UI or lifecycle acceptance, fake-provider orchestration integration, actual process/host isolation, network-egress, artifact-release boundary, device crash/power-loss tests.

No canonical LOOP/CASE/D identifier, product runtime/provider selection, budget, PR, merge, deployment or release decision is changed by this document.


## 13. Ambiguous dispatch decision helper prototype

New research-only files:
- scripts/dispatch_reconciliation.py
- scripts/test_dispatch_reconciliation.py

This pure helper does not send requests, create IDs, persist an outbox, or claim exactly-once execution. It selects a safe action for a caller that already has the original persisted dispatch context.

| Situation | Decision |
|---|---|
| Reserved locally, no first send happened | dispatch_first |
| Provider acknowledgement already recorded or attempt is running | poll_existing |
| Attempt is terminal | do_not_replay |
| Authoritative provider lookup returns exact matching effect, attempt, request fingerprint, endpoint, account, token, provider, API version and region | adopt_existing |
| Authoritative lookup returns non-acceptance for that exact scope and attempt | retry_same_attempt |
| Exact documented idempotency contract matches endpoint, account, provider, API version, region, token, fingerprint, active retention, same-request deduplication and parameter-mismatch rejection | retry_same_attempt |
| Lookup is unknown/non-authoritative, token contract is absent or out of retention | hold_unknown |
| Authoritative lookup conflicts with expected effect, attempt or scope | conflict |

The provider token is optional for lookup-based reconciliation. It is required for token-based replay. A same-scope authoritative lookup is still required before an absent result may be used to retry. A non-authoritative "found" or "not found" response cannot cause adoption or redispatch.

The original 28-case suite validated the first decision-kernel version only. The red-team-expanded 33-case suite additionally covers tokenless result metadata, malformed context, and eventually consistent absence. It does not validate provider response authentication, actual provider consistency, request-body storage, transactional atomicity, retry timing, race/fencing behavior or durable state transitions. Do not wire this helper to a live provider until those mechanisms exist and have separate tests.


## 15. Provider absence and idempotency are distinct proofs

A provider lookup returning "not found" is not, by itself, proof that a prior request was never accepted. The lookup may be eventually consistent, scoped differently from the mutation, or omit in-flight/partially accepted work. The dispatch helper now models absence_final separately from authoritative: only an adapter that has verified the provider's documented final-absence semantics for the exact operation, endpoint, account, region/zone, attempt and request may set it true. Otherwise the safe decision is hold_unknown.

Likewise, an idempotency contract is not one generic boolean. It must be pinned per provider API operation and version, including the exact key scope, request-parameter comparison, concurrency behavior, when the provider begins retaining a result, and retention/pruning behavior. Provider API versions can have materially different semantics. For example, Stripe's current documentation distinguishes API v1 (replay of the first saved status/body, including 500, with keys eligible for pruning after at least 24 hours) from API v2 (different retry behavior for successful versus failed/partially failed operations). This is why the model includes provider and API version and why adapter-specific contract tests are mandatory.

The authoritative, absence_final, and idempotency-contract fields are not cryptographic proofs. They are claims made by the trusted adapter after authentication and source verification. The current pure helper cannot authenticate them and must not be exposed as an authorization boundary.


## 16. Malformed provider lookup input

The dispatch decision helper also rejects non-string lookup outcomes before membership tests. A malformed lookup outcome such as a list must resolve to hold_unknown, not raise an exception. Non-string dispatch state similarly resolves to conflict. These are defensive shape checks only; authenticated provenance remains an adapter responsibility.
