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


## 14. Additional pinned-source review of Codex Windows ACL, firewall and launch support — 2026-11-01

ChatGPT continued the Codex source review at the same exact commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635. This closes some of Claude's listed gaps and identifies ACL questions that need high-priority independent review. No Windows execution was performed.

### 14.1 Offline firewall: direct source read

Pinned file: codex-rs/windows-sandbox-rs/src/firewall.rs, blob b5dfb2ef49652176b2b17a02e55719d1e864b471.

Source confirms:
- The offline outbound rule is an enabled outbound BLOCK for NET_FW_IP_PROTOCOL_ANY, across all firewall profiles, with remote addresses excluding loopback and LocalUserAuthorizedList scoped to the offline sandbox user's SID.
- The rule configuration is read back; the code checks that the expected offline SID appears in LocalUserAuthorizedList.
- With local binding disabled, the code blocks UDP loopback and blocks TCP loopback except the configured proxy ports. It first installs a broad TCP block, then narrows the blocked remote-port complement so a failed narrowing update remains fail-closed.
- With allow_local_binding enabled, the code removes the loopback TCP/UDP block rules and the legacy proxy allow rule. This opens loopback to local services; it is not a narrow per-service permission.
- The rules are idempotently reconfigured by stable internal names. Failure to configure/read back the expected scope returns a setup error.

This upgrades the offline SID/firewall scope from third-party-only to source-verified at this commit. It does not prove that Windows Firewall is enabled, that external policy cannot override/disable the rules, or that every traffic mechanism is covered on a real host.

### 14.2 ACL source: high-priority deny-application concerns

Pinned file: codex-rs/windows-sandbox-rs/src/acl.rs, blob f351dba190a9f50a5362ea64fe5c6675bf5b3f8c.

Source confirms:
- The workspace write allow mask includes FILE_GENERIC_READ, FILE_GENERIC_WRITE, FILE_GENERIC_EXECUTE, DELETE and FILE_DELETE_CHILD.
- add_deny_write_ace applies an inheritable deny ACE to the target path itself, with write/append/attribute/delete and FILE_DELETE_CHILD rights. The inspected function does not add a separate FILE_DELETE_CHILD deny ACE to the target's parent, unlike srt's explicit parent-FDC design.
- The protected paths are created as directories if absent before the deny is applied; setup comments identify protected children such as .git, .codex and .agents.

Two code-level concerns require independent security review and targeted Windows tests:

**A. Parent-delete semantics:** a writable parent root is granted FILE_DELETE_CHILD, while the protected child receives a deny ACE on the child object. The inspected Codex helper does not explicitly deny FILE_DELETE_CHILD on the parent. Windows permits deletion through the parent right as an alternative to DELETE on the child, so this is a concrete possible carveout-bypass path to test. This report does not claim a runtime exploit has been demonstrated. Test protected directory/file deletion and rename through the writable parent, including nested paths and inherited ACEs.

**B. Incomplete-deny detection and silent ACL-write failures:** dacl_has_write_deny_for_sid returns true when a matching deny ACE overlaps ANY bit of the full deny-write mask; it does not prove that all required deny rights are present. add_deny_write_ace also returns Ok(false) when SetEntriesInAclW or SetNamedSecurityInfoW fails, rather than propagating the Win32 error. Ok(false) is also the no-new-ACE result, so callers cannot distinguish an already-present deny from these write failures. The setup caller logs only Err; it treats Ok(false) as no action. This is a source-level error-reporting/control concern, not a runtime exploit claim.

### 14.3 Setup error aggregation

Pinned file: codex-rs/windows-sandbox-rs/src/setup_main_win.rs, blob 78c0a8be8e53bcad0e2015a3d48d8b94d5533dde.

The full setup routine accumulates write-root and deny-path ACL errors in refresh_errors. The final explicit bail on a non-empty refresh_errors is conditional on refresh_only. The initial/full setup path is refresh_only=false, so this function does not turn those accumulated ACL errors into a failure at that final check. This deserves review alongside the silent Ok(false) behavior above. Firewall setup errors and sandbox-directory lock errors have separate direct error paths. Do not generalize this finding to every setup operation.

