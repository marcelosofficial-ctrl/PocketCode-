# Outbox reconciliation timestamp guard — test packet (2026-11-20)

Status: VERIFIED code-path gap; tests NOT RUN; implementation NOT changed.

## Verified behavior

In `scripts/fake_outbox.py`, `resolve_reconciliation()` accepts `now=None` on both timestamp-sensitive transitions:
- `outcome="found"` with nonempty provider reference adopts the provider operation while writing both `acknowledged_at` and `reconciliation_observed_at` as None.
- `outcome="not_found"` with `absence_final=True` authorizes same-attempt retry while writing `reconciliation_observed_at=None`.

The guard currently validates timestamp only when `now is not None`; booleans, non-integers and negative values are rejected only when provided. Existing tests `test_lost_ack_found_reconciles_without_second_dispatch` and `test_final_exact_absence_allows_same_attempt_retry` exercise these paths without timestamps. Positive observation-time test exists (not re-read this pass).

## Minimal safe change

Validate `now` **before mutating** for each transition that requires observation time:
`isinstance(now, int) and not isinstance(now, bool) and now >= 0`.
Do not change the unknown/non-authoritative hold behavior or claim this caller-supplied timestamp proves reconciliation authority.

## Required tests

1. Found: reject missing `now`, `True`, float/string, negative; record remains reconciling unchanged; valid non-negative timestamp stores both time fields and adopts provider ref.
2. Final exact absence: reject missing `now`, `True`, float/string, negative; record remains reconciling unchanged; valid timestamp stores observation time, enters retry_authorized, retains identical EffectId + AttemptId.
3. Unknown/non-final absence remains hold_unknown and never releases retry, regardless of timestamp.
4. Verify each rejection is atomic (state and all reconciliation fields unchanged).

## Caveats / acceptance boundary

The fake outbox remains an in-memory contract model. A timestamp is not provider evidence; authority/exact identity/finality are supplied caller booleans, not authenticated. This guard improves field integrity only—not durability, transactional outbox semantics, thread/process fencing, receiver atomic dedupe, or provider proof.

Next: patch-capable editor required to safely change source and tests. Run focused tests and exact-head suite, recording exact commit SHA and output.
