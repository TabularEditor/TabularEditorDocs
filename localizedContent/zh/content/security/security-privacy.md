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

This document describes the security and privacy considerations of Tabular Editor 3 and its use. 下文中，“Tabular Editor”一词既可指商业工具 Tabular Editor 3，也可指开源工具 Tabular Editor 2.X。 Whenever something considers only one of the tools, we will use their explicit names "Tabular Editor 3" or "Tabular Editor 2.X".

## Microsoft 关于 Tabular Editor 等第三方工具的建议

Microsoft 在此处说明其支持使用社区第三方工具：[用于开发企业级 Power BI 和 Analysis Services 模型的社区和第三方工具](https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft 的 Power BI 实施规划文档在高级数据建模场景与企业级开发中明确提到 Tabular Editor：[Power BI 使用场景：高级 Data model 管理](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## 信任中心

At Tabular Editor, we are committed to transparency and strong security practices. Visit our [Trust Center](https://trust.tabulareditor.com/) to find details about our SOC 2 audit report, key policy documents, license terms, and our approach to infrastructure and organizational security. You’ll also find information about our sub-processors and how we work to keep your data safe.

## 元数据与数据隐私

Tabular Editor 主要是一款离线工具，这意味着所有数据和元数据都保存在安装了 Tabular Editor 的本机上，所有用户交互也都在本地完成。 An Internet connection is not required to run and use Tabular Editor.

不过，在某些场景下，Tabular Editor 会出于不同目的连接到远程服务。 These are described in the following:

### Analysis Services XMLA 协议

与 Analysis Services 实例或 Power BI Premium Workspace 的所有通信，都通过 [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) 客户端库进行；更具体地说，是通过 [AMO 的 Tabular Object Model (TOM) 扩展](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions)。 These client libraries are provided by Microsoft for redistribution in 3rd party applications such as Tabular Editor. For licensing details, please refer to the [AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989).

当 Tabular Editor 连接到 Analysis Services 实例（本地网络或云端）或 Power BI Premium Workspace（云端）时，会通过上述客户端库建立连接。 By design, the AMO library handles the authentication and authorization of the user. Only users with administrative privileges on the Analysis Services instance or Power BI Premium workspace, are allowed to connect. This is no different than when using Microsoft tools such as SQL Server Management Studio or SQL Server Data Tools (which use the same client libraries for connectivity).

### Tabular Object Model 元数据

Once the AMO/TOM client library establishes connection, Tabular Editor will request the full Tabular Object Model (TOM) metadata for the specific Analysis Services database or Power BI dataset that the user wants to connect to. The AMO/TOM client library then serves this metadata to the client application (Tabular Editor) in a programmatic approach, allowing the application to apply metadata changes, such as renaming an object, adding a description, modifying a DAX expression, etc. In addition, the AMO/TOM client library provides methods for serializing the TOM metadata into a JSON-based format. Tabular Editor uses this technique to allow users to save the model metadata as a local JSON file, for purposes of version control of the data model structure. **Note: The JSON file produced this way contains no actual data records. The file contains only model metadata, that is, information about the structure of the model in terms of tables, columns, measures, DAX expressions, etc.** While model metadata is generally not considered confidential information, it is the responsibility of the user of Tabular Editor to handle any file produced this way with the required confidentiality (i.e. not sharing the file with 3rd parties, etc.).

**除非用户明确发起相关操作，否则 Tabular Editor 不会收集、发布、共享、传输或以其他方式公开通过 AMO/TOM 客户端库获取的任何模型元数据**（例如，将模型元数据 JSON 文件保存到共享网络位置，或将模型元数据部署到另一个 Analysis Services 实例或 Power BI Workspace）。

### 模型数据内容

下文中，“模型数据”指存储在 Analysis Services 数据库或 Power BI Dataset 中的实际数据记录。 Depending on the source database or dataset, it is very likely that the model data is confidential.

Because of the requirement for a user to have administrative privileges on the instance of Analysis Services or Power BI workspace that they are connecting to, the user will, by definition, also have access to all data content of the Analysis Services database or Power BI dataset. Tabular Editor only allows retrieval of data through the AMO client library mentioned above. Tabular Editor 3 provides features for browsing and querying model data. Regardless of which technique is used to access the data **Tabular Editor only stores retrieved data in local memory. Tabular Editor does not collect, publish, share, transfer or otherwise make public any model data obtained through the tool**. If a user chooses to copy or export query results obtained through Tabular Editor, it is their responsibility to treat the copied or exported data according to the confidentiality of the data. This is no different than a user connecting to the Analysis Services database or Power BI dataset using client tools such as Excel or Power BI, in which case they will also have the option to copy query results.

### AI 助手

Tabular Editor 3 includes an AI Assistant for chat-based semantic model development. From 3.27.0 it is part of a default installation; before that it had to be selected deliberately. If the component is not installed, no AI-related code is present on the machine and none of the behavior described in this section applies.

The AI Assistant uses a **bring-your-own-key** model. You provide an API key from a supported AI provider (OpenAI, Anthropic, Azure OpenAI or any OpenAI-compatible endpoint). No built-in API key is included and Tabular Editor does not provide or intermediate any AI service.

**数据流。** AI 助手与 AI 提供商之间的所有通信都在客户端计算机与提供商 API 之间直接进行。 No data passes through Tabular Editor servers. What is sent depends on what you ask for, and is bounded by five permission resources, each carrying one access level:

| Resource   | What it covers                                                                                                                        | 级别                  | 默认值   |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ----- |
| 模型元数据      | Table, column and measure names, expressions, descriptions and similar. Read also covers VertiPaq Analyzer statistics | Deny / Read / Write | Read  |
| Model data | Data values from your model, such as DAX query results. Requires a live connection                                    | Deny / Read         | Deny  |
| 最佳实践分析器    | Read lists rules and runs the analysis; Write adds or modifies rules                                                                  | Deny / Read / Write | Read  |
| Documents  | Your open C# script and DAX query editors. Read is their contents; Write is needed to create or modify them           | Deny / Read / Write | Write |
| 宏          | Your macro library                                                                                                                    | Deny / Read / Write | Write |

Write covers Read. Model data is denied by default, because metadata describes a model where data values are the model's contents.

**Permission management.** The grants are standing settings rather than per-request prompts. Review and change them under **Tools > Preferences > AI Features > Permissions**, or in the **Tools > MCP Server...** dialog, which edits the same record. Where the chat needs something a grant does not cover, it shows a permission card at that moment, and you answer for the turn, the session, the current model or always. **Always allow** raises the standing grant and never lowers one. Global grants are stored in the local Preferences.json file; grants given for a single model are stored in that model's user options (.tmuo) file and apply to the chat only. Setting a resource back to **Deny** makes the chat ask again.

**Administrator ceilings.** In the Enterprise, Consultancy and Trial editions, an administrator can cap each resource by [policy](xref:policies), separately for the chat and for the MCP server, and the MCP cap can only be lower. A cap outranks every grant, including one a user has already given, and the corresponding option is shown read-only. These policies fail closed: if any Enterprise-tier policy value is present on a machine that is not licensed for it, the AI Assistant and the MCP server refuse to start rather than ignoring the policy.

**Audit record.** Tabular Editor 3 writes a local record of what the AI Assistant and the MCP server did: which permissions were requested and how they were answered, which tools ran and whether each succeeded, failed or was refused, and the full text of any C# script an agent ran or handed over for review. Prompts, replies and data values are not recorded. The daily files are kept for 30 days, and **Open audit folder** under **Tools > Preferences > AI Features** opens them. Administrators can redirect the location and change the retention period.

**API 密钥存储。** API 密钥会以加密方式存储在本地计算机的偏好文件 Preferences.json 中。 If the AI module is not loaded (for example because it was excluded during installation or disabled by policy), any previously stored API key configuration is cleared automatically.

**对话存储。** 对话会存储在客户端本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中。 No conversation data is sent to Tabular Editor servers.

**Disabling the AI Assistant.** You can exclude the AI features component during installation, clear the provider under **Tools > Preferences > AI Features > AI Assistant**, or enforce a [policy](xref:policies) through the Windows registry: `DisableAi` turns off all AI functionality including the MCP server and clears stored provider configuration, while `DisableAiChat` turns off the chat alone and leaves the MCP server running.

**Penetration testing.** A separate penetration test of the AI Assistant has been performed. The report is available in our [Trust Center](https://trust.tabulareditor.com/).

### MCP server

Tabular Editor 3 can act as an MCP (Model Context Protocol) server, so that an AI agent running on the same machine can work on the model you have open. See @mcp-server for the feature itself.

**Network exposure.** The server is an HTTP listener bound explicitly to `127.0.0.1`, by default on port 42100. It is not reachable from another machine. Browser requests carrying a non-local `Origin` header are rejected as a defense against DNS rebinding. The server runs only after you start it, or from application start if you have asked for that.

**Authentication.** Loopback binding is the default boundary, so the server accepts local connections without credentials out of the box. On a host where several people are signed in at once, such as a Remote Desktop or Citrix server, that is not sufficient: any session on the machine reaches `127.0.0.1`. While the token is off, any process on the machine can connect without credentials. Turn on **Require access token** under **Tools > Preferences > AI Features > MCP Server**, and clients must present a bearer token, which is stored encrypted in the local Preferences.json file. Administrators can enforce this with the `RequireMcpAccessToken` [policy](xref:policies).

**Data flow.** Tabular Editor does not contact an AI provider for this feature and holds no API key for it. The agent is the only party that talks to a provider, under its own configuration and its own subscription. What the agent can read from the model is bounded by the same five permission grants that govern the AI Assistant, snapshotted when the server starts, and any tool a grant does not cover is never offered to the agent. Model data is denied by default, so no data values leave the model unless you grant that explicitly.

**Changes to the model.** An agent changes the model only through the C# scripting engine, atomically and as a single undo step, and only with the model metadata grant at Write. Raw TMSL and XMLA execution is never available to an agent, and a script that reaches outside the model is never executed for it.

**Audit record.** Permission decisions, tool calls and the full text of any C# script an agent ran or handed over for review are written to a local audit log. Prompts, replies and data values are not recorded.

**Disabling the MCP server.** Clear **Enable MCP Server** under **Tools > Preferences > AI Features > MCP Server**, or enforce the `DisableMcpServer` or `DisableAi` [policy](xref:policies). The server is part of the AI features component, so excluding that component at install time removes it as well.

### Web 请求

Tabular Editor 仅会在以下情况下向在线资源（Web URL）发起请求：

- **License activation\*.** When Tabular Editor 3 is first launched, and at periodic intervals thereafter, the tool may perform a request to our licensing service. This request contains encrypted information about the license key entered by the user, the e-mail address of the user (if provided), the local machine name and a one-way encoded hash identifying the current installation. No other data is transmitted in this request. The purpose of this request, is to activate and validate the license key used by the installation, enforce trial limitations, as well as allowing the user to manage their installations of Tabular Editor 3 through our licensing service.
- **升级检查\*.** 每次启动 Tabular Editor 3 时，它可能会向我们的应用服务发起请求，以确定是否有可用的新版 Tabular Editor 3。 This request does not contain any data.
- **Usage telemetry\*.** By default, Tabular Editor 3 collects and transmits anonymous usage data as users interact with the tool. This data includes information about which UI objects a user interacts with and the timing of each. It also contains high-level information about the Tabular data model being edited through the tool. This information only relates to high-level properties like compatibility level and mode, number of tables, type of server (Analysis Services vs. Power BI vs. Power BI Desktop), etc. **No personally identifiable data is collected this way**, neither do we collect any information about names of objects or DAX expressions in the Tabular Object Model itself. A user may opt out of sending telemetry data to us at any point.
- **错误 Report\*.** 当发生意外错误时，我们会传输堆栈跟踪和（已匿名化的）错误信息，并附带你提供的可选说明。 If a user opts out of sending telemetry data, error reports will also not be sent.
- **使用 DAX 格式化器。**（仅限 Tabular Editor 2.x）你可以在 Tabular Editor 中点击按钮来格式化 DAX 表达式。 In this case, the DAX expression (and nothing else) is sent to the www.daxformatter.com webservice. The first time a user clicks this button, an explicit warning message is shown, asking them to confirm their intent. Tabular Editor 3 does not perform web requests when formatting DAX code.
- **DAX Optimizer**. If a user has a [Tabular Tools account](https://tabulartools.com) with a [DAX Optimizer](https://daxoptimizer.com) subscription, they will be able to browse their DAX Optimizer workspace, view issues and suggestions, and upload new VPAX files directly from within Tabular Editor 3. VPAX files contains model metadata and statistics, but no actual model _data_. The DAX Optimizer Integration feature in Tabular Editor 3 causes various requests to one or more of the below endpoints (depending on authentication type and region specified when the Tabular Tools account was created).<br/>
  For more information, please consult the [DAX Optimizer documentation](https://docs.daxoptimizer.com/legal/data-processing).<br/>
  Endpoints used:
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **AI 助手。** 当 AI 助手已完成配置并在使用时，Tabular Editor 3 会将请求直接发送到所配置的 AI 提供商 API。 The endpoints depend on the selected provider (for example `https://api.openai.com` for OpenAI, `https://api.anthropic.com` for Anthropic, or a user-specified endpoint for Azure OpenAI and custom providers). Only data covered by the permission grants is included in these requests. See the [AI Assistant](#ai-assistant) section above for the resources and their defaults.
- **AI knowledge base updates.** The knowledge base the AI Assistant searches is a local database that ships with the AI features component. Tabular Editor 3 checks for a newer copy and downloads it from `https://cdn.tabulareditor.com`. The request carries no data about you or your model.
- **MCP server.** The MCP server makes no outbound requests. It accepts connections on the loopback interface only, and the agent that connects to it is what talks to an AI provider, under its own configuration. See the [MCP server](#mcp-server) section above.
- **导入最佳实践规则。** Tabular Editor 提供一项功能，让你可以指定一个 URL，从中获取以 JSON 格式提供的最佳实践规则列表。 This type of request only downloads the JSON data from the URL - no data is transmitted to the URL.
- **Using C# scripts.** Tabular Editor allows users to write and execute code written in C#, for purposes of automation. Such a script may potentially connect to online resources, using C# language features and the .NET runtime. The user is always responsible for ensuring that executed code does not cause any unintended sharing of data. Tabular Editor ApS cannot be held liable for any damages, losses or leaks caused by the use of the C# scripting feature in general. Tabular Editor will never execute C# scripts without the explicit action of the user.

\***我们通过许可证激活服务、使用情况遥测或错误 Report 获得的任何信息，都会予以保密。 We will not share, publish or distribute the data collected in any way, shape or form.**

**防火墙允许列表 / 接受列表**
如需允许上述 Web 请求的流量，请将以下地址加入允许列表：

- 许可证激活 / 升级检查：**https://api.tabulareditor.com**
- 使用情况遥测 / 错误 Report：**https://\*.in.applicationinsights.azure.com**
- DAX Formatter（仅 Tabular Editor 2.x）：**https://www.daxformatter.com**
- 导入最佳实践规则 / C# Script：视具体情况而定
- DAX优化器：端点见上文列表。
- AI 助手：取决于所配置的提供商（例如 \*\*https://api.openai.com\*\*、\*\*https://api.anthropic.com\*\*，或你指定的 Azure OpenAI / 自定义端点）
- AI knowledge base updates: **https://cdn.tabulareditor.com**
- MCP server: nothing. It listens on **127.0.0.1** and makes no outbound requests

> [!NOTE]
> 系统管理员可能会强制执行某些[策略](xref:policies)，用来禁用上面列表中的部分或全部功能。

## 应用程序安全

Tabular Editor 安装在 Windows 电脑上时不需要任何提升权限，也不会访问这台电脑上的任何受限资源。 One exception from this rule, is if using the Tabular Editor installer file (.msi), in which case the executable and support files required by the tool, are by default copied to the `Program Files` folder, which typically requires elevated permission. Both the Tabular Editor binary files as well as the installer file, have been signed with a code signing certificate issued to Kapacity A/S, which is your guarantee that the code has not been tampered with by any 3rd party.

应用程序运行时，所有对外部资源的访问都通过 AMO/TOM 客户端库或上面提到的 Web 请求完成。

C# Script 功能允许 Tabular Editor 在 .NET 运行时中执行任意 C# 代码。 Such code is only compiled and executed on the explicit request of the user. C# scripts may also be saved as "macros", which makes it easier for the user to manage and execute multiple different scripts. The code is stored to the users own `%localappdata%` folder, ensuring that only they or a local machine administrator, can access the scripts. The user is always responsible for ensuring that executed code does not cause any unintended sideeffects. Under no circumstance can Tabular Editor ApS be held liable for any damages, losses or leaks caused by the use of the C# scripting or custom actions/macros features.

Organizations that do not want this left to the individual user can govern it centrally. The `DisableCSharpScripts` and `DisableMacros` [policies](xref:policies) turn the features off entirely, in every edition. With Tabular Editor 3 Enterprise Edition, `BlockUnsafeScripts` keeps scripting available but allows only scripts and macros that stay within the semantic model: anything that reads or writes a file, reaches the network, starts another program or loads outside code is refused before it runs, wherever the script came from - a script document, the Best Practice Analyzer, a macro, the AI Assistant, the MCP server or the command line. See [Administrator policies](xref:csharp-scripts#administrator-policies).
