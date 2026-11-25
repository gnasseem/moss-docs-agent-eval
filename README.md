# moss-docs-agent-eval

An independent, small project: can an agent answer developer questions from Moss's public documentation, does it find the right page, and what does it do when the docs do not say? 24 questions (12 single-fact lookups, 6 that need arithmetic or two pages, 6 where the docs are silent or the question's premise is wrong) are put to an agent that has only a search and a page-read command over `llms-full.txt` from docs.moss.dev. Not affiliated with or endorsed by Moss. It uses only the public docs; nothing calls the Moss service and no account or key is needed.

- `docs.py`: splits `llms-full.txt` into 209 pages; BM25 `search` and `read`; logs every call.
- `questions.py`: the 24 questions, the rule that scores each, and the page that holds the answer.
- `ask.py`: prints the question and records the answer.
- `score.py`: reads `runs/logs/`, writes `results.csv`.
- `labels.csv`: hand labels for the trap answers.
- `FINDINGS.md`: the results.

## Run it

```
mkdir docs
curl -sL https://docs.moss.dev/llms-full.txt -o docs/llms-full.txt
curl -sL https://docs.moss.dev/llms.txt -o docs/llms.txt
python docs.py search 'rate limit requests per minute'
python docs.py read 56
python ask.py task rpm__haiku
python ask.py answer rpm__haiku '120 sustained, 10 burst'
python score.py
```

Run ids are `<question>__<model>`; set `DOCS_RUN_ID` to the run id when calling `docs.py` so searches and reads are logged. To re-run with the SDK, give the model `docs.py search` and `docs.py read` as tools, set `ANTHROPIC_API_KEY`, and write the same log lines. The docs change, so figures in `questions.py` match the copy fetched on 2026-11-25.

## How the published results were produced

No API key was used. Each run was one Claude subagent (haiku or sonnet) given only the shell commands above and the question; it was not told that some questions have no answer in the docs. The logs in `runs/logs/` have the same shape a loop through the SDK would write.

## What it found

See `FINDINGS.md`: both models answered all 18 answerable questions correctly and, on the 6 the docs cannot answer, said so (or corrected the premise) rather than inventing a value. The cases where the docs give no answer are listed there. One run per question and model, questions written by me from the same docs.
