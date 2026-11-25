---
uid: preferences
title: Controlling preferences
author: Morten Lønskov
updated: 2026-11-13
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
# Tabular Editor 3 Preferences

The Preferences dialog controls Tabular Editor 3's user interface, file formats, connectivity, data browsing, AI features and editor behavior.

This article describes the Tabular Editor 3 Preferences dialogs and the settings that you can control through it.

To access the preferences dialog, go to **Tools > Preferences**.

> [!NOTE]
> All Tabular Editor preferences are stored for each Windows user profile, in the `%localappdata%\TabularEditor3` folder. It is possible to migrate your settings to another machine by simply copying the contents of this folder.

> [!TIP]
> Use the search box at the top of the Preferences dialog to quickly find specific settings.

## Tabular Editor > Power BI

![The Power BI preferences page](~/content/assets/images/pref-power-bi.png)

### Power BI Desktop

**Allow unsupported modeling operations (pre-June 2025, not recommended)** (disabled): Applies only to Power BI Desktop versions older than June 2025, which restrict the modeling operations an external tool can make. When checked, all TOM properties are available for editing while Tabular Editor 3 is connected to such a version, including changes that Power BI Desktop doesn't support. The setting has no effect on Power BI Desktop June 2025 or later.

### Power BI Service

**API base URL** (`https://api.powerbi.com`): The base URL of the Power BI REST API, which Tabular Editor calls when it lists the workspaces you have access to, for example when you import tables from Power BI dataflows. The list also offers the sovereign cloud endpoints `https://api.powerbigov.us`, `https://api.high.powerbigov.us`, `https://api.mil.powerbigov.us`, `https://api.powerbi.de` and `https://api.powerbi.cn`, and you can type another URL.

**Default authentication** (Integrated): The authentication mode used by default when you connect to a Power BI or Fabric XMLA endpoint or to Azure Analysis Services: **Integrated**, **Microsoft Entra MFA** or **Username and password**.

### Dataset Preferences

**Hide auto date/time warnings** (disabled): Hide the warnings that the DAX analyzer raises for the date tables Power BI Desktop adds when its auto date/time option is enabled. The DAX expressions on these tables don't follow best practices.

**Line break on first line of DAX** (disabled): Make the first character of every DAX expression you edit a line break, which keeps the expression readable in the Power BI Desktop formula bar. Applies to Power BI semantic models only.

**Only for multi-line DAX expressions** (enabled): Available while **Line break on first line of DAX** is checked. Add the line break only to expressions that span more than one line.

## Tabular Editor > Proxy Settings

![The Proxy Settings preferences page](~/content/assets/images/pref-proxy-settings.png)

Configure the proxy server Tabular Editor uses for web requests. See @proxy-settings for troubleshooting.

### Proxy Settings

**Proxy Type** (None):

- **None**: connect without a proxy
- **System**: use the proxy configured in Windows
- **Custom**: use the proxy configured in the **Custom proxy** section

### Custom proxy

These settings are available when **Proxy Type** is **Custom**.

**Proxy address**: The address of the proxy server, for example `http://proxy.company.com:8080`.

