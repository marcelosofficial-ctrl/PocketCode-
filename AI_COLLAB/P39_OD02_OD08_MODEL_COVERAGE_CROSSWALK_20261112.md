# P39 OD-02..OD-08 model coverage crosswalk

Date: 2026-11-12  
Status: source-pinned static coverage audit; no implementation or tests executed.  
Authority: `P39_OWNER_DELEGATED_DECISIONS_20261111.md`. This note does not alter OD-01..OD-13, LOOP-01..14, CASE-01..16 or D-IDs.

## 1. Exact source pins

Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`.

| File | Blob SHA |
|---|---|
| `scripts/release_grant_conformance.py` | `f9107fe46d60bbb5cd7115daf2513cd751221986` |
| `scripts/test_release_grant_conformance.py` | `e3bbe94838807a1f9214042af262a2497c057fd7` |
| `scripts/result_receipts.py` | `0d1588f8590b57e0bf7447c7d5c519186ff0f39d` |
| `scripts/test_result_receipts.py` | `d1f3546d15a6f5473b9a8eda43ea7a1fee0bca7c` |
| `AI_COLLAB/P39_OWNER_DELEGATED_DECISIONS_20261111.md` | `a72a4351d97f3723f8aac0b1f66cd400532136cb` |

Both Python modules identify themselves as in-memory/reference models, not durable production adapters or authenticated trust boundaries.

## 2. Policy-to-model coverage

| Decision | Existing model evidence | Remaining gap / disposition |
|---|---|---|
| **OD-02 claim-time authorization** | `ResultReceiptStore.reserve_release()` calls the synchronous `release_artifact()` authorization path before creating a new grant. Tests cover expired/revoked authorization and exact scope. | `start_release_transfer()` takes only grant ID/time; `ReleaseGrantContractModel.claim_worker()` takes only grant/owner/time/lease. Neither rechecks current authorization or policy epoch at the worker-claim boundary. Existing release-request authorization tests do not close this gap. |
| **OD-03 active-transfer revocation** | `record_release_progress()` tracks bounded monotonic byte progress. `cancel_release_transfer()` marks the local model grant cancelled; tests ensure cancelled grants cannot resume/complete. | No transport cancellation call, same-attempt cancellation acknowledgement or emitted-byte boundary exists. A local cancelled state is not proof that an external transfer stopped. Keep in-flight transfer INCOMPLETE until an authoritative acknowledgement model is defined. |
| **OD-04 recovery vs renewed authority** | Reservation replay returns the same grant identity for the same idempotency scope and exact intent; tests cover lost reservation response, refreshed authorization and same-grant interrupted-transfer resume. Reservation returns no artifact bytes. | `start_release_transfer()` and `record_release_progress()` accept no fresh capability/current-policy proof. Recovery identity is represented, but the requirement that every resume/retry needs a new capability bound to current fence, object version, operation and range is not proven. |
| **OD-05 policy epoch at commit** | `reserve()` and `reserve_release()` accept authorization/policy-revision inputs; tests exercise exact operation, receipt and artifact scope. | No independent current-policy authority or linearizable policy-epoch check at the commit boundary is modeled. Caller-supplied `auth_allowed`, `policy_revision` and authorization snapshots are not proof of current authority or race ordering. |
| **OD-06 authoritative time** | Lease/authorization methods validate caller-supplied integer timestamps, expiry and monotonicity. Tests reject malformed/boolean timestamps and backward event time. | APIs receive `now` / `now_ms` as arguments. No adapter-owned authoritative clock, commit timestamp or lease-time source is proven. These tests prove input validation, not clock authority. |
| **OD-07 globally unique restore-safe high-water** | Models use monotonic in-memory counters/fence maps and test worker takeover fencing within one process. | Grant IDs are generated from `_next_grant` or collection length; receipt/event/fence counters are in-memory. No restart, backup restore, collision or high-water rollback proof. |
| **OD-08 exact receipt and artifact content** | `ResultReceiptStore` stores `ResultReceipt.receipt_sha256`; artifact entries include SHA-256, integrity state and quarantine; release checks latest receipt, attempt, object version, authorization, quarantine and actual bytes. Tests cover digest mismatch, quarantine, stale receipt and exact object version. | The separate `ReleaseGrantContractModel.ReceiptHead` carries only IDs/revision/object version/length; `reserve()` does not bind receipt SHA, artifact SHA or quarantine. The 33-case grant plan now adds A8. The Python receipt fingerprint uses `json.dumps(sort_keys=True, separators=...)`; it is not proof of RFC 8785/JCS cross-language canonicalization. |

## 3. Do not conflate the two models

The release-grant conformance model and receipt/transfer model are separate in-memory implementations with different scope:

- `ReleaseGrantContractModel.record_progress()` increments aggregate_version even for equal progress and writes no matching event/outbox. Its P40 grant-event plan addresses parity and relay defects.
- `ResultReceiptStore.record_release_progress()` returns the unchanged grant for equal progress and records no new progress event. It has a different local event list and does not supply the missing P40 grant-event outbox/relay.
- `ResultReceiptStore.release_artifact()` models a synchronous completed release. It explicitly does not model an in-flight stream or active transfer revocation. Its `ReleaseGrant` transfer helpers are separate in-memory state transitions, not a network transport or acknowledgement.
- A passing test in either model cannot be transferred to the other model or treated as adapter/production/CASE acceptance.

## 4. Ranked follow-up after a separate gate

1. If authorized, add model-only cases for fresh claim-time authorization, stale/revoked policy at claim, capability renewal on resume, cancellation request vs same-attempt acknowledgement, policy-epoch commit race, authoritative-clock adapter boundary, restore high-water rollback, and receipt/artifact digest + quarantine binding.
2. Keep effect-dispatch fence, grant transition fence and grant-event relay fence independent.
3. Require full existing scripts suite on the exact new source SHA, with environment and per-case output. Model-only PASS remains distinct from durable adapter, provider, device and CASE acceptance.

## 5. Evidence boundary

- VERIFIED: method signatures, state changes and test names were inspected at the blob pins above.
- INFERRED: the listed gaps are the minimum missing proof for OD-02..OD-08 across these reference models.
- UNKNOWN: production policy service, clock, durable transaction, transport cancellation/ack, identity provider, backup/restore and adapter behavior.
- NOT RUN: all tests in this audit. No source/test files changed, no adapter or infrastructure selected, and the P39 implementation/adapter gate remains CLOSED.
