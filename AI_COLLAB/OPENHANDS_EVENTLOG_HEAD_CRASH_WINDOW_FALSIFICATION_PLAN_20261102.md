# OpenHands EventLog / active-HEAD crash-window falsification plan

**Date:** 2026-11-02  
**Status:** PROPOSED TEST SPECIFICATION ONLY / NOT EXECUTED  
**Purpose:** Falsify or confirm the source-derived hypothesis that an event can be durably appended to OpenHands EventLog while the persisted ConversationState active leaf (HEAD) remains on the previous event after a crash.

## 1. Scope and evidence boundary

Pinned reference source:
- Repository: `OpenHands/software-agent-sdk`
- Ref: `98849457621881ae2414719b82b8bc1cf535b4ab`
- Relevant source reviewed: `openhands-sdk/openhands/sdk/conversation/event_store.py`, `openhands-sdk/openhands/sdk/conversation/state.py`, `openhands-sdk/openhands/sdk/io/local.py`, `openhands-sdk/openhands/sdk/io/base.py`, and agent-server lease/event-service code.

The source review observed that `ConversationState.append_event(event)` calls EventLog append before assigning `leaf_event_id`; the leaf assignment then persists the base-state snapshot separately. The two writes are individually protected by the EventService guarded-write mechanism when used through that service, but they are not one atomic transaction.

**Hypothesis under test:** If the process terminates after the event file is durably written but before the new `leaf_event_id` is durably saved, restore may retain the old, still-existing leaf as active HEAD. The new event may remain readable in the EventLog but not be part of the active branch.

This is not yet a demonstrated defect. No test has been executed by ChatGPT. The plan below is a future, disposable test against the pinned source, not a PocketCode acceptance case and not a claim about PocketCode implementation.

## 2. Required harness properties

Use a disposable local filesystem directory, one conversation, a deterministic event fixture, and a fresh process for every crash/restart boundary. Do not use NFS, network shares, cloud-synced folders, or a shared production store. The source explicitly warns that file locking is unreliable on NFS/network filesystems.

The harness must:
1. Pin and record the exact source commit and dependency lock state.
2. Create a conversation with a known persisted base state and an existing event `E0` that is the active leaf.
3. Prepare a new event `E1` with a unique event ID and `parent_id=E0`.
4. Instrument named persistence boundaries without changing the logical ordering under test.
5. At each boundary, terminate the writer process abruptly, not by raising a normal exception that may run cleanup/finally handlers.
6. Start a separate restore process using only persisted files.
7. Capture raw directory listing, event JSON bytes/hashes, length marker/index state, base_state JSON bytes/hash, restored `leaf_event_id`, EventLog sequence/index, parent path from restored leaf, and any gap/repair diagnostics.
8. Repeat each boundary at least 20 times or use deterministic crash hooks that make the exact boundary reproducible. Report the exact number of repetitions and outcomes.
9. Keep event-file durability distinct from the return value of the append call. A successful in-process return alone is not proof that data survived process termination or power loss.
10. Avoid claiming power-loss durability from process-kill tests. If power-loss behavior matters, it needs a separate filesystem/VM crash harness and documented storage assumptions.

## 3. Fault-injection boundaries

| ID | Kill point | Expected persisted state to inspect | Question |
|---|---|---|---|
| OH-HEAD-FI-01 | Before EventLog append begins | Only E0 and old base snapshot | Does restore remain unchanged? |
| OH-HEAD-FI-02 | During E1 event-file write, before atomic file replacement/commit completes | E1 absent, partial, or complete depending on actual write primitive and kill point | Is a torn/partial event ignored or reported safely? |
| OH-HEAD-FI-03 | Immediately after E1 event file is committed, before append returns / before leaf assignment | E1 exists; base snapshot should still name E0 | Does restore keep E0 active while E1 is present/readable? |
| OH-HEAD-FI-04 | After EventLog.append returns, immediately before `leaf_event_id` assignment | E1 exists; base snapshot names E0 | Same orphaned-event/old-HEAD question, with append completion known |
| OH-HEAD-FI-05 | During base_state atomic write for new leaf, before replace | Determine whether old or new snapshot survives; never assume | Is snapshot replacement atomic under this harness? |
| OH-HEAD-FI-06 | Immediately after new base_state replacement completes | E1 exists; base snapshot should name E1 | Does restore select E1 and preserve parent path? |
| OH-HEAD-FI-07 | After append and leaf save, before caller receives success | E1 and HEAD may both be durable although caller saw no acknowledgement | Does retry create duplicate/conflicting event or is exact-ID replay handled safely? |
| OH-HEAD-FI-08 | During concurrent lease takeover attempt around guarded append and guarded HEAD save | Record lease owner/generation and which writes committed | Can takeover interleave between the two separately guarded writes, and what state is visible to the new owner? |

