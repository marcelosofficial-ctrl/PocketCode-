# Lifecycle, Idempotency, and Artifact Policy — Decision Proposal

**Status:** Selected provider-neutral baseline after owner delegation on 2026-10-27; not a frozen public API or live-execution authorization. See [research rationale](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md).  
**Date:** 2026-10-27  
**Scope:** Offline orchestration/report contract only. Strict $0; no provider, accounts, workloads, or tests run.

## Why this proposal exists

The execution contract and lifecycle-resolution note identify the same unresolved edges from different angles. This note turns those edges into deterministic rules that can be implemented and tested later without selecting a provider. It deliberately leaves external status names and numeric resource caps open.

## 1. Separate immutable observations from derived disposition

Store an append-only event/evidence record for facts such as request accepted/rejected, policy revision confirmed, execution started, output bytes observed, termination reason/exit code, artifact digest verified, cleanup attempted, and cleanup confirmed/failed. Each record should carry a job ID, event ID, source/provenance, and timestamp or sequence when available.

Derive the user-facing disposition from the evidence record and a versioned policy. Do not treat one mutable status field as the history. Corrections append reconciliation evidence and create a new report version; they do not rewrite a previously issued report in place.

Selected baseline field vocabulary (working contract labels; exact public API/schema is not frozen):
- **Execution outcome:** NOT_STARTED | EXIT_ZERO | EXIT_NONZERO | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | UNKNOWN.
- **Cleanup state:** PENDING | CONFIRMED | FAILED | UNKNOWN, with append-only cleanup-attempt evidence.
- **Job disposition:** REJECTED | PASS | FAILED | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | INCOMPLETE | PROVIDER_ERROR.
- **Evidence quality:** COMPLETE | MISSING | CONTRADICTORY | STALE, retained as evidence metadata rather than a replacement for the three fields above.

The pure helper uses this execution-outcome/disposition vocabulary. A provider adapter must not infer termination from a timeout or cancellation request; the separate termination-confirmed evidence gate remains mandatory. Exact external field names may change before schema freeze, but semantics must remain aligned.

## 2. Deterministic race rule

Use one per-job atomic terminalization/decision record (compare-and-set or equivalent transaction) with a monotonically increasing decision version. The first eligible authoritative decision wins for the current execution attempt; later events are still recorded but cannot silently overwrite it.

**Determinism qualification:** atomic compare-and-set guarantees a single committed winner, but does not by itself guarantee that two concurrent signals will choose the same winner across repeated runs. Assign a monotonic coordinator-ingress sequence to accepted events and define the decision from that sequence, or explicitly choose a conservative precedence rule. Provider timestamps alone may be skewed or absent. Offline tests should assert one committed decision, retained competing evidence, and exactly-once cleanup; tests that demand the same winner across race permutations require an explicit precedence rule first.

- Cancellation request and client deadline are not proof of termination.
- A timeout decision requires trusted deadline evidence and the defined timeout enforcement result. If process termination is still unknown, report that explicitly; do not claim the process is stopped.
- A late zero-exit event after a committed timeout/cancel is diagnostic evidence. Reconcile only if the contract defines an authoritative provider sequence proving the earlier decision was provisional; otherwise disposition remains INCOMPLETE/PROVIDER_ERROR, never silently PASS.
- Duplicate events with the same provider event ID are idempotent. Conflicting events with the same ID or impossible sequence are evidence contradictions.
- Cleanup is single-flight per job/attempt. Duplicate cleanup requests attach to the same operation or safely retry an idempotent operation; they must not create multiple contradictory terminal results.

**Selected reconciliation rule:** do not reverse a committed timeout/cancel execution decision in place. Later or conflicting evidence is retained; unless a future contract version defines authoritative evidence that proves the earlier decision was provisional, derive INCOMPLETE/PROVIDER_ERROR as appropriate and issue a new versioned report rather than silently replacing the decision.

## 3. Cleanup failure and result exposure

A successful process exit and valid output may be preserved as execution facts even when cleanup fails. Overall disposition must not be PASS while cleanup is failed or unconfirmed.

Default conservative proposal:
- Keep collected artifacts quarantined and unavailable to normal download/report handoff while cleanup is unconfirmed or failed.
- The status report may disclose that execution evidence exists, but must not include artifact contents, live provider URLs, credentials, or claims that the environment was destroyed.
- Release artifacts only after cleanup is confirmed and artifact validation plus tenant authorization pass. If the product later chooses provisional artifact access, it needs an explicit owner decision, separate API field/status, short-lived authorization, warning UX, and threat review.
- If cleanup eventually succeeds on retry, append the retry evidence and derive a new disposition/report version. Preserve the original cleanup failure event and report history. Do not call the original report “PASS” retroactively.

