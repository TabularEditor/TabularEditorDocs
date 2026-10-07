---
uid: ai-audit-log
title: AI audit log
author: Morten Lønskov
updated: 2026-09-23
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

Tabular Editor 3 [Enterprise Edition](xref:editions), including Trial licenses, writes a local log of [AI Assistant](xref:ai-assistant) and [MCP server](xref:mcp-server) activity on your computer. It records:

- which permissions were requested and how they were answered
- which tools ran and how each one ended
- the full text of any C# script the AI Assistant or an MCP agent ran or submitted to run

## Log location

Unless an administrator has moved it, the log is written to:

```text
%LocalAppData%\TabularEditor3\AI\audit
```

**Open audit folder** on **Tools > Preferences > AI Features** and in the **Tools > MCP Server...** dialog opens it. The folder is created when the first record is written and holds one `ai-audit-<date>.jsonl` file per UTC day, with saved scripts under `scripts\<date>`.

## What is recorded

Each line is one JSON object, and every record starts with the same fields:

| Field | What it holds |
| -- | -- |
| `ts` | When it happened, UTC, to the millisecond |
| `event` | Which kind of record this is, from the next table |
| `surface` | `chat` for the AI Assistant, `mcp` for an external agent through the MCP server |
| `sessionId` | The conversation or MCP session the action belongs to. Absent when it belongs to neither |
| `model` | The name of the semantic model that was open. Absent when no model was open |
| `user` | The Windows account name |

The fields that follow the common ones depend on the event:

| `event` | Written when | What it carries |
| -- | -- | -- |
| `consent` | A permission is requested | The resource, the access level, whether it was a one-off or a standing grant, whether you granted or denied it, and for how long |
| `tool_call` | A tool runs | The tool's name, the permissions it needed as `Resource:Access`, how it ended, how many milliseconds it took, the names of its arguments and the total size of their values in bytes |
| `script` | The AI Assistant or an MCP agent runs, or submits to run, a C# script | The tool, the status, the outcome, the path of the saved copy, its SHA-256 hash and how many model changes it made |
| `turn` | A chat turn finishes | The provider, the model name, the endpoint host, the outcome, the turn number and the token counts, including what was cached and what was billed |
| `config` | The AI configuration changes | The provider, the model name and the endpoint host |
| `mcp_server` | The MCP server starts or stops | The port, whether an access token is required, and on start, the permission granted for each of the five resources |
| `mcp_session` | An agent connects or disconnects | The client's name and version, and the negotiated MCP protocol version |

A `tool_call` record ends with one of these outcomes:

- `ok`
- `error`
- `denied`: the permission it needed wasn't granted
- `policy`: an administrator's limit blocked it
- `cancelled`: you stopped the turn, or the client disconnected before the tool finished

### Scripts are saved in full

Each script is saved verbatim as a `.csx` file under `scripts\<date>`, and the `script` record holds only the file's path and SHA-256 hash. Use the hash to verify that the file matches the script that ran.

## What is never recorded

- the text of your prompts and the assistant's replies
- any value from your model (a `tool_call` records only argument names and their total size)
- API keys and access tokens

## Retention

Log files and `scripts\<date>` folders older than 30 days are deleted by a cleanup that runs once per Tabular Editor session, before the first record is written. Administrators can change the retention period, or keep everything. See [Policies](#policies).

## Policies

These [policies](xref:policies), both of which require Enterprise Edition, control the log:

| Value | Kind | What it does |
| -- | -- | -- |
| `AiAuditLogPath` | Path | Writes the log to another folder for central collection, such as a UNC path to a network share. The path must be absolute; a relative path is ignored and the default folder is used |
| `AiAuditLogRetentionDays` | Number, 0 to 3650 | How many days to keep. `0` keeps everything. The default is 30 |

Redirecting the log also moves the saved scripts, and because the log is written with the signed-in user's Windows account, that account needs write access to a redirected folder.

If the log can't be written, for example because a network share is unreachable, Tabular Editor writes one information entry to its application log for the session and doesn't log later failures. The AI Assistant and the MCP server keep working.

## Next steps

- @ai-assistant
- @mcp-server
- @policies
- @editions
