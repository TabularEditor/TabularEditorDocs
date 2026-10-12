---
uid: ai-compliance
title: AI 功能合规指南
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
          partial: true
          note: "仅适用于通用策略。不含权限限制、提供程序锁定或审计日志"
        - edition: Business
          partial: true
          note: "仅适用于通用策略。不含权限限制、提供程序锁定或审计日志"
        - edition: Enterprise
          full: true
---

# AI 功能合规指南

Tabular Editor 3 中的 [AI 助手](xref:ai-assistant) 和 [模型上下文协议 (MCP) 服务器](xref:mcp-server) 让 AI 模型能够在权限授予范围内访问打开的语义模型；管理员可通过组策略限制这些权限，企业版还会将相关活动记录到审计日志中。本页面面向负责批准组织使用这些功能的 IT、安全和合规团队。

## AI 功能

| 功能      | 作用                                                                                                   | 调用 AI 提供程序的主体                               | 网络流量                    |
| ------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------- |
| AI 助手   | Tabular Editor 3 中的聊天面板，可读取、查询并修改当前打开的语义模型                                                           | 由用户计算机上的 Tabular Editor 3 调用，使用用户输入的 API 密钥 | 出站到已配置的提供程序端点           |
| MCP 服务器 | 一个本地服务器，用户已在运行的 AI 代理，例如 Claude Code、GitHub Copilot、Codex 或 Cursor，可连接到该服务器。随后，该代理会读取、查询并修改当前打开的语义模型 | 由该代理按其自身的配置和订阅调用                            | 仅接受来自 `127.0.0.1` 的入站连接 |