### 14.4 Firewall and ACL interaction

The Codex write allow mask includes FILE_DELETE_CHILD. The deny helper applies its inheritable deny on the protected target, but no parent-FDC deny was found in the inspected helper. srt's ACL helper explicitly denies FILE_DELETE_CHILD on the parent. This difference makes parent-mediated deletion a high-priority comparative test, especially for RevDev's destructive-operation refusal. Keep this as a proposed test until validated on Windows.

### 14.5 Accounts, credentials and helper materialization

Pinned files:
- codex-rs/windows-sandbox-rs/src/sandbox_users.rs, blob 13460b94444ec084db8bbd0c3f998e1739207b77.
- codex-rs/windows-sandbox-rs/src/dpapi.rs, blob c4dcc79fa602860714af3fe606bea44c1a583d6b.
- codex-rs/windows-sandbox-rs/src/helper_materialization.rs, blob b7d00e1dd9263f9e6476bcd456a3da2319efed2d.
- codex-rs/windows-sandbox-rs/src/setup_main_win.rs, same blob as §14.3.

Source confirms:
- Codex provisions separate offline and online local user accounts and a CodexSandboxUsers group.
- The sandbox user password blobs are protected with DPAPI machine scope (CRYPTPROTECT_LOCAL_MACHINE), then stored in the sandbox secrets directory. The setup code applies a DENY for the sandbox group to that secrets directory; the sandbox bin directory is locked so the sandbox group gets read/execute while the real user retains write access.
- Machine-scope DPAPI means the file ACL is an important access boundary; this is not user-bound DPAPI encryption.
- Helper materialization uses file size and modification time to decide whether the copied helper is fresh. It uses a temporary file in .sandbox-bin and rename, but does not compute a cryptographic hash or verify a signature in the inspected path. The sandbox group is given read/execute rather than write access to the helper directory, which is a separate mitigating ACL. Do not describe the freshness check as cryptographic integrity verification.

### 14.6 Elevated runner IPC and process containment

Pinned files:
- codex-rs/windows-sandbox-rs/src/elevated/runner_pipe.rs, blob c8ae092c4a00fc3e029be48cb77cc78db4580d87.
- codex-rs/windows-sandbox-rs/src/process.rs, blob 1571bb8ccf47c798787e5d1eee3e18de277dc74a.
- codex-rs/windows-sandbox-rs/src/spawn_prep.rs, blob 1b3704d6a26287d578eb5b30945d53b683607f6d.

Source confirms:
- Elevated runner IPC uses a random 128-bit nonce in paired pipe names.
- Pipe DACL is sandbox-user-only, and the parent checks GetNamedPipeClientProcessId against the runner PID it just launched.
- The inspected process.rs path uses CreateProcessAsUserW with an explicit stdio handle list in the pipe path. It does not create the process suspended or assign it to a Job Object in this module.
- No Job Object/kill-on-close containment was found in the inspected Codex Windows sandbox files. This is not proof that no other surrounding component provides process-tree handling; descendant orphan behavior remains UNKNOWN until the full launch/cancellation path is inspected and tested.
- spawn_prep applies allow/deny path ACL preparation and computes write roots/deny carveouts, but does not close the parent-FDC question above.

### 14.7 Updated Codex assessment

Codex now has source-verified token construction, offline firewall rule construction, SID scoping/read-back, two local accounts, protected secret-directory setup and elevated named-pipe IPC. Its source also reveals priority questions: target-only deny ACEs versus parent FILE_DELETE_CHILD grants, incomplete deny-presence detection, swallowed ACL API errors, initial-setup error aggregation, no Job Object in the inspected process launch path, and size/mtime rather than cryptographic helper integrity.

These findings lower confidence in adopting Codex without further review; they do not establish that the shipped product is exploitable. The exact ACL and setup concerns need independent security review and disposable Windows tests. Codex remains STUDY ONLY.

### 14.8 Non-actions

