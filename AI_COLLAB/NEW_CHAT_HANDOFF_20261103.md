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


## 2026-11-03 cross-project branch-pointer reconciliation

A newer RevDev continuity handoff, DevRelay-Missions/resume/revdev/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_2026-11-03.md, references a different PocketCode branch: pocketcode-execution-boundary-crosswalk-2026-11-01 with a handoff-reported 602-ahead snapshot. The owner-designated branch for this continuation remains pocketcode-ai-workflow-director-research-2026-10-28.

Live comparison of the owner-designated branch during this continuation: **556 ahead / 0 behind** main 555840d8d83342513d9cd353d4d1522d46a5c82d. PR #2 and #3 remain OPEN / DRAFT / UNMERGED with unchanged heads eb8b7ea83cb0e8fe1880351276c485b761431791 and 0ddcc0bc97bac5d446aefedf3d71f99411bd841d.

Do not silently switch branches, merge histories, copy branch-specific files, or treat their blob SHAs and status snapshots as interchangeable. Continue on the branch explicitly designated by the owner unless the owner clarifies otherwise. The 602-ahead figure belongs to the other handoff's earlier snapshot and was not reverified here.


## 2026-11-03 static mobile prototype audit

Read-only audit: MOBILE_RUNNER_PROTOTYPE_STATIC_UX_EVIDENCE_AUDIT_20261103.md, blob 4e5679dccd041bdae55a05b22e51a0d5bd668f58. Reviewed source prototypes/mobile-runner/index.html, blob e2c4ece041be95ce9a73bc60ff354702b21c33c2.

Key findings:
1. The prototype's sales CSV -> summary.txt example is not the frozen CSV-to-JSON comparison task. Align the example with the frozen fixture if this is the task-comparison demo, or label it as a separate illustrative flow.
2. The copied report currently lacks separate stdout/stderr capture state and explicit artifact state. The failure example hides the file card but the copied report does not explicitly state artifact absence.
3. The CSV panel is fixed sample text, not a user file-import flow.
4. Timeout/cancellation controls and state distinctions are absent. Do not imply the demo can stop code.
5. Tab/panel ARIA relationships and keyboard navigation are incomplete; the existing checker only covers source heuristics.
6. Clipboard behavior remains browser-dependent and unverified.

Good existing safeguards to preserve: visible simulated-execution banner; example buttons do not claim to run; both copied artifacts state no code was executed; debugging prompt includes editor code, sample CSV and report; README warns against putting private data in the public demo.

Recommended next design order: canonical task alignment; truthful compact receipt with execution/disposition/streams/artifact states; distinguish sample from actual input; reserve timeout/cancellation UI; complete accessibility and later test on actual browsers. This is a design audit only. No source/tests, browser/device interaction, clipboard test, accessibility audit, execution, installation, Actions, deployment, provider workload or spend occurred. Prototype remains simulated; product-path comparison and differentiator remain NOT RUN / UNVALIDATED.


## 2026-11-03 latest live branch reconciliation

