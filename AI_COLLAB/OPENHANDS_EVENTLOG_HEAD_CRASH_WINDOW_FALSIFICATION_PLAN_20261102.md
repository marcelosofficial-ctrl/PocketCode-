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
