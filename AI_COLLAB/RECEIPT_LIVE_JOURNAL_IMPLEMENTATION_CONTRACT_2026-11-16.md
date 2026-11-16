# Live-journal receipt implementation contract

Date: 2026-11-16
Status: design contract / NOT IMPLEMENTED
Scope: model-only receipt provenance and journal concurrency. No adapter, provider, persistence, runtime, workflow or canonical acceptance changes.

## Problem statement

A detached `JournalReceiptSnapshot` can be captured at time T1, then a matching conflict can be appended at T2, and a receipt can be created at T3 from the old snapshot. The receipt then omits evidence already present in the journal when receipt creation began. A module sentinel and frozen dataclass do not authenticate the snapshot or establish freshness.

The preferred API in `AI_COLLAB/NEXT_TASK.md` is to pass the exact live `EventJournal` into `ResultReceiptStore.create_receipt` and derive the evidence cut inside that operation. Do not accept a detached snapshot as provenance.

## Required API shape (proposal, not a claim about current code)

Conceptually:

```python
receipt_store.create_receipt(
    ...,
    journal=event_journal,
)
```

The receipt store asks the journal for one scoped, immutable evidence cut. The caller must not provide observation high-water, accepted-event high-water, conflict sequence references or a snapshot object. The exact effect and dispatch-attempt identity used by receipt creation must be passed to the journal query and checked against the receipt's own identity.

The journal owns the source of truth for:
- journal-global observation high-water;
- journal-global accepted-event high-water;
- conflict sequence references scoped to the exact effect and dispatch attempt;
- the ordering and coherence of those values at one logical cut.

The store owns receipt identity, revision/successor rules, canonical fingerprint construction and immutable receipt persistence in the existing in-memory model. This proposal does not make the store durable or cryptographically authenticated.

## Linearization and concurrency contract

If the model claims thread-safe capture, every journal append path that mutates any field used by the snapshot and the entire multi-field snapshot read must use the same journal lock.

1. Acquire the journal lock.
2. Read the observation high-water, accepted-event high-water and exact-scope conflict sequence references.
3. Validate invariants while still holding the lock: accepted high-water is not above observation high-water; conflict references are ordered, unique, positive and not above observation high-water.
4. Freeze/copy the values into an immutable value object.
5. Release the lock.
6. Construct the receipt fingerprint and receipt from that immutable cut.

The snapshot read in step 2 is the linearization point. An append that acquires the same lock before the cut is included; an append that acquires it after the cut is logically later. The receipt need not block all subsequent journal activity while hashing or storing the immutable receipt. This is linearizable evidence-at-cut, not a promise that the receipt always includes events appended after its cut.

Do not lock only the snapshot reader while leaving append paths unlocked. Do not infer atomicity from the Python GIL or a frozen dataclass. If the model deliberately does not support concurrent access, state that EventJournal is single-threaded/non-thread-safe and make synchronization an explicit adapter obligation; do not claim a concurrent coherent snapshot.

Avoid lock inversion: the receipt store must not hold its own store lock while waiting for the journal lock if another path can acquire them in the opposite order. Prefer obtaining the journal cut before taking the receipt-store mutation lock, then perform the receipt's existing duplicate/revision checks under the store lock. If receipt ordering requires a different lock order, document and test that one order globally.

## Identity and misuse rules

- Preserve `CommandId`, `EffectId`, `DispatchAttemptId`, `ExecutionId`, `ObservationSequence`, `ResultReceiptId/revision` and `PublicationAttemptId` as distinct identities.
- The journal query must be exact-scope: same effect with a different attempt is not a match; same attempt under a different effect is not a match.
- High-waters remain journal-global; conflict references remain effect/attempt-scoped.
- Reject bool-as-int, negative/zero sequence values where prohibited, duplicate or unsorted references, references above the observation cut, and accepted high-water above observation high-water.
- A journal object or Python method call is not cryptographic producer authentication. Preserve the explicit model trust boundary; producer authentication, persistence, process coordination and tamper resistance remain adapter obligations.
- Do not treat the private sentinel as an authorization mechanism. Remove reliance on it for receipt provenance once the live-journal API is implemented; ordinary value-object validation may remain.

## Regression packet

1. `test_receipt_creation_derives_snapshot_from_live_journal`: accepted event seq 1, scoped conflict seq 2, create receipt from journal; assert observation high-water 2, accepted high-water 1, conflict refs `(2,)`.
2. `test_receipt_includes_conflict_appended_before_creation_cut`: create any earlier snapshot if legacy code still permits it, append a scoped conflict, then create through the live-journal API; assert the new receipt includes the conflict. Assert there is no public detached-snapshot argument.
3. `test_receipt_conflict_refs_are_exact_effect_attempt`: append conflicts for two effect/attempt pairs; each receipt includes only its own references while both use the journal-global high-waters.
4. `test_receipt_successor_binds_late_conflict_without_mutating_predecessor`: a later receipt revision binds later evidence; predecessor fingerprint and conflict tuple remain unchanged.
5. `test_receipt_snapshot_highwaters_are_consistent`: reject malformed types, bool-as-int, unsorted/duplicate/out-of-range references and impossible high-water relationships.
6. `test_snapshot_capture_is_atomic_under_concurrent_append`: coordinate append and capture at the shared lock; assert every cut is a valid prefix and never a torn combination of high-waters and conflict refs.
7. `test_receipt_store_and_journal_lock_order_has_no_deadlock`: if both objects use locks, exercise concurrent receipt creation and append under a bounded test timeout. Do not use a timeout as proof of general deadlock freedom; use it as a regression tripwire.

## Acceptance boundary

- This is a model-level contract only. It does not close P39 implementation/adapter conformance.
- CASE-04 remains INCOMPLETE / `timed_out`.
- Report format 1 remains unchanged; no report-v2 migration.
- No durable outbox, consumer inbox, relay lease/fence, provider dispatch, authenticated producer, native process termination proof or client artifact acknowledgement is implied.
- Exact-tree tests remain NOT RUN until a network-capable execution path checks out and reports the exact commit SHA.
- Do not modify CI workflow to solve the test gap without separate authorization.

## Implementation sequencing

1. Inspect only the relevant bounded method/class sections in `scripts/event_journal.py` and `scripts/result_receipts.py` using a patch-capable working tree; verify base commit and blob SHAs first.
2. Apply a small diff, not a reconstructed whole-file replacement. Re-fetch changed hunks and inspect the final diff.
3. Add the focused receipt regressions in the corresponding test file; keep each commit to at most two files and approximately 200 changed lines.
4. Run focused tests and the full suite locally or in an authorized exact-SHA CI lane; record command, environment, exact SHA and output. Until then label NOT RUN.
5. Red-team identity scope, append/capture ordering, lock ordering, duplicate receipt revision and failure paths before claiming model completion.

## Tooling finding from this pass

The available GitHub connector exposes complete-blob creation, tree construction, commit creation, ref update and whole-file Contents replacement. It exposes no patch/hunk application or local clone/execute capability. Creating a standalone helper without a reviewed import seam would add dead code, so this pass deliberately did not do that. A patch-capable working tree (for example, an owner-provided local checkout or an authorized code-editing environment) is required before changing the large existing source and test files safely.
