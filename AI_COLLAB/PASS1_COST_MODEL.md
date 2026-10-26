# Pass 1 — Illustrative execution cost model

**Research ID:** PC-PASS1-2026-10-26-COST-01  
**Checked:** 2026-10-26  
**Purpose:** Normalize a small-run cost example to expose pricing traps; this is not a quote, provider recommendation, or authorization to spend.  
**Budget:** $0. No accounts or workloads used.

## Scenario assumptions

- One Python script runs for 60 seconds.
- No network egress, persistent storage, logs beyond provider defaults, concurrency, package-build time, or retry is charged in the simplified variable-cost calculation.
- The model is a lower-bound illustration, not an all-in estimate. Real jobs include startup, queueing, idle tails, files, storage, request/API charges, logs, failed attempts, abuse, and platform/orchestration costs.
- CPU/memory settings differ by provider; numbers below are **not a fair performance comparison**.
- Rates are from official pages checked 2026-10-26 and may change.

## Per-run variable-cost illustration

| Provider / product | Assumed resource configuration | Rate basis | 60-second arithmetic | Important exclusions / catch |
|---|---|---|---|---|
| Modal Sandbox + Notebooks | 1 vCPU equivalent (= 0.5 physical core), 1 GiB memory, 60s active | $0.00003942 / physical core-second; $0.00000667 / GiB-second | CPU $0.0011826 + memory $0.0004002 = **$0.0015828** active | Modal pricing page says a default 60-second post-input idle tail is billable unless configured; if a full extra 60s tail applies at same resources, illustrative total is **$0.0031656**. Starter includes compute credit but usage is pay-as-you-go; this is not a hard $0 cap. |
| Daytona | 1 vCPU, 1 GiB memory, 60s active | $0.0504 / vCPU-hour; $0.0162 / GiB-hour | CPU $0.00084 + memory $0.00027 = **$0.00111** active | Excludes storage beyond allowance, startup/idle, network, and tier/account effects. Network policy depends on organization tier; some tiers require card/top-up. |
| E2B | 1 vCPU, 1 GiB memory, 60s active | $0.000014 / vCPU-second; $0.0000045 / GiB-second | CPU $0.00084 + memory $0.00027 = **$0.00111** active | Excludes storage, plan/concurrency/base costs and other charges. Exact Hobby/Pro eligibility needs confirmation. E2B requires prior written consent before testing. |
| Cloudflare Containers | `standard-2`: 1 vCPU, 6 GiB memory, 12 GB disk, 60s active at 100% CPU | $0.000020 / active vCPU-second; memory/disk usage billed against included quotas first | CPU usage would be $0.0012 before included allowance; this scenario uses 1 vCPU-minute, 0.1 GiB-hour memory and 0.2 GB-hour disk, within the published monthly included amounts | Requires Workers Paid at **$5/month**; Workers, Durable Objects, logs and egress can add charges. Marginal usage may be within quota, but this is not a $0 service. |

Sources: [Modal pricing](https://modal.com/pricing), [Daytona pricing](https://www.daytona.io/pricing), [E2B pricing](https://e2b.dev/pricing), [Cloudflare Containers pricing](https://developers.cloudflare.com/containers/platform/pricing/).

## Illustrative variable costs at 1,000 identical runs

| Provider | Variable compute/memory estimate | Caveat |
|---|---:|---|
| Modal | $1.5828 active-only; up to $3.1656 if each run also incurs a full 60-second billable idle tail at the same resources | Does not include other charges; free credit is not a hard spending limit |
| Daytona | $1.11 active-only | Excludes plan/tier effects, storage and other charges |
| E2B | $1.11 active-only | Excludes plan/concurrency/storage and other charges; testing consent required |
| Cloudflare | $0 marginal compute/memory/disk for this scenario only while included monthly quota remains, plus the $5/month Workers Paid base plan | Workers, Durable Objects, logs, egress and other use can add charges |

## Interpretation

1. Compute cost per short run can look tiny, but it is not the product's total cost. Orchestration, request handling, storage, logs, startup/idle time, abuse and support may dominate.
2. Free credits are not a guaranteed $0 ceiling. A strict $0 budget means no provider account/workload until the owner explicitly approves the provider and spend gate.
3. Cloudflare's included resource quotas do not remove its $5/month base plan. Daytona's free allowance does not by itself prove the intended egress policy is available on a zero-payment tier. Modal's Starter can bill beyond included compute. E2B testing requires prior written consent.
4. Do not choose a provider from these arithmetic examples. Normalize the same runtime/CPU/memory/storage/idle/egress/limits/plan assumptions and validate them with official current docs before making a decision.
5. The existing controlled proof runbook remains unexecuted and requires explicit owner approval.

## Required next cost-model iteration

- Fix a representative run mix (short success, exception, timeout, cancellation, output/file-heavy run, retries).
- Normalize the actual minimum resource configuration for each shortlisted product.
- Include cold-start and idle-tail distributions, free allowance exhaustion, storage/log retention, network egress, request/API charges, quotas, concurrency, provider base fees, and cost of abuse.
- Model best/expected/adverse monthly usage and show which settings enforce a true hard stop.
- Keep all live tests blocked until the owner approves a provider and exact billing controls.
