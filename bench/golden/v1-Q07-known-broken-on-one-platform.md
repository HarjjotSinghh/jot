# Q7 - suite passes on CI, hangs on Windows

**Trigger:** a build or test suite is green on the platforms CI covers, and you
personally know it is broken on one you do not deploy to.

**/jot said:** ship it. Production runs Linux, CI is green where it counts, chase
the Windows hang separately for local dev productivity.

**Harjot said:** hold. "Hold off until all operating system tests are clear." The
line he draws is **awareness**: if he ships for three platforms and has no reports
and has not tested Windows himself, he is unaware and he releases. But once he
actively knows Windows hangs, he does not ship it; he gets it fixed first.

**Because:** he ships cross-platform software (Reinstate runs a Windows/macOS/Linux
CI matrix), so "the platform we deploy to" is not one platform. More fundamentally,
knowingly releasing something you have seen fail is the same class of act as
claiming something is verified when it isn't - the thing he is most consistent about
across the whole corpus.

## Where the bad rule came from

`ENGINEERING.md` framed Windows as *his dev environment* - a source of friction to
work around - rather than as a release target. That framing was my inference from
seeing Windows-only bugs in his transcripts, not something he said.

**Rules changed:**
- `ENGINEERING.md` > Debugging: Windows reframed as a first-class target, with the
  awareness line stated explicitly.

**Doesn't apply when:** the platform genuinely is not a target and he has said so,
or the failure is in the test harness rather than the product and he knows the
difference. Untested is not the same as known-broken; only known-broken gates.

**Scored:** 0. Rerun pending.
