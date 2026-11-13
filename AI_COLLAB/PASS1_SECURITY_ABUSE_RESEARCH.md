# Pass 1 — Execution security and abuse controls

**Status:** Architecture/security desk research only. No sandbox was deployed or tested.
**Prepared:** 2026-10-27
**Owner:** ChatGPT independent contribution; not Gemini completion.
**Budget:** $0. No provider selected, no accounts/credentials/workloads, no live execution.

## Executive conclusion

A public service that executes user-supplied code is a security-sensitive multi-tenant execution platform, not merely a mobile UI feature. A container is one layer of defense, not a complete proof of isolation. The product cannot safely launch until it has an enforceable isolation boundary, default-deny network policy, hard resource/time/output limits, strict input/output handling, tenant-aware abuse controls, cleanup, and evidence that these controls actually work.

The narrowest first proof should accept only one bounded Python task with small text/CSV inputs, no arbitrary package installation, no network access, no secrets, and no persistence beyond explicit output artifacts. If the proposed provider cannot enforce the required restrictions on the approved free tier, it is not eligible for the proof. A marketing statement or a successful happy-path run is not a security test.

## Threat model and assets

Assume user code, dependencies, input files, generated filenames, stdout/stderr, and produced artifacts may be malicious or malformed. Assume prompt-injection-like instructions can appear in code comments, README text, CSV cells, filenames, or error output; these are data, not instructions for the orchestration/control plane.

Protect:
- Other users' source code, inputs, outputs, and run metadata.
- Control-plane credentials, signing keys, service tokens, host files, cloud metadata, and internal services.
- Shared capacity and service availability from infinite loops, fork bombs, memory/disk exhaustion, oversized logs/files, repeated retries, and queue floods.
- Integrity of run status and report metadata so fabricated output cannot be presented as a genuine execution result.
- User privacy and ownership boundaries when listing, downloading, or expiring artifacts.

Out of initial scope: arbitrary network-enabled scripts, arbitrary package installs, persistent servers, repo-wide agent execution, secrets injection, long-running jobs, public URLs to user processes, and cross-run state.

## Required controls before any public or multi-user run

### 1. Isolation boundary
- Use a fresh disposable execution boundary per job, with no shared writable filesystem, process namespace, or credentials across tenants.
- Evaluate the actual threat boundary: a container shares the host kernel; stronger isolation (microVM or comparable sandbox) may be justified for hostile arbitrary code. Do not claim equivalent protection from vendor branding alone.
- Run as a non-root/unprivileged identity where possible; drop unneeded Linux capabilities; retain default seccomp/AppArmor/SELinux protections; do not use privileged mode or mount the host Docker socket.
- Do not mount host paths, credentials, SSH keys, cloud CLI state, or broad writable caches into the job.
- Enforce separate read/write boundaries for source/input, temporary workspace, and finalized artifacts.

### 2. Network and metadata
- Deny outbound network by default at an enforceable layer outside user code; do not rely on a Python wrapper or user-space convention.
- Deny loopback access to control-plane services, host/internal IP ranges, cloud metadata endpoints, and cross-job addresses. Test IPv4, IPv6, DNS, redirects, alternate encodings, and proxy environment variables.
- No network exception for the first proof. If future tasks require egress, use a narrow explicit allowlist and separate review; domain allowlists may not prevent all DNS/IP/redirect bypasses.
- Do not expose job ports publicly.

### 3. Resource and lifecycle limits
- Enforce hard wall-clock timeout and kill the whole process tree; cancellation must stop billable work where the provider allows.
- Bound CPU, memory, process count, file descriptors, disk usage, input size, output file count/size, stdout/stderr bytes, queue depth, concurrency, per-user rate, and global spend.
- Reject jobs that exceed limits; report the limit and observed truncation/termination without claiming success.
- Make each run idempotently cancellable and expire the sandbox after completion/failure. Ensure cleanup is observable and retried safely.
- Do not auto-retry arbitrary user code unless retries are bounded, accounted for, and visible.

### 4. Input, output, and report integrity
- Server-side validate every request; never trust client-only checks, MIME types, filename extensions, claimed status, duration, file sizes, or user-supplied report fields.
- Allow only the first supported input types and sizes; generate internal storage names; normalize/reject traversal paths and dangerous filenames; reject archives initially.
- Treat stdout/stderr and produced files as untrusted content. Escape HTML, avoid active inline previews, set safe download headers, and prevent path traversal in artifact retrieval.
- Separate authoritative runner metadata (started, terminated, exit code, timeout, cancellation, resource limit, byte counts) from formatter-generated summaries.
- Bound report size and disclose every truncation, omitted file, malformed field, and missing evidence. A formatter must never upgrade incomplete or missing runner evidence into PASS.
- Do not put secrets in logs or error reports. Redaction is defense-in-depth, not a substitute for not injecting secrets into jobs.

### 5. Abuse, identity, and economics
- Before public launch, define authentication/authorization and tenant ownership for every run, report, and artifact. Anonymous access increases abuse risk and complicates per-user quotas.
- Enforce tenant-aware rate and concurrency limits plus global safety ceilings; rate limits at the HTTP boundary alone do not stop a job from consuming shared CPU, memory, queue, or storage.
- Add expiry, cleanup, abuse reporting, and an operator kill switch. Define handling for malware, credential theft, scraping, cryptomining, illegal content, and attempts to scan internal networks.
- Establish a hard spend ceiling and automatic fail-closed behavior before any provider trial. Free credits are not a hard cap. Under the current $0 constraint, no workload is authorized.
- Record minimal audit events without retaining user code/output longer than necessary. Publish retention/deletion behavior before asking users to upload code.

