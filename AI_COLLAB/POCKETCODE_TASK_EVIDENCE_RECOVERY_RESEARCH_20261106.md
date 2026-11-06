# PocketCode task, evidence and recovery research — 2026-11-06

**Status:** Source-backed architecture/research decision record. Design only. No product source, runtime, provider, acceptance ID, schema or budget decision changes here.
**Repository:** marcelosofficial-ctrl/PocketCode-
**Starting branch HEAD:** `4055595c73f2505314bbb8b51a5e1cc2701aa765`
**Scope:** Mobile execution realities, competitors, task/event recovery, evidence receipts, protocol reuse and adversarial corrections.

## 1. Executive decision

PocketCode should be a **provider-neutral task, execution-evidence, recovery and AI-correction control plane** that interoperates with existing editors/runners. It should not compete as another general-purpose phone Python IDE, and it should not assume a local interpreter, browser runtime, remote PC or hosted sandbox.

The frozen standard-library CSV-to-JSON task remains a workflow benchmark, not proof of market differentiation or hostile-code containment. A correct `summary.json` is necessary but insufficient: PocketCode must bind exact source/input bytes, execution boundary, observations, artifact bytes, recovery and user-mediated AI correction into one truthful history.

**No runtime/provider is selected.** The $0 default, no-PC dependency, explicit paste/import, no clipboard polling, default-deny security posture, canonical LOOP-01..14 and CASE-01..16, D-001..D-005, and separate RevDev/PocketCode acceptance boundaries remain unchanged.

## 2. Red-team corrections to prior work

### 2.1 CASE-04 is not a simple precedence patch

An earlier cross-project note suggested making trusted `timed_out` state win over a nonzero generic `exit_code`. That is unsafe as a general rule. Current `scripts/report_contract.py` accepts only `execution_status` and an untyped integer `exit_code`; it cannot distinguish a natural child exit from wrapper exit, forced-termination code, stale observation or contradictory terminal event. Existing test `test_nonzero_exit_overrides_script_printed_pass` locks in `succeeded + 2 => FAIL`, without representing the producer/meaning of that integer.

**Correction:** preserve CASE-04 as INCOMPLETE / `timed_out` when timeout is trusted. First define typed observations at the coordinator/adapter boundary. Keep child exit, wrapper exit, termination request, confirmed termination, lifecycle status and evidence consistency separate. Contradictory terminal facts remain INCOMPLETE pending reconciliation. Do not patch `classify_verdict()` by precedence alone.

### 2.2 “ACP” is stale and ambiguous

The old Agent Communication Protocol project at `i-am-bee/ACP` was archived on 2025-08-27 and its README says it became part of A2A under the Linux Foundation. It must not be described as a current maintained standalone protocol.

**Correction:** if agent-to-agent interoperability becomes relevant, evaluate current A2A v1.0.1. Use MCP for agent-to-tool integration and A2A for agent-to-agent communication. Neither replaces PocketCode's CommandId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceipt or evidence-authority model. Spell out protocol names because “ACP” is also used by unrelated projects.

### 2.3 iOS embedded Python cannot provide a child-process exit code

Python's official iOS documentation says Python runs embedded in an iOS app and iOS apps cannot use subprocesses, multiprocessing or IPC. A same-process embedded interpreter is not a child process. Calling an embedded function and observing its return or exception must not be represented as a native process exit code.

**Correction:** make evidence boundary-specific:
- `embedded_in_process`: host-observed entrypoint start, return value, raised exception, captured streams and output read-back; no child PID or OS child exit code.
- `external_child_process`: child PID/identity, natural exit code or signal, wrapper result and process-tree termination as separate observations.
- `remote_supervised`: supervisor/provider lifecycle, child facts if exposed, wrapper facts and provider-side cleanup as distinct observations.

An embedded `SystemExit(0)` is not proof of an OS child process exiting zero.

### 2.4 A hash is integrity evidence, not producer authenticity

SHA-256 binds a receipt to bytes and detects later mismatch. It does not prove which process produced the bytes, whether the observation was authorized, or whether the claimed runtime ran. in-toto separates artifact subject/digest statement from authentication envelope and verifier trust policy.

