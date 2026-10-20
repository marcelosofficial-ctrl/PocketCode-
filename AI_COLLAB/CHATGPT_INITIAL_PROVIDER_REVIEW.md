# ChatGPT Initial Provider Review — Independent Evidence Pass

**Research snapshot:** 2026-10-20  
**Status:** Preliminary primary-source review, not a provider decision and not a live security test. Gemini must independently research and extend this analysis. No accounts, credentials, paid workloads, or execution tests were used.

## Purpose

Start the technical comparison while Gemini works on broader research. The next technical gate is not “which API is easiest”; it is whether a provider can safely and affordably support short, disposable Python runs with file input/output, explicit terminal states, timeouts, cancellation, bounded output, and default-deny networking.

## Preliminary evidence table

### Modal Sandboxes

Sources:
- Product/pricing: https://modal.com/products/sandboxes
- JS Sandbox API: https://modal.com/docs/sdk/js/latest/Sandbox
- Networking/security: https://frontend-deadbeef.modal.com/docs/guide/sandbox-networking

What current official documentation says:
- Sandboxes expose process execution, filesystem access, stdout/stderr streams and configurable CPU/memory.
- API supports a blockNetwork option and outbound CIDR/domain allowlists.
- The networking/security page says the default sandbox has no inbound connections or access to Modal resources, but outbound connections to public IPs are allowed by default.
- The security page describes gVisor-based isolation.
- The product pricing page currently lists CPU and memory usage rates and a minimum CPU allocation. Rates are time-sensitive and must be recalculated for representative runs.

Potential fit:
- A reasonably direct API shape for a provider adapter, explicit network control, streams, and configurable resources.

Important unknowns:
- Actual measured startup/latency for our workload; job cancellation guarantees; lifecycle billing; output/file edge cases; account limits; contract/data handling; incident response; exact isolation details for chosen deployment mode; whether configuration can guarantee no network egress on every run.

Assessment:
- Strong candidate for a controlled proof, but do not treat vendor docs as proof of security. Verify network-block behavior and cleanup in live tests before exposing user workloads.

### Daytona Sandboxes

Sources:
- Sandbox overview: https://www.daytona.io/docs/en/sandboxes/
- Isolation: https://www.daytona.io/docs/en/isolation
- Pricing: https://www.daytona.io/
- Volumes and tenant scoping: https://www.daytona.io/docs/volumes/

What current official documentation says:
- Sandbox docs describe Linux containers by default and VM-based options, including Firecracker microVMs, plus Windows/macOS/GPU environments for specific workloads.
- The isolation page describes microVM isolation with separate kernel, filesystem, memory and network stack, with network egress open by default and configurable egress policy.
- Documentation describes scoped API keys, project boundaries and network policies.
- The homepage currently publishes resource rates for vCPU, memory, and storage; pricing, minimum billing units and free allowances need a careful current check.
- Volumes can persist across sandbox lifecycle and offer tenant subpaths; persistent storage introduces separate retention and isolation questions.

Potential fit:
- Rich environment lifecycle and multiple isolation modes; good candidate if a microVM boundary is available to the actual account and chosen API.

Important unknowns:
- Exact isolation tier and contractual guarantees for the plan we would use; cost for brief ephemeral runs including startup/idle/storage; network policy behavior and defaults; deletion and retention semantics; quota and concurrency limits; whether the richer platform is unnecessary operational complexity for a narrow MVP.

Assessment:
- Strong candidate for the second deep comparison. The distinction between default Linux container and microVM option must be explicit; do not describe every Daytona sandbox as hardware-isolated without verifying the exact mode selected.

### Cloudflare Sandbox SDK

Sources:
- Security: https://developers.cloudflare.com/sandbox/concepts/security/
- Pricing: https://developers.cloudflare.com/sandbox/platform/pricing/
- Current SDK docs: https://developers.cloudflare.com/sandbox/

What current official documentation says:
- The current security documentation states that the sandbox is isolated from the Worker and other sandboxes, but processes inside a single Container share one Linux system and can see each other's files/processes and localhost ports.
- It warns that deployed sandbox processes have root-equivalent Linux capabilities, so ordinary file permissions are not a boundary against code running inside that same sandbox.
- Pricing depends on underlying Containers resources and also related Workers, Durable Objects, and optional logs.
- Documentation includes multiple SDK versions; the current non-0.x docs should be used for new work, and older 0.x pages should not be mixed into a design without version clarity.

Potential fit:
- Attractive integration with a Workers application and a documented security model.

