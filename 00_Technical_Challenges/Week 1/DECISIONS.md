# Decisions

One row one decision. This week is the first one. By Week 5 this file will explain what decisions you made during this bootcamp.

## Retrieval, week 1

**What I changed**

> Replaced character-window splitting (1000/200) with heading-based splits on `##` / `###`, so each section or film entry becomes one chunk.

**Why**

> Character splits cut films mid-entry and mixed titles in one window; lookup and multi-part questions often ranked the wrong evidence. On the same 10 questions: **before 5/10 → after 9/10**. Heading splits keep entries intact (e.g. Coherence / Hunt / Submarino as whole chunks) and retrieve the taste-profile section as a unit. They do not fix exhaustive list questions when `k=3`.

**What would change my mind**

> Heading splits create about one chunk per film, so every question re-embeds the whole catalog and cost grows with N. If the list got much larger, I wouldn't keep doing that blindly — I'd need a different approach to indexing/retrieval at that scale, not just bigger character windows.

### Eval table (same 10 questions)

Corpus: `data/my_movies.txt`. Before = character split (1000/200). After = heading split on `##` / `###`.

| # | Question | Before | After | What changed |
|---|----------|--------|-------|--------------|
| 1 | What did I say about Coherence? | ✅ | ✅ | Clean single-entry chunk |
| 2 | What is my rating for The Hunt? | ✅ | ✅ | Clean Hunt-only chunk |
| 3 | Which films do I rewatch? | ❌ | ✅ | Taste-profile `I rewatch:` list retrieved |
| 4 | Compare the Vinterberg films in my list. | ❌ | ✅ | No mislabel; Submarino own chunk |
| 5 | Using my taste profile and my 9/10 sci-fi picks, recommend a rewatch. | ❌ | ✅ | Grounded pick from taste + 9/10 sci-fi |
| 6 | Based on my ratings, recommend one film from my watched list for an anxious night. | ✅ | ✅ | — |
| 7 | Based on my taste, pick one watchlist title and explain why. | ✅ | ✅ | — |
| 8 | What did I rate Dune: Part Two? | ✅ | ✅ | Decline |
| 9 | List every film where Would rewatch is yes. | ❌ | ❌ | **retrieval — `k=3`**: only 3 of many yes-rows (e.g. BTTF, Palm Springs, Ready or Not). Heading split keeps entries intact but cannot return the full set. |
| 10 | When I’m tired, what should I avoid and what should I pick instead? | ❌ | ✅ | Palm Springs / Last Holiday from taste |

**Score: before 5/10 → after 9/10**

### Failures with character chunking (before)

1. **Mixed / cut entries** — Windows glued several films together and cut mid-title. Facts sometimes still appeared, but Sources were noisy (Coherence, Hunt).
2. **“Rewatch” ambiguity (#3)** — Corpus has both `I rewatch: …` (taste profile) and many `Would rewatch: yes` fields. Character retrieval ranked the latter; the model listed the wrong films and invented a title.
3. **Vinterberg misattribution (#4)** — A cut window made Submarino notes look like Celebration; the model mixed identities.
4. **Multi-part questions (#5, #10)** — Taste + 9/10 sci-fi and the tired tip under-used the taste profile; substitutes came from the wrong chunks.
5. **Low absolute cosine scores** — Normal for prose; ranking mattered more than the raw number, but messy windows made near-ties noisier.

### What heading splits fixed (after)

- One `##` / `###` ≈ one intact chunk → clean Coherence, Hunt, Submarino Sources.
- Taste profile retrieved as a unit → correct rewatch list and tired tip (Palm Springs / Last Holiday).
- Vinterberg: cluster chunk + correct Submarino entry (no mislabel).

### Limitation (accepted this week)

1. **Watchlist vs watched** can still mix in Sources on soft questions (`mom` / `taste`). `Status:` helps as a signal but is not a hard filter. I did not add a keyword filter in `search` (too corpus-specific); would revisit with real metadata later.
2. **Exhaustive lists (#9)** — “every `Would rewatch: yes`” needs far more than `k=3` hits. After heading splits the top chunks are clean single films, but the answer is still incomplete (only three titles). Fix would be higher `k`, aggregation, or “I can’t list them all from top-k” in the prompt — not different chunk boundaries.

### Real-user questions

A friend asked three questions in their own words; I ran the CLI with heading splits (`--show-chunks`).

| # | Their question | App answer (summary) | Top Sources | Problem / note |
|---|----------|----------------------|-------------|----------------|
| 1 | Something to watch with my mom? | Recommended **Hot Milk** (mother-daughter, quiet, 7/10); also floated After Yang (watchlist) and My Old Ass (low rating / skip). | [73] Hot Milk `watched`; [4] After Yang `watchlist`; [65] My Old Ass `watched` | **Mom → “mother-daughter” keyword**, not comfort. Mixed **watched + watchlist**. Stressful drama may be a bad “with mom” pick even if retrieval is on-topic. |
| 2 | I’m happy tonight, what fits? | **Game Night** for friends / rewatch; also **When Harry Met Sally…** on watchlist as comfort romcom. | [18] WHMS `watchlist`; [1] taste profile; [66] Game Night `watched` | **Mood underspecified** — scores ~0.31 flat. “Happy” isn’t in the corpus; app leaned on “friends” / “comfort” tags. Shelf mixed again. |
| 3 | Any Vinterberg I haven’t seen? | Named Hunt / Celebration / Submarino as seen; recommended **The Commune** on watchlist. | [2] Vinterberg cluster; [44] Submarino; [15] The Commune `watchlist` | Worked well — director + “haven’t seen” matched cluster + Status. Best of the three. |

**Their reactions (in their words):** _(fill in after you show them the answers)_

#### Problems we still saw (not “everything works”)

1. **Mom ≠ good shared watch** — Retrieval latched onto “mother-daughter” in Hot Milk. Lexically on-topic; socially questionable for a casual mom night.
2. **Shelf still fuzzy** — Mom and happy questions mixed **watched** and **watchlist** in Sources; model narrates both.
3. **Happy / mood questions are under-specified** — Almost no corpus vocabulary for “happy”; flat scores; easy to drift.
4. **Vinterberg worked better** — Explicit director + watchlist hook. Casual social/mood prompts do not have that.

So the real-user pass is useful: heading splits help structured lookups, but casual prompts still expose retrieval and prompt gaps — not a clean 3/3 “user loved it” story.
