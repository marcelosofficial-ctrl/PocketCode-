# PocketCode Product Hypothesis Card — 2026-10-28

**Status:** Provisional research instrument; no user study, hands-on competitor benchmark, implementation, or owner-approved scope decision has occurred.  
**Product authority:** [PRODUCT_SPEC.md](../PRODUCT_SPEC.md), [PROJECT_STATUS.md](../PROJECT_STATUS.md), [ROADMAP.md](../ROADMAP.md), and [execution-loop acceptance](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md).  
**Evidence inputs:** [main mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md), [PR #3 user/problem evidence](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_USER_PROBLEM_EVIDENCE.md), [PR #3 competitor research](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_COMPETITOR_RESEARCH.md), and [phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md).

## 1. Candidate user and moment

**Candidate segment:** Someone who primarily has a phone available and receives a small, concrete script or code fragment from an AI assistant, but does not want to install/configure a full IDE or connect to a personal computer just to run one bounded task.

**Triggering moment:** They have code plus a small input file (for example synthetic CSV or JSON), but their current AI app cannot execute the code in the way the task needs. They need the real result, not a plausible assistant-generated answer.

This candidate is intentionally narrower than “everyone who codes on a phone.” It is not yet selected as the final audience.

## 2. Job to be done

“When I have a small code task and only my phone is practical, help me run it with clear limits, inspect the real outcome and output files, and carry trustworthy evidence back to my AI assistant so I can fix and rerun it—without configuring a full development environment.”

## 3. Core promise to test

The **execution location is an open variable**, not a foregone conclusion: compare a local iOS Python app, browser-local Pyodide/WASM, a remote PC, and hosted execution. The first working solution may be local-first for a bounded set of tasks; only choose hosted execution if the actual task needs capabilities that a safe local path cannot provide and the hosted path has a demonstrable advantage and an approved cost/security gate.

One supported task flow:

1. Paste a short script and explicitly select synthetic/small input files.
2. See the exact runtime and limitations before starting.
3. Run only in an approved, isolated environment.
4. See truthful terminal/job disposition, stdout/stderr, exit evidence, truncation and output files; distinguish program failure from timeout, cancellation, infrastructure failure, and unconfirmed cleanup.
5. Copy a bounded report that helps an AI diagnose the next step, without silently including source or secrets.
6. Apply a correction and rerun.

This is an acceptance hypothesis, not a statement that any runner or backend already exists. Until an approved and tested execution path exists, any prototype result remains **SIMULATED**.

## 4. Alternatives the hypothesis must beat

| Alternative | Why it may win | What PocketCode must prove to justify itself |
|---|---|---|
| Local iOS Python app such as [Pyodios](https://pyodios.caffeinatedmath.com/) | Runs some Python tasks on-device with no server, account or hosted-run cost; public docs claim WebAssembly execution on iOS 26+ | A reusable report/AI correction loop or task/package capability not already met by local execution; do not assume this gap without testing |
| Browser-local Pyodide/WASM | Could support a narrow local-first PWA task without a server | Actual target-browser package/file behavior, responsiveness, interruption handling and permission boundary; WASM is not proof of hard isolation |
| Existing local phone IDE/runtime | No hosted execution bill; often keeps files on-device; can be fast | Less setup friction for the specific task, without overstating privacy/security |
| Termux / local Linux environment | Flexible and powerful for Android users willing to configure it | Meaningfully easier for the candidate novice/occasional user |
| Remote PC / SSH / remote-agent client | Reuses a user's existing environment and codebase | Works in the important case where a PC/host is unavailable, or reduces setup enough to matter |
| Browser cloud IDE / hosted workspace | Already provides remote execution and rich tooling | Clearly simpler for one task, with better report handoff; account, cost, storage and mobile friction must be measured |
| Direct copy/paste from terminal or AI output | Free and minimal; may be entirely sufficient | Report changes must materially improve the next debugging turn over copying the raw error |
| No action / postpone until a computer is available | Avoids setup, privacy concerns and trust in a new service | The task's need and frequency are strong enough that waiting is genuinely costly |

## 5. Evidence and uncertainty

| Claim | Current status | What would change it |
|---|---|---|
| Some people want to run/debug small code tasks from phones | Plausible, supported by qualitative anecdotes | Repeated recent examples from a clearly defined user group and observed task completion |
| A hosted disposable run is easier than existing local/remote alternatives | **UNVERIFIED** | Same-task comparison with setup steps, failure points and user preference |
| A copyable evidence-rich report improves AI correction | **UNVERIFIED** | Paired tasks comparing raw error vs structured report, preserving full outputs and conditions |
| A sustainable $0 or explicitly approved-cost path exists for any execution path | **UNVERIFIED / NEEDS LIVE TEST** for hosted execution; local execution is documented but untested here | Compare actual local task/package fit first; hosted cost ceiling, isolation, egress, termination and cleanup still need separate evidence |
| AI Workflow Director saves time/tokens or improves correctness | **UNVERIFIED** | Complete, comparable paired outputs and measured inputs/outputs; one pair is exploratory only |
| The project name is distinct enough for launch | **HIGH RISK / UNRESOLVED** | Separate naming options and an appropriate formal brand/trademark/domain review |

Current support is not representative. No interviews, installs, real task comparison, provider execution, or AI efficiency benchmark are claimed.

## 6. Falsification criteria

The hypothesis should be narrowed, pivoted, or stopped if any of these are supported by the best available evidence:

- Most target users complete the task more easily with a free local IDE, Termux, existing cloud IDE, or a host they already control.
- The true pain is writing/editing on a small screen or learning support, not execution and evidence handoff.
- People cannot or will not transfer their code/input to the environment the product requires.
- The copyable report does not improve the next correction relative to raw stderr or a normal chat prompt.
- The task is too infrequent to justify a separate product, or the workflow adds more steps than it removes.
- Required isolation, egress restrictions, termination, cleanup, artifact authorization, or a reliable cost boundary cannot be demonstrated.

Do not interpret a positive desk-research result, one anecdote, one AI pair, or a simulated UI as product-market fit or proof of security.

## 7. Proposed low-cost research protocol

**Protocol proposal, not an approved owner decision:** when feasible, recruit people based on a recent real incident rather than general enthusiasm. Ask what happened the last time they tried to run code from a phone, what tool they used, and what they did next. Avoid leading them toward PocketCode.

Run one fixed, privacy-safe task across their current preferred method and a proposed narrow flow. The task can be a short Python script reading a synthetic CSV and writing a summary file, with one deliberate failure case. Measure:

- task completion, setup steps, app switches, time-to-first-result, and need for outside help;
- correctness against a known expected output;
- whether error/output/result artifacts are available and truthful;
- whether the report enables a useful next correction;
- user preference and reasons for choosing an existing alternative;
- privacy, account, platform, cost, and trust objections.

The PR #3 research proposed a starting exploratory threshold of 4/6 participants independently describing a recent repeatable problem and 3/6 completing a common task with materially fewer steps or a more useful report. These small thresholds are **not statistically representative** and should be reviewed before use; do not claim they are validated standards.

No interviews are required to keep the project moving during the phone-only period. Public desk research and careful source review can reduce uncertainty, but cannot substitute for a hands-on user/task comparison.

## 8. Current recommendation

**Continue discovery, narrow the task candidate, and do not select an execution provider or begin backend implementation.** The next useful proof is evidence that one specific phone-only job is materially better with the proposed run/inspect/report loop than the strongest available workaround. Include local device/browser execution as a first-class option; hosted execution must earn its place rather than being assumed. If the comparative advantage is absent, pivot toward a more clearly differentiated report/continuity utility—or stop the hosted-runner direction rather than adding features to compensate.

This recommendation remains provisional and does not authorize implementation, spending, provider/account setup, live execution, merge, or deployment.