A fresh GitHub comparison of the owner-designated PocketCode research branch \`pocketcode-ai-workflow-director-research-2026-10-28\` reports **561 ahead / 0 behind** main, merge base \`555840d8d83342513d9cd353d4d1522d46a5c82d\`. This supersedes the earlier 555/556-ahead snapshots recorded above. It is a divergence count, not a merge-readiness assessment.

PR #2 remains OPEN / DRAFT / UNMERGED at unchanged head \`eb8b7ea83cb0e8fe1880351276c485b761431791\`; PR #3 remains OPEN / DRAFT / UNMERGED at unchanged head \`0ddcc0bc97bac5d446aefedf3d71f99411bd841d\`. Both were re-fetched and left untouched.

RevDev's separate research branch currently compares 463 ahead / 0 behind its own main, merge base \`058f9025319d12e76195659c715ccb4afce133b8\`. Do not conflate repository branch counts or copy branch-specific blob references.

No PR/source/test/Actions/provider/account/workload/spend/host/queue/runtime/install/deployment/merge changes occurred. The frozen task product-path comparison and paired AI correction experiment remain NOT RUN; the differentiator remains UNVALIDATED.


## 2026-11-03 branch-count snapshot supersession

The 561-ahead PocketCode figure in the preceding addendum is superseded. The latest comparison immediately before this documentation update reported this owner-designated branch at **563 ahead / 0 behind** main, merge base \`555840d8d83342513d9cd353d4d1522d46a5c82d\`. This is a historical snapshot taken before the present continuity commits, not a live count after them. Re-fetch the branch comparison before making any decision. PR #2/#3 remain open, draft, unmerged, at their unchanged protected heads.


## 2026-11-03 mobile prototype next-pass design

Read [MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md](MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md), blob \`2b2b05bd0efbd339cdef2dff14cd404bc25f168b\`, before any future mobile-prototype source work.

The spec resolves the next design pass: align the example to the frozen \`main.py\` + \`items.csv\` CSV-to-JSON task; show the expected \`summary.json\`; include the malformed-header case; and present one complete simulated receipt that distinguishes expected fixture values from actual observations. In particular, remove fabricated sample durations, do not imply a runtime was selected, distinguish sample stdout/stderr expectations from collected streams, and explicitly show artifact/cleanup/release states.

No fake import, run, cancellation, or termination controls should be added. A simulated UI cannot prove LOOP-01 file intake, LOOP-03/04 execution, LOOP-10 file creation, LOOP-12 isolation, or real clipboard/device behavior. Existing LOOP-01..14 and CASE-01..16 remain unchanged.

No prototype source or tests were changed. No browser/device tests, file import, clipboard test, execution, installation, provider workload, Actions, account, spend, host/queue operation, PR mutation, merge or deployment occurred. The fixed-task product-path comparison and paired AI correction experiment remain NOT RUN; report differentiator remains UNVALIDATED.


---

## 12. 2026-11-03 follow-up — Pyodide 314.0.7 capability audit and execution-path decision

**New source-backed research artifact:** [`AI_COLLAB/PYODIDE_314_0_7_CAPABILITY_ATTENUATION_AUDIT_20261103.md`](PYODIDE_314_0_7_CAPABILITY_ATTENUATION_AUDIT_20261103.md), blob `d799cb4adcc08bfe3548921ae021ab58feae3f20`.

Executive decision:
- Stock Pyodide 314.0.7 is **not approved as the security boundary for arbitrary hostile/untrusted Python**.
- Do not prioritize a trusted-bootstrap import-scrub shim for MVP. The exact source shows `jsglobals` only controls the `js` module, while bootstrap separately registers `pyodide_js` exposing `FS`, `_module`, and `_api`.
- Unregistering a JS module does not remove an already-imported module from `sys.modules`; the package loader also retains a JS-backed `loadedPackages` reference, and optional webloop/http modules can cache more JS references. The source review does not prove that these references alone recover the full API, so treat them as residual capability paths requiring adversarial tests, not as a demonstrated exploit.
- Pyodide's `run_js()` is an eval wrapper through `js`; removing that module should block this particular route only if all JS references are removed and CSP remains strict. Never use `unsafe-eval` as a Safari workaround.
- Upstream's CSP test fixture is not a PocketCode no-egress policy. It uses `default-src http: 'wasm-unsafe-eval'`; the pinned test marks Safari expected-fail for `wasm-unsafe-eval`.
- A disposable dedicated worker is useful for responsiveness and can be terminated by a live parent, but WebKit documents iOS background tab suspension and timer throttling. A browser timer is not a durable wall-clock deadline while the app is suspended. Worker termination does not prove per-run memory/disk quotas or persistent-storage cleanup.

Execution-path recommendation:
- Browser-local Pyodide: keep only as a possible user-approved convenience path for code the user already trusts; isolated origin, disposable worker, no credentials, deny-by-default CSP/no egress, bounded inputs/outputs, and no hostile-code or hard-quota claim. Not selected.
- Isolated Linux/VM: continue as the required research direction for arbitrary untrusted code, with independent supervisor/workload boundary, network denial, memory/swap/CPU/process/disk limits, hard deadline, process-tree reconciliation, and artifact integrity. Happy Agent Linux strict service remains a reference, not ready implementation.
- User-owned remote PC: future RevDev/PocketCode bridge candidate, but only with a disposable execution boundary; ordinary host-account execution is not safe for hostile code. PC state remains UNKNOWN and unavailable in current phone-only period.
- Manual copy/paste: transparent fallback and control condition for report-value research, never a PocketCode execution.

No canonical LOOP/CASE IDs or meanings changed. No code/tests/browser/device tests were run. Fixed-task product comparison remains NOT RUN; runtime/provider selection remains NONE; budget remains $0.

### Latest live GitHub reconciliation (2026-11-03 follow-up)

- PocketCode branch head: `78b0c15273ff0f66072dbb5d58a9a0f6c0c904cf`; compare `main...research`: **569 ahead / 0 behind**, merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- RevDev branch head: `675902cced5bf92a63ab73bb865834014c0e2b59`; compare `main...research`: **471 ahead / 0 behind**, merge base `058f9025319d12e76195659c715ccb4afce133b8`.
- PocketCode PR #2 and #3 remain OPEN / DRAFT / UNMERGED at heads `eb8b7ea83cb0e8fe1880351276c485b761431791` and `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- RevDev PR #1 remains OPEN / DRAFT / UNMERGED at head `59f88dc0bd884872cf379c8aeb6272c9a70c71ce`.
- No PR was modified, no Actions run was triggered, and no source/test/runtime/host/queue change occurred.



