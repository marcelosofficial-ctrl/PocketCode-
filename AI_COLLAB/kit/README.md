# AI Work Kit

Makes any AI chat, free or paid, resume a large project from a ~1,750-word start-up capsule instead of re-reading everything. Nothing is deleted; only the way work is loaded changes.

Use: (1) install into a repo with prompts/INSTALL_<project>.txt, one stage at a time; (2) start every new chat with prompts/START_NEW_CHAT_<project>.txt; (3) after an error send RESUME_AFTER_ERROR.txt; (4) end a chat with CLOSE_SESSION.txt; (5) after a chat that went silent or showed "Stopped thinking", read docs/STUCK_CHAT_FORENSICS.md and send RECONCILE_AFTER_STUCK.txt in a new chat.

Read docs/WORK_PROTOCOL.md for the rules and docs/WHY_CHATGPT_GETS_STUCK.md for the evidence. tools/ctx_kit.py (standard library only; tests included) measures docs, builds the capsule, checks budgets and proves no information was lost.
