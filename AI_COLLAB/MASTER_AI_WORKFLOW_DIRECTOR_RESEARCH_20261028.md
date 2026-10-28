# PocketCode — Master AI Workflow Director Research
**Research date:** 2026-10-28  
**Status:** Research synthesis and product proposal; not a frozen product/API decision or implementation.  
**Purpose:** Establish one durable reference for a distinct PocketCode feature that helps different AI assistants work efficiently, preserve project continuity, conserve free-tier usage, and return useful results to the mobile coding workflow. This research extends—not replaces—the existing PocketCode product hypothesis and the separate RevDev project.

**Implementation-planning companion:** [AI Workflow Director — First Testable Feature Slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) defines the proposed four profiles, task-packet and continuation-capsule contracts, 16 static acceptance cases, and an evaluation protocol. It is still a proposal; no implementation or tests are claimed.

**Manual evaluation companion:** [AI Workflow Director — Offline Evaluation Kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) supplies eight fixed task fixtures, paired baseline/Director instructions, a scoring rubric, and an evidence record. It is a test protocol only; no assistant runs or benchmark results are claimed.

**Conformance-test companion:** [Deterministic AWD-01–16 test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) converts the proposed acceptance cases into required assertions, forbidden behaviors, cross-case invariants, and explicit open contracts. It is design-only; none of the cases have been executed.  

**Canonical fixture catalogue:** [AWD-01–AWD-16 repeatable fixture inputs and observable pass/fail rules](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) elaborates every existing acceptance ID with proposed harness inputs, layer boundaries, forbidden behavior, and unresolved dependencies. All cases remain NOT RUN.  

**Contract reconciliation and decision gate:** [Decision register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) compares eight proposed defaults against MVP requirements, marks safe semantic assertions, and records unresolved decisions without treating recommendations as accepted.

**Pre-implementation readiness audit:** [Focused audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) reviews AWD-08, AWD-11, AWD-12, and AWD-14, prioritizes blockers versus deferrable work, and proposes a minimal offline builder scope. It is static analysis only; implementation remains unauthorized.

**Reference fixtures:** [Expected-output examples for five priority cases](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) make scoring more consistent; these are human-authored examples for EVAL-01, 02, 04, 06, and 08, not test results.

**Phone-friendly run sheet:** [Manual paired-run procedure](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md) gives exact baseline/Director prototype prompts, canonical profile mapping, five copy-paste task fixtures, and a per-run evidence record. It is still an unexecuted protocol.

**Current continuity checkpoint:** [PocketCode current checkpoint](POCKETCODE_CURRENT_CHECKPOINT_20261028.md) records the working branch, completed audit corrections, explicit evidence boundaries, and ordered next passes.

## Executive conclusion

PocketCode should develop a distinct feature provisionally named **AI Workflow Director**. It should not try to secretly control every AI app or pretend all assistants expose the same integration interface. Instead, it should generate small, context-aware instructions and task handoffs, then use the safest communication channel each platform actually supports.

The recommended design has three layers:

1. **Universal baseline:** a compact, copyable instruction profile and per-task prompt that can be pasted into any AI app with a text input. This must work without an API key, paid subscription, special extension, or account connection.
2. **Opt-in platform adapters:** setup guidance for persistent custom instructions; user-initiated share-sheet/shortcut flows; and exportable project instruction files or skills for developer tools that support them. The feature registry records what each assistant actually supports, its restrictions, and when that information was checked.
3. **Optional native/API integrations:** only when an AI provider publishes a suitable interface and the owner explicitly approves the cost, permissions, data handling, and implementation. Do not assume a paid consumer subscription includes API calls.

PocketCode can improve the efficiency of free AI use, but it **cannot guarantee that an AI will always follow the instructions, prevent every usage cap, or bypass provider limits**. Its job is to reduce avoidable waste, retain progress when limits are reached, and make the next useful step easy. It must not evade rate limits or provider restrictions.

The long-term relationship with RevDev should be expressed first through **shared contracts, handoff semantics, lifecycle states, and report evidence**, not a premature repository merge. RevDev remains the PC automation path; PocketCode is the mobile-first workspace and AI workflow director. Both may eventually be front ends to a compatible task/control model, but compatibility is a hypothesis until compared against verified RevDev artifacts.

## 1. Research scope and evidence labels

This was conducted as three passes:

