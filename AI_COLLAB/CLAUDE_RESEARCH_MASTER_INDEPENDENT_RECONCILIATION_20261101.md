# Claude Open-Source Research Master: Independent Reconciliation

Date: 2026-11-01  
Reviewer: ChatGPT, independent evidence reconciler  
Input: Claude's pasted "PocketCode + RevDev: Open-Source Research Master Document" (research-only; no repository/source execution claimed by Claude)  
Status: desk review and selected primary-source verification only. No adoption, implementation, test, device run, install, provider use, spend, or host operation is authorized by this document.

## 1. Executive verdict

Claude's research is valuable as a discovery and reading list. It is not an adoption plan and its P0 labels must not be treated as owner decisions. The strongest near-term contribution is a set of source-study targets and design patterns:

1. Anthropic sandbox-runtime and OpenAI Codex Windows sandbox code as security reference material for RevDev.
2. OpenHands event/state persistence as a pattern to compare with existing RevDev P8U and PocketCode lifecycle work.
3. MCP Tasks as an optional interoperability vocabulary, not a source of truth for either product.
4. ACP v1 as a possible future PocketCode adapter protocol, subject to a narrow read-only feasibility spike after the existing milestone is clarified.
5. Happy as prior art for pairing, remote session mirroring and approvals, not yet a fork candidate.
6. StreamJsonRpc and Polly as credible RevDev library candidates, but only if the existing architecture demonstrates a real gap they solve.

No source code, runtime, provider, acceptance suite, host, queue, or deployment should change as a result of this research alone.

## 2. Evidence labels and scope

Claude explicitly distinguished session-verified primary evidence [V], secondary evidence [S], training knowledge [K], inference [I], and recommendations [R]. Preserve that distinction. This review performed a separate, limited check of selected current primary pages. A primary README or documentation page verifies what that page says, not production suitability, licence at an arbitrary future commit, security completeness, or successful integration.

The following were checked in current primary sources:

- Anthropic sandbox-runtime README and Windows security/limitations sections.
- OpenAI Codex Windows sandbox token source page.
- MCP 2026-07-28 release post and linked Tasks extension change.
- ACP current protocol documentation.
- OpenHands Conversation architecture documentation.
- Microsoft StreamJsonRpc repository description.
- Polly official getting-started documentation.

Not independently re-verified in this pass: the full 71-row licence ledger, Happy's actual pairing/encryption implementation, every repository's maintenance status, Tailscale plan limits, Gemini CLI retirement, third-party CVE details, Temporal/Restate deployment/licence claims, and all [K] rows. These remain research leads, not accepted facts.

## 3. Primary-source verification and corrections

### 3.1 Anthropic sandbox-runtime / Windows

**Confirmed:** Windows support is labelled alpha. The documented design uses a dedicated sandbox account, a write-restricted token, NTFS ACLs and a WFP egress fence with proxy-mediated access. The current README documents important caveats:

- Schannel clients cannot complete HTTPS from the restricted token. Examples include System32 curl, PowerShell Invoke-WebRequest/Invoke-RestMethod, .NET HttpClient, NuGet/dotnet restore, winget, and Git configured for Schannel.
- OpenSSL-based and language-specific TLS clients may work, but require their own trust bundle/configuration.
- allowWrite grants persist between sessions and require ACL work across the granted tree.
- Kept roots can be read by other sandboxed sessions until grants are removed, even though write access is scoped.
- WFP attribution has stated limitations for token impersonation and traffic carried by system services.
- Profile and per-user tool access require careful treatment; do not assume the sandbox can safely or conveniently use the operator's existing per-user toolchain.

**Decision:** retain as a high-priority *study* for RevDev's future PC return. Do not approve an installation, local account, WFP rule, ACL mutation, or integration. Treat the Schannel compatibility inventory and shared-machine implications as mandatory pre-prototype questions. Windows alpha status and the operational footprint make it inappropriate to describe as a drop-in or as an already accepted security boundary.

OpenAI Codex's token source is a valuable independent implementation reference. Reading the source is not proof that its entire sandbox is directly reusable or equivalent to srt. Gemini should inspect token creation, ACL handling, process creation, cleanup and failure paths, with exact commit hashes.

