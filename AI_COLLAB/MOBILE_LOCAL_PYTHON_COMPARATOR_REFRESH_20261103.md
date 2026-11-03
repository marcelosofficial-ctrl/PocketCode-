# Mobile local-Python comparator refresh — iOS and Android

**Date:** 2026-11-03  
**Status:** Public-source desk research only. No app installed, no account created, no task run, no device test, and no product implementation performed.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Authority:** Research supplement to `PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md`. Does not change canonical LOOP/CASE acceptance, select a runtime, or authorize installs/tests.

## 1. Executive verdict

The local-mobile Python landscape is stronger than the current comparison table's shortlist suggests. This document supplements `AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md` (blob `81d155e4d0ccdacc9122e05e23db01d5dd5c3024`), which already covers Pyto, Pythonista, Coilbook and Python Code Editor & IDE in greater iOS depth. This refresh adds Android's direct local-Python IDE baseline and consolidates current iOS local alternatives. There are mature local Python tools on both iOS and Android:

- iOS: Pyodios, Carnets, and a-Shell.
- Android: Pydroid 3, with Termux as a command-line/power-user comparison path.

The fixed CSV-to-JSON task is simple enough that these existing apps can plausibly perform it without a hosted provider. Therefore "run a Python script on a phone" is not a defensible PocketCode differentiator.

**Product decision recommendation:** keep local execution as one possible adapter/path, but focus PocketCode's differentiation on the trustworthy execution workflow around the code: stable run/attempt identity, authoritative lifecycle evidence, honest timeout/cancellation/unknown states, exact input/output identity, artifact integrity, cleanup/recovery evidence, and a compact report that materially improves cross-assistant correction. These are target capabilities and hypotheses, not implemented or validated PocketCode features.

Do not build a second general-purpose Python IDE or notebook environment unless the fixed-task comparison demonstrates a concrete unmet need that existing tools cannot satisfy.

## 2. Current public-source comparator facts

These are vendor/maintainer descriptions, not independent verification of app behavior or security.

| Platform | Candidate | Documented strengths | Material caveats / evidence limits |
|---|---|---|---|
| iOS | Pyodios 1.1 | Local Python via Pyodide 314.0.5 / CPython 3.14.2; editor, notebooks, REPL, files, package manager; imports/exports through iOS Files/share sheet; offline after runtime/package initialization | Requires iOS/iPadOS 26+; approximately 300 MB Python memory budget; first initialization 5–15 seconds; fresh Python session on app launch; app-specific 120-second UI timeout does not stop executing code, requiring session restart/reopen to recover. Uses WebAssembly/Pyodide, so it is not evidence of hostile-code isolation. Android port is planned with no release date. |
| iOS | Carnets | Free standalone Jupyter app; embedded local Python interpreter; works offline; common scientific packages preinstalled; can share notebooks and open notebooks/directories via iOS Files | Notebook-centric, not a complete developer-ops workflow. Additional package installation is limited to pure-Python packages in the standard app; compiled package support differs by edition. No source evidence reviewed here establishes a durable run-bound evidence receipt or hostile-code sandbox. |
| iOS | a-Shell | Free local Unix terminal; Python, JavaScript, C/C++, shell utilities, file transfer, SSH and Git-oriented workflow; runs locally/offline | Terminal-first and more power-user oriented. Broad shell/network tools are capabilities, not proof of a security boundary for hostile scripts. |
| Android | Pydroid 3 | Offline Python interpreter; graphical editor, terminal, debugger, package manager and custom repository for selected scientific packages; Google Play listing reports 10M+ downloads and Python 3.13.13 update on 2026-09-12 | Google Play lists ads and in-app purchases; some editor features are Premium-only. Android package/native-library compatibility varies. No source evidence reviewed here establishes durable run-bound attestations or hostile-code containment. |
| Android | Termux | Power-user terminal path; Python and Linux-like tooling are available through its package ecosystem; suitable control for Git/SSH/CLI workflows | Setup and command-line knowledge are higher-friction than a focused mobile workflow. A terminal environment is not automatically an OS-level hostile-code sandbox. |

### Primary sources

- Pyodios official site: https://pyodios.caffeinatedmath.com/
- Pyodios official FAQ: https://pyodios.caffeinatedmath.com/faq
- Pyodios files/import/export guide: https://pyodios.caffeinatedmath.com/guide/files
- Pyodios project/workspace guide: https://pyodios.caffeinatedmath.com/guide/projects
- Pyodios App Store listing: https://apps.apple.com/us/app/pyodios/id6762922366
- Carnets App Store listing: https://apps.apple.com/us/app/carnets-jupyter/id1450994949
- Carnets source and documentation: https://github.com/holzschu/Carnets
- Carnets privacy policy: https://github.com/holzschu/Carnets/blob/master/privacy_policy.md
- a-Shell App Store listing: https://apps.apple.com/us/app/a-shell/id1473805438
- Pydroid 3 official site: https://pydroid.app/
- Pydroid 3 Google Play listing: https://play.google.com/store/apps/details?id=ru.iiec.pydroid3
- Python's Android platform guide: https://docs.python.org/3/using/android.html

## 3. What this changes in PocketCode's product strategy

### 3.1 Do not compete on interpreter/editor breadth

A basic editor, Python interpreter, console, syntax highlighting, package installer, local file browser, or offline execution is already available from established apps. Rebuilding those features would consume effort without establishing product-market differentiation.

