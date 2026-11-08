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


## 6. Static consistency supplement (2026-11-08; proposed, not owner-approved)

The immutable static audit is recorded in `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md`. The following clarifications are part of this proposal for independent review.

### 6.1 Current formatter compatibility limitation

The pinned `scripts/report_contract.py` implementation is not yet a renderer of an independently resolved verdict. `format_report()` calls `classify_verdict(status, exit_code)` itself. That helper returns FAIL for any valid nonzero exit code or `program_failed` status.

Therefore:
- EP-04 (`program_failed` plus natural child exit zero) and EP-05 (`succeeded` plus natural child nonzero) cannot currently render the proposed INCOMPLETE result while retaining those raw values in the two existing fields.
- Do not feed wrapper/signal/forced-termination values into the legacy `exit_code` field.
- Do not weaken or patch verdict precedence as a shortcut.
- Before implementation, define a typed, already-resolved projection result that retains raw lifecycle and child/wrapper/termination observations separately, and define how a pure renderer displays its pre-resolved verdict. Alternatively, explicitly defer EP-04/05 renderer coverage until a versioned report contract is approved.
- Authentication, process identity, event binding and policy trust remain coordinator/adapter responsibilities. The formatter stays a pure bounded renderer.

The typed projection vocabulary in §2 remains descriptive, not a frozen wire schema. A possible result must preserve both the resolved verdict and the raw contradictory facts; it must not erase the original lifecycle status merely to force the legacy helper to return INCOMPLETE.

### 6.2 Additional adversarial cases proposed

These are new proposal IDs only. They do not change CASE-01..16.

| Test | Input combination | Expected assertion |
|---|---|---|
| EP-21 | Deadline/cancellation/resource-limit termination requested, but termination acknowledgement is absent or lost | INCOMPLETE; termination NOT_CONFIRMED/UNKNOWN; cleanup and artifact release remain blocked where required |
| EP-22 | Wrapper exits zero, child exit is unobserved | INCOMPLETE; wrapper success is not child success |
| EP-23 | Child is terminated by signal/resource control; a shell-style code such as 137/143 is observed | Preserve signal/cause separately; do not call it a natural child nonzero exit; INCOMPLETE absent an independent trusted natural result |
| EP-24 | Natural child exit zero is trusted, but wrapper fails during post-run collection or cleanup | Preserve child and wrapper/cleanup facts separately; execution verdict vs artifact-release disposition requires owner-approved mapping |
| EP-25 | Timeout/resource limit and a purported natural child nonzero observation coexist | If trusted event ordering proves natural failure before the deadline, preserve that result; otherwise retain contradiction as INCOMPLETE pending reconciliation |

EP-21 and EP-23 close the gap between a termination request, a signal/forced termination and confirmed process exit. EP-22 prevents a successful wrapper shutdown from being mistaken for child success. EP-25 prevents numeric code precedence from deciding a timeout race without event provenance.

### 6.3 Explicit owner decisions required

- **EP-18:** if a child exits zero but the required policy/egress barrier is absent or mismatched, the minimum safe result is no PASS and a recorded policy-boundary violation. Whether the execution verdict is INCOMPLETE or another disposition, and whether any artifact may be retained/released, requires owner-approved security semantics.
- **EP-24:** if child execution succeeded but the wrapper failed during collection/cleanup, preserve the child result and wrapper failure separately. Define whether the execution verdict remains PASS while overall job disposition is degraded, or whether a required collection/cleanup gate makes it INCOMPLETE. Do not decide this in the formatter.
- **EP-04/05:** approve the resolved-verdict/renderer boundary before adding implementation tests. Preserve raw lifecycle and child observations.
- **Termination semantics:** define what evidence confirms process termination, how late exit observations are reconciled, and what cleanup can be called complete when termination is unconfirmed.

### 6.4 Existing test coverage boundary

The pinned tests cover direct succeeded+0, succeeded+nonzero, program_failed without a code, missing code, selected nonterminal statuses, timeout/cancel/rejection/infrastructure without a code, and bool rejection. They do not cover EP-04/05 contradictions, wrapper-vs-child identity, signal termination, stale observations, attempt binding or the new EP-21..25 cases. The current helper tests prove only deterministic two-field classification, not trusted provenance or coordinator projection.

**Verification remains unchanged:** this supplement is documentation-only. No source/tests changed, no tests/builds/device runs executed, and canonical LOOP/CASE/D identifiers remain unchanged.
