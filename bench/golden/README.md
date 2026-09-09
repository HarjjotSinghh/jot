# Golden cases

Every benchmark question where `/jot` scored **0 or -1** becomes a file here. These
are the regression suite: they are re-run on every distillation update, and a change
that fixes one while breaking another is a rule stated too broadly.

## Format

One file per case, named `<set>-<qid>-<slug>.md`:

```md
# Q4 - subagent model choice

**Trigger:** choosing a model for a fan-out of general-purpose subagents

**/jot said:** the strongest available model, for quality
**Harjot said:** Sonnet 5, always, never Opus or Fable
**Because:** the fan-out is where the volume is; Opus and Fable burn his weekly
and session usage, and he wants that budget on the main thread

**Rule added:** AGENTIC.md > "Subagents are Sonnet 5"
**Doesn't apply when:** he explicitly asks for a stronger model on one hard call
**Scored:** 0 -> 2 on rerun 20260910
```

## Why the `Doesn't apply when` line is mandatory

A distillation goes bad by over-applying real rules, not by holding wrong ones. A
rule without a stated range gets fired on every adjacent situation, and the
correction rate goes *up* rather than down - which defeats the entire purpose of
distilling in the first place.

If you cannot name a case where the rule should not fire, the rule is either
trivially true or you have not understood it yet. Both mean it does not go in.