**Correction:** use digests for content identity/read-back integrity. Do not call an unsigned local JSON receipt an attestation or cryptographic proof. If signed attestations are needed, first define producer identity, key custody, rotation, revocation and verifier policy.

### 2.5 A local database cannot make a remote side effect exactly-once

SQLite can make a local transaction atomic. It cannot atomically commit a local row and a remote provider dispatch across two independent systems.

**Correction:** persist an intent/outbox record before dispatch, use stable semantic EffectId and provider idempotency/query support where available, persist acknowledgements/observations, and reconcile ambiguous outcomes. If the remote side effect may have occurred but cannot be queried or deduplicated, mark UNKNOWN and do not blindly redispatch.

## 3. Competitor and platform research

Public product claims are not independent hands-on tests.

| Product | Verified public capability / maintenance | Licence / cost evidence | PocketCode decision |
|---|---|---|---|
| **a-Shell** | App Store describes local iOS Unix terminal, Python, JS, C/C++, shell, offline use, file transfer and Git via `lg2`. Public repo is active and identifies BSD-3-Clause. | Free App Store listing; BSD-3-Clause source. | Strong free local-runner baseline. Do not rebuild its terminal or claim offline Python is unique. |
| **Carnets** | App Store describes standalone on-device Jupyter/JupyterLab with embedded Python, offline use and common scientific packages. Project site says open source under FreeBSD licence; privacy policy says local execution. | Free App Store listing; FreeBSD licence claim on project site. | Notebook/data-analysis baseline, not a task receipt/recovery layer. |
| **Pyto** | First-party site advertises local Python, debugger, editor, packages, WASM runtime, command line, compilers, virtual environments and Shortcuts. Docs say interpreter runs in app process due to iOS restrictions. | Current local storefront price and current app-source licence were not pinned in this pass. | Another reason not to build a general editor. Do not assume its compatibility layer creates an OS process boundary. |
| **Coilbook** | First-party pages claim on-device CPython 3.14, offline projects, console, file access, traceback display, Stop and no-account/no-ad basic runs. | First-party site advertises free execution and paid extras; App Store binary was not installed or independently tested here. App-source licence not verified. | Direct overlap with the simple Pyodios task. Stop/traceback are hypotheses, not proof of process isolation or hard termination. |
| **Pyodios 1.1.0** | Owner-reported Build 7: Pyodide 314.0.5 / Python 3.14.2. Official docs say fresh session per launch, project/session folder copies, external imports require reopening, files over 16 MB are not copied, approximate 300 MB Python memory, and 120-second UI timeout does not stop code. | App itself not verified open source; Settings lists bundled licences (Pyodide MPL-2.0, CPython PSF, Comlink Apache-2.0). | Installed-device comparator only. Do not adopt its bridge or call its UI timeout cancellation. Preserve current exact-match output project. |
| **Replit mobile** | First-party pages describe AI Agent on iOS/Android for websites/web apps, progress, preview and deployment. Native iOS app creation/submission uses the web workflow, not the mobile app. | Hosted service; pricing/free usage not evaluated for this project. No account/workload authorized. | Competitor for mobile AI task/progress UX, not a $0 execution dependency. |
| **Cline** | Current repository supports IDE, CLI, desktop and SDK. Docs describe durable task history, interrupted-task resume and shadow-Git checkpoints. v4.1.25 (2026-10-16) added cloud tasks that continue after editor close; v4.1.26 (2026-10-26) includes reconnect/retry/task-interaction fixes. | Apache-2.0. | Reuse task history, snapshots, resume and explicit diffs. Do not adopt agent engine, auto-approve mode or desktop/cloud topology. A checkpoint is not an execution receipt. |
| **OpenHands** | Release v1.36.0 dated 2026-11-05. Software Agent SDK/Agent Server separates SDK, server API, TypeScript client and automation. Agent Server documents REST/WebSocket access and filesystem persistence for conversations, events and workspace files. | OpenHands app repo MIT; Software Agent SDK repo MIT. | Study event retrieval and API separation. Do not assume its store proves append-only semantics, cross-system exactly-once dispatch or PocketCode security. |
| **MCP Tasks** | Dated 2026-07-28 spec: task durably created before handle returned; client persists task IDs and resumes polling; terminal states expose result/error. Cancellation is cooperative; acknowledgement does not prove work stopped. | Protocol specification, not a runtime dependency. | Adapt async task status/polling only. Task handle is not CommandId or child-exit evidence. |
| **A2A v1.0.1** | Agent-to-agent protocol with task lifecycle, messages/artifacts, polling/streaming/push. Client-side artifact version history is recommended. Spec warns streaming disconnects may miss status messages and task history may not persist every message. | Apache-2.0; latest surfaced release v1.0.1 (2026-05-26). | Candidate interoperability adapter only. Persist PocketCode's own event/receipt ledger. |
| **in-toto Attestation** | v1.2 statement binds immutable subjects to digests and predicate types; statement, predicate, envelope and bundle are separate. Validation checks recognized attester and subject digest. | Framework under development; check exact implementation licence before code reuse. | Reuse digest-bound subject concept. Do not adopt signatures until trusted producer/key-management model exists. |
| **SQLite** | Official docs describe ACID transactions/crash recovery. WAL appends committed frames; sync mode changes power-loss durability. WAL NORMAL may lose recent transaction after power failure; FULL adds sync after each commit. | Public-domain SQLite engine. | Candidate local journal, subject to iOS crash tests and explicit durability setting. Local transaction cannot make provider dispatch atomic. |

