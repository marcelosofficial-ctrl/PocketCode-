# Code Execution Backend Research

**Research snapshot:** 2026-10-20  
**Status:** Desk research only. No vendor selected. Prices and service terms change; recheck official documentation before implementation or spending money.

## Decision context

PocketCode may need to execute user-submitted code remotely so the same workflow works from iPhone and Android without requiring a personal computer or server. This introduces a serious trust boundary: user code must not run inside the main application process or gain access to application secrets.

The backend must be evaluated on isolation model, network policy, lifecycle/cleanup, output streaming, file handling, supported operating systems, cold-start latency, resource limits, regional availability, retention, API maturity, and total cost. A vendor's use of the word “sandbox” is not sufficient evidence by itself.

## Candidate options

### E2B

Official source: https://e2b.dev/

- Offers hosted sandbox infrastructure for AI agents and code execution.
- The official site describes a microVM-oriented open-source runtime and usage-based billing.
- At the research snapshot, the public pricing page advertised a free Hobby tier with a one-time usage credit, while Pro had a monthly base price plus usage costs.
- Potential fit: a purpose-built sandbox API and a familiar developer workflow.
- Must verify: current plans, actual execution/file/streaming APIs, time limits, region/data handling, network controls, free-tier restrictions, and total cost at expected use.

### Modal Sandboxes

Official sources:
- https://modal.com/products/sandboxes
- https://modal.com/docs/sdk/js/latest/Sandbox

- Provides disposable sandboxes, process execution, stdout/stderr streams, filesystem access, configurable CPU/memory, and egress controls.
- Official pricing is usage-based; the product page showed a monthly amount of included compute at the time of research.
- Potential fit: flexible execution environments and programmatic control.
- Must verify: account requirements, minimum charges, lifecycle billing, cold-start distribution, supported runtime images, quotas, region/data handling, and whether the operations model is appropriate for a small consumer product.

### Daytona Sandboxes

Official sources:
- https://www.daytona.io/docs/en/sandboxes/
- https://www.daytona.io/pricing
- https://www.daytona.io/docs/billing

- Provides programmatically managed execution environments. Official documentation describes Linux container sandboxes and additional VM-based options, including Windows and macOS environments for applicable workloads.
- The public pricing page showed pay-as-you-go resource pricing and a free compute allowance at the time of research.
- Potential fit: persistent or disposable environments, file operations, and multiple OS/runtime options.
- Must verify: the exact isolation tier for untrusted public submissions, billed lifecycle states, storage charges, idle behavior, network policy, account limits, and costs for short executions.

### Cloudflare Sandboxes / Workers

Official sources:
- https://developers.cloudflare.com/sandbox/
- https://developers.cloudflare.com/sandbox/concepts/
- https://developers.cloudflare.com/sandbox/concepts/security/

- Cloudflare documents container and Dynamic Worker sandbox options for generated or untrusted code, with the application controlling what data and network access the code receives.
- The documentation states that the sandbox feature is available on a Workers Paid plan at the time of research.
- Potential fit: integration with a web application and edge-oriented request handling.
- Must verify: current feature maturity, platform constraints, supported process/filesystem behavior, isolation guarantees for the exact workload, outbound network defaults, plan costs, execution duration, and whether the container option fits arbitrary Python scripts.

### Judge0 CE

Official source: https://ce.judge0.com/docs

- API-oriented code execution service with support for many languages, multi-file submissions, time/memory limits, and detailed execution results.
- Documentation describes hosted API access and self-hosting options; the open-source edition is GPL-3.0 licensed.
- Potential fit: a fast way to prototype a narrow code-runner API without building a language-execution protocol from scratch.
- Must verify: hosted provider's current plans, queues/rate limits, file and output behavior, package installation limitations, retention, and the security model of the specific hosted/self-hosted deployment.
- Important caveat: self-hosting shifts patching, operations, isolation review, and abuse prevention to us.

### Piston

Official source: https://github.com/sanmayc1/Piston

- Open-source code execution engine with an HTTP API and language runtime support.
- Its README describes Linux isolation and resource controls such as execution-time and output limits, with network access disabled by default in the documented setup.
- Potential fit: evaluating an open-source engine for a controlled, self-hosted prototype.
- Must verify: maintenance status, supported language versions, deployment requirements, isolation review, API limits, and whether a managed production service is available on suitable terms.
- Important caveat: using an engine is not the same as having a secure, operated public service. Deployment and threat-model responsibilities remain.

## Comparison summary

| Candidate | Strongest apparent reason to investigate | Main unknown / cost risk | Current recommendation |
|---|---|---|---|
| E2B | Purpose-built hosted microVM sandbox workflow | Pricing tiers, API fit, data/region controls | Shortlist for API proof |
| Modal | Flexible disposable environments and output streams | Billing model and operations complexity | Shortlist for API proof |
| Daytona | Environment flexibility, including VM options | Isolation tier and resource lifecycle billing | Shortlist if persistent environments/Windows matter |
| Cloudflare | Tight fit with a web app architecture | Feature constraints and paid-plan/runtime fit | Shortlist if choosing Cloudflare for the app |
| Judge0 CE | Language-runner API and broad language catalog | Hosted service constraints or self-hosting burden | Prototype alternative for short, bounded submissions |
| Piston | Open-source engine and documented resource controls | Self-hosting and production hardening | Research only until operations/security are assessed |

