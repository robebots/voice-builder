"""Find the person's existing voice and writing setup. Read-only.

Looks at several signals instead of a fixed list, so it catches tools it has never heard of:
  - skills in every agent's skill folders (following symlinks), filtered to writing and voice skills
  - always-on instruction files, and whether they already hold writing rules or a voice-builder block
  - installed apps, classified from their own metadata (name, bundle ID, category, and why they ask for the microphone)
  - dictation or writing app installers sitting in Downloads that were never installed
  - browser extensions in Chrome, Arc, Brave, and Edge
  - MCP servers configured for Claude Code, Codex, and Kimi
Reads only metadata: skill frontmatter, headings, app Info.plist files, extension manifests, config keys.
Never reads messages, documents, or secrets (MCP config values are skipped, only server names are kept).

Usage: python3 -I scan_setup.py
"""
import json
import os
import pathlib
import plistlib
import re

HOME = pathlib.Path.home()
TILDE = lambda p: str(p).replace(str(HOME), "~")

SKILL_DIRS = ["~/.agents/skills", "~/.claude/skills", "~/.codex/skills", "~/.kimi-code/skills", "~/.kimi/skills",
              "~/.hermes/skills", "~/.claude/plugins", "~/.config/opencode/skills"]
INSTRUCTION_FILES = ["~/.claude/CLAUDE.md", "~/.codex/AGENTS.md", "~/.kimi/AGENTS.md", "~/.kimi-code/AGENTS.md",
                     "~/.agents/AGENTS.md", "~/.config/opencode/AGENTS.md"]

VOICE_TERMS = re.compile(r"\bvoice\b|\btone\b|writing style|\bunslop|humaniz|de-?slop|\bslop\b|sound(s)? like", re.I)
DRAFT_TERMS = re.compile(r"\bdraft|\bemail|follow-?up|proposal|newsletter|\bblog|announcement|copywrit|\bcopy\b|"
                         r"\breply|\bprose\b|one-?pager|\bposts?\b|linkedin|tweet|rewrite|\bedit(ing|or)\b", re.I)
DEV_TERMS = re.compile(r"\bhook|plugin|slash command|agent development|skill development|\bmcp\b|\bcode\b|commit", re.I)

DICTATION = re.compile(r"dictat|transcri|speech|speak|voice|whisper|meeting|record|notetak|note-?tak", re.I)
WRITING_APP = re.compile(r"grammar|writ(e|er|ing)|\bmail\b|superhuman|spark|notion|obsidian|\bbear\b|ulysses|"
                         r"raycast|textexpander|espanso|\blex\b|hemingway|quillbot|wordtune|jasper|copy\.ai|"
                         r"granola|otter|fathom|fireflies|circleback|read\.?ai|tactiq|willow|wispr|superwhisper|"
                         r"aqua|typeless|monologue|macwhisper|slack|gmail|outlook|linear", re.I)


def frontmatter(path):
    try:
        text = path.read_text(errors="ignore")[:4000]
    except OSError:
        return {}
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    out = {}
    for key in ("name", "description"):
        km = m and re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M)
        if km:
            out[key] = km.group(1).strip().strip('"')
    return out


def walk_skills(root, seen, max_depth=7):
    """os.walk that follows symlinks, without looping."""
    root_depth = len(root.parts)
    for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
        here = pathlib.Path(dirpath)
        real = here.resolve()
        if real in seen or len(here.parts) - root_depth > max_depth or {"node_modules", ".trash", ".git"} & set(here.parts):
            dirnames[:] = []
            continue
        seen.add(real)
        if "SKILL.md" in filenames:
            yield here


def skills():
    seen_dirs, seen_skills, found = set(), set(), []
    for d in SKILL_DIRS:
        root = pathlib.Path(d).expanduser()
        if not root.exists():
            continue
        for folder in walk_skills(root, seen_dirs):
            skill_md = folder / "SKILL.md"
            real = skill_md.resolve()
            if real in seen_skills:
                continue
            seen_skills.add(real)
            fm = frontmatter(skill_md)
            name, desc = fm.get("name", folder.name), fm.get("description", "")
            blob = f"{name} {desc[:400]}"
            voice = bool(VOICE_TERMS.search(blob)) or name.endswith("-voice")
            drafting = bool(DRAFT_TERMS.search(blob)) and not DEV_TERMS.search(blob)
            if voice or drafting:
                found.append({"name": name, "kind": "voice" if voice else "drafting", "description": desc[:200],
                              "folder": TILDE(folder), "real_folder": TILDE(real.parent),
                              "owned_by": "plugin or synced (read-only)" if re.search(r"plugins|synced", str(folder)) else "local"})
    return sorted(found, key=lambda s: (s["kind"] != "voice", s["name"]))


def instructions():
    out = []
    for f in INSTRUCTION_FILES:
        p = pathlib.Path(f).expanduser()
        if not p.exists():
            continue
        text = p.read_text(errors="ignore")
        out.append({
            "file": f,
            "symlink": p.is_symlink(),
            "generated_or_managed": bool(re.search(r"managed by|generated|do not edit|not this file", text[:400], re.I)),
            "has_voice_builder_block": "voice-builder:agent-voice" in text,
            "writing_headings": [h for h in re.findall(r"^#{1,3}\s+(.+)$", text, re.M) if VOICE_TERMS.search(h) or re.search(r"writ", h, re.I)][:8],
            "imports": [TILDE(i) for i in re.findall(r"^@(\S+)", text, re.M)][:10],
        })
    return out


