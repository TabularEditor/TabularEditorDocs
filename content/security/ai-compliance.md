---
uid: ai-compliance
title: AI features compliance guide
author: Morten Lønskov
updated: 2026-10-09
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Business
          partial: true
          note: "General policies only. No permission limits, provider lock or audit log"
        - edition: Enterprise
          full: true
---

# AI features compliance guide

The [AI Assistant](xref:ai-assistant) and the [Model Context Protocol (MCP) server](xref:mcp-server) in Tabular Editor 3 give AI models access to the open semantic model, within permission grants that administrators limit by group policy and that Enterprise Edition records in an audit log. This page is for the IT, security and compliance teams that approve these features for an organization.

## The AI features

| Feature | What it does | What calls the AI provider | Network traffic |
| -- | -- | -- | -- |
| AI Assistant | A chat panel in Tabular Editor 3 that reads, queries and changes the open semantic model | Tabular Editor 3, from the user's machine, with an API key the user enters | Outbound to the configured provider endpoint |
| MCP server | A local server that an AI agent the user already runs, such as Claude Code, GitHub Copilot, Codex or Cursor, connects to. The agent then reads, queries and changes the open semantic model | The agent, under its own configuration and subscription | Inbound on `127.0.0.1` only |

Both features ship in the AI features component, which is part of a default installation from Tabular Editor 3.27.0. They share the permission grants, the administrator policies and the audit log, with the differences described under [Permission grants](#permission-grants).

Tabular Editor ApS doesn't operate an AI service and doesn't include an API key. Prompts, replies, model metadata and model data from either feature never pass through Tabular Editor servers. With telemetry on, Tabular Editor 3 sends AI usage events to Tabular Editor ApS with the provider, the model name, a conversation ID and token counts. The `DisableTelemetry` policy turns them off.

The [Tabular Editor Trust Center](https://trust.tabulareditor.com/) publishes the independent penetration test report for the AI Assistant, the SOC 2 audit report and the list of sub-processors.

## Data flow

### AI Assistant

The AI Assistant sends requests directly from the user's machine to the provider configured under **Tools > Preferences > AI Features > AI Assistant**: OpenAI, Anthropic, Azure OpenAI or any OpenAI-compatible endpoint, including a model hosted on your own network. Authentication is by API key only. See [Supported providers](xref:ai-assistant#supported-providers).

A request to the provider contains:

- the system prompt and the Custom Instructions in effect, including any your organization publishes
- the user's messages and the conversation history
- context about the open model added to the user's messages: the database name, object counts, the current selection, the title of the active document, model errors and recent changes. A user's **Model metadata** setting doesn't withhold it; a `MaxModelMetadataAccess` limit of `Deny` does
- the results of the tools the assistant called, within the [permission grants](#permission-grants)
- passages from the Tabular Editor knowledge base, a local database built from the Tabular Editor documentation, blog, GitHub issues and discussions

Model metadata covers the whole model definition: object names, descriptions and annotations, DAX and M expressions, partition source queries, data source connection details, roles, role members and row-level security filters. Values typed into the model definition, such as a `DATATABLE` expression or an **Enter data** table, are part of the metadata.

Text from these sources becomes part of the request and influences what the assistant does. Restrict write access to an organization Custom Instructions folder to the people who approve its content.

Your organization's agreement with the provider governs retention, the region data is processed in and whether the provider uses requests for model training. To keep processing in an Azure tenant or a network your organization governs, use Azure OpenAI, [Microsoft Foundry](xref:ai-assistant#using-microsoft-foundry) or a [self-hosted model](xref:ai-assistant#using-a-local-or-organizational-llm), and lock the configuration by [policy](#restrict-the-ai-provider).

### MCP server

The MCP server is an HTTP listener bound to `127.0.0.1`, on port 42100 by default. It has no API key, makes no outbound requests and rejects browser requests with a non-local `Origin` header.

The connected agent sends what it reads from Tabular Editor 3 to its own provider, under the agent's configuration and the provider's terms. Tabular Editor 3 has no setting for the agent's provider, so govern the agent through its own administrative controls. The agent's own tools, such as file and shell access, are outside Tabular Editor 3 as well. Model files on disk, conversation files and audit files are readable by any agent running as the user.

**Require access token** is off by default. While it's off, any process on the machine can connect to the server without credentials, including processes in other users' sessions on a Remote Desktop or Citrix host. The `RequireMcpAccessToken` policy enforces the token for every user. Agent registration files store the token in plain text, and **Regenerate token** in the **Tools > MCP Server...** dialog invalidates every existing registration. See [Running on a shared machine](xref:mcp-server#running-on-a-shared-machine).

### Network endpoints

Allow these endpoints through your firewall or proxy for the AI features:

| Traffic | Endpoint |
| -- | -- |
| AI Assistant requests | The configured provider endpoint, for example `https://api.openai.com`, `https://api.anthropic.com`, an Azure OpenAI resource or your own gateway |
| AI model catalog | `https://api.tabulareditor.com/AiModels`. An anonymous request for the list of models, made when a user opens the model list for OpenAI or Anthropic. The list is cached for 24 hours. `DisableUpdates` turns it off |
| AI knowledge base updates | `https://cdn.tabulareditor.com`. A check at most once a day while the AI Assistant is configured, with no data about the user or the model. No policy turns it off except `DisableAi`. Users clear **Check for knowledge base updates on startup** under **Tools > Preferences > AI Features > AI Assistant** |
| MCP server | None |

License validation, update checks and telemetry use separate requests. See [Web requests](xref:security-privacy#web-requests).

### Data stored on the user's machine

All paths are under `%LocalAppData%\TabularEditor3` unless stated otherwise.

| Item | Location | Format |
| -- | -- | -- |
| Provider API key | `Preferences.json` | Encrypted with the Windows Data Protection API for the current user. Cleared when the AI component isn't loaded or `DisableAi` is set |
| MCP access token | `Preferences.json` | Encrypted with the Windows Data Protection API for the current user |
| Standing permission grants | `Preferences.json` | JSON |
| Per-model permission grants | The model's [user options](xref:user-options) (`.tmuo`) file: next to a model loaded from files, or under `UserOptions` for a model opened from a server | JSON |
| Conversations | `AI\Conversations` | Unencrypted JSON. Holds prompts, replies and tool results, including DAX query rows when **Model data** is at **Read**. Archived copies are written before each compaction. Files stay until the user deletes the conversation |
| User Custom Instructions | `AI\CustomInstructions` | Markdown |
| Knowledge base | `kb.sqlite` | SQLite database |
| AI model catalog | `AiModels.json` | JSON |
| Audit log | `AI\audit`, or the folder set by `AiAuditLogPath` | See [Audit log](#audit-log) |

## Permission grants

Permission grants control what the AI Assistant and the MCP server reach, with one access level per resource. The user sets each level under **Tools > Preferences > AI Features > Permissions**. On Enterprise Edition, an administrator can set a permission limit for each resource by policy:

| Resource | What the AI features reach | Default | Limit for both features | Limit for the MCP server only |
| -- | -- | -- | -- | -- |
| Model metadata | Read: the model definition and VertiPaq Analyzer statistics. Write: changing the model through C# scripts | Read | `MaxModelMetadataAccess` | `McpMaxModelMetadataAccess` |
| Model data | Read: DAX query results, which are data values from the model | Deny | `MaxModelDataAccess` | `McpMaxModelDataAccess` |
| Best Practice Analyzer | Read: rules and analysis results. Write: adding and changing rules | Read | `MaxBpaAccess` | `McpMaxBpaAccess` |
| Documents | Read: the contents of open C# script, DAX query and DAX script documents. Write: creating and overwriting them | Write | `MaxDocumentsAccess` | `McpMaxDocumentsAccess` |
| Macros | Read: the user's macro library, including macro code | Write | `MaxMacrosAccess` | `McpMaxMacrosAccess` |

At the default levels, the AI features read the model definition, run the Best Practice Analyzer, read the macro library and read and overwrite open script and query documents. They don't read data values and they don't change the model. Macro code and open documents can contain connection strings and other credentials. Set `MaxMacrosAccess` and `MaxDocumentsAccess` if they do in your organization.

The AI Assistant and the MCP server apply the grants as follows:

- **AI Assistant.** When a request needs access the standing grant doesn't cover, a permission card appears in the chat. The user allows it for the turn, for the session or always, and for **Model metadata** and **Model data** also for the current model. No card appears for access above a permission limit.
- **MCP server.** No prompt appears. The server reads the standing grants when it starts, and tools a grant doesn't cover aren't offered to the agent. Grants given for one model or one session apply to the chat only.

A permission limit outranks every user grant, including grants given for one model and grants given before the policy was set, and the matching setting offers only the levels up to the limit. An `McpMax...` limit only lowers the shared limit for the MCP server. See [Permissions and consent](xref:ai-assistant#permissions-and-consent).

## Safeguards on model changes

The AI features run scripts that change a model only when **Model metadata** is at **Write**. Every change runs through the [C# scripting engine](xref:csharp-scripts) against the model loaded in Tabular Editor 3:

- A script's changes form one undo entry, named **C# script (AI Assistant)** or **C# script (MCP)**.
- A script that fails part-way is rolled back completely.
- The AI Assistant runs scripts only when the user turns on **Allow AI assistant to run C# scripts directly**, which is off by default. With **Preview changes** on, the default, a preview dialog shows the changes from each script run and the user accepts or cancels them. Both settings are user preferences, with no policy to lock them.
- **Execute** on a script the AI Assistant writes in the chat runs it as the user's own script, at any **Model metadata** level. The safety check applies; the restrictions on `ReadFile` and the DAX helper methods below don't.
- An MCP agent's scripts run without a preview dialog. The user reviews the changes afterwards in the **TOM Explorer** and the **Properties** view, which mark every unsaved change.
- Changes stay unsaved in the loaded model until the user saves. No AI tool saves or deploys a model. Links in the assistant's replies can start Tabular Editor commands, including **Save** and **Deploy**, when the user selects them. If the user opened the model through a live connection to Analysis Services or a Power BI workspace, saving writes the changes to that server.
- A script that uses the file system, the network or an external assembly isn't run. The AI Assistant shows it with an **Unsafe** badge and **Execute** disabled. For an MCP agent it opens as a review document, or is refused when **Documents** is below **Write**.
- The safety check analyzes the compiled script. Reflection, expression trees, `Activator`, `AppDomain`, XML readers and deserialization count as unsafe.
- In a script the AI Assistant or an MCP agent runs, `ReadFile`, `SaveFile`, `Bpa.ExportCsv`, `ExecuteCommand`, calls that run a macro and Semantic Bridge calls always fail. `ExecuteCommand` sends Tabular Model Scripting Language (TMSL) and XML for Analysis (XMLA) commands to the server.
- In the same scripts, the DAX helper methods require **Model data** at **Read**, like the DAX query tool.

The `BlockUnsafeScripts` policy applies the same safety check to every script and macro: from the user, the Best Practice Analyzer, the AI Assistant, the MCP server or the Tabular Editor CLI. `DisableCSharpScripts` turns off C# script documents and removes the tool that runs scripts from the AI Assistant and both script tools from the MCP server. Macros keep running unless `DisableMacros` is also set. See [How an agent changes your model](xref:mcp-server#how-an-agent-changes-your-model).

## Administrator controls

Administrators enforce the controls through Windows group policy, with the administrative templates that ship with Tabular Editor 3 or by writing registry values directly. See @policies for the registry keys, value types and template setup.

A policy under `HKEY_LOCAL_MACHINE` outranks the same value under `HKEY_CURRENT_USER`. Standard users can't change either `Software\Policies` key. Tabular Editor 3 reads policies when it starts, and the MCP server reads permission grants when it starts, so a policy change reaches a running session after the user restarts Tabular Editor 3.

Enterprise Edition policies apply on Enterprise, Consultancy and Trial licenses. On Desktop and Business Edition, administrators can turn the AI features off, enforce the MCP access token, turn off C# scripts and macros and turn off telemetry. In the tables below, **All** means every edition of Tabular Editor 3.

### Turn the AI features off

| Requirement | Policy | Edition |
| -- | -- | -- |
| No AI features, and the AI component isn't installed | `DisableAi` | All |
| No AI Assistant, MCP server allowed | `DisableAiChat` | All |
| No MCP server, AI Assistant allowed | `DisableMcpServer` | All |

`DisableAi` also clears any stored provider configuration, including the API key. See [Deploying without the AI features](xref:installation-activation-basic#deploying-without-the-ai-features).

The portable build of Tabular Editor 3 has no installer step. It honors `DisableAi` at runtime. Use application control, such as AppLocker or Windows Defender Application Control, if users must not run older versions.

### Limit what the AI features reach

| Requirement | Policy | Edition |
| -- | -- | -- |
| A limit per resource for both features | `MaxModelMetadataAccess`, `MaxModelDataAccess`, `MaxBpaAccess`, `MaxDocumentsAccess`, `MaxMacrosAccess` | Enterprise |
| A lower limit per resource for MCP agents | `McpMaxModelMetadataAccess`, `McpMaxModelDataAccess`, `McpMaxBpaAccess`, `McpMaxDocumentsAccess`, `McpMaxMacrosAccess` | Enterprise |
| Withhold individual tools from MCP agents | `McpDisabledTools` | Enterprise |
| No C# script documents, AI script tools or macros | `DisableCSharpScripts` and `DisableMacros` | All |
| C# scripts that pass the safety check only | `BlockUnsafeScripts` | Enterprise |

Take the tool names for `McpDisabledTools` from the `tool_call` records in the audit log.

### Restrict the AI provider

| Requirement | Policy | Edition |
| -- | -- | -- |
| One approved provider | `AiProvider` | Enterprise |
| One approved endpoint or gateway | `AiEndpoint` | Enterprise |
| One approved model or Azure OpenAI deployment | `AiModel` | Enterprise |
| Billing to an approved OpenAI organization or project | `AiOrganizationId`, `AiProjectId` | Enterprise |
| A list of approved providers | `AiAllowedProviders` | Enterprise |
| A list of approved endpoint hosts | `AiAllowedEndpointHosts` | Enterprise |

`AiProvider`, `AiEndpoint`, `AiModel`, `AiOrganizationId` and `AiProjectId` replace the user's setting, and `AiProvider` set to `None` turns the AI Assistant off. If the configuration breaks `AiAllowedProviders` or `AiAllowedEndpointHosts`, the AI Assistant doesn't send the request and an error names the provider or endpoint host. `AiAllowedEndpointHosts` checks only an endpoint the user enters, so OpenAI and Anthropic without a custom endpoint reach their public API whatever the list holds. Pair it with `AiProvider` or `AiAllowedProviders`. No policy requires HTTPS; lock `AiEndpoint` to an `https://` address. Policies don't distribute API keys. With the endpoint locked to a resource your organization owns, such as an Azure OpenAI resource or an internal gateway, only keys your organization issues work. With a public endpoint such as `api.openai.com`, users can enter a personal key. These policies apply to the AI Assistant only.

### Custom Instructions and the MCP port

| Requirement | Policy | Edition |
| -- | -- | -- |
| Organization-approved Custom Instructions for every user | `AiCustomInstructionsPath` | Enterprise |
| Ignore Custom Instructions users write themselves | `DisableUserCustomInstructions` | Enterprise |
| MCP agents authenticate with an access token | `RequireMcpAccessToken` | All |
| A fixed MCP server port | `McpPort` | Enterprise |

### Enterprise policies on other editions

If any Enterprise policy value is present on a machine whose license isn't Enterprise, the AI Assistant and the MCP server don't start, and a `BlockUnsafeScripts` value stops every script and macro from running. A value Tabular Editor 3 can't interpret denies the resource for a permission limit, makes the AI Assistant unavailable for `AiProvider` and enforces `BlockUnsafeScripts`. Any other invalid value is ignored, and the setting it controls stays unrestricted. Roll out Enterprise policies only to machines with a matching license. See [What happens without Enterprise Edition](xref:policies#what-happens-without-enterprise-edition).

To check which policies apply on a machine, open **Tools > Preferences > Tabular Editor > Updates and Feedback**. The **Managed by your organization** section lists every policy value found, its source key and any value marked **(invalid)**.

## Audit log

On Enterprise Edition, Tabular Editor 3 writes a local record of AI Assistant and MCP server activity to one JSON Lines file per day. Each record carries a UTC timestamp, the feature (`chat` or `mcp`), the session and the open model's name where they apply, and the Windows user name. Nothing is recorded before a license is activated.

The log records:

- permission requests and the user's answer
- every tool call, with the tool name, the permissions it needed, its outcome (`ok`, `error`, `denied` or `cancelled`), its duration and the names and total size of its arguments
- every C# script sent to be run, including scripts that failed at run time, were refused or were handed back for review, saved as a `.csx` file with its SHA-256 hash
- the provider, model, endpoint host and token counts for each chat turn
- AI configuration changes
- MCP server start and stop, with the permission level of each resource
- MCP agent connections, with the name and version the client reports

Prompt text, reply text, argument values, data values from the model, API keys and access tokens aren't recorded. Scripts that fail to compile and scripts the AI features write into a document for the user to run aren't saved.

Files older than 30 days are deleted unless `AiAuditLogRetentionDays` sets another period, and `0` keeps every file. Each copy of Tabular Editor 3 deletes expired files from the folder it writes to before it writes its first record in a session.

The log is written by the user's own Tabular Editor 3 process, so the user has write and delete access to it, including on a redirected share. If the log can't be written, for example because the share is unreachable, the AI Assistant and the MCP server keep running and the failure is written once to Tabular Editor's application log.

`AiAuditLogPath` redirects the log. A relative path is ignored. Daily file names and script file names don't include the user or machine name, so give each user a separate folder. Environment variables such as `%USERNAME%` are expanded only in a `REG_EXPAND_SZ` value; the administrative template writes `REG_SZ`, which is used as written.

See @ai-audit-log for the record format.

## Recommended baseline

The following baseline is guidance for an organization that allows AI-assisted model development and keeps model data away from AI providers. Adjust it to your own risk assessment.

| Control | Setting | Effect |
| -- | -- | -- |
| Provider | `AiProvider`, `AiEndpoint`, `AiModel` and `AiAllowedEndpointHosts` set to a resource your organization owns and has a data processing agreement for | The AI Assistant sends requests only to that endpoint, with keys your organization issues |
| Model data | `MaxModelDataAccess` set to `Deny` | No DAX query result reaches the AI Assistant or an MCP agent |
| Macros | `MaxMacrosAccess` set to `Deny` | Macro code isn't sent to an AI provider |
| Scripts | `BlockUnsafeScripts` set to `1` | No script or macro writes files, reaches the network, starts other programs or loads outside code |
| MCP authentication | `RequireMcpAccessToken` set to `1` | Only clients with the user's access token connect to the MCP server |
| Audit retention | `AiAuditLogRetentionDays` set to your retention requirement | Audit files are kept for that period |
| Audit location | `AiAuditLogPath` set per user to a folder on a share | Audit files are collected centrally |

The following registry file applies the machine-wide part of the baseline. It locks the AI Assistant to an Azure OpenAI resource and keeps audit files for 365 days. Replace the endpoint and deployment name with your own, and apply the file only to machines licensed for Enterprise Edition:

```ini
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS]
"BlockUnsafeScripts"=dword:00000001

[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Tabular Editor ApS\TE3]
"AiProvider"="AzureOpenAI"
"AiEndpoint"="https://contoso-ai.openai.azure.com"
"AiModel"="tabular-editor-assistant"
"AiAllowedEndpointHosts"="contoso-ai.openai.azure.com"
"MaxModelDataAccess"="Deny"
"MaxMacrosAccess"="Deny"
"RequireMcpAccessToken"=dword:00000001
"AiAuditLogRetentionDays"=dword:0000016d
```

`BlockUnsafeScripts` sits in the shared key, so the Tabular Editor CLI enforces it as well. Set `AiAuditLogPath` to a folder for each user: either a `REG_EXPAND_SZ` value such as `\\fileserver\te-audit$\%USERNAME%` under the `HKEY_LOCAL_MACHINE` key, or a `REG_SZ` value per user under `HKEY_CURRENT_USER\SOFTWARE\Policies\Tabular Editor ApS\TE3`.

## Common questions

### Does Tabular Editor ApS receive our prompts, metadata or data?

No. See [Data flow](#data-flow).

### Is our data used to train AI models?

Tabular Editor ApS receives no prompts, replies or model content. Your agreement with the AI provider decides whether the provider trains on requests.

### Where is our data processed?

At the AI Assistant's configured endpoint, and wherever an MCP agent's provider runs. See [Restrict the AI provider](#restrict-the-ai-provider).

### Can users get around a policy?

A user can't change a policy without local administrator rights. Versions before 3.27.0, including older portable builds, read only `HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor` and ignore every policy on this page. See [Turn the AI features off](#turn-the-ai-features-off).

### Can the AI features change or deploy a production model?

They run scripts on the loaded model only with **Model metadata** at **Write**, and only the user saves or deploys. See [Safeguards on model changes](#safeguards-on-model-changes).

### Can the AI features read data from our models?

DAX query results require **Model data** at **Read**, and the default is **Deny**. Values typed into the model definition are part of the metadata. See [Data flow](#data-flow).

### Can an MCP agent use a provider we haven't approved?

Yes. Govern the agent through its own administrative controls, or set `DisableMcpServer`. See [MCP server](#mcp-server).

### How do we stop the AI features in an incident?

Set `DisableAi` and have users restart Tabular Editor 3. Revoke the affected API keys at the provider. See [Turn the AI features off](#turn-the-ai-features-off).

### Is the audit log tamper-evident?

No. The user can change and delete their own audit files. See [Audit log](#audit-log).

## See also

- @ai-assistant
- @mcp-server
- @ai-audit-log
- @policies
- @security-privacy
- @editions
