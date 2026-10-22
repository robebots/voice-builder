# voice-builder

A Claude skill that learns how you write from your Slack and Gmail, then builds you a personal voice skill that drafts the way you do. It figures out your role, what you usually write, and the styles you use with clients, internal folks, and your work besties (email and Slack separately). Then it asks a few questions about what it found, and re-checks your sent messages every week to stay current. Drafts also follow the [unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) rules, so they don't read like AI.

Setup takes about 10 minutes.

## Install

1. In the Claude desktop app, connect Slack and Gmail under Settings → Connectors.
2. Open the Code tab, start a session in any folder, and paste:

```
Clone https://github.com/robebots/voice-builder into ~/.claude/skills/voice-builder (or git pull there if it already exists), then use the voice-builder skill to build my voice.
```

When it's done you'll have a skill named after you, like `sam-voice`. Say "draft this in my voice" anywhere in Claude Code to use it.

## What it does with your messages

It only reads, and it never sends, posts, or drafts anything in Slack or Gmail. It saves patterns like "lowercase in DMs, no sign-off" or "asks first, context second in client emails", not your messages, names, or client details. Everything it writes stays in `~/.claude/skills/<your-name>-voice/` on your machine.

## Commands

- "build my voice": first-time setup, or a rebuild
- "refresh my voice": check recent sent messages and update the profile (this also runs on the schedule you pick)
- "that sounds too formal" (or any feedback on a draft): your voice skill records the lesson

## Credits

`references/unslop.md` is from [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack), MIT License, Copyright (c) 2026 Lauren Tan.
