---
uid: policies
title: Policies
author: Daniel Otykier
updated: 2026-09-17
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "Tabular Editor 2 reads the legacy registry key only, and honors only the policies marked TE2 below."
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "General policies only"
        - edition: Business
          partial: true
          note: "General policies only"
        - edition: Enterprise
          full: true
    - product: Tabular Editor CLI
      partial: true
      note: "On Windows, and only for the policies marked CLI below."
---

# Policies

If you administer Tabular Editor for an organization, you can limit its features, and configure the AI Assistant and the MCP server on your users' behalf, through group policy. Set the values in the Windows registry by hand, or use the administrative templates that ship with Tabular Editor 3.

Most policies are general policies, available in every edition of Tabular Editor 3. The policies that configure the AI Assistant and the MCP server require [Tabular Editor 3 Enterprise Edition](xref:editions), and are marked **Enterprise** below.

> [!NOTE]
> This functionality requires the following versions of Tabular Editor:
>
>   - Tabular Editor [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) or newer
>   - Tabular Editor [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) or newer, for the general policies
>   - Tabular Editor 3.27 or newer, for the registry keys below, for machine-wide policies and for every Enterprise policy
>   - Tabular Editor CLI 0.7 or newer

## Registry keys

Policies are read from six keys, and the first key that defines a value decides that value. Every key under `HKEY_LOCAL_MACHINE` outranks every key under `HKEY_CURRENT_USER`, so a machine-wide policy set through Computer Configuration cannot be overridden by the user. Within a hive, a product-specific key outranks the shared key, which outranks the legacy key:

```
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3
HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS
HKEY_LOCAL_MACHINE\Software\Policies\Kapacity\Tabular Editor
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS\TE3
HKEY_CURRENT_USER\Software\Policies\Tabular Editor ApS
HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor
```

- `Tabular Editor ApS\TE3` is read by Tabular Editor 3 only. The Tabular Editor CLI reads `Tabular Editor ApS\TECLI` in its place; the other four keys are the same for both.
- `Tabular Editor ApS` is the shared key, read by both Tabular Editor 3 and the CLI.
- `Kapacity\Tabular Editor` is the key used by earlier versions. It is still read, and it is the only key Tabular Editor 2 reads, so set a policy there too if it also has to reach Tabular Editor 2.

Precedence applies to each value separately: a machine-wide `DisableTelemetry` of 0 overrides a per-user `DisableTelemetry` of 1, while a `DisableCSharpScripts` set only per user still applies.
Value names are not case sensitive.

## Value types

| Kind of setting | Registry type | Notes |
|--|--|--|
| On/off policy | `REG_DWORD` | Any non-zero value enforces the policy. `0`, and the absence of the value, both mean it is not enforced. |
| Choice | `REG_SZ` | The name of the choice, for example `Read`. A `REG_DWORD` holding the position of the choice in the list is also accepted, which is what the administrative template writes. |
| List | `REG_MULTI_SZ` | One entry per line. A `REG_SZ` whose entries are separated by semicolons is also accepted. |
| Path, address or name | `REG_SZ` | |

Tabular Editor reads policy values once, at start-up. A change takes effect the next time you start the application.

## General policies

To enforce one of these, add a `REG_DWORD` value with the name below and a non-zero value. The **Products** column shows which products honor the policy: **TE3** is Tabular Editor 3, **CLI** is the Tabular Editor CLI, and **TE2** is Tabular Editor 2, which reads the legacy key only.