For OH-HEAD-FI-08, use two processes and a controllable lock/barrier. Verify the lock is actually shared by the selected local filesystem. Do not infer that a lease generation fences external side effects; this test covers only the guarded persistence calls.

## 4. Assertions and classification

For every restored state, classify the following independently:

- **Event durability:** E1 absent / partial-invalid / present-valid.
- **EventLog discoverability:** E1 indexed and readable / present but gap or index repair / not discoverable.
- **Active HEAD:** E0 / E1 / missing or repaired fallback / other.
- **Active ancestry:** whether the path from restored HEAD contains E1 and E0 in the expected parent order.
- **Append acknowledgement:** writer received success / did not receive success / unknown.
- **Lease ownership:** owner and generation at each guarded write, if EventService is in scope.
- **Recovery action:** no-op / index rebuild / missing-leaf fallback / explicit reconciliation required.

Do not collapse these into one PASS/FAIL result. In particular:
- E1 being present in the event directory does not prove E1 is active.
- E1 being active after restore does not prove the caller received an acknowledgement.
- A missing E1 file does not prove the append never began.
- A successful lease check does not prove an external provider action was fenced.
- A process-kill result does not prove power-loss durability.

## 5. Falsification criteria

The specific orphaned-event/old-HEAD hypothesis is **confirmed for the tested source/environment** only if OH-HEAD-FI-03 or FI-04 reproducibly yields all of:
1. a valid, persisted E1 event file;
2. successful EventLog discovery of E1 after fresh restore;
3. persisted base_state still naming E0;
4. restore selecting E0 as active leaf; and
5. E1 absent from the active ancestry/path returned from E0.

The hypothesis is **not reproduced in the tested environment** if every deterministic kill at FI-03/FI-04 results in either E1 not being durably present or restore selecting E1 as active HEAD, across the stated repetitions. This does not prove absence under other filesystems, versions, or power-loss conditions.

The hypothesis is **inconclusive** if instrumentation changes ordering, the process does not die at the intended boundary, the event file or base snapshot cannot be classified, or the test uses a different source revision without recording it.

A confirmed orphan is a source/version-specific consistency defect or documented behavior requiring design review. It is not automatically a PocketCode requirement or a reason to copy/replace the storage architecture.

## 6. Retry and reconciliation cases

After each crash state, separately test a caller retrying the same logical event:
- same event ID and byte-identical payload;
- same event ID with changed payload;
- new event ID with same logical operation;
- same event with a different parent;
- delayed retry after a later event has become active.

Record whether duplicate detection is idempotent, rejects conflict, or creates a second logical event. Do not assume event-ID uniqueness provides operation idempotency.

Also test a stale/missing leaf separately from the orphan case. OpenHands restore reportedly repairs a missing saved leaf by moving to the last surviving real event; that behavior must not be confused with a still-existing old leaf. A fallback to the last event may also be wrong for branched histories unless branch selection is explicit.

## 7. Mapping to PocketCode owner decisions (no decisions made)

