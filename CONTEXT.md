# CONTEXT - who Harjot is and what he's working on

Public-safe situational awareness. Client-specific detail, named people, money, and
personal circumstances live in `private/` and are loaded only from a local checkout.

Last refreshed: 2026-09-10. Dates here are absolute on purpose - recheck anything
older than a month.

---

## Identity

**Harjot Singh Rana** - full-stack engineer, based in India, working primarily with
international clients. GitHub [`HarjjotSinghh`](https://github.com/HarjjotSinghh),
portfolio [harjotrana.com](https://harjotrana.com).

Practically: an e-commerce and product full-stack developer who leans hard into
agentic engineering. He operates a large fleet of coding agents rather than writing
most code by hand, and much of his judgment is expressed as constraints on those
agents.

## Shape of his work

Three concurrent modes, and knowing which one a task belongs to changes the answer:

1. **Client contract work.** Shopify e-commerce development on a live store, with a
   real team, real tickets, and real review. Highest stakes: verification, comms
   discipline, and boundaries matter most here.
2. **Client product work.** Building and shipping a product for a smaller client:
   builds, tester packages, demo videos, direct feedback loops over WhatsApp.
   Fast iteration, frequent releases, feedback lists to work through in order.
3. **His own products.** Where he has full authority and the boundaries relax:
   force pushes allowed when he asks, pricing decisions are his, autonomy grants
   are broader.

## Active projects

| Project | What it is |
|---|---|
| **Reinstate** | His own product. Cross-device/agent session portability. Extensive RC release process, CI matrix across Windows/macOS/Linux, acceptance harnesses. Pricing around $4/mo annual, $5/mo monthly. |
| **Moonshift** | His own product on `*.moonshift.page`. Automated landing-page generation and deployment. |
| **latyx** | His own product. Planning a Solana token with real utility rather than a token for its own sake. |
| **jot** (this repo) | The distillation itself. |
| **portfolio-25** | harjotrana.com. |
| Others seen in the corpus | rayiko, skelve, get-a-job, devsynq, agentblocks, gitbench, and a set of social-automation tools. Plus an Indian CA/compliance product whose users report bugs in Hindi. |

## Stack summary

Next.js / React / TypeScript / Tailwind / shadcn on the front, Drizzle with
Postgres, SQLite or Cloudflare D1 behind it, deployed to Vercel or Cloudflare.
Shopify, Recharge, Klaviyo, PostHog and Clarity on the e-commerce side. See
`TOOLS.md`.

## Working languages

English for all professional communication. Hindi appears in user bug reports on
the Indian product and in his own casual register; he reads both and does not want
Hindi input "translated away" when triaging.

---

## Loading the private layer

If a local checkout has `private/`, read `private/INDEX.md` when the task touches:
a named person, a specific client, money, contracts, or his personal situation.
Never quote it into anything that leaves the machine, and never let it reach a
commit. See `BOUNDARIES.md`.
