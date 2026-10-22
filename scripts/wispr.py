"""Read the person's own words from Wispr Flow (dictations and recorded meetings), read-only.

Skips sensitive meetings by title, keeps only the person's own speaker turns, and redacts
everything before printing. By default it prints counts and patterns only, never text.

Usage:
  python3 -I wispr.py                      # stats only
  python3 -I wispr.py --sample 20          # plus 20 redacted turns to judge tone
  python3 -I wispr.py --include-named      # also use meetings titled with people's names (ask first)
  python3 -I wispr.py --db PATH            # non-default Wispr data folder
"""
import argparse
import collections
import json
import pathlib
import re
import sqlite3
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from redact import redact  # noqa: E402

DEFAULT = pathlib.Path.home() / "Library/Application Support/Wispr Flow"
SENSITIVE = re.compile(
    r"interview|candidate|hiring|recruit|offer|salary|comp(ensation)?\b|payroll|benefit|hr\b|people ops|"
    r"performance|review cycle|1:1 review|pip\b|legal|lawyer|attorney|contract|nda|medical|doctor|therap|"
    r"health|family|parent|custody|divorce|dating|bank|loan|mortgage|tax|invest|personal",
    re.I,
)
FILLER = ["like", "you know", "i mean", "kind of", "sort of", "basically", "um", "uh", "actually", "just"]
PHRASES = ["i think", "we should", "the thing is", "the problem", "for example", "what if", "let's",
           "figure out", "does that make sense", "my concern", "i want", "we need"]


def connect(base):
    return sqlite3.connect(f"file:{base / 'flow.sqlite'}?mode=ro", uri=True)


def dictations(db):
    cols = {r[1] for r in db.execute("PRAGMA table_info(History)")}
    raw = "asrText" if "asrText" in cols else None
    if not raw:
        return []
    return [r[0] for r in db.execute(f"select {raw} from History where {raw} is not null and length({raw}) > 0")]


def names_in(smap):
    return {w.lower() for p in smap.get("people", {}).values() for w in (p.get("name") or "").split() if len(w) > 1}


def meeting_turns(db, base, include_named=False):
    turns, kept, skipped = [], 0, collections.Counter()
    for mid, title, smap in db.execute("select id, coalesce(title,''), speakerMap from Meetings where isDeleted = 0"):
        smap = json.loads(smap or "{}")
        if not title.strip():
            skipped["untitled"] += 1
            continue
        if SENSITIVE.search(title):
            skipped["sensitive title"] += 1
            continue
        # Titles that are just people's names ("Sam and Rob", "30 min with Sam") could be anything, interviews included.
        if not include_named and {w.lower() for w in re.findall(r"[A-Za-z]+", title)} & names_in(smap):
            skipped["named 1:1"] += 1
            continue
        me = {pid for pid, p in smap.get("people", {}).items() if p.get("origin") == "self"}
        labels = {str(k) for k, a in smap.get("assignments", {}).items()
                  if (a.get("consensus") or a.get("user") or a.get("mic") or a.get("llm")) in me}
        f = base / "meetings" / mid / "refined.ndjson"
        if not labels or not f.exists():
            skipped["no speaker match"] += 1
            continue
        kept += 1
        for line in f.read_text().splitlines():
            d = json.loads(line)
            if str(d.get("speaker", {}).get("id")) in labels and d.get("text", "").strip():
                turns.append(d["text"].strip())
    return turns, kept, skipped


def stats(turns):
    words = [w for t in turns for w in re.findall(r"[a-z']+", t.lower())]
    text = " " + " ".join(words) + " "
    n = max(1, len(words))
    sents = [s for t in turns for s in re.split(r"[.!?]+", t) if s.strip()]
    count = lambda p: len(re.findall(rf"(?<![a-z']){re.escape(p)}(?![a-z'])", text))
    return {
        "turns": len(turns),
        "words": len(words),
        "words_per_turn": round(len(words) / max(1, len(turns)), 1),
        "words_per_sentence": round(len(words) / max(1, len(sents)), 1),
        "turns_with_question": sum("?" in t for t in turns),
        "filler_per_1k": {p: round(1000 * count(p) / n, 1) for p in FILLER if count(p)},
        "phrases_per_1k": {p: round(1000 * count(p) / n, 1) for p in PHRASES if count(p)},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=pathlib.Path, default=DEFAULT)
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--include-named", action="store_true", help="also use meetings titled with people's names")
    args = ap.parse_args()
    if not (args.db / "flow.sqlite").exists():
        print(json.dumps({"error": "no Wispr Flow history found", "path": str(args.db)}))
        return
    db = connect(args.db)
    d = dictations(db)
    turns, kept, skipped = meeting_turns(db, args.db, args.include_named)
    out = {
        "dictations": stats(d),
        "meetings_used": kept,
        "meetings_skipped": dict(skipped),
        "meeting_turns": stats(turns),
    }
    print(json.dumps(out, indent=2))
    if args.sample:
        longest = sorted(turns + d, key=lambda t: -len(t.split()))[: args.sample * 3]
        step = max(1, len(longest) // max(1, args.sample))
        print("\nRedacted sample (tone only, don't quote):")
        for t in longest[::step][: args.sample]:
            print("-", redact(t)[:300])


if __name__ == "__main__":
    main()
