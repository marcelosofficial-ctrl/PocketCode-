# Mobile Technical Tasks: Product Opportunity Map

**Status:** Discovery proposal; not a promise of implemented capability  
**Budget:** $0 unless the owner explicitly changes it  
**Relationship to RevDev:** Design the concepts so a future shared PC/phone product remains possible. Keep repositories separate for now.

## Problem statement

An AI assistant may tell a person to run code, inspect a file, transform data, or perform a computer-oriented task while the person only has a phone. The user then has to find an awkward workaround, explain their device constraints to the AI, or postpone the task. PocketCode should explore which of these jobs it can perform safely and reliably on a phone.

The airport Python/polaroid workflow and the AI assuming the user was on a PC are owner-reported examples. They are useful discovery signals, not evidence of how often this happens across users.

## Opportunity map

Rankings are hypotheses to investigate, not a committed roadmap.

| Opportunity | Example phone task | Potential value | Main constraint | Early priority |
|---|---|---|---|---|
| Run an AI-generated script | Run Python that transforms photos or processes CSV/JSON | Directly addresses the core problem | Secure runtime, files, dependencies, execution cost | First |
| File conversion and batch processing | Convert images, rename files, resize photos, transform CSV/JSON/text | Clear input → output workflow; useful without a PC | File-size limits, formats, privacy, output downloads | High, after runtime proof |
| Diagnose and verify code | Capture actual errors, exit status, logs, generated files; copy report to AI | Makes the AI iteration loop concrete | Report must be trustworthy and bounded | First-class core |
| Validate structured data | Check JSON/CSV, compare records, summarize validation failures | Often lighter than a full application | File size, sensitive data, clear validation rules | Candidate for an early low-risk workflow |
| Run tests or small checks | Execute a script's test suite or a provided validation command | Useful for AI-generated project changes | Multi-file projects, dependencies, runtime limits | Later |
| Generate downloadable artifacts | Produce a report, transformed data file, or simple document | Gives a tangible result on the phone | File handling and format support | High if safe and bounded |
| Work with multiple project files | Upload source and inputs, run code with relative paths | Handles realistic small tasks | Directory layout, path safety, storage lifecycle | After single-script proof |
| Remote computer / shell tasks | Run commands on a PC or remote environment | Could help when a task genuinely needs desktop software | Remote access, credentials, consent, high security complexity | Not first MVP |
| GUI automation or controlling a PC | Have AI operate desktop applications remotely | Broad potential capability | Device permissions, remote-control risk, platform restrictions | Explicitly out of initial scope |
| Install arbitrary packages or use open internet | AI asks script to fetch/install dependencies | Expands compatibility | Supply-chain risk, egress abuse, cost, reproducibility | Deny by default; evaluate narrowly |
| Direct AI integrations | Send reports or scripts directly between PocketCode and AI apps | Fewer copy/paste steps | API access, account linking, provider policies, maintenance/cost | Not required for MVP |

## Initial target workflow

Start with one small, repeatable workflow that can be tested without buying services:

1. User receives a Python script from an AI assistant.
2. User pastes the script and adds a small synthetic input file.
3. PocketCode clearly shows the supported runtime and restrictions.
4. User runs it in a controlled environment.
5. PocketCode shows actual status, stdout/stderr, exit code and duration when available, and generated files.
6. One Copy result action copies a plain-text diagnostic report.
7. User pastes that report into any AI assistant, applies a correction, and reruns.

File conversion or structured-data validation may be a useful concrete demonstration, but do not implement several features at once. First prove truthful execution and the report loop.

## Device awareness and AI discovery

PocketCode cannot assume that external AI assistants automatically know it exists or will recommend it. Model knowledge, search results, app catalogs, assistant instructions, and integrations are different discovery channels; there is no guaranteed way to cause a model to recommend a new app.

Low-cost discoverability work, when the product has real capabilities:
- Publish a clear public description of what the app can and cannot execute.
- Provide task-oriented examples and a short setup guide.
- Explain the workflow in plain text that users can share with an assistant.
- Make the supported-runtime list, file limits, privacy behavior, and security model easy to find.
- Investigate relevant app listings and official integration mechanisms only when those channels are actually available.
- Never claim an assistant integration or recommendation exists unless it has been implemented and verified.

A future capability page could give users a prompt like: “I only have my phone. I can use PocketCode to run supported scripts and send you the real result report. Give me a script and the input files needed, and tell me exactly what to paste into PocketCode.” This is a user-mediated workflow, not an automatic integration or a guarantee that the AI already knows PocketCode.

## Safety boundaries

- Treat all submitted code and files as untrusted.
- Never run untrusted code on the app server or developer workstation as a cost-saving shortcut.
- Do not pass service credentials or secrets into user code.
- Default-deny outbound network access.
- Enforce server-side time, CPU, memory, process, output, and storage limits.
- Make timeout, cancellation, infrastructure failure, and program errors distinguishable.
- Use synthetic examples for early tests; do not upload private photos or sensitive files to unverified infrastructure.
- Do not create provider accounts or run potentially billable workloads without explicit owner approval and a verified zero-cost path.
- Remote PC control, arbitrary shell access, and background device automation are out of scope until separately threat-modeled and approved.

## Long-term PC + phone convergence

The durable shared layer should be the execution request, lifecycle, result schema, verdict rules, file semantics, and copyable report. Phone and PC clients can present those capabilities differently. User accounts, cloud history, project synchronization, and a unified app may eventually be useful, but they add hosting, storage, privacy, authentication, and operating-cost commitments. Keep them as future decisions until there is evidence of need and a sustainable zero-cost or explicitly approved funding path.

## No-cost next steps

1. Compare RevDev's real result block and run semantics with PocketCode's proposed report.
2. Choose one realistic but small script task and write its acceptance criteria.
3. Refine the static phone prototype to one primary Run action and one obvious Copy result action; keep simulated output labeled.
4. Add provider-independent report/verdict tests before any runtime integration.
5. Use public firsthand user reports and existing-tool comparisons to identify gaps; treat anecdotes as qualitative signals, not proof of demand.
6. Gate all real execution behind documented isolation, network restrictions, cleanup, and zero-cost verification.

## Success criteria for the first useful proof

- A novice can identify where to paste code and which files to add without explanation.
- The app never labels a simulated result as a real run.
- Real execution evidence is returned accurately and bounded.
- The copied report is understandable when pasted into a different AI assistant.
- Program failure is distinguishable from timeout and platform failure.
- The workflow can be tested without mandatory paid AI integration.
- No private file or secret is silently included in the copied report.
