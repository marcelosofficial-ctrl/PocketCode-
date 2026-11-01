# PocketCode — Independent Adversarial Review of the Unified Coordinator Specification

**Date:** 2026-11-01  
**Status:** Static design review / proposed clarifications only. NOT IMPLEMENTED / NOT RUN.  
**Baseline:** `AI_COLLAB/UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md` blob `51edbb9bd1e3f3518b0e80620be9c0ebe88f49ab`; branch head observed as `c6c1ebde744cbd2ac7bf2869c3923d14185cca84`.  
**Scope:** Adversarial review of concurrency, stale workers, delayed external calls, event ingress, cancellation, publication and transfer. This review does not select infrastructure, alter canonical acceptance IDs, close owner decisions, authorize implementation or claim any test passed.

## 1. Executive verdict

The unified specification is a strong baseline and correctly states that leases are not fences, provider calls are not transactionally covered by a database epoch, and ambiguous outcomes must remain UNKNOWN. The review found several races that should be made explicit before a coordinator implementation is designed.

The most important additional point is:

> A fencing epoch protects coordinator state only when every state mutation checks it atomically. It cannot revoke a previously issued external-call capability, stop a delayed network request from reaching a provider, or make two concurrent operations from the same epoch serial.

The specification already requires both epoch and expected state/version for coordinator mutations. This review sharpens the implementation contract and adds missing failure-injection cases. These are proposed extensions, not canonical acceptance IDs.

## 2. Findings

### ADV-01 — Fencing epoch alone does not serialize same-epoch operations

**Scenario:** Worker A owns epoch 12. Two concurrent tasks in A both read state version 40. One commits a transition to version 41. The other still presents epoch 12 and attempts a different mutation based on version 40.

**Risk:** If a store checks only the current epoch, both operations may be accepted. A monotonic worker epoch fences old owners, but does not order concurrent writes by the current owner.

**Required contract:**
- Every mutation uses an atomic compare-and-swap over at least `tenant + job + attempt + epoch + expected state/version`.
- State version advances monotonically for every accepted mutation, or an equivalent serialized transaction/aggregate revision is enforced.
- Operation-specific idempotency is checked in the same transaction as the state change.
- A retry with the same operation identity and same immutable content returns the original result; same identity with changed content returns a typed conflict.
- No read-check-write sequence split across transactions may be described as fencing.

**Proposed test:** `CAS-01`: launch two distinct same-epoch mutations from the same expected version. Exactly one may commit; the loser must receive a typed version conflict and reconcile from the committed state. Repeat with identical operation identity/content and with identical identity/changed content.

**Proof:** Persistence concurrency (G3), not a fake-only result.

### ADV-02 — A committed dispatch authorization can be delayed before the provider call

**Scenario:** A owns epoch 21 and commits a dispatch intent. It receives a valid authorization to call Start, then pauses before sending the request. Its lease expires. B takes epoch 22. B queries the provider and receives a transient not-found. A resumes and sends its already-authorized Start request.

**Risk:** Rejecting A's later database writes does not stop its network request. The external side effect can happen after B's takeover. “Start only after a committed authorization” is necessary but not sufficient unless the authorization's external-use semantics are also addressed.

**Required contract:**
- Model provider Start as an independently identified external side effect with an immutable dispatch-intent ID and provider token.
- B must not create a replacement attempt/token merely because A is stale or a lookup currently says not-found.
- The provider contract must guarantee same-token concurrent/delayed requests converge to one operation, or provide a stronger provider-side conditional/fencing mechanism.
- If neither provider guarantee exists, no automatic takeover may issue Start. Keep the attempt UNKNOWN and require authoritative reconciliation/manual handling.
- If a dispatcher/outbox is used, document its at-least-once delivery semantics. A single dispatcher process or database outbox does not by itself prove exactly-once provider execution.
- Any authorization token for external dispatch must be bound to the one immutable intent, attempt, request fingerprint, policy revision and provider token. Its local expiry is not proof that a request already in flight or queued cannot arrive later.

**Proposed test:** `DISPATCH-01`: pause A after authorization but before network send; let B take over and reconcile; resume A. Assert that no new provider token/attempt is created, and all possible Start requests converge to the original provider operation or remain UNKNOWN. Repeat with delayed request arriving after a transient not-found.

**Proof:** Provider integration (G4). Fake call-order tests cannot prove the delayed network request is prevented.

### ADV-03 — Cancellation is another ambiguous external operation, not terminal evidence

**Scenario:** Coordinator sends Cancel, times out, and marks the job cancelled. Provider continues running, or cancellation was never received.

**Risk:** Treating a cancellation request/acknowledgement as proof of termination can release resources or artifacts while execution continues. A cancellation race can also produce a successful terminal result after cancellation was requested.

