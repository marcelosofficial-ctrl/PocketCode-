# RevDev + PocketCode: Product, Architecture, and Commercial Strategy

**Status:** Research synthesis and recommendation only; no product/architecture/brand/monetization decision is approved by this document.  
**Research checked:** 2026-10-28  
**Budget:** $0 unless the owner explicitly changes the constraint.  
**Repository boundary:** This memo is in the existing PocketCode continuity branch. It does not merge repositories, touch PR #2, select a provider, run workloads, trigger deployment, or change product/runtime state.

## Executive recommendation

Treat RevDev and PocketCode as two related product surfaces with a shared, versioned execution/report contract—not as one merged application today.

- **RevDev (PC):** desktop-oriented guarded automation and script execution, where Windows-specific capabilities and the existing product's trust boundaries matter.
- **PocketCode (mobile-first):** a provider-neutral workspace for creating/importing small code tasks, running supported work in a properly isolated remote environment, inspecting real results, and taking a concise evidence report back to any AI assistant.
- **Shared foundation:** run lifecycle, result schema, verdict semantics, report formatting/redaction/limits, stable identifiers, policy-decision vocabulary, and conformance fixtures.
- **Separate adapters:** Windows executor/automation, remote sandbox provider, mobile UI, desktop UI, authentication and deployment. Shared result types must not imply shared privileges or identical security guarantees.
- **No immediate rename, repo merge, shared backend, native-app build, provider account, or cloud execution.** Each requires separate evidence and owner approval.

The product opportunity is not simply “vibe coding from a phone.” Replit already markets mobile vibe coding for web apps. A more differentiated hypothesis is **an AI-provider-neutral execution and debugging companion that returns trustworthy evidence, works across phone and PC, and can later pair with RevDev when a user needs the desktop's capabilities**.

This is a hypothesis, not proven demand or a claim of uniqueness.

## 1. Product positioning and competition

### What is already present

- Replit's mobile app markets creating, iterating on, and publishing web apps from a phone: https://replit.com/mobile
- Replit's native mobile app workflow page says the fuller native iOS app build/submission workflow is accessed through Replit on the web, rather than being wholly inside the mobile app: https://replit.com/mobile-apps
- GitHub Codespaces, online IDEs, remote development environments, and browser-based coding tools are established alternatives; PocketCode should not position itself as merely another editor or terminal.
- Apple's App Review rules also explicitly warn against thin website wrappers and copycat positioning; see https://developer.apple.com/app-store/review/guidelines/ (Guidelines 4.1 and 4.2).

### Positioning worth testing

**Candidate:** “Run the code your AI gives you. See what actually happened. Send the evidence back to any AI. Keep building from your phone.”

Potential distinguishing workflow:
1. Bring a script and a small set of input files from any AI or project.
2. See the exact runtime and restrictions before running.
3. Execute only in a verified isolated environment.
4. See trustworthy status, stdout/stderr, exit code when available, duration when trustworthy, and generated files.
5. Copy a bounded, redacted report into ChatGPT, Claude, Gemini, or another assistant.
6. Apply a correction and rerun, preserving the prior result and provenance.
7. Export the project and evidence.

This narrows the product to the execution/evidence loop instead of trying to recreate every AI provider's editor, agent, model, and deployment stack.

### Evidence still needed

- Public desk research is qualitative and does not establish market size or willingness to pay.
- Test whether people want an independent execution companion versus simply using Replit, GitHub Codespaces, a remote desktop, a mobile terminal, or the AI provider's own product.
- Compare real tasks, not feature lists: small Python transformation, structured-data validation, generated file retrieval, test run, and failure report handoff.
- Record counter-evidence. If existing tools solve the user's most common phone-only task adequately, narrow the scope rather than adding features to appear different.

## 2. Naming and brand implications

