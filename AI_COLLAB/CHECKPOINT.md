# CHECKPOINT — 2026-11-14

- Startup sequence re-read from live branch. Start HEAD: `5489f61518b4aaea23c60824381de56965d709a6`.
- Source/test commit `ed4d8210ce480ee25ebd148ac5d7c24d322a0d73` updates only `scripts/test_release_grant_conformance.py`.
- Fixed an outdated future-event fixture that still used a now-invalid `completed` state and placeholder digest. The fixture now uses the model's canonical event constructor.
- Strengthened same-identity/different-payload test: alternate payload now has a valid canonical digest, so rejection tests the event identity collision rather than merely malformed digest.
- Added malformed-envelope rejection coverage for wrong source, wrong event ID, boolean aggregate version and unsupported state; asserts no consumer state mutation. One new test method, four subcases. Static test-method count: 30.
- Test execution attempted through clone and local execution environment; both failed because `github.com` could not be resolved. Tests NOT RUN.
- Previous grant implementation `45cb200` still models aggregate/event/outbox update at one in-memory commit point only. No durable atomicity or authenticated producer proof.
- Next: exact-tree tests; typed EventJournal-to-ResultReceipt snapshot composition; grant transition replay/order and outbox delivery tests.
- Preserve P39 adapter gate CLOSED, CASE-04 INCOMPLETE / timed_out, report-v2 gated and successful Pyodios `summary.json`.
