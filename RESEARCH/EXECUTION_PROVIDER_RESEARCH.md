# Code Execution Backend Research

**Research snapshot:** 2026-10-20  
**Status:** Desk research only. No vendor selected. Prices and service terms change; recheck official documentation before implementation or spending money.

## Decision context

PocketCode may need to execute user-submitted code remotely so the same workflow works from iPhone and Android without requiring a personal computer or server. This introduces a serious trust boundary: user code must not run inside the main application process or gain access to application secrets.

The backend must be evaluated on isolation model, network policy, lifecycle/cleanup, output streaming, file handling, supported operating systems, cold-start latency, resource limits, regional availability, retention, API maturity, and total cost. A vendor's use of the word “sandbox” is not sufficient evidence by itself.

## Candidate options

### E2B

Official source: https://e2b.dev/

- Offers hosted sandbox infrastructure for AI agents and code execution.
- The official site describes a microVM-oriented open-source runtime and usage-based billing.
- At the research snapshot, the public pricing page advertised a free Hobby tier with a one-time usage credit, while Pro had a monthly base price plus usage costs.
- Potential fit: a purpose-built sandbox API and a familiar developer workflow.
- Must verify: current plans, actual execution/file/streaming APIs, time limits, region/data handling, network controls, free-tier restrictions, and total cost at expected use.

### Modal Sandboxes

Official sources:
- https://modal.com/products/sandboxes
- https://modal.com/docs/sdk/js/latest/Sandbox

- Provides disposable sandboxes, process execution, stdout/stderr streams, filesystem access, configurable CPU/memory, and egress controls.
- Official pricing is usage-based; the product page showed a monthly amount of included compute at the time of research.
- Potential fit: flexible execution environments and programmatic control.
- Must verify: account requirements, minimum charges, lifecycle billing, cold-start distribution, supported runtime images, quotas, region/data handling, and whether the operations model is appropriate for a small consumer product.

### Daytona Sandboxes

Official sources:
- https://www.daytona.io/docs/en/sandboxes/
- https://www.daytona.io/pricing
- https://www.daytona.io/docs/billing

- Provides programmatically managed execution environments. Official documentation describes Linux container sandboxes and additional VM-based options, including Windows and macOS environments for applicable workloads.
- The public pricing page showed pay-as-you-go resource pricing and a free compute allowance at the time of research.
- Potential fit: persistent or disposable environments, file operations, and multiple OS/runtime options.
- Must verify: the exact isolation tier for untrusted public submissions, billed lifecycle states, storage charges, idle behavior, network policy, account limits, and costs for short executions.

### Cloudflare Sandboxes / Workers

Official sources:
- https://developers.cloudflare.com/sandbox/
- https://developers.cloudflare.com/sandbox/concepts/
- https://developers.cloudflare.com/sandbox/concepts/security/

- Cloudflare documents container and Dynamic Worker sandbox options for generated or untrusted code, with the application controlling what data and network access the code receives.
- The documentation states that the sandbox feature is available on a Workers Paid plan at the time of research.
- Potential fit: integration with a web application and edge-oriented request handling.
- Must verify: current feature maturity, platform constraints, supported process/filesystem behavior, isolation guarantees for the exact workload, outbound network defaults, plan costs, execution duration, and whether the container option fits arbitrary Python scripts.

### Judge0 CE

Official source: https://ce.judge0.com/docs

- API-oriented code execution service with support for many languages, multi-file submissions, time/memory limits, and detailed execution results.
- Documentation describes hosted API access and self-hosting options; the open-source edition is GPL-3.0 licensed.
- Potential fit: a fast way to prototype a narrow code-runner API without building a language-execution protocol from scratch.
- Must verify: hosted provider's current plans, queues/rate limits, file and output behavior, package installation limitations, retention, and the security model of the specific hosted/self-hosted deployment.
- Important caveat: self-hosting shifts patching, operations, isolation review, and abuse prevention to us.

### Piston

Official source: https://github.com/sanmayc1/Piston

- Open-source code execution engine with an HTTP API and language runtime support.
- Its README describes Linux isolation and resource controls such as execution-time and output limits, with network access disabled by default in the documented setup.
- Potential fit: evaluating an open-source engine for a controlled, self-hosted prototype.
- Must verify: maintenance status, supported language versions, deployment requirements, isolation review, API limits, and whether a managed production service is available on suitable terms.
- Important caveat: using an engine is not the same as having a secure, operated public service. Deployment and threat-model responsibilities remain.

## Comparison summary

| Candidate | Strongest apparent reason to investigate | Main unknown / cost risk | Current recommendation |
|---|---|---|---|
| E2B | Purpose-built hosted microVM sandbox workflow | Pricing tiers, API fit, data/region controls | Shortlist for API proof |
| Modal | Flexible disposable environments and output streams | Billing model and operations complexity | Shortlist for API proof |
| Daytona | Environment flexibility, including VM options | Isolation tier and resource lifecycle billing | Shortlist if persistent environments/Windows matter |
| Cloudflare | Tight fit with a web app architecture | Feature constraints and paid-plan/runtime fit | Shortlist if choosing Cloudflare for the app |
| Judge0 CE | Language-runner API and broad language catalog | Hosted service constraints or self-hosting burden | Prototype alternative for short, bounded submissions |
| Piston | Open-source engine and documented resource controls | Self-hosting and production hardening | Research only until operations/security are assessed |

## Proposed evaluation proof

Do not choose from marketing pages alone. For the top two candidates, run the same small test suite with no production user data:

1. Execute a successful Python program and capture stdout, stderr, exit status, and duration.
2. Execute a syntax error and a runtime exception.
3. Run a program that exceeds the configured timeout.
4. Test cancellation and worker termination.
5. Create and retrieve a small output file.
6. Test multi-file input.
7. Confirm output-size and memory limits.
8. Confirm the job cannot read application environment variables or other jobs' files.
9. Verify network restrictions and cleanup.
10. Measure cold-start and repeat-run latency.
11. Estimate cost for representative short jobs, including idle time and storage.
12. Review data processing terms, retention, regions, and account limits.

## Current conclusion

No provider has been selected. First narrow the product workflow and required execution contract, then run a controlled technical comparison. Do not enter API keys, upload private user projects, or incur paid usage during initial research without explicit owner approval.
