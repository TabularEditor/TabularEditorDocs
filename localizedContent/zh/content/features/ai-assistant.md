---
uid: ai-assistant
title: AI 助手
author: Morten Lønskov
updated: 2026-09-17
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

AI 助手是一款基于聊天的界面，面向 AI 辅助的语义模型开发，旨在帮助你更快创建语义模型。它采用企业级设计，可让你完全掌控发送给 AI 的内容，并内置同意管理，让你可以放心使用 AI 助手。 AI 助手已通过独立的安全渗透测试。详情请访问 [Tabular Editor 信任中心](https://trust.tabulareditor.com)。它可以浏览模型元数据、编写并执行 DAX 查询、生成 C# Script、运行 Best Practice Analyzer 检查、查询 VertiPaq分析器统计信息，并搜索 Tabular Editor 知识库。

AI 助手采用自带密钥 BYOK 模式。你只需从受支持的提供商中选择一个并提供其 API 密钥，助手就会直接通过该提供商的 API 运行。

还有第二种进入方式，完全不需要密钥。从 3.27.0 起，Tabular Editor 3 可以充当 MCP 服务器，因此你已订阅的智能体，如 Claude Code、GitHub Copilot、VS Code 智能体模式、Codex 或 Cursor，都可以通过与聊天相同的工具和相同的权限，在当前打开的模型上工作。参见 @mcp-server。两者共用同一份权限配置，所以无论你用哪一种，只需设置一次权限范围。

> [!NOTE]
> 从 Tabular Editor 3.26.0 开始，AI 助手处于公共预览阶段。我们欢迎你反馈使用体验，帮助我们持续改进。

![AI 助手窗格首次打开时的样子：助手的欢迎语列出了它能做什么——回答问题、查询模型、编写并执行 C# Script、修改模型——以及它不能做什么；下方是一个空白信息框](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 快速入门

1. 打开 **工具 > 偏好 > AI 功能 > AI 助手**
2. 选择 AI 提供商（全新安装时默认是 **无（AI 已禁用）**），然后输入你的 API 密钥
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入一条信息并按 **Enter** 键开始对话

助手当前使用的模型显示在信息框正上方的状态栏中。参见[选择模型](#choosing-a-model)，无需离开聊天即可更改模型。

> [!TIP]
> 使用我们的 [AI 助手交互式演示](https://demos.tabulareditor.com/psl/of150vcy?) 了解如何设置和使用它。

> [!NOTE]
> API 密钥会以加密形式存储在你的本地计算机上。

## 支持的提供程序

在 **工具 > 偏好 > AI 功能 > AI 助手 > AI 提供商** 中配置 AI 提供商。从下拉列表中选择一个提供商（在你完成配置之前，默认值为 **无（AI 已禁用）**），输入 API 密钥，并可选择覆盖默认模型。

将模型字段留空即可使用提供商的默认模型。对于 OpenAI 和 Anthropic，默认值列在下表中；Azure OpenAI 和“自定义”提供商没有默认值，因此这两者的模型字段始终都需要填写。

| 提供程序           | 默认模型                    | 需要配置                          |
| -------------- | ----------------------- | ----------------------------- |
| OpenAI         | gpt-5.5 | API 密钥。可选：基础 URL、组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6       | API 密钥。可选：基础 URL              |
| Azure OpenAI   | 无。必须提供部署名称              | API 密钥、端点 URL 和部署名称           |
| 自定义（兼容 OpenAI） | 无。必须提供模型名称              | API 密钥和自定义端点 URL              |

![AI 提供商偏好页，其中“选择提供商”下拉列表已展开，显示“无（AI 已禁用）”、OpenAI、Anthropic、Azure OpenAI 和“自定义（兼容 OpenAI）”，下方有 URL 和 API 密钥字段](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### 选择模型

当前活动模型显示在信息框上方的状态栏中，位于上下文用量条旁边。点击它会打开一个选择器，列出当前已配置提供商可用的模型；选择后会应用到之后的每个请求，不会弹出对话框，也无需重启。最后一项 **偏好...** 会打开 **工具 > 偏好 > AI 功能 > AI 助手**，用于设置列表中没有的内容。

![信息框上方已打开的模型选择器，其中列出了 claude-sonnet-5、claude-fable-5-1、claude-fable-5、claude-opus-5、claude-haiku-4-5、claude-opus-4-8，以及以粗体显示的当前活动项 claude-sonnet-4-6，底部还有偏好……位于分隔线下方](~/content/assets/images/ai-assistant/ui-model-picker.png)

如果没有可用列表可供选择（例如自定义或 Azure OpenAI 的部署名称，或某台机器从未检索过模型列表），模型名称不会显示为选择器，而是一个指向同一偏好页面的普通链接。

> [!NOTE]
> 只有在提供商、API 密钥和模型都已配置好之后，该指示器才会显示。

### OpenAI

将提供程序选择为 **OpenAI**，然后输入你的 API 密钥。如果你的 OpenAI 账户使用组织 ID 和项目 ID，也可以选择填写这些信息。默认模型为 **gpt-5.5**，但你可以将其更改为你账号下可用的任意模型。

![AI 提供方偏好页面：已选择 OpenAI，显示已遮蔽的 API 密钥，Organization ID 和 Project ID 字段为空，以及模型名称](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供商，然后输入你的 API 密钥。默认模型是 **claude-sonnet-4-6**。你可以将模型名称更改为你账户中可用的任意 Anthropic 模型。

![AI 助手偏好页面：已选择 Anthropic 作为提供方，基础 URL 为 https://api.anthropic.com，显示已遮蔽的 API 密钥，模型名称为 claude-sonnet-4-6](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行每分钟输入 token（ITPM）的速率限制。新创建的 API 密钥起始为 Tier 1，Claude Sonnet 4.x 的 ITPM 上限为 30,000。对大型模型发起的一次请求就可能超过此限制。购买 $40 或以上的 API 额度即可升至第 2 档（450,000 ITPM）。有关各档位的完整详情，请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

选择 **Azure OpenAI** 作为提供商，并配置以下三个字段：

- **API 密钥**：用于访问你的 Azure OpenAI 资源的密钥
- **服务终结点**：你的资源的终结点 URL，例如 `https://your-resource.openai.azure.com`。使用资源 URL，而不要使用 `privatelink` 别名；SSL 证书是为 `*.openai.azure.com` 签发的，直接连接到 `*.privatelink.openai.azure.com` 会导致证书验证失败
- **部署**：填写的是 **部署名称**，不是底层模型名称，也不是资源名称

Azure OpenAI 要求在每次 API 调用中都提供部署名称。部署名称是在创建部署时指定的，因此它可以是任意字符串。部署通常会以其所服务的模型命名（例如 `gpt-4o`），但这只是约定，并非强制要求。如果你输入的是资源名称，或者一个并未作为部署存在的底层模型名称，请求就会失败。

#### 查找部署名称

在 [Azure AI Foundry 门户](https://ai.azure.com) 中：

1. 登录并选择你的 Azure OpenAI 资源
2. 打开 **部署**（如果资源已升级到 Foundry，则为 **模型 + 终结点**）
3. 复制 **名称** 列中的值

在你的组织采用 Azure AI Foundry 之前创建的部署，可能不会在门户中显示。可通过 Azure CLI 列出它们：

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

更多详情见 [创建并部署 Azure OpenAI 资源](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model)。

有关 403 错误、SSL 失败或 "DeploymentNotFound" 响应，请参阅 @azure-openai-connection-errors。

> [!NOTE]
> **Azure OpenAI** 提供程序适用于使用 `api-version` 查询参数的经典 Azure OpenAI 资源。如果你使用的是新的 **Microsoft Foundry**，请参阅下文的[使用 Microsoft Foundry](#using-microsoft-foundry)。

### 自定义（OpenAI 兼容）

“自定义”提供商选项支持本地或组织内部的 LLM，只要它们提供 OpenAI 兼容的 API 端点即可。输入你的 API 密钥和自定义端点 URL。这样你就可以将所有数据保留在自己的基础设施内，以满足数据隐私或合规要求。

### 使用本地或组织内部的 LLM

你可以通过“自定义”提供商让 AI 助手对接自托管的 LLM。这样可确保所有数据都保留在你自己的基础设施内，无论是运行在本地计算机上的模型，还是托管在你所在组织网络中的集中式 LLM。无论哪种方式，都不会将数据发送到第三方云提供商。

以下工具可托管模型并提供 OpenAI 兼容的 API：

- [Ollama](https://ollama.com) — 轻量级 CLI，用于在本地下载并运行模型
- [LM Studio](https://lmstudio.ai) — 带图形界面的桌面应用，用于管理并运行本地模型
- [LocalAI](https://localai.io) — 自托管、社区驱动的替代方案，支持多种模型

这些工具既可以在开发者的工作站上运行供个人使用，也可以部署在组织内的共享服务器上，为你的团队提供集中管理的 LLM 端点。

#### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取一个模型（下载），例如：`ollama pull llama3.1`
3. 启动 Ollama 服务器（安装后会自动运行，默认使用端口 11434）
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:11434/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `llama3.1`）
8. **API 密钥** 字段可设置为任意非空值（例如 `ollama`）。 Ollama 不需要身份验证，但该字段不能为空

#### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 拉取一个模型。可以通过左侧面板的模型搜索页面或 CLI 来完成。例如：`lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 启动 LM Studio 服务器。可以通过左侧面板的开发者页面或 CLI 来完成。例如：`lms server start`
   注意：你需要将其配置为 OpenAI 兼容模式。另外，你可能需要将默认上下文大小调整为 100,000 tokens 以上。
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`）
8. **API 密钥** 字段可设置为任意非空值（例如 `lms`）。 LM Studio 不需要身份验证，但该字段不能为空

> [!NOTE]
> 本地模型的响应质量取决于模型规模以及你的硬件配置。更大的模型通常能产生更好的结果，但需要更多 RAM 和性能更强的 GPU。 AI Assistant 的工具调用能力需要使用支持 OpenAI 兼容格式函数调用的模型。

> [!TIP]
> 我们建议选择参数量至少为 30B 的模型，但理想情况下至少应有 100B 参数。例如，Qwen3.5-122B-A10B 模型在我们的内部测试中表现良好。

### 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com)（前身为 Azure AI Foundry）可让你在 Azure 环境中部署 OpenAI 和 Anthropic 模型。这些模型应通过 Tabular Editor 中的 **OpenAI** 或 **Anthropic** 提供程序访问，而不是 **Azure OpenAI** 提供程序；后者用于经典 Azure OpenAI 资源。

> [!IMPORTANT]
> 不要将 **Azure OpenAI** 提供程序用于 Microsoft Foundry 模型。 **Azure OpenAI** 提供程序仅兼容经典 Azure OpenAI 资源。

#### Microsoft Foundry 上的 OpenAI 模型

要使用部署在 Microsoft Foundry 中的 OpenAI 模型（如 GPT-4o 或 GPT-5.4-mini）：

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **OpenAI**
3. 将 **Base URL** 设置为你的 Foundry 资源端点，并在末尾加上 `/openai/v1`。 URL 采用以下任一格式：
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. 输入 Foundry **API 密钥**
5. 将 **模型名称** 设置为你的部署名称（例如 `gpt-5.4-mini`）

> [!NOTE]
> Microsoft Foundry 门户不会直接显示基础 URL。门户会显示一个包含完整 API 路径的 **目标 URI**（例如 `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`）。基础 URL 只需使用 `https://your-resource.services.ai.azure.com/openai/v1`。

#### Microsoft Foundry 中的 Anthropic 模型

要使用部署在 Microsoft Foundry 中的 Anthropic 模型（例如 Claude Sonnet 4.6）：

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **Anthropic**
3. 将 **基础 URL** 设置为你的 Foundry 资源端点，并在末尾追加 `/anthropic`，例如 `https://your-resource.services.ai.azure.com/anthropic`
4. 输入你的 Foundry **API 密钥**
5. 将 **模型名称** 设置为模型标识符（例如 `claude-sonnet-4-6`）

> [!NOTE]
> 门户会显示一个 **目标 URI**，例如 `https://your-resource.services.ai.azure.com/anthropic/v1/messages`。基础 URL 只需填写到并包含 `/anthropic` 为止。

## 功能

AI 助手可以访问你的模型上下文，并能执行以下操作：

- **模型探索**：查询模型元数据，包括表、列、度量值、关系及其属性
- **DAX 查询编写**：生成 DAX 查询并对你在连接模式下连接的模型执行，结果集会直接在聊天中返回
- **C# Script 生成**：创建用于修改模型的 C# Script。根据你的设置，助手要么在新的编辑器窗口中打开该脚本供你运行，要么自行执行更改。请参阅 [让助手更改你的模型](#letting-the-assistant-change-your-model)。模型元数据更改可通过 **Ctrl+Z** 撤销
- **Best Practice Analyzer**：运行 BPA 分析，查看规则违规情况，并创建或修改 BPA 规则
- **VertiPaq分析器**：查询内存使用统计信息和列的基数
- **文档访问**：读取并修改已打开的文档，例如 DAX 脚本和 DAX 查询
- **知识库搜索**：搜索内置的 Tabular Editor 文档以获取答案
- **UI 导航**：生成 `te3://` 操作链接，用于打开特定的 Tabular Editor 对话框和功能

通过 [MCP 服务器](xref:mcp-server) 连接的代理具备相同能力，但有一个例外：UI 导航只能通过聊天完成。这两种界面都可以通过运行 C# Script 来更改你的模型，而且都会以单个可撤销的步骤执行。不同之处在于，系统如何向你呈现更改，以及如何获得你的许可。请参阅 [通过 MCP 服务器共享的内容，以及不会共享的内容](#what-the-mcp-server-shares-and-what-it-does-not)。

> [!NOTE]
> 在处理未连接到 Analysis Services 或 Power BI 的模型文件(例如 `.bim` 文件或 `.tmdl` 文件夹)时，凡是需要活动数据库连接的工具(包括 DAX 查询执行和 VertiPaq分析器统计信息)都会自动隐藏。助手仍会为你编写 DAX 查询，但在建立连接之前，DAX 查询项上的 **Execute** 按钮将处于禁用状态。如果之前已从 `.vpax` 文件加载过，VertiPaq分析器统计信息仍然可用。

## 让助手更改你的模型

默认情况下，助手会编写一个 C# Script，并在编辑器窗口中打开，供你阅读和运行。从 Tabular Editor 3.27.0 起，它也可以改为直接替你执行更改。

在 **工具 > 偏好 > AI 功能 > AI 助手** 下勾选 **Allow AI assistant to run C# scripts directly**。该设置默认关闭，需由你手动开启；并且只有在 **工具 > 偏好 > AI 功能 > 权限** 下将 **模型元数据** 设为 **写入** 后，此复选框才可用。

### 当助手运行脚本时会发生什么

- **你会先看到更改。** 默认开启 **Preview changes** 时，会在任何更改生效之前弹出[预览对话框](xref:csharp-scripts#run-c-scripts-with-preview)。选择 **取消** 会将模型还原，并告知助手你已拒绝该更改，因此它会询问应如何调整，而不是再次尝试同样的操作。关闭该偏好后，更改会直接应用，不会显示对话框。
- **一步撤销。** 脚本执行的所有操作都会合并为撤销历史中的一条记录，名称为 _C# Script (AI Assistant)_。按一次 **Ctrl+Z** 即可将模型还原。
- **要么全部成功，要么完全不改动。** 执行到一半失败的脚本不会修改模型，助手会报告错误，而不会留下只完成一半的编辑。
- **只有模型内的操作会按这种方式运行。** 涉及文件、网络或外部程序集的脚本绝不会替你执行。它会以脚本项的形式返回，带有 **Unsafe** 徽章，且 **Execute** 按钮处于禁用状态；助手还会说明脚本使用了哪些内容。

如果你要求的是脚本而不是直接更改，助手仍会给你一个脚本。_给我写个脚本，把所有度量值重命名为句首大写格式_ 会打开一个脚本文档供你自行运行，不管该设置如何设置。

管理员可以通过 `DisableCSharpScripts` [策略](xref:policies) 完全禁止此功能，这也会阻止助手为你编写可供你自行运行的脚本。

管理员也可以通过 `BlockUnsafeScripts` 策略允许脚本功能，但将其限制在模型内部。在该策略下，任何涉及文件、网络或外部程序集的脚本都会被直接拒绝，而不会交给你审核，无论它来自何处。见[管理员策略](xref:csharp-scripts#administrator-policies)。

## 对话

AI 助手支持多个同时进行的对话。每个对话都会维护各自的信息历史记录和上下文。

- 对话会跨会话保留，并存储在本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 标题会在首次交流后自动生成。你可以手动重命名对话
- **自动压缩**：当对话接近上下文窗口限制时，较早的信息会被自动汇总，以释放空间。在压缩之前，会先归档完整对话的快照。阈值在[上下文压缩](#context-compaction)中设置，以模型自身上下文窗口的百分比表示

### 删除对话

**删除对话** 位于 AI 助手工具栏左端，紧邻 **新建对话**。系统会先要求你确认。

该对话及其历史记录会从磁盘中删除，且无法恢复。如果你想隐藏 AI 助手面板而不删除任何内容，可以使用面板标题栏上的关闭按钮，或者选择 **视图 > AI 助手**。

## 工件

当 AI 助手生成代码时，会生成可直接在编辑器窗口中打开的 **工件**：

- **C# Script**：在新的 C# Script 编辑器中打开，支持语法高亮、编译和执行
- **DAX 查询**：在新的 DAX 查询编辑器中打开，支持语法高亮和执行

生成物会在 AI 生成过程中实时流式输出。 C# Script 生成物包含安全分析，可标记潜在不安全的代码（例如文件系统访问或网络操作）。

![AI 助手窗格，显示生成的 C# Script 产物及其“执行”按钮，以及助手对该脚本作用的说明和随附的大小写敏感提示](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

当你从聊天中执行 C# Script 时，**脚本预览**对话框会并排显示该脚本对模型元数据所做的所有更改的差异对比。你可以接受这些更改，或将其撤销。详见[使用预览运行脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![“脚本预览 - 模型更改”对话框：左右并排显示更改前后的模型；其中 Internet Total Freight 度量值的格式字符串已更改，并新增了说明和显示文件夹，且每项更改都标注了对应的原始值](~/content/assets/images/preview-script-changes.png)

## 自定义指令

自定义指令是一组用于在特定任务中引导 AI 助手行为的指令。系统会先向助手提供所有可用指令的列表，助手只会加载它认为与你的请求相关的那些指令的全文。指令一旦加载，就会在该对话的剩余过程中持续生效。

> [!IMPORTANT]
> `description` 现在是助手在决定是否使用某条指令时唯一会读取的内容，所以要确保它准确且具体。

### 内置自定义指令

AI 助手包含以下内置自定义指令：

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

自定义指令会在助手回复上方以指示器形式显示，用于说明哪些指令影响了本次回复。你可以在 **工具 > 偏好 > AI 功能 > AI 助手 > 偏好 > 显示自定义指令指示器** 中打开或关闭该指示器的显示。

### 调用自定义指令

输入 `/` 浏览可用的自定义指令；或在信息开头输入完整的 `/instruction-id`，以明确调用某条特定指令。例如，`/dax-querying` 会强制使用 DAX 查询指令，无论信息内容如何。如果你在 `/id` 后面什么都不输入，助手就只会使用该指令。

当你想确保该指令确实生效时，仍然建议使用显式调用。显式调用的指令会在后续整个对话中持续生效，就像自动加载的指令一样。

### 添加自己的自定义指令

你可以将 `.md` 文件放到 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 中，以创建自定义指令。该文件夹会在 AI 助手首次运行时创建，其中包含一个可供参考和复制的 `example.md` 文件。在 AI 助手工具栏中选择 **打开自定义指令文件夹** 即可打开该文件夹。

每个文件都可以以 YAML frontmatter 开头，用于定义指令元数据。这些都不是必需的：

```yaml
---
id: my-custom-instruction
name: My Custom Instruction
description: A brief description shown in the autocomplete popup.
priority: 100
always_inject: false
hidden: false
---

你的指令内容写在这里。当该指令被激活时，这段文本会
注入到 AI 的系统提示词中。
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

关于文件读取方式的说明：

- Frontmatter 必须从文件第一行的 `---` 开始，并以另一行 `---` 结束。如果没有，或者 YAML 无法解析，则会将整个文件视为指令内容，并应用上述所有默认值
- 上表中未列出的键会被忽略。这也正是残留的 `triggers:` 部分不会造成影响的原因
- 正文中出现的任何 `{{version}}` 都会被替换为 Tabular Editor AI 组件的版本号
- 只会读取该文件夹下直接包含的 `.md` 文件，不会搜索子文件夹

### 来自你所在组织的自定义说明

管理员可以通过 `AiCustomInstructionsPath` [策略](xref:policies) 发布一个供所有人使用的自定义说明文件夹。它可以是只读的网络共享。除了内置说明外，这些说明也会为所有用户加载，用法与其他说明完全相同：会出现在 `/` 自动补全中，可按描述选择，也可通过 `/id` 调用。

如果同一个 `id` 同时存在于多个位置，最终生效的是：

1. 你所在组织的文件夹
2. 你自己的文件夹
3. 内置说明

因此，组织级说明会覆盖同名的内置说明和用户自己的文件。另一项策略 `DisableUserCustomInstructions` 会让 Tabular Editor 完全忽略你个人文件夹中的说明，并禁用 **Open Custom Instructions Folder**；内置说明和组织说明仍会继续加载。

这两项策略都需要 Tabular Editor 3 企业版。

## 权限与同意

AI 助手可访问的范围由 _五类资源_ 决定，每类资源对应一个访问级别。同样的五项授权也适用于 [MCP 服务器](xref:mcp-server)，因此查看和更改都只需在一个地方进行。

| 资源                         | 涵盖内容                                                | 级别           | 默认值    |
| -------------------------- | --------------------------------------------------- | ------------ | ------ |
| **模型元数据**                  | 表、列和度量值的名称、表达式、描述等。“读取”权限还包括 VertiPaq分析器的统计信息       | 拒绝 / 读取 / 写入 | **读取** |
| **模型数据**                   | 模型中的数据值，例如 DAX 查询结果。需要实时连接                          | 拒绝 / 读取      | **拒绝** |
| **Best Practice Analyzer** | 读取可列出规则并运行分析；写入可添加或修改规则                             | 拒绝 / 读取 / 写入 | **读取** |
| **文档**                     | 你已打开的文档编辑器：C# Script 和 DAX 查询。读取可访问其内容；创建或修改则需要写入权限 | 拒绝 / 读取 / 写入 | **写入** |
| **宏**                      | 你的宏库。读取可列出并读取宏；写入权限为未来的宏编辑工具预留                      | 拒绝 / 读取 / 写入 | **写入** |

**写入**授权已包含读取权限，因此无需同时授予两项权限。**模型数据**本质上是只读的（助手可以查询你的数据，但无法将值写回），因此只提供“拒绝”和“读取”。

> [!NOTE]
> **模型数据**是默认被拒绝的唯一资源。元数据描述的是你的模型；数&#x636E;_&#x5C31;&#x662F;_&#x6A21;型的内容，因此是否将其发送给 AI 提供商，应当由你慎重决定，而不是沿用默认设置。

有三项授权值得仔细看看：

- **模型元数据 > 写入**允许助手更改你的模型。单就这一点而言，这意味着助手会编写一个 C# Script，然后交给你运行。它也是实现[直接执行](#letting-the-assistant-change-your-model)所需的授权；不过，只有在你另外单独开启该功能后，助手才会自行运行脚本。无论哪种方式，只有经静态判定为安全的脚本才会运行；任何试图跳出模型、访问文件系统或网络的脚本，都绝不会替你执行。
- **Best Practice Analyzer > 读取** 允许助手运行分析，但运行时还需要 **模型元数据 > 读取**，因为分析会读取模型。
- 仅有 **模型数据 > 读取** 并不足以运行 DAX 查询：还需要 **模型元数据 > 读取**，因为查询可通过 `INFO` 函数、DMVs 以及其结果中的列名来读取元数据。

### 设置权限授予

打开 **工具 > 偏好 > AI 功能 > 权限**。每个资源都有一个下拉菜单，列出其可用级别。

![AI 功能 > 权限偏好设置，每个资源一个下拉菜单，默认值](~/content/assets/images/pref-ai-permissions.png)

没有单独的“询问我”级别。**拒绝** 就相当于“询问我”：在聊天中，当需要使用你尚未授权的资源时，会立即出现一张权限卡片。在 MCP 环境下，由于没有人可询问，被拒绝资源对应的工具将不可用。

> [!NOTE]
> 如果你在 3.27.0 之前使用过 AI 助手，就会注意到提示变少了。模型元数据、文档和宏现在的起始级别为“读取”或更高，因此聊天不再为它们请求授权。默认情况下，只有 DAX 查询结果和对 Best Practice Analyzer 规则的编辑仍会弹出卡片。将某个资源设为 **拒绝**，就能让它重新弹出提示。

> [!NOTE]
> 在企业版中，IT 管理员可以设置策略来决定这些权限。参见 @policies。

### 聊天中的权限卡片

当助手需要的资源超出你当前授权的范围时，会在对话中显示一张 **需要权限** 卡片，说明它想执行的操作，例如“AI 希望访问你的语义模型的元数据”，或显示它建议运行的 DAX 查询。

![聊天中的“需要权限”卡片，显示助手想要运行的 DAX 查询，并带有“允许”“在本次会话中允许”“对此模型允许”“始终允许”和“拒绝”按钮](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| 按钮           | 作用                                                                                            |
| ------------ | --------------------------------------------------------------------------------------------- |
| **允许**       | 仅当前这一轮。在完成你让它做的事时，助手可能会重复相同的请求，之后不会记住任何内容                                                     |
| **在本次会话中允许** | 直到重启 Tabular Editor 为止。仅保存在内存中，从不写入磁盘                                                         |
| **仅对该模型允许**  | 会记录在该模型的 [用户选项](xref:user-options) 文件中，因此下次打开该模型时仍会生效。仅针对 **模型元数据** 和 **模型数据** 提供，且仅在已加载模型时可用 |
| **始终允许**     | 在“权限”页中提高常设授权级别，对所有模型和所有会话生效                                                                  |
| **拒绝**       | 拒绝此请求。助手会在没有该访问权限的情况下继续，并在下次再询问                                                               |

**始终允许** 只会提高授权，不会降低授权：授予 Read 不会缩减你已有的 Write 授权。

你完全不必回应这张卡片。见下文的[在权限待定时停止当前轮次](#stopping-a-turn-while-permission-is-pending)。

### MCP 服务器会共享哪些信息，以及不会共享哪些信息

[MCP 服务器](xref:mcp-server)读取的是同样的五项授权，但不会使用卡片式流程。通过 MCP 连接的代理是无人值守的，因此没有人可供询问：

- 授权会在服务器启动时被快照保存，并在服务器整个运行期间决定其可用工具范围。服务器运行期间更改授权不会生效，直到你重启它。
- 只会读取全局授权。你通过 **仅对该模型允许** 授予的权限，以及会话级授权，都只对该聊天生效，绝不会传递给 MCP 代理。
- 被拒绝的资源对应的工具根本不会提供给代理，而不是先提供再拒绝。

### 撤销权限

在“权限”页中将该资源重新设为 **拒绝**。聊天会在下次需要该资源时再次询问；正在运行的 MCP 服务器会一直保留其启动时拥有的访问权限，直到你重启它。

降低全局授权不会清除按模型授予的权限。若要撤销其中一项，请删除模型的 `.tmuo` 文件，或删除其中的 `Permissions` 条目。详情见 @user-options。

### 审计记录

在 Tabular Editor 3 企业版中，会在本地保留一份记录，记录 AI 助手和 [MCP 服务器](xref:mcp-server) 的操作：请求了哪些权限以及你如何回应，运行了哪些工具以及各自是成功、失败还是被拒绝，以及任何已运行或提交给你审阅的 C# Script 的全文。你的提示词、助手的回复以及模型中的数据值都不会被记录。**工具 > 偏好 > AI 功能** 下的 **打开审计文件夹** 可打开这些文件所在的位置。

在 Desktop 版和商业版中，以及在许可证激活前，不会记录任何内容，不会创建文件夹，也不会显示该按钮。

见 @ai-audit-log，了解每条记录包含什么、文件存放在哪里，以及重定向这些文件的策略。

### 在等待权限时停止当前轮次

**需要权限** 卡片会等待你的答复，助手才能继续。你不必回答：按 **停止** 会结束当前轮次、移除该卡片，并将该请求视为已拒绝。面板会恢复正常状态，你可以在同一对话中发送新信息继续。

## 偏好设置

在 **工具 > 偏好 > AI 功能 > AI Assistant > 偏好** 中配置 AI 助手的显示与行为选项。

### 聊天显示

| 偏好         | 默认值  | 说明               |
| ---------- | ---- | ---------------- |
| 显示选择上下文指示器 | true | 在聊天中显示当前选定的模型对象  |
| 显示自定义指令指示器 | true | 在助手回复上方显示自定义指令标识 |
| 显示知识库搜索指示器 | true | 搜索知识库时显示进度       |

### 上下文压缩

| 偏好       | 默认值  | 说明                                               |
| -------- | ---- | ------------------------------------------------ |
| 自动压缩     | true | 接近上下文限制时自动摘要较早的信息                                |
| 自动压缩阈值 % | 80   | 达到模型自身上下文窗口的这一百分比时，将触发自动压缩。 50-100 以外的数值不会产生额外效果 |

### C# Script

| 偏好                     | 默认值   | 说明                                                                                                                                                                                |
| ---------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 允许 AI 助手直接运行 C# Script | false | 让助手直接执行模型更改，而不是打开脚本让你自行运行。在 **权限** 下将 **模型元数据** 设为 **写入** 之前，此项不可用；若启用了 `DisableCSharpScripts` [策略](xref:policies)，则始终不可用。见 [让助手更改你的模型](#letting-the-assistant-change-your-model) |
| 预览更改                   | true  | 在聊天中执行 AI 生成的 C# Script 时，显示“预览更改”对话框                                                                                                                                             |

还有两个设置位于 **AI 功能** 页面本身、在 **AI Assistant** 上方，因为它们同样适用于 MCP 服务器：_启动时检查知识库更新_，以及 **打开审计文件夹** 按钮。见 @preferences。

![AI Assistant 偏好页面，其中包含三个聊天显示指示器、自动压缩及其阈值，以及两个 C# Script 设置：未勾选“允许 AI 助手直接运行 C# Script”，已勾选“预览更改”】【](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token 使用量

每条发给 AI 助手的信息都会消耗输入 token。单条信息的 token 成本取决于包含了哪些上下文：

- **系统提示词和自定义说明**：每条信息都会一并发送。通常为 5,000 到 15,000 个 token，具体取决于启用了哪些自定义说明。
- **模型元数据**：当助手需要了解你的模型时，会通过工具调用提取元数据。为避免在处理大型模型时超出提供商的速率限制，助手会采用逐步披露的方式。也就是说，它会先获取一个轻量概览（表名、度量值名和关系），再按名称、描述或 DAX 表达式搜索相关对象，并且仅在问题需要时，才会深入查看特定表或对象的完整详情。原本会非常庞大的工具结果会被截断，并附带说明助手如何检索其余数据。

### 令牌计数器

令牌计数器位于信息框上方的状态栏中，紧挨着[当前模型指示器](#choosing-a-model)。该指示条会以千个令牌为单位显示 _已用_ / _总计_，并会随着上下文逐渐填满而变为绿色、琥珀色或红色。数字前出现 `±` 表示目前还无法提供精确计数。

将鼠标悬停在上面，可查看分为三个带标签部分的明细：

| 部分           | 涵盖内容                                       |
| ------------ | ------------------------------------------ |
| **上一轮**      | 最近一次交互的开销：新输入、从提供方的提示缓存中读取的令牌、写入缓存的令牌，以及输出 |
| **本次对话（计费）** | 同样的四项数字，累计整个对话中的每次请求，包括工具往返调用              |
| **上下文**      | 当前位于上下文窗口中的令牌数，并与该窗口的实际大小对照                |

某一行可能会显示为：`37,588 input + 131,744 cached · write 37,558 · output 2,866`。对于不支持提示缓存的提供方，不会显示缓存相关部分；而某个部分如果没有可 Report 的内容，则会被完全省略。

> [!TIP]
> 将上一轮与整个对话的总计分开显示，你就能判断一个简短的追问是否真的开销很大。在较长的对话中，**本次对话（计费）** 数字很大而 **上一轮** 数字很小，这很正常。

### 上下文窗口

上下文使用条、自动压缩触发点以及单次回复的最大长度，都会遵&#x5FAA;_&#x5F53;前所用模型的实际上下文窗口_，而不是某个固定数值。具有一百万令牌窗口的模型，会以一百万令牌作为度量值来计量。

如果无法得知模型的实际上下文窗口（例如使用 Azure OpenAI 或 Custom 部署名称，或在从未获取过模型目录的计算机上），Tabular Editor 会默认回退为 200,000 个令牌。

### 减少 token 使用量

提问前，先在 **TOM Explorer** 中选择特定对象。选中对象后，助手会将上下文限定在这些对象上，而不是拉取整个模型的元数据。这是同时减少 token 使用量和 API 成本的最有效方式。

其他减少 token 使用量的方法：

- 围绕特定的表、度量值或列提出更聚焦的问题，而不是对整个模型提出泛泛的问题。像 _“为所有度量值设置显示文件夹”_ 这样含糊的提示，会迫使助手检索整个模型的元数据。像 _“为我选中的度量值设置显示文件夹”_ 这样具体的提示，会将上下文限制在当前选择范围内，并且消耗的 token 少得多
- 切换话题时开启新对话，避免累积过长的对话历史
- 进行探索性提问时，使用更小或成本更低的模型

## 局限性

- 需要用户提供 API 密钥。不包含内置 API 密钥
- AI 的响应取决于所选模型及提供商的能力
- 可用的上下文窗口以所选模型自身为准；如果 Tabular Editor 无法确定，则默认假定为 200,000 个令牌
- AI 助手不能替代你对 DAX 和语义模型设计基础的理解
- 响应质量会因提供商和模型选择而异
- AI 助手无法连接到外部文件或服务，也无法搜索网页
- AI 助手无法连接到外部 MCP 服务器来扩展自身的工具集。这里说的只是聊天功能：Tabular Editor 3 本身可充当 MCP 服务器，因此你自己的代理可以对当前打开的模型进行操作。参见 @mcp-server
- AI 助手无法在聊天中切换到其他模型。使用 Tabular Editor 的用户界面更改模型连接
- AI 助手无法管理偏好

## 禁用 AI 助手

AI 助手是一个可选组件，自 Tabular Editor 3.27.0 起默认随产品安装。你可以再次运行 Tabular Editor 3 安装程序，修改现有的 Tabular Editor 3 安装，以包含或排除 AI 助手组件。如果你使用的是 Tabular Editor 3 便携版，可以从安装目录中删除名为 `TabularEditor3.AI.dll` 的文件来移除 AI 助手组件。

AI 助手和 MCP 服务器包含在同一个组件中，因此排除该组件或删除 `TabularEditor3.AI.dll` 会同时移除两者。要在保留 MCP 服务器的同时关闭聊天功能，请保留该组件，并使用 `DisableAiChat` 策略。

> [!NOTE]
> 无论是否安装 AI 助手组件，系统管理员都可以通过指定 [`DisableAi` 策略](xref:policies) 来禁用 Tabular Editor 3 中的所有 AI 功能，包括 MCP 服务器。 `DisableAiChat` 仅关闭聊天功能，`DisableMcpServer` 仅关闭 MCP 服务器。请参阅 @policies。
