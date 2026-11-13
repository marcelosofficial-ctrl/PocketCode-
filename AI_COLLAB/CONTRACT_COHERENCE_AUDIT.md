# Contract coherence audit — research-only

**Date:** 2026-10-27  
**Owner:** ChatGPT independent review; not Gemini completion  
**Status:** Static document review only. No code executed, no provider tested, no security claim validated.  
**Inputs:** [DRAFT_EXECUTION_CONTRACT.md](DRAFT_EXECUTION_CONTRACT.md), [PASS1_SECURITY_ABUSE_RESEARCH.md](PASS1_SECURITY_ABUSE_RESEARCH.md), [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md), and [DECISION_REGISTER.md](DECISION_REGISTER.md).

## Summary

The documents agree on the core safety posture: provider-neutral first, no outbound network/secrets/arbitrary installs/persistence for the first proof, mandatory controls fail closed, client claims are not execution evidence, and a fake adapter proves orchestration only. The draft is coherent enough to guide offline tests, but not ready to freeze as a production API. Several state/evidence edge cases must be made explicit before implementation.

## Findings and proposed resolutions

| ID | Risk / ambiguity | Proposed resolution before implementation | Offline test idea |
|---|---|---|---|
| C1 | PASS depends on execution and cleanup evidence, but cleanup failure is also represented as a separate terminal concern. A job could have valid program output but uncertain cleanup. | Preserve execution outcome separately from final service disposition. Never label overall job PASS unless required cleanup succeeds; report execution_outcome=SUCCEEDED with overall_status=INDETERMINATE or equivalent when cleanup is unconfirmed. Choose one vocabulary before API freeze. | Adapter returns exit 0 and valid output, then cleanup fails; overall result must not be PASS and must expose cleanup failure. |
| C2 | Timeout, cancellation, provider error, and limit-exceeded can race with late provider completion. | Define a single authoritative terminalization point and idempotent cancel/cleanup. Late events must not overwrite an already committed terminal outcome; preserve late evidence as diagnostics. | Deliver success after timeout, duplicate cancel, cleanup twice, and out-of-order callbacks; terminal outcome remains deterministic. |
| C3 | Requested policy, provider-confirmed policy, observed execution, and formatter output are separate concepts, but missing/contradictory evidence needs field-level rules. | Require an evidence record for each mandatory control: requested value, provider-applied/confirmed value, verification source, and result. Unknown/contradictory mandatory controls block start or prevent PASS. | Omit egress confirmation; claim “network disabled” in client input; return contradictory provider metadata; each must fail closed. |
| C4 | Cleanup success alone may not prove that the job’s files/processes/network identity were actually destroyed. | Treat provider cleanup acknowledgment as a signal, not universal proof. Record cleanup operation ID/result/time and any provider evidence available; do not claim stronger deletion guarantees than provider can substantiate. | Missing cleanup acknowledgment and malformed cleanup result never produce PASS; report does not claim secure erasure. |
| C5 | Proposed input/output/time limits are placeholders and may be confused with enforceable limits. | Keep provisional values visibly marked; define units, enforcement layer, boundary behavior, and whether stdout/stderr and artifacts share or have separate budgets. Production values must be enforced by trusted orchestration/provider, not just client-side validation. | Exact-boundary, one-byte-over, Unicode byte-vs-character, combined stdout/stderr, and artifact quota tests. |
| C6 | The adapter capability vocabulary is useful, but capability declaration can be stale or merely self-asserted. | Bind capability results to adapter/version/plan/config and a verification timestamp; distinguish provider documentation from observed configuration. Expire or recheck evidence when configuration changes. | A capability cached for a different plan/config must not authorize a run. |
| C7 | Artifact names/paths, links, and report rendering are attack surfaces even when inputs are restricted. | Normalize to generated server-side artifact IDs; reject path traversal and symlink-like semantics; keep display names separate from storage paths; escape untrusted text in HTML/UI. | ../, absolute paths, Unicode lookalikes, duplicate names, HTML/script strings, and content-type mismatch cases. |
| C8 | Tenant identity and job identity are stated, but authorization must cover every read/cancel/download/report operation. | Derive tenant from authenticated server context, never request body; authorize every operation against job owner; use opaque IDs as identifiers only, not bearer authorization. | Tenant B attempts status, cancel, artifact, and report access for tenant A’s job. |
| C9 | “No network” needs to include metadata, DNS, IPv4/IPv6, redirects, proxy variables, and provider control-plane exceptions. | Define the exact allowed egress model and document unavoidable platform/control-plane traffic. Verify controls at provider boundary; application-level checks are insufficient. | Threat-model matrix for DNS, metadata endpoints, IPv6, redirects, proxy env, and alternate protocols; real-provider cases remain blocked until authorized. |
| C10 | The report could conflate a well-formed report with a truthful execution result. | Include contract/schema version, job ID, terminal outcome, timestamps, policy confirmation, exit/limit facts, cleanup disposition, artifact manifest, and evidence provenance. Formatter validity must not elevate status. | Mutate formatter output to PASS while evidence says timeout; validator rejects inconsistency. |

## Minimum state/evidence rules proposed

1. A request is accepted only after schema, size, file type/path, and authorization checks.
2. No transition to RUNNING unless all mandatory controls are confirmed for the actual adapter configuration and plan.
3. Terminal outcome is decided once from authoritative provider events and trusted orchestration evidence; client-submitted status is ignored.
4. Overall PASS requires confirmed mandatory policy; authoritative completed execution; exit code 0; no timeout/cancel/limit violation/output truncation; artifact collection/validation success; and cleanup success under the explicitly chosen contract.
5. If execution succeeds but cleanup or evidence is uncertain, report a non-PASS overall status while preserving the observed execution outcome separately.
6. All status, cancellation, artifact, and report operations enforce tenant ownership server-side.
7. Provider evidence must distinguish documented capability, configured capability, and tested behavior. A fake adapter cannot mark real isolation/egress as tested.
8. Every external/provider claim must carry source URL and checked date in research notes; API/version/tier claims must not be generalized across versions.

## Priority acceptance-test map

- **P0 contract/unit tests:** C1, C2, C3, C5, C7, C8, C10. These are offline-testable once expected semantics are chosen.
- **P0 static review:** C4, C6, C9. Define honest evidence language and provider/config identity before any integration.
- **P1 authorized provider tests:** real timeout enforcement, resource ceilings, egress/metadata denial, cross-job isolation, process termination, cleanup, and tenant isolation. These remain blocked; no test should run without explicit owner approval, compliant $0 conditions, and any required vendor consent.
- **P1 user research:** validate whether the narrow task and report handoff solve a real recurring problem; contract correctness does not validate demand.

## Not resolved by this audit

- Exact production size/time/resource limits and billing ceilings.
- Whether cleanup failure should have a distinct top-level status or a two-axis status model.
- Authentication model and retention/deletion policy for a closed beta.
- Which provider, if any, can satisfy mandatory controls at a provable $0 ceiling.
- Whether a real execution service should be built at all; user demand is unvalidated.

## Guardrails

This audit is not implementation authorization. Do not select a provider, create accounts, enter billing details, execute hostile code, claim security proof, freeze the contract, merge PR #3, or deploy. Strict $0 remains binding and PR #2 remains untouched.
