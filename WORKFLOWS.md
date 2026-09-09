# WORKFLOWS - Harjot's repeatable procedures

Named sequences. When a task matches one, follow it rather than improvising.

---

## Feature

```
read the ticket and the existing code
  -> resolve business ambiguity with a human; resolve technical ambiguity yourself
  -> plan, in a file, if it spans more than one session
  -> implement in sections
  -> show each section against its reference, get approval
  -> commit approved sections in logical chunks
  -> open PR with inline ticket/PR links and screenshots
  -> wait for CodeRabbit, address every point
  -> merge
  -> verify live in production
  -> report the outcome, not the implementation
```

## Bug

```
reproduce, on the platform that's actually failing (Windows counts)
  -> find the root cause, not the symptom
  -> sweep the codebase for other instances of the same class
  -> smallest correct fix
  -> re-test through the real UI, iterate until it genuinely passes
  -> verify live
  -> screenshot into the issue/PR
```

If the bug predates his changes: flag it, name the actual cause, and offer the fix
as separate work rather than absorbing it silently.

## Client-reported bug list

He often pastes a numbered list of user-reported issues, sometimes in mixed
English and Hindi.

```
restate each numbered item as a testable statement
  -> fix each, in order, keeping the numbering
  -> verify each through the browser
  -> if a fix does not hold, iterate on that item before moving on
  -> report back against the original numbering, item by item
```

Never collapse his numbered list into prose. He tracks them by number.

## Refactor

```
establish behavioural guardrails first (tests, or a recorded before-state)
  -> refactor
  -> compare behaviour against the guardrails
  -> adversarial review pass
  -> chunked commits
```

**When to refactor mid-ticket.** If the mess is concretely blocking the work you
are already on, and you understand it, fix it now - even at a couple of hours. He
would rather clear it while the context is loaded than route around it for three
days. See `PRINCIPLES.md` > "Clear the blocker in your own path".

Defer it only when it is speculative, is not actually in your way, or sits on a
client's critical path where an unscoped change carries release risk you do not own.
Then open a follow-up and say what it unblocks.

## Frontend implementation

```
get the reference (Figma, screenshot, or the existing good surface)
  -> identify the real design system in the codebase: tokens, cn(), import alias, Tailwind version
  -> pull real components from the registries, do not invent them
  -> implement section by section
  -> present each section side by side with the reference
  -> fix the listed deltas exactly
  -> check light and dark, all responsive breakpoints, contrast
  -> verify on a real device
```

## Code review

```
intent: does this do what the ticket asked?
  -> behaviour: what changes for the user
  -> edge cases, especially first-run and empty states
  -> unnecessary complexity and abstractions used once
  -> verification: was it actually checked live, or just claimed
  -> attribution, unicode, emojis, internal tool names
```

## End-of-day update

```
gather work from every session on the machine, not just this one
  -> outcomes first, implementation only if it explains the outcome
  -> 120-180 words
  -> inline links to tickets and PRs
  -> blockers: what is blocked, who owns the next action
  -> drop yesterday's stale blockers
  -> save the draft to private/drafts/, he sends it
```

## Any outbound message

```
draft it in private/drafts/<topic>.md
  -> verify every factual claim in it against code, logs, or the live system
  -> strip em dashes, unicode, emojis
  -> add inline links
  -> cut a third
  -> hand it to him; he sends it
```

## Shipping something to a client for review

The pattern he uses for deliverables (builds, extensions, demos):

```
build it
  -> full end-to-end test as that specific person would use it
  -> bump the version, note what changed and why
  -> package: the artefact, plus a tester package with release notes and instructions
  -> record a demo video against that exact build
  -> draft the accompanying message
  -> he reviews the video and the message, then sends
```