### 3.2 MCP 2026-07-28 and Tasks

**Confirmed:** the 2026-07-28 release describes a stateless protocol core. Tasks moved out of the experimental core into the `io.modelcontextprotocol/tasks` extension, with polling via `tasks/get` and task updates. The extension is not mandatory core behaviour.

**Correction to Claude's interpretation:** MCP Tasks provides useful task-handle/interoperability vocabulary. It does not itself guarantee that an implementation persists a task durably across process, machine, account or provider failure. Nor does it define our full trust chain, authorization, evidence retention, immutable event provenance, release authorization, artifact transfer or user-facing verdict.

**Decision:** maintain a mapping table from each product's native task/mission lifecycle to MCP concepts if an MCP bridge is later useful. Do not rename native states, replace native IDs, adopt MCP as an authority, or freeze schema now. Keep the seven independent state axes already documented for PocketCode and the separate RevDev state/acceptance namespaces.

### 3.3 ACP

**Confirmed:** current public ACP documentation presents v1 as latest and v2 as draft. v1 uses JSON-RPC 2.0, initialization/capability negotiation, sessions, prompt/update flows, optional session loading, cancellation, and permission requests. Agents commonly run as client subprocesses.

**Correction:** ACP is an agent-client interaction protocol, not a complete provider-neutral durable orchestration platform. A remote phone-to-host design still needs an authenticated transport, reconnect/session identity, durable job state, evidence history, permission enforcement at the execution boundary, and replay/fencing semantics. Forwarding stdio over SSH/WebSocket is an adapter/transport design to validate, not a built-in guarantee of ACP.

**Decision:** ACP is a candidate for a later narrow read-only session viewer experiment. It is not a first-milestone requirement and does not displace the existing PocketCode fixed-task feasibility work. Compare ACP against a thin PTY/session adapter using the already defined product milestones, not agent ecosystem popularity.

### 3.4 OpenHands persistence and event log

**Confirmed:** OpenHands documents an EventLog as immutable append-only storage, a ConversationState, state-only updates as well as event-based updates, FIFO locking/atomic updates, callbacks after commit, and persistence/resume services. It also documents a common Conversation API with local and remote implementations.

**Important nuance:** the public architecture documentation supports the event-log and state-management pattern. It does not, by itself, establish that the correct RevDev implementation is one JSON file per event, nor that SQLite is the wrong choice. Claude's "per-event JSON file" description requires source-level verification against a pinned commit before it is copied as a concrete storage layout.

**Decision:** study as a pattern. For RevDev, compare with existing P8U/recovery/result/evidence structures before proposing any new journal. For PocketCode, compare with the seven-axis lifecycle and trust-chain gap matrix. Do not create a second event store or competing source of truth.

### 3.5 StreamJsonRpc

**Confirmed:** Microsoft's repository describes JSON-RPC 2.0 over .NET streams, WebSockets and pipes, with cancellation and related support.

**Decision:** keep as a possible RevDev dependency only if fresh source inspection shows a concrete named-pipe/stream RPC requirement not already met. The library does not supply peer authentication, pipe ACLs, method authorization, caller identity, or a security boundary. Those must be designed and tested independently. No dependency is approved now.

### 3.6 Polly

**Confirmed:** Polly's official docs show v8 resilience pipelines with strategies such as retry and timeout.

**Decision:** possible in-process resilience helper, not durable recovery. Retries must be restricted to known transient failures and safe/idempotent operations. Do not retry a side effect merely because its response was lost. A journal, operation identity, idempotency key, ambiguity handling and fencing are separate concerns. No dependency is approved now.

### 3.7 Happy

Claude's report identifies Happy as the closest prior art and explicitly says it did not read the pairing/crypto source in this pass. The GitHub repository overview is a discovery pointer, not sufficient security evidence for E2E claims, server trust, pairing lifecycle, key management, revocation, push notifications or permission enforcement.

