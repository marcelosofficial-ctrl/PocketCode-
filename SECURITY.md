# PocketCode Safety Requirements

This is a planning checklist, not a certification or claim that any implementation is secure.

## Design assumptions

Programs submitted by users can behave unexpectedly and may attempt to access resources beyond their intended task. The execution environment must be designed to contain failures and limit resource use.

## Requirements before accepting public user programs

- Run programs in a purpose-built, disposable execution environment, separate from the web application.
- Review the isolation guarantees of the chosen service and underlying technology.
- Use an unprivileged identity and avoid host mounts or elevated permissions.
- Enforce server-side time, CPU, memory, process, disk, output-size, concurrency, and per-user limits.
- Restrict outbound network access by default, and prevent access to internal services and cloud metadata endpoints.
- Allow only approved runtime and environment settings. Do not let clients specify arbitrary host configuration.
- Keep application credentials separate from the program environment.
- Authorize every read and write of projects, runs, and results.
- Limit upload sizes and validate archive paths before extraction.
- Define retention and deletion rules for source files, logs, and generated artifacts.
- Redact credentials and sensitive patterns from logs and copied reports.
- Keep dependencies patched and use versioned runtime images.
- Record operational events while minimizing unnecessary collection of source code and personal data.

## Dependencies

Installing packages adds security, reliability, and cost risks. Begin with a constrained package strategy. If package installation is supported, enforce limits and use controlled registries or network policies where practical. Do not promise that every package will work.

## Reporting

Do not publish credentials, private user data, or sensitive vulnerability details in public issues. Establish a private reporting path before launch.

## Launch gate

Do not expose a public code execution service until isolation, quotas, cleanup, network policy, access controls, monitoring, and operational response have been reviewed and tested.
