# Claude review: release-grant adapter research and red-team (P39)   2026-11-08

Reviewer: Claude (independent; Gemini's review not read). Reviewed: RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md only (read in full).
NOT reviewed: scripts/release_grant_conformance.py and its tests, RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md, P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md. No code was run. Tags: VERIFIED = checked on a primary page by me; INFERRED = my reasoning; UNCHECKED = a claim I did not re-verify.

## Verdict
The document's structure is sound: ranked gaps, separation of intent from proof, ordered outbox, fencing that must reach the protected resource, and honest NOT SELECTED status. The findings below are specification gaps that would let a conforming adapter still be wrong. None says the research is false.

## Findings
| ID | Severity | Where | Problem and counterexample | Proposed correction |
|---|---|---|---|---|
| F-01 | High | Recipe steps 1-8; POLICY-01 | The fresh authorization decision is fetched in step 1, outside the transaction. A revocation landing between step 1 and the commit in step 8 still yields a grant, so POLICY-01 ("revocation before grant commit: denied") cannot hold. RT-01 also excludes policy revision from the fingerprint, so nothing re-checks it | Store a monotonic revocation or policy epoch in the same store and read it inside the transaction; or state a bounded-staleness rule (decision TTL) and test it. Add POLICY-03 |
| F-02 | High | RT-01, recipe step 4 vs 6 | Ambiguity: step 4 re-reads the LATEST receipt (server-resolved) while the fingerprint covers "receipt ID/revision/hash". If the server fills that field, a legitimate same-key retry after the head advanced gets a different fingerprint and is rejected as "changed intent". If the client supplies it, say so | Fingerprint only client-supplied immutable references, never server-resolved latest values. Add IDEMP-01: retry with same key after head advance returns the original grant |
| F-03 | High | FENCE-02, step 10 | "Rejected based on expiry" needs a trusted clock. A phone clock can be set back; a worker's own clock cannot judge its own lease. Counterexample: clock moved backward, an expired worker's write is accepted | Judge expiry by the authority's clock or by explicit takeover epoch only; forbid worker-local time. Add CLOCK-01 |
| F-04 | Medium | RT-04, open decision 4 | Fence continuity relies on tombstones kept for an undecided "horizon". After the horizon, a recreated grant ID could restart its fence | Make grant IDs globally unique and non-reusable by construction (random 128-bit) so correctness does not depend on tombstone retention. Add ID-01 |
| F-05 | Medium | RT-03, ORDER-01/02 | Head-of-line blocking: one poison event N blocks N+1 forever, and "deferred_gap" retries have no bound | Define quarantine: aggregate HOLD with operator-visible state, max wait, no silent skip. Add ORDER-04 (poison event) |
| F-06 | Medium | RT-05, STREAM-01 | "Single-use or stream-scoped capability": single-use breaks resume after a dropped connection; reusable lets a stale worker reuse it | Specify a resumable capability bound to (grant, fence epoch, byte range) that the authority re-issues on each resume and invalidates at takeover. Add STREAM-02 |
| F-07 | Medium | SQLite sections, RACE-01..07 | SQLite BEGIN IMMEDIATE serializes all writers, so race tests pass trivially and cannot detect a flawed CAS. Also "fixed in 3.51.3 and later" includes 3.52.0, which a secondary source says was withdrawn | Run RACE tests with the CAS logic exercised independent of engine serialization (a second engine or forced-busy schedule). Pin 3.51.3 or 3.53.0 and later; record the SQLite version bundled in any Pyodide build. Evidence below |
| F-08 | Low | Section 2.3 Redis | Claim that Redis docs recommend fencing tokens: UNCHECKED by me | Re-verify against the cited page before relying on it |
| F-09 | Low | CRASH-03 | Covers relay crash before mark-delivered; no test for crash between consumer commit and relay mark | Add CRASH-04 |

## Spot checks of VERIFIED claims (2 of about 25)
- SQLite WAL-reset bug: fixed in 3.51.3 (2026-03-13) with backports 3.44.6 and 3.50.7; affects WAL databases with two or more connections writing or checkpointing at the same instant: matches the document [VERIFIED: sqlite.org changes page; a Tailscale-related write-up]. New: 3.53.0 (2026-04-09) also lists the fix. 3.52.0 was withdrawn and 3.51.3 re-released with only the WAL fix [S: one secondary report].
- Everything else in the research section was not re-checked.

## Missing tests (summary)
POLICY-03, IDEMP-01, CLOCK-01, ID-01, ORDER-04, STREAM-02, CRASH-04, and RACE tests that do not depend on single-writer serialization.

## Open decisions this review makes more urgent
Decision 1 (revocation of an in-flight transfer) must be answered before F-01 can be closed; decision 4 (retention) matters less once F-04 is applied.

No code, test or contract was changed by this review.
