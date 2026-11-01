# Open-Source Candidate Deep Dive — CodeMirror, Pyodide, wasmsh and Aider

**Date:** 2026-11-01  
**Purpose:** Follow-up source-level triage of the four strongest plausible code-reuse candidates from Gemini's report.  
**Status:** Static source inspection only. No build, install, execution, benchmark, device test or dependency adoption.

## 1. Executive result

| Candidate | Pinned upstream evidence | Reuse surface | Decision |
|---|---|---|---|
| CodeMirror 6 | GitHub migration marker `codemirror/view` commit `fbff59ba004d80d8c914f64c42586387b08706ac`; current npm package `@codemirror/view@6.43.15` (MIT), published 12 days before this review; current upstream Forgejo source could not be fetched here (403). | Use maintained npm packages, not copy source from archived GitHub snapshot. | **KEEP as leading browser editor candidate.** Must pin package version/integrity and test target devices. |
| Pyodide | Repository commit `950e0de49536778f2d7a0efc825e932d812be9e7`; FAQ blob `8cf61babf27af837592d7e17b3c919bdaea795ea`; filesystem docs blob `35198e99260c5a7c3e09dd30277ce1028ec39065`. | Use Pyodide as a browser Python runtime candidate, not as a generic OS sandbox. | **KEEP for fixed-task comparison.** Not selected until iPhone behavior and report evidence are tested. |
| wasmsh | Repository commit `beb3eff548be7beb6dfdda3bf7c2f893f51d9c26`; sandbox docs blob `b5fba0d9407539bdfd93effc37d20cdec97c7862`; supported syntax blob `54805677df2c986d1f1c3d2e15040a6ec7f253d9`; VM blob `6ff6fcbf6faa2af6dec642236271bc2f8f4a916f`; Pyodide package manifest blob `e2b532b95bea582e70ca906896e3941aa7d9e616`. | Separate WASM shell interpreter and VFS; potentially pair with Pyodide. | **INVESTIGATE LATER.** Technically promising but a separate shell/runtime adds scope and host-side obligations. |
| Aider repo map | Repository commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`; `aider/repomap.py` blob `541bba6ef4a5385b8cf032201ec6e3f3e32a6ea6`; requirements blob `cddf41382622a5348e84fb1cb1cd8dfddde6e64c`; Apache-2.0 license blob `d645695673349e3947e8e5ae42332d0ac3164cd7`. | Symbol-level repo map concept, not a clean standalone module. | **PATTERN ONLY.** Do not import Aider's full internal module or provider stack. |

## 2. CodeMirror 6 — a repository migration trap, not abandonment

Gemini points to `github.com/codemirror/CodeMirror`, which resolves to the legacy CodeMirror 5 repository, not the CodeMirror 6 source. The CodeMirror GitHub organization archived its old repositories on 2026-04-15 and moved active development to `https://code.haverbeke.berlin/codemirror/<package>`. The old `codemirror/view` GitHub repository is a forwarding/archive snapshot, not the current development repository.

This is not evidence that CodeMirror 6 is abandoned: npm currently lists `@codemirror/view@6.43.15`, MIT, published 12 days before this review. The official changelog records Android Chrome and iOS virtual-keyboard fixes in the 6.43.x line. The current Forgejo source host returned HTTP 403 to this review environment, so the exact latest source commit was **not** verified.

**Practical reuse direction:**
- Use the published `@codemirror/*` packages and their documented extension model, not a copied source subtree.
- Pin exact package versions and lockfile integrity, not a GitHub commit from the archived mirror.
- Build the editor around the existing mobile accessory symbol bar and explicit file workflow; do not expect the editor package to supply those product features.
- Device tests must cover iOS Safari/WebView and Android Chrome/WebView composition, autocorrect/autocapitalize, selection, paste, indentation, viewport resize, keyboard show/hide, scrolling, undo/redo, and external keyboards.
- Treat the CodeMirror input source as strong prior art, not proof of PocketCode mobile UX acceptance.

## 3. Pyodide — useful for the actual first bounded task, with clear browser constraints

The inspected Pyodide docs confirm:
- Python is CPython compiled to WebAssembly/Emscripten and can run in browser or Node.
- The default Emscripten filesystem is MEMFS and does not survive page reload.
- IDBFS can persist data, but IndexedDB synchronization is asynchronous and must be explicitly invoked.
- Native browser directory mounting through File System Access API is documented as experimental and Chromium-only; Pyodide's FAQ says that API is not supported in Safari.
- Browser code can access Web APIs through the JavaScript bridge. Do not expose secrets, privileged bridge functions, same-origin credentials, or broad application state to untrusted code.
- Pyodide does not support ordinary Python `threading`, `multiprocessing` or `subprocess` process creation in the normal browser build. Compatibility must be checked against the actual target task and package set.

