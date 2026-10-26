# Pass 1 — Competitor and substitute refresh

**Research ID:** PC-PASS1-2026-10-26-COMPETITORS-01  
**Checked:** 2026-10-26  
**Scope:** Current official product pages for mobile IDEs, remote-agent clients, and cloud IDE substitutes. This is a bounded workstream B subpass, not a complete market study.  
**Budget:** $0; public pages only.

## Executive finding

The core idea is **not** differentiated by “coding from a phone,” “running code on a phone,” “AI-assisted editing,” or “using a phone to supervise a remote coding agent.” Current official pages describe multiple products already covering those jobs.

The most material findings:

1. **Exact-name collision:** [PocketCode](https://www.pocketcodeapp.com/en) is an existing one-word Android IDE with on-device runtimes, terminal/SSH, Git, API/database tools, multi-provider AI BYOK, and a free tier. Its own FAQ explicitly distinguishes itself from Catrobat's two-word “Pocket Code.” The current PocketCode project name is a high-priority branding/discoverability risk, not a cleared name.
2. **Direct phone-native competition:** [Derle](https://derle.app/) currently markets an IDE for Android and iPhone with local execution, a Linux terminal, Git, live previews, and an assistant that edits/runs commands with user approval. This directly challenges a broad “AI coding from your phone without a laptop” claim.
3. **iOS offline/remote alternative:** [Kodo](https://www.kodoeditor.com/) is free for iPhone/iPad, supports local HTML/CSS/JS previews, on-device AI, GitHub/SQLite, and SSH/SFTP/FTP; its current page says it does not run Python/PHP/Swift locally, directing those workloads to a user-owned server.
4. **Remote-agent alternative:** [Codeg](https://docs.codeg.app/getting-started/installation) has iOS/Android clients, but agents/files/sessions stay on a desktop or server the user controls. The current mobile apps are described as test releases, with iOS 26+ and Android 12+ requirements.
5. **Hosted substitute:** [GitHub Codespaces](https://github.com/features/codespaces) offers browser-based cloud development from any internet-connected device. Personal accounts have included monthly quotas (120 compute hours and 15 GB-month storage on Free; 180 hours and 20 GB-month on Pro), after which use is blocked if there is no valid payment method or billed if one is set.

These are official product claims, not independent hands-on tests. This pass did not install apps, create accounts, compare the same task in each product, or validate customer demand.

## Product-by-product evidence

| Product | What the current official page says | Direct overlap | Potential gap for PocketCode to test | Confidence / caveat |
|---|---|---|---|---|
| PocketCode (one word) | Android 9+, 64-bit; on-device Node/Python/Ruby/PHP/Java/Kotlin and other tools; terminal/SSH, Git, database/API tools, multi-provider AI BYOK; free tier, Pro advertised at $6.99/month | Very high: mobile coding, local execution, AI choice, terminal, files | Cross-platform iOS/Android parity, no-install disposable environment, repeatable runtime, safe isolation, bounded execution report | High confidence in what its own current site claims; no hands-on verification. Name risk is critical |
| Derle | Markets Android and iPhone apps; on-device Linux/toolchains, terminal, Git, previews, AI assistant, command approvals and restore points; free tier plus optional Pro | Very high: local coding/run/debug and agentic editing from phone | A hosted cross-device runtime that avoids local storage/OS/toolchain constraints; task-specific execution evidence | High confidence in marketing claims; underlying runtime/security not independently tested |
| Kodo | iPhone/iPad editor, offline local files and HTML/CSS/JS preview, optional on-device AI, SSH/SFTP/FTP, GitHub/SQLite; does not locally run Python/PHP/Swift | Medium/high for iOS editing, AI, and remote execution | Simple Python/file execution without setting up or maintaining a server | High confidence in stated feature scope; no app install/test |
| Codeg | Native iOS/Android clients connect to Codeg desktop/server; host owns project files, agents, and sessions; current mobile apps described as test releases | High for supervising remote coding agents | No user-owned host prerequisite; simple one-shot run/report loop rather than long-lived agent session | High confidence in documented architecture; availability/stability may change |
| GitHub Codespaces | Cloud development environment accessible from any internet-connected device; repo/devcontainer workflow; personal monthly included compute/storage quotas; paid use after quota when payment method is configured | High for “work without your PC” and cloud runtime | Faster/no-setup task-specific UX, minimal project setup, explicit safe run states and AI-neutral report handoff | High confidence in official product/billing docs; phone usability not independently tested |

## Falsifiable differentiation hypothesis

A defensible hypothesis is **not** “PocketCode lets you code on your phone.” Existing products already claim that.

A more specific hypothesis to test is:

> For a person who has code from an AI assistant but does not want to install an IDE, configure a server, or open a full cloud development environment, PocketCode makes one supported run unusually simple: paste code/add small inputs, execute in a disposable documented environment, inspect trustworthy bounded evidence, and paste that report back into any AI assistant.

This hypothesis still needs falsification against:
- a one-task workflow in GitHub Codespaces;
- local execution in PocketCode and Derle;
- Kodo plus a user-owned SSH server;
- Codeg or another remote-agent client;
- a manual browser/terminal/copy-paste workflow.

If the task can be completed just as quickly with a free existing tool, or if target users need a full persistent IDE rather than one-shot runs, the current narrow product may not justify a separate hosted service.

## High-priority risks

- **Name:** do not invest in branding, domain, logo, or launch materials until distinct naming options and formal trademark/domain checks are reviewed.
- **Differentiation:** local phone IDEs already execute real code and offer AI; hosted cloud IDEs already remove the need for a local PC.
- **Economics:** local competitors avoid a per-run hosted compute bill. A hosted runner needs a specific convenience/safety/reproducibility advantage large enough to justify ongoing cost and abuse controls.
- **Scope:** do not respond by adding every competitor feature. Keep the first proof narrow and validate one job.
- **Security claims:** competitor product claims do not establish their or PocketCode's actual security properties; no live testing was done.

## Sources checked 2026-10-26

- [PocketCode official site](https://www.pocketcodeapp.com/en) and [About](https://www.pocketcodeapp.com/en/about)
- [Derle official site](https://derle.app/)
- [Kodo official site](https://www.kodoeditor.com/)
- [Codeg mobile installation docs](https://docs.codeg.app/getting-started/installation) and [architecture](https://docs.codeg.app/reference/architecture)
- [GitHub Codespaces product page](https://github.com/features/codespaces)
- [GitHub Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)

## Next research step

Complete a task-based comparison with one fixed task, for example “run a 20-line Python script that reads a small CSV and produces a summary file.” Record setup steps, time-to-first-run, input/output handling, error visibility, AI handoff, mobile friction, runtime reproducibility, cost/limits, and security claims. Use public docs/screenshots first; do not create accounts or run workloads without explicit approval.
