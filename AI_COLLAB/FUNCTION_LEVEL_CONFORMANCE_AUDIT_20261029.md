# PocketCode — function-level conformance audit (static)

**Date:** 2026-10-29  
**Status:** Static source/test inspection only. No tests executed in this pass. No runtime/provider behavior verified.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Scope:** Narrow follow-on to the cross-branch audit. This adds concrete source-level observations and test priorities; it does not replace canonical acceptance, modify PR #2/#3, select a provider, or authorize implementation.

## 1. Pinned source verification

The inspected blob SHAs match the previously recorded pins:

| File | Branch | Blob SHA | Evidence |
|---|---|---|---|
| `scripts/report_contract.py` | `chat-continuity-report-regressions-2026-10-26` | `e9d944a722c2fac5279952696528da72a7011af3` | Static source inspected |
| `scripts/test_report_contract.py` | `chat-continuity-report-regressions-2026-10-26` | `39f3a3ef865ed55f333a1edc208096d99197d023` | Test source inspected; not run here |
| `scripts/lifecycle_contract.py` | `pocketcode-pass0-audit-2026-10-26` | `ba8d4d0b217c90513bed020e298029ef4e16f164` | Static source inspected |
| `scripts/test_lifecycle_contract.py` | `pocketcode-pass0-audit-2026-10-26` | `39db87d9f44f5e8474f33cff60136e529364199a` | Test source inspected; not run here |
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `main` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | Canonical acceptance pin previously verified; unchanged |

## 2. Concrete findings

### FLA-01 — malformed output-limit flags can produce a false specific disposition

