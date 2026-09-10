#!/usr/bin/env python3
"""Retime a rendered HyperFrames project to a snappier, motion-design pace.

Two things move together, or the frame desynchronises:

  * every `data-start` / `data-duration` attribute scales by `new/old`
  * the GSAP root timeline gets `timeScale(old/new)`

Scaling only the attributes would leave the animation running past its clip;
scaling only the timeline would leave dead air at the tail. Doing both keeps the
last beat landing exactly where it landed before, just sooner.

Per-frame ratios rather than one global factor: the frames carrying the most
text to read get the gentlest speedup, because "snappy" stops being a virtue the
moment the viewer cannot finish a line.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# frame stem -> (old duration, new duration) in seconds, from the storyboard
PLANS = {
    "jot-promo": {
        "01-the-tax": (7, 4.5),
        "02-the-logs": (11, 7),
        "03-one-rule": (11, 8),      # densest reading in the set, gentlest cut
        "04-benchmark": (10, 6),
        "05-provenance": (9, 5.5),
    },
    "jot-promo-square": {
        "01-the-tax": (7, 4.5),
        "02-the-logs": (11, 7),
        "03-benchmark": (10, 6),
        "04-provenance": (9, 5.5),
    },
}

ATTR = re.compile(r'(data-(?:start|duration)=")([0-9]*\.?[0-9]+)(")')


def fmt(x: float) -> str:
    """Trim trailing zeros so the markup stays readable."""
    return f"{x:.3f}".rstrip("0").rstrip(".") or "0"


def retime(path: Path, old: float, new: float, stem: str) -> str:
    text = path.read_text(encoding="utf-8")
    ratio = new / old
    scale = old / new

    text, n_attr = ATTR.subn(
        lambda m: m.group(1) + fmt(float(m.group(2)) * ratio) + m.group(3), text
    )

    # Insert timeScale immediately before the registration so it applies to the
    # finished timeline, whatever was added to it above.
    reg = re.compile(r'(\n(\s*)window\.__timelines\[")')
    if "timeScale(" in text:
        text = re.sub(r"tl\.timeScale\([0-9.]+\);", f"tl.timeScale({scale:.4f});", text)
        note = "timeScale updated"
    elif reg.search(text):
        text = reg.sub(
            lambda m: f"\n{m.group(2)}tl.timeScale({scale:.4f});  // snappier pace\n"
            + m.group(1).lstrip("\n"),
            text,
            count=1,
        )
        note = "timeScale inserted"
    else:
        note = "NO REGISTRATION FOUND"

    path.write_text(text, encoding="utf-8")
    return f"  {stem:15} {old}s -> {new}s  (x{scale:.2f})  {n_attr} attrs, {note}"


def main() -> int:
    root = Path(__file__).resolve().parent / "videos"
    for project, plan in PLANS.items():
        print(f"\n{project}")
        frames = root / project / "compositions" / "frames"
        for stem, (old, new) in plan.items():
            f = frames / f"{stem}.html"
            if not f.exists():
                print(f"  {stem:15} MISSING")
                continue
            print(retime(f, old, new, stem))

        # The storyboard's own durations must agree, or assemble-index rebuilds
        # the index against the old timings and the cuts land in the wrong place.
        sb = root / project / "STORYBOARD.md"
        text = sb.read_text(encoding="utf-8")
        for stem, (old, new) in plan.items():
            text = re.sub(
                rf"(- src: compositions/frames/{re.escape(stem)}\.html\n- duration: )[0-9.]+s",
                rf"\g<1>{fmt(new)}s",
                text,
            )
        total = sum(new for _, new in plan.values())
        text = re.sub(r"^duration: [0-9.]+s", f"duration: {fmt(total)}s", text, flags=re.M)
        sb.write_text(text, encoding="utf-8")
        print(f"  storyboard total -> {fmt(total)}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
