# Append-only event provenance model — 2026-11-06

**Status:** deterministic in-memory model and unit tests. This is not a production event bus, durable journal, cryptographic verifier, or trusted runtime integration.

## Implemented

- `scripts/event_journal.py` defines an immutable `AuthenticatedProducer` evidence value, immutable accepted event records, conflict quarantine records, and a coordinator-sequenced append-only journal.
- Producer claims must be complete, match the configured audience, and authorize the exact event source.
- Event identity follows `(source, producer_event_id)`. The same authenticated producer replaying identical immutable payload bytes is a duplicate and returns the original sequence.
- Reuse of an event identity with changed payload bytes, or by a different authenticated producer identity, is quarantined. It never overwrites the accepted event.
- Payload SHA-256 is calculated from the exact accepted bytes. The original bytes are retained, not reconstructed from parsed JSON.
- Occurrence and observation timestamps are stored separately. Neither timestamp controls ordering.
- The journal assigns its own strictly increasing sequence to accepted events and quarantined conflicts.
- Effect-linked events require an exact current fencing token registered for the `(EffectId, DispatchAttemptId)` pair. A stale fence is rejected.
- Inputs reject booleans where integer timestamps/fences are required, mutable payload types, incomplete identities, invalid audience and unauthorized source.

## Verification

Command: `python -m unittest discover -s <working-copy> -p 'test_event_journal.py' -v`

**21/21 passed** under the current local Python interpreter. This is a deterministic unit-test result only. It does not test multi-process races, durable append atomicity, process/power-loss recovery, key rotation, signature verification, credential revocation, or a mobile runtime.

## Security boundary and required production adapter

`AuthenticatedProducer` is a value object representing the output of a trusted authentication adapter. Python callers can construct it, so its presence alone is not cryptographic proof. Production must keep the journal behind an adapter that verifies the credential/signature, issuer, subject, key status, audience, source authorization, revocation and replay policy before constructing this value. Do not accept this object directly from untrusted app/provider payloads.

The in-memory `advance_fence` method is a model operation. A durable implementation must atomically compare-and-advance fencing state with the event append. It must not allow a stale worker to race between fence check and append.

## Explicit non-decisions

No event transport, signature algorithm, credential store, key-rotation mechanism, database, runtime, provider, budget or release mechanism is selected. Existing canonical LOOP/CASE/D IDs and CASE-04 semantics are unchanged.

## Next gate

Combine outbox and journal state in a fake coordinator, then test crash points across reservation, dispatch intent, event append, acknowledgement and projection rebuild. Only after those semantics are stable should a durable store be selected and tested with concurrent workers and process restart.

## Red-team refinement — duplicate identity semantics

The suite is now **21/21 passed**. An exact replay requires the same source/event ID, issuer and subject, exact payload bytes, and the same occurrence timestamp. Observation time may differ because it records when the journal saw the event again. A key rotation for the same issuer/subject does not break deduplication; the newly observed key ID remains a property of the authentication observation, while the first accepted event retains its original key ID. A different issuer/subject, changed payload, or changed occurrence timestamp is quarantined. This prevents key rotation from creating false conflicts while rejecting altered event facts.
