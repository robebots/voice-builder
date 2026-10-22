---
name: voice-builder
description: Builds and maintains a personal writing-voice skill from the person's own Slack and Gmail history plus a short guided interview, with separate registers for clients, internal comms, and close teammates. Use when someone says "build my voice", "set up my voice skill", "learn how I write", "refresh my voice", or a scheduled voice refresh runs. Not for drafting messages; the generated <name>-voice skill does that.
---

# Voice builder

This skill makes a small skill called `<first-name>-voice` that drafts messages the way the person writes. It learns from what they actually sent, asks how they want to sound, and keeps learning on a schedule. Every draft also follows the unslop rules in `references/unslop.md`.

There are two modes. **Setup** runs the first time, or when they ask to rebuild. **Refresh** runs on the schedule, or when they say "refresh my voice".

## Ground rules

- Read only. Never send, post, react, label, or create drafts in Slack or Gmail while building or refreshing.
- Analyze only messages the person wrote. Other people's messages are context for who the recipient is, nothing more.
- Files keep abstract patterns only, such as "opens client emails with 'Hi <first name>,'" or "lowercase in DMs, no sign-off". A recurring phrase of five words or fewer ("sounds good", "lmk") is fine if it holds no names, numbers, or business facts. Never store a message, a name, a client, a deal, or anything someone else wrote.
- If the voice skill already has its own rules about what to store or how rule changes get approved (check its `notes.md`), those win over this file.
- Show the person what you found before writing anything. They decide what goes in.
- Skip messages that are mostly code or links, auto-generated (calendar replies, forwards), or under four words.

## Setup

### 1. Check connections

Look for a Slack search tool and a Gmail search tool. If one is missing, say: "Connect Slack and Gmail in Settings → Connectors, then say 'build my voice' again." One source is enough to continue. Say which one you're working from.

Get their identity: the Slack profile of the current user (name, user ID) and their email address from a sent message. Their email domain is what "internal" means.

### 2. Warm-up questions

Use the AskUserQuestion tool. If it isn't available, ask in chat one question at a time. Ask these in one call:

1. "Who do you write to most?" (multiSelect) Clients or prospects / Leadership / Cross-team colleagues / Close teammates
2. "Where does most of your writing happen?" Slack / Email / About even
3. "What should this help with most?" Client replies / Quick Slack messages / Longer updates and docs / All of it
4. "Any habits you already want to drop?" (multiSelect) Over-explaining / Hedging and apologizing / Too many exclamation points / Sounding stiff

The default registers are **Clients** (external email and Slack Connect channels), **Internal** (team channels, leadership, cross-team email), and **Buddies** (DMs and small group DMs with people they talk to often). Add a register for anything they type under "Other" if you later find enough messages for it.

### 3. Pull samples

Go back 90 days. Aim for about 150 Slack messages and 40 sent emails, spread across channels, DMs, and recipients instead of the latest burst.

- Slack: search with filters `from:<@THEIR_ID> after:<YYYY-MM-DD>`. Run separate searches per `channel_types` (`im,mpim`, `private_channel`, `public_channel`) so DMs don't get crowded out. Turn off context to save space.
- Gmail: search `in:sent newer_than:90d`, then open a spread of threads for the bodies. Use only the part they wrote, not the quoted reply below it.

Sort each message into a register by recipient. Email to an outside domain or a Slack Connect channel goes to Clients. Internal email and team channels go to Internal. DMs and group DMs with frequent partners go to Buddies.

### 4. Analyze each register

For each register, write down findings with rough counts, not impressions:

- Length: words per Slack message, paragraphs per email
- Openers and sign-offs ("Hi X," / "Hey" / none; "Best," / "Thanks," / first name / none)
- Caps and punctuation: sentence case or lowercase, trailing periods in Slack, exclamation points per message, ellipses, em dashes
- Emoji, and whether reactions replace replies
- Directness: where the ask sits, how they say no, how they push back
- Softeners: "just", "I think", "sorry", "no worries if not"
- Recurring short phrases
- Structure: when they use bullets and when prose
- Humor, slang, or profanity, only if it repeats

