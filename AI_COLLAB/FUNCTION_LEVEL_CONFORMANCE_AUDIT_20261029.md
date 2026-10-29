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
