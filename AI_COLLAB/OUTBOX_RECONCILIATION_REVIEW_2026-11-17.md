# Outbox Reconciliation Review — 2026-11-17

## Scope and evidence

Reviewed the active-branch implementations in `scripts/fake_outbox.py`, `scripts/release_grant_conformance.py`, and the existing `scripts/test_fake_outbox.py` tests. This is a reference-model review only; it is not evidence of durable adapter behavior.

## VERIFIED — positive reconciliation can omit observation time

`FakeOutboxStore.resolve_reconciliation()` requires a non-negative `now` for final exact-identity absence, then persists it as `reconciliation_observed_at`. The `outcome == "found"` path, however, accepts `now=None`, writes `acknowledged_at=None` and `reconciliation_observed_at=None`, and still returns `adopt_existing`.

The existing test `test_lost_ack_found_reconciles_without_second_dispatch` exercises precisely that timestamp-free path. A separate test verifies timestamp persistence only when `now` is supplied. Therefore the current suite does not enforce a timestamped positive reconciliation observation.

### Narrow follow-up

- Require a valid non-negative integer `now` for `found`, just as final absence does.
- Keep the exact-identity and authoritative gates; do not treat these caller booleans as cryptographic/provider verification.
- Add a regression asserting that `found` without `now` is rejected and leaves the record in `reconciling`.
- Assert that a valid `found` transition persists the same observation time in both `acknowledged_at` and `reconciliation_observed_at`.
- Preserve adoption semantics: no second dispatch, same EffectId/AttemptId, and immutable original reservation.

## VERIFIED — model boundary remains deliberately limited

Both outbox and release-grant implementations are synchronous in-memory reference models. Their staged commit points demonstrate intended atomic transition semantics only; they do not establish database transactionality, crash durability, cross-process fencing, or receiver-side atomic deduplication. The reconciliation method explicitly says caller trust is not verified. Do not promote these models to adapter-conformance evidence.

## INFERRED — next implementation order

1. Fix positive-reconciliation timestamp validation and focused tests in the fake outbox model.
2. Keep provider evidence authentication and exact operation/scope binding as a separate adapter boundary; booleans supplied by a caller are not proof.
3. Continue to treat durable outbox + consumer inbox transactionality and restart/replay tests as open adapter work.

## Execution status

- Source review: complete.
- Source/test changes: none in this review.
- Tests/CI: NOT RUN.
- Production adapter/durable storage: UNKNOWN / NOT PROVEN.
