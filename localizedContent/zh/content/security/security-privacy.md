---
uid: security-privacy
title: 安全概述
author: Daniel Otykier
updated: 2026-09-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Tabular Editor 3 的安全与隐私

本文档介绍 Tabular Editor 3 及其使用中的安全与隐私注意事项。下文中，“Tabular Editor”一词既可指商业工具 Tabular Editor 3，也可指开源工具 Tabular Editor 2.X。每当内容仅涉及其中一个工具时，我们会明确使用其名称“Tabular Editor 3”或“Tabular Editor 2.X”。

## Microsoft 关于 Tabular Editor 等第三方工具的建议

Microsoft 在此处说明其支持使用社区第三方工具：[用于开发企业级 Power BI 和 Analysis Services 模型的社区和第三方工具](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft 的 Power BI 实施规划文档在高级数据建模场景与企业级开发中明确提到 Tabular Editor：[Power BI 使用场景：高级 Data model 管理](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## 信任中心

在 Tabular Editor，我们始终坚持透明原则，并践行严格的安全实践。访问我们的[信任中心](https://trust.tabulareditor.com/)，查看 SOC 2 审计 Report、关键政策文件、许可条款，以及我们在基础设施和组织安全方面的做法。您还可以找到有关我们子处理方的信息，以及我们如何确保您的数据安全。

## 元数据与数据隐私

Tabular Editor 主要是一款离线工具，这意味着所有数据和元数据都保存在安装了 Tabular Editor 的本机上，所有用户交互也都在本地完成。运行和使用 Tabular Editor 无需互联网连接。

不过，在某些场景下，Tabular Editor 会出于不同目的连接到远程服务。具体如下：

### Analysis Services XMLA 协议

与 Analysis Services 实例或 Power BI Premium Workspace 的所有通信，都通过 [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 客户端库进行；更具体地说，是通过 [AMO 的 Tabular Object Model (TOM) 扩展](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)。这些客户端库由 Microsoft 提供，可在 Tabular Editor 等第三方应用程序中再分发。有关许可的详细信息，见 [AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989)。

当 Tabular Editor 连接到 Analysis Services 实例（本地网络或云端）或 Power BI Premium Workspace（云端）时，会通过上述客户端库建立连接。按照设计，AMO 库负责处理用户的身份验证和授权。只有在 Analysis Services 实例或 Power BI Premium Workspace 中具有管理员权限的用户才能连接。这与使用 SQL Server Management Studio 或 SQL Server Data Tools 等 Microsoft 工具并无不同（它们使用相同的客户端库进行连接）。

### Tabular Object Model 元数据

AMO/TOM 客户端库建立连接后，Tabular Editor 会请求用户要连接的特定 Analysis Services 数据库或 Power BI Dataset 的完整 Tabular Object Model（TOM）元数据。然后，AMO/TOM 客户端库会以编程方式将这些元数据提供给客户端应用程序（Tabular Editor），使应用程序能够应用元数据更改，例如重命名对象、添加说明、修改 DAX 表达式等。此外，AMO/TOM 客户端库还提供了将 TOM 元数据序列化为基于 JSON 的格式的方法。 Tabular Editor 使用此技术让用户可以将模型元数据保存为本地 JSON 文件，用于对 Data model 结构进行版本控制。\*\*注意：以这种方式生成的 JSON 文件不包含任何实际数据记录。该文件仅包含模型元数据，即有关模型结构的信息，包括表、列、度量值、DAX 表达式等。\*\*虽然模型元数据通常不被视为机密信息，但使用 Tabular Editor 的用户仍有责任按所需的保密要求处理以这种方式生成的任何文件（即不与第三方共享此类文件等）。

**除非用户明确发起相关操作，否则 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过 AMO/TOM 客户端库获取的任何模型元数据**（例如，将模型元数据 JSON 文件保存到共享网络位置，或将模型元数据部署到另一个 Analysis Services 实例或 Power BI Workspace）。

### 模型数据内容

下文中，“模型数据”指存储在 Analysis Services 数据库或 Power BI Dataset 中的实际数据记录。根据源数据库或 Dataset 的不同，模型数据很可能属于机密信息。

由于用户必须在要连接的 Analysis Services 实例或 Power BI Workspace 中具有管理员权限，因此从定义上说，用户也能访问 Analysis Services 数据库或 Power BI Dataset 中的全部数据内容。 Tabular Editor 仅允许通过上述 AMO 客户端库检索数据。 Tabular Editor 3 提供了浏览和查询模型数据的功能。无论使用哪种技术访问数据，**Tabular Editor 都只会将检索到的数据存储在本地内存中。 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过该工具获取的任何模型数据**。如果用户选择复制或导出通过 Tabular Editor 获取的查询结果，则有责任根据数据的保密级别妥善处理所复制或导出的数据。这与用户使用 Excel 或 Power BI 等客户端工具连接到 Analysis Services 数据库或 Power BI Dataset 并无不同；在这种情况下，用户同样可以选择复制查询结果。

### AI 助手

Tabular Editor 3 内置 AI 助手，用于基于聊天的语义模型开发。从 3.27.0 起，它已成为默认安装的一部分；在此之前，需要手动选择安装。如果未安装该组件，计算机上就不会存在任何与 AI 相关的代码，本节所述的行为也都不适用。

AI 助手采用 **自备密钥** 模式。您需要提供来自受支持的 AI 提供商的 API 密钥（OpenAI、Anthropic、Azure OpenAI 或任何与 OpenAI 兼容的端点）。不包含内置 API 密钥，Tabular Editor 也不提供或中转任何 AI 服务。

**数据流。** AI 助手与 AI 提供商之间的所有通信都在客户端计算机与提供商 API 之间直接进行。不会有任何数据经过 Tabular Editor 的服务器。发送哪些内容取决于您的请求，并受五类权限资源的限制；每类资源对应一个访问级别：

| 资源      | 涵盖内容                                                           | 级别           | 默认值 |
| ------- | -------------------------------------------------------------- | ------------ | --- |
| 模型元数据   | 表、列和度量值名称、表达式、说明等。“读取”还包括 VertiPaq分析器统计信息                      | 拒绝 / 读取 / 写入 | 读取  |
| 模型数据    | 模型中的数据值，例如 DAX 查询结果。需要实时连接                                     | 拒绝 / 读取      | 拒绝  |
| 最佳实践分析器 | “读取”用于列出规则并运行分析；“写入”用于添加或修改规则                                  | 拒绝 / 读取 / 写入 | 读取  |
| 文档      | 你当前打开的 C# Script 脚本编辑器和 DAX 查询编辑器。“读取”用于查看其内容；要创建或修改它们，则需要“写入” | 拒绝 / 读取 / 写入 | 写入  |
| 宏       | 你的宏库                                                           | 拒绝 / 读取 / 写入 | 写入  |

写入权限包含读取权限。默认拒绝访问模型数据，因为元数据描述的是模型本身，而数据值才是模型的内容。

**权限管理。** 这些授权是持续生效的设置，而不是按每次请求弹出的提示。你可以在 **工具 > 偏好 > AI 功能 > 权限** 中查看和更改这些设置，也可以在 **工具 > MCP 服务器...** 对话框中进行编辑；两处修改的是同一项设置。当聊天需要的权限超出当前授权范围时，会在当时显示权限卡片，你可以选择仅对本轮、本次会话、当前模型或始终允许。**始终允许** 会提高持续授权级别，但不会降低已有授权。全局授权存储在本地 Preferences.json 偏好文件中；针对单个模型授予的授权存储在该模型的用户选项 (.tmuo) 文件中，并且仅对该聊天生效。将某个资源重新设为 **拒绝** 后，聊天会再次询问。

**管理员上限。** 在企业版、咨询版和试用版中，管理员可以通过 [策略](xref:policies) 为每项资源分别设置上限，并分别应用于聊天和 MCP 服务器；MCP 的上限只能更低。上限优先于任何授权，包括用户已经给出的授权，并且对应选项会显示为只读。这些策略采用默认拒绝机制：如果某台机器上存在任何企业级策略值，但该机器并未获得相应许可，AI 助手和 MCP 服务器将拒绝启动，而不是忽略该策略。

**审计记录。** Tabular Editor 3 会在本地记录 AI 助手和 MCP 服务器执行过的操作：请求了哪些权限以及如何响应、运行了哪些工具以及每个工具是成功、失败还是被拒绝，以及代理运行或提交供你审核的任何 C# Script 的完整文本。提示词、回复和数据值不会被记录。每日文件会保留 30 天，在 **工具 > 偏好 > AI 功能** 下选择 **打开审计文件夹** 可打开它们所在的文件夹。管理员可以重定向存储位置并更改保留期限。

**API 密钥存储。** API 密钥会以加密方式存储在本地计算机的偏好文件 Preferences.json 中。如果 AI 模块未加载（例如在安装期间被排除，或因策略而被禁用），之前存储的 API 密钥配置会自动清除。

**对话存储。** 对话会存储在客户端本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中。不会将任何对话数据发送到 Tabular Editor 服务器。

**禁用 AI 助手。** 你可以在安装时排除 AI 功能组件，在 **工具 > 偏好 > AI 功能 > AI 助手** 下清除提供程序，或通过 Windows 注册表强制实施 [策略](xref:policies)：`DisableAi` 会关闭包括 MCP 服务器在内的所有 AI 功能，并清除已存储的提供程序配置；`DisableAiChat` 则只关闭聊天功能，并让 MCP 服务器继续运行。

**渗透测试。** 已对 AI 助手进行了单独的渗透测试。该 Report 可在我们的 [信任中心](https://trust.tabulareditor.com/) 查看。

### MCP 服务器

Tabular Editor 3 可以充当 MCP（Model Context Protocol）服务器，使在同一台计算机上运行的 AI 代理能够处理你当前打开的模型。关于该功能本身，可参见 @mcp-server。

**网络暴露。** 该服务器是一个显式绑定到 `127.0.0.1` 的 HTTP 侦听器，默认使用端口 42100。无法从另一台计算机访问它。为防范 DNS 重绑定，浏览器发出的、携带非本地 `Origin` 标头的请求会被拒绝。该服务器仅在你启动后才会运行；如果你选择随应用启动，也可以在应用启动时自动运行。

**身份验证。** 回环绑定是默认的安全边界，因此服务器默认会在无需凭据的情况下接受本地连接。但在一个同时有多名用户登录的主机上（例如远程桌面或 Citrix 服务器），这还不够：该机器上的任何会话都可以访问 `127.0.0.1`。未启用访问令牌时，该机器上的任何进程都可以在无凭据的情况下连接。在 **工具 > 偏好 > AI 功能 > MCP 服务器** 下启用 **要求访问令牌**，客户端就必须提供 Bearer 令牌；该令牌会以加密形式存储在本地的 Preferences.json 文件中。管理员可以通过 `RequireMcpAccessToken` [策略](xref:policies) 强制实施此要求。

**数据流。** Tabular Editor 不会为此功能联系任何 AI 提供程序，也不会为其保存任何 API 密钥。只有代理会与提供程序通信，并使用其自身的配置和订阅。代理可从模型中读取的内容，受与 AI 助手相同的五项权限授予所限制；这些授予会在服务器启动时进行快照保存，任何不在授予范围内的工具都不会提供给代理。默认不允许访问模型数据，因此除非你明确授予该权限，否则不会有任何数据值离开模型。

**对模型的更改。** 代理只能通过 C# Script 脚本引擎更改模型；更改会以原子方式执行，并作为单个撤销步骤记录，而且仅在模型元数据权限被授予“写入”时才允许这样做。代理永远无法执行原始 TMSL 和 XMLA；此外，任何会访问模型之外内容的脚本也不会为代理执行。

**审计记录。** 权限决策、工具调用，以及任何由代理运行或提交供审查的 C# Script 的完整文本，都会写入本地审计日志。提示、回复和数据值不会被记录。

**禁用 MCP 服务器。** 在 **工具 > 偏好 > AI 功能 > MCP 服务器** 中取消勾选 **启用 MCP 服务器**，或强制执行 `DisableMcpServer` 或 `DisableAi` [策略](xref:policies)。该服务器属于 AI 功能组件，因此在安装时排除该组件也会一并移除它。

### Web 请求

Tabular Editor 仅会在以下情况下向在线资源（Web URL）发起请求：

- **许可证激活\*.** 首次启动 Tabular Editor 3 时，以及之后的定期时间点，工具可能会向我们的许可服务发起请求。该请求包含以下经过加密的信息：用户输入的许可证密钥、用户的电子邮件地址（如果提供）、本地计算机名称，以及用于标识当前安装的单向编码哈希值。此请求不会传输其他数据。此请求的目的是激活并验证该安装所使用的许可证密钥、实施试用限制，以及让用户能够通过我们的许可服务管理其 Tabular Editor 3 安装。
- **升级检查\*.** 每次启动 Tabular Editor 3 时，它可能会向我们的应用服务发起请求，以确定是否有可用的新版 Tabular Editor 3。此请求不包含任何数据。
- **使用情况遥测\*.** 默认情况下，Tabular Editor 3 会在用户与该工具交互时收集并传输匿名使用数据。这些数据包括用户与哪些 UI 对象交互，以及每次交互的时间信息。其中还包含有关通过该工具编辑的 Tabular Data model 的高级信息。这些信息仅涉及兼容级别、模式、表数量、服务器类型（Analysis Services、Power BI 或 Power BI Desktop）等高级属性。**不会通过这种方式收集任何可识别个人身份的数据**；我们也不会收集 Tabular Object Model 本身中任何对象名称或 DAX 表达式的信息。用户可随时选择停止向我们发送遥测数据。
- **错误 Report\*.** 当发生意外错误时，我们会传输堆栈跟踪和（已匿名化的）错误信息，并附带你提供的可选说明。如果用户选择不发送遥测数据，错误 Report 也不会发送。
- **使用 DAX 格式化器。**（仅限 Tabular Editor 2.x）你可以在 Tabular Editor 中点击按钮来格式化 DAX 表达式。在这种情况下，会将 DAX 表达式（且仅此一项）发送到 www.daxformatter.com Web 服务。用户首次单击此按钮时，会显示一条明确的警告信息，要求其确认此操作。 Tabular Editor 3 在格式化 DAX 代码时不会发起 Web 请求。
- **DAX优化器**。如果用户拥有 [Tabular Tools 账户](https://tabulartools.com)，并订阅了 [DAX优化器](https://daxoptimizer.com)，即可直接在 Tabular Editor 3 中浏览自己的 DAX优化器 Workspace、查看问题和建议，并上传新的 VPAX 文件。 VPAX 文件包含模型元数据和统计信息，但不包含实际的模型 _数据_。 Tabular Editor 3 中的 DAX优化器集成功能会向以下一个或多个端点发送请求（具体取决于创建 Tabular Tools 账户时指定的身份验证类型和区域）。<br/>如需了解更多信息，请参阅 [DAX优化器文档](https://docs.daxoptimizer.com/legal/data-processing)。<br/>使用的端点：
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **AI 助手。** 当 AI 助手已完成配置并在使用时，Tabular Editor 3 会将请求直接发送到所配置的 AI 提供商 API。具体端点取决于所选提供商（例如：OpenAI 使用 `https://api.openai.com`，Anthropic 使用 `https://api.anthropic.com`；Azure OpenAI 和自定义提供商则使用用户指定的端点）。这些请求中仅包含权限授予范围内的数据。有关这些资源及其默认值，请查看上文的 [AI 助手](#ai-assistant) 部分。
- **AI 知识库更新。** AI 助手搜索的知识库是随 AI 功能组件一同提供的本地数据库。 Tabular Editor 3 会检查是否有新版本，并从 `https://cdn.tabulareditor.com` 下载。该请求不会携带任何关于用户或其模型的数据。
- **MCP 服务器。** MCP 服务器不会发起任何出站请求。它只接受来自回环接口的连接，而与其连接的代理会按照其自身配置与 AI 提供程序通信。请查看上文的 [MCP 服务器](#mcp-server) 部分。
- **导入最佳实践规则。** Tabular Editor 提供一项功能，让你可以指定一个 URL，从中获取以 JSON 格式提供的最佳实践规则列表。此类请求只会从该 URL 下载 JSON 数据，不会向该 URL 传输任何数据。
- **使用 C# Script。** Tabular Editor 允许用户编写并执行用 C# 编写的代码，以实现自动化。此类脚本可利用 C# 语言功能和 .NET 运行时连接到联机资源。用户始终有责任确保所执行的代码不会导致任何非预期的数据共享。对于因使用 C# Script 功能而造成的任何损害、损失或泄露，Tabular Editor ApS 概不负责。如果没有用户的明确操作，Tabular Editor 绝不会执行 C# Script。

\***我们通过许可证激活服务、使用情况遥测或错误 Report 获得的任何信息，都会予以保密。我们绝不会以任何形式共享、发布或分发所收集的数据。**

**防火墙允许列表 / 接受列表**
如需允许上述 Web 请求的流量，请将以下地址加入允许列表：

- 许可证激活 / 升级检查：**https://api.tabulareditor.com**
- 使用情况遥测 / 错误 Report：**https://\*.in.applicationinsights.azure.com**
- DAX Formatter（仅 Tabular Editor 2.x）：**https://www.daxformatter.com**
- 导入最佳实践规则 / C# Script：视具体情况而定
- DAX优化器：端点见上文列表。
- AI 助手：取决于所配置的提供商（例如 \*\*https://api.openai.com\*\*、\*\*https://api.anthropic.com\*\*，或你指定的 Azure OpenAI / 自定义端点）
- AI 知识库更新：**https://cdn.tabulareditor.com**
- MCP 服务器：无。它监听在 **127.0.0.1**，且不会发起任何出站请求

> [!NOTE]
> 系统管理员可能会强制执行某些[策略](xref:policies)，用来禁用上面列表中的部分或全部功能。

## 应用程序安全

Tabular Editor 安装在 Windows 电脑上时不需要任何提升权限，也不会访问这台电脑上的任何受限资源。不过有一个例外：如果使用 Tabular Editor 安装程序文件 (.msi)，该工具所需的可执行文件和支持文件默认会复制到 `Program Files` 文件夹，这通常需要提升权限。 Tabular Editor 的二进制文件和安装程序文件均已使用颁发给 Tabular Editor ApS 的代码签名证书进行签名，这能保证代码未被任何第三方篡改。

应用程序运行时，所有对外部资源的访问都通过 AMO/TOM 客户端库或上面提到的 Web 请求完成。

C# Script 功能允许 Tabular Editor 在 .NET 运行时中执行任意 C# 代码。此类代码仅会在用户明确请求时才会编译和执行。 C# Script 也可以保存为“宏”，这样用户就能更轻松地管理和执行多个不同的脚本。代码会存储在用户自己的 `%localappdata%` 文件夹中，从而确保只有该用户本人或本机管理员才能访问这些脚本。用户始终有责任确保所执行的代码不会产生任何意外的副作用。在任何情况下，Tabular Editor ApS 均不对因使用 C# Script 或自定义操作/宏功能而造成的任何损害、损失或泄漏承担责任。

不希望由单个用户自行决定此事的组织，可以进行集中管控。 `DisableCSharpScripts` 和 `DisableMacros` [策略](xref:policies)会在所有版本中将这些功能（C# 脚本和宏）完全关闭。在 Tabular Editor 3 企业版中，`BlockUnsafeScripts` 会保留脚本功能，但只允许在语义模型范围内运行的脚本和宏：任何读取或写入文件、访问网络、启动其他程序或加载外部代码的操作，都会在运行前被拒绝，无论脚本来自何处——脚本文档、Best Practice Analyzer、宏、AI Assistant、MCP 服务器或命令行。参见[管理员策略](xref:csharp-scripts#administrator-policies)。