- **Pass 1 — workflow-optimizer systems:** inspected Ponytail's published skill/benchmark, Claude Code's official skill/hook/memory guidance, Anthropic's coding-agent best practices, OpenAI's Codex guidance, and the composable-skills approach used by Superpowers.
- **Pass 2 — phone and provider communication:** checked official iOS Shortcuts/share-sheet guidance, Android sharing guidance, and current official help for ChatGPT custom instructions, Claude personalization, and Gemini instructions.
- **Pass 3 — PocketCode/RevDev convergence:** read PocketCode's current Product Specification, Roadmap, Decision Log, and RevDev/PocketCode shared-core proposal. Reconfirmed PR #2 and #3 were still draft/open/unmerged on 2026-10-28; this research branch does not modify them.

Use these terms:
- **Verified source fact:** directly described in the cited primary source.
- **Maintainer-reported result:** reported by the project whose tool is being evaluated, not independently reproduced here.
- **Recommendation:** proposed PocketCode behavior, not yet accepted as a final architecture decision.
- **Unknown:** not established by the research or by current device/runtime evidence.

This is desk research, not a real-device integration test, user study, or benchmark of PocketCode. Research cannot prove that an instruction will reliably change the behavior of every current or future model.

## 2. Pass 1 — what workflow-optimizer extensions teach us

### 2.1 Ponytail: useful methods, not a magic prompt

Ponytail is an open-source, MIT-licensed coding-agent skill/plugin. Its central principle is the smallest complete solution, with a “lazy senior developer” posture. Its current skill asks the agent to inspect the task and affected code, trace callers/tests/fixtures/config, reuse the standard library and platform features before adding abstractions, test risky logic, and report what was skipped or remains risky. It has narrower review/audit/report commands and supports multiple coding-agent harnesses through different adapters or packaging.

The transferable pattern is **behavior + workflow + feedback**, not simply a memorable persona:
- inspect relevant existing code before proposing a rewrite;
- reuse existing utilities, dependencies, platform features and conventions;
- avoid speculative abstraction and unrequested scope;
- make the smallest change that satisfies explicit requirements;
- test branches, parsers, security-sensitive paths and other risky logic;
- distinguish what was verified from what was not checked;
- use targeted review/audit actions rather than reflexively reviewing everything;
- keep a visible record of cost, turns, agent time and tests where the environment exposes those measurements.

Ponytail's own 2026-10-07 benchmark reports 39 tasks, five runs per task for three arms (585 sessions), using Opus 5.5 in the Claude Code CLI. It reports 45% lower output tokens, 26% lower cost and 41% lower elapsed time versus no skill. Only 18 of the tasks had executable hidden correctness/security checks: the reported passing counts were 86/90 without the skill and 87/90 with Ponytail 5. The maintainer provides its methodology and a reproduction route. These are useful signals but **not independent results**, were measured in a coding CLI with shell disabled, and do not establish the same savings for ChatGPT, Claude or Gemini consumer mobile apps—especially their free tiers. PocketCode should measure its own outcomes before advertising any percentage improvement.

Source: https://github.com/DietrichGebert/ponytail  
Skill: https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md  
Benchmark and limitations: https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-10-07-agentic.md  
Project overview: https://ponytail.dev/

### 2.2 Skills and hooks versus ordinary chat instructions

Claude Code's official documentation distinguishes always-loaded project/user instructions from skills whose descriptions are available up front while the full skill body usually loads only when invoked. It also warns that long instruction files consume context and can weaken adherence. Hooks in a coding-agent harness can inject context at specific points in a tool lifecycle and, in some cases, enforce tool decisions. These mechanisms are not available in every ordinary mobile chat app.

Anthropic recommends concise project instructions and concrete task scope, relevant files, commands, expected output and tests. OpenAI's Codex guidance similarly recommends structured tasks, planning larger changes before editing, using repository instructions such as AGENTS.md, and leaning on tests and real project context.

Superpowers demonstrates a broader multi-harness approach built from composable skills and a workflow methodology. Its setup documentation still requires installing/supporting the workflow separately for each agent harness. That is the important architecture lesson: **portability is achieved by translating a shared behavioral intent into each tool's supported mechanism**, not by assuming one plugin can control every assistant.

