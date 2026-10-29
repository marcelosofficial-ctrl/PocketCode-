# PocketCode Output-State and Verdict/Release Boundary Recheck — 2026-10-29

**Status:** Read-only semantic crosswalk and continuity note. SPECIFIED ONLY / NOT RUN.
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`
**Canonical authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and applicable CASE criteria.
**Scope:** Continue after the timeout-precedence audit with a bounded check of output/collection vocabulary and execution-verdict versus artifact-release separation. No implementation, tests, canonical acceptance, provider, runtime, store, PR, merge, or deployment changes.

## 1. Exact current evidence re-fetched

| Path | Blob SHA | Use |
|---|---|---|
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | Canonical LOOP/CASE criteria |
| `PRODUCT/EXECUTION_CONTRACT.md` | `128a00a9b2a335514814cab76fb5781fe8f9f858` | Output and verdict/release contract |
| `scripts/report_contract.py` | `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` | Current pure report helper |
| `scripts/test_report_contract.py` | `85109f056009d65a274e9306deb39b68e1fefbd2` | Existing unit-test source |
| `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` | `e67b2659cf2d71ef77d8e4619c91143e71062470` | D-03 working default and unresolved owner decision |
| `AI_COLLAB/EXECUTION_VERDICT_ARTIFACT_RELEASE_RECONCILIATION_20261029.md` | `8f0d592995a625f9bf47ac15848c92008e15f855` | Existing verdict/release boundary analysis |
| `AI_COLLAB/CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md` | `428897fb54e02c0dc27e987efa7a9690706c9732` | Cross-boundary invariant and open questions |
| `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` | `083123e764a35f761d6d8a779272b07b5a0c8d45` | Runtime/collector provenance is boundary-dependent |
| `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` | `8d665bd5b650fe00dd8133a729b13cca7cb523eb` | Projection separation and report-history requirements |

All were fetched from the named research branch during this pass. Branch-search confirmed the branch exists but did not return a current HEAD SHA. No tests were run.

## 2. Output-state vocabulary crosswalk

D-03 in the owner register says these states must remain distinct: `COMPLETE`, `PARTIAL`, `UNAVAILABLE`, `EMPTY`, `RUNTIME_LIMIT`, and `DISPLAY_TRUNCATED`. The canonical contract also requires bounded stdout/stderr and explicit truncation markers, while CASE-07 requires configured output limits to be enforced and truncation/rejection disclosed.

| State/fact | Current helper representation | Semantic assessment | Evidence |
|---|---|---|---|
| Stream missing/unavailable | `stdout/stderr is None` renders `unavailable` | Distinguishes absent capture from empty capture, but does not encode why unavailable | Static source |
| Stream captured and empty | Empty string renders `(empty)` | Correctly distinct from unavailable | Existing test source covers it; NOT RUN |
| Captured text exceeds display field limit | `_safe_text` adds `[field truncated]` | Display/formatter truncation is signalled, but not as a typed state | Static source |
| Source/collector says output was truncated | Caller boolean `stdout_truncated` / `stderr_truncated` adds `[output truncated by source]` | Source-reported truncation is visible, but collector cap versus runtime limit is not distinguished | Static source |
| Runtime enforced a deadline/resource limit | Lifecycle status may be `timed_out`; no separate typed stream state in this helper | Runtime limit and output collection state are separate concepts; do not infer one from the other | Contract + D-01/D-03 |
| Partial output captured before failure/disconnect | May appear as a string plus status/notes; no explicit COMPLETE/PARTIAL collection enum | Caller must preserve the partialness/provenance; current formatter cannot independently prove completeness | Static source |
| No output expected for the task | `none reported` / empty output file list | Must not be treated as failure universally | Canonical LOOP-10, D-03 |

### Bounded conclusion

The helper currently distinguishes `None` from empty string and distinguishes source-reported truncation from its own field-level truncation in the text output. It does **not** represent the full D-03 state vocabulary as structured, typed evidence. This is a representation/contract gap to consider at the eventual adapter boundary, not proof of a canonical violation by this formatter alone: the helper's documented role is to format caller-supplied evidence, and the provider/runtime is not selected.

Do not add fields or freeze an enum in this pass. First identify the authorized execution boundary and determine which completeness facts it can authoritatively report. If there is no trusted evidence, use UNKNOWN/UNAVAILABLE rather than guessing.

## 3. Verdict and artifact-release separation

The canonical execution contract explicitly says:
- PASS is an execution verdict based on trusted terminal success, exit code zero, and evidence required by the particular acceptance case.
- An artifact-free task may PASS; an empty output-file list is not a universal failure.
- If files exist, report observed metadata and uncertainty honestly.
- Download/release is a separate current authorization decision that checks run/attempt association, trusted manifest, quarantine/lifecycle state, safe object identity, size/type/path policy, and exact immutable bytes.
- Release denial, missing artifact, quarantine, or stale authorization must not rewrite the historical execution verdict.
- A specific case may require its named artifact, but that is a case-specific gate, not a universal artifact-presence gate.

The current pure helper matches the boundary in a limited way: `classify_verdict` does not inspect output files; `format_report` only renders supplied output-file metadata. It contains no release authorization or download enforcement. That is appropriate separation for a pure formatter but provides **no evidence** that any future API/store enforces the release gate.

The cross-decision audit further requires separate projections for raw execution outcome, job disposition, user-facing verdict, cleanup state, collection completeness, and artifact-release status. Later cleanup/release observations must not mutate a historical report version; new evidence should create a new version under the proposed report-history rules. Those persistence rules remain SPECIFIED ONLY / NOT RUN.

## 4. Relevant open boundary questions, without broadening scope

The adapter-boundary decision gate says the evidence model depends on whether the selected execution path is an existing on-device app, browser-local Pyodide, or a future server/provider adapter. These have not been proven equivalent. Before finalizing output-state mapping, identify:
1. Which component actually launches the child program.
2. Which component has authoritative child exit and lifecycle evidence.
3. Whether wrapper/termination codes exist separately from child exit.
4. Whether output collection can fail or truncate independently of execution.
5. Whether output completeness is available as a trusted fact or only inferred from stream length.

The earlier timeout-precedence issue remains the immediate verdict regression: current `report_contract.py` checks any nonzero integer before `timed_out`, whereas canonical CASE-04 and D-01 working default require trusted timeout to remain INCOMPLETE / `timed_out`. Its existing test only pairs uncertain states with a missing exit code. No code or tests were changed.

A search for a file named `COORDINATOR_CONTRACT.md`, `COORDINATOR_ACCEPTANCE_CROSSWALK_20261029.md`, and `COORDINATOR_CONTROL_MATRIX_20261029.md` at this exact branch returned 404. This is not evidence that no coordinator criteria exist elsewhere. No specific `COORD-01` text was located in this pass, so no claim is made about its exact wording or status. If COORD-01 is to be crosswalked next, fetch its actual canonical file/path first rather than infer from the label.

## 5. Evidence limits and next bounded task

- Static source and contract review only; tests NOT RUN.
- No runtime/provider/store or device tested; no caller trust boundary established.
- No source, test, canonical acceptance, PR #2, PR #3, or other implementation changed.
- No merge, deployment, account, billing, hosted workload, Actions, queue, or host action.
- RevDev AWC-001–AWC-018, P8U-01–12, P0-D 1–10 remain distinct from PocketCode AEC-001–AEC-012.
- RevDev publisher/orphan/retry/recovery P0 remains release-blocking. PocketCode execution location and integration topology remain undecided and approval-gated.

**Next bounded task:** locate and re-fetch the exact canonical coordinator criteria containing COORD-01, then reconcile only its verdict/release projection against the current output-state vocabulary and CASE-04. Do not modify source or tests unless separately authorized.