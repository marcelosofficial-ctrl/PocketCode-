# PocketCode — Fixed-Task Comparison Worksheet (Design Only)

**Date:** 2026-10-28  
**Status:** Task protocol and expected outputs only. No apps were installed, no scripts were run in a mobile runner, and no benchmark was performed.  
**Purpose:** Convert the product hypothesis into a repeatable comparison that can show when local-on-device, browser/WASM, remote-PC, hosted, or ordinary copy/paste workflows are already sufficient.

**Parent docs:** [Four-month phone-only master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) · [Product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) · [Competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) · [Execution-contract audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md).

## 1. Decision this worksheet should inform

**Question:** For a phone-only user with a small Python + CSV task, which existing path completes the task with the least friction while preserving real output/error evidence, and is there a user-valued gap left for PocketCode?

This is not a benchmark of general-purpose IDEs or AI model quality. It is a fixed, narrow task study. Record alternatives that win; do not frame every competitor limitation as a PocketCode advantage.

## 2. Fixed synthetic task

The script should use only the Python standard library and remain small enough for a phone screen. No internet, credentials, user files, third-party package installation, or real secrets are needed.

### Success input: items.csv

~~~csv
item,quantity,unit_price
notebook,2,3.50
pen,3,1.25
~~~

### Program behavior

Read the explicitly provided CSV, multiply quantity by unit price using decimal-safe arithmetic, group totals by item, and write a deterministic summary.json. Print one short confirmation. No network or other side effect is expected.

### Expected result: summary.json

~~~json
{"grand_total":"10.75","line_items":2,"totals_by_item":{"notebook":"7.00","pen":"3.75"}}
~~~

Equivalent JSON whitespace is acceptable; key values, decimal strings, line-item count, and per-item totals must match. File names and returned file content are part of the comparison, not merely an in-chat answer.

### Deliberate failure input

Use the same CSV with the required unit_price header removed. Expected behavior: the program reports a clear, relevant error and does not produce a misleading valid summary.json. Where the environment exposes a trustworthy process exit status, it should be non-zero; where it does not, record “exit status unavailable” rather than inferring it from text.

## 3. Alternatives to assess

Do not install software, create accounts, upload private files, or start paid trials as part of desk research. A later hands-on session must be explicitly chosen and use only the synthetic input above.

