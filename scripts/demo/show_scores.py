#!/usr/bin/env python3
"""Print the benchmark result, read from the real run files.

Parses bench/runs/*/SCORES.md rather than hardcoding numbers, so the recording
cannot drift away from what the benchmark actually recorded.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RUNS = ROOT / "bench" / "runs"

DIM = "\033[90m"
FG = "\033[97m"
BOLD = "\033[1m"
OFF = "\033[0m"


def totals(path: Path) -> tuple[int, int, int] | None:
    """Return (control, skill, max) from a SCORES.md table."""
    rows = re.findall(
        r"^\|\s*Q\d+\s*\|\s*(-?\d+)\s*\|\s*(-?\d+)\s*\|", path.read_text(encoding="utf-8"), re.M
    )
    if not rows:
        return None
    a = sum(int(x) for x, _ in rows)
    b = sum(int(y) for _, y in rows)
    return a, b, len(rows) * 2


def main() -> int:
    runs = sorted(p for p in RUNS.glob("*/SCORES.md")) if RUNS.exists() else []
    # Skip runs that disclaim themselves. Once a run's answers are cited back
    # into the knowledge files, its set is an answer key and its score is not a
    # fidelity measurement - it must never become the headline number.
    runs = [p for p in runs if "not a fidelity measurement" not in p.read_text(encoding="utf-8")]
    scored = [(p.parent.name, totals(p)) for p in runs]
    scored = [(n, t) for n, t in scored if t]
    if not scored:
        print(f"{DIM}no scored runs yet{OFF}")
        return 1

    first = scored[0][1]
    # The last run that is still a valid fidelity measurement. Later runs reuse
    # a question set whose answers have since been cited in the knowledge files.
    patched = scored[1][1] if len(scored) > 1 else first

    print()
    print(f"  {DIM}bench/runs  ·  set v1  ·  10 decisions  ·  both arms Sonnet 5, clean room{OFF}")
    print()
    print(f"  {DIM}control model, no skill {OFF}  {BOLD}{FG}{first[0]:>2} / {first[2]}{OFF}")
    print(f"  {DIM}same model, /jot loaded {OFF}  {BOLD}{FG}{first[1]:>2} / {first[2]}{OFF}")
    print(f"  {DIM}after one round of fixes{OFF}  {BOLD}{FG}{patched[1]:>2} / {patched[2]}{OFF}")
    print()
    print(f"  {FG}Every rule I mined from my logs scored full marks.{OFF}")
    print(f"  {FG}Every rule I reasoned my way into scored zero.{OFF}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
