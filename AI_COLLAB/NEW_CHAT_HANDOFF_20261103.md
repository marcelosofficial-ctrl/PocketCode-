# PRIMARY NEW-CHAT HANDOFF — PocketCode + RevDev
**Prepared:** 2026-11-03  
**Purpose:** Complete transfer package. This document is the current read-first handoff and supersedes the 2026-11-01 bootstrap's live-state snapshot, while preserving that older document as historical context.  
**Repository:** `marcelosofficial-ctrl/PocketCode-`  
**Research branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Latest verified branch head at preparation:** `c0514044707b6a440bed2f7a7f758bdbf6500d14`  
**Main/base:** `555840d8d83342513d9cd353d4d1522d46a5c82d`  
**Latest verified comparison:** 546 ahead / 0 behind.

---

## 0. Immediate instructions to the new chat

Continue the existing PocketCode + RevDev programme. This is not a new project, a greenfield rewrite, or an invitation to repeat discovery. Read this handoff first, then use the linked source documents only where needed. Preserve existing owner decisions, contracts, product goals and security boundaries.

The user is phone-first and has no reliable PC/local access for approximately four months, planned from 2026-10-28 through 2027-02-28. Current PC/source checkout/runtime/installed binary/local queue/local AI state is **UNKNOWN** until the owner returns and supplies fresh evidence. Historical paths and hashes are not current-state proof.

The owner expects substantial work per pass and wants you to make sensible executive decisions about research/documentation priorities. Do not ask for permission for harmless read-only research or continuity documentation on the named research branch. Ask only when a genuinely owner-only decision/action is required, and keep that request short at the end.

**Standing restrictions:**
- $0 budget. Do not create accounts, start provider workloads, consume paid services, spend money or assume a hosted free tier.
- Do not push/deploy/install/restart, change source/tests, trigger GitHub Actions, merge/close/retarget PRs, change queues/runtime/host state, handle secrets, elevate privileges or weaken security boundaries without explicit authorization.
- Documentation-only continuity updates on the named isolated research branch are authorized.
- PR #2 and PR #3 are protected: leave both untouched and unmerged.
- No provider, runtime, framework or dependency is selected for PocketCode.
- No PC access means no claims about local tests, builds, installations, binaries, runtime, queues or Windows product state.
- Do not claim to have contacted Claude or Gemini. The owner manually forwards prompts and reports.
- Use ordinary chat, not Work mode.
- No automatic clipboard polling or system-wide overlays. Explicit paste-to-context and an in-app accessory symbol bar remain the intended interaction constraints.

## 1. Product direction and goals

### PocketCode

PocketCode is a phone-first iOS/Android product for helping people build, execute, inspect and improve software from a phone, including when they do not have a PC. It is not merely a report/receipt generator and not merely a generic multi-agent cockpit.

Core loop:
1. Provide code and explicit inputs.
2. Run it in an execution environment whose actual security/resource boundary is understood.
3. Inspect truthful result, files, errors and lifecycle evidence.
4. Produce a bounded, useful, copyable report that preserves evidence and uncertainty.
5. Carry that report to any AI assistant for correction.
6. Rerun and compare.

The product should reduce the number of repetitive AI "done" exchanges and help users complete safe technical tasks that otherwise require a computer. A broader Agentic Orchestration Control Plane direction is a hypothesis, not permission to abandon the narrow first workflow.

First proof remains narrow: a bounded coding task, an honest run result, and a useful correction loop. Do not expand MVP into arbitrary shell, autonomous LLM loops, arbitrary runtime images, guaranteed network, persistent multi-user workspace or hosted platform without evidence and owner approval.

Principles:
- Phone-first UX, not a desktop IDE squeezed onto a phone.
- Provider-neutral task orchestration.
- Clear distinction between user intent, policy approval, authorization, dispatch, execution, result, cleanup and artifact release.
- Truthful lifecycle/result/evidence and recovery; unknown is not pass or fail.
- Untrusted code must not inherit app credentials, broad browser APIs, host files or ambient secrets.
- Real resource limits, termination, cleanup, provenance and artifact integrity must be enforced and evidenced, not merely asserted.
- Explicit user-controlled context sharing; no clipboard polling.
- No system-wide overlay; an in-app accessory symbol bar is acceptable.
- $0 default budget.
- The name collision with Catrobat's “Pocket Code” remains an open branding issue. Do not rename silently.

### RevDev relationship

RevDev is a separate Windows desktop mission/developer-ops automation product. PocketCode is its phone-first counterpart in a coherent larger PC-and-phone programme. This convergence of product direction does **not** mean merging repositories, runtimes, roadmaps, clients, adapters, acceptance suites, release gates or security boundaries. Shared conceptual foundations may include provider-neutral workflows, task packets, bounded multi-pass work, lifecycle/result semantics, evidence provenance and compact checkpoints. Any shared implementation or protocol needs a separate justified decision.

