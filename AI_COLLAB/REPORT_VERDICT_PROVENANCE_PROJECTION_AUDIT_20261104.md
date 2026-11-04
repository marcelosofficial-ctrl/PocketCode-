# PocketCode report verdict projection and provenance audit

**Date:** 2026-11-04  
**Status:** READ-ONLY STATIC SOURCE/CONTRACT RECONCILIATION / NO TESTS EXECUTED  
**Repository:** `marcelosofficial-ctrl/PocketCode-`  
**Owner-designated branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Also present:** the separate `pocketcode-execution-boundary-crosswalk-2026-11-01` branch contains the same exact helper/test blobs. This audit is authored on the owner-designated branch; it does not merge or copy branch histories.

## 1. Executive decision

Keep `scripts/report_contract.py` a pure, bounded report projection helper. **Do not make it pretend to authenticate execution evidence.** Its module and formatter docstrings explicitly state that input comes from a caller and that the helper is not a runner, provider adapter, API, or source of trusted metadata. That is an appropriate separation of responsibility.

The required trust guarantee belongs at the ingress/coordinator boundary described by the existing `ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`: only a trusted coordinator should construct/validate the envelope supplied to the formatter; raw client/task/script/report JSON must not set authoritative lifecycle, exit, policy, cleanup, artifact or tenant fields.

However, the helper's current verdict function has a separate **precedence gap**: any integer nonzero `exit_code` returns FAIL before lifecycle status is considered. This includes nonterminal and non-program terminal statuses. The only nonzero test exercises `succeeded + 2`; timeout/cancel/infrastructure tests use `None`, and nonterminal tests use `0`. Thus the test matrix does not cover the problematic combinations.

Executive recommendation:
1. Keep report formatting separate from evidence authentication.
2. Before any production caller exists, specify and test an ingress contract that binds trusted observations to one tenant/job/run/attempt and authenticated producer.
3. Reconcile the projection rule so a forced-termination/wrapper exit code cannot override a trusted timeout/cancel/infrastructure lifecycle outcome.
4. Distinguish a natural child-process nonzero exit from a wrapper/worker termination code.
5. Treat `succeeded + nonzero` and other impossible combinations as contradictory evidence, not as a silently trusted precedence.
6. Do not implement or change canonical acceptance until Claude/Gemini review and owner approval are reconciled.

## 2. Exact source pins and branch verification

The owner-designated branch was freshly read and contains these exact blobs:

