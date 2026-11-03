# iOS Python Runner Competitive Baseline — 2026-11-03

**Status:** Public-source desk research. Product claims are vendor/App Store descriptions unless explicitly identified as platform documentation. No apps were installed or tested.  
**Purpose:** Test whether PocketCode's proposed mobile execution value is differentiated from existing iPhone Python tools.  
**Scope:** iPhone/iOS first, because PocketCode's current owner is phone-first and has an iPhone. Android comparison remains separate and open.

## Executive decision

**Do not build a generic iPhone Python IDE/interpreter as PocketCode's differentiator.** The market already has free or low-cost local Python apps with offline execution, file import/export, consoles, stop controls, projects, notebooks and even debugging. One recently indexed product, Coilbook, claims a free CPython 3.14 experience with a Files-app project folder and stop button; another recent App Store product, Python Code Editor & IDE, claims local execution, pip, debugger, pytest, project import and ZIP export. These descriptions are not hands-on verification, but they are sufficient to invalidate the assumption that "run Python on an iPhone" is unique.

PocketCode should differentiate at the **task orchestration and evidence layer**, not by rebuilding the editor/runtime:
1. A portable, provider-neutral task packet that binds exact source and input files to one run identity.
2. A trustworthy host-observed execution receipt: input hashes, runtime identity, start/terminal evidence, exit/outcome, stdout/stderr capture and truncation, output inventory and hashes, cancellation/cleanup evidence, and explicit unknowns.
3. A durable run history and recovery model that never re-executes a completed task merely because report publication or AI handoff failed.
4. A copyable, compact AI debugging packet that carries exact failing source, error/traceback, evidence and constraints into any assistant, with an explicit user-mediated handoff.
5. A bounded correction loop that diffs the AI's proposed patch, lets the user approve it, reruns the same task with a new attempt identity, and preserves prior evidence.

This is a product-direction decision, not approval of a runtime or implementation. The frozen CSV-to-JSON task is still useful as a **workflow/evidence benchmark**, but it is too simple to prove an execution backend advantage by itself.

## 1. Competitor baseline (public descriptions, not hands-on tests)

| Tool | Publicly stated capabilities | Cost/availability signal | What it means for PocketCode |
|---|---|---|---|
| **a-Shell** | Local Unix terminal; runs Python, JS, C/C++ and shell commands offline; file editing and standard command-line tools; SSH/SCP/CURL also listed | App Store listing: Free; iPhone/iPad | Strong $0 control for a script plus data-file workflow. PocketCode cannot claim local offline Python as unique. It may be less approachable than a guided task/report workflow, but that is a hypothesis to test. |
| **Carnets** | Standalone local Jupyter/JupyterLab; notebooks, embedded Python, offline operation, common scientific packages, file/directory access and sharing | App Store listing: Free; iPhone/iPad | Strong free notebook/data-analysis baseline. Not the same as a guided script-run lifecycle, but overlaps with task execution and visible outputs. |
| **Pyto** | Local Python 3.10 interpreter; standard library and bundled third-party modules; editor, terminal, debugger, Shortcuts, file-system APIs and iOS integrations | App Store listing: Free download with IAP; listing shows Lite $7.99 and Full $14.99 (US storefront snapshot) | Mature direct competitor for local scripting, project work and automation. Exact local storefront pricing and current runtime behavior require device/storefront confirmation. |
| **Pythonista 3** | Local Python 3.10 IDE, standard library and bundled packages, iOS-specific modules, share-sheet script invocation and file import | App Store US snapshot: $9.99 | Strong paid scripting baseline. Its documentation says subprocess/multiprocessing launch is blocked by iOS sandbox constraints and scripts run in the app process. |
| **Coilbook** | Developer site claims on-device CPython 3.14, offline script editor, console, interactive input, stop control, notebooks, Files-app folders and import/open from Files/Mail/AirDrop | Developer site claims free unlimited code runs; 3 projects/1 user notebook free; Pro extras. The direct App Store listing/storefront was not independently confirmed in this pass. | Particularly close to PocketCode's frozen-task path. The basic editor/run/import/output loop is already claimed by a competitor. |
| **Python Code Editor & IDE** | App Store description claims embedded local Python, offline execution, pip, debugger, pytest, multi-file projects, Files/iCloud/Drive import and ZIP import/export | App Store AU listing: Free download with IAP; recent listing. US listing shows weekly/yearly Pro IAP. Small review count in third-party catalogues. | Broad advertised overlap with a generic mobile code-runner. Treat claims as unverified until hands-on test; recent/low-review status means reliability and feature depth are unknown. |

### 1.1 Source notes and confidence

