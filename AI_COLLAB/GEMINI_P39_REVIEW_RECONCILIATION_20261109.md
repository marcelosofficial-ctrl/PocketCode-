# Gemini P39 review reconciliation

Date: 2026-11-09  
Reviewer artifact: owner-supplied `AI_COLLAB/GEMINI_P39_INDEPENDENT_REVIEW_20261109.md` (full text supplied in chat; not yet present on the branch at review time).  
Target source/test SHA: `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.  
Method: independent static source reconciliation against the exact GitHub blob pins. No tests executed.

## Executive disposition

**Gemini's report is useful but its four headline findings are not accurate as written.** Two underlying model gaps are supported after correcting the target and mechanism; two are adapter/contract boundaries. Several of the nine secondary claims misidentify modules or describe APIs/fields that do not exist.

The P39/P40 implementation gate remains **CLOSED**. OD-01..OD-13 remain OPEN. No source, tests, PRs, canonical IDs, runtime, provider, database or transport changed/selected.

## Immutable evidence checked

At commit `744cb4dc7cd4994647c84ac7476d0c78a21f0540`:
- `scripts/release_grant_conformance.py` blob `f9107fe46d60bbb5cd7115daf2513cd751221986`
- `scripts/test_release_grant_conformance.py` blob `e3bbe94838807a1f9214042af262a2497c057fd7`
- `scripts/event_journal.py` blob `371a175739b9cb65cd4d59bb4cd5b3c1c4953564`
- `scripts/test_event_journal.py` blob `333cf5ec856d4244c3f84da9e82bb2fa126607b5`
- `scripts/fake_outbox.py` blob `813957e5061d40cba2ebb5e2936edcbac645820b`
- `scripts/test_fake_outbox.py` blob `67951a77f87e9523c9080970068fd158680f23a9`
- Supplemental cross-check, not in Gemini's six-file manifest: `scripts/result_receipts.py` blob `0d1588f8590b57e0bf7447c7d5c519186ff0f39d`.

The supplemental receipt file is explicitly outside Gemini's six-file pin set. Its blob was independently fetched from the same commit for this reconciliation.

## Headline findings

| Gemini finding | Source reconciliation | Disposition |
|---|---|---|
| P39-S1 says `event_journal.py` separately commits aggregate version and outbox | **Wrong module/mechanism.** `event_journal.py` is an in-memory append-only journal with a single local sequence; it has no aggregate version or outbox. A related, real defect exists in `release_grant_conformance.py`: `reserve()` stages grant/event/outbox together at v1, but `record_progress()` increments `aggregate_version` without appending the matching event/outbox. | **ACCEPT WITH CORRECTION, BLOCKING model gap.** Bind every versioned transition to an event/outbox atomically, or separate progress sequence from aggregate event version. No claim of a real database crash was tested. |
| P39-S2 says `result_receipts.py::verify_receipt()` hashes only payload bytes and permits tenant re-binding | **Not supported as stated.** The pinned `result_receipts.py` has no `verify_receipt()`; `create_receipt()` fingerprints a canonical object containing receipt identity, execution/projection fields, evidence references/digests, artifact manifest, uncertainties, timestamp and predecessor metadata. The report's named function and tenant-header exploit do not match this source. A distinct digest defect does exist in `release_grant_conformance.py::consume_event()`: it trusts `GrantEvent.payload_sha256` rather than recomputing a canonical envelope digest. | **REJECT Gemini's receipt claim; ACCEPT corrected consumer-envelope gap, BLOCKING model gap.** Hash all semantic event fields inside the trusted consumer. Tenant/grant/source authorization binding is a separate finding and must not be conflated with digest integrity. |
| P39-S3 says `fake_outbox.py` has no lease/fence | **Contradicted by source.** `FakeOutboxStore.claim()` assigns an incrementing fence and lease expiry; active leases cannot be stolen; stale workers fail `_require_current_lease()`; recovery distinguishes pre-send and post-intent. The actual grant-event outbox in `release_grant_conformance.py` has no relay claim/lease/fence or ordered conditional delivered mark. | **ACCEPT WITH CORRECTION, HIGH model gap** for the grant-event relay; reject the claim about `fake_outbox.py`. |
| P39-S4 says DB fencing cannot terminate open streams | **Correct physical boundary, wrong characterization if called a defect in these models.** The receipt model explicitly says it is synchronous and does not represent in-flight streaming; it calls active-transfer cancellation a separate policy decision. No production transport adapter exists in the pinned source. | **ACCEPT AS ADAPTER/MVP OBLIGATION, NOT MODEL DEFECT.** Owner must decide streaming scope and revocation semantics; if streaming is in MVP, require transport cancellation and client-byte evidence tests. |

## Nine-topic review

1. **Producer identity:** `event_journal.py` requires an `AuthenticatedProducer` supplied by an adapter and explicitly does not verify credentials. This is a real adapter trust boundary, not proof that the model authenticates HMAC/OAuth. Require trusted adapter identity and atomic fence-plus-append in production.
2. **Tenant/grant/source binding:** the grant-event consumer does not establish that an event belongs to an existing tenant-scoped grant/source. Accept as a distinct model gap (Claude RG-B2 / P39-S5 family). Do not describe it as a consequence of a receipt digest re-binding exploit.
3. **Idempotency substitution:** Gemini's `client_request_id` example does not match these APIs. `FakeOutboxStore.reserve()` is keyed by effect/attempt and compares both request fingerprint and immutable request bytes. Release-grant reservation is scoped by principal, tenant and request key, with an immutable intent fingerprint. Changed intent conflicts. Reject the described attack against these targets.
4. **Revocation during export:** the receipt model checks supplied authorization/revocation synchronously at release. Reservation replay returns the original grant but is explicitly not a new byte-release authorization. Revalidation and cancellation during a real asynchronous transfer are adapter/policy obligations; do not infer policy.
5. **Event provenance:** the grant model creates a deterministic grant-version event ID; the journal accepts producer event IDs. A cryptographic parent/root chain is not present, so provenance-chain completeness is a legitimate specification question, but Gemini's claim that IDs are random UUIDs is unsupported.
6. **Ordering/gaps:** `ReleaseGrantContractModel.consume_event()` returns `deferred_gap` for a future version. It does not silently drop it. Durable quarantine, retry and operator-visible poison-gap handling remain adapter/operational requirements.
7. **Lease expiry:** `fake_outbox.py` has lease expiry and fencing. Separately, `release_grant_conformance.py` accepts caller-supplied `now` in worker lease operations. This matches Claude RG-B3: model-oracle defect; production adapter must use authoritative store/coordinator time.
8. **Restore/fence reset:** the Python models are in-memory and do not implement backup/restore. Fence high-water continuity across restore is an adapter durability requirement, not a demonstrated defect in a durable database.
9. **Open streams:** accepted as transport boundary/MVP decision, not as a defect in the sequential reference model.

## Corrected bounded findings and tests

- **P39-EVENT-PARITY-01 (BLOCKING):** progress transition increments aggregate version but emits no corresponding event/outbox. Cover first progress, repeated no-op progress, multiple progress changes and terminal transitions; assert contiguous replayable versions and no-op stability.
- **P39-EVENT-DIGEST-01 (BLOCKING):** consumer trusts caller-provided digest. Mutate grant/version/state/source metadata while reusing digest; reject. Recompute digest over canonical semantic envelope inside trusted consumer.
- **P39-EVENT-BINDING-01 (HIGH):** forged first event for unknown grant or unauthorized source must not be accepted; bind to a real grant and tenant/source authority.
- **P39-RELAY-FENCE-01 (HIGH):** grant-event relay A pauses, lease expires, B claims and delivers, then A's stale mark must fail. Enforce lease, monotonic fence, per-grant version ordering and conditional delivered mark.
- **P39-CLOCK-01 (BLOCKING):** caller-supplied future/backdated time must not steal or extend a lease; use authoritative store/coordinator clock.
- **P39-STREAM-01 (OWNER/ADAPTER):** if streaming is in MVP, revoke between chunks and distinguish bytes accepted, emitted, client-observed and client-acknowledged. Otherwise explicitly defer stream claims.
- **P39-RESTORE-FENCE-01 (ADAPTER):** backup/restore/migration must preserve or safely advance fence high-water marks and prevent stale worker resurrection.

Merge these with existing Claude P39 tests where equivalent; do not duplicate runs or alter canonical LOOP/CASE/D identifiers. Existing Claude reconciliation remains authoritative for its independent C1-C7 results, which were run against a byte-verified copy and not this repository suite.

## Evidence and gate

- Gemini: all listed tests NOT RUN. No live provider, remote sandbox, device or transport tests.
- This reconciliation: static GitHub source reads only; tests NOT RUN.
- Historical Actions 42365455316: 266/266 PASS only at source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- Current documentation HEAD `3cd1b689cb6d37963c2f9eb2005e9a9b834b11c1`: no associated workflow runs returned; CI NOT RUN.
- Owner OD-01..OD-13 remain OPEN. Reviewer recommendations do not authorize implementation.

**Next:** obtain explicit owner decisions; reconcile the corrected event parity/digest/relay findings with the existing Claude dispositions; only then prepare a bounded model-only implementation proposal. No source/test change is authorized by this review.
