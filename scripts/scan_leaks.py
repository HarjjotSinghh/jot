#!/usr/bin/env python3
"""
Refuse to let the private layer reach the public one.

This repo is public. The knowledge files quote real sessions, and those sessions
name colleagues, clients, and internal tooling. A quote that is useful evidence in
`private/` is a leak in `PRINCIPLES.md`, and .gitignore does not catch that class of
mistake: the file is tracked on purpose, it is the *words inside it* that must not
ship.

So this scans every git-tracked file against a denylist. The denylist itself lives
at `private/redact.txt`, gitignored, because publishing the list of words you are
hiding tells everyone exactly what to look for.

  python scripts/scan_leaks.py            # scan tracked files, exit 1 on a hit
  python scripts/scan_leaks.py --staged   # scan only what is staged (pre-commit)
  python scripts/scan_leaks.py --install  # install as a pre-commit hook

If `private/redact.txt` is missing, structural checks still run: nothing under
private/, state/evidence/, state/pending/ or bench/runs/ may ever be tracked.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# The denylist always lives beside this script, in the jot checkout.
HOME_REPO = Path(__file__).resolve().parent.parent
DENYLIST = HOME_REPO / "private" / "redact.txt"


def _target_repo() -> Path:
    """The repo to scan: whichever one the caller is standing in.

    This used to be hardcoded to HOME_REPO, which meant running the script from
    another repository silently scanned jot instead of the repo you were about to
    push, found nothing staged, and printed "clean". A scanner that passes by not
    looking is worse than no scanner.
    """
    out = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode == 0 and out.stdout.strip():
        return Path(out.stdout.strip()).resolve()
    return HOME_REPO


REPO = _target_repo()

# Paths that must never be tracked, whatever .gitignore currently says.
FORBIDDEN_PATHS = re.compile(
    r"^(private/|state/evidence/|state/pending/|bench/runs/|.*/drafts/|drafts/)"
)

# Always-on patterns: these are leaks regardless of the denylist.
ALWAYS = [
    (re.compile(r"sk-[A-Za-z0-9_\-]{16,}"), "OpenAI-style API key"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9\-]{10,}"), "Slack token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key"),
    (re.compile(r"\bU0[A-Z0-9]{8,}\b"), "Slack user ID"),
    (re.compile(r"\bC0[A-Z0-9]{8,}\b"), "Slack channel ID"),
]

TEXT_SUFFIXES = {
    ".md", ".txt", ".py", ".yml", ".yaml", ".json", ".toml", ".sh",
    ".ps1", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", "",
}


def git(*args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, check=False,
    )
    return [line for line in out.stdout.splitlines() if line.strip()]


def load_denylist() -> list[tuple[re.Pattern[str], str]]:
    """One term per line. `#` comments and blanks ignored. Matched case-insensitively.

    A line may be `term` or `term => reason`.
    """
    if not DENYLIST.exists():
        return []
    terms = []
    for raw in DENYLIST.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        term, _, reason = line.partition("=>")
        term = term.strip()
        if not term:
            continue
        # Word-boundary where the term is wordy, substring where it has punctuation.
        pat = (rf"\b{re.escape(term)}\b" if re.fullmatch(r"[\w .'-]+", term)
               else re.escape(term))
        terms.append((re.compile(pat, re.I), reason.strip() or "denylisted term"))
    return terms


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--install", action="store_true")
    args = ap.parse_args()

    if args.install:
        hook = Path(git("rev-parse", "--git-path", "hooks")[0])
        if not hook.is_absolute():
            hook = REPO / hook
        hook.mkdir(parents=True, exist_ok=True)
        dest = hook / "pre-commit"
        dest.write_text(
            "#!/bin/sh\n"
            "# Blocks the private layer from reaching a commit. See scripts/scan_leaks.py\n"
            'exec python "$(git rev-parse --show-toplevel)/scripts/scan_leaks.py" --staged\n',
            encoding="utf-8", newline="\n",
        )
        dest.chmod(0o755)
        print(f"installed pre-commit hook: {dest}")
        return 0

    files = git("diff", "--cached", "--name-only") if args.staged else git("ls-files")

    if REPO != HOME_REPO:
        print(f"scanning {REPO} (denylist from {HOME_REPO.name})", file=sys.stderr)

    if not files:
        what = "staged" if args.staged else "tracked"
        print(f"REFUSING TO PASS: no {what} files found in {REPO}.",
              file=sys.stderr)
        print("Zero files scanned is not evidence of cleanliness.",
              file=sys.stderr)
        return 1

    denylist = load_denylist()
    if not denylist:
        print(f"note: no denylist at {DENYLIST}; running structural checks only",
              file=sys.stderr)

    problems: list[str] = []

    for rel in files:
        if FORBIDDEN_PATHS.match(rel):
            problems.append(f"{rel}: this path must never be tracked")
            continue

        path = REPO / rel
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        for lineno, line in enumerate(text.splitlines(), 1):
            for pat, why in ALWAYS:
                if pat.search(line):
                    problems.append(f"{rel}:{lineno}: {why}")
            for pat, why in denylist:
                m = pat.search(line)
                if m:
                    problems.append(f"{rel}:{lineno}: '{m.group(0)}' - {why}")

    if problems:
        print("\nBLOCKED - private content in the public layer:\n", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(
            "\nRedact the term, or move the passage into private/. "
            "Quoting real evidence is fine; naming the people in it is not.\n",
            file=sys.stderr,
        )
        return 1

    scope = "staged" if args.staged else "tracked"
    print(f"clean: {len(files)} {scope} files, {len(denylist)} denylist terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
