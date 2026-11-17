# Outbox Reconciliation Review — 2026-11-18 correction

## Scope and evidence

Rechecked the exact active-branch implementation in `scripts/fake_outbox.py` (lines 110–246) and `scripts/test_fake_outbox.py` (lines 1–188). This is a synchronous in-memory reference-model review, not durable adapter evidence.

## VERIFIED — both reconciliation outcomes accept missing observation time

Correction to the 2026-11-17 review: its statement that final exact-identity absence already required `now` was incorrect.

In `FakeOutboxStore.resolve_reconciliation()`:

- `outcome == "found"` validates `now` only when it is non-`None`. With `now=None`, it acknowledges and adopts the existing provider operation while persisting both `acknowledged_at` and `reconciliation_observed_at` as `None`.
- `outcome == "not_found"` with `absence_final is True` has the same conditional-validation defect. With `now=None`, it authorizes retry and records `reconciliation_observed_at=None`. The error text says time is required, but the condition does not reject its absence.
- Existing tests `test_lost_ack_found_reconciles_without_second_dispatch` and `test_final_exact_absence_allows_same_attempt_retry` both exercise timestamp-free transitions. The separate positive timestamp test checks persistence only when a time is supplied.

The precise defect is shared: each branch uses `if now is not None and invalid(now)` where the contract requires `if now is None or invalid(now)`. Validation must reject booleans, non-integers and negative integers as well.

## Required narrow correction

1. For both authoritative exact-identity `found` and final `not_found`, require `now` to be a non-negative integer before mutating the record.
2. Add no-time rejection tests for both outcomes; assert the exception and that the record remains `reconciling` with no provider reference, acknowledgement timestamp, or retry authorization.
3. Add invalid-time cases (`True`, negative integer, non-integer) for both branches.
4. Assert valid `found` stores the same `now` in `acknowledged_at` and `reconciliation_observed_at`; assert valid final absence stores `now` in `reconciliation_observed_at` and retains the same EffectId/AttemptId.
5. Preserve no-second-dispatch adoption and exact-final-absence gating. Caller booleans remain assertions, not cryptographic/provider proof.

## Model boundary

The outbox and release-grant models are synchronous and in-memory. They do not prove database transactionality, crash durability, cross-process fencing, receiver-side atomic deduplication, or authenticity of reconciliation evidence.

## Execution status

- Source review: VERIFIED at active-branch blob `813957e5061d40cba2ebb5e2936edcbac645820b`.
- Test review: VERIFIED at active-branch blob `67951a77f87e9523c9080970068fd158680f23a9`.
- Source/test changes: NOT MADE; the available write API replaces complete files and no safe patch/hunk action is exposed.
- Current marker commit combined status: no status contexts; associated workflow runs: none. Tests/CI: NOT RUN.
- Durable provider adapter and authoritative evidence: UNKNOWN / NOT PROVEN.

## Next

Use a patch-capable working tree to implement the two-branch timestamp guard and focused regressions. Then return to the higher-ranked live-journal receipt provenance/freshness gap. Do not change workflows, adapters, provider/runtime choices, PRs, canonical acceptance IDs, or P39/CASE-04 gates.
