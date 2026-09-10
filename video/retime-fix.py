#!/usr/bin/env python3
"""Correct the retime: scale GSAP time VALUES, not timeScale().

The first attempt used `tl.timeScale(n)`, which is wrong for this renderer.
HyperFrames renders deterministically by SEEKING the paused timeline, and
GSAP's `seek()` takes local timeline time - `timeScale` only affects playback
rate, so a seek-based render ignores it entirely. The animation kept its
original 10s span inside a clip that had been shortened to 6.5s, so the last
scene was still building when the clip ended and the crossfade took over.

The fix is to scale the numbers the timeline is actually built from:
durations, delays, staggers, position parameters, and any bare arrays of cue
times. `data-start` / `data-duration` were already scaled correctly by the
first pass, so only the script block changes here.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RATIOS = {
    "jot-promo": {
        "01-the-tax": 4.5 / 7,
        "02-the-logs": 7 / 11,
        "03-one-rule": 8 / 11,
        "04-benchmark": 6 / 10,
        "05-provenance": 5.5 / 9,
    },
    "jot-promo-square": {
        "01-the-tax": 4.5 / 7,
        "02-the-logs": 7 / 11,
        "03-benchmark": 6 / 10,
        "04-provenance": 5.5 / 9,
    },
}

# Named time properties inside a tween vars object.
PROP = re.compile(r"\b(duration|delay|stagger|repeatDelay)(\s*:\s*)([0-9]*\.?[0-9]+)")
# A trailing position parameter: the last argument of a tl.<method>(...) call,
# written as a bare number just before the closing paren.
POS = re.compile(r"(,\s*)([0-9]*\.?[0-9]+)(\s*\)\s*;)")
# Arrays of cue times, e.g. var rowStarts = [1.9, 2.05, 2.2];
CUES = re.compile(r"(=\s*\[)([0-9.,\s]+)(\];)")


def fmt(x: float) -> str:
    return f"{x:.4f}".rstrip("0").rstrip(".") or "0"


def scale_script(script: str, r: float) -> tuple[str, int]:
    n = 0

    def prop(m):
        nonlocal n
        n += 1
        return m.group(1) + m.group(2) + fmt(float(m.group(3)) * r)

    def pos(m):
        nonlocal n
        n += 1
        return m.group(1) + fmt(float(m.group(2)) * r) + m.group(3)

    def cues(m):
        nonlocal n
        parts = [p.strip() for p in m.group(2).split(",") if p.strip()]
        if not all(re.fullmatch(r"[0-9]*\.?[0-9]+", p) for p in parts):
            return m.group(0)
        n += len(parts)
        return m.group(1) + ", ".join(fmt(float(p) * r) for p in parts) + m.group(3)

    script = PROP.sub(prop, script)
    script = POS.sub(pos, script)
    script = CUES.sub(cues, script)
    return script, n


def main() -> int:
    root = Path(__file__).resolve().parent / "videos"
    for project, plan in RATIOS.items():
        print(f"\n{project}")
        for stem, r in plan.items():
            p = root / project / "compositions" / "frames" / f"{stem}.html"
            if not p.exists():
                print(f"  {stem:15} MISSING")
                continue
            text = p.read_text(encoding="utf-8")

            # Drop the ineffective timeScale line from the first attempt.
            text, removed = re.subn(r"[ \t]*tl\.timeScale\([0-9.]+\);[^\n]*\n", "", text)

            # Only touch the script block; markup timings are already correct.
            blocks = list(re.finditer(r"<script>(.*?)</script>", text, re.S))
            total = 0
            for m in reversed(blocks):
                scaled, n = scale_script(m.group(1), r)
                total += n
                text = text[: m.start(1)] + scaled + text[m.end(1) :]

            p.write_text(text, encoding="utf-8")
            print(f"  {stem:15} x{r:.3f}  {total} time values scaled, "
                  f"{removed} timeScale line(s) removed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
