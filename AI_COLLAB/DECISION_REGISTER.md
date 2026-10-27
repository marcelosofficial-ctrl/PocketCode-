# Decision Register — PocketCode

**Status:** research-stage decision control, updated 2026-10-27  
**Scope:** PR #3 research-only branch. This register does not authorize implementation, spending, provider selection, rename, merge, or deployment.  
**Budget gate:** strict $0. No provider account, credential, live workload, paid plan, billing change, or spend without explicit owner approval.

## 1. Evidence ledger

### Supported by current repository inspection or cited public documentation
- The current mobile prototype simulates execution; it is not evidence of a real execution backend.
- A narrow candidate workflow is: submit a short Python task plus small text/CSV input, receive an authoritative result and safe output artifacts, then copy a concise report into any AI chat.
- Public anecdotes show both quick phone-task demand and strong counterevidence (touch friction, setup/package constraints, local IDEs, Termux, remote desktops). They are not representative market evidence.
- Existing mobile editors and remote-development products already cover meaningful parts of phone-based coding. “Code from a phone” alone is not a defensible differentiator.
- Vendor documentation can establish what is claimed/documented, not prove our configuration is secure or suitable.
- Current paper review found no provider approved for a live proof under the strict $0 gate. Cloudflare Containers requires a paid base plan; Daytona controls are version/tier-sensitive; credits are not hard spending caps; E2B requires prior written consent before tests.
- Client-supplied status is not execution evidence. A trustworthy PASS requires verified policy, authoritative execution result, exit status, output-limit status, and cleanup evidence under the proposed contract.

### Hypotheses to test, not facts
- People have a recurring, painful need to verify short AI-generated Python+CSV tasks directly from a phone.
- No-setup disposable execution plus trustworthy bounded output/report handoff is meaningfully better than existing mobile IDEs, hosted notebooks, Termux, or remote development.
- A viable, secure runtime can be operated within the owner’s $0 constraint.
- A phone-first workflow can be useful without broad agent orchestration, arbitrary packages, network access, persistent jobs, or repo-wide editing.

### Unknown / not completed
- Frequency, urgency, and segment size of the target problem; willingness to pay; retention; and acquisition.
- Comparative task completion time and failure rate across real alternatives.
- Legal/trademark/name clearance for “PocketCode”; collision risk is a reason to investigate, not a legal conclusion.
- Native app distribution requirements, provider-specific real isolation, egress controls, cancellation/cleanup, tenant isolation, and total operating cost.
- Gemini’s required Pass 0–7 and cross-review completion. ChatGPT’s work is separately attributed and is not evidence that Gemini completed it.
- Gemini Pass 1 review has now been received from the user and triaged in GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md; this does not imply all recommendations are adopted.

## 2. Decision register

| ID | Decision | Current position | Reversible? | Gate / owner approval |
|---|---|---|---|---|
| D1 | First workflow to investigate | Short Python + small CSV/text input → authoritative bounded result/report | Yes | Research-only hypothesis |
| D2 | Product scope | Exclude arbitrary packages, network, secrets, persistent jobs, public ports, and broad agent orchestration from first proof | Yes | Revisit only with threat model and evidence |
| D3 | Provider | None selected; Gemini's Modal-default recommendation not adopted | Yes | No account/workload until mandatory controls and $0 hard cap are proven and owner explicitly approves |
| D4 | Budget | Strict $0 | No implicit relaxation | Explicit owner approval required to change |
| D5 | Runtime security | Fail closed when mandatory control is unsupported or unverified | Safety invariant | Cannot weaken merely to fit a free tier |
| D6 | Contract limits/state semantics | Draft only; two-axis execution outcome/disposition is leading proposal, not frozen schema | Yes | Resolve cleanup/result exposure, timeout-cancel races, idempotency conflicts, network-policy barrier evidence, output/redaction limits, and cost telemetry before implementation |
| D7 | Project name | “PocketCode” collision risk flagged | Yes | Research legal/name options; no rename without owner approval |
| D8 | Code/runtime implementation | Not authorized by this research PR | Yes | Separate implementation plan and approval |
| D9 | Merge/deploy/public release | Not authorized by this register | N/A | Explicit owner approval |
| D10 | Gemini attribution | Pending independent evidence | N/A | Log only verified Gemini artifacts/results |

## 3. Research gaps and next actions

### Gemini Pass 1 review — received 2026-10-27
- **Adopt as findings:** lifecycle axis separation, fail-closed network-policy applied-state barrier, deterministic race/process-tree/output/artifact/idempotency/cost tests.
- **Not adopted automatically:** Modal as default provider, blanket rejection of local Android execution, a fixed 24-hour idempotency TTL, 1 MiB inline output cap, universal CSV semantic validation, or a project rename.
- **Source correction:** E2B official pricing lists a free Hobby tier with one-time $100 usage credit and a $150/month Pro tier plus usage; Pro is not a universal entry requirement. Credits still do not satisfy a hard $0 cap. See the review integration note for current official URLs and remaining uncertainty.
- **Network barrier:** Daytona v2 alpha exposes desired/applied policy, status and revision; no user task should start until the exact mandatory policy is confirmed applied. This remains a design invariant, not runtime proof.

