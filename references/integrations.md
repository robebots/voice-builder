# Hooking the voice into their tools

Run `python3 -I scripts/scan_setup.py` to see what they have. It reads only metadata. Then offer only what applies, and never change another app's settings or another skill's files yourself. Give them the setting to pick or the text to paste.

## Their existing voice and style skills

The scan marks these `kind: voice`, for example another `*-voice` skill, a humanizer, or a style guide.

- **One they wrote (local):** offer to merge its rules into `<first-name>-voice`, keeping their wording, or to keep both with the new voice skill winning on conflicts. Never delete theirs.
- **One from a plugin or synced from their org (read-only):** leave it alone. If it covers the same ground, say which one wins when. Org rules usually win for org documents.

## Skills that draft things for them

The scan marks these `kind: drafting`, for example follow-up emails, proposals, one-pagers, or posts. These are often org plugins, so don't edit them. Instead, add one line to the agent-voice block:

> When another skill drafts something {{First}} will send, write it in the `{{first}}-voice` skill's voice, inside that skill's own templates, rules, and red lines.

Name the skills you found so they know where this applies.

## Wispr Flow

The voice skill does the real code-switching, per person and per situation. Wispr's Styles page (left sidebar → Styles) only sets one tone per app category: Personal Messages, Work Messages, Email, and Other. It can't tell their manager from their work bestie. So treat it as a rough export: pick the anchor they use most in each category, and say plainly that dictation won't switch the way drafts do.

| Wispr category | Use their register | Note |
|---|---|---|
| Work Messages | Their most common Slack anchor | Very Casual isn't offered here. Casual is closest for lowercase writers. |
| Email | Their most common email anchor | Formal, Casual, or Excited |
| Personal Messages | Work besties, if they DM friends from personal apps | Very Casual is available here |
| Other | Their most common register | |

Styles only affect new dictations.

## Other dictation and writing apps

For anything else the scan found (Willow, Superwhisper, Raycast AI, Superhuman, Grammarly, ChatGPT or Claude profile preferences), check whether the app has a custom instructions, style, or tone setting. If it does, give them a short paste-in block, under 500 characters, built from the profile and scrubbed like everything else:

```
Write like me: <core voice in one line>. Switch by who it's for: <close teammates: e.g. lowercase, short>; <leadership or clients: e.g. full sentences, greeting>; bad news gets <e.g. longer, no jokes>. Match the other person's tone a notch. Never: <two or three don'ts>. No em dashes, no AI filler.
```

If an installer is sitting in Downloads but the app isn't installed, mention it once. Don't install anything.

## Agent sessions

Their prompts to coding agents are their rawest voice. With their OK, `scripts/agent_prompts.py` reads only what they typed or dictated to Claude Code and Codex (`--extra <folder>` for Kimi Code or others). It drops tool output, sub-agents, injected context, pastes, and code, and redacts what's left. Use it for:

- the agent-voice block: how they talk to you is the best guide for how you talk back
- their conversational profile, next to meeting transcripts

Raw prompts are full of typos and fragments. Learn the word choice and directness, not the mess.

## What the scan can't see

Web-only tools, phone apps, connectors added on claude.ai or chatgpt.com, and anything on another computer. Ask once: "Anything I missed? Other places you write or dictate?"
