---
uid: mcp-server
title: MCP Server
author: Morten Lønskov
updated: 2026-09-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# MCP Server

Tabular Editor 3 can act as an MCP (Model Context Protocol) server. Any agent that speaks MCP, such as Claude Code, GitHub Copilot, VS Code agent mode, Codex or Cursor, connects to the running instance and works on the semantic model you have open: reading it, querying it, analyzing it and, if you allow it, changing it.

You don't configure an AI provider in Tabular Editor to use this. There's no API key to paste and no second subscription to buy. The intelligence comes from the agent you're already paying for, and Tabular Editor supplies what that agent has never had: the real model, loaded, validated and ready to edit.

## Why run the agent against Tabular Editor

An agent that edits model files on disk is working blind. It has the text of a `.bim` or a TMDL folder and no way to know whether the result loads, whether a measure's DAX resolves, or what the change did to the rest of the model. Tabular Editor closes that gap, because the agent isn't handed files. It's handed the model.

- **The model as it stands in front of you**, unsaved edits included. Whatever Tabular Editor has open is what the agent sees: a Power BI Desktop model, a PBIP project, a TMDL folder, a `.bim` file, a workspace database or a live connection to Analysis Services, Azure Analysis Services or Fabric. The agent works the same way against all of them, online or offline.
- **The same engine you use.** Agent changes go through the [Tabular Object Model wrapper](xref:csharp-scripts) and the same C# scripting engine, with the same validation, the same formula fixup and the same undo stack. An agent can't produce a model state you couldn't have produced by hand.
- **Analysis the agent can't do on its own.** [Best Practice Analyzer](xref:best-practice-analyzer) results, VertiPaq Analyzer statistics, DAX query results against live data and the Tabular Editor knowledge base are all tools the agent can call. It stops guessing about your model and starts measuring it.
- **A review step you can see.** Everything the agent does lands in your session as unsaved changes, marked in the [TOM Explorer and the Properties view](xref:unsaved-changes). You read the diff in the UI, revert the parts you don't want and save when you're happy. Nothing reaches the source until you save it.

That last point is the difference between delegating work and losing control of it. The agent proposes, your session holds the result, and you're the one who checks, test and save it.

## Before you start

- Tabular Editor 3.27.0 or later, any edition.
- The **AI features** component installed. It's part of a default installation from 3.27.0 onwards. See @installation-activation-basic if you deploy Tabular Editor centrally, and @policies if your administrator has turned AI features off.
- An agent that supports MCP over streamable HTTP.

## Start the server

