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

There is a second way in that needs no key at all. From 3.27.0 Tabular Editor 3 can act as an MCP server, so an agent you already subscribe to, such as Claude Code, GitHub Copilot, VS Code agent mode, Codex or Cursor, works on the open model through the same tools and the same permissions as the chat. See @mcp-server. The two share one permission record, so whichever you use, you set the boundaries once.

> [!NOTE]
> 从 Tabular Editor 3.26.0 开始，AI 助手处于公共预览阶段。我们欢迎你反馈使用体验，帮助我们持续改进。

![The AI Assistant pane as it first opens, with the assistant's greeting listing what it can do - answer questions, query the model, write and execute C# scripts, change the model - and what it cannot, above an empty message box](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 快速入门

1. Open **Tools > Preferences > AI Features > AI Assistant**
2. Select your AI provider (on a fresh install this defaults to **None (AI disabled)**), then enter your API key
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入一条信息并按 **Enter** 键开始对话

The model the assistant is using is shown in the status strip directly above the message box. See [Choosing a model](#choosing-a-model) to change it without leaving the chat.

> [!TIP]
> 使用我们的 [AI 助手交互式演示](https://demos.tabulareditor.com/psl/of150vcy?) 了解如何设置和使用它。

> [!NOTE]
> API 密钥会以加密形式存储在你的本地计算机上。

## 支持的提供程序

Configure your AI provider under **Tools > Preferences > AI Features > AI Assistant > AI Provider**. Select a provider from the dropdown (the default is **None (AI disabled)** until you configure one), enter your API key and optionally override the default model.

Leave the model field blank to use the provider's default model. For OpenAI and Anthropic the defaults are listed in the table below; Azure OpenAI and the Custom provider have no default, so those two always need a value.

| 提供程序           | 默认模型                             | 需要配置                          |
| -------------- | -------------------------------- | ----------------------------- |
| OpenAI         | gpt-5.5          | API 密钥。可选：基础 URL、组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6                | API 密钥。可选：基础 URL              |
| Azure OpenAI   | 无。 A deployment name is required | API 密钥、端点 URL 和部署名称           |
| 自定义（兼容 OpenAI） | 无。 A model name is required      | API 密钥和自定义端点 URL              |

![The AI Provider preferences page with the Choose provider dropdown open on None (AI disabled), OpenAI, Anthropic, Azure OpenAI and Custom (OpenAI-compatible), and a URL and API Key field beneath it](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### Choosing a model

The active model is shown in the status strip above the message box, next to the context usage bar. Click it to open a picker listing the models currently available for the configured provider; choosing one applies to every request that follows, with no dialog and no restart. The last entry, **Preferences...**, opens **Tools > Preferences > AI Features > AI Assistant** for anything not on the list.

![The model picker open above the message box, listing claude-sonnet-5, claude-fable-5-1, claude-fable-5, claude-opus-5, claude-haiku-4-5, claude-opus-4-8 and the active claude-sonnet-4-6 in bold, with Preferences... beneath a separator](~/content/assets/images/ai-assistant/ui-model-picker.png)

Where there is no list to offer (a Custom or Azure OpenAI deployment name, or a machine where the model list has never been retrieved), the model name is a plain link to those same preferences instead of a picker.

> [!NOTE]
> The indicator is hidden until a provider, an API key and a model are all in place.

### OpenAI

将提供程序选择为 **OpenAI**，然后输入你的 API 密钥。如果你的 OpenAI 账户使用组织 ID 和项目 ID，也可以选择填写这些信息。默认模型为 **gpt-5.5**，但你可以将其更改为你账号下可用的任意模型。

![The AI Provider preferences page with OpenAI selected, a masked API key, empty Organization ID and Project ID fields, and the model name](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供商，然后输入你的 API 密钥。默认模型是 **claude-sonnet-4-6**。你可以将模型名称更改为你账户中可用的任意 Anthropic 模型。

![The AI Assistant preferences page with Anthropic selected as the provider, the base URL https://api.anthropic.com, a masked API key and claude-sonnet-4-6 as the model name](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行每分钟输入 token（ITPM）的速率限制。新创建的 API 密钥起始为 Tier 1，Claude Sonnet 4.x 的 ITPM 上限为 30,000。对大型模型发起的一次请求就可能超过此限制。购买 $40 或以上的 API 额度即可升至第 2 档（450,000 ITPM）。有关各档位的完整详情，请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

选择 **Azure OpenAI** 作为提供商，并配置以下三个字段：

- **API key**: the access key for your Azure OpenAI resource
- **Service endpoint**: the endpoint URL for your resource, for example `https://your-resource.openai.azure.com`. 使用资源 URL，而不要使用 `privatelink` 别名；SSL 证书是为 `*.openai.azure.com` 签发的，直接连接到 `*.privatelink.openai.azure.com` 会导致证书验证失败
- **Deployment**: the **deployment name**, not the underlying model name and not the resource name

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

你可以通过“自定义”提供商让 AI 助手对接自托管的 LLM。 This keeps all data within your own infrastructure, whether that is a model running on your local machine or a centrally hosted LLM within your organization's network. 无论哪种方式，都不会将数据发送到第三方云提供商。

以下工具可托管模型并提供 OpenAI 兼容的 API：

- [Ollama](https://ollama.com): lightweight CLI for downloading and running models locally
- [LM Studio](https://lmstudio.ai): desktop application with a graphical interface for managing and running local models
- [LocalAI](https://localai.io): self-hosted, community-driven alternative with broad model support

这些工具既可以在开发者的工作站上运行供个人使用，也可以部署在组织内的共享服务器上，为你的团队提供集中管理的 LLM 端点。

#### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. 拉取一个模型（下载），例如：`ollama pull llama3.1`
3. 启动 Ollama 服务器（安装后会自动运行，默认使用端口 11434）
4. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:11434/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `llama3.1`）
8. The **API Key** field can be set to any non-empty value (e.g. `ollama`). Ollama does not require authentication, but the field cannot be left blank

#### 示例：LM Studio

1. [下载并安装 LM Studio](https://lmstudio.ai/download)
2. 拉取一个模型。可以通过左侧面板的模型搜索页面或 CLI 来完成。例如：`lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. 启动 LM Studio 服务器。可以通过左侧面板的开发者页面或 CLI 来完成。例如：`lms server start`
   注意：你需要将其配置为 OpenAI 兼容模式。另外，你可能需要将默认上下文大小调整为 100,000 tokens 以上。
4. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. 将 **Model name** 设置为你拉取的模型（例如 `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`）
8. The **API Key** field can be set to any non-empty value (e.g. `lms`). LM Studio does not require authentication, but the field cannot be left blank

> [!NOTE]
> 本地模型的响应质量取决于模型规模以及你的硬件配置。更大的模型通常能产生更好的结果，但需要更多 RAM 和性能更强的 GPU。 AI Assistant 的工具调用能力需要使用支持 OpenAI 兼容格式函数调用的模型。

> [!TIP]
> 我们建议选择参数量至少为 30B 的模型，但理想情况下至少应有 100B 参数。例如，Qwen3.5-122B-A10B 模型在我们的内部测试中表现良好。

### 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com)（前身为 Azure AI Foundry）可让你在 Azure 环境中部署 OpenAI 和 Anthropic 模型。 These models are accessed through the **OpenAI** or **Anthropic** provider in Tabular Editor, not the **Azure OpenAI** provider, which is for classic Azure OpenAI resources.

> [!IMPORTANT]
> 不要将 **Azure OpenAI** 提供程序用于 Microsoft Foundry 模型。 **Azure OpenAI** 提供程序仅兼容经典 Azure OpenAI 资源。

#### Microsoft Foundry 上的 OpenAI 模型

要使用部署在 Microsoft Foundry 中的 OpenAI 模型（如 GPT-4o 或 GPT-5.4-mini）：

1. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
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

1. In Tabular Editor, go to **Tools > Preferences > AI Features > AI Assistant > AI Provider**
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
- **C# script generation**: Create C# scripts for model modifications. The assistant either opens the script in a new editor window for you to run, or carries the change out itself, depending on your settings. See [Letting the assistant change your model](#letting-the-assistant-change-your-model). 模型元数据更改可通过 **Ctrl+Z** 撤销
- **Best Practice Analyzer**：运行 BPA 分析，查看规则违规情况，并创建或修改 BPA 规则
- **VertiPaq分析器**：查询内存使用统计信息和列的基数
- **文档访问**：读取并修改已打开的文档，例如 DAX 脚本和 DAX 查询
- **知识库搜索**：搜索内置的 Tabular Editor 文档以获取答案
- **UI 导航**：生成 `te3://` 操作链接，用于打开特定的 Tabular Editor 对话框和功能

An agent connected over the [MCP server](xref:mcp-server) is offered the same capabilities, with one exception: UI navigation is chat-only. Both surfaces can change your model by running a C# script, and both do it as a single undoable step. What differs is how the change is put to you, and how permission is settled. See [What the MCP server shares, and what it does not](#what-the-mcp-server-shares-and-what-it-does-not).

> [!NOTE]
> Tools that require an active database connection, including DAX query execution and VertiPaq Analyzer statistics, are automatically hidden when working with a model file (for example a `.bim` or `.tmdl` folder) that is not connected to Analysis Services or Power BI. The assistant still writes DAX queries for you, but the **Execute** button on DAX query artifacts is disabled until a connection is established. 如果之前已从 `.vpax` 文件加载过，VertiPaq分析器统计信息仍然可用。

## Letting the assistant change your model

By default the assistant writes a C# script and opens it in an editor window for you to read and run. From Tabular Editor 3.27.0 it can carry the change out itself instead.

Tick **Allow AI assistant to run C# scripts directly** under **Tools > Preferences > AI Features > AI Assistant**. The setting is off until you turn it on, and the checkbox is unavailable until **Model metadata** is set to **Write** under **Tools > Preferences > AI Features > Permissions**.

### What happens when the assistant runs a script

- **You see the change first.** With **Preview changes** on, which is the default, the [preview dialog](xref:csharp-scripts#run-c-scripts-with-preview) appears before anything stands. Choosing **Cancel** puts the model back and tells the assistant you rejected the change, so it asks what to do differently rather than trying the same thing again. With the preference off, the change is applied without a dialog.
- **One undo step.** Everything the script did collapses into a single entry named _C# script (AI Assistant)_. One **Ctrl+Z** puts the model back.
- **All or nothing.** A script that fails part way through leaves the model untouched, and the assistant reports the error rather than leaving you with half an edit.
- **Only model work runs this way.** A script that reaches for files, the network or an external assembly is never executed for you. It comes back as a script artifact carrying an **Unsafe** badge with **Execute** disabled, and the assistant tells you what it used.

Asking for a script rather than for the change still gives you a script. _Write me a script that renames every measure to sentence case_ opens a script document for you to run yourself, whatever this setting says.

Administrators can prevent this entirely with the `DisableCSharpScripts` [policy](xref:policies), which also stops the assistant writing scripts for you to run.

They can also allow scripting but keep it inside the model, with the `BlockUnsafeScripts` policy. Under it a script that reaches for files, the network or an external assembly is refused outright rather than handed to you for review, wherever it came from. See [Administrator policies](xref:csharp-scripts#administrator-policies).

## 对话

AI 助手支持多个同时进行的对话。每个对话都会维护各自的信息历史记录和上下文。

- 对话会跨会话保留，并存储在本地的 `%LocalAppData%\TabularEditor3\AI\Conversations\` 中
- 标题会在首次交流后自动生成。你可以手动重命名对话
- **Auto-compaction**: when the conversation approaches the context window limit, older messages are automatically summarized to free up space. A snapshot of the full conversation is archived before compaction. The threshold is set under [Context Compaction](#context-compaction), and is a percentage of the model's own context window

### Deleting a conversation

**Delete conversation** sits at the left-hand end of the AI Assistant toolbar, next to **New conversation**. It asks for confirmation first.

The conversation and its history are removed from disk and cannot be recovered. To hide the AI Assistant panel instead of deleting anything, use the close button on the panel's title bar, or **View > AI Assistant**.

## 工件

当 AI 助手生成代码时，会生成可直接在编辑器窗口中打开的 **工件**：

- **C# Script**：在新的 C# Script 编辑器中打开，支持语法高亮、编译和执行
- **DAX 查询**：在新的 DAX 查询编辑器中打开，支持语法高亮和执行

生成物会在 AI 生成过程中实时流式输出。 C# Script 生成物包含安全分析，可标记潜在不安全的代码（例如文件系统访问或网络操作）。

![The AI Assistant pane showing a generated C# script artifact with an Execute button, and the assistant's explanation of what the script does and the case-sensitivity caveat it comes with](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

当你从聊天中执行 C# Script 时，**脚本预览**对话框会并排显示该脚本对模型元数据所做的所有更改的差异对比。你可以接受这些更改，或将其撤销。详见[使用预览运行脚本](xref:csharp-scripts#run-c-scripts-with-preview)。

![The Script Preview - Model Changes dialog, the model before and after side by side, with the Internet Total Freight measure's format string changed and a description and a display folder added, each marked against its original](~/content/assets/images/preview-script-changes.png)

## 自定义指令

自定义指令是一组用于在特定任务中引导 AI 助手行为的指令。 The assistant is given a list of every available instruction and only loads the full text of the ones it judges relevant to your request. Once an instruction has been loaded it stays in effect for the rest of the conversation.

> [!IMPORTANT]
> The `description` is now the only thing the assistant reads when deciding if an instruction should be used, so keep yours accurate and specific.

### 内置自定义指令

AI 助手包含以下内置自定义指令：

| 自定义指令                            | Invoke with           | Covers                                                                                                                                               |
| -------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| DAX 查询                           | `/dax-querying`       | Writing and executing DAX queries: column and measure qualification, verifying filter values, validating and updating queries        |
| 模型修改                             | `/model-modification` | C# scripts that create or change model objects: TOMWrapper API patterns, execution order, idempotent updates, naming rules           |
| Semantic Model Design            | `/model-design`       | Star schema, relationships and cross-filtering, date tables, measures versus calculated columns, calculation groups, naming                          |
| Semantic Model Organization      | `/organize-model`     | Auditing and tidying model metadata: naming conventions, table groups, display folders, hidden columns, format strings, descriptions |
| Semantic Model Size Optimization | `/optimize-model`     | Reducing model memory and size: VertiPaq measurement, column removal, data type tuning, structural changes, SKU limits               |
| 宏                                | `/macros`             | Reusable C# macros for the Macros window: selection contexts, generic-code rules                                                     |
| DAX 用户自定义函数                      | `/udf`                | Writing DAX UDFs: syntax, `VAL`/`EXPR` parameter modes, type hints, namespaces, DaxLib                                               |
| 最佳实践分析器                          | `/bpa`                | Reviewing violations and writing custom rules as LINQ Dynamic expressions                                                                            |

自定义指令会在助手回复上方以指示器形式显示，用于说明哪些指令影响了本次回复。 You can toggle this display in **Tools > Preferences > AI Features > AI Assistant > Preferences > Show custom instructions indicator**.

### 调用自定义指令

输入 `/` 浏览可用的自定义指令；或在信息开头输入完整的 `/instruction-id`，以明确调用某条特定指令。例如，`/dax-querying` 会强制使用 DAX 查询指令，无论信息内容如何。 If you type nothing after the `/id`, the assistant is just asked to use that instruction.

Explicit invocation is still worth using when you want to be certain the instruction is applied. An explicitly invoked instruction stays in effect for the rest of the conversation, just as an automatically loaded one does.

### 添加自己的自定义指令

你可以将 `.md` 文件放到 `%LocalAppData%\TabularEditor3\AI\CustomInstructions\` 中，以创建自定义指令。 The folder is created the first time the AI Assistant runs, with an `example.md` file in it to copy from. Use **Open Custom Instructions Folder** on the AI Assistant toolbar to get there.

Each file may open with YAML frontmatter defining the instruction metadata. None of it is required:

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

| 字段              | 必需 | 默认值                  | 说明                                                                                                                    |
| --------------- | -- | -------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `id`            | 否  | 不含 `.md` 的文件名        | 唯一标识符，也会作为 `/id` 用于显式调用                                                                                               |
| `name`          | 否  | `id` 使用标题式大小写        | 自动完成中的显示名称                                                                                                            |
| `description`   | 否  | Falls back to `name` | Say what the instruction covers and when it applies                                                                   |
| `priority`      | 否  | 100                  | Higher values are injected first when several Custom Instructions are in effect                                       |
| `always_inject` | 否  | false                | If true, always included in the system prompt. Such an instruction is not offered in `/` autocomplete |
| `hidden`        | 否  | false                | 如果为 true，则不会在 `/command` 的自动补全中显示                                                                                     |

具有与内置指令相同 `id` 的自定义指令会覆盖内置版本。

Notes on how files are read:

- Frontmatter must start with `---` on the very first line of the file and end with a `---` line. If it does not, or if the YAML cannot be parsed, the whole file is treated as instruction content and every default above applies
- Keys that are not in the table above are ignored. This is what makes a leftover `triggers:` section harmless
- `{{version}}` anywhere in the body is replaced with the Tabular Editor AI component's version
- Only `.md` files directly in the folder are read; subfolders are not searched

### Custom Instructions from your organization

An administrator can publish a folder of Custom Instructions for everyone, with the `AiCustomInstructionsPath` [policy](xref:policies). It can be a read-only network share. Those instructions load for every user in addition to the built-in ones, and they are used exactly like any other: offered in `/` autocomplete, chosen by their description, invoked by `/id`.

Where the same `id` exists in more than one place, the one that wins is:

1. Your organization's folder
2. Your own folder
3. The built-in instructions

So an organization instruction overrides both a built-in one and a user's own file of the same name. A separate policy, `DisableUserCustomInstructions`, makes Tabular Editor ignore the instructions in your own folder altogether and disables **Open Custom Instructions Folder**; the built-in and organization instructions keep loading.

Both policies require Tabular Editor 3 Enterprise Edition.

## Permissions and consent

What the AI Assistant may touch is governed by _five resources_, each carrying one access level. The same five grants govern the [MCP server](xref:mcp-server), so there is one place to look and one place to change your mind.

| Resource                   | What it covers                                                                                                                                           | 级别                  | 默认值       |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------- |
| **Model metadata**         | Table, column and measure names, expressions, descriptions and similar. Read also covers VertiPaq Analyzer statistics                    | Deny / Read / Write | **Read**  |
| **Model data**             | Data values from your model, such as DAX query results. Requires a live connection                                                       | Deny / Read         | **Deny**  |
| **Best Practice Analyzer** | Read lists rules and runs the analysis; Write adds or modifies rules                                                                                     | Deny / Read / Write | **Read**  |
| **Documents**              | Your open document editors: C# scripts and DAX queries. Read is their contents; Write is needed to create or modify them | Deny / Read / Write | **Write** |
| **Macros**                 | Your macro library. Read lists and reads macros; Write is reserved for future macro-editing tools                                        | Deny / Read / Write | **Write** |

A **Write** grant covers Read, so there is no need to grant both. **Model data** is read-only by nature (the assistant can query your data but has no way to write values back), so it offers only Deny and Read.

> [!NOTE]
> **Model data** is the one resource denied by default. Metadata describes your model; data _is_ your model's contents, so sending it to an AI provider is a decision worth making deliberately rather than inheriting from a default.

Three grants are worth a closer look:

- **Model metadata > Write** lets the assistant change your model. On its own, that means writing a C# script and handing it to you to run. It is also the grant that makes [direct execution](#letting-the-assistant-change-your-model) possible, but the assistant only runs scripts itself once you have turned that on separately. Either way, only scripts that are statically determined to be safe ever run, and a script that reaches outside the model, to the file system or the network, is never executed for you.
- **Best Practice Analyzer > Read** lets the assistant run the analysis, but running it also needs **Model metadata > Read**, since the analysis reads the model.
- **Model data > Read** is not sufficient on its own to run a DAX query: that needs **Model metadata > Read** as well, because a query can read metadata through `INFO` functions, DMVs and the column names in its own result.

### Setting the permission grants

Open **Tools > Preferences > AI Features > Permissions**. Each resource has a dropdown carrying its available levels.

![AI Features > Permissions preferences, one dropdown per resource at its default](~/content/assets/images/pref-ai-permissions.png)

There is no separate "ask me" level. **Deny** is what asking looks like: in the chat, a resource you have not granted produces a permission card at the moment it is needed. Over MCP, where there is nobody to ask, a denied resource's tools are unavailable.

> [!NOTE]
> If you used the AI Assistant before 3.27.0 you will notice fewer prompts. Model metadata, Documents and Macros now start at Read or above, so the chat no longer asks for them. Only DAX query results and Best Practice Analyzer rule edits still raise a card out of the box. Set a resource to **Deny** to get its prompt back.

> [!NOTE]
> In the Enterprise Edition, IT administrators can set policies that determine these permissions. See @policies.

### Permission cards in the chat

When the assistant needs a resource your standing grant does not cover, a **Permission Required** card appears in the conversation, naming what it wants to do, for instance "The AI would like to access the metadata of your semantic model", or the DAX query it proposes to run.

![A Permission Required card in the chat, naming the DAX query the assistant wants to run, with Allow, Allow for session, Allow for this model, Always allow and Deny buttons](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| Button                   | What it does                                                                                                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Allow**                | This turn only. The assistant may repeat the same request while it finishes what you asked, and nothing is remembered afterwards                                                                          |
| **Allow for session**    | Until Tabular Editor is restarted. Held in memory, never written to disk                                                                                                                                  |
| **Allow for this model** | Recorded in the model's [user options](xref:user-options) file, so it applies the next time you open this model. Offered for **Model metadata** and **Model data** only, and only while a model is loaded |
| **Always allow**         | Raises the standing grant on the Permissions page, for every model and every session                                                                                                                                      |
| **Deny**                 | Refuses this request. The assistant carries on without that access and asks again next time                                                                                                               |

**Always allow** only ever raises a grant, never lowers one: allowing a read cannot narrow a Write grant you already had.

You do not have to answer the card at all. See [Stopping a turn while permission is pending](#stopping-a-turn-while-permission-is-pending) below.

### What the MCP server shares, and what it does not

The [MCP server](xref:mcp-server) reads the _same five grants_, but it does not use the card flow. An agent connecting over MCP is unattended, so there is nobody to prompt:

- Grants are _snapshotted when the server starts_ and govern its tool surface for the server's lifetime. Changing a grant while the server is running has no effect until you restart it.
- Only the _global_ grants are read. A grant you gave with **Allow for this model**, and a session grant, apply to the chat alone and never reach an MCP agent.
- A denied resource's tools are not offered to the agent at all, rather than being offered and then refused.

### Withdrawing permission

Set the resource back to **Deny** on the Permissions page. The chat asks again the next time it needs that resource; a running MCP server keeps the access it started with until you restart it.

Lowering a global grant does not clear a per-model grant. To withdraw one of those, delete the model's `.tmuo` file, or the `Permissions` entry within it. See details in @user-options.

### Audit record

On Tabular Editor 3 Enterprise Edition, a local record is kept of what the AI Assistant and the [MCP server](xref:mcp-server) did: which permissions were asked for and how you answered, which tools ran and whether each one succeeded, failed or was refused, and the full text of any C# script that was run or handed to you for review. Your prompts, the assistant's replies and data values from your model are never recorded. **Open audit folder** under **Tools > Preferences > AI Features** takes you to the files.

On Desktop and Business Edition, and before a license is activated, nothing is recorded, no folder is created and the button is not shown.

See @ai-audit-log for what each record holds, where the files live and the policies that redirect them.

### Stopping a turn while permission is pending

A **Permission Required** card waits for an answer before the assistant can carry on. You do not have to answer it: pressing **Stop** ends the turn, removes the card and treats the request as denied. The panel returns to its normal state and you can carry on in the same conversation with a new message.

## 偏好设置

Configure AI Assistant display and behavior options under **Tools > Preferences > AI Features > AI Assistant > Preferences**.

### 聊天显示

| 偏好         | 默认值  | 说明               |
| ---------- | ---- | ---------------- |
| 显示选择上下文指示器 | true | 在聊天中显示当前选定的模型对象  |
| 显示自定义指令指示器 | true | 在助手回复上方显示自定义指令标识 |
| 显示知识库搜索指示器 | true | 搜索知识库时显示进度       |

### 上下文压缩

| 偏好       | 默认值  | 说明                                                                                                                                                  |
| -------- | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| 自动压缩     | true | 接近上下文限制时自动摘要较早的信息                                                                                                                                   |
| 自动压缩阈值 % | 80   | Percentage of the model's own context window at which auto-compaction is triggered. Values outside 50-100 have no additional effect |

### C# Script

| 偏好                                            | 默认值   | 说明                                                                                                                                                                                                                                                                                                                                                                                      |
| --------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allow AI assistant to run C# scripts directly | false | Let the assistant carry out model changes itself instead of opening a script for you to run. Unavailable until **Model metadata** is set to **Write** under **Permissions**, and unavailable entirely under the `DisableCSharpScripts` [policy](xref:policies). See [Letting the assistant change your model](#letting-the-assistant-change-your-model) |
| 预览更改                                          | true  | 在聊天中执行 AI 生成的 C# Script 时，显示“预览更改”对话框                                                                                                                                                                                                                                                                                                                                                   |

Two further settings sit on the **AI Features** page itself, above **AI Assistant**, because they apply to the MCP server as well: _Check for knowledge base updates on startup_, and the **Open audit folder** button. See @preferences.

![The AI Assistant preferences page, with the three chat display indicators, Auto compact and its threshold, and the two C# script settings: Allow AI assistant to run C# scripts directly, cleared, and Preview changes, ticked](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token 使用量

每条发给 AI 助手的信息都会消耗输入 token。单条信息的 token 成本取决于包含了哪些上下文：

- **系统提示词和自定义说明**：每条信息都会一并发送。通常为 5,000 到 15,000 个 token，具体取决于启用了哪些自定义说明。
- **Model metadata**: when the assistant needs to understand your model, it retrieves metadata through tool calls. To stay within provider rate limits on large models, the assistant uses a progressive-disclosure approach. That is, it first fetches a lightweight overview (table and measure names, relationships), then searches for relevant objects by name, description or DAX expression and only drills into full details for the specific tables or objects that the question requires. 原本会非常庞大的工具结果会被截断，并附带说明助手如何检索其余数据。

### 令牌计数器

The token counter sits in the status strip above the message box, next to the [active model indicator](#choosing-a-model). The bar reads _used_ / _total_ in thousands of tokens and is colored green, amber or red as the context fills up. A `±` in front of the figure means an exact count is not available yet.

Hover over it for a breakdown in three labeled sections:

| Section                                           | What it covers                                                                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Last turn**                                     | What the most recent exchange cost: fresh input, tokens served from the provider's prompt cache, tokens written to the cache and output |
| **This conversation (billed)** | The same four figures accumulated across every request in the conversation, tool round-trips included                                                   |
| **Context**                                       | Tokens currently in the context window, against the window's real size                                                                                  |

A line reads, for example, `37,588 input + 131,744 cached · write 37,558 · output 2,866`. The cache parts are left out for providers that do not support prompt caching, and a section is left out entirely when it has nothing to report.

> [!TIP]
> Separating the last turn from the conversation total is what tells you whether a short follow-up question was actually expensive. A large **This conversation (billed)** figure next to a small **Last turn** figure is normal in a long conversation.

### Context window

The context usage bar, the auto-compaction point and the maximum length of a single reply all follow the _real context window of the model in use_, not one fixed figure. A model with a one-million-token window is measured against a million tokens.

Where the model's real window is not known (an Azure OpenAI or Custom deployment name, or a machine where the model catalog has never been retrieved), Tabular Editor falls back to 200,000 tokens.

### 减少 token 使用量

提问前，先在 **TOM Explorer** 中选择特定对象。选中对象后，助手会将上下文限定在这些对象上，而不是拉取整个模型的元数据。这是同时减少 token 使用量和 API 成本的最有效方式。

其他减少 token 使用量的方法：

- 围绕特定的表、度量值或列提出更聚焦的问题，而不是对整个模型提出泛泛的问题。像 _“为所有度量值设置显示文件夹”_ 这样含糊的提示，会迫使助手检索整个模型的元数据。像 _“为我选中的度量值设置显示文件夹”_ 这样具体的提示，会将上下文限制在当前选择范围内，并且消耗的 token 少得多
- 切换话题时开启新对话，避免累积过长的对话历史
- 进行探索性提问时，使用更小或成本更低的模型

## 局限性

- 需要用户提供 API 密钥。不包含内置 API 密钥
- AI 的响应取决于所选模型及提供商的能力
- The usable context window is the selected model's own; where Tabular Editor cannot determine it, 200,000 tokens is assumed
- AI 助手不能替代你对 DAX 和语义模型设计基础的理解
- 响应质量会因提供商和模型选择而异
- AI 助手无法连接到外部文件或服务，也无法搜索网页
- The AI Assistant cannot connect to external MCP servers to extend its own tools. This is about the chat only: Tabular Editor 3 itself acts as an MCP server, so your own agent can work on the open model. See @mcp-server
- AI 助手无法在聊天中切换到其他模型。使用 Tabular Editor 的用户界面更改模型连接
- AI 助手无法管理偏好

## 禁用 AI 助手

The AI Assistant is an optional component, installed by default from Tabular Editor 3.27.0. 你可以再次运行 Tabular Editor 3 安装程序，修改现有的 Tabular Editor 3 安装，以包含或排除 AI 助手组件。如果你使用的是 Tabular Editor 3 便携版，可以从安装目录中删除名为 `TabularEditor3.AI.dll` 的文件来移除 AI 助手组件。

The AI Assistant and the MCP server ship in the same component, so excluding it or deleting `TabularEditor3.AI.dll` removes both. To turn off the chat while keeping the MCP server, leave the component in place and use the `DisableAiChat` policy.

> [!NOTE]
> Regardless of whether the AI Assistant component is installed or not, a system admin can disable all AI functionality in Tabular Editor 3, the MCP server included, by specifying the [`DisableAi` policy](xref:policies). `DisableAiChat` turns off the chat alone, and `DisableMcpServer` the MCP server alone. See @policies.
