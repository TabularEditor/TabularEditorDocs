---
uid: ai-compliance
title: AI 功能合规指南
author: Morten Lønskov
updated: 2026-10-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Business
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Enterprise
          full: true
---

# AI 功能合规指南

Tabular Editor 3 中的[AI 助手](xref:ai-assistant)和[模型上下文协议 (MCP) 服务器](xref:mcp-server)使 AI 模型能够访问开放语义模型，访问权限受管理员通过组策略限制，且企业版会在审计日志中记录相关信息。本页面面向为组织批准这些功能的 IT、安全和合规团队。

## AI 功能

| 功能 | 功能作用 | 调用 AI 提供商的实体 | 网络流量 |
| -- | -- | -- | -- |
| AI 助手 | Tabular Editor 3 中的聊天面板，用于读取、查询和更改打开的语义模型 | Tabular Editor 3，从用户计算机发出，使用用户输入的 API 密钥 | 出站至配置的提供商端点 |
| MCP 服务器 | 用户已运行的 AI 代理（例如 Claude Code、GitHub Copilot、Codex 或 Cursor）连接到的本地服务器。然后，代理读取、查询和更改打开的语义模型 | 代理，根据其自身的配置和订阅 | 仅入站到 `127.0.0.1` |

这两个功能均包含在 AI 功能组件中，该组件是 Tabular Editor 3.27.0 默认安装的一部分。它们共享权限授予、管理员策略和审计日志，差异详见[权限授予](#permission-grants)。

Tabular Editor ApS 不运营 AI 服务，也不提供 API 密钥。来自任一功能的提示、回复、模型元数据和模型数据绝不会经过 Tabular Editor 服务器。在启用遥测的情况下，Tabular Editor 3 会将 AI 使用事件连同提供商、模型名称、会话 ID 和令牌计数一起发送给 Tabular Editor ApS。对于 MCP 服务器，事件包含工具名称、每次工具调用的结果和持续时间，以及 MCP 客户端的名称和版本（如果是已知客户端）。工具参数、工具结果和错误消息不会被发送。`DisableTelemetry` 策略会将其关闭。

[Tabular Editor 信任中心](https://trust.tabulareditor.com/)发布 AI 助手的独立渗透测试报告、SOC 2 审计报告以及分包处理商列表。

## 数据流

### AI 助手

AI 助手将请求直接从用户的计算机发送到在**工具 > 首选项 > AI 功能 > AI 助手**下配置的提供商：OpenAI、Anthropic、Azure OpenAI 或任何与 OpenAI 兼容的端点，包括托管在您自己网络上的模型。身份验证仅通过 API 密钥进行。请参阅[支持的提供商](xref:ai-assistant#supported-providers)。

向提供商发出的请求包含：

- 系统提示和当前有效的自定义指令，包括您的组织发布的任何指令
- 用户的消息和对话历史记录
- 添加到用户消息中的有关开放模型的上下文：数据库名称、对象计数、当前选择、活动文档的标题、模型错误和最近的更改。用户的**模型元数据**设置不会阻止它；`MaxModelMetadataAccess`限制为`Deny`时会阻止它
- 助手调用的工具的结果，在[权限授予](#permission-grants)范围内
- 来自 Tabular Editor 知识库的段落，该知识库是一个由 Tabular Editor 文档、博客、GitHub 问题和讨论构建的本地数据库

模型元数据涵盖整个模型定义：对象名称、描述和注释、DAX 和 M 表达式、分区源查询、数据源连接详细信息、角色、角色成员和行级安全筛选器。在模型定义中输入的值（例如 `DATATABLE` 表达式或**输入数据**表）是元数据的一部分。

来自这些来源的文本将成为请求的一部分，并影响助手的操作。将对组织自定义指令文件夹的写入访问权限限制为仅限批准其内容的人员。

贵组织与提供商的协议规定了保留期限、数据处理所在区域以及提供商是否使用请求进行模型训练。要将处理保留在 Azure 租户或贵组织管理的网络中，请使用 Azure OpenAI、[Microsoft Foundry](xref:ai-assistant#using-microsoft-foundry) 或[自托管模型](xref:ai-assistant#using-a-local-or-organizational-llm)，并通过[策略](#restrict-the-ai-provider)锁定配置。

### MCP 服务器

MCP 服务器是一个 HTTP 侦听器，默认情况下绑定到 `127.0.0.1` 的 42100 端口。它没有 API 密钥，不发出出站请求，并拒绝带有非本地“Origin”标头的浏览器请求。

已连接的代理根据代理的配置和提供商的条款，将其从 Tabular Editor 3 读取的内容发送给自己的提供商。Tabular Editor 3 没有针对代理提供商的设置，因此请通过代理自身的管理控制来管理代理。代理自身的工具（例如文件和 shell 访问）也位于 Tabular Editor 3 之外。**模型源详细信息**首选项设置代理随模型名称一起接收的模型文件路径或服务器的多少，并且不会更改模型元数据中的连接详细信息。请参阅[检查是否成功](xref:mcp-server#check-that-it-worked)。以用户身份运行的任何代理都可以读取磁盘上的模型文件、会话文件和审计文件。

**需要访问令牌**默认关闭。在禁用此选项时，计算机上的任何进程都可以无需凭据连接到服务器，包括远程桌面或 Citrix 主机上其他用户会话中的进程。`RequireMcpAccessToken` 策略对每位用户强制使用令牌。代理注册文件以纯文本形式存储令牌，**“工具”>“MCP 服务器…”**对话框中的**“重新生成令牌”**将使所有现有注册失效。请参阅[在共享计算机上运行](xref:mcp-server#running-on-a-shared-machine)。

### 网络端点

通过您的防火墙或代理允许这些端点使用 AI 功能：

| 流量 | 终结点 |
| -- | -- |
| AI 助手请求 | 已配置的提供商终结点，例如 `https://api.openai.com`、`https://api.anthropic.com`、Azure OpenAI 资源或您自己的网关 |
| AI 模型目录 | `https://api.tabulareditor.com/AiModels`。当用户打开 OpenAI 或 Anthropic 的模型列表时，发出的模型列表匿名请求。该列表缓存 24 小时。`DisableUpdates` 会将其关闭 |
| AI 知识库更新 | `https://cdn.tabulareditor.com`。在配置 AI 助手时，最多每天检查一次，不包含有关用户或模型的数据。除 `DisableAi` 外，没有策略会将其禁用。用户在**工具 > 首选项 > AI 功能 > AI 助手**下取消选中**启动时检查知识库更新** |
| MCP 服务器 | 无 |

许可证验证、更新检查和遥测使用单独的请求。请参阅[Web 请求](xref:security-privacy#web-requests)。

### 存储在用户计算机上的数据

除非另有说明，否则所有路径均位于 `%LocalAppData%\TabularEditor3` 下。

| 项目 | 位置 | 格式 |
| -- | -- | -- |
| 提供商 API 密钥 | `Preferences.json` | 使用当前用户的 Windows 数据保护 API 进行加密。当 AI 组件未加载或已设置 `DisableAi` 时清除 |
| MCP 访问令牌 | `Preferences.json` | 使用当前用户的 Windows 数据保护 API 加密 |
| 永久权限授予 | `Preferences.json` | JSON |
| 按模型授予的权限 | 模型的[用户选项](xref:user-options) (`.tmuo`) 文件：位于从文件加载的模型旁边，或位于从服务器打开的模型的 `UserOptions` 下 | JSON |
| 对话 | `AI\Conversations` | 未加密的 JSON。包含提示、回复和工具结果，包括当**模型数据**处于**读取**状态时的 DAX 查询行和 Analysis Services 错误文本。每次压缩之前都会写入存档副本。文件将保留至用户删除对话时 |
| 用户自定义指令 | `AI\CustomInstructions` | Markdown |
| 知识库 | `kb.sqlite` | SQLite 数据库 |
| AI 模型目录 | `AiModels.json` | JSON |
| 审计日志 | `AI\audit`，或由 `AiAuditLogPath` 设置的文件夹 | 请参阅[审计日志](#audit-log) |

## 权限授予

权限授予用于控制 AI 助手和 MCP 服务器的访问范围，每个资源对应一个访问级别。用户在**工具 > 首选项 > AI 功能 > 权限**下设置每个级别。在企业版中，管理员可以通过策略为每个资源设置权限限制：

| 资源 | AI 功能的访问范围 | 默认 | 两项功能的限制 | 仅限 MCP 服务器的限制 |
| -- | -- | -- | -- | -- |
| 模型元数据 | 读取：模型定义、VertiPaq分析器统计数据以及模型的错误和警告。服务器错误文本也需要**模型数据 > 读取**。写入：通过 C# 脚本更改模型 | 读取 | `MaxModelMetadataAccess` | `McpMaxModelMetadataAccess` |
| 模型数据 | 读取：DAX 查询结果和 Analysis Services 返回的错误文本，其中可能包含来自模型的数据值 | 拒绝 | `MaxModelDataAccess` | `McpMaxModelDataAccess` |
| Best Practice Analyzer | 读取：规则和分析结果。写入：添加和更改规则 | 读取 | `MaxBpaAccess` | `McpMaxBpaAccess` |
| 文档 | 读取：打开的 C# 脚本、DAX 查询和 DAX 脚本文档的内容，以及打开的文档（包括数据透视网格）的错误和警告。写入：创建和覆盖它们 | 写入 | `MaxDocumentsAccess` | `McpMaxDocumentsAccess` |
| 宏 | 读取：用户的宏库，包括宏代码 | 写入 | `MaxMacrosAccess` | `McpMaxMacrosAccess` |

在默认级别，AI 功能会读取模型定义、运行 Best Practice Analyzer、读取宏库以及读取并覆盖打开的脚本和查询文档。它们不会读取数据值，也不会更改模型。宏代码和已打开的文档可能包含连接字符串和其他凭据。如果您的组织中包含连接字符串和其他凭据，请设置 `MaxMacrosAccess` 和 `MaxDocumentsAccess`。

AI 助手和 MCP 服务器按以下方式应用授权：

- **AI 助手。**当请求需要访问权限而常设授权未涵盖时，聊天中会显示权限卡。用户可以针对此轮、此会话或始终允许访问，对于**模型元数据**和**模型数据**，还可以针对当前模型允许访问。对于超过权限限制的访问，不会显示卡片。
- **MCP 服务器。**不会出现提示。服务器在启动时会读取常设授权，并且不会向代理提供授权未涵盖的工具。针对一个模型或一个会话授予的权限仅适用于聊天。

权限限制的优先级高于每个用户授权，包括针对一个模型授予的授权以及在设置策略之前授予的授权，且匹配的设置仅提供不超过该限制的级别。`McpMax...` 限制只会降低 MCP 服务器的共享限制。请参阅[权限和同意](xref:ai-assistant#permissions-and-consent)。

## 模型更改的保障措施

只有当**模型元数据**处于**写入**状态时，AI 功能才会运行更改模型的脚本。每次更改都会通过 [C# 脚本引擎](xref:csharp-scripts)针对 Tabular Editor 3 中加载的模型运行：

- 脚本的更改形成一个撤消条目，名为**C# 脚本（AI 助手）**或**C# 脚本（MCP）**。
- 执行过程中部分失败的脚本将完全回滚。
- 仅当用户启用**允许 AI 助手直接运行 C# 脚本**时，AI 助手才会运行脚本，该选项默认关闭。在默认情况下，如果启用**预览更改**，则预览对话框会显示每次运行脚本所产生的更改，用户可以选择接受或取消这些更改。这两个设置都是用户偏好，没有锁定它们的策略。
- 对 AI 助手在聊天中编写的脚本执行**执行**操作，会在任何**模型元数据**级别将其作为用户自己的脚本运行。安全检查适用；对 `ReadFile` 和以下 DAX 帮助程序方法的限制不适用。
- MCP 代理的脚本在没有预览对话框的情况下运行。用户随后在**TOM Explorer**和**属性**视图中查看更改，这两个视图会标记所有未保存的更改。
- 在用户保存之前，更改将一直未保存地保留在已加载的模型中。没有 AI 工具会保存或部署模型。当用户选择助手回复中的链接时，这些链接可以启动 Tabular Editor 命令，包括**保存**和**部署**。如果用户通过与 Analysis Services 或 Power BI 工作区的实时连接打开模型，则保存操作会将更改写入该服务器。
- 不会运行使用文件系统、网络或外部程序集的脚本。AI 助手会以带有“**不安全**”徽章且“**执行**”被禁用的方式显示该脚本。对于 MCP 代理，它将作为审核文档打开，或者当**文档**位于**写入**下方时被拒绝。
- 安全检查会分析已编译的脚本。反射、表达式树、`Activator`、`AppDomain`、XML 读取器和反序列化均被视为不安全。
- 在 AI 助手或 MCP 代理运行的脚本中，`ReadFile`、`SaveFile`、`Bpa.ExportCsv`、`ExecuteCommand`、运行宏的调用以及 Semantic Bridge 调用始终失败。`ExecuteCommand` 将表格模型脚本语言 (TMSL) 和 XML for Analysis (XMLA) 命令发送到服务器。
- 在相同的脚本中，DAX 帮助程序方法需要**读取**时的**模型数据**，就像 DAX 查询工具一样。

`BlockUnsafeScripts` 策略对每个脚本和宏应用相同的安全检查：来自用户、Best Practice Analyzer、AI 助手、MCP 服务器或 Tabular Editor CLI。`DisableCSharpScripts` 会禁用 C# 脚本文档，并从 AI 助手移除运行脚本的工具，以及从 MCP 服务器移除两个脚本工具。除非也设置了 `DisableMacros`，否则宏将继续运行。请参阅[代理如何更改您的模型](xref:mcp-server#how-an-agent-changes-your-model)。

## 管理员控制

管理员通过 Windows 组策略、使用 Tabular Editor 3 随附的管理模板或直接写入注册表值来实施控制。请参阅 @policies，了解注册表项、值类型和模板设置。

`HKEY_LOCAL_MACHINE`下的策略优先于`HKEY_CURRENT_USER`下的同一值。标准用户无法更改任何一个 `Software\Policies` 键。Tabular Editor 3 在启动时读取策略，MCP 服务器在启动时读取权限授予，因此，用户在重新启动 Tabular Editor 3 后，策略更改才会应用于正在运行的会话。

企业版策略适用于企业版、咨询版和试用版许可证。在 Desktop 和 Business 版本中，管理员可以禁用 AI 功能、强制使用 MCP 访问令牌、禁用 C# 脚本和宏以及禁用遥测。在下表中，**所有**表示 Tabular Editor 3 的每个版本。

### 关闭 AI 功能

| 要求 | 策略 | 版本 |
| -- | -- | -- |
| 无 AI 功能，且新安装中不包含 AI 组件，升级时会移除 AI 组件 | `DisableAi` | 所有 |
| 无 AI 助手，允许 MCP 服务器 | `DisableAiChat` | 所有 |
| 无 MCP 服务器，允许使用 AI 助手 | `DisableMcpServer` | 所有 |

`DisableAi` 还会清除所有已存储的提供商配置，包括 API 密钥。对于设置策略后安装程序未在其上运行过的安装，AI 文件将保留在磁盘上，而 Tabular Editor 3 不会加载这些文件。请参阅[使用 DisableAi 策略强制执行决定](xref:installation-activation-basic#enforcing-the-decision-with-the-disableai-policy)。

Tabular Editor 3 的便携式版本没有安装程序步骤。它在运行时遵循 `DisableAi`。如果用户不得运行旧版本，请使用应用程序控制，例如 AppLocker 或 Windows Defender 应用程序控制。

### 限制 AI 功能的访问范围

| 要求 | 策略 | 版本 |
| -- | -- | -- |
| 两项功能每种资源的限制 | `MaxModelMetadataAccess`、`MaxModelDataAccess`、`MaxBpaAccess`、`MaxDocumentsAccess`、`MaxMacrosAccess` | 企业版 |
| MCP 代理的每个资源的下限 | `McpMaxModelMetadataAccess`、`McpMaxModelDataAccess`、`McpMaxBpaAccess`、`McpMaxDocumentsAccess`、`McpMaxMacrosAccess` | 企业版 |
| 不向 MCP 代理提供个别工具 | `McpDisabledTools` | 企业版 |
| 无 C# 脚本文档、AI 脚本工具或宏 | `DisableCSharpScripts` 和 `DisableMacros` | 所有 |
| 仅限通过安全检查的 C# 脚本 | `BlockUnsafeScripts` | Enterprise |

从审计日志中的`tool_call`记录中获取`McpDisabledTools`的工具名称。

### 限制 AI 提供程序

| 要求 | 策略 | 版本 |
| -- | -- | -- |
| 一个已批准的提供商 | `AiProvider` | Enterprise |
| 一个已批准的端点或网关 | `AiEndpoint` | 企业版 |
| 一个已批准的模型或 Azure OpenAI 部署 | `AiModel` | 企业版 |
| 向已批准的 OpenAI 组织或项目收费 | `AiOrganizationId`、`AiProjectId` | 企业版 |
| 已批准的提供商列表 | `AiAllowedProviders` | 企业版 |
| 已批准的端点主机列表 | `AiAllowedEndpointHosts` | 企业版 |

`AiProvider`、`AiEndpoint`、`AiModel`、`AiOrganizationId` 和 `AiProjectId` 替换用户的设置，将 `AiProvider` 设置为 `None` 会关闭 AI 助手。如果配置违反了 `AiAllowedProviders` 或 `AiAllowedEndpointHosts`，AI 助手不会发送请求，并且会显示一个错误，指出提供程序或端点主机的名称。`AiAllowedEndpointHosts` 仅检查用户输入的端点，因此，如果没有自定义端点，无论列表中包含什么，OpenAI 和 Anthropic 都会访问其公共 API。将其与`AiProvider`或`AiAllowedProviders`配对。没有政策要求使用 HTTPS；将 `AiEndpoint` 锁定到 `https://` 地址。策略不会分发 API 密钥。如果终结点锁定到贵组织拥有的资源（例如 Azure OpenAI 资源或内部网关），则只有贵组织颁发的密钥才能使用。使用 `api.openai.com` 等公共端点时，用户可以输入个人密钥。这些策略仅适用于 AI 助手。

### 自定义指令和 MCP 端口

| 要求 | 策略 | 版本 |
| -- | -- | -- |
| 经组织批准的适用于每个用户的自定义指令 | `AiCustomInstructionsPath` | Enterprise |
| 忽略用户自行撰写的自定义指令 | `DisableUserCustomInstructions` | Enterprise |
| MCP 代理使用访问令牌进行身份验证 | `RequireMcpAccessToken` | 所有 |
| 固定 MCP 服务器端口 | `McpPort` | Enterprise |

### 其他版本的企业策略

如果许可证不是 Enterprise 的电脑上存在任何 Enterprise 策略值，则 AI 助手和 MCP 服务器不会启动，并且 `BlockUnsafeScripts` 值会阻止所有脚本和宏运行。如果存在 Tabular Editor 3 无法解释的值，则会因权限限制而拒绝资源，导致 AI 助手无法用于 `AiProvider` 并强制执行 `BlockUnsafeScripts`。任何其他无效值都将被忽略，其所控制的设置仍不受限制。仅对具有匹配许可证的计算机推出企业版策略。请参阅[没有企业版会发生什么](xref:policies#what-happens-without-enterprise-edition)。

要查看哪些策略适用于某台计算机，请打开**工具 > 首选项 > Tabular Editor > 更新和反馈**。“由您的组织管理”部分列出了找到的每个策略值、其源键以及所有标记为“（无效）”的值。

## 审计日志

在企业版中，Tabular Editor 3 每天将 AI 助手和 MCP 服务器活动的本地记录写入一个 JSON Lines 文件。每条记录都包含 UTC 时间戳、功能（`chat` 或 `mcp`）、会话和适用时的打开模型名称，以及 Windows 用户名。在激活许可证之前，不会记录任何内容。

日志记录：

- 权限请求和用户的回答
- 每次工具调用，包括工具名称、其所需的权限、其结果（`ok`、`error`、`denied`或`cancelled`）、其持续时间以及其参数的名称和总大小
- 每个发送以供运行的 C# 脚本，包括运行时失败、被拒绝或被退回以供审核的脚本，均保存为带有其 SHA-256 哈希值的 `.csx` 文件
- 每个聊天回合的提供程序、模型、端点主机和令牌计数
- AI 配置更改
- MCP 服务器的启动和停止，以及每个资源的权限级别
- MCP 代理连接，包含客户端报告的名称和版本

提示文本、回复文本、参数值、来自模型的数据值、API 密钥和访问令牌均不会被记录。无法编译的脚本以及 AI 功能写入文档供用户运行的脚本不会被保存。

除非 `AiAuditLogRetentionDays` 设置了其他期限，否则超过 30 天的文件将被删除，而 `0` 表示保留所有文件。每个 Tabular Editor 3 副本都会在其会话中写入第一条记录之前，从其写入的文件夹中删除过期的文件。

日志由用户自己的 Tabular Editor 3 进程写入，因此用户对其具有写入和删除权限，包括在重定向的共享上。如果无法写入日志，例如由于共享不可访问，AI 助手和 MCP 服务器将继续运行，并且故障将写入 Tabular Editor 的应用程序日志一次。

`AiAuditLogPath` 会重定向日志。相对路径将被忽略。每日文件名和脚本文件名不包含用户或计算机名称，因此请为每位用户提供一个单独的文件夹。`%USERNAME%` 等环境变量仅在 `REG_EXPAND_SZ` 值中展开；管理模板写入 `REG_SZ`，该值按写入内容使用。

有关记录格式，请参阅 @ai-audit-log。

## 建议的基准

以下基线是针对允许进行 AI 辅助模型开发且不将模型数据提供给 AI 提供商的组织的指导。请根据您自己的风险评估进行调整。

| 控制项 | 设置 | 效果 |
| -- | -- | -- |
| 提供商 | `AiProvider`、`AiEndpoint`、`AiModel` 和 `AiAllowedEndpointHosts` 设置为您的组织拥有并签订了数据处理协议的资源 | AI 助手仅向该端点发送请求，并使用您的组织颁发的密钥 |
| 模型数据 | `MaxModelDataAccess` 设置为 `Deny` | 没有 DAX 查询结果或 Analysis Services 错误文本传送到 AI 助手或 MCP 代理 |
| 宏 | `MaxMacrosAccess` 设置为 `Deny` | 宏代码不会发送到 AI 提供商 |
| 脚本 | `BlockUnsafeScripts` 设置为 `1` | 任何脚本或宏都不能写入文件、访问网络、启动其他程序或加载外部代码 |
| MCP 身份验证 | `RequireMcpAccessToken` 设置为 `1` | 只有具有用户访问令牌的客户端才能连接到 MCP 服务器 |
| 审计保留 | `AiAuditLogRetentionDays` 设置为您的保留要求 | 审计文件保留该期限 |
| 审计位置 | `AiAuditLogPath` 为每位用户设置为共享上的文件夹 | 审计文件集中收集 |

以下注册表文件应用基线的全机范围部分。它将 AI 助手锁定到 Azure OpenAI 资源，并保留审计文件 365 天。将端点和部署名称替换为您自己的名称，并将该文件仅应用于已获得企业版许可证的计算机：

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

`BlockUnsafeScripts` 位于共享键中，因此 Tabular Editor CLI 也会强制执行该设置。将 `AiAuditLogPath` 设置为每个用户的文件夹：可以是 `HKEY_LOCAL_MACHINE` 项下的 `REG_EXPAND_SZ` 值（例如 `\\fileserver\te-audit$\%USERNAME%`），也可以是 `HKEY_CURRENT_USER\SOFTWARE\Policies\Tabular Editor ApS\TE3` 下的每个用户的 `REG_SZ` 值。

## 常见问题

### Tabular Editor ApS 是否会收到我们的提示、元数据或数据？

不会。请参阅[数据流](#data-flow)。

### 我们的数据是否被用于训练 AI 模型？

Tabular Editor ApS 不会收到任何提示、回复或模型内容。您与 AI 提供商的协议决定了提供商是否根据请求进行训练。

### 我们的数据在哪里处理？

在 AI 助手的配置端点以及 MCP 代理的提供商运行的任何位置。请参阅[限制 AI 提供商](#restrict-the-ai-provider)。

### 用户可以绕过策略吗？

用户如果没有本地管理员权限，就无法更改策略。3.27.0 之前的版本（包括较旧的便携式版本）仅读取 `HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor`，并忽略此页面上的所有策略。请参阅[关闭 AI 功能](#turn-the-ai-features-off)。

### AI 功能可以更改或部署生产模型吗？

它们仅在**模型元数据**为**写入**时才在已加载的模型上运行脚本，并且仅由用户保存或部署。请参阅[模型更改的保障措施](#safeguards-on-model-changes)。

### AI 功能可以读取我们模型中的数据吗？

DAX 查询结果和 Analysis Services 错误的文本需要**读取**权限下的**模型数据**，默认值为**拒绝**。在**读取**下方，来自服务器的错误文本被替换为固定句子。在模型定义中输入的值是元数据的一部分。请参阅[数据流](#data-flow)。

### MCP 代理是否可以使用我们未批准的提供商？

可以。通过代理自身的管理控制来管理代理，或者设置 `DisableMcpServer`。请参阅[MCP 服务器](#mcp-server)。

### 如何在事件中停止 AI 功能？

设置 `DisableAi` 并让用户重启 Tabular Editor 3。在提供商处撤销受影响的 API 密钥。请参阅[关闭 AI 功能](#turn-the-ai-features-off)。

### 审计日志是否具有防篡改性？

不可以。用户可以更改和删除自己的审计文件。请参阅[审计日志](#audit-log)。

## 另请参阅

- @ai-assistant
- @mcp-server
- @ai-audit-log
- @policies
- @security-privacy
- @editions
