# Q5 - the two-hour refactor that unblocks the next three tickets

**Trigger:** mid-ticket, you find structurally bad code you could fix in a couple of
hours, and fixing it would make your own next few days materially easier.

**/jot said:** don't. Ship the two-line fix, propose the refactor as follow-up.
Cited "refactoring because it looks ugly inside an unrelated ticket is a boundary
violation" and "propose, don't start".

**Harjot said:** do it now. "I don't want trouble down the line. If the issue is
clear to me and I can fix it, even at two hours, I get it fixed first, because it
improves my workflow and makes the job much easier for the next three days."

**Because:** the rule he actually holds is about *unsolicited strategic
initiatives* - discovering seven new directions while Tuesday's ticket is open. It
is not about clearing a concrete, understood blocker sitting directly in the path of
work he has already committed to. The distilled rule collapsed those two into one
and fired the wrong one.

## Where the bad rule came from

Not from his transcripts. It was imported from third-party advice in the prompt that
started this repo ("Don't perform broad refactors merely because existing code looks
ugly"), which reads as sensible and is not how he works.

**Rules changed:**
- `WORKFLOWS.md` > Refactor: removed the blanket "boundary violation" framing.
- `PRINCIPLES.md`: added "Clear the blocker in your own path" with its range.

**Doesn't apply when:** the mess is not blocking him, is speculative, or is on a
client's critical path where an unscoped two-hour change carries review and release
risk he does not own. Then it goes in a follow-up ticket.

**Scored:** 0. Rerun pending.