RevDev's original goals remain active: Projects-first developer-ops UI; a single “done” starts substantial bounded batches of scripts/operations plus verification/repair; per-operation green/red progress; adaptive batch size; terminal pass/fail sound; return-to-AI continuation; durable state/evidence; reliable publication/recovery and grouped interaction cycles. Do not let recovery/audit work erase the original product goals.

## 2. Three-AI roles and collaboration

Latest owner-approved roles:
- **Claude:** lead developer and engineering/architecture reviewer for RelayRef; also independent research contributor.
- **Gemini:** co-developer and independent security/spec auditor.
- **ChatGPT:** continuity holder, evidence reconciler, acceptance/test architect, conformance reviewer and eventual deployment coordinator when PC access returns.

Older role drafts exist. The above is current.

The owner manually forwards prompts and reports. Do not claim direct communication with the other AIs. Use all three when independent perspectives add value. Assign one primary task owner, ask reviewers focused questions, and reconcile evidence before changing anything.

Claude's 2026-11-02 research reports were supplied by the owner. They are useful but explicitly thin: primarily web search/page fetch, no pinned commit SHAs for most claims, only one LICENSE file opened in the follow-up, and no complete source-tree/acceptance review. Treat claims as candidate evidence until verified against exact source. Gemini's earlier open-source research review and later security/spec work are also valuable but not automatically authoritative. Preserve PocketCode goals and contracts over any AI's proposed architecture.

## 3. Current verified GitHub state

Repository: `marcelosofficial-ctrl/PocketCode-`  
Research branch: `pocketcode-ai-workflow-director-research-2026-10-28`  
Latest head: `c0514044707b6a440bed2f7a7f758bdbf6500d14`  
Main/base: `555840d8d83342513d9cd353d4d1522d46a5c82d`  
Compare: **546 ahead / 0 behind** at the last verification on 2026-11-03.

Latest key document blobs:
- `AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md`: `ae0c5d5a4b4e0c7edae39c53fc9118fa70aee493`
- `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`: `5041cafde16fbd07a87c87f93ee5d9caf6a0b8a5`
- `AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md`: `edafc4eb0b9815d2f23bea8326ea98449d411b56`
- `PROJECT_STATUS.md` before this new handoff update: `56602a5274e963c17b70d6220eb8d201379193dd`
- `AI_COLLAB/NEW_CHAT_BOOTSTRAP_20261101.md`: `0660aadf8660b3b0650cbcfcb3404725b5217508` (historical/bootstrap context; read this handoff for current state)
- `AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md`: `9da8c89ddfea1cd9626d0831845efb1e6e780480` (historical long addendum)

PRs:
- **PR #2:** open, draft, unmerged; head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- **PR #3:** open, draft, unmerged; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- Both base `main`; neither modified in current work. Re-fetch before consequential work.

The research branch is large (546 commits ahead) and is not automatically mergeable. Commit count is not quality evidence. Do not merge or rebase as a cleanup action.

## 4. Work completed immediately before this handoff

### 4.1 Linux strict-service containment audit

The source-level review of Happy Agent's Linux strict service at pinned commit `fb9f68ff10333068b87436bd1d531d6d353f5c93` found useful patterns:
- separate cgroup per service;
- cgroup v2 `memory.max`, swap disabled, `memory.oom.group=1`, `pids.max`;
- workload placed in cgroup before app command;
- empty private root, selected read-only input mounts and private scratch;
- clean explicit environment rather than inheriting supervisor variables;
- separate egress process/bridge;
- process identity, pidfd/PDEATHSIG, startup markers, cgroup-empty reconciliation and conservative recovery.

Further adversarial review found significant gaps:
- no demonstrated trusted absolute wall-clock deadline;
- no hard CPU quota;
- no demonstrated disk quota;
- selected inputs are live read-only mounts, not immutable snapshots;
- special files/FIFOs and scratch/input overlap need stronger treatment;
- egress-on IP/L7 policy needs further adversarial validation;
- parent-death race in egress child needs attention;
- this is a service model, not yet a bounded one-shot job runner.
- Linux strict service needs Linux 5.12+, user namespaces and admin-delegated cgroup v2 memory/process controllers; it is not Windows/macOS support.

Happy Agent Windows adapter is **not acceptable as-is** for hostile/untrusted code:
- broad root read access plus explicit deny paths means it is not an allowlist-only read boundary;
- parent environment variables are copied through to child execution; unit tests explicitly retain variables such as AWS keys/private keys;
- no demonstrated hard memory/CPU limits.
- This is a source-path finding, not a live runtime test.

Decision: retain Happy Agent Linux strict-service as the strongest inspected Linux reference, not as a PocketCode dependency/provider/selected architecture. Do not use the Windows adapter as-is. Full detail and mapping to LOOP/CASE is in Section 11 of `RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md`. No upstream tests or PocketCode adaptation were run.

