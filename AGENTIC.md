# AGENTIC - how Harjot runs AI agents

He is a heavy multi-agent operator: several Claude Code sessions in parallel, plus
Codex, Grok, Gemini CLI, Cursor, OpenCode and others, with roughly 180 skills
installed. This file is how he routes and constrains them.

---

## Model routing

### Subagents are Sonnet 5. Never Opus. Never Fable.
- **Do:** Every general-purpose subagent, every fan-out worker, every background
  task runs on Sonnet 5.
- **Because:** Opus and Fable burn his weekly and session usage fast, and the
  fan-out is where the volume is. He wants the budget spent on the main thread.
- **Not when:** He explicitly asks for a stronger model on a specific hard call.
- **Evidence:** `[stated 2x, emphatic]` 2026-09-01 "pls make sure they're sonnet 5,
  never opus or fable (burns my weekly usage and session usage a lot), remember this
  pls"; 2026-08-29 "use sonnet 5 subagents, never opus or fable subagents."

### Route by model, not just by cost
He does not treat frontier models as interchangeable. The split he actually uses:

| Work | Model |
|---|---|
| Frontend, UI, visual judgment | Claude |
| Backend, harder reasoning, systems | Codex, or whichever model reasons hardest |
| Parallel, lower-priority, or second-opinion passes | Grok, Gemini, or a secondary agent |

For a fan-out, the rule is the **cheapest model that still chunks the task
correctly** - Sonnet 5 in Claude, the cheapest of the current family elsewhere. His
reasoning is explicit: a bigger model returns the same answer in about 90% of
scenarios, and the difference is his weekly and session budget.

- **Evidence:** `[stated]` model-specialisation preference; `[observed]` 2026-09-10
  benchmark Q4: "the cheapest model available that also does task chunking... there
  won't be any difference if I were to use a bigger or better model."

### In products, name the primary and the fallback explicitly
The cheap fast model is primary; the stronger model is the fallback, never the
other way round. Getting that inverted draws a sharp correction.

### Cross-model second opinions on direction
For anything consequential he hands the same prompt to two or more of ChatGPT,
Claude, Grok and Gemini and compares how they diverge. He asks agents to save the
prompt sequence to a markdown file so it can be handed to another agent cleanly.
Offer this proactively for plans and architecture calls; don't do it for tickets.

---

## Autonomy

### An approval covers what it named, and does not extend
When he says "I am approving this, so don't question it, just go for it", run *that
task* to completion without re-litigating it. Do not stop halfway through an
approved run to ask whether to continue.

But the grant does not travel. A sub-decision the approval did not name is not
covered by it, even when it is small, reversible and local. Ask.

- **Because:** He is accountable for the outcome and wants the decision to route
  through him. One message costs close to nothing, and he has said plainly that he
  would ask first.
- **Evidence:** `[observed]` 2026-09-10 benchmark, Q10: "I would ask first before
  proceeding myself." An earlier version of this file read a single 2026-07-27 line
  ("I am approving this, so don't question it") as a general theory of how his
  approvals scope, and told the user with confidence not to ask. One line is an
  anecdote. See `bench/golden/v1-Q10-blanket-approval-scope.md`.

### Default posture without an explicit grant
- **Reversible and local:** just do it.
- **Reads of any kind** - browsing a dashboard, reading Slack, querying logs: do it.
- **Writes to a live system, messages to humans, merges, money:** stop and ask.
  See `BOUNDARIES.md`.

### Dry runs before real actions
For any automation that will eventually act in the world (applying to jobs, sending
replies, posting), build dry-run mode first and stay in it until the output is
consistently right. Throwaway accounts, never his main ones.

### Browser work: he logs in, you drive
The pattern he uses is: he authenticates manually in a Playwright/browser session,
hands over, the agent does all the read-only exploration and produces the list of
intended edits, he approves, then the agent executes the writes.

---

## Parallelism and context

- He treats agents as **specialised engineering teammates**, not as one tool: he
  assigns different parts of a project to different models, has one model review
  another's output, and compares them where they disagree.
- He runs **multiple sessions on the same project simultaneously** and expects an
  agent writing a summary to account for the other sessions' work by reading their
  transcripts on disk, not just its own.
- He wants **handoff artifacts**: prompts saved to markdown, plans saved to files,
  daily handoffs, so work can move between agents and machines.
- He prefers **markdown files as agent memory** over a database. He has said
  explicitly that markdown is the best way to do it, and notes that different agents
  store memory differently (some SQLite, some markdown).
- He uses **`ultracode` where it's warranted** and skills aggressively - `/impeccable`,
  `/ui-ux-pro-max`, `/frontend-skill`, `$job-discovery` and many others. When output
  is slop-shaped, the fix is often "load the right skill", including installing it
  if it isn't present.

---

## What he corrects agents for, most often

Ranked by how often it shows up in his transcripts:

1. **Answering a nearby question instead of the one asked.**
2. **Not matching the reference** (Figma, an existing good screen, a stated spec).
3. **Claiming done without verifying live.**
4. **Acting outward** - sending, posting, committing attribution - without approval.
5. **Adding decoration**: emojis, em dashes, unicode, unnecessary containers.
6. **Stopping early** on an iterate-until-green task.
7. **Asking him something the codebase could answer.**
8. **Quietly dropping a requirement** from a multi-part request. He numbers his
   asks; answer all the numbers.

## What earns approval

Closing the loop visibly, catching a landmine before it ships, doing the sweep for
sibling bugs unprompted, and producing something he can copy-paste or click
straight into use.
