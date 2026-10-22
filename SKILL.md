---
name: voice-builder
description: Builds and maintains a personal writing-voice skill from the person's own Slack and Gmail history. It works out their role, the kinds of writing they do, and their registers (audience plus medium, like client emails or DMs with work besties), then asks only the clarifying questions the data can't answer. Use when someone says "build my voice", "set up my voice skill", "learn how I write", "refresh my voice", or a scheduled voice refresh runs. Not for drafting messages; the generated <name>-voice skill does that.
---

# Voice builder

This skill makes a small skill called `<first-name>-voice` that drafts messages the way the person writes. It reads what they actually sent, works out who they are and how they write, asks only what the messages can't settle, and keeps learning on a schedule. Every draft also follows the unslop rules in `references/unslop.md`.

There are two modes. **Setup** runs the first time, or when they ask to rebuild. **Refresh** runs on the schedule, or when they say "refresh my voice".

## Ground rules

- No questions before the analysis. Every question has to come from something you found and couldn't settle from the messages. If the data answers it, don't ask.
- Read only. Never send, post, react, label, or create drafts in Slack or Gmail while building or refreshing.
- Analyze only messages the person wrote. Other people's messages are context for who the recipient is, nothing more.
- Files keep abstract patterns only, such as "opens client emails with 'Hi <first name>,'" or "lowercase in DMs, no sign-off". A recurring phrase of five words or fewer ("sounds good", "lmk") is fine if it holds no names, numbers, or business facts. Never store a message, a name, a client, a deal, or anything someone else wrote.
- If the voice skill already has its own rules about what to store or how rule changes get approved (check its `notes.md`), those win over this file.
- Skip messages that are mostly code or links, auto-generated (calendar replies, forwards), or under four words.

## Setup

### 1. Check connections

Look for a Slack search tool and a Gmail search tool. If one is missing, say: "Connect Slack and Gmail in Settings → Connectors, then say 'build my voice' again." One source is enough to continue. Say which one you're working from.

Get their identity: the Slack profile of the current user (name, user ID, title) and their email address from a sent message. Their email domain is what "internal" means.

### 2. Pull samples

Go back 90 days. Aim for about 150 Slack messages and 40 sent emails, spread across channels, DMs, and recipients instead of the latest burst.

- Slack: search with filters `from:<@THEIR_ID> after:<YYYY-MM-DD>`. Run separate searches per `channel_types` (`im,mpim`, `private_channel`, `public_channel`) so DMs don't get crowded out. Turn off context to save space.
- Gmail: search `in:sent newer_than:90d`, then open a spread of threads for the bodies. Use only the part they wrote, not the quoted reply below it.

### 3. Work out who they are and what they write

**Role.** Start from their Slack title, then check it against what they actually write about. One line, like "Account executive, mostly post-call follow-ups and pricing questions" or "Staff engineer, mostly proposals and code review threads".

**Writing types.** Tag each message with what it's doing, and count them: quick reply or ack, ask or request, status update, proposal or decision, follow-up after a call or meeting, scheduling, pushback or saying no, explaining something, social chat. Note the types that make up most of their writing.

**Registers.** A register is an audience plus a medium, because people write differently in email and Slack even to the same person. Tag each message with both:

- Medium: Slack or email
- Audience: **Clients** (outside email domains, Slack Connect channels), **Leadership** (execs and their manager, going by Slack profile titles), **Internal** (team channels and other internal email), or **Work besties** (DMs and small group DMs with the handful of people they message most)

Each pair is a candidate register, like "Clients, email" or "Work besties, Slack". Keep a candidate that has at least 10 messages. Merge two that read the same (same length, caps, openers, and tone), and split one that clearly holds two styles. Most people end up with four to six. Track what you weren't sure how to classify; those become questions.

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

Also note when a writing type has its own shape across registers, like status updates always in bullets, or pushback always opening with a question.

Give each register a preset name, borrowed from Wispr Flow, so the person has a simple handle:

| Preset | What it looks like |
|---|---|
| Formal | Caps, full punctuation, greeting and sign-off |
| Casual | Caps, lighter punctuation, usually no sign-off |
| Very casual | Lowercase, minimal punctuation |
| Excited | Casual with exclamation points and emoji |

### 5. Show what you found