**Decision:** study source before considering fork versus clean-room. Required review: pairing and QR bootstrap, key derivation/storage, device identity and revocation, ciphertext boundaries, metadata leakage, hosted-server dependency/defaults, self-hosting, push payloads, session reconnect, permission approval, CLI wrapper and threat model. Do not fork or reuse crypto code based on README claims alone.

### 3.8 DSSE and in-toto

**Decision:** formats are worth studying for artifact/evidence digest binding, but Claude's proposed "about 100 lines" implementation estimate is not an adoption basis. DSSE envelopes and in-toto statements do not automatically establish trustworthy provenance. Need exact payload canonicalization/serialization rules, digest coverage, signer identity, key custody, rotation/revocation, trust roots, verification policy, replay protection, and the distinction between integrity and authorization. Begin with unsigned deterministic SHA-256 manifests only if they fit the existing result contract; signing is a separate later design. Do not replace existing result files or LATEST_RESULT semantics by assertion.

### 3.9 Pyodide

The earlier dedicated Pyodide 314.0.7 review remains controlling for pinned-version findings. Claude's report adds anecdotal iOS memory observations but no measurements on the user's phone. Worker termination is a hard-stop mechanism, not proof of cleanup, safe recovery, or a known memory ceiling. Do not upgrade "candidate for a small local lane" into "adopted runtime". Keep the canonical fixed task unchanged and defer device validation until explicitly authorized and physically possible.

## 4. Candidate disposition

| Candidate | Disposition | Reason / gate |
|---|---|---|
| srt Windows | STUDY NOW; PC prototype deferred | Windows alpha, elevation, persistent ACL/WFP footprint, Schannel breakage, cross-session read and shared-machine caveats |
| Codex Windows sandbox | STUDY NOW | Independent source reference; needs exact commit and security review |
| OpenHands EventLog/state | STUDY NOW | Useful pattern; reconcile with existing P8U and PocketCode lifecycle before storage choice |
| MCP Tasks | MAP ONLY | Optional extension vocabulary, not durability or authority |
| ACP v1 | DEFERRED SPIKE | Promising adapter protocol; not first milestone or durable orchestration |
| Happy | STUDY SOURCE | Prior art; no fork/crypto decision without source-level threat review |
| StreamJsonRpc | CONDITIONAL CANDIDATE | Adopt only if a real IPC need is evidenced; ACL/authz remain our responsibility |
| Polly | CONDITIONAL CANDIDATE | In-process resilience only; retries need idempotency/side-effect classification |
| SQLite WAL | NO NEW JOURNAL DECISION | Audit P8U/existing contracts first; avoid duplicate state authority |
| Stateless | DEFERRED | Could encode local transitions but does not define durable semantics; may duplicate existing code |
| Velopack | DEFERRED | Packaging/update architecture and authorization rules need PC evidence; check-only default remains required |
| DSSE/in-toto | FORMAT STUDY | Integrity/provenance format only; trust and key management are separate |
| CodeMirror 6 | UI CANDIDATE | Strong mobile-editor candidate, but no editor/library adoption without milestone and UX architecture decision |
| xterm.js | DEFERRED | Terminal surface is not necessarily desirable for the phone-first control plane; no general terminal promise |
| isomorphic-git | DEFERRED | Browser storage, repo size, mobile performance and correctness untested |
| Tailscale / Headscale | OWNER DECISION OPEN | Third-party coordination/control-plane policy and current plan terms need verification |
| Worktrunk / agent-worktree | STUDY ONLY | Native Git worktree patterns; no PC validation |
| FileSystemWatcher + reconcile | PATTERN ONLY | Must be checked against existing watcher implementation; no rewrite based on generic advice |
| Job Objects | FUTURE DESIGN CHECK | Process-tree control/timeouts are useful, but not a security sandbox and not proof of child terminal evidence |
| Termux | OPTIONAL ANDROID INTEGRATION ONLY | Do not embed GPL code; not an iOS execution strategy |

## 5. Critical cross-project guardrails

### 5.1 RevDev: no duplicate journal before audit

RevDev's local source, installed binary, runtime, watcher and queue are UNKNOWN while the PC is unavailable. Historical paths and previous test results do not establish current state. Claude did not inspect RevDev source and acknowledges that its journal proposal could duplicate P8U.

