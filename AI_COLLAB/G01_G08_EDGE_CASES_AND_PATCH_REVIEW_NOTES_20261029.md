# PocketCode — G-01..G-08 edge cases and patch review notes

**Date:** 2026-10-29  
**Status:** Static source review and proposed test design only. Not owner-approved implementation behavior.  
**Source under review:** PR #3 head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`  
**Source blob:** `scripts/lifecycle_contract.py` = `ba8d4d0b217c90513bed020e298029ef4e16f164`  
**Test blob:** `scripts/test_lifecycle_contract.py` = `39db87d9f44f5e8474f33cff60136e529364199a`

This note adds implementation-level edge cases to the consolidated decision packet. It does not authorize a patch. Re-fetch the branch and both blobs before any future change.

## Source-confirmed observations

1. `derive_disposition()` checks `contradictory_evidence`, then `NOT_STARTED`, then evaluates `execution_outcome == "LIMIT_EXCEEDED" or limit_violated or output_truncated`. The two flags are type-hinted `bool` but are not runtime-validated. A truthy malformed value can select LIMIT_EXCEEDED. If strict validation is approved, validate both flags before any disposition branch so malformed input cannot be masked by early returns.
2. `OutputBudget.__init__()` only checks `cap <= 0`. Since `bool` is an `int` subtype and floats can compare to integers, `True` and positive floats can pass initial validation. Numeric strings can fail later with a less-local TypeError. Constructor validation should be exact and deterministic.
3. `canonical_request_fingerprint()` initially checks that required identity fields are nonempty strings, then normalizes `runtime` using `runtime.strip().lower()`. A whitespace-only runtime is truthy at the first check but normalizes to an empty string in the fingerprint document. Reject blank-after-strip without altering valid nonblank normalization or other fingerprint fields.
4. `_canonical_input_name()` rejects `COM1` through `COM9` and `LPT1` through `LPT9` via regex but does not include Windows' superscript-digit aliases `COM¹/²/³` and `LPT¹/²/³`. Use an explicit additional set or exact alternation; do not generalize all Unicode numeric characters into device aliases.
5. `DeletionTombstones.add()` unconditionally overwrites `(fingerprint, expiry)` for a tenant/key. This confirms the proposed repeated-add concern. The API accepts `deleted_at`, not a separate current-time value, so the expired-key-reuse case needs an explicit rule before coding.

## Additional test details and semantic traps

### G-01 — validation precedence

Proposed tests should pass each malformed flag with ordinary `EXIT_ZERO`, with `NOT_STARTED`, and with `contradictory_evidence=True`. If the selected contract is “invalid helper arguments raise TypeError,” each malformed flag must raise regardless of the outcome branch; otherwise early returns create outcome-dependent validation.

Valid boolean behavior must be separately regression-tested, including both flags false and each flag true. This is validation, not a recommendation to change the existing valid-value mapping of truncation/limits. D-01 still governs the eventual semantics of valid limit-caused termination.

### G-02 — exact integer boundary

Use `type(value) is int` or an equivalent check that explicitly excludes bool. Test both cap parameters independently with:
- valid positive integer and default values;
- `True`, `False`;
- positive float such as `1.5`;
- numeric string such as `"10"`;
- zero and negative integer.

Recommended exception split remains `TypeError` for unsupported types and `ValueError` for integer values <= 0. Preserve any existing supported minimum cap unless the owner explicitly changes that rule.

### G-03 — identity normalization boundary

Test whitespace-only values independently for contract version, tenant ID, runtime, and entrypoint. Add a regression assertion that a nonblank runtime such as `" Python "` still fingerprints exactly as the existing `"Python"` behavior does under `strip().lower()`. Do not trim tenant ID, contract version, or entrypoint as a side effect; this proposal only rejects blank-after-strip values. Keep fingerprint version 1 unless a separate schema decision says otherwise.

### G-07 — explicit portable-name fixtures

Test each of `COM¹`, `COM²`, `COM³`, `LPT¹`, `LPT²`, `LPT³`, plus extension forms (for example `COM¹.txt`) and relevant casing variants. Also retain ordinary safe names and existing `COM1`/`LPT1` cases. This is helper-level portability coverage, not proof of filesystem behavior on every target OS.

### G-08 — tombstone retention and key reuse (OWNER CHOICE REQUIRED)

Minimum tests:
1. Add key/fingerprint at t=100; re-add same fingerprint at t=90. Expiry must not move earlier.
2. Add same fingerprint later; decide whether expiry is preserved as the maximum of the existing deadline and new deadline, or whether repeated add is a strict no-op.
3. Re-add a different fingerprint before expiry: raise `IdempotencyConflict` (or a separately documented conflict exception) and leave the original record byte-for-byte unchanged.
4. Repeat identical operations in another tenant: tenant isolation remains.
5. Add a different fingerprint after the old deadline, without calling `lookup()` first. Decide whether `add()` may replace the expired tombstone. The current API has no `now` parameter: `deleted_at` may be event time rather than the actual time this new tombstone is accepted. Therefore it is unsafe to assume `deleted_at >= old_expiry` proves that the old tombstone has expired *now* unless the contract guarantees monotonic, trusted event time. Options are (a) keep add pure and explicitly define the supplied timestamp as the authoritative ordering clock, (b) pass a trusted `now`/acceptance time into the model, or (c) require callers to perform an expiry check before add. Pick one before implementation.
6. Keep lookup expiry exact: `now >= expires_at` means expired.

**Important distinction:** “A conflicting fingerprint cannot overwrite a live tombstone” is not the same as “a key can never be reused after retention expires.” Do not accidentally implement the latter because expired records are only lazily deleted by `lookup()`. The current API also needs an authoritative time basis to distinguish expired from live during `add()`. The repository already defines `IdempotencyConflict` for tenant-scoped key reuse with a different request; prefer reusing that exception for a live tombstone conflict rather than inventing a parallel exception type.

### Non-goals

- No provider, durable-store, coordinator, or cross-process guarantees.
- No change to canonical LOOP/CASE acceptance or event schema.
- No assertion that pure helper behavior proves runtime enforcement, authentication, race safety, or artifact-release security.

## Recommended review order

1. Owner explicitly chooses G-01..G-03 validation/error behavior.
2. Owner explicitly approves G-07 filename portability behavior.
3. Owner resolves G-08 live-conflict, expiry, and later-repeat semantics before implementation.
4. Re-fetch current PR #3 source/test pins; implement only authorized IDs; add tests; run only the explicitly authorized local pure suite if an execution environment is available.
5. Record source edit, test execution, and integration proof separately.

No source or test file was changed, and no tests were run in creating this note.