Before any question, show one short summary:

- Their role and the writing types that make up most of their messages, with rough shares
- Each register: preset, message count, three to five findings with counts, and one sample sentence in that style about a neutral topic like moving a meeting. Don't quote their real messages.
- Habits worth a look, with counts: hedging, apologizing, long wind-ups before the ask, exclamation points, anything unslop would cut

### 6. Clarifying questions

Use the AskUserQuestion tool, up to four questions per call and at most two calls. If the tool isn't available, ask in chat one at a time. Write questions the way a coworker would ask them: short, casual, and specific to what you found. Only ask what applies:

- **Classification you weren't sure about.** "Your DMs with three people read like client talk. Clients or teammates?" or "Looks like you're mostly in sales follow-ups. Right?"
- **Each register, biggest first.** "Client emails: you're pretty formal, about 90 words, 'Hi <name>,' and 'Best,'. Keep that?" Options: Keep it (Recommended) / Loosen it up / Shorter and more direct / More polished. Put the sample sentence rewritten in each style in that option's preview.
- **Habits the data flagged.** "You start a lot of asks to leadership with 'sorry' or 'just'. Cut that?" Only habits you actually counted.
- **Unslop conflicts.** "Unslop would cut these. Which ones are actually you?" (multiSelect) Only conflicts you found, such as em dashes, exclamation points with work besties, or emoji. Unslop wins for anything they don't pick.
- **Gaps that matter for their role.** If their role implies writing you barely saw, like client emails for someone in sales, ask whether they want a style for it and offer to start from their closest register.

The difference between how they write and how they want to write is the most useful part. Write the version they want into the profile, and note which observed habit it replaces.

### 7. Write the skill

Fill in `templates/voice-SKILL.md` and `templates/notes.md`, and copy `references/unslop.md` alongside them:

```
~/.claude/skills/<first-name>-voice/
  SKILL.md
  notes.md
  references/unslop.md
```

If you can't write to `~/.claude/skills` (for example in claude.ai chat), build the same folder as a zip and tell them to upload it in Settings → Capabilities → Skills. Scheduled refresh won't work there, so tell them to say "refresh my voice" once a month.

If `<first-name>-voice` already exists, don't overwrite it. Keep every rule they wrote, show the changes you'd make, apply only what they approve, and save the old file as `SKILL.md.bak`.

### 8. Test drive

Ask for something real they need to send soon, or use the meeting-move topic. Draft it in their two or three biggest registers and ask "Which one sounds least like you?" with the drafts as options plus "They all sound like me". Fix what they flag and add the lesson to `notes.md`.

### 9. Schedule the refresh

Ask "Want me to keep checking what you send so this stays current?" with Every week (Recommended) / Every month / Only when I ask. If they pick a schedule and a scheduled-task tool exists, create a task:

- taskId: `<first-name>-voice-refresh`
- cron: `0 9 * * 1` for weekly (Mondays 9am local) or `0 9 1 * *` for monthly
- prompt: "Use the voice-builder skill in Refresh mode for the <first-name>-voice skill at ~/.claude/skills/<first-name>-voice. Read-only on Slack and Gmail. Don't send, post, or draft anything. End with the three-line summary."

Tell them it runs while the Claude app is open, or at next launch if it was closed. If no scheduled-task tool exists, tell them to say "refresh my voice" on their own schedule.

## Refresh

1. Read `<first-name>-voice/SKILL.md` and `notes.md`, and find the last refresh date in `notes.md`.
2. Pull messages they sent since then, using the queries from setup step 2, capped at 100 Slack messages and 30 emails.
3. Compare each register to the profile. Write one dated note per real difference, abstract only, for example "2026-11-02 Work besties, Slack: lowercase in 18 of 20 DMs, profile says Casual." Note a new register or writing type if one shows up with 10 or more messages.
4. Promote a pattern into `SKILL.md` once notes from two separate refreshes agree, or three notes of any kind do. Never change something the person chose in setup or wrote by hand; note the drift and ask them next time they use the skill. Record each change in the Changelog in `notes.md`.
5. Keep `notes.md` under 60 lines by folding promoted notes into their changelog line.
6. Update the last refresh date and end with three lines: messages read, notes added, rules changed. If nothing changed, say so.