### 3.1 Differentiation decision

Phone editors, notebooks, terminals, local Python interpreters, AI code generators, cloud IDEs and agent session history already exist. PocketCode's target combination is:
1. Exact task packet and input/source identity.
2. Boundary-aware host-observed execution facts.
3. Durable attempt-scoped event history and result receipt.
4. Recovery that never reruns a completed side effect because report publication or AI handoff failed.
5. Artifact integrity and release gating.
6. Provider-neutral user-mediated AI correction with new attempt lineage.

If PocketCode cannot prove measurable improvement in these areas, pivot to a portable orchestration/receipt layer that interoperates with existing runners, not a competing editor.

## 4. Protocol and implementation reuse decisions

| Reference | Reuse | Do not inherit |
|---|---|---|
| Cline | Task-scoped history; workspace checkpoints; compare/restore; interrupted-task resume; reconnect handling. | Shadow Git as authoritative receipt, provider routing, cloud execution, broad auto-approval. |
| OpenHands | Durable conversation/event retrieval; API/client/automation separation; forward-compatible event variants. | Whole SDK/Agent Server runtime or unverified transaction/idempotency guarantees. |
| MCP Tasks | Durable task-handle creation; polling interval; reconnect by persisted task ID; cooperative cancellation semantics. | Task IDs as command identity or cancel ACK as termination proof. |
| A2A | Agent discovery/capability negotiation; task/artifact exchange; task status and artifact updates. | Streaming/task history as complete immutable audit log. |
| in-toto | Subject digest and typed predicate separation. | Unsigned local receipts called attestations. |
| SQLite | Atomic local reservation/event/receipt transactions; restart recovery; explicit journal/sync configuration. | Exactly-once remote side effects. |

MCP is agent-to-tool; A2A is agent-to-agent. The legacy Agent Communication Protocol (ACP) is archived. No protocol selection is made in this pass.

## 5. Proposed PocketCode architecture slice

Design recommendation only, not a frozen schema.

### 5.1 Immutable task packet

Bind CommandId and task intent to exact entrypoint, working directory, source/input manifest (relative path, byte size, encoding/media where known, SHA-256), runtime requirements, execution-boundary kind, requested limits/permissions/egress policy, user authorization scope and semantic request fingerprint. A filename alone is not input identity. A source hash alone does not prove user approval.

### 5.2 Identity and side effects

Preserve `CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt`.
- **EffectId:** stable across retries of the same intended external side effect.
- **AttemptId:** fresh for each actual dispatch/execution attempt.
- **Request fingerprint:** exact source/input/runtime/policy/argument identity.
- **Fence/lease:** stale workers cannot append terminal observations or publish for a superseded attempt.

