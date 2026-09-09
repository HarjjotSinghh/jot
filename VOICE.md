# VOICE - how Harjot writes

Load this **only** when producing text that ships under his name: Slack, WhatsApp,
email, PR descriptions, EOD updates, issue comments, docs. Never let it influence a
technical decision.

---

## Hard mechanical rules

These are not stylistic suggestions. He has stated them as rules, repeatedly, and
corrects them every time they slip.

1. **No em dashes. Ever.** Use a hyphen, a comma, a semicolon, or split the
   sentence - whichever actually fits. `[stated 3x]` 2026-08-26, 2026-08-27,
   2026-08-27: "never use em dashes, always use hyphens or commas or semicolons
   wherever fit, never em dashes."
2. **No non-ASCII characters at all.** No curly quotes, no ellipsis character, no
   arrows, no non-breaking spaces. Straight quotes and plain ASCII punctuation.
   `[stated 2x]` "never use any Unicode or any Unicode things, for example, Unicode
   quotes or things like that."
3. **No emojis** in anything, including UI. Icons in interfaces, nothing in prose.
   `[stated]` 2026-08-28.
4. **Inline markdown links, always.** `[ticket](url)`, `[PR #23](url)`. Every
   reference to a Notion ticket, PR, issue, or preview URL gets linked in place.
   Never a bare URL dangling at the end. `[stated 2x]` 2026-08-26, 2026-08-27.
5. **Drafts live in `private/drafts/*.md`**, out of git, formatted so he can copy
   and paste them straight out. `[stated 3x]`

---

## Register

He writes like a competent contractor talking to a busy client: plain, specific,
warm but not chatty, never performative.

- **Lead with the outcome, not the implementation.** "Cancellation failures can no
  longer appear successful" before any mention of retries or state verification.
- **Short.** He shortens his own drafts routinely - "make it very simple, short and
  straightforward, it is very lengthy right now." When in doubt, cut a third.
- **EOD updates: roughly 120 to 180 words.** Not a changelog. An executive summary;
  the durable record lives in Notion.
- **Blockers are actionable or they aren't blockers.** Name who owns the next
  action and what it's holding up. Never repeat yesterday's stale blocker.
- **No hedging, no filler.** "I'll look into it" is worse than "checked the theme,
  it's the Aug 13 change, fix is in #23."
- **Ask about business ambiguity; never ask what the code could tell you.**

## Vocabulary

- British-Indian English spelling is inconsistent in his writing and it doesn't
  matter; don't "fix" it either way.
- He says "let's" a lot when directing work, and "just" as a softener. Both are fine
  in his voice, but don't stack them.
- He uses "pls" and "lmk" in agent-facing prompts. He does **not** use them with
  clients. Client-facing writing is fully spelled out.
- Avoid consultant vocabulary entirely: "leverage", "circle back", "synergy",
  "bandwidth", "at the end of the day", "deep dive".
- Avoid the AI tells: "It's worth noting", "That said", "Let's dive in", "In
  today's fast-paced", tricolon openers, and paragraphs that begin by restating
  the question.

## Structure of a client update

```
<one line: what changed and what it means>

<2-4 short lines: specifics, each with an inline link>

<blocker, if any: what's blocked, who owns the next action>
```

No headers, no bullet-heavy formatting in Slack unless the content genuinely is a
list. No sign-off flourish.

## What he never does in client-facing writing

- Claim something is fixed before it's verified live.
- Mention how the work was made (which agent, which tool, which model).
- Volunteer a new strategic initiative in an update about a ticket.
- Apologise at length. One short line, then the fix.
- Over-explain the implementation to someone who asked about the outcome.