- **Lifecycle D-04 (OPEN):** informs the need to define authenticated event identity, parent/order semantics, replay/conflict behavior, immutable observations, gap reporting and active-branch selection. OpenHands EventID, disk sequence, dense index, parent_id and leaf_event_id remain distinct source concepts, not PocketCode field names.
- **D-05 (BLOCKED):** a persistence lease/generation does not prove that the exact policy revision was atomically applied before execution starts.
- **D-06 (owner-open):** event append or lease fencing does not make a provider request idempotent and does not resolve an ambiguous dispatch whose acknowledgement was lost.
- **D-08 (owner-open):** event journal behavior alone does not define durable report history, tombstones, retention, versioning or deletion semantics.
- **RevDev:** do not map this model onto native MissionId/RunId, RelayRef, P8U or publication/remediation states. RevDev PC/runtime/queue state remains UNKNOWN.

No new canonical LOOP/CASE/COORD/DR/SCF/P8U acceptance ID is assigned here. If the owner later wants this behavior in PocketCode acceptance, first trace it to the existing native IDs and record an explicit owner decision.

## 8. Required evidence in a future result

A useful report must include:
- exact source commit, file paths, symbols and line ranges;
- OS, filesystem type/mount options, Python/runtime and dependency versions;
- exact test command and harness commit/hash;
- each kill point and how it was deterministically reached;
- repetitions and raw per-run classifications;
- before/after hashes for event files and base_state;
- restore logs and active ancestry;
- whether EventService lease guards were enabled;
- deviations from source behavior and any harness instrumentation;
- explicit statement whether this was process termination or simulated power loss.

## 9. Non-actions and current status

This document is a design for future falsification only. It does not report execution. No OpenHands tests, builds, provider calls, device runs, persistence services, PocketCode source/tests/schema, canonical acceptance, PR #2/#3, Actions, deployment, account, billing, or PC/RevDev host/queue operations were performed. No provider or store is selected. All RevDev PC state remains UNKNOWN.


## 10. Source refinement: agent-server has an explicit interrupted-tool recovery path — 2026-11-02

A second exact-ref read of the pinned source found an important qualification that must be included in any result. At the same pinned commit `98849457621881ae2414719b82b8bc1cf535b4ab`:

- `openhands-sdk/openhands/sdk/conversation/state.py` lines 342–364 confirms append then leaf assignment. Lines 632–655 show public-field autosave; the base-state write occurs after assignment and is separately guarded when a write guard is configured.
- `openhands-agent-server/openhands/agent_server/event_service.py` lines 1424–1467 explicitly recognizes this crash window. On loading a conversation whose persisted `execution_status` is RUNNING, it marks status ERROR, scans the **full event log** for unmatched actions, and if the first unmatched action has no observation-like event for its `tool_call_id`, appends a non-retryable internal AgentErrorEvent with `parent_id=first_action.id`. The source comment says this explicit parent avoids attaching the recovery result to stale HEAD as a sibling and leaving an orphan tool result on the active branch.
- `state.py` lines 268–320 clarify that a set, still-existing leaf is returned as-is; missing-leaf repair only runs when the saved leaf event file is absent. A still-existing stale leaf is not automatically advanced to the last event by that repair helper.

This means the underlying append/HEAD non-atomicity is directly acknowledged by the source, and the server contains a targeted recovery mechanism for interrupted tool actions. It would be inaccurate to describe the current source as having no recovery. It would also be inaccurate to conclude that the recovery closes every possible gap: the recovery is conditional on the restored state being RUNNING, on finding an unmatched action, and on no observation-like event already existing for that tool_call_id. It appends an interruption error rather than proving the original tool side effect did not occur.

### 10.1 Required additional tests

Add the following to the future harness before drawing a product conclusion:

