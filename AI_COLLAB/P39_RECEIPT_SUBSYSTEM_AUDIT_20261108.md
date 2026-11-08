# Receipt subsystem and durable-adapter audit (source pin 744cb4d)

**Date:** 2026-11-08  
**Scope:** Focused line-range audit of scripts/result_receipts.py, scripts/test_result_receipts.py and AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md. This closes the explicit read gap in Claude's P39 review; it does not imply the durable adapter exists.

## 1. Immutable evidence pins

| File | Blob SHA | Scope read |
|---|---|---|
| scripts/result_receipts.py | 0d1588f8590b57e0bf7447c7d5c519186ff0f39d | lines 1–760, focused sequential ranges |
| scripts/test_result_receipts.py | d1f3546d15a6f5473b9a8eda43ea7a1fee0bca7c | lines 1–~780, focused sequential ranges |
| AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md | 413d866a2137cff01c0d35d0668fbd3420640755 | lines 1–280 |

Source/test SHA: 744cb4dc7cd4994647c84ac7476d0c78a21f0540. No source code or tests changed; no tests were executed in this audit.

## 2. What the receipt model does establish

**VERIFIED at the pinned source:**

- Artifact staging computes SHA-256 from immutable bytes and records byte length, object version, effect/attempt binding, integrity state and quarantine (result_receipts.py:31-48, 378-414). Partial writes and mismatched reported digests are quarantined.
- Receipt creation hashes a canonical JSON representation of revision identity, execution/collection/lifecycle/cleanup facts, evidence refs/digests, full artifact manifest, uncertainties and predecessor/revision metadata (431-518). The resulting receipt_sha256 is stored in immutable ResultReceipt.
- Receipt revisions are append-only within the in-memory store. A revision key with identical canonical content replays; changed content conflicts. New versions must extend the current latest predecessor for the exact effect/attempt and cannot fork (477-518; tests for immutable replay, predecessor, fork and history preservation).
- Artifact release checks exact receipt/artifact/object-version/attempt binding, latest receipt, manifest membership, operation scope, authorization flags/revocation/expiry, quarantine and actual staged bytes digest/length before returning bytes (526-612; tests in test_result_receipts.py:181-~440).
- Release-grant idempotency is scoped by principal + tenant + request key. Fingerprint binds exact receipt/artifact/object version/attempt/current attempt/scope and operation, but excludes rotating authorization ID, policy revision, expiry and allow/revocation snapshot (result_receipts.py:181-274). Tests verify refreshed-authorization replay and changed-intent conflict.
- A lost reservation response can recover the same grant after a receipt successor. The existing test verifies grant identity and original receipt pin, then resumes and completes the same logical transfer (test_result_receipts.py:500-~780).
- Publication attempts are append-only, scoped by receipt/destination/idempotency key, and retrying a failed copy with a new key records a real second attempt (result_receipts.py:613-660; tests around lines 200-300).

**Important correction to RG-O2 scope:** the claim that "the receipt model has no receipt hash/artifact digest/quarantine field" is false if applied to ResultReceiptStore. This model has receipt_sha256 and artifact manifest entries with SHA-256, integrity state and quarantine. Claude's RG-O2 specifically concerns the separate compact ReceiptHead in release_grant_conformance.py, not the richer receipt subsystem. Whether the compact head must duplicate the full receipt/artifact digest is a contract-design question; the canonical receipt ID/version may already reference immutable content. Do not mechanically add duplicate fields without deciding the binding requirement.

## 3. Gaps and boundaries confirmed

### RCP-01: process-local identities/sequences are not restart-safe

**VERIFIED model limitation, not production proof.**
- Receipt IDs are generated as receipt-{len(self._receipts)+1} (result_receipts.py:509-517).
- Release-grant IDs are generated as release-grant-{len(self._release_grants)+1} (251-263).
- Release-grant event numbers are generated from the in-memory event-list length (184-193).
- A fresh ResultReceiptStore starts with empty lists/maps, so independent instances can issue the same receipt/grant IDs and event numbers. This is the same identity-continuity class as Claude RG-H4 in the separate ReleaseGrantContractModel, and applies here too.
- Add P39-ID-02: prove unique IDs and non-resetting sequence/fence authority across independent instances, restart, restore and migration. Random IDs need durable uniqueness/collision handling; sequence/fence continuity needs an authority outside deletable rows.

### RCP-02: transfer resume has no current-policy gate in the model API

**VERIFIED interface limitation; production behavior UNKNOWN.**
- reserve_release() validates the authorization object's primitive types and stable-intent binding, then returns an existing grant before calling release_artifact() for a fresh authorization decision (199-249).
- This is intentionally correct for idempotent recovery: replay must return the original grant and must not create a second grant or reinterpret it against a newer receipt. It does not itself authorize bytes.
- However, start_release_transfer() and record_release_progress() accept only grant ID/time/progress, with no refreshed policy decision, authorization epoch, owner/fence or cancellation authority (276-333). A resumed transferring grant is returned unchanged.
- The docs state that idempotency lookup alone does not authorize bytes and that recovery applies an explicit revocation/cancellation policy, but the sequential API does not encode the policy gate. Treat this as a known model/adapter boundary requiring explicit design, not proof of a production bypass.
- Before any adapter can resume bytes, it must authenticate the caller, check the selected current-policy rule and current grant/fence, and reissue a stream capability bound to grant/fence/object version/operation/range. Add P39-POLICY-06 for retry/resume after revocation and P39-STREAM-04 if streaming is in MVP. Keep existing P39-POLICY-02..04 semantics distinct.

