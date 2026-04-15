---
uid: ai-assistant
title: AI 助手
author: Morten Lønskov
updated: 2026-04-15
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

AI 助手是一种基于聊天的界面，用于 AI 辅助的语义模型开发，帮助你更快地创建语义模型。 它采用企业级设计，可让你完全掌控发送给 AI 的内容，并内置同意管理，让你可以放心使用 AI 助手。 AI 助手已通过独立的安全渗透测试。 详情请访问 [Tabular Editor 信任中心](https://trust.tabulareditor.com)。 它可以浏览模型元数据、编写并执行 DAX 查询、生成 C# Script、运行 Best Practice Analyzer 检查、查询 VertiPaq分析器统计信息，并搜索 Tabular Editor 知识库。

AI 助手采用自带密钥 BYOK 模式。 你只需从受支持的提供商中选择一个并提供其 API 密钥，助手就会直接通过该提供商的 API 运行。

> [!NOTE]
> AI 助手自 Tabular Editor 3.26.0 起处于公开预览阶段。 我们欢迎你反馈使用体验，帮助我们持续改进。

![AI Assistant First Pane on Open](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 快速入门

1. 打开 **工具 > 偏好 > AI 助手**
2. 选择你的 AI 提供商并输入 API 密钥
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入一条信息并按 **Enter** 键开始对话

> [!TIP]
> 使用我们的 [AI 助手交互式演示](https://demos.tabulareditor.com/psl/of150vcy?) 了解如何设置和使用它。

> [!NOTE]
> API 密钥会以加密形式存储在你的本地计算机上。

## 支持的提供程序

在 **工具 > 偏好 > AI 助手 > AI 提供程序** 下配置 AI 提供程序。 从下拉列表中选择一个提供程序，输入你的 API 密钥，并可选择替换默认模型名称。

| 提供程序           | 默认模型              | 需要配置                    |
| -------------- | ----------------- | ----------------------- |
| OpenAI         | gpt-4o            | API 密钥。 可选：组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6 | API 密钥                  |
| Azure OpenAI   | 视部署而定             | API 密钥、端点 URL 和部署名称     |
| 自定义（兼容 OpenAI） | 由用户指定             | API 密钥和自定义端点 URL        |

![AI 助手提供程序偏好设置选择](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### OpenAI

将提供程序选择为 **OpenAI**，然后输入你的 API 密钥。 如果你的 OpenAI 账户使用组织 ID 和项目 ID，也可以选择填写这些信息。 默认模型是 **gpt-4o**，但你可以将其更改为你账户中可用的任意模型。

![AI 助手 OpenAI 配置](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供商，然后输入你的 API 密钥。 默认模型是 **claude-sonnet-4-6**。 你可以将模型名称改为你账号下可用的任意 Anthropic 模型。

![AI 助手 Anthropic 配置](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行输入 token/分钟（ITPM）的速率限制。 新创建的 API 密钥起始为 Tier 1，Claude Sonnet 4.x 的 ITPM 上限为 30,000。 对大型模型发起的一次请求就可能超过此限制。 购买 $40 或以上的 API 额度即可升至第 2 档（450,000 ITPM）。 有关各档位的完整详情，请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

选择 **Azure OpenAI** 作为提供商，并配置以下三个字段：

- **API 密钥** — 用于访问你的 Azure OpenAI 资源的密钥
- **服务终结点** — 你的资源的终结点 URL，例如 `https://your-resource.openai.azure.com`。 使用资源 URL，不要使用 `privatelink` 别名；SSL 证书是为 `*.openai.azure.com` 签发的，直接连接到 `*.privatelink.openai.azure.com` 会导致证书验证失败
- **模型名称** — 填写的是 **部署名称**，不是底层模型名称，也不是资源名称

Azure OpenAI 要求在每次 API 调用中都提供部署名称。 部署名称是在创建部署时指定的，因此它可以是任意字符串。 部署通常会以其所服务的模型命名（例如 `gpt-4o`），但这只是约定，并非强制要求。 如果你输入的是资源名称，或者一个并未作为部署存在的底层模型名称，请求就会失败。

#### 查找部署名称

在 [Azure AI Foundry 门户](https://ai.azure.com) 中：

1. 登录并选择你的 Azure OpenAI 资源
2. 打开 **部署**（如果资源已升级到 Foundry，则为 **模型 + 终结点**）
3. 复制 **名称** 列中的值

在你的组织采用 Azure AI Foundry 之前创建的部署，可能不会显示在门户中。 可通过 Azure CLI 列出它们：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

更多详情见 [创建并部署 Azure OpenAI 资源](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model)。

有关 403 错误、SSL 失败或 "DeploymentNotFound" 响应，请参阅 @azure-openai-connection-errors。

### 自定义（OpenAI 兼容）

“自定义”提供商选项支持本地或组织内部的 LLM，只要它们提供 OpenAI 兼容的 API 端点即可。 输入你的 API 密钥和自定义端点 URL。 这样你就可以将所有数据保留在自己的基础设施内，以满足数据隐私或合规要求。

### 使用本地或组织内部的 LLM

你可以通过“自定义”提供商让 AI 助手对接自托管的 LLM。 这会将所有数据保留在你自己的基础设施内——无论是运行在本机上的模型，还是在组织网络中集中托管的 LLM。 无论哪种方式，都不会将数据发送到第三方云提供商。

以下工具可托管模型并提供 OpenAI 兼容的 API：

- [Ollama](https://ollama.com) — 轻量级 CLI，用于在本地下载并运行模型
- [LM Studio](https://lmstudio.ai) — 带图形界面的桌面应用，用于管理并运行本地模型
- [LocalAI](https://localai.io) — 自托管、社区驱动的替代方案，支持多种模型

这些工具既可以在开发者的工作站上运行供个人使用，也可以部署在组织内的共享服务器上，为你的团队提供集中管理的 LLM 端点。

#### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取一个模型（下载），例如：`ollama pull llama3.1`
3. 启动 Ollama 服务器（安装后会自动运行，默认使用端口 11434）
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:11434/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `llama3.1`）
8. **API Key** 字段可以设置为任意非空值（例如 `ollama`）——Ollama 不需要身份验证，但该字段不能为空

#### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 拉取一个模型。 可以通过左侧面板的模型搜索页面或 CLI 来完成。 例如：`lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 启动 LM Studio 服务器。 可以通过左侧面板的开发者页面或 CLI 来完成。 例如：`lms server start`
   注意：你需要将其配置为 OpenAI 兼容模式。 另外，你可能需要将默认上下文大小调整为 100,000 tokens 以上。
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`）
8. **API Key** 字段可以设置为任意非空值（例如 `lms`）——LM Studio 不需要身份验证，但该字段不能为空

> [!NOTE]
> 本地模型的响应质量取决于模型规模以及你的硬件配置。 更大的模型通常能产生更好的结果，但需要更多 RAM 和性能更强的 GPU。 AI Assistant 的工具调用能力需要使用支持 OpenAI 兼容格式函数调用的模型。

> [!TIP]
> 我们建议选择参数量 _至少_ 为 30 十亿、理想情况下至少为 100 十亿的模型。 例如，Qwen3.5-122B-A10B 模型在我们的内部测试中表现良好。

## 功能

AI 助手可以访问你的模型上下文，并能执行以下操作：

- **模型探索**：查询模型元数据，包括表、列、度量值、关系及其属性
- **DAX 查询编写**：生成 DAX 查询并对你在连接模式下连接的模型执行，结果集会直接在聊天中返回
- **C# 脚本生成**：创建用于修改模型的 C# Script，并在新的编辑器窗口中打开。 当你在聊天中点击 **Execute** 时，默认会显示 [预览更改](xref:csharp-scripts#running-scripts-with-preview) 对话框，让你在接受前先审阅所有模型元数据更改。 你也可以在编辑器中打开脚本，并从脚本工具栏运行它，可选择是否启用预览。 模型元数据更改可通过 **Ctrl+Z** 撤销
- **Best Practice Analyzer**：运行 BPA 分析，查看规则违规情况，并创建或修改 BPA 规则
- **VertiPaq分析器**：查询内存使用统计信息和列的基数
- **文档访问**：读取并修改已打开的文档，例如 DAX 脚本和 DAX 查询
- **知识库搜索**：搜索内置的 Tabular Editor 文档以获取答案
- **UI 导航**：生成 `te3://` 操作链接，用于打开特定的 Tabular Editor 对话框和功能

## 对话

AI 助手支持多个并行对话。 每个对话都会维护各自的信息历史记录和上下文。

- 对话会跨会话保留，并存储在本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 标题会在首次交流后自动生成。 你也可以手动重命名对话
- **自动压缩**：当对话接近上下文窗口限制（约 80%）时，较早的信息会自动总结，以腾出空间。 压缩前会先归档完整对话的快照

## 工件

当 AI 助手生成代码时，会生成可直接在编辑器窗口中打开的 **工件**：

- **C# Script**：在新的 C# Script 编辑器中打开，支持语法高亮、编译和执行
- **DAX 查询**：在新的 DAX 查询编辑器中打开，支持语法高亮和执行

生成物会在 AI 生成过程中实时流式输出。 C# Script 生成物包含安全分析，可标记潜在不安全的代码（例如文件系统访问或网络操作）。

![AI Assistant Generate C# Script](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

当你在聊天中执行 C# Script 时，**脚本预览**对话框会并排显示该脚本对模型元数据所做的所有更改的差异对比。 你可以接受这些更改，或将其撤销。 详见[使用预览运行脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![脚本预览 - 模型更改](~/content/assets/images/preview-script-changes.png)

## 自定义指令

自定义指令是一组指令，用于引导 AI 助手在特定任务中的行为。 它们会根据意图识别自动启用，也可以手动调用。

### 内置自定义指令

AI 助手包含以下内置自定义指令：

| 自定义指令  | 触发词                 |
| ------ | ------------------- |
| DAX 查询 | DAX、查询、EVALUATE、度量值 |
| 模型修改   | 修改、更改、添加、更新、创建      |
| 模型设计   | 设计、架构、模式、最佳实践       |
| 整理模型   | 整理、清理、文件夹、重命名       |
| 优化模型   | 优化、性能、慢、速度          |
| 宏      | 宏、自动化、录制            |
| UDF    | UDF、函数、用户自定义函数      |
| BPA    | BPA、最佳实践、规则、违规      |

自定义指令会在助手回复上方以指示器形式显示，用于说明哪些指令影响了本次回复。 你可以在 **偏好 > AI Assistant > 偏好 > 显示自定义指令指示器** 中切换该指示器的显示。

### 调用自定义指令

输入 `/` 浏览可用的自定义指令；或在信息开头输入完整的 `/instruction-id`，以明确调用某条特定指令。 例如，`/dax-querying` 会强制使用 DAX 查询指令，无论信息内容如何。

### 添加自己的自定义指令

你可以通过将 `.md` 文件放到 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 来创建自定义指令。 每个文件都需要包含 YAML front matter，用于定义指令的元数据：

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

你的指令内容写在这里。当该指令被激活时，这段文本会
注入到 AI 的 system prompt 中。
```

| 字段                          | 必需 | 默认值                                                    | 说明                                |
| --------------------------- | -- | ------------------------------------------------------ | --------------------------------- |
| `id`                        | 否  | 不含 `.md` 的文件名                                          | 唯一标识符，也会作为 `/id` 用于显式调用           |
| `name`                      | 否  | `id` 使用标题式大小写                                          | 自动完成中的显示名称                        |
| `description`               | 否  | -                                                      | 显示在名称下方的简短说明                      |
| `priority`                  | 否  | 100                                                    | 当匹配到多个自定义指令时，数值越高越优先注入            |
| `always_inject`             | 否  | false                                                  | 如果为 true，则始终包含在系统提示词中             |
| `hidden`                    | 否  | false                                                  | 如果为 true，则不会在 `/command` 的自动补全中显示 |
| `triggers.keywords`         | 否  | [] | 触发该指令的词（不区分大小写）                   |
| `triggers.patterns`         | 否  | [] | 用于复杂匹配的正则表达式                      |
| `triggers.context_required` | 否  | [] | 必须满足的条件（例如 `model_loaded`）        |

具有与内置指令相同 `id` 的自定义指令会覆盖内置版本。

## 同意

AI 助手在向 AI 提供商发送数据之前会先征求你的同意。 同意按特定数据类型进行限定：

| 同意类别      | 说明                              |
| --------- | ------------------------------- |
| 查询数据      | DAX 查询结果和数据样本                   |
| 读取文档      | 读取打开的文档内容，例如 DAX 脚本和 DAX 查询     |
| 修改文档      | 对打开的文档进行更改                      |
| 模型元数据     | 表和列架构、度量值定义以及其他模型元数据            |
| 编辑 BPA 规则 | 创建或修改 Best Practice Analyzer 规则 |
| 读取宏       | 读取宏定义                           |

当 AI 助手首次需要访问某种数据类型时，将弹出同意对话框。 你可以选择同意的持续时间：

| 选项   | 范围                                                        |
| ---- | --------------------------------------------------------- |
| 这次   | 仅限单次请求                                                    |
| 本次会话 | 直到重新启动 Tabular Editor                                     |
| 此模型  | 保存在模型的用户选项 (.tmuo) 文件中 |
| 始终   | 全局偏好，将在所有模型和会话间保留                                         |

![AI Assistant Consent Dialog](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

### 管理同意项

你可以在 **Tools > 偏好设置 > AI Assistant > AI Consents** 下查看并重置同意选项。 每个同意类别都会显示其当前状态。 点击 **Reset** 可撤销处于“Always allowed”状态的同意，并将其恢复为“Ask when needed”。

![AI Assistant Consent Settings](~/content/assets/images/ai-assistant/ai-assistant-consent-reset.png)

## 偏好设置

在 **Tools > 偏好设置 > AI Assistant > 偏好设置** 中配置 AI Assistant 的显示和行为选项。

### 聊天显示

| 偏好         | 默认值  | 说明               |
| ---------- | ---- | ---------------- |
| 显示选择上下文指示器 | true | 在聊天中显示当前选定的模型对象  |
| 显示自定义指令指示器 | true | 在助手回复上方显示自定义指令标识 |
| 显示知识库搜索指示器 | true | 搜索知识库时显示进度       |

### 上下文压缩

| 偏好       | 默认值  | 说明                 |
| -------- | ---- | ------------------ |
| 自动压缩     | true | 接近上下文限制时自动摘要较早的信息  |
| 自动压缩阈值 % | 80   | 令牌使用率达到该百分比时触发自动压缩 |

### 知识库

| 偏好         | 默认值  | 说明                          |
| ---------- | ---- | --------------------------- |
| 启动时检查知识库更新 | true | Tabular Editor 启动时自动检查知识库更新 |

### C# Script

| 偏好   | 默认值  | 说明                                    |
| ---- | ---- | ------------------------------------- |
| 预览更改 | true | 在聊天中执行 AI 生成的 C# Script 时，显示“预览更改”对话框 |

![AI 助手偏好](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token 使用量

每条发给 AI 助手的信息都会消耗输入 token。 单条信息的 token 成本取决于包含了哪些上下文：

- **系统提示词和自定义说明**：每条信息都会一并发送。 通常为 5,000 到 15,000 个 token，具体取决于启用了哪些自定义说明。
- **模型元数据**：当助手需要理解你的模型时，会通过工具调用获取元数据。 精简摘要包含表名、列名、度量值名称、关系和说明。 完整的元数据获取会包含完整的模型定义。 对于大型模型，这可能会消耗数万个 token。

### 减少 token 使用量

提问前，先在 **TOM Explorer** 中选择特定对象。 选中对象后，助手会将上下文限定在这些对象上，而不是拉取整个模型的元数据。 这是同时减少 token 使用量和 API 成本的最有效方式。

其他减少 token 使用量的方法：

- 围绕特定的表、度量值或列提出更聚焦的问题，而不是对整个模型提出泛泛的问题。 像 _“为所有度量值设置显示文件夹”_ 这样含糊的提示，会迫使助手检索整个模型的元数据。 像 _“为我选中的度量值设置显示文件夹”_ 这样具体的提示，会将上下文限制在当前选择范围内，并且消耗的 token 少得多
- 切换话题时开启新对话，避免累积过长的对话历史
- 进行探索性提问时，使用更小或成本更低的模型

## 局限性

- 需要用户自行提供 API 密钥。 不包含内置 API 密钥
- AI 的响应取决于所选模型及提供商的能力
- 最大上下文窗口为 200,000 个 token
- AI 助手不能替代你对 DAX 和语义模型设计基础的理解
- 响应质量会因提供商和模型选择而异
- AI 助手无法连接到外部文件或服务，也无法搜索网页
- AI 助手无法添加或充当 MCP 服务器
- AI 助手无法在聊天中切换到其他模型。 使用 Tabular Editor 的用户界面更改模型连接
- AI 助手无法管理偏好

## 禁用 AI 助手

AI 助手是一个可选组件。 该功能目前处于公开预览阶段，安装时默认不会包含，但用户可以选择安装。 你可以再次运行 Tabular Editor 3 安装程序，修改现有的 Tabular Editor 3 安装，以包含或排除 AI 助手组件。 如果你使用的是 Tabular Editor 3 便携版，可以从安装目录中删除名为 `TabularEditor3.AI.dll` 的文件来移除 AI 助手组件。

> [!NOTE]
> 无论是否安装 AI 助手组件，系统管理员都可以通过指定 [`DisableAi` 策略](xref:policies) 来禁用 Tabular Editor 3 中的所有 AI 功能。