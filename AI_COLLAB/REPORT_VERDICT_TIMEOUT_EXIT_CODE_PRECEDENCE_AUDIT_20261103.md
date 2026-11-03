# PocketCode report verdict precedence audit: timeout and termination exit codes

**Date:** 2026-11-03  
**Status:** READ-ONLY STATIC SOURCE/TEST AUDIT / NO TESTS EXECUTED  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`

## Executive finding

The current report helper can classify a trusted `timed_out` lifecycle status as user-facing `FAIL` when an integer nonzero exit code is also present. The same first-condition precedence can classify `cancelled` and `infrastructure_failed` as `FAIL`.

This is a concrete static behavior of the pinned helper, and a test-coverage gap. It conflicts with the existing acceptance contract when the nonzero exit code is the consequence of enforced termination rather than a confirmed program failure.

No source, tests, canonical acceptance, owner decision, PR, provider, device, workflow or runtime was changed or exercised.

## Exact source pins

- `scripts/report_contract.py`, blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`
- `scripts/test_report_contract.py`, blob `85109f056009d65a274e9306deb39b68e1fefbd2`
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `PRODUCT/EXECUTION_CONTRACT.md`, blob `128a00a9b2a335514814cab76fb5781fe8f9f858`

## Source behavior

In `classify_verdict()`, current ordering is:

1. If exit_code is an integer other than bool and is nonzero, OR status is `program_failed`, return `FAIL`.
2. If status is `succeeded` and exit_code is integer zero, return `PASS`.
3. Otherwise return `INCOMPLETE`.

Consequently:
- `timed_out` + 137 => `FAIL`
- `cancelled` + 143 => `FAIL`
- `infrastructure_failed` + 1 => `FAIL`
- `timed_out` + null => `INCOMPLETE`

The formatter passes a validated integer exit code to this helper. The code excludes bools correctly, but does not condition nonzero-exit failure on a lifecycle status that actually establishes program failure.

## Contract conflict

The existing `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` says:
- Verdict `INCOMPLETE` covers timeout, cancellation, rejection, infrastructure failure, and missing/ambiguous terminal evidence.
- CASE-04 requires `INCOMPLETE / timed_out` when trusted execution control confirms the timeout.
- CASE-06 requires `INCOMPLETE / infrastructure_failed`.

The proposed `PRODUCT/EXECUTION_CONTRACT.md` separately defines `timed_out` as trusted server/provider deadline enforcement, `cancelled` as confirmed cancellation/termination, and says a provider retry must not turn unknown execution into success or fabricate an exit code.

A nonzero exit code alone does not establish that the user's program failed. It may be an OS/process termination code resulting from a trusted timeout, cancellation, worker shutdown or infrastructure intervention. Preserve both facts: lifecycle status and observed exit code.

## Existing test gap

The current unit test `test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete` calls these statuses with `exit_code=None`. It does not exercise nonzero termination codes. The helper therefore passes its current timeout test while retaining the precedence defect.

This audit does not claim the unit tests were executed.

## Proposed decision table for owner/reviewer approval

| Trusted lifecycle status | Exit code | Candidate verdict | Reason |
|---|---:|---|---|
| succeeded | 0 | PASS | Trusted success plus zero exit |
| succeeded | nonzero | FAIL or INCOMPLETE, per existing contract clarification | Contradictory terminal evidence must not be silently accepted |
| program_failed | any/unknown | FAIL | Explicit trusted program-failure outcome |
| timed_out | null | INCOMPLETE | Trusted timeout, no process code |
| timed_out | nonzero | INCOMPLETE | Nonzero may be termination consequence |
| cancelled | null/nonzero | INCOMPLETE | Cancellation is not program failure |
| rejected | null/nonzero | INCOMPLETE | Rejection is not program failure |
| infrastructure_failed | null/nonzero | INCOMPLETE | Infrastructure failure is not program failure |
| accepted/queued/running/unknown | any | INCOMPLETE | No trusted terminal program result |

The row `succeeded + nonzero` deserves separate owner clarification: if the trusted provider status says succeeded but the process exit is nonzero, the sources conflict. Do not let either source silently override the other. A conservative verdict is INCOMPLETE unless the approved contract defines which source is authoritative for that contradiction. The current implementation returns FAIL.

## Proposed pure-helper test matrix

Before a source change, add deterministic unit cases for:
1. Every lifecycle status crossed with exit code null, 0, 1, 124, 137, 143 and bool values.
2. `timed_out + 137` remains INCOMPLETE when timeout is independently trusted.
3. `cancelled + 143` remains INCOMPLETE when cancellation is independently trusted.
4. `infrastructure_failed + nonzero` remains INCOMPLETE absent trusted program-failure classification.
5. `succeeded + nonzero` is handled as the explicitly approved contradictory-evidence policy, not guessed.
6. `program_failed + null/0/nonzero` remains FAIL only where the status itself is trusted program-failure evidence.
7. Unknown/nonterminal status with any exit code does not become PASS.
8. Report preserves both lifecycle status and exit code without implying the exit code's cause.

Keep pure-helper tests distinct from fake coordinator, persistence, provider integration and actual process termination tests. Passing helper tests cannot prove that the timeout was enforced or that the worker stopped.

## Recommended implementation direction, pending review

Use the trusted lifecycle outcome as the first classification discriminator. Only a trusted `program_failed` status, or an explicitly approved unambiguous program-exit result, should yield FAIL. Treat timeout/cancel/rejection/infrastructure/unknown statuses as INCOMPLETE even when a termination code is present, while preserving the raw code and its provenance.

For `succeeded + nonzero`, record a contradiction and return INCOMPLETE unless the owner explicitly decides otherwise. Never fabricate the exit code or infer that a worker stopped from a browser/client timeout.

This is a recommendation, not an implementation decision or source patch. Claude should review the exact precedence semantics; Gemini should challenge whether any caller-controlled or untrusted status can influence the verdict and whether termination codes are authenticated/trusted.

## Disposition

- Static source behavior: CONFIRMED at pinned helper blob.
- Missing test coverage: CONFIRMED by current test source inspection.
- Runtime behavior: NOT RUN.
- Provider/process termination semantics: NOT PROVEN.
- Acceptance conflict: CASE-04 and CASE-06 make the intended incomplete classification explicit; contradictory `succeeded + nonzero` remains a separate open semantics issue.
- Canonical acceptance IDs/text: unchanged.
- Source/tests: unchanged.
- PR #2/#3: untouched.