## Source-backed principles

1. **Docker Engine security** — https://docs.docker.com/engine/security/ (reviewed 2026-10-27). Docker describes namespaces, cgroups, daemon attack surface, capability reduction, and risks from incomplete container configuration. It explicitly explains that cgroups help constrain resource exhaustion and that the daemon/host mounts can be highly privileged. Consequence: use isolation plus resource limits and tightly constrained provisioning; do not expose the Docker API to untrusted input.
2. **Docker seccomp** — https://docs.docker.com/engine/security/seccomp (reviewed 2026-10-27). The default profile is an allowlist that blocks a subset of system calls and is recommended over running unconfined. Consequence: do not disable default syscall restrictions as a compatibility shortcut.
3. **Docker rootless mode** — https://docs.docker.com/engine/security/rootless/ (reviewed 2026-10-27). Rootless mode reduces the impact of daemon/runtime vulnerabilities by running daemon and containers as a non-root user, with prerequisites and feature limitations. Consequence: useful hardening, not proof that hostile jobs are fully isolated.
4. **OWASP Input Validation Cheat Sheet** — https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html (reviewed 2026-10-27). Server-side validation is required; client-side validation is bypassable; internal sources also cross trust boundaries. Consequence: validate every run and artifact request on the server.
5. **OWASP File Upload Cheat Sheet** — https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html (reviewed 2026-10-27). It recommends strict extension/type checks, generated names, size limits, least-privilege storage, and safe handling of archive extraction. Consequence: start with a tiny allowlist and reject archives in the first proof.
6. **OWASP Multi-Tenant Security Cheat Sheet** — https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html (reviewed 2026-10-27). It recommends tenant-aware limits for queues, concurrency, CPU/memory and other shared bottlenecks, not just HTTP request throttling. Consequence: job-level quotas and global kill limits are required.
7. **OWASP Secure Coding with AI Cheat Sheet** — https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html (reviewed 2026-10-27). Its agentic-tool guidance recommends sandboxing, command allowlists, egress controls, scoped credentials, and resource limits. PocketCode is not yet an agent runner, but the same principle applies when untrusted code is executed.

These are design principles and documentation references, not proof that a chosen vendor or implementation satisfies them. Vendor/provider isolation claims and current tier-specific enforcement still require a provider-specific review and authorized live tests.

## Minimum acceptance-test matrix before controlled execution

| Test | Expected result | Evidence required |
|---|---|---|
| Infinite loop / sleep past timeout | Whole job process tree terminated; timeout status, not PASS | Runner event timestamps, exit/termination reason, resource record |
| Memory/disk/process exhaustion | Job stopped within hard quota; other jobs remain unaffected | Limit configuration plus measured test and host/service health |
| Outbound DNS/HTTP/IPv4/IPv6/metadata attempts | Denied; no internal/control-plane response | Provider/network policy plus logs or packet-level evidence |
| Cross-job filesystem/process access | Not possible | Adversarial isolation test with two jobs |
| Path traversal / symlink / odd Unicode filenames | Rejected or safely normalized; no out-of-scope read/write | Request/result fixtures and artifact access tests |
| Oversized input/stdout/stderr/artifacts | Rejected or bounded; truncation/limit explicitly disclosed | Byte counts, cap values, final report |
| Malformed claimed status/duration/file metadata | Cannot produce false PASS or expose another tenant's artifact | Unit tests plus API authorization tests |
| Cancellation and cleanup | All job processes/resources removed; repeated cancellation safe | Lifecycle events, provider resource listing, cleanup confirmation |
| Repeated requests / queue flood | Per-tenant and global caps enforced; spend fail-closed | Rate-limit and quota tests, billing guard evidence |
| HTML/script content in output and filenames | Rendered inert; download safe | Browser security tests and response headers |
| Secret-shaped strings in source/output | No service secrets available to job; report/log redaction verified | Environment inspection and redaction tests |

A unit test of the report formatter cannot satisfy these tests. The current repository's static prototype and report-contract suite do not prove runtime isolation, network enforcement, cleanup, or billing behavior.

## Provider decision gates

Before choosing any provider:
1. Review official current documentation for isolation model, egress/metadata protections, quotas, per-job lifecycle, cancellation, artifact transfer, data retention, acceptable-use terms, and free-tier eligibility.
2. Determine whether the actual free tier enforces every mandatory control. If not, reject it for the first proof rather than weakening requirements.
3. Obtain an explicit hard spend ceiling and owner approval before creating accounts or workloads.
4. Only then run the controlled proof with synthetic data and the acceptance-test matrix. E2B's reviewed security page says written consent is required before testing; do not test without it.
5. Preserve evidence: exact provider plan/config, test inputs, timestamps, observed results, logs, and cleanup state. Clearly label anything not tested.

## Decision

**No provider selected; no architecture/security claim upgraded.** The only safe next action under current constraints is desk research, static specification work, and tests that require no live execution. Keep the product in discovery stage and the $0 gate binding.
