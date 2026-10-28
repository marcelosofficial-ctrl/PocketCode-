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

## 5A. Cross-path synthesis sheet (fill only after individual attempts)

This is a **blank synthesis template**, not a ranking. Keep each scenario separate until both success and malformed-input records exist. Copy one row per path; leave unknowns as `U` and explain the evidence. Never turn a source claim into a direct observation.

| Path / exact version | Success scenario | Malformed-input scenario | Real file exported? | Trustworthy status / exit? | Report provenance useful? | Setup friction | Data location / network known? | Cost terms verified? | Disqualifier / strongest counter-evidence |
|---|---|---|---|---|---|---|---|---|---|
| AI chat + manual copy/paste | NOT RUN | NOT RUN | U | U | U | U | U | U | |
| Local iOS Python app (name/version) | NOT RUN | NOT RUN | U | U | U | U | U | U | |
| Browser-local Pyodide/WASM (exact browser/build) | NOT RUN | NOT RUN | U | U | U | U | U | U | |
| Remote PC / agent (exact client + host conditions) | NOT RUN | NOT RUN | U | U | U | U | U | U | |
| Hosted coding environment (exact plan/limits) | NOT RUN | NOT RUN | U | U | U | U | U | U | |
| Other current workaround (name it) | NOT RUN | NOT RUN | U | U | U | U | U | U | |

### Decision record — do not complete before evidence exists

- **Best existing path for this exact task:** NOT DECIDED
- **Evidence class:** NOT RUN
- **Observed user/setup friction and conditions:** NOT RUN
- **Did any path fail the correctness or failure-handling gate?** NOT RUN
- **Did structured report evidence materially improve a separate AI's next correction versus raw error text?** NOT RUN
- **Which result would falsify the PocketCode hypothesis?** Existing path is at least as easy for the target user, creates/verifies the required output and failure behavior, and provides sufficient evidence/handoff without a material unmet need.
- **What remains unknown even if the task passes?** Representative user demand; security/isolation properties; broader package/runtime compatibility; long-run reliability; service economics; legal/name clearance.
- **Recommendation:** CONTINUE DISCOVERY until evidence supports a narrower conclusion. Do not infer a product advantage from a blank template or one successful run.

**Comparison integrity rules:** Do not average success and failure into one score; a success-case pass cannot compensate for a misleading malformed-input result. Do not rank a path when a critical correctness/evidence dimension is `U`. Compare only like-for-like task conditions, note any unavoidable differences, and report unavailable platforms as `NOT RUN` rather than as failures. A one-task result can eliminate a bad fit or justify another test; it cannot prove market demand or security.

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

## 8. Reproducible attempt protocol (added 2026-10-28; still design-only)

This section tightens the task so two paths cannot pass merely by displaying a plausible answer. It does not authorize installs, accounts, uploads, provider runs, or any hands-on test.

### Canonical inputs

Use UTF-8 text with LF line endings and no byte-order mark. Each scenario starts in a **fresh, empty workspace**. Do not reuse an output directory between success and failure.

Success input, exact logical contents of `items.csv`:

```csv
item,quantity,unit_price
notebook,2,3.50
pen,3,1.25
```

Failure input, exact logical contents of `items.csv` (required header removed):

```csv
item,quantity
notebook,2
pen,3
```

Use the standard-library decimal type (or demonstrably equivalent decimal-safe arithmetic); binary floating-point formatting is not an acceptable reason to change the expected decimal strings.

Success output must be a real created file named `summary.json` with these parsed values:

- `grand_total`: string `10.75`
- `line_items`: integer `2`
- `totals_by_item.notebook`: string `7.00`
- `totals_by_item.pen`: string `3.75`

Whitespace/key order may vary, but value types and values must match. No timestamps, random IDs, machine paths, or other nondeterministic fields should be added. Record the actual file bytes or a copy of the complete file content; a chat answer that merely prints the expected JSON is not proof that the file was created or exportable.

Failure case must identify the missing `unit_price` field clearly, return a trustworthy non-success process status if the environment exposes one, and leave **no valid `summary.json`** in the fresh workspace. If the platform cannot expose a process status, record that limitation as `UNAVAILABLE`; do not infer a failure exit code from the displayed error.

### Per-attempt capture sequence

1. Record path/app/version and platform/browser version where visible. If a value is unavailable, write `UNKNOWN`.
2. Start from a fresh workspace; capture the exact input method and every setup/action step. Do not count a step from memory after the attempt.
3. Start a timer immediately before the first required setup action; stop when the real output file is available for inspection/export. Record elapsed time only for a real attempt; distinguish setup time from run time if both can be measured.
4. Run the success case. Capture the actual `summary.json`, any reported status/exit code, stdout/stderr if available, and whether the file can be saved/exported.
5. Reset to a separate fresh workspace and run the malformed-header case. Capture the exact error and status, then inspect whether a misleading `summary.json` exists.
6. Record whether execution was on-device, in browser-local WASM, on a user-controlled remote host, provider-hosted, or unknown. Record whether network access was required or observed; do not infer offline operation from marketing text.
7. Record what survives into a copyable report: exact values, source/provenance, unavailable fields, truncation, file name/size, and any explicit simulated/demo label.
8. Record cleanup, persistence, or deletion only if directly observable and relevant; otherwise use `UNKNOWN`. Do not claim sandboxing, isolation, or data deletion based only on a UI label.
9. Assign `0`, `1`, `2`, or `U` only after the attempt. Attach the observation supporting each non-`U` score.

### Stop / disqualifier rules

- Stop if the path requires payment, a paid trial, billing activation, credential setup, or a provider workload not explicitly approved.
- Do not upload private or real user data; this protocol uses only synthetic inputs.
- Mark correctness `0` if the produced file has wrong values/types, is fabricated rather than created, or cannot be distinguished from a demo.
- Mark failure handling `0` if the malformed input is presented as successful or a valid-looking output is left in the fresh workspace.
- Mark evidence quality `0` if the report asserts execution without traceable observations, or silently substitutes guessed exit/status data.
- Mark security/privacy `U` unless the relevant property is directly established by a suitable test or authoritative evidence; one successful task is not a sandbox/security test.
- If an attempt is interrupted, ambiguous, or missing a required observation, use `INCONCLUSIVE` for that scenario; do not fill gaps with another path's evidence.
- The static PocketCode prototype remains ineligible for execution/correctness scoring because its run result is simulated.

### Minimum attempt record (copy/paste)

```text
Path / app + version:
Date:
Platform / browser:
Scenario: SUCCESS | MALFORMED_HEADER
Evidence class: DIRECTLY OBSERVED | SOURCE REVIEW | BLOCKED | NOT RUN
Workspace fresh: YES | NO | UNKNOWN
Setup steps (ordered):
Setup time:
Run time:
Execution location:
Input method:
Actual output file created: YES | NO | UNKNOWN
Actual output content / file hash (if available):
Reported status:
Exit code (actual or UNAVAILABLE):
stdout / stderr:
Malformed case error:
Valid summary.json present after malformed case: YES | NO | UNKNOWN | NOT APPLICABLE
Output export/save verified:
Report evidence and provenance:
Network required/observed:
Persistence / cleanup observation:
Cost/account prerequisites:
Score + evidence (each dimension):
Disqualifier or uncertainty:
Overall scenario: PASS | FAIL | BLOCKED | INCONCLUSIVE | NOT RUN
```

**Current status remains NOT RUN.** This is a more reproducible protocol, not a benchmark result or permission to start testing.