### Priority P0 — can be advanced offline, without accounts or spend
1. **Contract coherence audit:** compare request validation, lifecycle states, report evidence, cleanup semantics, and proposed limits across the draft contract, security matrix, and prototype report contract. Output: conflict list and acceptance tests.
2. **Evidence/link integrity:** verify every external source link and date in research docs; label stale/version-specific statements; distinguish official vendor claim from inference.
3. **Threat-to-test traceability:** map each mandatory security control to an adversarial test, required observable evidence, and fail-closed result. Do not claim a test passed unless actually executed.
4. **Scope/decision traceability:** ensure master plan, checkpoint, and PR description point to the same next action and correctly label draft/proposed decisions.

### Priority P1 — requires owner/user participation but no spend
5. **Behavior-based validation:** ask 5–8 target users about a recent actual task, then compare the same small deterministic Python+CSV task against tools they already use. Record setup time, success/failure, time to useful output, artifact retrieval, report handoff, and preference. No hypothetical “would you use it?” as sole evidence.
6. **Name review:** research distinct candidate names and obvious public collisions; this is preliminary screening only, not legal advice or clearance.
7. **Cross-agent review:** ask Gemini to review the specific artifacts and return evidence, contradictions, and test gaps. Do not count a requested review as completion.

### Priority P2 — blocked pending explicit approval / prerequisites
8. **Real provider proof:** blocked until a provider can enforce all mandatory controls, written permission is obtained where required, and spend is provably capped at $0. Free credits/trials do not satisfy a hard cap by themselves.
9. **Native app/distribution or production architecture:** defer until the narrow workflow is validated and provider/security feasibility is demonstrated.
10. **Merge, deploy, public claims, or name change:** owner approval required; no action implied by research completion.

## 4. Stop / continue / pivot criteria (exploratory, not statistical claims)

- **Stop or pause** if target users cannot recall recent instances of the problem, existing tools solve the task acceptably with little friction, or no compliant $0 proof path exists.
- **Re-scope** if demand is for file conversion, debugging/explanation, or remote-session control rather than disposable execution; document the evidence before changing the target.
- **Continue to a gated prototype** only if multiple participants show a recent real need, the fixed-task comparison reveals a repeatable advantage, and the security/provider gate has a plausible compliant path.
- These criteria are decision aids for a small exploratory sample, not statistically valid market thresholds.

## 5. Non-negotiable no-go list

Until explicitly approved by the owner: no provider accounts or credentials; no paid plans, card entry, billing changes, or spend; no live user-code execution or adversarial provider tests; no tests requiring vendor consent before that consent is obtained; no weakening mandatory isolation/egress/resource/cleanup controls; no merge or deployment; no public security or performance claims; no project rename; no claim that Gemini completed work absent recorded evidence.

## 6. Handoff checklist for any AI

1. Read this register, `RESEARCH_CHECKPOINT.md`, `DRAFT_EXECUTION_CONTRACT.md`, and `PASS1_SECURITY_ABUSE_RESEARCH.md`.
2. Work only on an explicitly assigned gap; inspect current branch files before editing to avoid duplicate work.
3. Separate facts, hypotheses, recommendations, and tests actually performed.
4. Add primary-source URLs and checked dates for changing provider/product claims.
5. Update this register/checkpoint/master plan/progress log only when state actually changes.
6. Never represent fake-adapter results as proof of real isolation or billing.
7. Preserve strict $0, keep PR #3 draft/unmerged, and leave PR #2 untouched.


## 7. 2026-10-27 lifecycle semantics follow-up

See [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md) for a consolidated proposal. It recommends append-only evidence plus a derived disposition, deterministic atomic terminalization, quarantining artifacts until cleanup confirmation, same-key/different-payload conflict, server-generated artifact identities with digest verification, bounded streaming, and explicit ESTIMATED/UNAVAILABLE cost states.

This proposal narrows implementation ambiguity but does **not** freeze the schema. Owner review remains needed for artifact release after cleanup failure, event reconciliation, idempotency retention, canonical fingerprint fields, and stream overflow behavior. The expanded cases in [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md) are NOT RUN.

**Next priority (current, after the 2026-10-27 static link and status pass):** owner review of [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md), followed by one coordinated contract/matrix update if the recommendations are approved. Do not implement lifecycle tests while expected outcomes remain undecided. PR #3 remains draft/unmerged and PR #2 untouched. No provider selection, spend, accounts, live workloads, merge, or deployment; PR #3 stays draft/unmerged and PR #2 untouched.
