# PocketCode — G-07 and G-08 patch-ready test specification

**Status:** Static test/behavior proposal only. NOT IMPLEMENTED; NOT RUN; no PR branch modified.  
**Target:** PR #3 pure helper `scripts/lifecycle_contract.py` and `scripts/test_lifecycle_contract.py`, after explicit authorization and fresh SHA checks.  
**Companion:** [PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md](PURE_TEST_COVERAGE_GAP_AUDIT_20261029.md).

## G-07 — Windows superscript device-name aliases

### Source observation
The portable basename validator uppercases the stem and checks `(?:COM|LPT)[1-9]`. That pattern does not include the Windows-reserved superscript-digit aliases `COM¹`, `COM²`, `COM³`, `LPT¹`, `LPT²`, and `LPT³`. Existing fixtures cover `COM1.csv`, not the superscript aliases. This is a pure name-validation gap; it does not by itself prove path traversal or file-write reachability.

### Test cases
For each of `COM¹`, `COM²`, `COM³`, `LPT¹`, `LPT²`, `LPT³`, assert `canonical_request_fingerprint` rejects the name with `ValueError`. Include extension variants such as `COM¹.txt` and `LPT³.bin` because Windows device-name rules apply even when an extension is present. Retain existing tests for `COM1.csv`, `CON`, `NUL`, path separators, drive-relative syntax, trailing dot/space and Unicode NFC collisions.

### Minimal change recommendation
Extend the reserved device-stem predicate to explicitly include the superscript aliases, e.g. an explicit set membership check after the existing normalization. Do not rely on `int()` conversion or general Unicode numeric normalization without specifying exactly which characters normalize; broad compatibility normalization may unexpectedly rewrite user-provided names.

### Acceptance conditions
- All six superscript aliases are rejected, with and without a filename extension.
- Existing valid names and existing reserved-name behavior remain unchanged.
- Error remains a validation rejection; do not silently rename/canonicalize the submitted name.
- The tests establish only helper-level name validation, not actual filesystem safety.

## G-08 — tombstone repeated-add retention and fingerprint consistency

### Source observation
`DeletionTombstones.add` assigns `(fingerprint, deleted_at + RETENTION_SECONDS)` directly to the tenant/key. A repeated add can overwrite a prior fingerprint and can shorten an existing expiration if the new `deleted_at` is older. Existing tests cover tenant scoping and expiration but not repeated-add behavior.

### Behavior recommendation
Treat a tombstone as a stable record for one tenant-scoped idempotency key:
- Same tenant/key + same fingerprint: idempotent. Preserve the later of existing and proposed expiry; do not shorten retention.
- Same tenant/key + different fingerprint: reject as conflict and leave the original record unchanged.
- Different tenant with same key: independent record.
- Exact expiry boundary remains `now >= expires_at` as currently tested.

This recommendation assumes the tombstone's fingerprint binds the original request identity and should not be overwritten after deletion. If product policy intends key reuse during retention, that is a contract change requiring owner review; do not silently implement it here.

### Required tests
1. Add `(t1,k,f1,deleted_at=100)`, then re-add `(t1,k,f1,deleted_at=50)`; assert lookup remains available until the original later deadline and expires exactly at that deadline.
2. Add `(t1,k,f1,deleted_at=100)`, then re-add `(t1,k,f1,deleted_at=200)`; assert the expiry is not shortened and the chosen extension policy is deterministic. Under the recommendation above, expiry becomes the later deadline.
3. Add `(t1,k,f1,...)`, then attempt `(t1,k,f2,...)`; assert a documented conflict exception and that subsequent lookup still returns `f1` until original expiry.
4. Add same key/fingerprint for `t2`; assert tenant isolation.
5. Keep existing expiry tests at deadline minus one, exact deadline, and deadline plus one.
6. Confirm invalid `deleted_at` inputs (bool, negative, non-int) continue to reject.

### Acceptance conditions
- Repeated add cannot replace the request fingerprint for a live tombstone.
- Repeated add cannot shorten an existing retention deadline.
- Conflicting add does not mutate the stored record.
- Expiration remains deterministic at the exact deadline.
- Document that this is an in-memory pure model, not durable retention or a cross-process concurrency guarantee.

## Patch discipline and verification

1. Re-fetch the exact PR #3 source and test blob SHAs before any patch. Current prior-audit pins: `scripts/lifecycle_contract.py` = `ba8d4d0b217c90513bed020e298029ef4e16f164`; `scripts/test_lifecycle_contract.py` = `39db87d9f44f5e8474f33cff60136e529364199a`.
2. Keep G-07/G-08 in a separate small commit from G-01..G-03 unless the owner explicitly approves a combined patch. Their semantics differ (portable filename rejection vs tombstone lifecycle).
3. Add tests before or alongside the minimal implementation. Run only an authorized local pure unit suite, recording exact command/environment/exit code. Do not trigger Actions or workloads.
4. Inspect diff for changes to canonical acceptance, fingerprint version, idempotency semantics outside tombstones, provider behavior, or deployment.
5. Report source change, test execution and integration proof as separate statuses.

## Provenance and state

Static comparison against the exact source/test blobs pinned above. No code changes, no tests run, no provider/store/runtime selected. PR #2/#3 remain unchanged; canonical acceptance remains unchanged. This document does not constitute owner approval or patch authorization.
