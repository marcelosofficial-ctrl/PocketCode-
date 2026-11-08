# Exit-provenance static consistency audit

**Date:** 2026-11-08  
**Status:** ChatGPT static audit only; not Claude's independent review; no source/test changes or execution.  
**Immutable pins:** helper blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`; test blob `85109f056009d65a274e9306deb39b68e1fefbd2`; canonical acceptance blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`; provenance matrix blob `f146bd45cdbc3e7f6f1301ad3c0e172ffa4443d7`.

## 1. Executive result

**VERIFIED:** the exit-provenance proposal accurately identifies the missing distinction between child exit, wrapper exit and forced termination. Its conservative outcomes generally align with canonical LOOP-03..05 and CASE-04.

**HIGH-PRIORITY SPEC GAP:** proposed EP-04 and EP-05 require INCOMPLETE for contradictory terminal facts, but the currently pinned `format_report()` cannot render that result while preserving the contradictory lifecycle status and child code. It calls `classify_verdict(status, exit_code)` internally. The classifier returns FAIL whenever `exit_code` is a valid nonzero integer or status is `program_failed`, before considering any contradiction. The proposed spec says the formatter should render an already-resolved result, but the current helper is itself the verdict classifier and has no resolved-verdict input.

This does not invalidate the coordinator design. It means a separate typed projection result and a renderer contract change (or an explicit legacy compatibility limitation) must be specified before EP-04/05 can be implemented faithfully. Do not patch the helper in this audit.

## 2. Pinned source facts

### `scripts/report_contract.py` blob 2459137

- `classify_verdict(execution_status, exit_code)` accepts only status plus one generic exit code.
- `valid_exit` is an integer excluding bool.
- Any valid nonzero exit returns FAIL, regardless of lifecycle status.
- `program_failed` returns FAIL, even if exit code is zero.
- PASS requires exactly `succeeded` plus valid integer zero.
- All other combinations return INCOMPLETE.
- `format_report()` sanitizes invalid/bool exit codes to None, then calls `classify_verdict(status, exit_code)`. It has no pre-resolved verdict argument.
- The module explicitly says it is a formatter, not a runner, provider adapter or source of trusted metadata.

### `scripts/test_report_contract.py` blob 85109f0

Existing verdict tests cover:
- succeeded + 0 => PASS;
- succeeded + 2 => FAIL;
- program_failed + None => FAIL;
- succeeded + None => INCOMPLETE;
- accepted/queued/running + 0 => INCOMPLETE;
- timed_out/cancelled/rejected/infrastructure_failed/unknown + None => INCOMPLETE;
- bool exit => INCOMPLETE.

They do **not** cover program_failed + 0, contradictory lifecycle/child observations, wrapper-vs-child identity, signals, termination acknowledgement, stale or cross-attempt terminal events, or the typed coordinator projection.

### Canonical acceptance blob c6714c2

- LOOP-03 requires trusted completion evidence and child exit 0 for PASS.
- LOOP-04 defines a confirmed program failure, including nonzero exit or confirmed program/runtime failure.
- LOOP-05 says timeout, cancellation, rejection and uncertain infrastructure cannot be success.
- CASE-04 specifically requires trusted timeout to remain INCOMPLETE / timed_out.
- CASE-05 distinguishes cancellation confirmation from unconfirmed termination.
- CASE-06 requires infrastructure failure without trustworthy program result to remain INCOMPLETE.
- CASE-09/10 keep script-reported checks separate from process verdict.
- CASE-15 is a security/isolation acceptance scenario, not a program exit classification rule.

## 3. EP-01..EP-20 cross-check

