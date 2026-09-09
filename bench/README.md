# bench - does /jot actually decide like Harjot?

A distillation that sounds like him but chooses differently is worse than useless:
it produces confident wrong calls in his name. This measures **decision fidelity**,
not impression fidelity.

---

## Design

Three arms answer the same questions. Two of them are models; the third is Harjot.

| Arm | Who | Context |
|---|---|---|
| **A - control** | A fresh model session | No skill. Generic good-engineer defaults. |
| **B - treatment** | A fresh model session | `/jot` loaded, nothing else. |
| **C - ground truth** | Harjot | Answers blind, having seen neither A nor B. |

Both model arms run in **clean-room sessions**: a fresh context that has never seen
the conversation in which the skill was built. This is not optional. A model that
helped write the knowledge files already knows the answers and will score
artificially high.

**Order matters.** A and B run first and their answers are written to files that
are not shown to Harjot. Then Harjot answers. Then everything is revealed and
scored together. If he sees the model's answer first, his own answer is
contaminated and the benchmark is dead.

The control arm is what makes the number mean something. B scoring 14/20 is
meaningless on its own; B scoring 14 while A scores 7 says the skill is carrying
7 points of judgment that a default model does not have.

---

## Scoring

Each question is scored 0-2 against Harjot's answer.

| Score | Meaning |
|---|---|
| **2** | Same call **and** substantially the same reason |
| **1** | Same call, weak or wrong reason; or a different call he'd still sign off on |
| **0** | Different call he would not make |
| **-1** | Fabricated a preference he does not hold, or violated a stated boundary |

Negative scores are deliberate. Inventing a Harjot opinion is the failure mode this
whole repo exists to prevent, and it must cost more than simply not knowing.

Report as `B: 15/20 vs A: 8/20`, plus the per-question table.

---

## Running it

```bash
python scripts/bench_run.py --set v1 --new-run
```

That creates `bench/runs/<timestamp>/` containing `questions.md`, and empty
`arm-a-control.md`, `arm-b-jot.md`, `arm-c-harjot.md`.

1. Fill A and B from two clean-room sessions (see the prompts in the run folder).
2. Give Harjot `questions.md` only. He fills `arm-c-harjot.md`.
3. Score:

```bash
python scripts/bench_score.py --run <timestamp>
```

It builds a side-by-side comparison table for scoring, then records the totals.

`bench/runs/` is gitignored: it holds his unscored answers.

---

## A benchmark set burns itself

The moment you promote a run's results into the knowledge files, that set stops
being a measurement. Evidence lines quote the correct answer, so the next run reads
the answer key on its way in. This is not hypothetical: set v1 was retired after one
promotion cycle, when seven of its ten questions ended up quoted verbatim across
`PRINCIPLES.md`, `ENGINEERING.md`, `AGENTIC.md` and `FRONTEND.md`. The arm-B agent
noticed and said so before anyone asked it to.

Two ways to live with it:

1. **Hold out a set.** Write more questions than you score. Keep some sealed, and
   only ever cite the ones you have already spent.
2. **Cite the rule, not the answer.** Record that a benchmark corrected a rule's
   range without quoting the correct call. Weaker evidence, longer-lived set.

A spent set is not waste. It becomes a **regression suite**: run it on every
knowledge-file change to confirm the patches held and nothing adjacent broke. It
just cannot tell you how faithful the skill is any more.

## Turning misses into golden cases

Every question where B scored 0 or -1 becomes a golden test case in
`bench/golden/`, with the correct answer and the rule that would have produced it.
The rule is then written into the relevant knowledge file with an evidence tag
pointing back at the golden case.

Golden cases are re-run on every distillation update. A rule that fixes one case
and breaks another is a rule stated too broadly; that's the signal to add a
`Doesn't apply when` line rather than a new rule.

---

## What a good result looks like

- **B at 16/20 or better** while A trails by 5 or more: the skill is doing real work.
- **B and A within 2 points:** the knowledge files are recording things any
  competent model already does. Delete the obvious rules and distil harder.
- **B below A:** the skill is actively misleading. Usually over-broad rules applied
  outside their range.
- **Any -1 in B:** fix that before anything else, whatever the total says.
