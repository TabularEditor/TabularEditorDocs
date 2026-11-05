---
uid: ai-assistant
title: AI 助手
author: Morten Lønskov
updated: 2026-10-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.26.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# AI 助手

AI 助手是一个用于语义模型开发的聊天面板。它会探索您的模型元数据、编写并运行 DAX 查询、生成 C# 脚本、解释并修复您的模型和已打开文档中的错误、运行 Best Practice Analyzer 检查、查询 VertiPaq Analyzer 统计数据并搜索 Tabular Editor 知识库。[权限设置](#permissions-and-consent)控制它向您的 AI 提供商发送的内容。AI 助手已通过独立渗透测试；请参阅[Tabular Editor 信任中心](https://trust.tabulareditor.com)。

AI 助手采用“自带密钥”模式，即您提供来自受支持提供商之一的 API 密钥，助手直接针对该提供商的 API 运行。

您还可以通过 [MCP 服务器](xref:mcp-server)使用自己的代理，无需 API 密钥。Claude Code、GitHub Copilot、VS Code 代理模式、Codex 或 Cursor 等代理在开放模型上使用与聊天相同的工具和权限设置，但会话和每个模型的授权除外，这些授权仅适用于聊天。请参阅[MCP 服务器和 AI 助手的区别](#mcp-server-and-ai-assistant-differences)。



![首次打开的“AI 助手”窗格，助手的问候语列出了它能做什么（回答问题、查询模型、编写和执行 C# 脚本、更改模型）以及它不能做什么，下方是一个空的消息框](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 开始使用

1. 打开**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**
2. 选择您的 AI 提供商（在新安装时，此项默认为**无（AI 已禁用）**），然后输入您的 API 密钥
3. 从**视图 > AI 助手**打开 AI 助手面板
4. 输入消息并按 **Enter** 键开始对话

> [!TIP]
> [AI 助手的交互式演示](https://demos.tabulareditor.com/psl/of150vcy?)介绍了设置和使用方法。

> [!NOTE]
> API 密钥以加密形式存储在您的本地计算机上。

## 支持的提供商

在**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**下配置您的 AI 提供商。从下拉列表中选择一个提供商（在您配置提供商之前，默认值为**无（AI 已禁用）**），输入您的 API 密钥，并可选择覆盖默认模型。

将模型字段留空以使用提供商的默认模型。OpenAI 和 Anthropic 有默认值；Azure OpenAI 和自定义提供程序始终需要一个值。

| 提供商 | 默认模型 | 需要的配置 |
| -- | -- | -- |
| OpenAI | gpt-5.5 | API 密钥。可选的基本URL、组织ID和项目ID |
| Anthropic | claude-sonnet-4-6 | API 密钥。可选基本URL |
| Azure OpenAI | 无。需要部署名称 | API 密钥、端点 URL 和部署名称 |
| 自定义（兼容 OpenAI） | 无。需要模型名称 | API 密钥和自定义端点 URL |

![AI 提供商首选项页面，其中“选择提供商”下拉菜单显示为“无”（AI 已禁用）、OpenAI、Anthropic、Azure OpenAI 和自定义（兼容 OpenAI），下方有 URL 和 API 密钥字段](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### 选择模型

活动模型显示在信息框上方的状态条中，位于上下文使用情况条旁边。点击它即可打开一个选择器，其中列出了已配置提供商的可用模型；您选择的模型将从下一个请求开始应用。最后一个条目**首选项……**将打开**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**，用于处理不在列表中的任何内容。对于 Azure OpenAI 和自定义提供商，或者在检索模型列表之前，模型名称是一个链接，可打开这些首选项。

![模型选择器在消息框上方打开，列出了 claude-sonnet-5、claude-fable-5-1、claude-fable-5、claude-opus-5、claude-haiku-4-5、claude-opus-4-8 和以粗体显示的当前模型 claude-sonnet-4-6，分隔线下方是“首选项…”](~/content/assets/images/ai-assistant/ui-model-picker.png)

> [!NOTE]
> 在设置提供商、API密钥和模型之前，模型指示器处于隐藏状态。

### OpenAI

选择 **OpenAI** 作为提供商，然后输入您的 API 密钥。如果您的 OpenAI 账户使用组织 ID 或项目 ID，也请输入这些 ID。模型名称可为您的帐户上提供的任何模型。

![早期版本的 AI 提供商首选项页面，已选择 OpenAI，API 密钥已遮挡，组织 ID 和项目 ID 字段为空，模型名称为 gpt-4o](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择**Anthropic**作为提供商，然后输入您的 API 密钥。模型名称可为您的账户上可用的任何 Anthropic 模型。

![“AI 提供商”首选项页面，其中选择了 Anthropic 作为提供商，基础 URL 为 https://api.anthropic.com，API 密钥已遮挡，模型名称为 claude-sonnet-4-6](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 根据您的账户等级实施每分钟输入令牌数 (ITPM) 的速率限制。对于 Claude Sonnet 4.x，新的 API 密钥从 1 级开始，ITPM 为 30,000。针对大型模型的单个请求可能会超过此限制。购买 $40 或以上的 API 额度即可达到 2 级（450,000 ITPM）。有关完整等级详细信息，请参阅[Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits )。

### Azure OpenAI

选择**Azure OpenAI**作为提供商，并配置以下字段：

- **API 密钥**：您的 Azure OpenAI 资源的访问密钥
- **服务端点**：资源URL，例如`https://your-resource.openai.azure.com`。SSL 证书是为 `*.openai.azure.com` 颁发的，因此 `*.privatelink.openai.azure.com` 地址无法通过证书验证
- **部署**：显示在**部署**的**名称**列中的部署名称

Azure OpenAI 要求在每次 API 调用中提供部署名称。名称在创建部署时设置，通常与它所服务的模型相匹配，例如 `gpt-4o`，但也有可能不同。如果您输入的资源名称或模型名称不存在于部署中，则请求将失败。

在 [Azure AI Foundry 门户](https://ai.azure.com)中查找部署名称：

1. 登录并选择您的 Azure OpenAI 资源
2. 打开**部署**（如果资源已升级到 Foundry，则打开**模型 + 端点**）
3. 复制**名称**列中的值

如果您的组织采用 Azure AI Foundry 之前创建的部署未显示在门户中，请使用 Azure CLI 列出部署：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

请参阅[创建和部署 Azure OpenAI 资源](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model)。

对于 403 错误、SSL 故障或“DeploymentNotFound”响应，请参阅@azure-openai-connection-errors。对于在 Microsoft Foundry 中部署的模型，请参阅[使用 Microsoft Foundry](#using-microsoft-foundry)。

### 自定义（兼容 OpenAI）

自定义提供程序可连接到任何公开 OpenAI 兼容 API 端点的 LLM，例如您自己计算机上的模型或托管在您组织网络上的模型。输入您的 API 密钥和端点 URL。使用自托管模型，所有数据都将保留在您自己的基础设施中，不会将任何数据发送到第三方云提供商。请参阅[使用本地或组织 LLM](#using-a-local-or-organizational-llm)。

## 使用本地或组织 LLM

您可以使用自定义提供程序，针对自托管 LLM 运行 AI 助手。这样，所有数据都将保留在您自己的基础设施中，无论是在您的本地计算机上运行的模型，还是在您组织的网络中集中托管的 LLM。无论哪种方式，都不会将数据发送到第三方云提供商。
这些工具在开发人员的工作站或用作团队端点的共享服务器上托管具有OpenAI兼容API的模型：

- [Ollama](https://ollama.com)：用于在本地下载和运行模型的轻量级 CLI
- [LM Studio](https://lmstudio.ai)：具有图形界面的桌面应用程序，用于管理和运行本地模型
- [LocalAI](https://localai.io)：自托管、社区驱动的替代方案，支持广泛的模型

### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取模型，例如 `ollama pull llama3.1`
3. 启动 Ollama 服务器。安装后会自动启动，默认端口为 11434
4. 在 Tabular Editor 中，转到**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**
5. 将**选择提供商**设置为**自定义（兼容 OpenAI）**
6. 将**服务终结点**设置为 `http://localhost:11434/v1`
7. 将**模型名称**设置为您拉取的模型，例如 `llama3.1`
8. 将**API 密钥**设置为任何非空值，例如 `ollama`。Ollama 不需要身份验证，但该字段不能为空

### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 从左侧面板的模型搜索页面下载模型，或使用 CLI 下载模型，例如 `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 从左侧面板中的开发人员页面启动 LM Studio 服务器，或使用 `lms server start` 启动。开启兼容 OpenAI 的模式。如果上下文大小低于 100,000 个 token，请将其提高到 100,000 个以上
4. 在 Tabular Editor 中，转到**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**
5. 将**选择提供商**设置为**自定义（兼容 OpenAI）**
6. 将**服务终结点**设置为 `http://localhost:1234/v1`
7. 将**模型名称**设置为您下载的模型，例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
8. 将**API 密钥**设置为任何非空值，例如 `lms`。LM Studio 不需要身份验证，但该字段不能为空


> [!NOTE]
> 使用本地模型的回复质量取决于模型大小和您的硬件。较大的模型能提供更好的结果，但需要更多的 RAM 和性能更强的 GPU。AI 助手的工具调用需要一个支持以 OpenAI 兼容格式进行函数调用的模型。

> [!TIP]
> 使用参数至少为 300 亿的模型，最好为 1000 亿或更多。Qwen3.5-122B-A10B 在内部测试中表现良好。

## 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com)（前身为 Azure AI Foundry）在您的 Azure 环境中部署 OpenAI 和 Anthropic 模型。在 Tabular Editor 中使用 **OpenAI** 或 **Anthropic** 提供商连接到这些模型。

> [!IMPORTANT]
> 请勿对 Microsoft Foundry 模型使用 **Azure OpenAI** 提供程序。它仅适用于使用 `api-version` 查询参数的经典 Azure OpenAI 资源。

### Microsoft Foundry 上的 OpenAI 模型

配置部署在 Microsoft Foundry 中的 OpenAI 模型，例如 GPT-4o 或 GPT-5.4-mini：

1. 在 Tabular Editor 中，转到**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**
2. 将**选择提供程序**设置为**OpenAI**
3. 将**基础 URL**设置为您的 Foundry 资源端点，并附加`/openai/v1`，格式如下所示：
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. 输入您的 Foundry **API 密钥**
5. 将**模型名称**设置为您的部署名称，例如`gpt-5.4-mini`

> [!NOTE]
> Microsoft Foundry 门户不显示基础 URL。它显示的是包含完整 API 路径的**目标 URI**，例如 `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`。对于基础 URL，仅使用`https://your-resource.services.ai.azure.com/openai/v1`。

### Microsoft Foundry 上的 Anthropic 模型

对于部署在 Microsoft Foundry 中的 Anthropic 模型，例如 Claude Sonnet 4.6：

1. 在 Tabular Editor 中，转到**工具 > 首选项 > AI 功能 > AI 助手 > AI 提供商**
2. 将**选择提供程序**设置为**Anthropic**
3. 将**基础 URL** 设置为您的 Foundry 资源端点，并附加 `/anthropic`，例如 `https://your-resource.services.ai.azure.com/anthropic`
4. 输入您的 Foundry **API 密钥**
5. 将**模型名称**设置为模型标识符，例如 `claude-sonnet-4-6`

> [!NOTE]
> 门户显示**目标 URI**，例如 `https://your-resource.services.ai.azure.com/anthropic/v1/messages`。对于基准 URL，请使用截至并包含`/anthropic`的部分。

## 功能

在您的[权限授予](#permissions-and-consent)范围内，AI 助手会使用您的模型上下文：

- **模型探索**：查询模型元数据，包括表、列、度量值、关系及其属性
- **DAX 查询编写**：生成 DAX 查询，对照您连接的模型运行这些查询，并在聊天中返回结果集
- **C# 脚本生成**：为模型更改创建 C# 脚本。根据您的设置，助手会在编辑器窗口中打开脚本供您运行，或者自行运行脚本；请参阅[让助手更改您的模型](#letting-the-assistant-change-your-model)
- **Best Practice Analyzer**：运行 BPA 分析，列出规则违规情况，并创建或修改 BPA 规则
- **VertiPaq Analyzer**：查询内存使用情况统计数据和列基数
- **模型错误**：列出模型的错误、警告和 Analysis Services 消息，与[消息视图](xref:messages-view)中显示的消息相同，并首先列出根本原因。当模型的错误发生变化时，助手会收到通知。
- **文档访问**：读取和修改打开的 DAX 查询、C# 脚本和 DAX 脚本，并读取每个打开的文档（包括 Pivot Grid）的错误和警告。活动文档是助手的上下文的一部分，因此您可以询问“为什么我在此查询中看到此错误？”。它无法读取或更改 Pivot Grid 的布局
- **知识库搜索**：搜索嵌入的 Tabular Editor 文档
- **UI 导航**：生成 `te3://` 操作链接，用于打开特定的 Tabular Editor 对话框和功能

通过 [MCP 服务器](xref:mcp-server)连接的代理具有相同的功能，但 UI 导航除外。两者都通过将 C# 脚本作为单个不可撤消的步骤来运行，从而更改您的模型。它们在您如何查看更改和授予权限方面存在差异；请参阅[MCP 服务器和 AI 助手的差异](#mcp-server-and-ai-assistant-differences)。

> [!NOTE]
> 当模型从文件（例如 `.bim` 文件或 TMDL 文件夹）加载且未连接到 Analysis Services 或 Power BI 时，需要连接的工具（包括 DAX 查询执行和 VertiPaq Analyzer 统计信息）将被隐藏。助手仍会编写 DAX 查询，但在您连接之前，DAX 查询工件上的**执行**功能处于禁用状态。从 `.vpax` 文件加载的 VertiPaq分析器统计数据仍可用。

## 让助手更改您的模型

默认情况下，助手会编写一个 C# 脚本，并在编辑器窗口中打开该脚本，供您阅读和运行。当您在**工具 > 首选项 > AI 功能 > AI 助手 > 首选项**下选择**允许 AI 助手直接运行 C# 脚本**时，它也可以自行运行脚本。

该设置默认关闭，并且在**工具 > 首选项 > AI 功能 > 权限**下将**模型元数据**设置为**读/写**之前不可用。

### 助手运行脚本时会发生什么

- 如果**Preview changes**（预览更改）已启用（默认设置），则在应用更改之前会显示[预览对话框](xref:csharp-scripts#run-c-scripts-with-preview)。**取消**将撤消更改，并将拒绝情况报告给助手。如果**预览更改**已关闭，则会在不显示对话框的情况下应用更改。
- 脚本的更改是一个撤消条目，即**C# 脚本（AI 助手）**。焦点仍停留在聊天框中，在此处按 **Ctrl+Z** 不会撤消模型更改。要撤消整个脚本，请点击 TOM Explorer 并按 **Ctrl+Z**，或在**编辑**菜单中选择**撤消 C# 脚本（AI 助手）**。
- 如果脚本在执行过程中部分失败，模型将保持不变，并且助手会报告错误。
- 如果脚本成功执行并引入或解决了 DAX 错误，助手会收到这些错误的列表，并按根本原因分组。
- 访问文件、网络或外部程序集的脚本不会运行。它将作为带有“不安全”徽章且“执行”被禁用的脚本工件打开，助手的回复会说明脚本使用了什么。

如果您要求提供脚本，例如“为我编写一个将每个度量值重命名为句首大写形式的脚本”，即使启用了此设置，助手也会将其作为脚本文档打开，由您自行运行。

`DisableCSharpScripts` [策略](xref:policies)适用于每个版本，并同时禁用直接执行和助手交给您运行的脚本。

`BlockUnsafeScripts` 策略需要 Enterprise Edition，并适用于 Tabular Editor 中的每个脚本，包括通过 [MCP 服务器](xref:mcp-server)运行的脚本。设置此策略后，助手仍可以编写访问文件、网络或外部程序集的脚本，但该脚本不会运行，也不会打开任何项目以供审核。请参阅[管理员策略](xref:csharp-scripts#administrator-policies)。

## 对话

AI 助手支持多条同时进行的对话，每条对话都有自己的消息历史记录和上下文。

- 对话跨会话保留，并本地存储在 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 标题在第一次交流后自动生成，您可以重命名对话
- **自动压缩**：当对话接近上下文窗口的限制时，在对完整对话的快照进行存档后，系统会对较旧的消息进行摘要，以释放空间。阈值是模型自身上下文窗口的百分比，在[上下文压缩](#context-compaction)下设置

### 删除对话

**删除对话**位于 AI 助手工具栏的左端，紧挨着**新建对话**。确认提示后，对话及其历史记录将从磁盘中删除，且无法恢复。面板标题栏上的“关闭”按钮，或**“视图”>“AI 助手”**，可隐藏面板，但不会删除任何内容。

## 产物

AI 助手生成的代码会在编辑器窗口中以*工件*的形式打开：

- **C# 脚本**：具有语法高亮显示、编译和执行功能的 C# 脚本编辑器
- **DAX 查询**：具有语法突出显示和执行功能的 DAX 查询编辑器

随着 AI 生成工件，工件会陆续显示，C# 脚本工件包含安全分析，该分析会标记不安全的代码，例如文件系统访问或网络操作。

![“AI 助手”窗格显示生成的 C# 脚本工件，其中包含“执行”按钮，以及助手对脚本功能的解释和随附的大小写敏感性注意事项](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

如果**预览更改**已启用，从聊天中运行 C# 脚本将打开**脚本预览**对话框，其中并排显示脚本对模型元数据所做的所有更改的差异，您可以在其中接受或撤销这些更改。请参阅[运行带预览功能的脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![“脚本预览 - 模型变更”对话框，模型变更前后的内容并排显示，其中“Internet Total Freight”度量的格式字符串已更改，并添加了描述和显示文件夹，每个变更都与原始内容进行了对比标记](~/content/assets/images/preview-script-changes.png)

## 自定义指令

*自定义指令*是一组指令，用于指导 AI 助手执行特定任务。助手会收到所有可用指令的列表及其`description`，并仅加载与您的请求相关的指令的完整文本，因此请确保描述准确且具体。加载的指令在对话的其余部分中一直有效。

### 内置自定义指令

AI 助手包含以下自定义指令：

| 自定义指令 | 调用方式 | 涵盖内容 |
| -- | -- | -- |
| DAX 查询 | `/dax-querying` | 编写和执行 DAX 查询：列和度量值限定、验证筛选值、验证和更新查询 |
| 模型修改 | `/model-modification` | 用于创建或更改模型对象的 C# 脚本：TOMWrapper API 模式、执行顺序、幂等更新、命名规则 |
| 语义模型设计 | `/model-design` | 星型模式、关系和交叉筛选、日期表、度量值与计算列、计算组、命名 |
| 语义模型组织 | `/organize-model` | 审核和整理模型元数据：命名约定、表组、显示文件夹、隐藏列、格式字符串、描述 |
| 语义模型大小优化 | `/optimize-model` | 减少模型内存和大小：VertiPaq 测量、列删除、数据类型调整、结构更改、SKU 限制 |
| 宏 | `/macros` | 用于“宏”窗口的可重用 C# 宏：选择上下文、通用代码规则 |
| DAX 用户自定义函数 | `/udf` | 编写 DAX UDF：语法、`VAL`/`EXPR` 参数模式、类型提示、命名空间、DaxLib |
| Best Practice Analyzer | `/bpa` | 查看违规并以 LINQ Dynamic 表达式的形式编写自定义规则 |

在**工具 > 首选项 > AI 功能 > AI 助手 > 首选项**下选中**显示自定义指令指示器**后，每个回复上方的指示器将显示影响该回复的指令。

### 调用自定义指令

键入`/`以浏览可用的自定义指令。让您的消息以指令的`/id`开头，即可加载该指令，而无需考虑消息内容；例如，`/dax-querying`将加载DAX查询指令。没有消息的 `/id` 会加载指令，而不会发出请求。显式加载的指令在对话的其余部分中保持有效，就像助手自行加载的指令一样。

### 添加您自己的自定义指令

通过将 `.md` 文件放置在 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 中来创建自定义指令。该文件夹在 AI 助手首次运行时创建，其中包含一个 `example.md` 文件，可供您从中复制。点击 AI 助手工具栏上的**打开自定义指令文件夹**即可打开该文件夹。

定义指令元数据的 YAML 前置 मैटर是可选的：

```yaml
---
id: my-custom-instruction
name: My Custom Instruction
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
---

Your instruction content goes here. This is the text that will be
injected into the AI's system prompt when the instruction is activated.
```

| 字段 | 是否必填 | 默认值 | 说明 |
| -- | -- | -- | -- |
| `id` | 否 | 不带 `.md` 的文件名 | 唯一标识符，也用作显式调用的 `/id` |
| `name` | 否 | 首字母大写的 `id` | 自动补全中显示的名称 |
| `description` | 否 | 回退到 `name` | 说明该指令涵盖的内容以及何时适用 |
| `priority` | 否 | 100 | 当多条自定义指令生效时，值较高的指令将优先注入 |
| `always_inject` | 否 | false | 如果为 true，则始终包含在系统提示中。`/` 自动补全中不提供此类指令 |
| `hidden` | 否 | false | 如果为 true，则不显示在 `/command` 自动补全中 |

`id` 与内置指令匹配的自定义指令会覆盖内置版本。

Tabular Editor 按以下方式读取文件：

- 前置内容必须以`---`开头，位于文件的第一行，并以`---`行结尾。如果不是这样,或者如果无法解析 YAML,则整个文件将被视为指令内容,并且上述所有默认值均适用。
- 不在上述表格中的键将被忽略。仍有`triggers:`部分的早期版本文件将按原样加载
- 正文中的任何 `{{version}}` 都将替换为 Tabular Editor AI 组件的版本
- 仅读取直接位于该文件夹中的 `.md` 文件；不搜索子文件夹

### 来自您组织的自定义指令

管理员可以使用 `AiCustomInstructionsPath` [策略](xref:policies)为所有人发布一个自定义指令文件夹，该文件夹可以是只读网络共享。除了内置的指令外，这些指令还会为每个用户加载，并且工作方式与其他指令一样：在`/`自动补全中提供，按其描述选择，通过`/id`调用。

如果相同的 `id` 存在于多个位置，则优先级为：

1. 您所在组织的文件夹
2. 您自己的文件夹
3. 内置指令

一项单独的策略 `DisableUserCustomInstructions` 会使 Tabular Editor 忽略您自己文件夹中的指令，并禁用**打开自定义指令文件夹**；内置指令和组织指令仍会加载。这两项策略都需要 Tabular Editor 3 企业版。

## 权限和同意

为每个资源设置访问级别，以控制 AI 助手可以访问的内容，[MCP 服务器](xref:mcp-server)使用相同的设置。

| 资源 | 涵盖内容 | 级别 | 默认 |
| -- | -- | -- | -- |
| **模型元数据** | 表、列和度量值名称、表达式、描述等。“读”还包括 VertiPaq 分析器统计数据以及模型的错误和警告消息 | 拒绝/读/写 | **读** |
| **模型数据** | 来自您模型的数据值，例如 DAX 查询结果，以及 Analysis Services 返回的错误文本（其中可能包含数据值）。DAX 查询需要实时连接 | 拒绝/读取 | **拒绝** |
| **最佳实践分析器** | 读权限可读取规则列表并运行分析；写权限可添加或修改规则 | 拒绝/读/写 | **读** |
| **文档** | 您打开的文档：DAX 查询、C# 脚本、DAX 脚本和 Pivot Grid。“读”是指其内容及其错误和警告；“写”是指需要创建或修改它们。无法读取或修改 Pivot Grid 布局 | 拒绝/读取/写入 | **写入** |
| **宏** | 您的宏库。“读”可列出并读取宏；“写”保留供将来宏编辑工具使用 | 拒绝/读/写 | **写** |

**写**（在下拉菜单中标记为**读/写**）包括读。

> [!NOTE]
> 授予**模型数据**会将模型中的数据值发送给你的 AI 提供商。

某些授权依赖于其他授权：

- [直接执行](#letting-the-assistant-change-your-model)需要**模型元数据 > 写入**，您需要单独启用此项。
- 运行 Best Practice Analyzer 除了需要**Best Practice Analyzer > 读取**外，还需要**模型元数据 > 读取**。
- 运行 DAX 查询除了需要**模型数据 > 读取**外，还需要**模型元数据 > 读取**。查询可以通过 `INFO` 函数、DMV 及其结果中的列名来读取元数据。

### 设置权限授予

打开**工具 > 首选项 > AI 功能 > 权限**，其中每个资源都有一个下拉菜单，显示其可用级别。

![AI 功能 > 权限首选项，每个资源都有一个处于默认状态的下拉列表](~/content/assets/images/pref-ai-permissions.png)

聊天没有单独的“询问”级别，当需要将资源设置为**拒绝**时，会显示[权限卡](#permission-cards-in-the-chat)。

> [!NOTE]
> 从 3.27.0 开始，**模型元数据**、**文档**和**宏**的默认设置为“读取”或更高权限，聊天不再提示这些权限。默认情况下，只有 DAX 查询结果和 Best Practice Analyzer 规则编辑才会显示卡片。将资源设置为**拒绝**，以恢复其提示。

> [!NOTE]
> 在企业版中，管理员可以通过策略限制这些权限。请参阅@policies。

### 聊天中的权限卡片

当助手需要你的常设授权未涵盖的资源时，对话中会显示“需要权限”卡片。该卡片会说明助手想要执行的操作，例如“AI 希望访问你语义模型的元数据”，或者显示其提议运行的 DAX 查询。

![聊天中的“需要权限”卡片，其中列出了助手想要运行的 DAX 查询，并提供了“允许”、“允许用于会话”、“允许用于此模型”、“始终允许”和“拒绝”按钮](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| 按钮 | 功能 |
| -- | -- |
| **允许** | 仅适用于此轮。助手在完成您的任务时可以重复相同的请求，之后不会记住任何内容 |
| **仅在本次会话中允许** | 适用于 Tabular Editor 重新启动之前。授权保留在内存中，绝不会写入磁盘 |
| **允许用于此模型** | 记录在模型的[用户选项](xref:user-options)文件中，并在下次打开此模型时应用。仅适用于**模型元数据**和**模型数据**，并且仅在加载模型时适用 |
| **始终允许** | 在“权限”页面上提升永久授权，适用于每个模型和每个会话 |
| **拒绝** | 拒绝此请求。助手将在没有该访问权限的情况下继续运行，下次需要该权限时，卡片将再次出现 |

**始终允许**绝不会降低现有授权；允许在“写入”时对资源进行读取，则会将其保留在“写入”级别。

### 在权限待处理时停止回合

回合将暂停，直到您回复**需要权限**卡片。**停止**会在没有回答的情况下结束回合，移除卡片并将请求计为已拒绝。发送新消息以继续对话。

### MCP 服务器和 AI 助手的区别

[MCP 服务器](xref:mcp-server)使用相同的五项授权，但不显示权限卡片：

- 授权在服务器启动时读取，并一直有效，直到服务器停止，因此更改后的授权仅在您重启服务器后才会生效
- 仅适用全局授权。通过**允许用于此模型**或**允许用于会话**授予的权限仅适用于聊天
- 被拒绝的资源的工具不在代理的工具列表中

### 撤销权限

在“权限”页面上将资源重新设置为“拒绝”，以撤销其授权。然后，下次聊天需要该资源时，聊天将显示一个权限卡。

降低全局授权不会清除针对特定模型的授权。删除模型的 `.tmuo` 文件，或其中的 `Permissions` 条目，以撤销针对每个模型的授权。请参阅 @user-options。

### 审计记录

在企业版（包括咨询版和试用版许可证）中，Tabular Editor 会写入 AI 助手和[MCP 服务器](xref:mcp-server)活动的本地日志。它会记录：

- 请求了哪些权限以及您的回答
- 运行了哪些工具，以及每个工具是成功、失败还是被阻止
- 助手或 MCP 代理运行或提交运行的任何 C# 脚本的完整文本，包括运行时失败或被拒绝的脚本

您的提示、助手的回复以及来自您模型的数据值绝不会被记录。无法编译的脚本不会被保存，助手写入文档供您自行运行的脚本文本也不会被保存。**工具 > 首选项 > AI 功能**下的**打开审计文件夹**可打开日志文件夹。

如果没有企业版许可证，且在许可证激活之前，不会记录任何内容，不会创建任何文件夹，也不会显示该按钮。请参阅 @ai-audit-log，了解每条记录包含的内容、文件的存储位置以及重定向这些文件的策略。

## 偏好

在**工具 > 首选项 > AI 功能 > AI 助手 > 首选项**下配置 AI 助手的显示和行为选项。

### 聊天显示

| 首选项 | 默认值 | 描述 |
| -- | -- | -- |
| 显示所选内容上下文指示器 | 关闭 | 在聊天中显示当前所选的模型对象 |
| 显示自定义指令指示器 | 关闭 | 在助手的回复上方显示自定义指令指示器 |
| 显示知识库搜索指示器 | 关闭 | 显示搜索知识库时的进度 |

### 上下文压缩

| 首选项 | 默认 | 说明 |
| -- | -- | -- |
| 自动压缩 | 开 | 接近上下文限制时自动汇总较早的信息 |
| 自动压缩阈值 % | 80 | 触发自动压缩时模型自身上下文窗口的百分比。该字段接受 25 至 100。低于 50 的值按 50 处理，高于 90 的值按 90 处理 |

### C# Script

| 首选项 | 默认值 | 说明 |
| -- | -- | -- |
| 允许 AI 助手直接运行 C# 脚本 | 关闭 | 让助手自行运行其 C# 脚本。关闭时，助手会打开每个脚本，由您来运行。在**权限**下将**模型元数据**设置为**读/写**之前不可用，并且在 `DisableCSharpScripts` [策略](xref:policies)下完全不可用。请参阅[让助手更改您的模型](#letting-the-assistant-change-your-model) |
| 预览更改 | 开 | 从聊天中执行 AI 生成的 C# 脚本时，显示“预览更改”对话框 |

**启动时检查知识库更新**和**打开审核文件夹**按钮位于**AI 功能**页面上，在**AI 助手**上方，两者也适用于 MCP 服务器。请参阅@preferences。

![AI 助手首选项页面，三个聊天显示指示器均未选中（默认设置），“自动压缩”已选中，阈值为 80，“允许 AI 助手直接运行 C# 脚本”未选中，“预览更改”已选中](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token 使用情况

向 AI 助手发送的每条消息都会消耗输入令牌。单条消息的令牌成本取决于其包含的上下文：

- **系统提示和自定义指令**：随每条消息一起发送，通常为 5,000 至 15,000 个令牌，具体取决于哪些自定义指令处于活动状态
- **模型元数据**：通过工具调用分阶段检索。助手首先获取一个轻量级概览（表名和度量值名称、关系），然后按名称、描述或 DAX 表达式搜索相关对象，并仅检索问题所需的表或对象的完整详细信息。非常大的工具结果会被截断，并提供有关助手如何检索其余部分的指导

### 令牌计数器

令牌计数器位于消息框上方的状态条中，在[活动模型指示器](#choosing-a-model)旁边。该进度条以千个为单位显示已使用/总计的令牌数，并随着上下文的填充而显示为绿色、琥珀色或红色。数字前面的`±`表示尚无确切计数。

将鼠标悬停在计数器上，即可查看细目：

| 部分 | 涵盖内容 |
| -- | -- |
| **上一轮** | 最近一次交互的成本：新输入、从提供商的提示缓存中提供的token、写入缓存的token以及输出 |
| **此对话（已计费）** | 在对话中的每个请求中累积的相同四个数字，包括工具往返 |
| **上下文** | 当前在上下文窗口中的令牌数，与窗口的实际大小对比 |

例如，一行显示为`37,588 input + 131,744 cached · write 37,558 · output 2,866`。对于不支持提示缓存的提供商，将省略缓存部分；如果某个部分没有可报告的内容，则会省略该部分。

> [!TIP]
> 将**上一轮**与**此对话（已计费）**进行比较，查看单个问题的成本。在长时间的对话中，**“本次对话（已计费）”**数字较大，而旁边的**“上一轮”**数字较小，这是正常现象。

### 上下文窗口

上下文使用情况栏、自动压缩点和单个回复的最大长度使用所选模型的上下文窗口。例如，具有一百万个令牌窗口的模型将以一百万个令牌为基准进行衡量。如果模型的窗口未知（Azure OpenAI 或自定义部署名称，或从未检索过模型目录的计算机），Tabular Editor 将使用 200,000 个令牌。

### 减少 Token 使用量

在提出问题之前，请在**TOM Explorer**中选择特定对象。然后，助手将其上下文范围限定为所选对象，并且不会检索整个模型的元数据，这可以最大限度地减少令牌使用量和 API 成本。

减少 Token 使用量的其他方法：

- 针对特定表、度量值或列提出有针对性的问题。“为所有度量值设置显示文件夹”等模糊提示会使助手检索整个模型的元数据。像“为我选择的度量值设置显示文件夹”这样的具体提示会将上下文限制在当前选择范围内，使用的令牌要少得多。
- 切换主题时开始新的对话，以免历史记录过长
- 对于探索性问题，使用更小或更便宜的模型

## 局限性

- 需要您自己的 API 密钥；未内置 API 密钥
- 回答质量取决于您选择的提供商和模型
- AI 助手不能替代对 DAX 和语义模型设计基础知识的了解
- AI 助手无法访问外部文件或服务，也无法搜索网络
- AI 助手无法连接到外部 MCP 服务器以扩展其自身的工具。要将您自己的代理与 Tabular Editor 3 一起使用，请参阅 @mcp-server
- AI 助手无法连接到与聊天不同的模型。在 Tabular Editor 用户界面中更改模型连接
- AI 助手无法管理偏好设置

## 禁用 AI 助手

AI 助手是一个可选组件，从 Tabular Editor 3.27.0 开始默认安装。再次运行 Tabular Editor 3 安装程序，然后选择**修改**，以在现有安装中包含或排除该组件。升级将保留现有选择；请参阅[升级和 AI 功能组件](xref:installation-activation-basic#upgrades-and-the-ai-features-component)。在便携式版本中，从安装目录中删除 `TabularEditor3.AI.dll` 即可将其移除。

同一组件包含 MCP 服务器，因此排除该组件或删除 `TabularEditor3.AI.dll` 会同时移除两者。要仅关闭聊天功能，请保留该组件并设置 `DisableAiChat` 策略。

> [!NOTE]
> 无论是否安装该组件，系统管理员都可以使用 [`DisableAi` 策略](xref:policies)关闭 Tabular Editor 3 中的所有 AI 功能，包括 MCP 服务器。`DisableMcpServer` 仅关闭 MCP 服务器。请参阅 @policies。
