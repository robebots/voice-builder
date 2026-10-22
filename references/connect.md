# Connecting Slack and Gmail

Walk the person through this one step at a time, only for what's missing, and only for the agent they're using. Wait for them to say it's done, then check that the tools work before moving on. If their workspace admin has to approve something, say so plainly and move on with what you have.

## Claude (desktop app, claude.ai, or Claude Code signed in with the same account)

1. Settings → Connectors.
2. Find Slack, click Connect, and sign in to the work Slack.
3. Find Gmail, click Connect, and sign in to the work Google account.
4. Start a new session so the tools load, then say "build my voice" again.

Claude Code in a terminal can also add Slack with `claude plugin install slack`, which asks for the Slack sign-in.

## Codex

- Slack: run `codex mcp add --transport http slack https://mcp.slack.com/mcp`, approve the Slack sign-in in the browser, then check with `codex mcp list`.
- Gmail: there's no official Gmail server for Codex yet. Use Slack only, or paste emails (below).

## Kimi Code and other agents

- Slack: add an MCP server pointing at `https://mcp.slack.com/mcp` using the agent's MCP settings, and sign in when it asks.
- Gmail: paste emails (below) unless they already have a Gmail tool.

## Meeting notetakers (optional)

Transcripts show how they talk, which is often warmer and clearer than how they write. Check for any of these, in this order:

1. A notetaker already connected to the agent: Circleback, Read AI, Granola, Fireflies, Otter, Fathom, or similar. Use its search and transcript tools.
2. Zoom or Google Meet transcripts saved to Google Drive, if a Drive tool is connected. Search for docs with "Transcript" in the title.
3. If they use a notetaker that isn't connected: in Claude, look for it under Settings → Connectors. In other agents, check the tool's site for an MCP server. If there's none, they can export three to five transcripts as text files and drop them in a folder for you to read.

## Wispr Flow (optional, Mac)

Wispr keeps dictation history on the machine, in `~/Library/Application Support/Wispr Flow/flow.sqlite` (table `History`). This path comes from community tools, not Wispr's docs, so check it exists first. Open it read-only (`sqlite3 -readonly`), look at the columns, and prefer the raw transcript over `formattedText`, since the formatted version has been polished by AI. If they've set Wispr to auto-delete or not store history, there's nothing to read, and that's fine.

## No connection at all

Ask them to paste messages they sent, with names and client details swapped for placeholders if they like:

- 10 Slack messages: a few DMs, a few channel posts, and a longer one if they have it
- 5 sent emails: at least one internal and one external, if they write external email

That's enough for a first version. Say that it'll be rougher than one built from their full history, and that "refresh my voice" picks up more once they connect.
