# Pass 1 — Runtime/provider feasibility gate

**Status:** Desk comparison only; not a benchmark, security audit, or provider selection.  
**Prepared:** 2026-10-27  
**Owner:** ChatGPT independent contribution; not Gemini completion.  
**Budget:** $0. No account creation, live workload, paid plan, or test authorization.

## Decision summary

**No candidate is approved for a live proof under the current constraints.** The gate is not “which one is cheapest per minute?” but “can mandatory controls be enforced on a plan that costs nothing, and can they be verified before accepting hostile code?”

- **Cloudflare Containers/Sandboxes** has the clearest paper fit for per-job Linux execution: current docs say Containers run inside separate Firecracker microVMs and internet access defaults off. But Containers require Workers Paid at $5/month; this fails the strict $0 rule. Future candidate only if the owner explicitly changes the budget.
- **Daytona** documents per-sandbox network policy, but **v0 and v2 alpha are materially different documentation surfaces**. The v0 Network Limits page describes tier-based organization restrictions: Tier 1/2 restrictions cannot be overridden at sandbox level, while Tier 3/4 permit sandbox-level controls. The current v2 alpha page instead says egress is open by default, policy must be explicitly applied, and desired/applied policy may differ during updates; it also states network policies apply to Linux/macOS, not Windows/GPU sandboxes. Do not combine these as one API/plan behavior. Exact product version, plan, applied policy, and billing controls remain unverified.
- **Modal** documents sandbox creation and a network-blocking option, but the reviewed credit model is not a guaranteed spend ceiling. Exact current configuration and adversarial validation are required.
- **E2B** documents per-sandbox microVM isolation, but its current security page requires prior written consent before testing. Do not run tests without consent. Plan/concurrency/base terms and a hard spend cap remain unverified.

No provider has been tested. This is a documentation comparison, not a security certification or a claim that any provider is insecure.

## Gate matrix

| Candidate | Isolation documented | Network control documented | Cost constraint | Current decision |
|---|---|---|---|---|
| Cloudflare Containers / Sandboxes | Container sandbox in separate Firecracker microVM; own kernel/network per current docs | Container internet access defaults off; outbound handlers/allowed hosts can constrain traffic | Containers require Workers Paid $5/month; no free Container tier | **Not eligible at $0**; best paper candidate if budget is later approved |
| Daytona | Container and VM sandbox types; limits per sandbox | v0 tier-based restrictions; v2 alpha explicit network policy with open egress by default; version and OS scope matter | Free trial/credits are not a hard spend ceiling; tier upgrades require payment/top-ups | **Hold** pending exact version/tier, applied-policy evidence, billing guard, and isolation review |
| Modal | Disposable Sandbox API documented; exact isolation boundary/settings need current plan-specific verification | Network-blocking API documented; default network and exceptions need exact config review | Starter credits can offset compute but are not a hard $0 cap | **Hold** pending cost guard and adversarial egress/lifecycle proof |
| E2B | MicroVM per sandbox documented | Egress policy and metadata reachability need provider-specific proof | Pricing/concurrency terms and a hard cap not verified; prior written consent required before tests | **Do not test yet**; written consent and cost/security review first |

## Important qualifications

### Cloudflare
- Current Sandboxes documentation says a Container runs in a Firecracker microVM with its own kernel and network, not shared with another workload.
- Processes within one sandbox share files, processes, localhost, and root-level capabilities; a separate Linux user is not an adequate intra-sandbox boundary.
- Internet access starts disabled for Containers, but enabling it or using an outbound handler creates a potential data-exfiltration path. Keep credentials in the Worker/control plane, never in the sandbox.
- Container pricing states Workers Paid costs $5/month; included resource quotas do not remove the base fee. Incompatible with the current strict $0 budget.

### Daytona
- **v0 source:** https://www.daytona.io/docs/en/network-limits/ — tier-based network restrictions and the older network-settings parameter model.
- **v2 alpha source:** https://www.daytona.io/docs/en/v2/network-limits/ — egress open by default, explicit policy, desired versus applied state, and Linux/macOS scope (not Windows/GPU). The page is marked alpha.
- The v2 page does not substantiate the older precise Tier 1/2 override wording. Keep that claim attributed to v0, not v2.
- Per-sandbox resource caps and organization pool quotas are separate; a per-sandbox cap does not prove a global spend ceiling or prevent queue abuse.
- A zero-egress test must confirm DNS, IPv4/IPv6, loopback, private/link-local/metadata, and redirects behavior under the exact plan. Documentation alone is not proof.