### 4.2 Browser/Pyodide cross-origin design

A research topology is documented:
authenticated app origin → sandboxed cross-origin iframe on a separate static-only execution origin → dedicated module worker with pinned Pyodide. The execution origin must have no session cookies, credentials, private APIs, server functions, user data or shared parent-domain cookie scope. Inputs cross via bounded run-scoped MessageChannel; outputs are untrusted and bounded. CSP must be applied to the worker response as well as frame. CORS is not an egress security boundary.

This remains a proposal. It does not prove hostile-code containment, hard CPU/memory limits, trusted timeout or iOS compatibility.

### 4.3 Critical Pyodide 314.0.7 source findings

Exact Pyodide 314.0.7 source was inspected. This is more reliable than the original general claim that an empty `jsglobals` object might hide all browser capabilities.

Verified findings:
1. `PyodideConfig.jsglobals` controls the Python `js` module, not every JS capability.
2. Pyodide also automatically registers `pyodide_js`, backed by its public JS API object.
3. That object exposes `FS`, `_module`, `_api` and other API methods. The filesystem documents persistent backends including IDBFS.
4. `pyodide.code.run_js()` delegates to JavaScript `eval` through the `js` module.
5. The Python import hook has an unregister mechanism, but removing an import registration does not automatically remove already imported module references from `sys.modules`.
6. `pyodide._package_loader` imports a JS-backed `loadedPackages` proxy during initialization. Clearing `sys.modules` alone does not prove that this cached JS reference is gone.
7. Pyodide's webloop and HTTP helpers rely on `pyodide_js` and its APIs. Removing it may disable asyncio/network helper functionality; this may be acceptable for a synchronous, fixed standard-library task, but must be tested.
8. Pyodide 314.0.7's own restrictive-CSP test is marked expected-fail on Safari because Safari does not support `wasm-unsafe-eval`. Do not silently replace it with weaker `unsafe-eval`.

