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


## 10. iOS browser-runtime and worker-cancellation revalidation — 2026-11-03

This is a narrow update to the browser-local execution comparison. It does not select Pyodide or change the fixed-task experiment.

### 10.1 Current Pyodide release and payload implication

The current official Pyodide stable documentation and release page still identify **314.0.7** as the latest stable version. The release page lists **315.0.0-alpha.2** as the prerelease/next channel, not the stable default. The full 314.0.7 distribution is documented as 200+ MB; the smaller `pyodide-core` archive contains the minimum runtime files and is intended for deployments that retrieve optional packages separately.

Implication for PocketCode: do not use the 200+ MB full distribution as the assumed first-run payload. The frozen CSV-to-JSON task uses Python's standard library, so a core-only build may be a better comparator. This is a hypothesis to measure, not a verified payload size or load-time claim. Record first cold download, warm cache startup, offline/reload behavior, memory pressure and package requests separately. Pin the exact runtime and lockfile; do not use the moving `dev` CDN channel.

### 10.2 Interrupt and hard termination are separate controls

Pyodide 314.0.7 documents `pyodide.setInterruptBuffer()` as a web-worker-only mechanism that consumes a `SharedArrayBuffer` shared with another browser thread. Writing SIGINT (2) requests a Python `KeyboardInterrupt`. This is a cooperative language-level interrupt path. It is not an operating-system kill, a memory cap, or proof that every WebAssembly instruction/C extension will yield to Python signal handling.

The browser `Worker.terminate()` path is the independent host-controlled stop mechanism. Do not conflate the two:
- `setInterruptBuffer`: graceful/cooperative interrupt attempt; record whether the code actually handles and returns from it.
- `Worker.terminate()`: host-controlled abrupt termination request; do not rely on an in-worker acknowledgement after calling it. Verify externally that execution stops, no further worker activity occurs, resources recover, and the page remains responsive.
- App/page close, reload, backgrounding, or PWA suspension: separate lifecycle events, not substitutes for a confirmed worker-stop observation.

SharedArrayBuffer availability is conditional on the browser's security/isolation context. Feature-detect `crossOriginIsolated` and `SharedArrayBuffer` at runtime; do not make them a required assumption for all deployed iOS contexts. A COOP/COEP setup also affects cross-origin resource loading, so the exact runtime/CDN and service-worker deployment must be tested together.

### 10.3 WebKit fix status: do not over-credit stable iOS

WebKit bug 289686 concerned a worker running non-yielding WebAssembly/atomic wait that could continue after `worker.terminate()` or page reload, with a possible high-CPU spin symptom. The bug is now marked RESOLVED FIXED. The fix landed in WebKit main as commit `03e836de2f7bd5627a95f60357633d59fb6bb18` (319508@main) on 2026-08-20.

