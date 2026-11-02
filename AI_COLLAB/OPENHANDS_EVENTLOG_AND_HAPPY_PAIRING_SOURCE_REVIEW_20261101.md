# OpenHands EventLog and Happy Pairing Source Review

Date: 2026-11-01
Reviewer: ChatGPT
Type: read-only public-source review. No builds, tests, device runs, source changes or upstream actions.

## 1. Scope and pinned source identities

This review follows the earlier plan to inspect OpenHands event persistence and Happy device pairing at source level. It is not an adoption recommendation.

| Project | Repository | Branch snapshot | License |
|---|---|---|---|
| Happy | https://github.com/slopus/happy | main tree commit 323fb2e9fd0c9a44ceab9239fbc586c513f7f844 | MIT |
| OpenHands SDK | https://github.com/OpenHands/software-agent-sdk | main tree commit 98849457621881ae2414719b82b8bc1cf535b4ab | MIT |

### Happy source files

- packages/happy-android/crypto/src/main/kotlin/com/slopus/happy/crypto/PairingCrypto.kt — blob 1b0942947f04579fbd3b05ceb1cdb01be7fd6221
- packages/happy-android/app/src/main/kotlin/com/slopus/happy/connection/PairingService.kt — blob 8e283ea1bf5e49d72dd788923593dbe691a25226
- packages/happy-android/app/src/main/kotlin/com/slopus/happy/connection/PairingLink.kt — blob 9ba86f7f3d35a6183e854bddfd99d616daf32785
- packages/happy-android/app/src/main/kotlin/com/slopus/happy/connection/PairingFlow.kt — blob 82c8d0b3cc65e29d823b8b93676aea9efbb5a3a3
- packages/happy-android/crypto/src/test/kotlin/com/slopus/happy/crypto/PairingCryptoTest.kt — blob 0da9661981533ee15bbe8c869aba6fc0c87495b7
- packages/happy-android/app/src/test/kotlin/com/slopus/happy/connection/PairingTest.kt — blob 7038cde41f4ce0989f90f60b5c63c0957df90d15
- docs/encryption.md — blob 4a249bde6ac9b9ddc8457b815fd5253367cb680a
- docs/protocol.md — blob 4701e53c71810652ca547454320713efcc44701
- docs/api.md — blob fb3a451b9fbb490ffcd67ba5c8cc34d97826e53d
- packages/happy-agent/src/auth.ts — blob 3427d6cf382c992750399ea64c89c0ddd9941af3
- packages/happy-agent/src/credentials.ts — blob 81c8871e3c576c8da526b59273d30e5f74c49768
- packages/happy-android/app/src/main/kotlin/com/slopus/happy/auth/CredentialStore.kt — blob af92bb1b14ed80ed04a225d1840b4fcf2d687b04

### OpenHands source files

- openhands-sdk/openhands/sdk/conversation/event_store.py — blob efefd007223cd762601d01c6a0b87a9ec22186b5
- openhands-sdk/openhands/sdk/conversation/state.py — blob aed9428fa253058feac7b5e7a41ac5863db46b7b
- openhands-sdk/openhands/sdk/io/base.py — blob ce0d50afee77652ad7723f8fbd4a6ac6e0ac7165
- openhands-sdk/openhands/sdk/io/local.py — blob b31d270068557f125b45e48095c7ebbc3c0825fc
- openhands-sdk/openhands/sdk/conversation/impl/local_conversation.py — blob 4f2fb14a4b33bccaecae7c12be15c51539350b1e
- openhands-agent-server/openhands/agent_server/event_service.py — blob e02803e37e70a9dee43a815d34c5649e91332daf
- openhands-agent-server/openhands/agent_server/conversation_lease.py — blob 195904d81f340d39480ec94f549892267561e371

## 2. Happy: device pairing and trust establishment

### 2.1 Pairing-link format and handling