**Classification:** CONFIRMED SOURCE-LEVEL VALIDATION GAP; MISSING REGRESSION TEST  
**Function:** `derive_disposition()` in PR #3  
**Source:** [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py#L27-L65)

The helper explicitly checks gate booleans with `value is True` for the EXIT_ZERO PASS gates and checks timeout/cancel termination with `termination_confirmed is True`. However, its earlier limit branch uses ordinary truthiness:

```python
if execution_outcome == "LIMIT_EXCEEDED" or limit_violated or output_truncated:
    return "LIMIT_EXCEEDED"
```

Consequently, `limit_violated="false"` or `output_truncated=1` can return `LIMIT_EXCEEDED`. This does not create PASS, but it incorrectly upgrades malformed/ambiguous evidence into a specific runtime-limit claim. The current test source checks malformed gate booleans and a true output-truncation flag, but does not appear to test malformed `limit_violated` or `output_truncated` values.

**Minimal regression cases:**
- `limit_violated="false"` with otherwise valid EXIT_ZERO evidence must be rejected or yield a conservative incomplete result, never LIMIT_EXCEEDED.
- `output_truncated=1` must be rejected or yield a conservative incomplete result, never LIMIT_EXCEEDED.
- Explicit `False` must retain the existing non-limit semantics.
- Test malformed values alongside contradictory evidence so precedence is deliberate.

Do not silently reinterpret malformed evidence as `False`; choose and document whether the contract raises a validation error or returns INCOMPLETE.

### FLA-02 — fingerprint helper accepts whitespace-only required identity fields

**Classification:** CONFIRMED SOURCE-LEVEL INPUT-VALIDATION GAP; DOWNSTREAM IMPACT DEPENDS ON CALLER  
**Function:** `canonical_request_fingerprint()`  
**Source:** [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py#L171-L220)

The initial required-field check accepts any non-empty string. Runtime is subsequently normalized with `runtime.strip().lower()`; therefore a whitespace-only runtime passes the initial check but fingerprints as an empty runtime. Whitespace-only contract version, tenant ID, or entrypoint also pass the non-empty check (entrypoint is not stripped). This is a source-level validation gap in the fingerprint helper, not proof that a real request path accepts such values; a future request validator may reject them before this function is called.

**Minimal regression cases:** whitespace-only contract version, tenant ID, runtime, and entrypoint should be rejected at the defined validation boundary. Test normalized runtime emptiness explicitly. Decide whether entrypoint canonicalization belongs here or in a separate request validator; do not imply the fingerprint itself validates path safety.

### FLA-03 — output budget configuration lacks strict integer validation

**Classification:** MISSING REGRESSION TEST / CONFIGURATION-VALIDATION GAP  
**Function:** `OutputBudget.__init__()` and `OutputBudget.add()`  
**Source:** [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py#L253-L300)

The constructor checks only whether caps compare as less than or equal to zero. It does not explicitly require positive integers excluding booleans. A positive float can pass construction and later be used as a slice bound in `chunk[:allowed]`, which raises `TypeError` rather than producing a controlled validation error. A boolean is also accepted as an integer-like cap in Python.

**Minimal regression cases:** reject `True`, `False`, a positive float, a string, zero, and negative caps at construction; accept positive integers. This is primarily configuration robustness, not evidence that an external user can set these caps.

### FLA-04 — event reducer does not bind terminal events to a job/attempt identity

**Classification:** INTEGRATION GAP / TRUSTED-COORDINATOR REQUIREMENT  
**Function:** `reduce_terminal_events()`  
**Source:** [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py#L70-L137)

The reducer validates event ID, coordinator sequence, and kind, then orders/reduces events. It does not require a job or attempt identifier, nor does its interface receive the expected attempt identity. It therefore cannot itself prove that supplied events all belong to the same attempt. The existing adapter protocol already states that attempt binding is mandatory; this is not evidence of a live cross-attempt vulnerability because the helper is a pure reducer and no coordinator integration is present.

**Required future test:** mix a valid terminal event for attempt A with an otherwise valid terminal event for attempt B. The coordinator must reject/quarantine cross-attempt evidence and must not let it resolve attempt A. Keep this separate from duplicate-event-ID and duplicate-sequence tests already present.

### FLA-05 — bounded report output is not the same as bounded formatter input processing

**Classification:** PERFORMANCE/ROBUSTNESS GAP TO EVALUATE; NOT A VERDICT BUG  
**Function:** `_safe_text()` and `format_report()` in PR #2  
**Source:** [report_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/chat-continuity-report-regressions-2026-10-26/scripts/report_contract.py#L20-L35)

`_safe_text()` converts and scans the entire supplied value to build a safe string before truncating it to the requested character limit. The final report is bounded, but processing a very large supplied stdout/stderr or field can still allocate and scan substantially more data than the displayed limit. Existing tests exercise large strings, but the report-size cap does not itself establish a bounded-memory or bounded-CPU property.

**Recommended disposition:** assess expected upstream collector limits before changing the formatter. If the formatter is expected to tolerate arbitrarily large strings, add a test/implementation that bounds conversion and escaping work. Otherwise document that bounded input is an upstream precondition. Do not confuse this with runtime output enforcement or use it to change the execution verdict.

## 3. Existing coverage to reuse, not duplicate

The inspected PR #3 test source already covers:
- EXIT_ZERO PASS requires confirmed cleanup and all four boolean gates.
- Malformed truthy values for policy, termination, artifact, and tenant gates do not produce PASS.
- Timeout with unconfirmed termination is INCOMPLETE.
- True output truncation currently produces LIMIT_EXCEEDED.
- Coordinator sequence ordering, provider timestamps ignored for ordering, multiple terminal events as contradictory, duplicate event identity and conflicting reuse.
- Deterministic replay when distinct events share a coordinator sequence.
- Basic artifact gate behavior and rejection of truthy non-boolean digest/job/tenant gate values.
- Serial idempotency replay/conflict/tenant scope and deterministic batch examples.
- Report history append-only behavior in the in-memory model and PASS-gate validation.

These are source-covered assertions, not proof that the checked-in tests passed in this pass. The serial batch tests do not establish database atomicity or cross-process race safety. The in-memory report-history tests do not establish durable storage or tamper resistance. The artifact predicate tests do not establish real stored-byte integrity or authenticated download behavior.

The inspected PR #2 test source already covers:
- Verdict handling for success, nonzero exit, missing exit, nonterminal states, and boolean exit-code rejection.
- Simulated reports never PASS.
- Empty versus unavailable output.
- Escaping newlines in user-controlled fields.
- Script-reported checks remain distinct from the process verdict.
- Non-finite durations, report truncation, malformed list entries, and malformed truncation flags.

Do not duplicate these existing source cases without identifying a new boundary or failure mode.

## 4. Focused conformance test matrix

| ID | Minimal case | Expected assertion | Boundary | Canonical anchors | Status |
|---|---|---|---|---|---|
| FLA-T01 | `limit_violated="false"` or `output_truncated=1` | Reject malformed evidence or return INCOMPLETE; never assert LIMIT_EXCEEDED from malformed truthiness | Pure helper | LOOP-03/07; CASE-07/12 | Missing from inspected tests |
| FLA-T02 | Whitespace-only required fingerprint fields | Reject invalid identity/runtime values at documented validation boundary | Request/fingerprint validation | LOOP-02/03; CASE-08 | Missing from inspected tests |
| FLA-T03 | Float/bool/string output caps | Constructor raises clear validation error before stream processing | Pure helper/config | LOOP-07; CASE-07 | Missing from inspected tests |
| FLA-T04 | Event stream contains two attempt IDs | Cross-attempt event cannot resolve requested attempt | Coordinator/event boundary | LOOP-03/05/09; CASE-11/13/16 | Not expressible by current reducer interface alone |
| FLA-T05 | Extremely large caller-supplied text | Processing bound is established, or bounded input is explicitly a precondition | Report helper/upstream collector | LOOP-07/11; CASE-07/12 | Needs requirements decision |

## 5. Cross-branch invariant that must remain explicit

PR #2's `classify_verdict()` can return PASS for `("succeeded", 0)`. PR #3's `derive_disposition()` can return INCOMPLETE for EXIT_ZERO when cleanup or a required gate is missing. This is not a defect in either isolated helper: their input models differ and no adapter currently connects them. The future mapping must not translate raw EXIT_ZERO directly to report status `succeeded` without preserving the derived disposition and evidence-quality state.

Only a trusted coordinator may project PASS after all required gates are authoritatively satisfied. Report formatting must not be treated as a trust boundary.

## 6. Remaining integration and real-boundary blockers

Still not implemented or verified by these helpers:
- Atomic policy-revision barrier immediately before dispatch.
- Durable, cross-process idempotency and lost-ack recovery.
- Trusted provider status lookup and termination confirmation.
- Runtime-enforced output/resource limits and network egress restrictions.
- Artifact store writes, final stored-byte digest checks, quarantine, and release-time authorization.
- Authenticated tenant/job/attempt binding at the actual API/download boundary.
- Separate wrapper versus child-process exit evidence if the selected architecture needs both.
- Real end-to-end input/output artifact flow and copy-to-another-AI correction loop.

The existing canonical acceptance remains authoritative: all 14 LOOP criteria and all 16 CASE scenarios remain in scope. A smoke test or pure-helper suite cannot replace hosted safety acceptance.

## 7. Evidence and change status

- Source pins listed above match the inspected GitHub blob SHAs.
- Findings are static source observations; no tests were run here.
- PR #2, PR #3, canonical acceptance, and provider/runtime selection were not changed.
- No account, billing, workload, merge, deployment, or production implementation was initiated.
- This document is research/continuity only and does not authorize implementation.


## 8. Additional evidence-integrity finding

### FLA-06 — terminal-event reducer returns shallow copies of event records

**Classification:** CONFIRMED SOURCE-LEVEL MUTABILITY GAP; INTEGRATION IMPACT DEPENDS ON CALLER  
**Function:** `reduce_terminal_events()`  
**Source:** [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py)

The reducer uses `event = dict(raw)`, which copies the outer mapping but retains references to nested values such as `payload`. The returned `events` and `conflicts` therefore can share mutable payload objects with the caller's input. If a caller mutates an original nested payload after reduction, the reducer's returned evidence view changes too, even though its previously computed outcome/contradiction flags do not automatically recompute.

This is not proof of a live audit-log vulnerability. It is a concrete helper-level evidence-immutability gap if callers retain and rely on the returned mappings as an evidence snapshot.

**Minimal regression:**
1. Reduce an event whose payload is a mutable dictionary.
2. Mutate the original nested payload after reduction.
3. Assert that the returned accepted/conflict evidence remains unchanged.
4. Repeat with nested lists and nested dictionaries if the accepted payload contract permits them.

**Possible fix choices:** require immutable/canonical event payloads at the trust boundary; deep-copy validated payloads; or serialize and validate events into a canonical immutable representation before reduction. Avoid blindly deep-copying arbitrary objects without defining the allowed payload type.

**Canonical anchors:** LOOP-03/09/11; CASE-11/13/16.

This supplements FLA-04: event-to-attempt binding and event-payload immutability are separate requirements. Binding proves which attempt an event claims to describe; immutability prevents the supplied evidence representation from changing after it has been reduced.

## 9. Cross-document implementation-ready test sequence

The companion `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` defines COORD-01..10 for coordinator behavior. The combined next sequence, if later authorized, is:

1. Add pure-helper tests for malformed limit flags, whitespace-only fingerprint inputs, invalid output-budget cap types, and mutable event payload aliasing.
2. Resolve whether required stdout/stderr collection is a PASS gate for each supported runtime. Do not silently infer that requirement from artifact validity.
3. Build coordinator tests with exact dispatch counts, same-attempt lookup, policy revision barrier, and release-time authorization checks.
4. Add persistence/concurrency tests before claiming idempotency or report history is durable.
5. Run real controlled-boundary acceptance only after a provider/runtime is separately approved.

No tests were run and no code or canonical acceptance was changed as part of this addendum.


## 10. Additional reducer consistency findings

### FLA-07 — duplicate-event identity comparison omits attempt/job binding fields

**Classification:** CONFIRMED SOURCE-LEVEL GAP; CONTRACT DEPENDENT  
**Function:** `reduce_terminal_events()`

The reducer's duplicate-event signature is exactly `(sequence, kind, payload)`. If the surrounding event contract carries `job_id`, `attempt_id`, tenant scope, policy revision, or evidence-source identity, those fields are not compared when a repeated `event_id` is encountered. Two records with the same event ID, sequence, kind, and payload but different attempt/job identity can therefore be treated as an idempotent duplicate; the later record is silently ignored rather than marking a conflict.

This finding is conditional on those fields being part of the event contract. The current helper does not define a full event schema, so do not claim a live cross-attempt vulnerability. The integration must establish event-ID scope and validate all identity-bearing fields before reduction.

**Minimal regression:** create two records with the same event ID, sequence, kind, and payload but different attempt IDs (and separately different job/tenant identity). If identity fields are required by the chosen event schema, assert contradiction and preserve the conflicting record; alternatively reject/quarantine the event before it reaches this reducer.

**Required contract decision:** define whether event IDs are globally unique or scoped by tenant/job/attempt, and enumerate the immutable fields covered by duplicate equivalence. Provider timestamps may remain excluded from ordering, but that does not imply all other metadata can be ignored.

**Canonical anchors:** LOOP-03/05/09/11; CASE-11/13/16.

### FLA-08 — duplicate coordinator sequence marks contradiction without consistently recording the colliding events

**Classification:** CONFIRMED DIAGNOSTIC-COMPLETENESS GAP  
**Function:** `reduce_terminal_events()`

After sorting accepted events, the reducer detects repeated coordinator sequence values and sets `contradictory_evidence = True`, but it does not add the records sharing that sequence to `conflicts` at that point. If the collision is between nonterminal events, the later terminal-event check may add nothing either. The result can therefore say evidence is contradictory while the returned conflict list does not identify the sequence-collision records.

This does not by itself make a PASS possible if the caller correctly honors the contradiction flag. It weakens explanation, diagnostics, and later reconciliation.

**Minimal regression:** submit two distinct nonterminal event IDs with the same sequence. Assert contradiction is true and both colliding records (or an explicit structured collision record referencing both) are represented in conflict diagnostics. Repeat with one terminal and one nonterminal event sharing the sequence.

**Possible fix:** collect all sequence groups with cardinality greater than one and record every member in conflict diagnostics, with deterministic ordering and no accidental duplicate entries.

**Canonical anchors:** LOOP-05/07/09; CASE-11/13/16.

These findings are separate from FLA-04 (the reducer has no expected attempt argument) and FLA-06 (nested event payloads remain mutable through shallow copies). Together they identify three distinct concerns: identity binding, duplicate equivalence, and evidence-snapshot integrity/diagnostics.


## 9. Idempotency reservation input validation

### FLA-09 — idempotency helper relies on truthiness rather than validating identifier types and normalized values

**Classification:** CONFIRMED SOURCE-LEVEL INPUT-VALIDATION GAP; CALLER IMPACT UNKNOWN  
**Function:** `reserve_idempotency()`; related boundary: `reserve_idempotency_batch()`  
**Pinned source:** `scripts/lifecycle_contract.py`, PR #3 branch `pocketcode-pass0-audit-2026-10-26`, blob `ba8d4d0b217c90513bed020e298029ef4e16f164`.

The helper checks `if not tenant_id or not key or not fingerprint or not proposed_job_id`, which only rejects false-like values. It does not enforce that these four values are strings, non-whitespace, or in any documented canonical form. Truthy non-string values can therefore be stored in the reservation record despite the declared `dict[tuple[str, str], tuple[str, str]]` contract. Unhashable tenant/key values can fail later during tuple-key dictionary lookup with a lower-level `TypeError`, rather than the helper's documented-style `ValueError`. Whitespace-only strings are also accepted. The batch wrapper repeats the same truthiness-only validation before calling the helper.

This is a pure-helper contract/robustness gap. It does not establish that an actual API accepts malformed identifiers; a future request validator may reject them. It also does not establish a concurrency or durable-idempotency defect, which remains outside this in-memory model.

**Minimal regression matrix:**
- Reject non-string values for tenant ID, idempotency key, request fingerprint, and proposed job ID.
- Reject empty and whitespace-only values after the contract-defined normalization step.
- Reject unhashable tenant/key values with a clear validation error, not an incidental dictionary exception.
- Keep tenant scoping and same-key/same-fingerprint replay behavior unchanged for valid canonical strings.
- Apply equivalent validation through `reserve_idempotency_batch()`; do not let its type annotations stand in for runtime validation.

**Contract decision:** define whether identifiers are opaque case-sensitive strings or normalized strings, and which fields may be trimmed. Do not silently normalize an idempotency key if doing so could merge distinct caller-supplied keys; alternatively reject whitespace-only values without rewriting valid opaque keys.

**Canonical anchors:** LOOP-03/05/09; CASE-08/11/13/16.

### Tombstone review result — existing regression coverage is incomplete

The pinned PR #3 `DeletionTombstones.add()` stores `(fingerprint, deleted_at + RETENTION_SECONDS)` directly at the tenant/key map entry. The current test covers tenant scoping and expiration at the exact 30-day deadline, but does not cover repeated `add()` calls for the same tenant/key with a changed fingerprint or a different `deleted_at`. On this pinned branch, a repeated add replaces the previous fingerprint and expiry; depending on the supplied timestamp, it can change the retained fingerprint or shorten/extend the deadline.

This is recorded as a **cross-branch regression check**, not a new independent FLA ID in this pass, because a separate lifecycle/fingerprint audit branch was previously reported to contain tombstone overwrite/retention work and its current source was not re-verified here. Before adopting any change, compare the exact branch/file revisions and preserve the intended policy: duplicate deletion events should not silently rewrite the original tombstone identity or reset retention unless an explicit contract says so.

### Output-budget follow-up

The pinned constructor still accepts positive non-integer caps because it checks only `<= 0`; the existing test source exercises cap behavior but has no constructor-type matrix. This corroborates FLA-03 and is **not** a separate finding. A future regression should reject booleans, floats, strings, zero, and negative values at construction; valid positive integers should remain accepted.

**Evidence status:** static inspection only. No tests were executed. No implementation or canonical acceptance documents changed.


## 10. Cross-branch reconciliation — lifecycle fingerprint audit branch

**Checked after FLA-09 was recorded.** The separate branch `pocketcode-lifecycle-fingerprint-audit-2026-10-27` contains a later source revision and test additions. This changes the status of FLA-02/FLA-09 and the tombstone review; it does not change the pinned PR #3 source or establish that these changes are merged or executed.

- Updated `scripts/lifecycle_contract.py` blob: `316345341603848c4a86a6a82e533daa796c7695`.
- Updated `scripts/test_lifecycle_contract.py` blob: `ef9a68de632be30c091afe57f0724fd030a513f9`.

### FLA-02 — candidate fix exists on the separate branch

The updated fingerprint helper rejects whitespace-only contract version, tenant ID, runtime, and entrypoint while preserving the runtime normalization behavior. Its new test covers empty/whitespace-only fields and confirms equivalent runtime casing/spacing fingerprints identically. Status: **source-level fix present on the separate branch; tests NOT RUN here; not assumed integrated**.

### FLA-09 — candidate fix exists on the separate branch

The updated `reserve_idempotency()` now requires tenant ID, key, fingerprint, and proposed job ID to be nonblank strings. The test source adds empty, whitespace-only, `None`, and integer cases for each field. Status: **source-level fix present on the separate branch; tests NOT RUN here; not assumed integrated**.

### Tombstone overwrite/retention concern — addressed in the separate branch's source

The updated `DeletionTombstones.add()` validates tenant/key/fingerprint as nonblank strings; same-key retries with a changed fingerprint raise `IdempotencyConflict`; same-fingerprint retries preserve the later expiry via `max(old_expiry, new_expiry)`, preventing a retry from shortening retention. Added tests cover shortened/extended timestamps and fingerprint conflict. Status: **source-level fix and regression tests present on the separate branch; tests NOT RUN here; not assumed integrated**. The earlier tombstone note in Section 9 remains accurate for the pinned PR #3 blob, but must not be generalized to the newer branch.

### Remaining audit item

The separate branch's `OutputBudget.__init__()` still appears to validate caps only using `<= 0`; strict positive-integer/non-boolean validation remains a candidate gap unless another revision addresses it. This remains FLA-03, not a new finding.

**Interpretation:** the lifecycle/fingerprint branch provides candidate remediation and tests, not execution evidence. Do not cherry-pick, merge, or describe fixes as integrated without explicit authorization and branch review. PR #2, PR #3, and canonical acceptance remain unchanged; no tests were run in this pass.
