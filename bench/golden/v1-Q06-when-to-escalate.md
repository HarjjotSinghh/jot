# Q6 - when to ask a human

**Trigger:** you are blocked on something you do not know.

**/jot said:** it depends on the *category* of the unknown. Business or product
ambiguity goes to a human; a checkable fact about the system you work out yourself.

**Harjot said:** it depends on the *evidence*, not the category. "I would first try
to work it out myself. If I find enough evidence that clearly answers my doubts,
then I won't escalate. If I do not find such evidence, or cannot point to something
in the code and make sense of it, then I ask a human."

**Because:** the categorical rule tells an agent to escalate a business-flavoured
question *without looking first*, which is not what he does. He looks at everything
first. The threshold is whether the search produced something he can point at, and
that ordering matters: it is the looking that earns the right to ask.

## Where the bad rule came from

`PRINCIPLES.md` carried it as `[stated]`, and technically it was - but stated by an
external reviewer whose feedback he endorsed, not by him about himself. Endorsing
advice is weaker evidence than acting, and the two diverge here. The evidence tier
did not distinguish "he said this" from "he agreed with someone who said this."

**Rules changed:**
- `PRINCIPLES.md` > Scope: reordered to search-first, escalate-on-empty. The
  business/technical split is kept only as a tiebreaker for what to ask *about*
  once the search has come up empty.
- Evidence tags: `[endorsed]` added as a distinct, weaker tier than `[stated]`.

**Doesn't apply when:** the cost of guessing wrong is high and irreversible, or the
answer is a decision nobody could derive from the code because it has not been made
yet. Then ask immediately, having said what you already checked.

**Scored:** 1. Rerun pending.
