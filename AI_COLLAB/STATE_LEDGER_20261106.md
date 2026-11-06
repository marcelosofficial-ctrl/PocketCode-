# PocketCode state ledger — 2026-11-06

**Repository:** marcelosofficial-ctrl/PocketCode-  
**Branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Last verified before this checkpoint:** f545974e5d76c8282968c3a86ae69d22cad81343  
**Compare before this checkpoint:** 840 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is branch-history divergence, not product progress. Fetch live refs before consequential work.

## Goal
Build a phone-first, provider-neutral Agentic Orchestration Control Plane that makes AI-generated technical tasks executable from iOS/Android and returns truthful, portable evidence for AI correction. It is not a generic Python IDE. RevDev and PocketCode are intended to converge into one PC-and-phone product/program while retaining separate repos, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates.

## Current device evidence
- Owner-reported app: Pyodios 1.1.0 / Build 7; Pyodide 314.0.5; Python 3.14.2; WASM. Device model/iOS version UNKNOWN.
- Owner ran unchanged canonical main.py with items.csv in one project. Editor displayed exactly [Bridge/executePython] PythonError.
- Owner inspected existing summary.json; it exactly matches canonical oracle: grand total string 10.75, 2 line items, notebook 7.00, pen 3.75.
- Owner checked More → Settings → Error Log → View Error Log. Only Editor: PythonError; no traceback.
- Classification: ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE. Native process exit, stderr, bridge root cause UNKNOWN. Export/read-back, relaunch persistence, malformed-input and PocketCode acceptance NOT RUN.
- Next exact action: in the existing Pyodios session, run the read-only sys.last_exc / sys.last_value probe in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md. Preserve the success project. Do not rerun/overwrite, restart/reset, clear variables/logs or run GC. If no exception is available, record unavailable evidence.

## Product decisions and constraints
- $0 default; no paid provider, host, account, workload or billing without separate owner decision.
- No runtime/provider/cloud host selected; Discovery/product definition phase. No PC requirement for PocketCode.
- Explicit paste-to-context; no clipboard polling or intrusive overlays. SSH/Tailscale and optional cloud remain adapters/research only.
- Stock Pyodide/WASM is not a hostile-code sandbox. Default-deny permissions; egress off by default for untrusted code; disposable externally constrained execution required.
- No secrets/private data in public repo. No product claims beyond verified evidence.
- D-001 unified PC/phone direction with separate development boundaries; D-002 GitHub durable source; D-003 public repo has no secrets; D-004 validate before stack commitment; D-005 $0 default.

## Product shape and architecture
- MVP: explicit paste/import → bounded execution → honest status and actual stdout/stderr/exit evidence where available → real artifact list/export → compact copyable report → user-mediated AI correction → distinct preserved attempts.
- Later candidates: file conversion/batch processing, CSV/JSON validation, tests, downloadable artifacts, multi-file workspaces, remote SSH/Tailscale, optional cloud adapters. GUI automation, arbitrary package install/open internet and direct AI integrations are not first-MVP commitments.
- Preserve identity chain: CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt. Session IDs/task handles are not command IDs.
- Separate child execution facts, wrapper/supervisor facts, lifecycle/disposition, verdict, cleanup, artifact integrity/release and AI correction lineage. Preserve idempotency, replay, fencing and provenance.
- PASS requires trusted terminal success and child exit 0; FAIL requires confirmed program/runtime failure; INCOMPLETE for timeout/cancel/rejection/infrastructure/missing/contradictory evidence. UI timeout does not prove process termination.
- Keep canonical LOOP-01..14, CASE-01..16 and D IDs unchanged. CASE-04 remains INCOMPLETE/timed_out when trusted timeout. Do not precedence-patch scripts/report_contract.py until typed child-exit vs wrapper-exit vs termination provenance is resolved. EVAL-06 is separate checkpoint experiment.

## Three-AI roles
- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect and cross-project coordinator.
- Owner forwards reports manually. No direct AI-to-AI communication assumed. One lead writer per branch/work item; other AIs review read-only or take disjoint scopes.

## Research references and current open work
- OpenHands and Cline are pattern references, not frameworks to adopt wholesale. MCP Tasks may inform async tool-task status; the legacy Agent Communication Protocol (ACP) was archived 2025-08-27 and merged into A2A. Evaluate current A2A for agent-to-agent interoperability, not archived ACP. MCP/A2A task IDs do not replace PocketCode command/attempt identity or trusted receipts. Reject wildcard auto-approval.
- After Pyodios probe: malformed-header fixture in separate fresh project; then export/read-back and natural relaunch persistence as separate tests. Do not overwrite success project.
- Source work next: typed CASE-04 exit provenance; degraded collector/teardown/artifact release; synchronous pre-execution network-isolation barrier. Use fake adapters/processes and exact-SHA tests; no live services or spend.

## Repository state
- PR #2 and #3 are OPEN/DRAFT, unmerged, unchanged; they are separate branches. Do not merge or modify absent explicit authorization.
- Actions run query for active branch returned no items; this is not proof no CI activity exists.
- Latest pass changes documentation/continuity only; no PocketCode product code/tests/runtime/provider/fixture/schema/acceptance/PR/merge/deployment changed.
- Read first: AI_COLLAB/CHAT_START_HERE.md, then this ledger, then AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md and AI_COLLAB/NEW_CHAT_HANDOFF_20261106.md.


