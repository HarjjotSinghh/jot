#!/usr/bin/env python3
"""
Mine every coding agent on this machine for Harjot's judgment events.

What you say you do is aspirational. What you typed at an agent that was one
keystroke from doing the wrong thing is evidence. This pulls the second kind out
of every agent's local session store and normalises them into one corpus.

Adapters (auto-detected, skipped silently when absent):

  claude   ~/.claude/projects/**/*.jsonl  +  any extra --claude-root
  codex    ~/.codex/sessions/**/rollout-*.jsonl
  grok     ~/.grok/sessions/**/chat_history.jsonl
  gemini   ~/.gemini/tmp/**/logs.json
  cursor   %APPDATA%/Cursor/User/globalStorage/state.vscdb  (cursorDiskKV bubbles)
  opencode ~/.opencode/**/*.json, ~/.local/share/opencode/**
  generic  --extra-jsonl for anything else that looks like {role,content} lines

Output (all under --out):
  corpus-events.jsonl   normalised, scored, deduped events
  corpus-digest.md      readable top-N digest for distillation
  corpus-stats.json     per-agent counts and signal histogram

Usage:
  python scripts/extract_corpus.py
  python scripts/extract_corpus.py --agents claude codex cursor --min-score 5
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

# --------------------------------------------------------------------------
# Signal lexicons. Weight reflects how strongly the phrase implies a *decision*
# rather than a task instruction. Corrections outrank everything: they are the
# moment a stated preference met reality and reality lost.
# --------------------------------------------------------------------------

LEXICONS: dict[str, tuple[int, list[str]]] = {
    "correction": (5, [
        r"\bno,? (?:don'?t|do not|that'?s|it'?s|we|i|you)\b",
        r"\bthat'?s (?:not|wrong|incorrect)\b",
        r"\bnot what i\b", r"\bi (?:said|asked|told you)\b",
        r"\byou were supposed to\b", r"\bwhy did you\b", r"\bwho asked you to\b",
        r"\brevert\b", r"\bundo\b", r"\broll ?back\b",
        r"\bstop\b", r"\bwait,?\b", r"\bhold on\b",
        r"\binstead\b", r"\bactually,?\b",
        r"\bdon'?t do that\b", r"\bthat'?s wrong\b",
    ]),
    "rejection": (4, [
        r"\bno need (?:for|to)\b", r"\bdon'?t add\b", r"\bdon'?t create\b",
        r"\bremove (?:that|this|the)\b", r"\bget rid of\b", r"\bdelete (?:that|this)\b",
        r"\boverkill\b", r"\bover-?engineer", r"\btoo (?:much|complex|complicated|many)\b",
        r"\bunnecessary\b", r"\bwe don'?t need\b", r"\bskip (?:that|the)\b",
        r"\bkeep it simple\b", r"\bsimpler\b", r"\byou don'?t need to\b",
    ]),
    "preference": (4, [
        r"\bi (?:prefer|like|want|hate|don'?t like|dislike)\b",
        r"\bfrom now on\b", r"\bgoing forward\b", r"\balways\b", r"\bnever\b",
        r"\bmake sure (?:you|to)\b", r"\bremember (?:that|to|this)\b",
        r"\bmy (?:rule|preference|style|convention)\b",
        r"\bi usually\b", r"\bi tend to\b", r"\bthe way i\b",
        r"\badd a rule\b", r"\bone more rule\b",
    ]),
    "rationale": (3, [
        r"\bbecause\b", r"\bthe reason (?:is|being|i)\b", r"\bthat way\b",
        r"\bso that\b", r"\botherwise\b", r"\bwhich means\b",
        r"\bthe point is\b", r"\bmy thinking (?:is|was)\b",
    ]),
    "taste": (3, [
        r"\bslop\b", r"\bugly\b", r"\blooks? (?:bad|off|wrong|cheap|generic)\b",
        r"\bai[- ]generated\b", r"\bgeneric\b", r"\bbland\b",
        r"\bspacing\b", r"\btypography\b", r"\bcontrast\b", r"\bhierarchy\b",
        r"\bmake it (?:look|feel)\b", r"\bdoesn'?t look\b", r"\btoo (?:rounded|bright|dark)\b",
        r"\bem[- ]dash", r"\bemoji", r"\bfigma\b",
    ]),
    "approval": (2, [
        r"\bperfect\b", r"\bexactly\b", r"\bthat'?s (?:it|right|the one)\b",
        r"\bship it\b", r"\blgtm\b", r"\bnice,? (?:that|this)\b", r"\bgood,? now\b",
        r"\bapproved\b",
    ]),
    "escalation": (3, [
        r"\bdon'?t ask me\b", r"\bjust (?:do|decide|pick)\b", r"\byour call\b",
        r"\bask me (?:before|first)\b", r"\bcheck with me\b", r"\bdecide yourself\b",
        r"\bi will (?:send|approve|decide)\b", r"\blet me (?:approve|review)\b",
    ]),
    "process": (2, [
        r"\bfirst,? (?:read|check|understand|look)\b",
        r"\bbefore (?:you|doing|writing|changing)\b",
        r"\bverify\b", r"\breproduce\b", r"\btest (?:it|this|first)\b",
        r"\bdon'?t (?:guess|assume)\b", r"\bplan (?:it|first)\b",
    ]),
}

COMPILED = {
    name: (weight, [re.compile(p, re.I) for p in pats])
    for name, (weight, pats) in LEXICONS.items()
}

NOISE = re.compile(
    r"^\s*(?:"
    r"continue|go on|go ahead|proceed|yes|ok(?:ay)?|y|sure|thanks?|ty|next|done|"
    r"reply with exactly this token.*|"
    r"\[request interrupted.*|"
    r"/\w[\w-]*|"                       # a bare slash command carries no judgment
    r"caveat: the messages below.*"
    r")\s*$",
    re.I | re.S,
)

# Machine-authored text that rides in on a user turn: task results, monitor
# events, hook output, injected agent instructions. None of it is Harjot deciding.
MACHINE = re.compile(
    r"<(?:task-notification|tool-use-id|output-file|local-command-std\w+|"
    r"user-prompt-submit-hook|ci-monitor-event|environment_details)\b|"
    r"^\s*<summary>Monitor event|"
    r"^\s*\[SYSTEM NOTIFICATION|"
    r"^\s*#\s*(?:AGENTS|CLAUDE|GEMINI)\.md instructions\b|"
    r"^\s*<INSTRUCTIONS>|"
    r"^\s*<system-reminder>|"
    # Compaction summaries are the nastiest case. The agent writes them, but
    # they arrive as a user turn, and they are long prose *about* Harjot's
    # intent, which is precisely what the lexicon rewards. At 2% of the corpus
    # they took 40% of the top-50 band: exactly the slice a human reads when
    # distilling. They describe his judgment. They are not evidence of it.
    r"^\s*This session is being continued from a previous conversation|"
    r"^\s*(?:##\s*)?\d?\.?\s*Primary Request and Intent\b|"
    r"^\s*Analysis:\s*$",
    re.I,
)

SYSTEM_BLOCK = re.compile(
    r"<(?:system-reminder|command-name|local-command|task-notification)[^>]*>.*?</[^>]+>",
    re.S | re.I,
)
SECRETY = re.compile(
    r"(sk-[A-Za-z0-9_\-]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9\-]{10,}"
    r"|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|Bearer\s+[A-Za-z0-9._\-]{20,})",
)


# --------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------

def flatten(content) -> str:
    """Reduce any of the agents' content shapes to plain human text."""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        for k in ("text", "message", "content"):
            if isinstance(content.get(k), str):
                return content[k]
        return ""
    if isinstance(content, list):
        out = []
        for block in content:
            if isinstance(block, str):
                out.append(block)
            elif isinstance(block, dict):
                if block.get("type") in (None, "text", "input_text", "output_text"):
                    t = block.get("text") or block.get("content")
                    if isinstance(t, str):
                        out.append(t)
        return "\n".join(out)
    return ""


