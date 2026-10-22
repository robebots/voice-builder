# voice-builder

Teaches your AI agent to write like you. It reads what you've sent on Slack and Gmail, plus your meeting transcripts (Circleback, Read AI, Granola, and others) and Wispr Flow dictation to learn how you talk. It skips anything that looks AI-drafted so it learns from you, not from AI. It figures out your role and the styles you use with clients, internal folks, and your work besties (email and Slack separately), asks a few questions about what it found, and builds you a personal voice skill. It also changes how the agent talks to you, so replies sound plain and a bit like you instead of like a chatbot. Everything follows the [unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) rules, and it re-checks your sent messages every week to stay current.

Works in Claude (desktop app or Claude Code), Codex, Kimi Code, and other agents that support skills. Setup takes about 15 minutes.

## Get started

Paste this into your agent:

```
Set up my writing voice from https://github.com/robebots/voice-builder
```

If Slack or Gmail isn't connected yet, it walks you through connecting them.

## What it does with your messages

It only reads, and it never sends, posts, or drafts anything in Slack or Gmail. In meeting transcripts it reads only what you said, and it skips HR, hiring, legal, and review meetings. It saves patterns like "lowercase in DMs, no sign-off" or "asks first, context second in client emails", not your messages, names, or client details. Everything it writes stays on your machine.

## After setup

- "draft this in my voice": uses your voice skill
- "that sounds too formal" (or any feedback on a draft): your voice skill records the lesson
- "refresh my voice": checks recent sent messages and updates everything (this also runs on the schedule you pick)

## For the agent doing the install

1. If you can run shell commands:
   ```bash
   git clone https://github.com/robebots/voice-builder ~/.agents/skills/voice-builder || git -C ~/.agents/skills/voice-builder pull
   ```
   If you're Claude Code, also link it so you can find it:
   ```bash
   mkdir -p ~/.claude/skills && ln -sfn ~/.agents/skills/voice-builder ~/.claude/skills/voice-builder
   ```
2. If you can't run commands (a chat-only app), tell them to download this repo as a zip (green Code button → Download ZIP) and upload it as a skill in their app's settings. In Claude that's Settings → Capabilities → Skills. Then they say "build my voice".
3. Read `~/.agents/skills/voice-builder/SKILL.md` and start Setup right away. Don't wait for a new session.

## Credits

`references/unslop.md` is from [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack), MIT License, Copyright (c) 2026 Lauren Tan.