Important unknowns:
- Exact suitability of current Sandbox/Containers for arbitrary hostile Python scripts; whether each run can be provisioned and destroyed with strict per-job boundaries; runtime/package constraints; cancellation/output/files; actual all-in price; egress policy; plan constraints; lifecycle behavior.

Assessment:
- Worth screening, but the security boundary is especially important: processes in a single container are mutually visible and root-equivalent inside that container. A job-per-sandbox design and documented isolation of separate sandboxes must be confirmed before considering it for untrusted public execution.

### E2B

Sources:
- Product/pricing: https://e2b.dev/
- Open-source SDK/runtime and detailed implementation docs must be checked during the next pass.

What current official product page says:
- E2B markets hosted sandboxes for AI agents and describes an open-source microVM-oriented runtime.
- The current pricing page advertises a free Hobby plan with one-time usage credit, session duration limits and concurrency limits; Pro has a monthly base fee plus usage costs.

Potential fit:
- Purpose-built sandbox API and an open-source runtime may support a good balance of quick proof and portability.

Important unknowns:
- Current exact API support for bounded process execution, files, streaming and cancellation; networking default and allowlist/block behavior; underlying isolation evidence; retention, region and data terms; account quotas; cold starts and current all-in cost; license and self-hosting effort.

Assessment:
- Keep in the shortlist. The pricing tier and isolation claims require exact current docs and test evidence before recommendation.

## Preliminary comparison (not a final ranking)

| Criterion | Modal | Daytona | Cloudflare Sandbox | E2B |
|---|---|---|---|---|
| Execution/file API evidence | Official SDK documents process and filesystem interfaces | Official docs describe process and file operations | Must inspect current SDK details further | Must inspect current API docs further |
| Isolation evidence found | gVisor; sandbox lacks access to Modal resources by default | Explicit container and Firecracker microVM options; exact mode matters | Sandboxes isolated from Worker/other sandboxes; processes inside one sandbox share system and root-equivalent capability | Product page claims microVM-oriented runtime; deeper docs needed |
| Network default in docs reviewed | Outbound public IP allowed unless blocked/restricted | Egress open by default, configurable policy | Need verify exact current SDK default and control | Needs verification |
| Price evidence | CPU/memory rates on product page | vCPU/memory/storage rates on homepage | Resource + Workers/DO/logs costs | Tier limits + usage costs |
| Main uncertainty | Exact isolation, lifecycle/cancel, all-in cost | Mode-specific isolation and short-job economics | Per-job boundary, sandbox-internal privilege, all-in cost | Detailed network, lifecycle, and cost behavior |
| Status | Candidate | Candidate | Screen further | Candidate |

## Required next tests before selection

For each finalist, use the same controlled test suite, if and only if the owner authorizes account/credential use:
1. Valid Python script returns exact output and successful terminal status.
2. Syntax error and runtime exception return truthful failure states and stderr.
3. Infinite loop is terminated by a server-side deadline.
4. Cancellation stops execution or has a documented bounded termination delay.
5. Output limit is enforced, with explicit truncation/rejection.
6. A generated file is retrievable with exact verified bytes.
7. Input files are scoped to the job and not available to another job.
8. No-network policy blocks outbound connections and attempts to reach internal/metadata addresses.
9. Cleanup is verified after success, failure, timeout and cancellation.
10. Client disconnect/retry does not invent success or duplicate a billable run without idempotency.
11. Record cold/warm latency, usage metrics, provider errors and cost.
12. Verify data retention/deletion and logs handling against current terms.

Do not test against production secrets or real user files. Do not expose a public endpoint. Do not start paid workloads without explicit owner approval.

## Current recommendation

Do not choose a provider yet. Maintain Modal, Daytona and E2B as the leading research candidates and keep Cloudflare in the screen. Gemini should independently verify these notes and may replace this shortlist with evidence. The decision gate is documented isolation + controllable no-network mode + reliable lifecycle/files + acceptable measured latency and cost, not brand familiarity.

## Open questions

- Can all runs use an isolated disposable worker without any persistent shared workspace?
- Can network egress be blocked at the provider boundary rather than only inside userland?
- What is the exact billed lifetime for a short run, including startup, idle time, storage and coordinator resources?
- Can cancellation and cleanup be observed and tested deterministically?
- What data is logged or retained by provider and for how long?
- Which options support reliable file I/O and output streaming with low integration burden?
- Which provider allows future self-hosting or migration without rewriting product logic?
