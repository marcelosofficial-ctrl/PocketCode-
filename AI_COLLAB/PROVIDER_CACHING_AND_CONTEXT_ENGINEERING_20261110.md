# PoCo context engineering and provider caching (research and proposal, 2026-11-10)

Status: PROPOSED. Nothing is implemented; no provider is selected (D-004). This answers the brief's section 3 (A, B, C) with provider-specific facts. Sources were read 2026-11-10 on the providers' own documentation unless marked SECONDARY. Documentation changes often: re-read the linked page before building anything, and record the date. Tags: VERIFIED, SECONDARY, INFERRED, UNKNOWN.

## 1. Provider facts that must not be assumed identical
| Topic | Anthropic (Claude API) | OpenAI | Google (Gemini API) |
|---|---|---|---|
| How caching starts | Automatic caching with one request-level cache_control marker, or up to 4 explicit block-level breakpoints (VERIFIED, platform.claude.com prompt-caching docs) | Automatic for prompts of 1,024 tokens or more (VERIFIED, developers.openai.com prompt-caching guide) | Implicit caching on newer models, plus explicit cached-content objects you create (VERIFIED, ai.google.dev caching page) |
| What matches | A prefix in the order tools, then system, then messages; changing an earlier part invalidates what follows (VERIFIED) | Exact prefix match, in 128-token increments (VERIFIED) | Implicit: no guarantee; explicit: the cached object you reference (VERIFIED) |
| Lifetime | 5 minutes by default, refreshed on use; a 1-hour option costs more to write (VERIFIED; multiplier values changed across models, read the pricing page) | A short in-memory window or a longer retention depending on model (VERIFIED that both exist; per-model values UNKNOWN here) | Explicit cache has a TTL you set (default one hour on the page I read) and storage is billed for the TTL (VERIFIED) |
| Routing control | none beyond prefix stability | a prompt_cache_key groups related requests; newer models need it for reliable hits; explicit breakpoints and cache-write billing appear in the newest guide (VERIFIED) | explicit object id |
| Minimum size | varies by model (UNKNOWN current values) | 1,024 tokens (VERIFIED) | varies by model and by version of the page: one version lists 1,024 to 4,096, a secondary article claims 32,768; UNKNOWN, read the live page |
| What to log | the usage fields for cache creation and cache read (names from memory, INFERRED) | cached_tokens in usage (INFERRED) | cached token count in usage metadata (INFERRED) |
The pages also warn that the Gemini documentation is moving to a newer Interactions API, so any Gemini integration must re-check the current interface.

## 2. What PoCo should do with that (PROPOSED)
1. **One stable-prefix layout for every provider:** tools, then project instructions, then the repository map, then the per-task packet last. A change to the first three layers is an event (it resets the cache everywhere), so they change rarely and deliberately.
2. **A CachePolicy adapter per provider** behind the provider-neutral interface: Anthropic gets a breakpoint at the end of the stable prefix; OpenAI gets the stable prefix plus a per-project prompt_cache_key; Gemini uses implicit caching by default and an explicit cache object only when the static context is large enough to pass the live minimum and is reused several times within the TTL.
3. **Measure instead of believing:** record the provider's cached-token fields in every run's evidence record, so efficiency claims in the product are numbers, not hopes. Do not promise savings in the store listing or the website until measured.
4. **No claim that PoCo overrides provider limits.** Caching lowers cost and latency for repeated context; it does not extend context windows or change model ability.

## 3. Context engineering architecture (PROPOSED)
| Layer | Purpose | Reuse instead of building |
|---|---|---|
| Project instructions | one canonical file rendered per provider (AGENTS.md for tools that read it; CLAUDE.md; GEMINI.md; the 1,500-character ChatGPT custom instruction for free accounts, VERIFIED earlier) | the AGENTS.md convention (in use in this repo) |
| Repository map | a ranked, token-budgeted map of files and symbols so the AI reads structure, not files | Aider's repo map: tree-sitter definitions and references ranked with PageRank under a token budget, default about 1,024 tokens, Apache-2.0 (VERIFIED earlier); a stdlib-only variant for Python is feasible without tree-sitter |
| Task packet | one bounded task with at most 3 inputs, an output file and a done-when | our own packet format (AI_LANES_AND_DISPATCH) |
| Retrieval | fetch only the sections a task needs; extracts for big documents | extracts and INDEX (in use) |
| Compression with provenance | summaries must keep decision IDs and point back to the source with a hash so nothing essential is lost silently | Cline SDK's compaction with a hash-validated prefix (design read earlier, SECONDARY for code) |
| Durable decisions | IDs never renumbered, evidence tags kept | LOOP, CASE, D-IDs (in use) |

## 4. Tool schemas across providers (SECONDARY, plus INFERRED)
- OpenAI strict function calling expects every property required, additionalProperties false, optional values expressed as nullable; Anthropic tool definitions use a permissive input_schema with an optional strict mode; Gemini uses function declarations in an OpenAPI-style subset (or a JSON Schema field in newer versions); MCP uses inputSchema and, in the 2026-07-28 revision, outputSchema.
- **PROPOSED:** keep one canonical definition (a JSON Schema subset the product controls) and write small converters per provider with tests that round-trip a fixed set of tools. An open-source converter exists (a young MIT TypeScript package, tool-schema, almost no adoption), so treat it as a reading aid, not a dependency.

## 5. Model routing (PROPOSED)
Split planning from editing as Aider's architect and editor modes do: a stronger reasoning model plans, a cheaper or more obedient model applies edits. In PoCo this is a routing table by task type with a cost and capability note per provider and a date; every entry that is not verified says UNKNOWN. No vendor is hard-coded.

## 6. Efficiency measures PoCo can really offer
Fewer repeated explanations (project instructions and decisions persisted), less repeated exploration (repo map and extracts), less unnecessary context (task packets, retrieval), fewer repeated conversations (checkpoint and resume), fewer lost decisions (IDs and ledger), fewer unverified claims (evidence tags and run evidence), less manual coordination (inbox queue). Each is already practised in this repository by hand; the product would automate and measure them.

## 7. Open items
Read the current Anthropic pricing page for cache multipliers and minimums; read the live OpenAI and Gemini pages for retention and minimums; decide whether the first prototype calls any provider at all (the no-spend decision means the owner's own API keys or free tiers only); verify field names in real usage responses.

## Sources (read 2026-11-10)
platform.claude.com/docs/build-with-claude/prompt-caching; developers.openai.com/api/docs/guides/prompt-caching; ai.google.dev/gemini-api/docs/caching; secondary: Portkey and Microsoft Foundry caching pages, fast.io Gemini caching article, tool-schema conversion write-ups (agentpatterns.ai, toolschema docs).
