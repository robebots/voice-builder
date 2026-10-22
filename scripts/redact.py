"""Redact private details from text before an agent reads it.

Usage: python3 -I redact.py < input.txt > redacted.txt
Also importable: from redact import redact
"""
import re
import sys

PATTERNS = [
    # secrets first, so later patterns don't split them
    (re.compile(r"\b(?:sk|pk|rk|ghp|gho|xox[abprs]|AKIA|AIza)[-_A-Za-z0-9]{12,}\b"), "[secret]"),
    (re.compile(r"\b[A-Za-z0-9_\-]{32,}\b"), "[secret]"),
    (re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"), "[email]"),
    (re.compile(r"https?://\S+|www\.\S+"), "[link]"),
    (re.compile(r"<[@#!][A-Z0-9|^>]+>"), "[mention]"),
    (re.compile(r"@[A-Za-z][\w.-]{1,30}"), "[mention]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[id]"),
    (re.compile(r"\b(?:\d[ -]?){13,19}\b"), "[number]"),
    (re.compile(r"(?:\+?\d{1,2}[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}\b"), "[phone]"),
    (re.compile(r"[$€£]\s?\d[\d,]*(?:\.\d+)?\s?(?:[kKmMbB]\b|million|billion)?"), "[amount]"),
    (re.compile(r"\b\d[\d,]*(?:\.\d+)?\s?(?:k|K|M|B|million|billion|dollars|bucks)\b"), "[amount]"),
    (re.compile(r"\b\d+\s+[A-Z][a-z]+\s+(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Lane|Ln|Dr|Drive)\b\.?"), "[address]"),
]

# Capitalized words that aren't sentence starts are usually names of people, companies, or projects.
COMMON = set("""I I'm I'll I've I'd OK Ok Okay Yes No Hey Hi Hello Thanks Thank So And But Or If When What Why How
Who Where Which The A An It It's That This Those These We We're You You're They They're He She Monday Tuesday
Wednesday Thursday Friday Saturday Sunday January February March April May June July August September October
November December Slack Gmail Google Zoom AI API PR PRs UI UX V1 V2 MVP CEO CTO QA OKR OKRs FYI ASAP TBD""".split())
NAME_RUN = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-z]+(?:[A-Z][a-z]+)*(?:\s+[A-Z][a-z]+)*)\b")


def _names(text: str) -> str:
    def swap(m):
        words = m.group(1).split()
        return m.group(0) if all(w in COMMON for w in words) else "[name]"
    return "\n".join(NAME_RUN.sub(swap, line) for line in text.split("\n"))


def redact(text: str) -> str:
    for pattern, label in PATTERNS:
        text = pattern.sub(label, text)
    return _names(text)


if __name__ == "__main__":
    sys.stdout.write(redact(sys.stdin.read()))
