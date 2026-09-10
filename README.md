# jot

Harjot Singh Rana's engineering judgment, distilled into a portable agent skill.

The point is not to imitate how he writes. It is to let an agent **make the call he
would make** - so it stops escalating decisions he has already made a hundred times,
and stops making the ones he'd have to reverse.

```bash
npx skills add HarjjotSinghh/jot -g
```

Then, in any agent that supports Agent Skills:

```
/jot should this state be global or local?
/jot review this PR
/jot does this hero section look like AI slop?
/jot which model should these subagents run on?
/jot draft the EOD update
```

---

## How it's built

A thin skill stub, and a knowledge base that lives in this repo.

```
skills/jot/SKILL.md   loader; resolves a local checkout first, this repo's raw URLs second
ENTRY.md              routing table + the decision procedure
PRINCIPLES.md         durable rules that survive a framework change
ENGINEERING.md        backend, debugging, git, review
FRONTEND.md           visual taste, design parity, slop detectors
AGENTIC.md            model routing, autonomy grants, parallelism
WORKFLOWS.md          named sequences: feature, bug, refactor, review, EOD
TOOLS.md              what he reaches for, and the friction he hits
BOUNDARIES.md         hard stops - read before anything outward-facing
VOICE.md              how he writes; loaded only for text going out under his name
OPERATING.md          attention, cadence, escalation
CONTEXT.md            who he is, what's active
private/              gitignored: people, clients, money, positioning
state/                mined evidence, changelog, pending promotions
bench/                the benchmark that says whether any of this works
scripts/              corpus extraction and benchmark tooling
```

The stub never changes. All churn happens in the knowledge files, so every agent
that points at this repo stays in sync without a separate update.

## Where the rules come from

Not from an interview. Asking someone how they work produces the aspirational
version - everybody writes tests first when you ask them.

`scripts/extract_corpus.py` mines the local session stores of every coding agent on
the machine (Claude Code, Codex, Grok, Gemini CLI, Cursor, OpenCode) for the moments
that actually encode judgment: the corrections, the rejections, the "no, do it this
way instead, because". Each one is paired with the agent turn it was reacting to,
scored against a judgment lexicon, deduped, and written to `state/evidence/`.

The first pass found 1,398 distinct judgment events across 1,290 conversations.
Every rule in the knowledge files carries an evidence tag pointing back at them:

- `[observed Nx]` - extracted from N distinct real sessions, dated
- `[stated]` - he wrote it down as a rule
- `[inferred]` - derived from adjacent behaviour, lower confidence, flagged in use

A rule with no evidence is a vibe. If it can't be traced, it doesn't go in.

```bash
python scripts/extract_corpus.py
python scripts/extract_corpus.py --agents claude codex cursor --min-score 5
```

## Does it work?

`bench/` answers that with a three-arm test: a control model with no skill, the same
model with `/jot` loaded, and Harjot answering blind. All three take the same ten
decisions; the model arms run in clean-room sessions and their answers stay hidden
until Harjot has committed to his.

The number that matters is the **delta** between the two model arms. A skill that
scores well only because any competent model would have scored well is recording
things that didn't need recording.

Misses become golden cases in `bench/golden/`, and each one turns into a rule with a
`Doesn't apply when` line - because the second-worst failure mode is a real rule
applied outside its range. The worst is fabricating a preference he doesn't hold.

```bash
python scripts/bench_run.py --set v1
python scripts/bench_score.py --run <timestamp>
```

## Privacy

The public layer holds judgment. The private layer holds the specifics that make it
actionable: named colleagues, client engagements, money, contracts, and how he is
positioned. `private/` and `state/evidence/` are gitignored and never fetched over
the network; the skill loads them only from a local checkout.

Nothing from the private layer may influence what a repository records - not in a
commit, not in a PR body, not as a hint, not as a filename.

---

Prior art: [kunchenguid/kun](https://github.com/kunchenguid/kun), which made the
case that the repeatable part of your judgment is worth externalising, and that it
isn't the part that was ever your moat.
