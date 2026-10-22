---
name: voice-builder
description: Builds and maintains a personal writing-voice skill from the person's own Slack and Gmail history. It works out their role, the kinds of writing they do (including formal writing like PRs, proposals, or policies), and their registers (audience plus medium), then asks only the clarifying questions the data can't answer. It also sets how the agent itself talks to them. Works in Claude Code, Codex, Kimi Code, and other agents that read SKILL.md. Use when someone says "build my voice", "set up my voice skill", "learn how I write", "refresh my voice", or a scheduled voice refresh runs.
---

# Voice builder

This skill makes two things:

1. A skill called `<first-name>-voice` that drafts what the person sends to other people, the way they write it, in the right register and role.
2. A short block in the agent's always-on instructions that sets how the agent talks to the person: unslopped, plain, in their register, using some of their own words back to them.

It reads what they actually sent, works out who they are and how they write, asks only what the messages can't settle, and keeps learning on a schedule. Unslop rules (`references/unslop.md`) apply to everything it writes.

There are two modes. **Setup** runs the first time, or when they ask to rebuild. **Refresh** runs on the schedule, or when they say "refresh my voice".

## Ground rules

- No questions before the analysis. Every question has to come from something you found and couldn't settle from the messages. If the data answers it, don't ask.
- Read only. Never send, post, react, label, or create drafts in Slack or Gmail while building or refreshing.
- Analyze only messages the person wrote. Other people's messages are context for who the recipient is, nothing more.
- Files keep abstract patterns only, such as "opens client emails with 'Hi <first name>,'" or "lowercase in DMs, no sign-off". A recurring word or phrase of five words or fewer ("sounds good", "lmk") is fine if it holds no names, numbers, or business facts. Never store a message, a name, a client, a deal, or anything someone else wrote.
- If the voice skill or an instruction file already has its own rules about what to store or who approves changes, those win over this file.
- Skip messages that are mostly code or links, auto-generated (calendar replies, forwards), or under four words.

## Works in any agent

Use whatever your agent has, and say what you're using.

