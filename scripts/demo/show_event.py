#!/usr/bin/env python3
"""Print one real judgment event from the mined corpus, formatted for screen.

Used by the recorded demo. Reads the live corpus rather than a fixture, so what
appears on camera is whatever is actually in state/evidence right now.
"""

from __future__ import annotations

import json
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS = ROOT / "state" / "evidence" / "corpus-events.jsonl"

DIM = "\033[90m"
FG = "\033[97m"
OFF = "\033[0m"


def main() -> int:
    needle = (sys.argv[1] if len(sys.argv) > 1 else "sonnet").lower()

    if not CORPUS.exists():
        print(f"{DIM}no corpus yet - run scripts/extract_corpus.py first{OFF}")
        return 1

    best = None
    for line in CORPUS.read_text(encoding="utf-8").splitlines():
        ev = json.loads(line)
        said = ev["harjot_said"]
        if needle in said.lower() and len(said) < 400:
            # Highest signal score wins, not shortest. Shortest picked the
            # blandest of two matches here; score is what actually tracks how
            # much judgment a line carries.
            if best is None or ev["score"] > best["score"]:
                best = ev
    if best is None:
        print(f"{DIM}no event matching '{needle}'{OFF}")
        return 1

    print()
    print(f"  {DIM}{best['agent']}  ·  {best['timestamp'][:10]}  ·  signal score {best['score']}{OFF}")
    print()
    for para in best["harjot_said"].strip().splitlines():
        for wrapped in textwrap.wrap(para, width=76) or [""]:
            print(f"  {FG}{wrapped}{OFF}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
