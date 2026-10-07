---
uid: ai-audit-log
title: AI 审计日志
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

# AI 审计日志

Tabular Editor 3 [Enterprise Edition](xref:editions), including Trial licenses, writes a local log of [AI Assistant](xref:ai-assistant) and [MCP server](xref:mcp-server) activity on your computer. It records:

- which permissions were requested and how they were answered
- which tools ran and how each one ended
- the full text of any C# script the AI Assistant or an MCP agent ran or submitted to run

## Log location

除非管理员把它移到了别处，否则日志会写入：

```text
%LocalAppData%\TabularEditor3\AI\audit
```

**Open audit folder** on **Tools > Preferences > AI Features** and in the **Tools > MCP Server...** dialog opens it. The folder is created when the first record is written and holds one `ai-audit-<date>.jsonl` file per UTC day, with saved scripts under `scripts\<date>`.

## 记录了什么

Each line is one JSON object, and every record starts with the same fields:

| 字段          | 内容                                                |
| ----------- | ------------------------------------------------- |
| `ts`        | 发生时间，UTC，精确到毫秒                                    |
| `event`     | Which kind of record this is, from the next table |
| `surface`   | AI 助手使用 `chat`，通过 MCP 服务器连接的外部代理使用 `mcp`          |
| `sessionId` | 该操作所属的对话或 MCP 会话。若两者都不属于，则不包含该字段                  |
| `model`     | 当时打开的语义模型名称。 Absent when no model was open        |
| `user`      | Windows 账户名称                                      |

The fields that follow the common ones depend on the event:

| `event`       | 在以下情况下写入                                                              | 包含内容                                                                                                                                                                                 |
| ------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `consent`     | A permission is requested                                             | 资源、访问级别、它是一次性授权还是持续授权、你是批准还是拒绝，以及授权时长                                                                                                                                                |
| `tool_call`   | 工具运行时                                                                 | The tool's name, the permissions it needed as `Resource:Access`, how it ended, how many milliseconds it took, the names of its arguments and the total size of their values in bytes |
| `script`      | The AI Assistant or an MCP agent runs, or submits to run, a C# script | 工具、状态、结果、已保存副本的路径、其 SHA-256 哈希，以及它对模型做出的更改次数                                                                                                                                         |
| `turn`        | 一次聊天轮次结束时                                                             | 提供方、模型名称、端点主机、结果、轮次编号以及 Token 数量，包括缓存量和计费量                                                                                                                                           |
| `config`      | AI 配置变更                                                               | 提供方、模型名称和端点主机                                                                                                                                                                        |
| `mcp_server`  | MCP 服务器启动或停止                                                          | 端口、是否需要访问令牌，以及在启动时为五类资源分别授予的权限                                                                                                                                                       |
| `mcp_session` | 智能体连接或断开连接                                                            | 客户端名称和版本，以及协商确定的 MCP 协议版本                                                                                                                                                            |

A `tool_call` record ends with one of these outcomes:

- `ok`
- `error`
- `denied`: the permission it needed wasn't granted
- `policy`: an administrator's limit blocked it
- `cancelled`: you stopped the turn, or the client disconnected before the tool finished

### Scripts are saved in full

Each script is saved verbatim as a `.csx` file under `scripts\<date>`, and the `script` record holds only the file's path and SHA-256 hash. Use the hash to verify that the file matches the script that ran.

## 绝不会记录的内容

- the text of your prompts and the assistant's replies
- any value from your model (a `tool_call` records only argument names and their total size)
- API keys and access tokens

## 保留期

Log files and `scripts\<date>` folders older than 30 days are deleted by a cleanup that runs once per Tabular Editor session, before the first record is written. Administrators can change the retention period, or keep everything. See [Policies](#policies).

## 策略

These [policies](xref:policies), both of which require Enterprise Edition, control the log:

| 值                         | 类型          | 作用                                                                                                                                                                                                   |
| ------------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AiAuditLogPath`          | 路径          | Writes the log to another folder for central collection, such as a UNC path to a network share. The path must be absolute; a relative path is ignored and the default folder is used |
| `AiAuditLogRetentionDays` | 数值，0 到 3650 | 保留天数。 `0` 表示全部保留。默认值为 30                                                                                                                                                                             |

Redirecting the log also moves the saved scripts, and because the log is written with the signed-in user's Windows account, that account needs write access to a redirected folder.

If the log can't be written, for example because a network share is unreachable, Tabular Editor writes one information entry to its application log for the session and doesn't log later failures. The AI Assistant and the MCP server keep working.

## 后续步骤

- @ai-assistant
- @mcp-server
- @policies
- @editions