## Final branch chronology correction — 2026-11-03

Earlier same-day counts of 569 ahead / 0 behind for PocketCode and 471 ahead / 0 behind for RevDev were captured before the final Pyodide audit and P8U documentation commits. A fresh comparison immediately before this handoff correction found:
- PocketCode owner-designated branch: head `2d6e6c478dfa22a1e6efeeaf1e672ff2d1871be6`, **572 ahead / 0 behind**, merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- RevDev research branch: head `01e0858bfd8733070b7c0f78b0f62bafe1fd2649`, **477 ahead / 0 behind**, merge base `058f9025319d12e76195659c715ccb4afce133b8`.

These are pre-correction snapshots. The present handoff update advances the PocketCode branch again, so re-fetch exact refs before the next consequential action. PR #2/#3 and RevDev PR #1 remain OPEN / DRAFT / UNMERGED; their heads were unchanged in the latest metadata read.


## 2026-11-03 iOS runner competitive baseline and product differentiation decision

Added [`AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md`](AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md). Public-source research checked a-Shell, Carnets, Pyto, Pythonista 3, Coilbook and Python Code Editor & IDE, plus official Python iOS and Apple sandbox documentation.

**Executive decision:** do not build a generic iPhone Python IDE/interpreter as PocketCode's differentiator. The market already advertises free/low-cost local offline Python, project/file import, notebooks, consoles, stop controls and debugging. Especially relevant:
- a-Shell's App Store listing advertises free offline local Python and Unix tools.
- Carnets advertises free local/offline Jupyter with file/directory support and sharing.
- Pyto and Pythonista advertise embedded local Python IDEs and file/automation workflows.
- Coilbook's first-party pages claim CPython 3.14, free unlimited runs, Files-app project folders, input/console and Stop. Its App Store storefront presence was not independently confirmed in this pass.
- Python Code Editor & IDE's App Store listing advertises local offline Python, debugger, pip, pytest, project import and ZIP export. The listing is recent and public ratings are sparse; all such feature claims remain unverified until hands-on use.

Official Python iOS documentation says Python must be embedded in an iOS app, not used as a system-wide Python executable. Pythonista/Pyto documentation describes same-process interpreter operation and iOS subprocess restrictions. Therefore a native embedded interpreter is useful for trusted local work, not a hostile-code OS sandbox. A Stop button does not prove process isolation or hard quotas.

PocketCode's differentiation should be the provider-neutral **task/evidence/recovery/AI-correction layer**:
1. immutable task/run packet binding exact source and input hashes;
2. explicit entrypoint/working directory and user authorization;
3. host-observed lifecycle/output evidence, exit/outcome, artifact hashes and cleanup uncertainty;
4. durable report/run history and recovery without rerunning a completed task;
5. portable AI debugging packet, explicit user-mediated handoff, patch preview/approval and attempt lineage.

