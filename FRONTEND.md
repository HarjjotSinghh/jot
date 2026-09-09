# FRONTEND - Harjot's visual judgment

He is a developer with strong design opinions and a low tolerance for generic
output. Most of his corrections to agents are visual, and most of those are about
**fidelity** (does it match the reference?) and **character** (does it look like
every other AI-generated page?).

---

## The two modes - get this right first

His taste is not one thing. It splits by surface, and applying the wrong mode is
the most common way to be wrong about him.

| Surface | Mode | What he asks for |
|---|---|---|
| Marketing: landing pages, hero sections, launch pages, OG/banner creatives | **Ambitious** | "truly mindblowing and incredible", "incredibly unique, creative and never-seen-before". Rejects work as "TOOOOO basic and simple". Scroll-stopping is the goal. |
| Product: dashboards, app UI, settings, tables, modals | **Restrained** | Clean, minimal, legible, consistent. One primary colour, everything else black and white. Hierarchy through type and spacing, not decoration. |

`[observed]` 2026-02-06 (shipper/klyre landing) vs 2026-01-26 (app UI: "use a
singular color and only keep 5% of our entire UI as that primary color, rest
everything should be black and white").

---

## Fidelity rules - the largest category of his corrections

### Match the design reference literally
- **Do:** When a Figma file, a screenshot, or another surface is the reference,
  match it exactly: the same image assets (down to compositing four separate layers
  the way the design does), font weight, letter tracking, star sizes, card heights,
  aspect ratios, where the text line-breaks, colour brightness, border colours,
  vertical offsets. Remove anything present in the build that isn't in the reference.
- **Because:** He reviews by putting the two side by side and reading off the
  differences. Every unmatched detail is a round trip.
- **Not when:** The reference is explicitly a rough direction, or a stated
  constraint (a real product image, an accessibility minimum) makes literal parity
  wrong. Then say which detail you're deviating on and why.
- **Evidence:** `[observed 6x]` 2026-09-02 and 2026-09-03, repeatedly: "make the
  font style exactly the same as the figma design, same font weight, same font
  tracking"; "all the cards in the Figma design are the same size and the same
  height, that should also be the case"; "also remove this: the figma design does
  not contain this"; "the way that the text is breaking in the Figma design, our
  actual design should also follow the same breaking".

### Whose design is it decides whether you may improve it
- **Do:** On someone else's design, ship it as drawn and raise the concern *as a
  question to the person you report to* - "these things look off, should I remove
  them or fix them?" - rather than to the designer directly, and rather than
  shipping your own improved version. Wait for the answer.
- **On his own project, the opposite:** if he owns it and a designer handed him the
  file, he changes what looks wrong himself, immediately, without asking anyone.
- **Because:** authority follows ownership. As the developer on a client's design he
  is not the one who gets to overrule it, and a two-line question costs nothing. As
  the owner he is the one whose call it is, so routing it through anyone is waste.
- **Evidence:** `[observed]` 2026-09-10 benchmark, Q3: "I would just prefer
  reporting it to someone I report my work to... If it's my project, I would just do
  it right away. If I am the employer and I had that Figma design by some other
  designer, and I feel like something's off, I would just go for it and change it
  myself."

### Point at an existing good surface and match it
- **Do:** When one part of the product already looks right, that becomes the spec
  for the rest: fonts, colour themes, styling, interaction patterns, and the real
  data it displays.
- **Evidence:** `[observed 2x]` "Refer to the brands/employer dashboard for
  reference, that is good visually"; "update the entire UI/UX design to match that
  of our .exe application. Fonts, color themes, styling, UI, UX."

### Review is side-by-side, section by section
- Build one section, present it against the reference, get approval, commit it,
  move to the next. He will paste `our:` and `figma:` screenshots and list the
  deltas. Expect that loop and optimise for it.

---

## Slop detectors - what makes him reject a design outright

He uses the phrase "generic AI slop design" as a rejection. Concretely:

- **Emojis anywhere in the UI.** Use icons. `[stated]` 2026-08-28.
- **Non-ASCII decoration in copy**: em dashes, curly quotes, arrows. Straight ASCII
  only. `[stated 4x]`
- **Sci-fi affectations**: `//` prefixes, `snake_case` or underscores shown in
  user-facing typography, terminal cosplay. "Make it communicate normally and not
  like a tech sci-fi movie." `[observed 2x]` 2026-01-26.
- **Nested rounded cards inside rounded cards**, containers used as the only means
  of establishing hierarchy.
- **The default AI landing page**: centered badge, giant gradient headline, two
  buttons, floating dashboard screenshot. If it looks like the last twenty, it's wrong.
- **Basic when the brief was ambitious.** On marketing surfaces, "clean and simple"
  reads to him as "you didn't try."

He reaches for the `/impeccable` and `/ui-ux-pro-max` skills when output is
slop-shaped, and for real component sources (shadcn/ui and the registries in his
`ui-sources` skill) rather than generating components from imagination.

---

## Non-negotiables

### Contrast and legibility are correctness bugs, not polish
White-on-white buttons, low-contrast text, unreadable states - he reports these as
defects and expects a systematic sweep for other instances, not a one-line fix.
`[observed]` 2026-02-13: "fix all such occurances and make sure all texts are
readable, check their color and background color to verify no such instances occur".

### Light and dark mode are both first-class
Every styled component defines both explicitly. Not one theme with a filter over it.
`[observed]` 2026-01-26.

### Typography carries the hierarchy
Separate font families for headings and body. Pairing chosen deliberately. Weight,
size and spacing do the work before any border or container is added.

### Motion should flow, and must never break interaction
- Section transitions overlap: the animate-out starts early enough to actually be
  seen before the next section animates in.
- Staggered fade-in/out is the safe default. Reach further only when it earns it.
- **If an effect breaks clicking, revert it.** He has explicitly said: fix it, and
  if it can't be fixed, revert and don't keep fiddling. `[observed]` - a custom
  cursor-follow effect that blocked clicks and broke a table layout.
- Micro-interactions and on-scroll reveals are wanted, per section, across pages.

### Interactive components must be complete
A carousel's progress indicator tracks real progress and the carousel loops back to
the first item. Empty states create what's needed rather than rendering nothing.
`[observed 2x]` 2026-09-07; "no, don't return empty result, instead, create the
required things (first time usage edge case handling)".

---

## Verification

- Check it on a real device, not just a resized desktop window. He asks for the
  preview URL to open on his own iPhone.
- Screenshot the result into the PR or the issue comment.
- Re-test through the browser after a fix, and keep iterating until it actually
  passes; don't hand back "should be fixed now".
