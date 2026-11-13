# Pass 1 — Public user/problem evidence and falsification protocol

**Status:** Desk-research subpass only; no interviews, app installs, task benchmark, or representative sample.
**Prepared:** 2026-10-27
**Research owner:** ChatGPT (independent contribution; not Gemini completion)
**Budget:** $0. No provider, account, credentials, live workload, deployment, or billing change.

## Executive finding

There are credible anecdotes that some people want to learn or run small scripts on a phone, including users without a computer and users who need occasional quick tasks. There is equally material counterevidence: touch input and screen size make sustained coding unpleasant; local mobile runtimes and terminal tools already solve some use cases; browser IDEs can be awkward on phones; and some users conclude a laptop or remote desktop is better.

**Conclusion:** The existence of a problem is plausible, but frequency, severity, target segment, willingness to switch, and willingness to pay are all unverified. Do not infer market demand from Reddit votes or a handful of posts. “Code from a phone” is too broad to position as the differentiator.

The narrow hypothesis worth testing is:

> Given AI-generated Python code and a small CSV/text input on a phone, a user can obtain a genuine, bounded run result plus downloadable/inspectable output files, then paste a clear report back into any AI assistant, with less setup and less ambiguity than their current workflow.

This only matters if the test shows a meaningful advantage over free/local/remote substitutes. The report must distinguish execution facts from formatter-produced claims; the existing prototype is simulated and does not run code.

## Evidence ledger

