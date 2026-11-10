# P40 model-only execution protocol
**Source-pinned revision:** 2026-11-11  
**Status:** PREPARED / NOT AUTHORIZED / NOT RUN  
**Target branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Authority:** P39 consensus, OD-01..OD-13, canonical LOOP-01..14 and CASE-01..16. This document does not authorize implementation, source/test edits, schema freeze, adapter selection, device tests, deployment, spending or canonical ID changes.

## 1. What this protocol tests, and what it cannot test

The current repository has five distinct in-memory/pure models. They are not interchangeable:
- `ReleaseGrantContractModel`: receipt-head CAS, release-grant reservation, grant event/outbox and transfer-worker progress.
- `FakeOutboxStore`: effect reservation, external dispatch intent, worker lease/fence and ambiguous provider reconciliation.
- `EventJournal`: append-only event evidence and local fencing.
- `ResultReceiptStore`: artifact/receipt revisions and caller-supplied release authorization snapshots.
- `project_verdict()`: pure projection of typed coordinator lifecycle and child-exit observations.

A passing test proves only the tested model behavior. It does not prove database atomicity, cryptographic producer authentication, cross-process fencing, crash durability, browser origin isolation, IndexedDB/OPFS persistence, transport cancellation or client acknowledgement.

P39/P40 implementation gate is CLOSED. This sequence is a preparation artifact only. Do not run or edit tests until the owner gate is explicitly cleared and a bounded run is authorized.

## 2. Required run pins and evidence rules

Before an authorized run, record repository, branch, exact source SHA, test SHA, blob SHAs, Python version, OS, command and test runner. Record the relevant OD decisions or explicit deferrals. Use the existing IDs and test families. Every case records initial state, operation, injected fault, final state and exact output. Assertions must fail if their preconditions are absent; empty collections or skipped branches cannot satisfy security assertions.

Tag evidence VERIFIED, INFERRED or UNKNOWN. Record PASS, FAIL or NOT RUN. Keep model, adapter, browser/device and canonical product outcomes separate.

## 3. Ordered model lanes

### Lane 1: release-grant transaction and aggregate parity

**Source:** `scripts/release_grant_conformance.py`  
**Tests:** `scripts/test_release_grant_conformance.py`  
**Existing methods:** `test_crash_after_staged_grant_leaves_no_partial_state`, `test_crash_after_staged_event_leaves_no_partial_state`, `test_crash_before_commit_leaves_no_partial_state`, `test_successful_commit_lost_response_replays_original_grant`, `test_grant_commit_wins_then_successor_keeps_grant_pinned`, `test_successor_commit_wins_then_old_receipt_grant_is_denied`, `test_only_one_successor_from_same_predecessor_can_win`.

Sequence:
1. Seed receipt head revision N. Reserve one exact release intent; assert one immutable grant, one v1 event, one outbox item and a pinned object version.
2. Inject each existing pre-commit failure point. Assert grant/event/outbox/fence/sequence state remains unchanged.
3. Simulate committed response loss; replay same tenant/principal/request key and same intent; assert the original grant and provenance are returned.
4. Race the two sequential CAS orderings: grant first then successor, and successor first then stale grant. Assert only the selected linearization order wins.
5. Add a gated assertion for equal-progress replay. Current `record_progress()` increments aggregate_version even when progress_bytes is unchanged. The intended no-op rule therefore is not satisfied by the current model. The current test suite does not cover this case.
6. Assert every aggregate version transition has exactly one matching immutable event/outbox item. Current `record_progress()` advances aggregate_version without appending a matching event/outbox record. Mark parity FAIL if the existing model is run against this requirement.

**Stop condition:** this lane exposes known model gaps. Do not silently weaken the expected parity rule to make the model pass.

### Lane 2: grant-event consumer integrity

**Existing methods:** `test_consumer_deduplicates_same_source_event_id`, `test_consumer_rejects_same_event_identity_with_changed_payload`, `test_consumer_defers_future_event_until_predecessor_arrives`, `test_consumer_does_not_mark_future_event_consumed_when_predecessor_is_missing`.

Sequence:
1. Deliver the original event twice; assert the second is duplicate.
2. Reuse an already accepted source/event identity with a changed digest; assert conflict.
3. Deliver version N+2 before N+1; assert `deferred_gap` and no consumed-version advance; then deliver predecessor and retry.
4. Record that these tests do not prove first-delivery authentication, digest recomputation or tenant/grant/source binding.

**BLOCKED assertions:** forged first delivery; altered semantic fields with retained digest; unknown grant; wrong tenant/source; producer spoofing. The current `GrantEvent` contains only a supplied digest, not canonical payload bytes, and `consume_event()` accepts a next-version first delivery without authenticating producer or validating grant scope. A meaningful test requires an owner-approved canonical envelope and trusted ingress contract. Do not invent either.

### Lane 3: effect-dispatch outbox recovery

**Source:** `scripts/fake_outbox.py`  
**Tests:** `scripts/test_fake_outbox.py`  
**Existing methods:** `test_reservation_and_outbox_intent_are_created_together`, `test_crash_before_commit_leaves_no_partial_reservation_or_sequence`, `test_crash_before_send_can_be_reclaimed`, `test_active_lease_cannot_be_stolen`, `test_stale_worker_is_fenced_after_reclaim`, `test_crash_after_dispatch_intent_requires_reconciliation`, `test_lost_ack_found_reconciles_without_second_dispatch`, `test_eventually_consistent_not_found_holds_unknown`, `test_final_exact_absence_allows_same_attempt_retry`, `test_duplicate_delivery_is_deduplicated`.

