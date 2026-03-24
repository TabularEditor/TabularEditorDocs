---
uid: ai-assistant
title: AI Assistant
author: Morten Lønskov
updated: 2026-03-19
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
# AI Assistant

The AI Assistant is a chat-based interface for AI-assisted semantic model development designed to help you create semantic models faster. With an enterprise-ready design, full control of what is sent to the AI, and built-in consent management, you can use the AI Assistant with confidence. It can explore your model metadata, write and execute DAX queries, generate C# scripts, run Best Practice Analyzer checks, query VertiPaq Analyzer statistics and search the Tabular Editor knowledge base.

The AI Assistant uses a bring-your-own-key model. You provide an API key from one of the supported providers and the assistant runs directly against that provider's API.

> [!NOTE]
> The AI Assistant is in public preview starting with Tabular Editor 3.26.0.


![AI Assistant First Pane on Open](~/content/assets/images/ai-assistant/ai-assistant-panel-first-open.png)

## Getting Started

1. Open **Tools > Preferences > AI Assistant**
2. Select your AI provider and enter your API key
3. Open the AI Assistant panel from **View > AI Assistant**
4. Type a message and press **Enter** to start a conversation

> [!NOTE]
> API keys are stored encrypted on your local machine.

## Supported Providers

Configure your AI provider under **Tools > Preferences > AI Assistant > AI Provider**. Select a provider from the dropdown, enter your API key and optionally override the default model name.

| Provider | Default Model | Configuration Required |
| -- | -- | -- |
| OpenAI | gpt-4o | API key. Optional Organization ID and Project ID |
| Anthropic | claude-sonnet-4-6 | API key |
| Azure OpenAI | Deployment-dependent | API key, endpoint URL and deployment name |
| Custom (OpenAI-compatible) | User-specified | API key and custom endpoint URL |

![AI Assistant Provider Selection](~/content/assets/images/ai-assistant/ai-assistant-provider-preferences.png)

### OpenAI

Select **OpenAI** as the provider and enter your API key. You can optionally specify an Organization ID and Project ID if your OpenAI account uses these. The default model is **gpt-4o**, but you can change it to any model available on your account.

![AI Assistant OpenAI Configuration](~/content/assets/images/ai-assistant/ai-assistant-openai-config.png)

### Anthropic

Select **Anthropic** as the provider and enter your API key. The default model is **claude-sonnet-4-6**. You can change the model name to any Anthropic model available on your account.

![AI Assistant Anthropic Configuration](~/content/assets/images/ai-assistant/ai-assistant-anthropic-config.png)

### Azure OpenAI

Select **Azure OpenAI** as the provider. Enter your API key and the service endpoint URL for your Azure OpenAI resource. Set the model name to match your deployment name.

### Custom (OpenAI-compatible)

The Custom provider option supports local or organizational LLMs that expose an OpenAI-compatible API endpoint. Enter your API key and the custom endpoint URL. This allows you to keep all data within your own infrastructure for data privacy or compliance requirements.

## Capabilities

The AI Assistant has access to your model context and can perform the following actions:

- **Model exploration**: Query model metadata including tables, columns, measures, relationships and their properties
- **DAX query writing**: Generate DAX queries and execute them against your connected model, returning result sets directly in the chat
- **C# script generation**: Create C# scripts for model modifications that open in a new editor window. Scripts are executed with the [run with preview](xref:csharp-scripts#running-scripts-with-preview) feature, showing a diff of all model changes before applying them. All changes are visible in real-time and can be undone with **Ctrl+Z**
- **Best Practice Analyzer**: Run BPA analysis, view rule violations and create or modify BPA rules
- **VertiPaq Analyzer**: Query memory usage statistics and column cardinality
- **Document access**: Read and modify open documents such as DAX scripts and DAX queries
- **Knowledge base search**: Search the embedded Tabular Editor documentation for answers
- **UI navigation**: Generate `te3://` action links that open specific Tabular Editor dialogs and features

## Conversations

The AI Assistant supports multiple simultaneous conversations. Each conversation maintains its own message history and context.

