# PocketCode Architecture

**Status:** Conceptual only. No stack or provider has been selected.

## Candidate architectures (none selected)

The remote-runner diagram below is only one candidate. No runtime location, app framework, backend, cloud provider or sandbox has been selected. Compare the alternatives on the same bounded task before implementing this shape.

### Candidate A — hosted/remote execution

The proposed provider-neutral request/result lifecycle and file/security constraints are documented in [PRODUCT/EXECUTION_CONTRACT.md](PRODUCT/EXECUTION_CONTRACT.md). That contract is a design proposal for a server-backed runner, not an implemented or approved public API.

In this candidate, a mobile-first web client communicates with an application API. The API authenticates the user, validates a run request, stores minimum necessary metadata, and dispatches execution to a disposable isolated worker. The worker returns structured results. The API exposes a bounded result stream or polling endpoint to the client.

Mobile browser
  -> HTTPS authenticated requests
Application API
  -> identity and authorization
  -> project/file metadata
  -> run limits and job state
  -> result/report API
  -> dispatch with scoped, short-lived job data
Execution coordinator
  -> disposable isolated worker
Worker
  -> pinned runtime image
  -> CPU, memory, process, disk, output and time limits
  -> restricted network by default
  -> temporary workspace
  -> no host secrets or privileged access
Structured result
  -> stdout, stderr, exit status, timing, allowed output files

#### Trust boundaries for Candidate A

##### Client
- Treat displayed output and filenames as untrusted data.
- Never contain execution-provider secrets.
- Make running, queued, cancelled, timed-out, and failed states explicit.
- Do not interpret an API acceptance response as proof that execution succeeded.

##### Application API
- Authenticate and authorize every project, run, and result access.
- Enforce per-user quotas and request-size limits.
- Validate runtime identifiers and environment configuration against allowlists.
- Never accept arbitrary container, command, mount, or host configuration from clients.
- Issue short-lived job-scoped credentials only when unavoidable.
- Redact secrets from logs and user-facing reports.

##### Execution worker
- Assume submitted code is malicious or buggy.
- Use a disposable sandbox/VM/container arrangement whose isolation guarantees are reviewed, not assumed.
- Run unprivileged with no host mounts or privileged capabilities.
- Enforce wall-clock, CPU, memory, process count, disk, output-size, and concurrency limits.
- Disable outbound networking by default until a safe package-install strategy is designed.
- Avoid access to cloud metadata endpoints, internal services, and control-plane credentials.
- Destroy the workspace after the configured retention window.

##### Storage
- Keep project files and results separate by user and project.
- Use explicit retention and deletion behavior.
- Do not persist arbitrary worker state unless a documented product need exists.
- Public repository files must not contain real user code or production secrets.

#### Example lifecycle for Candidate A only

A hosted/remote run should have a stable identifier and a terminal outcome from a defined set:
- succeeded
- program_failed
- timed_out
- cancelled
- rejected
- infrastructure_failed

A result should include runtime/image version, start and end times, duration, exit status when available, bounded stdout/stderr, generated file metadata, and truncation/limit indicators. A missing exit status must not be fabricated.

### Candidate B — local device or browser-local execution

In a local candidate, code may run in an on-device interpreter or in a browser/WASM runtime rather than on a PocketCode server. That removes or changes some server/provider assumptions; it does not automatically establish sandboxing or hard resource limits.

- Test file access/export, package compatibility, app/browser API exposure, network behavior, persistence and interruption on the target device.
- State which CPU/memory/time/output controls are truly enforced, which are cooperative, and which are unavailable.
- Keep the same honest report vocabulary where it fits, but do not invent a remote job ID, provider status, cleanup event or server-side control when no such thing exists.
- Treat the browser/native embedding API and its permissions as part of the security boundary. WebAssembly alone is not proof of a complete sandbox.

## Open technical decisions

- Execution location: local device, browser/WASM, remote PC, hosted service, or a combination only if evidence justifies it.
- PWA framework and hosting.
- API language/framework.
- Sandbox provider and isolation level.
- Worker scheduling and queue model.
- Package installation and cache policy.
- Streaming versus polling.
- Authentication provider.
- Project/file storage and encryption.
- Observability, retention, and deletion.
- Whether any runtime needs a VM boundary stronger than a container.

## Design rule

Do not select infrastructure based only on developer convenience. Compare documented isolation guarantees, abuse controls, cleanup behavior, cost, latency, portability, and operational burden first.