The Android client accepts a Happy V2 direct-pairing link shaped as happy://direct? followed by canonical unpadded base64url JSON. The decoded payload includes version, address/origin, port where applicable, 32-byte token, display name and expiry. Parsing checks:
- exact scheme/prefix and a 16 KB maximum link length;
- canonical base64url encoding;
- supported versions 1 or 2;
- v2 origin rules (no legacy address/port fields);
- valid address, port range, 32-byte token, bounded non-control display name;
- finite future expiry.

The address, token and expiry are treated as sensitive. The link object's string representation omits address and token. The name is explicitly unverified before pairing and is display-only.

### 2.2 Pairing cryptography

The phone generates a fresh 32-byte X25519 private key and 32-byte nonce. It publishes a SHA-256 commitment over a domain-separated label, its public key and nonce.

After receiving the daemon public key and nonce, both sides derive:
1. X25519 shared secret, rejecting malformed or all-zero low-order shared secrets;
2. a length-prefixed transcript binding the QR token, commitment, both public keys, both nonces, address and port;
3. SHA-256 transcript hash;
4. HKDF-SHA256 purpose-separated 32-byte keys for emoji, confirmation MAC and derived device token.

Role-specific HMAC-SHA256 proofs bind the role and transcript hash. The phone verifies the daemon MAC using constant-time comparison. The derived device token is not sent during the pairing handshake.

### 2.3 Pairing state machine

The Android client sequence is:
1. POST handshake start using the QR token as the credential; receive handshake ID, daemon key/nonce and expiry.
2. Derive keys and reveal the phone public key and nonce using the handshake ID.
3. Receive four emoji for human comparison.
4. Only after the person confirms the emoji, send the mobile role MAC.
5. Poll until the daemon reports completed; verify the daemon role MAC.
6. Only then return and persist the derived device token.

The effective expiry is the minimum of QR expiry and daemon handshake expiry. A mismatch/cancel attempts to reject the handshake; cancellation rejection is best effort with a 2-second bound. Unfinished pairing is documented in the client as storing no credentials.

### 2.4 What the tests prove, and what they do not

The Android crypto tests include fixed cross-implementation vectors for public keys, transcript hash, purpose keys, emoji, device token and role MAC; they reject low-order/malformed keys and non-canonical base64url. Pairing tests cover malformed/expired QR codes, correct derived token, bad daemon proof and cancellation/rejection. The pairing service tests use a FakeDaemon.

**Critical limitation:** repository code search for /v0/mobile-connector/handshake found only Android/iOS client PairingService implementations and client tests. The public repository does not expose the daemon-side handler for this pairing route. docs/api.md documents cloud account-linking routes, not this local mobile-connector handshake. Therefore this audit cannot verify server/daemon enforcement of:
- one-time QR token consumption and replay rejection;
- handshake ID entropy, binding and invalidation;
- rate limits and abuse controls;
- atomic state transitions under concurrent confirm/reject/expiry;
- authoritative expiry and cleanup after daemon crash;
- device-token storage, revocation and authorization scope.

The client cryptography is a useful study reference, but the protocol is not independently closed from client source alone.

### 2.5 Account linking and credential storage are separate flows

Account linking is not the same as pairing a phone to an agent. The new phone creates a box key pair and shows its public key; an already authenticated phone encrypts the 32-byte account master secret to that public key; the server relays the encrypted response; the new phone decrypts it. Android stores account credentials through Expo SecureStore.

By contrast, happy-agent CLI's credentials.ts stores JSON containing bearer token and account secret in ~/.happy/agent.key, requesting directory mode 0700 and file mode 0600. The source does not encrypt that file at rest. Actual Windows ACL enforcement of these POSIX mode arguments was not verified. Do not treat the CLI file as equivalent to Android SecureStore.

### 2.6 Content encryption boundaries

docs/encryption.md documents:
- legacy client payload encryption using NaCl secretbox (XSalsa20-Poly1305);
- newer per-record data keys using AES-256-GCM;
- data-key wrapping to account content public keys using NaCl box with an ephemeral key pair;
- server storage of encrypted content as opaque blobs;
- third-party service tokens encrypted at rest using a server-only key tree derived from HANDY_MASTER_SECRET, not end-to-end encrypted.