|Value|Products|When enforced...|
|--|--|--|
| DisableUpdates | TE3, TE2 | Tabular Editor will not check whether newer versions are available online. Users cannot check for updates manually either. |
| DisableCSharpScripts | TE3, TE2 | Tabular Editor will not let users create or execute C# scripts. |
| DisableMacros | TE3, TE2 | Tabular Editor will not let users save or run macros. Macros stored in the `%LocalAppData%` folder are not loaded when the application starts. |
| DisableBpaDownload | TE3, CLI, TE2 | Best Practice Analyzer rules cannot be downloaded from the web. Rules stored locally or alongside the model keep working. |
| DisableWebDaxFormatter | TE3, CLI, TE2 | The DAX formatter that sends code to daxformatter.com is disabled. Tabular Editor 3 still offers its built-in formatter, which sends nothing over the network. |
| DisableErrorReports | TE3 | Users cannot send error or crash reports to the Tabular Editor support team. |
| DisableTelemetry | TE3, CLI | No anonymous usage data is collected or sent to the Tabular Editor support team. |
| DisableDaxOptimizer | TE3 | The DAX Optimizer integration is not available. |
| DisableDaxOptimizerUpload | TE3 | Users cannot upload VertiPaq Analyzer files through the DAX Optimizer integration. Implied when `DisableDaxOptimizer` is enforced. |
| RequireDaxOptimizerObfuscation | TE3 | Users cannot upload clear-text VertiPaq Analyzer files through the DAX Optimizer integration; only obfuscated files may be uploaded. Implied when `DisableDaxOptimizer` or `DisableDaxOptimizerUpload` is enforced. |
| DisableDaxPackageManager | TE3 | The DAX Package Manager is not available. |
| DisableAi | TE3 | All AI functionality is turned off: the AI Assistant, the MCP server and every AI-powered feature are unavailable, nothing AI-related is loaded when the application starts, and any stored provider configuration, including the API key, is cleared. |
| DisableAiChat | TE3 | The AI Assistant chat panel is unavailable. Other AI functionality, including the MCP server, is unaffected. |
| DisableMcpServer | TE3 | The MCP server is unavailable, so external agent tools cannot connect to Tabular Editor 3. The AI Assistant chat is unaffected. |
| RequireMcpAccessToken | TE3 | Clients connecting to the MCP server must present the access token shown in the **Tools > MCP Server...** dialog, and users cannot turn that requirement off. |

## Enterprise policies

These policies configure the AI Assistant and the MCP server, and require Tabular Editor 3 Enterprise Edition. They are honored by Tabular Editor 3 only, and belong under `Tabular Editor ApS\TE3`.

### Permission limits

Each of these sets an upper limit on what the AI Assistant and the MCP server may reach for one kind of resource. The accepted values are `Deny`, `Read` and `Write`, except for model data, where `Read` is the highest meaningful setting.

A limit caps what a user may grant: an existing permission above the limit is reduced to it, the matching option under **Tools > Preferences > AI Features > Permissions** and in the **Tools > MCP Server...** dialog is shown read-only, and the AI Assistant no longer asks for permission it cannot be given. No grant outranks a limit - not a standing permission, not one given for a single model and not one given in an earlier version. The user's own choice is left untouched in their preferences, so it returns if the policy is removed.

|Value|Accepted values|Limits access to...|
|--|--|--|
| MaxModelMetadataAccess | Deny, Read, Write | The metadata of the open model: table, column and measure names, expressions, descriptions, Best Practice Analyzer results and VertiPaq statistics. `Write` additionally allows the assistant to run its own C# scripts against the model. At `Deny`, nothing about the open model is sent at all - no model summary, no notice that the model changed and no current selection. |
| MaxModelDataAccess | Deny, Read | Data values from the model, that is, the results of DAX queries. |
| MaxBpaAccess | Deny, Read, Write | Best Practice Analyzer rules. `Read` allows listing the rules and running the analysis; `Write` additionally allows adding and changing rules. |
| MaxDocumentsAccess | Deny, Read, Write | The documents the user has open, such as C# scripts and DAX queries. `Read` allows reading their contents; `Write` additionally allows changing them. |
| MaxMacrosAccess | Deny, Read, Write | The user's macro library. |
| McpMaxModelMetadataAccess | Deny, Read, Write | The same five resources, for the MCP server alone. |
| McpMaxModelDataAccess | Deny, Read | |
| McpMaxBpaAccess | Deny, Read, Write | |
| McpMaxDocumentsAccess | Deny, Read, Write | |
| McpMaxMacrosAccess | Deny, Read, Write | |

The five `McpMax...` values apply to the MCP server alone. When one of them is not set, the MCP server inherits the corresponding `Max...` limit. They can only lower that limit, never raise it, so an unattended agent is never allowed more than the interactive assistant.

### AI provider

