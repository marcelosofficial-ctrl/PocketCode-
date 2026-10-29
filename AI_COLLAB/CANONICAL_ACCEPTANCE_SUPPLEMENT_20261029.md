# PocketCode — canonical acceptance supplement

**Date:** 2026-10-29  
**Status:** Proposed test-planning supplement only; NOT RUN; no implementation authorization.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Canonical acceptance:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.  
**Companion audits:** `TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md`; `TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`.

## Purpose and guardrails

This file supplies 14 proposed supplementary test cases identified by the coverage audit. It supplements rather than replaces canonical LOOP-01..14 and CASE-01..16. It is not a schema, implementation, runtime choice, provider approval, or proof of behavior.

**Execution availability:** user is phone-only; PC/runtime/source state is not available for direct validation. All tests below are proposed and NOT RUN. Tests needing an actual app can be marked BLOCKED until the app is accessible; service/security tests remain BLOCKED until an execution boundary is explicitly selected and authorized. No account, workload, paid/free-tier assumption, or provider setup is authorized.

### Test readiness labels

- **DESIGN-READY:** test inputs/assertions can be specified now; execution still not authorized or performed.
- **PHONE-COMPARATOR:** potentially testable on a reachable phone app/browser without a PC, but only claims that the actual comparator exposes.
- **BOUNDARY-DEPENDENT:** requires a chosen runtime/service and trustworthy evidence source.
- **GOVERNANCE-GATED:** must not run before explicit owner authorization and current $0 verification.

## Supplement cases

| ID | Scope / canonical links | Preconditions and fixture | Required assertions | Readiness |
|---|---|---|---|---|
| SUP-UX-01 | Phone workflow; LOOP-01 | On an accessible iPhone, enter a short script and attach one explicitly selected input file | Script and input selection are user-driven; correct input is attached; no PC dependency is claimed unless observed | PHONE-COMPARATOR |
| SUP-UX-02 | Lifecycle UI honesty; LOOP-02/13 | Inspect every available status view and any sample/demo result | Validation, queued/running, and terminal states are distinct where supported; every simulated result is visibly labelled; copy/product text does not claim unsupported background or cross-app automation | PHONE-COMPARATOR |
| SUP-REPORT-01 | Structured checks; LOOP-06, CASE-09 | Fixture emits named PASS, FAIL, SKIP, WARN checks with an explicit source label; include a process exit 0 and a failed script-reported check | Preserve each name/status/source; do not equate process exit 0 with task correctness; label script-originated checks as unverified program output | PHONE-COMPARATOR for rendering; trusted validation BOUNDARY-DEPENDENT |
| SUP-REPORT-02 | Actual report copy; LOOP-07/08/11, CASE-12 | Produce success, failure, and incomplete reports; seed harmless synthetic secret-like and unrelated fixture values | Copy action yields one bounded complete report; selectable-text fallback works if clipboard action fails; unrelated/secret-like data is omitted; unavailable, empty, partial, and display-truncated streams are distinct | PHONE-COMPARATOR |
| SUP-REPORT-03 | Two-run correction loop; LOOP-09, CASE-16 | Run A and B with distinct synthetic inputs; make B finish first if the environment supports asynchronous runs | Reports/artifacts bind to the correct run IDs, prior report remains available, correction can be made and re-run, and reversed completion does not cross results | PHONE-COMPARATOR for local UX; BOUNDARY-DEPENDENT for remote jobs |
| SUP-RUN-01 | Valid program evidence; CASE-01 | Approved controlled environment; exact fixture and expected output recorded before run | Trusted terminal result and exit 0 match expected output; report does not trust a program-printed PASS as evidence | BOUNDARY-DEPENDENT; GOVERNANCE-GATED if provider workload |
| SUP-RUN-02 | Syntax/runtime failures; CASE-02/03/10 | Separate syntax-error fixture, runtime exception after a known output prefix, and script printing PASS before nonzero exit | Actual diagnostic and prefix retained; trusted nonzero exit yields FAIL; conflicting printed PASS remains raw output; wrapper/service failure is not misreported as child failure | BOUNDARY-DEPENDENT |
| SUP-RUN-03 | Timeout and cancellation; LOOP-05, CASE-04/05/06 | Controlled bounded-deadline fixture and an active run eligible for cancellation | Distinguish request from confirmed termination; capture authoritative terminal state; unknown termination remains INCOMPLETE; worker/provider failure before program result fabricates no exit code | BOUNDARY-DEPENDENT; GOVERNANCE-GATED if provider workload |
| SUP-RUN-04 | Output limit and collection; LOOP-07, CASE-07 | One trusted limit-caused termination fixture; one capture/retention-cap fixture with independent EXIT_ZERO if supported; one report-display truncation fixture; a collector-failure fixture if collection can fail independently | Preserve actual terminal evidence; distinguish limit-caused termination from capture-only and display-only truncation; output remains within externally enforced bounds; empty, unavailable, partial-failure, and truncated are not conflated. User-verdict mapping for confirmed limit-caused failure remains owner-open under D-01; case-specific required collection rules govern whether capture-only truncation can still yield PASS. | BOUNDARY-DEPENDENT |
| SUP-FILE-01 | Input path validation; CASE-08 | Missing input, unsafe filename, traversal attempt, and valid file | Unsafe/missing input is safely rejected or yields a clearly evidenced failure; no path escape; no success summary when required input is absent | BOUNDARY-DEPENDENT for untrusted runtime; local comparator only tests its own behavior |
| SUP-FILE-02 | Output artifact safety; LOOP-10/12, CASE-14 | Valid output, traversal-like output name, oversized output, mismatched job/attempt association | Only bounded safe artifacts appear; actual open/export/download works; no raw worker filesystem path is exposed; invalid/mismatched artifacts are denied | BOUNDARY-DEPENDENT |
| SUP-SEC-01 | Isolation and egress; LOOP-12, CASE-15 | Approved disposable environment; harmless outbound-connect attempt and synthetic environment-secret sentinel | Egress denial is observed from outside untrusted code; sentinel/service credentials are absent; runtime/resource enforcement and cleanup are evidenced independently of program output | BOUNDARY-DEPENDENT; GOVERNANCE-GATED |
| SUP-REC-01 | Lost acknowledgement and reconnect; CASE-11/13 | Fault-injected dispatch accepted but response lost; state lookup returns FOUND, terminal, or UNKNOWN | Resolve the original tenant/key/fingerprint to the same run; dispatch counter never exceeds one for automatic recovery; UNKNOWN remains unknown with no blind redispatch; reconnect reads authoritative same-run state | BOUNDARY-DEPENDENT |
| SUP-GOV-01 | Zero-cost and authorization gate; LOOP-14 | Before any provider account or workload, capture current authoritative pricing/limits, required permissions, and explicit owner authorization | No account, billing enablement, or potentially billable workload without approval and verified zero-cost conditions; if uncertainty remains, stop and mark BLOCKED | GOVERNANCE-GATED |

