# Research Checkpoint Addendum — 2026-10-27

**Checkpoint ID:** PC-RESEARCH-CP-ADD-2026-10-27-001  
**Branch:** pocketcode-pass0-audit-2026-10-26  
**Scope:** Follow-up after the original checkpoint; source/version coherence, lifecycle semantics, and Gemini handoff.  
**Status:** Static research and document review only. No tests run, no provider workloads, no accounts, no spend, no deployment, no merge.

## Canonical updates since the original checkpoint

- [Contract coherence audit](CONTRACT_COHERENCE_AUDIT.md) — static audit of lifecycle, evidence, cleanup, limits, capability freshness, artifact safety, tenant authorization, egress, and report integrity.
- [Contract coherence resolution](PASS1_CONTRACT_COHERENCE_RESOLUTION.md) — proposal to separate execution-outcome facts from overall job disposition. **Proposal only; not an accepted API decision.**
- [Offline acceptance-test matrix](OFFLINE_ACCEPTANCE_TEST_MATRIX.md) — proposed deterministic tests, including LC-01 through LC-12. **Not run.** Fake adapters cannot establish provider isolation, real termination, effective egress enforcement, or billing behavior.
- [Source/version coherence audit](PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md) — records provider-document version and source-integrity follow-ups.
- [Runtime/provider gate](PASS1_RUNTIME_PROVIDER_GATE.md) — provider-neutral gate; no provider approved for live tests under the current strict $0 budget.
- [Gemini review request](GEMINI_REVIEW_REQUEST.md) — prepared for external copy/paste. It has **not** been sent to Gemini by ChatGPT, and Gemini review is not complete.

## Source/version corrections to preserve

1. **Daytona v0 and v2 alpha are different documentation contexts.** Do not transfer v0 tier-based override claims into v2 alpha. Review both pages separately:
   - v0 network limits: https://www.daytona.io/docs/en/network-limits/
   - v2 alpha network limits: https://www.daytona.io/docs/en/v2/network-limits/
   - v2 alpha limits: https://www.daytona.io/docs/en/v2/limits/
   The v2 alpha network documentation says egress is open by default and requested policy may differ from applied policy. A configured request alone is not proof of effective enforcement. These are documentation findings, not runtime verification.

2. **E2B security/testing permission:** current reviewed page is https://e2b.dev/security. It says to contact E2B before running tests because prior written consent is required. No testing was attempted.

3. **Modal networking:** https://modal.com/docs/guide/sandbox-networking. Direct page retrieval returned an upstream 502, but a current search-indexed result was available on 2026-10-27: public outbound access is allowed by default; `block_network=True` blocks all outbound traffic including DNS; ordinary allowlist configurations allow DNS without restriction; domain allowlisting is Beta and limited to TLS/443. Re-open the primary page before a provider decision. Pricing: https://modal.com/pricing. Included credits are not a guaranteed hard $0 ceiling.

4. **Cloudflare Containers pricing:** https://developers.cloudflare.com/containers/platform/pricing/ lists the Workers Paid base plan at $5/month. That conflicts with the current strict $0 constraint absent an explicit owner-approved budget change.

5. **Do not equate official documentation with verified behavior.** Provider claims remain unvalidated until an explicitly authorized, controlled proof is conducted. No such proof is currently authorized.

## Lifecycle decision still open

The draft contract's sequence can be read as SUCCEEDED followed by cleanup, while other prose implies success requires cleanup success. The proposed resolution is to distinguish:

- **Execution outcome:** observed process facts (for example zero exit, non-zero exit, timeout, cancellation, or termination unconfirmed).
- **Overall job disposition:** the policy-governed final report status after evidence, artifact, and cleanup gates.

This separation is a candidate model, not an approved schema. Before implementation, choose explicit semantics for cancellation/timeout races, cleanup failure, retries, duplicate events, missing evidence, and partial artifact publication. No PASS may be reported if mandatory evidence or cleanup requirements are unmet.

## Product validation and limits

- The prototype remains simulated; no real execution backend exists.
- The Python+CSV quick-run verifier remains a hypothesis, not validated demand.
- No representative interviews or hands-on task benchmark has been completed.
- PocketCode naming collision risk remains unresolved; no legal conclusion or rename decision.
- Strict $0: no accounts, credentials, provider workloads, billing changes, deployment, or merge.

## Current repository/PR snapshot

At checkpoint creation, PR #3 was open, draft, unmerged, with branch head c7c1a6601c4635f12aefa1c6d164a1d248bea8ed. Re-check live PR metadata before relying on that SHA. PR #2 must remain untouched.

## Next actions

1. Obtain Gemini's independent review using the handoff request; do not mark it complete until actual findings are returned.
2. Reconcile provider-version wording in the main provider research document with the source/version audit.
3. Verify internal links and source claims; reopen Modal networking documentation directly before any provider decision, since the search-indexed result was available but the direct page fetch returned 502.
4. Update the decision register/checkpoint after the review, preserving explicit proposal-versus-decision labels.
5. Only after review, decide whether the contract is coherent enough for an offline-only implementation plan. No provider selection or live test without separate approval.
