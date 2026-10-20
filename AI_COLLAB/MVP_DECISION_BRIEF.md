# PocketCode — MVP Decision Brief

**Updated:** 2026-10-20  
**Status:** Independent desk-research recommendation; not an approved provider or stack decision.  
**Scope:** Decide what to prove next, not design the entire future platform.

## Executive recommendation

Keep the first product proof narrow: a phone-browser workflow that runs a small Python script with optional input files, shows genuine execution evidence, allows output download, and creates a useful report that can be pasted into any AI assistant.

Do not implement autonomous agent loops, native mobile apps, SSH/Tailscale, multiple language runtimes, WASM AST parsing, floating overlays, or background clipboard monitoring as part of the first proof.

**Provider shortlist for a controlled proof (not a selection):**
1. **Cloudflare Sandbox Containers** — investigate first if a browser-facing application and its deployment are likely to use Cloudflare. Its current official security documentation describes a Container as running in a Firecracker microVM with its own kernel/network and says Containers start with internet disabled by default. Each sandbox is a trust boundary; code and processes within the same sandbox share access to that sandbox's files/processes. Sources: https://developers.cloudflare.com/sandbox/concepts/ and https://developers.cloudflare.com/sandbox/concepts/security/
2. **Modal Sandboxes** — compare as a provider-focused programmable sandbox API with process execution, streams, filesystem access, CPU/memory settings, timeout/idle timeout, and documented sandbox lifecycle. Exact product/rate card and network policy must be confirmed for the intended configuration. Sources: https://modal.com/docs/sdk/py/latest/Sandbox and https://modal.com/pricing
3. **Daytona Sandboxes** — retain as a comparison candidate, especially if persistent environments later become important. Its network policy documentation says custom sandbox-level policies depend on organization tier; Tier 1/2 policies cannot be overridden at sandbox level, while Tier 3/4 support per-sandbox allowlists or block-all. This tier dependency must be resolved before it can pass a default-deny requirement. Sources: https://www.daytona.io/docs/en/network-limits/ and https://www.daytona.io/docs/en/sandboxes/

This is a research shortlist, not a claim that any provider has passed live tests. Do not create an account, enter credentials, incur charges, or deploy a public endpoint without owner approval.

## Product proof: minimum vertical slice

### User journey

1. Open a responsive web page on a phone.
2. Paste a small Python program and optionally add a small input text/CSV file.
3. Press Run and see an explicit queued/running state.
4. See real stdout, stderr, exit status, duration where available, and a clear terminal status.
5. Download a generated output file.
6. Copy a bounded, redacted execution report to the AI assistant of the user's choice.
7. Paste a corrected version and run again.

### Not included in this proof

- AI model API integration or agentic loops;
- repository-wide autonomous editing;
- arbitrary package installation or unrestricted outbound network access;
- SSH/Tailscale or user-managed remote hosts;
- persistent workspaces or multi-user collaboration;
- native iOS/Android applications;
- Rust/TypeScript execution or local WASM parser engine;
- system-wide overlays or clipboard monitoring.

## Provider gate: documentation before live proof

A candidate may proceed to controlled live testing only after the following are answered for the exact product, plan, and configuration:

| Gate | Required evidence |
|---|---|
| Isolation | Provider documents the isolation boundary; clarify whether jobs share a kernel, filesystem, processes, or persistent volume |
| Egress | Can all outbound access be disabled or strictly allowlisted outside untrusted code? Can metadata/private/internal targets be blocked? |
| Limits | Trusted server-side controls for wall time, CPU, memory, process count, disk, files, input/output size and concurrency |
| Lifecycle | Documented create, run, timeout, cancellation, termination and cleanup semantics |
| Files | Safe file upload/download behavior and limits; no path traversal across the job boundary |
| Result contract | Real stdout/stderr, truthful exit status, clear infrastructure failures, bounded output |
| Data handling | Region, retention, provider logs, deletion, subprocessors and terms understood |
| Cost | Exact product rate card and billing boundaries identified; expected and adverse usage formulas reproducible |
| Operations | Quotas, account requirements, regional availability, rate limits, cold-start measurement method and failure behavior known |
| Policy | Intended use fits the provider's acceptable-use terms |