No Windows test, build, installation, source edit, PR, host operation, queue action, schema change, canonical acceptance change, provider, spend or deployment was performed. Source reading only.


## 15. Source navigation anchors

Line numbers below refer to the exact pinned refs/blobs already listed in Sections 2, 13 and 14.

### srt at 81145771c9bfc51c5669f071b515209321e0d078
- token.rs (blob 56b4c4fd402db4ca8b2f525f3be5b1ad92e83f1c): flags/SID list around 82–112; token construction and read-back around 220–320; default DACL around 375–420.
- wfp.rs (blob c3af835ec1479ac19bb1b35181a23d89e5c55640): layer/fence design around 1–55; transactional filter installation around 620–755; status logic around 870–905; filter completeness tests around 990–1145.
- acl.rs (blob fe3aca61a1512e5f3e27c3b2de21c7e337320c22): additive ACE model around 1–25; masks around 100–130; grant/deny and parent-FDC behavior around 930–1015; ACE composition around 1060–1135.
- job.rs (blob d9d3f19c2b061fb7ae43dd94437223b3a09aa561): kill-on-close and UI restrictions around 1–124.
- launch.rs (blob c25c3a57aa2aadb4ea6c9208009276d3575c489f): fail-closed launch and self-protection around 115–205; suspended process creation, job assignment and resume around 267–345.
- runner.rs (blob 43e746e5e0a4d712bc587afa47871c9a67930815): broker-to-runner command boundary and dispatch around 1–170.
- install.rs (blob 9466d08fb2ac7bc20ec96abcb70c0d17d5d2d1e4): machine store and CA-key DACL trade-off around 1–95.
- state_db.rs (blob 428b6354fd2ea8ecab2a8ab7ee95680ef7ce7653): refcount/disk-is-truth/crash-recovery design around 1–46; holder/persistent table definitions around 77–180.
- persist.rs (blob 51f377d4b220a9812ba10d03604176819d312c43): persistent grant/deny recovery and forget logic, including crash recovery around 729–800 and 1152–1190.
- ambient.rs (blob 31f2b19da5f19c3dfef2bcf1edb961d379e7151d): install-time ambient deny targets and cleanup semantics around 1–50.
- probe.rs (blob e961cf81e8772f20ddbcd5691617fdbefa3ee750): token-shape verification and residual classification around 1–300 and 300–620.
- windows-sandbox-utils.ts (blob fb8f0aa206724e1b52719d564c99b1ede71ae4c7): default IPv4 loopback readiness probe around 1669–1725.
- winsrt.test.ts (blob 29a4ed5bc201ee093a6b1c6c82e7294bb4189508): explicit ICMP-not-fenced test around 5195–5201.

### Codex at 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635
- token.rs (blob 71a4b1dd7c0a9aa70dad76313cb89dcdadcc7119): restricting SID list and CreateRestrictedToken around create_token_with_caps_from.
- firewall.rs (blob b5dfb2ef49652176b2b17a02e55719d1e864b471): offline firewall rules around 25–200; rule configuration and LocalUserAuthorizedList read-back around 206–290.
- acl.rs (blob f351dba190a9f50a5362ea64fe5c6675bf5b3f8c): deny-presence predicate around 217–260; write grant mask around 262–345; add_deny_write_ace around 452–510.
- setup_main_win.rs (blob 78c0a8be8e53bcad0e2015a3d48d8b94d5533dde): firewall setup around 578–620; write-root grants and deny-path ACL handling around 642–800; refresh-only error bail around 890–895.
- sandbox_users.rs (blob 13460b94444ec084db8bbd0c3f998e1739207b77): local account/group provisioning around 35–160; machine-scope DPAPI blob writing around 360–490.
- dpapi.rs (blob c4dcc79fa602860714af3fe606bea44c1a583d6b): CRYPTPROTECT_LOCAL_MACHINE around 1–80.
- helper_materialization.rs (blob b7d00e1dd9263f9e6476bcd456a3da2319efed2d): size/mtime freshness and temp-file copy/rename around 210–360.
- elevated/runner_pipe.rs (blob c8ae092c4a00fc3e029be48cb77cc78db4580d87): random pipe names, DACL and client PID verification around 47–130.
- process.rs (blob 1571bb8ccf47c798787e5d1eee3e18de277dc74a): CreateProcessAsUserW and explicit handle list around 85–205.
- spawn_prep.rs (blob 1b3704d6a26287d578eb5b30945d53b683607f6d): allow/deny ACL preparation and write-root derivation around 218–310.

