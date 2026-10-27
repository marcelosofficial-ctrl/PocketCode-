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
| SRC-02 | High | `PASS1_PROVIDER_RESEARCH.md`, Daytona source list and narrative | Main section links the v0 page and describes tier-based restrictions; later continuation correctly warns v2 differs. The two sections can be read as one unified contract. | Label the main network behavior explicitly **v0** and the later page **v2 alpha**. Keep the distinction next to each claim, not only in a later caveat. |
| SRC-03 | Medium | `PASS1_RUNTIME_PROVIDER_GATE.md`, E2B source list | Lists `https://e2b.dev/docs/security`, while the current reviewed page is `https://e2b.dev/security`; older URLs may redirect/change. | Prefer the current security URL; retain the written-consent prerequisite and check it again before any future approved test. |
| SRC-04 | Medium | `PASS1_RUNTIME_PROVIDER_GATE.md`, Modal source list | The listed URLs are current candidate docs, but the source-refresh note records an upstream 502 on a direct fetch of the networking page. | Keep network behavior labeled as a documentation claim; re-fetch current docs before any design/provider decision. No live proof at $0. |
| SRC-05 | Medium | `RESEARCH_CHECKPOINT.md` | Latest checkpoint text ends at offline test matrix and does not yet link the lifecycle-resolution note or the updated matrix. | Add the new artifact links and state that the two-axis outcome/disposition model is proposed, not adopted; LC-01–LC-12 are NOT RUN. |
| SRC-06 | Medium | `GEMINI_REVIEW_REQUEST.md` | Read-first list does not include the new lifecycle-resolution note or expanded test matrix, so Gemini could review a stale subset unless it reads the branch broadly. | Add both links and explicitly ask Gemini to reconcile them with the contract, decision register, and provider gate. |

## Primary sources rechecked

- Daytona v2 alpha Network Limits: https://www.daytona.io/docs/en/v2/network-limits/ — says egress is open by default, supports an explicit block-all policy, and exposes desired versus applied policy during updates. It also says policies apply to Linux/macOS, not Windows/GPU sandboxes. A successful request to set policy is not proof that the applied policy is active.
- Daytona v0 Network Limits: https://www.daytona.io/docs/en/network-limits/ — contains tier-based restrictions: Tier 1/2 organization restrictions cannot be overridden per sandbox; Tier 3/4 permit sandbox-level controls. Keep this attributed to v0.
- Daytona v2 Limits: https://www.daytona.io/docs/en/v2/limits/ — page is marked alpha and documents per-sandbox CPU/memory/disk limits separately from organization and API rate limits. These are not a global spend ceiling.
- E2B current security page: https://e2b.dev/security — says prior written consent is required before testing.
- Modal networking: https://modal.com/docs/guide/sandbox-networking — source refresh noted direct-fetch 502 in this review; current search result described public outbound IP access as allowed by default and a block option. Re-fetch before reliance.
- Cloudflare Containers pricing: https://developers.cloudflare.com/containers/platform/pricing/ — reviewed notes state no Free-plan allocation; Workers Paid base plan is $5/month plus possible metered usage/egress.

## Cross-document status truth

- No provider is selected or approved for a live test at strict $0.
- Free credits/trials are not a hard $0 cap.
- E2B testing remains blocked until written consent is obtained.
- Provider docs are vendor claims; configuration and observed behavior remain unverified.
- The lifecycle two-axis model is a proposal, not a frozen schema.
- Offline acceptance cases, including LC-01–LC-12, are proposed and NOT RUN.
- No market validation or hands-on competitor benchmark has occurred.
- Gemini review is pending; preparing a request is not delivery or completion evidence.

## Next safe action

Correct the source/version wording in the provider gate and main provider research; update the checkpoint and Gemini review request links. Then do a final pass for stale claims and internal-link integrity. Keep PR #3 draft/unmerged and PR #2 untouched.
