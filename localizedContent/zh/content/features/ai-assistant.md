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

The AI Assistant is a chat panel for semantic model development. It explores your model metadata, writes and runs DAX queries, generates C# scripts, runs Best Practice Analyzer checks, queries VertiPaq Analyzer statistics and searches the Tabular Editor knowledge base. [Permission settings](#permissions-and-consent) control what it sends to your AI provider. The AI Assistant has undergone independent penetration testing; see the [Tabular Editor Trust Center](https://trust.tabulareditor.com).

The AI Assistant uses a bring-your-own-key model, where you provide an API key from one of the supported providers and the assistant runs directly against that provider's API.

You can also use your own agent through the [MCP server](xref:mcp-server), with no API key. An agent such as Claude Code, GitHub Copilot, VS Code agent mode, Codex or Cursor works on the open model with the same tools and permission settings as the chat, except for session and per-model grants, which apply to the chat only. See [MCP server and AI Assistant differences](#mcp-server-and-ai-assistant-differences).

![The AI Assistant pane as it first opens, with the assistant's greeting listing what it can do (answer questions, query the model, write and execute C# scripts, change the model) and what it cannot, above an empty message box](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## 快速入门

1. Open **Tools > Preferences > AI Features > AI Assistant > AI Provider**
2. 选择 AI 提供商（全新安装时默认是 **无（AI 已禁用）**），然后输入你的 API 密钥
3. 从 **视图 > AI 助手** 打开 AI 助手面板
4. 输入一条信息并按 **Enter** 键开始对话

> [!TIP]
> The [interactive demo of the AI Assistant](https://demos.tabulareditor.com/psl/of150vcy?) walks through setup and use.

> [!NOTE]
> API 密钥会以加密形式存储在你的本地计算机上。

## Supported providers

在 **工具 > 偏好 > AI 功能 > AI 助手 > AI 提供商** 中配置 AI 提供商。从下拉列表中选择一个提供商（在你完成配置之前，默认值为 **无（AI 已禁用）**），输入 API 密钥，并可选择覆盖默认模型。

将模型字段留空即可使用提供商的默认模型。 OpenAI and Anthropic have defaults; Azure OpenAI and the Custom provider always need a value.

| 提供程序           | Default model           | Configuration required        |
| -------------- | ----------------------- | ----------------------------- |
| OpenAI         | gpt-5.5 | API 密钥。可选：基础 URL、组织 ID 和项目 ID |
| Anthropic      | claude-sonnet-4-6       | API 密钥。可选：基础 URL              |
| Azure OpenAI   | 无。必须提供部署名称              | API 密钥、端点 URL 和部署名称           |
| 自定义（兼容 OpenAI） | 无。必须提供模型名称              | API 密钥和自定义端点 URL              |

![AI 提供商偏好页，其中“选择提供商”下拉列表已展开，显示“无（AI 已禁用）”、OpenAI、Anthropic、Azure OpenAI 和“自定义（兼容 OpenAI）”，下方有 URL 和 API 密钥字段](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### 选择模型

当前活动模型显示在信息框上方的状态栏中，位于上下文用量条旁边。 Click it to open a picker listing the models available for the configured provider; a model you pick applies from the next request. The last entry, **Preferences...**, opens **Tools > Preferences > AI Features > AI Assistant > AI Provider** for anything not on the list. For the Azure OpenAI and Custom providers, or before the model list has been retrieved, the model name is a link that opens those preferences.

![信息框上方已打开的模型选择器，其中列出了 claude-sonnet-5、claude-fable-5-1、claude-fable-5、claude-opus-5、claude-haiku-4-5、claude-opus-4-8，以及以粗体显示的当前活动项 claude-sonnet-4-6，底部还有偏好……位于分隔线下方](~/content/assets/images/ai-assistant/ui-model-picker.png)

> [!NOTE]
> The model indicator is hidden until a provider, an API key and a model are all set.

### OpenAI

将提供程序选择为 **OpenAI**，然后输入你的 API 密钥。 If your OpenAI account uses an Organization ID or a Project ID, enter those too. The model name accepts any model available on your account.

![The AI Provider preferences page from an earlier version, with OpenAI selected, a masked API key, empty Organization ID and Project ID fields and gpt-4o as the model name](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

选择 **Anthropic** 作为提供商，然后输入你的 API 密钥。 The model name accepts any Anthropic model available on your account.

![The AI Provider preferences page with Anthropic selected as the provider, the base URL https://api.anthropic.com, a masked API key and claude-sonnet-4-6 as the model name](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

> [!IMPORTANT]
> Anthropic 会根据你的账户等级，强制执行每分钟输入 token（ITPM）的速率限制。新创建的 API 密钥起始为 Tier 1，Claude Sonnet 4.x 的 ITPM 上限为 30,000。对大型模型发起的一次请求就可能超过此限制。购买 $40 或以上的 API 额度即可升至第 2 档（450,000 ITPM）。有关各档位的完整详情，请参阅 [Anthropic 速率限制文档](https://docs.anthropic.com/en/api/rate-limits)。

### Azure OpenAI

Select **Azure OpenAI** as the provider and configure these fields:

- **API 密钥**：用于访问你的 Azure OpenAI 资源的密钥
- **Service endpoint**: the resource URL, for example `https://your-resource.openai.azure.com`. The SSL certificate is issued for `*.openai.azure.com`, so a `*.privatelink.openai.azure.com` address fails certificate validation
- **Deployment**: the deployment name shown in the **Name** column of **Deployments**

Azure OpenAI 要求在每次 API 调用中都提供部署名称。 The name is set when the deployment is created and often matches the model it serves, for example `gpt-4o`, but it can differ. If you enter the resource name or a model name that doesn't exist as a deployment, the request fails.

Find the deployment name in the [Azure AI Foundry portal](https://ai.azure.com):

1. 登录并选择你的 Azure OpenAI 资源
2. 打开 **部署**（如果资源已升级到 Foundry，则为 **模型 + 终结点**）
3. 复制 **名称** 列中的值

If a deployment created before your organization adopted Azure AI Foundry doesn't appear in the portal, list the deployments with the Azure CLI:

```bash
az cognitiveservices account deployment list --name "<resource-name>" --resource-group "<resource-group>" --output table
```

See [Create and deploy an Azure OpenAI resource](https://learn.microsoft.com/azure/ai-foundry/openai/how-to/create-resource#deploy-a-model).

有关 403 错误、SSL 失败或 "DeploymentNotFound" 响应，请参阅 @azure-openai-connection-errors。 For models deployed in Microsoft Foundry, see [Using Microsoft Foundry](#using-microsoft-foundry).

### 自定义（兼容 OpenAI）

The Custom provider connects to any LLM that exposes an OpenAI-compatible API endpoint, such as a model on your own machine or one hosted on your organization's network. Enter your API key and the endpoint URL. With a self-hosted model, all data stays within your own infrastructure and nothing is sent to a third-party cloud provider. See [Using a local or organizational LLM](#using-a-local-or-organizational-llm).

## 使用本地或组织内部的 LLM

你可以通过“自定义”提供商让 AI 助手对接自托管的 LLM。这样可确保所有数据都保留在你自己的基础设施内，无论是运行在本地计算机上的模型，还是托管在你所在组织网络中的集中式 LLM。无论哪种方式，都不会将数据发送到第三方云提供商。
These tools host models with an OpenAI-compatible API, on a developer's workstation or on a shared server that serves as a team endpoint:

- [Ollama](https://ollama.com) — 轻量级 CLI，用于在本地下载并运行模型
- [LM Studio](https://lmstudio.ai) — 带图形界面的桌面应用，用于管理并运行本地模型
- [LocalAI](https://localai.io) — 自托管、社区驱动的替代方案，支持多种模型

### 示例：Ollama

1. [下载并安装 Ollama](https://ollama.com/download)
2. Pull a model, for example `ollama pull llama3.1`
3. Start the Ollama server. It starts automatically after installation, by default on port 11434
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:11434/v1`
7. Set **Model name** to the model you pulled, for example `llama3.1`
8. Set **API Key** to any non-empty value, for example `ollama`. Ollama doesn't require authentication, but the field can't be blank

### 示例：LM Studio

1. [Download and install LM Studio](https://lmstudio.ai/download)
2. Download a model from the model search page in the left panel, or with the CLI, for example `lms get lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
3. Start the LM Studio server from the developer page in the left panel, or with `lms server start`. Turn on OpenAI-compatible mode. If the context size is below 100,000 tokens, raise it above 100,000
4. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
5. 将 **Choose provider** 设置为 **Custom (OpenAI-compatible)**
6. 将 **Service Endpoint** 设置为 `http://localhost:1234/v1`
7. Set **Model name** to the model you downloaded, for example `lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF`
8. Set **API Key** to any non-empty value, for example `lms`. LM Studio doesn't require authentication, but the field can't be blank

> [!NOTE]
> 本地模型的响应质量取决于模型规模以及你的硬件配置。 Larger models give better results and need more RAM and a capable GPU. The AI Assistant's tool calling requires a model that supports function calling in the OpenAI-compatible format.

> [!TIP]
> Use a model with at least 30 billion parameters, and preferably 100 billion or more. Qwen3.5-122B-A10B performed well in internal testing.

## 使用 Microsoft Foundry

[Microsoft Foundry](https://ai.azure.com) (formerly Azure AI Foundry) deploys OpenAI and Anthropic models in your Azure environment. Connect to these models with the **OpenAI** or **Anthropic** provider in Tabular Editor.

> [!IMPORTANT]
> Don't use the **Azure OpenAI** provider for Microsoft Foundry models. It works only with classic Azure OpenAI resources that use the `api-version` query parameter.

### Microsoft Foundry 上的 OpenAI 模型

Configure an OpenAI model deployed in Microsoft Foundry, such as GPT-4o or GPT-5.4-mini:

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **OpenAI**
3. Set **Base URL** to your Foundry resource endpoint with `/openai/v1` appended, in one of these formats:
   - `https://your-resource.services.ai.azure.com/openai/v1`
   - `https://your-resource.openai.azure.com/openai/v1`
4. 输入 Foundry **API 密钥**
5. Set **Model name** to your deployment name, for example `gpt-5.4-mini`

> [!NOTE]
> The Microsoft Foundry portal doesn't show the base URL. It shows a **Target URI** with the full API path, for example `https://your-resource.services.ai.azure.com/api/projects/YourProject/openai/v1/responses`. For the base URL, use only `https://your-resource.services.ai.azure.com/openai/v1`.

### Microsoft Foundry 中的 Anthropic 模型

For an Anthropic model deployed in Microsoft Foundry, such as Claude Sonnet 4.6:

1. 在 Tabular Editor 中，依次点击 **Tools > 偏好 > AI Features > AI Assistant > AI Provider**
2. 将 **选择提供程序** 设置为 **Anthropic**
3. Set **Base URL** to your Foundry resource endpoint with `/anthropic` appended, for example `https://your-resource.services.ai.azure.com/anthropic`
4. 输入 Foundry **API 密钥**
5. Set **Model name** to the model identifier, for example `claude-sonnet-4-6`

> [!NOTE]
> The portal shows a **Target URI** such as `https://your-resource.services.ai.azure.com/anthropic/v1/messages`. For the base URL, use the part up to and including `/anthropic`.

## 功能

Within your [permission grants](#permissions-and-consent), the AI Assistant works with your model context:

- **Model exploration**: queries model metadata, including tables, columns, measures, relationships and their properties
- **DAX query writing**: generates DAX queries, runs them against your connected model and returns the result sets in the chat
- **C# script generation**: creates C# scripts for model changes. Depending on your settings, the assistant opens the script in an editor window for you to run, or runs it itself; see [Letting the assistant change your model](#letting-the-assistant-change-your-model). **Ctrl+Z** undoes model metadata changes
- **Best Practice Analyzer**: runs BPA analysis, lists rule violations and creates or modifies BPA rules
- **VertiPaq Analyzer**: queries memory usage statistics and column cardinality
- **Document access**: reads and modifies open documents: DAX queries, C# scripts and DAX scripts
- **Knowledge base search**: searches the embedded Tabular Editor documentation
- **UI navigation**: generates `te3://` action links that open specific Tabular Editor dialogs and features

An agent connected over the [MCP server](xref:mcp-server) has the same capabilities except UI navigation. Both change your model by running a C# script as a single undoable step. They differ in how you review changes and grant permissions; see [MCP server and AI Assistant differences](#mcp-server-and-ai-assistant-differences).

> [!NOTE]
> When the model is loaded from a file, such as a `.bim` file or a TMDL folder, and isn't connected to Analysis Services or Power BI, tools that need a connection are hidden, including DAX query execution and VertiPaq Analyzer statistics. The assistant still writes DAX queries, but **Execute** on DAX query artifacts is disabled until you connect. VertiPaq Analyzer statistics loaded from a `.vpax` file stay available.

## 让助手更改你的模型

By default, the assistant writes a C# script and opens it in an editor window, where you read and run it. It can also run the script itself when you select **Allow AI assistant to run C# scripts directly** under **Tools > Preferences > AI Features > AI Assistant > Preferences**.

The setting is off by default and unavailable until **Model metadata** is set to **Read/Write** under **Tools > Preferences > AI Features > Permissions**.

### 当助手运行脚本时会发生什么

- If **Preview changes** is on (the default), the [preview dialog](xref:csharp-scripts#run-c-scripts-with-preview) appears before the changes are applied. **Cancel** reverts them and reports the rejection to the assistant. If **Preview changes** is off, the changes are applied without a dialog.
- The script's changes are one undo entry, **C# script (AI Assistant)**. **Ctrl+Z** undoes the whole script.
- If the script fails part-way through, the model is left unchanged and the assistant reports the error.
- A script that accesses files, the network or external assemblies doesn't run. It opens as a script artifact with an **Unsafe** badge and **Execute** disabled, and the assistant's reply names what the script used.

If you ask for a script, for example "Write me a script that renames every measure to sentence case", the assistant opens it as a script document that you run yourself, even with this setting on.

The `DisableCSharpScripts` [policy](xref:policies) applies in every edition and turns off both direct execution and the scripts the assistant hands you to run.

The `BlockUnsafeScripts` policy requires Enterprise Edition and applies to every script in Tabular Editor, including scripts run over the [MCP server](xref:mcp-server). When it's set, the assistant can still write a script that accesses files, the network or external assemblies, but the script doesn't run and no artifact opens for review. 见[管理员策略](xref:csharp-scripts#administrator-policies)。

## 对话

The AI Assistant supports multiple simultaneous conversations, each with its own message history and context.

- conversations persist across sessions and are stored locally in `%LocalAppData%\TabularEditor3\AI\Conversations\`
- titles are generated automatically after the first exchange, and you can rename a conversation
- **Auto-compaction**: when a conversation approaches the context window limit, older messages are summarized to free up space, after a snapshot of the full conversation is archived. The threshold is a percentage of the model's own context window, set under [Context compaction](#context-compaction)

### 删除对话

**Delete conversation** is at the left end of the AI Assistant toolbar, next to **New conversation**. After you confirm the prompt, the conversation and its history are removed from disk and can't be recovered. The close button on the panel's title bar, or **View > AI Assistant**, hides the panel without deleting anything.

## 工件

Code that the AI Assistant generates opens as an _artifact_ in an editor window:

- **C# scripts**: a C# script editor with syntax highlighting, compilation and execution
- **DAX queries**: a DAX query editor with syntax highlighting and execution

Artifacts stream in as the AI generates them, and C# script artifacts include a safety analysis that flags unsafe code, such as file system access or network operations.

![AI 助手窗格，显示生成的 C# Script 产物及其“执行”按钮，以及助手对该脚本作用的说明和随附的大小写敏感提示](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

If **Preview changes** is on, running a C# script from the chat opens the **Script Preview** dialog with a side-by-side diff of all model metadata changes the script made, where you accept or revert the changes. See [Running scripts with preview](xref:csharp-scripts#run-c-scripts-with-preview).

![“脚本预览 - 模型更改”对话框：左右并排显示更改前后的模型；其中 Internet Total Freight 度量值的格式字符串已更改，并新增了说明和显示文件夹，且每项更改都标注了对应的原始值](~/content/assets/images/preview-script-changes.png)

## 自定义指令

_Custom Instructions_ are instruction sets that guide the AI Assistant on specific tasks. The assistant receives a list of every available instruction with its `description`, and loads the full text only of those relevant to your request, so keep descriptions accurate and specific. A loaded instruction stays in effect for the rest of the conversation.

### 内置自定义指令

The AI Assistant includes these Custom Instructions:

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

With **Show custom instructions indicator** selected under **Tools > Preferences > AI Features > AI Assistant > Preferences**, indicators above each response show which instructions influenced it.

### 调用自定义指令

Type `/` to browse available Custom Instructions. Start your message with an instruction's `/id` to load it regardless of the message content; for example, `/dax-querying` loads the DAX querying instruction. A `/id` with no message loads the instruction without making a request. An explicitly loaded instruction stays in effect for the rest of the conversation, like one the assistant loads itself.

### 添加自己的自定义指令

Create a Custom Instruction by placing a `.md` file in `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. 该文件夹会在 AI 助手首次运行时创建，其中包含一个可供参考和复制的 `example.md` 文件。 **Open Custom Instructions Folder** on the AI Assistant toolbar opens it.

The YAML frontmatter that defines the instruction metadata is optional:

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

A Custom Instruction whose `id` matches a built-in instruction overrides the built-in version.

Tabular Editor reads the files as follows:

- frontmatter must start with `---` on the very first line of the file and end with a `---` line. If it doesn't, or if the YAML can't be parsed, the whole file is treated as instruction content and every default above applies
- keys that aren't in the table above are ignored. Files from earlier versions that still have a `triggers:` section load unchanged
- 正文中出现的任何 `{{version}}` 都会被替换为 Tabular Editor AI 组件的版本号
- only `.md` files directly in the folder are read; subfolders aren't searched

### 来自你所在组织的自定义说明

An administrator can publish a folder of Custom Instructions for everyone with the `AiCustomInstructionsPath` [policy](xref:policies), and the folder can be a read-only network share. Those instructions load for every user in addition to the built-in ones and work like other instructions: offered in `/` autocomplete, chosen by their description, invoked by `/id`.

Where the same `id` exists in more than one place, precedence is:

1. your organization's folder
2. your own folder
3. the built-in instructions

A separate policy, `DisableUserCustomInstructions`, makes Tabular Editor ignore the instructions in your own folder and disables **Open Custom Instructions Folder**; the built-in and organization instructions still load. 这两项策略都需要 Tabular Editor 3 企业版。

## 权限与同意

Set an access level for each resource to control what the AI Assistant can access, and the [MCP server](xref:mcp-server) uses the same settings.

| 资源                         | 涵盖内容                                                                                                                | 级别           | 默认值    |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------ | ------ |
| **模型元数据**                  | 表、列和度量值的名称、表达式、描述等。“读取”权限还包括 VertiPaq分析器的统计信息                                                                       | 拒绝 / 读取 / 写入 | **读取** |
| **模型数据**                   | 模型中的数据值，例如 DAX 查询结果。需要实时连接                                                                                          | 拒绝 / 读取      | **拒绝** |
| **Best Practice Analyzer** | 读取可列出规则并运行分析；写入可添加或修改规则                                                                                             | 拒绝 / 读取 / 写入 | **读取** |
| **文档**                     | Your open documents: DAX queries, C# scripts and DAX scripts. 读取可访问其内容；创建或修改则需要写入权限 | 拒绝 / 读取 / 写入 | **写入** |
| **宏**                      | 你的宏库。读取可列出并读取宏；写入权限为未来的宏编辑工具预留                                                                                      | 拒绝 / 读取 / 写入 | **写入** |

**Write** (labeled **Read/Write** in the dropdowns) includes Read.

> [!NOTE]
> Granting **Model data** sends data values from your model to your AI provider.

Some grants depend on others:

- **Model metadata > Write** is required for [direct execution](#letting-the-assistant-change-your-model), which you turn on separately.
- Running the Best Practice Analyzer needs **Model metadata > Read** in addition to **Best Practice Analyzer > Read**.
- Running a DAX query needs **Model metadata > Read** in addition to **Model data > Read**. A query can read metadata through `INFO` functions, DMVs and the column names in its result.

### 设置权限授予

Open **Tools > Preferences > AI Features > Permissions**, where each resource has a dropdown with its available levels.

![AI 功能 > 权限偏好设置，每个资源一个下拉菜单，默认值](~/content/assets/images/pref-ai-permissions.png)

The chat has no separate "ask" level and shows a [permission card](#permission-cards-in-the-chat) when it needs a resource set to **Deny**.

> [!NOTE]
> From 3.27.0, **Model metadata**, **Documents** and **Macros** default to Read or higher, and the chat no longer prompts for them. By default, only DAX query results and Best Practice Analyzer rule edits show a card. 将某个资源设为 **拒绝**，就能让它重新弹出提示。

> [!NOTE]
> In Enterprise Edition, administrators can cap these permissions by policy. 参见 @policies。

### 聊天中的权限卡片

When the assistant needs a resource your standing grant doesn't cover, a **Permission Required** card appears in the conversation. The card names what the assistant wants to do, for example "The AI would like to access the metadata of your semantic model", or shows the DAX query it proposes to run.

![聊天中的“需要权限”卡片，显示助手想要运行的 DAX 查询，并带有“允许”“在本次会话中允许”“对此模型允许”“始终允许”和“拒绝”按钮](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

| 按钮           | 作用                                                                                                                                                                    |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **允许**       | Applies to this turn only. The assistant can repeat the same request while it finishes your task, and nothing is remembered afterwards                |
| **在本次会话中允许** | Applies until Tabular Editor is restarted. The grant is held in memory and never written to disk                                                      |
| **仅对该模型允许**  | Recorded in the model's [user options](xref:user-options) file and applied the next time you open this model. 仅针对 **模型元数据** 和 **模型数据** 提供，且仅在已加载模型时可用 |
| **始终允许**     | 在“权限”页中提高常设授权级别，对所有模型和所有会话生效                                                                                                                                          |
| **拒绝**       | Denies this request. The assistant continues without that access, and the card appears again the next time it needs it                                |

**Always allow** never lowers an existing grant; allowing a read on a resource at Write leaves it at Write.

### 在等待权限时停止当前轮次

The turn pauses until you answer a **Permission Required** card. **Stop** ends the turn without an answer, removes the card and counts the request as denied. Send a new message to continue the conversation.

### MCP server and AI Assistant differences

The [MCP server](xref:mcp-server) uses the same five grants but shows no permission cards:

- grants are read when the server starts and apply until it stops, so a changed grant takes effect only after you restart the server
- only global grants apply. Grants given with **Allow for this model** or **Allow for session** apply to the chat only
- a denied resource's tools aren't in the agent's tool list

### 撤销权限

Set a resource back to **Deny** on the Permissions page to withdraw its grant. The chat then shows a permission card the next time it needs that resource.

Lowering a global grant doesn't clear a per-model grant. Delete the model's `.tmuo` file, or the `Permissions` entry in it, to withdraw per-model grants. See @user-options.

### 审计记录

In Enterprise Edition, including Consultancy and Trial licenses, Tabular Editor writes a local log of AI Assistant and [MCP server](xref:mcp-server) activity. It records:

- which permissions were requested and how you answered
- which tools ran and whether each one succeeded, failed or was blocked
- 助手或 MCP 代理运行或提交运行的任何 C# Script 的完整文本，包括在运行时失败或被拒绝执行的脚本

你的提示词、助手的回复以及模型中的数据值都不会被记录。无法编译的脚本不会被保存；同样，助手写入文档供你自行运行的脚本文本也不会被保存。 **Open audit folder** under **Tools > Preferences > AI Features** opens the log folder.

Without an Enterprise license, and before a license is activated, nothing is recorded, no folder is created and the button isn't shown. See @ai-audit-log for what each record holds, where the files are stored and the policies that redirect them.

## 偏好设置

在 **工具 > 偏好 > AI 功能 > AI Assistant > 偏好** 中配置 AI 助手的显示与行为选项。

### Chat display

| 偏好         | 默认值 | 说明               |
| ---------- | --- | ---------------- |
| 显示选择上下文指示器 | 关   | 在聊天中显示当前选定的模型对象  |
| 显示自定义指令指示器 | 关   | 在助手回复上方显示自定义指令标识 |
| 显示知识库搜索指示器 | 关   | 搜索知识库时显示进度       |

### Context compaction

| 偏好       | 默认值 | 说明                                                                                                                               |
| -------- | --- | -------------------------------------------------------------------------------------------------------------------------------- |
| 自动压缩     | 开   | 接近上下文限制时自动摘要较早的信息                                                                                                                |
| 自动压缩阈值 % | 80  | 达到模型自身上下文窗口的这一百分比时，将触发自动压缩。 The field accepts 25 to 100. Values below 50 act as 50 and values above 90 act as 90 |

### C# Script

| 偏好                     | 默认值 | 说明                                                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 允许 AI 助手直接运行 C# Script | 关   | Lets the assistant run its C# scripts itself. When off, the assistant opens each script and you run it. Unavailable until **Model metadata** is set to **Read/Write** under **Permissions**, and unavailable entirely under the `DisableCSharpScripts` [policy](xref:policies). 见 [让助手更改你的模型](#letting-the-assistant-change-your-model) |
| 预览更改                   | 开   | 在聊天中执行 AI 生成的 C# Script 时，显示“预览更改”对话框                                                                                                                                                                                                                                                                                                                                                   |

**Check for knowledge base updates on startup** and the **Open audit folder** button are on the **AI Features** page, above **AI Assistant**, and both also apply to the MCP server. 见 @preferences。

![The AI Assistant preferences page, with the three chat display indicators cleared (the default), Auto compact selected with a threshold of 80, Allow AI assistant to run C# scripts directly cleared and Preview changes selected](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Token usage

每条发给 AI 助手的信息都会消耗输入 token。 The token cost of a single message depends on the context it includes:

- **System prompt and Custom Instructions**: sent with every message, typically 5,000 to 15,000 tokens depending on which Custom Instructions are active
- **Model metadata**: retrieved through tool calls, in stages. The assistant first fetches a lightweight overview (table and measure names, relationships), then searches for relevant objects by name, description or DAX expression, and retrieves full details only for the tables or objects the question requires. A very large tool result is truncated, with guidance on how the assistant can retrieve the rest

### Token counter

The token counter is in the status strip above the message box, next to the [active model indicator](#choosing-a-model). The bar reads used / total in thousands of tokens and is colored green, amber or red as the context fills up. A `±` in front of the figure means an exact count isn't available yet.

Hover over the counter to see a breakdown:

| 部分           | 涵盖内容                                       |
| ------------ | ------------------------------------------ |
| **上一轮**      | 最近一次交互的开销：新输入、从提供方的提示缓存中读取的令牌、写入缓存的令牌，以及输出 |
| **本次对话（计费）** | 同样的四项数字，累计整个对话中的每次请求，包括工具往返调用              |
| **上下文**      | 当前位于上下文窗口中的令牌数，并与该窗口的实际大小对照                |

某一行可能会显示为：`37,588 input + 131,744 cached · write 37,558 · output 2,866`。 The cache parts are left out for providers that don't support prompt caching, and a section is left out when it has nothing to report.

> [!TIP]
> Compare **Last turn** with **This conversation (billed)** to see what a single question cost. In a long conversation, a large **This conversation (billed)** figure next to a small **Last turn** figure is normal.

### 上下文窗口

The context usage bar, the auto-compaction point and the maximum length of a single reply use the selected model's context window. For example, a model with a one-million-token window is measured against a million tokens. If the model's window isn't known (an Azure OpenAI or Custom deployment name, or a machine where the model catalog has never been retrieved), Tabular Editor uses 200,000 tokens.

### Reducing token usage

提问前，先在 **TOM Explorer** 中选择特定对象。 The assistant then scopes its context to the selected objects and doesn't retrieve metadata for the entire model, which reduces both token usage and API cost the most.

其他减少 token 使用量的方法：

- Ask focused questions about specific tables, measures or columns. A vague prompt such as "Set display folders on all measures" makes the assistant retrieve metadata for the entire model. A specific prompt such as "Set display folders on the measures I have selected" limits the context to the current selection and uses far fewer tokens
- Start a new conversation when you switch topics, so long histories don't accumulate
- 进行探索性提问时，使用更小或成本更低的模型

## 限制

- requires your own API key; no API key is built in
- response quality depends on the provider and model you select
- the AI Assistant doesn't replace knowledge of DAX and semantic model design fundamentals
- the AI Assistant can't access external files or services, or search the web
- the AI Assistant can't connect to external MCP servers to extend its own tools. To use your own agent with Tabular Editor 3, see @mcp-server
- the AI Assistant can't connect to a different model from the chat. Change model connections in the Tabular Editor user interface
- the AI Assistant can't manage preferences

## 禁用 AI 助手

AI 助手是一个可选组件，自 Tabular Editor 3.27.0 起默认随产品安装。 Run the Tabular Editor 3 installer again to include or exclude it in an existing installation. In the portable build, delete `TabularEditor3.AI.dll` from the installation directory to remove it.

The same component contains the MCP server, so excluding it or deleting `TabularEditor3.AI.dll` removes both. To turn off only the chat, keep the component and set the `DisableAiChat` policy.

> [!NOTE]
> Whether or not the component is installed, a system administrator can turn off all AI functionality in Tabular Editor 3, the MCP server included, with the [`DisableAi` policy](xref:policies). `DisableMcpServer` turns off the MCP server alone. 参见 @policies。
