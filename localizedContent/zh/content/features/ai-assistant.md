---
uid: ai-assistant
title: AI 助手
author: Morten Lønskov
updated: 2026-10-09
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

AI 助手是用于语义模型开发的聊天面板。它会浏览模型元数据、编写并运行 DAX 查询、生成 C# Script、运行 Best Practice Analyzer 检查、查询 VertiPaq分析器统计信息，并搜索 Tabular Editor 知识库。[权限设置](#permissions-and-consent) 控制它会向你的 AI 提供程序发送哪些内容。 AI 助手已通过独立渗透测试；你可以查看 [Tabular Editor 信任中心](https://trust.tabulareditor.com)。

AI 助手采用自带密钥（BYOK）模式，你提供来自某个受支持提供商的 API 密钥，助手会直接调用该提供商的 API。

你也可以通过 [MCP 服务器](xref:mcp-server) 使用自己的代理，无需 API 密钥。 Claude Code、GitHub Copilot、VS Code 代理模式、Codex 或 Cursor 等代理，可在打开的模型上使用与聊天相同的工具和权限设置进行操作；但会话级授权和按模型授权除外，这两者仅适用于聊天。查看 [MCP 服务器与 AI 助手的差异](#mcp-server-and-ai-assistant-differences)。

![AI 助手窗格首次打开时的界面：上方是助手的问候语，列出它能做什么（回答问题、查询模型、编写并执行 C# Script、修改模型）以及不能做什么，下方是空白信息输入框](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 快速入门

1. 依次打开 **工具 > 偏好 > AI 功能 > AI 助手 > AI 提供程序**
2. 选择 AI 提供商（全新安装时默认是 **无（AI 已禁用）**），然后输入你的 API 密钥
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入一条信息并按 **Enter** 键开始对话

> [!TIP]
> 我们的 [AI 助手交互式演示](https://demos.tabulareditor.com/psl/of150vcy?) 将逐步讲解设置和使用方法。

> [!NOTE]
> API 密钥会以加密形式存储在你的本地计算机上。

## 支持的提供程序

在 **工具 > 偏好 > AI 功能 > AI 助手 > AI 提供商** 中配置 AI 提供商。从下拉列表中选择一个提供商（在你完成配置之前，默认值为 **无（AI 已禁用）**），输入 API 密钥，并可选择覆盖默认模型。

将模型字段留空即可使用提供商的默认模型。 OpenAI 和 Anthropic 都有默认值；Azure OpenAI 和自定义提供程序始终需要填写相应的值。

| 提供程序           | 默认模型                    | 需要配置                          |
| -------------- | ----------------------- | ----------------------------- |
| OpenAI         | gpt-5.5 | API 密钥。可选：基础 URL、组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6       | API 密钥。可选：基础 URL              |
| Azure OpenAI   | 无。必须提供部署名称              | API 密钥、端点 URL 和部署名称           |
| 自定义（兼容 OpenAI） | 无。必须提供模型名称              | API 密钥和自定义端点 URL              |

![AI 提供商偏好页，其中“选择提供商”下拉列表已展开，显示“无（AI 已禁用）”、OpenAI、Anthropic、Azure OpenAI 和“自定义（兼容 OpenAI）”，下方有 URL 和 API 密钥字段](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### 选择模型

当前活动模型显示在信息框上方的状态栏中，位于上下文用量条旁边。点击它会打开一个选择器，其中列出了当前已配置提供程序的可用模型；你选择的模型会从下一次请求开始生效。最后一项 **偏好...** 会打开 **工具 > 偏好 > AI 功能 > AI 助手 > AI 提供程序**，以便配置列表中未包含的选项。对于 Azure OpenAI 和自定义提供程序，或者在尚未检索到模型列表之前，模型名称会显示为链接，点击后会打开相应的偏好设置页面。

![信息框上方已打开的模型选择器，其中列出了 claude-sonnet-5、claude-fable-5-1、claude-fable-5、claude-opus-5、claude-haiku-4-5、claude-opus-4-8，以及以粗体显示的当前活动项 claude-sonnet-4-6，底部还有偏好……位于分隔线下方](~/content/assets/images/ai-assistant/ui-model-picker.png)

> [!NOTE]
> 只有在提供程序、API 密钥和模型都已设置后，才会显示模型指示器。

### OpenAI

将提供程序选择为 **OpenAI**，然后输入你的 API 密钥。如果你的 OpenAI 账户使用 Organization ID 或 Project ID，也一并填写。模型名称可以填写你账户中可用的任何模型。

![早期版本的 AI 提供程序偏好设置页：已选择 OpenAI，显示已遮盖的 API 密钥，Organization ID 和 Project ID 字段为空，模型名称为 gpt-4o](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供商，然后输入你的 API 密钥。模型名称可以填写你账户中可用的任何 Anthropic 模型。

![AI 提供程序偏好设置页：提供程序选择为 Anthropic，基础 URL 为 https://api.anthropic.com，显示已遮盖的 API 密钥，模型名称为 claude-sonnet-4-6](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行每分钟输入 token（ITPM）的速率限制。新创建的 API 密钥起始为 Tier 1，Claude Sonnet 4.x 的 ITPM 上限为 30,000。对大型模型发起的一次请求就可能超过此限制。购买 $40 或以上的 API 额度即可升至第 2 档（450,000 ITPM）。有关各档位的完整详情，请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

选择 **Azure OpenAI** 作为提供商，并配置以下字段：

- **API 密钥**：用于访问你的 Azure OpenAI 资源的密钥
- **Service endpoint**：资源 URL，例如 `https://your-resource.openai.azure.com`。 SSL 证书是为 `*.openai.azure.com` 签发的，因此使用 `*.privatelink.openai.azure.com` 地址会导致证书验证失败
- **Deployment**：在 **Deployments** 的 **Name** 列中显示的部署名称

Azure OpenAI 要求在每次 API 调用中都提供部署名称。该名称是在创建部署时设置的，通常与其服务的模型一致，例如 `gpt-4o`，但也可能不同。如果你输入资源名称，或输入的模型名称并未作为部署存在，请求就会失败。

可在 [Azure AI Foundry 门户](https://ai.azure.com) 中找到部署名称：

1. 登录并选择你的 Azure OpenAI 资源
2. 打开 **部署**（如果资源已升级到 Foundry，则为 **模型 + 终结点**）
3. 复制 **名称** 列中的值

如果在你的组织采用 Azure AI Foundry 之前创建的部署未显示在门户中，可以用 Azure CLI 列出这些部署：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

见 [创建并部署 Azure OpenAI 资源](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model)。

有关 403 错误、SSL 失败或 "DeploymentNotFound" 响应，请参阅 @azure-openai-connection-errors。对于部署在 Microsoft Foundry 中的模型，请参阅[使用 Microsoft Foundry](#using-microsoft-foundry)。

### 自定义（兼容 OpenAI）

自定义提供商可以连接到任何提供 OpenAI 兼容 API 端点的 LLM，例如你自己机器上的模型，或托管在你组织网络中的模型。输入你的 API 密钥和端点 URL。使用自托管模型时，所有数据都会保留在你自己的基础设施中，不会发送到第三方云提供商。见 [使用本地或组织内的 LLM](#using-a-local-or-organizational-llm)。

## 使用本地或组织内部的 LLM

你可以通过“自定义”提供商让 AI 助手对接自托管的 LLM。这样可确保所有数据都保留在你自己的基础设施内，无论是运行在本地计算机上的模型，还是托管在你所在组织网络中的集中式 LLM。无论哪种方式，都不会将数据发送到第三方云提供商。这些工具可以在开发者的工作站上托管提供 OpenAI 兼容 API 的模型，也可以托管在充当团队端点的共享服务器上：

- [Ollama](https://ollama.com) — 轻量级 CLI，用于在本地下载并运行模型
- [LM Studio](https://lmstudio.ai) — 带图形界面的桌面应用，用于管理并运行本地模型
- [LocalAI](https://localai.io) — 自托管、社区驱动的替代方案，支持多种模型

### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取一个模型，例如 `ollama pull llama3.1`
3. 启动 Ollama 服务器。安装后会自动启动，默认使用端口 11434
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:11434/v1`
7. 将 **Model name** 设置为你拉取的模型，例如 `llama3.1`
8. 将 **API Key** 设置为任意非空值，例如 `ollama`。 Ollama 不要求身份验证，但该字段不能为空

### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 从左侧面板中的模型搜索页面下载一个模型，或使用 CLI，例如 `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 从左侧面板中的开发者页面启动 LM Studio 服务器，或使用 `lms server start`。启用 OpenAI 兼容模式。如果上下文大小低于 100,000 个 token，请将其调高到 100,000 以上
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. 将 **模型名称** 设置为你下载的模型，例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
8. 将 **API 密钥** 设置为任意非空值，例如 `lms`。 LM Studio 不需要身份验证，但该字段不能为空

> [!NOTE]
> 本地模型的响应质量取决于模型规模以及你的硬件配置。更大的模型通常效果更好，但也需要更多 RAM 和性能足够的 GPU。 AI Assistant 的工具调用功能要求模型支持 OpenAI 兼容格式的函数调用。

> [!TIP]
> 使用参数量至少为 30 billion 的模型，最好为 100 billion 或更多。 Qwen3.5-122B-A10B 在内部测试中表现良好。

## 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com)（前身为 Azure AI Foundry）可让你在 Azure 环境中部署 OpenAI 和 Anthropic 模型。在 Tabular Editor 中，使用 **OpenAI** 或 **Anthropic** 提供程序连接这些模型。

> [!IMPORTANT]
> 不要将 **Azure OpenAI** 提供程序用于 Microsoft Foundry 模型。它仅适用于使用 `api-version` 查询参数的经典 Azure OpenAI 资源。

### Microsoft Foundry 上的 OpenAI 模型

按如下方式配置在 Microsoft Foundry 中部署的 OpenAI 模型，例如 GPT-4o 或 GPT-5.4-mini：

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **OpenAI**
3. 将 **基础 URL** 设置为你的 Foundry 资源端点，并在末尾追加 `/openai/v1`，格式如下之一：
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. 输入 Foundry **API 密钥**
5. 将 **模型名称** 设置为你的部署名称，例如 `gpt-5.4-mini`

> [!NOTE]
> Microsoft Foundry 门户不会显示基础 URL。它会显示一个包含完整 API 路径的 **目标 URI**，例如 `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`。对于基础 URL，只使用 `https://your-resource.services.ai.azure.com/openai/v1`。

### Microsoft Foundry 中的 Anthropic 模型

对于在 Microsoft Foundry 中部署的 Anthropic 模型，例如 Claude Sonnet 4.6：

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **Anthropic**
3. 将 **基础 URL** 设置为你的 Foundry 资源端点，并在末尾追加 `/anthropic`，例如 `https://your-resource.services.ai.azure.com/anthropic`
4. 输入 Foundry **API 密钥**
5. 将 **模型名称** 设置为模型标识符，例如 `claude-sonnet-4-6`

> [!NOTE]
> 门户会显示一个 **目标 URI**，例如 `https://your-resource.services.ai.azure.com/anthropic/v1/messages`。对于基础 URL，只使用到并包含 `/anthropic` 为止的部分。

## 功能

在你授予的[权限](#permissions-and-consent)范围内，AI Assistant 会在你的模型上下文中执行以下操作：

- **模型探索**：查询模型元数据，包括表、列、度量值、关系及其属性
- **DAX 查询编写**：生成 DAX 查询，对连接模式下连接的模型执行，并在聊天中返回结果集
- **C# 脚本生成**：创建用于模型更改的 C# Script。根据你的设置，助手会在编辑器窗口中打开脚本供你运行，或自行运行该脚本；请参阅[让助手更改你的模型](#letting-the-assistant-change-your-model)。 **Ctrl+Z** 撤销对模型元数据的更改
- **Best Practice Analyzer**：运行 BPA 分析，列出规则违规情况，并创建或修改 BPA 规则
- **VertiPaq分析器**：查询内存使用统计信息和列的基数
- **文档访问**：读取并修改已打开的文档：DAX 查询、C# Script 和 DAX 脚本
- **知识库搜索**：搜索内置的 Tabular Editor 文档
- **UI 导航**：生成 `te3://` 操作链接，用于打开特定的 Tabular Editor 对话框和功能

通过 [MCP 服务器](xref:mcp-server) 连接的代理具备相同的能力，但不包括 UI 导航。两者都会通过运行一个 C# Script 来更改模型，并将该更改作为一个可撤销的单一步骤记录。它们的区别在于你如何审查更改以及授予权限；请参阅 [MCP 服务器与 AI 助手的差异](#mcp-server-and-ai-assistant-differences)。

> [!NOTE]
> 当模型从文件加载(例如 `.bim` 文件或 TMDL 文件夹)，且未连接到 Analysis Services 或 Power BI 时，需要连接的工具会被隐藏，包括 DAX 查询执行和 VertiPaq分析器统计信息。助手仍会编写 DAX 查询，但在你连接之前，DAX 查询项上的 **Execute** 会被禁用。从 `.vpax` 文件加载的 VertiPaq分析器统计信息仍然可用。

## 让助手更改你的模型

默认情况下，助手会编写一个 C# Script 并在编辑器窗口中打开，供你查看并运行。当你在 **工具 > 偏好 > AI 功能 > AI 助手 > 偏好** 下选中 **允许 AI 助手直接运行 C# Script** 时，它也可以自行运行该脚本。

此设置默认关闭，并且只有在 **工具 > 偏好 > AI 功能 > 权限** 下将 **模型元数据** 设置为 **读取/写入** 后才可用。

### 当助手运行脚本时会发生什么

- 如果 **预览更改** 处于开启状态（默认值），则会在应用更改前显示[预览对话框](xref:csharp-scripts#run-c-scripts-with-preview)。**取消** 会还原这些更改，并将此次拒绝 Report 给助手。如果 **预览更改** 处于关闭状态，则会在不显示对话框的情况下应用更改。
- 该脚本的更改会作为一个撤销条目显示为：**C# Script (AI Assistant)**。 **Ctrl+Z** 会撤销整个脚本所做的更改。
- 如果脚本在执行到一半时失败，模型将保持不变，助手会 Report 该错误。
- 访问文件、网络或外部程序集的脚本不会运行。它会以脚本工件形式打开，带有 **Unsafe** 徽章，且 **Execute** 被禁用；助手的回复还会说明脚本使用了什么。

如果你要求生成脚本，例如“给我写一个脚本，把每个度量值都重命名为 sentence case”，助手会将其作为脚本文档打开，由你自行运行，即使启用了此设置也是如此。

`DisableCSharpScripts` [策略](xref:policies) 适用于所有版本，并会同时禁用直接执行和助手交给你运行的脚本。

`BlockUnsafeScripts` 策略需要企业版，并适用于 Tabular Editor 中的所有脚本，包括通过 [MCP 服务器](xref:mcp-server)运行的脚本。启用后，助手仍然可以编写访问文件、网络或外部程序集的脚本，但脚本不会运行，也不会打开任何工件供你查看。见[管理员策略](xref:csharp-scripts#administrator-policies)。

## 对话

AI 助手支持多个同时进行的对话，每个对话都有各自的信息历史记录和上下文。

- 对话会跨会话保留，并存储在本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 标题会在首次交流后自动生成，你也可以重命名对话
- **自动压缩**：当对话接近上下文窗口限制时，系统会先归档完整对话的快照，再将较早的信息概括成摘要以释放空间。该阈值是模型自身上下文窗口的百分比，可在 [上下文压缩](#context-compaction) 中设置

### 删除对话

**删除对话** 位于 AI 助手工具栏的最左侧，紧挨着 **新建对话**。确认提示后，对话及其历史记录会从磁盘中删除，且无法恢复。点击面板标题栏上的关闭按钮，或选择 **视图 > AI 助手**，只会隐藏面板，不会删除任何内容。

## 工件

AI 助手生成的代码会作为 _工件_ 在编辑器窗口中打开：

- **C# Script**：在 C# Script 编辑器中打开，支持语法高亮、编译和执行
- **DAX 查询**：在 DAX 查询编辑器中打开，支持语法高亮和执行

工件会随着 AI 生成而流式呈现；C# Script 工件还包含安全分析，可标记不安全代码，例如访问文件系统或进行网络操作。

![AI 助手窗格，显示生成的 C# Script 产物及其“执行”按钮，以及助手对该脚本作用的说明和随附的大小写敏感提示](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

如果启用了 **预览更改**，在聊天中运行 C# Script 时会打开 **脚本预览** 对话框，并排显示该脚本对所有模型元数据所做更改的差异，你可以在其中接受或还原这些更改。请参阅 [带预览运行脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![“脚本预览 - 模型更改”对话框：左右并排显示更改前后的模型；其中 Internet Total Freight 度量值的格式字符串已更改，并新增了说明和显示文件夹，且每项更改都标注了对应的原始值](~/content/assets/images/preview-script-changes.png)

## 自定义指令

_自定义指令_ 是一组指令集，用于在特定任务中引导 AI 助手。助手会收到所有可用指令及其 `description` 的列表，并且只加载与你请求相关的那些指令的全文，所以描述要尽量准确、具体。已加载的指令会在该对话的剩余过程中持续生效。

### 内置自定义指令

AI 助手包含以下自定义指令：

| 自定义指令       | 调用方式                  | 涵盖内容                                                    |
| ----------- | --------------------- | ------------------------------------------------------- |
| DAX 查询      | `/dax-querying`       | 编写和执行 DAX 查询：列与度量值的限定引用、验证筛选器值、验证并更新查询                  |
| 模型修改        | `/model-modification` | 用于创建或更改模型对象的 C# Script：TOMWrapper API 模式、执行顺序、幂等更新、命名规则 |
| 语义模型设计      | `/model-design`       | 星型架构、关系与交叉筛选、日期表、度量值与计算列、计算组、命名                         |
| 语义模型组织      | `/organize-model`     | 审核并整理模型元数据：命名约定、表格组、显示文件夹、隐藏列、格式字符串、说明                  |
| 语义模型大小优化    | `/optimize-model`     | 减少模型内存占用和大小：VertiPaq 度量值、删除列、数据类型调优、结构调整、SKU 限制         |
| 宏           | `/宏`                  | 用于宏窗口的可复用 C# 宏：选择上下文、通用代码规则                             |
| DAX 用户自定义函数 | `/udf`                | 编写 DAX UDF：语法、`VAL`/`EXPR` 参数模式、类型提示、命名空间、DaxLib        |
| 最佳实践分析器     | `/bpa`                | 查看违规项，并使用 LINQ Dynamic 表达式编写自定义规则                       |

在 **工具 > 偏好 > AI 功能 > AI 助手 > 偏好** 下选中 **显示自定义指令指示器** 后，每条回复上方的指示器会显示哪些指令影响了该回复。

### 调用自定义指令

输入 `/` 可浏览可用的自定义指令。在信息开头输入某条指令的 `/id`，即可加载该指令，而不受信息内容影响；例如，`/dax-querying` 会加载 DAX 查询指令。仅输入 `/id` 而不附带信息，会加载该指令，但不会发出请求。显式加载的指令会在后续整个对话中持续生效，就像助手自行加载的指令一样。

### 添加自己的自定义指令

将 `.md` 文件放到 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 中，即可创建自定义指令。该文件夹会在 AI 助手首次运行时创建，其中包含一个可供参考和复制的 `example.md` 文件。在 AI Assistant 工具栏上点击 **Open Custom Instructions Folder** 即可打开该文件夹。

用于定义指令元数据的 YAML frontmatter 是可选的：

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

| 字段              | 必需 | 默认值           | 说明                                          |
| --------------- | -- | ------------- | ------------------------------------------- |
| `id`            | 否  | 不含 `.md` 的文件名 | 唯一标识符，也会作为 `/id` 用于显式调用                     |
| `name`          | 否  | `id` 使用标题式大小写 | 自动完成中的显示名称                                  |
| `description`   | 否  | 默认使用 `name`   | 说明该指令涵盖的内容以及适用时机                            |
| `priority`      | 否  | 100           | 当多个自定义指令同时生效时，数值越高越先注入                      |
| `always_inject` | 否  | false         | 如果为 true，则始终包含在系统提示词中。此类指令不会出现在 `/` 自动完成列表中 |
| `hidden`        | 否  | false         | 如果为 true，则不会在 `/command` 的自动补全中显示           |

具有与内置指令相同 `id` 的自定义指令会覆盖内置版本。

Tabular Editor 会按以下方式读取这些文件：

- frontmatter 必须以文件第一行的 `---` 开始，并以单独一行 `---` 结束。如果不符合上述格式，或者 YAML 无法解析，则整个文件都会被视为指令内容，并应用上述所有默认值
- 上表中未列出的键会被忽略。早期版本中仍包含 `triggers:` 部分的文件可按原样加载
- 正文中出现的任何 `{{version}}` 都会被替换为 Tabular Editor AI 组件的版本号
- 只会读取文件夹中直接包含的 `.md` 文件；不会搜索子文件夹

### 来自你所在组织的自定义说明

管理员可以通过 `AiCustomInstructionsPath` [策略](xref:policies) 发布一个面向所有人的自定义指令文件夹，该文件夹也可以是只读网络共享。除内置指令外，这些指令也会为每位用户加载，其使用方式与其他指令相同：会出现在 `/` 自动完成中，可按说明选择，也可通过 `/id` 调用。

如果多个位置存在相同的 `id`，优先级如下：

1. 你所在组织的文件夹
2. 你自己的文件夹
3. 内置指令

另一项策略 `DisableUserCustomInstructions` 会让 Tabular Editor 忽略你自己文件夹中的指令，并禁用 **Open Custom Instructions Folder**；内置指令和组织文件夹中的指令仍会加载。这两项策略都需要 Tabular Editor 3 企业版。

## 权限与同意

为每项资源设置访问级别，以控制 AI Assistant 可以访问哪些内容；[MCP 服务器](xref:mcp-server) 也使用相同的设置。

| 资源                         | 涵盖内容                                                     | 级别           | 默认值    |
| -------------------------- | -------------------------------------------------------- | ------------ | ------ |
| **模型元数据**                  | 表、列和度量值的名称、表达式、描述等。“读取”权限还包括 VertiPaq分析器的统计信息            | 拒绝 / 读取 / 写入 | **读取** |
| **模型数据**                   | 模型中的数据值，例如 DAX 查询结果。需要实时连接                               | 拒绝 / 读取      | **拒绝** |
| **Best Practice Analyzer** | 读取可列出规则并运行分析；写入可添加或修改规则                                  | 拒绝 / 读取 / 写入 | **读取** |
| **文档**                     | 你当前打开的文档：DAX 查询、C# Script 和 DAX 脚本。读取可访问其内容；创建或修改则需要写入权限 | 拒绝 / 读取 / 写入 | **写入** |
| **宏**                      | 你的宏库。读取可列出并读取宏；写入权限为未来的宏编辑工具预留                           | 拒绝 / 读取 / 写入 | **写入** |

**Write**（在下拉列表中标为 **Read/Write**）也包含 Read 权限。

> [!NOTE]
> 授予 **模型数据** 权限会将模型中的数据值发送给你的 AI 提供商。

某些授权依赖于其他授权：

- 要使用[直接执行](#letting-the-assistant-change-your-model)，必须具备 **模型元数据 > 写入** 权限；直接执行功能需要另行开启。
- 运行 Best Practice Analyzer 除了需要 **Best Practice Analyzer > 读取** 外，还需要 **模型元数据 > 读取**。
- 运行 DAX 查询除了需要 **模型数据 > 读取** 外，还需要 **模型元数据 > 读取**。查询可以通过 `INFO` 函数、DMV 以及结果中的列名来读取元数据。

### 设置权限授予

打开 **工具 > 偏好 > AI 功能 > 权限**。在这里，每个资源都有一个下拉菜单，可选择其可用级别。

![AI 功能 > 权限偏好设置，每个资源一个下拉菜单，默认值](~/content/assets/images/pref-ai-permissions.png)

聊天没有单独的“询问”级别，当它需要某个被设为 **拒绝** 的资源时，会显示一张[权限卡片](#permission-cards-in-the-chat)。

> [!NOTE]
> 从 3.27.0 起，**模型元数据**、**文档** 和 **宏** 默认设置为“读取”或更高级别，聊天也不会再为它们弹出提示。默认情况下，只有 DAX 查询结果和对 Best Practice Analyzer 规则的编辑会显示卡片。将某个资源设为 **拒绝**，就能让它重新弹出提示。

> [!NOTE]
> 在企业版中，管理员可以通过策略限制这些权限的上限。参见 @policies。

### 聊天中的权限卡片

当助手需要的资源超出你当前授权的范围时，对话中会出现一张 **需要权限** 卡片。卡片会说明助手想做什么，例如“AI 想访问你的语义模型的元数据”，或者显示它建议运行的 DAX 查询。

![聊天中的“需要权限”卡片，显示助手想要运行的 DAX 查询，并带有“允许”“在本次会话中允许”“对此模型允许”“始终允许”和“拒绝”按钮](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| 按钮           | 作用                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------ |
| **允许**       | 仅适用于当前这一轮。在完成你的任务期间，助手可能会重复提出同样的请求，之后也不会记住任何内容                                             |
| **在本次会话中允许** | 在 Tabular Editor 重启前一直有效。该授权只保存在内存中，绝不会写入磁盘                                                |
| **仅对该模型允许**  | 会记录到模型的[用户选项](xref:user-options) 文件中，并在你下次打开此模型时生效。仅针对 **模型元数据** 和 **模型数据** 提供，且仅在已加载模型时可用 |
| **始终允许**     | 在“权限”页中提高常设授权级别，对所有模型和所有会话生效                                                               |
| **拒绝**       | 拒绝此请求。助手会在没有该访问权限的情况下继续；下次需要该权限时，卡片会再次出现                                                   |

**始终允许** 绝不会降低现有授权；如果某个资源当前是“写入”，即使你允许的是“读取”，它也会保持为“写入”。

### 在等待权限时停止当前轮次

在你回应 **需要权限** 卡片之前，本轮对话会暂停。**停止** 会在不作答的情况下结束本轮，移除卡片，并将该请求计为已拒绝。发送一条新信息以继续对话。

### MCP 服务器与 AI 助手的区别

[MCP 服务器](xref:mcp-server)使用相同的五种授权，但不会显示权限卡片：

- 服务器启动时会读取这些授权，并持续生效直到服务器停止，因此更改后的授权只有在你重启服务器后才会生效
- 只有全局授权会生效。通过 **对此模型允许** 或 **本次会话允许** 授予的权限仅对该聊天生效
- 被拒绝的资源对应的工具不会出现在代理的工具列表中

### 撤销权限

要撤销某项资源的授权，就在 **权限** 页面将它重新设为 **拒绝**。之后，聊天在下次需要该资源时会显示一张权限卡片。

降低全局授权级别不会清除按模型授予的权限。要撤销按模型授予的权限，请删除该模型的 `.tmuo` 文件，或删除其中的 `Permissions` 项。参见 @user-options。

### 审计记录

在企业版中，包括 Consultancy 和 Trial 许可证，Tabular Editor 会将 AI Assistant 和 [MCP 服务器](xref:mcp-server) 的活动写入本地日志。记录内容包括：

- 请求了哪些权限，以及你如何回应
- 运行了哪些工具，以及每个工具是成功、失败还是被阻止
- 助手或 MCP 代理运行或提交运行的任何 C# Script 的完整文本，包括在运行时失败或被拒绝执行的脚本

你的提示词、助手的回复以及模型中的数据值都不会被记录。无法编译的脚本不会被保存；同样，助手写入文档供你自行运行的脚本文本也不会被保存。在 **工具 > 偏好 > AI 功能** 下点击 **打开审计文件夹**，即可打开日志文件夹。

如果没有企业版许可证，或许可证尚未激活，则不会记录任何内容，不会创建文件夹，也不会显示该按钮。关于每条记录包含的内容、文件存储位置以及重定向这些文件的策略，参见 @ai-audit-log。

## 偏好设置

在 **工具 > 偏好 > AI 功能 > AI Assistant > 偏好** 中配置 AI 助手的显示与行为选项。

### 聊天显示

| 偏好         | 默认值 | 说明               |
| ---------- | --- | ---------------- |
| 显示选择上下文指示器 | 关   | 在聊天中显示当前选定的模型对象  |
| 显示自定义指令指示器 | 关   | 在助手回复上方显示自定义指令标识 |
| 显示知识库搜索指示器 | 关   | 搜索知识库时显示进度       |

### 上下文压缩

| 偏好       | 默认值 | 说明                                                                              |
| -------- | --- | ------------------------------------------------------------------------------- |
| 自动压缩     | 开   | 接近上下文限制时自动摘要较早的信息                                                               |
| 自动压缩阈值 % | 80  | 达到模型自身上下文窗口的这一百分比时，将触发自动压缩。此字段可接受 25 到 100 之间的值。低于 50 的值按 50 处理，高于 90 的值按 90 处理 |

### C# Script

| 偏好                     | 默认值 | 说明                                                                                                                                                                                                   |
| ---------------------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 允许 AI 助手直接运行 C# Script | 关   | 允许助手自行运行 C# Script。关闭后，助手会打开每个脚本，由你来运行。只有在 **权限** 下将 **模型元数据** 设为 **读取/写入** 后，此功能才可用；如果启用了 `DisableCSharpScripts` [策略](xref:policies)，则始终不可用。见 [让助手更改你的模型](#letting-the-assistant-change-your-model) |
| 预览更改                   | 开   | 在聊天中执行 AI 生成的 C# Script 时，显示“预览更改”对话框                                                                                                                                                                |

**启动时检查知识库更新** 选项和 **打开审计文件夹** 按钮位于 **AI 功能** 页面中 **AI Assistant** 上方，这两项也适用于 MCP 服务器。见 @preferences。

![AI Assistant 偏好页面：三个聊天显示指示器均未选中（默认），已选择“自动压缩”，阈值为 80，“允许 AI 助手直接运行 C# Script”未选中，并已选择“预览更改”](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token 使用量

每条发给 AI 助手的信息都会消耗输入 token。单条信息的 token 成本取决于其包含的上下文：

- **系统提示词和自定义指令**：会随每条信息一起发送；通常为 5,000 到 15,000 个 token，具体取决于启用了哪些自定义指令
- **模型元数据**：通过工具调用分阶段获取。助手会先获取一个轻量级概览（表和度量值名称、关系），然后按名称、描述或 DAX 表达式搜索相关对象，并且只在问题需要时才检索相关表或对象的完整信息。如果工具调用结果非常大，会被截断，并附带说明，指导助手如何获取剩余内容

### Token 计数器

Token 计数器位于信息框上方的状态栏中，紧挨着[当前模型指示器](#choosing-a-model)。进度条会以千 token 为单位显示“已用 / 总量”，并会随着上下文逐渐填满而呈现绿色、琥珀色或红色。数字前面的 `±` 表示暂时还无法提供精确计数。

将鼠标悬停在计数器上可查看明细：

| 部分           | 涵盖内容                                       |
| ------------ | ------------------------------------------ |
| **上一轮**      | 最近一次交互的开销：新输入、从提供方的提示缓存中读取的令牌、写入缓存的令牌，以及输出 |
| **本次对话（计费）** | 同样的四项数字，累计整个对话中的每次请求，包括工具往返调用              |
| **上下文**      | 当前位于上下文窗口中的令牌数，并与该窗口的实际大小对照                |

某一行可能会显示为：`37,588 input + 131,744 cached · write 37,558 · output 2,866`。对于不支持提示缓存的提供商，将省略缓存部分；当某个部分没有任何可报告的内容时，该部分也将被省略。

> [!TIP]
> 对比 **上一轮** 和 **本次对话（计费）**，就能看出单个问题消耗了多少 token。在较长的对话中，**本次对话（计费）** 的数值很大，而 **上一轮** 的数值很小，这是正常现象。

### 上下文窗口

上下文使用进度条、自动压缩触发点以及单次回复的最大长度，都以所选模型的上下文窗口为准。例如，如果某个模型的窗口为一百万 token，就会以一百万 token 作为度量值基准进行衡量。如果无法得知模型的窗口大小（例如仅有 Azure OpenAI 或 Custom 的部署名称，或某台机器从未检索过模型目录），Tabular Editor 会按 200,000 个 token 计算。

### 减少 token 使用量

提问前，先在 **TOM Explorer** 中选择特定对象。这样一来，助手会将上下文范围限定为所选对象，而不会检索整个模型的元数据；这样最能减少 token 用量和 API 成本。

其他减少 token 使用量的方法：

- 尽量围绕特定的表、度量值或列提问。像“为所有度量值设置显示文件夹”这样含糊的提示词，会让助手检索整个模型的元数据。像“为我当前选中的度量值设置显示文件夹”这样明确的提示词，会将上下文限制在当前选择范围内，并使用少得多的 token
- 切换主题时就开始新对话，以免历史记录越积越长
- 进行探索性提问时，使用更小或成本更低的模型

## 限制

- 需要你自己的 API 密钥；不内置 API 密钥
- 响应质量取决于所选的提供商和模型
- 该 AI 助手不能替代你对 DAX 和语义模型设计基础的理解
- 该 AI 助手无法访问外部文件或服务，也无法搜索网页
- 该 AI 助手无法连接到外部 MCP 服务器来扩展自己的工具。若要在 Tabular Editor 3 中使用您自己的代理，请参阅 @mcp-server
- 该 AI 助手无法在聊天中切换到其他模型。在 Tabular Editor 用户界面中更改模型连接
- 该 AI 助手无法管理偏好

## 禁用 AI 助手

AI 助手是一个可选组件，自 Tabular Editor 3.27.0 起默认随产品安装。重新运行 Tabular Editor 3 安装程序，以在现有安装中添加或移除该组件。在便携版本中，从安装目录中删除 `TabularEditor3.AI.dll` 即可将其移除。

同一个组件还包含 MCP 服务器，因此排除该组件或删除 `TabularEditor3.AI.dll` 会同时移除两者。如果只想关闭聊天功能，保留该组件并设置 `DisableAiChat` 策略。

> [!NOTE]
> 无论是否安装该组件，系统管理员都可以通过 [`DisableAi` 策略](xref:policies) 关闭 Tabular Editor 3 中的所有 AI 功能，包括 MCP 服务器。 `DisableMcpServer` 仅关闭 MCP 服务器。参见 @policies。
