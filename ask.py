"""What the agent under test runs from the shell, with docs.py:

    python ask.py task <run_id>               print the question
    python ask.py answer <run_id> '<answer>'  record the final answer
run_id is <question>__<model>. Searches and page reads go to runs/logs/<run_id>.jsonl through DOCS_RUN_ID.
"""
import json, os, sys
from questions import Q

HERE = os.path.dirname(os.path.abspath(__file__))
cmd, run_id = sys.argv[1], sys.argv[2]
path = os.path.join(HERE, "runs", "logs", run_id + ".jsonl")
os.makedirs(os.path.dirname(path), exist_ok=True)
if cmd == "task":
    print(Q[run_id.split("__")[0]]["q"])
elif cmd == "answer":
    with open(path, "a") as f:
        f.write(json.dumps({"type": "answer", "text": sys.argv[3]}) + "\n")
    print("recorded")