A documentation pass does not substitute for a live test. If a provider cannot demonstrate the necessary isolation or network controls, it is not suitable for arbitrary untrusted code under this design.

## Initial scorecard (qualitative, confidence limited)

Scores are deliberately not numeric: evidence is incomplete and the candidates are not yet tested in the same environment.

| Criterion | Cloudflare Sandbox Containers | Modal Sandboxes | Daytona Sandboxes |
|---|---|---|---|
| Fit for web-app integration | Promising if app uses Cloudflare | Promising; separate service integration | Promising; separate service integration |
| Documented isolation shape | Firecracker microVM per Container according to current docs | Sandbox API documents managed isolated environments; exact guarantees/config must be reviewed | Container default; VM options available; exact mode must be selected |
| Default network posture | Containers start with enableInternet false; verify exact deployed configuration | Verify exact Sandbox API configuration and egress behavior before selection | Depends on tier and configured network rules; tier is a decision-critical unknown |
| Files/processes | Full Linux container tools; same sandbox is shared trust boundary | Process/filesystem API; test exact limits and file semantics | Full development sandbox; likely broader than MVP needs |
| Short script execution | Plausible; test cold start and request/runtime fit | Plausible; test cold start and billing boundaries | Plausible; test lifecycle billing and network tier |
| Operational burden | Potentially lower if already using Cloudflare; platform coupling | Separate provider SDK/service and account setup | Separate provider SDK/service and tier-specific policy decisions |
| Cost certainty | Exact Workers/Sandbox plan and resource charges still need calculation | Exact Sandbox product rate card must be reconciled | Exact billed states, CPU/RAM/storage and plan rules need calculation |
| Current status | Documentation candidate only | Documentation candidate only | Documentation candidate only |

### Important Cloudflare security caveat

Cloudflare's security documentation explicitly says that processes within one Container share the same Linux system, files, process visibility, and localhost; a separate Linux user does not create a meaningful boundary inside that sandbox. The same documentation warns that credentials placed in the sandbox can be read by code running there. The app must authenticate the caller, derive sandbox identity from that authenticated identity, and never place application/provider secrets in an untrusted sandbox. Source: https://developers.cloudflare.com/sandbox/concepts/security/

### Important Daytona network caveat

Daytona documents network policy differences by organization tier. Tier 1/2 cannot override network policy at the sandbox level; Tier 3/4 can configure networkAllowList, domainAllowList, or networkBlockAll. This is a concrete selection gate, not a minor footnote. Source: https://www.daytona.io/docs/en/network-limits/

## Required controlled proof

After provider choice and owner approval, run a small test suite with non-sensitive sample code only:

- PC-RUN-001 success and exact output;
- PC-RUN-002 syntax error;
- PC-RUN-003 runtime exception;
- PC-RUN-004 server-enforced timeout;
- PC-RUN-005 cancellation;
- PC-RUN-006 bounded output;
- PC-RUN-007 output file bytes match expected bytes;
- PC-RUN-008 input file is available in the intended job;
- PC-RUN-009 one job cannot read another job's files or secrets;
- PC-RUN-010 disallowed egress and internal/metadata targets are blocked;
- PC-RUN-011 retry/disconnect behavior does not duplicate jobs unexpectedly;
- PC-RUN-012 cleanup matches the documented retention policy;
- PC-RUN-013 provider failure is distinguished from user-program failure;
- PC-RUN-014 copied report is useful and contains no secrets or unbounded output.

Record exact provider product/plan, configuration, test date, observed outputs, failure behavior, cold-start and repeat-run timing, and actual billed usage if any. Never label a test passed unless it was executed and its evidence recorded.

## Current cost and network facts to carry into the decision

Checked against current official provider pages on 2026-10-20. These are desk-research facts, not an account-specific quote or a live security test.