- **High confidence for listing claims, not actual behavior:** App Store product descriptions for a-Shell, Carnets, Pyto and Pythonista.
- **Medium confidence:** Coilbook's own product/help/privacy pages. They provide detailed capability descriptions and a privacy policy, but they are first-party marketing/documentation. This research did not independently confirm its App Store storefront listing.
- **Medium/low confidence:** Python Code Editor & IDE's App Store description and third-party app catalogues. Its advertised features are broad, but the app is recent and has very few public ratings. Treat each advertised feature as a test hypothesis, not an established product fact.
- Ratings, prices and availability vary by storefront and can change. No Belgian storefront purchase or install check was performed.

## 2. Platform constraint that changes the product architecture

Python's official iOS documentation explains that Python on iOS is distributed in embedded mode inside an app; iOS does not expose a system-wide Python executable/REPL. The same-process constraint matters: Pythonista's documentation explicitly says subprocess/multiprocessing launch fails under iOS sandboxing and scripts run in the app process. Pyto documentation likewise describes its interpreter running in the app process.

Implications:
- A native iOS embedded interpreter is a practical local runner for user-approved code, but it is not a separate OS process sandbox for hostile code.
- A Stop button can be a useful product control, but PocketCode must verify what it actually interrupts and what state remains. Do not infer process isolation, hard memory/CPU limits, or a guaranteed cleanup boundary from a UI stop control.
- iOS app sandboxing protects app containers from other apps and the OS; it does not turn arbitrary code running inside PocketCode's own process into a separate hostile-code security domain.
- For genuinely untrusted code, continue researching a separately supervised remote Linux/VM or user-owned PC boundary. Do not silently upgrade a same-process interpreter into that role.
- Local execution has lifecycle limitations when apps are backgrounded/suspended. Foreground-run receipts must not imply guaranteed background completion.

## 3. What the frozen task actually tests

The frozen task is intentionally narrow: standard-library CSV input `items.csv`, `main.py`, and output `summary.json`. It tests:
- importing two related files without filename/path confusion;
- choosing the correct working directory;
- capturing a real run result and exact output bytes;
- exposing the artifact to the user;
- carrying a truthful report into an AI correction step.

It does **not** prove:
- hostile-code containment;
- CPU/memory/disk quotas;
- long-running task reliability;
- broad third-party package compatibility;
- background execution guarantees;
- cross-app AI integration;
- a product advantage over established iOS Python apps.

A basic successful CSV-to-JSON run is therefore necessary but not sufficient. The benchmark should score the full task lifecycle, not only whether `summary.json` exists.

## 4. Recommended PocketCode product boundary

### Build / own
- Task packet schema and immutable run/attempt identity.
- File manifest with path, size, encoding where known, and SHA-256.
- Explicit working-directory and entrypoint binding.
- User-visible authorization and execution-location choice.
- Host-captured lifecycle and output evidence; no trusting program-generated claims for runner state.
- Artifact inventory, byte hashes, export and retention semantics.
- Separate execution outcome, job disposition, publication state, cleanup state and artifact-release state.
- Durable report/checkpoint and no-rerun recovery after publication/handoff failure.
- Provider-neutral AI repair packet, user-mediated copy/share, patch preview/approval and new attempt lineage.
- Acceptance/evidence oracle and platform adapters.

### Reuse / adapt / interoperate
- Existing local Python runtimes where a user has them and explicitly selects them.
- OS-native file import/export and share sheet, using explicit user actions.
- Existing editor/terminal/notebook apps as baselines or external execution targets, if an explicit handoff adapter can capture enough provenance to label the result honestly.
- Remote user-owned PC or isolated Linux service as a separate execution adapter, with its own security gate and evidence source.

### Do not build first
- A new general-purpose Python editor, REPL, package manager, notebook environment or debugger.
- A generic AI chat interface that merely pastes code into a provider.
- A cloud runner that needs paid usage or a new account.
- A claim of hostile-code isolation based only on an embedded interpreter, browser worker or stop button.

## 5. Benchmark redesign: compare complete workflows

The same frozen source/input/result fixture should be used unchanged across candidate paths. Capture actual user-observable steps and host-verifiable evidence separately.

| Dimension | Required observation |
|---|---|
| Import | Can user import both `main.py` and `items.csv` as one project without manual path surgery? Are exact bytes/hashes preserved? |
| Configure | Can entrypoint, working directory and any arguments be stated unambiguously? |
| Run | Does it execute offline? Is actual runtime/version identified? Does `input()` work if required? |
| Stop/failure | Can a stuck run be stopped? What evidence proves interruption? What is unknown after app suspension/crash? |
| Output | Are stdout/stderr separately captured? Is exit status available? Can the exact `summary.json` bytes be read/exported and hashed? |
| Receipt | Does the tool produce a machine-readable or copyable run record bound to exact inputs, runtime, attempt and output hashes? |
| AI repair | Can the exact failure evidence be copied/shared without manually reconstructing context? Does it avoid clipboard polling/overlays? |
| Correction | Can user inspect a proposed diff, approve it, rerun, and preserve old/new run lineage? |
| Recovery | If app closes or report handoff fails after successful execution, can the exact existing result be recovered without rerun? |
| Privacy/cost | Is execution local/offline? Does the workflow require an account, provider, subscription or network? |