Same EffectId + same fingerprint means look up and reconcile the same logical effect; it is not permission to execute again. A start retry is permitted only when the selected provider's documented idempotent-start contract covers that exact key and fingerprint, or authoritative lookup proves the original dispatch was not accepted. If acceptance is ambiguous or lookup is UNKNOWN, do not redispatch automatically. Same EffectId + changed fingerprint is a conflict. A user-approved correction creates a new logical effect and attempt lineage.

### 5.3 Boundary-specific observations

| Boundary | Trustworthy candidates | Must remain unavailable unless exposed |
|---|---|---|
| Embedded interpreter (native iOS/Pyodios style) | Host-observed entrypoint start, return, exception, captured streams, output inventory/read-back. | Child PID, OS child exit code, process-tree kill. |
| Browser/WASM worker | Parent-observed worker creation, messages, worker error, requested termination and termination event if observed. | Hard OS CPU/memory quota, complete network denial, termination after parent/page loss unless proven. |
| External child process | Child PID, natural exit or signal, wrapper exit separately, bounded streams, process-tree termination confirmation. | Provider resource deletion unless independently observed. |
| Remote supervisor | Durable supervisor state, child facts if exposed, policy revision applied before dispatch, provider cleanup observations. | Child exit inferred from wrapper status, cleanup inferred from local DB close, policy inferred from update request success. |

A natural child exit field exists only for an external child process when authoritatively observed. Never copy an embedded return or wrapper exit into it.

### 5.4 Event journal and recovery

Each observation carries EventId, command/attempt/execution binding, monotonic per-attempt sequence, producer role/channel, evidence authority, event type, observed/received times, payload digest, schema version and fence generation where relevant.

Reducer rules:
1. Same EventId + same payload is an idempotent duplicate.
2. Same EventId + different payload is a conflict; quarantine it.
3. Wrong command/attempt/execution binding cannot mutate the active attempt.
4. Stale fence cannot append terminal state or publish.
5. Sequence gaps remain gaps; do not fabricate events.
6. Conflicting terminal observations remain visible and produce INCOMPLETE pending reconciliation.
7. UI snapshots derive from durable history; snapshots do not replace it.

**Local journal candidate:** SQLite. In one local transaction reserve the semantic effect/attempt and persist dispatch intent; after adapter response append observations and receipt references transactionally. If WAL is selected, specify `synchronous=FULL` where power-loss durability is required and validate on target iOS hardware. Choose Apple file-protection class deliberately.

**Remote side effects:** outbox/inbox reconciliation. Local commit and provider dispatch are not one atomic transaction. After crash between dispatch and acknowledgement, query the original attempt by its provider idempotency key. Redispatch only if authoritative lookup proves the original start was not accepted, or the provider contract guarantees an identical start retry is idempotent for that same key and fingerprint. If lookup is UNKNOWN or the provider lacks that guarantee, preserve UNKNOWN and stop automatic replay.

### 5.5 Receipt and artifacts

Immutable receipt binds task/attempt, input/source digests, runtime/boundary, start/terminal observations and provenance, stdout/stderr capture state/bytes/truncation, actual artifact inventory/size/digests, cleanup/termination, publication and release state, unknowns and contradictions.

Artifact workflow:
1. Write attempt-scoped staging object.
2. Close writer and read back exact bytes.
3. Verify digest, size, path, type and attempt binding.
4. Mark immutable in manifest.
5. Revalidate authorization and digest at release.
6. Quarantine partial, changed, wrong-attempt or digest-mismatched objects.
7. Record release separately from execution verdict.

Known program failure remains a program failure if cleanup is uncertain; cleanup and release remain separate. Whether cleanup is a required PASS gate follows the canonical case contract, not a formatter shortcut.

### 5.6 AI correction

1. User explicitly copies/shares receipt and selected source/input context.
2. Report includes exact task/attempt IDs, source/input hashes, diagnostics, artifact hashes and uncertainty.
3. User chooses any AI assistant and pastes the packet.
4. AI proposes patch; PocketCode shows diff against exact prior source.
5. User approves patch and changed inputs/permissions.
6. New attempt is created; prior receipt/artifacts remain immutable.
7. Copy/share failure retries publication of the same receipt; it does not rerun execution.

No clipboard polling, overlays, automatic provider capture or silent inclusion of unrelated files.