- Conversations persist across sessions, stored locally in `%LocalAppData%\TabularEditor3\AI\Conversations\`
- Titles are generated automatically after the first exchange. You can rename conversations manually
- **Auto-compaction**: When the conversation approaches the context window limit (~80%), older messages are automatically summarized to free up space. A snapshot of the full conversation is archived before compaction

## Artifacts

When the AI Assistant generates code, it creates **artifacts** that open directly in editor windows:

- **C# Scripts**: Open in a new C# script editor with syntax highlighting, compilation and execution support
- **DAX Queries**: Open in a new DAX query editor with syntax highlighting and execution support
- **Macros**: C# scripts saved as reusable macros

Artifacts stream in real-time as the AI generates them. C# script artifacts include safety analysis that flags potentially unsafe code (e.g. file system access or network operations).

![AI Assistant Generate C# Script](~/content/assets/images/ai-assistant/ai-assistant-generate-c-sharp-script.png)

## Custom Instructions

Custom Instructions are instruction sets that guide the AI Assistant's behavior for specific tasks. They are activated automatically based on intent detection or invoked explicitly.

### Built-in Custom Instructions

The AI Assistant includes the following built-in Custom Instructions:

| Custom Instruction | Triggers On |
| -- | -- |
| DAX Querying | DAX, query, evaluate, measure |
| Model Modification | Modify, change, add, update, create |
| Model Design | Design, architecture, pattern, best practice |
| Organize Model | Organize, clean up, folder, rename |
| Optimize Model | Optimize, performance, slow, speed |
| Macros | Macro, automate, record |
| UDFs | UDF, function, user-defined |
| BPA | BPA, best practice, rule, violation |

Custom Instructions are shown as indicators above assistant responses, indicating which instructions influenced the response. You can toggle this display in **Preferences > AI Assistant > Preferences > Show custom instructions indicator**.

### Invoking a Custom Instruction

Type `/` to browse available custom instructions, or type the full `/instruction-id` at the start of your message to explicitly invoke a specific instruction. For example, `/dax-querying` forces the DAX querying instruction regardless of message content.

### Add your own Custom Instructions

You can create custom instructions by placing `.md` files in `%LocalAppData%\TabularEditor3\AI\CustomInstructions\`. Each file requires YAML frontmatter defining the instruction metadata:

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

| Field | Required | Default | Description |
| -- | -- | -- | -- |
| `id` | No | Filename without `.md` | Unique identifier, also used as `/id` for explicit invocation |
| `name` | No | Title-cased `id` | Display name in autocomplete |
| `description` | No | - | Short description shown below the name |
| `priority` | No | 100 | Higher values are injected first when multiple Custom Instructions match |
| `always_inject` | No | false | If true, always included in the system prompt |
| `hidden` | No | false | If true, not shown in `/command` autocomplete |
| `triggers.keywords` | No | [] | Words that activate the instruction (case-insensitive) |
| `triggers.patterns` | No | [] | Regex patterns for complex matching |
| `triggers.context_required` | No | [] | Conditions that must be met (e.g. `model_loaded`) |

Custom Instructions with an `id` matching a built-in instruction will override the built-in version.

## Consent

The AI Assistant requests permission before sending data to the AI provider. Consent is scoped to specific data types:

| Consent Category | Description |
| -- | -- |
| Query data | DAX query results and data samples |
| Read documents | Reading content from open documents such as DAX scripts and DAX queries |
| Modify documents | Making changes to open documents |
| Model metadata | Table and column schemas, measure definitions and other model metadata |
| Edit BPA rules | Creating or modifying Best Practice Analyzer rules |
| Read macros | Reading macro definitions |

When the AI Assistant needs access to a data type for the first time, a consent dialog appears. You can choose the duration of your consent:

| Option | Scope |
| -- | -- |
| This time | Single request only |
| This session | Until Tabular Editor is restarted |
| For this model | Persisted in the model's user options (.tmuo) file |
| Always | Global preference, persisted across all models and sessions |

![AI Assistant Consent Dialog](~/content/assets/images/ai-assistant/ai-assistant-generate-consent-dialog.png)

### Managing Consents

You can review and reset your consent choices under **Tools > Preferences > AI Assistant > AI Consents**. Each consent category shows its current state. Click **Reset** to revoke an "Always allowed" consent and return it to "Ask when needed".

![AI Assistant Consent Settings](~/content/assets/images/ai-assistant/ai-assistant-consent-reset.png)

## Preferences

Configure AI Assistant display and behavior options under **Tools > Preferences > AI Assistant > Preferences**.

### Chat Display

| Preference | Default | Description |
| -- | -- | -- |
| Show selection context indicator | true | Display the currently selected model object in the chat |
| Show custom instructions indicator | true | Show Custom Instruction indicators above assistant responses |
| Show knowledge base search indicator | true | Display progress when searching the knowledge base |

### Context Compaction

| Preference | Default | Description |
| -- | -- | -- |
| Auto compact | true | Automatically summarize old messages when approaching the context limit |
| Auto compact threshold % | 80 | Token usage percentage that triggers auto-compaction |

### C# Script

| Preference | Default | Description |
| -- | -- | -- |
| Show script impact preview | true | Show the script impact preview dialog when executing AI-generated C# scripts |

![AI Assistant Preferences](~/content/assets/images/ai-assistant/ai-assistant-preferences.png)

## Limitations

- Requires a user-provided API key. No built-in API key is included
- AI responses depend on the selected model and provider capabilities
- Maximum context window is 200,000 tokens
- The AI Assistant is not a replacement for understanding DAX and semantic model design fundamentals
- Response quality varies by provider and model selection
- The AI Assistant cannot connect to external files, services or search the web
- The AI Assistant cannot add or act as an MCP server
- The AI Assistant cannot connect to a different model from within the chat. Use the Tabular Editor user interface to change model connections
- The AI Assistant cannot manage preferences

## Disabling the AI Assistant

The AI Assistant is an optional component. You can exclude it during installation. If installed, you can disable it under **Tools > Preferences > AI Assistant**. When disabled, the AI Assistant does not run or send any data to external providers.