| ID | Setup / fault | Required assertion |
|---|---|---|
| OH-HEAD-FI-09 | Crash after action event file commits but before leaf autosave; persisted execution_status=RUNNING; restore through EventService | Full-log scan finds unmatched action; recovery error is explicitly parented to that action; restored active branch includes action then recovery error; no sibling/orphan result |
| OH-HEAD-FI-10 | Same crash state but persisted execution_status is not RUNNING | Determine whether EventService intentionally skips interrupted-tool recovery; document resulting active branch and any stale action visibility |
| OH-HEAD-FI-11 | RUNNING state, matching ObservationBaseEvent already exists anywhere in full log for the tool_call_id | Verify duplicate suppression and whether active ancestry is still coherent; a log-wide match must not silently hide a missing active-branch observation |
| OH-HEAD-FI-12 | Multiple unmatched actions in full log | Verify the first-action selection and whether one recovery error is sufficient or later unmatched actions remain unresolved |
| OH-HEAD-FI-13 | Observation matches tool_call_id but has a different action association | Verify the intentional tool_call_id-based duplicate suppression and whether it can suppress recovery for the wrong action |
| OH-HEAD-FI-14 | Crash after external tool side effect but before observation persistence, then restart recovery | Verify user-facing result remains interrupted/unknown; do not claim the side effect did not occur or automatically redispatch it |

Also record whether recovery's `_conversation._on_event(error_event)` is routed through the same write guard and whether the recovery append and any status/HEAD saves remain separate writes. Do not assume a recovery event is transactionally coupled to execution_status=ERROR.

### 10.2 Revised interpretation

The generic FI-03/FI-04 cases still test the SDK persistence boundary. FI-09..14 test the agent-server's application-level recovery path. Report both layers separately:
- **SDK persistence property:** event append and active-HEAD snapshot are separate operations; a stale still-existing leaf can remain the effective HEAD.
- **Agent-server recovery property:** a RUNNING conversation with an unmatched action is reconciled by a non-retryable interruption error explicitly parented to the action, subject to the conditions above.
- **External side-effect property:** remains outside this mechanism. The recovery record does not prove whether a tool/provider side effect happened before the crash and must not authorize automatic retry.

No test has been run. This refinement narrows the hypothesis and test scope; it does not change PocketCode D-04/D-05/D-06/D-08 or select OpenHands as a store.


## 11. Existing pinned tests and integration recipe found — 2026-11-02

A targeted source search found that this recovery path already has meaningful test coverage in the pinned OpenHands tree. This changes the purpose of the proposed plan: avoid duplicating the existing tests; focus only on gaps they do not prove.

### 11.1 Existing unit-test coverage

Pinned file `tests/agent_server/test_event_service.py`, blob `fc6e589f71318ac36df92b72c1fd0225549d1436`, lines 2419–2678, contains `TestEventServiceStartWithRunningStatus`:
- `test_start_sets_error_status_when_running_from_disk` (2423 onward): mocked RUNNING state with one unmatched action; asserts status becomes ERROR and exactly one AgentErrorEvent is emitted with tool_name/tool_call_id and restart wording.
- `test_start_does_not_add_error_event_when_no_unmatched_actions` (2506 onward): RUNNING but no events; asserts ERROR and no AgentErrorEvent.
- `test_start_does_nothing_when_status_not_running` (2560 onward): IDLE; asserts status unchanged and no recovery event.
- `test_start_skips_error_event_when_observation_already_exists` (2610 onward): matching tool_call_id but different action_id; asserts duplicate suppression.

The inspected assertions do **not** verify that the synthesized AgentErrorEvent has `parent_id=first_action.id`, nor do they restore real persisted files and assert active ancestry. They use a mocked LocalConversation and a MagicMock state. The existing tests validate branch conditions and event emission, not the actual crash/persistence/restore sequence.

Pinned file `tests/sdk/conversation/test_get_unmatched_actions.py`, blob `35798b1bccb60b0976cf0785682ef17181e4450b`, covers unmatched-action classification, ObservationEvent/UserRejectObservation/AgentErrorEvent matching by tool_call_id, different tool_call_id non-matching, and mixed responses. This is SDK helper coverage, not server process-crash integration.

### 11.2 Existing documented integration scenario

