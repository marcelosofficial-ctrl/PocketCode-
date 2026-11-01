# PocketCode Product Path Comparison — Source Review and Experiment Refinement

**Date:** 2026-11-01  
**Status:** Source-backed desk review only. No competitor app was installed, no account created, no task run, no interview conducted, and no product implementation or provider workload performed.  
**Purpose:** Refresh the fixed-task comparison using current primary-source descriptions and identify the smallest experiment that could falsify the remaining product hypothesis.  
**Authority:** This is a research addendum. It does not amend PRODUCT_SPEC, canonical LOOP/CASE acceptance, the product hypothesis card, implementation scope, or owner decisions.

## 1. Executive verdict

The current product hypothesis is still not validated. The landscape is materially stronger than a simple “run AI-generated code on a phone” framing:

- **iOS local Python:** Pyodios is a serious direct comparator for small Python tasks, including the standard-library CSV task in the fixed-task worksheet.
- **Android local coding agents:** AndroidHarness and PhoneCode both describe substantial on-device coding workflows. PhoneCode is particularly notable because its own documentation treats its Android runtime boundary and Play release gates as first-class engineering concerns.
- **Android power-user workstation:** Atlan offers a phone-first Termux/proot cockpit, while openly documenting that its phone-side proot Bash is not an OS sandbox.
- **Remote-host clients:** Codeg and Pairlet provide capable mobile control surfaces, but the actual agent/workspace remains on a reachable computer or server.
- **Browser-local Python:** Pyodide can use browser-managed virtual/persistent filesystems, but its direct native-directory mounting route is Chromium-only. Safari on iOS has OPFS, which is not the user's ordinary Files directory.

**Decision recommendation:** Do not select a hosted provider or build a general-purpose runner. Continue testing the narrowest remaining claim: whether a small, portable, execution-location-neutral receipt improves cross-assistant diagnosis or continuation enough to matter beyond each competitor's native logs and ordinary copy/paste.

The comparison worksheet's fixed CSV task remains useful for correctness and file flow, but it is not sufficient by itself to prove the proposed report differentiator. Add a paired report-handoff experiment after the execution task has real evidence.

## 2. Current-source comparison matrix

All product capabilities below are vendor/maintainer documentation claims, not independently tested PocketCode results.

