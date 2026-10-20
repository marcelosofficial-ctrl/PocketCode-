# PocketCode

**Vibe code. Run it. Fix it. From your phone.**

PocketCode is an early-stage project exploring a mobile-first workspace for people who use AI to create code and want to test and improve it without always having access to a computer.

## The idea

AI can generate code, but generated code still needs to be run, inspected, and corrected. PocketCode is exploring a provider-neutral workflow that helps people:

1. Bring code and project files into a phone-friendly workspace.
2. Run supported code in an appropriate isolated environment.
3. Inspect actual output, errors, exit status, and generated files.
4. Share execution evidence with the AI assistant of their choice.
5. Review changes and rerun to check whether they worked.

This is a product hypothesis, not a claim that these capabilities are already implemented or unique to PocketCode. Our working marketing angle is vibe coding from your phone; the product proof we need is reliable, real execution and debugging.

## Current status

**Discovery and product definition.** No production runtime, cloud provider, framework, pricing model, or supported-language commitment has been finalized.

The initial MVP candidate is a mobile-first web app with one remote runtime and a clear, verifiable run-and-inspect workflow. The scope will be narrowed through competitor research, user feedback, and technical testing.

## Project documents

- [Project status](PROJECT_STATUS.md)
- [Product specification](PRODUCT_SPEC.md)
- [First-run workflow](PRODUCT/FIRST_RUN_WORKFLOW.md)
- [Roadmap](ROADMAP.md)
- [Architecture proposal](ARCHITECTURE.md)
- [Safety requirements](SECURITY.md)
- [Decision log](DECISIONS.md)
- [Cross-agent contributor instructions](AGENTS.md)
- [Marketing and positioning hypothesis](MARKETING/POSITIONING_HYPOTHESIS.md)
- [Initial competitor research](RESEARCH/COMPETITOR_MATRIX.md)
- [Competitive analysis and positioning hypotheses](RESEARCH/COMPETITIVE_ANALYSIS.md)
- [Code execution backend research](RESEARCH/EXECUTION_PROVIDER_RESEARCH.md)

## Principles

- Mobile-first, with no assumption that the user has a PC nearby.
- Provider-neutral, with no mandatory AI subscription or vendor lock-in.
- Honest about which runtimes and features are actually supported.
- Execution evidence over unverified success claims.
- User code and files must be handled with security, privacy, and resource limits in mind.
- Code, projects, and results should remain exportable.

## Contributing and AI collaboration

Read [AGENTS.md](AGENTS.md) before proposing or making changes. Claude-specific and Gemini-specific entry instructions are provided in [CLAUDE.md](CLAUDE.md) and [GEMINI.md](GEMINI.md).

The repository is public. Do not commit API keys, credentials, private user data, or production secrets.

## Naming

PocketCode is a provisional project name. Naming, product collisions, trademark risk, and domain availability have not yet been fully reviewed.
