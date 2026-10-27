# Gemini Pass 1 Review Integration — 2026-10-27

**Status:** Independent review received from Gemini and integrated as review evidence. Recommendations below are triaged; they are not all adopted decisions.  
**Owner:** ChatGPT independent synthesis  
**Scope:** PR #3 research branch only. PR #2 untouched.  
**Budget / safety:** strict $0. No provider account, workload, code execution, security test, billing change, merge, or deployment occurred during this integration.

## Executive disposition

**Verdict: not ready to freeze the contract.** Gemini's review confirms the highest-priority lifecycle ambiguity and identifies useful test gaps. The two-axis model remains the leading candidate, but canonical API enums and transition rules are not yet approved. Provider selection and implementation remain blocked.

## Adopt as high-priority findings

1. **Separate process outcome from final job disposition.** A process exit code is an observation; cleanup and evidence gates determine whether the job can be reported as PASS. Do not rewrite the draft state machine as a frozen API without owner review.
2. **Require a network-policy pre-execution barrier when policy application is asynchronous.** For Daytona v2, official docs explicitly expose desired/applied policy, status (pending/applied/failed), revisions, and ETag; policy changes are applied in the background. Execution must not start until the expected policy is confirmed applied. On timeout, mismatch, missing status, or failed policy, fail closed. ETag is a concurrency/revision token, not itself proof of enforcement.
3. **Test timeout/cancel races, process-tree cleanup, output limits, artifact integrity, and request idempotency** in deterministic orchestration tests.
4. **Keep secret handling and report output bounded.** Redaction should be defense-in-depth and streaming/bounded; it cannot guarantee detection of every secret. Never place provider credentials in the untrusted task environment. Do not silently modify arbitrary user output; report that redaction occurred and preserve controlled raw evidence only where the approved data policy allows.
5. **Keep product and naming risks explicit.** The existing Pocket Code/Catrobat collision is a distribution/brand risk to investigate, not a legal conclusion. A 10-user behavior-based test is a proposal, not evidence already collected.

## Important corrections and non-adoptions

### Provider claims

- **Daytona v2:** verified against current official documentation on 2026-10-27. The v2 page is marked alpha; egress is open by default; policy changes are applied in the background; API returns desired and applied policies, status and revision information; ETag is used for revision-aware updates. Do not start user code until applied policy matches the exact required policy and its revision. Source: https://www.daytona.io/docs/en/v2/network-limits/
- **E2B pricing:** official pricing currently lists a free Hobby tier with a one-time $100 usage credit, sessions up to one hour, and 20 concurrent sandboxes; Pro is $150/month plus usage and supports sessions up to 24 hours. Thus “E2B has a $150 mandatory floor for all usage” is false. However, the one-time credit is not a permanent hard $0 cap, and E2B's security page says prior written consent is required before testing. No E2B test is authorized. Sources: https://e2b.dev/pricing and https://e2b.dev/security
- **E2B idle billing:** the review's claim that idle sandboxes continuously accrue charges until destroyed is plausible but must be pinned to current official lifecycle/billing documentation before it is encoded as a verified rule. The cost model should conservatively include the full sandbox lifetime until confirmed termination and label the exact billing boundary unknown if not sourced.
- **Modal:** official pricing currently shows Starter at $0/month plus compute, with $30/month compute credits; environment-level budgets are listed for Team/Enterprise, not Starter. Credits are not a hard $0 cap. The official networking guide says outbound public-IP access is allowed by default; block_network=True blocks outbound traffic; domain allowlisting is Beta and TLS/443-only; dynamic policy updates are Alpha. This does not make Modal the default provider. No provider is selected. Sources: https://modal.com/pricing and https://modal.com/docs/guide/sandbox-networking
- **Cloudflare Containers:** official pricing confirms Workers Paid starts at $5/month and Container resources have no Free-plan allocation. Not eligible under the current strict $0 rule. Source: https://developers.cloudflare.com/containers/platform/pricing/
- **Third-party sources:** do not use a third-party blog as the sole evidence for vendor pricing, lifecycle billing, or security semantics when an official source is available.

### Architectural recommendations not adopted as decisions

