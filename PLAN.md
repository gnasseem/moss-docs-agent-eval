# Plan

Independent project, not affiliated with Moss (usemoss). Question: when a coding or support agent has to answer developer questions from Moss's public documentation (docs.moss.dev, `llms-full.txt`), how often is the answer right, does it open the page that holds the answer, and what does it do when the docs do not say? Built only on the public docs; nothing calls the Moss service and no account or key is used.

## How model calls run

The `claude` CLI is signed out and there is no API key, so each question is one Claude subagent (haiku or sonnet) that is given only a shell tool and two commands: `docs.py` (BM25 search and page read over the local copy of the docs) and `ask.py` (task and answer). `ANTHROPIC_API_KEY` is not used by any script here; the docs tool is plain Python so a re-run with the SDK only needs a loop around the same two commands.

## Checklist

- [x] `docs/`: llms.txt and llms-full.txt fetched 2026-11-25 (not committed; the README has the curl lines)
- [x] `docs.py`: page split, BM25 search, page read, call log
- [x] `questions.py`: 24 questions (12 lookup, 6 multi-step, 6 traps where the docs are silent or the premise is wrong), each with its rule and the page that holds the answer
- [x] `ask.py`, `score.py`
- [x] Runs: haiku and sonnet, all 24 questions
- [x] Hand labels for the trap answers (`labels.csv`)
- [x] `results.csv`
- [x] `FINDINGS.md`: only what the runs produced
- [x] `README.md`
- [ ] Push to gnasseem/moss-docs-agent-eval (the orchestrator does this after checking)

Possible next pass: repeats per question, closed-book baseline, a run through the SDK with an API key, questions on the SDK reference pages.