Score each cell as **verified**, **advertised but unverified**, **not available**, or **unknown**. Do not infer "not available" merely because a feature is not mentioned in marketing material.

### Candidate set for the first controlled comparison

1. **a-Shell** — best first $0 local-terminal control; App Store listing explicitly advertises offline Python and file editing.
2. **One native IDE** — Python Code Editor & IDE if available on the owner's Belgian storefront, otherwise Pyto's free tier. Do not assume the broad new IDE's marketing claims work until verified.
3. **Coilbook** — include if its App Store listing is available on the target storefront and the owner is willing to test it. Its first-party documentation describes a very close standard-library task workflow.
4. **PocketCode prototype** — compare the task-aligned receipt/report design, not the current simulated sample. It must be labelled simulated until an actual runner is connected and evidence is captured.

Carnets and Pythonista can be secondary controls if notebook or share-sheet workflows matter. Avoid installing every competitor; two strong baselines are enough for the first pass.

## 6. Product differentiation hypothesis to test

PocketCode's defensible advantage should be:

> **"A task can be run wherever it is safe and practical, and its exact inputs, execution facts, outputs, recovery state and AI correction history remain portable and trustworthy."**

This is stronger than "Python on your phone" and aligns with the wider RevDev/PocketCode convergence direction:
- provider-neutral task packets;
- bounded multipass work;
- stable lifecycle/result semantics;
- provenance and artifact integrity;
- publication/recovery separate from execution;
- compact checkpoints and explicit continuation.

It is still a hypothesis. Existing apps may already provide some or all of these pieces; hands-on evidence is required before claiming a gap.

## 7. Next decisions and gates

1. Keep execution runtime/provider selection OPEN.
2. Keep Pyodide rejected as a hostile-code sandbox; it is not the default local execution choice.
3. Do not implement a new embedded interpreter or IDE until the benchmark shows a meaningful unmet workflow need.
4. First compare a-Shell plus one current native IDE against the task-aligned receipt design. User/device availability and explicit authorization are prerequisites; no installs or runs were performed here.
5. If PocketCode cannot show a measurable improvement in trustworthy receipts, no-rerun recovery, and low-friction AI correction, pivot toward a provider-neutral workflow/receipt layer that interoperates with existing runners rather than competing as an IDE.
6. Keep Android research separate. Do not assume iOS interpreter/process restrictions transfer unchanged to Android.
7. Preserve LOOP-01..14, CASE-01..16 and P8U/P0-D as separate acceptance suites. This document changes no canonical ID or expected string.

## 8. Public references

- [a-Shell App Store listing](https://apps.apple.com/us/app/a-shell/id1473805438)
- [Carnets App Store listing](https://apps.apple.com/us/app/carnets-jupyter/id1450994949)
- [Carnets privacy policy](https://github.com/holzschu/Carnets/blob/master/privacy_policy.md)
- [Pyto App Store listing](https://apps.apple.com/us/app/pyto-ide/id1436650069)
- [Pyto external-file documentation](https://pyto.readthedocs.io/en/latest/external.html)
- [Pythonista 3 App Store listing](https://apps.apple.com/us/app/pythonista-3/id1085978097)
- [Pythonista iOS FAQ](https://omz-software.com/pythonista/docs-3.4/py3/ios/faq.html)
- [Coilbook product page](https://levan2002.github.io/coilbook/)
- [Coilbook help / file workflow](https://levan2002.github.io/coilbook/help.html)
- [Coilbook privacy policy](https://levan2002.github.io/coilbook/privacy.html)
- [Python Code Editor & IDE App Store AU listing](https://apps.apple.com/au/app/python-code-editor-ide/id6795116281)
- [Python Code Editor & IDE App Store US listing / privacy information](https://apps.apple.com/us/app/python-code-editor-ide/id6795116281)
- [Official Python documentation: using Python on iOS](https://docs.python.org/3/using/ios.html)
- [Apple Platform Security: runtime process security](https://support.apple.com/en-au/guide/security/sec15bfe098e/web)

**Final status:** public research strongly invalidates "local iPhone Python runner" as a unique value proposition. PocketCode's differentiator must be measured at the evidence, recovery and AI-correction workflow layer. No app was installed or executed; no product comparison was empirically completed.