|Value|Kind|Accepted values|What it does|
|--|--|--|--|
| AiProvider | Choice | None, OpenAI, Anthropic, AzureOpenAI, Custom | Locks the AI Assistant to one provider. `None` turns the AI Assistant off; the MCP server is not affected. |
| AiEndpoint | Address | | Locks the endpoint or base URL requests are sent to, for example an internal gateway or an Azure OpenAI resource. |
| AiModel | Name | | Locks the model, or the Azure OpenAI deployment name. The model picker in the chat panel is replaced by a plain indicator, so users cannot switch models. |
| AiOrganizationId | Name | | Locks the OpenAI organization requests are billed to. |
| AiProjectId | Name | | Locks the OpenAI project requests are billed to. |
| AiAllowedProviders | List | Any of the provider names above | Restricts which providers users may configure. A provider set by `AiProvider` is allowed whether or not it is listed, and `None` is always offered - an allowlist is not a way to stop a user turning the assistant off. |
| AiAllowedEndpointHosts | List | Host names | Restricts which hosts an endpoint may point at, for example `gateway.contoso.com` or `*.contoso.com`. |

Locked settings appear read-only under **Tools > Preferences > AI Features > AI Assistant**, and the AI Assistant uses the locked configuration whatever the user had chosen before. Nothing is written into the user's own preferences, so their provider, endpoint, model and API key come back if the policy is removed. API keys are never distributed by policy.

Host names are matched against the host part of the endpoint URL only. Matching ignores case and ignores the port. A leading `*.` covers the subdomains of a domain but not the domain itself, so list both if both are wanted. The list applies to every provider whenever an endpoint is set, so a base-URL override cannot be used to get past it.

A configuration the policy does not permit is refused, and the AI Assistant says which rule refused it instead of sending the request: a provider that is not on the allowlist, an endpoint host that is not on the host allowlist, an endpoint that is not a valid URL while a host allowlist applies, or a locked Azure OpenAI or Custom provider with no endpoint at all.

### Custom Instructions

|Value|Kind|What it does|
|--|--|--|
| AiCustomInstructionsPath | Path | Names a folder of Custom Instructions that the AI Assistant loads for every user, in addition to the ones that ship with the product. A UNC path to a read-only network share is supported. Where an organization instruction and a user's own instruction share the same identifier, the organization's wins. |
| DisableUserCustomInstructions | On/off | The AI Assistant ignores Custom Instructions the user has placed in their own folder, and the button that opens that folder is disabled. Instructions that ship with the product, and any organization folder, still load. |

### MCP server

|Value|Kind|What it does|
|--|--|--|
| McpDisabledTools | List | Names of MCP tools that are never offered to a connected client. Listed tools are absent from the client's tool list and refuse to run even if a client asks for one by name. The AI Assistant chat is not affected. |
| McpPort | Number, 1024 to 49151 | Locks the port the MCP server listens on, so one client configuration can be shared across an organization. The default is 42100. The server only ever listens on the loopback address. |

### Audit log

Tabular Editor 3 keeps a local record of AI Assistant and MCP server activity - tool calls, permission decisions, configuration and server sessions. The text of a prompt or a response is never recorded. The log is written in every edition; these two policies, which change where it goes and how long it is kept, require Enterprise Edition.

|Value|Kind|What it does|
|--|--|--|
| AiAuditLogPath | Path | Redirects the audit log, so it can be collected centrally. A UNC path to a network share is supported. When the policy is not set, the log is written to the user's local application data folder. |
| AiAuditLogRetentionDays | Number, 0 to 3650 | How many days of audit log to keep; older files are deleted. `0` keeps everything. The default is 30 days. |

## What happens without Enterprise Edition

Enterprise policies are never quietly ignored. If any of the values in the Enterprise tables above is set - even one Tabular Editor cannot interpret - and the installed copy of Tabular Editor 3 is not licensed for Enterprise Edition, the AI Assistant and the MCP server refuse to start, and the AI Assistant reports that your organization has configured AI policies that require Tabular Editor 3 Enterprise Edition, naming the values in question. Everything else in Tabular Editor 3 keeps working, and the general policies above keep being enforced.

Enterprise policies also fail closed when a value cannot be interpreted. A permission limit that is mistyped denies the resource rather than being read as "no limit", and a provider name Tabular Editor does not recognize makes the AI Assistant unavailable rather than falling back to the user's own choice.