When PC access returns, first gather fresh read-only evidence for:
- current source commit and dirty state;
- exact P8U modules, state transitions, operation identities, durable records and recovery behaviour;
- mission/result schemas and exact evidence files;
- watcher reconciliation and queue ownership/fencing;
- installed binary identity separately from source;
- current acceptance crosswalk and gaps.

Only then decide whether a new SQLite journal is needed. Preserve native acceptance IDs and the separation of execution outcome, coordination disposition, evidence persistence/integrity, publication, release authorization, transfer/receipt, and user-facing verdict.

### 5.2 Retry and cancellation semantics

Polly retry is not crash recovery. At-least-once delivery plus idempotent operations is a useful design assumption, but it does not justify blind retries. Ambiguous external starts must remain ambiguous until evidence resolves them. Cancellation request, cancellation acknowledgement, process termination and verified terminal result are distinct facts. A Job Object is a containment/control mechanism, not a substitute for trusted terminal evidence.

### 5.3 Lenient syntax, strict authority

Claude suggests accepting observed reply-format drift. This is compatible with robustness only if parsing tolerance is strictly separated from policy and authorization:
- tolerate only explicitly enumerated syntactic variants with warnings;
- preserve exact raw input and parse diagnostics;
- never infer missing ACK, nonce, mission identity, version authority, confirmation or guard;
- never allow a parser normalization to promote parsed content into policy-approved or authorized content;
- never relax HOSTED_DENY or destructive-operation rules;
- maintain the established distinction between RDV-END and RDV-REPLY-END and the documented legacy alias diagnostics.

Do not implement a "robustness principle" that accepts ambiguous authority.

### 5.4 PocketCode remains the existing product

Do not turn PocketCode into a general mobile terminal, unrestricted shell, vendor-CLI wrapper, or hosted execution service. Preserve:
- phone-first control plane;
- explicit clipboard operations, no background clipboard polling;
- no system-wide overlay;
- accessory symbol bar;
- local WASM/JSC only for small bounded tasks;
- remote SSH/Tailscale or cloud fallback only under explicit trust/owner decisions;
- fixed-task worksheet as canonical;
- seven independent lifecycle/state axes and the existing D-01..D-08 decision boundaries;
- zero-spend constraint.

## 6. Decisions on Claude's questions

1. **Mission states vs MCP:** keep native RevDev vocabulary and map to MCP Tasks only at an adapter boundary.
2. **Event files vs SQLite:** no decision. First audit P8U and current storage. The right design may be a transactional SQLite journal with exportable/inspectable immutable event records, but this is a hypothesis, not a selection.
3. **Fork Happy vs clean-room:** no decision. Source-level pairing/crypto/threat-model review first; likely reuse UX/patterns before considering code.
4. **ACP vs PTY for first milestone:** neither is required for the current fixed-task milestone. For a later remote-agent milestone, compare thin PTY adapter and ACP v1 with a read-only viewer spike.
5. **Tailscale vs Headscale:** owner decision remains open. Do not assume free-tier limits or accept third-party control plane by default.
6. **Gemini's three reads:** Codex token/ACL/process creation; srt Windows policy/ACL/WFP and failure/cleanup paths; OpenHands EventLog/state persistence. Then Happy pairing/crypto as a separate security-focused pass.
7. **Licence conflicts:** verify at exact commit and record LICENSE/NOTICE before any vendoring. No licence cell based only on README badge or third-party aggregator is sufficient.

## 7. Recommended next work passes

### Pass A — reconcile existing work, no schema changes
- Compare Claude's candidate list against the current PocketCode trust-chain gap matrix, lifecycle/identity mapping, fixed-task worksheet and decision register.
- Record that no adoption is approved.
- Obtain Gemini's independent SCF-001..018 review and Claude's corresponding review; reconcile fixture-by-fixture without changing native acceptance IDs.

