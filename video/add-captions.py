#!/usr/bin/env python3
"""Add a burned-in caption track cued to the actual spoken words.

The shipped captions.mjs exits 0 and writes nothing here, with no diagnostic, so
this builds the track directly from `audio_meta.json` - which carries per-word
start/end times from the TTS pass - and from the frame windows in the assembled
index.

Each spoken line is split at its sentence boundary and each half becomes its own
caption, timed from the first word of that half to shortly after its last. That
is the part hand-guessed windows could not do: a caption now appears exactly when
the sentence is spoken.

Run after assemble-index, which regenerates index.html and drops this layer.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

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

TAIL = 0.28   # how long a caption lingers past its last word
LEAD = 0.10   # how early it appears before the first word


def frame_starts(index_html: str) -> dict[int, float]:
    """Absolute start time of each frame, in storyboard order."""
    starts = {}
    for i, m in enumerate(
        re.finditer(r'data-composition-src="compositions/frames/[^"]+"\s*\n\s*data-start="([0-9.]+)"',
                    index_html), 1):
        starts[i] = float(m.group(1))
    return starts


def split_sentences(words):
    """Split a line's words into sentence groups, keeping their timings."""
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if re.search(r"[.?!]$", w["text"]):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def build(project: pathlib.Path, top: int, width: int, size: int, dark_frames: set[int]):
    index = project / "index.html"
    meta = project / "audio_meta.json"
    if not meta.exists():
        return "no audio_meta.json - run audio.mjs first"

    html = index.read_text(encoding="utf-8")
    if 'class="cap"' in html:
        return "already captioned, skipped"

    starts = frame_starts(html)
    voices = json.loads(meta.read_text(encoding="utf-8"))["voices"]

    cues = []
    for v in voices:
        base = starts.get(v["frame"])
        if base is None:
            continue
        for grp in split_sentences(v["words"]):
            text = " ".join(w["text"] for w in grp).strip()
            a = round(base + grp[0]["start"] - LEAD, 3)
            b = round(base + grp[-1]["end"] + TAIL, 3)
            cues.append((a, b, text, v["frame"]))

    html = html.replace("    </style>",
                        CSS % {"top": top, "width": width, "size": size} + "    </style>", 1)

    divs, tweens = [], []
    for i, (a, b, text, frame) in enumerate(cues, 1):
        cls = "cap cap-dark" if frame in dark_frames else "cap"
        divs.append(f'      <div id="cap-{i}" class="{cls} clip" data-start="{a}" '
                    f'data-duration="{round(b - a, 3)}" data-track-index="2">{text}</div>')
        tweens.append(
            f'        tl.fromTo("#cap-{i}", {{ opacity: 0, y: 8 }}, '
            f'{{ opacity: 1, y: 0, duration: 0.2, ease: "power2.out" }}, {a});\n'
            f'        tl.to("#cap-{i}", {{ opacity: 0, duration: 0.14, ease: "power2.in" }}, '
            f'{round(b - 0.14, 3)});')

    html = html.replace("\n    </div>\n\n    <script>",
                        "\n\n" + "\n".join(divs) + "\n    </div>\n\n    <script>", 1)

    block = ('      // -- captions, cued to the spoken words in audio_meta.json --\n'
             '      (function () { var tl = window.__timelines["main"];\n'
             + "\n".join(tweens) + "\n      })();\n")
    # Append after the transitions IIFE closes, never inside it.
    anchor = re.search(r"([ \t]*tl\.to\(\{\}, \{ duration: [0-9.]+ \}, 0\);[^\n]*\n[ \t]*\}\)\(\);\n)", html)
    if not anchor:
        return "could not find the timeline anchor"
    html = html.replace(anchor.group(1), anchor.group(1) + block, 1)

    index.write_text(html, encoding="utf-8")
    opens, closes = html.count("(function ()"), html.count("})();")
    return (f"{len(cues)} captions, IIFE {opens}/{closes} "
            f"{'balanced' if opens == closes else 'MISMATCH'}")


def main() -> int:
    root = pathlib.Path(__file__).resolve().parent / "videos"
    for proj, top, width, size in (("jot-promo", 946, 1500, 40),
                                   ("jot-promo-square", 952, 940, 36)):
        print(f"{proj}: {build(root / proj, top, width, size, dark_frames={1})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
