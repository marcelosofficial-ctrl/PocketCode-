# PocketCode — canonical acceptance traceability matrix
**Date:** 2026-10-29  
**Status:** Research planning only. NOT RUN. No implementation or provider selected. This maps the unchanged canonical acceptance plan; it does not redefine acceptance.

## Purpose

Keep every existing `LOOP-01..14` criterion and `CASE-01..16` scenario visible while separating (a) what a local iPhone comparator can teach us, (b) what requires a controlled execution service, and (c) what evidence would count. This closes a planning gap: a short CSV smoke test is useful but does not cover the complete acceptance set.

**Canonical source:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`), unchanged.  
**Related guides:** `AI_COLLAB/EXECUTION_PATH_DECISION_MATRIX_20261029.md`; `AI_COLLAB/STAGED_ACCEPTANCE_GATES_20261029.md`.

## Evidence status vocabulary

- **DOCUMENTED:** public docs or repository prose describe a feature; not independently verified.
- **SOURCE-COVERED:** source/tests contain relevant logic/assertions; does not mean tests ran or behavior works.
- **OBSERVED:** directly seen in a real test with environment and raw evidence recorded.
- **VERIFIED:** repeatable test with explicit expected/actual results and preserved evidence.
- **NOT RUN / UNKNOWN / BLOCKED:** no real test evidence, evidence absent, or environment unavailable.

Current execution evidence for this plan: **NOT RUN**. No criterion below should be read as passed.

## LOOP criteria traceability

| Canonical ID | Acceptance intent | Best first evidence | Local comparator contribution | Controlled service needed for full claim? |
|---|---|---|---|---|
| LOOP-01 | Phone-first code/input flow | iPhone capture of script and individually selected input file | Yes; directly tests usability | No |
| LOOP-02 | Honest lifecycle UI; simulated state visibly labelled | Capture state transitions and distinguish real vs simulated reports | Partial; app may not expose trusted lifecycle | For server lifecycle claims, yes |
| LOOP-03 | PASS only on trusted completion + exit 0 | Raw terminal evidence plus UI/report projection | Only if runtime exposes authoritative exit evidence | Usually for proposed server contract |
| LOOP-04 | Program error distinct from infrastructure error | Syntax/runtime failure with raw diagnostic and terminal evidence | Partial; app may conflate layers | Yes if service/wrapper failure is in scope |
| LOOP-05 | Timeout/cancel/rejection/uncertainty never shown as success | Controlled deadline/cancel cases and status evidence | Often cannot prove trusted termination | Yes for hosted untrusted execution |
| LOOP-06 | Structured checks preserve name/status/source | Fixture with PASS/FAIL/SKIP/WARN and source labels | Yes for report formatting; not check truth | No for formatting; independent validation needed for trusted checks |
| LOOP-07 | Bounded useful diagnostics | Report plus limits/truncation/unknown evidence; identify required streams per acceptance case | Partial; inspect actual bounds and collection behavior | Yes for server-enforced bounds |
| LOOP-08 | One complete bounded copy action; selectable fallback | Copy/paste report and test fallback when clipboard access fails | Yes | No |
| LOOP-09 | Preserve prior result; edit/rerun; identify runs | Two sequential runs with distinguishable inputs/results | Yes for local run history UX | Server run IDs needed for hosted claim |
| LOOP-10 | Safe, bounded output files and download | Actual output creation/open/export; unsafe name and size cases | Partial; local export only | Yes for authenticated hosted downloads |
| LOOP-11 | Copy excludes secrets/unrelated/unbounded content | Seed irrelevant/sensitive fixture values; inspect copied report | Yes for report privacy behavior | Service must also prevent secret injection/exposure |
| LOOP-12 | Disposable constrained execution, external limits, egress denied | Threat-model evidence plus controlled tests of limits/egress/cleanup | No reliable proof from ordinary app UX alone | Yes |
| LOOP-13 | No unsupported claims of cross-app/background automation | Product copy/UI audit against real iOS capability | Yes | No |
| LOOP-14 | $0 gate; no unapproved account/billing/workload | Current pricing/limits evidence and explicit owner authorization record before any workload | Yes, as governance evidence | Provider-specific review required before service selection |

## CASE scenario traceability

| Canonical ID | Scenario | Minimum evidence required | Gate |
|---|---|---|---|
| CASE-01 | Valid script exits 0 | Exact input, observed expected output, trusted terminal status/exit 0 | 1 smoke test, then 2 |
| CASE-02 | Syntax error before start | Real diagnostic and evidence supporting program failure | 2 |
| CASE-03 | Runtime exception after partial output | Partial output preserved, actual error, terminal status | 2 |
| CASE-04 | Infinite loop/deadline | Enforced deadline and trusted timeout/termination evidence; client timer alone is insufficient | 3 for hosted untrusted code |
| CASE-05 | Cancellation while active | Request and authoritative result: confirmed, already terminal, or unknown | 3 for hosted untrusted code |
| CASE-06 | Worker/provider fails before program result | Infrastructure failure evidence; no fabricated exit code | 3 |
| CASE-07 | Output exceeds cap | Configured cap, observed bounded output, explicit truncation/rejection; separate limit-caused termination from collection-only cap with EXIT_ZERO and report-only truncation | 2, then 3 for externally enforced cap. Canonical criterion does not prescribe one verdict for every cap behavior; D-01 remains an owner-review mapping. |
| CASE-08 | Missing/unsafe input path | Rejection before execution or evidenced program failure; no path escape | 1/2 |
| CASE-09 | Exit 0 but script reports failed check | Execution PASS kept distinct from task/check correctness; script check visible | 2 |
| CASE-10 | Prints “PASS” but exits nonzero | FAIL verdict, raw conflicting text and actual nonzero exit | 2 |
| CASE-11 | Connection lost while run continues | Reconnect resolves authoritative same-run state; no inference from disconnect | 3; remote-only |
| CASE-12 | Copy report after failure/incomplete | Complete bounded report preserves status, uncertainty, diagnostics and truncation | 1/2 |
| CASE-13 | Retry after ambiguous network response | Same request resolves to original run or authoritative unknown; no blind second dispatch | 3; remote idempotency boundary |
| CASE-14 | Unsafe/oversized output file | Path traversal/size rejected; only safe artifact metadata/link exposed | 2, then 3 for hosted store |
| CASE-15 | Outbound network/secrets attempt | Enforced egress denial; no service credentials in untrusted environment | 3; provider/runtime security gate |
| CASE-16 | Runs finish out of start order | Distinct run identifiers bind correct report/artifacts despite reordered completion | 2 for local UX; 3 for remote asynchronous jobs |

## Efficient execution order (not a reduction of scope)

1. **Boundary selection:** identify the actual environment and what evidence it can expose. No test if unavailable.
2. **Low-cost workflow signal:** CASE-01 and a clear malformed-input/program-failure case, real file artifact, report copy/paste. Label as smoke evidence only.
3. **Report correctness:** CASE-02, CASE-03, CASE-07, CASE-09, CASE-10, CASE-12, plus LOOP-06/07/08/11 and CASE-16-related UI behavior.
4. **Lifecycle/recovery:** CASE-04/05/06/11/13/16. These need trustworthy runtime/service controls; a local app cannot pass them merely by showing a timer or status label.
5. **Security/artifact boundaries:** CASE-08/14/15 and LOOP-10/12. Use a controlled test environment and evidence independent of the untrusted script.
6. **Governance and product honesty:** LOOP-13/14 before platform automation or provider workload. Do not create an account or launch a potentially billable workload to learn whether a free tier exists.

This ordering is a test-efficiency plan. All canonical acceptance criteria remain in force.

## Interpretation guardrails

- A local comparator can validate usability and report handoff; it cannot establish hosted multi-tenant isolation, server-enforced limits, provider-side termination, or durable recovery.
- A printed JSON object, mock, timer, boolean, or script-reported PASS is not authoritative evidence by itself.
- An exit code may be unavailable in some environments. Record UNKNOWN rather than manufacture it.
- `FAILED` versus `INCOMPLETE` projection remains an owner decision. Preserve observed execution outcome separately from job disposition.
- Artifact release is a separate fail-closed gate.
- The canonical contract and acceptance plan remain proposals, not implemented capabilities.

## Current state

- Canonical acceptance source unchanged at blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- All 14 LOOP criteria and 16 CASE scenarios are represented above.
- No provider, runtime, or adapter selected.
- No tests/workloads run; no evidence promoted beyond documented research.
- PR #2, PR #3, and main contract untouched.