## 2026-11-06 — Cross-project working-method upgrade

Authority: owner-provided RevDev working-method decision. Applies to PocketCode continuity and engineering process only; does not replace product goals, revise runtime/security/budget boundaries, or transfer RevDev code, architecture or acceptance evidence.

- GitHub is durable project memory; chats are replaceable workers. New chats resume from live GitHub state, not hidden context.
- Read compact entrypoint, latest ledger and active handoff first. Retrieve only task-specific source/tests/review packets; search/index large records before expanding. Avoid duplicate master documents and historical rereads without a concrete question.
- Use bounded substantial passes with objective, scope, expected result, evidence requirements and stop condition. Prefer a verified vertical slice over many open threads.
- Batch independent read-only operations in modest groups. Serialize dependent work and shared writes. Keep outputs compact. Verify every write by exact read-back.
- On interruption/tool failure, do not assume success or failure. Re-fetch live branch and target objects, inspect commits and exact blobs, reconcile whether the operation happened, then resume. Never blindly replay a possibly completed mutation.
- Durable operation model: stable EffectId across retries; fresh AttemptId per actual attempt; exact input/argument hashes; explicit dependencies and authorization scope; durable operation history; per-operation progress/evidence; heartbeats/leases; fencing; bounded retries; exact reconciliation of ambiguous external effects.
- Keep execution outcome, collection state, lifecycle/job disposition, cleanup, publication and final acceptance distinct. Successful execution is not automatically a published or accepted result.
- Checkpoint every 2–3 meaningful passes and immediately after consequential implementation, testing, review, CI or architectural decisions. Update entrypoint and ledger, append work log, pin exact branch/source/test hashes, and rotate before context becomes unhealthy.
- Roles remain Claude lead developer/reviewer; Gemini co-developer and independent security/spec auditor; ChatGPT continuity/evidence/acceptance/cross-project coordinator. Owner forwards reports manually; one lead writer per shared work item.
- RevDev and PocketCode remain one PC-and-phone product direction with separate repos, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates. Share provider-neutral concepts only; never transfer acceptance evidence.

Verification at checkpoint start: branch HEAD 4446135bf1345f37aa5d221d27c0eabbdbcef5c7; main 555840d8d83342513d9cd353d4d1522d46a5c82d; compare 820 ahead / 0 behind. PR #2 head eb8b7ea83cb0e8fe1880351276c485b761431791 and PR #3 head 0ddcc0bc97bac5d446aefedf3d71f99411bd841d remain OPEN/DRAFT. Branch-filtered Actions query returned zero runs; exact-head status/check-runs have no individual checks. Current branch CI is UNKNOWN, not PASS. No product code, tests, device state, schema, acceptance IDs, budget or runtime/provider decision changed.

Next task: owner runs only the read-only Pyodios sys.last_exc / sys.last_value Console probe in the existing successful session. Preserve exact-match summary.json; do not rerun, overwrite, restart, clear, GC or run the wrapper there. After device evidence, continue typed child/wrapper/termination/lifecycle provenance before any CASE-04 formatter change.


## 2026-11-06 — Task/evidence/recovery research decision

- Added `AI_COLLAB/POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md`, source-backed across mobile execution, competitors, event/task protocols, artifact provenance and durable local journaling.
- Recommended differentiation: provider-neutral task packets, boundary-aware host observations, durable attempt history, immutable receipts/artifacts, no-rerun recovery and user-mediated AI correction. Do not build another general phone Python IDE.
- Critical platform correction: iOS embedded Python cannot spawn subprocesses/multiprocessing/IPC. In-process return/exception must not be reported as child exit. Separate embedded, browser-worker, external-child and remote-supervisor evidence.
- CASE-04 remains INCOMPLETE/timed_out on trusted timeout. Reject precedence-only formatter change; generic `exit_code` cannot distinguish child, wrapper, forced termination, stale or contradictory evidence.
- Protocol correction: legacy ACP is archived; A2A v1.0.1 is current successor for agent-to-agent interoperability. MCP Tasks is a task-handle/status pattern. Neither replaces PocketCode identities or receipt ledger.
- SQLite is a candidate local journal, with explicit WAL/synchronous durability and target-device crash tests. It cannot make a remote side effect exactly-once; use outbox/idempotency/reconciliation.
- No runtime/provider, budget, canonical ID, product source, test, acceptance, PR or deployment decision changed. Owner Pyodios saved-exception probe remains NOT RUN; artifact preserved.


## 2026-11-06 — Prototype integrity and static regression recovery

