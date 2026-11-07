# Why free ChatGPT keeps getting stuck on RevDev and PocketCode (evidence-tagged)

Tags: [S] secondary or community source, [V] verified by me this session, [I] my inference, [UNK] unknown.

## What the two errors mean
- "Streaming interrupted. Waiting for the complete message": the live connection carrying the answer dropped before it finished. Causes reported: network hiccups, load on OpenAI's side, VPN or extension interference [S: several guides]. The reply may still be completing on the server, so waiting 30-60 seconds before reloading is recommended [S].
- "The operation couldn't be completed (APIClientInterface.ConversationDetailError error 1)": I found no documentation of this exact string [UNK]. The wording points to the iOS app failing to fetch or open the conversation detail [I]. The nearby documented failure is "Could not load this ChatGPT conversation".

## What is platform-side (not fixable by us)
- Since late September 2026, OpenAI's community forum has many reports of conversations failing to load, stream-recovery timeouts, and intermittent errors on every plan and device, coming and going over hours [S].
- One user's capture showed a single conversations request returning about 69 MB [S, anecdotal]. Long conversations were reported as more likely to fail, though short ones also failed [S].
- The iPad app can show "Stopped thinking" while a long request keeps running and later produces output, which suggests the UI loses sync after backgrounding [S, one report].
- Free accounts run the small default model with a small context window (about 16K tokens in older reports; check Settings > Usage) [S].

## What we control, and probably make worse [I]
1. Very long chats: every new message reloads a heavy conversation, and long chats degrade [S].
2. "Think harder" plus "read the repo and continue": minutes-long streams that give the connection more time to drop, and a huge read at the start.
3. "Continue working efficiently" as the only instruction: forces the model to rediscover the task by re-reading everything.
4. A stale default branch: I read PocketCode's main README on 2026-11-06 and it still says "Discovery and product definition", while the handoff says the real work is on a branch 862 commits ahead [V]. A fresh chat that lands on main gets the wrong picture.
5. Many large state documents with no size budget. I could not read the working branch or the RevDev repo, so I could not measure their sizes [UNK]. RevDev's repo returned an access error to me (likely private) [V].

## The fix, in one line
Make the repo the memory, make a new chat cost about 2,500 tokens to start, keep every turn small, checkpoint constantly, and treat any chat as disposable.

## Prior art used
- Cline Memory Bank: a small set of docs rebuilt into context each session; its own guidance says activeContext should hold current state only, not a log [V: Cline docs]. Adaptation: tiers and word budgets instead of "read every file every time", which would overload a free chat.
- AGENTS.md convention (already used by PocketCode): one entry file every tool reads [V: repo].
- Agent-zero style stall rule: two identical diffs in a row means stop [S].
- Ponytail (YAGNI skill): reuse-first, minimal code. Independent testing credited about 10% savings [S].