These anchors are source-navigation aids, not proof of runtime behavior. All line-range claims remain tied to the stated commit.


## 16. Follow-up: srt WFP partial-set and IPv6 verification gap — current-main recheck 2026-11-01

This section separates the source defect, the open repair PR, the separate IPv6 verifier proposal, and the limits of external Windows measurements.

### 16.1 Current main is still on the vulnerable status implementation

Current anthropics/sandbox-runtime main resolves to commit 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77. At that ref:
- vendor/srt-win-src/src/wfp.rs blob remains c3af835ec1479ac19bb1b35181a23d89e5c55640.
- filter_status() collects tagged filters and sets have_block = tags.iter().any(|(_, t)| t.kind == KIND_BLOCK_USER). It reports installed if ANY block-user filter remains, otherwise absent. It does not require the IPv4 and IPv6 block filters, nor both proxy permits, to be present.
- src/sandbox/windows-sandbox-utils.ts blob is dbc7c23f4373c69403109429a41144018111941b. verifyWindowsWfpEgress() creates its default listener bound only to 127.0.0.1, then invokes srt-win wfp verify against that IPv4 target. It does not create an IPv6 listener or run a second family-specific probe.

This directly confirms the two implementation gaps reported in issue #723. These are source facts at the stated current-main snapshot.

### 16.2 Issue #723: observed partial-filter behavior

Open issue: https://github.com/anthropics/sandbox-runtime/issues/723

The reporter's detailed body describes tests on one Windows 11 build 26200, with srt-win built from 24eb39e94a6de386e83d126c52317d8e0fa49522, using loopback listeners and three repetitions per state:
- Delete the IPv6 block filter: status still says installed; IPv4 probe says blocked; IPv6 listener accepts; the default IPv4-only verifyWindowsWfpEgress passes; plain install exits 0 with "already installed" and does not restore the filter.
- Delete the IPv4 block filter: the IPv4 runtime probe fails closed.
- Delete both permit filters: status still says installed, but plain install fails with an unknown port range.
- install --force restores the full filter set in the tested cases.

The report explicitly says it did NOT test real IPv6/internet egress, other Windows builds, reboot with a partial set, non-elevated status, or service-originated traffic. Treat it as a detailed externally reported reproduction, not an independently repeated test or universal Windows result.

### 16.3 PR #716 is open and proposes a partial-state repair, but is not merged

PR: https://github.com/anthropics/sandbox-runtime/pull/716

GitHub currently reports PR #716 as open and unmerged. Its diff:
- Adds partial WFP status.
- Defines a complete filter set by checking required proxy-permit and block-user entries at both IPv4 and IPv6 ALE connect layers, and checks consistency of proxy ranges and sandbox user SID tags.
- Uses the recorded loopback mode to detect when all open-loopback permits disappeared.
- Makes partial installations visible to dependency checks and allows a plain install to repair when the requested configuration matches; --force is required when the existing recorded configuration differs.
- Adds unit tests that remove each filter from an in-memory enumerated set and expect partial, plus config/repair tests.

The PR's Rust tests are source-level/unit tests. They are not, by themselves, a Windows integration test that deletes a live WFP filter and observes repair. The issue reporter separately states that the PR branch was measured on the same setup, three times per state, with the partial state detected and repaired. That is useful external evidence, but still one machine and not our independent execution.

### 16.4 A separate IPv6 readiness-probe change is not part of PR #716