Give each register a preset name, borrowed from Wispr Flow, so the person has a simple handle:

| Preset | What it looks like |
|---|---|
| Formal | Caps, full punctuation, greeting and sign-off |
| Casual | Caps, lighter punctuation, usually no sign-off |
| Very casual | Lowercase, minimal punctuation |
| Excited | Casual with exclamation points and emoji |

### 5. Guided review

Show a short summary per register: the preset, three to five findings with counts, and one sample sentence written in that style about a neutral topic like moving a meeting. Don't quote their real messages.

Then make one AskUserQuestion call with one question per register, for example "Clients: you write Formal, about 90 words, 'Hi <name>,' and 'Best,'. Keep it?" The options are Keep it (Recommended) / More casual / Shorter and more direct / More polished. Put the sample sentence rewritten in each style in that option's preview.

Then one more call:

- "Unslop would remove these habits of yours. Which should stay?" (multiSelect) List only the conflicts you actually found, such as em dashes, exclamation points with buddies, "let me know if", or emoji. Unslop wins for anything they don't pick.
- "Anything I should never do in your name?" (multiSelect) Offer things that fit what you saw, such as apologizing for slow replies, emoji with clients, or long emails, plus anything from warm-up question 4.

The difference between how they write and how they want to write is the most useful part. Write the version they want into the profile and note which observed habit it replaces.

### 6. Write the skill

Fill in `templates/voice-SKILL.md` and `templates/notes.md`, and copy `references/unslop.md` alongside them:

```
~/.claude/skills/<first-name>-voice/
  SKILL.md
  notes.md
  references/unslop.md
```

If you can't write to `~/.claude/skills` (for example in claude.ai chat), build the same folder as a zip and tell them to upload it in Settings → Capabilities → Skills. Scheduled refresh won't work there, so tell them to say "refresh my voice" once a month.

If `<first-name>-voice` already exists, don't overwrite it. Keep every rule they wrote, show the changes you'd make, apply only what they approve, and save the old file as `SKILL.md.bak`.

### 7. Test drive

Ask for something real they need to send soon, or use the meeting-move topic. Draft it once per register and ask "Which one sounds least like you?" with the drafts as options plus "They all sound right". Fix what they flag and add the lesson to `notes.md`.

### 8. Schedule the refresh

Ask "Should I check your sent messages and keep this current?" with Weekly (Recommended) / Monthly / Only when I ask. If they pick a schedule and a scheduled-task tool exists, create a task:

- taskId: `<first-name>-voice-refresh`
- cron: `0 9 * * 1` for weekly (Mondays 9am local) or `0 9 1 * *` for monthly
- prompt: "Use the voice-builder skill in Refresh mode for the <first-name>-voice skill at ~/.claude/skills/<first-name>-voice. Read-only on Slack and Gmail. Don't send, post, or draft anything. End with the three-line summary."

Tell them it runs while the Claude app is open, or at next launch if it was closed. If no scheduled-task tool exists, tell them to say "refresh my voice" on their own schedule.

## Refresh

1. Read `<first-name>-voice/SKILL.md` and `notes.md`, and find the last refresh date in `notes.md`.
2. Pull messages they sent since then, using the queries from setup step 3, capped at 100 Slack messages and 30 emails.
3. Compare each register to the profile. Write one dated note per real difference, abstract only, for example "2026-11-02 Buddies: lowercase in 18 of 20 DMs, profile says Casual."
4. Promote a pattern into `SKILL.md` once notes from two separate refreshes agree, or three notes of any kind do. Never change something the person chose in setup or wrote by hand; note the drift and ask them next time they use the skill. Record each change in the Changelog in `notes.md`.
5. Keep `notes.md` under 60 lines by folding promoted notes into their changelog line.
6. Update the last refresh date and end with three lines: messages read, notes added, rules changed. If nothing changed, say so.
