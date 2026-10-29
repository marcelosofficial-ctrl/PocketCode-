# PocketCode — staged acceptance gates (preserve canonical scope)
**Date:** 2026-10-29  
**Status:** Research clarification only. No code or tests run. No canonical acceptance criteria changed. No provider selected.

## Why this clarification is necessary

The two fixed CSV cases in `AI_COLLAB/EXECUTION_PATH_DECISION_MATRIX_20261029.md` are a small **workflow smoke test**, not the complete PocketCode first-useful-proof milestone. The canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` defines a broader milestone: controlled success and program-failure runs, timeout, bounded report, real input-to-output transformation, report handoff to a separate AI assistant for correction, and evidence for isolation, egress, resource limits, cancellation, and cleanup.

Do not downgrade the canonical acceptance scope to make an early comparator experiment look complete. This file adds a staged path toward the existing criteria; it does not replace or amend the canonical documents.

## Gate 0 — choose a testable boundary

Before testing, state which environment is actually being evaluated:
- Existing iPhone Python app as a user-workflow comparator;
- Browser-local Python/Pyodide;
- PocketCode-owned/provider-backed execution service.

Record the exact app/runtime/version if visible. Do not assume local and hosted environments have equivalent process boundaries, termination guarantees, or security controls. If the environment is inaccessible, stop and record BLOCKED/NOT RUN; do not simulate results.

## Gate 1 — workflow smoke test (learning only)

Run only when the environment is available and the test action is authorized:
1. Valid CSV produces the expected calculated values and a real output artifact.
2. Malformed CSV produces a clear error and no valid-looking summary.
3. Output file can actually be opened/exported and the evidence can be copied into a separate AI assistant.
4. Record all unknowns: status/exit code, stdout/stderr availability, capture completeness, termination, runtime limits, isolation, and cleanup.

**Pass means only:** this environment demonstrated the tested user workflow for these cases. It does not prove PocketCode acceptance, secure execution, or production suitability.

## Gate 2 — execution-loop behavior

Against the canonical acceptance plan, separately demonstrate:
- trusted terminal status and exact lifecycle state; acceptance/queued is not success;
- success and nonzero program failure, including a script that prints “PASS” but exits nonzero;
- deadline/timeout and cancellation, with termination claimed only when trusted controls confirm it;
- bounded stdout/stderr and report/file outputs, with truncation distinct from unavailable or failed collection;
- real input-to-output file transformation, safe file names/paths, and actual artifact access;
- same-key retry/reconnect behavior after an ambiguous response, without blindly dispatching a second run;
- report copied to another AI assistant, followed by a correction that is re-executed and evidenced.

A local comparator may be unable to demonstrate some service-specific criteria. Mark them NOT APPLICABLE TO THIS COMPARATOR or UNKNOWN with rationale; do not count them as passed.

## Gate 3 — hosted execution safety and service acceptance

Only if a hosted service is being considered, require evidence for:
- authenticated tenant/user scoping on read, cancel, and artifact download;
- runtime and resource limits enforced outside the untrusted program;
- outbound network denied by default and no provider/service secrets exposed to the run;
- trusted timeout/cancellation and cleanup behavior;
- safe artifact association, bounded output, and authorization before release;
- idempotency and authoritative state lookup after a lost/ambiguous response;
- exact policy revision/ETag confirmation before dispatch if policy can change;
- abuse controls and a documented retention/cleanup policy.

A provider's feature description, a boolean flag, a mock, or a unit-test model is not evidence of these live guarantees. If a candidate cannot provide enforceable termination or network restrictions for untrusted code, treat that as a selection blocker rather than papering over it in report formatting.

## Evidence labels

Use these labels consistently:
- **DOCUMENTED:** a source/document says the capability exists; not independently verified.
- **SOURCE-COVERED:** code/test source contains relevant logic/assertions; not proof tests ran or behavior works.
- **OBSERVED:** directly seen in a real test, with environment and raw evidence recorded.
- **VERIFIED:** independently repeatable test with explicit expected/actual results and preserved evidence.
- **UNKNOWN / NOT RUN / BLOCKED:** evidence is absent, the test was not executed, or the environment was unavailable.

Do not promote DOCUMENTED or SOURCE-COVERED to OBSERVED/VERIFIED. Keep failures, uncertainty, and unavailable evidence visible.

## Gate exit rule

No architecture/provider decision follows automatically from Gate 1. Use smoke-test results to learn about mobile usability and artifact flow. Advance to a provider comparison only when a concrete requirement cannot be met by the comparator, or when a required security/lifecycle guarantee inherently depends on a controlled execution service. Then evaluate candidates against the canonical acceptance criteria, current $0 constraints, and verifiable evidence.

## Current state

- Canonical `PRODUCT/EXECUTION_CONTRACT.md` and `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` unchanged.
- Existing two-case checklist is a smoke test only.
- Pyodios and browser-local paths have not been hands-on tested in this research pass.
- No provider selected; no test or workload run.
- No changes to PR #2, PR #3, or main.