Sources:
- Claude Code skills: https://code.claude.com/docs/en/skills
- Claude Code hooks: https://code.claude.com/docs/en/hooks
- Claude Code memory/instructions: https://code.claude.com/docs/en/memory
- Anthropic's best practices: https://www.anthropic.com/research/claude-code-best-practices
- OpenAI's Codex practices: https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- Superpowers: https://github.com/obra/Superpowers

### 2.3 Design implications

PocketCode should not ship a giant master prompt that is attached to every turn. A more token-efficient structure is **progressive disclosure**:

- a very small always-on behavioral kernel;
- one compact profile selected for the current task;
- only the project facts, code excerpts, errors or results needed for that task;
- a fuller specialist playbook only when the task actually needs it;
- a bounded continuation capsule when a chat/context is ending or a usage limit blocks further work.

Use the persona idea only as a light style cue. The instructions must state observable behaviors and boundaries. Ultra-compressed or “caveman” wording is not a universal win: compression that removes important constraints, evidence requirements or nuance is a regression.

The goal is **minimum total effort to reach a verified result**, not the fewest words in one answer. A tiny prompt that causes five repair turns can cost more than a slightly longer, well-scoped request.

## 3. Pass 2 — communicating with AI apps on a phone

### 3.1 The OS handoff ladder

Different integration levels should be explicit in the product and UI.

**Level 0 — universal copy/paste (must-have baseline).** Generate a compact instruction or task packet, let the user review it, copy it, and paste it into any AI assistant. Accept the assistant's response back through explicit paste/import. This works without an API connection and is the only defensible baseline for “any AI app.”

**Level 1 — user-initiated share sheet.** On iOS, apps and Shortcuts can receive selected content through the share sheet; a Shortcut can be made available from another app and can process the content that app shares. On Android, ACTION_SEND and the Android Sharesheet can pass text using the appropriate MIME type, such as text/plain. This is a useful bridge for moving a snippet, task packet, error report or file into compatible apps.

A share operation is not proof that the receiving AI app will prefill a chat, append to an existing conversation, or automatically submit the content. Those behaviors depend on the receiving app and supported entry points. PocketCode should show the generated content first and make the user's transfer explicit.

**Level 2 — provider-specific setup guides and shortcuts.** Where a provider has persistent instructions or documented deep links, PocketCode can show current setup steps and offer a ready-to-copy profile. An iOS Shortcut can assist a user-initiated workflow where supported actions exist. Android can launch compatible targets through intents. Neither should be presented as universal, silent control over the target app.

**Level 3 — official APIs/connectors.** An API can give PocketCode more direct control over a model interaction, but it is a separate integration with separate credentials, data handling, rate limits and cost. OpenAI explicitly bills API usage separately from ChatGPT subscriptions; Anthropic likewise treats Claude.ai subscriptions and API Console usage as separate products. Therefore direct APIs are not a zero-cost substitute for the consumer app and must remain optional and unapproved until separately evaluated.

**Level 4 — agent-to-agent/tool protocols.** MCP is oriented toward agent-to-tool/resource connectivity, and A2A toward communication between independent agents. They may matter if PocketCode or a compatible coding agent exposes those endpoints. They do not make ordinary consumer AI mobile apps automatically interoperable, and A2A itself describes machine-to-machine agent communication rather than a consumer chat application.

Sources:
- Apple Shortcuts from another app: https://support.apple.com/en-gb/guide/shortcuts/apd163eb9f95/ios
- Apple share actions/opening apps: https://support.apple.com/en-euro/guide/shortcuts/apdaf74d75a5/ios
- Android send/share data: https://developer.android.com/develop/ui/compose/sharing/send
- ChatGPT/API billing separation: https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
- Claude/API billing separation: https://support.anthropic.com/en/articles/9876003-i-subscribe-to-a-paid-claude-ai-plan-why-do-i-have-to-pay-separately-for-api-usage-on-console
- MCP/A2A distinction: https://a2a-protocol.org/latest/

### 3.2 Current examples of provider-specific customization

This is a dated snapshot, not a promise that these features, labels or limits never change.

