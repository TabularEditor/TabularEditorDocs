---
uid: ai-assistant
title: AI 助手
author: Morten Lønskov
updated: 2026-04-17
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

AI 助手是一个用于 AI 辅助语义模型开发的基于聊天的界面，旨在帮助你更快地创建语义模型。 它采用企业级设计，你可以完全控制发送给 AI 的内容，并内置同意管理功能，因此可以放心使用 AI 助手。 AI 助手已接受独立的安全渗透测试。 有关详细信息，请访问 [Tabular Editor 信任中心](https://trust.tabulareditor.com)。 它可以浏览你的模型元数据、编写并执行 DAX 查询、生成 C# Script、运行 Best Practice Analyzer 检查、查询 VertiPaq分析器统计信息，并搜索 Tabular Editor 知识库。

AI 助手采用自带密钥 BYOK 模式。 你只需提供某个受支持提供商的 API 密钥，助手就会直接调用该提供商的 API 运行。

> [!NOTE]
> AI 助手自 Tabular Editor 3.26.0 起进入公开预览。 我们会继续完善这项功能，欢迎你反馈使用体验。

![AI 助手首次打开时的面板](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 开始使用

1. 打开 **工具 > 偏好 > AI 助手**
2. 选择你的 AI 提供商——全新安装时默认为 **无（AI 已禁用）**——然后输入你的 API 密钥
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入信息后按 **Enter** 开始对话

> [!TIP]
> 使用我们的 [AI 助手交互式演示](https://demos.tabulareditor.com/psl/of150vcy?) 了解如何设置和使用它。

> [!NOTE]
> API 密钥会以加密形式存储在你的本机上。

## 支持的提供商

在 **工具 > 偏好 > AI 助手 > AI 提供商** 中配置你的 AI 提供商。 从下拉列表中选择一个提供商——在你完成配置之前，默认值为 **无（AI 已禁用）**——输入你的 API 密钥，并可按需覆盖默认模型。 对于 OpenAI 和 Anthropic，**模型名称** 字段是一个预先填充常见模型的可输入下拉框；你也可以手动输入自定义模型名称。

| 提供商            | 默认模型              | 所需配置项                          |
| -------------- | ----------------- | ------------------------------ |
| OpenAI         | gpt-4o            | API 密钥。 可选：基础 URL、组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6 | API 密钥。 可选的基础 URL              |
| Azure OpenAI   | 因部署而异             | API 密钥、端点 URL 和部署名称            |
| 自定义（兼容 OpenAI） | 用户指定              | API 密钥和自定义端点 URL               |

![AI 助手提供商偏好设置](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### OpenAI

选择 **OpenAI** 作为提供商，然后输入你的 API 密钥。 如果你的 OpenAI 账户使用这些 ID，你也可以选择填写 Organization ID 和 Project ID。 默认模型是 **gpt-4o**，但你可以将其更改为你的账户中可用的任何模型。

![AI 助手 OpenAI 配置](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供方，然后输入你的 API 密钥。 默认模型是 **claude-sonnet-4-6**。 你可以将模型名称更改为你账户中可用的任意 Anthropic 模型。

![AI 助手 Anthropic 配置](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行每分钟输入 token（ITPM）的速率限制。 新创建的 API 密钥从 Tier 1 起步，Claude Sonnet 4.x 的速率上限为 30,000 ITPM。 对大型模型发起的单次请求就可能超过这个限制。 购买 40 美元及以上的 API 额度，即可达到 Tier 2（450,000 ITPM）。 完整的层级信息请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

选择 **Azure OpenAI** 作为提供方，并配置以下三个字段：

- **API 密钥** — 你的 Azure OpenAI 资源的访问密钥
- **服务端点** — 你的资源的端点 URL，例如 `https://your-resource.openai.azure.com`。 使用资源 URL，而不要使用 `privatelink` 别名；SSL 证书是为 `*.openai.azure.com` 签发的，直接连接到 `*.privatelink.openai.azure.com` 会导致证书验证失败
- **模型名称** — 指 **部署名称**，不是底层模型名称，也不是资源名称

Azure OpenAI 要求在每次 API 调用中都提供部署名称。 部署名称是在创建部署时选定的，因此可以是任意字符串。 部署通常会以其提供的模型命名（例如 `gpt-4o`），但这只是约定，不是要求。 如果你输入资源名称，或输入未作为部署存在的原始模型名称，请求将会失败。

#### 查找部署名称

在 [Azure AI Foundry 门户](https://ai.azure.com) 中：

1. 登录并选择你的 Azure OpenAI 资源
2. 打开 **Deployments**（如果资源已升级到 Foundry，则为 **Models + endpoints**）
3. 复制 **Name** 列中的值

在你的组织采用 Azure AI Foundry 之前创建的部署，可能不会在门户中显示。 也可以通过 Azure CLI 列出部署：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

有关更多详细信息，请参阅 [创建并部署 Azure OpenAI 资源](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model)。

如果遇到 403 错误、SSL 失败或 "DeploymentNotFound" 响应，请参阅 @azure-openai-connection-errors。

> [!NOTE]
> **Azure OpenAI** 提供程序适用于使用 `api-version` 查询参数的经典 Azure OpenAI 资源。 如果你使用的是新的 **Microsoft Foundry**，请参阅下方的 [使用 Microsoft Foundry](#using-microsoft-foundry)。

### 自定义（兼容 OpenAI）

“自定义”提供程序选项支持本地或组织内部的 LLM，只要它们提供与 OpenAI 兼容的 API 端点。 输入你的 API 密钥和自定义端点 URL。 这样一来，出于数据隐私或合规要求，你可以将所有数据保留在自己的基础设施内。

### 使用本地或组织内部的 LLM

你可以通过“自定义”提供程序，让 AI 助手对接自托管 LLM。 这样可以将所有数据保留在你自己的基础设施内——无论是运行在本地计算机上的模型，还是在你所在组织网络中集中托管的 LLM。 无论采用哪种方式，都不会将数据发送到第三方云提供商。

有多种工具可以托管模型，并提供与 OpenAI 兼容的 API：

- [Ollama](https://ollama.com) —— 轻量级 CLI，用于在本地下载和运行模型
- [LM Studio](https://lmstudio.ai) —— 带图形界面的桌面应用，用于管理和运行本地模型
- [LocalAI](https://localai.io) —— 自托管、社区驱动的替代方案，支持广泛的模型

这些工具既可以运行在开发人员的工作站上供个人使用，也可以部署在组织内部的共享服务器上，为团队提供集中管理的 LLM 端点。

#### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取一个模型，例如：`ollama pull llama3.1`
3. 启动 Ollama 服务器（安装后会自动运行，默认使用端口 11434）
4. 在 Tabular Editor 中，依次选择 **工具 > 偏好 > AI 助手 > AI 提供程序**
5. 将 **选择提供程序** 设置为 **自定义（兼容 OpenAI）**
6. 将 **服务端点** 设置为 `http://localhost:11434/v1`
7. 将 **模型名称** 设置为你拉取的模型（例如 `llama3.1`）
8. **API 密钥** 字段可以设置为任何非空值（例如 `ollama`）——Ollama 不要求身份验证，但该字段不能为空

#### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 拉取一个模型。 可通过左侧面板的模型搜索页面或通过 CLI 完成。 例如：`lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 启动 LM Studio 服务器。 可通过左侧面板的开发者页面或通过 CLI 完成。 例如：`lms server start`
   注意：你需要将其配置为 OpenAI 兼容模式。 此外，你可能还需要将默认上下文大小调整到 100,000 token 以上。
4. 在 Tabular Editor 中，转到 **Tools > 偏好 > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`）
8. **API Key** 字段可设置为任意非空值（例如 `lms`）——LM Studio 不需要身份验证，但该字段不能为空

> [!NOTE]
> 本地模型的响应质量取决于模型大小和你的硬件。 更大的模型通常能产生更好的结果，但需要更多 RAM 和性能足够的 GPU。 AI 助手的工具调用功能需要模型支持 OpenAI 兼容格式的函数调用。

> [!TIP]
> 我们建议使用参数量 _至少_ 为 30 billion 的模型，理想情况下至少为 100 billion。 例如，Qwen3.5-122B-A10B 模型在我们的内部测试中表现良好。

### 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com)（前身为 Azure AI Foundry）可让你在 Azure 环境中部署 OpenAI 和 Anthropic 模型。 这些模型应通过 Tabular Editor 中的 **OpenAI** 或 **Anthropic** 提供程序访问，而不是 **Azure OpenAI** 提供程序；后者用于经典 Azure OpenAI 资源。

> [!IMPORTANT]
> 不要将 **Azure OpenAI** 提供程序用于 Microsoft Foundry 模型。 **Azure OpenAI** 提供程序仅兼容经典 Azure OpenAI 资源。

#### Microsoft Foundry 上的 OpenAI 模型

要使用部署在 Microsoft Foundry 中的 OpenAI 模型（如 GPT-4o 或 GPT-5.4-mini）：

1. 在 Tabular Editor 中，转到 **Tools > 偏好 > AI Assistant > AI Provider**
2. 将 **Choose provider** 设置为 **OpenAI**
3. 将 **Base URL** 设置为你的 Foundry 资源端点，并在末尾加上 `/openai/v1`。 URL 采用以下格式之一：
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. 输入 Foundry **API 密钥**
5. 将 **模型名称** 设置为部署名称（例如 `gpt-5.4-mini`）

> [!NOTE]
> 在 Microsoft Foundry 门户中不会直接显示基础 URL。 门户会显示一个包含完整 API 路径的 **目标 URI**（例如 `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`）。 基础 URL 请仅使用 `https://your-resource.services.ai.azure.com/openai/v1`。

#### Microsoft Foundry 上的 Anthropic 模型

若要使用在 Microsoft Foundry 中部署的 Anthropic 模型（例如 Claude Sonnet 4.6）：

1. 在 Tabular Editor 中，依次转到 **工具 > 偏好 > AI 助手 > AI 提供程序**
2. 将 **选择提供程序** 设置为 **Anthropic**
3. 将 **基础 URL** 设置为你的 Foundry 资源端点，并在末尾加上 `/anthropic`，例如 `https://your-resource.services.ai.azure.com/anthropic`
4. 输入 Foundry **API 密钥**
5. 将 **模型名称** 设置为模型标识符（例如 `claude-sonnet-4-6`）

> [!NOTE]
> 门户会显示一个 **目标 URI**，例如 `https://your-resource.services.ai.azure.com/anthropic/v1/messages`。 对于基础 URL，只使用到并包括 `/anthropic` 的部分。

## 功能

AI 助手可以访问你的模型上下文，并执行以下操作：

- **模型探索**：查询模型元数据，包括表、列、度量值、关系及其属性
- **DAX 查询编写**：生成 DAX 查询，并在连接模式下针对你已连接的模型执行这些查询，结果集会直接返回到聊天中
- **C# Script 生成**：创建用于修改模型的 C# Script，并在新的编辑器窗口中打开。 当你在聊天中单击 **执行** 时，默认会显示 [预览更改](xref:csharp-scripts#run-c-scripts-with-preview) 对话框，让你在接受更改前查看所有对模型元数据的更改。 你也可以在编辑器中打开该脚本，并通过脚本工具栏运行它，可选择使用或不使用预览。 模型元数据更改可使用 **Ctrl+Z** 撤销
- **Best Practice Analyzer**：运行 BPA 分析、查看规则违规项，并创建或修改 BPA 规则
- **VertiPaq分析器**：查询内存使用统计信息和列基数
- **文档访问**：读取并修改打开的文档，例如 DAX 脚本和 DAX 查询
- **知识库搜索**：搜索内置的 Tabular Editor 文档以查找答案
- **UI 导航**：生成 `te3://` 操作链接，用于打开 Tabular Editor 中特定的对话框和功能

> [!NOTE]
> 在处理未连接到 Analysis Services 或 Power BI 的模型文件(例如 `.bim` 文件或 `.tmdl` 文件夹)时，所有需要活动数据库连接的工具——包括 DAX 查询执行和 VertiPaq分析器统计信息——都会自动隐藏。 AI 助手仍会为你编写 DAX 查询，但在建立连接之前，DAX 查询工件上的 **执行** 按钮将保持禁用状态。 如果之前已从 `.vpax` 文件加载，VertiPaq分析器统计信息仍然可用。

## 对话

AI 助手支持同时进行多个对话。 每个对话都维护各自的信息历史记录和上下文。

- 对话会跨会话保留，并存储在本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 首次交互后会自动生成标题。 你可以手动重命名对话
- **自动压缩**：当对话接近上下文窗口限制（约 80%）时，会自动汇总较早的信息以释放空间。 在压缩前，会先归档完整对话的快照

## 工件

当 AI 助手生成代码时，会创建可直接在编辑器窗口中打开的 **工件**：

- **C# Script**：在新的 C# 脚本编辑器中打开，提供语法高亮、编译和执行支持
- **DAX 查询**：在新的 DAX 查询编辑器中打开，提供语法高亮和执行支持

这些工件会在 AI 生成过程中实时流式呈现。 C# Script 工件包含安全分析，可标记可能不安全的代码（例如文件系统访问或网络操作）。

![AI 助手生成 C# Script](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

当你从聊天中执行 C# Script 时，**脚本预览**对话框会并排显示该脚本对模型元数据所做全部更改的差异对比。 你可以接受这些更改，也可以将其还原。 详见 [使用预览运行脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![脚本预览 - 模型更改](~/content/assets/images/preview-script-changes.png)

## 自定义指令

自定义指令是一组指令，用于在特定任务中引导 AI 助手的行为。 它们会根据意图检测自动激活，也可以手动调用。

### 内置自定义指令

AI 助手内置以下自定义指令：

| 自定义指令  | 触发关键词               |
| ------ | ------------------- |
| DAX 查询 | DAX、查询、EVALUATE、度量值 |
| 模型修改   | 修改、更改、添加、更新、创建      |
| 模型设计   | 设计、架构、模式、最佳做法       |
| 整理模型   | 整理、清理、文件夹、重命名       |
| 优化模型   | 优化、性能、慢、速度          |
| 宏      | 宏、自动化、录制            |
| UDFs   | UDF、函数、用户定义         |
| BPA    | BPA、最佳做法、规则、违规      |

自定义指令会以指示器的形式显示在助手回复上方，用于表明哪些指令对该回复产生了影响。 你可以在 **偏好 > AI 助手 > 偏好 > 显示自定义指令指示器** 中切换是否显示该指示器。

### 调用自定义指令

输入 `/` 以浏览可用的自定义指令，或者在信息开头输入完整的 `/instruction-id`，以显式调用特定指令。 例如，`/dax-querying` 会强制使用 DAX 查询指令，无论信息内容如何。

### 添加自定义指令

将 `.md` 文件放入 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 即可创建自定义指令。 每个文件都需要包含 YAML frontmatter，用于定义指令元数据：

```yaml
---
id: my-custom-skill
name: My Custom Skill
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
triggers:
  keywords:
    - keyword1
    - keyword2
  patterns:
    - "\\bregex pattern\\b"
  context_required:
    - model_loaded
---

Your instruction content goes here. This is the text that will be
injected into the AI's system prompt when the instruction is activated.
```

| 字段                          | 必填 | 默认值                                                    | 说明                               |
| --------------------------- | -- | ------------------------------------------------------ | -------------------------------- |
| `id`                        | 否  | 不含 `.md` 的文件名                                          | 唯一标识符，也用作显式调用时的 `/id`            |
| `name`                      | 否  | 标题式大小写的 `id`                                           | 自动补全中显示的名称                       |
| `description`               | 否  | -                                                      | 显示在名称下方的简短说明                     |
| `priority`                  | 否  | 100                                                    | 当多个自定义指令匹配时，数值越高越会先被注入           |
| `always_inject`             | 否  | false                                                  | 如果为 true，则始终包含在系统提示中             |
| `hidden`                    | 否  | false                                                  | 若为 true，则不会在 `/command` 的自动补全中显示 |
| `triggers.keywords`         | 否  | [] | 激活该指令的词语（不区分大小写）                 |
| `triggers.patterns`         | 否  | [] | 用于复杂匹配的正则表达式模式                   |
| `triggers.context_required` | 否  | [] | 必须满足的条件（例如 `model_loaded`）       |

其 `id` 与内置指令相同的自定义指令，会覆盖内置版本。

## 同意

AI 助手会在把数据发送给 AI 提供方之前先征求你的同意。 同意的范围仅限于特定数据类型：

| 同意类别      | 描述                              |
| --------- | ------------------------------- |
| 查询数据      | DAX 查询结果和数据样本                   |
| 读取文档      | 读取已打开文档中的内容，例如 DAX 脚本和 DAX 查询   |
| 修改文档      | 修改已打开的文档                        |
| 模型元数据     | 表和列的架构、度量值定义及其他模型元数据            |
| 编辑 BPA 规则 | 创建或修改 Best Practice Analyzer 规则 |
| 读取宏       | 读取宏定义                           |

当 AI 助手首次需要访问某种数据类型时，会弹出授权对话框。 你可以选择授权的有效期限：

| 选项    | 适用范围                                                      |
| ----- | --------------------------------------------------------- |
| 仅本次   | 仅限单次请求                                                    |
| 本次会话  | 直到重新启动 Tabular Editor                                     |
| 针对此模型 | 保存在模型的用户选项 (.tmuo) 文件中 |
| 始终    | 全局偏好，在所有模型和会话中持续生效                                        |

![AI 助手同意对话框](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

### 管理同意设置

你可以在 **工具 > 偏好 > AI 助手 > AI 同意设置** 中查看并重置你的同意选择。 每个同意类别都会显示其当前状态。 点击 **重置** 可撤销“始终允许”的同意，并将其恢复为“需要时询问”。

![AI 助手同意设置](~/content/assets/images/ai-assistant/ai-assistant-consent-reset.png)

## 偏好

在 **工具 > 偏好 > AI 助手 > 偏好** 中配置 AI 助手的显示和行为选项。

### 聊天显示

| 偏好         | 默认   | 说明                  |
| ---------- | ---- | ------------------- |
| 显示选择上下文指示器 | true | 在聊天中显示当前选中的模型对象     |
| 显示自定义指令指示器 | true | 在助手回复上方显示“自定义指令”指示器 |
| 显示知识库搜索指示器 | true | 搜索知识库时显示进度          |

### 上下文压缩

| 偏好       | 默认值  | 说明                 |
| -------- | ---- | ------------------ |
| 自动压缩     | true | 在接近上下文上限时自动总结较早的信息 |
| 自动压缩阈值 % | 80   | 触发自动压缩的令牌使用百分比     |

### 知识库

| 偏好         | 默认值  | 说明                            |
| ---------- | ---- | ----------------------------- |
| 启动时检查知识库更新 | true | 在 Tabular Editor 启动时自动检查知识库更新 |

### C# Script

| 偏好   | 默认值  | 说明                                   |
| ---- | ---- | ------------------------------------ |
| 预览更改 | true | 执行聊天中 AI 生成的 C# Script 时，显示“预览更改”对话框 |

![AI 助手偏好设置](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## 令牌用量

发送给 AI 助手的每条信息都会消耗输入令牌。 单条信息的令牌开销取决于包含哪些上下文：

- **系统提示和自定义指令**：会随每条信息一起发送。 通常为 5,000 到 15,000 个令牌，具体取决于启用了哪些自定义指令。
- **模型元数据**：当助手需要了解你的模型时，会通过工具调用检索元数据。 为了在处理大型模型时不超出提供商的速率限制，助手会采用渐进式披露的方法——先获取轻量级概览（表和度量值名称、关系），再按名称、说明或 DAX 表达式搜索相关对象，只有在问题确实需要时，才会进一步获取特定表或对象的完整信息。 原本会非常庞大的工具结果会被截断，并附带说明，指导助手如何获取其余数据。

### 令牌计数器

聊天输入区域右下角的令牌计数器会显示当前对话的累计令牌用量，其中包括工具往返调用中的输入。 将鼠标悬停在计数器上可查看明细：

- **输入** — 对话中按原价计费的输入令牌；下方还会显示其中有多少来自提供商的提示缓存
- **缓存写入** — 写入提示缓存的令牌（取决于提供商）
- **输出** — 由模型生成的令牌
- **上下文压力** — 当前上下文窗口的使用比例；也会通过计数器旁边的滑动条直观显示

### 减少令牌用量

提问前，先在 **TOM Explorer** 中选择特定对象。 选择对象后，助手会将上下文范围限定为这些对象，而不是检索整个模型的元数据。 这是同时降低令牌用量和 API 成本的最有效方式。

减少令牌用量的其他方法：

- 围绕特定的表、度量值或列提问，而不是对整个模型提出宽泛的问题。 像 _"为所有度量值设置显示文件夹"_ 这样含糊的提示，会迫使助手检索整个模型的元数据。 像 _"为我选中的度量值设置显示文件夹"_ 这样具体的提示，会将上下文限制在当前选择范围内，并显著减少令牌用量
- 切换主题时开始新对话，避免累积过长的对话历史
- 对于探索性问题，使用更小或成本更低的模型

## 局限性

- 需要用户提供 API 密钥。 不包含内置 API 密钥
- AI 响应取决于所选模型和提供商的能力
- 最大上下文窗口为 200,000 个令牌
- AI 助手不能替代对 DAX 和语义模型设计基础的掌握
- 响应质量会因提供商和所选模型而异
- AI 助手无法连接外部文件或服务，也无法搜索互联网
- AI 助手无法添加 MCP 服务器，也无法充当 MCP 服务器
- AI 助手无法在聊天中连接到其他模型。 使用 Tabular Editor 的用户界面来更改模型连接
- AI 助手无法管理偏好

## 禁用 AI 助手

AI 助手是一个可选组件。 在该功能处于公开预览阶段期间，安装时默认不包含该组件，但用户可以选择将其包含在内。 重新运行 Tabular Editor 3 安装程序即可修改现有 Tabular Editor 3 安装，以选择包含或排除 AI 助手组件。 如果使用的是 Tabular Editor 3 的便携版本，可以通过从安装目录中删除名为 `TabularEditor3.AI.dll` 的文件来移除 AI 助手组件。

> [!NOTE]
> 无论是否安装了 AI 助手组件，系统管理员都可以通过指定 [`DisableAi` 策略](xref:policies) 来禁用 Tabular Editor 3 中的所有 AI 功能。
