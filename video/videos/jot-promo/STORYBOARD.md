---
format: 1920x1080
duration: 31s
message: Your engineering judgment is already written down, in your coding agents' logs. jot extracts it into a skill any agent can load.
arc: Hook -> Mechanism -> Proof -> Payoff
audience: Developers running several coding agents who are tired of re-explaining the same preferences to each one
mode: autonomous
music: none
---

## Frame 1 - The tax

- status: animated
- src: compositions/frames/01-the-tax.html
- duration: 4.5s
- transition_in: cut
- scene: The same correction typed at four different agents, stacking up
- voiceover: "You have told your agents the same thing a hundred times."
- type: hook
- persuasion: Pain agitation
- beat: recognition
- blueprint: kinetic-type-beats (Adapt)
- focal: authored/log-lines
- roles: log-lines = cutout - agent labels = supporting - ground = background
- poster: 5

Adapt: keep the in-place token swap as the signature move, but the token that
swaps is the **agent name** while the corrected instruction stays fixed. That is
the whole problem in one image: same judgment, retyped forever.

Scene 1 (0.0-1.6s): near-black ground. One mono line types in at optical centre,
left-aligned in a 900px measure: `never opus or fable - burns my weekly usage`.
Caret blinks. Nothing else on screen.
Scene 2 (1.6-3.4s): a small label springs in above the line - `claude code`.
`spring-pop-entrance`, 180ms, from y+8.
Scene 3 (3.4-5.2s): the label token swaps in place - `codex`, then `cursor`,
then `grok` - hard cuts at 450ms intervals, `discrete-text-sequence`. The mono
line beneath never moves. This is the signature move.
Scene 4 (5.2-7.0s): the four labels are now stacked as a quiet column at right,
all four visible at once. Caption line resolves. Held read, no camera.

## Frame 2 - The logs already have it

- status: animated
- src: compositions/frames/02-the-logs.html
- duration: 7s
- transition_in: crossfade
- scene: A terminal runs the extractor across five agent stores and lands on the count
- voiceover: "Every one of those corrections is sitting in a log file. This reads all of them."
- type: mechanism
- persuasion: Mechanism reveal
- beat: relief
- blueprint: prompt-type-submit-generate (Reproduce)
- focal: authored/terminal
- roles: terminal = cutout - agent counts = supporting - ground = background
- poster: 8

The terminal is a designed component, not a screenshot: `#FAFAFA` surface, one
hairline border, a title bar reading `jot`, mono at a size that survives a phone.

Scene 1 (0.0-1.2s): the terminal window springs up from 0.96 scale, centred,
1360px wide. Empty prompt, caret blinking. `spring-pop-entrance`.
Scene 2 (1.2-3.2s): the command types character by character with human jitter:
`python scripts/extract_corpus.py`. Caret holds one beat. Return.
Scene 3 (3.2-5.6s): status theater - five store paths stream in as dim rows,
one per 240ms, `waterfall-entry`. Each row is a real path: `~/.claude/projects`,
`~/.codex/sessions`, `~/.grok/sessions`, `~/.gemini/tmp`, `Cursor/state.vscdb`.
Scene 4 (5.6-8.4s): the rows resolve into a right-aligned count column, each
number counting up to its real value - Codex 1,048, Claude Code 209, Cursor 110,
Grok 17, Gemini 14. `counting-dynamic-scale`, staggered 120ms.
Scene 5 (8.4-11.0s): one line lands beneath the rule: `1,398 judgment events`
at display size, cobalt. The terminal holds. No camera move.

## Frame 3 - One correction, one rule

- status: animated
- src: compositions/frames/03-one-rule.html
- duration: 8s
- transition_in: crossfade
- scene: A raw log line on the left becomes a written rule card on the right
- voiceover: "One thing you typed once becomes a rule, with its reason and its limit."
- type: key_feature
- persuasion: Proof of mechanism
- beat: click
- blueprint: grid-card-assemble (Adapt)
- focal: authored/rule-card
- roles: log-line = cutout - rule-card = cutout - ground = background
- poster: 8

Adapt: keep the staggered cascade as the signature move, but the cascade is the
four lines of one markdown file rather than N tiles in a grid. The left half
holds the raw evidence the whole time so the transformation stays legible.

Scene 1 (0.0-2.2s): left column only, 40% width. The verbatim mined line sits as
raw log text, dim mono, wrapped at 44ch, with `claude - 2026-09-01` above it:
"wait which agents/models are we using for the general-purpose tasks? pls make
sure they're sonnet 5, never opus or fable (burns my weekly usage and session
usage a lot), remember this pls"
Scene 2 (2.2-3.4s): a hairline connector draws left to right, `svg-path-draw`,
900ms. The right half is still empty.
Scene 3 (3.4-4.6s): the file card springs in at right, 52% width - a markdown
file mockup with a filename chrome bar reading `AGENTIC.md`. Empty body.
Scene 4 (4.6-9.0s): the four rule lines cascade in, 520ms apart,
`waterfall-entry`, each with its label in ink and its body in grey:
**Subagents are Sonnet 5. Never Opus. Never Fable.** then Do, Because,
Not when, Evidence.
Scene 5 (9.0-11.0s): the `Evidence` line's date `2026-09-01` and the date above
the raw log line both mark in cobalt for 400ms, tying the two halves together.
Held read.

