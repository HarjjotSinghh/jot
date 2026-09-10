#!/usr/bin/env python3
"""Print the rule that a mined event became, straight out of the knowledge file.

Reads AGENTIC.md live, so the recording shows the real file rather than a copy
that can drift away from it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

DIM = "\033[90m"
FG = "\033[97m"
BOLD = "\033[1m"
OFF = "\033[0m"

DEFAULT = ("AGENTIC.md", "### Subagents are Sonnet 5")


def main() -> int:
    filename, heading = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else DEFAULT
    path = ROOT / filename
    if not path.exists():
        print(f"{DIM}missing {filename}{OFF}")
        return 1

    text = path.read_text(encoding="utf-8")
    start = text.find(heading)
    if start == -1:
        print(f"{DIM}heading not found: {heading}{OFF}")
        return 1
    # Run to the next heading of the same or higher level.
    rest = text[start + len(heading):]
    end = re.search(r"^#{1,3} ", rest, re.M)
    block = heading + (rest[: end.start()] if end else rest)

    print()
    print(f"  {DIM}{filename}{OFF}")
    print()
    for line in block.strip().splitlines():
        line = line.rstrip()
        if line.startswith("###"):
            print(f"  {BOLD}{FG}{line.lstrip('# ')}{OFF}")
        elif line.startswith("- **"):
            label, _, tail = line[2:].partition(":**")
            print(f"  {FG}{label.strip('* ')}:{OFF}{DIM}{tail}{OFF}")
        else:
            print(f"  {DIM}{line}{OFF}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