## 6. Decision-ready regression plan

Design scenarios only. No canonical LOOP/CASE/D IDs are added.

| Layer | Scenario | Required result |
|---|---|---|
| Identity | Same EffectId and fingerprint requested twice | Reconcile same effect; no duplicate dispatch. |
| Identity | Same EffectId but changed source/input/runtime/policy | Conflict, not retry. |
| Dispatch | Crash after reservation, before dispatch | Reconcile pending intent before dispatch. |
| Dispatch | Crash after provider dispatch, before acknowledgement | Query by idempotency key; never blindly create second run. |
| Events | Exact duplicate event after reconnect | Idempotently ignore duplicate without losing history. |
| Events | Reused EventId with changed payload | Quarantine conflict. |
| Events | Wrong tenant/attempt or stale fence | Reject; cannot alter current receipt. |
| Events | Sequence gap or disconnect at terminal event | INCOMPLETE until replay/reconciliation. |
| Verdict | Natural child exit 0 + trusted succeeded + case-required gates | PASS. |
| Verdict | Natural child nonzero + consistent terminal evidence | FAIL with exact child exit/diagnostics. |
| Verdict | Wrapper nonzero, child exit unavailable | INCOMPLETE. |
| Verdict | CASE-04 timeout + wrapper 137 / forced termination | INCOMPLETE / timed_out; preserve wrapper/termination separately. |
| Verdict | succeeded + natural child nonzero, or program_failed + natural child zero | INCOMPLETE pending reconciliation. |
| Embedded | SystemExit/PythonError in embedded interpreter | Host-observed return/exception; no fabricated child exit. |
| Collection | Collector truncates/fails after child exit | Preserve raw exit; mark capture degraded; evaluate required evidence gates. |
| Cancellation | Cancel ACK while worker remains working | Requested, not termination confirmed. |
| Cleanup | Known program failure + ambiguous teardown | Preserve FAIL; cleanup UNKNOWN; release blocked as policy requires. |
| Artifact | Partial write, digest mismatch, wrong attempt, changed bytes | Quarantine; never overwrite prior immutable artifact. |
| Security | Applied policy revision pending/stale/mismatched | Do not dispatch; fail closed. |
| Security | Submitted code prints forged lifecycle JSON | Ordinary untrusted stdout; no state mutation. |
| Mobile | App backgrounds/suspends during embedded run | Record unknown/interruption; no background completion/termination claim. |
| Publication | Receipt complete, copy/share fails | Retry same receipt, no rerun. |
| Correction | User approves changed source/input | New effect/attempt; prior evidence immutable. |

Traceability: CASE-04 stays INCOMPLETE/timed_out for trusted timeout; CASE-09/10 keep program checks separate from execution; CASE-16 binds out-of-order results to attempts. LOOP-03/04/05/07/08/10/11/12/14 retain their meanings. No canonical IDs are added, renamed or closed.

## 7. Pyodios: exact next sequence

Owner evidence remains:
- Pyodios 1.1.0 / Build 7, Pyodide 314.0.5, Python 3.14.2 (owner-reported).
- Existing `summary.json` exactly matches oracle: total 10.75, 2 line items, notebook 7.00, pen 3.75.
- Editor displayed `[Bridge/executePython] PythonError`.
- Error Log showed only `Editor: PythonError`, no traceback.
- Classification: ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE.

Next action remains the read-only `sys.last_exc` / `sys.last_value` Console probe in the existing session. Do not rerun, overwrite, restart, clear, reset or garbage-collect the success project. If no saved exception is available, record unavailable evidence, not proof no exception occurred.

Then, in separate fresh projects/attempts:
1. Run malformed-header fixture once and verify no `summary.json` is created.
2. Export the existing success artifact and read back exported bytes.
3. Perform one ordinary app relaunch and inspect project/artifact persistence without rerunning.

Do not test infinite loops or use Pyodios' 120-second UI timeout as a termination test. Official FAQ says execution continues after UI timeout until session/app restart.

## 8. Immediate work sequence