The distinction matters: Happy's content E2E design does not imply every credential or server-held token is E2E encrypted.

### 2.7 Happy disposition for PocketCode

Potentially useful pattern: explicit device pairing with transcript-bound ECDH, human-verifiable short code, mutual MAC confirmation and a derived device credential that is withheld until confirmation.

Do not adopt/fork the pairing protocol yet. The server-side handshake implementation is missing from this repository view, and the CLI credential file is not a secure-storage template. Happy remains a pairing/UX study target, not a selected PocketCode dependency.

## 3. OpenHands: EventLog, state snapshot and ownership fencing

### 3.1 EventLog persistence model

OpenHands SDK EventLog is a file-per-event append-only log:
- event JSON files carry an on-disk monotonically allocated sequence and event ID;
- append acquires a FileStore lock, refreshes its index when the length marker cannot prove the cache current, rejects duplicate event IDs and unknown explicit parents, then writes the event;
- the disk index is never reused after a lost file;
- a sidecar length marker accelerates detection of other writers;
- startup scans files and builds an in-memory dense index while preserving original disk sequence numbers for resume cursors;
- missing event files are reported and surviving later events remain readable; the missing event itself is not reconstructed;
- parent links support branches, legacy linear histories and bounded path-to-root reads.

This is an append-only event history with stable cursor semantics, not a relational transaction log or a replicated event broker.

### 3.2 LocalFileStore and deployment caveats

LocalFileStore:
- writes text through atomic_write_text (temporary write/replace pattern);
- caches reads and explicitly assumes exclusive access; external modifications may produce stale cache reads;
- uses filelock for file-based locks;
- FileStore/EventLog documentation warns that file locking is not reliable on NFS/network filesystems.

This is important for any shared-storage deployment: a local file lock is not a distributed lock/fencing service. A different FileStore backend or external coordination mechanism is required where the filesystem cannot guarantee the lock semantics.

### 3.3 ConversationState snapshot and restore

ConversationState stores base_state.json separately from the event files:
- fresh create writes an initial base snapshot and opens EventLog;
- restore validates the conversation ID, reopens EventLog, repairs a missing saved leaf by moving to the last surviving real event, rebuilds the active view and preserves persisted stats;
- when an Agent is supplied on restore, tool compatibility is checked against the persisted agent;
- public field assignments autosave the base snapshot; grouped state mutations defer the save until context-manager exit;
- if a Cipher is configured, persisted secrets are encrypted; without one, secret values are redacted and lost on restore.

The event log and base snapshot are distinct persistence objects.

### 3.4 Crash-window candidate: event append and active HEAD are not one atomic write

ConversationState.append_event performs EventLog.append(event), then assigns leaf_event_id to the new event. leaf_event_id assignment triggers a separate base_state.json autosave (or a deferred save at state context-manager exit).

The inspected code does not wrap the event-file append and base-state HEAD update in one filesystem transaction. A process crash after the event file is written but before the base snapshot records the new leaf can leave a durable event that is not the active HEAD after restore, because a set, still-existing leaf_event_id is accepted as the HEAD. This is a **source-derived crash-window hypothesis**, not a reproduced bug. It needs a targeted fault-injection test before drawing a product conclusion.

### 3.5 EventService lease generation and guarded writes

OpenHands agent-server adds a stronger ownership layer around persistence:
- each conversation lease stores owner_instance_id, monotonically increasing generation and expiry;
- claim/renew/release are serialized by a file lock;
- takeover increments generation when the old lease is expired or its same-host process is known dead;
- guarded_write holds the lease lock while checking owner and generation and while the protected disk write executes;
- EventService attaches this guard to ConversationState and EventLog writes.

This is stronger than a lease checked only before starting a write: the generation check and disk write share the lock, so a new owner cannot take over between the check and the guarded write.

**Boundary:** the guard fences only writes routed through it. It does not automatically fence an external process launch, provider request or other side effect already issued by a stale worker. The lease is not a substitute for downstream idempotency/fencing at the side-effect boundary. The event append and subsequent base-state HEAD update are each guarded, but remain separate writes and are not an atomic pair.