### E1 — Recurring interest, but use cases vary
- Source: [Reddit r/Python — “Who is using mobile devices for Python, development and how?”](https://www.reddit.com/r/Python/comments/1wwxwa3/who_is_using_mobile_devices_for_python/)
- Date shown by Reddit: 2026-10-03.
- Observations: replies describe a tablet/phone running Termux and scripts that produce CSVs; another reply says they did not find a useful case; a reply describes compilation friction and falling back to a desktop.
- Interpretation: supports both possible utility for bounded tasks and a strong ceiling on broader mobile development.
- Evidence quality: self-selected anecdotes; no denominator, verification, or representative sample.

### E2 — Small tasks and occasional utility can work
- Source: [Reddit r/Python — “Programming from your phone: has anyone actually managed to do it?”](https://www.reddit.com/r/Python/comments/1gp2zw4/programming_from_your_phone_has_anyone_actually/)
- Date shown by Reddit: 2024-11-11.
- Observations: replies range from “not useful” and frustration with small screens/touch keyboards to Pythonista users running one-liners, a person making an API helper, and occasional Termux/SSH use while travelling.
- Interpretation: the most promising job may be occasional execution/verification, not writing a full project on a phone. But the posts also show that existing apps and Termux can satisfy some users.
- Evidence quality: anecdotal and dated; use to form interview questions, not estimate demand.

### E3 — No-computer learners face access and usability constraints
- Source: [Reddit r/learnpython — “Where to begin with only a phone and no money?”](https://www.reddit.com/r/learnpython/comments/1kmbhm3/where_to_begin_with_only_a_phone_and_no_money/)
- Date shown by Reddit: 2025-05-14.
- Observations: poster reports friction with mobile learning sites and paid restrictions, already has Pydroid 3, and later says a family member may provide a laptop.
- Interpretation: there may be an access/affordability segment, but educational content and a mobile coding runner are different jobs. This segment may also have very low willingness to pay.
- Evidence quality: one personal account; not evidence that a hosted runner is the best solution.

### E4 — Current learner requests continue, with local tools recommended
- Source: [Reddit r/PythonLearning — “Is there a good way to practice Python on a phone without a laptop?”](https://www.reddit.com/r/PythonLearning/comments/1whoi2f/is_there_a_good_way_to_practice_python_on_a_phone/)
- Date shown by Reddit: 2026-09-16.
- Observations: poster asks for a free phone-based Python option; a reply recommends Pydroid and suggests a low-cost laptop as more convenient.
- Interpretation: current need signals exist, but recommendations point toward local execution or obtaining a computer, not necessarily a new hosted product.
- Evidence quality: small discussion, no adoption or retention data.

### E5 — Browser IDE mobile friction is concrete, but evidence is old
- Source: [Reddit r/github — “Codespace VS Code configuration for iPhone”](https://www.reddit.com/r/github/comments/zwa27n)
- Date shown by Reddit: 2022-12-27.
- Observations: poster reports panes and controls being difficult to use on an iPhone and missing keyboard shortcuts; they still consider Codespaces one of the better options.
- Interpretation: a single-purpose mobile workflow may reduce UI burden compared with a full IDE, but this is an old post and must be retested against current tools.
- Evidence quality: one dated report; not proof of current Codespaces limitations.

### E6 — Local tools are a serious substitute
- Sources: [Reddit r/learnpython — “Best android python IDE?”](https://www.reddit.com/r/learnpython/comments/1k8swuq/best_android_python_ide/) and [Reddit r/androidapps — “Good app for coding?”](https://www.reddit.com/r/androidapps/comments/1on1964/good_app_for_coding/).
- Dates shown by Reddit: 2025.
- Observations: commenters suggest Pydroid, Termux, editors, and combinations of local tools; they mention ads, permissions concerns, setup learning, and keyboard/screen friction.
- Interpretation: any proposed hosted runner must demonstrate a clear improvement over existing local tools, not merely that those tools have imperfections.
- Evidence quality: community advice, not systematic product testing.

## Synthesis: what this evidence does and does not support

Supported as a plausible hypothesis:
- Some users occasionally need to run a small script from a phone.
- Users without a computer and users away from their workstation may have different jobs and constraints.
- Full IDE UX, touch input, setup, package support, ads/permissions, and transfer of results back to an AI are candidate pain points.

Not supported:
- How many users experience the problem or how frequently.
- Whether AI-generated code is the dominant trigger.
- Whether a hosted service beats local execution, Codespaces, SSH, or existing mobile IDEs on the same task.
- Whether users would trust uploaded code/data, accept hosted execution, or pay.
- Whether a safe service can run sustainably within the owner's strict $0 budget.
- Any claim of market size, product-market fit, or validated differentiation.

## Segment choice and counter-hypotheses

Test segment A first: **people who already use an AI assistant and have recently wanted to verify a short Python script plus small text/CSV input from a phone.** This is a sequencing choice because the task is narrow and measurable, not because the segment is proven largest.

Keep these alternatives live:
1. **Local runtime wins:** Pydroid/Pythonista/Termux already provides the fastest, cheapest, most trusted route.
2. **Remote IDE wins:** Codespaces or an existing server is acceptable and provides more capability.
3. **The pain is code authoring, not execution:** touch typing dominates; a one-click runner does not fix the actual problem.
4. **The pain is AI context transfer:** a report/attachment protocol alone may solve the issue without hosted execution.
5. **The problem is too infrequent:** users tolerate their current workaround and won't return.
6. **Security blocks adoption:** users won't upload code or data to an unfamiliar execution service.
7. **Economics block adoption:** free local alternatives and a $0 operating budget leave no viable service model.

## Zero-cost validation protocol (not yet executed)

### Step 1 — Recruit based on recent behavior, not enthusiasm
Seek 5–8 people who have actually tried to run or verify code on a phone in the last 30 days. This is an exploratory usability sample, not statistically representative. Include both iOS and Android if available; record device/OS and whether they have access to a computer. Do not count friends who merely say the idea sounds useful as validation.

Ask:
- “Tell me about the last time you tried to run code from your phone.”
- “What code and input did you have, and where did they come from?”
- “What did you do next, step by step?”
- “Where did you get stuck, if anywhere?”
- “What did you do with the output or error afterward?”
- “How often has this happened in the last month?”
- “What did you try before, and why did you keep or abandon it?”
- “What data or code would you refuse to upload to a hosted runner?”
- Only after the history questions: “What would have to improve for you to change your current method?”

Avoid leading with a product pitch or asking “Would you use this?”

### Step 2 — Fixed comparison task
Use a harmless deterministic task that reads a small CSV and emits a summary CSV plus a JSON/text report. No secrets, network calls, credentials, personal data, arbitrary packages, or production code. Give every tool the same source code and input file.

Compare, where available without paid signup:
- Current preferred local phone tool (e.g., Pydroid/Pythonista/Termux).
- Browser/cloud IDE or existing remote environment the participant already uses.
- A clickable prototype of the proposed flow, explicitly labelled **simulation** until real execution exists.

Do not imply the current prototype executed code. Do not create provider accounts or trigger workloads under the $0 gate.

### Step 3 — Record observable outcomes
For each attempt record:
- Setup steps and elapsed time to first genuine result.
- Whether the participant can identify success/failure without interpretation help.
- Whether stdout/stderr and output files are findable and correct.
- Whether the report contains enough bounded context for an AI to help with the next fix.
- Number of copy/paste or app-switch steps.
- Recovery after a deliberately introduced, harmless syntax/input error.
- User preference after completing the task, plus the reason.
- Device, OS, network conditions, tool/version, and whether the participant already knew the tool.

Keep observed behavior separate from self-reported preference.

### Step 4 — Pre-register decision rules before sessions
Do not set thresholds after seeing results. A proposed exploratory rule (owner may revise before testing):
- **Continue investigating** only if at least 4 of 6 participants independently describe a recent repeatable problem, and at least 3 of 6 complete the same task with materially fewer setup/app-switch steps or more useful error/report handoff than their current method.
- **Re-scope** if the primary pain is authoring/keyboard ergonomics or learning guidance rather than execution and evidence.
- **Stop/pivot** if most participants complete the task faster with a free local tool, already have an acceptable remote workflow, or cannot name a recent real instance.
- Any positive signal only justifies the next research step; it does not validate market size, willingness to pay, safety, or launch readiness.

These are proposed screening thresholds for a tiny exploratory sample, not statistical claims. Freeze them before data collection.

### Step 5 — Evidence and privacy hygiene
- Ask permission before recording notes; do not collect names or sensitive code/data.
- Use synthetic CSV and deterministic code.
- Do not upload participant code to any provider.
- No live execution provider test, account creation, or spending without explicit owner approval and a reviewed hard cost ceiling.
- No deployment, merge, or production claim as part of validation.

## Current product implication

Keep the MVP proposal at hypothesis stage: a mobile-friendly, single-purpose run → genuine bounded evidence/files → report-to-any-AI handoff flow. Avoid building native apps, remote-agent orchestration, Tailscale/SSH control plane, overlays, or multi-language support until user evidence proves these are required. First establish that the narrow task is frequent, painful, and underserved by existing tools.

## Sources and date notes

All sources above are public Reddit discussions; pages were discovered/reviewed on 2026-10-27. Dates shown are the posts' dates, not the date of a systematic study. Votes/comments are not representative statistics. Official competitor/provider claims remain separately documented in [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md) and [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md).