## Proposed evaluation proof

Do not choose from marketing pages alone. For the top two candidates, run the same small test suite with no production user data:

1. Execute a successful Python program and capture stdout, stderr, exit status, and duration.
2. Execute a syntax error and a runtime exception.
3. Run a program that exceeds the configured timeout.
4. Test cancellation and worker termination.
5. Create and retrieve a small output file.
6. Test multi-file input.
7. Confirm output-size and memory limits.
8. Confirm the job cannot read application environment variables or other jobs' files.
9. Verify network restrictions and cleanup.
10. Measure cold-start and repeat-run latency.
11. Estimate cost for representative short jobs, including idle time and storage.
12. Review data processing terms, retention, regions, and account limits.

## Current conclusion

No provider has been selected. First narrow the product workflow and required execution contract, then run a controlled technical comparison. Do not enter API keys, upload private user projects, or incur paid usage during initial research without explicit owner approval.


## 2026-11-01 — resource containment and teardown documentation recheck

This section supplements, and does not silently replace, the 2026-10-20 desk-research snapshot above. It records official-documentation semantics relevant to PC-EXT-02 and PC-EXT-04. No provider was contacted and no workload/account was used.

### Provider-specific facts verified from current official documentation

| Candidate | Resource / isolation documentation | Teardown semantics | Current implication |
|---|---|---|---|
| E2B | E2B says each sandbox runs in its own Firecracker microVM and kernel. This is a vendor architecture statement, not independent proof. | Security page says destroyed on timeout or shutdown; it does not by itself specify the exact wait/lookup semantics PocketCode needs for orphan reconciliation. | Keep as an investigation candidate only. Obtain exact API lifecycle, hard resource ceilings, storage and terminal-state evidence before any decision. |
| Modal | CPU/memory request is not necessarily a hard cap; separate CPU/memory limits cap burst. Default outbound access to public IPs is allowed. gVisor and VM runtimes are documented. | JS SDK exposes `terminate()`; current docs describe runtime termination. A real adapter still needs exact wait/lookup behavior and stable resource identity. | Require explicit egress policy at create, explicit hard caps, and authoritative termination observation. Dynamic policy update is documented Alpha; domain allowlist Beta. |
| Daytona v2 | v2 Linux docs expose CPU/memory maxima and lifecycle/network policy controls. v2 documentation labels the API alpha. | Delete returns when teardown starts; state progresses through deleting/destroying to deleted/destroyed. Direct `get` reads the control plane. | Never map delete-call return to cleanup-confirmed. Poll/read terminal state. Verify v2 maturity and selected account capabilities. |
| Daytona stable v0 | Stable docs expose resource configuration and lifecycle features; exact resource proof still needs selected sandbox class and effective configuration. | Delete is fire-and-forget by default; explicit `wait`/DeleteAndWait can wait for destroyed state. | Adapter must request wait or independently reconcile the same ID. |
| Cloudflare Sandboxes | Current `@cloudflare/sandbox` 1.0 uses a Durable Object identity/storage layer plus a separately lived container instance; SDK 0.x is a legacy API with different documented destroy semantics. Workers Paid is required. | In 1.0, `destroy()` stops the container instance, but DO storage, snapshots and mounted buckets have independent lifetimes. Legacy 0.x `destroy()` documents deleting its sandbox files/processes/sessions. | Pin API generation; reconcile container stop, DO state, snapshots and buckets separately. Active container usage is billed on Workers Paid; no $0 assumption. |
| Firecracker self-hosted | Production host guidance requires defence in depth: KVM, patching, seccomp, Jailer or equivalent, cgroups/namespaces, privilege dropping and protected host paths. | Jailer documentation says operator owns cleanup; `notify_on_release` can race if setup/process crashes. | A low-level building block, not a managed service. It transfers host operations, isolation and cleanup obligations to us. |

### Important distinctions for the provider comparison

