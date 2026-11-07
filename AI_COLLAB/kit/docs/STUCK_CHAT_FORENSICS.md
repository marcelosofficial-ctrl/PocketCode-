# Stuck chat forensics: what survived, and where to look (phone-friendly)

Rule zero: GitHub is the truth, the chat is only a notification. Commits stay on GitHub even when a chat loses its answer.

## What the evidence says [S = community or issue reports, I = my inference]
- "Stopped thinking" with no final answer and no error is a known failure. A captured server snapshot showed reasoning and tool steps saved after a progress message, but no final answer saved, and the chat looked complete [S: openai/codex issue 54974]. Affected chats were not necessarily long.
- A chat can stay "Working", Stop can fail, and newer messages can be searchable but missing from the view, on phone and desktop alike [S: openai/codex issue 58943]. The reporters say this does not prove the messages were deleted.
- A long iPad task showed "Stopped thinking" several times while the same task kept running and later produced output [S: OpenAI community].
- A failed-run email from GitHub means a push or pull-request event happened, because workflows only start on those [I]. Emails arriving minutes after a chat "stops" suggest the agent kept executing tool steps (including commits) after the screen lost sync. This is likely, not proven.
- Plain ChatGPT chat does not keep working after a reply ends. Only agent or Work/Codex-style runs continue in the background [S: TechRadar].
- I found no source saying ChatGPT deletes stuck messages on purpose. Messages that exist on the server but are not displayed, or answers that never got saved, both fit the evidence [I].

## What is probably safe and what is probably lost [I]
- Safe: anything committed to GitHub (check, never assume).
- Maybe recoverable: messages saved server-side but not shown.
- Probably lost: research that lived only in a chat reply whose final answer was never saved.

## Check in this order (5 minutes, no AI needed)
Replace OWNER/REPO/BRANCH with your own.
1. Commits on the branch, newest first: https://github.com/OWNER/REPO/commits/BRANCH . Note the times. Match them to the failure emails (the short code in the email title, like bd2dd8b, is the commit).
2. What changed since the last good state: https://github.com/OWNER/REPO/compare/main...BRANCH . Open a commit to see its files.
3. CI runs: https://github.com/OWNER/REPO/actions . A red run on commit X means the code in X fails its tests. It does not mean the chat is still working.
4. Is anything still running? If there is no new commit for 15 minutes and no "in progress" run, treat the chat as dead.
5. Recover the chat text: open the same chat on the web and on another device; search ChatGPT for a distinctive phrase from the lost reply; or Settings > Data controls > Export data, which emails you your chat history (I have not verified that stuck turns are included).

## Rebuild from facts, not from the chat
Start a NEW chat and send prompts/RECONCILE_AFTER_STUCK.txt. It lists the commits since the last checkpoint, reads each CI result, separates claimed work from committed work, and writes a RECONCILIATION note in the repo.

## Prevention (all in WORK_PROTOCOL.md)
- Write-ahead: every finding is written to a repo file and committed before the chat summarizes it.
- Small units: one commit per unit, each under about 10 minutes of model time.
- Red CI rule: never stack new work on a red commit. The first task is to fix it or to record exactly why it is red.
- Keep the app in the foreground while a Think or Work run is active.
