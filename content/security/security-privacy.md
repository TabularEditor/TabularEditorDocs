---
uid: security-privacy
title: Security overview
author: Daniel Otykier
updated: 2026-09-17
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Tabular Editor 3 Security and Privacy

This document describes the security and privacy considerations of Tabular Editor 3 and its use. In the following, the phrase "Tabular Editor" can mean both the commercial tool Tabular Editor 3, as well as the open-source tool Tabular Editor 2.X. Whenever something considers only one of the tools, we will use their explicit names "Tabular Editor 3" or "Tabular Editor 2.X".

## Microsoft advice on third-party tools such as Tabular Editor

Microsoft supports the use of community third-party tools as communicated here: [Community and third-party tools for developing enterprise-level Power BI and Analysis Services models]( https://powerbi.microsoft.com/en-us/blog/community-tools-for-enterprise-powerbi-and-analysisservices)

Microsoft's Power BI implementation planning documentation specifically includes Tabular Editor in advanced data modeling scenarios and enterprise development: [Power BI usage scenarios: Advanced data model management](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-advanced-data-model-management#tabular-editor)

## Trust Center
At Tabular Editor, we are committed to transparency and strong security practices. Visit our [Trust Center](https://trust.tabulareditor.com/) to find details about our SOC 2 audit report, key policy documents, license terms, and our approach to infrastructure and organizational security. You’ll also find information about our sub-processors and how we work to keep your data safe.

## Metadata and Data Privacy

Tabular Editor is primarily an offline tool, meaning that all data and metadata reside locally in the client machine on which Tabular Editor is installed, and all user interactions are performed locally as well. An Internet connection is not required to run and use Tabular Editor.

That being said, there are scenarios in which Tabular Editor connects to remote services for various purposes. These are described in the following:

### Analysis Services XMLA Protocol

All communication with Analysis Services instances or Power BI Premium workspaces happens through the use of the [Microsoft Analysis Management Objects (AMO)](https://docs.microsoft.com/en-us/analysis-services/amo/developing-with-analysis-management-objects-amo?view=asallproducts-allversions) client libraries, or more specifically, the [Tabular Object Model (TOM) extension for AMO](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions). These client libraries are provided by Microsoft for redistribution in 3rd party applications such as Tabular Editor. For licensing details, please refer to the [AMO EULA](https://go.microsoft.com/fwlink/?linkid=852989).

When Tabular Editor connects to an instance of Analysis Services (local network or cloud) or a Power BI Premium workspace (cloud), this connection is performed through the client libraries mentioned above. By design, the AMO library handles the authentication and authorization of the user. Only users with administrative privileges on the Analysis Services instance or Power BI Premium workspace, are allowed to connect. This is no different than when using Microsoft tools such as SQL Server Management Studio or SQL Server Data Tools (which use the same client libraries for connectivity).

### Tabular Object Model metadata

Once the AMO/TOM client library establishes connection, Tabular Editor will request the full Tabular Object Model (TOM) metadata for the specific Analysis Services database or Power BI dataset that the user wants to connect to. The AMO/TOM client library then serves this metadata to the client application (Tabular Editor) in a programmatic approach, allowing the application to apply metadata changes, such as renaming an object, adding a description, modifying a DAX expression, etc. In addition, the AMO/TOM client library provides methods for serializing the TOM metadata into a JSON-based format. Tabular Editor uses this technique to allow users to save the model metadata as a local JSON file, for purposes of version control of the data model structure. **Note: The JSON file produced this way contains no actual data records. The file contains only model metadata, that is, information about the structure of the model in terms of tables, columns, measures, DAX expressions, etc.** While model metadata is generally not considered confidential information, it is the responsibility of the user of Tabular Editor to handle any file produced this way with the required confidentiality (i.e. not sharing the file with 3rd parties, etc.).

**Tabular Editor does not collect, publish, share, transfer or otherwise make public any model metadata obtained through the AMO/TOM client library unless the user specifically initiates an action to do so** (for example by saving the model metadata JSON file to a shared network location, or deploying the model metadata to another instance of Analysis Services or Power BI workspace).

### Model data content

In the following, "model data" refers to the actual data records stored within the Analysis Services database or Power BI dataset. Depending on the source database or dataset, it is very likely that the model data is confidential.

Because of the requirement for a user to have administrative privileges on the instance of Analysis Services or Power BI workspace that they are connecting to, the user will, by definition, also have access to all data content of the Analysis Services database or Power BI dataset. Tabular Editor only allows retrieval of data through the AMO client library mentioned above. Tabular Editor 3 provides features for browsing and querying model data. Regardless of which technique is used to access the data **Tabular Editor only stores retrieved data in local memory. Tabular Editor does not collect, publish, share, transfer or otherwise make public any model data obtained through the tool**. If a user chooses to copy or export query results obtained through Tabular Editor, it is their responsibility to treat the copied or exported data according to the confidentiality of the data. This is no different than a user connecting to the Analysis Services database or Power BI dataset using client tools such as Excel or Power BI, in which case they will also have the option to copy query results.

### AI Assistant

Tabular Editor 3 includes an AI Assistant for chat-based semantic model development. From 3.27.0 it is part of a default installation; before that it had to be selected deliberately. If the component is not installed, no AI-related code is present on the machine and none of the behavior described in this section applies.

The AI Assistant uses a **bring-your-own-key** model. You provide an API key from a supported AI provider (OpenAI, Anthropic, Azure OpenAI or any OpenAI-compatible endpoint). No built-in API key is included and Tabular Editor does not provide or intermediate any AI service.

**Data flow.** All communication between the AI Assistant and the AI provider happens directly from the client machine to the provider API. No data passes through Tabular Editor servers. What is sent depends on what you ask for, and is bounded by five permission resources, each carrying one access level:

| Resource | What it covers | Levels | Default |
| -- | -- | -- | -- |
| Model metadata | Table, column and measure names, expressions, descriptions and similar. Read also covers VertiPaq Analyzer statistics | Deny / Read / Write | Read |
| Model data | Data values from your model, such as DAX query results. Requires a live connection | Deny / Read | Deny |
| Best Practice Analyzer | Read lists rules and runs the analysis; Write adds or modifies rules | Deny / Read / Write | Read |
| Documents | Your open C# script and DAX query editors. Read is their contents; Write is needed to create or modify them | Deny / Read / Write | Write |
| Macros | Your macro library | Deny / Read / Write | Write |

Write covers Read. Model data is denied by default, because metadata describes a model where data values are the model's contents.

**Permission management.** The grants are standing settings rather than per-request prompts. Review and change them under **Tools > Preferences > AI Features > Permissions**, or in the **Tools > MCP Server...** dialog, which edits the same record. Where the chat needs something a grant does not cover, it shows a permission card at that moment, and you answer for the turn, the session, the current model or always. **Always allow** raises the standing grant and never lowers one. Global grants are stored in the local Preferences.json file; grants given for a single model are stored in that model's user options (.tmuo) file and apply to the chat only. Setting a resource back to **Deny** makes the chat ask again.

**Administrator ceilings.** In the Enterprise, Consultancy and Trial editions, an administrator can cap each resource by [policy](xref:policies), separately for the chat and for the MCP server, and the MCP cap can only be lower. A cap outranks every grant, including one a user has already given, and the corresponding option is shown read-only. These policies fail closed: if any Enterprise-tier policy value is present on a machine that is not licensed for it, the AI Assistant and the MCP server refuse to start rather than ignoring the policy.

**Audit record.** Tabular Editor 3 writes a local record of what the AI Assistant and the MCP server did: which permissions were requested and how they were answered, which tools ran and whether each succeeded, failed or was refused, and the full text of any C# script an agent ran or handed over for review. Prompts, replies and data values are not recorded. The daily files are kept for 30 days, and **Open audit folder** under **Tools > Preferences > AI Features** opens them. Administrators can redirect the location and change the retention period.

**API key storage.** API keys are stored encrypted on the local machine in the Preferences.json file. If the AI module is not loaded (for example because it was excluded during installation or disabled by policy), any previously stored API key configuration is cleared automatically.

**Conversation storage.** Conversations are stored locally on the client machine in `%LocalAppData%\TabularEditor3\AI\Conversations\`. No conversation data is sent to Tabular Editor servers.

**Disabling the AI Assistant.** You can exclude the AI features component during installation, clear the provider under **Tools > Preferences > AI Features > AI Assistant**, or enforce a [policy](xref:policies) through the Windows registry: `DisableAi` turns off all AI functionality including the MCP server and clears stored provider configuration, while `DisableAiChat` turns off the chat alone and leaves the MCP server running.

**Penetration testing.** A separate penetration test of the AI Assistant has been performed. The report is available in our [Trust Center](https://trust.tabulareditor.com/).

### MCP server

Tabular Editor 3 can act as an MCP (Model Context Protocol) server, so that an AI agent running on the same machine can work on the model you have open. See @mcp-server for the feature itself.

**Network exposure.** The server is an HTTP listener bound explicitly to `127.0.0.1`, by default on port 42100. It is not reachable from another machine. Browser requests carrying a non-local `Origin` header are rejected as a defense against DNS rebinding. The server runs only after you start it, or from application start if you have asked for that.

**Authentication.** Loopback binding is the default boundary, so the server accepts local connections without credentials out of the box. On a host where several people are signed in at once, such as a Remote Desktop or Citrix server, that is not sufficient: any session on the machine reaches `127.0.0.1`. While the token is off, any process on the machine can connect without credentials. Turn on **Require access token** under **Tools > Preferences > AI Features > MCP Server**, and clients must present a bearer token, which is stored encrypted in the local Preferences.json file. Administrators can enforce this with the `RequireMcpAccessToken` [policy](xref:policies).

**Data flow.** Tabular Editor does not contact an AI provider for this feature and holds no API key for it. The agent is the only party that talks to a provider, under its own configuration and its own subscription. What the agent can read from the model is bounded by the same five permission grants that govern the AI Assistant, snapshotted when the server starts, and any tool a grant does not cover is never offered to the agent. Model data is denied by default, so no data values leave the model unless you grant that explicitly.

**Changes to the model.** An agent changes the model only through the C# scripting engine, atomically and as a single undo step, and only with the model metadata grant at Write. Raw TMSL and XMLA execution is never available to an agent, and a script that reaches outside the model is never executed for it.

**Audit record.** Permission decisions, tool calls and the full text of any C# script an agent ran or handed over for review are written to a local audit log. Prompts, replies and data values are not recorded.

**Disabling the MCP server.** Clear **Enable MCP Server** under **Tools > Preferences > AI Features > MCP Server**, or enforce the `DisableMcpServer` or `DisableAi` [policy](xref:policies). The server is part of the AI features component, so excluding that component at install time removes it as well.

### Web requests

Tabular Editor may perform requests to online resources (web URLs) only in the following cases:

- **License activation\*.** When Tabular Editor 3 is first launched, and at periodic intervals thereafter, the tool may perform a request to our licensing service. This request contains encrypted information about the license key entered by the user, the e-mail address of the user (if provided), the local machine name and a one-way encoded hash identifying the current installation. No other data is transmitted in this request. The purpose of this request, is to activate and validate the license key used by the installation, enforce trial limitations, as well as allowing the user to manage their installations of Tabular Editor 3 through our licensing service.
- **Upgrade checks\*.** Each time Tabular Editor 3 is launched, it may perform a request to our application service, in order to determine if a newer version of Tabular Editor 3 is available. This request does not contain any data.
- **Usage telemetry\*.** By default, Tabular Editor 3 collects and transmits anonymous usage data as users interact with the tool. This data includes information about which UI objects a user interacts with and the timing of each. It also contains high-level information about the Tabular data model being edited through the tool. This information only relates to high-level properties like compatibility level and mode, number of tables, type of server (Analysis Services vs. Power BI vs. Power BI Desktop), etc. **No personally identifiable data is collected this way**, neither do we collect any information about names of objects or DAX expressions in the Tabular Object Model itself. A user may opt out of sending telemetry data to us at any point.
- **Error reports\*.** When an unexpected error occurs, we transmit the stack trace and (anonymized) error message, along with an optional description provided by the user. If a user opts out of sending telemetry data, error reports will also not be sent.
- **Using the DAX formatter.** (Tabular Editor 2.x only) A DAX expression may be formatted by clicking a button in Tabular Editor. In this case, the DAX expression (and nothing else) is sent to the www.daxformatter.com webservice. The first time a user clicks this button, an explicit warning message is shown, asking them to confirm their intent. Tabular Editor 3 does not perform web requests when formatting DAX code.
- **DAX Optimizer**. If a user has a [Tabular Tools account](https://tabulartools.com) with a [DAX Optimizer](https://daxoptimizer.com) subscription, they will be able to browse their DAX Optimizer workspace, view issues and suggestions, and upload new VPAX files directly from within Tabular Editor 3. VPAX files contains model metadata and statistics, but no actual model *data*. The DAX Optimizer Integration feature in Tabular Editor 3 causes various requests to one or more of the below endpoints (depending on authentication type and region specified when the Tabular Tools account was created).<br/>
  For more information, please consult the [DAX Optimizer documentation](https://docs.daxoptimizer.com/legal/data-processing).<br/>
  Endpoints used:
  - https://account.tabulartools.com
  - https://licensing.api.daxoptimizer.com/api
  - https://australiaeast.api.daxoptimizer.com/api
  - https://eastus.api.daxoptimizer.com/api
  - https://westeurope.api.daxoptimizer.com/api
- **AI Assistant.** When the AI Assistant is configured and in use, Tabular Editor 3 sends requests directly to the configured AI provider API. The endpoints depend on the selected provider (for example `https://api.openai.com` for OpenAI, `https://api.anthropic.com` for Anthropic, or a user-specified endpoint for Azure OpenAI and custom providers). Only data covered by the permission grants is included in these requests. See the [AI Assistant](#ai-assistant) section above for the resources and their defaults.
- **AI knowledge base updates.** The knowledge base the AI Assistant searches is a local database that ships with the AI features component. Tabular Editor 3 checks for a newer copy and downloads it from `https://cdn.tabulareditor.com`. The request carries no data about you or your model.
- **MCP server.** The MCP server makes no outbound requests. It accepts connections on the loopback interface only, and the agent that connects to it is what talks to an AI provider, under its own configuration. See the [MCP server](#mcp-server) section above.
- **Importing Best Practice Rules.** Tabular Editor has a feature that allows a user to specify an URL from which to retrieve a list of Best Practice rules in a JSON based format. This type of request only downloads the JSON data from the URL - no data is transmitted to the URL.
- **Using C# scripts.** Tabular Editor allows users to write and execute code written in C#, for purposes of automation. Such a script may potentially connect to online resources, using C# language features and the .NET runtime. The user is always responsible for ensuring that executed code does not cause any unintended sharing of data. Tabular Editor ApS cannot be held liable for any damages, losses or leaks caused by the use of the C# scripting feature in general. Tabular Editor will never execute C# scripts without the explicit action of the user.

\***Any information we obtain through the license activation service, the usage telemetry or the error reports, is kept confidential. We will not share, publish or distribute the data collected in any way, shape or form.**

**Firewall allowlist / acceptlist**
To allow traffic to the above mentioned web requests, you'll have to whitelist:
- License activation / upgrade checks: **https://api.tabulareditor.com**
- Usage telemetry / Error reports: **https://*.in.applicationinsights.azure.com**
- DAX Formatter (Tabular Editor 2.x only): **https://www.daxformatter.com**
- Import Best Practice Rules / C# Scripts: Depends on the context
- DAX Optimizer: Endpoints listed above.
- AI Assistant: Depends on the configured provider (e.g. **https://api.openai.com**, **https://api.anthropic.com**, or user-specified Azure OpenAI / custom endpoints)
- AI knowledge base updates: **https://cdn.tabulareditor.com**
- MCP server: nothing. It listens on **127.0.0.1** and makes no outbound requests

> [!NOTE]
> A system administrator may enforce certain [policies](xref:policies), which can be used to disable some or all of the features shown on the list above.

## Application Security

Tabular Editor does not require any elevated privileges on the Windows machine in which it is installed, neither does it access any restricted resources on the machine. One exception from this rule, is if using the Tabular Editor installer file (.msi), in which case the executable and support files required by the tool, are by default copied to the `Program Files` folder, which typically requires elevated permission. Both the Tabular Editor binary files as well as the installer file, have been signed with a code signing certificate issued to Tabular Editor ApS, which is your guarantee that the code has not been tampered with by any 3rd party.

When the application is executing, all access to external resources are performed through the AMO/TOM client library or the web requests mentioned above.

The C# script feature allows Tabular Editor to execute arbitrary C# code within the .NET runtime. Such code is only compiled and executed on the explicit request of the user. C# scripts may also be saved as "macros", which makes it easier for the user to manage and execute multiple different scripts. The code is stored to the users own `%localappdata%` folder, ensuring that only they or a local machine administrator, can access the scripts. The user is always responsible for ensuring that executed code does not cause any unintended sideeffects. Under no circumstance can Tabular Editor ApS be held liable for any damages, losses or leaks caused by the use of the C# scripting or custom actions/macros features.

Organizations that do not want this left to the individual user can govern it centrally. The `DisableCSharpScripts` and `DisableMacros` [policies](xref:policies) turn the features off entirely, in every edition. With Tabular Editor 3 Enterprise Edition, `BlockUnsafeScripts` keeps scripting available but allows only scripts and macros that stay within the semantic model: anything that reads or writes a file, reaches the network, starts another program or loads outside code is refused before it runs, wherever the script came from - a script document, the Best Practice Analyzer, a macro, the AI Assistant, the MCP server or the command line. See [Administrator policies](xref:csharp-scripts#administrator-policies).