## Reuse existing TPM tests rather than duplicating them

The following stay in the lifecycle/projection suite and should be referenced rather than copied into a second matrix:

- TPM-01: zero exit with all mandatory gates confirmed.
- TPM-02/03: zero/nonzero outcomes with cleanup uncertainty.
- TPM-04/06: contradictory terminal evidence and timeout/exit conflict.
- TPM-07/08: identical event replay and event-ID conflict.
- TPM-09: append-only report version after late evidence.
- TPM-10/11: runtime output limit versus display truncation.
- TPM-12: partial collection failure versus empty stream.
- TPM-13: lost dispatch acknowledgement and no blind redispatch.
- TPM-14: reject evidence bound to another attempt.
- TPM-15: program-generated fake PASS is not authoritative.
- TPM-16: artifact release is denied when a current release gate fails.

These TPMs remain specifications, NOT RUN. They do not replace the additional real-boundary cases above where indicated.

## Execution order

1. **No-environment documentation work:** review fixture and expected-result definitions; keep acceptance IDs intact.
2. **Phone comparator, only when accessible:** SUP-UX-01/02, SUP-REPORT-01/02, and the locally applicable part of SUP-REPORT-03. Record exact app/runtime and raw observations. Do not call this hosted security acceptance.
3. **Controlled execution boundary:** SUP-RUN-01..04, SUP-FILE-01/02, SUP-REC-01, and the relevant TPM fake-adapter suite only after an approved boundary and implementation exist.
4. **Security and governance:** SUP-SEC-01 and SUP-GOV-01 before any claim of hosted untrusted-code safety or any provider workload.

## Evidence record required for each executed test

Record: test ID; canonical LOOP/CASE IDs; branch/commit; date; device/OS/app/runtime or service boundary; exact fixture/input; expected result written before execution; actual raw output and terminal evidence; report version/run ID; artifact metadata; cleanup/termination evidence; deviations; unknowns; and final label (OBSERVED or VERIFIED only when the evidence standard is actually met).

A screenshot or UI label alone does not establish trusted exit status, enforced isolation, egress denial, durable idempotency, or cleanup. If a test cannot expose the required evidence, record UNKNOWN/BLOCKED instead of PASS.

## Change control

- No canonical acceptance criterion is removed, renamed, or weakened.
- No provider/runtime is selected by this supplement.
- No code or test was run to create this document.
- No account, billing change, workload, merge, deployment, or production action occurred.