“Pocket Code” is already the name of Catrobat's established free/open-source mobile visual-programming app:
- Official product description: https://catrobat.org/docs/getting-started/what-is-pocket-code/
- Existing App Store listing: https://apps.apple.com/de/app/pocket-code/id1117935892

This is a confirmed product/name collision, not a completed legal trademark search. “PocketCode” as one word does not remove discoverability, confusion, or trademark risk. Do not invest in a final icon, domain, marketing campaign, or paid listing under this name before a proper name/trademark/store search.

Potential naming directions to investigate, not approved:
- **A distinct standalone mobile brand:** best if PocketCode must work without RevDev or a PC.
- **RevDev Mobile / RevDev Companion:** clearer family connection if its main value eventually is to pair with RevDev on a PC; risks making a useful standalone mobile product sound dependent on the desktop product.
- **One RevDev product with mobile and desktop clients:** strongest family coherence, but premature until the shared contract and user journeys are proven.

Recommendation: keep the repository/project codename for internal continuity, but treat the public name as unresolved. Do not rename RevDev or combine the brands yet.

## 3. Connection options

| Option | Description | Benefits | Main cost/risk | Recommendation now |
|---|---|---|---|---|
| A. Shared contract, separate products/repos | Versioned run/result/report contract; each product owns its UI and executor adapter | Low coupling, useful now, independently testable | Need conformance tests and disciplined versioning | **Recommended first step** |
| B. Shared library/package | Publish a small language-neutral schema and perhaps report-formatting package after semantics stabilize | Less drift in field names/verdict rules | Packaging/toolchain burden; Python/C# clients may need separate implementations | Later, only after contract proves stable |
| C. Shared backend, separate clients | Phone and PC call a common authenticated API | Shared history, accounts, reporting and policy controls | Hosting, identity, cost, availability, data retention, attack surface | Research later; not approved |
| D. Explicit phone-to-PC pairing | PocketCode requests an approved operation from a running RevDev agent/relay | Can use the user's PC for Windows-only tasks and avoid duplicating runtimes | Network exposure, pairing/auth, PC online requirement, consent and dangerous remote-control surface | Long-term optional capability; threat-model separately |
| E. One merged app/repository now | Consolidate product, UI, runtime, identity and roadmap | Superficially simpler brand/code ownership | Couples different platforms and trust domains before compatibility is proven | **Do not do now** |

### The best technical seam

Share **descriptions and evidence**, not execution privileges.

A portable contract could define:
- schema version and stable run/mission ID;
- request origin and provenance;
- runtime ID/version and allowed capability profile;
- lifecycle states and exactly one terminal outcome;
- verdict plus exact execution status;
- exit code only when supplied by a trusted execution source;
- bounded stdout/stderr with truncation markers;
- output-file metadata and safe retrieval handles;
- trusted timestamps/duration only when available;
- rejection, timeout, cancellation, infrastructure failure and uncertainty semantics;
- redaction and report-size policy;
- policy decision and authorization evidence, without allowing an untrusted report field to grant authorization.

Each client/provider should advertise capabilities and enforce its own policy. A field saying “authorized” inside a report must never itself authorize execution. Policy checks must happen at the actual enforcement boundary.

### Security boundary

RevDev's PC executor and PocketCode's remote sandbox are not interchangeable:
- PocketCode should execute untrusted code only in a disposable isolated worker, never in the application server or the developer's workstation.
- RevDev must continue to use its own explicit action authorization, guard and executor checks.
- A shared schema or parser does not prove a shared implementation is safe.
- A mobile app connecting to a PC must require explicit pairing, scoped permissions, visible approval for consequential operations, revocation, replay protection, and an auditable result. Do not expose an unrestricted remote shell as the first integration.
- The mobile/remote product should default-deny outbound network access for submitted code, enforce server-side quotas/deadlines/output limits, and verify worker termination and cleanup.
- Apply OWASP MASVS as a mobile-app security checklist for storage, authentication, network, platform interaction, code and privacy: https://mas.owasp.org/MASVS/