The release evidence needs careful interpretation:
- The fix is explicitly listed in the official [Safari Technology Preview 252 release notes](https://webkit.org/blog/18304/release-notes-for-safari-technology-preview-252/).
- Safari 27.0 became the stable iOS/WebKit generation in September 2026, but the official [Safari 27.0 resolved-issues page](https://webkit.org/blog/18325/webkit-features-for-safari-27-0/) does not enumerate bug 289686 / 147482360.
- The current [Safari 27.2 release notes](https://webkit.org/blog/18515/webkit-features-for-safari-27-2/) list 20 fixes, but do not enumerate this worker-termination fix.
- Apple confirms [iOS 27.2 and iPadOS 27.2 shipped on 2026-10-26](https://support.apple.com/en-us/149230). The Safari 27.2 release-note page confirms Safari 27.2 is included in iOS 27.2.

Therefore, the defensible conclusion is: **the code fix exists in WebKit main and is present in Safari Technology Preview 252, but public stable-release notes reviewed here do not establish that the exact fix is present in the stable iOS 27.2 engine.** Absence from release notes is not proof the change was omitted. It is also not sufficient evidence to claim the fix shipped. Only a target-device test or an authoritative release-build mapping closes this uncertainty.

### 10.4 Required iPhone proof matrix before relying on local execution

Run these only when the device and explicit test conditions are available. Test both Safari tab and installed PWA where the PWA route is supported:

1. **Capability inventory:** exact iOS/Safari build; browser vs PWA; `crossOriginIsolated`; `SharedArrayBuffer`; module-worker creation; worker startup; OPFS availability; actual Pyodide/core and package versions.
2. **Cooperative interrupt:** a bounded Python loop that can process SIGINT; assert that a `KeyboardInterrupt` is observed, the worker reports a terminal message and the UI remains responsive.
3. **Hard stop:** a non-yielding Python loop, a compiled WebAssembly tight loop, and an `Atomics.wait`/shared-memory worker. Trigger `Worker.terminate()`; verify the worker cannot continue consuming CPU, battery or memory after the stop is reported.
4. **Page lifecycle:** reload, close, background/resume, app switch, PWA suspend/resume, force quit and page-process termination. Distinguish a lost UI from a confirmed stopped worker.
5. **Recovery and leakage:** repeat start/stop at least 20 times, then inspect responsiveness, memory recovery, stale worker messages, storage consistency and whether previous run output can appear in the next run.
6. **Resource pressure:** bounded memory stress and large file input/output; observe actual failure behavior, browser termination, persisted workspace and user-facing uncertainty. Do not infer a hard memory quota from an OOM or tab reload.
7. **Cold/warm runtime delivery:** measure core-only standard-library startup and cached startup separately from the full build. Verify that an offline/reload scenario does not silently fetch arbitrary packages or produce a misleading success.

The report must label browser-local execution honestly: worker termination is client/browser evidence, not trusted remote-host evidence; a local `KeyboardInterrupt` is not the same as a server-enforced deadline; and browser-origin APIs exposed to Python remain part of the capability surface.

### 10.5 Decision

Keep **Pyodide 314.0.7 core-only** as the leading browser-local candidate for the fixed standard-library task, but only as a candidate for the comparison. Do not adopt the full distribution by default, do not rely on `setInterruptBuffer` as the sole timeout mechanism, and do not assert that current iOS stable Safari has the WebKit 289686 fix without an authoritative build mapping or on-device test.

This leaves the product recommendation unchanged: browser-local Python is one candidate execution path, not PocketCode's complete execution/security architecture. Safari/PWA behavior, worker-stop certainty, resource pressure, storage and file handoff remain NOT RUN. No runtime, provider, app, account or package was installed; no workload or device test was performed.


### 10.6 Browser API and network confinement

A Web Worker improves UI responsiveness and removes direct DOM access, but it is not a network-disabled process. The stable Pyodide JavaScript API documents that `jsglobals` defaults to `globalThis`; its own browser example imports `fetch` from Python's `js` module. A worker's `WorkerGlobalScope` also exposes `fetch()`. Therefore Python code can reach browser networking capabilities through JavaScript interop unless the execution context constrains them.

**CSP placement is a critical detail.** The worker's policy is not generally inherited from the document that created it. For a normal network-loaded worker, the worker script response itself needs a `Content-Security-Policy` response header. MDN documents that the exception is a worker loaded from a globally unique `blob:` or `data:` URL, which inherits its creator's policy. The CSP `connect-src` directive controls `fetch()`, XHR, WebSocket, EventSource and `sendBeacon()`. A restrictive policy on the app page alone is not adequate evidence for a separately loaded worker.

Recommended browser-local boundary for the first fixed-task comparison:

- Put execution in a dedicated, static-only origin with no authenticated application endpoints, no user/session cookies, no API credentials, no secret-bearing local storage and no privileged JS bridge.
- Serve the worker script with its own restrictive CSP response header. Keep `worker-src` and `script-src` narrow, and restrict `connect-src` to the minimum needed to load pinned runtime assets. The preferred first-task deployment is same-origin, immutable runtime assets on that static-only origin, with no third-party package fetch while user code is running.
- Do not allow the run origin to share a parent-domain authentication cookie. Same-origin `fetch` is still possible if CSP permits it, so the origin must not host private APIs or sensitive responses.
- Treat every message from the worker as untrusted output. Accept only a versioned message schema, enforce byte limits before parsing/rendering, and never execute worker-supplied commands in the app context.
- Test attempted Python-to-JS `fetch`, XHR, WebSocket, EventSource and `sendBeacon` to external endpoints, plus attempts to reach same-origin API paths. Verify CSP violation evidence and that no request reached the test sink. Repeat this on iOS Safari and installed PWA.

This is a proposed design constraint, not an already implemented PocketCode boundary. A CSP failure, unexpected same-origin endpoint, cookie presence or unbounded worker message must fail the test, not be papered over by CORS or by hiding APIs from the Python prompt.

### 10.7 Stable browser memory limits

A second important version distinction: stable Pyodide 314.0.7's official `loadPyodide()` configuration does not list `maxMemoryBytes`. The option appears in current development/314.1.0.dev documentation, where it caps WebAssembly heap growth and returns `MemoryError` after the configured maximum. A search of the stable 314.0.7 JavaScript API returns no such option.

Consequences:
- Do not configure or document `maxMemoryBytes` as a supported stable 314.0.7 feature.
- A WebAssembly build-time maximum, browser/device memory pressure and a product-configured per-run quota are different things. Do not treat one as proof of another.
- Until a stable Pyodide release exposes a supported cap, a browser-local runner cannot claim a product-controlled hard per-run memory ceiling solely from its Pyodide configuration.
- Input, archive expansion, output and message sizes still need explicit application-level bounds. These reduce accidental pressure but do not replace a hard heap limit.
- Memory exhaustion tests must record whether the worker failed, the tab/PWA was terminated, the browser stayed responsive, and the next run recovered. They must not infer a clean resource-limit outcome from a generic allocation error or page reload.

### 10.8 Browser-path acceptance boundary

The browser-local Pyodide candidate may still provide a valuable low-cost, phone-first execution experience for small bounded tasks. However, a worker plus Pyodide alone does **not** meet the full meaning of LOOP-12. To be considered a constrained execution boundary, the implementation must independently demonstrate:
1. no app secrets or privileged same-origin endpoints are reachable from the run context;
2. external network attempts are blocked by the worker's applied policy;
3. worker messages and output collection are bounded before app-side buffering;
4. deadline enforcement stops a non-yielding worker on supported iOS builds;
5. memory pressure is safely contained and does not destabilize the app/device;
6. page/PWA lifecycle transitions do not turn a lost observation into a false success.

Until then, use browser Pyodide as a **browser-local comparator / limited-execution candidate**, not as a verified hostile-code sandbox or a substitute for a server-side OS boundary. The distinction preserves the existing LOOP-12 and CASE-15 meanings.


### 10.9 Proposed cross-origin execution topology

The preferred browser-local design should not host untrusted execution on the authenticated PocketCode app origin. A same-origin worker can still make same-origin requests and potentially interact with same-origin browser facilities. The stronger candidate topology is:

PocketCode app origin (authenticated)
- Project/UI/session state and authenticated API credentials.
- Creates a sandboxed cross-origin iframe.
- Transfers only bounded input and a run-scoped message port.

Dedicated execution origin (static-only, no credentials)
- No login, cookies, private API, server functions or user secrets.
- Minimal iframe bootstrap and immutable pinned assets.
- Creates a module Web Worker.

Dedicated execution worker
- Pinned Pyodide 314.0.7 core.
- Fresh in-memory filesystem per run.
- No arbitrary package installation.
- No privileged JS bridge.
- Bounded input/output protocol.

The execution origin should be a different registrable domain from the authenticated app, not merely a sibling subdomain, unless cookie scope is proven host-only and no parent-domain cookie can be sent to the execution host. It must not serve authenticated APIs, user-specific responses, signed download endpoints, or server-side functions. Prefer immutable static files only. The app must never send access tokens, session cookies, provider credentials, Git credentials, or private project secrets to this origin.

A cross-origin iframe can be sandboxed with scripts enabled while retaining its own distinct origin. The allow-same-origin token is safe only while the iframe remains genuinely cross-origin from its parent. Never serve the execution iframe from the authenticated app origin. Do not grant top navigation, popups, downloads, forms, modals, pointer lock or other capabilities unless a later case proves they are necessary.

The parent app should:
- Pin the exact expected execution origin and iframe window reference.
- Use a fresh cryptographically random run nonce and a fresh MessageChannel for each attempt.
- Bind every message to protocol version, run ID, attempt ID, nonce and monotonically increasing sequence number.
- Reject messages from the wrong origin, wrong window, wrong port, stale attempt, duplicate sequence, unexpected message type or invalid state transition.
- Enforce a strict maximum message count, per-message byte size, cumulative bytes, output bytes and execution duration.
- Never accept a worker message as proof of trusted exit, termination or security policy. It is untrusted program/worker output.
- Treat a closed port, iframe navigation, page loss or missing terminal message as UNKNOWN/INCOMPLETE until independently reconciled. A parent timeout does not prove the worker stopped.

The iframe bootstrap is a relay, not an authority. It validates the parent message schema, creates the worker from a fixed same-origin URL, passes only the run input, and forwards bounded worker messages. It has no access to the app's credentials or authenticated API. The worker's terminal message is a claim from the browser execution context, not a remote trusted attestation.

### 10.10 Candidate CSP and capability policy
**Safari-specific blocker:** Pyodide 314.0.7's own browser test suite marks its restrictive-CSP test as an expected failure on Safari with the explicit reason that Safari does not support wasm-unsafe-eval. The fixture policy uses wasm-unsafe-eval to permit WebAssembly while withholding JavaScript unsafe-eval. This means the proposed worker CSP is not currently proven to load Pyodide on iOS Safari. Do not silently add unsafe-eval as a workaround: that directive also permits JavaScript eval/Function code generation and materially weakens the policy. If the target Safari requires unsafe-eval, the Python-visible API must first be proven unable to reach eval or equivalent code-generation paths, and the result remains a major residual risk. Otherwise, the browser Pyodide path may be unavailable under the desired CSP on iOS.


The following is a starting policy for a prototype, not a verified cross-browser configuration. Test the exact response headers and Pyodide boot sequence on each supported browser. CSP is defence in depth; it is not a process sandbox.

Execution iframe response (illustrative):

    Content-Security-Policy: default-src 'none'; script-src 'self'; style-src 'self'; worker-src 'self'; connect-src 'self'; img-src 'none'; font-src 'none'; media-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors https://app.example
    Referrer-Policy: no-referrer
    Permissions-Policy: camera=(), microphone=(), geolocation=(), accelerometer=(), gyroscope=(), magnetometer=(), usb=(), serial=(), bluetooth=()

Dedicated module worker response (illustrative):

    Content-Security-Policy: default-src 'none'; script-src 'self' 'wasm-unsafe-eval'; connect-src 'self'; worker-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'
    Referrer-Policy: no-referrer

Interpretation and caveats:

- script-src self permits only pinned same-origin worker/runtime scripts. wasm-unsafe-eval is required for WebAssembly compilation under CSP without enabling JavaScript unsafe-eval; it must not be broadened to unsafe-eval.
- connect-src self allows the worker to fetch only public static assets from its own execution origin. It does not mean networking is absent. The execution origin must therefore be static-only, with no authenticated or sensitive endpoints and no dynamic write API.
- The runtime, .wasm, standard library archive, lockfile and any allowed package files must be pinned, immutable and served from that same origin. Do not leave an unreviewed third-party CDN in connect-src.
- worker-src none in the worker response is intended to prevent user code from creating nested workers. Verify actual browser behavior; do not assume every CSP directive is enforced identically on all supported iOS versions.
- The iframe frame-ancestors must allow only the exact PocketCode app origin. The app's own frame-src should allow only the execution origin.
- No CORS policy is a substitute for CSP. CORS controls whether a response can be read by a caller; it is not a reliable outbound-network denial control.
- The worker response must carry its own CSP. A normal network-loaded worker does not generally inherit the creating document's policy. A blob/data worker inherits creator policy, but then its exact CSP, module-loading and iOS behavior need separate proof.
- wasm-unsafe-eval permits WebAssembly compilation/instantiation. It is not a restriction on what the Python program computes inside its WASM runtime, and it does not impose memory or CPU limits.
- CSP does not remove browser storage, timing, CPU, memory or all browser API capabilities. The separate origin and restricted JS bridge remain important.

The static-only execution origin may still receive requests to its own public assets. That is an accepted and bounded capability for this candidate, not a claim of zero network. The first proof must demonstrate that no request can reach the app origin, arbitrary Internet destinations, or any endpoint carrying private data.

### 10.11 Pyodide JavaScript-global minimization hypothesis

Pyodide 314.0.7 documents PyodideConfig.jsglobals as the object used for the Python js module, defaulting to globalThis. This gives us a potential capability-reduction experiment: initialize Pyodide with a frozen, null-prototype, empty JavaScript object rather than the worker's actual global object. However, source inspection of the exact 314.0.7 tag shows that this is only one of two automatically registered JavaScript modules. Pyodide also registers pyodide_js, backed by its public API object. That object exposes FS, PATH, ERRNO_CODES, _module and _api, and its API includes methods such as loadPackage, runPython, runPythonAsync and module registration. The documented FS exposes persistent filesystem backends including IDBFS. Therefore, an empty jsglobals object does NOT remove the broader Pyodide JavaScript API or prevent Python from reaching its filesystem/runtime objects through import pyodide_js.

Pyodide also exposes pyodide.code.run_js(), which imports eval from the js module and evaluates JavaScript. An empty jsglobals object should make that particular import unavailable, but this must be tested against the exact runtime and every other exposed API. Do not treat jsglobals alone as a capability boundary. The source-level proof must account for both js and pyodide_js, the full Python-visible Pyodide API, and the Emscripten FS object.

Required isolated proof:
1. Inspect the exact pinned Pyodide tag's import-hook registration and public API. In 314.0.7, pyodide_js is automatically registered as a Python-importable module and the public API object exposes FS, _module and _api. Confirm the exact runtime's exposed properties, not only the docs summary.
2. Determine whether pyodide_js can be unregistered or replaced with a minimal safe facade before untrusted code runs. Remove or attenuate FS, _module, _api, package loading, JS-module registration, stream setters and any other privileged API not needed by the fixed task. Prove that deleting sys.modules entries does not allow re-import through the JS import hook. Verify required Pyodide internals continue to work.
3. Prove that the Python-visible surface cannot mount IDBFS or other persistent filesystems, access OPFS/IndexedDB/Cache Storage, mutate host streams, register JS modules, or recover the original worker global. A fresh in-memory FS is not enough if pyodide_js.FS remains exposed.
4. Load pinned Pyodide 314.0.7 with an empty frozen null-prototype jsglobals object.
5. Verify ordinary standard-library task behavior and stdout/stderr capture still work.
6. From untrusted Python, attempt to resolve js.fetch, js.postMessage, js.indexedDB, js.caches, js.navigator, js.location, js.globalThis, pyodide.http.pyfetch, and access through pyodide.ffi.
7. Attempt to import/use pyodide_js and every custom JS module or proxy exposed by the host wrapper. The intended first proof exposes no privileged JS API.
8. Inspect the resulting Python-visible object graph for references to worker globals, functions, ports, message handlers, Pyodide loader objects and host capabilities.
9. Repeat on iOS Safari and installed PWA. Verify that the configuration behaves the same and does not silently fall back to globalThis.

If the test cannot demonstrate that Python lacks direct access to the worker's privileged APIs, do not rely on this option. Keep the execution origin credential-free and assume the Python code can use any worker API permitted by the browser and CSP.

### 10.12 Storage, cross-run state and message-flood controls

A dedicated origin separates the worker from app credentials, but a reused execution origin can still create persistent browser state. A fresh Worker alone does not clear IndexedDB, Cache Storage, OPFS, service-worker state or browser caches.

For the first comparison:
- Do not mount IDBFS or OPFS; use a fresh in-memory Pyodide filesystem for each attempt.
- Do not expose browser storage APIs through jsglobals or custom JS modules.
- Do not register a service worker on the execution origin.
- Pin and verify immutable runtime assets; do not let a user task install packages or mutate runtime files.
- Clear per-run memory/filesystem state after termination. Treat browser cache as public immutable runtime cache, not user workspace.
- If the API-minimization proof cannot prevent persistent storage access, evaluate a per-run unique execution origin or an opaque-origin iframe design. Both introduce deployment and iOS compatibility questions; neither is selected.

The message channel is also an attack surface. The parent must not trust the iframe to enforce output bounds. Use a strict schema with small fixed-size chunks, maximum event count, cumulative output cap, and a parent-side monotonic deadline. On the first over-limit or malformed message, close the channel and request worker/iframe termination. Record the request and external stop observation separately. Do not buffer an arbitrary structured-clone object and only then decide it is too large; the worker wrapper and protocol must prevent oversized messages from being generated in the normal path, while the parent independently limits accepted cumulative data.

A malicious program may attempt to flood logs or create a huge result object. The UI must not render arbitrary HTML, Markdown or links from worker output without escaping and length bounds. The final report must distinguish complete, truncated, unavailable and uncollected output.

### 10.13 Browser boundary threat cases to add to the proof matrix

These are test cases for the existing fixed-task proof, not new canonical acceptance IDs:

| Threat case | Attack | Required observation |
|---|---|---|
| BR-01 | Python calls js.fetch to an external collector | Request blocked by worker CSP; collector receives nothing |
| BR-02 | Python calls XHR/WebSocket/EventSource to external host | Blocked; no external connection established |
| BR-03 | Python calls same-origin private API path | No such API exists on execution origin; request returns no sensitive data |
| BR-04 | Python attempts app-origin fetch | CSP blocks it; app API sees no request |
| BR-05 | Python inspects JS globals and imports pyodide_js | Restricted js scope and attenuated pyodide_js expose no worker globals, FS, _module, _api, eval, stream controls or privileged wrapper references, or candidate fails this hardening gate |
| BR-06 | Python attempts IndexedDB/Cache Storage/OPFS writes and mounts IDBFS through pyodide_js.FS | Persistent browser storage is unavailable to user code; no cross-run state persists |
| BR-07 | Python forges terminal/result messages | Parent rejects untrusted or malformed schema; no false success |
| BR-08 | Python floods messages/stdout/stderr | Parent enforces event/byte caps and records truncation/termination honestly |
| BR-09 | Iframe navigates or closes during execution | Parent does not treat disappearance as success or confirmed cancellation |
| BR-10 | Old worker/iframe sends delayed output after retry | Run/attempt/nonce/sequence binding rejects stale message |
| BR-11 | Runtime or lockfile is changed between runs | Pinned digest/version check rejects unexpected bytes |
| BR-12 | User code tries to create nested workers or import remote modules | CSP blocks; no unapproved script is loaded |
| BR-13 | iOS Safari loads Pyodide under restrictive worker CSP | Pyodide starts with WebAssembly permitted but JavaScript eval denied; if Safari requires unsafe-eval or the test fails, browser security gate is BLOCKED |

No BR identifier is a canonical LOOP/CASE acceptance ID. These are proposed test names only. They must remain in this research matrix unless an explicit crosswalk is approved.

### 10.14 Decision and next proof order

The cross-origin execution origin plus restrictive iframe/worker CSP is the preferred browser-local architecture candidate. It reduces direct access to app credentials and narrows network reachability without requiring a hosted execution provider. It is not equivalent to a Linux namespace/cgroup sandbox and cannot honestly claim hard CPU or memory quotas.

The next browser proof should be a tiny, isolated harness rather than product implementation:
1. Serve a static-only execution origin with the exact response headers and no cookies/API.
2. Load the pinned Pyodide module worker from that origin.
3. Test the empty jsglobals capability hypothesis.
4. Run the frozen CSV task and malformed-input case unchanged.
5. Exercise all BR-01..12 threat cases with a controlled external request sink and same-origin route inventory.
6. Measure message limits, worker termination, cold/warm startup and memory pressure.
7. Repeat the security/cancellation subset on target iOS Safari and installed PWA.

If any app credential, app API, arbitrary external request, unbounded message path or false-success lifecycle path remains reachable, browser execution stays a limited local convenience and must not be advertised as a hostile-code sandbox. No provider selection or canonical acceptance change follows from this proposal.


### 10.15 Sources for the browser boundary review
- Pinned Pyodide 314.0.7 source: [api.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/api.ts) registers both js and pyodide_js and exposes FS/_module/_api; [pyodide.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/pyodide.ts) defines jsglobals; [test_pyodide.py](https://github.com/pyodide/pyodide/blob/314.0.7/src/tests/test_pyodide.py) marks the restrictive-CSP test xfail on Safari; [test_csp.html](https://github.com/pyodide/pyodide/blob/314.0.7/src/templates/test_csp.html) uses wasm-unsafe-eval; [api.ts FS docs](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/api.ts) list IDBFS among the filesystem backends.
- Pyodide 314.0.7 Python API source: [pyodide.code.run_js](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/code.py) delegates to JavaScript eval through the js module.
- Pyodide 314.0.7 capability attenuation source: [Python import-hook registration/unregistration](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/_pyodide/_importhook.py), [package import notes](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/__init__.py), [webloop dependency on pyodide_js](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/webloop.py), and [HTTP fetch dependency on js.fetch](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/http/_pyfetch.py).

Official sources checked 2026-11-03:

- Pyodide 314.0.7 JavaScript API, including the jsglobals option: https://pyodide.org/en/stable/usage/api/js-api.html
- Pyodide 314.0.7 type translations and JavaScript global access: https://pyodide.org/en/stable/usage/type-conversions.html
- Pyodide 314.0.7 Web Worker guide: https://pyodide.org/en/stable/usage/webworker.html
- Pyodide 314.0.7 service-worker guide and module worker setup: https://pyodide.org/en/stable/usage/service-worker.html
- MDN CSP worker policy placement and blob/data inheritance exception: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy
- MDN connect-src controlled APIs and examples: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/connect-src
- MDN worker-src scope: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/worker-src
- MDN WorkerGlobalScope fetch: https://developer.mozilla.org/en-US/docs/Web/API/WorkerGlobalScope/fetch
- WebAssembly CSP proposal for wasm-unsafe-eval: https://github.com/WebAssembly/content-security-policy/blob/main/proposals/CSP.md

These sources document browser and runtime capabilities. They do not establish that the proposed iframe/origin/CSP topology works on iOS, that Pyodide jsglobals can be safely minimized, or that worker memory/CPU/termination guarantees satisfy LOOP-12. Those remain proof obligations.


### 10.11.1 Potential trusted-bootstrap attenuation experiment

The pinned 314.0.7 source gives a possible, testable mitigation path, but it is not yet proven:

- The JS API exposes unregisterJsModule. It delegates to the Python import hook's unregister_js_module, which removes a named JavaScript proxy from the import finder.
- Pyodide's Python package documentation explicitly says both js and pyodide_js are available for import after Pyodide is initialized.
- The import hook documents that unregistering a JS module does not remove an already imported module from sys.modules; that cache must also be cleared.
- pyodide.webloop imports pyodide_js._api.scheduleCallback when loaded, and pyodide.http.pyfetch imports js.fetch and pyodide_js._api.abortSignalAny. Those features may stop working if the privileged JS module is removed. They are not needed by the frozen synchronous CSV task, but this must be measured rather than assumed.
- pyodide.ffi exposes register_js_module and unregister_js_module to Python. A hostile script may re-register a module using a JsProxy it can obtain. The proof must show that Python can only construct proxies for objects it already owns and cannot recover the original host API object or worker global.

Candidate trusted bootstrap, to be tested in a throwaway harness only:
1. Initialize Pyodide with a frozen null-prototype empty jsglobals object and no custom JS modules.
2. Keep the returned Pyodide API object only in the trusted worker wrapper's lexical closure. Do not assign it to globalThis, a worker property, a message payload, or any object reachable from Python.
3. Before dispatching user code, call the trusted JS API's unregisterJsModule("pyodide_js").
4. Remove any already-imported pyodide_js and pyodide_js.* entries from sys.modules using trusted bootstrap code. Verify that later imports fail because the import finder no longer contains that registration.
5. Audit pyodide._package_loader.loadedPackages: the package loader imports this JS-backed map during Pyodide initialization, so clearing sys.modules does not remove the cached reference. Replace it with an immutable Python-only snapshot or None before untrusted code, if the package loader still needs to remain importable.
6. Keep the host-only FS handle, stdout/stderr callbacks and worker message port in private wrapper variables. Do not expose them through jsglobals, pyodide_js, pyodide.ffi, registered modules or Python globals.
7. Verify pyodide.code.run_js fails because js.eval is absent. Verify this remains true on Safari even if a compatibility CSP policy has to permit WebAssembly using unsafe-eval.
8. Attempt to re-register pyodide_js and js from Python using pyodide.ffi.register_js_module and only Python-created JsProxy objects. Confirm that this cannot restore the original API, worker globals, FS handle, message port or eval reference.
9. Test the exact standard-library fixture, file I/O, bounded stdout/stderr and exception reporting after attenuation. Explicitly test which optional Pyodide features stop working.

This candidate is acceptable only if the full hostile-Python test corpus cannot recover a privileged object. It is not enough that a few known names raise ImportError. The wrapper must retain its private handles, and the Python-visible import/module/object graph must be audited after each runtime update. If this requires patching Pyodide internals or maintaining a fork, treat that as a significant dependency and maintenance cost under the $0 constraint.

**Safari CSP qualification:** Pyodide 314.0.7's own test suite marks the restrictive-CSP test as an expected failure on Safari with the reason "Safari doesn't support wasm-unsafe-eval". Its fixture uses wasm-unsafe-eval to permit WebAssembly without JavaScript unsafe-eval. A Safari deployment may therefore need unsafe-eval or a weaker script policy to load Pyodide. Since unsafe-eval also permits JavaScript eval/Function code generation, it is only a candidate if the preceding API attenuation is proven and a target-device test demonstrates that untrusted Python still cannot obtain eval. If that cannot be shown, reject the browser path for hostile-code execution on that Safari version. Do not quietly weaken CSP to make the demo work.