- **Questions:** if you have a multiple-choice question tool (AskUserQuestion in Claude Code, or your agent's equivalent), use it. Otherwise ask in chat as one numbered list with lettered options, and let them answer in one line.
- **Slack and Gmail:** any connected Slack or Gmail tools work (MCP servers, connectors, apps). If one is missing, guide them through `references/connect.md`.
- **Skills folder:** install to `~/.agents/skills/<first-name>-voice/`. Codex and Kimi Code read that folder. If they use Claude Code, also symlink `~/.claude/skills/<first-name>-voice` to it. If you can't write files at all (a chat-only app), build the folder as a zip for them to upload.
- **Always-on instructions:** Claude Code reads `~/.claude/CLAUDE.md`, Codex reads `~/.codex/AGENTS.md`, and Kimi Code reads `~/.kimi/AGENTS.md` (newer installs: `~/.kimi-code/AGENTS.md`). Only touch the files for agents whose folder exists on this machine.

## Setup

### 1. Check connections

Find the Slack and Gmail tools. If either is missing, walk them through `references/connect.md` for their agent before going further. Don't just point them at it. One source is enough to continue if they can't connect the other. Say which one you're working from.

Get their identity: their Slack profile (name, user ID, title) and their email address from a sent message. Their email domain is what "internal" means.

### 2. Pull samples

Go back 90 days. Aim for about 150 Slack messages and 40 sent emails, spread across channels, DMs, and recipients instead of the latest burst.

- Slack: search messages from their user ID after the start date. Search DMs and group DMs, private channels, and public channels separately so DMs don't get crowded out. Skip surrounding context to save space.
- Gmail: search `in:sent newer_than:90d`, then open a spread of threads for the bodies. Use only the part they wrote, not the quoted reply below it.

### 3. Work out who they are and what they write

**Role.** Start from their Slack title, then check it against what they write about. One line, like "Account executive, mostly post-call follow-ups and pricing questions". Find the closest row in `references/roles.md`.

**Writing types.** Tag each message with what it's doing, and count them: quick reply or ack, ask or request, status update, proposal or decision, follow-up after a call, scheduling, pushback or saying no, explaining something, sharing a link, social chat.

**Formal writing.** Slack and email rarely show it, but it's most of what an agent will draft. From their role row, list the formal writing they probably do (PRs and RFCs for engineers, proposals for sales, policies for HR). Note any you actually saw.

**Registers.** A register is an audience plus a medium, because people write differently in email and Slack even to the same person. Tag each message with both:

- Medium: Slack or email
- Audience: **Clients** (outside email domains, Slack Connect channels), **Leadership** (execs and their manager, going by Slack profile titles), **Internal** (team channels and other internal email), or **Work besties** (DMs and small group DMs with the handful of people they message most)

Each pair is a candidate register, like "Clients, email" or "Work besties, Slack". Keep a candidate that has at least 10 messages. Merge two that read the same, and split one that clearly holds two styles. Most people end up with four to six. Track what you weren't sure how to classify; those become questions.

### 4. Analyze each register

For each register, write down findings with rough counts, not impressions:

- Length: words per Slack message, paragraphs per email
- Openers and sign-offs
- Caps and punctuation: sentence case or lowercase, trailing periods, exclamation points, ellipses, em dashes
- Emoji, and whether reactions replace replies
- Directness: where the ask sits, how they say no, how they push back
- Softeners: "just", "I think", "sorry", "no worries if not"
- Recurring words and short phrases (these also feed the agent voice)
- Structure: when they use bullets and when prose
- Humor, slang, or profanity, only if it repeats

Also note when a writing type has its own shape across registers, like status updates always in bullets.

Give each register a preset name, borrowed from Wispr Flow:

| Preset | What it looks like |
|---|---|
| Formal | Caps, full punctuation, greeting and sign-off |
| Casual | Caps, lighter punctuation, usually no sign-off |
| Very casual | Lowercase, minimal punctuation |
| Excited | Casual with exclamation points and emoji |

### 5. Show what you found

Before any question, show one short summary:

- Their role, the writing types that make up most of their messages with rough shares, and the formal writing their role usually involves
- Each register: preset, message count, three to five findings with counts, and one sample sentence in that style about a neutral topic like moving a meeting. Don't quote their real messages.
- Habits worth a look, with counts: hedging, apologizing, long wind-ups before the ask, exclamation points, anything unslop would cut

### 6. Clarifying questions

Up to four questions per round and at most three rounds. Write them the way a coworker would ask: short, casual, and about what you found. Only ask what applies.

**Round 1: role and formal writing.** Always ask these two, because messages can't fully answer them:

- "Looks like you're a <role>, mostly <top writing types>. Right?" Options: Yes / plus the two closest roles from `references/roles.md`.
- "Besides Slack and email, what do you want help writing?" (multiSelect) Offer the formal writing from their role row.

Then ask them to point at one or two examples of the formal writing they picked: a link you can read (a PR, a Google Doc) or pasted text. Analyze those like a register: structure, length, how they open, what they always include. If they have none, start from the role defaults plus their most formal register, and say so. If their company has a template or skill for that document type, note it as the thing to follow.

**Round 2: registers.**

- Classification you weren't sure about: "Your DMs with three people read like client talk. Clients or teammates?"
- Each register, biggest first: "Client emails: you're pretty formal, about 90 words, 'Hi <name>,' and 'Best,'. Keep that?" Options: Keep it (Recommended) / Loosen it up / Shorter and more direct / More polished, each with the sample sentence rewritten in that style as a preview.

**Round 3: habits.**

- Habits the data flagged: "You start a lot of asks to leadership with 'sorry' or 'just'. Cut that?" Only habits you actually counted.
- Unslop conflicts: "Unslop would cut these. Which ones are actually you?" (multiSelect) Only conflicts you found. Unslop wins for anything they don't pick, and always wins in formal writing.

The difference between how they write and how they want to write is the most useful part. Write the version they want into the profile, and note which observed habit it replaces.

### 7. Write the voice skill

Fill in `templates/voice-SKILL.md` and `templates/notes.md`, and copy `references/unslop.md` alongside them:

```
~/.agents/skills/<first-name>-voice/
  SKILL.md
  notes.md
  references/unslop.md
```

Then add the Claude Code symlink if they use Claude Code. If `<first-name>-voice` already exists, don't overwrite it. Keep every rule they wrote, show the changes you'd make, apply only what they approve, and save the old file as `SKILL.md.bak`.

### 8. Set the agent's own voice

Fill in `templates/agent-voice.md` from what you found: their register with you (usually their work-besties or internal style, one notch more careful), their typical length, up to 10 of their recurring words, and their role. Show the filled block and ask "Want me to talk to you like this too?" with Yes / Change something / No.

On yes, add the block to each always-on instruction file for agents they have. If the file already has a `voice-builder:agent-voice` block, replace that block only. Create the file if the agent's folder exists but the file doesn't. If a file is a symlink, is generated by a script, or says someone else owns it, don't edit it: show the block and say where it should go instead.

### 9. Test drive

Ask for something real they need to send soon, or use the meeting-move topic. Draft it in their two biggest registers, plus one piece of formal writing they picked, and ask "Which one sounds least like you?" with the drafts as options plus "They all sound like me". Fix what they flag and add the lesson to `notes.md`.

### 10. Schedule the refresh

Ask "Want me to keep checking what you send so this stays current?" with Every week (Recommended) / Every month / Only when I ask.

- If the agent has a scheduled-task tool (Claude desktop has one), create a task named `<first-name>-voice-refresh` that runs Mondays at 9am local (`0 9 * * 1`) or the 1st of the month (`0 9 1 * *`).
- Otherwise, offer a cron entry that runs their agent's non-interactive mode with the prompt below (for example `codex exec "<prompt>"`, or `claude -p "<prompt>"`; check the CLI's `--help` for others). Show the exact line and add it only if they say yes.
- The prompt: "Use the voice-builder skill in Refresh mode for the <first-name>-voice skill at ~/.agents/skills/<first-name>-voice. Read-only on Slack and Gmail. Don't send, post, or draft anything. End with the three-line summary."

If nothing can run on a schedule, tell them to say "refresh my voice" once a month.

## Refresh

1. Read `<first-name>-voice/SKILL.md` and `notes.md`, and find the last refresh date in `notes.md`.
2. Pull messages they sent since then, using the queries from setup step 2, capped at 100 Slack messages and 30 emails.
3. Compare each register to the profile. Write one dated note per real difference, abstract only, for example "2026-11-02 Work besties, Slack: lowercase in 18 of 20 DMs, profile says Casual." Note a new register or writing type if one shows up with 10 or more messages, and any new recurring words.
4. Promote a pattern into `SKILL.md` once notes from two separate refreshes agree, or three notes of any kind do. Never change something the person chose in setup or wrote by hand; note the drift and ask them next time they use the skill. Record each change in the Changelog in `notes.md`.
5. If the recurring words or their register with you changed, update the `voice-builder:agent-voice` blocks too, following the same ownership rule as setup step 8.
6. Keep `notes.md` under 60 lines by folding promoted notes into their changelog line.
7. Update the last refresh date and end with three lines: messages read, notes added, rules changed. If nothing changed, say so.
