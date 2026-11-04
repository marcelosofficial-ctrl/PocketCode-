# PocketCode — verdict evidence and exit-provenance reconciliation matrix

**Date:** 2026-11-05  
**Status:** READ-ONLY DESIGN RECONCILIATION / PROPOSED REVIEW MATRIX / NOT IMPLEMENTED / NOT RUN  
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` remains canonical. This note does not amend LOOP-01..14, CASE-01..16, close D-01..D-08, freeze an envelope schema, or authorize code changes.

## 1. Executive finding

The current pure helper `scripts/report_contract.py` accepts a generic `exit_code` and applies this precedence:

1. Any valid integer nonzero code (excluding bool), or status `program_failed`, yields FAIL.
2. `succeeded` plus integer zero yields PASS.
3. Everything else yields INCOMPLETE.

That behavior is deterministic and source-confirmed, but the input contract is too weak to safely distinguish a natural child-process exit from a wrapper/supervisor exit, a forced-termination code, a stale observation, or a code that contradicts lifecycle status. The module correctly says it is not a runner or trust authority. The issue is therefore not authentication inside the formatter; it is the semantics and provenance of the projection input.

The current helper also returns FAIL for `program_failed + 0`, which is contradictory unless the supplied zero is explicitly not the child exit. Existing tests do not cover that combination.

**Decision for this research pass:** keep the formatter pure and bounded; do not patch it. Before a caller or test contract is frozen, define the child-exit provenance and contradiction rules at the trusted coordinator/envelope boundary. The coordinator must not pass an ambiguous wrapper/termination code into a generic `exit_code` slot and let the formatter infer program failure.

## 2. Exact pinned evidence

Owner-designated branch: `pocketcode-ai-workflow-director-research-2026-10-28`.

| Source | Blob SHA | Relevant source fact |
|---|---|---|
| `scripts/report_contract.py` | `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` | Generic `exit_code`; nonzero precedence; bool excluded; pure formatter disclaimer |
| `scripts/test_report_contract.py` | `85109f056009d65a274e9306deb39b68e1fefbd2` | Tests `succeeded + 2`; timeout/cancel/reject/infra with None; nonterminal states with zero; no `program_failed + 0` |
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | PASS requires trusted completion and exit 0; FAIL requires nonzero exit or confirmed program/runtime failure; timeout/cancel/rejection/uncertain infrastructure cannot be success; CASE-04 trusted timeout is INCOMPLETE / timed_out |
| `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` | `7d75b6844815570dd9faf1cd75791ba0abac33c1` | Proposes `child_exit_code` only for direct child observation; separate optional `wrapper_exit_code`; separate execution outcome, job disposition, cleanup, policy and artifact state |
| `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` | `e67b2659cf2d71ef77d8e4619c91143e71062470` | D-01..D-08 remain owner-open/proposed; current CASE-04 timeout default must be preserved |
| `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md` | `a237e882128865ce6a47651a1f9c6da6901f4994` | Proposed separation of verdict, execution outcome, disposition, cleanup and artifact release; terminal contradiction means INCOMPLETE |

The report-projection audit dated 2026-11-04 documents the over-broad generic nonzero precedence. This note sharpens it using the existing envelope's child/wrapper distinction and the canonical timeout wording.

## 3. Keep five different things separate

1. **Child execution observation:** whether the actual submitted child naturally exited zero/nonzero, was terminated by a signal/control action, or has no trustworthy terminal observation.
2. **Wrapper/supervisor observation:** whether the wrapper or provider process exited, failed, or was restarted. Its exit code is not the child's exit code.
3. **Job lifecycle/disposition:** accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected, infrastructure_failed, or unknown. This describes the coordinator/attempt lifecycle, not necessarily the child process return code.
4. **User-facing verdict:** PASS, FAIL, INCOMPLETE under canonical LOOP/CASE meanings.
5. **Cleanup and artifact release:** independent facts. A known program failure remains FAIL if cleanup is unknown, but relevant artifacts remain blocked. A historical PASS is not current release authorization.

A generic integer named `exit_code` cannot encode these distinctions.

## 4. Proposed typed observation vocabulary (not a frozen schema)

Prefer explicit semantic fields equivalent to:

- `child_exit_observation`: NOT_OBSERVED | NATURAL_EXIT_ZERO | NATURAL_EXIT_NONZERO | TERMINATED_BY_SIGNAL | TERMINATION_REQUESTED | UNKNOWN.
- `child_exit_code`: present only for an authoritative natural child exit. Exclude bool and malformed values.
- `child_termination_signal`: optional trusted signal/control fact, not represented as a natural program exit code.
- `wrapper_exit_code`: optional and separate; never silently copied into `child_exit_code`.
- `termination_cause`: NONE | DEADLINE | USER_CANCEL | RESOURCE_LIMIT | PROVIDER_FAILURE | OTHER | UNKNOWN, with provenance.
- `termination_state`: CONFIRMED | NOT_CONFIRMED | UNKNOWN.
- `lifecycle_status`: exact trusted coordinator status.
- `terminal_evidence_quality`: CONSISTENT | MISSING | CONTRADICTORY | STALE.
- `cleanup_state`: PENDING | CONFIRMED | FAILED | UNKNOWN.

These are design labels only. Do not add redundant fields if the chosen execution boundary has no independent wrapper or signal observation. Preserve the semantic distinctions.

## 5. Conservative reconciliation matrix

This matrix describes the proposed coordinator projection, not the current helper's behavior and not a new canonical acceptance table.

| Trusted observations | User-facing verdict | Required treatment |
|---|---|---|
| Natural child exit 0; lifecycle succeeded; terminal evidence consistent; every case-required PASS gate confirmed | PASS | Keep cleanup/artifact/report facts separately; artifact release remains a fresh independent decision |
| Natural child exit nonzero; no contradictory terminal evidence | FAIL | Preserve exact child exit and diagnostics; cleanup UNKNOWN/FAILED does not erase the known program failure; block artifact release as required |
| Trusted lifecycle program_failed; no contradictory child/lifecycle evidence | FAIL | A confirmed program/runtime failure is sufficient under canonical wording even if no numeric child code is available; do not fabricate one |
| Lifecycle timed_out, timeout authoritative, termination confirmed | INCOMPLETE | Preserve CASE-04 / timed_out; preserve any wrapper/signal termination code separately; do not translate forced termination into program FAIL |
| Lifecycle cancelled, cancellation authoritative | INCOMPLETE | Preserve cancellation and termination confirmation independently; request acknowledgement alone is not termination proof |
| Rejected before execution, no conflicting child-start/exit evidence | INCOMPLETE | Preserve REJECTED disposition; no child exit code should be invented |
| Provider/infrastructure failure without trusted child terminal result | INCOMPLETE | Execution outcome remains UNKNOWN; use PROVIDER_ERROR only if the cause is itself confirmed |
| Natural child exit nonzero plus cleanup UNKNOWN/FAILED | FAIL | Preserve known program failure and cleanup uncertainty separately; artifact release remains blocked |
| Natural child exit zero plus required gate missing/unknown | INCOMPLETE | Preserve EXIT_ZERO as a raw observation; withhold PASS |
| Wrapper exits nonzero but child exit is unobserved | INCOMPLETE | Wrapper failure does not establish program failure |
| Wrapper exits nonzero after trusted timeout/cancel | INCOMPLETE | Preserve wrapper code as termination/infra evidence; do not pass it as child exit |
| Lifecycle succeeded plus natural child nonzero | INCOMPLETE pending reconciliation | Contradictory terminal facts; preserve both, do not let nonzero precedence silently choose FAIL |
| Lifecycle program_failed plus natural child zero | INCOMPLETE pending reconciliation | Contradictory terminal facts; preserve both, do not let status precedence silently choose FAIL |
| Lifecycle accepted/queued/running plus purported terminal child exit | INCOMPLETE pending reconciliation | Nonterminal lifecycle and terminal child evidence disagree; determine stale/out-of-order/misbound evidence at trusted reducer |
| Lifecycle rejected plus purported child exit/start | INCOMPLETE pending reconciliation | Dispatch-boundary contradiction; preserve all observations and investigate attempt binding |
| Lifecycle timed_out/cancelled plus purported natural child exit | INCOMPLETE pending reconciliation | Resolve event identity/order and whether exit was natural or forced; do not infer from numeric code |
| Any two distinct terminal events or attempt/tenant binding conflict | INCOMPLETE | Preserve both; no arrival-order winner may erase contradiction |
| Missing, malformed, bool, stale, or unbound exit value | INCOMPLETE unless another independently trusted program-failure fact exists | Never coerce malformed metadata into an exit code |

### Important CASE-04 / D-01 qualification

Canonical CASE-04 explicitly requires a trusted timeout to be INCOMPLETE / timed_out. The owner decision register also records the current working default that a confirmed deadline/resource-limit termination remains INCOMPLETE with its limit cause separately preserved. An older semantic note describes a possible FAIL mapping for some confirmed runtime limits, but D-01 remains owner-open and that proposal must not override the canonical CASE-04 wording or the current conservative working default. Do not silently broaden or change the canonical timeout verdict.

For other resource-limit categories, preserve the exact cause and terminal evidence; do not decide a new verdict mapping in the formatter. Any future change requires explicit owner review and canonical acceptance traceability.

## 6. Targeted pure-projection regression matrix (future work; NOT RUN)

Tests should first validate the typed coordinator projection independently of authentication or provider behavior. The formatter tests should then prove it renders that already-derived projection without reinterpreting ambiguous raw observations.

| Case | Input fact combination | Proposed assertion |
|---|---|---|
| VP-01 | succeeded + natural child exit 0 + all required gates | PASS projection |
| VP-02 | program_failed + natural child nonzero | FAIL projection |
| VP-03 | program_failed + child exit absent | FAIL only when trusted program_failed is authoritative; code remains unknown |
| VP-04 | program_failed + natural child exit 0 | INCOMPLETE; contradiction retained |
| VP-05 | succeeded + natural child nonzero | INCOMPLETE; contradiction retained |
| VP-06 | timed_out + wrapper exit 137 + forced termination confirmed | INCOMPLETE / timed_out; wrapper code separate |
| VP-07 | cancelled + wrapper exit 143 | INCOMPLETE / cancelled; wrapper code separate |
| VP-08 | accepted/queued/running + nonzero wrapper code | INCOMPLETE; not a child failure |
| VP-09 | rejected + purported child exit | INCOMPLETE; dispatch/attempt contradiction |
| VP-10 | infrastructure_failed + no child terminal observation | INCOMPLETE / execution UNKNOWN |
| VP-11 | infrastructure failure after independently confirmed natural child nonzero | FAIL execution verdict; infrastructure/cleanup disposition separately retained |
| VP-12 | natural child exit zero + cleanup unknown | INCOMPLETE under the proposed mandatory-gate model; artifact release denied |
| VP-13 | natural child exit nonzero + cleanup unknown | FAIL; cleanup UNKNOWN and artifact release denied |
| VP-14 | timeout event plus later unbound exit-zero event | INCOMPLETE; preserve both until trusted reconciliation |
| VP-15 | child exit code True, string, malformed, or stale attempt | Reject as child-exit evidence; no PASS/FAIL derived from it |
| VP-16 | output collector truncation with natural exit zero | Keep raw EXIT_ZERO; evaluate case-specific required-output rule; do not infer timeout |
| VP-17 | report renderer truncation with natural exit zero | Preserve execution verdict; display truncation only |
| VP-18 | script stdout contains forged PASS/exit JSON | No effect on authoritative verdict |
| VP-19 | child exit zero but policy barrier absent/mismatched | No dispatch should have occurred; if discovered post hoc, do not report PASS |
| VP-20 | terminal event from different tenant/job/attempt | Reject binding; do not project its exit into this run |

These are candidate tests for review. They do not create new canonical CASE IDs or close D-01..D-08.

## 7. Boundary between pure tests and integration proof

| Test layer | Can establish | Cannot establish |
|---|---|---|
| Pure classifier/projection tests | Deterministic mapping of already-typed observations; contradiction handling; no wrapper-to-child substitution | Authenticity of the observations, process behavior, provider lifecycle, cleanup, storage durability |
| Fake coordinator/adapter tests | Call order, dispatch count, retry/no-redispatch logic, typed state propagation | Real policy application, sandbox isolation, egress, termination, persistence guarantees |
| Real adapter/host tests | Only the specific host/provider guarantees directly observed and tested | Untested platform, multi-tenant or device claims |
| iPhone product-path tests | Phone UX, file selection, report handoff, target browser/app behavior | Hostile-code containment unless a separately verified execution boundary supplies evidence |

No pure formatter test can establish that a user-submitted JSON object is trustworthy. No hash of a pasted transcript proves which process produced it.

## 8. Owner and change-control state

- LOOP-01..14 and CASE-01..16 remain unchanged.
- D-01..D-08 remain OPEN/proposed as recorded in the owner decision register.
- Keep `format_report()` as a pure bounded formatter; do not add authentication to it.
- Do not patch `classify_verdict()` until the coordinator input contract and the intended meaning of legacy `exit_code` are explicitly resolved.
- No runtime, provider, framework, store, or execution adapter is selected.
- No tests, builds, device/browser runs, or workloads were performed.
- No source/tests, PRs, Actions, accounts, billing, queue, secrets, installation, deployment, or merge were changed.