- Reviewed the live prototype/checker changes through HEAD `c22d8108c9ceab3d003cfc92debbb99cd87e8a82`.
- The prototype remains simulation-only. Its displayed `main.py` is pinned to the canonical SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7` (1,939 bytes); initial CSV bytes are checked against the fixed success fixture.
- Red-team found malformed Python regex syntax in the first checker update and two test methods misplaced inside the `VALID_HTML` fixture. Corrected checker regexes, restored the canonical source guard in the fixture, moved tests into the class, and added roving-tabindex checks. Current checker/test blobs: `ec56e6084c4e0e6e8274734e259b12a17110ffb4` / `d22829c64235c2334561d7deb5b3110c7243ab4e`; 11 test methods.
- Focused Python assertions for canonical source length/hash and CSV extraction/equality passed. Full unittest suite, browser JS, clipboard, VoiceOver/TalkBack and mobile tests remain NOT RUN. Current exact-head CI status has zero checks and zero workflow runs, not PASS.
- EffectId wording corrected: same key/fingerprint permits lookup/reconciliation, not automatic replay. UNKNOWN forbids redispatch unless authoritative evidence or a documented provider idempotency contract permits it.
- No product runtime/provider, canonical acceptance ID, budget, PR, merge or deployment changed. Pyodios owner probe remains outstanding.


## 2026-11-06 — Prototype canonical-fixture alignment

- `prototypes/mobile-runner/index.html` now displays the frozen CSV-to-JSON task, exact canonical `main.py`, success and malformed-header examples, and explicit simulated-only receipt fields. No code runs and no artifact is created/downloaded.
- Embedded `main.py` was extracted and verified as 1,939 UTF-8 bytes with SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`, matching the frozen worksheet/archive record. Initial `items.csv` success fixture is pinned with UTF-8/LF final newline.
- Static checker pins canonical source SHA and success input bytes; 11 regression test methods cover duplicate IDs, missing labels, fabricated timings, fake Run, tab relationships, prompt context, roving tabindex and fixture integrity.
- Local recreated 11-case Python harness passed 11/11; this was not execution of the exact repository test file or CI. Static checker passed against a reconstructed HTML fixture containing the exact pinned source/input. Real browser, screen reader, iOS and Android interaction remain NOT RUN.
- A checker indentation defect found during red-team review was corrected and read-back verified. The initial prototype remains simulation-only; no product runtime, provider, budget or acceptance ID changed.
- Pyodios saved-exception Console probe remains NOT RUN and is still the next owner action.


## 2026-11-06 — Fresh source maintenance gates

- Research note extended with Pyodide module-worker behavior, iOS app lifecycle constraints, SQLite WAL durability and WAL-reset bug, and MCP Tasks/A2A limitations.
- SQLite WAL selection is blocked until the bundled version is pinned at 3.51.3+ or supported backport (3.44.6 / 3.50.7), with the documented multi-connection write/checkpoint race tested. `synchronous=FULL` is required where power-loss durability is a requirement. WAL is not for network filesystems.
- MCP Tasks remain experimental (2025-11-25 spec); A2A v1.0.1 task streaming/history can omit updates/messages after disconnect. PocketCode's own receipt/event journal remains authoritative.
- Checker now accepts tab attributes regardless of class/id attribute ordering. Added a regression case for this. Test method count is 12; exact suite/CI not run.


## 2026-11-06 — Event history and provenance deepening

- Reviewed current OpenHands SDK EventLog/ConversationState implementation: one append chokepoint, parent-linked events, sequence assignment, cold-load projection rebuild, and explicit in-memory fallback when persistence is unconfigured. Reuse architecture pattern only; no durability/security guarantee inferred.
- Reviewed Cline task history and shadow Git checkpoint docs. Adopt source/input snapshot, compare/restore and interrupted-task UX ideas; explicitly keep checkpoints separate from execution receipts.
- Updated provenance references: in-toto Attestation v1.2 has predicate/statement/envelope/bundle separation; SLSA v1.2 is current and approved while v1.1 page is retired. Do not label unsigned receipts attestations or apply build provenance to arbitrary script execution.
- Research-only. No product runtime, provider, budget, canonical acceptance ID or schema changed.


## 2026-11-06 — Typed execution evidence and recovery contract

- Added AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md, a design-stage contract for typed lifecycle/child/wrapper/embedded observations, verdict reconciliation, ambiguous dispatch, source-scoped event identity, receipt/artifact integrity and mobile lifecycle boundaries.
- Added isolated scripts/execution_projection.py and scripts/test_execution_projection.py. The helper is not integrated with report_contract.py or a trusted coordinator. Producer class strings are shape checks, not authentication.
- Local verification: 31 projection tests passed under CPython 3.13.5; both files compiled. GitHub exact read-back: source blob f32237c8c5ee5d62b0416b3dd867515ce567c21b; test blob cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1.
- Added research sections 13–17: official Python 3.14 mobile/WASM subprocess constraints; wrapper/signal/SystemExit distinctions; current OpenHands/Cline/Temporal release and licence metadata; provider-scoped idempotency versus transactional outbox; CloudEvents source-scoped IDs and OpenTelemetry dual timestamps; bounded code adoption and attestation limits.
- New source/design checkpoint commit: 3c6db063fe209396cab2d23b3f61c9daedd373ce. The following continuity checkpoint records the source commit and exact read-back. Fetch the live ref before further work.
- CASE-04 remains INCOMPLETE/timed_out on trusted timeout. scripts/report_contract.py remains unchanged. LOOP/CASE/D IDs, runtime/provider, storage, budget, canonical schema, PRs and deployment unchanged.
- PR #2/#3 remain untouched. No Actions, mobile, fake-adapter, persistence, provider, artifact-release, egress, crash or canonical acceptance tests were run by this source/design checkpoint.
- Pyodios artifact status remains owner-inspected exact oracle match; bridge root cause and native exit unknown. Next owner action is the previously supplied read-only sys.last_exc / sys.last_value Console probe. Preserve the project and do not rerun/overwrite it.


## 2026-11-06 — PC-2026-11-06-P24 — Dispatch reconciliation kernel started

