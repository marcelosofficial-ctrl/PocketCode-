# Mobile interruption recovery and open-source sync audit — 2026-11-05

**Status:** Current platform-documentation and pinned source-code review. Design proposal only. No mobile stack/runtime/provider selected; no code copied into product, dependencies installed, or device tests run.

## 1. Executive decision

Adopt **durable intent + authoritative execution + resumable observation**.

The phone stores user intent, immutable request identity, prepared inputs, approvals, drafts and its last durably applied observation cursor. A selected remote host/worker owns a remote process and its authoritative lifecycle. A local mobile/browser runner owns only the work it can safely execute under its actual lifecycle and resource boundary. On reopen, PocketCode reconstructs the same run/attempt, reconciles with the execution owner and catches up observations. Reconnect must never silently redispatch the original command.

App lifecycle, network connectivity and execution lifecycle are separate axes. The phone can be offline while the remote execution is running or already complete. A local process disappearing without a terminal observation is UNKNOWN/INTERRUPTED, not success.

## 2. Platform facts and product consequences

### iOS

- `UIApplication.beginBackgroundTask` requests finite extra background time. It requires a matching `endBackgroundTask`; the expiration handler should cancel/defer work quickly. Failure to end the task can terminate the app. This is suitable for a short critical save or bounded handoff, not a long-running code-execution guarantee.
- `BGProcessingTask` can run for minutes but is interruptible, runs only when the device is idle, and is terminated when the user starts using the device. Use for opportunistic maintenance/reconciliation, not interactive coding execution.
- Background `URLSession` transfers HTTP(S) files in a system process and can survive ordinary app suspension/system termination. Background uploads must be file-backed rather than only in-memory. Transfers are rate-limited. If the user force-quits from the app switcher, background transfers are cancelled and iOS does not relaunch the app until the user opens it again.

**Decision:** background URLSession is a candidate for input/artifact transfer only. Stage upload bytes as durable files, bind transfer ID to digest/size, and verify server read-back. Do not use it as an agent/code runner, and do not claim force-quit preserved a transfer.

