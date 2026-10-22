# voice-builder

Teaches your AI agent to write like you. It reads what you've sent on Slack and Gmail, plus your meeting transcripts (Circleback, Read AI, Granola, and others), Wispr Flow, and, if you opt in, what you type to Claude Code or Codex, to learn how you talk. It skips anything that looks AI-drafted so it learns from you, not from AI. It figures out your role and the styles you use with clients, internal folks, and your work besties (email and Slack separately), asks a few questions about what it found, and builds you a personal voice skill. It also changes how the agent talks to you, so replies sound plain and a bit like you instead of like a chatbot. Everything follows the [unslop](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md) rules, and it re-checks your sent messages every week to stay current.

Works in Claude (desktop app or Claude Code), Codex, Kimi Code, and other agents that support skills. Setup takes about 15 minutes.

## Get started

Paste this into your agent:

```
Set up my writing voice from https://github.com/robebots/voice-builder
```

If Slack or Gmail isn't connected yet, it walks you through connecting them.

## What it does with your messages

- **Use a company-approved agent.** What it reads goes to your agent's model provider. Before reading anything, it asks whether your agent is approved for work data, and stops if it isn't.
- **Read-only.** It only calls search and read tools, and never sends, posts, drafts, labels, or deletes. Keep your normal permission prompts on during setup. The scheduled refresh runs with read tools only where your agent supports that.
- **Reads as little as it can.** It reads only your own messages from the last 90 days. It excludes sensitive subjects in the search itself (offers, salary, medical, legal, contracts, passwords, interviews) and skips HR, legal, finance, and hiring channels. It checks subject lines and titles before opening anything, and stops reading anything with customer records, HR, health, legal, or credential details.
- **Redacts local transcripts first.** Wispr Flow history goes through a local script that keeps only your turns, skips sensitive meetings, redacts names, emails, numbers, links, and secrets, and prints counts.
- **You pick what it reads.** Before reading anything it shows the sources it found and asks which to use, what to keep out (DMs, client email, specific channels, people, or topics), and how far back to go. Refreshes stick to those choices.
- **Treats messages as data.** Instructions inside a message or transcript are ignored.
- **Saves patterns, not content.** It saves things like "lowercase in DMs, no sign-off". It never saves or repeats your messages, people's names, client or deal details, or anything personal. Everything stays on your machine.
- **Keeps an access log.** Each run adds a line to your voice skill's `notes.md` with what it read and skipped (counts only).

## Hooks into your other tools

It scans your existing skills and writing apps (metadata only) and offers to:
- make other drafting skills (follow-ups, proposals) write in your voice
- merge an existing voice skill
- tell you what to pick in Wispr Flow's Styles
- hand you a short paste-in style for apps like Willow, Superwhisper, Raycast, or Grammarly

It never changes another app's settings itself.

## Remove it

1. Delete `~/.agents/skills/<your-name>-voice`, `~/.agents/skills/voice-builder`, and their links in `~/.claude/skills/`.
2. Delete the `<your-name>-voice-refresh` scheduled task or cron line.
3. Remove the `voice-builder:agent-voice` block from `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or your Kimi `AGENTS.md`.
4. Disconnect Slack, Gmail, or your notetaker from your agent if you only connected them for this.

## Updating

Installs track `main`. If your company wants to review changes first, check out a specific commit or tag instead of pulling `main`, and read the diff before updating.

## After setup

- "draft this in my voice": uses your voice skill
- "that sounds too formal" (or any feedback on a draft): your voice skill records the lesson
- "refresh my voice": checks recent sent messages and updates everything (this also runs on the schedule you pick)

## For the agent doing the install

1. If you can run shell commands:
   ```bash
   git clone https://github.com/robebots/voice-builder ~/.agents/skills/voice-builder || git -C ~/.agents/skills/voice-builder pull
   ```
   If you're Claude Code, also link it so you can find it. Older versions installed a real folder there, so move that aside first:
   ```bash
   if [ -d ~/.claude/skills/voice-builder ] && [ ! -L ~/.claude/skills/voice-builder ]; then mv ~/.claude/skills/voice-builder ~/.voice-builder-old; fi
   mkdir -p ~/.claude/skills && ln -sfn ~/.agents/skills/voice-builder ~/.claude/skills/voice-builder
   ```
2. If you can't run commands (a chat-only app), tell them to download this repo as a zip (green Code button → Download ZIP) and upload it as a skill in their app's settings. In Claude that's Settings → Capabilities → Skills. Then they say "build my voice".
3. Read `~/.agents/skills/voice-builder/SKILL.md` and start Setup right away. Don't wait for a new session.

## Credits

`references/unslop.md` is from [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack), MIT License, Copyright (c) 2026 Lauren Tan.