- Began the next ranked gap after the typed exit projection: ambiguous provider acknowledgement and safe retry.
- Added local pure helper/test working copies for scripts/dispatch_reconciliation.py and scripts/test_dispatch_reconciliation.py. Actions are dispatch_first, adopt_existing, retry_same_attempt, poll_existing, hold_unknown, conflict and do_not_replay. The helper never generates new IDs, mutates durable state or sends requests.
- Bound lookups/idempotency capability to EffectId, DispatchAttemptId, request fingerprint, endpoint, account, provider, API version, region/zone scope, token (when present), retention and documented deduplication/mismatch behavior.
- Red-team found and fixed non-authoritative-found adoption and an unscoped authoritative-not-found retry. A provider token is optional for authoritative exact-lookup reconciliation but required for token-based replay.
- Local tests: 28/28 pass under CPython 3.13.5; both files compile. GitHub checkpoint commit 203628276e65909140bf4ed563071442c538548d created and read back: helper blob 2b0928002fdf690005711ea71f1a115a665490ef; tests blob f45eb831edb3cfdbcbf4284e3f81180eaee35f12. It is not a live adapter, outbox or exactly-once guarantee.
- Current project branch at the beginning of this slice was continuity commit 950387f766355825782072fdade057fe8caf5b8d. Earlier closeout compare was 842 ahead / 0 behind main, merge base 555840d83342513d9cd353d4d1522d46a5c82d. Exact-head Actions/check-runs were zero; aggregate status pending. PR #2/#3 remain open draft at original heads.
- Next: commit/read back the two helper files and contract/research updates, then build deterministic fake-store/outbox tests for crash points and fencing. Do not integrate with a provider or select storage yet.


## 2026-11-06 — P24 GitHub verification closeout

- Dispatch helper and 28-case test file are committed at 203628276e65909140bf4ed563071442c538548d and both were read back by exact Git blob SHA.
- Contract, research, start page, ledger and work log were also read back at the corresponding P24 checkpoint SHAs. P24 is no longer local-only.
- Exact-head verification: zero Actions runs, zero check-runs, combined commit status pending (no individual statuses). PR #2/#3 remain OPEN/DRAFT at original head SHAs eb8b7ea83cb0e8fe1880351276c485b761431791 and 0ddcc0bc97bac5d446aefedf3d71f99411bd841d.
- Branch compare at dispatch source commit: 843 ahead / 0 behind main, merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is history divergence, not product progress.
- Next read first: this entrypoint, then EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md; inspect dispatch_reconciliation.py and its tests, then plan fake-store/outbox crash/fencing cases. Fetch live branch/PR/CI state before further edits.


## 2026-11-06 — P25 extended dispatch red-team

- Further correction: authoritative=True alone does not make not-found final. Eventual consistency or incomplete lookup coverage may hide an accepted/in-flight effect. The helper now requires separate absence_final=True before it may choose retry_same_attempt from a not-found response.
- Provider idempotency must be exact-operation/API-version scoped. Stripe API v1 and v2 semantics differ; AWS EC2 supports operation-specific token behavior with regional/zonal scopes. See research section 19.
- Latest helper/test Git objects: source 6760b3301e818956f71fdf02e369407e3b5cdaf7; tests f1949ebcfd525c5715af7fd9e022d5d35f8f1063 (33 test methods). They are not branch-durable until committed and read back.
- Local test execution of this expanded 33-case revision is NOT RUN in this pass. Previous 61/61 claim applies only to the earlier 30-case dispatch revision and must not be carried forward to this changed code.
- No runtime/provider/database selection, PR mutation, merge, deployment, budget or canonical ID change.


## 2026-11-06 — P25 malformed-input guard

- Added a string-type guard for ProviderLookup.outcome before set membership; malformed unhashable values now hold_unknown rather than raising TypeError.
- Added regression cases for non-string lookup outcome and non-string dispatch state. Latest test file contains 34 unique test methods. Execution NOT RUN for this latest revision.
- Latest helper/test blobs: 165d141bc6ab47ad9d19d1ba537ab0e3e39aa16d and e65968cc2162dca8eb75d446e10eec06c0ab9220. Branch checkpoint pending.


## P25 test-file deduplication correction

- Final source review found the same test method name was defined twice in the expanded dispatch suite. Python unittest would silently replace the earlier method in the class namespace, so a regex-based method count overstated unique coverage.
- Removed the duplicate definition. The final test file now has 34 test methods and 34 unique method names. The 34-case suite remains NOT RUN after this correction.
- Final test blob: 7bcfa95c5a077b3a5d31825f0db73f593ac4d6a9. This supersedes the earlier P25 test blob SHA.


## P25 final closeout — 2026-11-06

- Latest verified branch checkpoint: 25a2083e6509d9fee2ad4ce7727405a70558813a.
- Final dispatch helper blob: 165d141bc6ab47ad9d19d1ba537ab0e3e39aa16d.
- Final dispatch tests blob: 7bcfa95c5a077b3a5d31825f0db73f593ac4d6a9. Read-back confirms 34 test methods with 34 unique names; duplicate method removed. Latest 34-case suite NOT RUN.
- Contract, research, entrypoint, ledger and work log were read back at their exact blob SHAs in this checkpoint.
- Exact-head Actions runs: 0; check-runs: 0; combined status pending with no individual statuses.
- PR #2/#3 remain OPEN/DRAFT at their original head SHAs. No PR mutation, merge, deployment, provider execution, billing or runtime/storage selection.
- Branch compare: 847 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is history divergence, not product progress.
- Next: implement a deterministic fake outbox/store with atomic reserve + outbox, duplicate delivery, lease fencing, crash-point recovery and event dedupe. Keep it isolated and explicitly non-production until a real durable store is selected and crash-tested.


