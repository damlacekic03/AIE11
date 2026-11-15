# Decisions

One row one decision. This week is the first one. By Week 5 this file will explain what decisions you made during this bootcamp.

## Retrieval, week 1

**What I changed**

> Replaced character-window splitting (1000/200) with heading-based splits on `##` / `###`, so each section or film entry becomes one chunk.

**Why**

> Character splits cut films mid-entry and mixed titles (e.g. Moon + neighbors); lookup questions ranked the wrong window. After heading splits, entries stay intact (e.g. Coherence / Hunt as whole chunks). 

**What would change my mind**

> Heading splits create about one chunk per film, so every question re-embeds the whole catalog and cost grows with N. If the list got much larger, I wouldn't keep doing that blindly — I'd need a different approach to indexing/retrieval at that scale, not just bigger character windows.