## 4. Shared result semantics

PocketCode's proposed PASS / FAIL / INCOMPLETE rules are a promising cross-product seam:

- **PASS:** confirmed complete execution with trustworthy exit code 0 and no required evidence missing.
- **FAIL:** confirmed program/runtime failure or non-zero exit code.
- **INCOMPLETE:** rejected, timed out, cancelled, infrastructure-failed, or lacking sufficient trustworthy evidence.

Keep the detailed terminal status visible; the verdict is a summary, not a replacement for status. Never turn a request accepted by a provider into a successful run. Never infer that cancellation succeeded just because the client stopped waiting. Never infer that a test was executed merely because a script printed “PASS.”

For RevDev, this contract must be compared against the actual product and RelayRef reference behavior when source/runtime access is available. The current RelayRef portable tests are not proof that the installed Windows product implements this contract.

## 5. App Store feasibility: resolve early, do not assume

Official guidance:
- App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple Developer Program agreement's programming-environment clause: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/

Relevant constraints include:
- Guideline 2.5.2 restricts downloading/installing/executing code that changes app features. A limited exception exists for programming environments intended for learning to program, with conditions including fully viewable/editable source code, a conspicuous programming-environment indicator, no code storefront, and a screen-occupancy limit described in the agreement.
- Guideline 4.2 expects useful, app-like functionality beyond a repackaged website.
- Guideline 4.1 prohibits copycat naming/branding.
- Apps with accounts must provide the required review access/demo mode; in-app purchases must be complete and reviewable.
- iOS background execution is limited and should not be the basis of an assumption that arbitrary jobs can continue indefinitely.

These rules do **not** establish that a remote execution companion is prohibited or automatically allowed. A remote sandbox is different from executing downloaded code inside the iOS app, but App Review's interpretation of the actual product flow must be verified. The educational-programming exception may not fit a general-purpose developer tool.

Recommended path:
1. Keep the responsive web/PWA prototype as the low-cost workflow-validation surface.
2. Make its UI and report contract portable to native clients without committing to a wrapper.
3. Before native investment, prepare a concise App Review question with screenshots and a clear explanation of where code executes, how source is displayed/edited, whether execution can change app features, and how user code is isolated.
4. If a native app is pursued, build real mobile utility (file picker/export, reliable run status/reconnect, secure credential storage where needed, accessible editor, native share sheet, offline draft recovery) rather than a thin webview.
5. Provide a working reviewer/demo mode and backend availability for review. Do not advertise unsupported languages or security guarantees.

## 6. Commercial model hypotheses

No monetization decision is approved. The $0 budget remains binding for implementation work.

### Cost model implications

A paid one-time app purchase is simple to explain, but it does not automatically cover recurring remote compute, storage, support, abuse prevention, and provider costs. A subscription with a clearly stated included usage allowance or prepaid execution credits may fit a hosted execution product better, but creates billing, entitlement, refund, usage-metering and customer-support work. These are hypotheses to test, not a recommendation to implement billing now.

Possible future experiments:
- Free local editing/report formatting, with no claim of remote execution.
- A capped free remote-run allowance, if a verified sustainable funding path exists.
- Paid usage/credits for variable-cost execution.
- A subscription with explicit included run/resource quotas for frequent users.
- A future paid RevDev desktop edition only after users demonstrate sustained value and a stable support/release process.

Avoid “unlimited runs” unless a defensible cost/abuse model supports it. Do not rely on promotional cloud credits as a business model. Provider-neutrality should mean the product does not require a particular AI subscription; it does not mean remote execution infrastructure has zero marginal cost.

### Store economics to recheck at launch

