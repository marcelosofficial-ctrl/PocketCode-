# Independent audit: Claude provider-caching and AI-lanes research

**Date:** 2026-11-11  
**Target:** `marcelosofficial-ctrl/PocketCode-`  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Audited HEAD:** `2247851a8bcff798609c27bec78e2dd72b0dd11b`  
**Claude research commit:** `3b73e2cc8a8371508b80d1e65393375f986b3760`  
**Claude design correction commit:** `2247851a8bcff798609c27bec78e2dd72b0dd11b`

## Executive disposition

Claude's new research is useful as a direction-setting draft, but the provider cache matrix is not safe to use as an implementation reference without the corrections below. Provider docs have changed materially. The AI-lane proposal also needs role and evidence-scope corrections. This audit is a separate evidence/reconciliation artifact; it does not select a provider, authorize paid API calls, or change project roles.

## Ranked gaps

1. **Provider caching facts are stale or underspecified.** OpenAI's current model-generation split, Gemini's API/model support split, and per-model minimum cache sizes materially change the implementation assumptions.
2. **No measurable cache-efficiency acceptance contract.** The proposal lists telemetry but does not define denominators, cost calculation, misses, concurrency warm-up, or how to prevent a cache-hit rate from being misrepresented as savings.
3. **One provider-neutral prompt ordering is over-generalized.** Anthropic documents a specific tools → system → messages prefix hierarchy; OpenAI caches its rendered context and settings; Gemini's implicit cache is best-effort prefix reuse. One serialized order cannot be asserted as universally optimal.
4. **Tool-schema portability is only a proposal.** Provider strictness and supported JSON Schema subsets differ. The cited young converter is not established as maintained or suitable. MCP JSON Schema is a legitimate reference, not proof of a drop-in universal provider schema.
5. **AI-lane roles/evidence need tightening.** The new routing table calls ChatGPT “lead”, while BOOT assigns Claude lead developer/architecture reviewer and ChatGPT continuity/evidence/coordinator. Account-specific connector observations are presented too generally.

## 1. Provider caching: verified current facts

### Anthropic Messages API

**VERIFIED (official docs opened 2026-11-11):**
- Automatic caching uses a top-level `cache_control`; explicit breakpoints mark content blocks. Prefix order is `tools`, then `system`, then `messages`.
- The total limit is four breakpoint slots. Automatic caching consumes one slot when combined with explicit breakpoints; four explicit block breakpoints leave no slot for automatic caching.
- Default TTL is five minutes. A one-hour TTL is available at 2× base input price. Five-minute writes are 1.25× base input; reads are 0.1× for most models, with documented model-specific lower rates.
- Minimum cacheable prompt size is model-specific, not a single provider constant: current docs list 512, 1,024, 2,048 or 4,096 tokens across active/legacy models. Below the model threshold, caching is silently skipped.
- Exact response usage fields are `cache_creation_input_tokens` and `cache_read_input_tokens`. The `input_tokens` field is only the uncached suffix after the last breakpoint, so it is not total input by itself.
- A newly written cache entry becomes available only after the first response starts. Concurrent requests sent before that point cannot assume a warm cache.

**Correction:** the source document's “one request-level marker or up to four explicit block-level breakpoints” needs to state that the automatic marker uses one of the four total slots. A fixed cache minimum must never be assumed without model/platform lookup.

### OpenAI Responses API

**VERIFIED (official docs and API reference opened 2026-11-11):**
- Current docs distinguish GPT-5.6-and-later from earlier models. GPT-5.6+ supports implicit and explicit breakpoints; explicit-only mode writes only selected breakpoints. The minimum cacheable prefix is 1,024 visible input tokens for GPT-5.6+, excluding hidden system tokens.
- Earlier models use implicit breakpoints only; the minimum varies with request settings. Reported `cached_tokens` is rounded down to 128-token multiples. This is a reporting rule, not a universal requirement that all cache prefixes be built in 128-token increments.
- For GPT-5.6+, `prompt_cache_key` is optional for separate cache accounting and is not required to optimize cache routing. For earlier models, a stable key helps route similar requests to the same cache; it does not pin a machine or guarantee a hit.
- Responses API GPT-5.6+ supports 30-minute and 12-hour minimum cache lifetimes. Current documented write rates are 1.25× and 2.5× respectively; reads are 0.1× on most models, with model-specific exceptions.
- Exact usage fields are `usage.input_tokens_details.cached_tokens`, `cache_write_tokens`, and `cache_write_tokens_details.ttl_30m_tokens` / `ttl_12h_tokens`.
- Tool names, descriptions, schemas, ordering, model/settings, and context changes can affect the rendered prefix. Stable history is helpful, but session continuity alone does not guarantee a hit.

