# PocketCode — Idempotency and Ambiguous-Dispatch Recovery Falsification Checklist

**Status:** Research/test specification only. NOT RUN. No implementation, database, provider, or runtime selected. This document is not canonical acceptance and does not authorize workload, account, billing, merge, or deployment actions.

## Purpose

D-06 defines what must be proven before PocketCode may claim that retries, concurrent submissions, process restarts, or lost dispatch acknowledgements cannot silently create duplicate jobs or misattribute results.

The key limitation is fundamental: **a durable local reservation alone cannot guarantee exactly-once execution at an external provider.** If a provider may accept a start while its acknowledgement is lost, safe recovery requires an authoritative way to find the original operation or a provider-enforced idempotent start contract. If neither exists, the correct state is UNKNOWN and automatic redispatch is forbidden.

## Proposed invariants — owner review required

1. **Scoped key:** uniqueness is scoped by authenticated tenant/principal and a normalized idempotency key. A key must not reveal another tenant's job, result, or existence.
2. **Semantic binding:** the reservation stores a versioned request fingerprint for all execution-affecting semantics (source/input identity or digest, runtime/entrypoint, effective policy semantics, relevant schema versions). Same key + same fingerprint resolves to the same logical job; same key + changed fingerprint returns conflict before any new dispatch.
3. **Atomic reservation:** concurrent identical requests cannot both win the first reservation. Enforce with a durable unique constraint/transaction or equivalent atomic primitive, not a process-local dictionary or check-then-insert.
4. **Durable dispatch intent:** persist the original job/attempt identity and a dispatch-intent state before crossing the external start boundary. A crash must not erase evidence that a start might have been attempted.
5. **No blind replay:** after the provider call may have been accepted, a timeout, connection loss, process crash, or missing acknowledgement transitions to reconciliation/UNKNOWN—not a new start. Retry lookup must target the same original provider operation/attempt.
6. **Recovery requires authority:** only authoritative lookup or provider-enforced idempotency can establish that the original operation was accepted/not accepted. A local timeout, stale cache, missing row, or client retry is not proof that no execution started.
7. **Release/lease discipline:** expired leases may permit a worker to resume reconciliation, but must never by themselves authorize a second external dispatch when the first dispatch outcome is ambiguous.
8. **Terminal binding:** recovered provider job/attempt IDs and terminal events must match the reserved tenant/job/attempt and policy binding before they affect verdicts or artifacts.
9. **Retention and tombstones:** reservation/idempotency records and deletion tombstones must survive at least the documented retry/recovery horizon. Repeated same-key tombstone updates must not shorten the retention window; conflicting fingerprint reuse must not overwrite identity silently.
10. **Honest degradation:** if durable storage or authoritative provider lookup is unavailable, report UNKNOWN/INCOMPLETE and expose a safe recovery action; never synthesize a job ID, exit code, or PASS.

These are proposed requirements, not verified behavior or a frozen schema.

## Suggested state model

State names are illustrative and must be reconciled with the final envelope before implementation:

- `RESERVED`: durable unique key + fingerprint + stable job/attempt identity committed; no external dispatch is yet known to have been attempted.
- `DISPATCH_INTENT`: durable intent recorded before invoking the provider. From this point, a crash may leave dispatch status ambiguous unless the system can prove the call was never made.
- `ACKNOWLEDGED`: provider acceptance and authoritative external operation identity recorded.
- `RECONCILING`: acknowledgement or operation status uncertain; only lookup/reconciliation is allowed.
- `RUNNING`: authoritative lookup confirms the same attempt is active.
- `TERMINAL`: trusted terminal evidence for the same attempt is recorded.
- `REJECTED_BEFORE_DISPATCH`: durable evidence proves validation/barrier rejection happened before any external start call.
- `UNKNOWN_MANUAL_RECONCILIATION`: provider cannot authoritatively establish whether the original start occurred. No automatic second start.

Important: the distinction between `RESERVED` and `DISPATCH_INTENT` must be transactionally meaningful. A recovery worker must not infer “not dispatched” merely because no acknowledgement row exists.

## DR-01..DR-12 — falsification cases