Sources: [beginBackgroundTask](https://developer.apple.com/documentation/uikit/uiapplication/beginbackgroundtask%28expirationhandler%3A%29), [background execution time](https://developer.apple.com/documentation/uikit/extending-your-app-s-background-execution-time), [BGProcessingTask](https://developer.apple.com/documentation/backgroundtasks/bgprocessingtask), [URLSession background configuration](https://developer.apple.com/documentation/foundation/urlsessionconfiguration/background%28withidentifier%3A%29), [background transfers](https://developer.apple.com/documentation/foundation/downloading-files-in-the-background).

### Android

- Android recommends WorkManager for work that must persist after the app exits or device restarts. It stores scheduled work in its own SQLite database, handles constraints/Doze and supports retries/backoff. It is not a promise of immediate execution or unlimited compute.
- Long-running WorkManager workers use foreground services. Android 16 warns these jobs can exhaust app job quotas.
- User-Initiated Data Transfer Jobs (UIDT), from Android 14/API 34, target longer user-started transfers such as downloads, show a notification and remain subject to system-health constraints.

**Decision:** WorkManager is a candidate for bounded, persistent reconciliation/sync. UIDT is a candidate for eligible large user-initiated transfers. Neither should be used to claim indefinite untrusted code execution. Test quota and vendor-specific behavior on real devices.

Sources: [WorkManager](https://developer.android.com/develop/background-work/background-tasks/persistent), [long-running workers](https://developer.android.com/develop/background-work/background-tasks/persistent/how-to/long-running), [Android 16 foreground service changes](https://developer.android.com/develop/background-work/services/fgs/changes), [UIDT](https://developer.android.com/develop/background-work/background-tasks/uidt).

### Expo / React Native (conditional)

Current Expo `expo-background-task` wraps WorkManager on Android and BGTaskScheduler on iOS. It is deferrable, may execute later than the minimum interval, and requires system conditions such as battery/network. The docs describe a 15-minute minimum interval on Android and OS-selected timing on iOS. A task function must be registered at module/global scope because a background launch may not mount React components. The TaskManager API is unavailable on web.

**Decision:** if Expo is selected, use it for deferrable sync/maintenance only. Keep the durable journal outside React state. Do not make it the user-code execution host.

Sources: [Expo BackgroundTask current docs](https://docs.expo.dev/versions/latest/sdk/background-task/), [Expo TaskManager current docs](https://docs.expo.dev/versions/latest/sdk/task-manager/).

## 3. Competitor code audit: Happy Coder

**Repository:** [slopus/happy](https://github.com/slopus/happy)  
**Reviewed commit:** `7e32e09454c26aa78e86df0d378b1e49375b743d` (2026-11-05). **License:** MIT; license blob `da0b4ae30a42be8db9776eb887acb671b19699a0`.

This is the strongest inspected native mobile sync/recovery reference. It is a paired companion to existing agent hosts, not evidence of PC-free local execution. iOS is Swift and Android Kotlin.

### Pinned sources inspected

| File | Blob SHA |
|---|---|
| iOS `AgentConnection/SyncEngine.swift` | `79d40e2fb0a13bbdfeb0d8ac20c6dfe84824f8fb` |
| iOS `AgentConnection/SyncStorage.swift` | `d924f3b850d37a1a2af545eec5a9d9f35537e7bb` |
| iOS `Sync/IntentOutbox.swift` | `6b428b6a9f4f49e329c34f101fc9f909b5919194` |
| iOS `Chat/Sending/OutboxSender.swift` | `3c955f9150200655846ba10f49b8448f4b3ca92b` |
| iOS `docs/offline-first.md` | `4275c79345c3c5ccaa6c8566e5e357e27ff0cc1f` |
| iOS `IntentOutboxTests.swift` | `ea867d13b419cf4c040b9a35ff6694033e68147b` |
| iOS `SyncEngineTests.swift` | `5fd1cbf930696710cdd917365b6d58057953d685` |
| Android `sync/SyncEngine.kt` | `1dc13dc07b00441ca7dfb1d15e72e34b530f536b` |
| Android `sync/MessageSync.kt` | `63b337573e04e2b95dc44c8f366e72855800616f` |
| Android `sync/MessageSender.kt` | `73c2acb5c0c952bcf7ac621a30a17ea1af637fb3` |
| Android `OutboxBatchTest.kt` | `f7d6e4b5df086df51a0d4134ec0634276dbcb969` |
| Android `PendingReceiptSendTest.kt` | `52b34073bd360401224cf4be396388843aefde7b` |
| Android `SessionResumeTest.kt` | `d92618ea350fdbc5deba5152f02a814cb3fe7a39` |

Selected pinned links: [iOS SyncEngine](https://github.com/slopus/happy/blob/7e32e09454c26aa78e86df0d378b1e49375b743d/packages/happy-ios/Sources/HappyCore/AgentConnection/SyncEngine.swift), [iOS SyncStorage](https://github.com/slopus/happy/blob/7e32e09454c26aa78e86df0d378b1e49375b743d/packages/happy-ios/Sources/HappyCore/AgentConnection/SyncStorage.swift), [iOS IntentOutbox](https://github.com/slopus/happy/blob/7e32e09454c26aa78e86df0d378b1e49375b743d/packages/happy-ios/Sources/HappyCore/Sync/IntentOutbox.swift), [offline-first design](https://github.com/slopus/happy/blob/7e32e09454c26aa78e86df0d378b1e49375b743d/packages/happy-ios/docs/offline-first.md), [Android MessageSender](https://github.com/slopus/happy/blob/7e32e09454c26aa78e86df0d378b1e49375b743d/packages/happy-android/app/src/main/kotlin/com/slopus/happy/sync/MessageSender.kt).

### Reusable implementation patterns

1. Disk-first UI: render cached state immediately, reconcile afterward.
2. Persist intent/message before network dispatch.
3. Stable client IDs reused across retries; the receiver's idempotency contract matters.
4. Android sender stages attachment rows and the user-message row in one SQLite transaction, then returns local acceptance.
5. Acknowledgements remove only the exact mutation/message ID; late acknowledgement cannot erase a newer action.
6. Pending local intent is an overlay on remote snapshots, preventing stale bootstrap flicker.
7. iOS stores snapshot payload and event cursor together in a SQLite transaction.
8. iOS pauses by advancing a generation, cancelling local observation/delivery tasks and marking the connection offline; reconnect starts reconciliation again.
9. Android uses per-session locks and catch-up after reconnect/foreground return.
10. Tests cover close/reopen with pending actions, retry/backoff, refusal rollback, concurrent enqueue, stale snapshot and message receipt ordering.

### What not to copy blindly

- Its generic intent queue coalesces one pending action per logical slot. Correct for set-like desired state (rename, archive/unarchive), wrong for immutable run requests, commands, correction applications, attempts, evidence receipts and non-idempotent effects.
- The reviewed iOS `IntentOutbox` uses `try?` in storage load/update/remove paths. A load error can look like an empty pending queue; a failed removal after remote success can leave the item for replay after restart; a failed retry update may not persist the schedule. PocketCode must surface STORAGE_UNAVAILABLE/RECOVERY_REQUIRED and reconcile exact identities instead of swallowing durability failures.
- A stable client ID is not exactly-once execution. It is safe only when the server implements matching idempotency semantics and retention. Ambiguous side-effecting run requests must be reconciled against the original operation identity.
- The outbox deletes delivered intents. It is not an immutable result/evidence archive.
- Actor/process-local serialization does not prove cross-device writer fencing.
- Native Swift/GRDB and Kotlin code is coupled to Happy's protocol, types, crypto and stores. MIT permits reuse with attribution/notice, but those files are not drop-in PocketCode components.

## 4. Competitor code audit: OpenHands Mobile

**Repository:** [OpenHands/openhands-mobile](https://github.com/OpenHands/openhands-mobile)  
**Reviewed commit:** `47f815b1d111b6a71b405dcb77acb3682da59b85` (2026-09-17). **License:** MIT.

Pinned sources:
- [WebSocket hook](https://github.com/OpenHands/openhands-mobile/blob/47f815b1d111b6a71b405dcb77acb3682da59b85/src/hooks/useConversationSocket.ts), blob `6709fcb2b2960510bca80daf94ebd9db4cc0eb41`.
- [ChatScreen](https://github.com/OpenHands/openhands-mobile/blob/47f815b1d111b6a71b405dcb77acb3682da59b85/src/screens/ChatScreen.tsx), blob `a0bf15408b0650930033b54b5247db38a043b7a4`.
- [Agent API](https://github.com/OpenHands/openhands-mobile/blob/47f815b1d111b6a71b405dcb77acb3682da59b85/src/api/agent-server.ts), blob `2028e1b7a0009b50ce91e5bea4b43518ac5ebb28`.
- [Connection store](https://github.com/OpenHands/openhands-mobile/blob/47f815b1d111b6a71b405dcb77acb3682da59b85/src/storage/connection-store.ts), blob `336218d385dad94b14cec9277d871c4abe9ea618`.

Useful patterns: REST history bootstrap followed by WebSocket; explicit server-version handshake; provider/model credentials remain at the laptop/backend; remote host and direct backend paths are kept distinct with no silent cloud fallback.

Limitations in inspected code:
- The socket reconnect reuses the original timestamp anchor from initial history; no persistent advancing cursor appears in the hook.
- It resets its retry counter on socket `onopen`, before proving a stable stream. A server that opens then closes quickly can repeatedly take the minimum-delay path. This is a source-derived risk hypothesis, not a reproduced defect.
- Chat events and optimistic local sends are React component state in the inspected screen, not a demonstrated durable outbox.
- A thrown POST removes the optimistic event and restores the draft. If the server accepted but its response was lost, these files do not demonstrate durable same-ID reconciliation.
- The web connection store uses browser localStorage for host/API-key data; native uses SecureStore. Do not copy this web credential pattern without a separate threat model.

**Decision:** borrow protocol shape, version handshake and explicit host/direct modes. Do not copy the hook/send flow as PocketCode's recovery layer.

## 5. Proposed PocketCode recovery contract

### Separate lifecycles

**Client/app:** ACTIVE, BACKGROUND, SUSPENDED, RELAUNCHING, OFFLINE, RECONNECTING, CATCHING_UP, IN_SYNC, REFERENCE_EXPIRED, STORAGE_UNAVAILABLE.

**Execution authority:** CREATED/VALIDATING/ACCEPTED/QUEUED/DISPATCHING/RUNNING and terminal outcomes SUCCEEDED, PROGRAM_FAILED, TIMED_OUT, CANCELLED, REJECTED, INFRASTRUCTURE_FAILED, INTERRUPTED or UNKNOWN (only as supported by the selected boundary).

A phone UI transition does not set execution state. Socket-open is not equivalent to caught-up. Expired cursor is not an expired run.

### Persist-before-dispatch

1. Validate request and current approval/policy.
2. Allocate immutable run/attempt/request identity and payload digest. Secret values must not enter the durable digest, logs or AI packet.
3. Persist request and local dispatch intent before the first network side effect.
4. Dispatch with the exact same idempotency identity/payload.
5. Persist typed acknowledgement and remote job ID.
6. If timeout/disconnect occurs after dispatch might have started, record OUTCOME_UNKNOWN and query the original identity at the execution authority. Do not blindly re-POST.
7. Once a remote ID is known, reconnect reads/subscribes to that same run. "Run again" creates a new attempt only after safe reconciliation or explicit user choice under uncertainty.

A local database can atomically commit request+outbox only if both share one transaction. It cannot transact atomically with a remote API.

### Event cursor and replay

- Stable event ID; bound to task/run/attempt; monotonic sequence or server cursor.
- Apply event to the local projection and advance the cursor in the same local DB transaction.
- Duplicate replay is idempotent. Detect stale, out-of-order and contradictory terminal observations.
- Reconnect from last committed cursor.
- If retention no longer covers the cursor, return an explicit gap/cursor-expired signal and rebootstrap authoritative snapshot + cursor.
- Event stream is not the only result archive. Terminal receipt, output capture and artifact manifest remain durable and queryable independent of event retention.
- Progress deltas may be coalesced in display. Terminal state, approval result and receipt cannot be lost or inferred from UI.

### Cancellation

Cancel is an immutable request bound to exact run/attempt. UI stays CANCEL_REQUESTED until the execution owner confirms terminal cancellation/termination. App suspension, process death, force-quit, disconnect and request timeout are not cancellation. Local cancellation needs supervisor/process-tree termination evidence.

### Local-only execution

Use bounded deterministic slices/checkpoints where possible. Persist source/input identity and checkpoint before yielding. Non-checkpointable code may be interrupted when backgrounded; absent a trusted terminal observation it is UNKNOWN/INTERRUPTED. Never silently resume by running the whole program again. A WASM worker disappearing is not proof of a clean timeout.

## 6. Code adoption decision

| Candidate | Decision |
|---|---|
| Happy iOS SQLite/outbox sources | Reuse design/tests. If native Swift is chosen, adapt transaction/outbox boundary with MIT notice. |
| Happy Android sender/sync sources | Reuse atomic-accept, stable-ID, receipt and per-session lock patterns if native Kotlin is chosen. |
| Happy tests | Port scenarios for reopen, late ack, stale snapshot, receipt ordering and storage faults. |
| OpenHands socket hook | Do not copy as-is; missing durable cursor/outbox and reconnect weakness. |
| Expo scheduler | Conditional, sync/maintenance only. |
| iOS URLSession / Android WorkManager/UIDT | Platform adapters for transfers and bounded reconciliation only. |

**Why no code was copied now:** PocketCode's architecture document still states no client framework or runtime is selected; the current narrow MVP remains a phone-browser proof. Happy's code is native and tightly coupled to its app. OpenHands is closer to Expo, but the inspected hook is weaker than our needed guarantee. Placing unbuilt platform-specific files in the repository would create dead code and falsely imply adoption. This is a deliberate compatibility decision, not a rejection of open source reuse.

## 7. Staged implementation gates

- **G0, contract:** separate client/execution lifecycles; immutable identity; persist-before-dispatch; ambiguity reconciliation; event cursor contract; immutable receipt archive.
- **G1, fixed-task proof:** retain current phone-browser comparison and truthful report; no hosted spend or unapproved workload.
- **G2, stack selection:** compare PWA, Expo/React Native and native Swift/Kotlin on file API, local DB, credential storage, process lifecycle, persistence, transfers, accessibility, cost and maintenance.
- **G3, local journal:** transactional request+outbox, immutable attempt history, strict storage-error handling, atomic snapshot+cursor, startup recovery.
- **G4, remote execution adapter:** host owns process/output/cleanup; phone disconnect detaches observer; reconnect reads same run; cancellation is acknowledged.
- **G5, platform background adapters:** iOS background URLSession; Android WorkManager/UIDT; Expo scheduler if selected. Sync/transfer only.
- **G6, device fault tests:** background, suspension, OS kill, force-quit, reboot, network loss around dispatch/ack, event gap/duplicate/out-of-order, storage failure, remote worker continues offline, cancellation reconciliation, transfer resumption, local interruption, two-device conflict.

Trace any proposed test back to exact LOOP-01..14 and CASE-01..16 requirement text before adding IDs. Do not remap or change canonical suites in this pass.

## 8. Product features genuinely worth adding

1. Persistent run inbox with attempt history and next safe action after reopen.
2. Separate **Reconnect to this run** and **Run again** actions.
3. Honest status: "Phone offline; execution status not yet reconciled."
4. A transfer queue with digest, size, byte progress and independent retry lifecycle.
5. Correction lineage with original run and immutable later attempts, protected by workspace checkpoints.
6. Sync integrity state: saved locally, sent, acknowledged, catching up, fully reconciled.
7. Storage recovery UI that shows RECOVERY_REQUIRED rather than an empty project when the local journal cannot be read.

These deepen run/inspect/report/iterate without turning PocketCode into a generic mobile remote-control dashboard.

## 9. Non-actions

No stack/provider/host selected; $0 budget unchanged. No production source/tests changed. No upstream source copied or vendored. Happy/OpenHands source/tests inspected, not executed by PocketCode. No device lifecycle tests, provider API, secret access, workload, or spend. PR #2/#3 and canonical LOOP/CASE/AWD/D decisions unchanged. This report is research/design evidence only.
