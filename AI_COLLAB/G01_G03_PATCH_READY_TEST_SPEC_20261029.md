# PocketCode — G-01..G-03 patch-ready test specification

**Date:** 2026-10-29  
**Status:** Proposed change design only. NOT IMPLEMENTED; NOT RUN; no PR branch modified.  
**Target branches:** G-01..G-03 belong on `pocketcode-pass0-audit-2026-10-26` (PR #3) only after explicit authorization and a fresh source SHA check.  
**Research branch:** pocketcode-ai-workflow-director-research-2026-10-28

## Why this packet exists

The coverage audit identified three narrow gaps that can be addressed before provider/store/runtime selection. This document narrows each gap to test cases and behavior choices, to prevent an implementation patch from accidentally changing semantic verdict rules. The source and tests remain as fetched in the prior audit: `scripts/lifecycle_contract.py` blob `ba8d4d0b217c90513bed020e298029ef4e16f164`; `scripts/test_lifecycle_contract.py` blob `39db87d9f44f5e8474f33cff60136e529364199a`. Re-fetch both immediately before any authorized patch.

## G-01 — strict validation of limit flags

### Current source-level observation
`derive_disposition(..., limit_violated=False, output_truncated=False)` uses ordinary truthiness in its limit branch. A non-empty string such as `"false"` is truthy and can produce `LIMIT_EXCEEDED`. This finding is limited to the pure helper input contract; it does not prove untrusted callers can reach it.

### Required test matrix
For each keyword argument `limit_violated` and `output_truncated`, test:
- valid: `False`, `True`;
- malformed: `None`, `0`, `1`, `""`, `"false"`, `[]`, `{}`.

Include a fixture where `execution_outcome="EXIT_ZERO"`, cleanup and all PASS gates are valid, so a malformed truthy value cannot hide behind an already failing gate. Include `contradictory_evidence=True` as a precedence regression only if the chosen validation policy allows evaluating that input combination.

### Contract choice required before writing assertions
Two defensible policies exist; choose one explicitly:
1. **Strict helper contract (recommended):** require exact booleans and raise `TypeError` or `ValueError` for malformed flag values before disposition derivation. Advantage: malformed evidence cannot be silently reinterpreted. Consequence: callers must validate/catch at the boundary.
2. **Fail-closed result contract:** malformed flag values produce `INCOMPLETE` (or a documented typed validation result) rather than an exception. Advantage: reducer stays total for untrusted values. Consequence: the API must distinguish invalid input from a genuine incomplete run, or diagnostics can be lost.

Do not silently coerce strings/numbers to booleans. Do not change the mapping of valid `LIMIT_EXCEEDED`, timeout, contradiction or exit-zero cases in this patch.

### Acceptance conditions
- Both flags have identical validation behavior.
- The valid boolean matrix preserves current intended outputs.
- Malformed values cannot create `LIMIT_EXCEEDED` solely through truthiness.
- Existing timeout and contradiction tests remain unchanged and pass when executed.
- Test output labels the suite as unit-only; no runtime enforcement claim.

## G-02 — strict positive integer validation for OutputBudget

### Current source-level observation
Constructor checks only `cap <= 0`. Python booleans are integers; positive floats and some other comparable values may pass construction and later fail or behave unexpectedly during slicing. This is a deterministic constructor-boundary concern.

### Required test matrix
For each `per_stream_cap` and `aggregate_cap`, test:
- valid positive integers: `1`, a normal default-scale integer;
- invalid: `True`, `False`, `0`, `-1`, `1.5`, `"10"`, `None`.

For each invalid case, assert failure occurs at construction, not later in `add()` or `finish()`. Include independent tests changing one cap at a time so the failing parameter is clear.

### Recommended contract
Require `isinstance(cap, int) and not isinstance(cap, bool) and cap > 0` for both caps, or use an equally strict integral-type check with an explicitly documented compatibility policy. Plain `isinstance(x, int)` is insufficient because `bool` subclasses `int`. Avoid accepting floats merely because they are mathematically integral unless the contract explicitly wants that.

### Acceptance conditions
- Invalid caps raise one documented validation exception during construction.
- No instance is partially initialized after invalid configuration.
- Existing exact-cap and one-byte-overflow semantics are preserved.
- `observed` may count bytes beyond retention caps as currently designed; this patch must not alter observed/retained accounting or truncation disposition.

## G-03 — reject whitespace-only required fingerprint identity fields

### Current source-level observation
The fingerprint helper rejects empty identity strings, but whitespace-only `contract_version`, `tenant_id`, `runtime`, or `entrypoint` passes the initial check. Runtime is then stripped/lowercased for the fingerprint, so a whitespace-only runtime can normalize to an empty string. Contract version, tenant and entrypoint currently retain their raw string values.

### Required test matrix
Build a valid fingerprint fixture, then replace each field independently with:
- `""`;
- one ASCII space;
- tabs/newlines or mixed whitespace;
- a nonblank string with surrounding whitespace (separate case).

Assert empty/whitespace-only required fields fail. Do not assume surrounding whitespace on a nonblank value is invalid for every field unless normalization policy is chosen explicitly.

### Contract choice required before assertions for nonblank surrounding whitespace
- **Required-field minimum:** reject strings where `not value.strip()`; preserve nonblank raw values except where the existing field contract explicitly normalizes them.
- **Canonical normalization:** trim and normalize each identity field consistently before hashing, with a deliberate versioning decision because this changes fingerprints and idempotency identity.

**Recommended minimal patch:** reject blank-after-strip required fields; preserve current normalization for nonblank values in this bounded change. If normalization across fields is desired, treat it as a separate fingerprint-version/contract decision. Never silently broaden normalization in a test-only patch.

### Acceptance conditions
- All four required fields reject blank/whitespace-only values.
- A whitespace-only runtime cannot become a valid empty runtime in the fingerprint document.
- Existing stable fingerprint tests and meaningful-field sensitivity remain unchanged.
- Any intentional change to fingerprint bytes or request identity is called out separately; do not treat fingerprint changes as harmless.

## Implementation order and patch discipline

1. Re-fetch PR #3 branch HEAD, the two file blobs, and any branch protection/CI evidence needed for context. If either source blob differs from the pins above, redo the audit for the changed function/test.
2. Confirm the error policy for G-01 and the whitespace normalization boundary for G-03. G-02's strict type rule can be proposed independently.
3. Add tests first on the PR #3 branch; avoid mixing these changes into the research branch or PR #2.
4. Make the smallest source changes required to satisfy tests. Do not bundle G-04, G-07, G-08 or redactor behavior into the same patch.
5. Run only a locally authorized, bounded unit command if available; record exact environment, command, output and exit code. If unavailable, leave tests NOT RUN. Do not trigger Actions or cloud workloads.
6. Inspect the final diff for accidental changes to timeout/contradiction verdicts, output accounting, fingerprint version or canonical LOOP/CASE acceptance.
7. Report result as source/test change only. A passing unit suite is not provider, persistence, security-boundary or device proof.

## Current state

No patch has been applied. No tests have been run. PR #3 and PR #2 remain unchanged. No user decision is inferred from this document. Canonical acceptance remains unchanged.