- `scripts/report_contract.py`: `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`
- `scripts/test_report_contract.py`: `85109f056009d65a274e9306deb39b68e1fefbd2`
- `PRODUCT/EXECUTION_CONTRACT.md`: `128a00a9b2a335514814cab76fb5781fe8f9f858`
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`: `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`: `7d75b6844815570dd9faf1cd75791ba0abac33c1`
- `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`: `e67b2659cf2d71ef77d8e4619c91143e71062470`

The helper/test hashes on the separate execution-boundary branch were re-fetched and are identical. The report-projection finding can therefore be discussed against the owner-designated source snapshot without transferring source files between branches.

## 3. Source-confirmed helper behavior

### 3.1 Current precedence

The helper currently performs these checks in order:

1. If `exit_code` is an integer other than bool and nonzero, **or** status is `program_failed`, return `FAIL`.
2. If status is `succeeded` and exit code is integer zero, return `PASS`.
3. Otherwise return `INCOMPLETE`.

The explicit bool exclusion is correct: Python `bool` is a subclass of `int`, so `True` is not accepted as an exit code.

### 3.2 Over-broad nonzero precedence

Because nonzero code is checked before status, the current helper returns FAIL for all of these combinations:

| Status supplied to helper | Exit code | Current result | Why this needs review |
|---|---:|---|---|
| accepted | 1 | FAIL | Accepted is not proof a child program ran or terminated |
| queued | 1 | FAIL | Queued is nonterminal |
| running | 1 | FAIL | Running is nonterminal; code may be stale, wrapper-level or mismatched |
| rejected | 1 | FAIL | Rejection ordinarily means the requested execution was not dispatched |
| timed_out | 137 | FAIL | 137 may be a termination consequence; canonical timeout is INCOMPLETE / timed_out |
| cancelled | 143 | FAIL | Cancellation is not program failure |
| infrastructure_failed | 1 | FAIL | Infrastructure failure without trustworthy child result is INCOMPLETE |
| unknown | 1 | FAIL | Unknown status is not sufficient context to attribute a program failure |
| succeeded | 2 | FAIL | Status and exit-code claims contradict the contract's definition of succeeded |

This table describes the helper's deterministic output for supplied values. It does not prove that any such combination is produced by a real runner.

### 3.3 Existing tests miss these combinations

- `test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete` supplies `exit_code=None`.
- `test_nonterminal_states_are_incomplete` supplies exit code `0`.
- `test_nonzero_exit_overrides_script_printed_pass` supplies only `classify_verdict("succeeded", 2)`. It does not provide stdout containing the text `PASS`, and the helper does not accept stdout as an input to verdict classification. It tests contradictory status/exit metadata, not script-output precedence.
- `test_program_reported_failed_check_remains_visible_on_process_pass` appropriately demonstrates that a program-reported failed check can remain visible while the process verdict is PASS, consistent with CASE-09's distinction between process success and task correctness.

Tests were inspected statically only. None was executed in this pass.

### 3.4 Formatter behavior and provenance boundary

`format_report()`:
- Sanitizes status to its known status vocabulary, replacing unrecognized values with `unknown`.
- Validates exit code as an integer excluding bool.
- Calls `classify_verdict(status, exit_code)`.
- Renders `Evidence source`, run ID, runtime, stdout/stderr, checks, files and notes from the supplied mapping.
- Does not authenticate any of those values. Its docstring explicitly says it does not verify trustworthiness.

The displayed `Evidence source` is plain caller-provided text, not proof of producer identity. Similarly, a valid-looking run ID, runtime label or exit code is not itself proof that the value came from the runner.

This is not a reason to add authentication to the formatter. The helper's current separation is deliberate. The production integration must ensure that the formatter receives a coordinator-validated envelope, never a raw request body or script-produced JSON.

## 4. Existing envelope contract already describes the missing trust boundary

The existing adapter/result-envelope specification contains the correct high-level rules:

- Raw facts are immutable; reconciliation creates a new evidence/report version.
- Only a trusted producer can set authoritative fields.
- Client-supplied task/report JSON and program-produced output cannot set lifecycle status, exit code, policy, cleanup, artifact authority or tenant ownership.
- Each event binds tenant, job, attempt, producer/source class, sequence, payload schema/version and policy revision as applicable.
- Coordinator-owned event identity is separate from provider-supplied source event identity.
- Exact replay requires scoped identity and immutable observation-field equality; changed payload under the same scoped event ID is a conflict.
- The report formatter receives an envelope created/validated by the trusted coordinator.
- A generic pure helper is only a projection and cannot authenticate evidence.

Therefore the architectural idea is already present. The unresolved work is **conformance and integration**, not inventing a second envelope architecture. The actual evidence ingress, authentication, run/attempt binding, durable append, terminal conflict handling and production formatter call path have not been implemented or proven by these documents.

Do not treat a typed Python object or a field named `trusted` as authentication. A dataclass/schema validates shape; trust must arise from the actual ingress boundary, authenticated producer/channel, authorization context and coordinator-owned event acceptance.

## 5. Three facts that must remain separate

1. **Program claims:** stdout, stderr, printed `PASS`, script-generated JSON checks and user-provided assertions. These are untrusted payload data. Display them with provenance, but never use them to set authoritative runner state.
2. **Lifecycle observations:** accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected or infrastructure_failed, with an authenticated producer and exact run/attempt binding.
3. **Process/termination observations:** natural child exit code, wrapper/supervisor exit code, signal/forced-termination result, cancellation request, termination confirmation and cleanup. Do not store these in one generic `exit_code` field unless the selected boundary defines exactly what it means.

A code such as 137 or 143 can describe how a process ended, but the integer alone does not establish whether the user's program failed naturally or was terminated by execution control. The producer, process identity, termination reason and event ordering matter.

## 6. Candidate projection table for review

This is a proposed conservative mapping consistent with the current canonical acceptance and working defaults. It is not an approved schema or policy change.

| Authenticated, attempt-bound evidence | Candidate verdict | Required handling |
|---|---|---|
| Natural child exit observed as 0; lifecycle confirms succeeded; all applicable mandatory gates met | PASS | Preserve exact child exit evidence and the envelope version used |
| Natural child exit observed as nonzero; trusted runner confirms program_failed/natural program termination | FAIL | Preserve child exit, error/streams and producer provenance |
| Trusted timed_out, cancelled or infrastructure_failed; code is absent or is a forced termination/wrapper code | INCOMPLETE | Preserve raw code separately; do not let it override lifecycle cause |
| accepted, queued or running with nonzero code but no authoritative terminal child-exit event | INCOMPLETE | Treat the code as stale, mismatched or unexplained until correlated |
| rejected with an exit code | INCOMPLETE / conflict | Rejection and child execution evidence conflict; preserve both and investigate dispatch boundary |
| succeeded + nonzero child code | INCOMPLETE / contradictory | Preserve both; neither silently overrides the other |
| program_failed + zero exit | FAIL only if trusted program/runtime failure is independently established; otherwise contradictory/INCOMPLETE | Preserve event and process evidence; do not infer |
| Unknown lifecycle + nonzero wrapper/termination code only | INCOMPLETE | No program-failure attribution |
| Unknown lifecycle + independently trusted natural child nonzero exit, correctly bound to attempt | Candidate FAIL | Requires source/termination semantics and owner-approved projection rule |

The crucial distinction is between a **natural child exit observation** and an integer exit/termination code returned by a wrapper or cancellation mechanism. Do not infer the former from the latter.

The current D-01 working default remains: a trusted enforced timeout is `INCOMPLETE / timed_out` under CASE-04, with limit cause recorded separately. D-01..D-04 remain OPEN; do not freeze these candidate rows without owner review. Preserve LOOP-01..14 and CASE-01..16 unchanged.

## 7. Required regression layers

### A. Pure projection tests

Use an explicit matrix crossing all known lifecycle states with:
- no code;
- zero;
- natural child nonzero;
- forced-termination code;
- wrapper nonzero;
- bool/malformed value.

Include `accepted/queued/running/rejected/timed_out/cancelled/infrastructure_failed/unknown + nonzero`, `succeeded + nonzero`, and `program_failed + zero`. Assert both verdict and retained raw evidence/reason. A pure test must label which evidence inputs are assumed trusted; it cannot establish their authenticity.

### B. Evidence-ingress tests

- Client submits `execution_status=program_failed`, `exit_code=1`, forged `evidence_source`, runtime, tenant or run ID. None may directly set trusted runner evidence.
- Script prints `PASS`, `FAIL`, fabricated JSON terminal status or an apparent exit code. The host-observed lifecycle/exit remains unchanged.
- Producer identity is authenticated and authorized for the event kind; wrong role/channel cannot set child-exit, timeout, policy, cleanup or artifact facts.
- Tenant/job/run/attempt/source/policy mismatch is rejected or quarantined before reduction.
- Duplicate identical scoped event is idempotent; same event identity with changed payload/sequence/scope is a conflict.
- Late terminal observations and multiple terminal candidates remain visible; no silent overwrite.

### C. Persistence/coordinator tests

- Accepted evidence is durable before it is used to derive a report.
- Restart/replay retains event identity, ordering, conflict state and derived disposition.
- Report append identity is idempotent; concurrent writers cannot lose observations.
- Late/conflicting evidence creates a new report version; issued history is not rewritten.
- The report projection records the exact run/attempt and evidence version from which it was derived.

### D. Real runtime/device tests

Only after a runtime is selected under the $0/security gates:
- prove child natural exit versus supervisor/worker termination;
- prove timeout/cancel enforcement and process-tree termination;
- prove cleanup and artifact integrity independently;
- test app suspension/reload and unknown-state recovery on supported devices.

A passing pure helper/fake-adapter suite does not prove any of these real boundary properties.

## 8. Review assignments prepared for the owner to forward

### Claude: architecture and semantic review

1. Does the proposed candidate table reconcile the report helper, execution contract, CASE-04, LOOP-04/05 and D-01 without changing canonical acceptance?
2. Which minimal boundary should own the natural-child-exit versus wrapper/termination distinction?
3. What is the smallest safe formatter interface that enforces “validated envelope only” at the production call path without pretending a Python type itself authenticates data?
4. Which deterministic tests should precede any source change? Identify counterexamples to every candidate row.

### Gemini: independent adversarial review

1. Can caller-controlled or script-controlled fields reach the formatter and influence verdict, run identity, evidence source or artifact metadata?
2. Can a forged/mismatched producer, tenant, run, attempt, sequence or late event create false PASS/FAIL?
3. Does any nonzero forced-termination/wrapper code become user program FAIL?
4. Can duplicate/replayed terminal events overwrite an earlier disposition or erase a contradiction?
5. What exact evidence proves producer authority and attempt binding, and what remains impossible to prove with a pure helper?

Do not claim either review has been received until the owner supplies the actual responses.

## 9. Disposition and non-actions

- Source behavior: CONFIRMED by static inspection at the pinned helper blob.
- Precedence/test coverage gap: CONFIRMED at the same pinned helper/test blobs.
- Formatter's explicit untrusted-input contract: CONFIRMED; do not call this alone an implementation defect.
- Existing adapter envelope design: already specifies the intended trusted-coordinator boundary; implementation/integration proof remains NOT RUN.
- Canonical LOOP/CASE IDs and expected meanings: unchanged.
- D-01..D-04 owner decisions: remain OPEN.
- Runtime/provider/ingress/persistence: unselected or NOT RUN.
- No source/test code changed. No tests, provider, account, workload, browser/device, Actions, PR, install, host, queue, merge or deployment operation occurred.
