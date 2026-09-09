#!/usr/bin/env python3
"""
Collate a benchmark run into one side-by-side document for scoring.

  python scripts/bench_score.py --run 20260910-0412

Reads the three answer sheets, interleaves them per question, and writes
COMPARISON.md in the run folder. Scoring itself is a human judgement call against
Harjot's answer; this just puts the three answers next to each other so the call is
easy to make.

If SCORES.md has been filled in, it also totals the columns.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARMS = [
    ("arm-c-harjot", "Harjot (ground truth)"),
    ("arm-b-jot", "B - /jot"),
    ("arm-a-control", "A - control"),
]


def parse_answers(path: Path) -> dict[str, str]:
    """Split an answer sheet into {question-id: answer text}."""
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    parts = re.split(r"^##\s+(Q\d+)", text, flags=re.M)
    # parts = [preamble, 'Q1', body, 'Q2', body, ...]
    for i in range(1, len(parts) - 1, 2):
        body = parts[i + 1]
        # drop the rest of the heading line, keep the answer
        body = body.split("\n", 1)[1] if "\n" in body else ""
        body = body.strip()
        if body and body != "_(answer here)_":
            out[parts[i]] = body
    return out


def total_scores(run: Path) -> str:
    scores = run / "SCORES.md"
    if not scores.exists():
        return ""
    rows = re.findall(r"^\|\s*(Q\d+)\s*\|\s*(-?\d+)?\s*\|\s*(-?\d+)?\s*\|",
                      scores.read_text(encoding="utf-8"), re.M)
    a = [int(x) for _, x, _ in rows if x]
    b = [int(x) for _, _, x in rows if x]
    if not a and not b:
        return ""
    n = len(rows) * 2
    lines = ["", "## Totals", ""]
    if a:
        lines.append(f"- **A (control):** {sum(a)}/{n}")
    if b:
        lines.append(f"- **B (/jot):** {sum(b)}/{n}")
    if a and b:
        lines.append(f"- **Delta:** {sum(b) - sum(a):+d} - what the skill is carrying")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    args = ap.parse_args()

    run = REPO / "bench" / "runs" / args.run
    if not run.is_dir():
        print(f"no such run: {run}")
        return 1

    questions = (run / "questions.md").read_text(encoding="utf-8")
    titles = dict(
        (m.group(1), m.group(0).lstrip("# ").strip())
        for m in re.finditer(r"^##\s+(Q\d+)[^\n]*", questions, re.M)
    )
    bodies = {}
    for qid, block in zip(
        re.findall(r"^##\s+(Q\d+)", questions, re.M),
        re.split(r"^##\s+Q\d+[^\n]*\n", questions, flags=re.M)[1:],
    ):
        bodies[qid] = block.split("---")[0].strip()

    answers = {key: parse_answers(run / f"{key}.md") for key, _ in ARMS}
    missing = [k for k, _ in ARMS if not answers[k]]
    if missing:
        print(f"warning: no answers yet in {', '.join(missing)}")

    out = [f"# Comparison - run {args.run}", ""]
    for qid in titles:
        out += [f"## {titles[qid]}", "", bodies.get(qid, ""), ""]
        for key, label in ARMS:
            out += [f"**{label}**", "", answers[key].get(qid, "_(no answer)_"), ""]
        out += ["---", ""]
    out.append(total_scores(run))

    dest = run / "COMPARISON.md"
    dest.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {dest}")
    for key, label in ARMS:
        print(f"  {label:24} {len(answers[key])} answers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