- Apple Developer Program membership is currently listed at USD $99/year: https://developer.apple.com/help/account/membership/program-enrollment
- Apple's Small Business Program advertises a 15% commission for qualifying developers with up to USD $1 million in proceeds: https://developer.apple.com/app-store/small-business-program/
- Storefront and payment terms can differ. Apple published updated EU App Store terms effective 1 October 2026; current EU rates and alternative-payment rules differ from the familiar generic “30%” summary: https://developer.apple.com/support/apps-in-the-eu/

Treat these as current research, not permanent assumptions. Recheck the applicable storefront, tax obligations, payment rules and program eligibility before pricing or launch. With the present $0 budget, do not enroll, purchase, or enable billing as part of this research.

## 7. A low-cost sequence for both projects

### Now: phone-accessible, documentation and contract work
1. Keep the repositories separate and do not touch existing PocketCode PR #2.
2. Create a shared contract conformance table using synthetic examples: success, non-zero exit, timeout, cancellation, rejection, infrastructure failure, missing exit code, truncated output, and generated files.
3. Define provenance for every result field: executor/provider-observed, script-reported, user-supplied, or unknown.
4. Map RelayRef and the RevDev product requirements to that contract without claiming unverified Windows integration.
5. Add tests for report formatting/verdict semantics and negative controls that ensure incomplete evidence never becomes PASS.
6. Refine one mobile task and keep the prototype's sample output visibly simulated.
7. Continue public desk research and naming review; do not start a hosted execution workload.

### Later: only after evidence and explicit approval
8. Compare actual RevDev output and runtime behavior once PC access returns.
9. Evaluate a small shared contract package or generated schemas; keep provider adapters separate.
10. Run a controlled provider proof only after the owner approves a genuinely zero-cost path and network restriction, termination, cleanup, isolation and billing controls are verified.
11. Test demand and willingness to pay before accounts, persistent cloud workspaces, billing, or a native app.
12. Evaluate optional phone-to-PC pairing as a separate threat-modeled capability.

## 8. Decision ledger

| Question | Current status | Next evidence needed |
|---|---|---|
| Should the products share a contract? | Strong recommendation; not yet a canonical cross-repo decision | Compare field semantics and add conformance tests |
| Should the repositories merge? | No; keep separate for now | Demonstrated maintenance benefit that outweighs coupling |
| Should PocketCode become RevDev Mobile? | Unresolved; do not rename now | Product dependency/user tests, brand/name review |
| Is “PocketCode” a safe public name? | Collision confirmed; legal/trademark clearance not done | Broader trademark/domain/store search and legal review as appropriate |
| Is a native iOS app allowed to run this workflow? | Unresolved, not presumed prohibited or approved | App Review clarification based on exact implementation |
| Which remote execution provider? | Unselected | Zero-cost proof path plus isolation/cost/termination evidence |
| Should either product be paid? | Unresolved; $0 implementation budget remains | User demand, cost model, pricing tests, support plan |
| Can PocketCode invoke RevDev on a PC? | Long-term possibility only | Pairing protocol, threat model, explicit consent and PC-side guard tests |

## Sources checked

- Apple, App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple, Developer Program License Agreement: https://developer.apple.com/support/terms/apple-developer-program-license-agreement/
- Apple, Developer Program membership cost: https://developer.apple.com/help/account/membership/program-enrollment
- Apple, Small Business Program: https://developer.apple.com/app-store/small-business-program/
- Apple, EU App Store terms: https://developer.apple.com/support/apps-in-the-eu/
- Replit mobile: https://replit.com/mobile
- Replit mobile app development: https://replit.com/mobile-apps
- Catrobat, Pocket Code product description: https://catrobat.org/docs/getting-started/what-is-pocket-code/
- Catrobat Pocket Code App Store listing: https://apps.apple.com/de/app/pocket-code/id1117935892
- OWASP MASVS: https://mas.owasp.org/MASVS/

**Evidence caveat:** Public-source desk research only. No user interviews, app review consultation, trademark clearance, live provider test, price test, security test, or product integration was performed for this memo.
