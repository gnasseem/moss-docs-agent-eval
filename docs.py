"""Docs tool the agent under test uses from the shell (reads docs/llms-full.txt, the public Moss docs).

    python docs.py search '<query>'     top 5 pages by BM25: number, title, URL
    python docs.py read <number>        print one page
Every call is appended to runs/logs/<run_id>.jsonl when DOCS_RUN_ID is set.
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = open(os.path.join(HERE, "docs", "llms-full.txt"), encoding="utf-8").read()


def load_pages():
    parts = re.split(r"\n(?=# [^\n]*\nSource: )", TEXT)
    pages = []
    for p in parts:
        m = re.match(r"# ([^\n]*)\nSource: (\S+)", p)
        if m:
            pages.append({"title": m.group(1), "url": m.group(2), "text": p})
    return pages


PAGES = load_pages()
TOKENS = [re.findall(r"[a-z0-9_]+", p["text"].lower()) for p in PAGES]
AVG = sum(len(t) for t in TOKENS) / len(TOKENS)


def search(query, k=5):
    q = re.findall(r"[a-z0-9_]+", query.lower())
    scores = []
    for i, toks in enumerate(TOKENS):
        s = 0.0
        for w in set(q):
            tf = toks.count(w)
            if tf:
                df = sum(1 for t in TOKENS if w in t)
                idf = math.log(1 + (len(PAGES) - df + 0.5) / (df + 0.5))
                s += idf * tf * 2.2 / (tf + 1.2 * (0.25 + 0.75 * len(toks) / AVG))
        scores.append((s, i))
    return [i for s, i in sorted(scores, reverse=True)[:k] if s > 0]


def log(entry):
    run_id = os.environ.get("DOCS_RUN_ID")
    if run_id:
        os.makedirs(os.path.join(HERE, "runs", "logs"), exist_ok=True)
        with open(os.path.join(HERE, "runs", "logs", run_id + ".jsonl"), "a") as f:
            f.write(json.dumps(entry) + "\n")


if __name__ == "__main__":
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == "search":
        hits = search(arg)
        log({"type": "search", "query": arg, "pages": [PAGES[i]["url"] for i in hits]})
        for i in hits:
            print(i, PAGES[i]["title"], PAGES[i]["url"])
    elif cmd == "read":
        p = PAGES[int(arg)]
        log({"type": "read", "page": p["url"]})
        print(p["text"])