| ID | Fault/setup | Required assertions | Evidence needed |
|---|---|---|---|
| DR-01 | Two concurrent identical requests, same tenant/key/fingerprint | Exactly one reservation wins; both callers resolve to the same job/attempt; one dispatch at most | Persistence-backed concurrency test |
| DR-02 | Same tenant/key but changed fingerprint (source/input/runtime/policy/schema version) | Conflict; zero additional dispatches; no old report/artifact substituted | Coordinator + persistent store test |
| DR-03 | Same textual key and fingerprint in two tenants | Independent reservations and results; no cross-tenant existence/result leakage | Authenticated API/store integration |
| DR-04 | Crash after reservation but before durable dispatch intent | Recovery proves no dispatch intent existed and follows a defined safe retry path; no duplicate reservation | Crash-injection persistence test |
| DR-05 | Crash after dispatch intent commit but immediately before provider call | If system cannot prove call was not made, reconcile conservatively; no automatic redispatch solely from lease expiry | Crash-point test; provider contract defines what can be proven |
| DR-06 | Provider accepts start but acknowledgement is lost | Lookup uses the original idempotency token/attempt; one external job; retry returns same identity if found | Fake for branch logic; actual provider integration for guarantee |
| DR-07 | Acknowledgement lost; authoritative lookup returns UNKNOWN/unavailable | No second dispatch; retain reservation and UNKNOWN status; clear retry/recovery instructions | Fake + persistence recovery test |
| DR-08 | Provider lookup authoritatively says original request was rejected/not created | Retry only if the provider contract makes this result definitive and the original request token remains safe; otherwise remain UNKNOWN | Provider-specific contract and integration test |
| DR-09 | Worker lease expires while first worker is blocked inside dispatch | Second worker reconciles/looks up original operation; lease expiry alone never starts another job | Concurrent worker + persistence test |
| DR-10 | Process restart after provider acceptance but before storing provider ID | Recover original operation by stable provider idempotency token or authoritative lookup; otherwise UNKNOWN and no new start | Restart integration test |
| DR-11 | Terminal event/result belongs to another tenant/job/attempt or has a changed fingerprint/policy binding | Reject/quarantine; never attach it to the reservation or release its artifacts | Trusted ingress + persistence integration |
| DR-12 | Tombstone/retry retention is updated repeatedly, shortened, expired, or conflicting fingerprint is supplied | Same-identity retry never shortens required retention; changed identity conflicts; after documented expiry behavior is explicit and cannot cause unsafe duplicate starts | Pure helper + persistence/clock-controlled test |

## Crash-point matrix

| Crash window | What is known after restart? | Safe default |
|---|---|---|
| Before reservation transaction commits | No reservation is known; retry can compete for atomic reservation | Revalidate and reserve atomically |
| After reservation, before dispatch-intent commit | No external call is permitted by protocol; prove this ordering with transaction and call-order evidence | Resume from reservation only if the invariant is proven |
| After dispatch-intent commit, before/during/after provider call | Provider may or may not have accepted | Reconcile original attempt; no blind redispatch |
| After provider acceptance, before acknowledgement persistence | External job may exist without local provider ID | Lookup using original stable idempotency token; if impossible, UNKNOWN |
| After acknowledgement persistence, before report update | Original external operation identity is known | Rebuild projection from durable evidence; do not start again |
| After terminal evidence, before report append | Terminal observation may exist but projection may be stale | Idempotently append/recompute with evidence identity and atomic versioning |
| During report/artifact publication | Partial write may exist | Do not publish a final manifest/release; verify stored bytes and reconcile |

## Storage contract questions that must be answered

Before claiming durability, document and test:

- What database/store is selected, and what transaction/unique-constraint semantics are guaranteed?
- Which exact fields make a reservation unique, and how is the tenant identity authenticated?
- Is the fingerprint versioned, and which fields are included/excluded? Are effective policy and schema versions included?
- How is the provider idempotency token derived and scoped without exposing secrets? Does the provider guarantee deduplication, for how long, and for which operation types?
- Can the original provider operation be found after a lost response or process restart? What does “not found” mean, and is it authoritative?
- What is the documented retention horizon for reservations, provider tokens, tombstones, reports and artifacts? What happens after expiry?
- How are two workers prevented from both claiming a state transition, and how is stale worker fencing enforced?
- How is a reconciliation action audited without turning a retry into an implicit second dispatch?

If these cannot be answered for the selected storage/provider, the relevant guarantee remains BLOCKED/UNKNOWN.

## Stop conditions

Stop and do not claim exactly-once or safe automatic recovery if any of the following holds:

- Reservation uniqueness is process-local or relies on read-then-insert.
- Dispatch may occur before the durable reservation/intent is committed.
- A timeout or lost acknowledgement can automatically trigger another start.
- Lease expiry is treated as proof that the prior start did not happen.
- Provider “not found” semantics are undocumented or eventually consistent without a safe reconciliation window.
- The provider lacks idempotent start and authoritative lookup, but the product still promises no duplicates.
- Restart recovery depends only on in-memory maps or client state.
- Changed request semantics reuse a previous job/report/artifact.
- Tenant/job/attempt binding is not validated on recovered results.
- Tests are only fake/in-memory but reported as proof of persistent uniqueness or provider guarantees.

## Evidence ladder

- **PURE/UNIT TESTED:** key normalization, fingerprinting, state-transition predicates and retention logic only.
- **FAKE-ADAPTER TESTED:** coordinator call order, zero/one dispatch counts under scripted faults, no-blind-retry branches.
- **PERSISTENCE INTEGRATION TESTED:** unique reservation, transactions, concurrent submissions, worker fencing, crash/restart recovery, append-only reports.
- **PROVIDER INTEGRATION TESTED:** actual idempotent-start and lookup semantics under lost acknowledgements and process interruption.
- **DEVICE ACCEPTED:** UI honestly communicates retrying, reconciling, unknown, conflict, and recovered results.

No lower level substitutes for a higher boundary guarantee.

## Relationship to existing contract

- D-06 in `OWNER_DECISION_REGISTER_20261029.md`.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`: FAKE-05/06 and the explicit limitation that local reservation does not create provider exactly-once guarantees.
- `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md`: COORD-07/08 and CASE-11/13/16.
- FLA-09 and tombstone-retention review in `AI_COLLAB/FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md`.
- Canonical anchors: LOOP-05/09/14; CASE-11/13/16. Canonical acceptance remains unchanged.

**Current result:** SPECIFIED ONLY / NOT RUN. No provider or persistent store is selected. No implementation, test, account, billing, workload, merge, or deployment action was performed.
