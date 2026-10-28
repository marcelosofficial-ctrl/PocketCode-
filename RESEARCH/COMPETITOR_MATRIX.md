# Competitor and Alternative Research

**Status:** Desk research refreshed with a narrow public-source addendum; not a complete market study or hands-on benchmark.  
**Latest snapshot:** 2026-10-28 (initial observations below date from 2026-10-20).  
**Purpose:** Avoid assuming that coding on a phone with AI is a unique idea. See [the 2026-10-28 phone-only competitor scan addendum](../AI_COLLAB/PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) and the richer [PR #3 competitor study](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_COMPETITOR_RESEARCH.md); this matrix is a navigation summary, not a duplicate full study.

## Initial landscape

| Product / alternative | Positioning observed in initial research | Why it matters | Questions to verify |
|---|---|---|---|
| PocketCode (one word) | Existing Android IDE with local runtimes, terminal/SSH, Git and multiple AI-provider options, per its official pages | Direct overlap and high naming/discoverability risk; not the same as Catrobat's two-word Pocket Code | Distinctive naming, formal trademark/domain review; actual hands-on feature comparison |
| AndroidHarness | Android-native coding agent; maintainer says it reads/edits projects and runs shell, Git, Python/Node and browser tools on-device | Directly challenges a no-PC Android coding-agent proposition | Setup friction, reliability, isolation boundary, data handling, exact supported device/runtime behavior |
| PhoneCode | Local Android coding agent/workspace; README describes on-device agent and local runtime migration/release gates | Local-first agent may beat hosted execution on cost/privacy for some Android users | Current released runtime path, platform/release status, file permissions, which tasks need remote execution |
| Atlan | Phone development cockpit with a Termux/proot Android path and cloud-client mode; project documentation acknowledges power-user setup and sandbox limitations | Broad coding-agent cockpit overlaps a general mobile workstation promise | Setup effort for novices, real device constraints, actual confinement for tool execution |
| Pairlet | Phone/tablet client for coding agents that remain on a user's running computer/server | Strong substitute when a reachable host already exists; less useful when the user truly has no PC/host | Whether target use occurs with a PC unavailable, network/host setup burden, session continuity |
| Derle | Phone-based IDE marketed with terminal, Git, preview, and AI assistance; iOS and Android advertised | Direct overlap with mobile IDE positioning | Execution architecture, languages, pricing, limitations |
| Kodo | iPhone/iPad code editor with AI and remote-development-related features | Relevant iOS-first alternative | Whether each workflow executes locally, remotely, or via SSH |
| Pyodios | iPhone/iPad Python editor, notebooks and REPL based on local Pyodide/WebAssembly; current listing says iOS/iPadOS 26+, no server, app listed free | Direct local execution substitute for supported Python tasks; challenges assumption that a hosted runner is necessary | Package support/memory/task file flows/AI handoff; distinguish local execution from full CPython OS/server capabilities |
| Rish | Experimental open-source mobile workspace and multi-provider AI integrations | Open-source and provider-flexibility reference | Maturity, supported platforms, security, activity |
| Paseo | Open-source/mobile-oriented coding and AI workflow | Alternative architecture and UX reference | Maintenance, runtimes, setup burden |
| Pockode | Mobile-oriented coding tool | Similar user need and naming proximity | Platform, runtime, persistence, pricing, active status |
| Codeg | Mobile coding/AI development workflow | Relevant workflow alternative | Execution and export capabilities |
| AndCode | Android local AI coding-agent project | Local execution and agent workflow reference | Scope, runtime limits, maintenance, security, device requirements |
| Replit | Hosted development environment with collaboration and AI features | Strong hosted IDE alternative | Phone usability and cost for target workflow |
| GitHub Codespaces | Hosted development environments tied to GitHub repositories | Existing way to code without owning a PC | Mobile UX, setup complexity, usage cost, beginner accessibility |
| SSH to a server / cloud VM | Flexible remote development approach | Powerful existing substitute for technical users | Setup burden and audience suitability |

## Initial strategic interpretation

A generic “run code on a phone” or “mobile IDE with AI” message is crowded. A potentially sharper hypothesis is an execution-and-verification loop that works with code from any AI provider:

1. Run code in a suitable isolated environment.
2. Show actual stdout, stderr, exit status, generated files, runtime details, and relevant limits.
3. Produce a compact report the user can send to any AI assistant.
4. Review proposed edits and rerun to verify whether the issue was fixed.

This is only a hypothesis. Existing products may already provide parts or all of this workflow. The next research pass must compare concrete user journeys rather than marketing claims.

## Public references from the initial pass

- Pocket Code: https://www.pocketcodeapp.com/en
- Derle: https://derle.app/
- Kodo: https://apps.apple.com/us/app/kodo-ai-code-editor-ide/id6781042920
- Rish: https://github.com/ZSeven-W/rish-app
- Paseo: https://git.mitgai.net/getpaseo/paseo
- Pockode: https://pockode.com/
- Codeg: https://docs.codeg.app/
- AndCode: https://github.com/yuga-hashimoto/and-code
- Replit: https://replit.com/
- GitHub Codespaces: https://github.com/features/codespaces

Links and product claims must be rechecked before decisions. This is not a feature-by-feature audit, and the existence of a product does not prove it is a direct substitute for every proposed feature.

## Next research actions

- [ ] Inspect each product's current official documentation, pricing, and platform availability.
- [ ] Build a workflow-level matrix: edit, execute, files, dependencies, networking, logs, Git, AI handoff, export, isolation, limits, price.
- [ ] Distinguish local execution, SSH/remote execution, and provider-hosted sandbox execution.
- [ ] Check whether the proposed evidence/report/fix/rerun workflow is genuinely missing.
- [ ] Validate PocketCode name for product collisions, trademark risk, and domain/social availability.
- [ ] Interview target users and test alternatives with realistic tasks.

## Dated research delta — 2026-10-28

New iOS-specific finding: [Pyodios](https://pyodios.caffeinatedmath.com/) says its current release runs Python 3.14 via Pyodide/WebAssembly locally on iOS/iPadOS 26+, without a server. Its FAQ documents limitations around initialization, memory, session persistence, and packages. [Official Pyodide docs](https://github.com/pyodide/pyodide) explain that package support depends on pure-Python wheels or Pyodide-compatible WASM builds. This raises a local-first/browser-WASM option for a narrow MVP; it does not prove the app or a PocketCode embedding will satisfy the full task/security needs.


The new alternatives above are based on current project/official pages, not independent product tests. Details and source caveats are centralized in [PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md](../AI_COLLAB/PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md). The broad conclusion remains a hypothesis: the differentiator to test is a narrow, trustworthy run/inspect/report/iterate loop, not generic AI coding from a phone. Do not claim a competitor gap until the same task is compared with real alternatives.


## Dated research delta — evidence/report features are not unique (2026-10-28)

Current public documentation makes the initial “portable evidence and correction loop” hypothesis more competitive than a generic gap statement suggests:

- [AndroidHarness](https://github.com/Sanuu7/AndroidHarness) describes inspectable tool-call cards, real command exit/termination outcomes, saved run history, resume after interruption, build/test status, failed-run handoff to its agent, and a diagnostic report with a fixed whitelist and explicit missing-log reporting.
- [Atlan](https://github.com/Atlansdaddy/atlan) describes mirrored console logs and automatic attachment of queued errors to the agent's next turn.
- [Pairlet](https://github.com/heypandax/pairlet) describes streamed output/tool events with timing, session continuity/replay, changed-file diffs, file preview, and usage context (with backend-specific capability gaps).
- [Pyodios](https://pyodios.caffeinatedmath.com/faq) describes real local execution and import/export of files; notebook export is also supported.
- [PhoneCode](https://github.com/dttdrv/phonecode) describes a local agent/workspace and an explicitly submitted AI-output-report endpoint.

These are source-backed maintainer descriptions, not independent verification. They rule out treating logs, error handoff, diagnostics, file export, or continuity as an assumed competitor omission. They do not prove that every alternative exports the same normalized run receipt or works as well for the same iPhone CSV task.

**Revised testable gap (still unverified):** a provider- and execution-location-neutral receipt that binds a specific run to its input/source revision and artifacts, explicitly marks unknown or unobserved evidence, distinguishes process outcome from job/artifact-release disposition, and is useful to a separate AI assistant. Compare this directly with each tool's native logs/reports and raw-error copy/paste. If the native path is equally easy and sufficiently truthful, or the receipt does not improve the next correction, narrow or stop this product direction.

See the [dated source review and revised test questions](../AI_COLLAB/PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md). All task comparisons remain **NOT RUN**.


## Platform-fit caveat for the fixed-task study — 2026-10-28

Separate **direct task substitutes** from **adjacent market competitors**. For the current iPhone-only scenario, the most relevant first comparison is ordinary copy/paste versus Pyodios on a compatible iOS 26+ device and browser-local Pyodide/WASM if file I/O is practical. AndroidHarness, PhoneCode and Atlan are important market-positioning counterexamples but their Android product descriptions do not make them direct iPhone execution paths. Pairlet has an iOS client but depends on a separate computer running its daemon, so it belongs in a host-available scenario rather than the no-PC scenario. Hosted IDEs require current account/plan/mobile-flow verification before scoring. All hands-on comparisons remain NOT RUN.


## Additional direct iPhone local-execution alternatives — 2026-10-29

- **Carnets** is listed as a free standalone offline Jupyter/Python app for iPhone/iPad with many bundled packages. Its listed size is large (1.5 GB for the standard app; 2.2 GB for the scipy variant), a practical phone-storage cost to measure.
- **Juno** documents local/offline Python, projects, scripts, notebooks, file management and Shortcuts, but says code execution is free to try and then requires a one-time Pro purchase. Treat as trial-only under the strict $0 constraint unless current terms demonstrate otherwise.
- **Pyroid** describes local/offline CPython and file/project workflows, but its listing limits free execution to five runs before paid Pro. Treat as limited-trial, not sustained $0 execution.

Sources: [Carnets App Store listing](https://apps.apple.com/us/app/carnets-jupyter/id1450994949), [Carnets developer project](https://holzschu.github.io/Carnets_Jupyter/), [Juno App Store listing](https://apps.apple.com/us/app/python-ide-jupyter-juno/id1462586500), [Pyroid App Store listing](https://apps.apple.com/us/app/pyroid/id6758005480). These are product descriptions, not hands-on verification. For the fixed task, compare ordinary chat/copy-paste, Pyodios and Carnets first if approved; all hands-on comparisons remain NOT RUN.

## Carnets workflow-fit caveat — 2026-10-29

Carnets' official project page describes a free, fully local Jupyter implementation with full directory access; its current App Store listing says notebooks and code run on-device and lists a 1.5 GB app size. This makes it a real local-execution comparator, not merely a notebook viewer. However, the workflow is Jupyter/notebook-centered: older maintainer support guidance says standalone `.py` files may need to be edited through the directory editor and executed from a notebook with `%run file.py`, rather than opened as notebooks. Treat that specific interaction as a historical clue, not proof of current behavior; hands-on verification is needed. iOS folder permission is part of the task setup: the developer explains that opening one file does not necessarily grant access to sibling data files unless the containing directory is explicitly selected.

Sources: [Carnets developer page](https://holzschu.github.io/Carnets_Jupyter/), [App Store listing](https://apps.apple.com/us/app/carnets-jupyter/id1450994949), [maintainer's older .py-file guidance](https://github.com/holzschu/Carnets/issues/38), [maintainer's directory-permission explanation](https://github.com/holzschu/Carnets/issues/101). These sources do not establish current exact script/file behavior. Comparison remains NOT RUN.


## Open-source implementation patterns — 2026-10-29

The focused [Open-Source Reuse Audit](../AI_COLLAB/OPEN_SOURCE_REUSE_AUDIT_20261029.md) reviews RunSeal (Apache-2.0), AndroidHarness (MIT), PhoneCode (Apache-2.0 original code with separately licensed bundled components), OpenHand (MIT), Pairlet (MIT root project; check dependency closure) and OpenHands (MIT core with enterprise carve-out). It records direct source links and adoption boundaries.

The prior-art scan confirms that structured run history, tool receipts, safe diagnostics, interrupted-task recovery, capability matrices, provider abstraction and event replay are already explored in open-source projects. These are not defensible differentiators by themselves. Strongest patterns to adapt to PocketCode's existing proposal are: authoritative lifecycle ownership; process outcome separated from wrapper failure; confirmed timeout/cancellation; explicit unsupported capabilities; recovery that inspects uncertain side effects instead of blindly replaying; privacy-whitelisted diagnostics with missing evidence explicit; and deterministic adversarial conformance tests. See the audit for platform and license caveats. No code was copied, no competitor was run, and no product decision is validated by source review alone.