1. Complete owner saved-exception probe and classify.
2. Define typed boundary-specific observations and reducer tests without changing canonical acceptance semantics.
3. Add deterministic fake-adapter tests for duplicate dispatch, crash-after-dispatch reconciliation, stale attempt/fence, collector degradation, timeout/wrapper conflict and teardown uncertainty.
4. Audit synchronous pre-execution policy barrier against existing lifecycle plan.
5. Align static prototype with existing task-aligned receipt spec; remove task mismatch/fabricated metrics, preserve simulation labels; run dependency-free source checks and later real mobile browser interaction test.
6. Only then compare one additional local iOS runner and one mobile AI coding service on same fixture. No installs, accounts, paid usage or hosted workload in this pass.

## 9. Source register

### PocketCode source pins
- `scripts/report_contract.py` and `scripts/test_report_contract.py`, opened at starting HEAD `4055595c73f2505314bbb8b51a5e1cc2701aa765`.
- `AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md`.
- `AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md`.
- `AI_COLLAB/IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md`.
- `AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md` and `AI_COLLAB/PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md`.

### Primary external sources
- Python iOS embedding/platform limits: https://docs.python.org/3.14/using/ios.html and https://docs.python.org/3.14/library/intro.html
- Apple background lifecycle/file protection: https://developer.apple.com/documentation/uikit/about-the-background-execution-sequence ; https://developer.apple.com/documentation/xcode/configuring-background-execution-modes ; https://developer.apple.com/documentation/uikit/encrypting-your-app-s-files
- Pyodios: https://pyodios.caffeinatedmath.com/faq ; https://pyodios.caffeinatedmath.com/guide/projects ; https://pyodios.caffeinatedmath.com/guide/files ; https://pyodios.caffeinatedmath.com/guide/settings
- Pyodide error wrapper source (current main, not asserted byte-identical to bundled 314.0.5): https://github.com/pyodide/pyodide/blob/main/src/core/error_handling.c
- a-Shell: https://apps.apple.com/us/app/a-shell/id1473805438 ; https://github.com/holzschu/a-shell
- Carnets: https://apps.apple.com/us/app/carnets-jupyter/id1450994949 ; https://holzschu.github.io/Carnets_Jupyter/
- Pyto: https://pyto.app/ ; https://pyto.readthedocs.io/en/latest/
- Coilbook: https://levan2002.github.io/coilbook/ ; https://levan2002.github.io/coilbook/help.html
- Replit mobile: https://replit.com/mobile ; https://replit.com/mobile-apps
- Cline: https://github.com/cline/cline ; https://docs.cline.bot/core-workflows/task-management ; https://docs.cline.bot/core-workflows/checkpoints ; https://github.com/cline/cline/releases
- OpenHands: https://github.com/OpenHands/OpenHands/releases ; https://github.com/OpenHands/software-agent-sdk ; https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-agent-server/openhands/agent_server/README.md
- MCP Tasks (2026-07-28): https://github.com/modelcontextprotocol/ext-tasks/blob/main/specification/2026-07-28/tasks.md
- Archived Agent Communication Protocol: https://github.com/i-am-bee/ACP
- A2A v1.0.1: https://github.com/a2aproject/A2A/blob/main/docs/specification.md ; https://github.com/a2aproject/A2A/releases
- in-toto: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md ; https://github.com/in-toto/attestation/releases
- SQLite: https://www.sqlite.org/transactional.html ; https://www.sqlite.org/atomiccommit.html ; https://www.sqlite.org/wal.html

## 10. Evidence status

**VERIFIED:** PocketCode source/test and relevant design docs opened at starting HEAD; primary external docs/repositories opened; live branch/PR/CI state checked before the research write.
**INFERRED:** orchestration/evidence/recovery is a stronger differentiator than another local editor; architecture above is recommended.
**UNKNOWN:** owner Console probe; Pyodios bridge root cause; exact iOS model/version; real PocketCode backend; target-device durability; runner that meets security and $0 gates.
**NOT RUN:** PocketCode product tests, mobile browser interaction tests, provider workloads, new iPhone tests, crash-injection, hostile-code tests and canonical LOOP/CASE acceptance.

No runtime, provider, paid service, account, workload, schema, canonical ID, PR, merge, deployment or product implementation was selected or changed by this research record.