| Assistant | Documented customization route | Important limitation for PocketCode |
|---|---|---|
| ChatGPT | Custom instructions are available across plans on web, desktop, iOS and Android. The current help page says Free/Go users can save up to 1,500 characters. | Good candidate for a persistent compact profile. The app must still support one-shot copy/paste when users do not configure it. |
| Claude | Account-wide instructions/preferences guide responses; Claude Projects and project instructions are currently listed as paid-plan features. | Do not make Projects a requirement for free users. Offer account-level setup where available and generic task packets for all users. Claude Code skills/hooks are a separate developer-tool capability, not the same as the ordinary Claude mobile app. |
| Gemini | Instructions for Gemini are documented in its mobile and web apps for eligible personal Google accounts. The official help page excludes work/school/supervised accounts and says the feature is unavailable in some surfaces such as Gems. | Check eligibility and current surface before promising it. Keep a universal prompt fallback. |

Sources:
- ChatGPT custom instructions: https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions
- Claude personalization: https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features
- Gemini instructions: https://support.google.com/gemini/answer/16598625

### 3.3 Platform limits and privacy boundary

PocketCode should not depend on:
- system-wide overlays or a floating UI covering other apps;
- background clipboard polling or silently reading other apps' chats;
- reading or modifying another app's private settings;
- UI scraping/accessibility automation as the default communication mechanism;
- credentials, cookies or private account access copied from another AI app.

Apple's sandbox model explicitly restricts access to other apps' preferences and arbitrary app control. Beyond feasibility and policy risk, these approaches would undermine user trust and make platform compatibility brittle.

Use explicit user-selected content and intentional handoffs. Preview the packet, identify included files/source/output, redact configured secrets where possible, show truncation, and let users exclude content before transfer. Redaction is best-effort and should not be marketed as perfect secret detection.

iOS sources: https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox and https://support.apple.com/en-gb/guide/shortcuts/apd163eb9f95/ios

## 4. The free-tier promise: optimize usage, never evade limits

“Works very well in free mode” should mean that the feature is designed around small budgets, not that it disables provider limits. Usage limits, model access, tools, context windows and feature eligibility change by provider, plan, region and account. PocketCode cannot truthfully guarantee that a free assistant will never rate-limit a user or that instructions will always be followed.

Proposed behavior:
- default to a compact instruction profile and short task-specific packet;
- avoid re-sending the whole project or research master when only one function, test or error matters;
- keep durable project facts in a local/exportable continuity record;
- batch related questions and edits into one clearly scoped mission when doing so reduces back-and-forth without making the task ambiguous;
- use one primary implementation assistant; ask for an independent review only for a bounded high-value question or higher-risk change;
- ask clarifying questions only when a missing answer materially blocks safe progress; otherwise state a reasonable assumption and proceed;
- request exact verification evidence and a concise summary, rather than repeated narrative progress reports;
- do not claim a test passed when it was merely written or not executed;
- track native usage/cost metrics only when the provider exposes them; otherwise mark them unavailable and use prompt length/turn count only as proxies;
- when a limit or tool cap is reached, save a continuation capsule, stop retries, and let the user resume later or transfer the capsule to a different assistant;
- never create rapid retry loops, evade quotas, rotate identities to bypass controls, or imply that PocketCode can override plan limits.

A compact profile should aim for approximately 1,000–1,200 characters where practicable, allowing a little headroom under ChatGPT Free/Go's currently documented 1,500-character limit. This is a design target for one common provider, **not** a universal character or token limit. The generic one-shot prompt should remain useful even where a provider offers no persistent-instruction feature.

## 5. Proposed feature: AI Workflow Director

**Status: product hypothesis/proposal.** The feature should be distinct and visible in PocketCode, not buried in settings and not limited to one provider.

### 5.1 Main components

**A. Workflow Profile Library**
- **Lite:** small changes, minimal analysis and concise output; use for simple, low-risk requests.
- **Balanced (default):** inspect relevant context, reuse existing patterns, define acceptance criteria, implement the smallest complete solution, run relevant checks and report evidence.
- **Careful:** explicit risk/edge-case review, security/privacy attention and stronger verification for consequential changes.
- **Review only:** analyze a proposal/diff/result without implementing it.
- Profile instructions say when *not* to expand scope. They must not tell a model to skip necessary safety, privacy, security or correctness work.

**B. Task Compiler**
Turn a user's goal and PocketCode workspace evidence into one compact prompt with:
1. one concrete outcome;
2. scope and constraints;
3. only relevant files/snippets/errors or evidence references;
4. observable acceptance criteria;
5. permitted/prohibited actions and whether implementation is authorized;
6. what verification to run or what evidence is unavailable;
7. a short response/checkpoint format.

The compiler should prefer existing project files and selected evidence over asking an AI to rediscover everything. It must not invent paths, tests, results, repo state or provider capabilities.