**Correction:** the source document's broad “automatic for 1,024+ tokens”, “exact prefix in 128-token increments”, and “newer models need a cache key for reliable hits” claims are inaccurate as general statements. Replace them with the generation-specific behavior above. Do not conflate token-reporting rounding with cache matching.

### Google Gemini API

**VERIFIED (official Google AI Studio docs opened 2026-11-11; the former ai.google.dev URL redirects to aistudio.google.com):**
- Implicit caching is enabled by default on Gemini 2.5 and newer, but savings occur only when a cache hit happens. The current per-model minimums listed are 2,048 tokens for Gemini 2.5 Flash/Pro and 4,096 for the listed Gemini 3/4 models.
- Explicit cached-content objects are currently Beta on `v1beta`, supported for Gemini 2.5 and 3, and not supported for Gemini 4.
- Explicit caching uses the GenerateContent API. The Interactions API supports implicit caching only.
- Explicit cache TTL defaults to one hour when omitted; TTL is configurable. Storage cost depends on cached token count and TTL. The minimum input token count for explicit caching varies by model; do not reuse the implicit-cache threshold table as the explicit threshold table.
- Google documents `usage_metadata` as the place to inspect cached-token usage. Keep the SDK/API version with the stored telemetry contract; do not guess field names from memory.

**Correction:** “Gemini uses implicit caching by default and explicit objects if the static context meets a universal 1,024–4,096 threshold” is not a safe rule. The feature split depends on model generation and API surface. Gemini 4 explicit caching is not available in the current docs.

## 2. Finished measurement contract (proposal, not implementation)

For every provider request, record a versioned, provider-normalized observation alongside the raw provider usage payload:

| Field | Definition |
|---|---|
| `provider`, `model_id`, `api_surface`, `sdk_version` | Exact service/model/API/SDK identity for interpreting changing fields |
| `request_fingerprint` | Digest of the normalized request shape; never store secrets or raw private prompts in public telemetry |
| `eligible_prefix_tokens` | Count of the provider-specific prefix intended to be reusable, calculated with the matching tokenizer/API where available |
| `cache_read_tokens`, `cache_write_tokens`, `uncached_input_tokens` | Normalized counters derived from documented raw fields; unknown if unavailable, never guessed |
| `cache_write_ttl`, `cache_mode` | Actual provider configuration used |
| `request_started_at`, `first_response_started_at`, `completed_at` | Timing to diagnose cache warm-up/concurrency and latency |
| `input_cost_estimate`, `cost_basis_version` | Calculated from exact model rates and raw token counters; mark estimate, not invoice |
| `observation_status` | `MEASURED`, `UNAVAILABLE`, `NOT_APPLICABLE`, or `ERROR` |

**Required calculations:**
- Cache-read share = cache-read tokens ÷ (cache-read + cache-write + uncached input tokens). If the denominator is zero or any term is unknown, report UNKNOWN.
- Cache-write overhead and cache-read savings must be priced separately using the exact model/API rates effective on the request date. Do not treat a hit rate as a savings percentage.
- Report p50/p95 time-to-first-token and total latency for matched cached/uncached request groups, plus total input cost. Keep output-token cost separate.
- Separate first-write/warm-up requests, cache misses, provider errors, and concurrent cold-start requests. Do not silently discard them from denominators.
- Run paired repeated requests with identical stable prefixes and controlled variable suffixes. Change one cache-relevant variable at a time. A provider-reported cache hit is evidence of reuse, not proof of product-level cost savings until billed usage and rate are reconciled.

**MVP decision:** this remains a future measurement contract only. D-005/D-006 prohibit spend; no API call, key, provider, cache adapter, model or paid experiment is authorized.

## 3. Context engineering and reusable open source

- **Aider repo map:** official docs verify a graph-ranked dependency map of important files/symbols and a default `--map-tokens` budget around 1,000 tokens. This is a sound design pattern for a compact, task-relevant repository map. Reuse the concept and output shape, not Aider's runtime. Aider is Apache-2.0; its GitHub releases page lists v0.86.0 as latest (published 2025-08-09) and repository API reported last push 2026-05-22. Treat it as a reference, not an assumed actively releasing dependency.
- **Aider architect/editor:** official docs confirm the architect model proposes a plan and a separate editor model converts it into edits. This adds a second model request and can increase cost/latency; do not make it the default under the $0 decision.
- **MCP schema:** the official MCP repository describes a TypeScript-first protocol schema also made available as JSON Schema and declares MIT licensing in its README. The repo showed active commits on 2026-11-11. Reuse it as an interop reference where useful, not as a universal LLM provider contract.
- **Google examples:** Google AI Studio docs are current and the page says explicit caching is Beta; the docs page states no software licence for the docs themselves. Its code samples carry Apache 2.0 per Google Developers Site Policies. No sample code copied.
- **Provider docs:** Anthropic/OpenAI/Google documentation pages are specifications and reference material, not code libraries. No source code copied and no third-party dependency added.