## PC-2026-11-06-P26 — Outbox recovery model and ChatGPT retrieval failure mitigation

- ChatGPT error investigation: owner reports repeated iOS error "The operation couldn't be completed. (APIClientInterface.ConversationDetailError.DetailError error 1.)". Public docs do not map this internal string. The symbol names suggest conversation-detail retrieval, but root cause remains UNKNOWN. iOS client/decoder, conversation backend, session/access, network path and large conversation payload remain hypotheses. GPT reasoning/model failure is not the leading hypothesis because failure appears before the conversation can be resumed, but this is not confirmed.
- OpenAI official incident history shows "Elevated errors in ChatGPT conversations" on 2026-10-30, marked resolved. It confirms server-side conversation incidents are possible; it does not establish this user's cause. Official status at investigation time did not declare an active Conversations incident. Runbook committed at AI_COLLAB/CHATGPT_IOS_CONVERSATION_DETAIL_ERROR_RUNBOOK_20261106.md.
- Permanent practical mitigation: GitHub branch/docs are durable source of truth; chats are replaceable workers. Preserve screenshot, timestamp, conversation ID/URL, request ID, app/OS/device versions and cross-client/network reproduction evidence for OpenAI Support. Do not claim a user-side fix can prevent the OpenAI error itself.
- Added scripts/fake_outbox.py and scripts/test_fake_outbox.py, plus AI_COLLAB/FAKE_OUTBOX_MODEL_20261106.md. Local CPython 3.13.5: 19/19 fake outbox tests passed; py_compile passed. This is a deterministic in-memory state model, not a durable transaction, concurrency, process-kill, power-loss or provider test.
- Model covers atomic in-memory reservation+outbox commit, EffectId stable across attempts, fresh attempt identity only after prior terminal state plus explicit authorization, lease owner/expiry/fence, stale-worker rejection, pre-send crash reclaim, post-dispatch reconciliation hold, exact found adoption, final absence gate, and fake receiver duplicate delivery.
- Red-team limitation: adapter evidence fields are caller-supplied assertions; no provider authentication/finality is proven. No storage/runtime/provider selected. A durable implementation must re-test transaction and fencing behavior against the selected store.
- Next: append-only event journal with source-scoped producer IDs, payload conflict quarantine, authenticated producer boundary, monotonic coordinator sequence, then artifact publication/release lifecycle. Keep all canonical IDs and CASE-04 semantics unchanged.
- Latest branch before this ledger update: 56bcc7167b33554a29b68c8fdccc448b9383b6b6. Earlier d62429c handoff checkpoint verified. PR #2/#3 remain OPEN/DRAFT and untouched. Exact current-head Actions/check status must be rechecked after this commit; no merge, deployment, paid provider, account or workload.

## PC-2026-11-06-P27 — Append-only event provenance model

- Added scripts/event_journal.py, scripts/test_event_journal.py and AI_COLLAB/EVENT_JOURNAL_MODEL_20261106.md.
- Local Python unit tests: 19/19 passed. This is an in-memory deterministic model only, not durable journal, cryptographic authentication, concurrent append, process/power-loss, or product integration.
- Event identity is (source, producer_event_id). Exact replay from same producer with identical bytes returns original sequence. Changed bytes or a different authenticated producer identity reusing that source/event ID is quarantined; original event is not replaced.
- Exact payload bytes and SHA-256 are retained. Occurrence and observation timestamps are separate; coordinator sequence alone orders events. Effect-linked events require the current attempt-scoped fence.
- Red-team boundary: AuthenticatedProducer is forgeable by arbitrary Python callers. Only a trusted authentication adapter may construct/pass it after cryptographic credential verification, authorization, revocation and replay checks. Durable fence validation and append must be one atomic transaction.
- No canonical IDs, CASE-04, runtime/provider/storage, budget, PR, merge or deployment changed. Next: fake coordinator spanning outbox + journal + projection rebuild, then durable-store selection only after semantics stabilize.

## PC-2026-11-06-P27 refinement — event replay red-team

- Re-reviewed duplicate semantics and corrected two edge cases.
- Same authenticated issuer+subject with rotated key ID and identical event facts is now deduplicated. Key rotation should not create a false event identity conflict.
- Exact duplicate also requires the same occurrence timestamp; observation timestamp may differ. Changed occurrence time is an altered event fact and is quarantined.
- Expanded local suite to 21 tests; 21/21 passed. GitHub source/test files were updated in follow-on commits. Authentication and durable atomicity limitations remain unchanged.


## 2026-11-06 coordinator composition increment

- Added `scripts/fake_coordinator.py` and `scripts/test_fake_coordinator.py` to compose the in-memory outbox and append-only event journal (14 focused cases).
- Persisted reservation creation time and acknowledgement observation time in the fake outbox so interrupted event appends can be repaired using stable event occurrence timestamps.
- The projection now surfaces interrupted outbox/journal boundaries explicitly as `dispatch_intent_unjournaled`, `reconciliation_required` and `acknowledgement_unjournaled`, rather than silently projecting an earlier event state.
- Scope remains deterministic in-memory modeling. Durable atomicity, concurrent writers, process/power-loss recovery, real provider authentication, product integration and CI are NOT ESTABLISHED. The 14 tests were exercised against API-compatible in-memory test doubles, not canonical repository modules in a checkout.
- Claude navigation: read `CLAUDE.md` and `AI_COLLAB/CLAUDE_HANDOFF_20261106.md` before taking the next implementation/review task.


