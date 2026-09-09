# Changelog

Promotions into the knowledge files. Newest first.

## 2026-09-10 - v0.1, first distillation

- Mined 5 local agent stores (Claude Code, Codex, Grok, Gemini CLI, Cursor): 1427 deduped judgment events from 1290 conversations.
- Wrote ENTRY, PRINCIPLES, ENGINEERING, FRONTEND, AGENTIC, WORKFLOWS, TOOLS, BOUNDARIES, VOICE, OPERATING, CONTEXT.
- Private layer seeded: CLIENTS, PEOPLE, PERSONAL, POSITIONING.

## 2026-09-10 - v0.2, first benchmark and patch cycle

Benchmark run `20260910-0404`, set v1, both model arms on Sonnet 5 in clean-room
sessions. **B (/jot) 13/20, A (control) 7/20, delta +6.**

Root cause of every miss, without exception:

- Rules mined from his transcripts (Q1, Q4, Q8, Q9): scored 2, 2, 2, 2.
- Rules inferred or imported from third-party advice (Q5, Q6, Q7, Q10): 0, 1, 0, 0.

Patched:

- `PRINCIPLES.md`: escalation rewritten from category-based to evidence-threshold.
  Added "Clear the blocker in your own path" - he takes the 2-hour refactor now.
- `ENGINEERING.md`: Windows reframed as a release target; added the known-broken vs
  untested distinction as a release gate. Added his commit-message shape.
- `AGENTIC.md`: an approval covers what it named and does not extend to new
  sub-decisions.
- `FRONTEND.md`: added the ownership flip - he asks on a client's design, changes it
  himself on his own.
- `ENTRY.md`: routing made binding with a three-file cap; added the `[endorsed]`
  evidence tier and a hard rule against asserting `[inferred]` as his position.

Four golden cases opened under `bench/golden/`.

Process finding: arm B loaded all 16 files for a 10-question set and still lost 4.
More context made the wrong rules easier to reach, not harder.

## 2026-09-10 - v0.3, personal context layer

Benchmark rerun `20260910-0420-rerun` against the v0.2 patches: **B 18/20, A 7/20,
delta +11** (was 13/20). Q5, Q6, Q7 and Q10 all closed to 2.

**Q9 regressed 2 -> 0.** The new "Clear the blocker in your own path" rule was
over-applied to a two-minute fix on a live customer list. Exactly the failure the
golden-case process exists to catch: a rule that fixes one case and breaks another is
stated too broadly. Fixed by adding a live-system exclusion to that rule and making
`BOUNDARIES.md` explicitly outrank every principle, not merely tie-break against them.

Contributing cause: the v0.2 routing tightening stopped the agent loading `private/`,
where the customer-list context lives. The private-load trigger was too narrow and now
includes live customer data and marketing systems regardless of whether a person is named.

Personal context layer added, all gitignored, structured by how fast each tier rots:

- `IDENTITY.md` (permanent) - background, track record, stack, learning style, register
- `PATTERNS.md` (semi-stable) - the behavioural patterns he asked to be called out on
- `PEOPLE.md`, `PROJECTS.md`, `CLIENTS.md`, `GOALS.md` (semi-stable)
- `CURRENT.md`, `FINANCE.md` (current, dated, verify before use)

Public rules gained from it: per-model routing (Claude frontend, Codex backend,
cheapest-that-chunks for fan-out), the decision-answer format, the two-register
distinction in `VOICE.md`, Go and Svelte in the stack, and macOS-preferred rather
than Windows-primary.

`scan_leaks.py` denylist grew to 47 terms and immediately caught three more
identifiers in the already-published public layer.