A follow-up comment on issue #723 describes a separate, unmerged branch for dual-family verifyWindowsWfpEgress:
- Bind a loopback listener on both 127.0.0.1 and ::1.
- Run wfp verify once for each family.
- Fail closed if either family cannot be bound or is not blocked.
- Adjust the --allow-loopback probe target to match the destination family.

The reporter gives 3/3 measurements per state for that branch on the same test setup, including the missing-IPv6-block case. The branch's source was not fetched in this audit and no PR was identified in the comment. Do not attribute this improvement to PR #716 or current main.

### 16.5 Other srt egress gaps are intentional and test-documented

At the same pinned PR #745 merge commit 81145771c9bfc51c5669f071b515209321e0d078:
- vendor/srt-win-src/src/wfp.rs installs filters only at FWPM_LAYER_ALE_AUTH_CONNECT_V4 and _V6.
- test/sandbox/winsrt.test.ts contains an explicit R2: ICMP (ping) is NOT fenced test. Its comment says ICMP does not traverse ALE_AUTH_CONNECT; the test expects ping not to fail with General failure.
- The same test file documents that Windows DNS resolution uses the DNS Client service under a NetworkService token, so the service's wire query does not carry the sandbox child's ALE_USER_ID. It runs node dns.lookup('google.com', ...) and expects successful resolution despite the sandbox network fence. This creates a DNS-query channel outside the child-token WFP block; do not describe the WFP fence as complete network isolation or complete DNS-exfiltration prevention.
- The WFP module itself documents that its BLOCK is keyed to the token user SID and does not match anonymous-token or deny-only-user-SID shapes. wfp verify reports these as residuals; the PR #745 description says they are warnings and do not change the pass result. Lowered-integrity probes that cannot be set up are also reported as unprobed residuals rather than failing the fence.

The default IPv4-only probe gap is separate from the deliberate ICMP/DNS service limitations. A passing probe proves only the tested direct-connect/token/family/target cases, not all network egress.

### 16.6 ACL and persistence details confirmed at the pinned srt source

At 81145771c9bfc51c5669f071b515209321e0d078:
- acl.rs defines MODIFY_NO_FDC as read/write/execute plus DELETE, explicitly without FILE_DELETE_CHILD. Deny targets receive a parent FILE_DELETE_CHILD deny; placeholder intermediate directories receive object-only DELETE denies so the intermediate cannot be renamed/rmdir'd to bypass a leaf stamp.
- state_db.rs describes a per-user SQLite session store, exclusive file lock across brokers, refcounted holders and working ACE rows. It records intent before applying each DACL mutation, commits path-by-path rather than one global transaction, and runs crash recovery when the lock is acquired.
- persist.rs records unfinished persistent DACL writes and replays them after a crash; explicit forget is the removal route for kept roots.
- install.rs documents an accepted shared-machine trade-off: BUILTIN\\Users has modify access to the machine CA-key material under ProgramData so unelevated self-heal can rewrite it. The sandbox group is explicitly denied. The source comment states any real local user can read or replace that CA key material. This is a documented trust decision, not a demonstrated exploit.

### 16.7 Updated interpretation

srt's Windows design is more carefully layered than a simple WFP+ACL summary suggests: restricted-token read-back, per-family WFP filters, additive ACL grants/denies, parent-FDC protection, job-object containment, persistent-write journaling and crash replay are all visible in source.

But three separate gaps must remain explicit:
1. Filter-set health: current main's installed state can mask a missing family filter; PR #716 proposes a fix but remains unmerged.
2. Readiness coverage: current main's default helper probes IPv4 loopback only; a separate proposed branch adds IPv6.
3. Protocol/service coverage: ICMP and DNS Client service-originated DNS queries are outside the direct child-token ALE_AUTH_CONNECT fence; anonymous and deny-only token shapes are residuals.

srt remains STUDY ONLY / ALPHA, not a recommended dependency or selected host boundary. No runtime test was run by ChatGPT.

### 16.8 Non-actions

No srt PR was merged or modified. No code was changed in either upstream project. No Windows test, build, installation, WFP mutation, ACL mutation, host action, RevDev/PocketCode source change, schema, acceptance, provider, spend or deployment was performed.