## 2026-11-06 reconciliation composition refinement

- Added a coordinator-level exact-scope reconciliation operation. Authoritative provider-found outcomes now persist their coordinator observation timestamp and append a distinct `provider_acceptance_reconciled` event; authoritative final absence appends `final_absence_reconciled` and projects `retry_authorized`.
- Non-final or non-authoritative absence remains held in `reconciliation_required` and emits no retry authorization event.
- The fake model still trusts the caller's reconciliation authority booleans. Real adapter authentication, durable atomicity, concurrent safety and production behavior remain NOT ESTABLISHED.


## 2026-11-06 recovery repair hardening

- Reconciliation outcomes now persist enough typed recovery metadata to repair a crash between the outbox state transition and journal append.
- Provider-found reconciliation records `acknowledgement_source=reconciliation`; the acknowledgement repair path re-emits the same reconciliation event identity and timestamp.
- Final exact absence now enters explicit `retry_authorized` state rather than generic pending. Projection exposes `retry_authorization_unjournaled` until the final-absence event is appended; a dedicated repair operation is idempotent.
- This remains an in-memory model; atomic commit across outbox and journal is still not implemented.


## 2026-11-06 lease and dispatch-intent crash repair

- Persisted lease-claim and dispatch-intent timestamps in the fake outbox. Added idempotent journal repair operations for both transitions.
- Projection now exposes `lease_claim_unjournaled` and `dispatch_intent_unjournaled` when the outbox transition is committed but its event is absent. This complements acknowledgement and final-absence repair.
- Added focused crash-window test cases. These are model tests; actual canonical test results are tracked by the new branch-scoped GitHub Actions workflow.


## 2026-11-06 first canonical CI findings

- Added branch-scoped Python unittest workflow and ran it on the repository checkout (Python 3.12). The run on `01ba09e` found 2 failures in the existing mobile prototype checker: both valid-fixture tests rejected the embedded `main.py` frozen hash. The run on `333212a` found those same 2 failures plus a projection-order regression: after expired dispatch intent, state must remain `reconciliation_required` even if the dispatch-intent event is also missing. The latter was corrected by prioritizing reconciliation-required state.
- Checker diagnostics now include the observed embedded source byte count and SHA-256 without changing the frozen expected hash. The next CI run will identify whether the fixture mismatch is in byte length, source content, or expected digest.


## 2026-11-06 fence-scoped projection refinement

- Read-model rebuild now evaluates lease, dispatch-intent and acknowledgement evidence against the current outbox fence, not merely whether any event of that kind exists for the attempt. This prevents an earlier safe retry's events from masking a missing event on a later dispatch under the same DispatchAttemptId.
- Added same-attempt retry coverage: final exact absence, higher fence, second dispatch intent interrupted before journal append must project as `dispatch_intent_unjournaled`.


## 2026-11-06 canonical fixture failure root cause

- The two mobile-prototype checker failures were traced to the test fixture's Python triple-quoted HTML string: embedded main.py used `"\n"` instead of `"\\n"` in the fixture source. Python interpreted the escape while constructing the fixture, removing the backslash and producing a 1-byte-short, different source hash. Corrected the fixture escaping; the frozen canonical SHA-256 in the checker remains unchanged.
- The current-fence projection tests passed in the subsequent CI run; no remaining recovery-model failures were reported there.


## 2026-11-06 — canonical repository CI green

- Added test-only workflow `.github/workflows/pocketcode-python-tests.yml`, triggered by script/workflow changes on the research branch. It uses Python 3.12 and `python -m unittest discover -s scripts -p "test_*.py" -v`, with contents:read only and no deploy step.
- Successful exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308082939 at `09290eaf1ac8af1461211ac90564440a70708f32`, Ubuntu 24.04 / Python 3.12, **154 passed, 0 failed**.
- Initial prototype checker fixture failure was fixed by double-escaping the embedded source's `\\n` in the Python triple-quoted test fixture. Frozen canonical source length/hash was not changed. Intermediate projection precedence regression was corrected and included in the green run.
- The green run validates repository Python unit tests at that exact SHA only. It does not validate later commits, iOS/Android behavior, actual Pyodios, durable transactions, concurrent workers, provider behavior, sandboxing or artifact release.


## 2026-11-06 result receipt and artifact release model started

- Added an isolated in-memory model for immutable versioned result receipts, exact-byte artifact manifests, quarantine, per-request current authorization checks and same-receipt publication retries. See `scripts/result_receipts.py` and `scripts/test_result_receipts.py`.
- The model is not durable, signed, malware-scanned, provider-authenticated or production-integrated. Digests establish byte integrity relative to stored values, not producer authenticity or safety. A later observation creates a linked receipt version; it never mutates an earlier receipt. Report-copy retry uses the same receipt and does not trigger task execution.
- Test result is pending the branch-scoped Python CI run at the next source commit.


## 2026-11-06 receipt-model CI defect

