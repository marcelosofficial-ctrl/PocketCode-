# Phone-Only Competitor Scan Addendum — 2026-10-28

**Status:** Dated public-source scan; not a hands-on benchmark, market-size study, legal review, or approved product decision.  
**Purpose:** Refresh only the material new alternatives found after the existing competitor research, without duplicating or overwriting the broader analysis on PR #3.  
**Authority:** Existing [PR #3 competitor research](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_COMPETITOR_RESEARCH.md), [main competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md), and [mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) remain the broader sources.

## Executive conclusion

The landscape is moving beyond “write code in a mobile editor.” Current public project pages describe local Android coding agents, local Linux toolchains, and phone clients that steer coding agents on a different computer. This makes a broad promise like “AI coding on your phone, no PC” less defensible on its own.

This scan suggests a sharper hypothesis to test: **make one supported execution task unusually clear and trustworthy—small input, constrained run, real outcome and artifact evidence, and a copyable report that can be used by any AI assistant—without asking users to configure a full IDE, maintain a remote host, or trust a simulated result.** That is still a hypothesis, and existing tools may already satisfy the job.

## Newly surfaced adjacent projects

| Alternative | What its own public page says (not independently verified) | Why it matters to PocketCode | Key distinction to test |
|---|---|---|---|
| [AndroidHarness](https://github.com/Sanuu7/AndroidHarness) | Native Android coding agent with project file access, Linux shell/toolchain, Git, Python/Node, browser/tools, and no-PC positioning. | Directly challenges an Android-first “agent works on the phone” concept. | Does a short run/report task require the wider agent workspace, or is a narrower mobile workflow materially easier and safer? |
| [Pyodios](https://pyodios.caffeinatedmath.com/) ([App Store](https://apps.apple.com/us/app/pyodios/id6762922366)) | Free iPhone/iPad app whose current page describes Python 3.14 through local Pyodide/WebAssembly, a script editor, notebooks, files, packages, and no server. Current release requires iOS/iPadOS 26+. | Strong direct substitute for running many small Python tasks on iOS without a PC or remote runtime. It weakens the assumption that a hosted runner is the only PC-free path. | Verify package support and task/output handoff; current FAQ reports first-run initialization, an approximately 300 MB Python memory budget, a fresh session each launch, and network need for packages not already present. |
| [PhoneCode](https://github.com/dttdrv/phonecode) | Native Android coding agent/local development workspace; its README describes per-project workspaces, local Git and Alpine/Linux runtime, model-provider choices, and explicit file/tool controls. It also describes runtime/platform release gates. | Another direct local-first substitute, with particular focus on device-local processing and avoiding a general-purpose hosted backend. | Is there a meaningful user need for a disposable remote run, cross-platform workflow, or standardized execution receipt rather than local tool execution? Check current release/platform availability before any comparison. |
| [Atlan](https://github.com/Atlansdaddy/atlan) | Phone-oriented development cockpit using Termux/proot on Android; offers editor, terminal, agent orchestration, deterministic checks, and a cloud-client mode for a hosted server. Its README explicitly notes host/platform and sandbox limitations. | Shows that power-user Android workflows and full coding-agent cockpits are already being explored. | Is the target user a power user willing to configure Termux, or someone who wants a small task flow without setting up a workstation? Don't promise stronger isolation than is actually demonstrated. |
| [Pairlet](https://github.com/heypandax/pairlet) | Open-source phone/tablet/desktop client for steering coding agents that remain on the user's computer; the published FAQ says the host computer and daemon must stay running and notes that the custom secure channel has not had an independent audit. | Demonstrates a credible phone-as-controller route when a PC exists. | Does PocketCode's phone-only case persist when the user has no reachable host, or is remote-PC access enough for the target user? |
| [PocketCode (one word)](https://www.pocketcodeapp.com/en/about) | Existing Android IDE markets on-device runtimes, terminal/SSH, Git, and multiple AI-provider options. Its official pages explicitly distinguish it from Catrobat's two-word “Pocket Code.” | High naming, discoverability, and differentiation risk for this project's provisional name. This is not a legal conclusion. | Review distinct naming options before domain, brand, or launch investment; do not rename the repository as part of this research pass. |

**Evidence class:** primary-source self-description. These pages can establish what maintainers claim, but not comparative usability, real-world security, user demand, or PocketCode's relative performance. No app was installed or executed as part of this scan.

## Implications

0. **Local iOS execution is a serious comparator.** [Pyodios](https://pyodios.caffeinatedmath.com/) currently claims local Python 3.14 execution via Pyodide/WebAssembly on iOS 26+. Its own FAQ also describes startup latency, a roughly 300 MB Python memory budget, session reset between launches, and package compatibility/network limitations. These are maintainer claims, not independent verification; include Pyodios and browser-local Pyodide in the next fixed-task comparison.
1. **Do not compete on breadth.** A list of languages, agents, terminal features, MCP connectors, or models is easy to match and expands risk. The present project is not yet ready to compete as a full mobile IDE.
2. **Choose a task, not an audience slogan.** “People who code on phones” is too broad. A user may be an offline learner, Android power user, travelling developer, iPhone-only user, or person with a remote PC; these needs are not equivalent.
3. **Make execution evidence the differentiator to test.** Show exactly what ran, what did not run, the status/exit evidence, bounded output, generated-file metadata, and any cleanup/evidence uncertainty. Do not collapse a successful process exit into overall job PASS if mandatory evidence is missing.
4. **Compare local, remote-PC, and hosted paths fairly.** Local execution may be faster/private/free; remote-PC workflows may reuse existing setup; hosted disposable runs may reduce setup but bring latency, data-transfer concerns, ongoing cost, and sandbox obligations.
5. **Keep the Director subordinate.** Compact prompts and continuity capsules may reduce repeated work but do not validate the core execution problem and do not create a product moat by themselves.
6. **Keep the product name provisional.** The existing same-spelling Android IDE makes name collision a concrete discovery/distribution risk; formal trademark/domain clearance remains unperformed.

## Fixed-task comparison to use in later research

Include local-on-device execution (especially Pyodios on iOS) and browser-local WASM alongside remote-PC and provider-hosted paths. A local result may be preferable when the script/package is supported; remote execution is justified only by demonstrated user value and a credible, approved safety/cost plan.

Use one synthetic, small task across alternatives where practical, such as: *accept a tiny CSV input, run a short Python transformation that produces a summary file, surface a known syntax/runtime failure, and produce a report a user can paste into a separate AI chat.*

Record, without guessing:

- Setup prerequisites and steps, first-run friction, and whether a PC or account is needed.
- Where code and inputs execute or persist (device, user's PC, or provider environment).
- Whether the task genuinely runs and outputs can be retrieved; distinguish documentation claims, screenshots, and observed evidence.
- How success, program error, timeout/cancel, infrastructure failure, output truncation, and missing evidence are represented.
- How the user transfers a report back to an AI, and whether the report preserves enough context for the next correction.
- Supported platform, file/runtime limits, privacy/retention claims, network constraints, setup time, cost terms, and known caveats.
- What the competitor does better. A fair study must capture counter-evidence, not only gaps.

Do not create accounts, run live provider workloads, submit private data, install software, pay, or launch deployments for this desk-research task. If a firsthand test is not feasible on the phone under the current limits, record it as **NOT RUN** and use only sourced statements.

## Next action

Use this addendum with the existing PR #3 competitor research; do not rewrite or duplicate that document. The [product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) and [fixed-task comparison worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) now record one candidate job, the local-first alternative, success/failure outcomes, and evidence criteria. The comparison remains **NOT RUN**. Next, challenge the hypothesis against these alternatives before promoting any architecture or MVP choice. No market validation has occurred.

## Source refresh — version and adjacent-tool changes (2026-10-28)

**Evidence class:** Current public-source claims only; not independently tested. This refresh does not supersede the broader PR #3 competitor study and does not convert the fixed-task comparison from NOT RUN.

| Alternative | Refreshed public evidence | Product implication / limit |
|---|---|---|
| [Pyodios FAQ](https://pyodios.caffeinatedmath.com/faq) and [App Store listing](https://apps.apple.com/us/app/pyodios/id6762922366) | Current documentation describes Python 3.14.2 through Pyodide/WebAssembly, iOS/iPadOS 26+, first-start initialization around 5–15 seconds, approximately 300 MB Python memory budget, a fresh session on each launch, and package/network caveats. The App Store page markets on-device execution without sending code to a server. | Strong local iOS comparator for the synthetic standard-library CSV task. Must still directly verify real file input/output, failure behavior, report portability, and exact device compatibility. Store ratings are too sparse to treat as representative user evidence. |
| [AndroidHarness README](https://github.com/Sanuu7/AndroidHarness) | Current README describes project file access, shell, Git, Python/Node, browser control, visible tool activity, and optional local GGUF models or built-in provider; it also describes broad storage permissions and optional Shizuku/root modes. | Stronger direct overlap than a simple editor. Compare task friction and evidence quality, but do not infer that its broad permissions are equivalent to PocketCode's desired safety boundary or that all model modes are free/unlimited. |
| [PhoneCode README](https://github.com/dttdrv/phonecode) | Current README describes per-project workspaces, local Git, bundled Alpine Linux, chosen model providers, no general-purpose PhoneCode backend, and keys held in Android Keystore. | Direct local-first Android substitute. Still needs platform/release availability and task-specific file/report behavior checked before scoring. |
| [Mobile Harness on F-Droid](https://f-droid.org/packages/com.jarves.mh/) | F-Droid's current page describes an experimental alpha for ARM64 Android: AI coding, Linux terminal, files/diffs, previews, persistent or quick projects, and guided Ubuntu runtime setup without requiring Termux or root. It lists Anthropic API and experimental Anthropic-compatible gateways. | Newly surfaced adjacent option worth tracking for Android. The listing does not establish zero-cost model use, production readiness, security isolation, or comparative ease. |
| [Pairlet README](https://github.com/heypandax/pairlet), [FAQ](https://pairlet.org/guides/faq.html), [security model](https://pairlet.org/guides/security.html) | Current repository advertises v1.9.4 and six agent backends, with capabilities differing by backend. The FAQ/security page says the user's host and daemon must remain available and that the custom encrypted channel has not received an independent security audit. | Refresh the earlier version-specific note: Pairlet is a moving target, not merely a Claude/Codex remote viewer. It remains a host-dependent alternative, not the answer when no reachable computer exists. Its own security caveat must remain visible. |

### What changes in the comparison plan

1. Keep Pyodios as the first iOS-local candidate because the fixed task needs only the standard library; this avoids conflating package-install limitations with the core task.
2. Add Mobile Harness to the Android alternative watchlist, but do not install or score it during desk research.
3. For AndroidHarness and PhoneCode, record that local execution and agent orchestration are already combined in existing products. PocketCode must show a concrete advantage in task setup, truthful evidence/reporting, cross-platform continuity, or safety—not simply claim “AI coding on a phone.”
4. Keep Pairlet in the remote-host category. Its broader agent support does not remove the requirement for a running host, and encryption is not the same as sandboxing or independent security assurance.
5. All task runs, timing, output correctness, user preference, and security behavior remain **NOT RUN / NOT VERIFIED**. Public documentation cannot fill those worksheet fields.


## Source refresh — execution limits and evidence implications (2026-10-28)

**Evidence class:** Current official/maintainer documentation reviewed on 2026-10-28. These are documented claims, not hands-on observations or independent safety validation. This section refines the comparison questions; it does not change the fixed-task result from NOT RUN.

| Source | Current documented fact | What it means for PocketCode research |
|---|---|---|
| [Pyodios FAQ](https://pyodios.caffeinatedmath.com/faq) and [current app page](https://pyodios.caffeinatedmath.com/) | Pyodios v1.1 describes CPython 3.14.2/Pyodide 314.0.5, requires iOS/iPadOS 26+, and runs Python locally. The FAQ says the first launch/updated environment may need initialization, a fresh Python session starts each app launch, files persist in app storage and can be imported/exported through Files, and Python has about 300 MB available. | The standard-library CSV task is a credible local-first candidate, not a reason to build a hosted runner. Direct task execution, export, and malformed-input behavior are still NOT RUN. |
| [Pyodios FAQ — interrupting code](https://pyodios.caffeinatedmath.com/faq) | The FAQ says code cannot currently be interrupted while executing; a run times out after 120 seconds, but code continues in the background and later runs wait until the Python session is restarted. | Record timeout/cancellation semantics and recovery as a separate reliability dimension. A timeout message must not be mistaken for confirmed process termination. For arbitrary or untrusted code, this is a material limitation to understand, not proof of a specific exploit. |
| [Pyodios App Store listing](https://apps.apple.com/us/app/pyodios/id6762922366) | The listing says “Data Not Collected” based on developer-provided privacy information and notes that the information has not been verified by Apple. | Attribute privacy statements to the developer; do not present the store label as an independent audit or proof of every execution/data-flow property. |
| [Pyodide browser file-access FAQ](https://pyodide.org/en/stable/usage/faq.html), [file-system docs](https://pyodide.org/en/stable/usage/file-system.html), and [file access quick reference](https://pyodide.org/en/stable/usage/accessing-files.html) | Browser-local Python needs an explicit browser file-transfer or file-system integration. The native File System Access API is described as experimental and limited to Chromium-based browsers; local-file access is constrained by browser security rules. | A browser/WASM implementation needs a real target-browser input/output design and test. Do not assume that running Python in WASM automatically grants convenient iPhone file access or hard resource/security boundaries. |
| [AndroidHarness Google Play listing](https://play.google.com/store/apps/details?id=com.androidharness.app) and [repository](https://github.com/Sanuu7/AndroidHarness) | Current public descriptions claim on-device project editing, shell, Git, browser tools, and Python/Node execution without a PC; the store listing shows the app is available as an Android product. | Treat it as a serious local-first substitute for the broader Android coding-agent idea. Claims do not establish comparative usability, complete isolation, or the user's exact device compatibility. |

### Updated comparison priorities

1. **For the fixed CSV task:** prioritize real input selection, actual `summary.json` creation/export, malformed-header behavior, and whether the report truthfully distinguishes observed status from unavailable exit evidence. Avoid adding third-party package setup to this standard-library task.
2. **For general product scope:** separately capture interruption, timeout, and recovery behavior. Do not infer termination from a timeout label.
3. **For privacy:** separate app-store developer disclosures, architecture descriptions, direct observations, and independent verification. These are different evidence classes.
4. **For browser/WASM:** test the intended target browser's explicit input/output flow before claiming a usable local-first PWA.
5. **For all alternatives:** execution correctness on one task does not prove isolation, abuse resistance, or security; keep those claims UNKNOWN unless independently established.

No apps were installed, no code was run in a competitor, no accounts were created, and no live provider or paid service was used. All fixed-task scenarios remain NOT RUN.


## Source review — evidence handoff is already present in adjacent tools (2026-10-28)

**Evidence class:** Current public project documentation, reviewed as maintainer/product claims. No app was installed, no task was run, and no security or usability behavior was independently verified.

This review materially narrows the proposed differentiator: PocketCode must not imply that logs, visible tool events, error handoff, diagnostic exports, or phone-to-agent continuity are generally missing from existing tools.

| Alternative and source | What its public documentation already describes | Consequence for PocketCode |
|---|---|---|
| [AndroidHarness README](https://github.com/Sanuu7/AndroidHarness) | Tool-call cards that can be inspected; shell/background jobs with actual exit codes and exit-vs-killed state; saved run history and execution status; interruption/resume cards; build/test output and pass/fail status; failed-run handoff to the agent; and a diagnostic report generated from a fixed whitelist, with missing/unavailable logs reported explicitly. | A broad claim that PocketCode uniquely offers truthful status, diagnostics, or error-to-agent handoff is not supportable from desk research. The narrow CSV task may already be served by a much broader local tool, albeit on Android; task friction and exact evidence export still need direct comparison. |
| [Atlan README](https://github.com/Atlansdaddy/atlan) | Its phone-oriented development cockpit says console logs are mirrored and errors are queued and automatically attached to the agent's next turn with file/line information; it also describes snapshots saved as real PNGs for visual debugging. | “No more manual copy/paste of errors” is also not a defensible differentiator by itself. Atlan's documented setup/platform assumptions and the user's actual target task need a fair comparison. |
| [Pairlet README](https://github.com/heypandax/pairlet) | Its phone/tablet client describes streaming output, tool events with timing, background-task state, session replay/reconnect backfill, changed-file diffs, file preview, context and usage; capabilities vary by agent backend. | Remote-host tools already provide rich session visibility and continuity. Pairlet remains dependent on a reachable host and its per-backend capability differences, but the report/continuity concept alone is not novel. |
| [Pyodios FAQ](https://pyodios.caffeinatedmath.com/faq) | It describes real local Python execution, saved files, file import/export through Files, and notebook export to HTML. | A generated file can already be retrieved through an ordinary local workflow. PocketCode must prove a material advantage in verification/report assembly or correction—not merely that it can export an artifact. |
| [PhoneCode README](https://github.com/dttdrv/phonecode) | It describes local project workspaces, agent execution, file operations, local Git and an explicitly submitted AI-output-report endpoint. | Local agent workflows and reporting-related concepts already exist; do not assume a unique cross-provider handoff gap without comparing the exact report contract and user journey. |

### Revised differentiation test

The remaining plausible gap is narrower and **unproven**: a small, portable, execution-location-neutral receipt with a stable schema that distinguishes *observed facts* from unavailable evidence, binds outputs to a specific run/input/source revision, preserves failure/timeout/cancellation uncertainty, and can be pasted into a separate AI app without requiring the same integrated agent or host.

That combination is a research question, not a claimed market gap. Existing products may already meet the user need with less friction. The fixed-task study should therefore ask:

1. Can the existing tool create and export the real output and represent the deliberate malformed-input failure truthfully?
2. Can a user retrieve the relevant evidence without switching into a complex workspace or maintaining a host?
3. Does a normalized receipt preserve any decision-relevant fact that the existing tool's native logs, diagnostic report, or raw error omits?
4. In a paired correction attempt, does that receipt improve the next AI correction compared with the competitor's normal report/log/raw error?
5. Is the advantage large enough to justify a separate app rather than a small interoperable format or workflow layer?

If the existing tool supplies equivalent evidence and the separate report does not improve correction or portability, narrow or stop the runner/report-product hypothesis. Keep all of these comparisons **NOT RUN** until observed.

No app installs, task runs, accounts, paid services, deployments, or provider workloads occurred in this source review.