Pinned feature map `.agents/skills/verify-agent-server/references/feature-map/F31-persistence-and-limits.md`, blob `5082730e1ba1d333daeaf321c21214ad4924cd12`, defines `F31.crash-tool-call` at lines 191–220. It starts a stubbed terminal sleep, waits until one ActionEvent exists and base_state says RUNNING, SIGKILLs the server, restarts, then asserts:
- conversation status is ERROR;
- exactly one AgentErrorEvent exists for the same tool_call_id with restart wording;
- there are zero ObservationEvents;
- after rewriting the stub and resuming, the model receives the error as the tool result and the conversation finishes.

The recipe's preconditions currently include a DeepSeek API key/model for the broader F31 verification run. ChatGPT did not execute it. The documented integration assertions do not inspect AgentErrorEvent.parent_id or the restored active-branch ancestry. The integration scenario is therefore a useful existing baseline, not proof of every branch/HEAD invariant.

### 11.3 Revised minimum new work

Do not recreate the already-covered unit scenarios. The smallest high-value additions are:
1. Extend the unit assertion to require `error_event.parent_id == unmatched_action.id`.
2. Add a real LocalFileStore persistence/restore test that creates E0, writes an ActionEvent E1, crashes between event append and leaf autosave, restores through EventService with RUNNING status, and asserts active ancestry E0 → E1 → recovery AgentErrorEvent.
3. Add a paired non-RUNNING persisted-state test showing whether the unmatched action remains outside active ancestry without recovery; record this as intentional behavior or a gap, not an automatic defect.
4. Add a case where a matching ObservationBaseEvent exists in the full event log but is not on the active ancestry; verify whether log-wide suppression is correct for the supported no-remote-branching model.
5. Add a multi-unmatched-action case and assert which actions receive recovery records. Current source selects only `unmatched_actions[0]`; do not assume later unmatched actions are reconciled.
6. Keep external side-effect ambiguity separate: SIGKILL after tool side effect but before observation persistence must not be interpreted as proof of non-execution or safe retry.

The original FI-01..08 SDK persistence boundaries remain useful only if the exact crash hook can be installed without changing ordering. For an end-to-end recovery test, the documented F31 SIGKILL scenario is the better baseline; avoid adding paid-model requirements by constructing a fully local stub-only harness if feasible, but do not claim equivalence until its control flow is verified.

No source tests were run by ChatGPT. These are source-presence and test-assertion reviews only. No code/test file was modified.


## 12. Event-file and length-marker ordering refinement — 2026-11-02

The pinned EventLog append order at `openhands-sdk/openhands/sdk/conversation/event_store.py` lines 288–297 is:
1. write the event JSON through FileStore;
2. update in-memory disk/index maps and length;
3. advance the sidecar length marker by deleting the prior marker and writing the new marker.

The marker helper at lines 320–330 deliberately deletes the old marker first, so an interrupted marker update should leave no marker rather than a stale marker claiming the new length. A later append can detect marker mismatch and count/scan event files. LocalFileStore string writes use `atomic_write_text` at `io/local.py` lines 63–68. The base snapshot uses the same FileStore string-write path.

Add explicit instrumentation around:
- after event JSON replacement but before in-memory map/length updates;
- after in-memory update but before marker deletion;
- after old marker deletion but before new marker write;
- after new marker write;
- during fresh EventLog construction/index scan and during append-time marker-mismatch rescan.

These boundaries help separate a missing marker/index-cache issue from the active-HEAD issue. A fresh-process restore is required because the original LocalFileStore cache is not authoritative after restart. Do not call a file atomically replaced “power-loss durable”: atomic rename/replace protects against partial visibility under the tested local filesystem, but the reviewed source alone does not prove fsync or stable-media persistence. The test must report process-crash survival separately from power-loss durability.


## 13. Higher-priority recovery gaps: multi-action batches and navigated branches — 2026-11-02

A deeper source pass found two supported execution/history features that make the existing recovery edge cases more important. These remain source-derived hypotheses requiring tests, not confirmed product defects.

### 13.1 Multiple tool calls are normal, persisted before batch execution