| Question | Cloudflare Containers / Sandbox | Modal Sandboxes | Product implication |
|---|---|---|---|
| Fixed/entry cost | Containers pricing currently lists usage as part of the **$5/month Workers Paid plan**; the Containers table lists no Free-tier allocation. CPU, memory and disk allowances/overages are metered. See [Containers pricing](https://developers.cloudflare.com/containers/platform/pricing/). | The current [Sandbox product page](https://modal.com/products/sandboxes) advertises **$30/month free compute**. Treat this as included credit, not proof that all production use is free or that it will remain available; confirm account eligibility, expiration, and billing terms before any test. | Neither option should be described as unconditionally free. Do not create an account or enable paid usage without owner approval. |
| Outbound network default | Current [sandbox security guidance](https://developers.cloudflare.com/sandbox/concepts/security/) says the Container's internet access is disabled by default; verify the exact current API/configuration and any proxy/intercepted egress paths. | Current [networking guidance](https://modal.com/docs/guide/sandbox-networking) says public outbound access is allowed by default; explicitly set `block_network=True` or a carefully reviewed allowlist for untrusted code. | Modal needs explicit egress configuration from the start. Cloudflare's default is promising but is not itself proof of a complete SSRF/metadata/private-network defense. |
| Isolation caveat | The [security model](https://developers.cloudflare.com/sandbox/concepts/security/) says processes inside a single sandbox share its Linux system, files, processes and localhost; do not put unrelated users' code in the same sandbox trust boundary. | Modal documents Sandboxes built on gVisor and isolated per-sandbox environments; verify account/workspace access, resource cleanup and the exact workload behavior in a controlled test. | Use a fresh disposable sandbox per run/user boundary for the first proof; never inject provider credentials or unrelated secrets into untrusted code. |

**Interim recommendation:** keep Cloudflare and Modal as candidates, not a winner. Cloudflare's documented no-internet default may reduce configuration mistakes; Modal exposes explicit network-blocking controls and has a clear sandbox execution API. Compare the exact configuration, fixed costs, lifecycle, file transfer, and ability to enforce limits before choosing. No provider has been exercised by PocketCode.

## Practical first-proof candidate (not a vendor decision)

For the first controlled proof, **Modal Sandboxes are the current leading candidate for evaluation**, not an approved selection. Reasons: the product has a documented Python SDK/process API, explicit server-configurable `block_network=True`, and the Starter plan currently advertises $30/month in compute credit that applies to Sandboxes. That makes it easier to evaluate without committing to a monthly platform subscription than Cloudflare Containers, which currently requires the $5/month Workers Paid plan. This comparison is about proof friction, not a conclusion that Modal is more secure or better for production.

Sources checked 2026-10-20:
- [Modal Sandbox SDK reference](https://modal.com/docs/sdk/py/latest/Sandbox): exposes `block_network`, whose default is `False`; the proof must set it to `True` explicitly and verify the resulting behavior.
- [Modal pricing](https://modal.com/pricing): Starter is $0/month plus compute and advertises $30/month compute credit; the page separately lists Sandbox CPU and memory rates. Credit eligibility and current billing settings must be confirmed before running anything.
- [Cloudflare Containers pricing](https://developers.cloudflare.com/containers/platform/pricing/): Containers are included in the $5/month Workers Paid plan with resource allowances and overage rates; the Free column lists no Containers usage.
- [Cloudflare sandbox security](https://developers.cloudflare.com/sandbox/concepts/security/): a Container is a trust boundary and code in it can access the sandbox's files/processes; credentials must not be injected into untrusted code.

### Illustrative compute arithmetic (not a cost estimate)

At Modal's currently listed Sandbox rates, a hypothetical run billed for 10 seconds at the minimum 0.125 physical cores and 0.25 GiB memory computes to:

`CPU: 10 × 0.125 × $0.00003942 = $0.000049275`  
`Memory: 10 × 0.25 × $0.00000667 = $0.000016675`  
`Subtotal: $0.00006595 per 10 billed seconds`

This excludes startup/idle time if billed, storage, network egress, request/control-plane charges, retries, and any usage outside included credits. It is arithmetic from listed rates only, not a prediction of real run cost. Do not use it as a budget until billing semantics are verified against a real account.

### Recommendation for the first proof

If the owner later approves a controlled provider test, start with a single disposable Modal Sandbox, pinned minimal Python image, explicit network block, short server-side wall-time deadline, small CPU/memory limits, no credentials, no package installation, and a tiny fixed test suite. Before executing even sample code, verify account billing/budget controls and confirm the API can terminate a timed-out process. If any of these cannot be demonstrated, stop and return to provider comparison. Keep Cloudflare as the fallback if its exact Container controls better satisfy the gate. **No account creation, credentials, live workload, or charges are authorized by this recommendation.**

## Cost model template

Do not rely on manually typed per-user totals. Calculate the model from the actual selected product rate card:

execution_cost = billed_CPU_seconds × CPU_rate + billed_memory_GiB_seconds × memory_rate + storage + egress + other provider charges

The above is a template only; providers may use different billing units, minimums, included credits, idle charging, or product-specific rates. Confirm the exact pricing semantics before applying it.

For usage scenarios, explicitly set:
- runs per user per month;
- billed duration per run, including startup/idle time where billed;
- CPU and memory allocation;
- timeout and retry rate;
- input/output sizes, storage duration and egress;
- free-tier credits (reported separately, not treated as sustainable economics);
- monthly fixed costs and minimums;
- abuse cap and maximum cost per run/user.

LLM costs are excluded from the first proof because it does not call a model API. The user brings the report to their preferred assistant. This both limits risk and tests whether the core workflow has value before adding inference costs.

## Implementation sequence

| Task ID | Status | Goal | Completion evidence |
|---|---|---|---|
| PC-MVP-001 | READY | Freeze the first-run acceptance criteria | Product workflow and test IDs agree |
| PC-PROV-001 | READY for desk research; owner approval required before paid/live tests | Compare exact Cloudflare and Modal products; keep Daytona as alternate if its tier meets egress requirements | Source-linked provider gate table, pricing formulas, unresolved questions |
| PC-CONTRACT-001 | READY | Define provider-neutral run/result lifecycle and file constraints | Request/result schemas and state machine reviewed |
| PC-SEC-001 | READY | Turn security launch gates into testable requirements | Threats mapped to controls and PC-RUN tests |
| PC-PROOF-001 | BLOCKED pending provider/account/owner approval | Run controlled real Python execution proof | Actual evidence recorded for PC-RUN-001 to 008 |
| PC-SEC-TEST-001 | BLOCKED pending controlled test environment | Test isolation, egress, cleanup and abuse limits | Evidence recorded for PC-RUN-009 to 014 |
| PC-UX-001 | READY | Create phone-reviewable UI prototype with simulated states | No fake execution represented as real; mobile layout reviewed |
| PC-USER-001 | NEEDS OWNER ACTION | Validate the workflow with target users | Non-leading interviews/usability observations and explicit decision threshold |

## Owner approvals deliberately not requested yet

No paid usage, provider account, credential creation, execution backend, native release, repository visibility change, or irreversible infrastructure action is included in this recommendation. The static mobile prototype has been implemented and reviewed by the owner; the next safe work is to finish the exact provider comparison and define the smallest controlled test plan. Any paid/live execution test remains blocked pending explicit owner approval.

## Sources

- Cloudflare, Choose a sandbox environment: https://developers.cloudflare.com/sandbox/concepts/
- Cloudflare, Sandbox security: https://developers.cloudflare.com/sandbox/concepts/security/
- Cloudflare, Credentials and network access: https://developers.cloudflare.com/sandbox/network/
- Modal, Sandbox API: https://modal.com/docs/sdk/py/latest/Sandbox
- Modal, Pricing: https://modal.com/pricing
- Daytona, Network Limits (Firewall): https://www.daytona.io/docs/en/network-limits/
- Daytona, Sandboxes: https://www.daytona.io/docs/en/sandboxes/

**Review status:** desk research only. No provider selected, no code run, no customer validation, no benchmark, and no security test performed.
