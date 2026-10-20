# PocketCode User Validation Script

**Status:** Ready to use; no interviews have been conducted.  
**Time:** 10–15 minutes  
**Goal:** Learn whether people have a recurring problem testing AI-generated code from a phone before investing in a backend.  
**Privacy:** Ask about the task, not sensitive code or account details. Do not record names, contact details, private project content, or credentials unless a separate consent-based research process is approved.

## Copy/paste invitation

Use this short message to recruit people without pitching the product or biasing their answers:

> Hey! I’m exploring a small idea for people who use AI to write code, especially when they only have a phone handy. I’m not selling anything—I’d just like to hear about the last time you tried to test AI-generated code and what happened. It would take about 10 minutes. Totally fine if you haven’t run into this problem.

Send it only to people you already have an appropriate way to contact. Do not add people to mailing lists or collect contact details in the research notes.

## Phone-friendly way to run a session

1. Ask the recent-behavior questions before sharing the prototype.
2. Keep the session to 10–15 minutes; skip questions already answered naturally.
3. Take short, non-identifying notes in the template below, or write them immediately after the call.
4. Mark direct observations separately from your interpretation.
5. End by asking for one specific task they might try later, not a vague promise to use the app.
6. After each conversation, note one thing that supports the idea and one thing that challenges it.

## Who to talk to

Start with 5–8 people who have personally tried to generate code with an AI assistant and then test it on a phone or without convenient access to a computer. Keep beginners and experienced developers distinguishable in notes; their needs may differ.

Do not pitch PocketCode before the first questions. Prefer a recent real experience over hypothetical enthusiasm.

## Interview flow

### 1. Recent behavior (3 minutes)

1. “Tell me about the last time you used an AI assistant to create or change code.”
2. “What were you trying to make the code do?”
3. “Where were you when you tried to test it, and what device did you have available?”
4. “What did you do next, step by step?”
5. “Where did you get stuck, if anywhere?”

**Follow-up prompts only when needed:** What tool did you use? Did you get real output or just an explanation? Did you need files or packages? How long did setup take?

### 2. Workaround and impact (3 minutes)

6. “How did you eventually get it working—or decide to stop?”
7. “What was the most frustrating part?”
8. “How often has something similar happened in the last month?”
9. “What did the problem cost you: time, a blocked task, lost work, or nothing important?”
10. “Have you tried another app or service for this? What made you keep or abandon it?”

Ask for observable behavior, not whether the person thinks the idea sounds good.

### 3. Test the proposed workflow (3 minutes)

Only after hearing their story, show the simulated mobile prototype and clearly say that it currently demonstrates the interface only; it does not execute code.

11. “What do you think this tool does?”
12. “Which part, if any, would have helped with the example you just described?”
13. “What would you expect to happen when you tap the run button?”
14. “What would make you trust—or distrust—the result?”
15. “What would be missing before you could use it for a real task?”

Do not count confusion about simulated output as demand for real execution; separate interface feedback from problem validation.

### 4. Alternatives and commitment (2–4 minutes)

16. “If this tool did not exist, what would you use next time?”
17. “What would need to be easier than your current workaround for you to switch?”
18. “When do you expect to face this problem again?”
19. “Would you be willing to try a real, limited Python prototype when it is safe to test? What specific task would you bring?”

If payment is relevant, ask only after the behavior questions: “Have you paid for a tool to solve this problem before? What did you pay for?” Do not treat a hypothetical “I would pay” as evidence of willingness to pay.

## Notes template

Record only non-identifying summaries.

- Participant segment: beginner / hobbyist / working developer / other
- Recent real task (one sentence):
- Device and environment available:
- Actual workaround:
- Main friction observed/reported:
- Frequency in last month: none / once / 2–3 times / weekly or more
- Consequence: low / moderate / high, with short reason
- Existing alternative and why it was/wasn't sufficient:
- Files needed? yes / no / unsure
- Did the prototype's purpose make sense without explanation? yes / partly / no
- Strongest evidence of demand (specific behavior, not praise):
- Strongest evidence against demand:
- Follow-up task they offered to test (if any):
- Researcher confidence: low / medium / high

Do not collect code, private files, email addresses, or other personal data in these notes.

## Lightweight decision rule

After 5–8 conversations, summarize patterns before making a build decision.

**Evidence to continue exploring the problem:**
- Multiple participants describe a recent, specific instance without being led.
- They already use a workaround or lose meaningful time when testing code away from a computer.
- The pain recurs and is not already solved well by a tool they have.
- At least a few can name a concrete task they would bring to a real prototype.

**Evidence to narrow or pause:**
- Most people only express general enthusiasm but cannot recall a recent instance.
- The problem is rare or low-impact.
- Existing on-device or cloud tools already solve it with acceptable setup.
- The key barrier is something outside the proposed scope, such as building a complete app rather than running a small script.

These are directional signals, not statistically representative findings. Record negative evidence, do not count compliments as validation, and do not claim market validation from a small convenience sample.

## Research outcome

After the interviews, write a one-page summary containing:
- Number and broad segments of participants (no identities).
- Repeated recent tasks and workarounds.
- Most common high-friction steps.
- Existing tools that adequately solved the problem.
- Evidence for and against the current hypothesis.
- The single next experiment, or an explicit decision to narrow/pause.

No interviews or validation findings are implied by this template.