- Do **not** adopt Modal as default (Gemini DEC-03) based only on free Starter credits. It does not establish a hard $0 cap or verified security.
- Do **not** reject all local Android execution on the basis of broad W^X / Phantom Process Killer claims without precise current primary sources and a specific design comparison. This project can defer local execution, but the rejection rationale needs evidence.
- Do **not** make a legal/trademark determination or rename the project without owner approval.
- Do **not** implement a 24-hour idempotency TTL as a universal rule without defining authenticated tenant scope, payload hash conflict behavior, retention, retries after expiration, and whether a prior terminal job is returned or a new one is permitted.
- Do **not** make CSV encoding/schema validation a universal contract requirement unless CSV is confirmed as the initial supported workflow. A bounded media-type/size and parser policy is appropriate; semantic schema checks should be workflow-specific.
- Do **not** treat fake-adapter tests as proof of real network enforcement, process-tree termination in provider infrastructure, microVM isolation, deployed tenant isolation, or billing.

## Proposed test additions (not run)

The acceptance matrix now adds:
- NET-BARRIER-01: no task start until exact expected policy revision is reported applied; mismatch/pending/failure/timeout all prevent start.
- RACE-01: simultaneous cancellation and timeout produce one authoritative terminal execution outcome; cleanup is idempotent.
- PROC-TREE-01: offline OS-specific harness test for descendant processes; platform-specific expectations must be stated. This does not prove provider termination.
- REDACT-01: synthetic secret-shaped output is redacted in the report path and redaction is disclosed. Detection coverage is not universal.
- STREAM-01: output is consumed in bounded chunks; inline report cap and truncation metadata are deterministic.
- IDEM-01: same tenant + same key + same canonical request returns existing job; same key with different payload is conflict; cross-tenant use cannot reveal or reuse another tenant's job.
- ARTIFACT-01: partial write or hash mismatch makes the artifact invalid and prevents PASS.
- COST-01: separate observed usage telemetry from estimated/unknown/final cost; missing provider billing data is never $0 by default.
- CSV-01: only applicable if the owner confirms CSV as initial workflow; reject invalid encodings/sizes before allocation according to the documented CSV policy.

All proposed. **No tests were implemented or run.**

## Contract semantics that still need an explicit owner decision

1. Canonical execution_outcome enum and job_disposition enum; distinguish immutable observations from derived disposition.
2. Whether valid output may be exposed as provisional when cleanup fails. Regardless, it must never be overall PASS before mandatory cleanup/evidence gates pass; if exposed, quarantine/label it and document residual risk.
3. Timeout/cancel winner semantics. Prefer a single authoritative event/atomic transition plus append-only event history; do not let the client UI invent a winner based solely on wall-clock ordering.
4. Idempotency key scope, canonical payload hash, conflict behavior, retention period, and post-expiry retry semantics.
5. Inline output byte cap and artifact policy. Gemini suggested 1 MiB; this is a candidate value, not validated capacity or approved API.
6. Secret-redaction scope and limitations; no regex/entropy detector can promise complete secret removal.
7. CSV validation belongs in the product-specific workflow contract only if CSV is confirmed as the first workflow.
8. Provider telemetry fields and cost states (FINAL, ESTIMATED, UNAVAILABLE) require source-aware semantics and must not conflate local resource observations with invoice facts.

## Market review disposition

Gemini's recommendation for a 10-user behavior-based trial is useful as a low-cost proposal, but no trial has been run and its sample is qualitative, not statistically representative. Prefer asking users about a recent real task, then compare the same fixed task against tools they already use. Record completion, setup time, errors, artifact access, and handoff friction. Do not ask only whether they “would use” the product.

## Next actions

1. Keep the contract in proposal status; extend the test matrix and write a focused decision note for the unresolved semantics.
2. Verify cost and provider lifecycle claims from current primary sources; keep the strict $0 provider gate.
3. Add a source-backed network-policy barrier invariant to the provider-neutral contract and tests without choosing a provider.
4. Keep product validation and naming research separate from runtime/security proof.
5. Update checkpoint and PR description to record Gemini review received, its adopted findings, and the unadopted recommendations.

## Evidence status

- Gemini report received in the PocketCode conversation on 2026-10-27.
- Provider source checks above were performed by ChatGPT independently; they are not claims that Gemini's sources were independently validated by Gemini.
- No source code was implemented, no tests were run, no provider was accessed, no billing changed, and no PR was merged.