| Path | Current documented capability | Material limitation or dependency | Fit for fixed CSV task | Research verdict |
|---|---|---|---|---|
| Pyodios on iOS | Local CPython 3.14.2 through Pyodide/WebAssembly; iOS/iPadOS 26+; files/editor/console; bundled scientific packages | Approximately 300 MB Python memory budget; startup can take 5–15 seconds; fresh Python session each app launch; a 120-second UI timeout does not stop the running Python code, and the session must be restarted to recover | Strong candidate: standard-library CSV and decimal arithmetic do not need a compiled third-party package. Actual import/export, malformed-input behavior, exit evidence and timeout recovery remain NOT RUN | Highest-priority iOS local comparator |
| Browser-local Pyodide/WASM on iOS | Python can run locally in a browser; MEMFS, IDBFS and browser-managed persistence are documented | MEMFS is lost on reload; IDBFS persistence must be configured; Pyodide's experimental direct native-directory mount uses File System Access API and is documented as Chromium-only; Safari OPFS is origin-private, not a direct mount of the user's Files directory | Plausible for the task with explicit file-picker input and downloadable output; iOS Safari flow must be proven on-device | Keep as a separate browser path, not equivalent to native app |
| AndroidHarness | Native Android coding agent; local shell, files, Git, tests, browser control and inspectable tool activity; optional local GGUF models or configured provider | Android 8+; shell route may involve Shizuku, Wireless ADB, optional root, Termux or fallback; Android 11+ all-files access is documented in setup; configured prompts/context/command output can be sent to chosen AI provider | Likely capable, but task flow, user friction, permissions and export evidence not independently observed | Strong Android competitor and permission/privacy counterexample |
| PhoneCode | Native Android agent; local project workspaces, Git, Alpine/PRoot development prototype; planned Play architecture uses QEMU software VM and isolated process | Maintainer explicitly labels PRoot runtime debug-only; Play release remains gated on QEMU, guest/runtime integration, lifecycle, sync, networking and licensing audits. A paid ChatGPT plan is needed for its Codex sign-in route; other provider choices exist | Likely capable on development prototype, but do not treat planned Play runtime as released capability. Its own release gate is relevant evidence | Strong Android local-first comparator; maturity must be version-pinned |
| Atlan | Phone-first Android cockpit using Termux/proot, editor, terminal, agents, checks and session continuity; cloud-client mode also exists | Android setup is power-user oriented. Its security document says phone-side proot Bash is not OS-sandboxed; its reported T2 confinement measurement is device-specific and not T3. iOS is client-only/cloud-client in its README | Can likely run small scripts where configured, but requires more setup and an AI engine; not an iOS local runtime | Power-user alternative, not novice baseline |
| Kodo | iOS/iPadOS editor, offline HTML/CSS/JS preview, optional on-device AI, SSH/SFTP/FTP and Git | Official FAQ says it does not execute Python locally; Python runs on user's computer/server over SSH | Not a direct local-Python substitute; useful editor/remote-host alternative | Relevant for editing and remote-host comparison |
| Codeg mobile | Native iOS/Android clients; streams agent output, tool calls and approvals | Official docs say mobile apps are clients, not standalone agent runtimes; files, agent CLIs and sessions remain on a Codeg desktop/server. iOS/Android apps described as test releases in the fetched documentation | Depends on reachable host/server | Strong remote-control alternative, not phone-only execution |
| Pairlet | Phone/tablet clients steer coding agents on user's computer; relay can be self-hosted | Computer and daemon must remain running/reachable; Pairlet FAQ says custom secure channel has not had an independent security audit | Depends on reachable host | Remote-PC alternative only |
| GitHub Codespaces | Browser/cloud development; personal Free accounts have 120 core-hours and 15 GB-month included | Compute and storage are separately metered; use beyond quota can be billed; without a payment method, billable use is blocked after quota. This is not unlimited free execution | Can run task in hosted environment if user accepts account, setup and quota constraints | Existing hosted fallback, not $0-guaranteed |
| Ordinary AI chat + manual copy/paste | No new runtime/account/provider needed; can generate code and reason about copied output | Cannot be scored as execution unless a real tool is used; generated expected JSON is not proof of file creation | Baseline only; if existing terminal output can be pasted, may be sufficient | Must remain in comparison |
| PocketCode static prototype | UX flow and report concept can be discussed | Current execution is simulated | Cannot be scored for execution, correctness, exit evidence or artifact creation | UI-only reference; score execution dimensions U |

## 3. Source-backed findings that change the comparison

### 3.1 Pyodios is a strong local comparator, but timeout semantics are a real failure-handling weakness

Its current FAQ states Python 3.14.2 / Pyodide 314.0.5, iOS/iPadOS 26+, 5–15 second initialization, approximately 300 MB Python memory availability, fresh sessions on launch, and a 120-second run timeout. Critically, the FAQ says code continues running after the UI reports timeout, subsequent runs wait behind it, and recovery requires restarting the Python session or reopening the app.

This creates a direct testable distinction:

- UI timeout is not process termination.
- A subsequent queued run is not evidence that the previous run stopped.
- Session restart is a recovery action that loses variables/imported packages but preserves files.

Do not translate these app-specific semantics into a generic claim about all Pyodide runtimes. The standard-library CSV task should avoid optional packages, so it isolates file handling, output correctness and failure honesty rather than package-install behavior.

Official source: https://pyodios.caffeinatedmath.com/faq

### 3.2 Safari browser-local files are possible, but direct filesystem access is not the same as Chrome