Pinned source evidence:
- `openhands-sdk/openhands/sdk/event/base.py` lines 181–200 explicitly says multiple ActionEvents are received for one LLM message when it returns multiple parallel tool calls.
- `openhands-sdk/openhands/sdk/agent/response_dispatch.py` lines 224–255 (`_ahandle_tool_calls`) iterates each tool call and invokes `_get_action_event(... on_event=...)` before calling `_aexecute_actions` on the complete list. The same order is present in sync `_handle_tool_calls` lines 170–200.
- `openhands-sdk/openhands/sdk/agent/agent.py` lines 695–716 calls `_ActionBatch.aprepare`; `_ActionBatch.aprepare` lines 327–352 awaits the whole parallel executor batch and only then returns results; `_ActionBatch.emit` lines 354–381 emits result/observation events afterward.
- `openhands-sdk/openhands/sdk/agent/parallel_executor.py` lines 128–191 runs multiple actions concurrently with `asyncio.gather` (or serially when max workers is 1), returning the batch results only after all calls complete.
- `ConversationState.get_unmatched_actions` lines 713–752 returns all unmatched executable actions in chronological order.
- Startup recovery at `openhands-agent-server/openhands/agent_server/event_service.py` lines 1436–1467 currently chooses only `unmatched_actions[0]` and emits one AgentErrorEvent explicitly parented to that first action.

Implication to test: if a multi-tool response has ActionEvents A1, A2, A3 persisted before execution and the process dies before batch result events are emitted, recovery currently creates a result only for A1. Because A2/A3 were appended after A1, their parent chain may be cut off from the new active leaf when the recovery event is explicitly parented to A1. The exact resulting active branch, unmatched set and subsequent LLM request must be asserted, not inferred. The separate interrupt path is different: `LocalConversation._emit_orphaned_action_errors` at lines 2777–2805 loops over all unmatched actions on the active branch and emits a synthetic error for each. Do not confuse this interrupt behavior with startup recovery.

Add cases:
- OH-HEAD-FI-15: 2+ tool calls in one LLM response; kill after all ActionEvents persisted but before batch results emitted. Assert all persisted actions, recovery error count, parent IDs, active ancestry, remaining unmatched actions, and model-facing reconstructed tool-call history.
- OH-HEAD-FI-16: one tool side effect completes while another parallel tool remains blocked; kill before batch emit. Verify the recovery record(s) do not imply which side effects completed and no action is automatically redispatched without explicit authorization.
- OH-HEAD-FI-17: repeat with `tool_concurrency_limit=1` to distinguish serial execution from multi-worker concurrency. Actions may still all be recorded before the first tool runs; inspect actual behavior.
- OH-HEAD-FI-18: compare startup recovery with the interrupt path, which emits errors for all active-branch orphans. Assert whether the difference is intentional and whether startup recovery leaves an incomplete batch.

### 13.2 Full-log suppression versus supported navigate/rewind

The earlier concern about a matching observation on a non-active branch was prematurely treated as likely synthetic. Pinned source explicitly supports navigation that leaves abandoned events on disk:
- `openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py` lines 988–1011: `navigate_to` moves HEAD to an existing event; all branches stay on disk, appending after navigation creates a sibling, and abandoned events remain in the log but drop out of the active view.
- `openhands-sdk/openhands/sdk/conversation/impl/remote_conversation.py` lines 1914–1943: `RemoteConversation.navigate_to` calls the server `/navigate` route and refreshes cached state.
- `openhands-agent-server/openhands/agent_server/event_service.py` lines 2358–2372 exposes the navigate operation.
- F10 feature map `F10-fork-navigate-condense-ask.md` lines 34–38 and 295–328 documents that navigation does not delete abandoned events and that the next append branches from the selected HEAD.
- Yet startup recovery at `event_service.py` lines 1431–1446 scans the full event log and suppresses recovery if any ObservationBaseEvent shares the first action's tool_call_id.

