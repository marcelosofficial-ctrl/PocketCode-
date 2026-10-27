# PocketCode — Owner Decision Packet (2026-10-27)

**Purpose:** resolve the minimum product/contract choices needed before writing deterministic offline state-machine/report tests.  
**Status:** selected baseline after owner delegation on 2026-10-27; see the selection record below.  
**Guardrails:** strict $0; no provider, account, workload, paid service, merge, or deployment. PR #3 stays draft; PR #2 stays untouched.

Read with [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md), [DRAFT_EXECUTION_CONTRACT.md](DRAFT_EXECUTION_CONTRACT.md), and [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md).

## Decision 1 — Artifact availability when cleanup is uncertain

**Recommendation:** quarantine all artifacts until cleanup is confirmed and artifact integrity, job ownership, and tenant authorization checks pass. A report may say that output was observed, but must not expose artifact bytes or a live provider URL. A later successful cleanup creates a new report version; it does not rewrite history.

- **Why:** avoids exposing data from an environment that may still be running.
- **Trade-off:** delays useful results after cleanup errors.
- **Tests unlocked:** LIFE-SEM-01/02, ART-SEM-01/03, REPORT-01.

## Decision 2 — Timeout/cancel ordering

**Recommendation:** assign each accepted control-plane event a monotonic coordinator-ingress sequence; terminalization uses one atomic compare-and-set keyed to the job attempt. The first eligible terminal decision in that sequence commits. Keep later/conflicting evidence append-only. Do not use provider timestamps alone to overwrite a committed decision. If ingress order cannot be established, disposition is INCOMPLETE/PROVIDER_ERROR, not PASS.

- **Why:** defines replayable ordering without pretending concurrent callbacks have a universal winner.
- **Trade-off:** whichever eligible event is serialized first wins; it does not impose a universal timeout-over-cancel priority.
- **Tests unlocked:** RACE-SEM-01 through RACE-SEM-04, LIFE-SEM-02.

## Decision 3 — Idempotency key and retention

**Recommendation:** scope keys to authenticated tenant. Same key + same canonical fingerprint returns the existing job/report reference; same key + different fingerprint returns conflict before allocation; explicit rerun creates a new attempt. Retain the key at least as long as any job/report remains addressable, and do not expire a key in a way that can accidentally re-execute a still-addressable request. After deletion, reject reuse or require a new key; never silently bind the key to a new payload.

- **Why:** prevents duplicate execution and cross-tenant result reuse.
- **Trade-off:** storage/retention policy must coordinate with privacy deletion and report retention.
- **Still required before API freeze:** precise canonical fields and a measurable retention/deletion rule.
- **Tests unlocked:** IDEM-SEM-01 through IDEM-SEM-04.

## Decision 4 — Output cap behavior

**Recommendation:** enforce byte caps while streaming; when a hard task-output cap is exceeded, request task termination and continue draining/discarding only as needed to avoid pipe deadlock, within a separately bounded drain/time budget. Mark the attempt LIMIT_EXCEEDED; never PASS. If termination cannot be confirmed, preserve that uncertainty.

- **Why:** avoids unbounded memory and limits runaway work while avoiding blocked pipe writers.
- **Trade-off:** some tasks may be terminated even if their final output would otherwise be useful.
- **Still required before implementation:** concrete byte/time budgets and whether stdout/stderr share an aggregate cap.
- **Tests unlocked:** STREAM-SEM-01, LIFE-SEM-01, limit-boundary cases.

## Decision 5 — Canonical request fingerprint

**Recommendation:** compute the fingerprint server-side over contract/schema version, authenticated tenant namespace, normalized runtime/entrypoint, exact decoded source bytes, normalized input names/media types and exact decoded input bytes, and effective server policy/version. Exclude retry timestamps, transport metadata, and client-supplied fingerprints. Any effective-policy change changes the fingerprint unless the service explicitly documents that the changed field is not request semantics.

- **Why:** ensures retries refer to the same request and policy, not just the same client token.
- **Trade-off:** canonicalization rules must be versioned and stable; equivalent but differently encoded payloads may be different requests unless normalization is explicit.
- **Tests unlocked:** IDEM-SEM-02/03 and policy-version mismatch cases.

## Decision 6 — Execution outcome vs service disposition

**Recommendation:** preserve immutable execution observations separately from derived overall disposition. Overall PASS requires authoritative zero exit, all mandatory policy evidence, no prohibited limit/timeout/cancel/truncation event, validated artifacts, correct tenant association, and confirmed cleanup. A report may be revised only by creating a new version with new evidence.

- **Why:** avoids false PASS when process execution succeeds but cleanup/evidence fails.
- **Trade-off:** external status vocabulary remains more complex than one flat state enum.
- **Still required before API freeze:** final field names, terminal labels, and the allowed reconciliation path from INCOMPLETE to a resolved disposition.
- **Tests unlocked:** LIFE-SEM-01/02, RACE-SEM-03/04, REPORT-01/02.

## Approval record

No choices are approved by this document. Record any owner-approved deviations here before implementing tests:

| Decision | Approved option / deviation | Date |
|---|---|---|
| 1. Artifact quarantine | Selected: quarantine until cleanup, integrity, and tenant/job authorization pass; version reports on recovery | 2026-10-27 |
| 2. Event ordering | Selected: coordinator-ingress sequence + atomic terminalization; ambiguity is non-PASS | 2026-10-27 |
| 3. Idempotency retention | Selected: tenant-scoped key/fingerprint; retain while addressable; 30-day deletion tombstone; new key for rerun | 2026-10-27 |
| 4. Output overflow | Selected: terminate at cap; bounded 1-second drain/discard; no PASS; limits provisional | 2026-10-27 |
| 5. Canonical fingerprint | Selected: versioned server-side canonical request/policy fingerprint over exact decoded bytes | 2026-10-27 |
| 6. Outcome/disposition model | Selected: immutable execution facts, separate cleanup state, versioned derived disposition | 2026-10-27 |

## After approval

1. Update the draft contract and matrix once, using the selected vocabulary and policy.
2. Implement pure offline tests with synthetic events and fake adapters; record exact commands/results only after execution.
3. Keep provider-dependent tests blocked until explicit approval, exact-plan review, vendor consent where required, and a proven $0 spending ceiling.
4. Do not treat offline tests as proof of egress enforcement, process isolation, cleanup, tenant isolation in deployment, or billing.


## Delegated selection status — 2026-10-27

The owner explicitly delegated selection to ChatGPT after reviewing this packet. The six recommended options are selected as the baseline for provider-neutral contract alignment and offline tests. This does not authorize provider use, spending, live execution, production implementation, merge, or deployment. Numeric output limits remain provisional offline-test defaults. Rationale and references will be recorded separately.


**Status clarification (supersedes earlier pending-status wording):** The owner delegated the six choices to ChatGPT on 2026-10-27, and the options in the approval table are selected. The earlier “recommendations only” and “After approval” wording is historical and should not be read as saying the decisions are still pending. The selections authorize only documentation alignment and provider-neutral offline tests; all provider, spend, live execution, production implementation, merge, and deployment gates remain closed.
