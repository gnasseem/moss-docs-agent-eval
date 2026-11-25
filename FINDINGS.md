# Findings

One run per question and model, 48 runs, 24 questions, docs fetched 2026-11-25. No human labels except the six trap questions per model, which were read and labelled by hand (`labels.csv`). Independent project; nothing here calls Moss.

## Result

| model | lookup (12) | multi-step (6) | docs silent or premise wrong (6) |
| --- | --- | --- | --- |
| haiku | 12/12 | 6/6 | 6/6 |
| sonnet | 12/12 | 6/6 | 6/6 |

Both models read the page that holds the answer in 33 of 36 lookup and multi-step runs, after 1 to 2 searches and about 1.5 page reads. The three misses (credits-out on haiku, docs-per-build on both) were answered correctly from a different page that states the same fact. The search tool is plain BM25 over the 209 pages of `llms-full.txt`.

The arithmetic questions came out exactly: memory for 300 indexes of 500 chunks (about 1,194 MiB from the sizing page's formula), the job cost ($0.665), billed retrievals (3), crawl charge ($0.60), session time ($6.00). The range-filter question (a text value against a numeric filter never matches) was answered correctly with the rule from the metadata-filtering page.

On the six questions the docs cannot answer, no run invented a value. Five of six per model said the docs do not give it (Rust crate, uptime percentage, euro price, GDPR and EU region, behaviour of alpha above 1). On the false premise of a 10 MB request body, both corrected it to the 4 MB Inference limit and the 413 status; 10 MB is the Control Plane limit, on a different page. Trap runs took the most reading, 3.5 to 4 pages against 1.5 for a lookup, so the agents searched before saying the answer was absent.

## What the docs leave open

These are the questions where the correct answer was "the docs do not say", so a developer asking an agent gets no figure:

- alpha above 1 in hybrid search: documented from 0.0 to 1.0, non-finite values are rejected (changelog), nothing on 1.5 or 2.0.
- No uptime or latency commitment for Moss Inference; "SLA guarantees" appears only as an Enterprise bullet.
- No GDPR statement and no hosting region; data residency is listed as Enterprise-only.
- No price in a currency other than dollars.

## Limits

The questions are mine and were written from the same docs the agents search, so they test retrieval and reading, not whether the docs are complete. 24 questions is a small set, one run per cell, two models, both at the ceiling, so this shows no difference between haiku and sonnet and no failure to fix. The trap labels are my reading of free-text answers. Each run was one Claude subagent driving `docs.py` and `ask.py` from the shell, see the README.