def app_info(app):
    try:
        with open(app / "Contents/Info.plist", "rb") as fh:
            info = plistlib.load(fh)
    except Exception:
        return None
    return {
        "name": info.get("CFBundleDisplayName") or info.get("CFBundleName") or app.stem,
        "bundle_id": info.get("CFBundleIdentifier", ""),
        "category": (info.get("LSApplicationCategoryType") or "").replace("public.app-category.", ""),
        "mic_reason": info.get("NSMicrophoneUsageDescription", ""),
    }


def apps():
    roots = [pathlib.Path("/Applications"), pathlib.Path("/Applications/Setapp"), HOME / "Applications"]
    out = []
    for root in roots:
        if not root.exists():
            continue
        for app in root.glob("*.app"):
            info = app_info(app)
            if not info or info["bundle_id"].startswith("com.apple."):
                continue
            label = f"{info['name']} {info['bundle_id']}"
            dictation = bool(info["mic_reason"] and DICTATION.search(info["mic_reason"])) or bool(DICTATION.search(label))
            writing = bool(WRITING_APP.search(label)) or info["category"] in ("productivity", "business", "social-networking")
            if dictation or WRITING_APP.search(label):
                out.append({"name": info["name"], "bundle_id": info["bundle_id"],
                            "kind": "dictation or meetings" if dictation else "writing or messaging"})
            elif writing and info["mic_reason"]:
                out.append({"name": info["name"], "bundle_id": info["bundle_id"], "kind": "uses microphone"})
    return sorted(out, key=lambda a: (a["kind"], a["name"].lower()))


def downloaded_not_installed(installed):
    names = {a["name"].lower() for a in installed}
    out = []
    for f in (HOME / "Downloads").glob("*"):
        if f.suffix.lower() not in (".dmg", ".pkg", ".zip") or not (DICTATION.search(f.stem) or WRITING_APP.search(f.stem)):
            continue
        base = re.split(r"[ ._-](installer|setup|mac|darwin|universal|arm64|x64|\d)", f.stem, maxsplit=1, flags=re.I)[0].lower()
        if base and not any(base in n for n in names):
            out.append(f.name)
    return sorted(out)


def browser_extensions():
    roots = {"Chrome": "Google/Chrome", "Arc": "Arc/User Data", "Brave": "BraveSoftware/Brave-Browser", "Edge": "Microsoft Edge"}
    out = set()
    for browser, rel in roots.items():
        base = HOME / "Library/Application Support" / rel
        for manifest in base.glob("*/Extensions/*/*/manifest.json"):
            try:
                m = json.loads(manifest.read_text(errors="ignore"))
            except Exception:
                continue
            name = m.get("name", "")
            if name.startswith("__MSG_"):
                key = name[6:-2]
                for loc in ("en", "en_US", m.get("default_locale", "en")):
                    msgs = manifest.parent / "_locales" / loc / "messages.json"
                    if msgs.exists():
                        try:
                            data = json.loads(msgs.read_text(errors="ignore"))
                            name = next((v["message"] for k, v in data.items() if k.lower() == key.lower()), name)
                        except Exception:
                            pass
                        break
            if DICTATION.search(name) or WRITING_APP.search(name):
                out.add(f"{name} ({browser})")
    return sorted(out)


def mcp_servers():
    out = {}
    cj = HOME / ".claude.json"
    if cj.exists():
        try:
            data = json.loads(cj.read_text(errors="ignore"))
            names = set(data.get("mcpServers", {}))
            for proj in data.get("projects", {}).values():
                names |= set(proj.get("mcpServers", {}))
            out["claude_code"] = sorted(names)
        except Exception:
            pass
    for agent, path in (("codex", "~/.codex/config.toml"), ("kimi", "~/.kimi/config.toml"), ("kimi", "~/.kimi-code/config.toml")):
        p = pathlib.Path(path).expanduser()
        if p.exists():
            out.setdefault(agent, [])
            out[agent] += re.findall(r"^\[mcp_servers\.([^\].]+)\]", p.read_text(errors="ignore"), re.M)
    for agent, path in (("kimi", "~/.kimi/mcp.json"), ("kimi", "~/.kimi-code/mcp.json")):
        p = pathlib.Path(path).expanduser()
        if p.exists():
            try:
                out.setdefault(agent, [])
                out[agent] += list(json.loads(p.read_text(errors="ignore")).get("mcpServers", {}))
            except Exception:
                pass
    return out


if __name__ == "__main__":
    installed = apps()
    print(json.dumps({
        "voice_and_writing_skills": skills(),
        "instruction_files": instructions(),
        "apps": installed,
        "downloaded_not_installed": downloaded_not_installed(installed),
        "browser_extensions": browser_extensions(),
        "mcp_servers": mcp_servers(),
        "cannot_see": ["web-only tools", "phone apps", "connectors added on claude.ai or chatgpt.com",
                       "tools on another computer"],
    }, indent=2))
