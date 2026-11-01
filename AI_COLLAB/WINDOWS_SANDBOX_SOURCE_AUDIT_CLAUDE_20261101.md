# Windows Sandbox Source-Level Security Audit: Codex vs Anthropic sandbox-runtime

Date: 2026-11-01  
Input: Claude's audit supplied in chat; independent follow-up verification against pinned GitHub source and PR metadata.  
Status: **PARTIAL SOURCE AUDIT. STUDY ONLY. NOT AN ADOPTION DECISION.**

No implementation, installation, host operation, test execution, schema change, acceptance-ID change, PR modification, merge, deployment or spend occurred.

## 1. Executive verdict

Do not select either implementation for RevDev or PocketCode. Both are useful security-design references, but the evidence is asymmetric and neither has been independently proven secure or suitable for our requirements.

- **Codex:** exact token-construction behavior is now independently verified in upstream source at one pinned commit. Full ACL setup, firewall implementation, setup/teardown, process-tree containment, default policy and upgrade/recovery behavior remain unverified here.
- **Anthropic sandbox-runtime (srt):** README and PR #745 design notes describe useful controls and candid residual gaps, but the Windows Rust enforcement implementation was not read. Windows support is alpha. The AppContainer fence bypass and fix are evidenced by PR text/metadata, not independent review of the Rust implementation.
- **RevDev:** OS sandboxing remains a possible optional, owner-installed defence-in-depth layer only. RevDev's current PC source, binary, runtime, watcher, queue and host state remain UNKNOWN. This research does not establish that RevDev currently lacks or has any particular sandbox capability.
- **PocketCode:** this is reference material for a future remote Windows-host adapter only. It does not change the phone-first product, fixed-task milestone, zero-budget constraint or execution-boundary model.

srt documents a broader Windows WFP/proxy fence and more explicit ACL lifecycle controls, but its own materials identify residual token shapes, loopback exposure, upgrade drift and alpha status. Codex has a primary engineering explanation and a verified token-source slice, but key enforcement details remain unverified. No winner is declared.

## 2. Evidence scope and exact identities

### 2.1 Codex upstream source independently verified

