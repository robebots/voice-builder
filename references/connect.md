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

## No connection at all

Ask them to paste messages they sent, with names and client details swapped for placeholders if they like:

- 10 Slack messages: a few DMs, a few channel posts, and a longer one if they have it
- 5 sent emails: at least one internal and one external, if they write external email

That's enough for a first version. Say that it'll be rougher than one built from their full history, and that "refresh my voice" picks up more once they connect.
