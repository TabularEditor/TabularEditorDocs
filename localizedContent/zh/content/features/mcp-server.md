---
uid: mcp-server
title: MCP 服务器
author: Morten Lønskov
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# MCP 服务器

Tabular Editor 3 可以充当 MCP（Model Context Protocol）服务器。 Agents that support MCP, such as Claude Code, GitHub Copilot, VS Code agent mode, Codex or Cursor, connect to the running instance to read, query and analyze the semantic model you have open, and to change it if you grant write access. To start, select **Tools > MCP Server...** and register your agent.

The MCP server doesn't use an AI provider or API key configured in Tabular Editor, and your agent uses its own provider and subscription.

The agent works on the model Tabular Editor has open, including unsaved changes. That can be a Power BI Desktop model, a PBIP project, a TMDL (Tabular Model Definition Language) folder, a `.bim` file, a workspace database or a live connection to Analysis Services, Azure Analysis Services or Fabric. The agent uses the same tools whether the model is connected or offline, except for tools that need a live connection, such as DAX queries.

Agent changes go through the [Tabular Object Model (TOM) wrapper](xref:csharp-scripts) and the C# scripting engine, with the same validation, formula fix-up and undo stack as your own edits. They appear as unsaved changes, marked in the [TOM Explorer and the Properties view](xref:unsaved-changes), and nothing is written to the source until you save.

## 开始之前

- Tabular Editor 3.27.0 或更高版本，任何版本均可。
- 已安装 **AI 功能** 组件。从 3.27.0 开始，它已包含在默认安装中。如果你以集中方式部署 Tabular Editor，请参阅 @installation-activation-basic；如果管理员已关闭 AI 功能，请参阅 @policies。
- 支持通过可流式传输的 HTTP 使用 MCP 的代理。

## 启动服务器