- A resource **request/reservation** is not a resource **hard limit**. Modal explicitly distinguishes them and bills by the higher of request or actual usage.
- A configured CPU bandwidth cap is not a wall-clock timeout. A CPU-bound infinite loop can remain alive while throttled.
- cgroup `io.max` is a bytes/operations-per-second control, not a total disk-capacity quota. `RLIMIT_FSIZE` is per-file, not total workspace capacity.
- For cgroup v2, `memory.events` is hierarchical by default unless `memory_localevents` is enabled; `memory.events.local` is local-only. Select counters according to the exact subtree and mount options. `cgroup.events: populated=0` confirms no live processes in that cgroup subtree at that time, not that a process was never migrated out, nor deletion of a remote sandbox or separately attached resources.
- An asynchronous delete accepted response must be followed by authoritative resource lookup until terminal destruction is confirmed. A local DB close or list/search miss is insufficient.
- Provider resource release and invoice/cost reconciliation are separate evidence axes. Billing delay cannot be interpreted as process liveness; a zero/pending invoice cannot prove cleanup.
- Modal's current Python SDK documents asynchronous container creation, `detach()` as disconnecting the client/connection resources, and `terminate(wait=True)` as waiting for sandbox execution termination and returning its exit code. `from_id`, `from_name(include_terminated=True)` and `list` provide identity-based lookup surfaces. Treat execution termination as a useful process-completion signal, not proof that independently attached storage has been released.
- Linux `RLIMIT_FSIZE` applies to an individual file and can generate SIGXFSZ; it is not a total workspace quota. See https://man7.org/linux/man-pages/man2/getrlimit.2.html.

### Official sources checked

- Linux cgroup v2: https://docs.kernel.org/admin-guide/cgroup-v2.html
- Firecracker production host setup: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md
- Firecracker Jailer: https://github.com/firecracker-microvm/firecracker/blob/main/docs/jailer.md
- Modal network security: https://modal.com/docs/guide/sandbox-networking
- Modal resource limits: https://modal.com/docs/guide/sandbox-resources
- Daytona v2 Linux sandbox and lifecycle: https://www.daytona.io/docs/en/v2/linux-sandboxes/
- Daytona stable Linux sandbox delete/wait: https://www.daytona.io/docs/en/linux-sandboxes/
- Cloudflare sandbox lifetime: https://developers.cloudflare.com/sandbox/concepts/lifetime/
- Cloudflare sandbox lifecycle API: https://developers.cloudflare.com/sandbox/sdk/api/lifecycle/
- E2B security architecture: https://e2b.dev/security

### Updated conclusion

No candidate is selected. The provider matrix is now sufficiently specific to design a controlled, provider-neutral comparison, but insufficient to claim that any candidate satisfies PocketCode's launch gates. Under the existing $0/no-account/no-workload constraints, the next permitted work is source-grounded review and design only.


## Cross-reference to detailed acceptance evidence

The current provider facts above are summarized in [AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md](../AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md). Use that review as the evidence-design companion when comparing candidates. It deliberately separates:
- requested resources from enforced hard ceilings;
- CPU throttling from wall-clock termination;
- I/O rate from disk capacity;
- child process-tree termination from provider resource deletion;
- sandbox deletion from attached volume/snapshot deletion;
- provider resource release from delayed billing reconciliation.

The provider shortlist remains unranked pending an actual first-workflow definition, owner decisions, and explicit account/budget approval. No vendor's public documentation is accepted as runtime proof.


### 2026-11-01 — additional lifecycle and host-output verification

A second official-docs pass found important API-generation distinctions and a host-side output attack surface:

- **Cloudflare 1.0 vs 0.x:** Current Sandboxes lifetime docs describe a Durable Object that keeps identity and its own storage while a container instance has a separate lifetime. Instance-local processes and disk end when it stops; snapshots and mounted R2 buckets outlive instances. The 0.x lifecycle API separately documents destruction of its sandbox files/processes/sessions and is explicitly for existing 0.x applications. Never use the 0.x `destroy()` statement as proof that 1.0 DO storage, snapshots or mounted buckets are gone. Current Sandboxes require Workers Paid; Containers pricing documents active memory/disk/CPU billing. Sources: https://developers.cloudflare.com/sandbox/concepts/lifetime/ ; https://developers.cloudflare.com/sandbox/sdk/api/lifecycle/ ; https://developers.cloudflare.com/containers/platform/pricing/ ; https://developers.cloudflare.com/sandbox/files/save-and-restore-a-workspace/.
- **Modal lifecycle:** Python SDK documentation says `Sandbox.create` provisions the corresponding container asynchronously; `detach()` disconnects the client and cleans connection resources; `terminate(wait=True)` waits for sandbox execution termination and returns an exit code. `from_id`, `from_name(include_terminated=True)` and `list` are available for identity-based reconciliation. These operations are distinct. Source: https://modal.com/docs/sdk/py/latest/Sandbox.
- **Firecracker host output:** Production guidance warns that guest-controlled serial output and guest-influenced logs can cause unbounded host memory/storage use unless bounded/rate-limited/discarded safely. This must be tested as a host resource boundary, not merely as a PocketCode report truncation case. Source: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md.
- **Cgroup process membership:** `cgroup.events: populated=0` is an observation of live processes in that cgroup and descendants. The host must prevent workload-controlled migration out of the observed subtree and preserve a supervisor-owned membership boundary. Source: https://www.kernel.org/doc/html/v6.14/admin-guide/cgroup-v2.html.

Provider selection remains NONE. All evidence remains desk research, not runtime verification.