def clean(text: str) -> str:
    text = SYSTEM_BLOCK.sub("", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def redact(text: str) -> str:
    return SECRETY.sub("[REDACTED-SECRET]", text)


def score(text: str) -> tuple[int, list[str]]:
    total = 0
    hits: list[str] = []
    for name, (weight, pats) in COMPILED.items():
        n = sum(1 for p in pats if p.search(text))
        if n:
            total += weight * min(n, 3)
            hits.append(name)
    words = len(text.split())
    if words >= 25:
        total += 1
    if words >= 80:
        total += 1
    if words < 6:
        total -= 3
    return total, hits


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None


def iter_jsonl(path: Path):
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except ValueError:
            continue


# --------------------------------------------------------------------------
# Adapters. Each yields normalised turns:
#   {"role": "user"|"assistant", "text", "timestamp", "project", "source"}
# in chronological order per conversation, one generator per conversation.
# --------------------------------------------------------------------------

def adapter_claude(roots: list[Path]):
    """Claude Code / Claude Desktop JSONL session store."""
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            turns = []
            for obj in iter_jsonl(path):
                t = obj.get("type")
                if obj.get("isSidechain"):
                    continue
                if t == "assistant":
                    txt = flatten((obj.get("message") or {}).get("content"))
                    if txt.strip():
                        turns.append({"role": "assistant", "text": txt,
                                      "timestamp": obj.get("timestamp", "")})
                elif t == "user" and obj.get("userType") == "external":
                    if obj.get("promptSource") == "sdk" or obj.get("entrypoint") == "sdk-cli":
                        continue
                    content = (obj.get("message") or {}).get("content")
                    # A tool_result carries no human words even in a user turn.
                    if isinstance(content, list) and not any(
                        isinstance(b, dict) and b.get("type") == "text" for b in content
                    ):
                        continue
                    txt = flatten(content)
                    if txt.strip():
                        turns.append({"role": "user", "text": txt,
                                      "timestamp": obj.get("timestamp", "")})
            if turns:
                yield "claude", path.parent.name, str(path), turns


def adapter_codex(root: Path):
    """OpenAI Codex CLI / VS Code rollout logs."""
    if not root.exists():
        return
    for path in root.rglob("rollout-*.jsonl"):
        turns, project = [], ""
        for obj in iter_jsonl(path):
            t = obj.get("type")
            payload = obj.get("payload") or {}
            if t == "session_meta":
                project = Path(str(payload.get("cwd", ""))).name or project
                continue
            if t != "response_item" or payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in ("user", "assistant"):
                continue
            txt = flatten(payload.get("content"))
            if txt.strip():
                turns.append({"role": role, "text": txt,
                              "timestamp": obj.get("timestamp", "")})
        if turns:
            yield "codex", project or path.parent.name, str(path), turns


def adapter_grok(root: Path):
    """Grok CLI chat history, one file per session, keyed by url-encoded cwd."""
    if not root.exists():
        return
    for path in root.rglob("chat_history.jsonl"):
        # .../sessions/<urlencoded cwd>/<session uuid>/chat_history.jsonl
        enc = path.parent.parent.name
        project = Path(
            enc.replace("%3A", ":").replace("%5C", "/").replace("%5c", "/")
        ).name or enc
        turns = []
        for obj in iter_jsonl(path):
            role = obj.get("type") or obj.get("role")
            if role not in ("user", "assistant"):
                continue
            txt = flatten(obj.get("content") or obj.get("message"))
            if txt.strip():
                turns.append({"role": role, "text": txt,
                              "timestamp": obj.get("timestamp", "")})
        if turns:
            yield "grok", project, str(path), turns


def adapter_gemini(root: Path):
    """Gemini CLI logs.json - user turns only; it does not persist model replies."""
    if not root.exists():
        return
    for path in root.rglob("logs.json"):
        data = read_json(path)
        if not isinstance(data, list) or not data:
            continue
        turns = []
        for obj in data:
            if not isinstance(obj, dict) or obj.get("type") != "user":
                continue
            txt = obj.get("message")
            if isinstance(txt, str) and txt.strip():
                turns.append({"role": "user", "text": txt,
                              "timestamp": obj.get("timestamp", "")})
        if turns:
            yield "gemini", path.parent.name[:12], str(path), turns


def adapter_cursor(db_paths: list[Path]):
    """Cursor stores each chat message as a `bubbleId:*` row in cursorDiskKV.

    type 1 = user, type 2 = assistant. Bubbles are not reliably ordered by key,
    so each is emitted as its own single-turn conversation; the pairing step then
    simply has no assistant context for them, which is acceptable - Cursor's
    value here is the user's words, not the model's.
    """
    for db in db_paths:
        if not db.exists():
            continue
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        except sqlite3.Error:
            continue
        try:
            rows = con.execute(
                "select key, value from cursorDiskKV "
                "where key is not null and key like 'bubbleId:%'"
            )
            pending_assistant = ""
            for key, value in rows:
                try:
                    obj = json.loads(value)
                except (ValueError, TypeError):
                    continue
                txt = obj.get("text") or ""
                if not isinstance(txt, str) or not txt.strip():
                    continue
                if obj.get("type") == 2:
                    pending_assistant = txt
                    continue
                if obj.get("type") != 1:
                    continue
                turns = []
                if pending_assistant:
                    turns.append({"role": "assistant", "text": pending_assistant,
                                  "timestamp": ""})
                turns.append({"role": "user", "text": txt, "timestamp": ""})
                pending_assistant = ""
                yield "cursor", "cursor", f"{db}#{key}", turns
        except sqlite3.Error:
            continue
        finally:
            con.close()


def adapter_opencode(roots: list[Path]):
    """OpenCode stores message parts as small JSON files under storage/."""
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.json"):
            if "node_modules" in path.parts:
                continue
            data = read_json(path)
            if not isinstance(data, dict):
                continue
            role = data.get("role")
            if role not in ("user", "assistant"):
                continue
            txt = flatten(data.get("content") or data.get("parts") or data.get("text"))
            if txt.strip():
                yield "opencode", path.parent.name[:12], str(path), [
                    {"role": role, "text": txt, "timestamp": str(data.get("time", ""))}
                ]


def adapter_generic(paths: list[Path]):
    """Anything else shaped like {role|type, content|message|text} per line."""
    for path in paths:
        if not path.exists():
            continue
        turns = []
        for obj in iter_jsonl(path):
            role = obj.get("role") or obj.get("type")
            if role not in ("user", "assistant"):
                continue
            txt = flatten(obj.get("content") or obj.get("message") or obj.get("text"))
            if txt.strip():
                turns.append({"role": role, "text": txt,
                              "timestamp": obj.get("timestamp", "")})
        if turns:
            yield "generic", path.stem[:24], str(path), turns


# --------------------------------------------------------------------------
# Core
# --------------------------------------------------------------------------

def default_sources() -> dict[str, object]:
    home = Path.home()
    appdata = Path(os.environ.get("APPDATA", home / "AppData/Roaming"))
    return {
        "claude": [home / ".claude/projects"],
        "codex": home / ".codex/sessions",
        "grok": home / ".grok/sessions",
        "gemini": home / ".gemini/tmp",
        "cursor": [
            appdata / "Cursor/User/globalStorage/state.vscdb",
            *(appdata / "Cursor/User/workspaceStorage").glob("*/state.vscdb"),
        ],
        "opencode": [
            home / ".opencode",
            home / ".local/share/opencode",
            Path(os.environ.get("LOCALAPPDATA", home)) / "opencode",
        ],
    }


def build_events(conversations, min_score: int, max_chars: int, stats: Counter):
    """Pair each human turn with the assistant turn it reacted to, then score."""
    for agent, project, source, turns in conversations:
        stats[f"conv:{agent}"] += 1
        last_assistant = ""
        for turn in turns:
            if turn["role"] == "assistant":
                last_assistant = turn["text"]
                continue

            text = clean(turn["text"])
            if not text or NOISE.match(text) or MACHINE.search(text[:400]):
                last_assistant = ""
                continue

            s, hits = score(text)
            if s < min_score:
                last_assistant = ""
                continue

            yield {
                "agent": agent,
                "score": s,
                "signals": sorted(hits),
                "project": project,
                "timestamp": turn.get("timestamp", ""),
                "source": source,
                "agent_proposed": redact(last_assistant[:max_chars]),
                "harjot_said": redact(text[:max_chars]),
            }
            last_assistant = ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", nargs="*", default=[
        "claude", "codex", "grok", "gemini", "cursor", "opencode",
    ])
    ap.add_argument("--claude-root", nargs="*", default=[],
                    help="extra Claude project stores (e.g. a relocated ~/.claude)")
    ap.add_argument("--extra-jsonl", nargs="*", default=[],
                    help="any other {role,content} jsonl transcripts")
    ap.add_argument("--out", default="state/evidence")
    ap.add_argument("--min-score", type=int, default=4)
    ap.add_argument("--top", type=int, default=2500)
    ap.add_argument("--max-chars", type=int, default=2400)
    args = ap.parse_args()

    src = default_sources()
    src["claude"] = list(src["claude"]) + [
        Path(os.path.expanduser(p)) for p in args.claude_root
    ]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    stats = Counter()

    def conversations():
        if "claude" in args.agents:
            yield from adapter_claude(src["claude"])
        if "codex" in args.agents:
            yield from adapter_codex(src["codex"])
        if "grok" in args.agents:
            yield from adapter_grok(src["grok"])
        if "gemini" in args.agents:
            yield from adapter_gemini(src["gemini"])
        if "cursor" in args.agents:
            yield from adapter_cursor(src["cursor"])
        if "opencode" in args.agents:
            yield from adapter_opencode(src["opencode"])
        if args.extra_jsonl:
            yield from adapter_generic([Path(p) for p in args.extra_jsonl])

    events: list[dict] = []
    seen: set[str] = set()

    for ev in build_events(conversations(), args.min_score, args.max_chars, stats):
        # Acceptance harnesses and IDE retries replay near-identical prompts;
        # one copy of each is plenty.
        key = hashlib.sha1(
            re.sub(r"\s+", " ", ev["harjot_said"].lower())[:400].encode()
        ).hexdigest()
        if key in seen:
            stats["deduped"] += 1
            continue
        seen.add(key)
        events.append(ev)
        stats[f"kept:{ev['agent']}"] += 1
        for sig in ev["signals"]:
            stats[f"signal:{sig}"] += 1

    events.sort(key=lambda e: (-e["score"], e["timestamp"]))

    jsonl_path = out_dir / "corpus-events.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as fh:
        for ev in events:
            fh.write(json.dumps(ev, ensure_ascii=False) + "\n")

    top = events[: args.top]
    digest = out_dir / "corpus-digest.md"
    with digest.open("w", encoding="utf-8") as fh:
        fh.write("# Corpus evidence digest\n\n")
        fh.write(
            f"{len(events)} deduped judgment events across "
            f"{len([k for k in stats if k.startswith('kept:')])} agents. "
            f"Top {len(top)} shown, highest signal first.\n\n"
            "Each entry is a decision pair: what the agent was doing, and what "
            "Harjot said about it. Distill rules from these, not from self-report.\n\n---\n\n"
        )
        for i, ev in enumerate(top, 1):
            fh.write(f"## {i}. score {ev['score']} · {ev['agent']} · {', '.join(ev['signals'])}\n\n")
            fh.write(f"`{ev['project']}` · {ev['timestamp'][:10]}\n\n")
            if ev["agent_proposed"]:
                fh.write("**Agent proposed:**\n\n```\n" + ev["agent_proposed"][:1200] + "\n```\n\n")
            fh.write("**Harjot said:**\n\n```\n" + ev["harjot_said"] + "\n```\n\n---\n\n")

    (out_dir / "corpus-stats.json").write_text(
        json.dumps(dict(stats), indent=2), encoding="utf-8"
    )

    print(f"events kept : {sum(v for k, v in stats.items() if k.startswith('kept:'))}")
    print(f"deduped     : {stats['deduped']}")
    for k in sorted(stats):
        if k.startswith(("kept:", "conv:", "signal:")):
            print(f"  {k:22} {stats[k]}")
    print(f"\nwritten : {jsonl_path}\ndigest  : {digest} (top {len(top)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
