# AI lanes and dispatch (any project; how to decide which AI does what)

Status: PROPOSED working rules, 2026-11-10 (same text as in the RevDev repository). Evidence tags: OBSERVED = seen in this project; SECONDARY = public write-ups read 2026-11-10; INFERRED.

## 1. What we observed (this project, last two weeks)
- **ChatGPT (free account):** highest throughput, writes to GitHub, reads CI, available all day; small context, unstable app ("Stopped thinking", dropped streams). It is the lead and the continuity holder (owner decision).
- **Claude:** careful evidence work and code execution in a sandbox (it found three blocking model defects in the release-grant model by running counterexamples); but usage limits mean a large task can take days, so it must never sit on the critical path.
- **Gemini:** long-document reading and independent security review; availability has been intermittent and it cannot write to GitHub itself.

## 2. Patterns from public practice (SECONDARY)
- Aider's architect and editor split: a strong reasoning model plans, a cheaper or more obedient model applies the edits.
- Four-persona workflows: planner, implementer, several independent reviewers.
- A multi-agent engineering guide (Augment, July 2026) reports that parallel agents increase reconciliation work and that debate-style review helps only when the critic verifies better than the generator, so reviewers should verify by evidence (execution, source pins), not opinion.

## 3. Task packet (every dispatched task has these fields)
ID | type | size | blocking | inputs (at most 3, with sections) | output file | done-when | timebox | reviewer lane
- type: DRAFT, IMPLEMENT, REVIEW, VERIFY (run something), RESEARCH, SUMMARIZE.
- size: S under 30 minutes of AI time, M under 2 hours, L must be split before dispatch.
- blocking: yes only for the lead. Reviewers and researchers receive blocking: no.

## 4. Routing table
| Task type | Primary lane | Why | Reviewer |
|---|---|---|---|
| Plans, task packets, reconciliation, commits, CI reading | ChatGPT (lead) | throughput, GitHub write access | Claude or Gemini on request |
| Bulk drafting of docs and registers | ChatGPT | volume | spot review |
| Implementation of small slices | ChatGPT, or Claude when it needs execution to be sure | tests decide | the other lane |
| Adversarial review with evidence (counterexamples, pinned sources) | Claude | executes code, checks pins | ChatGPT reconciles ACCEPT / REJECT / NEEDS-OWNER |
| Reading very large documents or source and extracting registers | Gemini | long context | ChatGPT checks samples |
| Independent security and specification audit | Gemini and Claude separately, without reading each other first | independence | ChatGPT reconciles |
| Owner decisions, PC actions, purchases, credentials | owner only | authority | none |

## 5. Rules that keep it efficient
1. Never wait: the lead proceeds on provisional status; reviews are asynchronous.
2. Size cap per dispatch: Claude and Gemini receive S or M packets with at most 3 input files; the lead splits anything larger.
3. One writer per file; reviewers are read-only except for their own findings file.
4. Disjoint lanes in parallel: while ChatGPT implements slice N, Claude reviews slice N-1 and Gemini reads the next source area.
5. Reconcile lightly: one decision table per review, not a document per finding.
6. Independent reviews are not shared with each other before both are submitted.
7. Queue in the repository: work is assigned by an OPEN message in the lane's INBOX file with the packet fields.

## 6. Measure and adjust
Keep AI_LANE_LOG.tsv with one line per dispatched packet: ID, lane, type, size, started, finished, defects found by the reviewer, rework needed. After 20 lines, re-route using the data. Until then the table is a hypothesis.