1. Choose **Tools > MCP Server...**.
2. Check the permissions (see [Deciding what the agent may do](#deciding-what-the-agent-may-do) below). The defaults let an agent read your model, run the Best Practice Analyzer and work with your open document tabs, and stop it from reading your data or changing the model.
3. Click **Start server**.

The dialog shows the address the server is listening on, `http://127.0.0.1:42100/` unless you've changed the port. A status bar indicator switches from **MCP Stopped** to **MCP Started**, with the address in its tooltip.

![The MCP Server dialog, showing the server URL, a masked access token and the five agent permission rows](~/content/assets/images/features/mcp-server/mcp-server-dialog.png)

![The MCP status bar indicator reading MCP Started, with its tooltip showing "MCP server listening on http://127.0.0.1:42100/. Click to open the connection dialog."](~/content/assets/images/features/mcp-server/status-bar-menu.png)

The server works with or without a model open. An agent that connects while no model is loaded gets told so rather than getting an error, and you can open a model afterwards without restarting the MCP server.

Right-click the status bar indicator for the things you'll want day to day: starting and stopping the server, copying a registration configuration and the preferences page. Left-clicking it opens the dialog without changing whether the server is running.

![The MCP status bar indicator with its right-click menu open on MCP Server details..., Stop MCP server, Copy MCP configuration and MCP Server preferences..., and the Copy MCP configuration submenu expanded to list Claude Code, VS Code, Copilot CLI, Codex and Cursor](~/content/assets/images/features/mcp-server/status-bar-context-menu.png)

### MCP preferences

Open **Tools > Preferences > AI Features > MCP Server**. Here you can set the preferences for the MCP server to for example start it automatically at start up. 

![MCP Server preferences, showing Enable MCP Server, Start MCP server automatically, Require access token and the port](~/content/assets/images/pref-mcp-server.png)

| Preference | Default | What it does |
| -- | -- | -- |
| **Enable MCP Server** | On | Clearing it stops a running server and removes the menu item and the status bar indicator |
| **Start MCP server automatically** | Off | Starts the server when Tabular Editor starts, so your agent can connect without you thinking about it |
| **Require access token** | Off | Makes agents present the access token shown in the server dialog. See [Running on a shared machine](#running-on-a-shared-machine) |
| **Port** | 42100 | The loopback port the server listens on. Anything from 1024 to 49151. Changing it invalidates existing agent registrations |

Tick **Start MCP server automatically** once you're past experimenting. An agent registration points at a fixed address, so a server that's always there is a server you never have to think about again.

## Register your agent

You register Tabular Editor with your agent once. In the server dialog, pick your agent from **Export configuration** and paste what lands on the clipboard. The configuration carries the address, and the access token if you've turned that on. The server registers itself under the name `tabular-editor`.

![The Export configuration dropdown, expanded to list Claude Code, VS Code, Copilot CLI, Codex and Cursor](~/content/assets/images/features/mcp-server/export-configuration.png)

**Claude Code.** Run the copied command in a terminal:

```bash
claude mcp add --transport http tabular-editor http://127.0.0.1:42100/
```

**VS Code**, in your MCP configuration:

```json
{
  "servers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Copilot CLI**, in `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "type": "http",
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

**Codex**, in `~/.codex/config.toml`:

```toml
[mcp_servers.tabular-editor]
url = "http://127.0.0.1:42100/"
```

**Cursor**, in `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tabular-editor": {
      "url": "http://127.0.0.1:42100/"
    }
  }
}
```

With **Require access token** on, each of these carries the token too, in the shape its own format wants.Copy the configuration from the dialog rather than writing it by hand and you get the right one.

Any other MCP client works too. Point it at `http://127.0.0.1:42100/` over streamable HTTP, and add the same header if you've required the token.

### Check that it worked

Ask your agent *what model am I connected to in Tabular Editor?* It answers with the model name, how the model is loaded, whether it has unsaved changes and its compatibility level. With no model open it says so, which is also a correct answer.

Nothing prompts you in Tabular Editor. That's the point: the permissions were settled before the agent connected.

## Deciding what the agent may do

An agent connecting over MCP works unattended and you decide up front what the agent can do through Tabular Editor. The same grants decide what the MCP server and the AI Assistant can do. They sit on the **Tools > MCP Server...** dialog itself, so you can set them on your way to starting the server, and on **Tools > Preferences > AI Features > Permissions**, which is the same setting in both places. The agent is handed exactly the tools your grants cover. Anything else is never offered to it.

Hovering a permission, either its label or its dropdown, describes what that level gives the agent. Where an administrator has capped a resource by [policy](xref:policies), the dropdown is read-only and says so.

There are five resources, each with one access level:

| Resource | Default | What the agent gets |
| -- | -- | -- |
| **Model metadata** | Read | Read: tables, columns, measures, expressions, descriptions, relationships and VertiPaq Analyzer statistics. Write: the ability to change the model through C# scripts |
| **Model data** | Deny | Read: DAX query results, so actual values from your model. Needs a live connection |
| **Best Practice Analyzer** | Read | Read: the rule set and the analysis results. Write: adding and modifying rules |
| **Documents** | Write | Read: the contents of your open C# script and DAX query tabs. Write: creating and modifying them |
| **Macros** | Write | Read: your macro library, with names, descriptions and code. Write is reserved for macro-editing tools that don't exist yet |

A **Write** grant covers Read, and the dialog labels that level **Read/Write** to make the point. **Model data** has no Write level, because there's no way to write data values back into a model.

Out of the box the agent reads your model and runs the Best Practice Analyzer. It can't read a single data value and it can't change the model. Those are the two grants you raise deliberately.

Note what the defaults *do* allow. **Documents** starts at Write, so an agent can create script and query tabs in your session and overwrite the contents of ones you already have open. Nothing is executed and nothing reaches the model, but it is a write, and it is the one default worth lowering if you keep work in progress in those tabs.

The two you raise deliberately are worth a moment's thought:

- **Model data > Read** is what sends values from your model to your agent, and through it to whichever provider your agent uses. Metadata describes your model, data *is* your model. Grant it when you want the agent to check its work against real numbers, and know that's what you're doing.
- **Model metadata > Write** is what turns the agent from an advisor into an editor. It's also the grant that gives you the most back, and the safeguards described in [How an agent changes your model](#how-an-agent-changes-your-model) exist to make it a reasonable thing to grant.

![The AI Features Permissions page, with one dropdown per resource at its default level](~/content/assets/images/pref-ai-permissions.png)

> [!IMPORTANT]
> Permissions are read when the server starts, and an agent is handed its tool list when it connects. After changing a grant, stop and start the server, then reconnect the agent. Until you do, the agent keeps working under the permissions that were in force when it connected.

## What the agent can do

When an agent connects, Tabular Editor offers it a set of capabilities shaped by your grants. You never invoke any of this yourself. What matters is knowing what you can ask for, and which grant a request depends on, because a capability your grants don't cover is never offered in the first place rather than being refused halfway through a task.

**Finding its way around.** Every agent can identify the instance it is talking to and the model that instance has open, search the Tabular Editor documentation, blog, GitHub issues and discussions, and look up the scripting API: the properties, methods and signatures available on the model objects. None of that touches your model, so none of it needs a grant.

That last part matters more than it sounds. It's why an agent writing a Tabular Editor script doesn't have to invent properties, functions or APIs from memory. It looks the signature up, in the version you're running.

**Reading the model.** With **Model metadata > Read**, which is the default, an agent can take an overview of your tables, their column and measure counts and every relationship; pull full detail for objects it names, including expressions, descriptions, format strings and data types; and search the model by name, description, DAX or M expression, format string or annotation. It can also ask for the model in full, though that is expensive and it is told so.

It can also see what you have selected in the TOM Explorer. That one is worth knowing about: select three measures, say *format these consistently*, and the agent knows what "these" means.

**Measuring the model.** **Best Practice Analyzer > Read** lets an agent list the effective rules, your own included, and run the analysis to get real violations back. **Best Practice Analyzer > Write** lets it add or change rules in your local collection. VertiPaq Analyzer statistics, meaning table sizes, column cardinalities and memory use, fall under **Model metadata > Read**. Running a DAX query and getting rows back needs **Model data > Read** on top of metadata access, and returns a bounded number of rows rather than an unbounded result set.

*Run the Best Practice Analyzer and fix what it finds* is the single most useful thing to delegate here, because the agent gets a concrete list of real problems in your model instead of generic advice about semantic models.

> [!NOTE]
> Querying data needs a live connection, and VertiPaq statistics need either a connection or statistics you have already collected. Both are settled when the agent connects, so if you connect the model afterwards, reconnect the agent to pick them up.

**Your documents and macros.** Listing your open script and query tabs needs only metadata access. Reading what is in them needs **Documents > Read**. Editing a tab, or putting a new C# script or DAX query in front of you to look at, needs **Documents > Write**. Anything an agent hands you this way is compiled, or validated against the open model, before you see it, so it has already had the chance to correct its own mistakes; a DAX query needs Tabular Editor connected to Analysis Services or Power BI for that validation to happen. Your macro library is a separate resource, read under **Macros > Read**.

**Changing the model.** That takes **Model metadata > Write**, and it works differently enough from everything above to be worth its own section. See [How an agent changes your model](#how-an-agent-changes-your-model) below.

## How an agent changes your model

With **Model metadata > Write**, an agent can change your model directly, and it does this by creating a [C# script](xref:csharp-scripts) in the background that Tabular Editor compiles, checks for safety and runs against the open model.

There is no second route, and that is deliberate. Anything the C# scripting API can do to a model can be asked for this way, so there's no list of supported operations to run out of: measures, columns, calculation groups, perspectives, translations, relationships, refresh policies, bulk renames, formatting passes. And because every change arrives the same way, there is one place where safety and review are enforced rather than one per operation. That indirection is what makes agent edits reviewable:

- **One undo step.** Everything a script did collapses into a single entry on the undo stack, whatever it touched. One **Ctrl+Z** puts the model back. See @undo-redo.
- **All or nothing.** A script that throws part-way through is rolled back completely. You never inherit half an edit.
- **A structured summary.** The agent gets back a description of every object it added, changed or removed, plus anything the script printed. It can tell you what it did without guessing, and it can tell when it did something other than what it intended.
- **Nothing waits for you.** A message a script would normally put on screen, through `Output`, `Info`, `Warning` or `Error`, is returned to the agent as part of the result instead of stopping the call on a dialog nobody is watching. While a long call runs, Tabular Editor shows a **Please wait** indicator and ignores clicks, so the window cannot be worked in against a model that is being changed underneath you, and clicks do not queue up and land the moment the agent finishes.
- **Marked in the UI.** Changed objects and properties are tinted and badged in the [TOM Explorer and the Properties view](xref:unsaved-changes) until you save. Use **Show changes** to filter both views down to the agent's work, and right-click **Revert** to undo a single property, a single object or a whole branch without touching the rest.

![The Edit menu open on a single Undo C# script (MCP) entry, with the TOM Explorer beside it marking an added measure in green, a changed measure in orange and a deleted measure struck through in red, and the Properties view filtered to the one property the agent changed](~/content/assets/images/features/mcp-server/agent-change-review.png)

That's the review loop: ask, watch it land, filter to what changed, revert what you disagree with, save. You're reviewing a diff in the tool you already know, not reading a summary and hoping.

The [AI Assistant](xref:ai-assistant) chat can run scripts the same way, and gets the same single undo step and the same rollback. Two things stay particular to an agent. It is never prompted, so there's no preview dialog and no **Cancel** to fall back on; the marked changes in the tree are your review step, after the fact rather than before it. And its undo entry is named *C# script (MCP)*, so you can tell an agent's work from the chat's in the undo dropdown.

### What an agent is never allowed to do

Some things are off the table regardless of your grants:

- **Raw TMSL and XMLA execution.** `ExecuteCommand` always fails for an agent-run script. It bypasses the object model, so it can't be undone or rolled back, which makes it incompatible with every guarantee above.
- **Anything outside the model.** A script that touches the file system, makes a web request or references an external assembly is never executed for an agent. It opens as an **Agent script (review)** document in Tabular Editor instead, and the agent is told you have to review and run it yourself. This needs the **Documents > Write** grant; without it the script is refused outright. The check is a semantic analysis of the compiled script rather than a scan of its text, so indirect routes to the same places, through reflection, expression trees, `Activator`, `AppDomain`, XML readers or deserialization, are refused too.
- **Querying data it wasn't granted.** The DAX helpers inside a script are gated on **Model data > Read** exactly like the query tool, so an agent can't reach data by wrapping a query in a script.

### Asking for a draft instead of a change

An agent doesn't have to execute anything. With **Documents > Write** it can put a C# script or a DAX query into a document in Tabular Editor for you to read and run yourself. The script is compiled and the query validated against your model before you see it, and errors go back to the agent, which can correct the document in place.

This is the right mode for a change you want to inspect before it happens, or for work you'd rather run against a different model later.

## A working session

The loop is: open the model, ask for something, watch it land, review it, save it. Here's what that looks like in practice.

**Start from what's wrong.** Open a model you inherited and ask:

> Run the Best Practice Analyzer and tell me what's worth fixing, worst first.

The agent runs the analysis, gets real violations with real object names, and reasons about your model instead of about semantic models in general. Follow up with *fix the format string violations*, and with **Model metadata > Write** granted it writes one script and runs it. The TOM Explorer fills with orange badges. Click **Show changes** in the [Properties view](xref:unsaved-changes) to read the before and after per property, right-click **Revert** on the two you disagree with and save.

**Start from a requirement.** Point the agent at a specification, a ticket or a spreadsheet of measure definitions:

> Add the measures in requirements.md to the Sales table. Follow the naming and format strings already used there.

It reads the existing measures first, so the new ones match what's already in the model rather than a convention it invented.



The requirements file comes from your agent's own workspace, not through Tabular Editor. That split is the whole arrangement: your agent brings the context it already has about your project, and Tabular Editor brings the model it could never see.

**Ask it to check its own work.** Grant **Model data > Read** and the agent can verify instead of assert:

> Confirm the new Margin % measure gives the same total as the old calculation for 2025.

It writes the DAX, runs it and compares. This is the grant that turns *I've added the measure* into *I've added the measure and here are the numbers*.

**Ask for a draft when you don't want a change.** Any time you'd rather read it first:

> Write me a script that renames every measure to sentence case, but don't run it.

The script arrives as a document in Tabular Editor, compiled and safety-checked, and you run it yourself when you've read it.

Two habits make all of this go better. Say which instance you mean when more than one is open: the agent can ask an instance which model it has, but it can't read your mind about which one you meant. And save, or at least review, between tasks: unsaved changes accumulate, and a smaller diff is a faster review.

## Running several instances

Each Tabular Editor instance hosts its own server on its own port, so you can run one agent against one model and a second agent against another.

Start the second instance, open **Tools > MCP Server...** and click **Start server**. The configured port is already taken, so Tabular Editor offers the next free one it finds within the following 20 ports. If all of those are busy it reports the conflict instead and you pick a port yourself in preferences. It never moves to a different port silently, because your agent registrations point at a fixed address and a silent move would break them.

Register the second port with your agent under its own name, and be explicit in your prompts about which one you mean.

## Running on a shared machine

The server binds to `127.0.0.1`, so nothing on another machine can reach it. Browser requests carrying a non-local `Origin` header are rejected on top of that, as a defense against DNS rebinding.

Loopback is a weaker boundary than it sounds, though. While the token is off, any process running on the machine can connect without credentials, and on a host where several people are signed in at once, a Remote Desktop or Citrix server for instance, that includes other people's sessions.

Tick **Require access token** under **Tools > Preferences > AI Features > MCP Server** and restart the server. Agents must then present the token shown in the server dialog, and the registration configurations you copy from the dialog include it. Requests without it are rejected.

The refresh button beside the token, tooltip **Regenerate token**, issues a new one. That invalidates every existing registration on purpose and restarts a running server, so use it when you think a token has been seen by someone it shouldn't have, and re-register your agents afterwards.

Administrators can make the token mandatory for everyone with the `RequireMcpAccessToken` policy, which also locks the preference. See @policies.

## What leaves your machine

Tabular Editor doesn't contact an AI provider when you work this way. It answers tool calls from a process on your own machine, over a loopback connection, and the knowledge base the agent searches is a local database that ships with the application and is refreshed from Tabular Editor's own service.

Your agent is what talks to a provider, under your own subscription and that provider's terms. So the question of what gets sent, and to whom, is answered where you already answer it for every other repository your agent works in. The lever you have on the Tabular Editor side is the permission grants: **Model data > Deny**, the default, means no value from your model can reach the agent in the first place, whatever it asks for.

See @security-privacy for the wider picture, including the [AI Assistant](xref:ai-assistant), which does call a provider directly and is configured separately.

## Administrator controls

The MCP server is on by default and any user can turn it off. Administrators have more than that:

- `DisableMcpServer` removes the feature entirely, leaving the AI Assistant chat alone.
- `DisableAi` turns off all AI functionality, the MCP server included, and keeps the AI component off the machine when the installer runs.
- `RequireMcpAccessToken` forces token authentication.
- `DisableCSharpScripts` stops an agent both running a C# script and drafting one into a document for you. Writing a DAX query, and everything that only reads, is unaffected.
- `BlockUnsafeScripts` keeps agent-run scripts but allows only the ones that stay within the model. It is the same line the agent already works to, applied to every script in Tabular Editor rather than to agent scripts alone, and it is enforced whatever the agent asks for. Enterprise tier.
- A set of Enterprise-tier policies caps what the AI Assistant and the MCP server may reach per resource. The `Max...` ceilings apply to both surfaces; the `McpMax...` ceilings apply to the MCP server alone and can only lower the shared one, so an unattended agent is never allowed more than the interactive chat. The same tier carries the audit log's location and retention, and the AI provider lock.

> [!WARNING]
> The Enterprise-tier policies fail closed. If any of their value names is present on a machine whose license is not Enterprise, Consultancy or Trial, the AI Assistant and the MCP server refuse to start, and the menu item and the status bar indicator disappear. One value set across a mixed fleet turns the feature off for everyone on the wrong edition, so roll these out against the licenses you actually have. See @policies.

On Enterprise Edition, Tabular Editor also keeps a local record of what the AI Assistant and the MCP server did, including every tool an agent called and the full text of any C# script it ran. Prompts, replies and data values are never recorded. **Open audit folder**, in the server dialog and on **Tools > Preferences > AI Features**, takes you to it. On Desktop and Business nothing is recorded and neither button is shown. See @ai-audit-log.

See @policies for the full list, the registry layout and the administrative templates, and @security-privacy for what leaves your machine.

## Troubleshooting

| What you see | What's happening |
| -- | -- |
| The agent says it has no tools for Tabular Editor | The server isn't running, or the agent connected before it was. Check the status bar reads **MCP Started**, then reconnect the agent |
| The agent can't see a permission you just granted | Grants are read at server start and the tool list is fixed at connect time. Stop and start the server, then reconnect the agent |
| The agent goes quiet after a long break | A session with no traffic for 20 minutes is closed. Reconnect the agent |
| The agent reports no model is open | The server runs independently of your model. Open a model in Tabular Editor and ask again; you don't need to restart anything |
| The agent can't run DAX queries | **Model data** is **Deny** by default. It also needs a live connection: against a model opened from disk, the query tool is unavailable whatever the grant says |
| Connections are rejected with 401 | **Require access token** is on and the agent isn't sending the token. Re-copy the registration configuration from the dialog, which includes it |
| The port is already in use | Another Tabular Editor instance or another application has it. Accept the next free port Tabular Editor offers, and update the agent's registration. With **Start MCP server automatically** on, a conflict at startup is silent: the indicator just reads **MCP Stopped** |
| **Tools > MCP Server...** isn't in the menu | **Enable MCP Server** is unticked in preferences, the AI features component isn't installed, an administrator has set `DisableMcpServer` or `DisableAi`, or an Enterprise-tier policy value is set on a machine that isn't licensed for it. See @policies |

## Next steps

- @ai-assistant for the permission model in full, and for the chat if you'd rather not bring your own agent.
- @unsaved-changes for reviewing and reverting what an agent did.
- @csharp-scripts for what a script can do, which is the ceiling on what an agent can do to your model.
- @policies for governing the server across an organization.

- @te-cli-skill if your agent works on model files in a repository or a pipeline rather than on a model you have open.