**C. Provider Capability Registry**
Store a small, versioned per-provider record: supported persistent-instruction route; free-plan applicability where official docs establish it; character limits if published; share/import/deep-link capabilities; API/connector availability; account/region prerequisites; last-verified date; primary source URL; known caveats. Show “unknown/not verified” instead of guessing. Re-check volatile provider details on release or before giving setup instructions.

**D. Handoff Bridge**
Provide an obvious Copy prompt, Copy result/report, Share, and Open assistant actions where supported. Keep copy/paste available even if share targets or links change. Transfer should require a user action and show what leaves PocketCode. On return, accept pasted AI replies and user-selected files as input to the workspace.

**E. Continuity Capsule**
Make long-chat continuity a product capability. At natural checkpoints or when the user requests it, create a compact portable state block with:
- project and task identity;
- verified branch/commit or source artifact references, when known;
- goal and current stage;
- decisions and constraints;
- exact files/artifacts and relevant errors;
- tests actually run and precise result;
- blockers, unknowns and next acceptance criterion.

The capsule must separate facts, proposals and unknowns, avoid copying the whole conversation, and be exportable as plain text/Markdown. It should help the user resume after a free-tier limit, context loss, model switch or app switch.

**F. Efficiency Evidence**
Track local workflow metrics without pretending every provider exposes token counts: instruction/payload character count, number of handoffs/turns the user records, number of repeated context items, verification status and whether the task was completed. Record provider-native token/cost metrics only when returned by an official interface or entered by the user. Keep local metrics private by default; no telemetry is needed for the first proof.

### 5.2 Minimal portable behavioral kernel (illustrative, not frozen)

> First inspect the relevant context and reuse existing code, libraries and platform features before inventing new ones. Solve only the requested task with the smallest complete change; avoid speculative abstractions and unrelated cleanup. For complex or risky work, state the goal and acceptance checks before editing. Verify the important behavior with the narrowest useful tests. Never claim to have run checks or inspected files when you have not. Keep output concise and specific: changed, verified, not checked, risks, and next step. Preserve decisions and exact evidence in a short checkpoint when context is running low.

This kernel should be tested against the target AI apps before it is promoted as the default. Provider-specific setup can install it as a persistent instruction; otherwise PocketCode prepends the smallest relevant version to the next task prompt. Avoid pasting the full behavior profile into every turn if a persistent setting is already configured.

### 5.3 Candidate task prompt template

**Goal:** [one outcome]  
**Context:** [only relevant files/snippets/errors and verified state]  
**Constraints:** [scope, platform, budget, safety and authorization boundaries]  
**Acceptance:** [observable success criteria]  
**Verification:** [tests/evidence to produce; say explicitly when not available]  
**Reply:** [changed / verified / not checked / risks / next step]

Do not append the same project master, all previous messages, or a generic exhaustive checklist to every prompt. The user should be able to select a “small task” path without triggering a long research or implementation ceremony.

## 6. Research-backed behavior rules to test

1. **Inspect before inventing.** Search the relevant workspace and existing dependencies before writing new utilities or proposing broad rewrites.
2. **Smallest complete change, not lowest code count at all costs.** Preserve needed validation, security, accessibility and error handling.
3. **Progressive disclosure.** Persistent kernel; on-demand task profile; context-specific packet; detailed specialist instructions only when justified.
4. **Structured task framing.** Use clear goal, relevant file references, constraints, acceptance criteria and verification expectations.
5. **One primary worker.** Avoid sending the same job to three assistants. Use Gemini/another assistant as an independent reviewer for a bounded question, not a duplicate implementer.
6. **Evidence-oriented responses.** Ask for exact tests/output and label unverified results, instead of verbose narration.
7. **Targeted test selection.** Run the narrowest relevant test first, expanding only when risk/scope merits it.
8. **Short context, durable state.** Store decisions and artifacts outside the chat, then send only the subset relevant to the current mission.
9. **Graceful interruption.** Never retry endlessly after rate/usage/context limits; save a continuation capsule and stop.
10. **Human approval stays explicit.** The profile is not an authorization mechanism. It cannot grant permission to access accounts, spend money, launch code, delete data, deploy or perform consequential actions.

These principles are recommendations drawn from tool documentation and maintainer reports; their effectiveness in consumer mobile apps still needs testing.

