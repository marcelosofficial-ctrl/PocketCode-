# PHONE-ONLY CI VISIBILITY: how AI collaborators read CI results without Actions log access (strategy question 3, CI half)

Written 2026-11-24 by Claude from this program's own experience, 2026-11-14 to 2026-11-24. Tags: VERIFIED (seen in this program's tool results or commits), INFERRED, UNKNOWN. Status: PROPOSED pattern; the evidence-branch part was implemented in one private project on 2026-11-24 and its first run result was pending when this was written. Nothing here is a PocketCode product claim.

## 1. The problem
- VERIFIED: the ChatGPT connector returned HTTP 400 or 404 for Actions run and log endpoints on several occasions; one Grok chat could list job steps but not download logs; Claude's GitHub connector has no Actions endpoints. The owner's phone can open a run page in Safari, but that costs owner time every run.
- Consequence: a red run can cost several round trips before anyone knows which step failed. A private emulator workflow went red four times in two days; the first three were diagnosed only because one chat could read job steps.

## 2. What each route gives (VERIFIED unless marked)
1. Gmail "Run succeeded" and "Run failed" emails (Claude, through its Gmail connector): workflow name, branch, commit short SHA, run id and URL, duration, finish time, each job with its conclusion and annotation count. No step names and no logs. In a multi-job workflow the email says which job failed, which is how the build job was seen to pass while the emulator job failed.
2. Pull request check runs (Claude's GitHub connector): returns check name, conclusion, timestamps and job URL, so a green or red build gate can be read directly. Seen on a portfolio pull request. Only runs triggered by a pull_request event appear; pushes to a pull request's base branch do not. INFERRED: the same holds for other connectors.
3. Jobs API through a chat connector: lists steps and conclusions when it works (one Grok chat); unreliable in others.
4. The owner opening the run page in Safari: always works, costs the owner's time.

## 3. Design rules for workflows that AI collaborators must debug
1. Split jobs by purpose (for example build, smoke, report) so the email names the failing job.
2. Turn every claimed result into an assertion step that prints one line starting "ASSERTION FAILED" plus a bounded diagnostic (last 80 lines of the relevant log), so a red step explains itself.
3. Add a final job that always runs and writes a short text report to a dedicated branch (for example `ci-evidence`, file `t022/LAST_RUN.md`): it asks the Actions jobs API for the steps that did not succeed, downloads the evidence artifact, trims it to a few hundred lines and commits it. Give that job alone `actions: read` and `contents: write`; keep the workflow default at `contents: read`. Any AI then reads the report with an ordinary file read. A push made with the workflow token does not start new workflow runs, and the main workflow's push trigger is limited to the working branch and its own file, so there is no loop. Never include secrets; cap sizes; overwrite one file per run instead of growing a log.
4. Keep jobs independent of disk-heavy neighbours: a hosted Linux runner has roughly 14 GB free, and one job doing an Android build plus an emulator image ran out of space; separate jobs get a whole runner each.
5. Avoid `cancel-in-progress` on refs that receive many small commits unless path filters keep those commits from triggering the run; a cancelled run leaves no evidence.
6. Record each run id, commit and conclusion in the repository (STATE.md or an inbox) the same turn it is read, because chat memory does not carry it.

## 4. Cost notes (INFERRED from observed runs)
- A private repository's standard Linux runner is a small machine (observed: a mobile build plus emulator boot took 13 to 20 minutes per run), so each run should earn its minutes: trigger only on the workflow's own path or manually.
- Free minutes are finite on private repositories; a public repository avoids that limit but exposes the workflow.

## 5. Still queued from question 3
Repo-map extracts for phone-sized context. Not started.