A thin editor or explicit paste/import surface may still be necessary to deliver PocketCode's workflow. It should remain deliberately narrow and task-focused.

### 3.2 Compete on evidence quality and workflow continuity

The stronger candidate value proposition is:

> Turn a phone-executed task into a run-bound, evidence-preserving result that another AI can reliably diagnose and continue from, without confusing script claims, process outcome, lifecycle state, artifact state, or uncertainty.

This proposition must be falsified against existing app output and ordinary copy/paste. Do not assume a native app cannot provide adequate logs or that PocketCode's proposed receipt is automatically better.

The receipt should preserve separate dimensions:
- task/source identity and exact input digests;
- run ID, attempt ID and logical operation identity;
- execution location and runtime/version;
- trusted lifecycle observations and their authenticated producer/provenance;
- process exit code and the source/meaning of that code;
- stdout/stderr capture state, bounds and truncation;
- output artifact names, byte sizes, digests and read-back status;
- cleanup/termination evidence;
- artifact availability/release authorization;
- retry/recovery history and conflicting/late observations;
- derived verdict/disposition with explicit uncertainty.

A formatter displaying `Evidence source: runner` is not enough. The evidence ingress must establish the source, bind observations to the exact run/attempt, preserve raw events and handle contradictory/late terminal events before a verdict is projected. See the separate report-verdict provenance audit on the RevDev continuity branch; its source review is pinned to the PocketCode execution-boundary branch and must not be silently copied between branches.

### 3.3 Distinguish trusted local execution from hostile-code containment

These products demonstrate that local execution can be convenient and inexpensive. They do not establish that arbitrary hostile code is safely contained. In particular:
- Pyodios uses Pyodide/WebAssembly; the separate pinned Pyodide 314.0.7 audit found stock Pyodide is not approved as PocketCode's hostile-code security boundary.
- A terminal/IDE running locally is not automatically a disposable sandbox with enforceable egress, resource quotas, process-tree termination and cleanup.
- An app's own output is not independent proof of what happened outside its process.
- A UI timeout is not evidence that execution stopped.

Keep user-trusted local convenience execution and arbitrary-untrusted-code execution as separate product/security modes. Do not let a successful fixed-task demonstration upgrade the security claim.

## 4. Revised fixed-task comparison protocol

Use the exact frozen `main.py` and `items.csv` bytes and the same success and malformed-header cases. Do not regenerate the task or change the input between conditions.

### Suggested comparator set

1. iOS local IDE: Pyodios first; Carnets as a second iOS local-Python control if time permits.
2. iOS terminal: a-Shell as a power-user control, not a novice baseline.
3. Android local IDE: Pydroid 3 first.
4. Android terminal: Termux as a power-user control.
5. Browser-local Pyodide: only if a browser/PWA path remains strategically relevant; test iOS file import/export, page backgrounding, reload and truthful timeout recovery.
6. Manual copy/paste to an AI assistant: no PocketCode execution; baseline for report comprehension and correction.
7. PocketCode prototype: simulated UI only; do not award execution, correctness, lifecycle, or artifact points.

Do not install or run these apps as part of desk research. Any hands-on test requires separate owner authorization and target-device availability.

### Measures

For every condition, record:
- exact source/input identity and whether bytes match the fixture;
- setup/import friction and time to first run;
- success-case output bytes and parsed values;
- malformed-input exit/status and partial output behavior;
- actual stdout/stderr availability and capture completeness;
- how a timeout/cancel is represented and whether execution is confirmed stopped;
- whether output artifacts are discoverable/exportable and byte-identical;
- what run identity/history survives app restart;
- what evidence is independently attributable versus merely copied from program output;
- whether another AI can diagnose/continue correctly from the handoff;
- total user steps and elapsed time.

Keep the execution-path comparison separate from the paired AI correction experiment. For the latter, use identical source, input and observed facts in both conditions: (a) ordinary native-app console/output copy and (b) PocketCode's proposed receipt. Score correction accuracy, unsupported claims, context needed, and user effort. A simulated receipt can test format comprehension only, not actual run evidence or product advantage.

## 5. Recommended next bounded sequence

1. Treat this comparator refresh as desk research only.
2. Keep the canonical task and task-aligned simulated receipt spec unchanged.
3. Obtain the focused Claude architecture review and Gemini security/spec review of the proposed evidence receipt, particularly the trust boundary between local runner, caller, and report projection.
4. Before any implementation, decide which first-proof execution path is actually being evaluated: trusted-user local convenience or arbitrary untrusted code. Do not blend their security claims.
5. When owner-authorized device access exists, run the same frozen task on one iOS and one Android local comparator, with a manual copy/paste control. Do not test every app before the first comparison answers the core hypothesis.
6. Only continue PocketCode implementation if the experiment demonstrates a measurable advantage beyond existing mobile Python apps and ordinary AI copy/paste.

## 6. Evidence and non-actions

This is public-source desk research and product-strategy analysis only. App capabilities are descriptions from their maintainers/store listings, not independent runtime or security validation. No app was installed, no source/input was executed, no provider/account/billing/workload was used, no device/browser/accessibility test was run, and no source/test/canonical acceptance/owner decision was changed. No GitHub Actions, PR, host, queue, install, merge, or deployment operation occurred.