| Path | Why include it | Current evidence / caveat |
|---|---|---|
| Ordinary AI chat + manual copy/paste | Baseline; cheapest and simplest alternative | The model may describe/guess the result rather than actually run code. Verify output rather than treating the explanation as execution. |
| Local iOS Python app, especially [Pyodios](https://pyodios.caffeinatedmath.com/) | Direct phone-only, no-server route for some Python tasks | Current public docs claim local Python through Pyodide/WASM on iOS 26+; package, memory, startup and file/report behavior need checking. No hands-on test performed. |
| [Pyto](https://apps.apple.com/us/app/pyto-ide/id1436650069) or another local Python app | Alternative local interpreter with broader native package claims | Pricing, compatibility, package restrictions, file-flow friction, and current maintenance must be verified; no install or test performed. |
| [Kodo](https://www.kodoeditor.com/) + SSH | iOS editor with remote shell path | Official page says Python is not executed locally in Kodo; remote Python requires a user-owned server. |
| Browser-local Pyodide/WASM | Potential zero-hosted-cost path inside a PWA | Technical alternative, not currently implemented in PocketCode. Need test iPhone browser, file input/output, worker responsiveness, persistence, package availability, and the actual embedding security boundary. |
| [GitHub Codespaces](https://github.com/features/codespaces) or [Replit](https://replit.com/mobile) | Hosted/browser-based tools already allow coding without owning a nearby PC | Require fair evaluation of onboarding, account/session requirements, current limits/cost, and mobile friction; don't assume current plan terms. |
| Remote PC/agent client, such as [Pairlet](https://github.com/heypandax/pairlet) or [Codeg](https://docs.codeg.app/) | Existing remote-host route | The remote computer/server must be available; less relevant when the user truly has no reachable host. |
| PocketCode static prototype | UX-shell reference only | Its current run result is simulated; it cannot be scored as executing this task. |

## 4. What to record per attempt

Use one record per path and scenario (success and failure). Separate official/documented claims from direct observation.

| Field | Values / recording rule |
|---|---|
| Path + app/version + source date | Exact app/version or web URL; record unavailable values as unknown |
| Platform/requirements | iOS/Android/browser version, account or PC requirement; no assumptions |
| Evidence class | DOCUMENTED CLAIM / DIRECTLY OBSERVED / SOURCE REVIEW / NOT RUN / BLOCKED |
| Setup steps | Count explicit user actions from a fresh start; preserve the step list |
| Time-to-first-result | Stopwatch only for a real attempt; do not infer from documentation |
| Execution location | On-device native runtime / browser WASM / user's PC / provider-hosted / unknown |
| Input flow | How the synthetic CSV was selected/pasted; record friction and limits |
| Correctness | Compare output file values against the expected output above |
| Output retrieval | Is the created file real and exportable, or is only displayed text available? |
| Failure behavior | Clear error, non-success exit if exposed, no misleading valid output file |
| Evidence quality | Real exit/status, runtime info, stdout/stderr, output manifest, truncation/missing fields, cleanup only if applicable and observable |
| AI handoff | Copyable report; what facts and unavailable values survive; whether a new AI turn can act on it |
| Privacy/network | Where code/data reside, network behavior required by the path, retention claims and unknowns |
| Limits/cost | Current documented cap/cost, hard vs soft cap, account/billing prerequisites; don't enter a payment method |
| Recovery | What happens after app/browser interruption or a failed run |
| Friction / user preference | Observed trouble points, need for help, whether the path would be chosen again and why |
| Disqualifiers | Any security/correctness failure that makes this path unsuitable for the task |

Do not fill “unknown” as zero, “free”, “private”, or “PASS”.

## 5. Scoring method (provisional)

After both success and failure scenarios are recorded, rate only observed dimensions:

- **0 — does not meet the criterion**
- **1 — partially meets it or requires a workaround**
- **2 — meets it for this task**
- **U — not observed / insufficient evidence**

Score each path on: setup/friction, correctness, truthful status/error, input/output file flow, useful AI handoff, privacy control, cost predictability, and task-appropriate constraints. Keep U visible; do not compute a total score when a critical dimension is U. Add short evidence for every non-U score.

Safety/correctness disqualifiers override a high convenience score. A simulated result can inform layout but scores U for real execution and evidence.

## 6. Decision rules to consider before any hands-on comparison

These are proposed rules to avoid deciding after seeing whichever result we prefer; they are not accepted product decisions.

- **Prefer a local path** when it runs the required task correctly, handles the needed files, gives sufficient real evidence, and avoids meaningful setup/report friction. A hosted backend has no automatic priority.
- **Consider browser/WASM** only for a bounded task/package subset that is shown to work on the target browser. Do not claim native OS isolation, unrestricted Python compatibility, or hard resource enforcement merely because code runs in WASM.
- **Consider remote-PC** only for a target segment that normally has a reachable host; don't make it the answer to the no-PC use case.
- **Consider hosted execution** only if local/browser paths fail a real target requirement and the hosted path adds demonstrable value. Isolation, exact policy-before-execution, limits, termination, cleanup, artifact authorization, and a credible approved cost boundary remain hard gates.
- **Narrow or stop** if existing alternatives complete the task equally well and the copyable report doesn't improve the next correction. Do not add multi-agent, account, sync, and IDE features to compensate for a missing advantage.

A single phone attempt or paired AI prompt is exploratory, not representative market evidence.

## 7. Current status and next use

- Task and expected success/failure outcomes specified: **DESIGN COMPLETE**.
- Existing alternatives reviewed via public sources: **PARTIAL**.
- Hands-on comparison, install, browser execution, and timing: **NOT RUN**.
- User interviews and market validation: **NOT RUN**.
- No implementation, provider workload, account creation, paid service, merge, deployment, or Actions run is authorized.

Next, use this worksheet to challenge the product hypothesis and decide what evidence would change the recommendation. If a hands-on test is later chosen, make one specific owner request and capture the full evidence record rather than running all alternatives indiscriminately.
