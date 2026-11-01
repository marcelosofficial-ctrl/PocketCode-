# NEW CHAT BOOTSTRAP — PocketCode + RevDev
**Prepared:** 2026-11-01  
**Purpose:** Complete continuation handoff for a new ChatGPT conversation. Read this before doing project work.  
**Authority:** Owner's stated goals and constraints remain authoritative. Research reports from Claude/Gemini are high-value recommendations and evidence, not automatic project decisions.

---

## 0. Immediate instruction to the new chat

Continue the existing PocketCode + RevDev work. Do not restart discovery from zero, do not treat this as a greenfield project, and do not overwrite the product goals or existing contracts because a new AI report recommends a different architecture.

The owner is phone-only for approximately four months from October 2026. They cannot access their PC, source checkout, installed binaries, runtime folders, local queues or local AI environment. Treat all present PC/source/runtime/queue/binary state as **UNKNOWN** until the owner regains PC access and supplies fresh evidence. The user is working from an iPhone and has limited free ChatGPT file intake. Keep work efficient, substantive and documentation/evidence-led.

The user expects you to continue working without asking for permission for every harmless research or documentation step. Ask for user action only when a decision, credential, device test, PC action or other owner-only step is genuinely required. Put any necessary request briefly at the end.

**Do not** merge, deploy, release, publish, trigger GitHub Actions, install software, run provider workloads, create accounts, spend money, invoke paid services, change source/tests, modify PRs, alter host/runtime/queue state, restart services, handle secrets, elevate privileges, or weaken security boundaries without explicit owner authorization. The only standing GitHub write permission relevant here is isolated, documentation-only continuity work on the named research branch. PR #2 and PR #3 are protected and must remain untouched.

Use ordinary ChatGPT chat, not Work mode. GitHub is the continuity store. Do not claim to have messaged Claude or Gemini; the owner manually forwards prompts and reports.

## 1. Project goals and relationship

### PocketCode

Repository: `marcelosofficial-ctrl/PocketCode-`.

PocketCode is intended to be a **phone-first AI coding application** for people who want to create, edit, run, inspect and improve code without needing a desktop computer. It began with a wish to run scripts directly on a phone, then research clarified that the product is better understood as an **Agentic Orchestration Control Plane** rather than a single local code runner.

Potential execution paths under investigation:
- Local phone/browser execution where the runtime and task are suitable.
- Browser/WASM runtimes for carefully bounded tasks.
- User-owned remote PC execution, potentially over a private network such as Tailscale, when the user has a reachable computer.
- Hosted execution only if it is justified, secure, operationally credible and compatible with the owner's $0 budget.
- Manual AI copy/paste as a useful fallback, not as the entire product.

Product principles:
- Phone-first UX, not a desktop IDE squeezed onto a small screen.
- Provider-neutral orchestration and explicit execution-path boundaries.
- Clear distinction between user intent, policy approval, authorization, dispatch, execution, result, cleanup and artifact release.
- Truthful run state, diagnostics, evidence, history and recovery.
- Explicit copy/paste or user action for context sharing. No background clipboard polling.
- No system-wide overlays. An in-app accessory symbol bar is acceptable.
- Untrusted user code must not gain secrets, broad app/browser capabilities or host access by default.
- Resource limits, real termination, cleanup, provenance, artifact integrity and unknown states must be enforced and evidenced, not merely asserted in UI.
- No provider selected. Budget is $0.
- Name collision with Catrobat's “Pocket Code” remains an open product/branding concern. Do not silently rename the project.

The first useful proof should remain narrow: a bounded phone-first coding task, an honest run result and a useful correction loop. Current proposal excludes autonomous LLM loops, arbitrary shell, persistent workspace, multi-user collaboration, arbitrary runtime images and guaranteed network access from the first proof unless an explicit later decision changes scope.

### RevDev

RevDev is a separate Windows desktop mission/automation product. It has mission intake, queues, watchers/workers, project management, structured result files, recovery and an operator UI. It may eventually complement PocketCode in a coherent phone+PC ecosystem, but do not merge the two projects' runtimes, security boundaries, acceptance suites, result contracts or deployment lifecycles without a separately justified architecture decision.

