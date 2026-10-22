"""Read what the person typed or dictated to their coding agents, read-only.

People talk to agents in their rawest voice. This keeps only the person's own prompts and drops
everything else: tool results, system and meta messages, sub-agent and reviewer sessions, injected
context, pasted blocks, code, and slash commands. It redacts before printing, and by default prints
counts and patterns only.

Sources: Claude Code (~/.claude/projects), Codex (~/.codex/sessions), plus any JSONL with
{"role": "user", "content": ...} lines via --extra (for Kimi Code or other agents).

Usage:
  python3 -I agent_prompts.py                    # stats only, last 90 days
  python3 -I agent_prompts.py --sample 20        # plus 20 redacted prompts to judge tone
  python3 -I agent_prompts.py --days 30 --extra ~/.kimi/sessions
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from redact import redact  # noqa: E402

HOME = pathlib.Path.home()
TAG_BLOCK = re.compile(r"<([a-zA-Z_][\w:-]*)\b[^>]*>.*?</\1>", re.S)
FENCE = re.compile(r"```.*?```", re.S)
FILLER = ["like", "you know", "i mean", "kind of", "sort of", "basically", "just", "actually", "literally"]
PHRASES = ["i think", "i want", "we should", "can you", "let's", "make sure", "the thing is", "what if",
           "figure out", "for example", "please", "thanks", "lol", "ya", "yeah", "ok", "dude", "bro"]


def clean(text):
    text = TAG_BLOCK.sub(" ", text)
    text = FENCE.sub(" ", text)
    lines = [l for l in text.splitlines() if len(l) < 400 and not re.match(r"\s*(at |File \"|Traceback|\$ |> )", l)]
    text = "\n".join(lines).strip()
    if not text or text.startswith(("/", "<")):
        return ""
    words = len(text.split())
    if words < 3 or words > 400:  # too short to say anything, or likely a paste
        return ""
    return text


def recent(ts, cutoff):
    if not ts:
        return True
    try:
        return dt.datetime.fromisoformat(str(ts).replace("Z", "+00:00")) >= cutoff
    except ValueError:
        return True


def claude(cutoff):
    out = []
    for f in (HOME / ".claude/projects").glob("*/*.jsonl"):
        for line in f.open(errors="ignore"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") != "user" or "toolUseResult" in d or d.get("isMeta") or d.get("isSidechain"):
                continue
            human = d.get("turnOrigin") == "human" or (d.get("origin") or {}).get("kind") == "human"
            if ("turnOrigin" in d or "origin" in d) and not human:
                continue
            if not recent(d.get("timestamp"), cutoff):
                continue
            c = d.get("message", {}).get("content")
            text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or [] if isinstance(x, dict) and x.get("type") == "text")
            text = clean(text)
            if text:
                out.append(text)
    return out


def codex(cutoff):
    out = []
    for f in (HOME / ".codex/sessions").rglob("*.jsonl"):
        lines = f.open(errors="ignore")
        try:
            meta = json.loads(next(lines)).get("payload", {})
        except (StopIteration, ValueError):
            continue
        source = meta.get("source")
        if source == "subagent" or isinstance(source, dict) or meta.get("thread_source") not in (None, "user"):
            continue
        if not recent(meta.get("timestamp"), cutoff):
            continue
        for line in lines:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            p = d.get("payload") if isinstance(d.get("payload"), dict) else {}
            if d.get("type") == "response_item" and p.get("type") == "message" and p.get("role") == "user":
                text = clean(" ".join(x.get("text", "") for x in p.get("content", []) if isinstance(x, dict)))
                if text:
                    out.append(text)
    return out


def extra(path, cutoff):
    out = []
    files = [path] if path.is_file() else list(path.rglob("*.jsonl"))
    for f in files:
        for line in f.open(errors="ignore"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            msg = d.get("message", d) if isinstance(d, dict) else {}
            if not isinstance(msg, dict) or msg.get("role") != "user" or not recent(d.get("timestamp"), cutoff):
                continue
            c = msg.get("content")
            text = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or [] if isinstance(x, dict))
            text = clean(text)
            if text:
                out.append(text)
    return out


def stats(prompts):
    words = [w for t in prompts for w in re.findall(r"[a-z']+", t.lower())]
    n, text = max(1, len(words)), " " + " ".join(words) + " "
    count = lambda p: len(re.findall(rf"(?<![a-z']){re.escape(p)}(?![a-z'])", text))
    share = lambda pred: round(sum(1 for t in prompts if pred(t)) / max(1, len(prompts)), 2)
    return {
        "prompts": len(prompts),
        "words": len(words),
        "words_per_prompt": round(len(words) / max(1, len(prompts)), 1),
        "starts_lowercase": share(lambda t: t[:1].islower()),
        "ends_with_punctuation": share(lambda t: t.rstrip()[-1:] in ".!?"),
        "has_question": share(lambda t: "?" in t),
        "has_exclamation": share(lambda t: "!" in t),
        "filler_per_1k": {p: round(1000 * count(p) / n, 1) for p in FILLER if count(p)},
        "phrases_per_1k": {p: round(1000 * count(p) / n, 1) for p in PHRASES if count(p)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--extra", type=pathlib.Path, action="append", default=[])
    args = ap.parse_args()
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=args.days)
    sources = {"claude_code": claude(cutoff), "codex": codex(cutoff)}
    for p in args.extra:
        sources[f"extra:{p.name}"] = extra(p.expanduser(), cutoff)
    print(json.dumps({k: stats(v) for k, v in sources.items()}, indent=2))
    if args.sample:
        everything = [t for v in sources.values() for t in v]
        step = max(1, len(everything) // args.sample)
        print("\nRedacted sample (tone only, don't quote):")
        for t in everything[::step][: args.sample]:
            print("-", redact(t)[:300].replace("\n", " "))


if __name__ == "__main__":
    main()