This is intentionally stricter than returning output immediately: user convenience does not justify exposing results while the execution boundary may still be alive.

## 4. Idempotency semantics

Before implementing idempotency, define canonicalization precisely: validated schema version, authenticated tenant, normalized task/runtime/entrypoint, decoded source/input bytes, and effective server-enforced policy participate in the canonical request fingerprint. Exclude transport-only fields such as retry timestamps. Never trust a client-supplied fingerprint.

For a key scoped to an authenticated tenant:
1. Same key + same canonical fingerprint + active job: return the existing job reference/status; do not launch another attempt.
2. Same key + same fingerprint + completed job: return the same job/report version reference subject to current authorization and retention rules; do not rerun implicitly.
3. Same key + different fingerprint: deterministic conflict; do not start a job and do not return the previous job's result as if it matched.
4. Same textual key from different tenants: independent namespaces, with no cross-tenant existence or timing leak.
5. Concurrent first submissions: atomic unique-key reservation determines one winner; losers re-read and apply the same-key rules above.
6. Explicit rerun: use a new attempt ID and an explicit rerun operation/policy; do not overload network retries as rerun intent.

**Selected provisional policy:** retain the full idempotency record while the job/report remains addressable; after deletion, retain a tenant-scoped one-way tombstone for 30 days and reject key reuse during that window. This 30-day period is an offline-test default, not a production/privacy commitment. Clients must not intentionally reuse keys, and the server does not guarantee detection after tombstone expiry. Full report/artifact retention, deletion evidence, and coordination with privacy obligations remain unresolved and must be defined before API freeze.

## 5. Artifact integrity and safe handoff

Treat artifact storage as a transaction:
1. Stream to a private temporary object with enforced per-file and aggregate byte limits.
2. Count actual bytes while streaming; stop or safely drain according to a documented policy when caps are exceeded.
3. Finalize only after the write completes; compute a digest over the final stored bytes and verify it by reading back or using an equally authoritative storage integrity result.
4. Atomically publish a manifest entry only when size, digest, generated storage ID, display-name validation, content-type policy, and job/tenant association are valid.
5. Interrupted write, digest mismatch, incomplete readback, unknown owner, or cleanup gate failure leaves the artifact quarantined/invalid and the overall job non-PASS.
6. Storage paths are generated from server-side opaque IDs, never constructed from client filenames. A display name is metadata only. Download authorization checks authenticated tenant and job ownership on every request.

A hash proves byte identity relative to the recorded digest, not safety of the content or truth of the execution claim. Keep those claims separate.

## 6. Bounded streaming and redaction

Do not accumulate unbounded stdout/stderr in memory before truncating. Process chunks through a bounded pipeline; enforce separate stream limits and, if needed, a combined budget. Track observed byte counts separately from retained bytes. The report states whether output is complete or truncated.

Secret redaction is defense-in-depth, not a guarantee. A detector must preserve enough overlap across chunks to detect configured patterns split between chunks, without buffering an unbounded stream. Tests should use synthetic token-shaped fixtures only. Do not pass service credentials into the task environment; redaction cannot make secret injection safe.

If a stream exceeds its cap, record the limit event and follow the defined termination policy. Do not report PASS if the contract says a cap violation invalidates successful completion. Decide whether the adapter terminates immediately or continues draining to avoid pipe deadlock; document and test the choice.

## 7. Cost and telemetry evidence

Keep provider-observed CPU/RAM/time/process metrics separate from provider invoice/usage cost. Use a cost evidence state such as FINAL | ESTIMATED | UNAVAILABLE, with source, observation time, currency, and scope. If the provider has not returned cost, show “unavailable” (or “estimated” with an explicit method); never infer $0 from missing data or free credits.

No live cost endpoint should be queried as part of offline tests. Synthetic fixtures should verify missing, delayed, stale, and contradictory usage records.

## 8. Proposed offline acceptance cases (NOT RUN)