Pinned source references:
- [api.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/api.ts)
- [pyodide.ts](https://github.com/pyodide/pyodide/blob/314.0.7/src/js/pyodide.ts)
- [Python import hook](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/_pyodide/_importhook.py)
- [Python package init](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/__init__.py)
- [package loader](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/_package_loader.py)
- [webloop](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/webloop.py)
- [HTTP fetch](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/http/_pyfetch.py)
- [run_js](https://github.com/pyodide/pyodide/blob/314.0.7/src/py/pyodide/code.py)
- [Safari CSP test](https://github.com/pyodide/pyodide/blob/314.0.7/src/tests/test_pyodide.py)
- [CSP fixture](https://github.com/pyodide/pyodide/blob/314.0.7/src/templates/test_csp.html)

Possible trusted-bootstrap attenuation experiment, not proven:
- Initialize Pyodide with a frozen null-prototype empty `jsglobals`.
- Keep the Pyodide API object and host-only FS/stream/message-port handles in a trusted JS closure, never exposed to Python.
- Before user code, unregister `pyodide_js`, remove cached `pyodide_js.*` imports, and audit/attenuate `pyodide._package_loader.loadedPackages`.
- Prove the Python-visible `pyodide.ffi` surface cannot re-register a privileged module or recover the original JS API/worker global.
- Prove `pyodide.code.run_js()` cannot reach eval, even if target Safari needs a weaker CSP to load WebAssembly.
- Test that fixed synchronous standard-library execution, file I/O, bounded output and exception reporting still work.
- Re-audit all object references on every Pyodide update.

This is a security-sensitive prototype hypothesis. If it requires a maintained Pyodide fork or cannot demonstrate that hostile Python cannot recover privileged objects, reject it for hostile-code execution. A browser worker may still be useful as a limited local convenience for trusted/small tasks, with honest limitations. Do not call it a verified sandbox.

### 4.4 GitHub updates made in this pass

Documentation-only updates on the existing research branch:
- Browser boundary desk review expanded and sourced.
- Threat cases BR-05/BR-06/BR-13 added.
- WP-09 added to the implementation readiness backlog, separate from hosted/provider WP-08.
- Project status updated with the findings and commit/blob pointers.
- Latest branch head verified as `c0514044707b6a440bed2f7a7f758bdbf6500d14`, 546 ahead/0 behind.
- PR #2 and #3 re-fetched and still open/draft/unmerged at unchanged heads.

No product source, tests, runtime, provider, account, budget, canonical acceptance, PR, workflow, deployment or local machine state was changed.

## 5. PocketCode acceptance and decision rules

Canonical acceptance IDs remain:
- `LOOP-01` through `LOOP-14`
- `CASE-01` through `CASE-16`

Do not add/remap/merge canonical IDs without an explicit, source-grounded crosswalk. Supplementary namespaces such as PC-LC, PC-AD, PC-DB, PC-RT, PC-EXT, RES, TDN, TPM, PBR/PF, DR and AR remain separate.

Owner-open semantic decisions:
- **D-01:** timeout semantics. Working default: trusted enforced timeout → `INCOMPLETE / timed_out`, with limit cause separately recorded. Do not silently convert to FAIL.
- **D-02:** provider failure without child exit → `INCOMPLETE`, execution outcome `UNKNOWN`; `PROVIDER_ERROR` only if cause confirmed.
- **D-03:** only evidence explicitly required by each case gates PASS. Optional diagnostics are not universal gates. EMPTY, UNAVAILABLE, PARTIAL, RUNTIME_LIMIT and DISPLAY_TRUNCATED are distinct.
- **D-04:** scoped event identity, exact replay vs conflict, coordinator ordering remain proposed.
- **D-05..D-08:** applied-policy binding, durable idempotency/recovery, release-time authorization/integrity and append-only crash-safe report history remain proposed boundary requirements.

Important D-01/D-03 nuance: a “complete result” in the execution contract must mean a complete trustworthy terminal-result record plus all evidence required by the particular case, not necessarily complete stdout/stderr/optional diagnostic streams.

Other key semantics:
- A confirmed trusted nonzero child exit is program FAIL even if cleanup is UNKNOWN/FAILED; report cleanup separately and block artifact release where appropriate.
- A zero exit is not PASS if mandatory evidence or safety gates fail.
- Parsed instruction ≠ policy approved ≠ authorized ≠ dispatched ≠ executed.
- Program result, job disposition, cleanup/teardown and artifact-release eligibility are separate.
- Unknown is not false, pass, fail or safe.
- Execution success does not automatically authorize artifact release.

Key docs:
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`
- `PRODUCT/EXECUTION_CONTRACT.md` (main blob historically `3861e51ae4f9e45a263b677402f26c41b240959d`; research branch proposed version is not automatically canonical)
- `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`
- `AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md`
- `AI_COLLAB/PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md`

Staged gates:
- G0 owner semantics OPEN.
- G1 boundary/cost BLOCKED.
- G2 pure helpers NOT STARTED/NOT RUN.
- G3 durable reservation/recovery BLOCKED.
- G4 evidence/report history BLOCKED.
- G5 artifact publication/release BLOCKED.
- G6 phone workflow NOT RUN.
- G7 canonical acceptance NOT RUN.

LOOP-12: untrusted code runs only in a disposable, constrained environment; egress denied by default and resource limits enforced outside code. No runtime/provider selected; NOT RUN.
CASE-15: untrusted script attempts outbound network access or reads environment secrets; network blocked by enforced policy and no service credentials present in execution environment.

## 6. Fixed-task experiment and paired comparison

Canonical worksheet: `AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`.

A canonical `main.py` fixture was frozen to remove comparability ambiguity. It reads `items.csv`, validates header/rows, uses Decimal, writes `summary.json`, and has explicit malformed-input behavior. Every path must use identical source or disclose wrapper/adaptation.

Fixture SHA-256: `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`, 1,939 bytes.

Isolated sanity check only:
- Python 3.13.5, Linux x86_64, isolated ChatGPT Python environment.
- Valid fixture: exit 0, expected JSON.
- Malformed header: exit 2, missing-`unit_price` error, no summary file.
- An unrelated spreadsheet-runtime warmup traceback polluted startup stderr.
- This was not a PocketCode product-path run.

**Product path comparison remains NOT RUN.** No iPhone app, Safari/PWA, Pyodide, remote PC, hosted provider or production runner test. No security, performance, termination, resource, cleanup or report-handoff conclusion.

Paired report-correction protocol is designed, source frozen, sanity check recorded, but product-path execution and AI correction experiment remain NOT RUN. It compares:
- A fresh chat given raw source/input/native observations only.
- A separate fresh chat given the same material represented by the proposed PocketCode report.
- Same assistant/model/mode/tools/task/evidence; no shared context or cross-exposure.
- Score diagnosis, evidence honesty, correction quality, verified success/failure behavior, user effort/time.
- Pair is CONFOUNDED if the report cannot represent a material fact/uncertainty in native evidence.
- At least 3 comparable pairs if free usage permits; smaller samples exploratory.
- Freeze evidence/prompt/rubric before either chat; randomize order where practical; no inventing a harder failure fixture after results.

Report differentiator is UNVALIDATED.

## 7. Existing open-source research and candidate decisions

No runtime/provider/framework/dependency is selected. Do not repeat broad catalogues.

Gemini's candidate catalogue was adjudicated:
- CodeMirror 6: leading browser editor candidate; test actual iOS/Android keyboard, IME, selection, paste, scroll, undo/redo. Old GitHub repos archived/moved to Forgejo; npm remains active.
- Pyodide: leading narrow browser-local Python candidate only; not a security boundary.
- wasmsh: later research only; constrained WASM shell, not OS shell; no shell in MVP.
- Aider repo-map: concept/pattern only; avoid importing Aider-coupled module.
- LangGraph: defer; checkpointing does not guarantee external exactly-once side effects.
- Piston hosted: reference only; public API not generally free after 2026-02-15.
- tsnet/AsyncSSH: not approved.
- Watchdog: pattern only; file events are hints, not durable reconciliation.
- FlaUI: conditional RevDev option only if a concrete UI automation gap appears.
- OpenHands ACI: archived; do not adopt.
- Judge0 GPL-3.0 is not an automatic blanket source-disclosure trigger; component-specific legal assessment if needed.
- gVisor/Firecracker/nsjail: server-side research only, not phone client features or easy drop-ins.
- Happy Agent Linux strict-service: strongest inspected Linux containment reference, not selected provider/dependency.
- Happy Agent Windows adapter: unsuitable as-is due broad read and inherited environment findings.

Claude's 2026-11-02 report suggested Pyodide worker, isolate taxonomy, in-toto/DSSE evidence, CodeMirror, isomorphic-git, ACP, Happy, Windows Job Objects and sandbox-runtime. It did not inspect source trees comprehensively or pin most commit SHAs. Recommendations are not decisions.

Additional Claude follow-up findings:
- Pyodide 314.0.7 version at report time.
- iOS/WebKit behavior largely unknown; no physical-device testing.
- WebKit bug 289686 fixed in WebKit main but stable iOS shipment mapping not proven.
- Job Objects provide process/resource containment, not filesystem/network isolation.
- sandbox-runtime Windows alpha has limitations including broad profile read grants, environment concerns, no CPU/memory quotas and machine-wide setup.
- in-toto Statement requires DSSE/signing/identity/replay/custom predicate for PocketCode's needs; test-result predicate lacks UNKNOWN. A signature does not prove execution truth.
- ACP v2 is draft and permission prompts are advisory, not security.
- Happy's E2E claims were not independently audited in Claude's report.

Current research direction is to reconcile these claims only where they affect the narrow execution-boundary decision. No more broad OSS catalogue work.

## 8. RevDev and RelayRef continuity

Repository: `marcelosofficial-ctrl/DevRelay-Missions`  
Branch: `review/revdev-adaptive-ai-workshare-2026-10-27`

Important RevDev docs:
- `resume/revdev/MASTER_CHAT_HANDOFF_2026-10-29.md`
- `PC_FREE_ROADMAP_AND_CHAT_START_HERE_2026-10-28.md`
- `CURRENT_GOALS.md`
- `THREE_AI_NEXT_ASSIGNMENTS_2026-10-28.md`
- `AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md`
- `NEW_CHAT_HANDOFF_2026-10-29_P8U_EVIDENCE_ORACLE.md`
- `NEW_CHAT_HANDOFF_2026-10-29_REVDEV_POCKETCODE_CONVERGENCE.md`
- `REVDEV_POCKETCODE_CROSS_PROJECT_ALIGNMENT_2026-10-29.md`
- semantic crosswalk draft.

Historical PC paths only, current state UNKNOWN:
- Source: `C:\Users\celo\source\repos\RevDev`
- Runtime: `C:\Users\celo\DevRelay\automation\`
- Installed binary: `%LOCALAPPDATA%\RevDev\app\RevDev.exe`
- Earlier installed binary/runtime/queue evidence must be freshly collected after PC access returns.

RelayRef v0.9 evidence:
- `RevDev_RelayRef_v0_9_2026-10-26.py`
- SHA-256 `a97db43551b4e91243721b3026802486a9f2bce0f63a63a34cf87217c23ca55d`
- 2,779 lines.
- Python 3.12.3 Linux self-test: 293/293, skipped 0.
- Python reference only; C#/Windows/product NOT_RUN/BLOCKED.
- Prior v0.6: 137/137.
- Semantics: parsed ≠ policy-approved ≠ authorized; confirmation + guard required; `RDV-END` not `RDV-REPLY-END`; `HOSTED_DENY`; broad reads NEED.
- Historical earlier PASS 177/177 at `REVDEV-R149-P8Y3B1-PURE-WATCHER-TRANSFORM` is not current PC proof.

RevDev acceptance crosswalk work:
- Preserve original acceptance ID meanings; Gemini previously remapped incorrectly.
- Claude proposal: B-03 authentication denied → TRANS-01 (not BOOT-03); BOOT-03 bootstrap conflict; VALID-03 missing manifest; V-03 missing required evidence file; B-07 roots; SAFE-01 add.
- SAFE-01/B-07 prototype on unchanged v0.9: SAFE-01 61 cases = 32 PASS / 29 FAIL (danger cases classified VALID); B-07 5 = 4 PASS / 1 FAIL (missing vs inaccessible roots indistinguishable); scratch patch 292/293 expected pin change `script_t5_delete_c_root` adds `BANNED_OPERATION:recursive-delete`.
- Do not infer integration from a proposal.

P8U focus: publisher/orphan-result recovery and grouped interaction-cycle reliability. Local mission result must be recovered/published exactly without rerun, overwriting newer results, duplicate consume/terminal events, losing steps or closing the wrong cycle. Await/reconcile Claude and Gemini evidence; do not claim Windows/product tests without PC.

RevDev ↔ PocketCode convergence:
- one coherent PC-and-phone product/program vision;
- separate repos, roadmaps, clients, adapters, acceptance suites and release gates;
- no shared code/runtime/security-boundary change without separate decision;
- conceptual common ground: provider-neutral AI workflows, task packets, bounded multi-pass work, lifecycle/result semantics, evidence provenance and compact checkpoints.
- Canonical suites remain separate: AEC-001–012, AWC-001–018, P8U-01–12, P0-D 1–10.

## 9. Current priorities and next passes

Do not continue the broad candidate survey. Prioritize the following sequence:

### Pass 1 — Finish Pyodide attenuation feasibility at source level
- Inspect exact 314.0.7 registration/unregistration lifecycle and every Python-visible JS proxy.
- Establish whether the package-loader cached proxy can be safely replaced/removed without breaking the fixed task.
- Enumerate `pyodide.ffi` capabilities and whether user code can re-register a privileged JS module.
- Audit other cached handles, module imports and wrapper objects, not just names in `sys.modules`.
- Decide whether this is realistically maintainable without a fork. If not, reject it for hostile code.
- No runtime/device test is possible on phone-only context unless owner provides an authorized suitable device/test path; mark NOT RUN.

### Pass 2 — Complete execution-boundary comparison
Compare only:
1. browser-local Pyodide candidate (with limitations and security gates);
2. true isolated Linux service reference (not selected, gaps listed);
3. user-owned remote PC (future option, no PC access now);
4. manual copy/paste fallback.
Use existing LOOP/CASE criteria and fixed task. Keep hosted execution at $0 and no provider selected. Explicitly separate local convenience from hostile-code isolation.

### Pass 3 — Map the execution/report evidence contract
Make one concise matrix for user intent → policy → authorization → dispatch → execution → result → cleanup → artifact release → report. Include unknown states, timeout semantics, required vs optional evidence, idempotency and recovery. Preserve D-01..D-08 owner-open status and existing canonical IDs.

### Pass 4 — Reconcile Claude/Gemini only where it affects decisions
Owner supplied Claude's 2026-11-02 report and follow-up. Gemini's earlier review is in repo. Do not ask for another broad report. Ask the owner for Gemini's new targeted verdict only if it would materially resolve a named conflict. Use exact pinned upstream sources.

### Pass 5 — Keep continuity tidy and PC-return ready
Update the existing checkpoint/status/handoff only when materially useful. Avoid another sprawling master document. No code implementation, provider test, workflow, merge or deployment.

## 10. Evidence discipline

Use these labels:
- VERIFIED_PRIMARY_SOURCE
- SECONDARY_SOURCE
- INFERENCE
- ASSUMPTION
- UNVERIFIED
- NEEDS_LIVE_TEST
- NEEDS_OWNER_APPROVAL

Execution/test status:
- PASS
- FAIL
- BLOCKED
- INCONCLUSIVE
- NOT RUN

Never upgrade a source review into a runtime test. Keep actual source hashes/commit tags. Use read-back verification for continuity writes. Report what changed, what it establishes, what it does not establish, next bounded task and any owner action.

## 11. Copy/paste prompt for the new ChatGPT chat

Paste everything in the block below as the first message. It is intentionally self-contained and directs the next chat to continue rather than restart.

---

You are continuing my existing PocketCode + RevDev project. This is a continuation, not a new project. Treat the attached/current GitHub handoff as authoritative for the latest state:

`marcelosofficial-ctrl/PocketCode-/AI_COLLAB/NEW_CHAT_HANDOFF_20261103.md`

Research branch:
`pocketcode-ai-workflow-director-research-2026-10-28`

Latest verified branch head at handoff:
`c0514044707b6a440bed2f7a7f758bdbf6500d14`

**First action:** read this handoff completely, then verify the current GitHub branch head, compare against main, fetch PROJECT_STATUS.md, the fixed-task worksheet, the browser desk review, the resource containment review, the implementation readiness backlog, the current checkpoint/continuity hub, and PR #2/#3. The 2026-11-03 handoff supersedes older branch-count snapshots. Do not assume the head/count/PR state is unchanged.

**My goals:** PocketCode is a phone-first iOS/Android coding product that helps me provide code and inputs, execute in an appropriate environment, inspect real results/files/errors, produce truthful evidence-rich reports, send those reports to any AI for correction, and rerun. It must solve real phone-first technical tasks, not just generate reports or become a generic multi-agent cockpit. RevDev is its separate Windows desktop counterpart in a coherent PC-and-phone product direction. Keep repos, runtimes, clients, adapters, acceptance suites, security boundaries and release gates separate. Shared concepts do not authorize shared implementation.

**Three-AI roles:** Claude is lead developer/engineering reviewer for RelayRef; Gemini is co-developer and independent security/spec auditor; ChatGPT is continuity holder, evidence reconciler, acceptance/test architect and eventual deployment coordinator when PC access returns. I manually forward prompts/reports. You cannot message the other AIs directly. Preserve their useful findings, but owner goals/contracts override AI recommendations.

**Constraints:** I am phone-only until around 2027-02-28. Treat PC/source/runtime/installed binary/queue state as UNKNOWN. Budget is $0. Do not create accounts, start provider workloads, spend money, install, deploy, restart, elevate, handle secrets, run GitHub Actions, change source/tests, alter queues/host state, merge, close or modify PR #2/#3, or weaken security boundaries without explicit authorization. Documentation-only continuity work on the existing research branch is authorized. No provider/runtime/framework is selected. No background clipboard polling or system overlays. Do not claim unrun tests.

**Current research conclusion:** Happy Agent Linux strict-service is the strongest inspected Linux containment reference, not an adopted dependency/provider. It has useful private filesystem, explicit environment, cgroup, process-reconciliation and egress-broker patterns, but lacks demonstrated trusted absolute deadline, CPU quota and disk quota, and has input/special-file/egress/parent-death gaps. Happy Agent Windows adapter is unsuitable as-is because of broad root read access and inherited environment credentials. See Section 11 of RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md.

**Critical Pyodide finding:** Exact 314.0.7 source shows an empty jsglobals only restricts the Python js module. Pyodide also registers pyodide_js, exposing FS, _module, _api and persistent IDBFS. pyodide.code.run_js uses JavaScript eval. Removing pyodide_js from the import hook does not clear cached sys.modules references, and pyodide._package_loader holds a JS-backed loadedPackages proxy. Webloop and HTTP helpers depend on pyodide_js. Pyodide's restrictive CSP test is expected-fail on Safari due wasm-unsafe-eval support. There is a possible trusted-bootstrap attenuation experiment, but it is unproven and may be impractical without a fork. Do not call Pyodide a secure sandbox. Continue source-level feasibility, then stop if no maintainable isolation route exists. No Pyodide runtime/device tests were run.

**Current product acceptance:** canonical LOOP-01..14 and CASE-01..16 unchanged. D-01..D-08 remain owner-open/proposed as described in the handoff. Keep timeout as INCOMPLETE/timed_out by working default, provider error without child exit as INCOMPLETE/UNKNOWN unless confirmed, optional diagnostics distinct from case-required evidence, and program result/cleanup/artifact release separate. Never remap IDs.

**Fixed task:** canonical main.py fixture SHA-256 70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7. Isolated Python sanity check passed valid/malformed fixture logic, but product-path comparison remains NOT RUN. Paired raw-evidence vs report correction experiment is designed/frozen but NOT RUN; differentiator UNVALIDATED.

**RevDev:** Continue existing RelayRef and P8U recovery/audit work using exact GitHub evidence. RelayRef v0.9 Python reference self-test was 293/293, Python-only; C#/Windows/product NOT RUN/BLOCKED. Preserve all acceptance ID meanings. P8U is about orphan-result publication/recovery and grouped interaction-cycle correctness. PC state UNKNOWN. RevDev and PocketCode acceptance suites remain separate.

**Your work style:** Be proactive and do substantial work per pass. Plan the next few passes, execute read-only/source research and useful documentation updates, and make executive decisions that reduce uncertainty while preserving constraints. Do not repeat broad OSS catalogues or ask me to repeat known context. Before each substantial pass, identify the decision it reduces; reuse existing docs; verify exact sources; distinguish source inspection from tests; update GitHub continuity with exact SHAs/read-back. If owner-only action is required, ask briefly at the end.

**Next tasks in order:**
1. Finish Pyodide 314.0.7 source-level attenuation feasibility: import-hook unregister semantics, pyodide.ffi re-registration, cached package-loader proxy, remaining Python-visible JS objects, and whether fixed synchronous tasks still work. Decide whether the approach is maintainable without a fork. No runtime test claim.
2. Complete a concise execution-boundary comparison: browser Pyodide (limited local convenience unless proven otherwise), isolated Linux service reference, user-owned remote PC (future, unavailable now), and manual copy/paste. Map against LOOP/CASE.
3. Produce one lifecycle/evidence matrix covering intent, policy, authorization, dispatch, execution, result, cleanup, artifact release and report, preserving unknown states and owner-open decisions.
4. Reconcile Claude/Gemini reports only where they change those decisions. No new broad research survey.
5. Keep the checkpoint and PC-return plan tidy. No implementation/provider selection/deployment.

Start by verifying the current GitHub state and then continue with task 1. Do not stop after summarizing this prompt. Do the work.

---

End of handoff.


## 2026-11-03 continuation addendum — first three research tasks completed

The next chat should read the companion audit:
[PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md](PYODIDE_ATTENUATION_EXECUTION_BOUNDARY_AND_LIFECYCLE_MATRIX_20261103.md).

### Pyodide 314.0.7 decision

The pinned source audit is complete. Do not continue the trusted-bootstrap attenuation experiment as a no-fork hostile-code sandbox candidate.

Verified source details:
- unregister_js_module removes a JS import-finder mapping but does not revoke already imported modules or clear sys.modules.
- pyodide.ffi exposes register_js_module and unregister_js_module.
- pyodide._package_loader imports and retains pyodide_js.loadedPackages.
- pyodide.webloop imports and retains pyodide_js._api.scheduleCallback.
- pyodide._state.save_state() explicitly says there is no general way to track all module global state.
- JsProxy exposes a JavaScript object's constructor; to_js creates JS object proxies. A constructor/code-generation route is CSP-dependent and was not executed.
- Pyodide 314.0.7's restrictive-CSP test is expected-fail on Safari because Safari does not support wasm-unsafe-eval.

Decision: reject as a maintainable hostile-code sandbox without a fork or recurring private patch/audit. Retain Pyodide only as a possible trusted/small-task convenience comparator. The fixed standard-library CSV-to-JSON task does not inherently require JS, pyodide_js, network, package installation or async execution, but its operation after any attenuation remains untested. No runtime, exploit, Safari, PWA or device test was performed.

### Execution-boundary comparison completed

The companion audit compares browser Pyodide, the pinned Happy Agent Linux strict-service reference, a future user-owned remote PC, and manual copy/paste. It maps all four against canonical LOOP-01..14 and CASE-01..16.

Key decisions:
- Linux strict-service remains the strongest inspected containment reference, not an adopted provider/dependency; CASE-04 is blocked by missing internal absolute deadline, and CPU quota/storage/output/lifecycle gaps remain.
- A remote PC is a future option only. Current PC, checkout, runtime, binary, credentials, network and queue remain UNKNOWN. Remote transport is not a sandbox.
- Manual copy/paste is the $0 first workflow baseline, but not PocketCode execution evidence.
- No runtime/provider/framework was selected.

### Lifecycle/evidence matrix completed

The companion audit defines nine independent stages: user intent, policy decision/application, authorization, reservation/dispatch, execution, program result/job disposition, cleanup, artifact integrity/release, and report creation/publication. It preserves UNKNOWN and the separation between execution outcome, job disposition, cleanup, artifact release and report state. D-01..D-08 remain owner-open/proposed; LOOP/CASE IDs and meanings are unchanged.

### Current remaining priorities

1. Continue focused product-value validation of the first useful manual phone workflow and report/correction loop. The fixed-task product-path comparison remains NOT RUN; paired AI correction experiment remains designed but NOT RUN; differentiator UNVALIDATED.
2. Keep PC-return checklist current. Do not assume any PC state until fresh owner evidence is supplied.
3. Continue RevDev P8U work separately, preserving its acceptance meanings and all local-state UNKNOWN conditions.
4. Do not restart broad provider/runtime surveys. Reopen execution selection only with concrete, evidence-backed $0-capable boundary candidates.
5. Keep PR #2/#3 open, draft, untouched and unmerged. No product source/tests, Actions, provider workloads, spend, account, runtime, queue, install, deploy, merge or host state was changed by this continuation.


### PC-return checklist refresh and branch snapshot

- Refreshed [PC_RETURN_CHECKLIST_DRAFT_20261028.md](PC_RETURN_CHECKLIST_DRAFT_20261028.md), blob SHA 6bfa59becb1992bb02ae46500673c85f3aa858a7. The addendum preserves the existing first-session order, explicitly rejects spending the first PC session on the no-fork Pyodide hostile-sandbox experiment, and adds fresh-state, remote-host-boundary and PR-protection reminders.
- The branch snapshot immediately before this checklist/handoff refresh was head 528702bf720f3d5659bcba918195bb030497f920, 553 ahead / 0 behind main 555840d8d83342513d9cd353d4d1522d46a5c82d. The current final head and comparison are recorded in PROJECT_STATUS.md after the final read-back.
- The original handoff header's c051404 head is the historical preparation snapshot. It was superseded first by the owner's supplied 4368a78 head, then by the documentation-only continuation commits. Always re-fetch the live ref rather than treating a handoff snapshot as current.