### Pass B — focused source-reading assignments
- Gemini: Codex Windows token/ACL/process creation and srt Windows policy/limitations; return exact commit, path, line/range, licence file and threat/cleanup analysis.
- Claude: OpenHands EventLog/state/persistence source and Happy pairing/encryption source; return exact commit, source paths, sequence diagrams, security assumptions and differences from our design.
- ChatGPT: independently reconcile, reject unsupported claims and update decision register only where evidence justifies it.

### Pass C — RevDev desk-only design preparation
- Prepare a read-only P8U evidence inventory template and a no-duplicate-journal decision checklist for when PC returns.
- Draft a strict parser-tolerance matrix based only on observed variants, preserving strict authority gates.
- Do not propose a new schema or implementation until the source audit.

### Pass D — PocketCode fixed-task continuity
- Continue only the already-defined iPhone feasibility work and source research.
- No native build, device test, provider workload, account, spend, or deployment.
- Do not allow broad candidate research to displace the canonical fixed task or product milestone.

## 8. Official primary references checked

- MCP 2026-07-28 release: https://blog.modelcontextprotocol.io/posts/2026-07-28/
- MCP Tasks extension proposal: https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2663
- ACP v1 overview (site also lists v2 as draft): https://agentclientprotocol.com/protocol/v1/overview
- Anthropic sandbox-runtime: https://github.com/anthropics/sandbox-runtime
- OpenAI Codex token source: https://github.com/openai/codex/blob/main/codex-rs/windows-sandbox-rs/src/token.rs
- OpenHands Conversation architecture: https://docs.openhands.dev/sdk/arch/conversation
- StreamJsonRpc: https://github.com/microsoft/vs-streamjsonrpc
- Polly getting started: https://github.com/App-vNext/Polly/blob/main/docs/getting-started.md
- Happy repository (overview only, not source-level security verification): https://github.com/slopus/happy

## 9. Non-actions and evidence status

This review did not inspect RevDev PC source or runtime, run code, install software, execute tests, exercise a device, add dependencies, use an AI provider workload, create accounts, incur spend, change schemas, alter canonical acceptance, touch PR #2 or PR #3, merge, deploy, publish, mutate a queue, or operate a host. RevDev PC state remains UNKNOWN. PocketCode remains research/documentation-only on its isolated branch.


## 10. Windows sandbox source-audit follow-up — 2026-11-01

Claude supplied a partial Codex-vs-srt Windows audit after timing out. The complete reconciled findings, evidence limits, proposed later tests and source-read backlog are recorded in [WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md](WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md).

### 10.1 Independent correction: Codex token flags are upstream-verified

ChatGPT independently fetched Codex source at exact commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635:
- codex-rs/windows-sandbox-rs/src/token.rs
- codex-rs/windows-sandbox-rs/src/elevated/command_runner_win.rs
- the commit diff/message.

This verifies the exact CreateRestrictedToken flags DISABLE_MAX_PRIVILEGE | LUA_TOKEN | WRITE_RESTRICTED, zero disabled SIDs, zero deleted privileges, restricting SID order (capabilities, extras, logon, Everyone), zero SID attributes, default-DACL setup and re-enabling SeChangeNotifyPrivilege. It also verifies the elevated runner's new user-SID constructors and the commit's explicit statement that the unelevated path is unchanged. The flags are therefore not derivative-only evidence as Claude's original report cautiously classified them.

The pinned commit's rationale documents a Ninja/default-named-pipe hang in the elevated write-restricted token and an elevated-only fix. It also states that the same repro remains in the unelevated sandbox. This is compatibility evidence for one narrow issue, not proof of the full sandbox.

### 10.2 srt PR #745 independently checked, source still unread

ChatGPT fetched PR #745 and verified its project-authored description: an AppContainer token could bypass the earlier WFP account-SID match; the fix adds all-packages SIDs; verification probes additional token shapes; anonymous and deny-only shapes remain residuals; lowered-integrity setup failures are not necessarily fatal; loopback-open mode exposes all local loopback services; and existing installations retain old filters until re-install because there is no migration.

The PR also says Windows CI ran its unit/smoke/integration legs but no manual Windows run was performed. The Rust implementation itself was not read. Do not convert PR design notes into source-verified behavior.

### 10.3 Disposition unchanged

