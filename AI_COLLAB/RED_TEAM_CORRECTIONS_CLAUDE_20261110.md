# Red-team corrections to Claude's earlier work (2026-11-10)

Claude re-checked its own earlier documents and found these mistakes or weak claims. Each is classified and, where small, fixed at the source in the same commit series.

| # | Document | Problem | Fix |
|---|---|---|---|
| 1 | APPLE_DESIGN_ENGINEERING_SPEC_20261108.md, section 3 | BUG: the line `html { font: -apple-system-body; font-size: 100%; }` sets the font shorthand and then overrides its size with 100%, which cancels the Dynamic Type hook it was meant to provide | removed the second declaration in the fixed spec |
| 2 | same, section 3 | wording: "linear() supported in Safari ... a 17.4 note lists a fix" proves support at 17.4 or later, not the first version | reworded to "supported at least since Safari 17.4" |
| 3 | IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md | the private-repository allowance was stated as 2,000 minutes with a 10x macOS multiplier (about 200 macOS minutes); GitHub's current billing page uses a dollar-based included amount, and standard-runner use in PUBLIC repositories stays free. The free-for-public claim is confirmed on the billing page; the old multiplier numbers are outdated | treat the private numbers as superseded; irrelevant to the no-spend path (this repository is public) |
| 4 | same roadmap, section 4 | the 4.7 update of 2025-11-13 was cited as VERIFIED from a search snippet; Claude did not open the Apple page that pass | downgraded to SECONDARY until the page is opened |
| 5 | WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md, section 3 | stated that no RevDev application source exists in any of the owner's 12 repositories; Claude listed repository names and one repository's root, not the contents of the others | restated: no repository is named for the RevDev application and DevRelay-Missions holds no application folder; the other repositories' contents were not searched |
| 6 | CLAUDE_P39_INDEPENDENT_REVIEW_2026-11-08.md (owner's copy) | scope sentence said the research packet was read "at the pins"; it was read at the branch tip | corrected in the file before delivery |
| 7 | RevDev O-1 review, first copy given to the owner | the unqualified claim that destination CAS could be the safety property was too strong; the contract separates duplicate prevention from cancellation enforcement | revised in the committed version (RV-H1); the first copy is superseded |
| 8 | AGENTS and INDEX rules | the INDEX budget of 1,200 words is now exceeded (about 1,500 words) because of the P39 and P40 rows | recommendation: collapse closed review rows into a group line; owner or ChatGPT to do it, Claude will not rewrite another AI's index entries |

Also confirmed correct on re-check: git blob SHAs of both transcribed code files; the P29 test run (3 of 3 in Claude's sandbox); the model-defect counterexamples.