### RCP-03: timestamps and completion observations are caller supplied

The receipt/grant model accepts created_at_ms, now_ms and observed_at_ms as function arguments (199-275, 276-360, 431-455, 526-612). Monotonicity checks prevent some backwards movement but do not establish trusted time. This mirrors RG-B3's lease-time issue, although receipt/grant timestamps do not all have lease semantics. Durable adapter must assign trusted observation/commit times; worker timestamps may be retained as untrusted occurrence claims. Add to the adapter contract, not a new verdict rule.

### RCP-04: progress/completion does not prove client receipt

record_release_progress() stores a caller-supplied byte count; complete_release_transfer() compares a caller-supplied digest to the stored artifact digest and full recorded length (304-360). The model does not observe transport acceptance, actual emitted bytes, client-observed bytes or client acknowledgement. This is explicitly disclaimed in T9 and matches the P39-S4/S8 transport boundary. Never describe completed in this reference model as cryptographic proof that the client received the bytes.

### RCP-05: no concurrent/durable evidence

The model uses in-memory dictionaries/lists and sequential method calls. Tests use one ResultReceiptStore instance and do not establish independent-connection/process races, transaction isolation, rollback, crash atomicity, restore safety or durable uniqueness. The durable adapter contract correctly requires two-process reservation races, concurrent receipt revision, release-grant/revision race, crash injection, restart, backup/restore and exact storage/runtime version recording (§§3–7). All such production-adapter behavior remains UNKNOWN / NOT RUN.

## 4. Test coverage reconciliation against Claude's RG-O1..O4

| Claude finding | Receipt subsystem result | Reconciliation |
|---|---|---|
| RG-O1 receipt ID reuse in release_grant_conformance.advance_receipt_head() | This is a separate compact-head model. ResultReceiptStore.create_receipt() generates its own IDs and rejects chain forks/revision-key reuse within one instance, but IDs reset across fresh instances. | CONFIRMED for the compact-head model by Claude; distinct restart identity issue RCP-01 here. Do not conflate reusing a historical receipt ID as successor with process restart reissuing a generated ID. |
| RG-O2 missing receipt hash/artifact digest/quarantine in ReceiptHead | Rich ResultReceiptStore has receipt_sha256 and artifact manifest digest/integrity/quarantine. Compact head lacks these fields. | NARROW / NEEDS CONTRACT DECISION. Not a subsystem-wide absence. Decide whether compact head must carry digest or whether immutable receipt reference is sufficient and verified at reservation. |
| RG-O3 stable fingerprint/client intent | The receipt subsystem fingerprint binds exact immutable receipt/artifact/object/attempt/scope, excludes rotating auth proof metadata, and replay returns original grant before latest-head check. | SUPPORTED by model tests. Research recipe still must state replay-before-new-head order and that replay does not authorize more bytes. |
| RG-O4 pinned grant assertion | The receipt subsystem end-to-end recovery test re-reads grant through get_release_grant() after receipt successor and compares to the partial grant; it also completes the same grant. | No analogous defect found in this subsystem. Claude's finding remains specific to the separate release_grant_conformance test and must be fixed there. |

## 5. Additional precise test/contract work

- P39-ID-02: receipt/grant/event identities and fence/observation sequence survive new store instance, restart, backup restore and migration without reuse.
- P39-POLICY-06: a recovered grant after policy revocation is not resumed until the selected current-policy check passes; idempotent lookup alone never authorizes bytes.
- P39-STREAM-04: if streaming is in MVP, old stream capability is rejected after takeover/revocation and resume receives a newly scoped capability.
- P39-TIME-01: durable observation/commit time comes from the trusted authority, not worker/caller time; preserve untrusted occurrence timestamps separately.
- P39-RECEIPT-02: decide and test whether compact ReceiptHead must bind receipt digest and artifact digest/quarantine, or whether a validated immutable receipt reference suffices.
- Extend adapter crash/race tests from T7/T9/T9A: receipt successor vs release-grant commit must serialize; two different processes must not fork a revision chain; a lost commit response recovers the same grant; rollback/restore cannot reuse receipt/grant identity or fence epoch.

## 6. Overall disposition

The receipt subsystem is a comparatively detailed sequential model: it covers immutable receipt revisions, digest-verified artifacts, quarantine, latest-receipt release gating, stable-intent idempotency, grant recovery, transfer state and publication retries. It does not prove durable or concurrent behavior. Claude's RG-O2/O4 findings are narrower than a general reading might suggest; RG-O1 applies to the other compact-head model. New actionable gaps are restart-safe identity, policy-gated transfer resume, trusted time and the distinction between server-recorded progress and client receipt.

**Verification:** source/test blobs were pinned and read in bounded ranges. No source/test code changed; no test command was run. No database, runtime, provider, broker or transport was selected.