### Modal
- Treat network blocking as a required configuration to verify, not a security guarantee by name. Confirm whether every process/protocol is covered and whether the chosen plan can enforce resource, lifecycle, and egress limits.
- Credits are a subsidy, not a billing kill switch. Without an owner-approved hard ceiling and automatic fail-closed billing guard, no workload should run.
- The current networking documentation fetch returned an upstream 502 during the latest desk review; re-fetch before any provider-specific design decision.

### E2B
- Current security page: https://e2b.dev/security. Prior written consent is a precondition for tests according to the reviewed page. Do not run even a small harmless proof before permission is obtained.
- Pricing arithmetic alone is insufficient to establish plan base fees, concurrency caps, overage behavior, cancellation charges, and a hard stop-spend control.

## Provider-neutral minimum contract

A provider adapter is not ready for implementation acceptance until it can return authoritative evidence for:

1. **Job identity and isolation:** unique job ID; fresh disposable boundary per job; no cross-job filesystem/process/credential access.
2. **Policy applied:** exact network mode and policy revision confirmed before execution; default deny including DNS and metadata paths.
3. **Hard limits:** configured and observed wall time, CPU, memory, process count, disk, input/output bytes, and process-tree termination.
4. **Lifecycle:** queued/start/end/timeout/cancel/failure states, cleanup acknowledgement, and safe handling of a lost client connection.
5. **Output integrity:** runner exit code and stdout/stderr, bounded artifact manifest, byte counts, and explicit truncation/error states.
6. **Tenant boundary:** authorization on every job/report/artifact read and delete; no user-controlled sandbox-name collision.
7. **Economics:** per-job cost estimate, usage ledger, provider account-level ceiling where available, concurrency/rate limits, and fail-closed global circuit breaker. If no true account billing ceiling exists, do not describe setup as guaranteed $0.
8. **Retention:** declared expiration, deletion confirmation, and minimal logs without code/data retention beyond need.

## Implementation implications

- Keep the provider interface small and provider-neutral. Do not spread SDK-specific sandbox assumptions into the mobile UI or report formatter.
- Model capability explicitly: supported, unsupported, not_verified, and blocked_by_plan are different states. Never silently degrade from blocked network to open network or from hard timeout to advisory timeout.
- A job must not start unless every mandatory capability is supported and verified for the exact plan/configuration.
- Separate requested policy, provider-confirmed policy, and observed test evidence in the report. A “secure” badge is not justified by configuration alone.
- For the current no-PC/no-spend phase, work only on schema, adapter contract, deterministic fake adapter, and static/unit tests. A fake adapter proves orchestration/report behavior only, not isolation.

## Acceptance criteria before any live proof

- [ ] Owner explicitly approves any budget above $0 and any account/provider creation.
- [ ] Official terms and acceptable-use policy permit the proposed arbitrary-code workload.
- [ ] Exact plan supports fresh job boundaries, enforceable default-deny network/metadata restrictions, resource limits, timeout, cancellation, cleanup, and bounded artifacts.
- [ ] Spend and concurrency fail-closed controls are configured and independently checked.
- [ ] Synthetic harmless test suite and adversarial test plan reviewed.
- [ ] Provider written consent obtained where required (E2B).
- [ ] Test record includes exact plan, config, inputs, results, logs, resource state, and cleanup evidence.
- [ ] No secrets, private source, or personal data are included.

## Official sources reviewed 2026-10-27

- Cloudflare Sandbox security: https://developers.cloudflare.com/sandbox/concepts/security/
- Cloudflare choosing a sandbox environment: https://developers.cloudflare.com/sandbox/concepts/
- Cloudflare outbound traffic: https://developers.cloudflare.com/containers/configuration/outbound-traffic/
- Cloudflare Containers pricing: https://developers.cloudflare.com/containers/platform/pricing/
- Daytona v2 Network Limits (explicitly alpha): https://www.daytona.io/docs/en/v2/network-limits/
- Daytona v0 Network Limits: https://www.daytona.io/docs/en/network-limits/
- Daytona v2 limits (explicitly alpha): https://www.daytona.io/docs/en/v2/limits/
- Daytona general limits: https://www.daytona.io/docs/en/limits/
- Modal Sandboxes guide: https://modal.com/docs/guide/sandboxes
- Modal Sandbox API: https://modal.com/docs/reference/modal.Sandbox
- E2B current security page: https://e2b.dev/security
- E2B pricing: https://e2b.dev/pricing

Source statements are documentation snapshots, not independently verified runtime behavior. Re-check plan details immediately before any approved proof.

## Decision

No provider selected. Under the strict $0 constraint, only offline design, static/unit testing, and simulated adapter work are eligible. Do not create accounts, run workloads, or claim production isolation.
