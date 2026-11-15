# Gemini research handoff — PocketCode (2026-11-15)

**Role:** independent research analyst for ChatGPT, not project implementer. Produce evidence and decisions that save implementation/review time. Research only: do not edit files, commit, open/modify PRs, change workflows, select infrastructure, or claim tests ran.

**Project:** `marcelosofficial-ctrl/PocketCode-`, branch `pocketcode-ai-workflow-director-research-2026-10-28`. Phone-first, provider-neutral, $0 AI workflow control plane. Read the current branch's `AI_COLLAB/BOOT.md`, `STATE.md`, and `NEXT_TASK.md` before researching. Treat live GitHub as authority; older handoffs may be stale. Preserve all constraints and acceptance IDs.

## Four-pass protocol

Work in one Gemini conversation if possible. At the start and end of every pass, update a compact durable **Research Ledger** (copy-forward text or file). Never rely on Gemini cross-chat memory. If starting a new chat, attach the latest ledger and previous pass reports first. Record decisions, evidence, citations, unresolved questions, and exact next steps—not a narrative transcript. Do not discard contradictory findings.

1. **Pass 1 — repository-grounded gap map.** Inspect the relevant source/tests in bounded sections: `scripts/event_journal.py`, `scripts/result_receipts.py`, `scripts/test_result_receipts.py`, grant/outbox model and tests, execution/lifecycle/report projection, and CI workflow. Do not read any large file wholesale. Map current APIs, invariants, failure modes, existing tests, missing tests, and source line references. Separate VERIFIED source facts from inference and unknowns.
2. **Pass 2 — external technical research.** Investigate primary sources, standards, mature implementations and postmortems for: (a) journal-to-receipt freshness, provenance and TOCTOU; (b) atomic snapshots/concurrency and append-only logs; (c) transactional outbox, idempotent delivery, ordering, lost acknowledgements and inbox dedupe; (d) producer authentication, identity/fencing and replay; (e) execution termination evidence and lifecycle/report semantics. Prioritize official specifications, language/runtime docs, papers, maintainer docs and source code. Include relevant negative evidence and licensing/maintenance notes. No technology adoption recommendations that violate $0/provider-neutral constraints.
3. **Pass 3 — adversarial comparison and test design.** Challenge Passes 1–2. Search for counterexamples, race windows, ambiguous semantics, hidden trust assumptions, incompatible guarantees and source contradictions. Compare at least two viable model-level designs where appropriate. Build minimal regression matrices with preconditions, event sequences, expected state/fingerprint/watermarks, and failure assertions. Mark adapter-only guarantees separately. Identify what cannot be proved in a pure in-memory model.
4. **Pass 4 — final synthesis for ChatGPT.** Reconcile the ledger and all three reports. Deliver one concise but deep, self-contained handoff with prioritized findings, recommended model-only changes, exact file/section/line anchors, proposed tests, risks, rejected alternatives, evidence citations, unresolved decisions and a sequenced implementation plan. Remove duplication, not caveats. Do not claim implementation or test completion.

## Mandatory quality controls

- For every material claim: direct source URL, title, publisher, date/version, exact supporting section/line/page, and a short explanation of what it proves. Prefer primary sources; use community reports only as leads, clearly labelled anecdotal.
- Triangulate important claims with two independent sources where feasible. Explicitly surface disagreements; never silently choose one source.
- Verify citations open and actually support the sentence. Distinguish current documentation from archived/version-specific behavior.
- Maintain a claim ledger with labels **VERIFIED / INFERRED / UNKNOWN / NOT RUN**. For code/test status, name exact commit SHA and whether evidence is static inspection or an actual run.
- Do not fabricate line numbers, test results, API behavior, benchmarks, guarantees, or source citations. Say “not found” when research is inconclusive.
- Keep PocketCode separate from RevDev. Preserve $0, no paid services, provider neutrality, explicit user paste/import, default-deny security and all existing LOOP/CASE/D/OD identifiers.
- P39 implementation/adapter conformance remains CLOSED; CASE-04 remains INCOMPLETE / `timed_out`. No workflow edits, provider/adapter implementation, device tests, deployment, PR changes, or infrastructure selection are authorized.
- Do not propose replacing large files wholesale. Recommend small, bounded changes only.

## Known priority questions

1. Current receipt creation accepts a detached `JournalReceiptSnapshot`; can a stale snapshot omit a later same-effect/attempt conflict? Compare deriving fresh evidence from the exact live `EventJournal` inside receipt creation versus explicit version/freshness tokens. Preserve journal-global observation/accepted-event high-waters and effect/attempt-scoped conflict references. Evaluate atomicity and thread-safety honestly.
2. What is the smallest sound model for grant transition + outbox semantics, including duplicate delivery, same identity/different digest, out-of-order versions, crash/lost acknowledgement and successor replay?
3. Which producer authentication, lease/fence, dedupe and ordering guarantees belong in the adapter rather than the model? Define trust boundaries precisely.
4. What does a supervisor's terminate/close acknowledgement actually prove versus native child/renderer teardown? How should unknown evidence remain unknown without changing report format 1?
5. How can exact-head CI be proven without altering the currently unauthorized workflow?

**Output cadence:** after each pass, provide a short pass report plus the updated ledger and a precise next-pass prompt. Do not wait until pass 4 to expose important discoveries. At pass 4, consolidate everything into one final handoff titled `POCKETCODE_GEMINI_FINAL_RESEARCH_HANDOFF`, suitable for ChatGPT to apply without asking Gemini follow-up questions.