**Practical reuse direction:**
- Keep Pyodide as the leading candidate for the existing standard-library CSV-to-JSON fixed task. That task avoids package installation and tests the real value of phone-local execution.
- Model the input/output workspace explicitly. On iOS, use deliberate import/export or app-owned origin storage; do not promise direct Files-folder mounting.
- Run execution off the UI thread where supported and define how a worker is terminated/replaced. Record that browser termination is a client-controlled local lifecycle, not remote provider evidence.
- Keep the user-visible report truthful about the evidence the browser runtime actually exposes. Do not claim trusted server-side isolation, process-tree kill, durable run history or artifact authorization from Pyodide alone.
- Test memory pressure, reload/interruption, worker failure, output caps, file export and Safari behavior on the actual device before claiming support.

## 4. wasmsh — stronger than a casual shell port, but not a general OS shell

The pinned upstream threat model is unusually explicit. It says the trusted host controls the shell's visible capabilities; the script has no host filesystem access; no network unless host allowlists hostnames; no OS process model (`fork`, `exec`, job control are absent); and native handlers/utilities are statically registered by the host.

The pinned `SUPPORTED.md` explicitly describes a subset of Bash, not 100% compatibility. Background execution syntax can parse, but the browser runtime runs synchronously. The VM source defines explicit step, output-byte, pipe-byte and recursion limits, but each limit value of zero means **unlimited**. The threat model also explicitly warns that a very large step budget combined with memory-heavy code can OOM the WASM module, and that allowlisted network destinations can still create DNS/request-shape exfiltration side channels.

The npm Pyodide package manifest says version 0.9.0, Apache-2.0, Node >=20, with browser-worker and Node entry points. The workspace is Rust 2021 and requires Rust 1.89. This is more than a small JavaScript utility.

**Practical reuse direction:**
- Do not add a shell to MVP merely because it exists.
- If a later product requirement justifies a shell, first make a narrow proof using its browser-worker path with all limits explicitly nonzero and network disabled.
- Inspect every registered command handler and every host bridge; the trust boundary depends on the embedder's registrations, not only the WASM module.
- Verify memory/stack/recursion behavior and ensure the host can terminate a worker independently of cooperative VM budgets.
- Treat allowed-host configuration as a high-risk capability requiring exact policy, DNS behavior review and no ambient credentials.
- Do not describe it as running arbitrary native commands or background processes. It is a constrained shell interpreter/runtime with a modeled command surface.

## 5. Aider repo map — adopt the idea, not the internal module

The pinned `aider/repomap.py` is not a small standalone Tree-sitter helper. It imports `diskcache`, `grep_ast`, Pygments, tqdm, Tree-sitter and Aider-specific modules (`aider.dump`, `aider.special`, `aider.waiting`). Its class expects a model object with token-counting behavior and an Aider I/O abstraction. It also owns caching and repo-map selection logic tied to Aider's prompt workflow.

Aider itself is Apache-2.0, but its complete dependency set is much larger than the repo-map concept. The code is tightly integrated with its application internals.

**Practical reuse direction:**
- Preserve the product idea: generate a bounded repository map containing important files, symbols, signatures and relationships rather than dumping whole files into an AI context.
- If later needed, build or select a small provider-neutral utility around Tree-sitter/grep-ast with a stable JSON/text output, strict file exclusions, symlink/path safety, size/token budgets and explicit parse failures.
- Do not import `aider/repomap.py` directly unless a future spike proves the dependency and maintenance cost is lower than a narrow implementation.
- This is not needed for the first execution-loop proof. Keep it behind a later codebase-context requirement.

## 6. Candidate order after source inspection

1. **CodeMirror 6:** browser editor candidate; use maintained package releases, verify device UX.
2. **Pyodide:** browser-local Python candidate; run the fixed-task comparison before selecting.
3. **wasmsh:** future optional shell candidate; defer until there is a real demand for shell semantics beyond Python/files.
4. **Aider repo-map:** optional codebase-context pattern; defer until large-repository context becomes a demonstrated problem.

This order is not an adoption sequence. The first two still compete in the fixed-task and device workflow; wasmsh and repo-map solve later/optional problems.

## 7. Follow-up required from Claude

Ask Claude to independently verify:
- CodeMirror's GitHub-to-Forgejo migration, active npm package/source revision, licence and exact mobile input support;
- Pyodide worker termination, browser API exposure, iOS storage/import/export and package compatibility;
- wasmsh command-surface completeness, step-budget implementation, zero/unlimited defaults, memory exhaustion, host bridge and allowlist threat model;
- whether Aider repo-map can be cleanly extracted without pulling in its internal model/I/O/cache dependencies;
- exact current licenses, transitive dependencies, release cadence and platform support.

No candidate has been adopted or tested. Preserve disagreements as OPEN until exact source evidence resolves them.
