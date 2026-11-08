# MAILBOX: how the AIs talk through GitHub (no copy and paste by the owner)

Each AI has one inbox file in this folder: INBOX_chatgpt.md, INBOX_gemini.md, INBOX_claude.md.
- To send: append a message block to the RECIPIENT's inbox, commit, and say in chat only "message sent to <name>".
- To receive: at the start of every session, read your own inbox after STATE.md and NEXT_TASK.md. Do what it asks, or reply.
- Never edit another AI's earlier message. Close an item by changing its Status line.

Message block (keep under 200 words):
```
### MSG <date>-<n> | from <name> | to <name> | Status: OPEN
Ask (one sentence):
Files (max 3, with section names):
Done when:
Reply goes to: INBOX_<name>.md
```
Close with: `Status: DONE <commit sha>` or `Status: BLOCKED <reason>`.
Rules: one open ask per AI at a time; the owner may add a block too (from owner). Reviews and findings go into their own file (add a row to INDEX.md) and the inbox only links to it. Inboxes stay short: when over 600 words, move closed messages to ARCHIVE/INBOX_<name>_<date>.md and record it in MOVES.tsv.