1. Select **Tools > MCP Server...**.
2. Review the permissions. See [Set agent permissions](#set-agent-permissions).
3. 点击 **启动服务器**。

The dialog shows the address the server listens on: `http://127.0.0.1:42100/` unless you've changed the port. The status bar indicator changes from **MCP Stopped** to **MCP Started**, with the address in its tooltip.

![The MCP Server dialog, showing the server URL, a masked access token and the five agent permission rows set to non-default levels](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![MCP 状态栏指示器显示 MCP Started，其工具提示显示 "MCP 服务器正在侦听 http://127.0.0.1:42100/。点击以打开连接对话框。"](~/content/assets/images/features/mcp-server/status-bar-menu.png)

The server runs with or without a model open. If no model is open, the tool results say so, and you can open a model at any time without restarting the server.

Right-click the status bar indicator to start or stop the server, copy a registration configuration or open the MCP Server preferences. Left-click it to open the dialog without starting or stopping the server.

![MCP 状态栏指示器及其已打开的右键菜单，菜单项包括“MCP 服务器详细信息...”、“停止 MCP 服务器”、“复制 MCP 配置”和“MCP 服务器偏好...”，其中“复制 MCP 配置”子菜单已展开，列出 Claude Code、VS Code、Copilot CLI、Codex 和 Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### MCP 偏好

Open **Tools > Preferences > AI Features > MCP Server** to set the server's startup, authentication and port options.

![MCP 服务器偏好，显示“启用 MCP 服务器”“自动启动 MCP 服务器”“需要访问令牌”和端口](~/content/assets/images/pref-mcp-server.png)

| 偏好               | 默认值   | 作用                                                                                                                            |
| ---------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------- |
| **启用 MCP 服务器**   | 开     | 取消勾选后，会停止正在运行的服务器，并移除菜单项和状态栏指示器                                                                                               |
| **自动启动 MCP 服务器** | 关     | Starts the server when Tabular Editor starts                                                                                  |
| **需要访问令牌**       | 关     | Agents must present the access token shown in the server dialog. 参见 [在共享计算机上运行](#running-on-a-shared-machine) |
| **端口**           | 42100 | 服务器侦听的回环端口，范围为 1024 到 49151。更改后会使现有的代理注册失效                                                                                    |

## 注册代理

In the server dialog, select your agent from **Export configuration** and paste the copied configuration into your agent. You register each agent once, and the configuration registers the server under the name `tabular-editor`.

![导出配置下拉菜单已展开，其中列出了 Claude Code、VS Code、Copilot CLI、Codex 和 Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

**Claude Code**: run the copied command in a terminal:

```bash
claude mcp add --transport http tabular-editor http://127.0.0.1:42100/
```

**VS Code**: add to your MCP configuration:

```json
{
  "servers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Copilot CLI**: add to `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Codex**: add to `~/.codex/config.toml`:

```toml
[mcp_servers.tabular-editor]
url = "http://127.0.0.1:42100/"
```

**Cursor**: add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

When **Require access token** is on, the exported configuration includes the token in each client's format. Copy the configuration from the dialog; don't write it by hand.

Any other MCP client connects to `http://127.0.0.1:42100/` over streamable HTTP. If **Require access token** is on, send the token in an `Authorization: Bearer <token>` header.

### 检查是否成功

Ask your agent:

> What model am I connected to in Tabular Editor?

The agent answers with the model name, how the model is loaded, whether it has unsaved changes and its compatibility level, or reports that no model is open. No prompt appears in Tabular Editor.

## Set agent permissions

Permissions control which tools an agent gets, and the [AI Assistant](xref:ai-assistant) uses the same permissions. Set them in the **Tools > MCP Server...** dialog or under **Tools > Preferences > AI Features > Permissions**, which both edit the same setting.

![AI 功能权限页面：每个资源各有一个下拉菜单，均处于默认级别](~/content/assets/images/pref-ai-permissions.png)

Hover over a permission's label or dropdown to see what each level allows. If an administrator has capped a resource by [policy](xref:policies), the dropdown is read-only and indicates the policy.

Each resource has an access level:

| 资源                         | 默认值 | 代理获得的内容                                                                                                                                                                                 |
| -------------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **模型元数据**                  | 读取  | 读取：表、列、度量值、表达式、描述、关系，以及 VertiPaq分析器统计信息。写入：能够通过 C# Script 脚本更改模型                                                                                                                        |
| **模型数据**                   | 禁止  | Read: DAX query results (data values from your model). 需要实时连接                                                                        |
| **Best Practice Analyzer** | 读取  | 读取：规则集和分析结果。写入：添加和修改规则                                                                                                                                                                  |
| **文档**                     | 写入  | Read: the contents of your open DAX queries, C# scripts and DAX scripts. Write: modifying them, and creating C# scripts and DAX queries |
| **宏**                      | 写入  | 读取：你的宏库，包括名称、说明和代码。 Write: no additional tools in this version                                                                                                          |

**Write** (labeled **Read/Write** in the dropdowns) includes Read, and **Model data** has no Write level.

**Documents** defaults to Write, which lets an agent create tabs and overwrite the contents of open DAX queries, C# scripts and DAX scripts. The agent doesn't run them, and the model doesn't change. If you keep unsaved work in those tabs, set **Documents** to **Read**.

Raising these grants above their defaults gives the agent more access:

- **Model data > Read** sends values from your model to your agent, and through it to your agent's provider. Grant it when the agent needs to check results against real values.
- **Model metadata > Write** lets the agent change the model through C# scripts. See [How an agent changes your model](#how-an-agent-changes-your-model) for the safeguards.

> [!IMPORTANT]
> Permissions are read when the server starts, and an agent gets its tool list when it connects. 更改授权后，先停止并重新启动服务器，再重新连接代理。 Until then, the agent keeps the permissions that were in force when it connected.

## 代理可以做什么

The agent's tools depend on your grants, and the following table lists what you can ask for and the grant each request needs.

| Request                                                                                                                                               | Grant needed                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Identify the Tabular Editor instance and the model it has open                                                                                        | None                                                |
| Search the Tabular Editor documentation, blog, GitHub issues and discussions                                                                          | None                                                |
| Look up the scripting API: the properties, methods and signatures on the model objects, for the Tabular Editor version you're running | None                                                |
| Get an overview of the tables, their column and measure counts and every relationship                                                                 | **Model metadata > Read**                           |
| Get full detail for named objects, including expressions, descriptions, format strings and data types                                                 | **Model metadata > Read**                           |
| Search the model by name, description, DAX or M expression, format string or annotation                                                               | **Model metadata > Read**                           |
| Get the full model. This uses a lot of tokens, and the tool description warns the agent                                               | **Model metadata > Read**                           |
| See the objects selected in the TOM Explorer                                                                                                          | **Model metadata > Read**                           |
| Get VertiPaq Analyzer statistics: table sizes, column cardinalities and memory use                                                    | **Model metadata > Read**                           |
| List the effective [Best Practice Analyzer](xref:best-practice-analyzer) rules, your own included, and run the analysis                               | **Best Practice Analyzer > Read**                   |
| Add or change rules in your local collection                                                                                                          | **Best Practice Analyzer > Write**                  |
| Run a DAX query and get rows back. A query returns 100 rows by default and at most 500                                                | **Model data > Read** and **Model metadata > Read** |
| List your open DAX queries, C# scripts and DAX scripts                                                                                                | **Model metadata > Read**                           |
| Read the contents of open tabs                                                                                                                        | **Documents > Read**                                |
| Edit a tab, or open a new C# script or DAX query for review                                                                                           | **Documents > Write**                               |
| Read your macro library                                                                                                                               | **Macros > Read**                                   |
| Change the model. See [How an agent changes your model](#how-an-agent-changes-your-model)                                             | **Model metadata > Write**                          |

Select objects in the TOM Explorer before you refer to them in a prompt, for example before asking "format these consistently".

Before a C# script or DAX query from the agent opens as a document, Tabular Editor compiles the script or validates the query against the open model, and returns any errors to the agent. DAX query validation needs Tabular Editor connected to Analysis Services or Power BI.

> [!NOTE]
> Querying data needs a live connection, and VertiPaq statistics need a connection or statistics you've already collected. Tool availability is set when the agent connects, so if you connect the model afterwards, reconnect the agent.

## 代理如何更改你的模型

With **Model metadata > Write**, an agent changes your model by creating a [C# script](xref:csharp-scripts) in the background. Tabular Editor compiles the script, checks it for safety and runs it against the open model.

A script can do anything the C# scripting API supports, for example add measures, columns, calculation groups, perspectives, translations, relationships and refresh policies, or bulk-rename and format objects. An agent-run script has these properties:

- its changes are one undo entry, **C# script (MCP)**, and **Ctrl+Z** undoes the whole script. 见 @undo-redo。
- if the script throws an exception part-way through, all its changes are rolled back.
- the agent receives a list of every object the script added, changed or removed, plus anything the script printed.
- messages from `Output`, `Info`, `Warning` or `Error` are returned to the agent as part of the result, and no dialog opens.
- while a long call runs, a **Please wait** indicator appears and clicks in Tabular Editor are discarded.
- changed objects and properties are marked in the [TOM Explorer and the Properties view](xref:unsaved-changes) until you save. **Show changes** filters both views to the changes, and right-click **Revert** undoes a single property, a single object or a whole branch.

![The Edit menu open on a single Undo C# script (MCP) entry, with the TOM Explorer marking an added measure in green, a changed measure in orange and a deleted measure struck through in red, and the Properties view filtered to the one changed property](~/content/assets/images/features/mcp-server/agent-change-review.png)

The [AI Assistant](xref:ai-assistant) chat runs scripts the same way, with the same single undo step and rollback, under the undo entry **C# script (AI Assistant)**. Agent scripts have no preview dialog and no **Cancel**. Review their changes afterwards in the TOM Explorer and the Properties view.

### Blocked operations

These are blocked regardless of your grants:

- `ExecuteCommand`, which runs raw TMSL or XMLA, always fails in an agent-run script.
- An agent script that accesses the file system, makes a web request or references an external assembly doesn't run. The check is the same analysis of the compiled script that the `BlockUnsafeScripts` policy uses; see [What counts as staying within the model](xref:csharp-scripts#what-counts-as-staying-within-the-model) for the full list. What happens to the script depends on your grants and policies:
  - With **Documents > Write**, the script opens as an **Agent script (review)** document, and the tool result tells the agent to have you review and run it.
  - Without **Documents > Write**, the script doesn't run and no document opens.
  - With the `BlockUnsafeScripts` [policy](xref:policies) set, the script doesn't run and no document opens.
- The DAX helpers inside a script need **Model data > Read**, the same as the query tool.

## Example tasks

### Fix Best Practice Analyzer violations

Open a model and ask:

> 运行 Best Practice Analyzer，告诉我哪些问题值得优先修复，按严重程度从高到低排列。

Follow up with "fix the format string violations". If **Model metadata > Write** is granted, the agent writes one script and runs it, and the changed objects are marked orange in the TOM Explorer. **Show changes** in the [Properties view](xref:unsaved-changes) shows the before and after values per property. Right-click **Revert** on any change you don't want, then save.

### Add measures from a specification

Point the agent at a specification, a ticket or a spreadsheet of measure definitions:

> 把 requirements.md 中的度量值添加到 Sales 表。沿用那里已有的命名和格式字符串。

The agent reads `requirements.md` from its own workspace.

### Verify results with a query

With **Model data > Read** granted, the agent can run DAX to check its work:

> 确认新的 Margin % 度量值在 2025 年得出的总计与旧计算相同。

It writes the DAX query, runs it and compares the results.

### Draft a script without running it

With **Documents > Write**, the agent can put a C# script or DAX query into a document that you review and run yourself, for example to check a change before it runs or to run it against another model later:

> 帮我写一个脚本，把每个度量值重命名为句首大写的 sentence case 格式，但不要运行它。

The script opens as a document in Tabular Editor, compiled and safety-checked. Run it after you've read it.

> [!TIP]
> Review and save between tasks to keep each set of unsaved changes small.

## 同时运行多个实例

Each Tabular Editor instance hosts its own server on its own port. To work on two models at once, open each in its own instance and connect one agent to each.

For a second server, start the second instance, open **Tools > MCP Server...** and click **Start server**. If the configured port is taken, a prompt offers the first free port among the next 20, or an error appears if none is free. You can also set another port under **Tools > Preferences > AI Features > MCP Server**.

Register the second port with your agent under its own name, and name the instance you mean in your prompts.

## 在共享计算机上运行

The server binds to `127.0.0.1`, which other machines can't reach. It also rejects browser requests with a non-local `Origin` header.

When **Require access token** is off, any process on the machine can connect without credentials. On a host where several people are signed in at once, such as a Remote Desktop or Citrix server, that includes processes in other people's sessions.

Select **Require access token** under **Tools > Preferences > AI Features > MCP Server** and restart the server. Agents must then present the token shown in the server dialog, and requests without it are rejected.

Select **Regenerate token** (the refresh button beside the token) to issue a new token, which invalidates existing registrations and restarts a running server. If the token is exposed, regenerate it and re-register your agents. 管理员可以通过 `RequireMcpAccessToken` 策略强制所有人都使用令牌，同时也会锁定该偏好设置。参见 @policies。

## 哪些内容会离开你的计算机

When you use the MCP server, Tabular Editor doesn't contact an AI provider and only answers tool calls from processes on your machine, over a loopback connection. The knowledge base the agent searches is a local database that ships with Tabular Editor and is updated from Tabular Editor's service.

Your agent sends data to its provider under your subscription and that provider's terms, and your agent's settings control what is sent. 当 **Model data** 保持默认值 **Deny** 时，代理将无法从 Tabular Editor 获取任何 DAX 查询结果。在模型定义中输入的值，例如 `DATATABLE` 表达式或 **Enter data** 表，属于模型元数据，代理可通过 **Model metadata > Read** 访问这些内容。

See @security-privacy for the wider picture, including the [AI Assistant](xref:ai-assistant), which calls a provider directly and is configured separately.

## 管理员控制

The MCP server is on by default, and any user can turn it off. Administrators can use these [policies](xref:policies) to control how the MCP operates:

| 策略                                          | Edition | 作用                                                                                                                                                                                                                                     |
| ------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DisableMcpServer`                          | All     | Removes the MCP server. The AI Assistant chat is unaffected                                                                                                                                                            |
| `DisableAi`                                 | All     | Turns off all AI functionality, the MCP server included. With a `REG_DWORD` value of `1`, the installer also leaves the AI component off the machine                                                                   |
| `RequireMcpAccessToken`                     | All     | Forces token authentication and locks the preference                                                                                                                                                                                   |
| `DisableCSharpScripts`                      | All     | Stops an agent running a C# script and drafting one into a document. Drafting a DAX query, and every tool that only reads, is unaffected                                                                               |
| `BlockUnsafeScripts`                        | 企业版     | Allows only scripts that stay within the model, for every script in Tabular Editor. An agent script that accesses files, the network, other processes or external assemblies doesn't run, and no review document opens |
| `Max...` and `McpMax...` permission limits  | 企业版     | Cap each resource. The `Max...` limits apply to the AI Assistant and the MCP server. The `McpMax...` limits apply to the MCP server alone and can only lower the `Max...` limit                        |
| `AiAuditLogPath`, `AiAuditLogRetentionDays` | 企业版     | Set the [audit log](xref:ai-audit-log) location and retention                                                                                                                                                                          |
| `AiProvider` and related values             | 企业版     | Lock the AI Assistant's provider. The MCP server isn't affected                                                                                                                                                        |

> [!WARNING]
> Without an Enterprise license, any Enterprise policy value stops the AI Assistant and the MCP server from starting and removes the menu item and the status bar indicator. A `BlockUnsafeScripts` value also blocks all scripts and macros, so deploy Enterprise policies only to Enterprise-licensed machines (see [What happens without Enterprise Edition](xref:policies#what-happens-without-enterprise-edition)).

On Enterprise Edition, Tabular Editor keeps a local [audit log](xref:ai-audit-log) of AI Assistant and MCP server activity, including every tool an agent called and the full text of any C# script it ran. Prompts, replies and data values aren't recorded. **Open audit folder** in the server dialog and on **Tools > Preferences > AI Features** opens the log folder. On Desktop and Business editions, nothing is logged and neither button appears.

See @policies for the full list, the registry layout and the administrative templates.

## 故障排查

| 你看到的现象                                                                    | 实际情况                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 代理提示它没有可用于 Tabular Editor 的工具                                             | 服务器没有运行，或者代理在服务器启动前就已连接。 Check that the status bar reads **MCP Started**, then reconnect the agent                                                                                                                                                                                                       |
| 智能体看不到你刚授予的权限                                                             | 授权会在服务器启动时读取，工具列表会在连接时确定。停止并重新启动服务器，然后重新连接智能体                                                                                                                                                                                                                                                            |
| The agent loses the connection after a long break                         | The server closes a session after 20 minutes with no requests and no open stream. 重新连接智能体                                                                                                                                                                                                |
| 智能体报告未打开任何模型                                                              | 服务器独立于你的模型运行。 Open a model in Tabular Editor and ask again. You don't need to restart anything                                                                                                                                                                                           |
| 智能体无法运行 DAX 查询                                                            | **模型数据** 默认设置为 **Deny**。 Queries also need a live connection: against a model opened from disk, the query tool is unavailable whatever the grant                                                                                                                                         |
| 连接被 401 拒绝                                                                | **要求访问令牌** 已开启，但智能体没有发送该令牌。 Copy the registration configuration from the dialog again. It includes the token                                                                                                                                                                             |
| 端口已被占用                                                                    | Another Tabular Editor instance or another application uses it. Accept the next free port in the prompt, and update the agent's registration. If **Start MCP server automatically** is on, a conflict at startup shows no prompt and the indicator reads **MCP Stopped** |
| 菜单中没有 **工具 > MCP 服务器...** | **Enable MCP Server** is cleared in preferences, the AI features component isn't installed, an administrator has set `DisableMcpServer` or `DisableAi`, or an Enterprise policy value is set on a machine that isn't licensed for it. 见 @policies                           |

## 后续步骤

- @ai-assistant for the full permission model and the built-in chat.
- 通过 @unsaved-changes 查看并撤销智能体所做的更改。
- @csharp-scripts for what a script, and therefore an agent, can change.
- 如需了解如何在组织范围内对服务器进行治理，请参阅 @policies。
- @te-cli-skill if your agent works on model files in a repository or a pipeline.