This creates a concrete falsification case: an action A has observation O on a later branch; the user navigates HEAD back to A, leaving O in the full log but outside active ancestry; a new run re-enters the pending action path; the tool is interrupted; startup sees the old O in the full log and may suppress the recovery error even though O is not on the active branch. Whether this exact state is reachable with the persisted RUNNING lifecycle and whether the intended semantics make re-execution user-authorized must be checked. The source comment that remote branching is unsupported (#3749) must be reconciled with the separately documented and exposed navigate/re-root API; do not silently treat those as identical concepts.

Add cases:
- OH-HEAD-FI-19: create A→O, navigate HEAD back to A, verify O remains in EventLog but is absent from active_branch; then reproduce RUNNING/startup recovery and inspect whether full-log suppression occurs.
- OH-HEAD-FI-20: repeat with a different tool_call_id observation to verify suppression is identity-scoped.
- OH-HEAD-FI-21: repeat after appending a sibling branch from A, with and without an observation on that sibling; assert recovery and active ancestry.
- OH-HEAD-FI-22: inspect intended user semantics for navigate-back-to-pending-action followed by send_message/run. Establish whether this is a deliberate re-execution path, a stale-result suppression bug, or an unsupported sequence.

### 13.3 F31 crash scenario: local stub qualification

The F31 crash-tool-call recipe creates `qa-f31-tool` with `fixture llm-stub`, builds `TOOL_AGENT` with model `openai/qa-stub`, a placeholder `qa-stub-key`, and `base_url=$TOOL/v1`, then creates conversation T with that inline agent (feature map lines 103–121). The crash scenario at lines 191–220 drives T through that stub, SIGKILLs the server while the stubbed terminal action is running, then rewrites the stub to finish and resumes the run. No actual DeepSeek completion is part of T's described request path.

The enclosing F31 setup also runs `llm preset deepseek` (line 109), and the broader F31 feature family contains DeepSeek-backed subfeatures. Do not claim the entire F31 suite is provider-free. The narrower crash-tool-call path appears to be local-stub-backed; verify whether the preset command is merely unrelated default setup or a required no-key prerequisite before publishing a standalone stub-only recipe. No F31 test has been executed by ChatGPT.

### 13.4 Priority update

Priority order for independent review and any future test work:
1. Multi-action startup recovery and active-branch truncation (FI-15..18).
2. Full-log observation suppression after supported navigate/rewind (FI-19..22).
3. Real persisted-file crash/restore parent_id + active ancestry assertion (FI-09..14).
4. EventLog marker boundaries and process-crash versus power-loss distinction.

The no-abandoned-branches explanation in the startup comment must be reconciled against the supported navigate API before treating FI-19..22 as merely synthetic. No upstream tests were run or modified. No PocketCode acceptance ID or owner decision changed.


## 14. Recovery error wording versus external side-effect uncertainty — 2026-11-02

The startup-created AgentErrorEvent text at `event_service.py` lines 1458–1462 states: “A restart occurred while this tool was in progress ... The tool execution was interrupted and did not complete.” Its classification is INTERNAL and `retryable=False` (lines 1463–1465).

That wording is stronger than the evidence necessarily supports. In a parallel batch, a tool may complete an external side effect and return a result into the in-memory batch while another tool remains blocked; because _ActionBatch.aprepare awaits the whole batch and _ActionBatch.emit persists results only afterward, a process crash can occur after one side effect completed but before any batch observation is emitted. Startup's synthetic error cannot know whether the side effect completed. The same ambiguity can occur for a single tool that completes its external effect immediately before process death but before its observation is durably appended.

Add an explicit assertion to FI-16 and the real integration harness: preserve the external side-effect ledger independently from conversation events, kill after the side effect is confirmed but before observation persistence, then assert the recovery event does not claim a verified negative execution outcome. If the current user-facing error string claims “did not complete,” report this as a semantic overstatement even if automatic retry is disabled. Do not conflate retryable=False with proof of non-execution or with provider idempotency.

For PocketCode's crosswalk, translate this only into a design warning: an interruption record should state that the result/evidence was not persisted and the external outcome is unknown unless independently proven. This does not make an OpenHands implementation decision or a PocketCode owner decision.


## 15. Reconcile the `#3749` comment against the issue itself — 2026-11-02

The startup comment at `event_service.py` lines 1431–1435 says remote branching is unsupported and cites #3749 as the reason there are no abandoned branches to exclude. Fetching OpenHands issue #3749 shows it is titled **“[Feature] Conversation history tree: agent-server HTTP exposure (fork/navigate/schema) (3/3)”**, is closed, and its body explicitly specifies the HTTP `POST /{id}/navigate` route, the `navigate` operation, branch-aware `parent_id`/`leaf_event_id`, and acceptance that `GET /events/search` still returns all branches after navigation. The pinned source and F10 feature map independently expose and test this navigation behavior.

This makes the code comment's citation appear contradictory or stale. Do not assume the issue's closure proves every branching mode is supported, but do require Gemini to inspect the merge/commit and explain precisely what “remote branching unsupported” means in the recovery comment. Distinguish: (a) concurrent/multi-writer branching, (b) creating separate forked conversations, (c) in-place navigate/re-root that leaves abandoned branches in the same EventLog. The last is explicitly supported by the pinned API docs/source. The recovery's full-log observation suppression must be tested against that behavior unless a stronger invariant prevents the relevant RUNNING state.


### 15.1 PR description cross-check

The closed PR search for #3749 surfaced two related PR descriptions:
- The SDK tree foundation PR describes `LocalConversation.navigate_to()` and says the remote wrapper was temporarily `NotImplementedError` until the HTTP surface in #3749.
- The agent-server PR for #3749 says it exposes the tree over HTTP, adds `POST /api/conversations/{id}/navigate`, and wires `RemoteConversation.navigate_to()` to call the new endpoint and refresh cached state instead of raising `NotImplementedError`.

This makes the narrow interpretation clear: a pre-#3749 SDK stage lacked the remote API, but the later pinned revision has remote navigate/re-root. The recovery comment's assertion that “remote branching is unsupported” therefore cannot be read as “remote navigate/re-root is unavailable.” It may still mean concurrent/multi-writer branching is unsupported; Gemini should identify the exact invariant and commit-level evolution. The documented abandoned-branch behavior remains a valid test target.


## 16. Historical crash-retry issue #2298 and active-branch re-execution path — 2026-11-02

Issue #2298 (“Duplicate observations for same tool_call_id after crash recovery”) is CLOSED. Its body documents the earlier defect where AgentErrorEvent was not counted as matching an ActionEvent, so a user resume re-executed the tool and produced both an error and an observation. The current pinned `state.py` lines 713–752 explicitly match AgentErrorEvent by tool_call_id, and the pinned SDK tests cover that behavior. Do not report the old #2298 defect as still present.

However, this does not eliminate the navigate/rewind case because two different event sequences are passed to the same helper:
- Startup recovery passes the full EventLog (`event_service.py` lines 1431–1446), so an observation on an abandoned branch can mark the action as already observed and suppress a recovery error.
- Normal agent pending-action detection uses `state.active_branch()` (`agent.py` lines 747–756), so the same abandoned observation is excluded and the action remains pending on the selected branch.

The F10 feature map explicitly says navigation to an earlier event leaves later events on disk but moves HEAD; a subsequent append creates a sibling. A concrete test sequence is therefore: create A→O, navigate HEAD back to A, send a new message to start a new run, let pending-action detection re-execute A (the active branch contains A but not O), interrupt that re-execution after a controlled side effect and before result persistence, then restart. If status is RUNNING, startup's full-log scan can see O from the abandoned branch and suppress the recovery error. On a later user resume, active-branch detection can still see A as pending and execute it again. Whether this exact lifecycle is valid and intended must be proven, but all constituent APIs are present in the pinned source and F10 spec. This is now the highest-priority FI-19 test.

The fix for #2298 shows why AgentErrorEvent must count as a terminal tool-result marker for the matching branch; it does not justify matching a result across abandoned branches. A correct branch-aware recovery check may need to use active ancestry plus a separate explicit crash-tail detection rule, but that is a design hypothesis for Gemini to challenge, not a recommendation to patch OpenHands.