**Recommendation (INFERRED):** keep a PocketCode-owned, versioned tool-contract model with a deliberately small common subset. Each provider adapter must transform and validate against that provider's current strict schema rules, with golden fixtures for required/nullable fields, enums, nested objects, unsupported keywords, ordering and round-trip loss. Preserve the original canonical schema and adapter diagnostics. Do not add the unverified `tool-schema` package or select MCP as the runtime.

## 4. AI-lane proposal: red-team corrections

1. **Role collision:** `AI_LANES_AND_DISPATCH.md` calls ChatGPT “lead”, while BOOT assigns Claude lead developer/architecture reviewer and ChatGPT continuity/evidence/coordination. Interpret the table as task routing only. It must not override BOOT or owner authority.
2. **Over-generalized product claims:** “ChatGPT Free writes GitHub”, “Gemini cannot write GitHub”, and availability statements are account/connector/session observations, not stable model capabilities. Label them as observations at a date and re-check tool access per task.
3. **Unmeasured thresholds:** S <30 minutes, M <2 hours, and rerouting after 20 packets are hypotheses. They are not empirical project limits. Keep them provisional until a real `AI_LANE_LOG.tsv` dataset supports them.
4. **Lead/implementer split:** Aider's architect/editor mode is a useful pattern, but not a direct multi-agent governance design. It makes two model calls and may increase cost; owner-approved roles and repository write boundaries still control.
5. **Missing failure path:** task packets need an explicit “blocked / partial / stop” result, evidence references, and an escalation owner. A task cannot be declared done just because the model produced the requested file.

**Corrected role interpretation:** Claude remains lead developer and architecture/implementation reviewer; Gemini remains co-developer and independent security/spec auditor; ChatGPT remains continuity holder, evidence reconciler, acceptance architect and cross-project coordinator. A task may have one designated writer/coordinator without changing those project roles. Owner-only decisions remain owner-only.

## 5. Red-team correction ledger

| Prior weakness | Correction made here |
|---|---|
| OpenAI cache rules collapsed into one 1,024-token/128-step rule | Split GPT-5.6+ and earlier models; distinguish cache minimum, cache boundaries and reporting rounding |
| OpenAI cache-key guidance said newer models need stable keys | Corrected: earlier models use keys for routing; GPT-5.6+ keys are optional accounting partitions |
| Gemini cache thresholds and explicit support treated as universal | Added current per-model minima, Gemini 4 exclusion, Interactions-vs-GenerateContent split, Beta status and model-dependent explicit minimum |
| Cache telemetry field names marked “from memory” | Replaced with opened official usage-field names; Gemini left SDK/API-version qualified |
| Universal stable-prefix ordering proposed across providers | Added provider-specific serialization and breakpoint behavior |
| AI lane “ChatGPT lead” conflicts with BOOT | Preserved BOOT roles and constrained routing table to task assignment |
| INDEX said under 1,200 words but contained 1,232 whitespace-delimited words | Separate index correction in this pass; exact count recorded in CHECKPOINT |

## Sources opened 2026-11-11

- Anthropic prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Anthropic tool definitions: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- OpenAI prompt caching: https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI function calling: https://developers.openai.com/api/docs/guides/function-calling
- Google Gemini context caching: https://aistudio.google.com/docs/caching
- Google Gemini function calling: https://ai.google.dev/gemini-api/docs/function-calling
- Aider repository map: https://aider.chat/docs/repomap.html
- Aider architect/editor: https://aider.chat/docs/usage/modes.html
- Aider releases: https://github.com/Aider-AI/aider/releases
- Aider repository/license: https://github.com/Aider-AI/aider
- MCP repository/schema/license: https://github.com/modelcontextprotocol/modelcontextprotocol

**Evidence boundary:** current docs were opened and inspected as above. The Gemini function-calling page returned HTTP 410 when opened, so its search result is not used as a VERIFIED implementation claim; the schema-subset recommendation remains INFERRED and must be rechecked from current API docs before implementation. No project code, tests, provider calls, device behavior or spend was exercised.
