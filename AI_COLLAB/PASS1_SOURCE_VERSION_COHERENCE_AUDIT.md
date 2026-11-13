# Cross-document source and version integrity audit

**Date:** 2026-10-27  
**Owner:** ChatGPT independent desk review  
**Status:** Documentation-only correction list; no provider tested and no product decision made.  
**Budget:** Strict $0. No accounts, workloads, billing changes, deployment, or merge.

## Executive result

The source-refresh note correctly narrows several provider claims, but the same version distinction is not yet consistent across all provider artifacts. The largest correction is Daytona: the older v0 network page contains tier-based network restrictions; the v2 page is alpha and documents a different network-policy API and lifecycle. Statements from those pages must not be blended into one supposedly current API/plan behavior.

This audit is an evidence-quality check, not a provider recommendation.

## Findings and required wording

| ID | Severity | Artifact / area | Finding | Required correction |
|---|---|---|---|---|
| SRC-01 | High | `PASS1_RUNTIME_PROVIDER_GATE.md`, Daytona section | Says current v2 docs describe Tier 1/2 organization restrictions that cannot be overridden per sandbox. The current v2 page reviewed here instead documents egress open by default, explicit policy application, desired/applied policy states, and Linux/macOS scope; the tier override wording appears on the v0 page. | Say v2 alpha has egress open by default and policy must be explicitly applied/verified; attribute tier override claims to v0 only. Do not infer plan behavior across versions. |
| SRC-02 | High | `PASS1_PROVIDER_RESEARCH.md`, Daytona source list and narrative | **Corrected 2026-10-27:** main Daytona section now explicitly labels the v0 tier model and separate v2 alpha network-policy behavior. | **Closed by documentation edit**; retain version labels and re-check current docs before provider decisions. |
| SRC-03 | Medium | `PASS1_RUNTIME_PROVIDER_GATE.md`, E2B source list | Lists `https://e2b.dev/docs/security`, while the current reviewed page is `https://e2b.dev/security`; older URLs may redirect/change. | Prefer the current security URL; retain the written-consent prerequisite and check it again before any future approved test. |
| SRC-04 | Medium | `PASS1_RUNTIME_PROVIDER_GATE.md`, Modal source list | Direct page retrieval returned 502, but the current official search-indexed networking guide explicitly states DNS is unrestricted except when all outbound traffic is blocked. | **Documentation wording corrected 2026-10-27:** record this DNS behavior as a vendor documentation claim; re-fetch the primary page before any provider decision. Runtime enforcement and metadata/private-path behavior remain unverified. |
| SRC-05 | Medium | `RESEARCH_CHECKPOINT.md` | Original checkpoint has not been rewritten in place; the linked [2026-10-27 checkpoint addendum](RESEARCH_CHECKPOINT_ADDENDUM_20261027.md) now records lifecycle proposal, expanded tests, provider/source caveats, and Gemini review status. | **Mitigated by addendum**; treat it as the current supplement and preserve NOT RUN / proposal-only status. |
| SRC-06 | Medium | `GEMINI_REVIEW_REQUEST.md` | **Corrected 2026-10-27:** read-first list includes lifecycle resolution, expanded test matrix, and source/version audit; the review request asks Gemini to reconcile them with the contract and provider gate. | **Closed by documentation edit**; verify links remain valid when handing off. |

## Primary sources rechecked

- Daytona v2 alpha Network Limits: https://www.daytona.io/docs/en/v2/network-limits/ — says egress is open by default, supports an explicit block-all policy, and exposes desired versus applied policy during updates. It also says policies apply to Linux/macOS, not Windows/GPU sandboxes. A successful request to set policy is not proof that the applied policy is active.
- Daytona v0 Network Limits: https://www.daytona.io/docs/en/network-limits/ — contains tier-based restrictions: Tier 1/2 organization restrictions cannot be overridden per sandbox; Tier 3/4 permit sandbox-level controls. Keep this attributed to v0.
- Daytona v2 Limits: https://www.daytona.io/docs/en/v2/limits/ — page is marked alpha and documents per-sandbox CPU/memory/disk limits separately from organization and API rate limits. These are not a global spend ceiling.
- E2B current security page: https://e2b.dev/security — says prior written consent is required before testing.
- Modal networking: https://modal.com/docs/guide/sandbox-networking — direct retrieval returned an upstream 502, but the current official search-indexed result was available on 2026-10-27. It says public outbound access is allowed by default and DNS is unrestricted except when all outbound traffic is blocked; `block_network=True` drops all outbound traffic. Domain allowlisting is Beta/TLS port 443; dynamic policy updates are Alpha. The wording gap is closed from the indexed source, but runtime behavior and exact configuration remain unverified. Re-open the primary page before a provider decision.
- Cloudflare Containers pricing: https://developers.cloudflare.com/containers/platform/pricing/ — reviewed notes state no Free-plan allocation; Workers Paid base plan is $5/month plus possible metered usage/egress.

## Cross-document status truth

- No provider is selected or approved for a live test at strict $0.
- Free credits/trials are not a hard $0 cap.
- E2B testing remains blocked until written consent is obtained.
- Provider docs are vendor claims; configuration and observed behavior remain unverified.
- The lifecycle two-axis model is a proposal, not a frozen schema.
- Offline acceptance cases, including LC-01–LC-12, are proposed and NOT RUN.
- No market validation or hands-on competitor benchmark has occurred.
- Gemini's independent Pass 1 review was received from the user on 2026-10-27 and triaged in `GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md`. This does not establish completion of Gemini's full Pass 0–7 protocol.

## Next safe action (status reconciled 2026-10-27)

The focused internal-link audit completed for 13 current documents with zero missing relative targets; the cross-document status pass also reconciled the current contract, matrix, lifecycle note, decision register, checkpoint, and master plan. This is not a full external-link availability audit. The Modal networking page still returned an upstream 502 on direct retrieval, so its indexed official text remains a source limitation to recheck before any provider decision. No provider decision is pending or authorized now: the current action is owner review of [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md). Keep PR #3 draft/unmerged and PR #2 untouched.
