# Pass 1 — Execution-provider official-source refresh (subpass C)

**Research ID:** PC-PASS1-2026-10-26-PROVIDERS-01  
**Checked:** 2026-10-26  
**Branch:** `pocketcode-pass0-audit-2026-10-26`  
**Scope:** Current official docs/pricing/security pages for four shortlisted hosted execution providers. This is a bounded part of Gemini workstream C, not completion of Pass 1 across A–H and not a provider decision.  
**Budget:** $0. No accounts, credentials, trials, billing, workloads, or live security tests used.

## Executive finding

The shortlist remains viable for further comparison, but none can be called “safe and free” solely from marketing pages. The provider with the most attractive advertised control is not automatically the lowest-cost or lowest-risk option. Current official docs expose materially different default network policies, billing structures, account-plan requirements, and per-sandbox trust boundaries.

**No provider selected.** For the $0 constraint, continue documentation-only research. A live proof requires explicit owner approval, current plan/billing review, and the existing controlled proof runbook. Do not create an account or attach a payment method based on the presence of a free allowance.

## Current official-source snapshot

### Modal Sandboxes

**Sources checked:** [Sandbox networking/security](https://modal.com/docs/guide/sandbox-networking), [Python Sandbox reference](https://modal.com/docs/sdk/py/latest/Sandbox), [pricing](https://modal.com/pricing), [Sandbox product page](https://modal.com/products/sandboxes).

- **Network default:** outbound connections to public IPs are allowed by default. The current indexed guide explicitly says DNS traffic is unrestricted except when all outbound traffic is blocked. `block_network=True` drops all outbound traffic; it cannot be combined with allowlists. Domain allowlisting is Beta and applies to TLS traffic on port 443; runtime policy updates are Alpha and have limitations. Treat this as a current documentation claim, not proof of deployed configuration or provider-level behavior under our exact plan. Private/metadata access and all alternate paths still require adversarial validation.
- **Isolation/runtime:** Modal documents gVisor as the current default Sandbox runtime in the current SDK release notes, with a VM runtime option. This is a vendor description, not PocketCode's own proof of isolation.
- **Pricing:** the pricing page distinguishes standard compute from “Modal Sandbox + Notebooks” rates. Sandbox/Notebook CPU is listed at $0.00003942 per physical core-second and memory at $0.00000667 per GiB-second; minimum 0.125 CPU cores/container is stated. Starter is $0/month plus compute and advertises $30/month included compute, but usage is pay-as-you-go beyond applicable included amounts. The page also notes a default 60-second post-input idle period is billable unless configured otherwise.
- **Implication:** the documented static network-blocking option is promising for a minimal no-network proof, but free credits are not a $0 guarantee. Model the actual Sandbox rates, startup, idle tail, memory, and egress; verify account-level hard-spend controls before any approved test.
- **Source note (2026-10-27):** the current search-indexed networking guide was rechecked after direct retrieval returned 502. It states that DNS traffic is unrestricted except when all outbound traffic is blocked; `block_network=True` drops all outbound traffic, while CIDR/domain allowlists permit only matching destination traffic under their documented rules. Domain allowlisting is Beta (TLS/443), and dynamic policy updates are Alpha. Source: https://modal.com/docs/guide/sandbox-networking. This is documentation review, not runtime verification.
- **Unresolved:** exact runtime version/semantics for the chosen SDK, termination behavior under timeout/cancel, resource limits, account hard-cap availability on the intended plan, regional/data terms, and observed behavior all require further verification.

### Daytona Sandboxes

**Sources checked:** [pricing](https://www.daytona.io/pricing), [v0 network limits](https://www.daytona.io/docs/en/network-limits/), [v0 limits/tiers](https://www.daytona.io/docs/limits), [v2 alpha network limits](https://www.daytona.io/docs/en/v2/network-limits/), [v2 alpha limits](https://www.daytona.io/docs/en/v2/limits/), [v2 isolation documentation](https://www.daytona.io/docs/en/v2/isolation/).

**Version warning:** the tier-based organization restrictions below are from the v0 documentation and must not be represented as v2 alpha behavior. The v2 alpha docs are a separate product/version context.

- **Isolation:** v2 documentation describes Firecracker microVMs with separate kernel, filesystem, and network stack. Treat this as a vendor description, not PocketCode's own proof of isolation.
- **v0 network policy:** the v0 network-limits page describes tier-based organization restrictions. Tier 1 and Tier 2 policies cannot be overridden at sandbox level; Tier 3 and Tier 4 permit sandbox-level allowlists or `networkBlockAll`, with strict enforcement. These claims apply to the documented v0 context only; verify current plan/API semantics before use.
- **v2 alpha network policy:** the v2 alpha network-limits page says egress is open by default and describes explicit policy configuration. The requested/desired policy may differ from the applied policy, so a request parameter alone is not evidence that the intended policy is effective. The docs describe this feature as alpha and list platform limitations. Do not merge these statements with the v0 tier model.
- **Pricing:** the pricing page lists $0.0504/vCPU-hour, $0.0162/GiB-hour memory, and $0.000108/GiB-hour storage after the first 5 GiB; it advertises $200 in free compute and a free trial without a credit card. The limits page says Tier 2 requires a linked credit card plus a $25 top-up, Tier 3 a $500 top-up, and Tier 4 a $2,000 top-up every 30 days. Reconfirm current plan terms before relying on them.
- **Implication:** a free allowance does not prove the intended plan exposes network controls that satisfy the threat model. Under the current strict $0 rule, do not create an account, link a card, top up, or launch a workload.
- **Unresolved:** intended API/version/tier, default organization policy, whether essential services remain reachable, exact lifecycle/cancellation/cleanup behavior, region/retention, and real cold-start/cost behavior.

### Cloudflare Containers / Sandboxes

**Sources checked:** [Sandbox security](https://developers.cloudflare.com/sandbox/concepts/security/), [choose a sandbox environment](https://developers.cloudflare.com/sandbox/concepts/), [Containers pricing](https://developers.cloudflare.com/containers/platform/pricing/), [Containers FAQ](https://developers.cloudflare.com/containers/faq/), [Sandbox SDK 1.0 changelog](https://developers.cloudflare.com/changelog/post/2026-09-30-sandbox-sdk-1-0/).

- **Version caution:** current docs distinguish Sandbox SDK 1.0 from the older 0.x SDK. Do not reuse 0.x pricing/security assumptions or code examples for a new implementation without checking the 1.0 migration/current docs.
- **Network policy:** a Container starts with `enableInternet: false` by default; an outbound handler can selectively mediate allowed requests. Dynamic Workers have the Worker's network access unless `globalOutbound: null` is set. These are distinct execution modes with different trust implications.
- **Isolation boundary:** Cloudflare says a sandbox is isolated from its Worker and other sandboxes, but processes inside a single Container share files, process visibility, localhost, and root-equivalent Linux capabilities. The sandbox is the trust boundary; do not share one sandbox across users/jobs. A separate user or process alone is not isolation.
- **Pricing:** Containers are available on the Workers Paid plan, listed at $5/month. The current pricing page includes 375 vCPU-minutes, 25 GiB-hours memory, and 200 GB-hours disk per month, with additional CPU/memory/disk and regional egress charges; Workers, Durable Objects, and logs add separate usage costs. Container instances can sleep, but the exact all-in per-run cost depends on the instance type, active CPU, memory/disk provisioned, duration, region, requests, and logs.
- **Implication:** default-disabled Container internet is a strong design property for a constrained proof, but the published base plan is not compatible with a strict $0 spend unless the owner explicitly changes that constraint. Dynamic Worker and Container modes must not be conflated.
- **Unresolved:** choose mode only after defining required language/process/filesystem behavior; verify lifecycle/termination and current 1.0 API; model full Workers + Durable Objects + Containers + logs + egress cost.

### E2B Sandboxes

**Sources checked:** [security and compliance](https://e2b.dev/security), [pricing](https://e2b.dev/pricing).

- **Isolation:** E2B states each sandbox runs in its own Firecracker microVM with a separate kernel/filesystem/memory boundary. Its page describes managed hosting on Google Cloud, encryption in transit/at rest, region options by plan, and separate BYOC availability. These are vendor claims; underlying reports/terms need review if shortlisted.
- **Pricing:** the current pricing page exposes per-second CPU/memory pricing and plan/concurrency differences. Examples listed include 2 vCPU at $0.000028/second and 4 GiB memory at $0.000018/second; the page also shows a $150 Pro base and $3,000/month Enterprise minimum in its estimator context. Do not extrapolate one sample configuration to total monthly cost without usage assumptions and exact plan.
- **Testing restriction:** E2B's security page explicitly asks users to contact E2B before running tests against the service because its terms require prior written consent. No testing should be attempted unless that consent is obtained.
- **Implication:** the documented per-sandbox microVM boundary is promising, but the plan economics and testing-consent requirement make E2B unsuitable for any unapproved live proof.
- **Unresolved:** exact plan eligibility, default egress policy, lifecycle/cancel/timeout behavior, current regions/retention, complete cost model, and written testing permission.

## Cross-provider comparison — not a ranking

| Gate | Modal | Daytona | Cloudflare Containers/Sandboxes | E2B |
|---|---|---|---|---|
| Network policy in official docs | Outbound open by default; `block_network=True` documented | Tier-based restrictions; sandbox-level block/allowlist depends on tier | Container internet disabled by default; Dynamic Worker mode differs | Egress policy needs further current-doc review |
| Isolation description | gVisor default; VM option in current docs | Firecracker microVM described | Separate sandbox VM boundary; all processes within one container share the same trust domain | Firecracker microVM per sandbox described |
| Zero-dollar risk | Free included compute, but pay-as-you-go/idle tail means no $0 guarantee | Free compute advertised; network-control tier and top-up rules need verification | Workers Paid base plan $5/month plus component usage | Plan/concurrency costs need full model; testing requires prior written consent |
| Main blocker | Prove spend control and exact network/termination semantics | Confirm zero-payment tier can meet egress gate | Base plan conflicts with $0 unless owner changes constraint | Written permission before any test; full plan/egress review |
| Status | Candidate only | Candidate only | Candidate only | Candidate only; no test without consent |

Prices and plan terms are snapshots checked 2026-10-26, not a quote or promise. Do not compare per-second figures until a normalized scenario defines runtime, CPU, memory, startup/idle duration, storage, egress, request/API, logs, concurrency, and free-credit assumptions.

## Required next checks

1. Read the exact current API/lifecycle docs for each shortlisted product and record success/error output, file transfer, cancellation, timeout, termination, and cleanup semantics.
2. Verify the network policy for the intended plan and execution mode, including whether internal/metadata destinations are blocked. A setting name is not proof; actual network tests belong in an approved controlled proof.
3. Build a normalized cost worksheet for one short run, a repeat-use user, and an adverse/abuse scenario. Keep unknowns explicit.
4. Review data processing, region, retention/deletion, logging, and terms for the chosen product.
5. Keep all live tests BLOCKED pending explicit owner approval; E2B additionally requires prior written consent before tests.

## 2026-10-27 runtime feasibility clarification

The provider-neutral decision matrix is in [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md). No candidate is approved for live testing under the current $0 constraint.

Important distinctions from the current official docs:
- Cloudflare Sandboxes documentation describes Containers running in separate Firecracker microVMs and Container internet access defaulting off, but Containers require the $5/month Workers Paid plan. This makes it a paper candidate for a later explicitly approved budget, not a current zero-cost option. Processes within a single sandbox still share files/processes/localhost and root-level capabilities.
- Daytona's v2 network page is explicitly alpha and says Tier 1/2 organization restrictions cannot be overridden at sandbox level. Its v0 page documents a different network-policy model; exact API/version/tier must be verified rather than combining claims.
- Modal credits are not a hard billing ceiling. Network blocking and lifecycle/resource settings require exact configuration and adversarial validation.
- E2B's reviewed security documentation requires prior written consent before testing. No test should be run before permission and a cost/security review.

No account, provider, workload, or spend occurred. Documentation statements are not runtime verification.