WebKit documents Origin Private File System (OPFS) support in Safari from iOS 15.2. OPFS is storage owned by the website origin; it is not necessarily a visible directory in the user's Files app. Pyodide documents MEMFS as in-memory and lost on page reload, IDBFS as a persistence option, and its experimental `mountNativeFS()` path as using the File System Access API supported only in Chromium browsers.

Therefore a realistic iPhone browser prototype would need explicit import/export (or a carefully designed origin-private workspace) and must test persistence/reload behavior. Do not promise a mounted Files directory on iOS Safari.

Official sources:
- https://webkit.org/blog/12257/the-file-system-access-api-with-origin-private-file-system/
- https://pyodide.org/en/stable/usage/file-system.html

### 3.3 iOS background execution needs a native/web distinction

Apple documents that ordinary apps are generally suspended in the background, while only defined background execution modes and specific task APIs allow qualifying work to continue. Apple now documents continuous background processing tasks for certain user-initiated work on iOS/iPadOS, but this does not grant arbitrary persistent shell/server execution and does not automatically apply to a Safari page or PWA.

Keep separate acceptance questions for:
- foreground browser execution;
- app/page backgrounding and suspension;
- native app use of an eligible background task API;
- interruption, termination, recovery and truthful final status.

Official sources:
- https://developer.apple.com/documentation/xcode/configuring-background-execution-modes
- https://developer.apple.com/documentation/BackgroundTasks/performing-long-running-tasks-on-ios-and-ipados

### 3.4 Android alternatives prove that “local agent + visible tool activity” is not a differentiator

AndroidHarness documents shell/file/Git/browser/tool activity and optional local models or configured providers. Its privacy policy says prompts and relevant context, including file contents and command output, are sent to the AI provider selected by the user. It also documents broad storage permissions and multiple shell backends. This is useful counter-evidence: local execution does not mean model prompts or outputs never leave the device.

PhoneCode documents a different approach: its PRoot/Alpine environment is a debug prototype; its planned Google Play path is a software-emulated QEMU system VM in an isolated Android process. Its own documentation keeps Play release blocked pending runtime integration and lifecycle/release gates. Treat the QEMU path as a design and partial engineering foundation, not as a released, fully validated end-user capability.

Atlan is candid that its Android proot Bash environment is not an OS sandbox. Its reported confinement tier is specific to a measured device and does not establish T3 or general Android isolation. It is not an iOS local-runtime solution.

Primary sources:
- https://github.com/Sanuu7/AndroidHarness
- https://github.com/Sanuu7/AndroidHarness/blob/main/PRIVACY.md
- https://github.com/dttdrv/phonecode
- https://github.com/dttdrv/phonecode/blob/main/MOBILE_BACKEND.md
- https://github.com/Atlansdaddy/atlan
- https://github.com/Atlansdaddy/atlan/blob/main/docs/SECURITY.md

### 3.5 Remote clients and cloud IDEs already cover adjacent jobs

Codeg's current docs describe mobile clients that connect to a user-controlled desktop/server; the agents and projects remain on that host. Pairlet likewise requires the computer and daemon to stay running and reachable. These are not PC-free solutions, but they are credible substitutes when the user has a host.

GitHub Codespaces has a defined included personal-account quota (currently 120 core-hours and 15 GB-month on Free); compute and storage are separately measured. Usage beyond included quotas can be billed, while a user without a payment method is blocked after exhausting the quota. Never describe it as unlimited free.

Primary sources:
- https://docs.codeg.app/getting-started/installation
- https://pairlet.org/guides/faq.html
- https://docs.github.com/en/billing/concepts/product-billing/github-codespaces

## 4. Revised comparison priority

Use the same CSV task, but do not spend effort testing every product in one pass.