Known historical paths (not evidence of current state):
- Source: `C:\Users\celo\source\repos\RevDev`
- Runtime: `C:\Users\celo\DevRelay\automation\`
- Historical runtime files: `watcher.ps1`, `queue-sync.ps1`, `mission-runner.ps1`, `DevRelay.Automation.psm1`, `launcher.ps1`, `project-manager.ps1`
- Installed binary: `%LOCALAPPDATA%\RevDev\app\RevDev.exe`
- Mission input: `incoming/<project>/*.devrelay.json`
- Exact results: `results/<project>/by-mission/<mission-id>.json`
- `LATEST_RESULT.json` is secondary only, never authoritative for exact mission identity.

Historical RevDev state before PC unavailability: source HEAD `e5ab891...` after `REVDEV-R149-P8Y3B1-PURE-WATCHER-TRANSFORM` PASS 177/177; installed binary hash prefix `464c77ff`; queue capsule commit `3a958...`; bootstrap commit `2bd753...`. These are historical anchors only. Do not infer present state from them.

Known RevDev concerns: multi-operation result correctness, queue stall, recovery without rerun, PowerShell 5.1 compatibility traps, `AWAITING_CHAT_CONTINUATION`, avoiding Queue Health flashing, timer bubble, operator UI, project cards beside ChatGPT, recent/queued visual states, no startup behavior. RevDev remains its own engineering project.

## 2. Three-AI collaboration

Current roles (latest owner-approved handoff):
- **Claude:** lead developer / engineering reviewer (RelayRef). Expected to return a medium-sized document soon containing substantial research and recommendations.
- **Gemini:** co-developer and independent security/spec auditor.
- **ChatGPT:** continuity holder, evidence reconciler, test architect, conformance reviewer and eventual deployment coordinator when PC access returns.

Earlier role drafts assigned ChatGPT some portfolio/deployment work and Gemini the Digestedv4/spec audit. The latest role assignment above supersedes older role drafts, but do not erase historical evidence.

The owner manually forwards prompts and reports. Never imply that you can contact the other AIs directly.

### Critical rule for Claude's incoming report

Claude's medium-sized report is expected soon. Treat it as a high-value independent contribution, especially where it contains source-level details, engineering feasibility or alternative implementation approaches.

However:
1. Preserve PocketCode's existing product goals and constraints.
2. Treat Claude's recommendations as proposals, not owner decisions.
3. Compare Claude's claims with Gemini's report, existing architecture/contracts, pinned source evidence and the actual repository.
4. Separate verified facts, upstream claims, engineering inference, recommendation and unresolved questions.
5. Check exact repository, immutable commit/tag, files, licence, platform support, dependencies, tests and security implications before suggesting code reuse.
6. Identify where Claude improves or contradicts Gemini, and where both may be wrong or incomplete.
7. Do not adopt a unified architecture, new provider, new runtime, dependency, schema, acceptance ID or scope expansion just because one report advocates it.
8. Keep useful recommendations even when rejecting their proposed implementation.
9. Update the research branch documentation with a traceable reconciliation after the report arrives. Do not modify PR #2/#3 or implementation code.

## 3. User operating constraints and evidence rules

- Phone-only for approximately four months from October 2026. All local PC evidence is stale/unknown until fresh owner-supplied evidence.
- Free ChatGPT usage limits and file intake constraints. Avoid asking for multiple large uploads if one consolidated document or focused excerpts will do.
- $0 budget. Do not assume free hosted execution is available or sustainable.
- User prefers substantial work per pass and minimal interruptions.
- Never claim a test, build, install, deployment, provider run or local check occurred unless it actually did.
- Label design-only, source-inspected, statically reviewed, isolated-harness-tested, device-tested and production-verified distinctly.
- Unknown is not false, pass, fail or safe.
- A parsed instruction is not policy approval; policy approval is not authorization; authorization is not execution.
- No silent acceptance ID remapping, schema changes or cross-project contract convergence.
- Research branch is not automatically mergeable. Its size and commit count are not quality evidence.
- Use exact commit/blob hashes and read-back verification for GitHub continuity writes.
- Do not rely on remembered branch state without rechecking current GitHub metadata when doing work.

## 4. PocketCode GitHub state at handoff

Repository: `marcelosofficial-ctrl/PocketCode-`.

Research branch:
`pocketcode-ai-workflow-director-research-2026-10-28`

Last verified comparison with main:
- 512 commits ahead, 0 behind.
- Base/main SHA: `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- Latest research-branch head at last comparison was not returned by the compare summary; re-fetch before relying on a head SHA.

Protected PRs:
- PR #2: open, draft, unmerged. Head `eb8b7ea83cb0e8fe1880351276c485b761431791`, base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #3: open, draft, unmerged. Head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`, same base.
- Do not modify these PRs.

Latest document blob pins:
- `AI_COLLAB/NEW_CHAT_BOOTSTRAP_20261101.md`: created as this handoff; re-fetch to obtain its blob SHA.
- `AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md`: `e0521f4dedb3dfe0ec1a12fc3c83a7f2cefac663` (before adding this standalone bootstrap link; update after creation).
- `AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`: `14acbe1d6ff8ce99e49d164d70653397600de9db`.
- `AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md`: `7b5b17a126e2a78efd7e2a303303c0c53a309a1e`.
- `PROJECT_STATUS.md`: `6c3174406ef10d9375cff1b09e21d716bef2160c`.
- `AI_COLLAB/GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md`: `aefc611ee273393257a181ec192b75246c80210a`.
- `AI_COLLAB/OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md`: `efb562e7061746ff738274cc3778f74a40ba2d69`.

Use the current research branch when reading or updating continuity docs. Recheck exact state before future writes.

## 5. Gemini open-source research: what it said and how we adjudicated it

Gemini supplied a four-stage broad open-source report. Its report is a valuable discovery catalogue, but not an approved architecture or adoption plan. It has weak traceability in places: generic placeholder citations, repeated references to uploaded material not available as inspectable source evidence, missing exact commits and incomplete module-level review. Its P1/P2 rankings and convergence roadmap are not accepted without verification.

### Candidate dispositions

| Candidate | Current disposition | Reason / next step |
|---|---|---|
| CodeMirror 6 | Leading browser editor candidate; keep investigating | Mobile input handling is real, but target-device UX still needs testing. |
| Pyodide | Leading browser-local Python candidate; compare, do not select | Good for narrow Python task; not a complete sandbox/security boundary. |
| wasmsh | Investigate later, not MVP | Constrained WASM shell, not a general OS shell; no shell in first proof. |
| Tailscale tsnet | Conditional research only | Go library, not drop-in PowerShell/.NET. Tailscale ACL is not app authorization. |
| Aider repo-map | Pattern only | Aider-specific module is coupled to cache, prompt, model token counting and internal imports. |
| LangGraph | Defer | Graph checkpointing does not make external execution exactly once or recover provider side effects. |
| Piston | Reference only, no hosted dependency | Public API no longer generally free from 2026-02-15; self-hosting needs operations/security work. |
| OpenHands ACI | Do not adopt archived ACI repository | Archived 2026-05-15; current editor moved to Agent SDK. |
| FlaUI | Conditional RevDev option | Consider only if a concrete Windows UI Automation gap is demonstrated. |
| Watchdog | Pattern only | Python filesystem watcher, not drop-in PowerShell watcher replacement. File events are hints; reconciliation/idempotency still needed. |
| Judge0 | Not selected | GPL-3.0 is not an automatic blanket disclosure of all PocketCode source; hosting/security/operations are bigger immediate blockers. |
| gVisor / Firecracker / nsjail | Server-side sandbox research only | Not mobile-client features or easy drop-ins; require host hardening and operational ownership. |
| react-native-external-keyboard / KodeMirror / Re-Editor | Not demonstrated necessary | Avoid adding dependencies before a validated mobile editor need. |

### Primary-source deep-dive pins and findings

**CodeMirror 6**
- Gemini's `github.com/codemirror/CodeMirror` points to legacy CodeMirror 5, not CodeMirror 6.
- Old GitHub package repos were archived on 2026-04-15 as active development moved to `https://code.haverbeke.berlin/codemirror/<package>`.
- GitHub `codemirror/view` commit `fbff59ba004d80d8c914f64c42586387b08706ac` is a forwarding commit, not current source.
- npm listed `@codemirror/view@6.43.15`, MIT, recent publication at research time.
- Official changelog includes Android Chrome and iOS virtual-keyboard fixes in 6.43.x.
- New Forgejo host returned 403 in research environment; exact current source commit was not verified.
- Decision: leading browser/PWA editor candidate. Pin package versions/integrity; test iOS Safari/WebView and Android Chrome/WebView for IME, autocorrect, autocapitalize, selection, paste, indentation, viewport resize, keyboard show/hide, scroll, undo/redo and external keyboard. Editor does not supply PocketCode's accessory bar or workflow.

**Pyodide**
- Repository commit: `950e0de49536778f2d7a0efc825e932d812be9e7`.
- FAQ blob: `8cf61babf27af837592d7e17b3c919bdaea795ea`.
- Filesystem docs blob: `35198e99260c5a7c3e09dd30277ce1028ec39065`.
- CPython compiled to WASM/Emscripten; browser and Node support.
- Default MEMFS is ephemeral. IDBFS needs explicit async sync. Native directory mount experimental and Chromium-only, not Safari.
- Python can access browser Web APIs through JS bridge. Do not expose privileged bridge, same-origin credentials, secrets or broad app state to untrusted code. Consider isolated origin/worker and strict broker.
- Normal `threading`, `multiprocessing`, `subprocess` process creation unavailable in browser build.
- Decision: promising for fixed standard-library CSV-to-JSON task, not general secure sandbox. Worker termination/replacement, output limits, import/export and origin storage require separate design and device tests.

**wasmsh**
- Repo commit: `beb3eff548be7beb6dfdda3bf7c2f893f51d9c26`.
- Sandbox docs blob: `b5fba0d9407539bdfd93effc37d20cdec97c7862`.
- Supported syntax blob: `54805677df2c986d1f1c3d2e15040a6ec7f253d9`.
- VM source blob: `6ff6fcbf6faa2af6dec642236271bc2f8f4a916f`.
- Pyodide package manifest blob: `e2b532b95bea582e70ca906896e3941aa7d9e616`.
- README claims shell with utilities, Python 3.13, VFS, network allowlist, step budgets, WASM profiles; Apache-2.0. npm version 0.9.0, Node >=20, Rust 1.89.
- Constrained interpreter, not general OS shell: no host filesystem, arbitrary fork/exec or job control. Background syntax parses but browser runtime is synchronous.
- Some limits use zero for unlimited. Host threat model warns memory exhaustion/OOM and network allowlist DNS/request-shape side channels. A host allowlist is a powerful capability.
- Decision: no shell in MVP. If later, narrow worker spike, nonzero limits, network disabled, inspect every command handler/host bridge, independent worker termination. Ask Claude to examine long-running builtins not bounded by VM step budget.

**Aider repo-map**
- Repo commit: `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`.
- `aider/repomap.py` blob: `541bba6ef4a5385b8cf032201ec6e3f3e32a6ea6`.
- requirements blob: `cddf41382622a5348e84fb1cb1cd8dfddde6e64c`.
- LICENSE blob: `d645695673349e3947e8e5ae42332d0ac3164cd7`.
- Apache-2.0; imports diskcache, grep_ast, Pygments, tqdm, Tree-sitter and Aider-specific modules. Reuse concept, not module by default. If needed, build/select a narrow provider-neutral Tree-sitter/grep-ast utility with path exclusions, symlink safety, size/token caps and explicit parse failures.

### Security/contract corrections to Gemini

1. A confirmed trusted nonzero child exit remains user-facing program FAIL even if cleanup is UNKNOWN/FAILED. Cleanup uncertainty is separately reported and artifacts remain blocked. A stream collection issue is not universally fatal if that stream is optional for the case. A zero exit cannot become PASS if mandatory case evidence/safety gates fail.
2. Policy-before-dispatch is already in the proposed design. The critical property is authoritative exact applied policy revision bound to dispatch, preventing TOCTOU. ETag is one possible mechanism, not a universal requirement. Local browser path and remote/provider path need not share identical policy mechanisms.
3. Canonical PocketCode acceptance remains LOOP-01..14 and CASE-01..16. Gemini's claimed 14 supplementary scenarios lack a traceable pinned crosswalk. Do not merge counts or remap IDs.
4. Artifact release requires authorization, safe normalized path/name, policy-selected media type, size/count, stored-byte integrity and job/attempt/tenant association at release. Secret scanning is not a selected universal gate.
5. GPL-3.0 does not automatically mean all PocketCode source must be disclosed. Licence obligations depend on components, combination and conveyance; AGPL has a distinct network-interaction clause. Obtain component-specific review if needed.

Administrative decisions: no architecture convergence; no LangGraph for MVP; no hosted Piston; no tsnet/AsyncSSH integration; no Watchdog/FlaUI dependency; no shell in MVP; CodeMirror/Pyodide remain candidates, not adopted dependencies.

## 6. Fixed-task comparison: current work and precise state

The existing worksheet is:
`AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`.

A reproducibility gap was found and fixed: the worksheet specified expected behavior but did not freeze one canonical source file. Section 2A now contains exact `main.py` code. It reads `items.csv`, validates headers/rows, uses `Decimal`, writes `summary.json` and returns an explicit status 2 for missing `unit_price`. Each candidate path must use the same source unchanged or disclose a wrapper/adaptation.

Expected success result:
- `grand_total`: string `"10.75"`
- `line_items`: integer `2`
- `totals_by_item`: `notebook: "7.00"`, `pen: "3.75"`
- JSON whitespace/key order irrelevant.

Section 2B records isolated fixture sanity check:
- Python 3.13.5, Linux x86_64, isolated ChatGPT Python environment.
- Source SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`, 1,939 bytes.
- Valid input: exit 0, expected JSON exactly.
- Malformed header: exit 2, missing-`unit_price` error, no `summary.json`.
- Harness injected unrelated spreadsheet-runtime warmup traceback into stderr at interpreter startup, so entire stderr is not clean application-only evidence.

**Status: fixture logic sanity checked, product-path comparison NOT RUN.** No phone, PocketCode app, browser, Safari, Pyodide, remote PC or hosted provider test. No performance, security, sandbox, egress, hard resource enforcement, termination, cleanup or report-handoff conclusions. Do not turn fixture sanity check into a product acceptance PASS.

When owner explicitly authorizes a practical path test, capture exact app/runtime/device/version, use fresh workspaces and same input/source, run both valid and malformed cases, record actual files and outputs, record user steps/turns, and distinguish raw execution evidence from any AI-generated interpretation. A later paired experiment may compare raw evidence against the existing proposed report rendering, measuring factual correction accuracy, provenance preservation, truthfulness, omissions, user effort and time. Do not invent missing facts or add acceptance IDs/schema fields.

## 7. Existing acceptance / architecture constraints

Canonical acceptance IDs:
- LOOP-01 through LOOP-14.
- CASE-01 through CASE-16.

Keep supplementary research identifiers in their own namespace. Never silently remap or merge acceptance IDs. Existing proposed provider-neutral result envelope remains authoritative for its intended design context; don't replace it or add fields just because a research report recommends it.

The proposed design emphasizes:
- Distinct job and attempt identity.
- Separate execution outcome and job disposition.
- Truthful lifecycle state and unknown/error handling.
- Authoritative policy revision at dispatch.
- Reconciliation after ambiguous dispatch/acknowledgement.
- Idempotency and deduplication.
- Cleanup/teardown evidence separate from program result.
- Artifact integrity, authorization and exact job/attempt provenance at release.
- Explicitly bounded resource controls and real termination.
- Report projection must not invent facts or suppress material evidence.

Existing docs to inspect before changing anything:
- `PRODUCT/EXECUTION_CONTRACT.md`
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`
- `ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` (location verify in repo)
- `PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md`
- `ARCHITECTURE.md`
- `DECISIONS.md`
- `ROADMAP.md`
- `PRODUCT_SPEC.md`
- `AI_COLLAB/SEMANTIC_DECISION_CROSSWALK_20261029.md`
- `AI_COLLAB/STAGED_ACCEPTANCE_GATES_20261029.md`
- `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`
- `AI_COLLAB/TRANSITION_MATRIX_ACCEPTANCE_COVERAGE_AUDIT_20261029.md`

## 8. Previous AWC / P0-D crosswalk findings — preserve exactly

- AWC fixture: `AI_WORK_COACH_SYNTHETIC_FIXTURES_V0_1.json`, blob `c2d4cba6c836f725f7bc4585f91e02d443fe89e1`, IDs AWC-001..018.
- RevDev supplement Sections 11–12 blob `d56da68bdc5414cf518d97abc63445f26c6af1fa`.
- P0-D source blob `6a0c804e1ad75edf1022af960acbb143ba1430b6`.
- PocketCode canonical LOOP/CASE acceptance blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.

AWC mappings:
- 001 none.
- 002 LOOP-06 adjacent only.
- 003 none.
- 004 LOOP-02/03 adjacent only.
- 005 none.
- 006 LOOP-07/CASE-12 adjacent only.
- 007 none.
- 008 none.
- 009 none.
- 010 LOOP-13 primary adjacency, LOOP-08 secondary transport analogy.
- 011 none.
- 012 LOOP-02 adjacent only; remove LOOP-14.
- 013–016 none.
- 017 none.
- 018 CASE-12 primary adjacency; LOOP-02/03 secondary conceptual honesty; remove LOOP-05.

P0-D:
- 1–7 no mapping.
- 8 CASE-12/LOOP-07 adjacent only.
- 9 none; CASE-16 is cross-run identity/order, not queue liveness.
- 10 split: 10a idempotent replay after ambiguous response CASE-13 adjacent; 10b run identity/order CASE-16 adjacent; 10c durable exact result publication/replay has no equivalent.
- Gemini review supplied AWC IDs inconsistent with pinned fixture; require exact source pins.
- Claude withdrew earlier CASE-16 suggestion for P0-D 9.

Do not change these mappings without new pinned source evidence and explicit crosswalk.

## 9. Lifecycle helper observations — separate namespace

Separate branch static observations for `scripts/lifecycle_contract.py`, blob `316345341603848c4a86a6a82e533daa796c7695`; tests blob `ef9a68de632be30c091afe57f0724fd030a513f9`. No tests run in that review.

- OBS-01 provider_error maps UNKNOWN then derive_disposition UNKNOWN -> PROVIDER_ERROR; no terminal evidence conflated with confirmed provider error.
- OBS-02 `contradictory_evidence` uses truthiness; malformed falsy values may bypass. Require explicit booleans.
- OBS-03 streaming redactor 768 carry buffer; long separators can leak bearer token; regex max 256 can fail/partially redact longer values.
- OBS-04 event kind does not authenticate producer.
- OBS-05 no expected tenant/job/attempt/source/policy context; stale/wrong-attempt events may enter reducer.
- OBS-06 generic output_truncated truthiness maps LIMIT_EXCEEDED without runtime enforcement and confirmed child termination.
- Other gaps: bool/float cap validation, malformed flags, no expected identity, shallow dict snapshot, best-effort redaction, in-memory idempotency/tombstones/history.
- Keep these OBS IDs distinct from Gemini's similarly named observations.

## 10. Resource/teardown research anchors

These are research findings, not an approved provider implementation.

### Linux cgroup v2
- `memory.max` hard limit; OOM killer may be invoked; allocation may fail ENOMEM.
- `memory.events` is hierarchical by default; `memory.events.local` is local; `memory_localevents` may change semantics.
- `oom` is not `oom_kill`; `oom_kill` may include any OOM killer.
- `memory.swap.max` separate.
- `cpu.max` is bandwidth, not wall-clock limit.
- `io.max` is BPS/IOPS, not disk capacity.
- `pids.max` limits tasks/TIDs; `pids.events.max` local/hierarchical semantics can vary.
- `cgroup.kill` SIGKILLs subtree race-safely.
- `cgroup.events populated=0` means no live processes in subtree at observation time, not provider object/volume deletion. Prevent migration out of observed subtree; read counters before cgroup removal.
- RLIMIT_FSIZE is per-file, not total workspace quota.

### Firecracker
KVM, patching, seccomp, Jailer/equivalent, cgroups/namespaces, privilege dropping and protected paths matter. Jailer is Firecracker-specific; operator owns cleanup; notify_on_release can race. Guest-accessible serial can flood VMM stdout/stderr and cause host storage/memory pressure. Serial limiter optional and absent by default; if enabled collect `uart.rate_limiter_dropped_bytes`. Bound VMM logs independently.

### Modal / Daytona / Cloudflare
- Modal CPU/memory request is not hard cap; distinguish request and limit. Sandbox.create async. detach only disconnects client; does not stop execution. terminate(wait=True) waits for termination.
- Daytona lifecycle started/stopped/paused/destroying/destroyed; delete is fire-and-forget by default; wait=True waits until destroyed.
- Cloudflare Sandbox SDK 1.0: Durable Object identity/storage separate from container instance. DO storage persists until app deletes; container process/files stop/destroy; snapshot root FS may persist; mounted R2 buckets outlive instance. Destroy stops container immediately without process cleanup. Workers Paid and separate cost categories. Do not conflate 0.x and 1.0.
- E2B Firecracker isolation is a vendor claim, not independently verified in this research.

## 11. RevDev / RelayRef continuity and current audit

RelayRef v0.6:
- `RevDev_RelayRef_v0_6_2026-10-22.py`, 55,931 bytes, SHA prefix `eea5fc8bf9f6a204`.
- Golden prefix `dddfcb07304d2d5c`; capsule C0 v1.2 prefix `71009d79a5448279`.
- Python tests 137/137 (v0.4 101, v0.5 112).
- Rules: parsed != policy-approved != authorized; confirmation + guard required; `RDV-END` not `RDV-REPLY-END`; `HOSTED_DENY`; bare `RDV-REPLY` close tolerated with `END_ALIAS_BARE` + `VERSION_MISSING`; broad reads use NEED.

Mobile test evidence 2026-10-22:
- Free ChatGPT/Gemini one run: T6 state-only ACK OK; T5 file-slice injection ignored.
- Later ChatGPT capsule v1.1 ACK UNKNOWN/ASK, state NEED tree, injection ignored, state-only bare close/no version.
- Claude parser v0.6 claimed 137/137 Python tests.

RelayRef v0.9 checkpoint CP-09A (Claude report 2026-10-26):
- `RevDev_RelayRef_v0_9_2026-10-26.py`, SHA `a97db43551b4e91243721b3026802486a9f2bce0f63a63a34cf87217c23ca55d`, 2,779 lines.
- v0.8 SHA prefix `888ab38c...`, v0.7 `00bca0d...`.
- v0.9 self-test Python 3.12.3 Linux: `TESTIDS=293:c230019...`, `SKIPPED=0`, `CASES=293/293`, stderr ENV.
- Python reference VERIFIED only; C# NOT_RUN; Windows/product BLOCKED; golden v0.9 not regenerated (needs `RevDev_Tools_2026-10-22.zip`).
- Changes CHG-01..08 include traversal limits, read metadata, exact code pins, capsule alignment, manifest verifier, reference cannot execute/write/network.
- Gemini v0.9 C# specs CS-SPEC-01..04 are specs, not integrated code.
- Claude notes possible v0.10 scope draft from v0.8 draft hash prefix `b97e...`.

Current RelayRef acceptance crosswalk task from `CHAT_HANDOFF_2026-10-27.md`: correct crosswalk while preserving original acceptance ID meanings. Gemini reconciliation incorrectly remapped IDs. Claude proposal says only some definitions known: B-03 authentication denied -> TRANS-01 (not BOOT-03); BOOT-03 bootstrap conflict; VALID-03 missing manifest fixture; V-03 missing required evidence file; B-07 roots; SAFE-01 add. SAFE-01/B-07 prototype on unchanged v0.9: SAFE-01 61 cases 32 PASS/29 FAIL (29 VALID gaps); B-07 5 checks 4 PASS/1 FAIL (missing vs inaccessible roots indistinguishable); scratch patch 292/293 expected pin change `script_t5_delete_c_root` adds `BANNED_OPERATION:recursive-delete`. Do not infer integration from proposal.

Three-AI roles latest: Claude lead developer (RelayRef), Gemini co-developer/security/spec auditor, ChatGPT continuity/evidence/test architect and eventual deployment coordinator. No PC access until owner says otherwise.

## 12. Current recommended work sequence for the new chat

1. **Start by verifying GitHub state.** Fetch this bootstrap, current checkpoint, handoff addendum, fixed-task worksheet, Gemini review, candidate deep dive, project status, branch-vs-main and PR #2/#3. Do not assume the SHAs above are still current.
2. **Do not start a broad duplicate OSS survey.** We already have Gemini's catalogue and pinned source-level reviews for CodeMirror/Pyodide/wasmsh/Aider.
3. **Wait for Claude's medium-sized report while continuing useful independent work.** When it arrives, parse it into claim/evidence/recommendation tables, verify exact source claims and reconcile against Gemini and current product goals.
4. **Prioritize the product path and fixed task.** Keep comparison NOT RUN until an owner-authorized device/path test is possible. Improve experiment protocol and decision quality without pretending to have device access.
5. **Check existing documents before creating new ones.** Reuse current execution contract, LOOP/CASE acceptance, report projection, semantic crosswalk and backlog. No duplicate acceptance IDs or schema fields.
6. **Maintain separation.** PocketCode and RevDev remain distinct systems; shared protocol compatibility is future research only.
7. **Use isolated documentation-only commits on the research branch.** Read back each update, record exact blob/commit SHAs, update checkpoint and handoff. Do not touch PR #2/#3.
8. **At a good checkpoint, prepare the next handoff early.** User wants a complete copy/paste handoff before chats become too long.

## 13. Questions that must remain open unless evidence/owner decides

- Final product name and collision handling.
- Exact MVP UX and supported phone/device matrix.
- Which execution path is the first supported path.
- Whether CodeMirror 6 is selected after device tests.
- Whether Pyodide is selected after browser/security/device tests.
- Any remote PC protocol and pairing/authentication design.
- Whether hosted execution is ever viable under $0 and security constraints.
- Any runtime/provider choice.
- Whether a future shared PocketCode/RevDev protocol is worth doing.
- Any adoption of new libraries, shell, orchestration graph, sandbox or agent framework.
- Whether/when the owner authorizes hands-on testing, implementation, PR changes or deployment.

Do not resolve these by assumption.

---

## COPY/PASTE MESSAGE FOR THE NEXT CHAT

You are continuing my existing PocketCode + RevDev projects. This is a continuation, not a new project. First read `AI_COLLAB/NEW_CHAT_BOOTSTRAP_20261101.md` on branch `pocketcode-ai-workflow-director-research-2026-10-28`, then read the current checkpoint, handoff addendum, fixed-task worksheet, Gemini research review and candidate deep dive linked/pinned in that bootstrap. Re-fetch current GitHub state before relying on any old SHA or PR status.

**My goals and constraints:** I am phone-only for around four months starting October 2026. Treat all PC/source/runtime/queue/binary state as UNKNOWN until I provide fresh evidence. Budget is $0. GitHub is our continuity store. Work thoroughly and efficiently, do substantial work per pass, avoid unnecessary questions, and use regular chat rather than Work mode. I manually forward messages to Claude and Gemini, so do not claim you contacted them.

**Our three-AI roles:** Claude is lead developer/engineering reviewer for RelayRef and is preparing a medium-sized research document with lots of useful information. Gemini is co-developer and independent security/spec auditor. You (ChatGPT) are continuity holder, evidence reconciler, test architect, conformance reviewer and eventual deployment coordinator when PC access returns.

**Important about Claude's upcoming report:** It is valuable and should be taken seriously, especially source-level technical findings and recommendations. But do not let it overwrite PocketCode's goals, existing contracts, constraints or owner decisions. Treat recommendations as proposals. Verify exact claims against pinned sources and our docs, compare with Gemini, preserve useful ideas, identify disagreements and evidence gaps, and make explicit decisions only where justified. Do not adopt a new architecture, provider, runtime, dependency, schema, acceptance ID or scope expansion just because Claude recommends it.

**PocketCode:** `marcelosofficial-ctrl/PocketCode-` is a phone-first AI coding app evolving toward an Agentic Orchestration Control Plane. Possible paths include local phone/browser execution, WASM, user-owned remote PC, hosted execution only if justified, and manual AI copy/paste fallback. Core values: phone-first UX, provider neutrality, truthful execution evidence/results, explicit user control, no background clipboard polling, no system-wide overlays, secure untrusted-code handling, real resource limits/termination/cleanup, artifact integrity/provenance and $0 budget. No execution provider is selected. The Catrobat “Pocket Code” naming collision remains open. First proof should be narrow: a bounded coding task, honest result, useful correction loop. Do not turn MVP into autonomous multi-agent shell or hosted platform without evidence.

**RevDev:** Separate Windows mission/automation system with queues, watchers/workers, project manager, structured result files and recovery. Do not merge its runtime/security/acceptance boundary with PocketCode. I have no PC access, so all local state is unknown. Historical paths and RelayRef v0.9 status are in the bootstrap.

**Research decisions already made:** CodeMirror 6 and Pyodide are leading candidates, not selected dependencies. wasmsh is later research only, no shell in MVP. Aider repo-map is a pattern only. LangGraph deferred. Piston hosted API not assumed free; reference only. tsnet/AsyncSSH not approved. FlaUI/Watchdog conditional only. OpenHands ACI archived, do not adopt. Judge0 GPL-3.0 is not a blanket source-disclosure prohibition. No unified PocketCode/RevDev architecture approved.

**Fixed-task work:** Read `AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`. It now includes one canonical `main.py` fixture and isolated sanity check. Fixture logic passed in isolated ChatGPT Python 3.13.5/Linux; this was not a PocketCode/mobile/browser/Pyodide/remote/hosted test. Product-path comparison remains NOT RUN. Do not represent it as a product PASS. Keep LOOP-01..14 and CASE-01..16 canonical; do not remap/add IDs or change schemas without explicit crosswalk/evidence.

**Safety and work boundaries:** No merge, deploy, release, publish, Actions, install, provider workload, account creation, spending, source/test changes, PR modification, runtime/queue/host changes, restarts, secrets, elevation or security-boundary weakening unless I explicitly authorize. Documentation-only continuity updates on the isolated research branch are authorized. PR #2 and #3 must remain untouched and unmerged.

**What to do next:** Verify the GitHub branch/docs/PRs, then continue useful work without duplicating Gemini's research. Claude's medium-sized report is coming soon. When I provide it, perform a rigorous claim-by-claim reconciliation against Gemini, our pinned source reviews, PocketCode's original goals and existing contracts. Continue improving the fixed-task experiment and product-path decision readiness without claiming device tests. Update GitHub documentation with exact evidence and read-back hashes. Keep PocketCode and RevDev distinct. Ask me only when an owner-only decision or action is genuinely required.

## Live continuity supplement — 2026-11-01 (later verification)

This supplement supersedes only the earlier branch-count snapshot in Section 5; it does not rewrite historical evidence or alter project decisions.

- Research branch: `pocketcode-ai-workflow-director-research-2026-10-28`.
- Exact branch head immediately before this supplement: `a80a0f6deaad711a17b85616b2d6b2d367e32d0e`.
- Fresh compare against `main`: **520 ahead / 0 behind**; base and merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #2 remains OPEN, DRAFT, UNMERGED at head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PR #3 remains OPEN, DRAFT, UNMERGED at head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- The detailed chronological verification is in `AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md`, Sections 31–34. Its latest read-back blob before this supplement was `9da8c89ddfea1cd9626d0831845efb1e6e780480`.
- The older Section 5 count (512 ahead) is a historical snapshot, not current status. Re-fetch refs before consequential work because each documentation commit advances the research branch.
- Claude's independent report is still expected; do not substitute another broad survey for its reconciliation. Until it is supplied, continue only with bounded, nonduplicative source/contract consistency work.
- No PR, source/test, canonical acceptance, workflow, provider, account, workload, host, queue, Action, merge, deployment or spend was changed in this verification pass.