**Required contract:**
- Distinguish `cancel_requested`, `cancel_acknowledged`, `cancel_effective` and authoritative terminal observation.
- Give cancellation its own stable operation ID/token, scope, idempotency and lookup/reconciliation rules.
- Cancellation acknowledgement alone must not establish that the provider process stopped.
- Preserve late terminal evidence after cancellation; derive final disposition from the contractually authoritative event set.
- If cancel outcome is ambiguous, retain RUNNING/UNKNOWN (or a distinct cancellation-pending state) until reconciled.

**Proposed test:** `CANCEL-01`: provider accepts Cancel but continues execution; then emits success. Ensure no early terminal projection, cleanup claim or release. `CANCEL-02`: Cancel acknowledgement is lost and retry uses the same cancel identity.

**Proof:** Fake coordinator plus provider lifecycle integration (G2/G4).

### ADV-04 — Event ingress identity and event ordering need separate namespaces

**Scenario:** A provider emits sequence 5 for operation X and sequence 5 for operation Y, or retries the same source event ID with altered payload. A worker-delivered event is accepted after takeover.

**Risk:** A provider sequence may be per operation, per stream, per region or merely advisory. It cannot be assumed globally monotonic. A coordinator-assigned sequence is a different authority. Duplicate source identity with changed content is a security/integrity conflict, not a harmless duplicate.

**Required contract:**
- Define source event identity scope explicitly: provider/account/project/region/operation/attempt/source namespace/event ID.
- Bind source event to the authenticated provider operation and internal attempt at ingress, not from worker/client assertions.
- Persist a canonical immutable payload (or canonical bytes) and digest at first acceptance. Reuse of the same source identity with a different digest becomes a retained conflict diagnostic; never overwrite the original.
- Keep provider sequence/cursor separate from coordinator append sequence. Document whether provider ordering is per operation and how gaps, duplicates and out-of-order delivery are handled.
- Assign coordinator ordering only inside the trusted durable ingress transaction; do not interpret it as provider causal order.
- Late authenticated source events remain ingestible independently of the worker epoch. Projection/reconciliation remains fenced by the current epoch and expected state version.

**Proposed tests:** `EVENT-01` same source ID/same bytes replay; `EVENT-02` same source ID/changed bytes; `EVENT-03` same provider sequence across distinct operations; `EVENT-04` event arrives after takeover but before current projection; `EVENT-05` out-of-order and missing provider sequence.

**Proof:** Pure reducer and authenticated ingress, then persistence concurrency (G1/G3/G4).

### ADV-05 — Event-set snapshot and projection commit can race

**Scenario:** Reconciler B reads event-set watermark 100. Event 101 arrives. B computes a terminal projection from 100 and commits after event 101 has been accepted.

**Risk:** A current fencing epoch alone does not guarantee the projection reflects all accepted evidence. A report can be marked final based on a stale event snapshot.

**Required contract:**
- Projection input records an immutable event-set watermark/version (or explicit event IDs/digests).
- Projection commit atomically verifies the current epoch, expected aggregate version and that the selected event-set watermark is still valid for the intended finalization semantics.
- If new evidence arrives before commit, either retry reduction against the new snapshot or persist the projection as explicitly provisional/stale, according to an owner-approved contract.
- Preserve prior projection versions; never silently mutate a previously issued report.
- Define what event types can reopen/revise a terminal projection and how late contradictory evidence is represented.

**Proposed test:** `PROJECTION-01`: inject a new terminal/conflicting event between snapshot read and projection commit. The stale projection must not be represented as current/final.

**Proof:** Persistence concurrency and report-history integration (G3).

### ADV-06 — Orphan-object cleanup can race with publication recovery

**Scenario:** Object write succeeds; manifest commit is delayed. A garbage collector sees an unreferenced object and deletes it while the publication recovery worker is about to reconcile the same publication ID.

**Risk:** Recovery loses the exact bytes needed to complete a publication, or a reused key points at different bytes.

**Required contract:**
- Object writes use immutable object versions and stable publication IDs.
- Staged objects remain private and protected from garbage collection for a documented recovery/retention horizon.
- Garbage collection must atomically verify no pending publication references the exact object version, and use a grace period longer than the maximum supported reconciliation window.
- Never overwrite a staged object at the same key with different bytes.
- A publication recovery operation must verify object version, digest and size before manifest commit.

**Proposed test:** `PUB-03`: pause between object write and manifest commit while GC runs. The object must remain available for the same publication operation, or the publication must remain safely quarantined without exposure.

**Proof:** Persistence plus artifact-store integration (G3/G5).

### ADV-07 — Token-retention horizon must cover the full uncertainty horizon

**Scenario:** Provider dedupe token expires after 24 hours, but a job can run for 72 hours and recovery may be offline for several days.

**Risk:** A retry after token expiry can create a second provider operation even though the original is still active or its state is unknown.

**Required contract:**
- Calculate the required provider-token retention from maximum job lifetime + maximum outage/recovery interval + maximum delayed-request interval + clock/consistency margin.
- If provider cannot guarantee that retention, automatic Start retry is prohibited after the guaranteed window.
- Keep a durable internal tombstone/attempt record longer than provider token retention; internal retention does not recreate expired provider deduplication.
- Define token expiry relative to provider acceptance time, not only local intent creation time.
- Preserve UNKNOWN when the provider's guarantee no longer covers the possible late-arrival window.

