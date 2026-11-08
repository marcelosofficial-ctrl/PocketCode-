# Exit provenance resolution: child, wrapper and termination

**Date:** 2026-11-08  
**Status:** PROPOSED SPECIFICATION AND TEST DESIGN / NOT IMPLEMENTED / NOT RUN  
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` remains canonical. This note does not amend LOOP-01..14, CASE-01..16, or D-01..D-08. It does not freeze an envelope schema or authorize source changes.

## 1. Problem and boundary

The pinned pure helper `scripts/report_contract.py` accepts one generic `exit_code`. `classify_verdict()` currently returns FAIL for any valid nonzero integer before checking lifecycle status, or for `program_failed`; it returns PASS for `succeeded + 0`; otherwise it returns INCOMPLETE. It correctly excludes bool from integer exit codes.

That input is insufficient to distinguish:
- the submitted child process naturally exiting;
- a wrapper, worker, browser, or provider process exiting;
- a child being killed by timeout, cancellation, or resource control;
- a termination request from confirmed termination;
- a stale, delayed, contradictory, or misbound terminal observation.

The formatter is intentionally not a runner, authentication authority, or lifecycle coordinator. Do not add trust verification to it. The trusted coordinator must resolve typed observations before producing the bounded report projection.

## 2. Required semantic facts

Keep these facts distinct. Names below are descriptive labels, not a frozen wire schema.

| Fact | Meaning | Rule |
|---|---|---|
| Child exit observation | Natural child exit, signal termination, requested termination, not observed, or unknown | Only a trusted natural child exit may supply a child exit code |
| Child exit code | Code returned by the actual submitted child after natural exit | Integer excluding bool; never copy wrapper/provider code into it |
| Wrapper exit | Exit of supervisor, worker, browser, or provider wrapper | Preserve separately; alone it does not establish child success or failure |
| Termination cause | Deadline, user cancellation, resource limit, provider failure, other, none, unknown | Preserve cause and source; numeric signal/code does not replace cause |
| Termination state | Confirmed, not confirmed, unknown | A request or browser disconnect is not confirmation |
| Lifecycle status | accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected, infrastructure_failed, unknown | Preserve exact trusted status; it is not itself a child return code |
| Evidence quality | consistent, missing, contradictory, stale, unbound | Contradictions are retained, not resolved by arrival order or numeric precedence |
| Cleanup and artifact state | pending, confirmed, failed, unknown; release allowed/blocked | Separate from execution verdict; unknown cleanup blocks release where required |

Attempt, execution, tenant and event identity must be bound before an observation can participate in the projection. Authentication and binding belong to the trusted adapter/coordinator, not the report formatter.

## 3. Conservative projection rules

| Trusted facts | Verdict | Required treatment |
|---|---|---|
| Natural child exit 0 + lifecycle succeeded + consistent terminal evidence + all case-required gates confirmed | PASS | Retain cleanup and artifact-release decisions separately |
| Natural child exit nonzero + no contradictory terminal evidence | FAIL | Preserve exact child code and diagnostics |
| Trusted lifecycle program_failed + no contradictory child/lifecycle evidence | FAIL | A confirmed program/runtime failure is sufficient without inventing a numeric code |
| timed_out + authoritative timeout + termination confirmed | INCOMPLETE | Preserve CASE-04 / timed_out; wrapper/signal code remains separate |
| cancelled + authoritative cancellation | INCOMPLETE | Preserve whether termination is confirmed; a request alone is not proof |
| rejected before execution, with no child-start/exit contradiction | INCOMPLETE | Do not invent a child exit |
| infrastructure_failed without trusted child terminal result | INCOMPLETE | Child outcome remains unknown |
| wrapper nonzero + child exit unobserved | INCOMPLETE | Wrapper failure is not child failure |
| wrapper nonzero after timeout/cancellation | INCOMPLETE | Preserve wrapper code as separate termination/infrastructure evidence |
| child exit zero + required gate missing/unknown | INCOMPLETE | Preserve raw EXIT_ZERO; withhold PASS |
| child exit nonzero + cleanup unknown/failed | FAIL | Preserve known failure; block artifact release as required |
| succeeded + natural child nonzero | INCOMPLETE pending reconciliation | Preserve contradiction; do not choose FAIL by nonzero precedence |
| program_failed + natural child zero | INCOMPLETE pending reconciliation | Preserve contradiction; do not choose FAIL by status precedence |
| accepted/queued/running + purported terminal child exit | INCOMPLETE pending reconciliation | Investigate ordering, staleness and attempt binding |
| rejected + purported child start/exit | INCOMPLETE pending reconciliation | Investigate dispatch-boundary contradiction |
| timed_out/cancelled + purported natural child exit | INCOMPLETE pending reconciliation | Resolve event identity and natural-vs-forced termination |
| stale, malformed, bool, or unbound exit value | INCOMPLETE | It is not child-exit evidence; another independent trusted failure fact may still establish FAIL |
| two distinct terminal events or tenant/job/attempt mismatch | INCOMPLETE | Preserve both observations; no last-writer/arrival-order winner |

**CASE-04 guard:** canonical acceptance requires trusted timeout to remain INCOMPLETE / timed_out. Do not map forced termination codes such as 137 or 143 to program FAIL. The current conservative working default for confirmed deadline/resource-limit termination remains INCOMPLETE with the cause separately preserved. Any other resource-limit verdict mapping requires explicit owner review. This note does not resolve D-01.

## 4. Adversarial regression cases

These are proposed pure-projection/coordinator tests, not new canonical CASE IDs. Inputs must model trusted observations and provenance, not merely caller-supplied JSON.

| Test | Input combination | Expected assertion |
|---|---|---|
| EP-01 | succeeded; natural child exit 0; all required gates confirmed | PASS |
| EP-02 | natural child exit nonzero; no conflicting lifecycle fact | FAIL; exact child code retained |
| EP-03 | trusted program_failed; child exit absent | FAIL; child code remains unknown |
| EP-04 | program_failed + natural child exit 0 | INCOMPLETE; contradiction retained |
| EP-05 | succeeded + natural child nonzero | INCOMPLETE; contradiction retained |
| EP-06 | timed_out; wrapper exit 137; forced termination confirmed | INCOMPLETE / timed_out; child exit remains absent |
| EP-07 | cancelled; wrapper exit 143 | INCOMPLETE / cancelled; wrapper code is not child code |
| EP-08 | running; wrapper exit nonzero; child exit unobserved | INCOMPLETE |
| EP-09 | infrastructure_failed; no child terminal observation | INCOMPLETE; child outcome unknown |
| EP-10 | infrastructure failure after independently trusted natural child nonzero | FAIL execution verdict; preserve separate infrastructure disposition |
| EP-11 | natural child exit 0; mandatory output/verification gate missing | INCOMPLETE; no PASS |
| EP-12 | natural child nonzero; cleanup unknown | FAIL; artifact release blocked |
| EP-13 | rejected; purported child start or exit | INCOMPLETE; dispatch/attempt contradiction |
| EP-14 | terminal event belongs to another tenant/job/attempt | Reject binding; do not project its exit into this run |
| EP-15 | child exit value is bool, string, malformed or stale | Reject as child-exit evidence; no verdict from that value |
| EP-16 | timeout event followed by late, unbound exit-zero event | INCOMPLETE; preserve both until trusted reconciliation |
| EP-17 | timed_out plus purported natural child exit | INCOMPLETE; resolve ordering and natural-vs-forced semantics |
| EP-18 | child exit zero but policy/egress barrier absent or mismatched | No PASS; record policy-boundary violation and investigate dispatch |
| EP-19 | output collector truncates after natural child exit zero | Preserve EXIT_ZERO; apply case-specific output requirement; do not infer timeout |
| EP-20 | wrapper restarts and reports a new code without child identity continuity | INCOMPLETE; no substitution or replay-based inference |

A formatter unit test can establish deterministic projection only. It cannot prove process identity, credential authenticity, real termination, sandbox isolation, persistence, or provider behavior. Those require adapter/host integration evidence.

## 5. Implementation sequencing and non-goals

1. First agree the typed coordinator observation contract and provenance rules.
2. Add pure projection tests for the combinations above, including contradictions and invalid child-code types.
3. Keep `format_report()` a bounded renderer of an already-resolved result. If legacy `exit_code` remains, define it explicitly as child-only or deprecate it; never silently reinterpret wrapper exit.
4. Add adapter integration tests for child identity, trusted lifecycle source, termination acknowledgement, stale-event rejection, cleanup and artifact-release gates.
5. Do not select a runtime, provider, database, transport or envelope serialization here.

**Pinned sources:** `scripts/report_contract.py` blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`; `scripts/test_report_contract.py` blob `85109f056009d65a274e9306deb39b68e1fefbd2`; `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`; `AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md` blob `f146bd45cdbc3e7f6f1301ad3c0e172ffa4443d7`.

**Verification:** documentation-only. No code changed, no tests/builds/device runs executed, and no canonical LOOP/CASE/D identifier changed.
