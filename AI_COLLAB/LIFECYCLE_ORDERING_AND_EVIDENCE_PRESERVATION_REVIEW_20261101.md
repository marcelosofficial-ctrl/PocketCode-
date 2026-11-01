# PocketCode — Lifecycle Ordering and Evidence-Preservation Review

**Date:** 2026-11-01  
**Status:** Static design review / proposed clarifications only. NOT IMPLEMENTED / NOT RUN.  
**Baseline:** `AI_COLLAB/UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md`, blob `51edbb9bd1e3f3518b0e80620be9c0ebe88f49ab`.  
**Purpose:** Check the proposed durable state machine and transaction order for evidence loss, unnecessary mandatory branches and ambiguous release/transfer semantics. No canonical acceptance IDs are changed and no implementation is authorized.

## 1. Verdict

The proposed state machine preserves many important distinctions, but its current linear presentation leaves three lifecycle hazards insufficiently specified:

1. It places `CLEANUP_PENDING` before `OUTPUT_COLLECTING`, although cleanup may destroy the workspace, temporary files, process logs or provider-side artifacts needed for collection.
2. It presents artifact preparation/publication as a continuation after every committed report, despite the existing contract allowing successful artifact-free tasks.
3. It uses `RELEASED` for an authorized object released to a caller, while separately requiring transfer completion to be recorded and partial transfers not to be called complete. Authorization, first-byte disclosure, transfer completion and caller verification are distinct facts.

These are not proof that the implementation is wrong. The state names and ordering are illustrative, but the ambiguity must be removed before they become implementation/API semantics.

## 2. LIFECYCLE-01 — Collection can be ordered after destructive cleanup

**Baseline location:** Unified specification Section 3 rows `CLEANUP_PENDING` and `OUTPUT_COLLECTING`; Section 4 boundaries H and I.

**Scenario:** Provider execution reaches terminal state. Coordinator enters cleanup and deletes the execution workspace or ephemeral container. Output collection then begins, but the expected files, stdout/stderr spool, process metadata or workspace snapshot no longer exists.

**Impact:** The system may report missing evidence as an empty output, classify a complete execution as incomplete, or be unable to produce artifacts that were present before cleanup. The phrase “cleanup” is too broad to establish safe ordering.

**Required clarification:**
- Split cleanup into at least two semantic categories:
  - **Execution/runtime finalization:** confirm the process/job is terminal, revoke further execution authority, stop billable compute where appropriate, and preserve a stable readable snapshot or provider-side output reference.
  - **Destructive workspace/resource cleanup:** delete ephemeral resources or data that could contain evidence.
- Require the output contract to specify where each required output lives, how long it remains available, and whether collection is possible after runtime finalization.
- If collection depends on a live workspace, collection/snapshot must precede destructive cleanup.
- If provider guarantees immutable retained outputs independently of the workspace, that guarantee must be documented and tested before cleanup can precede download.
- Do not use cleanup success as a proxy for evidence completeness. Do not use evidence completeness as a proxy for successful cleanup.
- Model the two facts independently and retain separate operation identities and recovery paths.

**Proposed ordering (conditional, not universal):**

`TERMINAL_EVIDENCE_ACCEPTED` → `EXECUTION_FINALIZATION_PENDING` → `OUTPUT_SNAPSHOT_OR_COLLECTION` → `EVIDENCE_SET_VALIDATION` → `DESTRUCTIVE_CLEANUP_PENDING` → `DESTRUCTIVE_CLEANUP_CONFIRMED`

The exact order may differ if the provider has a proven durable output snapshot. The invariant is that no destructive action may remove the only copy of required evidence before it is durably captured.

**Proposed tests:**
- `LIFE-01`: cleanup deletes workspace; assert collection is complete before deletion or fails safely without claiming empty output.
- `LIFE-02`: output snapshot is durable, then workspace cleanup occurs; restart between both operations and reconcile by stable IDs.
- `LIFE-03`: cleanup acknowledgement is lost after deletion; collection remains bound to immutable snapshot and cleanup reconciliation does not repeat a destructive action unsafely.
- `LIFE-04`: provider output-retention expiry occurs before collection; result becomes incomplete/unknown under the explicit contract, never silently empty.

Proof requires fake call-order tests (G2), then provider/runtime integration and persistence (G3/G4). No fake can establish provider retention.

## 3. LIFECYCLE-02 — Artifact-free jobs need an explicit terminal branch

**Baseline location:** Unified specification Section 3 rows `REPORT_COMMITTED`, `ARTIFACT_PREPARED`, `PUBLICATION_PENDING`, `PUBLISHED`; Section 8 states artifact-free successful tasks can remain valid.

**Scenario:** A successful task is configured to produce no downloadable artifact. Its report is committed. A literal linear interpretation of the state table then expects artifact preparation/publication before reaching a final state.

**Impact:** Implementers may accidentally make artifacts mandatory, block valid jobs indefinitely, create empty/fake artifacts, or conflate report durability with artifact publication.