The frozen CSV-to-JSON task remains a workflow benchmark, not proof of runtime advantage or sandbox security. First controlled comparison should use a-Shell plus one current native IDE (Python Code Editor & IDE if available in the owner's Belgian storefront, otherwise Pyto free tier), optionally Coilbook if store availability is confirmed. Do not install/run anything without explicit owner/device authorization. Mark capabilities advertised-but-unverified, unknown or verified; do not treat silence in marketing as absence.

No apps were installed, no tasks run, and no canonical LOOP/CASE meanings changed. Runtime/provider selection remains NONE; budget remains $0; fixed-task product comparison remains NOT RUN. Full rationale, source links, benchmark dimensions and go/no-go criteria are in the competitive baseline.


## 13. Mobile local-Python comparator refresh — 2026-11-03

Read `AI_COLLAB/MOBILE_LOCAL_PYTHON_COMPARATOR_REFRESH_20261103.md`, blob `f41e0706fe5590a5f8607514283030392cfe2fc9`.

Public-source desk research adds iOS comparators Pyodios, Carnets and a-Shell, plus Android Pydroid 3 and Termux. The fixed CSV-to-JSON task is not differentiated by basic on-device Python execution, editing, terminal access or file import/export alone. Do not build a second general-purpose mobile Python IDE without evidence of an unmet need.

The stronger product hypothesis is the workflow around execution: exact run/attempt/input identity, authoritative lifecycle evidence, truthful timeout/cancellation/unknown states, artifact integrity, cleanup/recovery provenance and a portable receipt that measurably improves cross-assistant correction. These remain target capabilities, not implemented or validated PocketCode features.

The comparator refresh is public-source research only. No app was installed, no task/device/browser test was run, and no runtime was selected. The frozen task product-path comparison and paired AI correction experiment remain NOT RUN. Keep the manual copy/paste control; compare identical source/input/observed facts in every condition. Do not award simulated prototype screens execution or correctness points.

The latest primary handoff remains this AI Workflow Director branch. The separate execution-boundary-crosswalk branch and its OpenHands research remain separate; do not copy or merge artifacts between branches without explicit authorization.


## 14. PocketCode verdict-provenance audit — pinned helper present on both branches

A read-only audit was added to the RevDev continuity branch:
`resume/revdev/CONTINUATION_ADDENDUM_VERDICT_PROVENANCE_BRANCH_GOVERNANCE_2026-11-03.md` (RevDev branch `review/revdev-adaptive-ai-workshare-2026-10-27`, blob `2edabe714653935ca6023047a126bfc2b148271c`).

The exact PocketCode helper/test blobs were first reconciled on the separate `pocketcode-execution-boundary-crosswalk-2026-11-01` branch and were then freshly fetched from this owner-designated AI Workflow Director branch with identical SHAs:
- `scripts/report_contract.py`, blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`
- `scripts/test_report_contract.py`, blob `85109f056009d65a274e9306deb39b68e1fefbd2`

The earlier audit correctly noted that the pure helper accepts caller-supplied data and does not authenticate it, but this is not automatically a defect in the helper: its own docstring says it is a formatter/projection, and the existing `ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` assigns evidence validation to a trusted coordinator. The unresolved issue is that no production ingress/call path has been implemented or proven to enforce that boundary.

The helper also returns FAIL for any integer nonzero exit code before considering lifecycle status, including nonterminal and other statuses. The current tests do not cover `accepted/queued/running/rejected/timed_out/cancelled/infrastructure_failed/unknown + nonzero`. Its test named `test_nonzero_exit_overrides_script_printed_pass` does not supply script output; it exercises `succeeded + nonzero` metadata. Keep script claims, lifecycle observations and natural child-exit versus wrapper/termination codes separate.


## 15. Latest branch comparison snapshot — 2026-11-03

Fresh read-only comparisons against each repository's `main` after the documentation updates:

| Repository / branch | Ahead | Behind | Merge base |
|---|---:|---:|---|
| RevDev `review/revdev-adaptive-ai-workshare-2026-10-27` | 487 | 0 | `058f9025319d12e76195659c715ccb4afce133b8` |
| PocketCode owner-designated `pocketcode-ai-workflow-director-research-2026-10-28` | 581 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |
| PocketCode separate `pocketcode-execution-boundary-crosswalk-2026-11-01` | 605 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |

These are divergence counts, not merge-readiness evidence. The two PocketCode branches remain separate. No branch merge, rebase, PR update, or cross-branch artifact transfer was performed. PR #2/#3 remain protected and untouched; re-fetch exact PR metadata before any consequential PR decision.


## 16. 2026-11-04 report projection and publisher follow-up

New owner-branch audit:
- [Report verdict/provenance projection audit](REPORT_VERDICT_PROVENANCE_PROJECTION_AUDIT_20261104.md), blob `f35dd2b9b310b2587d13d3fd0fb4e729864b4acb`.

It reconciles the pinned helper with the existing adapter-envelope design. The formatter should remain a pure projection. The actual gate is that a trusted coordinator must authenticate and bind evidence before calling it. The audit expands the static precedence truth table and prepares focused Claude/Gemini review questions. No source/test or canonical acceptance change was made; D-01..D-04 remain OPEN; tests NOT RUN.

RevDev also added [P8U-03/P8U-06 maintenance publisher audit](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U03_P8U06_MAINTENANCE_PUBLISHER_RETRY_ACCESS_AUDIT_2026-11-04.md), a static review of the tracked maintenance publisher only. It finds no explicit response-header-aware Retry-After handling and text-based 404 absence classification. This maps to existing P8U-03/P8U-06; live publisher parity remains UNKNOWN. P0 is still release-blocking; P8U/P0-D remain NOT RUN.

No tests, provider workloads, app installs, browser/device checks, Actions, PR changes, host/queue/runtime operations or deployments occurred.


## 17. 2026-11-04 shared semantic crosswalk with RevDev

Read the RevDev-side [identity, result and publication crosswalk](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/REVDEV_POCKETCODE_IDENTITY_RESULT_PUBLICATION_CROSSWALK_2026-11-04.md), blob `4c3b98e039cbaf5bde6cfc1ce1c2e7cd0efbbfbf`.

The shared product goal remains one coherent PC-and-phone programme with separate repositories, roadmaps, clients, adapters, acceptance suites, release gates and security boundaries. The crosswalk recommends aligning reusable invariants only:
- stable attempt identity and exact-content idempotence;
- immutable evidence/history and explicit conflict handling;
- execution outcome separate from publication/report state;
- ambiguous acknowledgement recovery without blind replay;
- mutable current pointers separate from immutable results;
- trusted provenance before report projection.

Important non-equivalences: RevDev Mission ID is not PocketCode job ID; RevDev runId is the closest attempt-level counterpart but not automatically interchangeable with PocketCode attempt_id; GitHub publication is not artifact release/download; RevDev grouped interaction-cycle/audio requirements remain native.

This is a design reconciliation only. No canonical acceptance IDs/expected strings, owner decisions, schemas, source, tests, runtimes, providers, PRs or security boundaries changed.


## 18. Latest cross-project branch comparison snapshot — 2026-11-04

Fresh read-only compare against each repository's `main`, captured before this handoff update:

| Repository / branch | Ahead | Behind | Merge base |
|---|---:|---:|---|
| RevDev `review/revdev-adaptive-ai-workshare-2026-10-27` | 498 | 0 | `058f9025319d12e76195659c715ccb4afce133b8` |
| PocketCode owner-designated `pocketcode-ai-workflow-director-research-2026-10-28` | 589 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |
| PocketCode separate `pocketcode-execution-boundary-crosswalk-2026-11-01` | 605 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |

These are divergence counts only, not merge-readiness evidence. The owner-designated branch remains `pocketcode-ai-workflow-director-research-2026-10-28`. The OpenHands source-research branch remains distinct and untouched; do not copy or merge its artifacts here.

PR #2/#3 and RevDev PR #1 remain open and untouched. Their review lists were empty in the latest review-list read. No PR action occurred.


## 19. RevDev publisher target-class and retry-trace refinements — 2026-11-04

The RevDev research branch now has:
- [P8U-03/P8U-06 retry/access audit](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U03_P8U06_MAINTENANCE_PUBLISHER_RETRY_ACCESS_AUDIT_2026-11-04.md), latest blob `e2cebf6b3274bc8c2137fb7d59a329928a886349`.
- [Publisher target classes/restart-idempotency audit](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/PUBLISHER_TARGET_CLASSES_AND_RESTART_IDEMPOTENCY_AUDIT_2026-11-04.md), latest blob `7ac2762bb630df0d34bdb7c80c7f164289981f8f`.

The retry audit confirms the maintenance-source success path drops earlier failed PATCH response text when a later attempt succeeds; only the final attempt count remains. The full API status/header/wait/attempt sequence is not durably retained. The GitHub private-resource 404 finding is further qualified: documented 404 causes also include malformed URLs/path parameters and unsupported methods, so a text match cannot establish exact-target absence.

The target-class audit separates immutable by-mission result, mutable latest pointers, timestamped history/evidence, evidence index and mutable handoff. Its restart behavior is conditional on the by-mission preflight: existing path triggers early return and skips history/evidence/handoff; absent path allows a fresh snapshot. This narrows earlier broad statements about every restart regenerating history/evidence.

All these findings are limited to the tracked RevDev maintenance copy. They do not prove installed/live behavior. RevDev P0 remains OPEN/release-blocking, P8U/P0-D NOT RUN, and the recovered P8U mission must never be replayed. No source or tests were changed or run.


## 20. 2026-11-04 latest repository comparison before handoff close

| Repository / branch | Ahead of main | Behind | Merge base |
|---|---:|---:|---|
| RevDev `review/revdev-adaptive-ai-workshare-2026-10-27` | 506 | 0 | `058f9025319d12e76195659c715ccb4afce133b8` |
| PocketCode owner-designated `pocketcode-ai-workflow-director-research-2026-10-28` | 591 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |
| PocketCode separate `pocketcode-execution-boundary-crosswalk-2026-11-01` | 605 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |

These comparisons were fetched immediately before this handoff edit. They are divergence counts, not merge-readiness evidence. Both PocketCode branches remain separate; no transfer/merge was performed. PR #1/#2/#3 remain open and untouched; the review-list calls in this continuation returned no submitted reviews.
