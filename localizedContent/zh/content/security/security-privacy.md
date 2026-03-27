---
uid: security-privacy
title: 安全概述
author: Daniel Otykier
updated: 2026-03-25
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

本文档介绍 Tabular Editor 3 及其使用过程中的安全与隐私注意事项。 下文中，“Tabular Editor”一词既可指商业工具 Tabular Editor 3，也可指开源工具 Tabular Editor 2.X。 当内容仅针对其中一款工具时，我们将使用明确名称“Tabular Editor 3”或“Tabular Editor 2.X”。

## Microsoft 关于 Tabular Editor 等第三方工具的建议

Microsoft 在此处说明其支持使用社区第三方工具：[用于开发企业级 Power BI 和 Analysis Services 模型的社区和第三方工具](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft 的 Power BI 实施规划文档在高级数据建模场景与企业级开发中明确提到 Tabular Editor：[Power BI 使用场景：高级 Data model 管理](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## 信任中心

在 Tabular Editor，我们坚持透明度，并践行强有力的安全措施。 访问我们的 [信任中心](https://trust.tabulareditor.com/)，了解我们的 SOC 2 审计报告、关键政策文档、许可条款，以及我们在基础设施和组织安全方面的做法。 您还可以了解我们的子处理方，以及我们为保障您的数据安全所做的工作。

## 元数据与数据隐私

Tabular Editor 主要是一款离线工具，这意味着所有数据和元数据都保存在安装了 Tabular Editor 的本机上，所有用户交互也都在本地完成。 运行和使用 Tabular Editor 不需要互联网连接。

不过，在某些场景下，Tabular Editor 会出于不同目的连接到远程服务。 具体如下：

### Analysis Services XMLA 协议

与 Analysis Services 实例或 Power BI Premium Workspace 的所有通信，都通过 [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 客户端库进行；更具体地说，是通过 [AMO 的 Tabular Object Model (TOM) 扩展](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)。 这些客户端库由 Microsoft 提供，可供 Tabular Editor 等第三方应用程序重新分发。 有关许可详情，请参阅 [AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989)。

当 Tabular Editor 连接到 Analysis Services 实例（本地网络或云端）或 Power BI Premium Workspace（云端）时，会通过上述客户端库建立连接。 按设计，AMO 库负责处理用户的身份验证和授权。 只有在 Analysis Services 实例或 Power BI Premium Workspace 上拥有管理员权限的用户才允许连接。 这与使用 SQL Server Management Studio 或 SQL Server Data Tools 等 Microsoft 工具并无不同（这些工具连接时也使用相同的客户端库）。

### Tabular Object Model 元数据

AMO/TOM 客户端库建立连接后，Tabular Editor 会请求用户要连接的特定 Analysis Services 数据库或 Power BI Dataset 的完整 Tabular Object Model (TOM) 元数据。 随后，AMO/TOM 客户端库会以编程方式将这些元数据提供给客户端应用程序（Tabular Editor），使应用程序能够应用元数据更改，例如重命名对象、添加说明、修改 DAX 表达式等。 此外，AMO/TOM 客户端库还提供将 TOM 元数据序列化为基于 JSON 的格式的方法。 Tabular Editor 使用该技术，使用户能够将模型元数据保存为本地 JSON 文件，用于对 Data model 结构进行版本控制。 **注意：以此方式生成的 JSON 文件不包含任何实际数据记录。 该文件仅包含模型元数据，即关于模型结构的信息，包括表、列、度量值、DAX 表达式等。** 虽然模型元数据通常不被视为机密信息，但 Tabular Editor 的用户有责任按所需的保密要求妥善处理以这种方式生成的任何文件（例如，不与第三方共享该文件等）。

**除非用户明确发起相关操作，否则 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过 AMO/TOM 客户端库获取的任何模型元数据**（例如，将模型元数据 JSON 文件保存到共享网络位置，或将模型元数据部署到另一个 Analysis Services 实例或 Power BI Workspace）。

### 模型数据内容

下文中，“模型数据”指存储在 Analysis Services 数据库或 Power BI Dataset 中的实际数据记录。 根据源数据库或 Dataset 的不同，模型数据很可能属于机密信息。

由于连接到 Analysis Services 实例或 Power BI Workspace 需要具备管理员权限，因此用户也将能够访问 Analysis Services 数据库或 Power BI Dataset 中的全部数据内容。 Tabular Editor 仅允许通过上述 AMO 客户端库检索数据。 Tabular Editor 3 提供用于浏览和查询模型数据的功能。 无论使用哪种技术访问数据，**Tabular Editor 都只会将检索到的数据存储在本地内存中。 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过该工具获取的任何模型数据**。 如果用户选择复制或导出通过 Tabular Editor 获取的查询结果，则其有责任根据数据的保密级别来处理这些复制或导出的数据。 这与使用 Excel 或 Power BI 等客户端工具连接到 Analysis Services 数据库或 Power BI Dataset 并无不同；在这种情况下，你同样可以选择复制查询结果。

### AI Assistant

Tabular Editor 3 includes an optional AI Assistant for chat-based semantic model development. The AI Assistant is an optional module that the user selects during installation. If you choose not to install the module, no AI-related code is present on the machine and none of the behavior described in this section applies. The AI Assistant uses a **bring-your-own-key** model. You provide an API key from a supported AI provider (OpenAI, Anthropic, Azure OpenAI or any OpenAI-compatible endpoint). No built-in API key is included and Tabular Editor does not provide or intermediate any AI service.

**Data flow.** All communication between the AI Assistant and the AI provider happens directly from the client machine to the provider API. No data passes through Tabular Editor servers. The data sent depends on the actions you perform in the chat and is scoped to the following categories, each requiring explicit user consent before any data is transmitted:

| Consent Category | Data Sent to AI Provider                                                          |
| ---------------- | --------------------------------------------------------------------------------- |
| Model metadata   | Table and column schemas, measure definitions and other structural model metadata |
| Query data       | DAX query results and data samples                                                |
| Read documents   | Content from open documents such as DAX scripts and DAX queries                   |
| Modify documents | Requests to make changes to open documents                                        |
| Edit BPA rules   | Best Practice Analyzer rule definitions                                           |
| Read macros      | Macro definitions from the user macro library                                     |

**Consent management.** The AI Assistant prompts for consent the first time it needs access to each data category. You choose the duration of your consent: single request, current session, the current model only, or always. You can review and revoke consents at any time under **Tools > Preferences > AI Assistant > AI Consents**. Per-model consents for query data and model metadata are stored in the model user options (.tmuo) file. Global "always" consents are stored in the local Preferences.json file.

**API key storage.** API keys are stored encrypted on the local machine in the Preferences.json file. If the AI module is not loaded (for example because it was excluded during installation or disabled by policy), any previously stored API key configuration is cleared automatically.

**Conversation storage.** Conversations are stored locally on the client machine in `%LocalAppData%\TabularEditor3\AI\Conversations\`. No conversation data is sent to Tabular Editor servers.

**Disabling the AI Assistant.** The AI Assistant is an optional component. You can exclude it during installation, disable it under **Tools > Preferences > AI Assistant**, or enforce the `DisableAi` [policy](xref:policies) through the Windows registry.

**Penetration testing.** A separate penetration test of the AI Assistant has been performed. The report is available in our [Trust Center](https://trust.tabulareditor.com/).

### Web 请求

Tabular Editor 仅会在以下情况下向在线资源（Web URL）发起请求：

- **许可证激活\*.** 首次启动 Tabular Editor 3 时，以及此后定期，工具可能会向我们的许可服务发起请求。 该请求包含你输入的许可证密钥的加密信息、你的电子邮件地址（如有提供）、本地计算机名称，以及用于标识当前安装的单向编码哈希值。 该请求不会传输任何其他数据。 该请求用于激活并验证此安装所使用的许可证密钥、执行试用限制，并允许你通过我们的许可服务管理你的 Tabular Editor 3 安装。
- **升级检查\*.** 每次启动 Tabular Editor 3 时，它可能会向我们的应用服务发起请求，以确定是否有可用的新版 Tabular Editor 3。 该请求不包含任何数据。
- **使用情况遥测\*.** 默认情况下，Tabular Editor 3 会在你使用工具时收集并传输匿名使用数据。 这些数据包括你与哪些 UI 对象交互，以及每次交互的时间信息。 它还包含有关通过该工具编辑的 Tabular 数据模型的概览信息。 这些信息仅涉及兼容级别和模式、表数量、服务器类型（Analysis Services、Power BI 或 Power BI Desktop）等高层属性。**我们不会以这种方式收集任何个人身份信息**，也不会收集 Tabular Object Model 本身中有关对象名称或 DAX 表达式的任何信息。 你可以随时选择不向我们发送遥测数据。
- **错误 Report\*.** 当发生意外错误时，我们会传输堆栈跟踪和（已匿名化的）错误信息，并附带你提供的可选说明。 如果你选择不发送遥测数据，也不会发送错误 Report。
- **使用 DAX 格式化器。**（仅限 Tabular Editor 2.x）你可以在 Tabular Editor 中点击按钮来格式化 DAX 表达式。 在这种情况下，只会将该 DAX 表达式(and nothing else)发送到 www.daxformatter.com Web 服务。 你第一次点击此按钮时，会显示一条明确的警告信息，让你确认是否继续。 Tabular Editor 3 在格式化 DAX 代码时不会发起 Web 请求。
- **DAX优化器**。 如果你拥有 [Tabular Tools 帐户](https://tabulartools.com) 并订阅了 [DAX优化器](https://daxoptimizer.com)，就可以直接在 Tabular Editor 3 中浏览你的 DAX优化器 Workspace、查看问题和建议，并上传新的 VPAX 文件。 VPAX 文件包含模型元数据和统计信息，但不包含任何实际的模型 _数据_。 Tabular Editor 3 中的 DAX优化器集成功能会向下面一个或多个端点发起各种请求（取决于创建 Tabular Tools 帐户时指定的身份验证类型和区域）。<br/>
  欲了解更多信息，请参阅 [DAX 优化器文档](https://docs.daxoptimizer.com/legal/data-processing)。<br/>
  使用的端点：
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **AI Assistant.** When the AI Assistant is configured and in use, Tabular Editor 3 sends requests directly to the configured AI provider API. The endpoints depend on the selected provider (for example `https://api.openai.com` for OpenAI, `https://api.anthropic.com` for Anthropic, or a user-specified endpoint for Azure OpenAI and custom providers). Only data for which the user has granted consent is included in these requests. See the [AI Assistant](#ai-assistant) section above for details on data categories and consent management.
- **导入最佳实践规则。** Tabular Editor 提供一项功能，让你可以指定一个 URL，从中获取以 JSON 格式提供的最佳实践规则列表。 此类请求只会从该 URL 下载 JSON 数据——不会向该 URL 传输任何数据。
- **使用 C# Script。** Tabular Editor 允许用户编写并执行 C# 代码，以实现自动化。 此类脚本可能会使用 C# 语言特性和 .NET 运行时连接到在线资源。 你始终需要确保执行的代码不会导致任何非预期的数据共享。 对于使用 C# Script 功能可能造成的任何损害、损失或泄露，Tabular Editor ApS 概不负责。 未经用户明确操作，Tabular Editor 绝不会执行 C# Script。

\***我们通过许可证激活服务、使用情况遥测或错误 Report 获得的任何信息，都会予以保密。 我们不会以任何方式、任何形式共享、发布或分发所收集的数据。**

**防火墙允许列表 / 接受列表**
如需允许上述 Web 请求的流量，请将以下地址加入允许列表：

- 许可证激活 / 升级检查：**https://api.tabulareditor.com**
- 使用情况遥测 / 错误 Report：**https://\*.in.applicationinsights.azure.com**
- DAX Formatter（仅 Tabular Editor 2.x）：**https://www.daxformatter.com**
- 导入最佳实践规则 / C# Script：视具体情况而定
- DAX优化器：端点见上文列表。
- AI Assistant: Depends on the configured provider (e.g. **https://api.openai.com**, **https://api.anthropic.com**, or user-specified Azure OpenAI / custom endpoints)

> [!NOTE]
> 系统管理员可能会强制执行某些[策略](xref:policies)，用来禁用上面列表中的部分或全部功能。

## 应用程序安全

Tabular Editor 安装在 Windows 电脑上时不需要任何提升权限，也不会访问这台电脑上的任何受限资源。 此规则有一个例外：如果使用 Tabular Editor 安装程序文件（.msi），工具所需的可执行文件和支持文件默认会复制到 `Program Files` 文件夹；而该文件夹通常需要提升权限。 Tabular Editor 的二进制文件和安装程序文件都已使用签发给 Kapacity A/S 的代码签名证书进行签名，这能保证代码没有被任何第三方篡改。

应用程序运行时，所有对外部资源的访问都通过 AMO/TOM 客户端库或上面提到的 Web 请求完成。

C# Script 功能允许 Tabular Editor 在 .NET 运行时中执行任意 C# 代码。 此类代码仅会在用户明确提出请求时才会编译并执行。 C# Script 也可以保存为“宏”，便于用户管理并执行多个不同的脚本。 代码会存储在用户自己的 `%localappdata%` 文件夹中，确保只有用户本人或本机管理员可以访问这些脚本。 你始终需要负责确保执行的代码不会造成任何非预期的副作用。 在任何情况下，对于因使用 C# Script 或自定义操作/宏功能而造成的任何损害、损失或泄露，Tabular Editor ApS 均不承担任何责任。
