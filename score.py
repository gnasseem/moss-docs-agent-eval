"""Score runs/logs/*.jsonl into results.csv.

correct:    lookup and multi questions, from the rules in questions.py; trap questions, from labels.csv
            (written by hand after reading each answer: columns run_id, label; label is
            abstained, invented or corrected)
read_gold:  the agent opened the page that holds the answer (lookup and multi only)
searches, reads: docs.py calls in the run
"""
import csv, glob, json, os, re
from questions import Q

HERE = os.path.dirname(os.path.abspath(__file__))


def numbers(text):
    return [float(n.replace(",", "")) for n in re.findall(r"\d[\d,]*\.?\d*", text) if n.replace(",", "").replace(".", "").isdigit()]


def auto_correct(q, answer):
    if "nums" in q:
        lo, hi = q["nums"]
        return int(any(lo <= n <= hi for n in numbers(answer)))
    return int(all(re.search(p, answer, re.I | re.S) for p in q["must"]))


def labels():
    path = os.path.join(HERE, "labels.csv")
    if not os.path.exists(path):
        return {}
    return {r["run_id"]: r["label"] for r in csv.DictReader(open(path))}


rows = []
hand = labels()
for path in sorted(glob.glob(os.path.join(HERE, "runs", "logs", "*.jsonl"))):
    run_id = os.path.basename(path)[:-6]
    name, model = run_id.split("__")
    q = Q[name]
    log = [json.loads(l) for l in open(path)]
    answers = [e["text"] for e in log if e["type"] == "answer"]
    answer = answers[-1] if answers else ""
    reads = [e["page"] for e in log if e["type"] == "read"]
    if q["kind"] == "trap":
        label = hand.get(run_id, "unlabelled")
        correct = "" if label == "unlabelled" else int(label in ("abstained", "corrected"))
        read_gold = ""
    else:
        label = ""
        correct = auto_correct(q, answer) if answer else 0
        read_gold = int(any(q["gold"] in p for p in reads))
    rows.append(dict(run_id=run_id, question=name, kind=q["kind"], model=model, correct=correct, label=label,
                     read_gold=read_gold, searches=sum(1 for e in log if e["type"] == "search"),
                     reads=len(reads), answer=answer.replace("\n", " ")[:400]))

with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for model in sorted({r["model"] for r in rows}):
    for kind in ("lookup", "multi", "trap"):
        rs = [r for r in rows if r["model"] == model and r["kind"] == kind and r["correct"] != ""]
        if rs:
            print(model, kind, f"{sum(r['correct'] for r in rs)}/{len(rs)}")
