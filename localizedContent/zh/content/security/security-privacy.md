---
uid: security-privacy
title: 安全概览
author: Morten Lønskov
updated: 2026-10-12
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
# Tabular Editor 3 安全与隐私

本文档介绍了 Tabular Editor 3 及其使用的安全和隐私注意事项。在下文中，“Tabular Editor”一词既可以指商业工具 Tabular Editor 3，也可以指开源工具 Tabular Editor 2.X。每当仅涉及其中一个工具时，我们将使用其明确的名称“Tabular Editor 3”或“Tabular Editor 2.X”。

## Microsoft 关于 Tabular Editor 等第三方工具的建议

Microsoft 支持使用社区第三方工具，具体说明请参阅此处：[用于开发企业级 Power BI 和 Analysis Services 模型的社区和第三方工具]( https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft 的 Power BI 实施规划文档特别将 Tabular Editor 列入高级数据建模场景和企业开发中：[Power BI 使用场景：高级数据模型管理](https://learn.microsoft.com/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## 信任中心
在 Tabular Editor，我们致力于透明度和强有力的安全实践。请访问我们的[信任中心](https://trust.tabulareditor.com/)，了解有关我们的 SOC 2 审计报告、关键政策文件、许可条款以及我们对基础设施和组织安全的做法的详细信息。您还将找到有关我们的分包处理者以及我们如何努力保护您的数据安全的信息。

## 元数据和数据隐私

Tabular Editor 主要是一款离线工具，这意味着所有数据和元数据都驻留在安装了 Tabular Editor 的客户端计算机的本地，所有用户交互也都在本地进行。运行和使用 Tabular Editor 无需互联网连接。

话虽如此，在某些情况下，Tabular Editor 会出于各种目的连接到远程服务。这些情况描述如下：

### Analysis Services XMLA 协议

与 Analysis Services 实例或 Power BI Premium 工作区的所有通信均通过使用 [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 客户端库，更具体地说，通过使用 [AMO 的 Tabular Object Model (TOM) 扩展](https://docs.microsoft.com/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)进行。这些客户端库由 Microsoft 提供，用于在 Tabular Editor 等第三方应用程序中进行再分发。有关许可的详细信息，请参阅[AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989)。

当 Tabular Editor 连接到 Analysis Services 实例（本地网络或云）或 Power BI Premium 工作区（云）时，此连接通过上述客户端库进行。根据设计，AMO 库负责处理用户的身份验证和授权。只有在 Analysis Services 实例或 Power BI Premium 工作区上拥有管理员权限的用户才能进行连接。这与使用 SQL Server Management Studio 或 SQL Server Data Tools 等 Microsoft 工具（它们使用相同的客户端库进行连接）的情况并无不同。

### Tabular Object Model 元数据

AMO/TOM 客户端库建立连接后，Tabular Editor 将请求用户希望连接到的特定 Analysis Services 数据库或 Power BI 数据集的完整 Tabular Object Model (TOM) 元数据。然后，AMO/TOM 客户端库以编程方式将这些元数据提供给客户端应用程序（Tabular Editor），使应用程序能够应用元数据更改，例如重命名对象、添加描述、修改 DAX 表达式等。此外，AMO/TOM 客户端库还提供了将 TOM 元数据序列化为基于 JSON 的格式的方法。Tabular Editor 使用此技术允许用户将模型元数据保存为本地 JSON 文件，以便对数据模型结构进行版本控制。**注意：以这种方式生成的 JSON 文件不包含实际数据记录。该文件仅包含模型元数据，即有关模型结构的表、列、度量值、DAX 表达式等信息。**虽然模型元数据通常不被视为机密信息，但 Tabular Editor 用户有责任以必要的保密方式处理以这种方式生成的任何文件（即不与第三方共享文件等）。

**除非用户明确发起相关操作，否则 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过 AMO/TOM 客户端库获得的任何模型元数据**（例如，将模型元数据 JSON 文件保存到共享网络位置，或将模型元数据部署到另一个 Analysis Services 实例或 Power BI 工作区）。

### 模型数据内容

在下文中，“模型数据”是指存储在 Analysis Services 数据库或 Power BI 数据集中的实际数据记录。根据源数据库或数据集的不同，模型数据很可能属于机密。

由于要求用户在其连接到的 Analysis Services 实例或 Power BI 工作区上具有管理员权限，因此，从定义上讲，用户也将有权访问 Analysis Services 数据库或 Power BI 数据集的所有数据内容。Tabular Editor 仅允许通过上述 AMO 客户端库检索数据。Tabular Editor 3 提供浏览和查询模型数据的功能。无论使用哪种技术访问数据，**Tabular Editor 都只将检索到的数据存储在本地内存中。Tabular Editor不会收集、发布、共享、传输或以其他方式公开通过该工具获得的任何模型数据**。如果用户选择复制或导出通过 Tabular Editor 获取的查询结果，则有责任根据数据的机密性处理复制或导出的数据。这与用户使用 Excel 或 Power BI 等客户端工具连接到 Analysis Services 数据库或 Power BI 数据集的情况并无不同，在这种情况下，他们也可以选择复制查询结果。

### AI 助手

Tabular Editor 3 包含一个用于基于聊天的语义模型开发的 AI 助手。从 3.27.0 版本开始，它是默认安装的一部分；在此之前，必须有意识地选择它。如果未安装该组件，则计算机上不存在任何与 AI 相关的代码，本节中描述的任何行为均不适用。

AI 助手使用**自带密钥**模型。您需要提供来自受支持的 AI 提供商（OpenAI、Anthropic、Azure OpenAI 或任何 OpenAI 兼容端点）的 API 密钥。不包含内置API密钥，Tabular Editor不提供或中介任何AI服务。

**数据流。** AI 助手与 AI 提供商之间的所有通信都直接从客户端电脑到提供商 API 进行。没有数据通过 Tabular Editor 服务器。发送的内容取决于您的请求，并受五种权限资源的约束，每种资源都具有一个访问级别：

| 资源 | 涵盖内容 | 级别 | 默认 |
| -- | -- | -- | -- |
| 模型元数据 | 表、列和度量值名称、表达式、描述等。“读”还涵盖 VertiPaq 分析器统计数据 | 拒绝/读/写 | 读 |
| 模型数据 | 来自您模型的数据值，例如 DAX 查询结果。需要实时连接 | 拒绝/读取 | 拒绝 |
| Best Practice Analyzer | “读”可读取规则列表并运行分析；“写”可添加或修改规则 | 拒绝/读/写 | 读 |
| 文档 | 您打开的 C# Script 和 DAX 查询编辑器。“读”是指它们的内容；“写”是指创建或修改它们所需的权限 | 拒绝/读/写 | 写 |
| 宏 | 您的宏库 | 拒绝/读/写 | 写 |

“写”涵盖“读”。默认情况下，模型数据被拒绝，因为元数据描述的是一个模型，其中数据值是模型的内容。

**权限管理。**授权是永久性设置，而不是针对每次请求的提示。请在**工具 > 首选项 > AI 功能 > 权限**下或在**工具 > MCP 服务器……**对话框中查看并更改这些权限，这两个位置编辑的是同一条记录。如果聊天需要某项权限而授权未涵盖，则此时会显示权限卡，您可以选择为该轮、该会话、当前模型或始终授予权限。**始终允许**会提升常设授权，但绝不会降低授权。全局授权存储在本地 Preferences.json 文件中；针对单个模型授予的授权存储在该模型的用户选项 (.tmuo) 文件中，且仅适用于聊天。将资源设置回**拒绝**会导致聊天再次询问。

**管理员上限。**在 Enterprise、Consultancy 和 Trial 版本中，管理员可以通过[策略](xref:policies)为每项资源设置上限，分别针对聊天和 MCP 服务器，且 MCP 的上限只能更低。上限优先于所有授权，包括用户已经授予的授权，并且相应的选项显示为只读。这些策略采用“故障关闭”机制：如果在未获得相应许可证的计算机上存在任何企业级策略值，AI 助手和 MCP 服务器将拒绝启动，而非忽略该策略。

**审计记录。** Tabular Editor 3 会记录 AI 助手和 MCP 服务器的操作的本地记录：请求了哪些权限以及如何回应这些请求，运行了哪些工具以及每个工具是成功、失败还是被拒绝，以及 AI 助手或代理运行或提交运行的任何 C# 脚本的完整文本，包括运行时失败或被拒绝的脚本。提示、回复和数据值均不会被记录，无法编译的脚本或写入文档供用户运行的脚本文本也不会被记录。每日文件将保留 30 天，可通过 **工具 > 首选项 > AI 功能** 下的 **打开审计文件夹** 打开这些文件。管理员可以重定向位置并更改保留期。

**API 密钥存储。** API 密钥以加密形式存储在本地计算机的 Preferences.json 文件中。如果未加载 AI 模块（例如，因为在安装过程中被排除在外或因策略而被禁用），则之前存储的所有 API 密钥配置都会自动清除。

**对话存储。**对话存储在客户端计算机的“%LocalAppData%\TabularEditor3\AI\Conversations\”中。不会将任何对话数据发送到 Tabular Editor 服务器。

**禁用 AI 助手。**您可以在安装过程中排除 AI 功能组件，在**工具 > 首选项 > AI 功能 > AI 助手**下清除提供商，或通过 Windows 注册表强制执行[策略](xref:policies)：“DisableAi”将关闭包括 MCP 服务器在内的所有 AI 功能，并清除已存储的提供商配置；而“DisableAiChat”仅关闭聊天功能，并使 MCP 服务器继续运行。

**渗透测试。**已对 AI 助手进行了单独的渗透测试。该报告可在我们的[信任中心](https://trust.tabulareditor.com/)查阅。

### MCP 服务器

Tabular Editor 3 可以充当 MCP（模型上下文协议）服务器，以便在同一台计算机上运行的 AI 代理可以在您打开的模型上工作。有关该功能本身的信息，请参阅 @mcp-server。

**网络暴露。**该服务器是一个 HTTP 侦听器，显式绑定到“127.0.0.1”，默认情况下位于端口 42100。无法从其他计算机访问。为防范 DNS 重新绑定，系统会拒绝带有非本地“Origin”标头的浏览器请求。服务器仅在您启动后才会运行，或者如果您有此要求，则会在应用程序启动时运行。

**身份验证。**环回绑定是默认边界，因此服务器开箱即用即可接受无需凭据的本地连接。在有数人同时登录的主机上（例如远程桌面或 Citrix 服务器），这并不够：该机器上的任何会话都能访问“127.0.0.1”。在令牌关闭时，计算机上的任何进程都可以在没有凭据的情况下进行连接。在**工具 > 首选项 > AI 功能 > MCP 服务器**下启用**需要访问令牌**，客户端必须出示持有者令牌，该令牌以加密形式存储在本地 Preferences.json 文件中。管理员可以使用“RequireMcpAccessToken”[策略](xref:policies)强制执行此操作。

**数据流。** Tabular Editor不会就此功能联系 AI 提供商，也不会持有其 API 密钥。代理是唯一一个根据自己的配置和订阅与提供商通信的一方。代理可以从模型中读取的内容受制于与管控 AI 助手的相同的五项权限授予，这些权限授予在服务器启动时进行快照，并且任何未被权限授予涵盖的工具绝不会提供给代理。默认情况下，模型数据会被拒绝，因此除非您明确授予权限，否则任何 DAX 查询结果都不会离开模型。在模型定义中输入的值（例如“DATATABLE”表达式或“输入数据表”）是模型元数据，受模型元数据权限的约束。

**对模型的更改。**代理仅通过 C# 脚本引擎以原子方式并作为单个撤消步骤更改模型，并且仅在具有“写入”权限的模型元数据授权的情况下才能更改。代理永远无法执行原始 TMSL 和 XMLA，并且永远不会为其执行超出模型范围的脚本。

**审计记录。**权限决策、工具调用以及代理运行或提交运行的任何 C# 脚本的完整文本都会写入本地审计日志。提示、回复和数据值不会被记录。

**禁用 MCP 服务器。**在**工具 > 首选项 > AI 功能 > MCP 服务器**下取消选中**启用 MCP 服务器**，或强制执行“DisableMcpServer”或“DisableAi”[策略](xref:policies)。服务器是 AI 功能组件的一部分，因此在安装时排除该组件也会将其一并移除。

### Web 请求

Tabular Editor 仅在以下情况下才会向在线资源（网页网址）发起请求：

- **许可证激活\*\。** Tabular Editor 3 首次启动时，以及此后的定期时间间隔内，该工具可能会向我们的许可服务发起请求。此请求包含有关用户输入的许可证密钥、用户电子邮件地址（如果提供）、本地计算机名称以及标识当前安装的单向编码哈希的加密信息。此请求中不会传输其他数据。此请求的目的是激活和验证安装所使用的许可证密钥，实施试用限制，以及允许用户通过我们的许可服务管理其 Tabular Editor 3 的安装。
- **升级检查\*\。**每次启动 Tabular Editor 3 时，它都可能向我们的应用程序服务发出请求，以确定是否有更新版本的 Tabular Editor 3 可用。此请求不包含任何数据。
- **使用遥测数据\*\。**默认情况下，Tabular Editor 3 会在用户与该工具交互时收集并传输匿名使用数据。这些数据包括有关用户与哪些 UI 对象进行交互以及每次交互的时间的信息。它还包含有关通过该工具编辑的表格数据模型的高级信息。这些信息仅与兼容性级别和模式、表数、服务器类型（Analysis Services、Power BI 或 Power BI Desktop）等高级属性相关。**我们不会以这种方式收集任何个人身份识别数据**，也不会收集有关 Tabular Object Model 本身中对象名称或 DAX 表达式的任何信息。用户可以随时选择退出向我们发送遥测数据。
- **错误报告\*\。**当发生意外错误时，我们会传输堆栈跟踪和（匿名的）错误消息，以及用户提供的可选描述。如果用户选择不发送遥测数据，则也不会发送错误报告。
- **使用 DAX 格式化程序。**（仅限 Tabular Editor 2.x）可以通过点击 Tabular Editor 中的按钮来格式化 DAX 表达式。在这种情况下，DAX 表达式（仅此而已）将发送到 www.daxformatter.com Web 服务。用户首次单击此按钮时，系统会显示一条明确的警告消息，要求他们确认自己的意图。Tabular Editor 3 在格式化 DAX 代码时不会执行 Web 请求。
- **DAX Optimizer**。如果用户拥有具有 [DAX Optimizer](https://tabulartools.com) 订阅的 [Tabular Tools 帐户](https://daxoptimizer.com)，他们将能够浏览其 DAX Optimizer 工作区、查看问题和建议，并直接从 Tabular Editor 3 中上传新的 VPAX 文件。VPAX 文件包含模型元数据和统计信息，但不包含实际的模型*数据*。Tabular Editor 3 中的 DAX Optimizer 集成功能会导致向以下一个或多个端点发出各种请求（具体取决于创建 Tabular Tools 账户时指定的身份验证类型和区域）。<br/>
  有关更多信息，请参阅[DAX Optimizer 文档](https://docs.daxoptimizer.com/legal/data-processing)。<br/>
  使用的端点：
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **AI 助手。**配置并使用 AI 助手时，Tabular Editor 3 会直接向配置的 AI 提供商 API 发送请求。端点取决于所选的提供商（例如，OpenAI 为“https://api.openai.com”，Anthropic 为“https://api.anthropic.com”，Azure OpenAI 和自定义提供商为用户指定的端点）。这些请求中仅包含权限授予所涵盖的数据。有关资源及其默认值，请参阅上文的[AI 助手](#ai-assistant)部分。
- **AI 知识库更新。** AI 助手搜索的知识库是随 AI 功能组件一起提供的本地数据库。Tabular Editor 3 会检查是否有更新的副本，并从“https://cdn.tabulareditor.com”下载。该请求不包含有关您或您的模型的数据。
- **AI 模型目录。**当用户打开 OpenAI 或 Anthropic 提供程序的模型列表时，Tabular Editor 3 会从“https://api.tabulareditor.com/AiModels”下载可用模型列表，并将其缓存到“%LocalAppData%\TabularEditor3\AiModels.json”中 24 小时。该请求是匿名的，不包含有关您、您的 API 密钥或您的模型的数据。“DisableUpdates”策略会将其关闭。
- **MCP 服务器。** MCP 服务器不发出出站请求。它仅接受环回接口上的连接，与之连接的代理根据其自身的配置与 AI 提供商进行通信。请参阅上方的[MCP 服务器](#mcp-server)部分。
- **导入最佳实践规则。** Tabular Editor 有一项功能，允许用户指定一个 URL，从中以基于 JSON 的格式检索最佳实践规则列表。此类型的请求仅从 URL 下载 JSON 数据，不会向 URL 传输任何数据。
- **使用 C# 脚本。** Tabular Editor 允许用户编写和执行用 C# 编写的代码，以实现自动化。此类脚本可能使用 C# 语言功能和 .NET 运行时连接到在线资源。用户始终有责任确保所执行的代码不会导致任何意外的数据共享。对于因使用 C# 脚本功能而导致的任何损害、损失或泄露，Tabular Editor ApS 概不承担责任。如果没有用户的明确操作，Tabular Editor 绝不会执行 C# 脚本。

\***我们通过许可证激活服务、使用情况遥测数据或错误报告获得的任何信息均将予以保密。我们不会以任何方式、形式或形式分享、发布或分发所收集的数据。**

**防火墙允许列表/接受列表**
要允许上述 Web 请求的流量，您必须将以下地址列入白名单：
- 许可证激活/升级检查/AI 模型目录：**https://api.tabulareditor.com**
- 使用情况遥测/错误报告：**https://*.in.applicationinsights.azure.com**
- DAX Formatter（仅限 Tabular Editor 2.x）：**https://www.daxformatter.com**
- 导入最佳做法规则/C# 脚本：取决于上下文
- DAX优化器：上述端点。
- AI 助手：取决于所配置的提供商（例如 **https://api.openai.com**、**https://api.anthropic.com** 或用户指定的 Azure OpenAI/自定义端点）
- AI 知识库更新：**https://cdn.tabulareditor.com**
- MCP 服务器：无。它在 **127.0.0.1** 上侦听，不发出任何出站请求。

> [!NOTE]
> 系统管理员可能会强制执行某些[策略](xref:policies)，这些策略可用于禁用上述列表中显示的部分或全部功能。

## 应用程序安全

Tabular Editor 在其安装所在的 Windows 计算机上不需要任何提升的权限，也不会访问该计算机上的任何受限资源。此规则的一个例外是，如果使用 Tabular Editor 安装程序文件 (.msi)，则该工具所需的可执行文件和支持文件默认情况下会复制到“Program Files”文件夹，该文件夹通常需要提升的权限。Tabular Editor 二进制文件和安装程序文件均已使用签发给 Tabular Editor ApS 的代码签名证书进行签名，这可以保证代码未被任何第三方篡改。

当应用程序运行时，对外部资源的所有访问均通过 AMO/TOM 客户端库或上述 Web 请求进行。

C# 脚本功能允许 Tabular Editor 在 .NET 运行时中执行任意 C# 代码。此类代码仅在用户明确要求时才会编译和执行。C# 脚本还可以保存为“宏”，这使用户能够更轻松地管理和执行多个不同的脚本。代码存储在用户自己的“%localappdata%”文件夹中，确保只有用户本人或本地计算机管理员才能访问脚本。用户始终有责任确保所执行的代码不会造成任何意外的副作用。在任何情况下，Tabular Editor ApS 均不对因使用 C# 脚本或自定义操作/宏功能而导致的任何损害、损失或泄露承担责任。

不想将此事项留给个人用户处理的组织可以集中管理。“DisableCSharpScripts”和“DisableMacros”[策略](xref:policies)会在所有版本中完全禁用这些功能。使用 Tabular Editor 3 企业版，“BlockUnsafeScripts”使脚本功能保持可用，但仅允许在语义模型范围内的脚本和宏：任何读取或写入文件、访问网络、启动其他程序或加载外部代码的操作，无论脚本来自何处（脚本文档、Best Practice Analyzer、宏、AI 助手、MCP 服务器或命令行），都会在其运行之前被拒绝。请参阅[管理员策略](xref:csharp-scripts#administrator-policies)。