**Use default credentials** (enabled): Authenticate to the proxy with your Windows credentials, the [same behavior as Power BI Desktop](https://learn.microsoft.com/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy).

**Username** and **Password**: The credentials for proxy authentication. Available when **Use default credentials** is cleared. The password is stored encrypted.

### Proxy bypassing

These settings apply when **Proxy Type** is **Custom**.

**Bypass on local** (enabled): Send requests to local addresses directly, without the proxy.

**Bypass list**: Addresses that skip the proxy, separated by semicolons.

## Tabular Editor > Modeling Operations

![The Modeling Operations preferences page](~/content/assets/images/pref-modeling-operations.png)

### Formula fix-up

**Automatic DAX formula fix-up** (enabled): Update the DAX expressions that reference an object when you rename it.

### Clipboard Operations

**Include metadata translations when copying objects** (enabled): Include the object's metadata translations when you copy it to the clipboard.

**Include perspective membership when copying objects** (enabled): Include the perspectives the object belongs to when you copy it to the clipboard.

**Include RLS when copying tables** (enabled): Include the table's row-level security expressions from every role when you copy a table to the clipboard.

**Include OLS when copying tables/columns** (enabled): Include the object-level security settings from every role when you copy a table or column to the clipboard.

**Fix-up table references upon paste/duplicate** (enabled): When you paste or duplicate a table, update the references to that table in the DAX expressions of its objects to the new table name.

### Perspective Membership Inheritance

**Inherit table membership when an object is created on a table** (disabled): New objects are added to the perspectives currently selected. When checked, a new object also joins the perspectives its table belongs to.

**Inherit table membership when an object is pasted/moved to a table** (disabled): When checked, an object you paste or move to a table takes the perspective membership of that table. When cleared, its perspective membership stays unchanged.

**When a table is added to a perspective, also add all child objects to that perspective** (enabled): Add the table's columns, measures and hierarchies to a perspective together with the table.

**When a table is removed from a perspective, also remove all child objects from that perspective** (enabled): Remove the table's columns, measures and hierarchies from a perspective together with the table.

## Tabular Editor > Updates and Feedback

![Updates and Feedback preferences](~/content/assets/images/pref-updates-and-feedback.png)

### Updates

**Show "Get Started" page on updates** (enabled): When checked, the **Get Started** page opens automatically the first time you run Tabular Editor after it has been updated. It appears **on updates**, not on every start-up. You can open it at any time from **Help > Get Started**.

**Check for updates on start-up** (enabled): Checks for a new version when the application starts.

**Major updates only** (disabled): When checked, only major version updates trigger notifications. Minor and patch updates are ignored. This setting is only available while **Check for updates on start-up** is checked.

Below these settings, the page shows the version you're running, for example **Current version: v28.0.0**, and a **Check for updates** button that runs the check immediately. After a check, the line adds **You are using the latest version.** or the version that's available. With **Major updates only** checked, the latest version means the latest major version.

### Managed by your organization

Where an administrator has configured [policies](xref:policies), a read-only **Managed by your organization** section is appended to this page listing every policy value Tabular Editor found, as `Name = value`. Hover over an entry to see which registry key and hive it came from.

A value Tabular Editor could not interpret is listed with an `(invalid)` marker rather than being left out. That marker is the fastest way to find the typo behind a policy that appears to do nothing, so check here first when a policy is not taking effect.

The section is absent when no policy applies. Settings that a policy locks or limits are shown read-only elsewhere in this dialog, and in the **Tools > MCP Server...** dialog, with a tooltip saying so.

### Usage Data and Feedback

**Help improve Tabular Editor by collecting anonymous usage data** (enabled): Data does not contain any personally identifiable information, nor any information about the structure or content of your data models. Clear it to opt out of telemetry.

**Send error reports** (enabled): In cases of crashes, Tabular Editor displays an option for sending a crash report when this is checked.

## Tabular Editor > User Interface

Control toolbars and menus, how much of the model's source location is shown, window layout, language, accessibility, fonts and the recent items lists.

![The User Interface preferences page with the Fonts section](~/content/assets/images/pref-user-interface.png)

### Toolbars and menus

**Show toolbars in floating windows** (enabled): Show toolbars in documents and views that you undock into floating windows.

**Hide inactive toolbars** (enabled): Hide toolbars that don't apply to the active document or view.

**Hide inactive menus** (enabled): Hide the [dynamic menus](xref:user-interface#dynamic-menus-context-dependent) that don't apply to the active document or view.

**Hide version number** (disabled): Hide the version, for example **v28.0.0**, from the title bar, which then reads **Tabular Editor 3**.

**Model source detail** (Full path): Set how much of the loaded model's source location appears in the title bar, the status bar connection item, document tab tooltips and the hover text of the recent files and models menus:

- **Full path**: the model name with its full path, server or workspace location
- **Name only**: the file name, folder name or database name, without paths or server names
- **Hidden**: neither the model name nor its location. The title bar shows **Model loaded** and the status bar shows **Connected** when you're connected to a server.

Agents connected through the @mcp-server receive the model title at the same level. If you selected **Hide model source details** in an earlier version, this setting is **Hidden**.

### Search and replace

**Dialog opacity when inactive** (70%): Opacity of the **Find and replace** dialog when it doesn't have focus.

### Layout

**Remember whether window is maximized** (enabled): Restore the main window's maximized state when Tabular Editor 3 starts.

**Remember window position and size** (enabled): Restore the main window's position and size when Tabular Editor 3 starts.

### Language

**User interface language** (English): The language of the user interface. Restart Tabular Editor 3 to apply a change.

### Accessibility

**Color blindness mode** (disabled): Mark objects added since the last save in teal where they'd otherwise be green, in the **TOM Explorer** change indicators and the model comparison view. See @accessibility.

### Fonts

Font changes apply when you restart Tabular Editor 3. A **Restart Required** message appears when you click **OK**.

**User interface font** (Language default): The font of menus, tool windows, dialogs, grids, message boxes, code editor tooltips and the AI Assistant chat. The list shows only fonts installed on the machine. **Language default** uses Segoe UI, Microsoft YaHei UI for Chinese and Yu Gothic UI for Japanese.

**User interface font size** (9 pt): The text size of the same elements, from 8 pt to 14 pt.

**Code editor font size** (10 pt): The text size in the DAX, M, SQL and C# editors and in code boxes in dialogs, from 8 pt to 14 pt. Ctrl+mouse wheel zooms one editor for the current session, and **Edit > Reset Zoom** returns it to this size.

If a font or size is set in `TabularEditor3.dll.config`, the first entry of the font list reads **Default** with that font, and the setting keeps applying until you change it here.

### Recent Items

**Use compact file paths** (enabled): Shorten long file paths in the recent files and models menus. With **Model source detail** set to **Full path**, the location part of the title bar is shortened too.

**Number of recent files displayed** (10): The maximum number of files in the recent files menu, up to 50.

**Number of recent models displayed** (10): The maximum number of models in the recent models menu, up to 50.

**Number of recent servers displayed** (10): The maximum number of servers in the **Server** list when you connect to a semantic model, up to 50. Pinned servers aren't counted and always stay in the list. See @xmla-as-connectivity.

**Clear recent files**, **Clear recent models**, **Clear recent servers** and **Clear all recent items**: Clear the corresponding lists. **Clear recent servers** and **Clear all recent items** keep pinned servers and their saved settings.

## Tabular Editor > TOM Explorer

![Tom Explorer Settings](~/content/assets/images/unsaved-changes/preferences.png)

Control how the TOM (Tabular Object Model) Explorer presents the model, and what happens to the objects you delete.

The toggles that decide which object types appear in the tree, such as measures, columns, hierarchies, partitions, display folders and hidden objects, are not preferences. They live on the @tom-explorer-view toolbar, where you can change them per model without opening this dialog.

### Display and filtering

**Use table groups** (enabled): Group your tables in the TOM Explorer, for example to keep calculation groups, dimensions and fact tables apart. Tabular Editor records a table's group in an annotation on the table itself, so the grouping travels with the model. It is internal to Tabular Editor: no other client tool, Power BI Desktop included, shows it. See @table-groups.

**Show full branch** (disabled): When you filter the tree, Tabular Editor shows the objects that match your filter string together with their parents. Enable this to also show every child of a match, whether or not the children match the string themselves.

**Highlight relationships** (enabled): Highlight the relationships that involve the table or column you have selected, so you can see at a glance what a column is joined to.

### Unsaved changes

These settings control how [unsaved changes](xref:unsaved-changes) are indicated in the TOM Explorer and the Properties view.

**Mark objects with unsaved changes** (enabled): Highlight objects in the TOM Explorer that differ from the last saved version of the model, using a tinted row and a badge on the object's icon: orange for edited objects, green for added objects and red for deleted objects. Tables, folders and groups that contain changed objects get a hatched fill. When disabled, deleted objects still stay visible according to the setting below, and the **Show changes** toolbar filter still works. Use **Color blindness mode** under **User Interface > Accessibility** to mark added objects in teal instead of green.

**Keep deleted objects visible** (Until the model is saved): How long deleted objects remain visible in the TOM Explorer, struck through, where they used to be. Right-click a deleted object and choose **Restore** to bring it back. Options:

- **Never**: Deleted objects disappear from the TOM Explorer at once.
- **Until the model is saved**: Deleted objects are treated as unsaved changes and disappear when the model is saved.
- **Until the model is closed**: Deleted objects stay visible, and restorable, for the whole editing session, even across saves.

**Gather deleted objects under a "Deleted objects" node** (disabled): Show the deleted objects of a table, hierarchy, role or table group together under a single **Deleted objects** node at the end of their container, instead of each where it used to be. Right-click the node and choose **Restore** to bring back all of them at once.

**Mark properties with unsaved changes in the Properties pane** (enabled): Highlight properties in the Properties view that differ from the last saved version of the model, using a tinted row on the **Advanced** tab and a tinted field with a change icon on the **Basic** tab. When disabled, the **Show changes** toolbar filter in the Properties view still works.

### Delete

**Always show delete warnings** (disabled): Asks you to confirm every object deletion. When cleared, a confirmation appears only for multi-object deletions and for objects that other objects reference.

> [!NOTE]
> All delete operations in Tabular Editor 3 can be undone by hitting CTRL+Z.

### Localization

These settings decide the format string Tabular Editor writes when you pick the **Currency** number format for an object in the Properties pane.

**Default currency** (English (United States)): The formatting convention to base the currency format string on. Pick the locale whose currency symbol, decimal separator and digit grouping you want.

**Use a custom currency symbol** (disabled): Supply your own symbol instead of taking one from the locale above. The three settings below apply only while this is checked.

**Custom currency symbol**: The symbol to use. Enter the symbol on its own, without the number; whitespace is ignored.

**Custom currency symbol position** (Before number): Whether the symbol goes before or after the numeric value.

**Put a space between the number and symbol** (disabled): Separate the symbol from the numeric value with a space.

## Tabular Editor > DAX Debugger

![The DAX Debugger preferences page](~/content/assets/images/pref-dax-debugger.png)

Control what the [DAX debugger](xref:dax-debugger) lists and how it opens inspected values.

### Locals

**Include function args** (enabled): List the arguments of function calls in the **Locals** view.

**Include table expressions** (disabled): List subexpressions that return a table in the **Locals** view.

**Use popup inspector** (enabled): Clicking the magnifying glass next to a **Locals** value shows the result in a dialog. When disabled, the result opens in a new DAX query.

### Watch

**Use popup inspector** (disabled): Clicking the magnifying glass next to a **Watch** value shows the result in a dialog. When disabled, the result opens in a new DAX query.

### DAX queries

**Ask before editing a DAX query that is being debugged** (enabled): Typing in a DAX query that's being debugged shows the **Stop debugging?** prompt. When disabled, typing in the query stops debugging without the prompt. Selecting **Don't ask again** in the prompt clears this option.

## Tabular Editor > Public Previews

![The Public Previews preferences page](~/content/assets/images/pref-public-previews.png)

Public previews are features you can try before they're final. They can change before they're released, based on your feedback. Each is off until you turn it on here.

**Basic Properties view** (disabled): Show the **Basic** and **Advanced** tabs in the [Properties view](xref:properties-view). **Basic** shows the properties Power BI Desktop shows, as a form, and **Advanced** shows every property. When disabled, the Properties view shows the property grid alone.

**Properties view tab** (Basic): The tab the Properties view shows while **Basic Properties view** is enabled. Available only while **Basic Properties view** is enabled. Clicking a tab in the Properties view also changes this setting.

## Tabular Editor > Keyboard

![The Keyboard preferences page](~/content/assets/images/keyboard-mappings.png)

Configure keyboard shortcuts for all Tabular Editor commands. Use the search functionality to quickly find specific commands and assign or modify their keyboard shortcuts to match your preferred workflow.

<a name="miscellaneous"></a>

## Tabular Editor > Miscellaneous

![The Miscellaneous preferences page](~/content/assets/images/pref-miscellaneous.png)

### Metadata Synchronization

These settings control how Tabular Editor 3 handles model metadata that changes outside the application. The first three apply to a model loaded from a database on an instance of Analysis Services and use an Analysis Services trace. **Automatically reload from disk (hot reload)** applies to a model loaded from a file or a folder and watches those files.

**Warn when local metadata is out-of-sync with deployed model** (enabled): Show an information bar when you have local changes to the model that you haven't saved to Analysis Services. The bar disappears when you save (**Ctrl+S**).

**Track external model changes** (enabled): Start a trace on a local instance of Analysis Services, such as the msmdsrv.exe process of Power BI Desktop, and refresh the local Tabular Object Model and the data browsing views when another tool changes the model.

**Refresh local Tabular Object Model metadata automatically** (enabled): Available while **Track external model changes** is checked. Refresh the local model metadata when an external change is detected. If you have local changes that you haven't saved, a prompt asks before they're overwritten.

**Automatically reload from disk (hot reload)** (enabled): Watch the metadata files the model was loaded from, and reload the model when another application, such as an AI agent, a script or another editor, changes them. It covers a model loaded from a `.bim` file or from a folder, and works independently of **Track external model changes**. If the model has unsaved changes, a prompt asks which copy to keep. See [Auto-reload from disk](xref:auto-reload).

**Cleanup orphaned Tabular Editor traces**: Removes the Analysis Services traces that other instances of Tabular Editor left on the server, for example after Tabular Editor 3 closed unexpectedly. The button and a line stating the number of traces appear only when the connected instance of Analysis Services has such traces.

### Best Practice Analyzer

**Scan for Best Practice violations in the background** (enabled): Runs the Best Practice Analyzer on a background thread whenever the model changes. If you clear it, run the analysis from the **Best Practice Analyzer** window. On large models or with complex rules, background scanning slows down editing.

**Enable built-in best practice rules** (enabled on new installations): Turn the built-in Best Practice Analyzer rules on or off. The rules cover error prevention, performance, maintenance, naming conventions, formatting, model layout, governance and security. See @built-in-bpa-rules.

### Notifications

**Show a notification when data refresh is completed** (enabled): Show a notification when a data refresh operation completes.

### DAX scripts

**Use comments as separators** (enabled): Insert comments into generated DAX scripts to make them easier to read.

**Sort scripted items alphabetically** (disabled): Sort the objects in a DAX script generated from a multi-object selection alphabetically. When cleared, the script follows the selection order.

## AI Features

The parent page carries the two settings that apply to every AI feature, the chat and the [MCP server](xref:mcp-server) alike.

**Check for knowledge base updates on startup** (enabled): The AI Assistant searches a local copy of the Tabular Editor documentation. When checked, Tabular Editor looks for a newer copy at start-up and downloads it if one is available. This is the only outbound request any AI feature makes on its own.

**Audit log**: **Open audit folder** opens this computer's record of what the AI Assistant and the MCP server did: permission decisions, which tools were called and how each one ended, and the full text of any script that was run or handed over for review. Prompts, replies and data values are never recorded. The record is an Enterprise Edition feature: on Desktop and Business nothing is recorded and the button is not shown. See @ai-audit-log.

## AI Features > AI Assistant

Connection settings for the AI Assistant chat. The **AI Provider** child page renders here. See @ai-assistant for what each provider needs.

**Choose provider** (None): Which AI provider the chat talks to: **OpenAI**, **Anthropic**, **Azure OpenAI** or **Custom (OpenAI-compatible)**. The fields below change with your choice. An administrator can lock this to a single provider, or narrow the list, by policy.

**Base URL** / **Service endpoint**: Where requests are sent. OpenAI and Anthropic supply a default and the field is optional. Azure OpenAI and Custom have no default, so an endpoint is required.

**API Key**: Your own key for the chosen provider. It is stored encrypted on this machine in `Preferences.json`. Tabular Editor ships no built-in key and never proxies your requests.

**OpenAI Organization ID** and **OpenAI Project ID**: Optional, and shown for the OpenAI provider only. Use them where your OpenAI account bills or scopes usage per organization or project.

**Model name** (**Deployment** for Azure OpenAI): Which model to use. For OpenAI and Anthropic this is a dropdown filled from an online catalog, so it is empty until the catalog has been fetched once on this machine. For Azure OpenAI the field is labelled **Deployment** and takes the name you gave the deployment, which is not necessarily the name of the underlying model. Leaving it blank uses the provider's default, except for Azure OpenAI and Custom, which have none.

## AI Features > AI Assistant > Preferences

How the chat behaves. See @ai-assistant for the detail behind each group.

### Chat Display

**Show selection context indicator** (enabled): Show which model object is currently selected above the chat, so you can see what the assistant will treat as context.

**Show custom instructions indicator** (enabled): Show which [Custom Instructions](xref:ai-assistant#custom-instructions) were applied above each reply.

**Show knowledge base search indicator** (enabled): Show progress while the assistant searches the knowledge base.

### Context Compaction

**Auto compact** (enabled): Summarize the older part of a conversation automatically as it approaches the model's context limit, so a long conversation can carry on.

**Auto compact threshold %** (80): How full the context window gets before compaction runs, as a percentage of the selected model's context window. Values outside 50 to 100 have no further effect.

### C# Script

**Allow AI assistant to run C# scripts directly** (disabled): Let the assistant carry out the model change you asked for, instead of writing a script and opening it for you to run. Only scripts the safety analysis considers safe are run this way, meaning scripts that touch model objects and nothing else; anything reaching for files, the network or an external assembly is still handed to you for review. Each run lands as a single undo step.

This setting is unavailable until **Model metadata** is set to **Write** on the [Permissions](#ai-features--permissions) page, and it becomes available as soon as you change that dropdown, without closing the dialog. It is also unavailable, with a tooltip saying so, where an administrator has set the `DisableCSharpScripts` [policy](xref:policies). It is off by default deliberately: **Model metadata > Write** is also what an agent needs over the MCP server, and granting it there must not silently change what the chat does. See [Letting the assistant change your model](xref:ai-assistant#letting-the-assistant-change-your-model).

**Preview changes** (enabled): Show the script preview dialog before a change the assistant made stands, so you can see every model metadata change and accept or cancel it. Cancelling puts the model back and tells the assistant you rejected the change.

## AI Features > MCP Server

Settings for the [MCP server](xref:mcp-server), which lets an external agent such as Claude Code, GitHub Copilot or Cursor work on the model you have open.

![MCP Server preferences](~/content/assets/images/pref-mcp-server.png)

**Enable MCP Server** (enabled): Whether the MCP server is available at all. Clearing it stops a running server and removes both the **Tools > MCP Server...** menu item and the status bar indicator.

**Start MCP server automatically** (disabled): Start the server when Tabular Editor starts, so an agent can connect without you starting it by hand. If the port is in use at start-up, the server does not start and no prompt is shown.

**Require access token** (disabled): Make agents present a bearer token, shown in the **Tools > MCP Server...** dialog. The server listens on the loopback interface only, so this matters most on a machine where several people are signed in at once, such as a Remote Desktop or Citrix host, where every session can reach `127.0.0.1`. Administrators can enforce it with the `RequireMcpAccessToken` [policy](xref:policies).

**Port** (42100): The loopback port the server listens on, from 1024 to 49151. Changing it invalidates existing agent registrations, which point at a fixed address. If the port is taken when you start the server by hand, Tabular Editor offers the next free port it finds.

## AI Features > Permissions

One standing grant per resource, governing both the AI Assistant chat and any agent connected over the MCP server. The chat can additionally ask for something a grant does not cover; an agent cannot, so for MCP the grants apply as they stand and only change when the server restarts.

![AI Features Permissions preferences](~/content/assets/images/pref-ai-permissions.png)

| Resource | Levels | Default | What it covers |
| -- | -- | -- | -- |
| **Model metadata** | Deny / Read / Write | Read | Tables, columns, measures, expressions, descriptions and relationships, plus VertiPaq Analyzer statistics. Write allows changes through C# scripts |
| **Model data** | Deny / Read | Deny | Data values from your model, such as DAX query results. There is no write level |
| **Best Practice Analyzer** | Deny / Read / Write | Read | Read lists rules and runs the analysis; Write adds or modifies rules |
| **Documents** | Deny / Read / Write | Write | Your open C# script and DAX query tabs. Read is their contents; Write creates or modifies them |
| **Macros** | Deny / Read / Write | Write | Your macro library |

**Write** covers Read, so there is no need to grant both. **Model data** is the one resource denied by default.

In the Enterprise, Consultancy and Trial editions an administrator can cap any of these by [policy](xref:policies), separately for the chat and for the MCP server. A capped dropdown is shown read-only. See @ai-assistant for how the chat asks for what a grant does not cover, and @mcp-server for what an agent sees.

## Data Browsing > Pivot Grid

<!-- SCREENSHOT RESHOOT (3.27.1): pref-pivot-grid.png. Show the Keep Pivot Grids open when a different model is opened section and the Field Headers and Field List labels. -->
![Pivot Grid preferences](~/content/assets/images/pref-pivot-grid.png)

### Basic

**Automatically refresh Pivot Grids by default** (enabled): Automatically refresh pivot grids when model changes are saved. Just like with DAX queries, this allows you to immediately see the impact of changes to measures.

**Show warning if Pivot Grid doesn't match model** (enabled): Show a warning when a Pivot Grid layout uses fields that the current model doesn't have, for example after you delete or rename a field, open a layout saved from a different model or keep a Pivot Grid open while you open a different model. The setting also controls the confirmation that appears before a different model opens while Pivot Grids with fields in their layout are kept open.

### Field Headers

**Word wrap field headers** (enabled): Field headers wrap to multiple lines when the header text doesn't fit on one line.

### Field List

**Always show field list** (enabled): Shows the field list when a new Pivot Grid is created.

**Keep fields visible** (enabled): Keeps a field in the Fields section of the field list after you add it to the Pivot Grid.

**Layout** (Fields Section and Areas Section Stacked): The default layout of the field list:

- **Fields Section and Areas Section Stacked**
- **Fields Section and Areas Section Side-By-Side**
- **Fields Section Only**
- **Areas Section Only (2 by 2)**
- **Areas Section Only (1 by 4)**

### Keep documents open when switching models

**Keep Pivot Grids open when a different model is opened** (enabled): Keep Pivot Grid documents open when you open a different model, and connect them to the new model. The field layout is kept, and fields that the new model doesn't have are dropped from it. When disabled, Pivot Grids close along with the previous model. See @pivot-grid.

## Data Browsing > DAX Query

<!-- SCREENSHOT RESHOOT (3.27.1): pref-dax-query.png. Show the Keep DAX Queries open when a different model is opened section. -->
![DAX Query preferences](~/content/assets/images/pref-dax-query.png)

### Basic

**Automatically execute DAX queries by default** (enabled): New DAX queries open with **Auto-execute** enabled, so the query re-runs whenever changes are made to the deployed semantic model. Turn it off if you would rather execute each query yourself.

**Keep existing sorting and filtering in the result grid** (When query is unchanged): Control whether to preserve grid filters and sorting when re-executing queries:

- **Never**: sorting and filtering are reset every time you execute the query
- **When query is unchanged**: sorting and filtering are reset only when you modify the query, ignoring changes to whitespace and comments
- **Always**: sorting and filtering are never reset for columns that are still in the result

### Query settings

**Smart selection** (enabled): When you execute part of a query, Tabular Editor turns that selection into a valid DAX query on your behalf, wrapping a scalar expression in curly braces and adding the `DEFINE` section or the `EVALUATE` keyword when they are not part of the selection. In a document with several `DEFINE ... EVALUATE` queries, the added `DEFINE` section is the one that belongs to the selected query. A selected column reference, including one in an `ORDER BY` clause, returns the column's distinct values.

**Row limit** (1,000): Wraps every `EVALUATE` statement in a `TOPN` call, to keep an accidental query over a large table from running for a long time or exhausting memory. Set it to `0` to remove the limit entirely.

### Code Generation

**Use comments as separators** (enabled): Insert comments into generated object definitions, for example the `DEFINE` block produced by **Define object in query**, to make them easier to read.

### Keep documents open when switching models

**Keep DAX Queries open when a different model is opened** (enabled): Keep DAX Query documents open when you open a different model. The query text is kept, previous results are cleared and the query runs against the newly opened model. When disabled, DAX Query documents close along with the previous model. See @dax-query.

## Data Browsing > Table Preview

![Table Preview preferences](~/content/assets/images/pref-table-preview.png)

### Basic

**Automatically refresh table previews by default** (enabled): New table previews open with **Auto-refresh** enabled, so the preview refreshes whenever changes are made to the deployed semantic model. This is useful when debugging: update an expression in one window while a preview of the same table is open in another.

**Sort table preview columns alphabetically** (disabled): When checked, table preview columns are sorted alphabetically by name, matching the order the @tom-explorer-view lists a table's columns in. When unchecked (the default), columns appear in the order the engine returns them, which is roughly internal column order and can look arbitrary.

**Max. values in filter dropdown** (5,000): Maximum number of distinct values listed in a column's filter dropdown. On a column with more distinct values than this, the values beyond the limit are not listed and cannot be ticked directly. Raising it lists more values at the cost of a heavier query each time the dropdown is opened. Accepts 100 to 1,000,000.

**Max. rows to sort without an attribute hierarchy** (100,000): Upper bound on the number of rows Tabular Editor sorts by a column that has no attribute hierarchy to sort on.

### DirectQuery

**Row limit** (100): Maximum number of rows to retrieve for a table preview in DirectQuery mode. Raise it if you need to see more data, bearing in mind that every row is fetched from the underlying source.

### Behavior

**Track selected column in TOM Explorer** (enabled): When you select a column in the @tom-explorer-view, the open table preview scrolls that column into view and highlights it, which is the quickest way to find one column of a very wide table. The same setting can be turned on and off for a single preview with **Track selected column** on the Table Preview toolbar.

## Text Editors > General

![The Text Editors General preferences page](~/content/assets/images/pref-text-editors-general.png)

Settings shared by the code editors.

**Allow multi-paste** (enabled): Paste the clipboard text into every selection, for example into a block selection made with **Alt**+select.

**Show indicators on scrollbar** (enabled): Mark the messages about the code on the vertical scrollbar. Hover over a marker to read the message, or click it to go to the code. With this checked, the vertical scrollbar is always visible.

**Word Wrap** (disabled): Wrap long lines in the code editors.

**Show visual word wrap indicator at the:** Available while **Word Wrap** is checked. Check **End of line**, **Start of line** or **Line margin** to mark wrapped lines at that position. All three are cleared by default.

## Text Editors > DAX Editor > General

![Dax Editor General](~/content/assets/images/dax-editor-general.png)

Settings for the DAX editor's display, the DAX syntax it accepts, DAX formatting and function documentation. See @dax-editor.

### General

**Line numbers** (enabled): Display line numbers in the left margin of the editor.

**Code folding** (enabled): Show collapsible regions in DAX code.

**Visible whitespace** (disabled): Show dots for spaces and arrows for tabs, for example when you diagnose indentation issues.

**Indentation guides** (enabled): Display vertical lines that show indentation levels.

**Use tabs** (disabled): When checked, pressing **Tab** inserts a tab character (`\t`). Otherwise, the editor inserts the number of spaces set in **Tab/indent width**.

**Tab/indent width** (4): The width of a tab or indent in character columns, from 1 to 20.

**Comment style:** (Slashes): The comment token Tabular Editor uses when you comment code through a UI action: **Slashes** (`//`) or **Hyphens** (`--`).

### DAX Settings

**Locale** (US (A, B, C, 1234.00)): The list separator and decimal separator of DAX code: **US (A, B, C, 1234.00)** or **Non-US (A; B; C; 1234,00)**.

The remaining settings decide which DAX syntax the editor accepts. Tabular Editor 3 determines this from the instance of Analysis Services the model is connected to. When it can't, for example when you load a Model.bim file, it guesses from the compatibility level. If the editor reports incorrect syntax or semantic errors, set these to match the engine you deploy to. Each defaults to **Auto-detect**.

**Semantic engine** (Auto-detect): The engine version to emulate: **SSAS 2016**, **SSAS 2017**, **SSAS 2019**, **SSAS 2022** or **AAS / PBI (Latest)**. Newer versions support more DAX functions.

**Scalar predicates** (Auto-detect): Whether a single scalar predicate in a `CALCULATE` filter argument can reference multiple columns.

**Directional CF** (Auto-detect): Whether [CROSSFILTER](https://dax.guide/crossfilter) accepts the directional syntax for many-to-many relationships.

**Date Literals** (Auto-detect): Whether the date literal syntax is accepted.

**Measure/Agg Shortcut** (Auto-detect): Whether scalar predicates can contain measure references and aggregation functions.

**Table-named variables** (Auto-detect): Whether a variable can have the same name as a table in the model.

Each of the last five settings offers **Auto-detect**, an **Always allow** option and a **Never allow** option.

### DAX Formatter by SQLBI

**Use daxformatter.com instead of built-in formatter** (disabled): Format DAX code with the [daxformatter.com](https://www.daxformatter.com) web service, which receives the code you format. The built-in formatter sends nothing over the network. Unavailable where an administrator has set the `DisableWebDaxFormatter` [policy](xref:policies).

**Request Timeout (ms)** (5000): Available while **Use daxformatter.com instead of built-in formatter** is checked. How long to wait for daxformatter.com to respond, from 100 to 20,000 milliseconds.

**Default DAX formatting** (Long lines): The formatting that **F6** applies: **Short lines** or **Long lines**. **Shift+F6** applies the other one. If you've customized the format shortcuts under [Keyboard](#tabular-editor--keyboard), this setting doesn't change them.

### DAX function documentation

**Documentation URL** (`https://dax.guide/{0}`): The page that opens in your web browser when you press **F12** with the cursor on a DAX function. Choose [DAX Guide](https://dax.guide) or the Microsoft documentation (`https://docs.microsoft.com/en-us/dax/{0}-function-dax`), or type a custom URL.

## Text Editors > DAX Editor > Auto Formatting

![The DAX Editor Auto Formatting preferences page](~/content/assets/images/auto-formatting-settings.png)

The DAX editor formats your code as you type. **Use default formatting settings** at the bottom of the page restores every setting on it.

**Auto format code as you type** (enabled): Apply the formatting rules when certain keys are pressed. For example, when a parenthesis is closed, everything within the parentheses is formatted according to the other settings on this page. The next three settings are available while this is checked.

**Auto-format function calls** (enabled): Add spacing between function arguments when you type the closing parenthesis.

**Auto-indent** (enabled): Indent the next line when you open a function call or after certain keywords.

**Auto-brace** (enabled): Insert or skip the matching character when you type an opening or closing brace or quote.

**Wrap selection** (enabled): When you type a brace with code selected, wrap the selection in the braces. When cleared, the brace replaces the selection.

### Formatting rules

These settings control how DAX code whitespace is formatted, both when auto-formatting occurs and when you format code manually.

**Space after functions** (disabled)

# [Enabled](#tab/space-after-function-on)

```DAX
SUM ( 'Sales'[Amount] )
```

# [Disabled](#tab/space-after-function-off)

```DAX
SUM( 'Sales'[Amount] )
```

***

**Newline after functions** (disabled): Applies only when a function call needs to be broken across multiple lines.

# [Enabled](#tab/newline-after-function-on)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [Disabled](#tab/newline-after-function-off)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

**Newline before operator** (enabled): When a binary expression is broken across lines, put the operator at the start of the next line. When cleared, the operator stays at the end of the first line.

**Pad parentheses** (enabled)

# [Enabled](#tab/pad-parentheses-on)

```DAX
SUM( Sales[Amount] )
```

# [Disabled](#tab/pad-parentheses-off)

```DAX
SUM(Sales[Amount])
```

***

**Long format line limit** (120): The maximum number of characters on a line before an expression is broken across multiple lines, when you format DAX with long lines. Accepts 10 to 200.

**Short format line limit** (60): The maximum number of characters on a line before an expression is broken across multiple lines, when you format DAX with short lines. Accepts 10 to 200.

### Casings and quotes

In addition to formatting the DAX code whitespace, Tabular Editor 3 can also fix object references and function/keyword casings.

**Fix measure/column qualifiers** (enabled): When checked, table prefixes are automatically removed from measure references, and automatically inserted on column references.

**Preferred keyword casing** (Default): The casing of keywords, such as `ORDER BY`, `VAR` and `EVALUATE`: **Default**, **All UPPERCASE**, **All lowercase** or **Capitalize first letter only**. **Default** writes keywords in uppercase, except the `CROSSFILTER` directions `Both`, `Oneway`, `Oneway_LeftFiltersRight` and `Oneway_RightFiltersLeft`. It also governs the fixed keyword values auto-complete offers for functions that take them: `ASC` and `DESC`, `KEEP`, `FIRST`, `LAST` and `DEFAULT`, the `CROSSFILTER` directions and `LOOKUP`'s `EXPLICIT` and `INFERRED`. Choose **Capitalize first letter only** to be offered `Explicit`.

**Preferred function casing** (Default): The casing of functions, such as `CALCULATE(...)` and `SUM(...)`, with the same options. **Default** writes functions in uppercase.

**Fix keyword/function casing** (enabled): When checked, casing of keywords and functions is automatically corrected whenever code is auto-formatted or manually formatted.

**Fix object reference casing** (enabled): DAX is a case-insensitive language. When this is enabled, references to variables, tables, columns and measures are automatically corrected such that the casing matches the definition of the referenced object.

**Always quote tables** (disabled): Quote every table reference. When cleared, the editor quotes a table name only when it has to, for example when the name contains special characters or matches a DAX function name.

**Always prefix extension columns** (disabled): Extension columns can be defined without a table name. When checked, the DAX editor adds the table prefix to an extension column, even an empty one: `''[ExtensionColumn]`.

## Text Editors > DAX Editor > Code Assist

![DAX Editor Code Assist preferences](~/content/assets/images/pref-dax-code-assist.png)

Configure parameter info (calltips), auto-complete and the warnings in the DAX editor.

### Parameter info

**Show parameter info automatically** (enabled): Show the parameters of the function you're typing. The dropdown below it sets when parameter info appears: **Only when typing** (the default), **When typing or moving cursor** or **Always**.

### Code auto-complete

**Show auto-complete popup automatically** (enabled): Open the auto-complete list as you type. When cleared, open it with **Ctrl+Space**.

**Auto-complete mode** (After entering a whitespace character or a letter): Available while **Show auto-complete popup automatically** is checked. When the list opens: **After entering a letter only**, **After entering a whitespace character or a letter** or **After entering any character**.

**Handle character deletion** (enabled): Keep the auto-complete list open and filter it again when you delete characters. When cleared, deleting a character closes the list.

**Show deprecated/not recommended DAX functions** (disabled): List deprecated and not recommended DAX functions in auto-complete.

**Usage based pre-selection** (enabled): Preselect the items you've chosen before in the current session.

**KPI expression references** (Suggest non-empty KPI expressions only): Whether auto-complete suggests references to KPI expressions. For a measure `[Sales Amount]` with a KPI, these are `[_Sales Amount Status]`, `[_Sales Amount Goal]` and `[_Sales Amount Trend]`. Options:

- **Never suggest KPI expressions**
- **Suggest non-empty KPI expressions only**
- **Suggest expressions for all model KPIs**
- **Suggest expressions for all model measures**

**Allow incremental search** (enabled): Filter the list by letters that appear in order in an item's name. For example, typing `icqs` matches `[Internet Current Quarter Sales]`.

**Only first letter of every word** (disabled): Available while **Allow incremental search** is checked. Match the letters you type against the first letter of each word in an item's name only.

### Errors and Warnings

**Show warnings for unused variables** (enabled): Show a warning when a DAX expression declares a variable that it never references.

## Text Editors > DAX Editor > Code Actions

![DAX Editor Code Actions preferences](~/content/assets/images/pref-dax-code-actions.png)

Configure [code actions](xref:code-actions), the code improvement and refactoring suggestions in the left margin of the DAX editor.

**Show code actions** (enabled): Show code action suggestions in the DAX editor.

**Variable prefix** (`_`): The prefix that code actions apply to variable names: `_`, `__`, `$`, `var_`, `var`, `v_`, `v` or `VAR_`.

**Apply variable casing** (disabled): Fix the casing of variable names when you apply a code action for variables.

**Preferred variable casing** (Default): Available while **Apply variable casing** is checked. The casing of variable names after the prefix: **Default**, **All UPPERCASE**, **All lowercase** or **Capitalize first letter only**.

**Extension column prefix** (`@`): The prefix that code actions apply to extension columns: `@`, `$`, `_`, `x` or `x_`.

## Text Editors > SQL Editor / M Editor / C# Editor

![The code editor preferences page, shared by the SQL, M and C# editors](~/content/assets/images/pref-code-editors.png)

The **SQL Editor**, **M Editor** and **C# Editor** nodes each have a **General** page with the same settings. Each editor keeps its own values.

**Line numbers** (enabled): Display line numbers in the left margin of the editor.

**Code folding** (enabled): Show collapsible regions in the code.

**Visible whitespace** (disabled): Show dots for spaces and arrows for tabs.

**Indentation guides** (enabled): Display vertical lines that show indentation levels.

**Use tabs** (disabled): When checked, pressing **Tab** inserts a tab character. Otherwise, the editor inserts spaces.

## Schema Compare

![Schema Compare preferences](~/content/assets/images/pref-schema-compare.png)

Configure how Tabular Editor detects and reports source schema changes when you update table schemas.

### Schema Change detection

**Use Analysis Services for change detection** (disabled): Detect schema changes by running a refresh operation on the Analysis Services database. Use it for data sources that Tabular Editor can't read schemas from directly.

### Schema Compare settings

**Ignore new column imports** (disabled): Don't import new columns from the source.

**Ignore column description changes** (disabled): Ignore differences between the description of an imported column and the column description in the source. Some data sources supply column descriptions.

**Ignore column data type changes** (disabled): Don't report source columns that map to a different data type than the imported column has.

**Ignore decimal to floating point data type changes** (disabled): Available while **Ignore column data type changes** is cleared. Don't report columns imported as Decimal that have a floating point type in the source.

## File Formats > General

![The File Formats General preferences page with the serialization settings sections](~/content/assets/images/pref-file-formats-general.png)

The serialization settings on this page and on the **Save-to-folder** pages apply when you save with **File > Save As** or **File > Save to Folder** and the model has no stored serialization settings, or when you uncheck **Use serialization settings from annotations** in the save dialog. **File > Save** uses the settings stored with the model, which you edit under **Model > Serialization options...**.

### Power BI Desktop

**Use PBIX filename as database name when serializing** (enabled): When you save a model loaded from Power BI Desktop as a Model.bim file or a folder, replace the database name, a GUID generated by Power BI Desktop, with the name of the .pbix file.

### New models

**Use latest default** (enabled): Create new models at the latest compatibility level. While checked, **Compatibility level** is unavailable.

**Compatibility level** (1600): The compatibility level of new models when **Use latest default** is cleared. The choices are the same as in the **New Model** dialog:

| Level | Target |
|---|---|
| 1200 | Azure Analysis Services / SQL Server 2016+ |
| 1400 | Azure Analysis Services / SQL Server 2017+ |
| 1500 | Azure Analysis Services / SQL Server 2019+ |
| 1600 | Azure Analysis Services / SQL Server 2022+ |
| 1700 | Azure Analysis Services / SQL Server 2025+ |
| 1706 | Power BI / Fabric |

1700 is the highest level Analysis Services supports; 1706 is the highest overall and is Power BI and Fabric only.

**Use workspace database** (enabled): Create a workspace database for new models, so you can query and test the model while you develop it.

**Default save format** (Always ask): The format of the first save of a new model: **Always ask**, **File (Model.bim)**, **Folder (Database.json)** or **TMDL**.

**Create user options (.tmuo) file** (enabled): Create the user options (.tmuo) file when you save a new model for the first time. The file holds encrypted data source credentials and other user-specific settings for the model.

### General serialization settings

Every format uses these settings: Model.bim files, Database.json folders and TMDL folders.

**Include sensitive** (disabled): Include sensitive properties, such as the `Password` property of a data source. If you check it, the saved files contain those values in plain text.

**Ignore incremental refresh partitions** (enabled): Don't save the partitions that an incremental refresh policy creates. In Model.bim files and TMDL folders, a table left without partitions gets a single partition with the policy's source expression, so the model opens in Power BI Desktop.

### JSON serialization settings

Model.bim files and Database.json folders use these settings. TMDL folders don't.

**Ignore inferred objects** (enabled): Don't serialize objects that the engine infers.

**Ignore inferred properties** (enabled): Don't serialize properties that the engine infers.

**Ignore timestamps** (enabled): Don't serialize timestamp metadata. A save without model changes then leaves the files unchanged.

**Ignore lineage tags** (disabled): Don't serialize Power BI lineage tags.

**Ignore privacy settings** (disabled): Don't serialize the `PrivacySetting` property of data sources. Check it if you deploy with a version of Microsoft.AnalysisServices.Deployment that doesn't support the property.

**Split multiline strings** (enabled): Write multiline strings, such as DAX expressions, as an array of lines.

**Sort arrays by name** (disabled): Sort some JSON arrays, such as roles and perspectives, by name.

## File Formats > Save-to-folder

![The Save-to-folder preferences page with the Save to Folder format setting](~/content/assets/images/pref-save-to-folder.png)

**Save to Folder format** (TMDL): The format **File > Save to Folder** writes: **TMDL** or **Folder (Database.json)**. A model loaded from a folder keeps its folder's format when you save it with **File > Save**.

Below the format, the page links to **Model > Serialization options...**, which edits the serialization settings stored with the loaded model. Clicking the link applies your changes, closes the Preferences dialog and opens **Model > Serialization options...**. With no model loaded, the menu path is plain text.

## File Formats > Save-to-folder > JSON Serialization

Settings for saves to a Database.json folder. **Reset to default** restores every setting on the page.

### Database.json settings

**Serialize relationships on from-tables** (enabled): Store each relationship as an annotation on the table at its from-side.

**Serialize perspective membership info on objects** (enabled): Store perspective membership as an annotation on each object.

**Serialize translations on translated objects** (enabled): Store metadata translations as an annotation on each translated object.

**Prefix file names sequentially** (disabled): Prefix each file name with the object's position in its collection. The folder then keeps the metadata order.

**Serialization depth** (all levels): The object types that get a file of their own: Data Sources, User Defined Functions (UDFs), Shared Expressions, Perspectives, Relationships, Roles, Tables, Columns, Hierarchies, Measures, Partitions, Calculation Items and Translations. Relationships, Perspectives and Translations are hidden when the matching **Serialize ...** setting above is checked.

## File Formats > Save-to-folder > TMDL Serialization

Settings for saves to a [TMDL](xref:tmdl) folder. **Reset to default** restores every setting on the page.

![The TMDL Serialization preferences page with Save objects to separate files checked](~/content/assets/images/pref-tmdl-serialization.png)

### TMDL settings

**Include metadata order** (enabled): Write the order of objects to `model.tmdl`.

**Indentation** (Tabs): Indent with tabs or spaces.

**Indentation width** (4): The number of spaces per indentation level when **Indentation** is Spaces.

**Encoding** (UTF8): The file encoding of the `.tmdl` files.

**Newline style** (Windows): The line ending: Default, Windows or Linux. Default uses the line ending of the operating system that saves the model.

**Casing style** (camelCase): The casing of TMDL keywords, such as property names and object types.

**Expression trim style** (No trim): How whitespace in expression lines is trimmed: No trim, Trim trailing whitespaces or Trim leading/common whitespaces.

**Save objects to separate files** (disabled): Save each object of a type checked in the tree below it to its own file. Every type is checked by default, and **Tables**, **Perspectives**, **Roles** and **Translations** can't be unchecked. Enterprise Edition only. See @tmdl-per-object-serialization.

## File Formats > VertiPaq Analyzer

![The VertiPaq Analyzer preferences page](~/content/assets/images/pref-vertipaq-analyzer.png)

### VPAX file format

**Include TOM** (enabled): Include the complete Tabular Object Model (TOM) in VertiPaq Analyzer (VPAX) exports.

### VertiPaq Analyzer settings

**Read statistics from data** (enabled): Scan the model data for statistics. It's more accurate than relying on Dynamic Management Views, and slower on large models. If reading statistics from data fails, for example when a high-cardinality column exceeds a Power BI capacity's per-query memory limit, **Collect Stats** collects the statistics from metadata and a **Stats collected without reading data** warning appears. The settings below are available while this is checked.

**Read statistics from DirectQuery tables** (disabled): Include DirectQuery tables when collecting statistics.

**RI violation samples** (3): The number of referential integrity violation samples to retrieve, from 1 to 100.

**Statistics from Direct Lake models** (Resident columns only): Which columns of a Direct Lake model to collect statistics for: **Resident columns only**, **Referenced columns only** or **Full**.

**Column batch size** (50): The batch size used when collecting column statistics, from 1 to 9,999.

## Model Deployment > General

![Model Deployment preferences](~/content/assets/images/pref-model-deployment.png)

### Deployment Options

**Add metadata annotation upon deployment** (disabled): Adds deployment details to the deployed model: the user, the client machine, the time, the Tabular Editor build and the deployment mode.

**Save Model.bim backup on deployment** (enabled): Saves a compressed copy of the model's `Model.bim` to the **Backup location** folder on every deployment. No backup is saved while **Backup location** is empty.

**Backup location**: The folder for deployment backups. Available when **Save Model.bim backup on deployment** is selected.

### Model Saving Options

**Save Model.bim backup on model save** (enabled): Saves a compressed copy of the model's `Model.bim` to the **Backup location** folder every time you save the model. No backup is saved while **Backup location** is empty.

**Backup location**: The folder for save backups. Available when **Save Model.bim backup on model save** is selected.

## Model Deployment > Data Refresh

### Direct Lake

This section appears in Enterprise Edition only.

**Auto-refresh when saving new tables** (enabled): Refreshes a Direct Lake model when you save it with new tables. If you clear it, new tables stay unprocessed until you refresh the model, and queries against them fall back to DirectQuery mode.

## DAX Optimizer > General

![The DAX Optimizer General preferences page](~/content/assets/images/pref-dax-optimizer.png)

Settings for the [DAX Optimizer integration](xref:dax-optimizer-integration).

### DAX Optimizer settings

**Connect automatically on start-up** (disabled): Connect to the DAX Optimizer service when Tabular Editor 3 starts.

### Obfuscation

**Use VPAX obfuscation by default** (enabled): Check the option to obfuscate a VPAX file by default when you upload it to DAX Optimizer.

**VPAX obfuscation dictionary location** (`%LocalAppData%\TabularEditor3\DaxOptimizer`): The folder that stores obfuscation dictionaries.

## Next Steps

For a user-friendly guide to the most commonly adjusted preferences, see the getting started guide [Personalizing TE3](xref:personalizing-te3).