**Proposed test:** `TOKEN-05`: delay an authorized Start beyond the provider token retention boundary; ensure no new token/attempt is issued and no false definitive-not-created conclusion is drawn.

**Proof:** Provider contract and persistence (G3/G4).

### ADV-08 — Release authorization cannot revoke bytes already disclosed

**Scenario:** A caller begins a range transfer. Authorization is revoked or artifact quarantine is raised while bytes are already being streamed.

**Risk:** The system cannot recall bytes already sent. A policy saying “revocation immediately stops access” is impossible to guarantee for an in-flight transfer unless the service defines bounded chunks and rechecks before each chunk. Even then, already transmitted bytes remain disclosed.

**Required contract:**
- Define release authorization as either a bounded transfer lease/snapshot or a per-request/per-range check. State exactly when it is evaluated.
- Bind transfer ID to principal, artifact ID, immutable object version, digest, allowed byte range and authorization decision.
- Recheck authorization before each new range/retry. Document that already-sent bytes cannot be recalled.
- Record bytes successfully emitted, not merely bytes requested or server-side read.
- A resumed transfer requires fresh authorization and the same immutable object version/digest; do not resume against a mutable path.
- Define whether quarantine blocks new ranges immediately and how an in-flight stream is terminated best-effort.

**Proposed test:** `REL-04`: revoke access/quarantine during a multi-range transfer. No subsequent range may begin without fresh authorization; already-sent bytes are recorded and not falsely described as recalled.

**Proof:** Authenticated HTTP/API integration (G5).

## 3. Consolidated additional test inventory

These IDs are proposed additions only and do not replace or renumber LOOP/CASE, DR or COORD acceptance IDs.

| Proposed ID | Main assertion | Required proof |
|---|---|---|
| CAS-01 | Same-epoch concurrent writes use expected-version CAS | G3 |
| DISPATCH-01 | Delayed authorized Start after takeover cannot create a second operation | G4 |
| CANCEL-01/02 | Cancel request/ack is distinct from effective termination; retries are idempotent | G2/G4 |
| EVENT-01..05 | Source identity, payload digest, sequence scope and late ingress are explicit | G1/G3/G4 |
| PROJECTION-01 | New event arriving during reduction prevents stale final projection | G3 |
| PUB-03 | GC cannot delete an object still inside publication recovery horizon | G3/G5 |
| TOKEN-05 | Token retention covers delayed Start and maximum uncertainty horizon | G3/G4 |
| REL-04 | Revocation/quarantine during transfer blocks later ranges but does not claim to recall sent bytes | G5 |

## 4. Required amendments to the unified specification

Before implementation design is frozen, update these clauses:

1. **Section 5 / 11:** State explicitly that epoch + expected aggregate version + operation identity must be checked atomically. Epoch alone is insufficient for same-worker concurrency.
2. **Section 5 / 6:** Add delayed authorized Start after takeover as a distinct race. A committed authorization cannot revoke a request already queued or delayed. Require provider convergence for same original token, or stop at UNKNOWN.
3. **Section 4 / 5:** Add cancellation as a separately identified external operation; request/acknowledgement is not terminal proof.
4. **Section 4 / 7 / D-04:** Define provider source-event identity, immutable payload digest, provider sequence scope and coordinator append sequence separately.
5. **Section 4 / 7:** Add event-set watermark/CAS to final projection to prevent a newly accepted event being omitted by an older reduction snapshot.
6. **Section 4 / 7:** Add publication-aware object garbage-collection grace/coordination.
7. **Section 6:** Define the token retention horizon from the full job/outage/delayed-request uncertainty window.
8. **Section 7 / D-07:** State explicitly that transfer revocation cannot recall bytes already sent; define range-boundary authorization and transfer accounting.

## 5. Priority and disposition

**P0 before coordinator implementation:** ADV-01, ADV-02, ADV-04, ADV-05. These affect whether duplicate execution, stale evidence or stale terminal/report projections can occur.

**P1 before provider/artifact integration:** ADV-03, ADV-06, ADV-07, ADV-08. These affect cancellation correctness, recovery liveness, dedupe expiry and release guarantees.

This review does not close D-04, D-05, D-06, D-07 or D-08. It does not establish that a provider or persistence store can satisfy these contracts. The proposed cases remain NOT RUN. No source code, canonical acceptance IDs, PR #2/#3, workflows, provider accounts, workloads, billing, merge or deployment were changed or used.

## 6. Next step

Have Gemini independently challenge this review and the unified specification, especially ADV-02 (delayed Start after takeover) and ADV-05 (event-set snapshot race). Have Claude translate accepted requirements into an implementation-neutral state-transition/API sketch only after owner decisions are recorded. Keep their outputs separate until reconciled; neither review should modify source or close owner decisions by assumption.