- First CI run including the receipt model discovered one implementation typo: the publication-attempt collection was initialized as a dictionary but consumed as an append-only list. Corrected initialization to an empty list. The failure was in receipt publication bookkeeping, not the recovery/outbox suite.


## 2026-11-06 — result receipt/artifact model CI green

- Added `scripts/result_receipts.py` and `scripts/test_result_receipts.py`. The model captures immutable receipt revisions, evidence ref/digest pairing, attempt-bound artifact manifest, exact-byte digest/size, partial-write and digest-mismatch quarantine, safe logical artifact names, per-request authorization revalidation, stale-attempt release denial and same-receipt report-publication retries.
- Successful exact-SHA CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308449590 at `ce7409ac9077154f5f058799b0d6028fb3e98ee0`, Ubuntu 24.04 / Python 3.12, **177 passed, 0 failed**.
- This is an in-memory conformance model. It does not authenticate evidence producers, sign receipts, scan artifacts, persist across restarts, provide actual download/share, or prove current authorization outside the passed test object.
- Next: compose receipts with accepted coordinator events, verify immutable later versions and publication retry semantics, then design durable atomicity requirements without selecting a store prematurely.


## 2026-11-06 receipt revision chain red-team refinement

- New receipt versions now form one linear chain per `(EffectId, DispatchAttemptId)`: the first version has no predecessor; each later version must name the latest version; a predecessor from another effect/attempt or a stale predecessor that would fork history is rejected. Exact revision-key replay remains idempotent.
- Added regression tests for cross-attempt/cross-effect links and stale-predecessor forks. New test count: 25 in the receipt model; branch CI pending for this commit.
- Added `AI_COLLAB/CLAUDE_PROJECT_MAP_20261106.md` with canonical GitHub links, navigation order, project/code/test map, roles, boundaries and Claude's next actions. Linked it from `CLAUDE.md` and the Claude handoff.


## 2026-11-06 — receipt version-chain CI green

- Exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308764330 at `4d4d66561b176b560b49fb00c6b600617bbeef97`; Ubuntu 24.04 / Python 3.12; command `python -m unittest discover -s scripts -p "test_*.py" -v`; **179 passed, 0 failed**.
- The run includes the new receipt version-chain tests: per effect/attempt, the first receipt has no predecessor and every later version extends the latest, preventing cross-effect/cross-attempt predecessor links and stale-predecessor forks.
- CI is test-only. No device, durable transaction, concurrency, provider, sandbox or artifact safety acceptance is implied.


## 2026-11-06 artifact-release authorization boundary clarification

- Red-team review found that the release method's earlier docstring overstated what it proves. It validates a caller-supplied authorization snapshot each time; it does not fetch/authenticate the authority or establish freshness/revocation independently. Updated the docstring and contract to state that the caller must resolve a fresh trusted decision for every release. Production needs storage-bound enforcement with principal/tenant/artifact-version/attempt/policy/scope/expiry/revocation binding.
- Added malformed artifact/receipt identifier guards to avoid unhandled type errors at API boundaries, plus explicit snapshot semantics tests. New receipt test count: 28; CI pending.


## Latest receipt/evidence composition checkpoint

- Exact tested commit: `6003375dddd51e5e11155a9144817a298d0f4cf0`
- GitHub Actions run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309075221
- Python 3.12 / Ubuntu 24.04; `python -m unittest discover -s scripts -p "test_*.py" -v`; **186 passed, 0 failed**.
- EventJournal now binds reservation events to EffectId + DispatchAttemptId before a lease exists (no fence yet), then requires the current fence for all attempt-bound events after the first lease. FakeCoordinator derives receipt evidence refs and payload digests only from accepted events for the exact effect/attempt; quarantined conflicts are excluded.
- New integration tests cover accepted evidence binding, conflict exclusion, receipt version creation from later observations, and safe reservation replay after a lease exists.
- This remains an in-memory research model. No durable storage, concurrent transaction guarantee, real producer authentication, real policy check, mobile/device integration or artifact release is established. Fetch live branch head before relying on this CI result.


## 2026-11-06 — coordinator-to-receipt evidence binding CI green

- Exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309075221 at `6003375dddd51e5e11155a9144817a298d0f4cf0`; Ubuntu 24.04 / Python 3.12; `python -m unittest discover -s scripts -p "test_*.py" -v`; **186 passed, 0 failed**.
- FakeCoordinator now creates receipt evidence references/digests from accepted journal events for the exact EffectId/DispatchAttemptId. Quarantined conflicts are excluded. A later accepted event can be captured in a new linked receipt version without mutating the predecessor.
- Reservation events are attempt-bound before a lease fence exists; lease-scoped events still require the current fence. This fixes the earlier inability to record reservation evidence before first claim.
- Limits: all are in-memory research models; no durable transaction, concurrent writer guarantee, cryptographic producer authentication, real provider, device, sandbox or production artifact authority.


## 2026-11-06 terminal verdict fail-closed gate

- Red-team review of the new coordinator-to-receipt composition found that the builder accepted caller-supplied PASS/FAIL even though its journal currently contains only dispatch/recovery lifecycle evidence. That would allow dispatch evidence to be packaged with a false terminal claim.
- FakeCoordinator receipt composition now accepts only INCOMPLETE until trusted terminal lifecycle + natural child-exit evidence or trusted program-failure evidence is integrated and projected through `execution_projection.py`. PASS/FAIL are rejected with no receipt append. Added regression test.
- This is a temporary fail-closed model boundary, not a change to canonical verdict semantics. Next integration must derive terminal verdicts from typed evidence, never accept a caller-supplied label as proof.


