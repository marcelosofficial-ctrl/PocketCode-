# Phone-Only Competitor Scan Addendum — 2026-10-28

**Status:** Dated public-source scan; not a hands-on benchmark, market-size study, legal review, or approved product decision.  
**Purpose:** Refresh only the material new alternatives found after the existing competitor research, without duplicating or overwriting the broader analysis on PR #3.  
**Authority:** Existing [PR #3 competitor research](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/AI_COLLAB/PASS1_COMPETITOR_RESEARCH.md), [main competitor matrix](../RESEARCH/COMPETITOR_MATRIX.md), and [mobile-coding user evidence](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md) remain the broader sources.

## Executive conclusion

The landscape is moving beyond “write code in a mobile editor.” Current public project pages describe local Android coding agents, local Linux toolchains, and phone clients that steer coding agents on a different computer. This makes a broad promise like “AI coding on your phone, no PC” less defensible on its own.

This scan suggests a sharper hypothesis to test: **make one supported execution task unusually clear and trustworthy—small input, constrained run, real outcome and artifact evidence, and a copyable report that can be used by any AI assistant—without asking users to configure a full IDE, maintain a remote host, or trust a simulated result.** That is still a hypothesis, and existing tools may already satisfy the job.

## Newly surfaced adjacent projects

| Alternative | What its own public page says (not independently verified) | Why it matters to PocketCode | Key distinction to test |
|---|---|---|---|
| [AndroidHarness](https://github.com/Sanuu7/AndroidHarness) | Native Android coding agent with project file access, Linux shell/toolchain, Git, Python/Node, browser/tools, and no-PC positioning. | Directly challenges an Android-first “agent works on the phone” concept. | Does a short run/report task require the wider agent workspace, or is a narrower mobile workflow materially easier and safer? |
| [PhoneCode](https://github.com/dttdrv/phonecode) | Native Android coding agent/local development workspace; its README describes per-project workspaces, local Git and Alpine/Linux runtime, model-provider choices, and explicit file/tool controls. It also describes runtime/platform release gates. | Another direct local-first substitute, with particular focus on device-local processing and avoiding a general-purpose hosted backend. | Is there a meaningful user need for a disposable remote run, cross-platform workflow, or standardized execution receipt rather than local tool execution? Check current release/platform availability before any comparison. |
| [Atlan](https://github.com/Atlansdaddy/atlan) | Phone-oriented development cockpit using Termux/proot on Android; offers editor, terminal, agent orchestration, deterministic checks, and a cloud-client mode for a hosted server. Its README explicitly notes host/platform and sandbox limitations. | Shows that power-user Android workflows and full coding-agent cockpits are already being explored. | Is the target user a power user willing to configure Termux, or someone who wants a small task flow without setting up a workstation? Don't promise stronger isolation than is actually demonstrated. |
| [Pairlet](https://github.com/heypandax/pairlet) | Open-source phone/tablet/desktop client for steering coding agents that remain on the user's computer; the published FAQ says the host computer and daemon must stay running and notes that the custom secure channel has not had an independent audit. | Demonstrates a credible phone-as-controller route when a PC exists. | Does PocketCode's phone-only case persist when the user has no reachable host, or is remote-PC access enough for the target user? |
| [PocketCode (one word)](https://www.pocketcodeapp.com/en/about) | Existing Android IDE markets on-device runtimes, terminal/SSH, Git, and multiple AI-provider options. Its official pages explicitly distinguish it from Catrobat's two-word “Pocket Code.” | High naming, discoverability, and differentiation risk for this project's provisional name. This is not a legal conclusion. | Review distinct naming options before domain, brand, or launch investment; do not rename the repository as part of this research pass. |

**Evidence class:** primary-source self-description. These pages can establish what maintainers claim, but not comparative usability, real-world security, user demand, or PocketCode's relative performance. No app was installed or executed as part of this scan.

## Implications

1. **Do not compete on breadth.** A list of languages, agents, terminal features, MCP connectors, or models is easy to match and expands risk. The present project is not yet ready to compete as a full mobile IDE.
2. **Choose a task, not an audience slogan.** “People who code on phones” is too broad. A user may be an offline learner, Android power user, travelling developer, iPhone-only user, or person with a remote PC; these needs are not equivalent.
3. **Make execution evidence the differentiator to test.** Show exactly what ran, what did not run, the status/exit evidence, bounded output, generated-file metadata, and any cleanup/evidence uncertainty. Do not collapse a successful process exit into overall job PASS if mandatory evidence is missing.
4. **Compare local, remote-PC, and hosted paths fairly.** Local execution may be faster/private/free; remote-PC workflows may reuse existing setup; hosted disposable runs may reduce setup but bring latency, data-transfer concerns, ongoing cost, and sandbox obligations.
5. **Keep the Director subordinate.** Compact prompts and continuity capsules may reduce repeated work but do not validate the core execution problem and do not create a product moat by themselves.
6. **Keep the product name provisional.** The existing same-spelling Android IDE makes name collision a concrete discovery/distribution risk; formal trademark/domain clearance remains unperformed.

## Fixed-task comparison to use in later research

Use one synthetic, small task across alternatives where practical, such as: *accept a tiny CSV input, run a short Python transformation that produces a summary file, surface a known syntax/runtime failure, and produce a report a user can paste into a separate AI chat.*

Record, without guessing:

- Setup prerequisites and steps, first-run friction, and whether a PC or account is needed.
- Where code and inputs execute or persist (device, user's PC, or provider environment).
- Whether the task genuinely runs and outputs can be retrieved; distinguish documentation claims, screenshots, and observed evidence.
- How success, program error, timeout/cancel, infrastructure failure, output truncation, and missing evidence are represented.
- How the user transfers a report back to an AI, and whether the report preserves enough context for the next correction.
- Supported platform, file/runtime limits, privacy/retention claims, network constraints, setup time, cost terms, and known caveats.
- What the competitor does better. A fair study must capture counter-evidence, not only gaps.

Do not create accounts, run live provider workloads, submit private data, install software, pay, or launch deployments for this desk-research task. If a firsthand test is not feasible on the phone under the current limits, record it as **NOT RUN** and use only sourced statements.

## Next action

Use this addendum with the existing PR #3 competitor research; do not rewrite or duplicate that document. The next research pass should compare source-dated facts and then fill a [problem hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) with one candidate job, strongest alternative explanations, and decision criteria. No market validation has occurred.