Sequence:
1. Verify reservation and outbox intent are created together in the model.
2. Verify pre-send expiry is reclaimable and increments the fence.
3. Verify active lease cannot be stolen and stale worker mutation is rejected after reclaim.
4. Verify post-send-intent expiry enters reconciliation, not direct retry.
5. Verify authoritative exact found adopts the existing provider operation; eventually consistent absence remains HOLD; final exact absence authorizes same-attempt retry only.

**Boundary:** these are effect-dispatch semantics. They do not prove grant-event relay claim, ordering or delivered-marker fencing.

### Lane 4: grant-event relay boundary

**Source:** `scripts/release_grant_conformance.py`, especially `mark_outbox_delivered()`.  
**Current capability:** outbox item exists and a delivered boolean can be set.

**NOT TESTABLE in the current model:** relay claim/lease, relay fence generation, stale relay acknowledgement, ordered predecessor cursor, poison-event HOLD/quarantine and audited repair. The existing transfer-worker lease protects `record_progress()`, not `mark_outbox_delivered()`.

After gate clearance, first agree whether relay semantics belong in the model or adapter contract. Do not borrow FakeOutbox lease assertions as evidence for this separate relay.

### Lane 5: event journal provenance and fencing

**Source:** `scripts/event_journal.py`  
**Tests:** `scripts/test_event_journal.py`  
**Existing methods:** `test_accepts_verified_authorized_producer`, `test_duplicate_same_source_event_and_same_payload_is_idempotent`, `test_same_source_event_id_cannot_be_replayed_across_attempt_scope`, `test_unfenced_worker_event_is_rejected_even_with_flag`, `test_same_event_replay_under_new_fence_is_quarantined`, `test_same_source_event_id_with_changed_payload_is_quarantined`, `test_quarantine_is_append_only_and_does_not_replace_accepted_event`, `test_wrong_audience_rejected`, `test_unauthorized_source_rejected`.

Sequence:
1. Verify payload digest is recomputed from immutable bytes.
2. Verify same source/event/payload/scope is idempotent and conflicting payload/scope is quarantined without replacing accepted evidence.
3. Verify stale/missing fence rejection and append-only quarantine.
4. Record that `AuthenticatedProducer` is an adapter-verified input type, not a credential verifier. The pure model does not prove cryptographic authentication, persistent fence continuity or atomic database check-and-append.

### Lane 6: receipt store and typed verdict projection

**Sources:** `scripts/result_receipts.py`, `scripts/execution_projection.py`.  
**Tests:** `scripts/test_result_receipts.py`, `scripts/test_execution_projection.py`.

Receipt assertions:
- artifact bytes produce the stored length and SHA-256;
- partial writes and digest mismatches are quarantined;
- receipt revision keys bind immutable content and revisions extend the latest predecessor without forking;
- release checks exact attempt, receipt revision, artifact membership and the supplied authorization snapshot;
- historical receipt cannot authorize a new release after a successor.

Projection assertions:
- PASS requires coordinator lifecycle `succeeded` and direct-child natural exit zero;
- wrapper exit, embedded SystemExit, signal termination, timeout, stale attempt, unknown status and contradictory evidence never become a fabricated child exit;
- no evidence remains INCOMPLETE.

**Boundary:** the receipt model is in-memory and authorization is caller-supplied. The projection is pure and does not authenticate its inputs. Neither models Worker errors, private control channels, cancellation acknowledgement, cleanup, stream closure, OPFS readback or IndexedDB transaction commit.

## 4. Explicitly outside the model-only run

These require a separately selected and implemented adapter/browser boundary, plus owner approval:
- IndexedDB transaction commit/abort, quota, eviction, reload, reinstall and target iOS/Android browser behavior.
- OPFS staging, flush, close, readback and reconciliation with IndexedDB metadata.
- Same-origin sibling Pages access to localStorage, IndexedDB, Cache API and service-worker scope.
- Pyodide Worker default-channel spoofing, private MessagePort reachability and actual guest-global access.
- Worker crash, error, messageerror, terminate invocation, disappearance and any runner-level completion observation.
- Real streaming, active-transfer revocation, bytes emitted versus client acknowledged, and native child-process exit.
- Durable adapter concurrency, process crash, backup/restore, producer authentication and external provider behavior.

The current Pages prototype is explicitly simulation-only. It does not execute Python, import files, create artifacts, select a runtime or call a provider. Do not describe it as a live execution product or as vulnerable to a Worker exploit that it cannot currently instantiate.

## 5. Gate and exit criteria

Before any model run:
1. OD-01..OD-13 must be answered or explicitly deferred by the owner.
2. Relevant unresolved contract gaps must be named, not silently assumed away.
3. The owner must explicitly open the P39/P40 gate and authorize the bounded run.
4. Exact source/test SHA and environment must be pinned.

A model pass cannot close canonical CASE acceptance by itself. Keep LOOP-01..14, CASE-01..16 and all D-IDs unchanged. CASE-04 remains INCOMPLETE / timed_out until trusted boundary evidence resolves it.

## 6. Current status

- **VERIFIED:** the source methods and existing test names listed above were statically inspected at the pinned branch.
- **INFERRED:** equal progress is a semantic no-op under the accepted P39 parity rule; current implementation violates it by advancing the aggregate version without a matching event/outbox.
- **UNKNOWN:** selected policy outcomes, canonical event envelope, trusted ingress, actual Pyodios Worker topology, deployed live Pages response, durable adapter and target-device storage behavior.
- **NOT RUN:** every scenario in this protocol. No source/test changes were made.
- **Gate:** CLOSED. OD-01..OD-13 OPEN. No implementation or execution authorization is implied.