## 2026-11-06 — dispatch-only terminal verdict gate CI green

- Exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42309370781 at `78286ad6b802a7925a2d7bba6dfb472dfde5c2a3`; Ubuntu 24.04 / Python 3.12; `python -m unittest discover -s scripts -p "test_*.py" -v`; **187 passed, 0 failed**.
- FakeCoordinator receipt composition currently permits only INCOMPLETE because its accepted journal events prove dispatch/recovery, not terminal program success/failure. Caller-supplied PASS/FAIL are rejected; future terminal outcomes must be derived through typed execution evidence and `execution_projection.py`.


## 2026-11-06 typed terminal evidence integration started

- Added FakeCoordinator append methods for typed lifecycle, exit and program-failure observations, plus reconstruction of a `VerdictProjection` from accepted attempt-bound journal events using journal sequence numbers.
- Receipt composition now derives the outcome from accepted evidence; an optional caller label must equal the projection. Projection reason is stored in the immutable receipt hash. Multiple observations of the same kind currently fail closed to INCOMPLETE/reconciliation rather than guessing a precedence.
- Added PASS/FAIL/INCOMPLETE integration tests. CI pending. These methods remain an unauthenticated in-memory model; production producer authentication and event schema validation are not implemented.


## 2026-11-06 — terminal observation fencing and journal scope CI green

- Exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310127313 at `f82e853323d9c0c526eeaa8ad31cb47da199e249`; Ubuntu 24.04 / Python 3.12; full Python suite **199 passed, 0 failed**.
- EventJournal duplicate identity now includes EffectId/DispatchAttemptId scope as well as source/event ID and producer/payload identity. A source event cannot silently alias another attempt.
- FakeCoordinator requires terminal observations to come from the current unexpired dispatch lease. Expired/reconciling workers cannot append terminal facts; they must use authoritative reconciliation. Valid non-object JSON payloads project to INCOMPLETE instead of raising.
- Receipt outcomes are reconstructed from accepted typed observations via `execution_projection.py`; caller-supplied outcome mismatches are rejected and projection reason is fingerprinted into the immutable receipt.
- Model limitations remain: in-memory, synchronous, no durable atomicity/concurrent safety, producer cryptographic authentication, device, provider or sandbox acceptance.


## Typed terminal evidence and current release gate checkpoint

- Exact tested commit: `fd41883364e98e9c2ee306e89a8140f5566083a9`
- CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310308543, Ubuntu 24.04 / Python 3.12, **201 passed, 0 failed**.
- FakeCoordinator now derives PASS/FAIL/INCOMPLETE via `execution_projection.py` from accepted attempt-bound lifecycle, direct-child exit and trusted program-failure observations. Caller-supplied verdict and lifecycle disposition must match the projection. Multiple same-kind observations and stale-fence terminal evidence fail closed to INCOMPLETE.
- Terminal observations require a current unexpired dispatch lease; expired/reconciling attempts must use authoritative reconciliation. This remains a caller-constructible in-memory model, not cryptographic producer authentication.
- Artifact release now binds to a receipt manifest, exact object version, attempt, principal/tenant, operation scope, authorization snapshot, expiry and revocation flag, and rechecks on every request. The authorization snapshot is still caller supplied, not an external policy decision.
- Current receipt publication and artifact storage are in-memory; no durable transactions, actual mobile release, malware scanning or provider integration are established. Fetch live head and exact-SHA CI before relying on this checkpoint.


## 2026-11-06 — monotonic lifecycle projection CI green

- Exact-SHA run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42310444948 at `b6eef9a8cc1df704ff2519a69fb9e347a2bcedf9`; Ubuntu 24.04 / Python 3.12; full suite **205 passed, 0 failed**.
- Lifecycle projection now reduces monotonic nonterminal progression (`accepted → queued → running`) and permits at most one terminal lifecycle state. It rejects regressions, terminal-state forks, unknown status strings and non-string status payloads. PASS still requires trusted succeeded lifecycle plus natural direct-child exit 0.
- This is an in-memory conformance model. It does not establish durable/concurrent event storage, cryptographic producer authentication, mobile, provider, sandbox or production release behavior.


## 2026-11-07 — reservation exception and fence-bound duplicate identity green

- Exact-SHA CI: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42311165889 at `e631e9ccda29e5632832a64ad6b5e8c4c0ae5765`; Ubuntu 24.04 / Python 3.12; full suite **211 passed, 0 failed**.
- Reservation is an attempt-bound, pre-lease event and stays unfenced. FakeCoordinator now explicitly uses `require_fence=False` only for initial reservation and reservation repair, so the same reservation event remains idempotent after a worker claim. Passing a fence to this path is rejected.
- EventJournal exact replay now also compares fence generation. Same source/event ID and same producer/payload/attempt under a new fence is quarantined, not treated as a duplicate. All worker events still require the current fence.
- CI failures encountered while building this edge case were resolved: first test fixture now initializes fence 1 before testing fence 2; reservation replay/repair uses the unfenced pre-lease identity. No remaining failures on exact tested SHA.
- Limitations remain: in-memory only, no durable transaction/concurrent writer guarantee or cryptographic producer authentication; no mobile/provider/sandbox/production acceptance.