1. **iOS local path:** Pyodios, if an owner-approved install/test is later chosen. This is the strongest direct iOS local-Python candidate.
2. **iOS browser path:** Pyodide in Safari, only if the product genuinely needs a browser/PWA route; test file import/export and reload persistence, not merely Python arithmetic.
3. **Android local path:** select one current, installable candidate (AndroidHarness or PhoneCode) only if Android access is available and the exact release/runtime gate is understood. Do not compare PhoneCode's debug PRoot prototype as though it were its intended Play release.
4. **Remote-host path:** Codeg or Pairlet only if a reachable host is available. They should not be counted as PC-free.
5. **Hosted path:** defer until a concrete requirement cannot be met locally and a genuinely zero-cost, owner-approved test path exists.
6. **Baseline:** manual copy/paste remains the control condition.

No app should be installed or tested without a separate deliberate owner choice. No paid trial, payment method, account creation, or hosted workload is permitted under the current $0 gate.

## 5. The missing experiment: does a portable run receipt improve the next AI correction?

The existing worksheet tests execution correctness and mentions structured-report benefit, but its blank synthesis sheet does not yet define a fair paired report-handoff protocol. This is the remaining product claim worth isolating.

### Experimental question

Given exactly the same source, input, observed run facts and raw stdout/stderr, does a compact portable receipt help a second AI assistant diagnose and correct the task more accurately or with less user effort than ordinary raw-error copy/paste?

### Conditions

- **A — Raw evidence:** Give a fresh AI chat the same task source and the unmodified observed stdout/stderr/status/artifact facts available from the run. Do not add a diagnosis.
- **B — Portable receipt:** Give a different fresh chat the same source and exactly the same observed facts, represented in a proposed compact receipt. Preserve provenance and explicitly mark unavailable facts. Do not add a diagnosis or hidden clue.
- Keep assistant, model, mode, plan, task, source, input and tool availability the same. If not, mark the pair confounded.
- Do not show either chat the other's answer. Save both complete outputs before scoring.

### Scoring

Score each condition separately for:
1. Correct root cause / next correction.
2. Preservation of observed facts and provenance.
3. No invented runtime, exit, artifact or cleanup claims.
4. Minimality and scope discipline.
5. Whether the proposed correction passes the same success and malformed-input acceptance criteria when independently verified.
6. User effort: copy/paste steps, turns and any manual explanation needed.

Record prompt/output characters and turns only as proxies, not tokens, latency or money. Keep correctness and evidence honesty as hard gates; a shorter but wrong response loses.

### Controls and anti-bias rules

- The receipt may reorganize evidence but may not add facts absent from the raw evidence.
- Both conditions must contain the same source/input context and all material diagnostics.
- A receipt that silently drops a relevant error, hides truncation or upgrades an unknown to a fact fails.
- A receipt that contains extra diagnosis, likely root cause or suggested fix is not a fair representation-only comparison.
- Use one deliberate, deterministic failure case and one success case. The malformed CSV header is suitable for testing honest failure handling, but may be too trivial to show a meaningful report advantage. If the initial pair is ceiling-limited, add one separately specified failure fixture rather than changing it after seeing results.
- Repeat at least three comparable pairs per condition if free usage permits. If not, report the sample count and treat the result as exploratory.
- Do not use a simulated PocketCode result as a real execution receipt. Until a real path is approved and exercised, a synthetic receipt may test only the report's information design, not end-to-end product value.

### What would falsify the receipt hypothesis?

If raw evidence leads to the same correct fix with equal or fewer turns/user steps, and the portable receipt does not improve provenance, truthful status or cross-assistant portability, do not build a standalone report layer as a product differentiator. Consider a small export/interoperability format only if a concrete user workflow requires it; otherwise stop or pivot.

## 6. Current architecture recommendation

**No execution provider and no runtime architecture should be selected yet.**

Keep these product concerns separable:
- **Task-packet / continuation utility:** local-only, explicit copy/paste, no provider calls.
- **Execution adapter:** a separate interface over local iOS, browser WASM, Android local runtime, remote PC, or hosted execution.
- **Run evidence / receipt:** provider-neutral representation of observed facts and unknowns, not an execution engine and not an authorization token.
- **Provider/host policy:** only relevant to a specific remote execution path and independently gated.