Neither sandbox is selected. srt remains alpha and STUDY ONLY. Codex remains STUDY ONLY. No sandbox installation, host mutation, Windows test, dependency, schema, acceptance change or product-direction change is approved. RevDev PC state remains UNKNOWN. The source-read backlog and PROP-ST-01..23 are proposals only, not canonical acceptance IDs.

The next bounded pass is Gemini's independent challenge/source read when available, not another broad 70-candidate research sweep. Claude's remaining separate work is OpenHands EventLog/state/persistence and Happy pairing/encryption source review.


## 11. Deeper srt source follow-up and open WFP readiness issue

ChatGPT independently read srt Windows Rust/TypeScript source at merge commit 81145771c9bfc51c5669f071b515209321e0d078. Full detail and exact blob references are in [WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md](WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md), Section 13.

Key new findings:
- srt token source uses LUA_TOKEN | WRITE_RESTRICTED; disables BUILTIN\Administrators and logon SIDs; deletes all privileges except SeChangeNotifyPrivilege; restricts to capability SIDs, sandbox user SID, Everyone and RESTRICTED; then reads back the token restriction and checks it.
- srt has source-verified Job Object KILL_ON_JOB_CLOSE containment. The target is created suspended, assigned to a non-breakaway child job, then resumed. UI restrictions, isolated desktop checks, handle whitelist and process mitigations are also in launch source.
- srt ACL source withholds FILE_DELETE_CHILD from modify grants and adds parent FILE_DELETE_CHILD denies for protected targets. State DB source shows refcounted holder rows, file identity binding, per-user file locking and recovery.
- WFP source installs only ALE_AUTH_CONNECT IPv4/IPv6 layers. The Windows test suite explicitly states ICMP ping is NOT fenced.
- Current srt main SHA 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77 still reports WFP state installed if ANY block-user filter exists. Open issue #723 reports a half-installed IPv6 case; open PR #716 proposes partial status and repair, but is not merged. The default TS readiness probe binds IPv4 loopback only, not IPv6.
- install.rs documents a shared-machine CA-key trade-off: BUILTIN\Users can read/replace ProgramData CA key material; the sandbox group is denied. This is a documented risk decision, not a proven exploit.

The deeper source work raises confidence in several srt controls while also confirming important limits. srt remains STUDY ONLY. No runtime tests were run by ChatGPT, no winner is selected, and no RevDev/PocketCode architecture decision changes.


## 12. Codex source follow-up: firewall verified, ACL concerns escalated for review

ChatGPT read additional Codex source at pinned commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635. See Section 14 of WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md.

Source confirms the offline account's outbound firewall BLOCK is NET_FW_IP_PROTOCOL_ANY, non-loopback, all profiles, SID-scoped through LocalUserAuthorizedList with SID read-back. When local binding is disabled, UDP loopback is blocked and TCP loopback is blocked except proxy ports. When allow_local_binding is enabled, those loopback blocks are removed.

The source review also identifies high-priority questions in Codex ACL setup:
- Workspace write grants include FILE_DELETE_CHILD, while add_deny_write_ace applies the deny to the target and does not explicitly add a parent FILE_DELETE_CHILD deny. Parent-mediated deletion/rename needs a targeted Windows test.
- dacl_has_write_deny_for_sid treats any overlapping deny bit as sufficient, rather than verifying complete mask coverage.
- add_deny_write_ace returns Ok(false) when ACL API writes fail, making failure indistinguishable from no change; callers do not log Ok(false).
- setup_main_win accumulates ACL errors but only bails on them in refresh_only mode.
- The inspected process launch path has no Job Object/kill-on-close; full descendant/orphan handling remains unknown.
- Helper freshness uses size+mtime, not a cryptographic hash/signature, while the sandbox group is ACL-limited to read/execute.

These are source-level concerns requiring independent review and disposable Windows tests, not proven runtime exploits. Codex remains STUDY ONLY. No implementation/adoption decision.


## 13. srt WFP partial-state and network-coverage clarification — 2026-11-01

The detailed source and issue reconciliation is in Section 16 of WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md.

