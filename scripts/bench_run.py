#!/usr/bin/env python3
"""
Scaffold a benchmark run: one folder, the question set, three empty answer sheets,
and the exact prompts for the two clean-room model arms.

  python scripts/bench_run.py --set v1

Nothing here calls a model. The arms are filled by real sessions - a fresh one per
arm - because a session that helped build the knowledge files already knows the
answers and would score the skill artificially high.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ARM_PROMPTS = {
    "arm-a-control": """\
# Arm A - control (no skill)

Run this in a **fresh session with no access to the jot repository** and no memory
of how it was built.

> You are answering as a competent senior full-stack engineer. Below are ten
> decisions from real client work. Answer each in three or four sentences: the call
> first, then why. Commit to an answer; do not hedge. Write your answers into
> `arm-a-control.md` under the matching headings, and print nothing else.
>
> <paste questions.md here>
""",
    "arm-b-jot": """\
# Arm B - treatment (/jot loaded)

Run this in a **fresh session** that has not seen the conversation where the
knowledge files were written.

> Load the `jot` skill from `{repo}` - read `skills/jot/SKILL.md` and follow it,
> including `ENTRY.md`, `PRINCIPLES.md`, the domain files its routing table selects,
> and the private layer if present.
>
> Then answer the ten decisions below **as Harjot would decide them**. Three or four
> sentences each: the call, then why, in his terms. Commit to an answer. If the
> knowledge base genuinely does not cover something, say so rather than inventing a
> preference - an honest gap scores better than a fabrication.
>
> Write your answers into `arm-b-jot.md` under the matching headings, and print
> nothing else.
>
> <paste questions.md here>
""",
    "arm-c-harjot": """\
# Arm C - ground truth (Harjot)

Answer these yourself, **before** reading either model arm. Three or four sentences
each: what you'd actually do, and why. Not what you think you should do - what you
would actually do on a normal Tuesday.

Where your answer depends on something the question left out, say what it depends
on and then answer for the most likely case.
""",
}


def split_questions(text: str) -> list[str]:
    return [h.strip() for h in re.findall(r"^##\s+(Q\d+.*)$", text, re.M)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="v1")
    ap.add_argument("--label", default="")
    args = ap.parse_args()

    qpath = REPO / "bench" / "questions" / f"{args.set}.md"
    if not qpath.exists():
        print(f"no such question set: {qpath}")
        return 1
    questions_md = qpath.read_text(encoding="utf-8")
    headings = split_questions(questions_md)
    if not headings:
        print("question set has no '## Qn' headings")
        return 1

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    name = f"{stamp}-{args.label}" if args.label else stamp
    run = REPO / "bench" / "runs" / name
    run.mkdir(parents=True, exist_ok=True)

    (run / "questions.md").write_text(questions_md, encoding="utf-8")

    for arm, prompt in ARM_PROMPTS.items():
        body = [prompt.format(repo=REPO), "", "---", ""]
        for h in headings:
            body += [f"## {h}", "", "_(answer here)_", ""]
        (run / f"{arm}.md").write_text("\n".join(body), encoding="utf-8")

    (run / "SCORES.md").write_text(
        f"# Scores - run {name}\n\n"
        f"Set `{args.set}`, {len(headings)} questions. "
        "2 = same call and reason, 1 = same call or acceptable alternative, "
        "0 = different call, -1 = fabricated a preference or broke a boundary.\n\n"
        "| Q | A control | B /jot | Note |\n|---|---|---|---|\n"
        + "".join(f"| {h.split(chr(8212))[0].split('-')[0].strip()} |  |  |  |\n" for h in headings)
        + "\n**Totals:** A `__`/%d, B `__`/%d\n" % (2 * len(headings), 2 * len(headings)),
        encoding="utf-8",
    )

    print(f"run: {run}")
    print(f"{len(headings)} questions, set {args.set}")
    print("\nnext:")
    print("  1. fill arm-a-control.md and arm-b-jot.md from two CLEAN sessions")
    print("  2. give Harjot questions.md only; he fills arm-c-harjot.md")
    print(f"  3. python scripts/bench_score.py --run {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