This is a research boundary, not an accepted architecture decision or implementation authorization. Do not assume a shared RevDev/PocketCode runtime or merge their repositories.

## 7. Open questions and explicit NOT RUN status

- Pyodios task/file/failure/timeout behavior on an actual iPhone: NOT RUN.
- Browser Pyodide on iOS Safari, including import/export and reload persistence: NOT RUN.
- AndroidHarness and PhoneCode task flow, permission friction and evidence export: NOT RUN.
- Atlan on a target Android device: NOT RUN.
- Codeg/Pairlet mobile-host flow: NOT RUN.
- Codespaces task flow and mobile friction: NOT RUN.
- Raw-evidence versus portable-receipt paired correction experiment: NOT RUN.
- Interviews and representative demand: NOT RUN.
- Product-market fit, security, and execution reliability: NOT ESTABLISHED.

## 8. Sources and verification dates

Official/primary sources consulted 2026-11-01:
- Pyodios FAQ: https://pyodios.caffeinatedmath.com/faq
- Pyodios product page: https://pyodios.caffeinatedmath.com/
- Pyodide filesystem docs: https://pyodide.org/en/stable/usage/file-system.html
- WebKit OPFS: https://webkit.org/blog/12257/the-file-system-access-api-with-origin-private-file-system/
- Apple background execution: https://developer.apple.com/documentation/xcode/configuring-background-execution-modes
- Apple long-running tasks: https://developer.apple.com/documentation/BackgroundTasks/performing-long-running-tasks-on-ios-and-ipados
- AndroidHarness README and privacy policy: https://github.com/Sanuu7/AndroidHarness and https://github.com/Sanuu7/AndroidHarness/blob/main/PRIVACY.md
- PhoneCode README and mobile backend: https://github.com/dttdrv/phonecode and https://github.com/dttdrv/phonecode/blob/main/MOBILE_BACKEND.md
- Atlan README and security posture: https://github.com/Atlansdaddy/atlan and https://github.com/Atlansdaddy/atlan/blob/main/docs/SECURITY.md
- Kodo: https://www.kodoeditor.com/
- Codeg mobile install requirements: https://docs.codeg.app/getting-started/installation
- Pairlet FAQ: https://pairlet.org/guides/faq.html
- GitHub Codespaces billing: https://docs.github.com/en/billing/concepts/product-billing/github-codespaces

These are source claims and maintainer descriptions. They are not independent audits or PocketCode test results.


## 9. Contract traceability correction — reuse the existing proposed report

A read-only traceability pass against the research branch found that the proposed portable receipt is **not a new feature/schema to invent**. The repository already defines the intended user-copyable report and its semantics:

- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` lines 36–38: LOOP-07 defines useful diagnostics; LOOP-08 defines one primary Copy result action with a complete, bounded, plain-text report.
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` lines 81–90: stable parseable field labels, observed facts, unavailable values, bounded output, provenance, process-vs-task distinction, user-initiated copy and run identity.
- `PRODUCT/EXECUTION_CONTRACT.md` lines 111–124: proposed report fields and safety rules.
- `PRODUCT/EXECUTION_CONTRACT.md` lines 126–181: proposed plain-text report illustration and required semantics, including evidence source, check provenance, optional unknown exit/duration, explicit truncation, output-file metadata, and format versioning.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` lines 20–32 and 39–76: proposed raw-fact immutability, attempt identity, provenance, unknowns, trusted producer authority, report-as-projection, and distinct output-collection states.

**Important status:** the report format and envelope are still proposals, not frozen public schemas or implemented behavior. The synthetic report in the contract is explicitly illustrative and is not evidence of a real run.

### Corrected paired experiment

Use the existing proposed canonical report as condition B. Do not design a competing "receipt v2" or add fields solely to make the experiment look novel.

- **A — Raw evidence:** source/input plus the exact raw observations and unmodified available output/status facts.
- **B — Existing proposed report projection:** the same source/input and same observations, rendered using the current proposed report field order and labels. It may organize and label facts but must not add a diagnosis, infer a missing exit code, promote script output into trusted evidence, or omit material raw facts.
- Both conditions must preserve identical information content. If the proposed report cannot represent a raw fact or its uncertainty, record that as a contract gap before testing; do not silently drop it.
- Use fresh, isolated assistant chats and the same model/mode/tools. Score correction quality, provenance, truthfulness, user effort and turns.
- A synthetic report can test only the usefulness of the proposed information layout. It cannot validate execution, trusted evidence production, artifact creation, or security.

### Scope consequence

No new LOOP/CASE ID is proposed. The experiment evaluates whether existing LOOP-07/08 report behavior creates user value beyond raw output and competitor-native logs. If the proposed report already meets the task but does not improve the next correction or portability, the product should not claim the report itself is a differentiator. Any schema change must go through the existing owner decision and contract review process, not be slipped into this research note.


## 8. Post-review worksheet chronology reconciliation — 2026-11-02

The statement in Section 5 that the paired report-handoff protocol was still missing was accurate for the worksheet revision available when this desk review was authored, but it was superseded later on 2026-11-01. The fixed-task worksheet was strengthened after this review's final commit. The two documents must be read chronologically, not as contradictory descriptions of the same repository state.

Verified Git history on `pocketcode-ai-workflow-director-research-2026-10-28`:

- This desk review's latest commit: `e92384eaf7a342545d15adaeb711e76074557b57`, 2026-11-01 19:50:12 UTC.
- Worksheet paired-experiment alignment commit: `39ca13f6c29d72cea29a5f10a4a8f52713b51c91`, 2026-11-01 20:29:15 UTC.
- Worksheet paired-experiment controls/scoring commit: `3aba52a462127d2b4cf5e6c3cb98c16cce99d836`, 2026-11-01 20:29:54 UTC.
- Worksheet canonical source fixture freeze: `96d1150211b14920105c23554a8adc36b930757f`, 2026-11-01 20:56:47 UTC.
- Worksheet newline correction: `ce734ed53a6073c6ee32c81b0183ade7d458097c`, 2026-11-01 20:56:58 UTC.
- Worksheet isolated fixture sanity-check record: `85bd49b9caac389a9c10c63f1856eca629fcee4f`, 2026-11-01 20:58:13 UTC.

The current worksheet now contains the paired correction test in Section 5B (lines 343–398), including:
- A: fresh assistant chat receives task source/input plus exact native/raw observations, without added diagnosis.
- B: a different fresh assistant chat receives the same source/input/observations represented by the existing proposed PocketCode report.
- Same assistant/model/mode/tools and task/evidence; no shared chat context or cross-exposure of answers.
- A pair is marked CONFOUNDED if the report cannot represent a material fact or uncertainty present in the native evidence.
- Independent scoring for diagnosis, evidence honesty, correction quality, verified success/failure behavior, and user effort.
- Frozen evidence/prompt/rubric before either chat is opened, randomized A/B order, and practical blinding of the scorer where possible.
- At least three comparable pairs if free usage permits; smaller samples remain exploratory.
- A ceiling-effect rule and prohibition on inventing a harder failure fixture after seeing results.

The correct current disposition is therefore:

- **Paired report-handoff protocol:** DESIGNED in the current worksheet.
- **Canonical task source:** FROZEN in the current worksheet; SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7` (1,939 bytes).
- **Isolated fixture sanity check:** RECORDED; validates fixture behavior only.
- **Real product-path execution:** NOT RUN.
- **Paired AI correction experiment:** NOT RUN; cannot begin until a real path produces an observed evidence packet, or else must be explicitly labelled a synthetic information-design-only test.
- **Product hypothesis / report differentiator:** UNVALIDATED.

This is a chronology and status reconciliation, not a new experiment, product decision, schema approval, or acceptance change. The earlier Section 5 recommendation to add the paired protocol has been satisfied by the later worksheet commits. Do not duplicate the protocol or treat its design completion as product-path evidence.
