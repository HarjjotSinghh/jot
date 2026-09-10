#!/usr/bin/env python3
"""Add a burned-in caption track to an assembled HyperFrames index.

The shipped caption pipeline derives word timings from `audio_meta.json`, which
only exists when a project has narration. This project is silent by design, so
that file is never written and `captions.mjs` silently no-ops - which is how a
video that was specified as "silent with burned-in captions" ended up with no
text at all.

Captions here are cued off the frame windows in the assembled index instead.
Each line is its own `class="clip"` element on its own track, faded by the main
timeline, sitting in the band below the content keep-out.
"""

from __future__ import annotations

import pathlib
import re
import sys

# (start, end, text). Times are absolute seconds on the master timeline, cued to
# sit inside their frame's window and clear before the next crossfade.
MASTER = [
    (1.20, 4.30, "You have told your agents the same thing a hundred times"),
    (5.30, 8.20, "Every one of those corrections is sitting in a log file"),
    (8.20, 11.30, "This reads all of them"),
    (12.30, 15.00, "One thing you typed once becomes a rule"),
    (15.00, 19.30, "with its reason, and the case where it does not apply"),
    (20.20, 22.80, "Then test it blind against yourself"),
    (22.80, 25.30, "Ten real decisions, answers sealed"),
    (26.10, 28.40, "Every rule mined from the logs scored full marks"),
    (28.40, 30.30, "Every rule I reasoned my way into scored zero"),
]

SQUARE = [
    (1.20, 4.30, "You have told your agents the same thing a hundred times"),
    (5.30, 8.20, "Every one of those corrections is sitting in a log file"),
    (8.20, 11.30, "This reads all of them"),
    (12.30, 14.80, "Then test it blind against yourself"),
    (14.80, 17.30, "Ten real decisions, answers sealed"),
    (18.10, 20.30, "Every rule mined from the logs scored full marks"),
    (20.30, 22.30, "Every rule I reasoned my way into scored zero"),
]

CSS = """
      /* Captions. Plain type on the ground colour, no pill: the preset's
         rounded caption chip would be a rounded card sitting on the rounded
         terminal card, which this project's design rules forbid. */
      .cap {
        position: absolute;
        left: 50%%;
        transform: translateX(-50%%);
        top: %(top)spx;
        width: %(width)spx;
        text-align: center;
        font-family: "Inter", system-ui, sans-serif;
        font-size: %(size)spx;
        font-weight: 400;
        line-height: 1.35;
        letter-spacing: -0.005em;
        color: #1A1A1A;
        opacity: 0;
      }
      .cap-dark { color: #FAFAFA; }
"""


def build(index: pathlib.Path, cues, top, width, size, dark_until):
    html = index.read_text(encoding="utf-8")
    if 'class="cap"' in html:
        return "already has captions, skipped"

    html = html.replace(
        "    </style>", CSS % {"top": top, "width": width, "size": size} + "    </style>", 1
    )

    divs = []
    tweens = []
    for i, (a, b, text) in enumerate(cues, 1):
        # Frame 1 is the only shot on a dark ground; its caption inverts.
        cls = "cap cap-dark" if b <= dark_until else "cap"
        divs.append(
            f'      <div id="cap-{i}" class="{cls} clip" data-start="{a}" '
            f'data-duration="{round(b - a, 3)}" data-track-index="2">{text}</div>'
        )
        # In fast, out faster: a caption that lingers reads as a subtitle bug.
        tweens.append(
            f'        tl.fromTo("#cap-{i}", {{ opacity: 0, y: 8 }}, '
            f'{{ opacity: 1, y: 0, duration: 0.22, ease: "power2.out" }}, {a});\n'
            f'        tl.to("#cap-{i}", {{ opacity: 0, duration: 0.16, '
            f'ease: "power2.in" }}, {round(b - 0.16, 3)});'
        )

    html = html.replace(
        "\n    </div>\n\n    <script>",
        "\n\n" + "\n".join(divs) + "\n    </div>\n\n    <script>",
        1,
    )

    block = (
        "      // -- captions (cued off frame windows; this project is silent) --\n"
        "      (function () { var tl = window.__timelines[\"main\"];\n"
        + "\n".join(tweens)
        + "\n      })();\n"
    )
    html = html.replace(
        '        tl.to({}, { duration:', block + '      (function () { var tl = window.__timelines["main"];\n'
        '        tl.to({}, { duration:', 1
    )
    index.write_text(html, encoding="utf-8")
    return f"{len(cues)} captions injected"


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent / "videos"
    jobs = [
        ("jot-promo", MASTER, 946, 1500, 40, 4.5),
        ("jot-promo-square", SQUARE, 952, 940, 36, 4.5),
    ]
    for proj, cues, top, width, size, dark in jobs:
        idx = root / proj / "index.html"
        print(f"{proj}: {build(idx, cues, top, width, size, dark)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
