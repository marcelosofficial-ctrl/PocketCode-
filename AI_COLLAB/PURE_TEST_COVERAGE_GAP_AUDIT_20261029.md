# PocketCode — pure-test coverage gap audit

**Date:** 2026-10-29  
**Status:** Static comparison of pinned test/source files only. Tests NOT RUN. No source files or PRs changed.  
**Research branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Companion:** [Pure contract test inventory](PURE_CONTRACT_TEST_INVENTORY_20261029.md)

## Verified source pins

| File | Branch | Current fetched blob SHA | Result |
|---|---|---|---|
| `scripts/test_report_contract.py` | `chat-continuity-report-regressions-2026-10-26` | `39f3a3ef865ed55f333a1edc208096d99197d023` | Matches previously audited pin |
| `scripts/report_contract.py` | `chat-continuity-report-regressions-2026-10-26` | `e9d944a722c2fac5279952696528da72a7011af3` | Matches previously audited pin |
| `scripts/test_lifecycle_contract.py` | `pocketcode-pass0-audit-2026-10-26` | `39db87d9f44f5e8474f33cff60136e529364199a` | Matches previously audited pin |
| `scripts/lifecycle_contract.py` | `pocketcode-pass0-audit-2026-10-26` | `ba8d4d0b217c90513bed020e298029ef4e16f164` | Matches previously audited pin |

These are exact branch refs and blob hashes fetched during this pass. The tests were read, not executed. “Covered” below means a relevant assertion exists in the test source, not that the behavior passed in execution.

## Gap-only result

### G-01 — malformed limit flags are not covered

**Target:** PR #3 `derive_disposition()`; test `test_timeout_unknown_termination_and_output_violation_never_pass`.  
**Observed coverage:** explicit `output_truncated=True` is covered; the broader malformed-gate test covers policy/termination/artifact/tenant gates, but not `limit_violated` or `output_truncated` with malformed types.  
**Missing cases:** `limit_violated="false"`, `output_truncated="false"`, integer 1, null, and other unsupported values.  
**Reason:** source uses ordinary truthiness in the limit branch, so malformed truthy values can become a specific LIMIT_EXCEEDED claim.  
**Disposition:** candidate source/test change on PR #3's own branch only, after deciding whether malformed inputs raise validation errors or yield a conservative result. Do not reinterpret malformed values silently as false.  
**Static finding:** matches FLA-01.

### G-02 — output-budget constructor type validation is missing

**Target:** PR #3 `OutputBudget`.  
**Observed coverage:** positive integer caps, exact aggregate cap, per-stream overflow, aggregate overflow, retained-byte bounds and post-overflow retention are tested.  
**Missing cases:** boolean, positive float, numeric string, zero and negative caps; ensure failure happens at construction with a documented error rather than later at slicing.  
**Disposition:** candidate source/test change on PR #3's own branch.  
**Static finding:** matches FLA-03.

### G-03 — whitespace-only fingerprint identity fields are not covered

**Target:** PR #3 `canonical_request_fingerprint()`.  
**Observed coverage:** deterministic repeat, source/policy sensitivity, input-order canonicalization, Unicode-normalization filename collision, unsafe names and whitespace-only content type are covered.  
**Missing cases:** whitespace-only contract version, tenant ID, runtime and entrypoint; runtime normalization to an empty value.  
**Disposition:** candidate source/test change on PR #3's own branch. Keep filename/path validation separate from identity-string validation.  
**Static finding:** matches FLA-02.

### G-04 — non-string key / ambiguous canonical schema boundary is not covered

**Target:** PR #3 `canonical_request_fingerprint()`.  
**Observed coverage:** normal semantic sensitivity and order normalization are tested.  
**Missing cases:** non-string mapping keys or schema-disallowed scalar types that may serialize ambiguously/collapse after canonicalization.  
**Disposition:** first define/verify the accepted request schema. Add a test only for inputs that are invalid at the real validation boundary; do not invent a broader schema from the helper alone.  
**Static finding:** relates to FLA-11; impact remains conditional on caller validation and schema.

### G-05 — nested event-payload immutability is not directly tested

**Target:** PR #3 `reduce_terminal_events()` and future event-ingestion boundary.  
**Observed coverage:** exact duplicate event IDs, changed sequence, duplicate coordinator sequence, deterministic ordering and terminal contradictions are covered. `ReportHistory` separately tests that returned report structures do not mutate stored history.  
**Missing case:** mutate a nested payload after it has been accepted and assert the accepted event snapshot is unchanged.  
**Disposition:** unit test can be specified now; implementation location depends on whether the reducer is expected to own/copy events or the future coordinator must freeze them. D-04 still controls the final accepted-event identity/schema rule.