To turn off all AI functionality without an Enterprise license, use the general `DisableAi` policy.

## Seeing which policies are in effect

Open **Tools > Preferences > Tabular Editor > Updates and Feedback**. When any policy is set, a **Managed by your organization** section lists every value Tabular Editor found, the value itself and which registry key and hive it came from. A value Tabular Editor could not interpret is marked *(invalid)*, which is the quickest way to find a typo in a policy that appears to have no effect.

Controls that a policy has locked or limited elsewhere in **Preferences**, and in the **Tools > MCP Server...** dialog, are shown read-only and carry a tooltip saying the setting is controlled by your organization's policy.

## Using the administrative templates

Tabular Editor 3.27 and newer install a Group Policy administrative template pair, so the policies above can be set from the Group Policy editor instead of by editing the registry. You will find them in the `Policies` folder of the installation folder, which by default is `C:\Program Files\Tabular Editor 3\Policies`:

- `TabularEditorApS.admx`
- `en-US\TabularEditorApS.adml`

To use them on a single machine, copy both files into `%SystemRoot%\PolicyDefinitions`, keeping the `en-US` folder structure:

```
C:\Windows\PolicyDefinitions\TabularEditorApS.admx
C:\Windows\PolicyDefinitions\en-US\TabularEditorApS.adml
```

To use them across a domain, copy them into the central store on a domain controller instead, keeping the same structure:

```
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\TabularEditorApS.admx
\\<your-domain>\SYSVOL\<your-domain>\Policies\PolicyDefinitions\en-US\TabularEditorApS.adml
```

Then open the Local Group Policy Editor (`gpedit.msc`) or the Group Policy Management Editor, and look under:

- **Computer Configuration > Administrative Templates > Tabular Editor** for machine-wide policies
- **User Configuration > Administrative Templates > Tabular Editor** for per-user policies

Policies shared by Tabular Editor 3 and the CLI sit directly under **Tabular Editor**. Policies Tabular Editor 3 honors alone are under **Tabular Editor > Tabular Editor 3**, with the AI Assistant, the MCP server and the DAX Optimizer integration in subfolders of their own.

Setting a policy to **Enabled** writes its registry value. Setting it to **Disabled**, or leaving it **Not configured**, means the policy is not enforced. The templates do not write to the legacy `Kapacity\Tabular Editor` key, so set that key by hand if a policy also has to reach Tabular Editor 2.

## Disabling web communications

If you want to ensure that Tabular Editor does not perform web requests, specify the `DisableUpdates`, `DisableBpaDownload`, `DisableWebDaxFormatter`, `DisableErrorReports`, `DisableTelemetry`, `DisableDaxOptimizer`, `DisableDaxPackageManager` and `DisableAi` policies.

> [!NOTE]
> Even when the above policies are specified, Tabular Editor 3 will still make occasional requests to `https://api.tabulareditor.com` for purposes of license validation. If Tabular Editor 3 is not able to reach this endpoint (due to a firewall or proxy), the user will have to [manually activate](xref:installation-activation-basic#manual-activation-no-internet) the product every 30 days.

## Disabling custom scripts

If you want to ensure that Tabular Editor does not allow users to execute arbitrary code, specify the `DisableCSharpScripts` and `DisableMacros` policies.

## Disabling AI features

If you want to prevent all AI functionality, specify the `DisableAi` policy. This prevents anything AI-related from loading at startup and clears any stored API key configuration. It applies in every edition and needs no Enterprise license.

From 3.27.0 the installer reads the policy too, from all six keys and with the same precedence, and leaves the AI component out entirely, so the AI assemblies are never written to the installation folder on a machine whose policy disables AI. Set the value as a `REG_DWORD` of `1`: the installer treats `1` as *disable* and any other present value as *not disabled*, where the application accepts any non-zero number. See [Deploying without the AI features](xref:installation-activation-basic#deploying-without-the-ai-features) for deploying the feature selection and the policy together.

To keep the AI Assistant available but confine what it may do, use the Enterprise policies above instead: set the permission limits to what your organization is comfortable with, lock the provider and endpoint to a gateway you operate, and use `McpDisabledTools` to withhold individual tools from connected agents.