## 7. RevDev convergence: “RevDev for the phone” without premature merger

The existing PocketCode shared-core proposal already recommends comparing the systems through a shared run lifecycle and result/report contract while keeping their repositories separate. Build on that proposal rather than creating a competing architecture.

### Shared concepts to align first
- task/mission ID and idempotent submission identity;
- accepted/queued/running/terminal/incomplete states;
- execution facts separate from overall disposition and cleanup status;
- authoritative exit status, stdout/stderr, duration, artifacts and explicit truncation;
- report version and evidence provenance;
- cancellation, timeout, rejection, provider/infrastructure failure and recovery;
- bounded AI handoff packet and continuation state;
- user authorization and a record of whether an action was requested, approved, blocked or not run.

### Keep separate until proven otherwise
- RevDev's Windows/PowerShell watcher, local automation queue, host execution process, installed binary/runtime and queue management;
- PocketCode's mobile UI, touch-first task editor, provider guidance, share/copy handoff and potential remote isolated runner;
- product release cycles and codebases.

The proposed shared foundation is an **interface contract**, not a shared UI or a merged repository. Compare the actual RevDev RelayRef/queue/result artifacts when they are available; PC/runtime/queue state must remain unknown while the owner has no PC access. Do not claim the current installed RevDev behavior is verified from memory.

### Suggested convergence sequence
1. Write a small provider-neutral task/handoff schema and result contract from requirements that genuinely overlap.
2. Map current RevDev RelayRef fields and real mission result artifacts against it when verified artifacts are available.
3. Build shared, provider-neutral test fixtures for success, failure, timeout, cancellation, missing evidence, limit breach and resumed context.
4. Specify adapters: desktop local queue/runtime; mobile workspace/remote execution; consumer AI app share/copy; optional official AI APIs.
5. Only after compatibility and user value are demonstrated, evaluate sharing libraries or code. Keep repository separation until an explicit architecture decision says otherwise.

The workflow director is the cross-cutting feature in this convergence path: it helps any assistant create a better task, consumes execution evidence from either client, and returns the evidence in a provider-neutral report. It does not replace the execution safety contract.

Related current proposal: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md

## 8. MVP and later-phase proposal

**Phase A — zero-cost research/static prototype**
- Add an AI Workflow Director entry point to the product concept.
- Create Lite/Balanced/Careful/Review-only profiles and a generic copyable task packet.
- Add a local continuation-capsule template and provider capability matrix.
- Test profile length and task-packet generation with static fixtures; no API keys, AI calls or provider workload required.

**Phase B — phone handoff**
- Use the native iOS/Android share mechanisms with copy/paste fallback.
- Include a clear preview and explicit user action before sharing.
- Accept pasted AI output and pass the real execution report back to the selected assistant manually.
- Verify behavior on actual iOS and Android devices before promising specific share flows. This phase is proposed, not implemented.

**Phase C — provider setup**
- Add sourced instructions for ChatGPT, Claude and Gemini first, followed by other assistants only when supported and demand justifies the maintenance.
- Respect provider plan/region/account limitations; the baseline must continue to work when persistent instructions are unavailable.
- Export project-agent rule files or skills only where the target coding harness supports them, with install guidance and license review.

**Phase D — evidence-led integration**
- Benchmark the feature on a small representative suite of coding/debugging tasks using consumer free modes first; compare paid modes separately if owner/testers have access.
- Consider official API/connector integrations only after cost, privacy and maintenance review and explicit approval. Consumer subscriptions must not be treated as API credits.

## 9. Acceptance criteria for the feature

The first useful version should not be called complete until:
- A user can generate a useful prompt and continuation capsule offline at $0.
- The generic prompt works by manual paste in an AI app without connecting accounts or using APIs.
- Provider-specific guidance names the verified feature and exact prerequisite, and links the current official source.
- Missing features, unsupported deep links, unknown limits and unavailable token metrics are disclosed rather than fabricated.
- The user sees and approves the exact content shared, with an opportunity to remove sensitive files or output.
- The share/copy route has a fallback when the target app cannot accept the content.
- The behavior profile reduces irrelevant context without telling the AI to omit required safety, tests or correctness.
- Usage-limit interruptions preserve the last checkpoint and stop automatic retrying.
- Reports distinguish actual evidence from user/AI assertions and unrun tests.
- RevDev compatibility work reuses the existing shared-core proposal and does not merge repositories or change PC runtime state.