## Frame 4 - Then prove it

- status: animated
- src: compositions/frames/04-benchmark.html
- duration: 6s
- transition_in: crossfade
- scene: A benchmark table fills in - control, with the skill, after fixes
- voiceover: "Then test it blind against yourself. Ten real decisions."
- type: proof
- persuasion: Evidence
- beat: verdict
- blueprint: dataviz-countup (Reproduce)
- focal: authored/bench-table
- roles: bench-table = cutout - method line = supporting - ground = background
- poster: 8

Scene 1 (0.0-1.8s): a method line types in at top, small mono, dim:
`set v1 - 10 decisions - both arms Sonnet 5 - clean room - answers sealed`.
Scene 2 (1.8-3.0s): the table frame draws on - two hairline rules, three empty
rows. `svg-path-draw`, 700ms. Row labels fade in at left.
Scene 3 (3.0-4.6s): row 1 resolves. `control model, no skill` and the number
counts 0 to 7. `counting-dynamic-scale`. A bar fills to 35% behind it.
Scene 4 (4.6-6.2s): row 2. `same model, /jot loaded` counts 0 to 13, bar to 65%.
Scene 5 (6.2-8.0s): row 3. `after one round of fixes` counts 0 to 18, bar to
90%, and this bar alone is cobalt. The count-up is the signature move.
Scene 6 (8.0-10.0s): held. No camera. The three numbers read as a column.

## Frame 5 - Where the score came from

- status: animated
- src: compositions/frames/05-provenance.html
- duration: 5.5s
- transition_in: crossfade
- scene: Mined rules scored full marks, reasoned-in rules scored zero, then the install line
- voiceover: "Every rule mined from the logs scored full marks. Every rule I reasoned my way into scored zero."
- type: payoff
- persuasion: The finding
- beat: land
- blueprint: kinetic-type-beats (Adapt)
- focal: authored/provenance
- roles: two-column scores = cutout - install line = supporting - ground = background
- poster: 4

Adapt: keep the statement-builds-across-beats structure and the spring-pop
payoff, but each beat carries a score row rather than a bare phrase, so the
claim and its evidence land in the same move.

Scene 1 (0.0-2.2s): left column springs in. Heading `mined from the logs`, and
beneath it four marks: `2 2 2 2`, ink, large mono. `spring-pop-entrance`.
Scene 2 (2.2-4.4s): right column springs in. Heading `reasoned my way into`,
and beneath it `0 1 0 0`, same size, grey. The contrast is the whole shot.
Scene 3 (4.4-6.4s): both columns slide up and compress to 60%; one line lands
beneath them at display size: `The evidence carried all of it.`
`kinetic-beat-slam`.
Scene 4 (6.4-9.0s): the columns fade to 20%. The wordmark `jot` settles at
centre with the install line beneath it in mono:
`npx skills add HarjjotSinghh/jot`. Held, still, no drift.

## Video direction

**Ground.** Every frame rides on the same `#FAFAFA` canvas as a full-duration
`class="clip"` background layer, never a `#root` background. Ink is `#1A1A1A`,
secondary `#6B6B6B`, hairlines `#D4D4D4`. Cobalt `#2563C9` appears exactly four
times in the whole video - the count in Frame 2, the date tie in Frame 3, the
18/20 bar in Frame 4, the wordmark in Frame 5 - and nowhere else. Scarcity is
what makes it read as a signal rather than decoration.

**Type.** Inter for display and body, Cascadia Mono for every command, path,
log line and score. Mono is never smaller than 26px at 1920 wide: this is
watched on a phone.

**Motion law.** One continuous read, not five slides. Every frame exits by
settling upward and the next enters from below, so the whole piece moves in one
direction. No idle wobble, no breathing, no back-half camera drift: once content
has resolved it holds still. Reveals are cued to the caption line and spread
across the back half of each shot - nothing dumps at t=0.

**Rhythm.** Frames 1 and 5 are dense with motion; Frames 3 and 4 end on long
held reads. That alternation is deliberate so the piece is not uniformly busy.

**Captions.** Burned in, bottom band, keep-out below y=920. The video is silent
by design and must be fully legible muted.

**Bans, from the subject's own recorded rules.** No emojis. No em dashes. No
unicode punctuation of any kind - ASCII only, including in the captions. No
rounded cards nested in rounded cards. No gradient headline, no floating
dashboard screenshot, no particle field.