Current srt main at 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77 still has two independent gaps:
- filter_status() treats any remaining block-user filter as installed, even if the other address family's block filter is missing.
- verifyWindowsWfpEgress() creates its default listener on IPv4 loopback only.

Issue #723 contains an externally reported Windows 11 26200 reproduction (3 repetitions per state on one machine) where deleting the IPv6 block left IPv6 reachable while status and the IPv4-only readiness probe passed. PR #716 remains open/unmerged and proposes partial detection plus repair semantics. Its dual-family status logic is not the same as a dual-family runtime readiness probe. A separate issue-comment branch proposes IPv4+IPv6 readiness checks; it is not merged and was not source-inspected here.

Additional explicit limits at srt PR #745 merge 81145771c9bfc51c5669f071b515209321e0d078: WFP is installed at ALE_AUTH_CONNECT V4/V6 only; the Windows test suite explicitly says ICMP is not fenced; its DNS test demonstrates the DNS Client service resolves names under a NetworkService token outside the child's ALE_USER_ID. Anonymous and deny-only token shapes are residual warnings, not a failed verdict. Do not call this complete network isolation.

The same pinned srt source confirms stronger ACL semantics (modify grants omit FILE_DELETE_CHILD; parent-FDC deny and intermediate DELETE protection), a per-user refcounted session DB with record-first per-path DACL mutation and crash replay, and a documented shared-machine trade-off that real local users can read or replace the ProgramData CA key material.

Disposition unchanged: srt is an ALPHA study reference only, not selected or adopted. No Windows test was run by ChatGPT; external issue measurements are explicitly labelled as such.


## 14. OpenHands EventLog and Happy pairing source review — 2026-11-01

Detailed source evidence is recorded in OPENHANDS_EVENTLOG_AND_HAPPY_PAIRING_SOURCE_REVIEW_20261101.md.

OpenHands software-agent-sdk main snapshot 98849457621881ae2414719b82b8bc1cf535b4ab (MIT):
- EventLog is a per-event JSON append-only store with event IDs, durable disk sequence numbers, parent validation, file locking, sidecar length marker, index rebuild and explicit missing-file gap reporting.
- LocalFileStore uses atomic text writes and filelock but caches reads and warns that external modifications can be stale; FileStore/EventLog docs say local file locks are unreliable on NFS/network filesystems.
- ConversationState stores base_state.json separately from the event files. append_event writes the event first and updates leaf_event_id/base snapshot separately. A crash between those operations is a source-derived orphaned-event/stale-HEAD hypothesis, not a reproduced bug.
- EventService uses owner ID + monotonic generation + expiry and guarded_write holds the lease lock across the ownership check and protected disk write. This fences guarded persistence writes, not external process/provider side effects. Event append and HEAD snapshot remain separate guarded writes, not one transaction.

Happy main snapshot 323fb2e9fd0c9a44ceab9239fbc586c513f7f844 (MIT):
- Android client pairing uses ephemeral X25519, a transcript binding QR token/commitment/keys/nonces/address/port, HKDF purpose-separated emoji/confirm/device-token keys, human emoji comparison and mutual role MAC confirmation. The device token is derived and withheld until daemon proof succeeds.
- Client tests cover fixed vectors, malformed/low-order inputs, failed proof and cancellation, but use a FakeDaemon.
- The public repository source search found only mobile PairingService clients/tests for /v0/mobile-connector/handshake; no daemon-side route implementation was located. Server-side one-time token/replay/rate-limit/expiry/atomic transition guarantees therefore remain unknown.
- Android uses Expo SecureStore for credentials. happy-agent CLI stores token+secret JSON in ~/.happy/agent.key with requested POSIX mode bits and no file-level encryption; Windows ACL semantics were not verified.
- Happy docs distinguish client E2E-encrypted content from third-party tokens encrypted server-side with HANDY_MASTER_SECRET.

Disposition: OpenHands is a persistence/ownership study, not a copy-ready store. Happy is a pairing/UX study, not a selected dependency or verified complete pairing protocol. No native contract, D-01..D-08 owner decision, fixed task, product direction or implementation decision changed.
