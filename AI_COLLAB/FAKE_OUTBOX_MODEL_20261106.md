# Fake outbox and recovery model — 2026-11-06

**Status:** deterministic in-memory design/test model only. It is not durable storage, a dispatcher, a provider adapter, or product execution code.

## Implemented behavior

- Reservation and dispatch-intent row are created at one in-memory commit point. A pre-commit crash injection leaves neither object nor sequence increment.
- EffectId remains stable across attempts. Each DispatchAttemptId has its own immutable request fingerprint and exact request bytes. A later attempt requires the prior attempt to be terminal and explicit new-attempt authorization.
- Leases carry owner, expiry and monotonically increasing fencing token. An active lease cannot be stolen; stale workers cannot progress after reclaim.
- Crash before dispatch intent returns the reservation to pending and permits reclaim.
- Crash after dispatch intent moves the operation to reconciliation. This covers both intent persisted before send and provider acceptance followed by lost acknowledgement. Those states are indistinguishable without provider evidence and cannot be blindly replayed.
- Exact authoritative found is adopted. Eventually consistent or non-final not-found remains UNKNOWN. Only adapter-verified exact-scope final absence can return the same attempt to pending.
- Fake consumer deduplicates repeated delivery by stable EffectId and exact request fingerprint; changed fingerprint conflicts.

## Verification

Command: python -m unittest discover -s scripts -p 'test_fake_outbox.py' -v

**19/19 passed** under CPython 3.13.5. Both files also passed py_compile.

These are deterministic model tests, not concurrency, process-kill, power-loss, filesystem, database, network, provider or device tests.

## Red-team boundary

The model does not claim atomicity beyond its synchronous in-memory commit point. fail_before_commit is a test failpoint, not a durable transaction test. resolve_reconciliation receives caller-supplied booleans; it does not authenticate provider responses or prove lookup finality. The fake consumer is not a guarantee that an external provider behaves this way.

After dispatching, no worker may claim the record until exact reconciliation resolves it. A durable implementation must preserve these semantics with database transactions, compare-and-swap/fencing and provider-specific adapter verification.

## Next gates

1. Add producer authentication and source-scoped event append/deduplication.
2. Add crash/reopen tests against a selected durable store only after version/build and durability semantics are pinned. SQLite remains unselected; existing WAL maintenance floor and power-loss requirements still apply.
3. Exercise actual concurrent claim races and stale-fence writes against that store.
4. Integrate no provider until exact operation idempotency, lookup consistency and absence-finality are documented and tested.
