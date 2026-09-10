---
workflow: product-launch-video
flow: automation
storyboard: no
mode: autonomous
destination: blog embed, YouTube, X
aspect: 1920x1080
length: 30-60s
language: en
narration: no
---

# BRIEF - jot product demo

## Message

Your judgment is already written down. It is sitting in your coding agents'
session logs, in every correction you ever typed, and it can be extracted and
handed to any agent.

## Angle

**Proof over promise.** The video does not claim the skill works; it shows the
measurement that proves it. The arc is: the logs exist -> one correction becomes
one rule -> a blind benchmark scores it -> the number.

Basis: the whole project's credibility rests on the benchmark, and the single
most quotable finding is that mined rules scored full marks while reasoned-in
rules scored zero. That is the ending.

## Intent

Sell, not show. There is no website to capture and no crawl: the source is a
local repository. **No-capture mode** - every asset is authored, using the real
content from `D:\Projects\jot`.

## Audience

Developers who run several coding agents and are tired of re-explaining the
same preferences to each one.

## Customizations

- **Emulated terminal component.** Not a screen recording. A designed terminal
  that types and runs the real commands, so type size and pacing are controlled.
- **Markdown file mockups.** The rule shown as a rendered file card, with its
  Do / Because / Not when / Evidence lines legible.
- **Benchmark table.** The three scores as a designed table, not terminal text.
- Silent. Burned-in captions carry the narration; muted autoplay is the norm.

## Design constraints, from the subject's own recorded rules

These are non-negotiable and come from `VOICE.md` and `FRONTEND.md` in the
source repo:

- **No emojis. No em dashes. No unicode punctuation.** ASCII only, everywhere.
- Monochrome, matching harjotrana.com: near-white `#FAFAFA` ground, near-black
  `#1A1A1A` ink, one accent used sparingly. Pure white blooms on video.
- Typography carries the hierarchy. Separate faces for headings and mono.
- No "generic AI landing page" motion: no centered gradient headline, no
  floating dashboard screenshot, no particle fields.

## Real content the video must use

Nothing invented. All values verified in the source repo on 2026-09-10.

- Corpus: **1,398 judgment events** from **1,290 conversations**, five agents.
  Codex 1,048 - Claude Code 209 - Cursor 110 - Grok 17 - Gemini 14.
  Signals: 505 corrections, 380 preferences, 133 taste calls.
- The mined line, verbatim, 2026-09-01:
  "wait which agents/models are we using for the general-purpose tasks? pls make
  sure they're sonnet 5, never opus or fable (burns my weekly usage and session
  usage a lot), remember this pls"
- The rule it became: `AGENTIC.md` > "Subagents are Sonnet 5. Never Opus. Never
  Fable." with Do / Because / Not when / Evidence.
- Benchmark, set v1, ten decisions, both arms Sonnet 5 in clean rooms:
  control **7/20**, with the skill **13/20**, after one round of fixes **18/20**.
- The closing line: "Every rule I mined from my logs scored full marks. Every
  rule I reasoned my way into scored zero."

## Do not show

- The 20/20 rerun. It is not a fidelity measurement and the blog says so.
- Any client name, colleague name, or internal tool name. The denylist is
  enforced by `scripts/scan_leaks.py` in the source repo.
