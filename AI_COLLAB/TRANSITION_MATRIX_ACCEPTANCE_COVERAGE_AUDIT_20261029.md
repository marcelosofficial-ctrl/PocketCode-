# Transition matrix — canonical acceptance coverage audit

**Date:** 2026-10-29. **Status:** research only; NOT RUN.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`.  
**Canonical source:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.  
**Matrix:** `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`, blob `ab570d38958193238494a4bdac3e9d022e03e9e0`.

This audit checks whether TPM-01..TPM-16 actually cover the canonical acceptance criteria. It does not amend acceptance or claim implementation. “Direct” means specified overlap only; “Partial” means additional assertions are required; “Gap” means this matrix does not establish the claim. All cases remain NOT RUN.

## LOOP coverage

| ID | Canonical intent | TPM linkage | Coverage finding |
|---|---|---|---|
| LOOP-01 | Phone-first script/input-file workflow | None | **Gap:** no mobile UX or selected-input test. |
| LOOP-02 | Honest lifecycle UI; simulated state labelled | TPM-01..16 indirectly | **Partial:** semantic projection is not a UI-state/simulation-label test. |
| LOOP-03 | PASS only on trusted completion + exit 0 | TPM-01, 05, 06, 15 | **Partial/direct semantics:** add missing/stale-gate and UI projection assertions; no real trusted source. |
| LOOP-04 | Program failure distinct from infrastructure failure | TPM-03..05 | **Partial:** separate wrapper/coordinator and child results only if both layers exist in chosen architecture. |
| LOOP-05 | Timeout/cancel/rejection/uncertainty never shown as success | TPM-06 | **Partial:** cancellation, rejection, and infrastructure-unknown cases need distinct tests. |
| LOOP-06 | Preserve structured check names/status/source | TPM-15 | **Gap:** forged PASS output does not test PASS/FAIL/SKIP/WARN fidelity or source labels. |
| LOOP-07 | Bounded useful diagnostics and file metadata | TPM-10..12 | **Partial:** test all required fields, all bounds, file metadata, and collector failure; define required streams per acceptance case instead of assuming every diagnostic stream is a universal PASS gate. |
| LOOP-08 | Copy result plus selectable-text fallback | None | **Gap:** no copy/paste or clipboard-failure test. |
| LOOP-09 | Preserve prior result; edit/rerun; identify runs | TPM-09, 14 | **Partial:** report versioning/attempt binding is not correction-loop UX. |
| LOOP-10 | Safe, bounded output-file listing/download | TPM-16 | **Partial:** release authorization is not path/name/size/list/download validation. |
| LOOP-11 | Copy excludes secrets, unrelated files, unbounded content | TPM-15 indirectly | **Gap:** requires seeded privacy fixtures and inspection of actual copied report. |
| LOOP-12 | Disposable isolation, externally enforced limits, egress denial | TPM-10, 16 | **Gap for core claim:** neither release gates nor output semantics prove isolation, egress denial, process limits, secret absence, or cleanup. |
| LOOP-13 | No unsupported cross-app/background automation claims | None | **Gap:** product-copy/UI and platform-capability audit needed. |
| LOOP-14 | $0 gate and no unapproved account/billing/workload | None | **Gap:** governance gate needed before provider selection or workload. |

## CASE coverage

| ID | Canonical scenario | TPM linkage | Coverage finding |
|---|---|---|---|
| CASE-01 | Valid script, expected output, exit 0 | TPM-01 | **Partial:** projection only; requires controlled run and trusted raw evidence. |
| CASE-02 | Syntax error before start | TPM-03..05 | **Partial/mislinked:** generic nonzero/contradiction is not a syntax-error fixture and diagnostic test. |
| CASE-03 | Runtime exception after partial output | TPM-03, 04 | **Partial/mislinked:** no real exception or partial-output retention assertion. |
| CASE-04 | Infinite loop/enforced deadline | TPM-06, 10 | **Partial:** no enforced deadline/confirmed termination proof. |
| CASE-05 | Cancellation while active | None | **Gap:** test confirmed stop, already terminal, and unknown termination. |
| CASE-06 | Worker/provider fails before program result | TPM-04 | **Partial:** contradiction is not a provider failure without a program result. |
| CASE-07 | Output exceeds configured limit | TPM-10 | **Partial/direct semantics:** prove external enforcement and bounded actual output. Test limit-caused termination separately from collection-only cap with trusted EXIT_ZERO and display-only truncation. CASE-07 requires explicit truncation/rejection evidence but does not prescribe one verdict for every cap behavior; D-01 remains open. |
| CASE-08 | Missing input or unsafe path/name | None | **Gap:** add safe pre-execution rejection/path-boundary cases. |
| CASE-09 | Exit 0 but script reports failed check | TPM-15 | **Partial:** test a named failed check while keeping process success distinct from task correctness. |
| CASE-10 | Prints PASS but exits nonzero | TPM-03, 05, 15 | **Direct semantics:** preserve raw text and trusted nonzero exit; still NOT RUN. |
| CASE-11 | Connection loss while execution continues | TPM-07, 08 | **Partial/mislinked:** event replay/conflict is not reconnect/backfill or same-run state lookup. |
| CASE-12 | Copy report after failed/incomplete run | TPM-02, 03, 09, 11, 12 | **Partial:** no actual copy action, selectable fallback, or full report payload test. |
| CASE-13 | Retry after ambiguous network response | TPM-07, 08, 13 | **Partial:** prove original run lookup by tenant/key/fingerprint, one dispatch maximum, and UNKNOWN if lookup cannot resolve. |
| CASE-14 | Path traversal/oversized output file | TPM-16 | **Gap/partial:** add path and size enforcement; release gates alone are insufficient. |
| CASE-15 | Outbound network/secret-read attempt | TPM-16 indirectly | **Gap:** no proof of enforced egress denial or absence of service credentials. |
| CASE-16 | Two runs finish out of start order | TPM-14 | **Partial/mislinked:** wrong-attempt evidence rejection does not test reversed completion order and report/artifact binding. |

## Important traceability corrections

1. TPM-07/08 are only partial for CASE-11/13: event replay is not reconnect recovery or idempotent dispatch.
2. TPM-14 is only partial for CASE-16: attempt binding is not a two-run out-of-order completion test.
3. TPM-16 is only partial for LOOP-10/12 and CASE-14/15: release checks do not prove file safety, runtime isolation, or egress denial.
4. TPM-02/03/09/11/12 cover report semantics for CASE-12, not actual copy/clipboard fallback.
5. TPM-03/04 cover nonzero-exit semantics, not CASE-02 syntax errors or CASE-03 partial output.
6. TPM-15 covers untrusted program output, not full LOOP-06 structured checks or LOOP-11 privacy.

## Recommended next increment

Keep TPM-01..16 as the focused lifecycle/projection suite. Add a separate canonical coverage supplement grouped by:
- Mobile/report UX: LOOP-01/02/06/08/09/11/13; CASE-09/12/16.
- Program/runtime observations: CASE-01..08 and CASE-10.
- Files/security: LOOP-10/12; CASE-14/15.
- Remote recovery/idempotency: CASE-11/13/16, only if remote asynchronous execution is selected.
- Governance: LOOP-14 and all pre-workload cost/authorization checks.

Each added case should specify preconditions, trusted evidence source, expected observation, verdict, disposition, artifact decision, report assertions, and cleanup. Mark environment-dependent cases BLOCKED until an approved boundary exists. Do not select a provider or launch a workload merely to close documentation gaps.

## Evidence and change control

Canonical acceptance remains unchanged at blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`. No canonical ID was renamed or removed. All TPM and proposed follow-on cases are NOT RUN. No runtime/provider selected; no app/backend behavior verified; no workload, account, billing change, merge, or deployment occurred.
