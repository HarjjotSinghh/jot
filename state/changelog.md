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