**Required clarification:**
- Add an explicit per-job artifact expectation, derived from the trusted task contract/case definition, not from whether a worker happened to upload a file.
- Distinguish `ARTIFACT_NOT_REQUIRED`, `ARTIFACT_REQUIRED_PENDING`, `ARTIFACT_PREPARED`, `ARTIFACT_PUBLISHED`, `ARTIFACT_FAILED` and `ARTIFACT_UNKNOWN` (names illustrative).
- If no artifact is required, report commitment may proceed to final job disposition without creating an artifact or release decision.
- If an artifact is required, report PASS alone cannot bypass artifact evidence requirements; the contract must say whether artifact failure changes job disposition or only artifact availability.
- Do not infer “not required” from an empty artifact list unless the trusted task contract says it is optional.

**Proposed tests:**
- `LIFE-05`: successful artifact-free job commits report and reaches its valid terminal disposition without object/manifest/release calls.
- `LIFE-06`: artifact-required job has no artifact; report outcome and artifact status remain separate and the agreed policy is applied.
- `LIFE-07`: unexpected artifact appears for artifact-free job; it is not automatically published or released.

Proof: G1 contract tests and G2 fake coordinator call-count assertions; later G5 for actual publication.

## 4. LIFECYCLE-03 — Authorization, disclosure and transfer completion are different events

**Baseline location:** Unified specification Section 3 `RELEASED`; Section 4 boundaries M/N; adversarial review ADV-08.

**Scenario:** The service authorizes a download and sends the first bytes. The client disconnects. Alternatively, the service streams all bytes but the client never verifies the digest or persists the file. A later retry resumes a range.

**Impact:** “Released” can ambiguously mean authorized, made available, first byte sent, all bytes sent, or successfully received and verified by the client. These claims have different evidence requirements.

**Required clarification:**
- Separate at least:
  - `RELEASE_AUTHORIZED`: policy decision permits a particular principal to access a particular immutable object version under a defined scope.
  - `TRANSFER_STARTED`: first byte was emitted by the service; this is already a disclosure event.
  - `TRANSFER_PARTIAL` / `TRANSFER_ABORTED`: fewer than the expected bytes were emitted or delivery ended ambiguously.
  - `TRANSFER_SERVER_COMPLETE`: service emitted the expected byte count for the bound object version. This does not prove client persistence or digest verification.
  - `CLIENT_VERIFIED`: only if the client explicitly returns a verifiable digest/receipt and the protocol defines its trust level. Do not assume this from HTTP success.
- Bind each transfer to a stable transfer ID, principal, release decision, immutable object version/digest, byte range and authorization policy revision.
- Every resumed request is a new authorization check and a continuation of the same immutable artifact identity, with a clear new transfer-attempt ID or range identity.
- Preserve the bytes-sent accounting even if authorization is revoked mid-stream. Already disclosed bytes cannot be recalled.
- Avoid the word `RELEASED` as a terminal transfer result unless its meaning is defined narrowly. Prefer a release-decision state plus independent transfer state.

**Proposed tests:**
- `LIFE-08`: authorization succeeds but no byte is sent; record authorization only.
- `LIFE-09`: disconnect after partial bytes; never record server-complete.
- `LIFE-10`: server emits all bytes but client receipt is absent; do not claim client-verified.
- `LIFE-11`: resumed range is requested after authorization revocation; deny new bytes, retain previous disclosure accounting.
- `LIFE-12`: same transfer retry changes object version/digest; reject.

Proof: G5 authenticated HTTP integration. Client verification requires a defined client receipt protocol and cannot be inferred from server logs.

## 5. Additional state-machine contract recommendations

Before freezing a coordinator API, define:
- Whether execution finalization and destructive cleanup are separate operations.
- A trusted per-task artifact expectation, including required/optional/not-applicable semantics.
- The independent state machines for job disposition, report version, artifact publication, release authorization and transfer.
- Which state is the aggregate's authoritative terminal state and which are subordinate lifecycle records.
- How each independent state is correlated by immutable job/attempt/evidence IDs without collapsing their meanings.
- Whether a report can be committed before destructive cleanup, and what evidence is required to make that report final versus provisional.
- Retention windows for provider outputs, snapshots, event records, reports and staged objects.

A single large linear enum is not recommended if it forces unrelated lifecycles into one sequence. Prefer a small aggregate state plus independently versioned sub-resources or explicitly typed projections, provided cross-resource invariants are enforced transactionally or reconciled safely.

## 6. Proposed additions (not canonical acceptance IDs)

| ID | Fault injection | Required result | Proof |
|---|---|---|---|
| LIFE-01..04 | Output collection versus destructive cleanup and output retention | No required evidence is destroyed before durable capture; ambiguity stays explicit | G2/G3/G4 |
| LIFE-05..07 | Artifact-free, required-artifact and unexpected-artifact paths | No accidental universal artifact requirement or fabricated artifact | G1/G2/G5 |
| LIFE-08..12 | Authorization, first-byte disclosure, partial/server-complete/client-verified transfer | No false completion or recall claim; immutable identity maintained | G5 |

These cases do not replace or renumber LOOP/CASE, DR, COORD, STALE, TOKEN, PUB or REL cases.

## 7. Priority

**P0 before implementation design:** LIFECYCLE-01 and LIFECYCLE-02. They affect evidence preservation and whether valid artifact-free tasks can finish.

**P1 before release/API design:** LIFECYCLE-03. It affects security claims, audit records and transfer correctness.

This review does not close D-01..D-08, select a provider/store, prove runtime retention, authorize source changes or claim any test passed. All proposed cases are NOT RUN. Documentation-only review; no source code, canonical acceptance, PR #2/#3, workflows, accounts, workloads, billing, merge or deployment changed.