## 10. Evaluation plan and metrics

Treat Ponytail's percentages as a motivating example, not an expected result. Create a small test set spanning: a one-line fix, reuse of an existing utility, a test repair, a bug with edge cases, a multi-file change, a security-sensitive change, a long-chat continuation, and a run-report debugging loop.

For each task, compare a baseline prompt with PocketCode's profile/task packet using the same target model and plan wherever possible. Record:
- task completion and correctness against explicit acceptance criteria;
- whether required tests were added/run and whether evidence was truthful;
- number of model turns and user copy/paste steps;
- repeated context, total prompt/output characters, and provider-native token counts if actually exposed;
- overengineering/unrequested changes;
- failures, rate/usage-limit interruptions, and whether continuation recovered without repeating work;
- user-rated clarity and effort.

Do not compare different models/plans as though the profile were the only variable. Do not treat prompt characters as exact tokens. Repeated trials should be used where the available quota permits; report missing samples and uncertainty. Prefer a small reproducible benchmark to unsupported marketing claims.

## 11. Open questions

- Which AI assistants must be supported in the first mobile release based on the owner's actual use and user validation?
- Should the profile library be local-only initially, or synchronized/exported with the user's projects?
- Which current iOS/Android sharing paths reliably prefill text in specific AI apps, and what do they actually do on real devices?
- How much persistent-profile customization is available in each free plan at implementation time?
- What prompt length/turn-count improvement is observable without hurting correctness?
- What portable schema best reconciles RevDev's RelayRef/mission protocol with PocketCode's task/result contract?
- Does a share-sheet based loop deliver enough value before direct AI APIs, and can it do so while maintaining the $0 budget?
- Which features are worth maintaining as provider-specific adapters, given constant product changes?

## 12. Current research disposition

**Recommended:** add AI Workflow Director as a distinct PocketCode feature hypothesis, keep a universal manual text handoff as its foundation, add optional user-directed OS sharing and provider setup adapters, and evaluate a compact profile plus task compiler and continuation capsule against a baseline.

**Not decided or authorized:** direct API use, API keys, provider account creation, billing, paid services, live execution, installation of third-party plugins into consumer AI apps, background cross-app monitoring, public deployment, merge, or a shared RevDev/PocketCode repository.

**Known blockers:** no completed real-device test matrix for AI-app handoff; no benchmark of profile effectiveness across free consumer AI apps; no verified comparison of actual RevDev runtime/queue artifacts with PocketCode's current contract.

## Sources checked (2026-10-28)

1. Ponytail official project and skill — https://github.com/DietrichGebert/ponytail and https://github.com/DietrichGebert/ponytail/blob/main/skills/ponytail/SKILL.md
2. Ponytail self-reported benchmark — https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-10-07-agentic.md
3. Claude Code skills, hooks and memory — https://code.claude.com/docs/en/skills ; https://code.claude.com/docs/en/hooks ; https://code.claude.com/docs/en/memory
4. Anthropic Claude Code best practices — https://www.anthropic.com/research/claude-code-best-practices
5. OpenAI Codex engineering practices — https://openai.com/business/guides-and-resources/how-openai-uses-codex/
6. Superpowers cross-harness skills framework — https://github.com/obra/Superpowers
7. ChatGPT custom instructions — https://help.openai.com/en/articles/8096356-chatgpt-custom-instructions
8. Claude personalization — https://support.claude.com/en/articles/10185728-understanding-claude-s-personalization-features
9. Gemini instructions — https://support.google.com/gemini/answer/16598625
10. Apple Shortcuts/share sheet — https://support.apple.com/en-gb/guide/shortcuts/apd163eb9f95/ios ; https://support.apple.com/en-euro/guide/shortcuts/apdaf74d75a5/ios
11. Android sharing — https://developer.android.com/develop/ui/compose/sharing/send
12. Apple app sandbox — https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox
13. ChatGPT/API billing — https://help.openai.com/en/articles/9039756-managing-billing-for-chatgpt-and-the-api-platform
14. Claude/API billing — https://support.anthropic.com/en/articles/9876003-i-subscribe-to-a-paid-claude-ai-plan-why-do-i-have-to-pay-separately-for-api-usage-on-console
15. Agent2Agent protocol and MCP distinction — https://a2a-protocol.org/latest/
16. Existing PocketCode shared-core proposal — https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md
