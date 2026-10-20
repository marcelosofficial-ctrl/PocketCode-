# Competitor and Alternative Research

**Status:** Initial desk research, not a complete or independently verified market study.  
**Research snapshot:** 2026-10-20  
**Purpose:** Avoid assuming that coding on a phone with AI is a unique idea.

## Initial landscape

| Product / alternative | Positioning observed in initial research | Why it matters | Questions to verify |
|---|---|---|---|
| Pocket Code | Android coding environment with multiple language/runtime and AI-related features | Existing product with a very similar name; potential naming confusion | Current runtime support, audience, maintenance, name/trademark risk |
| Derle | Phone-based IDE marketed with terminal, Git, preview, and AI assistance; iOS and Android advertised | Direct overlap with mobile IDE positioning | Execution architecture, languages, pricing, limitations |
| Kodo | iPhone/iPad code editor with AI and remote-development-related features | Relevant iOS-first alternative | Whether each workflow executes locally, remotely, or via SSH |
| Rish | Experimental open-source mobile workspace and multi-provider AI integrations | Open-source and provider-flexibility reference | Maturity, supported platforms, security, activity |
| Paseo | Open-source/mobile-oriented coding and AI workflow | Alternative architecture and UX reference | Maintenance, runtimes, setup burden |
| Pockode | Mobile-oriented coding tool | Similar user need and naming proximity | Platform, runtime, persistence, pricing, active status |
| Codeg | Mobile coding/AI development workflow | Relevant workflow alternative | Execution and export capabilities |
| AndCode | Android local AI coding-agent project | Local execution and agent workflow reference | Scope, runtime limits, maintenance, security, device requirements |
| Replit | Hosted development environment with collaboration and AI features | Strong hosted IDE alternative | Phone usability and cost for target workflow |
| GitHub Codespaces | Hosted development environments tied to GitHub repositories | Existing way to code without owning a PC | Mobile UX, setup complexity, usage cost, beginner accessibility |
| SSH to a server / cloud VM | Flexible remote development approach | Powerful existing substitute for technical users | Setup burden and audience suitability |

## Initial strategic interpretation

A generic “run code on a phone” or “mobile IDE with AI” message is crowded. A potentially sharper hypothesis is an execution-and-verification loop that works with code from any AI provider:

1. Run code in a suitable isolated environment.
2. Show actual stdout, stderr, exit status, generated files, runtime details, and relevant limits.
3. Produce a compact report the user can send to any AI assistant.
4. Review proposed edits and rerun to verify whether the issue was fixed.

This is only a hypothesis. Existing products may already provide parts or all of this workflow. The next research pass must compare concrete user journeys rather than marketing claims.

## Public references from the initial pass

- Pocket Code: https://www.pocketcodeapp.com/en
- Derle: https://derle.app/
- Kodo: https://apps.apple.com/us/app/kodo-ai-code-editor-ide/id6781042920
- Rish: https://github.com/ZSeven-W/rish-app
- Paseo: https://git.mitgai.net/getpaseo/paseo
- Pockode: https://pockode.com/
- Codeg: https://docs.codeg.app/
- AndCode: https://github.com/yuga-hashimoto/and-code
- Replit: https://replit.com/
- GitHub Codespaces: https://github.com/features/codespaces

Links and product claims must be rechecked before decisions. This is not a feature-by-feature audit, and the existence of a product does not prove it is a direct substitute for every proposed feature.

## Next research actions

- [ ] Inspect each product's current official documentation, pricing, and platform availability.
- [ ] Build a workflow-level matrix: edit, execute, files, dependencies, networking, logs, Git, AI handoff, export, isolation, limits, price.
- [ ] Distinguish local execution, SSH/remote execution, and provider-hosted sandbox execution.
- [ ] Check whether the proposed evidence/report/fix/rerun workflow is genuinely missing.
- [ ] Validate PocketCode name for product collisions, trademark risk, and domain/social availability.
- [ ] Interview target users and test alternatives with realistic tasks.
