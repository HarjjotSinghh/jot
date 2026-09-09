# ENGINEERING - Harjot's technical judgment

Backend, data, debugging, git, and review. Frontend taste lives in `FRONTEND.md`.

---

## Debugging

### Windows is a release target, not a dev-environment quirk
- **Do:** Treat "works on my Mac" as a non-result. A large share of the bugs he hits
  are Windows-only - Playwright and Chromium failures, path handling, file locking,
  memory blowups that hang the machine. Reproduce on Windows before theorising, and
  when it fails there, find a Windows-specific fix rather than writing a caveat.
- **Because:** He develops primarily on Windows 11 with a Mac secondary, and he
  ships genuinely cross-platform software - Reinstate runs a Windows/macOS/Linux CI
  matrix. "The platform we deploy to" is not one platform.
- **Not when:** The failure is clearly platform-independent (a logic bug, a bad query).
- **Evidence:** `[observed 3x]` "It seems to be Windows-only. This doesn't happen on
  production or on my Mac"; "If Playwright or Chromium is not working, look for any
  alternatives... only for Windows, because on Mac OS and on Linux it works
  perfectly fine."

### Known-broken gates the release. Untested does not.
- **Do:** Hold the release once you actually know it fails on any target platform,
  even one you do not deploy to today. Fix it first.
- **Because:** The line he draws is awareness, and it is the same line as never
  claiming something unverified. Shipping something you have watched fail is the
  same act as saying it works when you have not checked.
- **Not when:** You simply have not tested that platform and have no failure reports.
  Untested is not known-broken; he ships in that case and picks up the reports.
  Likewise if it is the test harness failing rather than the product, and you can
  tell the difference.
- **Evidence:** `[observed]` 2026-09-10 benchmark, Q7: "Hold off until all operating
  system tests are clear... if I'm unaware, I go ahead with the release. If I
  actively know that Windows is broken and hangs, then I would just not ship it and
  get it fixed first." An earlier version of this file framed Windows as his dev
  environment and produced a ship-it call. See
  `bench/golden/v1-Q07-known-broken-on-one-platform.md`.

### Find the root cause, then sweep for siblings
- **Do:** When you find a defect class, search the codebase for every other
  instance and fix them together. He says "fix all such occurrences" as a matter of
  course.
- **Not when:** The sweep would balloon a hotfix. Then fix the one, and open a
  follow-up issue naming the class.

### Iterate to an actually-green run
- **Do:** Keep fixing and re-running until a full end-to-end run genuinely
  succeeds. Not "this should work now."
- **Evidence:** `[observed 2x]` "keep fixing issues... until we get a successful
  deployment or successful run. If we don't, just keep iterating and fixing and
  re-running until and unless we get a successful one."

### Never silently disable a pipeline step
- **Do:** If a stage is skipped, that's a bug to hunt down, not a shortcut to keep.
- **Evidence:** `[observed]` "dont skip the q&a generation, like ever. never skip
  it. check all codebase if something is disabling it and remove it."

---

## Correctness bar

- **Handle the first-run edge case by creating what's missing**, not by returning
  empty. An empty result where the user expects a workspace is a bug.
- **Deletes must actually persist.** A record that reappears after refresh is the
  archetypal bug he reports; check the write path, not just the optimistic UI.
- **Dates and locale bugs matter** - a due date silently rolling to the wrong year
  is exactly the class of thing his users report.
- **Never mock silently.** Mocking a slow step for a demo is fine when he asks for
  it and it's labelled; presenting mocked output as real is not.

---

## Testing and verification

1. Unit tests where they're cheap and meaningful; he counts them and reports the
   number ("all 65 unit tests pass").
2. **End-to-end through the real UI, as the specific person who will use it.**
   Study their known habits, replicate their path, break it the way they will.
3. **Generate 20-30 realistic user questions** for anything answer-shaped, run
   them, fix every wrong answer.
4. **Verify live in production** after deploy. See `PRINCIPLES.md`.
5. **Verify on a real device** for anything mobile-facing.

He asks for a step-by-step manual verification guide when he wants to check
something himself. Write it as numbered steps he can follow on a phone.

---

## Git and PRs

- **Commit message shape:** a short one-line subject, "fix" plus the issue in plain
  words, one line maximum. Everything else - the detail, the cause, what you
  deliberately left out and why - goes in the description body, not the subject. He
  does not use conventional-commit `type(scope):` prefixes.
  `[observed]` 2026-09-10 benchmark, Q1.
- **Commits in logical chunks**, grouped by meaning. Never one giant commit.
- **Preserve real history** on release PRs; don't squash hundreds of commits into one.
- **No AI attribution** in commits or PR bodies. See `BOUNDARIES.md`.
- **No internal tooling names** in client-facing repos.
- **Screenshots in PRs, issues and comments** wherever they help.
- **Inline links** to the Notion ticket and related PRs in every description.
- **CodeRabbit is part of the definition of done**: open the PR, wait for its
  review, address every point it raises, then merge. `[observed]` 2026-09-05.
- **History rewriting is allowed on his own repos when he asks for it** - he will
  say "make it seem as if the original filenames were never committed, feel free to
  force push if required." Never do it unprompted; never on shared client branches.

---

## Architecture

Recorded preferences are thin here, so flag inference clearly. What is observable:

- **Explicit primary and fallback**, named, for anything with a provider: the cheap
  fast model is primary, the stronger model is the fallback, and that assignment is
  deliberate rather than emergent. `[observed]` "replace the model with the cheap
  flash model as primary. The mini model is supposed to be a fallback always, never
  the primary one."
- **Infrastructure defaults are load-bearing.** Getting a domain, subdomain pattern,
  or deployment target wrong triggers a strong correction. Confirm the target
  (Cloudflare Workers/Pages + D1, Vercel, a specific subdomain pattern) before building on it.
- **Schema clarity over cleverness.** He will point at the exact schema file to use
  and tell you to delete the competing implementation rather than support both.
- **Reach for an existing library rather than writing it** - "use any package or
  library required" is a normal instruction from him for solved problems
  (markdown rendering, PDF handling, date math).

`[inferred]` He has not recorded a general position on microservices, monorepo
boundaries, or ORM choice beyond using Drizzle. Say so rather than guessing.
