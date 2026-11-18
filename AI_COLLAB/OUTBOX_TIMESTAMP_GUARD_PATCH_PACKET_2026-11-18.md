# Outbox reconciliation timestamp guard — implementation packet (2026-11-18)

## Status
- VERIFIED: active branch source `scripts/fake_outbox.py` currently accepts `now=None` in both authoritative state-changing reconciliation branches.
- VERIFIED: the two existing tests `test_lost_ack_found_reconciles_without_second_dispatch` and `test_final_exact_absence_allows_same_attempt_retry` omit `now`, so they currently encode timestamp-free transitions.
- VERIFIED: `resolve_reconciliation` returns `hold_unknown` before timestamp validation when identity or authority is not exactly `True`; preserve that non-mutating hold behavior.
- INFERRED: the intended timestamp is a local observation-time input, not proof that the provider's result is actually authoritative. The model docstring already says caller trust is not verified.
- NOT RUN: no tests or CI were executed in this pass.

## Minimal source correction
In `FakeOutboxStore.resolve_reconciliation`, change both conditional guards from:

```python
if now is not None and (isinstance(now, bool) or not isinstance(now, int) or now < 0):
```

to:

```python
if now is None or isinstance(now, bool) or not isinstance(now, int) or now < 0:
```

Keep validation inside each state-changing branch. Do not move it above the exact-identity/authority hold, because an untrusted or wrong-scope result must remain a harmless `hold_unknown` without requiring a timestamp.

Recommended messages:
- found: `"reconciliation observation time is required and must be a non-negative integer"`
- final absence: `"reconciliation observation time is required and must be a non-negative integer"`

Do not remove the optional default from the public signature in this narrow fix: callers that receive a non-authoritative result can still safely obtain `hold_unknown` without a timestamp. The two mutating outcomes must reject omission.

## Regression tests to add
1. `test_found_reconciliation_requires_valid_observation_time_without_mutation`
   - Put the record in `reconciling`.
   - Capture the complete record before calling with a valid provider reference and `now=None`.
   - Assert `ValueError`; assert the record equals the captured record and remains `reconciling`, with no provider reference or acknowledgement timestamp.
2. `test_final_absence_requires_valid_observation_time_without_mutation`
   - Same setup; call `outcome="not_found", absence_final=True, now=None`.
   - Assert `ValueError`; assert byte-for-byte/equality-equivalent record state is unchanged and retry is not authorized.
3. Parameterize invalid values `True`, `-1`, `1.5`, and `"4"` across both mutating outcomes; each must raise before mutation.
4. Strengthen positive found-path coverage: with `now=4`, assert both `acknowledged_at == 4` and `reconciliation_observed_at == 4`, and state is `acknowledged`.
5. Add positive final-absence timestamp coverage: with `now=6`, assert `reconciliation_observed_at == 6`, `reconciliation_outcome == "final_absence"`, state is `retry_authorized`, and the original EffectId/AttemptId are unchanged.
6. Preserve the existing non-authoritative/wrong-identity test without `now`; it must still return `hold_unknown` and leave state unchanged.

## Evidence boundary / follow-on
- This is a synchronous in-memory fake/reference model. It does not establish provider-side authority, exact-scope lookup, crash durability, distributed fencing, or receiver-side atomic dedupe.
- The booleans `exact_identity_match` and `authoritative` remain caller assertions. A real adapter must bind them to authenticated provider evidence and the exact EffectId + DispatchAttemptId + operation scope.
- After this narrow guard/test fix, return to NEXT_TASK item 1: derive receipt provenance from the live EventJournal at receipt creation rather than accepting detached snapshots. Do not combine these API changes in one patch.
- Do not edit workflows or change P39/CASE gates. Tests/CI must be run on the exact resulting source tree before any pass claim.
