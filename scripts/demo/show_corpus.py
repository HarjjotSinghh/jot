#!/usr/bin/env python3
"""Print the corpus totals from the last full extractor run."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
STATS = ROOT / "state" / "evidence" / "corpus-stats.json"

DIM, FG, BOLD, OFF = "\033[90m", "\033[97m", "\033[1m", "\033[0m"

LABEL = {"claude": "Claude Code", "codex": "Codex", "cursor": "Cursor",
         "gemini": "Gemini CLI", "grok": "Grok", "opencode": "OpenCode"}


def main() -> int:
    if not STATS.exists():
        print(f"{DIM}no run yet{OFF}")
        return 1
    s = json.loads(STATS.read_text(encoding="utf-8"))
    kept = {k.split(":", 1)[1]: v for k, v in s.items() if k.startswith("kept:")}
    sig = {k.split(":", 1)[1]: v for k, v in s.items() if k.startswith("signal:")}
    conv = sum(v for k, v in s.items() if k.startswith("conv:"))

    print()
    print(f"  {BOLD}{FG}{sum(kept.values()):,}{OFF}{DIM} judgment events from {conv:,} conversations{OFF}")
    print()
    for agent, n in sorted(kept.items(), key=lambda kv: -kv[1]):
        print(f"  {DIM}{LABEL.get(agent, agent):<14}{OFF}{FG}{n:>6,}{OFF}")
    print()
    for name in ("correction", "preference", "taste"):
        if name in sig:
            print(f"  {DIM}{name:<14}{OFF}{FG}{sig[name]:>6,}{OFF}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