| ID | Fixture | Required assertion |
|---|---|---|
| LIFE-SEM-01 | Exit-zero evidence then cleanup failure | Preserve exit-zero fact; disposition not PASS; artifact remains quarantined |
| LIFE-SEM-02 | Cleanup retry succeeds after initial failure | Append retry event; preserve first failure; create new report version; release only after all gates pass |
| RACE-SEM-01 | Timeout and cancel arrive in either order, same logical tick | Exactly one atomic decision commits; both events retained; no duplicate cleanup. Reproducible winner requires recorded coordinator-ingress sequence or an explicitly approved precedence rule |
| RACE-SEM-02 | Duplicate event ID with same payload / conflicting payload | Same payload idempotent; conflict marks evidence contradictory |
| RACE-SEM-03 | Late success after timeout decision | No silent PASS; reconcile only under explicit authoritative ordering rule |
| IDEM-SEM-01 | Same tenant/key and same canonical request | One job/attempt; retries return existing reference |
| IDEM-SEM-02 | Same tenant/key, changed source/input/effective policy | Conflict before allocation; no second job; no first-result substitution |
| IDEM-SEM-03 | Concurrent same-key submissions | Exactly one reservation wins; other observes canonical existing-job rule |
| IDEM-SEM-04 | Same key in two tenant namespaces | Independent jobs; no cross-tenant response/existence leak |
| ART-SEM-01 | Interrupted write or digest mismatch | No manifest publication; artifact invalid/quarantined; no PASS |
| ART-SEM-02 | Display name contains traversal/Unicode lookalikes | Generated storage ID remains isolated; reject or safely normalize display metadata |
| ART-SEM-03 | Artifact belongs to other job/tenant | Deny status and download; do not disclose metadata |
| STREAM-SEM-01 | Many chunks exceed output cap | Memory bounded by design; retained bytes capped; observed count and truncation recorded |
| STREAM-SEM-02 | Synthetic secret-shaped pattern spans chunk boundary | Configured detector catches fixture; no claim of universal detection |
| COST-SEM-01 | Resource metrics exist, invoice data delayed/missing | Telemetry remains observed; cost ESTIMATED or UNAVAILABLE, never falsely FINAL/$0 |
| NET-SEM-01 | Required policy revision changes between prepare and execute | Revalidate immediately before start; mismatch prevents execution |

All are proposed specifications, not executed tests. A fake adapter validates deterministic control logic only, not real provider behavior.

## 9. Historical decision requests and next step

The six owner-delegated decisions below supersede the review requests recorded when this proposal was first drafted. The selected provider-neutral baseline is recorded in [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md): artifact quarantine until cleanup/integrity/authorization pass; coordinator-sequenced terminalization with conflicting terminal evidence treated as INCOMPLETE; tenant-scoped fingerprinted idempotency with a provisional 30-day post-deletion tombstone; bounded output with a provisional 1-second drain/discard window; versioned canonical fingerprinting; and separate execution outcome, cleanup state, and immutable versioned disposition.

Remaining work is implementation-independent contract/test traceability and exact offline test execution when a local interpreter is available. Production retention, numeric limits, provider semantics, public schema names, and cost telemetry still require review before implementation. No provider selection, account creation, spend, live security testing, merge, or deployment is authorized. Keep PR #3 draft/unmerged and PR #2 untouched.


## 10. Selected decision record — 2026-10-27

The owner delegated the six decisions to ChatGPT. The selected defaults are now recorded in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md), with research and official references in [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md).

- Artifacts remain quarantined until cleanup, integrity, and tenant/job authorization gates pass; recovery creates a new report version.
- Accepted coordinator events receive a monotonic sequence; one atomic terminal decision commits per attempt; ambiguity is non-PASS.
- Idempotency is tenant-scoped and fingerprinted; retain records while addressable and a one-way tombstone for 30 days after deletion; explicit reruns use a new key.
- Offline-test output defaults are 32 KiB per stream, 64 KiB aggregate retained output, and at most 1 second of drain/discard after a cap breach. Exceeding a cap is LIMIT_EXCEEDED, never PASS. These limits are provisional, not production-validated.
- Fingerprinting uses versioned canonical encoding over exact decoded source/input bytes and effective execution policy.
- Execution outcome, cleanup state, and versioned derived disposition are separate; issued reports are immutable.

The old owner-review list above is historical as of this decision. Numeric limits require review before any live execution. No provider, account, spend, live workload, production implementation, merge, or deployment is authorized.


## Replay clarification — 2026-10-27

The one-terminal-decision rule applies even when distinct terminal events arrive with different event IDs. Replay retains all accepted evidence and records the earliest terminal event by coordinator sequence as the nominal winner; any additional distinct terminal event is contradictory evidence and must derive INCOMPLETE, not PASS. This is a conservative offline contract rule, not a statement about any provider's event guarantees. Regression coverage added; tests not run.
