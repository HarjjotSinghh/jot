# TOOLS - what Harjot reaches for

Observed from real work, not from a CV. Tooling moves faster than judgment, so
treat this as the most perishable file here and check dates.

Last refreshed: 2026-09-10.

---

## Environment

- **macOS is his preferred development environment.** A Windows 11 Pro desktop is
  currently carrying the load because the Mac has been out of action; it is also his
  gaming and local-LLM-hosting machine. Production is Linux.
- So: assume three-platform reality, assume Windows is the one nothing else was
  tested on, and do not assume he is happy about developing there.
- **Limited Linux experience** outside the macOS terminal and WSL. A bare-metal
  Linux answer needs more scaffolding than you would give a Linux native.
- **PowerShell** primary, Git Bash available. Scripts should not assume a POSIX shell.
- Heavy local agent surface: Claude Code, Codex, Grok CLI, Gemini CLI, Cursor,
  Antigravity, OpenCode, Qwen, Continue, Factory, Kiro, Trae, Windsurf, Zed.

## Languages

TypeScript and JavaScript first. Python for tooling and AI work. **Go** for systems
work and CLIs. C and C++, the latter for DSA practice.

## Web stack

| Layer | Default | Notes |
|---|---|---|
| Framework | Next.js (App Router), React, TypeScript. Svelte/SvelteKit where it fits | |
| Styling | Tailwind, shadcn/ui | Components sourced from real registries via his `ui-sources` skill, never invented |
| Motion | Framer Motion, transitions.dev tokens | Stagger fade is the safe default |
| AI UI | `ai-sdk.dev` elements (e.g. prompt-input) | Named explicitly in his instructions |
| DB | Drizzle ORM; Postgres, SQLite, Cloudflare D1 | Picks per project, asks which is wanted |
| Runtime/pkg | Bun, npm | `bun tsc --noEmit` is his compile check |
| Deploy | Vercel; Cloudflare Workers/Pages | Confirm the target before building |
| Payments | Polar.sh | |
| Desktop | Electron | |
| Chain | Solana | token utility work |

## E-commerce / client stack

Shopify (theme development, Admin, Liquid), Recharge, Klaviyo, PostHog, Microsoft
Clarity, Google/Meta pixels, Airtable, Notion (tickets and durable record), Slack
(executive summary layer), CodeRabbit (PR review), GitHub.

## Automation and agents

Playwright and Playwright MCP for browser work, browser-stealth MCP where needed,
GitHub CLI, `npx skills` for cross-agent skill distribution.

---

## Preferences with a reason attached

### Markdown files over databases for agent memory
`[stated]` He considers markdown the best way to store agent memory and notes that
agents differ (some SQLite, some markdown). Portable, diffable, greppable, and it
survives the agent being replaced.

### Real component sources over generated ones
Generating components from imagination is what produces slop. Fetch from the
registries, read the code, adapt to the project's existing tokens and conventions.
`[stated]` in his global agent config.

### An existing library over a hand-rolled solution
For solved problems - markdown rendering, PDFs, dates - "use any package or library
required" is a normal instruction from him.

### Cheap model primary, strong model fallback
In products. See `AGENTIC.md`.

---

## Known friction

- **Playwright and Chromium break on Windows** in ways they don't on Mac or Linux.
  When they do, he wants a Windows-specific alternative rather than a platform caveat.
- **Memory and disk pressure** on the Windows box are a recurring real problem;
  local runs have hung the machine. Worth being conservative about parallel heavy
  processes and about leaving worktrees and `node_modules` around.
- **Passkey/2FA lockouts** have blocked him from client dashboards when the Mac was
  down. Don't design flows that assume one device.
