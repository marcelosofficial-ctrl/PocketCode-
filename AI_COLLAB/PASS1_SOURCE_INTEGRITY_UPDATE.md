# Provider source-integrity update — 2026-10-27

**Owner:** ChatGPT independent desk review  
**Status:** Current public documentation re-check only. No provider account, workload, benchmark, or runtime test. This is not provider approval.

## Findings that should inform the existing provider research

### Cloudflare Containers
- Current official pricing page states Containers have no Free-plan allocation and are included with the $5/month Workers Paid plan, with additional metered usage and egress charges possible.
- The existing conclusion “not eligible under strict $0” remains supported.
- Source: https://developers.cloudflare.com/containers/platform/pricing/
- Also surfaced in Workers pricing: https://developers.cloudflare.com/workers/platform/pricing/

### Daytona
- The current v2 Network Limits page explicitly labels v2 as alpha and says outbound egress is open by default. The policy must be explicitly applied to restrict egress.
- The same page says network policies apply to Linux and macOS sandboxes, but not Windows or GPU sandboxes. It documents separate desired and applied policies, which can differ while a policy update is applying; any future adapter must verify the applied policy before starting code.
- The current v2 Network Limits page does not contain the earlier “Tier 1/2 cannot be overridden” wording seen in prior review. Do not repeat that precise claim as a current v2-page fact without locating the exact source/version that supports it.
- The current general Limits page states Tier 1 requires email verification, while Tier 2 requires a linked credit card and a $25 top-up. This does not itself establish a hard $0 ceiling or prove network-policy availability for a specific account.
- Sources:
  - https://www.daytona.io/docs/en/v2/network-limits/
  - https://www.daytona.io/docs/en/v2/limits/
  - https://www.daytona.io/docs/en/limits/
- Existing conclusion remains: no live proof approved; exact current tier, API version, billing controls, and policy application must be confirmed before any future review.

### Modal
- Current public pricing page describes Starter as $0/month plus compute, with $30/month in compute credits; it also says overage can be billed and environment-level budgets are not included on Starter. Therefore, credits are not a hard $0 spending cap.
- Current networking documentation says outbound connections to public IPs are allowed by default, with explicit controls including a full block option. The first proof would need the exact blocking option applied and independently verified; documentation alone is not a test.
- Sources:
  - https://modal.com/pricing
  - https://modal.com/docs/guide/sandbox-networking
  - https://modal.com/docs/guide/sandboxes

### E2B
- The current official security page says each sandbox runs in its own Firecracker microVM and explicitly asks users to contact E2B before running any test because prior written consent is required by its terms.
- The existing no-testing-before-written-consent gate remains supported.
- Prefer the current security page URL below in new notes; older documentation URLs may redirect or change.
- Sources:
  - https://e2b.dev/security
  - https://e2b.dev/pricing

## Source review limits

- Public pages were searched/opened on 2026-10-27. This checks the wording visible in current pages, not an account-specific plan, configured policy, billing ceiling, or runtime behavior.
- No security controls were exercised. Provider documentation, configured state, and tested behavior remain separate evidence categories.
- Modal's documentation page returned an upstream 502 when opened directly, but the current search-indexed official guide was rechecked on 2026-10-27 and explicitly states DNS is unrestricted except when all outbound traffic is blocked. `block_network=True` drops all outbound traffic; domain allowlisting is Beta/TLS 443 and dynamic updates are Alpha. This closes the prior documentation ambiguity about DNS wording, not the runtime-verification gap. Recheck again before any approved provider-specific design decision.
- No provider selected. Strict $0 remains binding; no accounts, card entry, workloads, consent requests, or spend were made.

## Actionable correction

Update future summaries to say: Daytona v2 egress is open by default unless a policy is explicitly applied; the current v2 page does not substantiate the older precise tier restriction statement; verify the applied policy, not just the requested policy. For Modal, treat Starter credits and overage as incompatible with a guaranteed $0 ceiling unless an independently verified hard stop is available.