### 3.6 OpenHands disposition for RevDev/PocketCode

Useful study patterns:
- append-only per-event evidence with stable sequence and event ID;
- parent/branch identity separate from chronological sequence;
- duplicate ID and parent-existence validation;
- non-reused disk sequence numbers and explicit gap reporting;
- record-first durable ownership generation and guarded writes;
- crash recovery and explicit missing-event handling.

Do not copy the implementation wholesale. Its file-store lock assumptions are local-filesystem-specific, its event and base-state writes are not one transaction, and the lease fences disk writes rather than arbitrary external effects. Keep RevDev native acceptance and PocketCode D-01..D-08 decisions unchanged.

## 4. Cross-project implications

- PocketCode D-04 still needs an explicit authenticated event identity, replay/order policy and immutable evidence semantics. OpenHands is vocabulary and implementation study, not an approved contract.
- PocketCode D-05 remains BLOCKED: the applied policy revision still needs an atomic enforcement barrier at execution start.
- PocketCode D-06 remains owner-open: reservation, provider idempotency and ambiguous-start recovery are not solved by an EventLog.
- D-07/D-08 still need selected artifact/report stores and identity/version/retention semantics.
- RevDev's recovery/publisher cycle must continue to distinguish durable event evidence, actual execution outcome, publication, release authorization and delivery.
- Happy-style device pairing could be a later authorization/onboarding layer for a remote host, but cannot replace remote execution, OS policy enforcement or durable orchestration. It does not justify a general mobile terminal or system-wide overlay.

## 5. Next review priorities

1. Gemini, when available: independently challenge the Happy pairing trust assumptions, missing daemon-side proof, OpenHands append/HEAD crash window and lease fencing boundary.
2. Claude, when available: inspect the Happy daemon-side implementation only if an authoritative source repository or source archive can be identified; do not recreate it from client code or API comments.
3. ChatGPT: reconcile those reviews with the existing fixed-task worksheet, D-01..D-08, state/identity mapping and RevDev acceptance crosswalk.

## 6. Non-actions

No upstream source was changed. No tests, builds, device runs, installs, account operations, provider operations, schemas, canonical acceptance IDs, PocketCode PRs, RevDev host, PC source/runtime/queue, Actions, deployments, merges or spend were touched. All PC/RevDev runtime state remains UNKNOWN.


## 7. Agent-server recovery and existing tests addendum — 2026-11-02

A further read of the same pinned source found that the agent-server explicitly recognizes the append/HEAD crash window. At `event_service.py` lines 1424–1467, startup detects a persisted RUNNING conversation, marks it ERROR, scans the full EventLog for unmatched actions, and appends a non-retryable internal AgentErrorEvent explicitly parented to the first unmatched action if no ObservationBaseEvent exists for its tool_call_id. The comment explains this parent override prevents the recovery result from becoming a sibling under stale HEAD. SDK state.py lines 268–320 show a still-existing leaf is accepted as HEAD; missing-leaf repair only occurs when the saved leaf event is absent.

Existing tests were located:
- `tests/agent_server/test_event_service.py`, blob `fc6e589f71318ac36df92b72c1fd0225549d1436`, lines 2419–2678, covers RUNNING+unmatched, RUNNING+no unmatched, non-RUNNING, and observation suppression by tool_call_id even when action_id differs. These use mocked state and do not assert parent_id or restored active ancestry.
- `tests/sdk/conversation/test_get_unmatched_actions.py`, blob `35798b1bccb60b0976cf0785682ef17181e4450b`, covers helper matching by tool_call_id.
- The verification feature map F31.crash-tool-call, blob `5082730e1ba1d333daeaf321c21214ad4924cd12`, lines 191–220, documents a SIGKILL integration recipe checking ERROR, one matching AgentErrorEvent, zero ObservationEvents and resumed delivery. It does not check parent_id or active ancestry; the broader recipe has a DeepSeek API-key/model precondition.