这两项功能都随 AI 功能组件一同提供；自 Tabular Editor 3.27.0 起，该组件已包含在默认安装中。它们共用权限授予、管理员策略和审核日志；差异见[权限授予](#permission-grants)一节所述。

Tabular Editor ApS 不运营 AI 服务，也不提供 API 密钥。任一功能中的提示、回复、模型元数据和模型数据都不会经过 Tabular Editor 服务器。启用遥测后，Tabular Editor 3 会将 AI 使用事件发送给 Tabular Editor ApS，其中包括提供方、模型名称、会话 ID 和令牌计数。可通过 `DisableTelemetry` 策略将其关闭。

[Tabular Editor Trust Center](https://trust.tabulareditor.com/) 发布了 AI Assistant 的独立渗透测试 Report、SOC 2 审计 Report 以及子处理者列表。

## 数据流

### AI 助手

AI Assistant 会将请求直接从用户的计算机发送到在 **工具 > 偏好 > AI 功能 > AI Assistant** 中配置的提供方：OpenAI、Anthropic、Azure OpenAI，或任何兼容 OpenAI 的端点，包括托管在你们自有网络中的模型。仅支持通过 API 密钥进行身份验证。参见[支持的提供方](xref:ai-assistant#supported-providers)。

发送给提供方的请求包含：

- 当前生效的系统提示和自定义说明，包括你所在组织发布的任何自定义说明
- 用户的信息和对话历史记录
- 附加到用户信息中的、有关当前打开模型的上下文：数据库名称、对象数量、当前选定内容、活动文档标题、模型错误以及最近的更改。用户的 **模型元数据** 设置并不会阻止发送这些内容；只有将 `MaxModelMetadataAccess` 限制为 `Deny` 才会阻止
- 助手在[权限授予](#permission-grants)授权范围内调用工具所得的结果
- 来自 Tabular Editor 知识库的片段；该知识库是一个基于 Tabular Editor 文档、博客、GitHub 问题和讨论构建的本地数据库

模型元数据涵盖整个模型定义：对象名称、说明和注释、DAX 和 M 表达式、分区源查询、数据源连接详细信息、角色、角色成员以及行级安全性筛选器。直接输入到模型定义中的值，例如 `DATATABLE` 表达式或 **输入数据** 表，也属于元数据的一部分。

来自这些来源的文本会成为请求的一部分，并影响助手的操作。仅将你所在组织“自定义说明”文件夹的写入权限授予负责审核并批准其内容的人员。

你所在组织与提供方签订的协议决定了数据保留期限、数据处理所在区域，以及提供方是否会将请求用于模型训练。若要将处理限制在 Azure 租户或你所在组织管理的网络内，请使用 Azure OpenAI、[Microsoft Foundry](xref:ai-assistant#using-microsoft-foundry) 或[自托管模型](xref:ai-assistant#using-a-local-or-organizational-llm)，并通过[策略](#restrict-the-ai-provider)锁定该配置。

### MCP 服务器

MCP 服务器是一个绑定到 `127.0.0.1` 的 HTTP 侦听器，默认端口为 42100。它不使用 API 密钥，不发起出站请求，并且会拒绝带有非本地 `Origin` 标头的浏览器请求。

已连接的代理会在代理配置及提供程序条款的约束下，将它从 Tabular Editor 3 读取的内容发送到其所使用的提供程序。 Tabular Editor 3 中没有用于设置代理提供程序的选项，因此应通过代理自身的管理控制来管控该代理。代理自身的工具，例如文件访问和 Shell 访问，也同样在 Tabular Editor 3 之外。任何以该用户身份运行的代理都可以读取磁盘上的模型文件、对话文件和审计文件。

**要求访问令牌** 默认处于关闭状态。关闭时，这台计算机上的任何进程都可以在无需凭据的情况下连接到服务器，包括远程桌面或 Citrix 主机上其他用户会话中的进程。 `RequireMcpAccessToken` 策略会对每个用户强制要求使用令牌。代理注册文件会以纯文本存储该令牌，而在 **工具 > MCP 服务器...** 对话框中选择 **重新生成令牌** 会使所有现有注册失效。参见 [在共享计算机上运行](xref:mcp-server#running-on-a-shared-machine)。

### 网络端点

要使用 AI 功能，请在防火墙或代理中放行以下端点：

| 流量       | 端点                                                                                                                                                         |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AI 助手请求  | 已配置的提供程序端点，例如 `https://api.openai.com`、`https://api.anthropic.com`、某个 Azure OpenAI 资源或你自己的 Gateway                                                         |
| AI 模型目录  | `https://api.tabulareditor.com/AiModels`。当用户打开 OpenAI 或 Anthropic 的模型列表时，会发起一次匿名请求以获取模型列表。该列表会缓存 24 小时。 `DisableUpdates` 可将其关闭                             |
| AI 知识库更新 | `https://cdn.tabulareditor.com`。在已配置 AI 助手的情况下，最多每天检查一次，不会发送任何有关用户或模型的数据。除了 `DisableAi` 外，没有任何策略会将其关闭。用户在 **工具 > 偏好 > AI 功能 > AI 助手** 下取消选中 **启动时检查知识库更新** |
| MCP 服务器  | 无                                                                                                                                                          |

许可证验证、更新检查和遥测分别使用独立的请求。参见 [Web 请求](xref:security-privacy#web-requests)。

### 存储在用户计算机上的数据

除非另有说明，所有路径都位于 `%LocalAppData%\TabularEditor3` 下。

| Item       | 地点                                                                                        | 格式                                                                                          |
| ---------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 提供商 API 密钥 | `Preferences.json`                                                                        | 已使用适用于当前用户的 Windows 数据保护 API 加密。在未加载 AI 组件或设置了 `DisableAi` 时会被清除                            |
| MCP 访问令牌   | `Preferences.json`                                                                        | 已使用适用于当前用户的 Windows 数据保护 API 加密                                                             |
| 长期权限授予     | `Preferences.json`                                                                        | JSON                                                                                        |
| 按模型授予的权限   | 模型的[用户选项](xref:user-options)（`.tmuo`）文件：若模型从文件加载，该文件位于模型文件旁；若模型从服务器打开，则位于 `UserOptions` 下 | JSON                                                                                        |
| 对话         | `AI\Conversations`                                                                       | 未加密的 JSON。保存提示、回复和工具结果；当 **模型数据** 设为 **读取** 时，也包括 DAX 查询行。在每次压缩之前都会写入归档副本。文件会一直保留，直到用户删除该对话 |
| 用户自定义指令    | `AI\CustomInstructions`                                                                  | Markdown                                                                                    |
| 知识库        | `kb.sqlite`                                                                               | SQLite 数据库                                                                                  |
| AI 模型目录    | `AiModels.json`                                                                           | JSON                                                                                        |
| 审计日志       | `AI\audit`，或 `AiAuditLogPath` 指定的文件夹                                                     | 参见 [审计日志](#audit-log)                                                                       |

## 权限授予

权限授予决定 AI 助手和 MCP 服务器可以访问哪些内容，每个资源都有一个访问级别。用户可在 **工具 > 偏好 > AI 功能 > 权限** 中设置各级别。在企业版中，管理员可通过策略为每个资源设置权限上限：

| 资源      | AI 功能可访问的内容                                       | 默认值 | 两项功能的限制                  | 仅 MCP 服务器的限制                |
| ------- | ------------------------------------------------- | --- | ------------------------ | --------------------------- |
| 模型元数据   | 读取：模型定义和 VertiPaq分析器的统计信息。编写：通过 C# Script 更改模型    | 读取  | `MaxModelMetadataAccess` | `McpMaxModelMetadataAccess` |
| 模型数据    | 读取：DAX 查询结果，即模型中的数据值                              | 拒绝  | `MaxModelDataAccess`     | `McpMaxModelDataAccess`     |
| 最佳实践分析器 | 读取：规则和分析结果。写入：添加和修改规则                             | 读取  | `MaxBpaAccess`           | `McpMaxBpaAccess`           |
| 文档      | 读取：已打开的 C# Script、DAX 查询和 DAX 脚本文档内容。写入：创建并覆盖这些文档 | 写入  | `MaxDocumentsAccess`     | `McpMaxDocumentsAccess`     |
| 宏       | 读取：用户的宏库，包括宏代码                                    | 写入  | `MaxMacrosAccess`        | `McpMaxMacrosAccess`        |

在默认级别下，AI 功能会读取模型定义、运行 Best Practice Analyzer、读取宏库，并读取和覆盖已打开的脚本与查询文档。它们不会读取数据值，也不会更改模型。宏代码和打开的文档可能包含连接字符串及其他凭据。如果你的组织也需要这样做，请设置 `MaxMacrosAccess` 和 `MaxDocumentsAccess`。

AI Assistant 和 MCP 服务器会按如下方式应用这些授权：

- **AI Assistant。** 当某个请求需要的访问权限超出长期授权的范围时，聊天中会显示一张权限卡片。用户可以选择仅本轮、当前会话或始终允许；对于 **模型元数据** 和 **模型数据**，还可以选择仅对当前模型允许。如果所需访问高于权限上限，则不会显示卡片。
- **MCP 服务器。** 不会出现提示。服务器启动时会读取长期授权，不在授权范围内的工具不会提供给代理。为单个模型或单个会话授予的授权仅适用于当前聊天。

权限上限的优先级高于任何用户授权，包括针对单个模型授予的授权，以及在策略设置之前授予的授权；对应设置只会提供不超过该上限的级别。 `McpMax...` 上限只会降低 MCP 服务器的共享上限。请参阅 [权限和同意](xref:ai-assistant#permissions-and-consent)。

## 模型更改的保护措施

只有当 **模型元数据** 权限为 **写入** 时，AI 功能才会运行会更改模型的脚本。每项更改都会通过 [C# Script 引擎](xref:csharp-scripts) 在 Tabular Editor 3 中已加载的模型上执行：

- 一个脚本产生的所有更改会合并为一条撤销记录，名称为 **C# Script (AI Assistant)** 或 **C# Script (MCP)**。
- 脚本如果在执行中途失败，其更改会被完全回滚。
- 只有当用户开启默认处于关闭状态的 **Allow AI assistant to run C# scripts directly** 时，AI Assistant 才会运行脚本。默认情况下，**预览更改** 是开启的，此时预览对话框会显示每次脚本运行产生的更改，你可以选择接受或取消。这两个设置都是用户偏好，且没有可将其锁定的策略。
- 在聊天中对 AI Assistant 编写的脚本点击 **Execute** 后，它会作为你自己的脚本运行，且不受 **模型元数据** 级别限制。安全检查仍然适用；但对 `ReadFile` 和下文 DAX 辅助方法的限制不适用。
- MCP 代理的脚本运行时不会显示预览对话框。之后，你可以在 **TOM Explorer** 和 **属性** 视图中查看这些更改；两者都会标出每一项未保存的更改。
- 在你保存之前，更改会一直以未保存状态保留在已加载的模型中。没有任何 AI 工具会保存或部署模型。用户点击助手回复中的链接后，这些链接可以触发 Tabular Editor 命令，包括 **Save** 和 **Deploy**。如果用户通过与 Analysis Services 或 Power BI Workspace 的实时连接打开模型，保存会将更改写入该服务器。
- 使用文件系统、网络或外部程序集的脚本不会运行。 AI 助手会为其显示 **Unsafe** 徽章，并禁用 **Execute**。对于 MCP 代理，它会以审阅文档的形式打开；如果 **Documents** 权限低于 **Write**，则会被拒绝。
- 安全检查会分析已编译的脚本。反射、表达式树、`Activator`、`AppDomain`、XML 读取器和反序列化都被视为不安全。
- 在由 AI 助手或 MCP 代理运行的脚本中，`ReadFile`、`SaveFile`、`Bpa.ExportCsv`、`ExecuteCommand`、运行宏的调用以及 Semantic Bridge 调用始终会失败。 `ExecuteCommand` 会将 Tabular Model Scripting Language (TMSL) 和 XML for Analysis (XMLA) 命令发送到服务器。
- 在这些脚本中，DAX 辅助方法与 DAX 查询工具一样，要求 **模型数据** 权限至少为 **读取**。

`BlockUnsafeScripts` 策略会对每个脚本和宏应用相同的安全检查：无论它来自用户、Best Practice Analyzer、AI 助手、MCP 服务器还是 Tabular Editor CLI。 `DisableCSharpScripts` 会禁用 C# Script 文档，并从 AI 助手中移除用于运行脚本的工具，同时从 MCP 服务器中移除两个脚本工具。除非同时设置 `DisableMacros`，否则宏仍会继续运行。参见 [代理如何更改你的模型](xref:mcp-server#how-an-agent-changes-your-model)。

## 管理员控制

管理员可以通过 Windows 组策略、Tabular Editor 3 附带的管理模板，或直接写入注册表值来强制执行这些控制项。有关注册表项、值类型和模板设置，参见 @policies。

`HKEY_LOCAL_MACHINE` 下的策略优先于 `HKEY_CURRENT_USER` 下的相同值。标准用户无法更改这两个 `Software\Policies` 键中的任何一个。 Tabular Editor 3 会在启动时读取策略，MCP 服务器会在启动时读取权限授权，因此，策略更改要等到用户重启 Tabular Editor 3 后才会对当前会话生效。

企业版策略适用于企业版、咨询版和试用版许可证。在桌面版和商业版中，管理员可以关闭 AI 功能、强制使用 MCP 访问令牌、关闭 C# Script 和宏，以及关闭遥测。在下表中，**全部** 表示 Tabular Editor 3 的所有版本。

### 关闭 AI 功能

| 要求                    | 策略                 | 版本 |
| --------------------- | ------------------ | -- |
| 不含 AI 功能，且未安装 AI 组件   | `DisableAi`        | 全部 |
| 禁用 AI 助手，允许使用 MCP 服务器 | `DisableAiChat`    | 全部 |
| 禁用 MCP 服务器，允许使用 AI 助手 | `DisableMcpServer` | 全部 |

`DisableAi` 还会清除所有已保存的提供商配置，包括 API 密钥。请参阅 [在不使用 AI 功能的情况下进行部署](xref:installation-activation-basic#deploying-without-the-ai-features)。

Tabular Editor 3 的便携版无需安装。它在运行时会遵循 `DisableAi` 设置。如果用户不得运行旧版本，请使用应用程序控制，例如 AppLocker 或 Windows Defender Application Control。

### 限制 AI 功能可访问的范围

| 要求                           | 策略                                                                                                                     | 版本  |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------- | --- |
| 为两项功能统一按资源设置限制               | `MaxModelMetadataAccess`, `MaxModelDataAccess`, `MaxBpaAccess`, `MaxDocumentsAccess`, `MaxMacrosAccess`                | 企业版 |
| 为 MCP 代理按资源设置更低的限制           | `McpMaxModelMetadataAccess`, `McpMaxModelDataAccess`, `McpMaxBpaAccess`, `McpMaxDocumentsAccess`, `McpMaxMacrosAccess` | 企业版 |
| 不向 MCP 代理开放个别工具              | `McpDisabledTools`                                                                                                     | 企业版 |
| 不允许使用 C# Script 文档、AI 脚本工具或宏 | `DisableCSharpScripts` 和 `DisableMacros`                                                                               | 全部  |
| 仅允许通过安全检查的 C# Script         | `BlockUnsafeScripts`                                                                                                   | 企业版 |

从审计日志中的 `tool_call` 记录获取 `McpDisabledTools` 的工具名称。

### 限制 AI 提供程序

| 要求                        | 策略                                | 版本  |
| ------------------------- | --------------------------------- | --- |
| 一个经批准的提供程序                | `AiProvider`                      | 企业版 |
| 一个经批准的端点或 Gateway         | `AiEndpoint`                      | 企业版 |
| 一个经批准的模型或 Azure OpenAI 部署 | `AiModel`                         | 企业版 |
| 向经批准的 OpenAI 组织或项目计费      | `AiOrganizationId`, `AiProjectId` | 企业版 |
| 经批准的提供程序列表                | `AiAllowedProviders`              | 企业版 |
| 经批准的端点主机列表                | `AiAllowedEndpointHosts`          | 企业版 |

`AiProvider`、`AiEndpoint`、`AiModel`、`AiOrganizationId` 和 `AiProjectId` 会替换用户的设置，而将 `AiProvider` 设置为 `None` 会关闭 AI 助手。如果配置不满足 `AiAllowedProviders` 或 `AiAllowedEndpointHosts`，AI 助手不会发送请求，并且错误消息会指出相关的提供程序或端点主机。 `AiAllowedEndpointHosts` 只检查用户输入的端点，因此 OpenAI 和 Anthropic 若未使用自定义端点，无论列表中写了什么，都会访问其公共 API。将其与 `AiProvider` 或 `AiAllowedProviders` 搭配使用。没有任何策略会强制使用 HTTPS；请将 `AiEndpoint` 锁定为 `https://` 地址。策略不会分发 API 密钥。如果将端点锁定为贵组织拥有的资源(例如 Azure OpenAI 资源或内部 Gateway)，则只有贵组织签发的密钥才可使用。如果使用 `api.openai.com` 这样的公共端点，用户可以输入个人密钥。这些策略仅适用于 AI 助手。

### 自定义指令和 MCP 端口

| 要求                 | 策略                              | 版本  |
| ------------------ | ------------------------------- | --- |
| 为每位用户提供组织批准的自定义指令  | `AiCustomInstructionsPath`      | 企业版 |
| 忽略用户自行编写的自定义指令     | `DisableUserCustomInstructions` | 企业版 |
| MCP 代理使用访问令牌进行身份验证 | `RequireMcpAccessToken`         | 全部  |
| 固定的 MCP 服务器端口      | `McpPort`                       | 企业版 |

### 其他版本的 Enterprise 策略

如果在许可证非 Enterprise 的计算机上设置了任何 Enterprise 策略值，AI 助手和 MCP 服务器都不会启动；而 `BlockUnsafeScripts` 值会阻止所有脚本和宏运行。如果某个值无法被 Tabular Editor 3 解析，它会在权限限制中拒绝该资源，使 `AiProvider` 下的 AI 助手不可用，并强制启用 `BlockUnsafeScripts`。任何其他无效值都会被忽略，其所控制的设置将保持不受限制。仅向拥有对应许可证的计算机部署 Enterprise 策略。请参阅[未使用企业版时会发生什么](xref:policies#what-happens-without-enterprise-edition)。

要查看某台计算机上适用哪些策略，请打开 **工具 > 偏好 > Tabular Editor > 更新和反馈**。**由组织管理** 部分会列出找到的每个策略值、其源键，以及所有标记为 **（无效）** 的值。

## 审计日志

在企业版中，Tabular Editor 3 会在本地记录 AI 助手和 MCP 服务器的活动，并每天写入一个 JSON Lines 文件。每条记录都包含 UTC 时间戳、功能（`chat` 或 `mcp`）、对应的会话和当前打开模型的名称，以及 Windows 用户名。在许可证激活之前，不会记录任何内容。

日志会记录以下内容：

- 权限请求及用户的响应
- 每次工具调用，包括工具名称、所需权限、结果（`ok`、`error`、`denied` 或 `cancelled`）、持续时间，以及其参数的名称和总大小
- 每个提交运行的 C# Script（包括运行时失败、被拒绝或退回供审查的脚本）都会连同其 SHA-256 哈希一起保存为 `.csx` 文件
- 每轮聊天的提供方、模型、端点主机以及 token 数量
- AI 配置更改
- MCP 服务器的启动和停止，以及每个资源的权限级别
- MCP 代理连接，以及客户端上报的名称和版本

不会记录提示词文本、回复文本、参数值、来自模型的数据值、API 密钥和访问令牌。编译失败的脚本，以及 AI 功能写入文档供用户运行的脚本，都不会保存。

除非 `AiAuditLogRetentionDays` 设置了其他保留期，否则超过 30 天的文件会被删除；设置为 `0` 则保留所有文件。每个 Tabular Editor 3 实例都会在会话中写入第一条记录前，从其写入的文件夹中删除已过期的文件。

日志由用户自己的 Tabular Editor 3 进程写入，因此用户对其具有写入和删除权限，即使日志被重定向到共享位置也是如此。如果日志无法写入，例如因为共享不可访问，AI 助手和 MCP 服务器会继续运行，并且该故障只会在 Tabular Editor 的应用程序日志中记录一次。

`AiAuditLogPath` 用于重定向日志。相对路径会被忽略。每日文件名和脚本文件名都不包含用户名或计算机名，因此要为每个用户提供单独的文件夹。诸如 `%USERNAME%` 之类的环境变量只会在 `REG_EXPAND_SZ` 值中展开；管理模板写入的是 `REG_SZ`，因此会按原样使用。

记录格式请参见 @ai-audit-log。

## 推荐基线

以下基线为允许 AI 辅助模型开发、同时不让模型数据流向 AI 提供方的组织提供指导。请根据自身风险评估进行调整。

| 控制项      | 设置                                                                                     | 效果                               |
| -------- | -------------------------------------------------------------------------------------- | -------------------------------- |
| Provider | 将 `AiProvider`、`AiEndpoint`、`AiModel` 和 `AiAllowedEndpointHosts` 设置为你组织拥有且已签订数据处理协议的资源 | AI 助手仅向该端点发送请求，并使用由你组织签发的密钥      |
| 模型数据     | 将 `MaxModelDataAccess` 设置为 `Deny`                                                      | 任何 DAX 查询结果都不会发送到 AI 助手或 MCP 代理  |
| 宏        | 将 `MaxMacrosAccess` 设置为 `Deny`                                                         | 宏代码不会发送给 AI 提供方                  |
| 脚本       | 将 `BlockUnsafeScripts` 设置为 `1`                                                         | 任何脚本或宏都不能写入文件、访问网络、启动其他程序或加载外部代码 |
| MCP 身份验证 | 将 `RequireMcpAccessToken` 设置为 `1`                                                      | 只有持有用户访问令牌的客户端才能连接到 MCP 服务器      |
| 审计保留期    | 将 `AiAuditLogRetentionDays` 设置为满足你保留要求的期限                                              | 审计文件会在该期限内保留                     |
| 审计存储位置   | 为每位用户将 `AiAuditLogPath` 设置为共享位置上的某个文件夹                                                 | 审计文件会集中收集                        |

以下注册表文件会应用基线中适用于整台计算机的部分。它会将 AI Assistant 锁定到一个 Azure OpenAI 资源，并将审计文件保留 365 天。将终结点和部署名称替换为你自己的，并且仅将该文件应用于已获得企业版许可的计算机：

```ini
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS]
"BlockUnsafeScripts"=dword:00000001

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS\TE3]
"AiProvider"="AzureOpenAI"
"AiEndpoint"="https://contoso-ai.openai.azure.com"
"AiModel"="tabular-editor-assistant"
"AiAllowedEndpointHosts"="contoso-ai.openai.azure.com"
"MaxModelDataAccess"="Deny"
"MaxMacrosAccess"="Deny"
"RequireMcpAccessToken"=dword:00000001
"AiAuditLogRetentionDays"=dword:0000016d
```

`BlockUnsafeScripts` 位于共享注册表项中，因此 Tabular Editor CLI 也会强制执行它。将 `AiAuditLogPath` 设置为每个用户对应的一个文件夹：可以是在 `HKEY_LOCAL_MACHINE` 项下设置 `REG_EXPAND_SZ` 值，例如 `\\fileserver\te-audit$\%USERNAME%`，也可以是在 `HKEY_CURRENT_USER\SOFTWARE\Policies\Tabular Editor ApS\TE3` 下为每个用户设置 `REG_SZ` 值。

## 常见问题

### Tabular Editor ApS 会接收我们的提示词、元数据或数据吗？

不能。参见 [数据流](#data-flow)。

### 我们的数据会被用于训练 AI 模型吗？

Tabular Editor ApS 不会接收任何提示词、回复或模型内容。你与 AI 提供程序签订的协议决定该提供程序是否会使用请求来训练模型。

### 我们的数据在哪里处理？

数据会在 AI Assistant 配置的终结点处理，也可能在 MCP 代理提供程序运行的任何位置处理。参见 [限制 AI 提供程序](#restrict-the-ai-provider)。

### 用户能绕过策略吗？

没有本地管理员权限，用户无法更改策略。 3.27.0 之前的版本（包括较旧的便携版构建）只会读取 `HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor`，并忽略此页面上的所有策略。参见 [关闭 AI 功能](#turn-the-ai-features-off)。

### AI 功能能更改或部署生产模型吗？

只有在 **Model metadata** 设为 **Write** 时，它们才会在已加载的模型上运行脚本；并且只有用户才能进行保存或部署。参见 [模型更改的保护措施](#safeguards-on-model-changes)。

### AI 功能能从我们的模型中读取数据吗？

DAX 查询结果需要 **模型数据** 权限为 **读取**，默认是 **拒绝**。在模型定义中键入的值属于元数据的一部分。见 [数据流](#data-flow)。

### MCP 代理是否可以使用我们尚未批准的提供程序？

是的。可以通过代理自身的管理设置来控制它，或者设置 `DisableMcpServer`。见 [MCP 服务器](#mcp-server)。

### 发生事件时，如何停用 AI 功能？

设置 `DisableAi`，并让用户重启 Tabular Editor 3。在提供程序端撤销受影响的 API 密钥。见 [关闭 AI 功能](#turn-the-ai-features-off)。

### 审核日志是否可检测篡改？

不能。用户可以修改或删除自己的审核文件。见 [审核日志](#audit-log)。

## 另请参阅

- @ai-assistant
- @mcp-server
- @ai-audit-log
- @policies
- @security-privacy
- @editions
