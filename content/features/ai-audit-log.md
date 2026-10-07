---
uid: ai-audit-log
title: AI audit log
author: Morten Lønskov
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# AI audit log

Tabular Editor 3 Enterprise Edition keeps a local record of what the [AI Assistant](xref:ai-assistant) and the [MCP server](xref:mcp-server) did on this computer. It answers the question an auditor actually asks: which permissions were requested and how they were answered, which tools ran and how each one ended, and what any agent-written C# script contained.

The record is designed to be safe to collect. It captures *categories and outcomes*, never content. That is your prompts, the assistant's replies and data values from your model are never written to it.

## Where the record lives

Unless an administrator has moved it, the log is written to:

```
%LocalAppData%\TabularEditor3\AI\audit
```

Reach it with **Open audit folder**, which sits in two places: on **Tools > Preferences > AI Features**, and in the **Tools > MCP Server...** dialog. The folder is created the first time there's something to write, so on a fresh install there's nothing to open yet.

Inside it you'll find one file per day, `ai-audit-<date>.jsonl`, rolled over by UTC date, plus a `scripts` folder holding the scripts themselves under `scripts\<date>`.

## What is recorded

Each line is one JSON object. Every record opens with the same fields:

| Field | What it holds |
| -- | -- |
| `ts` | When it happened, UTC, to the millisecond |
| `event` | Which kind of record this is, from the table below |
| `surface` | `chat` for the AI Assistant, `mcp` for an external agent through the MCP server |
| `sessionId` | The conversation or MCP session the action belongs to. Absent when it belongs to neither |
| `model` | The name of the semantic model that was open. Absent when no model was |
| `user` | The Windows account name |

After those come the fields belonging to the event:

| `event` | Written when | What it carries |
| -- | -- | -- |
| `consent` | A permission is asked for | The resource, the access level, whether it was a one-off or a standing grant, whether you granted or denied it, and for how long |
| `tool_call` | A tool runs | The tool's name, the permissions it needed as `Resource:Access`, how it ended, how many milliseconds it took, the *names* of its arguments and the total size of their values in bytes |
| `script` | An agent runs or submits a C# script | The tool, the status, the outcome, the path of the saved copy, its SHA-256 hash and how many model changes it made |
| `turn` | A chat turn finishes | The provider, the model name, the endpoint host, the outcome, the turn number and the token counts, including what was cached and what was billed |
| `config` | The AI configuration changes | The provider, the model name and the endpoint host |
| `mcp_server` | The MCP server starts or stops | The port, whether an access token is required, and on start, the permission granted for each of the five resources |
| `mcp_session` | An agent connects or disconnects | The client's name and version, and the negotiated MCP protocol version |

A `tool_call` record ends one of five ways: `ok`, `error`, `denied` when the permission it needed wasn't granted, `policy` when an administrator's ceiling refused it, or `cancelled` when you stopped the turn or the client disconnected before it finished.

### Scripts are kept in full

The `script` event is the exception to "categories, not content", and deliberately so: a script an agent ran against your model is the thing you most need to be able to read afterwards. The script's text doesn't go into the log line. Instead the script is saved verbatim as its own `.csx` file under `scripts\<date>`, and the line points at that file and carries its SHA-256 hash, so you can prove the file on disk is the one that ran.

## What is never recorded

- The text of your prompts and the assistant's replies.
- Any value from your model. A `tool_call` records that a tool had arguments and how large they were, never what they said.
- API keys and access tokens.

## Retention

Files older than 30 days are deleted. The sweep runs once per session, before the first line is written, so a copy of Tabular Editor that's never opened never prunes.

Administrators can change the window, including keeping everything forever. See the policies below.

## Administering it

Two [policies](xref:policies) control the log. Both require Enterprise Edition.

| Value | Kind | What it does |
| -- | -- | -- |
| `AiAuditLogPath` | Path | Writes the log somewhere else, so it can be collected centrally. A UNC path to a network share works. The path has to be absolute; a relative one is ignored and the default folder is used |
| `AiAuditLogRetentionDays` | Number, 0 to 3650 | How many days to keep. `0` keeps everything. The default is 30 |

Redirecting the log moves the saved scripts with it, since they live inside the same folder.

Auditing never breaks the feature it audits. If the log can't be written, because a redirected share is unreachable for instance, the failure is noted once in Tabular Editor's own log and the AI Assistant and the MCP server carry on.

## See also

- @ai-assistant
- @mcp-server
- @policies
- @editions