| EP | Existing helper/test relationship | Static disposition |
|---|---|---|
| EP-01 | Directly matches existing PASS test. | Covered at pure-helper level; provenance still unproven. |
| EP-02 | succeeded + nonzero helper test yields FAIL. | Behavior covered, but test does not prove the code belongs to the child. |
| EP-03 | program_failed + None helper test yields FAIL. | Covered at helper level; trust in lifecycle status is external. |
| EP-04 | program_failed + child zero is FAIL in current helper. | **Not implementable as specified with current formatter/classifier.** Needs resolved projection/renderer contract. |
| EP-05 | succeeded + child nonzero is FAIL in current helper. | **Not implementable as specified with current formatter/classifier.** Needs resolved projection/renderer contract. |
| EP-06 | timeout + wrapper 137 should be represented with child code absent; helper then yields INCOMPLETE. | Not tested; coordinator must not put wrapper code in `exit_code`. |
| EP-07 | cancelled + wrapper 143; child code absent. | Not tested; preserve termination confirmation separately. |
| EP-08 | running + wrapper nonzero; child absent. | Existing nonterminal + zero test is not equivalent. Add explicit wrapper-only case. |
| EP-09 | infrastructure_failed + no child code. | Covered at helper level. |
| EP-10 | trusted natural child nonzero plus separate infrastructure failure. | Not represented by current two-field helper; requires separate execution verdict and infrastructure disposition. |
| EP-11 | child zero plus missing required gate. | Helper alone would PASS; coordinator must withhold PASS before rendering. No current test. |
| EP-12 | child nonzero plus cleanup unknown. | Helper returns FAIL; separate artifact-release block is not represented/tested. |
| EP-13 | rejected plus purported child start/exit. | No dispatch/attempt contradiction test. |
| EP-14 | wrong tenant/job/attempt binding. | Formatter cannot authenticate/bind; coordinator integration test required. |
| EP-15 | bool is covered; string/malformed/stale binding are not. | Extend input validation/provenance tests outside the formatter. |
| EP-16 | late unbound exit after timeout. | No stale/delayed observation test. |
| EP-17 | timeout plus purported natural child exit. | No contradiction/order test. |
| EP-18 | child zero plus absent/mismatched policy barrier. | No test. Expected verdict/security disposition needs explicit owner-approved mapping; minimum is no PASS. |
| EP-19 | collector truncation after child zero. | Renderer tests truncation, but not its interaction with required-output gates. |
| EP-20 | wrapper restart reports a code without child identity continuity. | No identity-continuity test. |

## 4. Additional adversarial cases required

Add these as proposed EP-prefixed cases, not canonical CASE IDs:

- **EP-21: termination requested, not confirmed.** Deadline/cancellation/resource-limit request is authoritative, but termination acknowledgement is absent or lost. Expect INCOMPLETE; termination remains NOT_CONFIRMED/UNKNOWN; do not mark cleanup complete or release artifacts.
- **EP-22: wrapper exits zero, child exit absent.** Expect INCOMPLETE. A successful wrapper/worker shutdown is not evidence that the submitted child completed.
- **EP-23: child terminated by signal/resource control.** Preserve signal and cause separately; do not reinterpret shell-style 128+signal values (including 137/143) as a natural child program exit. Expect INCOMPLETE unless an independent trusted natural child result exists.
- **EP-24: natural child zero, wrapper fails during post-run collection/cleanup.** Preserve the child observation and wrapper/cleanup failure separately. The execution verdict and artifact-release disposition require explicit contract mapping; do not silently convert either fact into the other.
- **EP-25: timeout/resource limit plus natural child nonzero observation with trusted event ordering.** The coordinator must resolve whether the child naturally failed before the deadline or was forcibly terminated; absent sufficient ordering/provenance, retain contradiction as INCOMPLETE.

EP-24's verdict mapping and EP-18's policy-barrier failure mapping are **NEEDS-OWNER** unless an existing canonical case already determines the exact outcome. EP-21..23 and EP-25 are required to close clear provenance gaps.

## 5. Required clarification to the proposal

1. Define a typed coordinator projection result that can preserve raw lifecycle status, child observation/code, wrapper observation, termination cause/state, evidence quality, cleanup and artifact disposition.
2. Define how the report renderer accepts a pre-resolved verdict without re-running the legacy two-field classifier. Alternative: explicitly mark EP-04/05 unsupported by the current formatter until a versioned report contract is agreed.
3. Keep legacy `exit_code` child-only if retained. Wrapper/signal/forced-termination values must never flow into it.
4. Keep execution verdict separate from infrastructure disposition, cleanup state and artifact release.
5. Define an explicit rule for unconfirmed termination and late child observations. A browser disconnect or kill request is not termination proof.
6. Preserve CASE-04 exactly as INCOMPLETE / timed_out. Do not map 137/143 to program FAIL.
7. Keep all proposed EP cases outside canonical CASE IDs unless the owner approves a traceable acceptance change.

## 6. Reviewer checklist and gate

Claude's requested independent review should explicitly answer:
- Does the proposed projection preserve every canonical LOOP/CASE meaning?
- How should EP-04/05 contradictions be rendered without losing the raw trusted lifecycle status?
- Are EP-21..25 necessary, or does an existing contract already cover any of them?
- What exact evidence proves child identity, natural exit, signal termination, timeout/cancellation acknowledgement, event ordering and attempt binding?
- Which EP-18/24 mappings require owner decisions?
- Does the proposal preserve formatter purity and avoid treating user-supplied JSON/transcripts as trusted evidence?

**Disposition:** proposal is directionally sound, but the formatter/projection boundary and additional termination cases must be clarified before implementation. Claude's independent review and owner decisions remain pending. No source/test changes; no tests run.