The remaining gap is a real local persistence/restore crash test asserting action → recovery error active ancestry and explicit parent_id, plus focused tests for full-log observation suppression and multiple unmatched actions. No test was run by ChatGPT. No upstream source/test was changed. See the expanded falsification plan for exact boundaries, including event-file/length-marker ordering and the distinction between process-crash survival and power-loss durability.


## 8. Multi-action recovery and navigation/rewind qualification — 2026-11-02

Further pinned-source review materially expands the crash-recovery analysis. Commit remains `98849457621881ae2414719b82b8bc1cf535b4ab`.

### 8.1 Multi-action batch path

- `event/base.py` lines 181–200 says multiple ActionEvents are produced when one LLM response contains multiple parallel tool calls.
- `response_dispatch.py` lines 224–255 (`_ahandle_tool_calls`) loops through all tool calls and calls `_get_action_event` before invoking `_aexecute_actions` on the accumulated list. `agent.py` lines 1517–1544 confirms `_get_action_event` invokes `on_event(action_event)` before returning.
- `agent.py` lines 695–716 delegates to `_ActionBatch.aprepare`; `_ActionBatch.aprepare` lines 327–352 awaits the full executor batch. `_ActionBatch.emit` lines 354–381 only emits the tool results after the batch returns.
- `parallel_executor.py` lines 128–191 uses `asyncio.gather` for concurrent tool calls (or sequential awaits when only one worker is configured).
- `state.py` lines 713–752 returns every unmatched executable ActionEvent in chronological order.
- Startup recovery at `event_service.py` lines 1436–1467 uses only `unmatched_actions[0]` and creates one AgentErrorEvent explicitly parented to that first action.
- By contrast, the normal interrupt path in `local_conversation.py` lines 2646–2654 calls `_emit_orphaned_action_errors`, which loops all active-branch orphans at lines 2777–2805.

This establishes a high-priority test gap: a normal multi-tool LLM response can persist several actions before execution results are emitted. A crash during the batch can leave multiple unmatched actions, while startup recovery answers only the first. Because later actions are descendants of earlier action events, the explicit parent to the first action may also detach later actions from the recovered active branch. This is not yet a confirmed defect; test exact parent chain, active branch, remaining unmatched actions and reconstructed LLM history. The detailed FI-15..18 cases are in the crash-window plan.

### 8.2 Full-log observation suppression after supported navigation

The earlier assumption that a non-active-branch observation is necessarily synthetic needs correction:
- `local_conversation.py` lines 988–1011 supports `navigate_to`, keeps all branches on disk, and documents that appending after navigation creates a sibling while abandoned events remain in the log.
- `remote_conversation.py` lines 1914–1943 calls the server `/navigate` route; EventService exposes navigation at lines 2358–2372.
- F10 feature map lines 34–38 and 295–328 documents that navigation preserves abandoned events while moving HEAD.
- Startup recovery at `event_service.py` lines 1431–1446 scans the full log and suppresses recovery if any ObservationBaseEvent matches the first action's tool_call_id.

A prior-branch observation can therefore exist in the full EventLog while being absent from active ancestry. Test whether a supported navigate-back-to-action → new run → interrupted tool → restart sequence can persist RUNNING state and cause the old observation to suppress recovery. Reconcile this with the comment that remote branching is unsupported (#3749); distinguish unsupported concurrent branching from the exposed in-place navigate/re-root behavior. Do not call this a confirmed bug until reachability and intended re-execution semantics are established. See FI-19..22.

### 8.3 F31 local stub nuance

F31 crash-tool-call creates a per-conversation agent with model `openai/qa-stub`, placeholder key `qa-stub-key`, and a local `llm-stub` base URL (F31 lines 103–121). The crash scenario (lines 191–220) sends the request to that stub, SIGKILLs during the stubbed terminal tool action, then changes the stub to finish and resumes. The wider F31 setup also runs `llm preset deepseek` and other F31 subfeatures use DeepSeek. Thus the specific crash-tool-call flow appears local-stub-backed, but whether the preset command is required in an isolated no-key invocation is not verified. Do not call the entire F31 suite provider-free.

No tests were run by ChatGPT. No upstream source/tests were modified. The expanded test plan is proposal only.