Repository: https://github.com/openai/codex  
Pinned commit: 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635  
Commit title: [codex] Fix elevated Windows sandbox named-pipe access (#20270)  
Parent: 31f8813e3edd4bc0385ce6a07b1bde8d36613576

Files read at that exact SHA:
- codex-rs/windows-sandbox-rs/src/token.rs
- codex-rs/windows-sandbox-rs/src/elevated/command_runner_win.rs
- Commit diff and message, including changes in src/lib.rs.

This was an exact-ref GitHub source read and diff review, not a clone, local build or Windows execution.

### 2.2 Anthropic srt evidence

Repository: https://github.com/anthropics/sandbox-runtime  
Windows PR: https://github.com/anthropics/sandbox-runtime/pull/745  
Merge commit: 81145771c9bfc51c5669f071b515209321e0d078  
First commit named by Claude: e9760b9

Independently read in this follow-up: PR #745 metadata and full PR description/design notes, including the AppContainer issue, token-shape verification, residuals, loopback behavior and lack of automatic migration.

Not read:
- src/sandbox/windows-sandbox-utils.ts
- src/sandbox/sandbox-manager.ts
- Windows Rust helper implementation under vendor/srt-win-src/src/
- WFP, runner, ACL, install, probe and cleanup source at a pinned commit.

The PR description is primary project-authored evidence about the change, but not a substitute for reviewing the implementation.

## 3. Codex: verified token-source findings

At commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635:

1. token.rs, create_token_with_caps_from, constructs restricting SIDs in this order: capability SIDs, extra restricting SIDs, logon SID, Everyone. Every SID_AND_ATTRIBUTES.Attributes value is set to zero.
2. The helper rejects an empty capability-SID list.
3. The CreateRestrictedToken call uses DISABLE_MAX_PRIVILEGE (0x01), LUA_TOKEN (0x04), and WRITE_RESTRICTED (0x08). It passes zero SIDs-to-disable with a null pointer, and zero privileges-to-delete with a null pointer.
4. After token creation, code sets a default DACL granting GENERIC_ALL to the logon SID, Everyone and capability SIDs, then enables SeChangeNotifyPrivilege.
5. get_user_sid_bytes obtains TokenUser information and copies the SID, returning errors on checked Win32 failure paths.
6. Two new constructors add the token's user SID to the extra restricting-SID list.
7. In elevated/command_runner_win.rs, spawn_ipc_process uses the new user-SID constructors for ReadOnly and WorkspaceWrite. DangerFullAccess and ExternalSandbox remain unreachable in that function.
8. The commit message explicitly says the unelevated path is unchanged. It explains that default-DACL named pipes created by tools such as Ninja could hang under the elevated write-restricted token because the sandbox user's SID was absent from the restricting SID set. The fix is scoped to the elevated runner and is not intended to grant the sandbox user additional filesystem ACL permissions.

**Correction to Claude's report:** the exact three CreateRestrictedToken flags are verified in upstream Codex source at the pinned SHA. They are not derivative-only evidence. The derivative crate and third-party gist are unnecessary for that claim.

**Limitation:** this commit is a narrow elevated named-pipe compatibility fix. It does not verify the entire Codex sandbox design. Full ACL setup, firewall rules, sandbox-account provisioning, uninstall/rollback, helper integrity, process/job-object containment and default Windows policy were not inspected.

## 4. srt: PR #745 details independently checked

The PR description states:

1. The previous WFP BLOCK filter matched tokens that passed an access check granting the sandbox account SID. An AppContainer token for that account also needs a package SID grant. Without that grant, a sandboxed process could create an AppContainer child and connect directly. The fix adds the two all-packages SIDs to the match descriptor.
2. srt-win wfp verify was expanded beyond the sandbox account's plain token. It probes anonymous, deny-only-user-SID and lowered-integrity token shapes, each with sockets created both before and after assuming the token.
3. The plain sandbox-token attempt must be blocked. An anonymous or deny-only token that connects is reported as a residual warning, not a failed verification. A lowered-integrity attempt that cannot be set up is reported as not made and does not fail the check.
4. Off-machine anonymous probing is opt-in and is not performed at session start.
5. network.allowLocalBinding: true opens loopback on Windows via an install-time PERMIT for 127.0.0.0/8 and ::1. This is off by default. When enabled, every service listening on machine loopback is reachable, including a local proxy that may forward off-machine.
6. The loopback mode is machine-wide, administrator-installed state. A session asking for a mode different from the installed mode is refused before launch.
7. Existing installs retain earlier filters until srt-win install is run again; the PR states there is no migration.
8. The PR says Windows CI ran Rust unit tests, smoke rows and integration rows on that PR head, but also explicitly says nothing was run on Windows by hand.

These are findings about what the PR description says. We have not verified Rust descriptor construction, WFP layer coverage, install-state reconciliation or actual runtime behavior.

## 5. Comparative assessment

| Area | Codex | srt | Confidence |
|---|---|---|---|
| Restricted token | Exact flags and SID-list construction read at pinned source SHA | README-level write-restricted-token description; Rust call not read | Codex high for inspected function; srt medium for documented design |
| Elevated/unelevated split | Pinned commit proves elevated runner change and unchanged unelevated path | One-time Windows install and machine-wide WFP design described in README/PR | Medium-high |
| ACL precedence and parent-delete protection | Full ACL code not read; third-party catalogue not accepted as proof | README documents additive ACEs and parent FILE_DELETE_CHILD denial | Medium for documented srt behavior; low for Codex |
| Network | Elevated Firewall details remain third-party/unverified; unelevated advisory behavior comes from OpenAI engineering post | WFP/proxy model documented; PR #745 describes AppContainer bypass/fix and residual shapes | Medium for design claims; low for complete enforcement |
| Process containment | Job Object/kill-on-close unknown | Job-object use described in README; source and kill semantics not read | Low-medium |
| Cleanup and persistent host state | Third-party catalogue only; install/uninstall source not read | README documents retained grants/refcount/recovery and uninstall/forget commands | Medium for documentation, not tested |
| Fail-closed | Some Codex token errors source-verified; full startup/default-policy behavior unknown | README describes fail-closed paths, with warning/residual exceptions | Medium |
| Schannel/tool compatibility | No Codex-specific evidence; similarity is inference only | README lists Schannel clients that fail | Medium for srt documentation; unknown for Codex |
| Shared-machine exposure | Not fully verified | README warns about shared-machine and cross-session kept-root access | Medium |
| Upgrade drift | Unknown | PR #745 explicitly says old installs retain prior filters until re-install | High for the PR's stated behavior |

Do not translate "write-restricted token" into "complete sandbox". Reads, writes, process creation, network egress, inherited handles, named pipes, impersonation, services, job containment, reparse points and host persistence are separate enforcement questions.

## 6. Threat-analysis conclusions

- Script lint/refusal is a policy layer, not OS enforcement.
- Environment-variable proxy settings and PATH stubs are advisory, not a network fence.
- A WFP filter is only as strong as its token matching, layer coverage, installation state, verification and upgrade behavior.
- A Job Object can help control process trees; it does not establish authorization, filesystem/network isolation or trusted terminal evidence.
- ACLs require checking inheritance, parent delete rights, reparse points, races, stale grants and cleanup.
- A passing startup probe is evidence about tested token shapes and targets only. It is not proof against all token impersonation, system-service-mediated traffic or future process behavior.

srt's AppContainer issue is a concrete example of why a security fence must be tested against token variants, not just the expected child token. Its residual reporting means a basic green verification result must be interpreted with warnings and skipped/unsettable probes, not as universal proof. The no-migration note means installed filter state can lag code version. Loopback-open mode materially expands reachability to local services.

Codex's named-pipe/Ninja incident demonstrates that token restriction can break ordinary developer tooling in ways that appear as hangs or missing completion rather than obvious access-denied errors. The pinned fix is elevated-only, and the commit explicitly says the same repro remains in the unelevated sandbox. Compatibility testing must cover real IPC patterns, not only filesystem probes.

No winner is declared. Source visibility, maturity, operational footprint and security completeness differ, and no independent adversarial runtime testing was done.

## 7. Relevance to RevDev

These are design candidates only, not implementation findings or owner decisions.

Potentially reusable principles:
1. Keep OS enforcement beneath existing lint, scope and confirmation rules. It must never replace them.
2. Distinguish advisory controls from enforced controls in evidence and UI.
3. Use one authoritative policy model for lint/scope and any later OS restrictions, especially delete/rename semantics.
4. Protect guard/configuration/evidence directories from the mission process where compatible with intended workflow.
5. Record read-only sandbox detection and exact policy/version/fence verification. RevDev must not silently install, elevate or repair a sandbox.
6. Treat inaccessible, mixed, stale and unverifiable roots as distinct evidence states, not generic success or one boolean.
7. Test named pipes, build servers, child processes, output capture, cancellation, cleanup and publisher/recovery flows before considering a restricted token.
8. Keep sandbox enforcement evidence separate from execution outcome, coordination disposition, evidence persistence, publication, release authorization, transfer receipt and user-facing verdict.

Conflicts and blockers:
- Both documented enforcing designs have persistent machine-level state and elevation/install implications. Any future adoption would require an explicit owner-performed out-of-band install and a read-only detector.
- srt's documented Schannel limitation conflicts with missions relying on PowerShell web cmdlets or .NET HttpClient/NuGet inside the restricted context.
- Codex's named-pipe incident suggests .NET build servers, MSBuild node reuse and other IPC-heavy tools need testing; these are hypotheses, not established failures.
- Any sandbox write permission that allows recursive delete or parent-child deletion could contradict RevDev's destructive-operation refusal.
- RevDev PC source/runtime/queue state is UNKNOWN. No assertion is made about current capability or implementation.

## 8. Relevance to PocketCode

- Treat these designs as possible remote-Windows-host enforcement references only.
- They do not imply local iOS sandboxing, a general mobile terminal, a universal shell or a hosted execution service.
- Any future remote-host adapter must preserve RevDev's authority and guards, authenticated session identity, explicit approval, evidence capture and release/transfer separation.
- The zero-budget rule remains. No provider, account, host install, security workload or spend is authorized.
- Keep remote Windows policy provider-neutral until a concrete milestone and threat model require a choice.

## 9. Proposed future tests, not acceptance IDs

PROP-ST-01..23 are temporary proposal identifiers only. They do not replace or extend native RevDev/PocketCode acceptance suites. Run only after PC access returns, explicit owner authorization, fresh read-only recon and a disposable test environment.

- **PROP-ST-01..03, read-only recon:** Windows edition/build; existing sandbox accounts/groups/firewall/WFP filters/UAC; inventory RevDev's actual network/TLS, IPC, process-tree and filesystem requirements.
- **PROP-ST-04..09, token/filesystem:** inspect token flags/SIDs; probe allowed workspace, sibling, temp and Everyone-writable paths; credential and guard-file reads; protected-child delete/rename via parent; junction/symlink/8.3/case aliases; recursive-delete command variants.
- **PROP-ST-10..14, network:** direct TCP/UDP/QUIC; AppContainer child; anonymous and deny-only token shapes; loopback service access; discrepancy between WFP status and actual filters.
- **PROP-ST-15..17, process/failure:** broker/runner kill and orphan behavior; malformed settings/token-creation failure and no downgrade; crash during ACL grant and recovery/refcount cleanup.
- **PROP-ST-18..20, compatibility:** Schannel clients, named-pipe/build-server tools, and RevDev P8U publisher/recovery interactions.
- **PROP-ST-21..23, shared machine/cleanup:** second-user access to grants/secrets; uninstall completeness; helper-binary replacement/integrity checks.

No proposed test has been run. These are not canonical acceptance criteria.

## 10. Exact unresolved source questions

**Codex**
- Read pinned ACL, account/group, firewall, setup, runner-pipe, environment, process-spawn and cleanup modules.
- Verify exact firewall rule scope and bypass surfaces.
- Verify process/job-object containment and orphan behavior.
- Verify default Windows policy, stale setup behavior, denied elevation and no-downgrade semantics.
- Verify persistent ACL cleanup/uninstall and helper-binary integrity at a pinned commit.
- Resolve .git/.codex/.agents deny coverage and parent delete/rename behavior against exact source.

**srt**
- Read pinned TypeScript wrapper/manager and Rust CLI/install/probe/runner/WFP/ACL sources.
- Verify WFP layer coverage for TCP/UDP/QUIC and inbound/receive paths.
- Verify partial filter-set detection and the #716/#723 status discrepancy from issue/PR bodies and source.
- Verify ACL grant/cleanup/recovery/refcount semantics and failure injection.
- Verify job-object flags, process-tree termination, reparse-point/TOCTOU handling and helper integrity.
- Confirm README Schannel behavior and version-specific details at a pinned release.

**Both**
- Establish exact commit SHA, LICENSE/NOTICE, source path/symbol and line range for every claim used in a decision.
- Distinguish code-demonstrated behavior, project documentation, test evidence, inference and unknown.
- Do not infer safety from vendor reputation, green CI or a successful narrow probe.

## 11. Recommended next work

1. Keep this audit in PARTIAL / STUDY ONLY status.
2. When Gemini returns, ask for an independent review of Codex token/ACL/process creation and srt WFP/ACL/failure/cleanup source, with exact pinned commits and code references. Gemini must challenge this report, not simply restate it.
3. Ask Claude, when available, to continue with OpenHands EventLog/state/persistence and Happy pairing/encryption source as separate assignments. Do not let timeout pressure turn an incomplete read into a completion claim.
4. Do not redo the broad 70-candidate research pass. The remaining work is bounded source reading and cross-checking.
5. Defer all PC tests and sandbox installation until PC access returns and the owner explicitly authorizes a disposable test environment.
6. Continue existing PocketCode fixed-task and state/identity work; do not let Windows sandbox research displace the canonical product milestone.

## 12. Non-actions

No source code, implementation, tests, schemas, canonical acceptance IDs, provider, account, host, firewall, WFP, ACL, queue, watcher, runtime, installation, elevation, deployment, PR, merge, billing or spend was changed or exercised. No PC tests or device tests were run. RevDev's current PC state remains UNKNOWN.


## 13. Additional pinned-source review of srt Windows enforcement — 2026-11-01

ChatGPT used the GitHub tree/API to read additional srt files at merge commit 81145771c9bfc51c5669f071b515209321e0d078. This closes several of Claude's source-read gaps, but does not complete the audit or validate Windows runtime behavior.

### 13.1 Token construction: direct source read

Pinned file: vendor/srt-win-src/src/token.rs, blob 56b4c4fd402db4ca8b2f525f3be5b1ad92e83f1c.

At this commit:
- Restricted-token flags are LUA_TOKEN | WRITE_RESTRICTED when write restriction is enabled; LUA_TOKEN alone otherwise. There is no DISABLE_MAX_PRIVILEGE flag in this srt function.
- SIDs to disable are BUILTIN\Administrators plus every SE_GROUP_LOGON_ID group in the base token. This differs from the inspected Codex call, which passed zero disabled SIDs.
- Privileges to delete are every privilege in the base token except SeChangeNotifyPrivilege. This differs from the inspected Codex call, which passed zero privileges-to-delete.
- The write-restricting SID list is capability SIDs (duplicates removed), then the sandbox user's own user SID, Everyone and NT AUTHORITY\RESTRICTED.
- After CreateRestrictedToken, srt reads the token's restricting-SID list and write-restricted flag back and rejects a mismatch.
- It sets medium integrity and a default DACL granting GENERIC_ALL to SYSTEM and the sandbox user SID.

This is a material implementation difference, not just documentation wording. It should be explicitly compared in any future independent review.

### 13.2 WFP: exact layers and known protocol gap

Pinned file: vendor/srt-win-src/src/wfp.rs, blob c3af835ec1479ac19bb1b35181a23d89e5c55640.

Source declares exactly two connect layers: FWPM_LAYER_ALE_AUTH_CONNECT_V4 and FWPM_LAYER_ALE_AUTH_CONNECT_V6. The installed set is four filters when loopback is closed, six when loopback-open is enabled. The filters are persistent and machine-wide. The normal proxy permit is limited to the configured loopback proxy port range (default 60080–60089). The open-loopback permit exposes every TCP/UDP loopback port except the dedicated probe port.

The same source comments state that anonymous-token and deny-only-user-SID socket creation is not matched by the BLOCK and is reported as a residual. The user SID is retained in the restricting-SID list because the WFP block is keyed to it. PR #745's all-packages SID change is present in the pinned source's SDDL tests.

**ICMP is explicitly outside this fence.** At the pinned commit, test/sandbox/winsrt.test.ts (blob 29a4ed5bc201ee093a6b1c6c82e7294bb4189508), around line 5198, has a Windows test named "R2: ICMP (ping) is NOT fenced" and explains that ICMP does not traverse ALE_AUTH_CONNECT. Do not describe srt's Windows network fence as blocking all network protocols. UDP/QUIC, inbound traffic, raw sockets and service-mediated egress still need their own exact coverage review; do not infer coverage beyond the inspected layer/test evidence.

### 13.3 WFP status false-positive: source confirms the concern

At the same pinned srt commit, vendor/srt-win-src/src/wfp.rs filter_status (around lines 870–905) sets state to installed when tags contain ANY block-user filter. It does not require the expected block and proxy-permit filters at both IPv4 and IPv6 connect layers.

The current srt main branch was independently refreshed at 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77. Its wfp.rs blob remains c3af835ec1479ac19bb1b35181a23d89e5c55640 and still has the same any-block installed check.

Issue #723 is open and reports one-machine Windows 11 build 26200 measurements: deleting one address-family block filter can leave status at installed; the default IPv4-only verify wrapper can pass while IPv6 is open; and plain install can early-return without repairing the partial set. These are issue-reporter measurements, not measurements performed by ChatGPT, and the issue itself lists important untested cases.

PR #716 is open, not merged, at head 5839245ed44cf01e42f5c603ceb810484d1b635f. Its proposed change introduces partial status when expected filter parts are missing and makes plain install repair partial sets. The branch's windows-sandbox-utils.ts default probe still binds 127.0.0.1 only; the normal wrapper does not independently test ::1. The PR description also notes that without a readable install record, an open-loopback set that lost both open-loopback permits can be mistaken for a closed set because the remaining filters do not reveal the prior mode.

Disposition: this is a material open readiness/repair concern. Do not describe the current main fence status as complete or self-healing. Re-check PR #716 and issue #723 before any later evaluation.

### 13.4 Process-tree containment: direct source read

Pinned files:
- vendor/srt-win-src/src/job.rs, blob d9d3f19c2b061fb7ae43dd94437223b3a09aa561.
- vendor/srt-win-src/src/launch.rs, blob c25c3a57aa2aadb4ea6c9208009276d3575c489f.
- vendor/srt-win-src/src/runner.rs, blob 43e746e5e0a4d712bc587afa47871c9a67930815.
- vendor/srt-win-src/src/install.rs, blob 9466d08fb2ac7bc20ec96abcb70c0d17d5d2d1e4.
- src/sandbox/windows-sandbox-utils.ts, blob fb8f0aa206724e1b52719d564c99b1ede71ae4c7.

Source shows:
- Broker launches a runner as the dedicated srt-sandbox account using CreateProcessWithLogonW; runner launches the target using CreateProcessAsUserW with the restricted token.
- The runner creates a child Job Object with KILL_ON_JOB_CLOSE and without BREAKAWAY_OK. It creates the target suspended, assigns it to the job, applies runner-thread self-protection, then resumes it. The job's lifetime therefore owns the child process tree; closing the job terminates remaining members.
- A separate broker-to-runner job can permit breakaway so the child can be assigned to the runner's load-bearing job. The runner-to-child job disallows breakaway.
- The Job Object also applies explicit UI restrictions for clipboard read/write, global atoms, USER/GDI handles from outside the job, system parameter writes, display settings, desktop switching and ExitWindows.
- Launch code requires a non-default isolated desktop and refuses if that check fails. It uses an explicit inherited-handle whitelist, process mitigations and a suspended-spawn/assign/resume sequence.
- Under write-restricted mode, runner self-protection and thread self-protection are required and failures abort. In the non-write-restricted path, broker DACL self-protection failure is logged as a warning rather than fatal.

This verifies the documented job-object pattern in source. It still does not prove all process-creation, inherited-handle, service, kernel or OS escape classes are closed.

### 13.5 ACL and persistence: direct source read

Pinned files:
- vendor/srt-win-src/src/acl.rs, blob fe3aca61a1512e5f3e27c3b2de21c7e337320c22.
- vendor/srt-win-src/src/state_db.rs, blob 428b6354fd2ea8ecab2a8ab7ee95680ef7ce7653.
- vendor/srt-win-src/src/persist.rs, blob 51f377d4b220a9812ba10d03604176819d312c43.
- vendor/srt-win-src/src/ambient.rs, blob 31f2b19da5f19c3dfef2bcf1edb961d379e7151d.

Source confirms:
- ACL grants and denies are additive explicit ACEs for the dedicated sandbox-user SID; the design avoids replacing the whole security descriptor.
- Modify grants include DELETE for the object but withhold FILE_DELETE_CHILD. Denies are applied on the target and include a parent FILE_DELETE_CHILD deny. A separate object-only DELETE deny protects placeholder intermediate directories without denying reads across a future subtree.
- Per-user SQLite session state tracks brokers, ACE holders, working ACEs and persistent grants/denies. Rows bind canonical paths to file identity. A per-user file lock serializes whole operations; recovery runs on every lock acquisition after a holder dies.
- The state DB documentation describes record-first ordering before the DACL write, per-path commits rather than one global transaction, recompose from live holders, and keeping rows/denies when release cannot safely converge. Persistent roots and ambient denies have distinct holderless lifetimes and are removed through explicit forget/uninstall paths.
- Ambient write-denies are installed for selected shared write locations such as ProgramData, Public and Windows Temp, and are folded into every recompose so session grant/release/recovery cannot silently strip them.

These are implementation details, not proof that every filesystem object, reparse point, race or crash case is safe. The persistent state and cleanup paths remain high-impact and require dedicated failure testing.

### 13.6 Shared-machine CA-key trade-off

Pinned file vendor/srt-win-src/src/install.rs documents that the ProgramData CA key-material directory is deliberately writable by BUILTIN\Users to support unelevated self-heal. Its comments explicitly accept that any real local user can read or replace the CA key material, while the sandbox group is denied access and the sandbox account is expected to be network-confined. This is a documented design trade-off, not a verified exploit, but it makes the shared-machine threat model especially important. Do not treat the install as safe for concurrent/untrusted local users without owner review.

### 13.7 Updated assessment

The additional source reads improve confidence that srt has deliberate token hardening, additive ACL semantics, refcounted crash recovery, job-object process-tree containment and layered launch protections. They also expose a concrete gap in the current WFP status/verification story and the explicit ICMP exclusion.

srt remains STUDY ONLY. Its Windows alpha status, residual token shapes, ICMP non-coverage, open partial-filter status issue, IPv4-only default probe, machine-wide install and shared-machine CA-key trade-off prevent calling it a complete or selected boundary. No runtime test was performed by ChatGPT.