### G-06 — event scope binding remains untested at helper level and absent from reducer interface

**Target:** PR #3 `reduce_terminal_events()`.  
**Observed coverage:** sequence and event-ID behavior; no expected job/attempt argument is present in the reducer interface.  
**Missing proof:** reject an event bound to a different tenant/job/attempt before reduction.  
**Disposition:** not a pure reducer test unless interface changes. Add coordinator/fake test per COORD-05; actual producer authentication and persistence require later integration evidence. D-04 must settle the exact scope tuple.

### G-07 — reserved Windows superscript device aliases are missing from filename fixtures

**Target:** PR #3 fingerprint/input-name validation tests.  
**Observed coverage:** CON, NUL and COM1 are tested, alongside traversal and path-like cases.  
**Missing cases:** COM¹, COM², COM³ and LPT¹, LPT², LPT³, plus case variants if the accepted normalization rules require them.  
**Disposition:** candidate filename validation test/source change on PR #3's own branch; verify Windows behavior separately before claiming cross-platform validation.  
**Static finding:** matches FLA-13.

### G-08 — tombstone re-add/expiry extension behavior is not covered

**Target:** PR #3 `DeletionTombstones.add()`.  
**Observed coverage:** tenant scope and before/exactly-at/after 30-day expiry are tested.  
**Missing cases:** repeated add with earlier expiry, later expiry, same fingerprint, and conflicting fingerprint. Assert repeated registration cannot shorten the intended retention horizon or overwrite a conflicting fingerprint silently.  
**Disposition:** candidate source/test change on PR #3's own branch; preserve the documented retention contract and verify the exact current implementation first.

### G-09 — redaction maximum-length and over-limit suffix behavior is not covered

**Target:** PR #3 `StreamingRedactor` and output budget.  
**Observed coverage:** bearer/provider key patterns, a configured secret pattern across chunks, and a match crossing the carry boundary are tested.  
**Missing cases:** maximum supported token length, token longer than the regex/carry bound, suffixes around the boundary, and multiline/near-match behavior.  
**Disposition:** add bounded regression fixtures and document limitations. This cannot establish that regex redaction is a primary security boundary; secrets must not be injected into untrusted execution in the first place.  
**Static finding:** matches FLA-12.

### G-10 — report formatter lacks explicit source-label regression for forged structured status text

**Target:** PR #2 `format_report()`.  
**Observed coverage:** newlines in user fields cannot forge report fields; simulated results cannot PASS; script-reported failed checks remain visible with provenance.  
**Gap status:** no urgent missing test established from this narrow comparison. A useful optional extension is a check whose detail or name includes status-looking JSON and assert it remains plain program-reported content. Do not label this a confirmed defect.

## Existing coverage worth preserving (not new gaps)

- PR #2: PASS/FAIL/INCOMPLETE lifecycle projection, bool exit-code rejection, simulated-report honesty, empty versus unavailable streams, newline field escaping, script-reported check provenance, finite duration validation, report truncation and cap preserving uncertainty.
- PR #3: contradiction precedence; explicit PASS gates; malformed PASS gate booleans; timeout termination uncertainty; timestamp-independent coordinator ordering; duplicate-event conflict; request fingerprint sensitivity and deterministic input ordering; common unsafe filename cases; tenant-scoped in-memory idempotency; output retention caps; streaming redaction boundaries; artifact gate booleans; report-history versioning/returned-object isolation; tombstone expiry; batch idempotency behavior.

These tests do not prove live coordinator behavior, cross-process races, durable storage, provider guarantees, authenticated evidence, policy enforcement at dispatch, HTTP transfer integrity or device acceptance.

## Recommended sequence

1. Resolve G-01..G-03 first: they are concrete validation gaps with bounded tests and no need to decide D-01..D-04's final verdict/event schema, provided the validation behavior itself is explicitly chosen.
2. Clarify the request schema before G-04; avoid creating invalid test inputs whose behavior is unspecified.
3. Add G-05 only after documenting which layer owns immutable event snapshots; D-04 must still settle identity and replay.
4. Keep G-06 at coordinator boundary, not as a claim against a pure helper that lacks expected-attempt context.
5. Address G-07..G-09 with narrow regression fixtures on the isolated PR branch, preserving owner approval and branch separation.
6. Re-fetch the branch and blob SHA immediately before any proposed patch. No source edit is made by this audit.

## Provenance and limits

Static comparison of four exact source/test blobs fetched from the named branches. No Python tests executed; no workflow/Actions triggered; no source file changed; PR #2 and PR #3 remain untouched; no provider/store/runtime selected; no workloads, accounts or billing. Canonical acceptance on main remains unchanged.
