---
uid: preferences
title: 管理偏好设置
author: Daniel Otykier
updated: 2026-09-16
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

# Tabular Editor 3 偏好设置

Tabular data model development processes and workflows differ greatly from organization to organization. To ensure that the tool can fit into as many of these workflows as possible, Tabular Editor 3 is highly customizable - not just in terms of the user interface's look and feel, but also on more advanced topics such as web proxies, updates and feedback, row limits, timeouts, schema compare preferences, etc.

本文介绍 Tabular Editor 3 的“偏好设置”对话框，以及你可以通过该对话框控制的设置。

要打开“偏好设置”对话框，请依次选择 **工具 > 偏好**。

> [!NOTE]
> 所有 Tabular Editor 偏好设置都会针对每个 Windows 用户配置文件分别存储在 `%localappdata%\\TabularEditor3` 文件夹中。 It is possible to migrate your settings to another machine by simply copying the contents of this folder.

> [!TIP]
> 在“偏好”对话框顶部使用搜索框，可快速找到特定设置。

## Tabular Editor > 功能

![偏好设置：常规功能](~/content/assets/images/pref-general-features.png)

### Power BI

##### _允许不受支持的编辑_（已禁用）

仅当将 Tabular Editor 3 作为 Power BI Desktop 的外部工具使用时，此选项才适用。 When checked, all TOM data modeling properties are available for editing when connected to an instance of Power BI Desktop. It's generally recommended to leave this unchecked, to make sure that you do not accidentally make changes to your Power BI file, [that are not supported by Power BI Desktop](xref:desktop-limitations).

##### _隐藏自动日期/时间警告_（已禁用）

When checked, warnings about Power BI auto date/time tables will be suppressed. 当 Power BI Desktop 中启用“自动日期/时间”设置时，会创建计算表格，从而触发 Tabular Editor 3 内置 DAX 分析器的警告。

##### _在 DAX 首行换行_（已禁用）

在 Power BI Desktop 中，由于公式栏显示 DAX 代码的方式，通常会在 DAX 表达式的第一行插入换行。 If you often switch back and forth between Tabular Editor and Power BI Desktop, consider enabling this option to have Tabular Editor 3 insert the line break automatically.

##### _仅适用于多行 DAX 表达式_（已启用）

启用“DAX 首行换行”后，此子设置用于控制是否仅对多行 DAX 表达式添加换行。 When checked, single-line expressions are left unchanged.

##### _默认 Power BI 身份验证模式_（集成）

选择连接到 Power BI Dataset 时要使用的默认身份验证方法（集成、ServicePrincipal 或 MasterUser）。

### 最佳实践分析器

##### _在后台扫描最佳实践违规项_（已启用）

如果未勾选，你需要在 Best Practice Analyzer 工具窗口中手动运行一次“最佳实践分析”，才能查看是否存在违规项。 If checked, the scan happens continuously on a background thread whenever changes are made. For very large models, or models with very complex Best Practice rules, this may cause issues.

##### _内置 BPA 规则_（新用户默认启用）

Choose whether to enable, disable, or be prompted about using Tabular Editor's built-in Best Practice Analyzer rules. The built-in rules cover key best practices across formatting, metadata, model layout, DAX expressions, and translations. New installations will have built-in rules enabled by default.

### 通知

##### _数据刷新通知_（已启用）

勾选后，数据刷新操作完成时会显示通知。

### DAX 公式自动修正

##### _启用公式修复_（已启用）

当对象被重命名或移动时，自动调整 DAX 表达式中的引用。 This feature ensures that your DAX code remains valid when you reorganize your model.

##### _粘贴时启用公式修复_（已启用）

在粘贴对象时，自动调整 DAX 表达式中的引用。 This is useful when copying measures or calculated columns between tables or models.

### Direct Lake

##### _Auto-refresh on save_ (enabled)

保存更改时自动刷新 Direct Lake 表，确保数据为最新。 This ensures that your Direct Lake model stays in sync with the underlying data source.

## Tabular Editor > 更新与反馈

![Updates and Feedback preferences](~/content/assets/images/pref-updates-and-feedback.png)

### Updates

##### _Show "Get Started" page on updates_ (enabled)

When checked, the **Get Started** page opens automatically the first time you run Tabular Editor after it has been updated. It appears **on updates**, not on every start-up. You can open it at any time from **Help > Get Started**.

##### _启动时检查更新_（已启用）

勾选后，Tabular Editor 会在应用启动时检查是否有新版本。 This ensures you stay up to date with the latest features and bug fixes.

##### _Major updates only_ (disabled)

When checked, only major version updates trigger notifications. Minor and patch updates are ignored. This setting is only available while _Check for updates on start-up_ is checked.

The version you are running is shown below these settings, along with a **Check for updates** button that runs the check immediately.

### Managed by your organization

Where an administrator has configured [policies](xref:policies), a read-only **Managed by your organization** section is appended to this page listing every policy value Tabular Editor found, as `Name = value`. Hover over an entry to see which registry key and hive it came from.

A value Tabular Editor could not interpret is listed with an `(invalid)` marker rather than being left out. That marker is the fastest way to find the typo behind a policy that appears to do nothing, so check here first when a policy is not taking effect.

The section is absent when no policy applies. Settings that a policy locks or limits are shown read-only elsewhere in this dialog, and in the **Tools > MCP Server...** dialog, with a tooltip saying so.

### Usage Data and Feedback

##### _通过收集匿名使用数据帮助改进 Tabular Editor_（已启用）

Data does not contain any personally identifiable information, nor any information about the structure or content of your data models. If you would still like to opt out of telemetry, uncheck this.

##### _发送错误 Report_（已启用）

勾选后，如果发生崩溃，Tabular Editor 会显示发送崩溃 Report 的选项。 Crash reports are very helpful when debugging, so please leave this checked if you don't mind!

## Tabular Editor > 部署

![Model Deployment preferences](~/content/assets/images/pref-model-deployment.png)

使用 Deployment Wizard 时，配置默认要部署的对象类型：

##### _部署数据源_（已禁用）

Include data source definitions when deploying. 如果你希望在部署模型更改的同时部署数据源连接字符串和设置，请启用此选项。

##### _部署分区_（已禁用）

Include partition definitions when deploying. 如果你希望在部署模型更改的同时部署分区配置，请启用此选项。

##### _部署刷新策略分区_（已禁用）

Include incremental refresh policy partitions when deploying. 此选项用于控制是否部署由增量刷新策略创建的分区。

##### _部署模型角色_（已禁用）

Include role definitions when deploying. 若要部署行级安全性（RLS）和对象级安全性（OLS）角色，请启用此选项。

##### _部署模型角色成员_（已禁用）

Include role member assignments when deploying. 若要部署安全角色的用户和组分配，请启用此选项。

##### _部署共享表达式_（已禁用）

Include shared expressions (M expressions) when deploying. 如需部署 Power Query 共享表达式，请启用此选项。

### 部署元数据

##### _标注部署元数据_（已禁用）

Add deployment timestamp and user information as annotations on deployed objects. 这有助于跟踪模型更改是在什么时候、由谁部署的。

### 备份设置

##### _保存时备份_（已启用）

在本地保存更改时创建模型备份。 This provides a safety net in case you need to revert changes.

##### _备份保存位置_

Specify the folder where save backups are stored. 默认情况下，除非指定位置，否则不会创建备份。

##### _部署时备份_（已启用）

在部署更改之前，为目标模型创建备份。 This allows you to restore the previous version if needed.

##### _备份位置_

Specify the folder where deployment backups are stored. 默认情况下，除非指定位置，否则不会创建备份。

## Tabular Editor > 默认设置

<!-- IMAGE NEEDED: pref-defaults.png
     The Tabular Editor > Defaults preferences page at its default settings.
     Alt text: "The Defaults preferences page" -->

##### _新模型兼容级别_（1600）

Set the default compatibility level for newly created models. The choices are the same as in the **New Model** dialog:

| 级别   | Target                                     |
| ---- | ------------------------------------------ |
| 1200 | Azure Analysis Services / SQL Server 2016+ |
| 1400 | Azure Analysis Services / SQL Server 2017+ |
| 1500 | Azure Analysis Services / SQL Server 2019+ |
| 1600 | Azure Analysis Services / SQL Server 2022+ |
| 1700 | Azure Analysis Services / SQL Server 2025+ |
| 1706 | Power BI / Fabric                          |

1700 is the highest level Analysis Services supports; 1706 is the highest overall and is Power BI and Fabric only.

##### _将最新兼容级别设为默认_（已启用）

新模型会自动使用最新可用的兼容级别。 When enabled, this overrides the specific compatibility level setting above, and the dropdown is disabled.

##### _新模型使用 Workspace 数据库_（已启用）

创建新模型时，会在 Analysis Services 上自动创建一个 Workspace 数据库。 This allows you to immediately test and query your model during development.

##### _默认保存模式_（AlwaysAsk）

选择保存时是始终保存为文件（.bim）、文件夹（多个 JSON 文件）、TMDL（Tabular Model Definition Language），还是每次保存都询问。 Options: AlwaysAsk, File, Folder, TMDL.

##### _保存到磁盘时使用 PBIX 文件名_（已启用）

保存从 PBIX 文件加载的模型时，默认使用 PBIX 文件名。 This maintains naming consistency between Power BI files and saved model metadata.

##### _为新模型创建用户选项_（已启用）

为新模型自动创建 .tmuo（Tabular Model User Options）文件。 These files store user-specific settings like diagram layouts and window positions.

## Tabular Editor > 键盘

![键盘映射](~/content/assets/images/keyboard-mappings.png)

为所有 Tabular Editor 命令配置键盘快捷键。 Use the search functionality to quickly find specific commands and assign or modify their keyboard shortcuts to match your preferred workflow.

## Tabular Editor > TOM Explorer

![Tom Explorer Settings](~/content/assets/images/unsaved-changes/preferences.png)

Control how the TOM (Tabular Object Model) Explorer presents the model, and what happens to the objects you delete.

The toggles that decide which object types appear in the tree, such as measures, columns, hierarchies, partitions, display folders and hidden objects, are not preferences. They live on the @tom-explorer-view toolbar, where you can change them per model without opening this dialog.

### Display and filtering

##### _Use table groups_ (enabled)

Group your tables in the TOM Explorer, for example to keep calculation groups, dimensions and fact tables apart. Tabular Editor records a table's group in an annotation on the table itself, so the grouping travels with the model. It is internal to Tabular Editor: no other client tool, Power BI Desktop included, shows it. See @table-groups.

##### _显示完整分支_（已禁用）

When you filter the tree, Tabular Editor shows the objects that match your filter string together with their parents. Enable this to also show every child of a match, whether or not the children match the string themselves.

##### _Highlight relationships_ (enabled)

Highlight the relationships that involve the table or column you have selected, so you can see at a glance what a column is joined to.

### Unsaved changes

These settings control how [unsaved changes](xref:unsaved-changes) are indicated in the TOM Explorer and the Properties view.

##### _Mark objects with unsaved changes_ (enabled)

Highlight objects in the TOM Explorer that differ from the last saved version of the model, using a tinted row and a badge on the object's icon: orange for edited objects, green for added objects and red for deleted objects. Tables, folders and groups that contain changed objects get a hatched fill. When disabled, deleted objects still stay visible according to the setting below, and the **Show changes** toolbar filter still works. Use **Color blindness mode** under **User Interface > Accessibility** to mark added objects in teal instead of green.

##### _Keep deleted objects visible_ (Until the model is saved)

How long deleted objects remain visible in the TOM Explorer, struck through, where they used to be. Right-click a deleted object and choose **Restore** to bring it back. Options:

- **Never**: Deleted objects disappear from the TOM Explorer at once.
- **Until the model is saved**: Deleted objects are treated as unsaved changes and disappear when the model is saved.
- **Until the model is closed**: Deleted objects stay visible, and restorable, for the whole editing session, even across saves.

##### _Gather deleted objects under a "Deleted objects" node_ (disabled)

Show the deleted objects of a table, hierarchy, role or table group together under a single **Deleted objects** node at the end of their container, instead of each where it used to be. Right-click the node and choose **Restore** to bring back all of them at once.

##### _Mark properties with unsaved changes in the Properties pane_ (enabled)

Highlight properties in the Properties view that differ from the last saved version of the model, using a tinted row. When disabled, the **Show changes** toolbar filter in the Properties view still works.

### Delete

##### _始终显示删除警告_（已禁用）

If you prefer Tabular Editor 3 to prompt you to confirm all object deletions, enable this setting. 否则，Tabular Editor 3 只会在删除多个对象时，或删除被其他对象引用的对象时提示你确认。

> [!NOTE]
> 在 Tabular Editor 3 中，所有删除操作都可以按 CTRL+Z 撤销。

### Localization

These settings decide the format string Tabular Editor writes when you pick the _Currency_ number format for an object in the Properties pane.

##### _Default currency_ (English (United States))

The formatting convention to base the currency format string on. Pick the locale whose currency symbol, decimal separator and digit grouping you want.

##### _Use a custom currency symbol_ (disabled)

Supply your own symbol instead of taking one from the locale above. The three settings below apply only while this is checked.

##### _Custom currency symbol_

The symbol to use. Enter the symbol on its own, without the number; whitespace is ignored.

##### _Custom currency symbol position_ (Before number)

Whether the symbol goes before or after the numeric value.

##### _Put a space between the number and symbol_ (disabled)

Separate the symbol from the numeric value with a space.

## Tabular Editor > 复制/粘贴

<!-- IMAGE NEEDED: pref-copy-paste.png
     The Tabular Editor > Copy/Paste preferences page at its default settings.
     Alt text: "The Copy/Paste preferences page" -->

控制复制对象时包含哪些元数据：

##### _Include translations_ (enabled)

随对象一起复制翻译元数据。 When enabled, any translations defined for the copied object will also be copied.

##### _包含透视_（已启用）

Copy perspective membership with objects. 启用后，复制的对象将与原对象属于相同的透视。

##### _包含 RLS_（已启用）

随对象一起复制行级安全性表达式。 This applies when copying tables that have RLS rules defined.

##### _包含 OLS_（已启用）

Copy Object-Level Security settings with objects. 在复制带有 OLS 限制的对象时适用。

## Tabular Editor > 透视

<!-- IMAGE NEEDED: pref-perspectives.png
     The Tabular Editor > Perspectives preferences page at its default settings.
     Alt text: "The Perspectives preferences page" -->

控制如何处理透视成员资格：

##### _新对象继承透视成员资格_（已禁用）

新建对象会自动从其父对象继承透视成员资格。 For example, a new measure would automatically be added to the same perspectives as its parent table.

##### _移动后的对象继承透视成员资格_（已禁用）

被移动的对象会从其新的父对象继承透视成员资格。 This is useful when reorganizing your model structure.

##### _将表添加到透视时继承_（已启用）

将表添加到透视时，自动添加该表的所有对象（列、度量值、层次结构）。

##### _从透视中移除表时一并移除_（已启用）

从透视中移除表时，自动移除该表的所有对象。

## Tabular Editor > 架构比较

![Schema Compare preferences](~/content/assets/images/pref-schema-compare.png)

配置在更新表架构并进行架构比较时要忽略哪些更改：

##### _忽略导入模式更改_（已禁用）

Don't flag changes to Import mode properties. 如果希望在架构比较期间忽略导入模式、DirectQuery 模式和 Dual 模式之间的更改，请启用此选项。

##### _忽略数据类型更改_（已禁用）

Don't flag column data type changes. 如果希望在架构比较期间忽略数据类型更改，请启用此选项。

##### _忽略描述更改_（已禁用）

Don't flag changes to object descriptions. 如果你不想在架构比较中看到描述的更改，请启用此选项。

##### _忽略 decimal 与 double 之间的更改_（已禁用）

不要将 decimal 与 double 数据类型之间的更改标记为差异。 This is useful when working with data sources that don't distinguish between these types.

##### _优先使用 Analysis Services 架构检测器_（已禁用）

Use Analysis Services metadata as the source of truth for schema detection. 启用后，Tabular Editor 将直接查询 Analysis Services 实例，而不是使用数据源提供程序的架构信息。

## Tabular Editor > 保存到文件夹/文件

![Save to Folder preferences](~/content/assets/images/pref-save-to-folder.png)

### 序列化模式

##### _使用 TMDL 格式_（已禁用）

使用 Tabular Model Definition Language（TMDL）格式而非 JSON 来保存模型元数据。 TMDL is the modern format recommended for version control and collaboration.

##### _使用推荐的序列化设置_（已启用）

Apply recommended settings for folder-based serialization (overrides custom settings). 启用后，Tabular Editor 会使用将模型保存到文件夹的最佳实践，并针对版本控制进行优化。

### 传统（JSON）序列化设置

##### _Prefix filenames_ (disabled)

为文件名添加数字前缀以便排序。 This can help maintain a consistent file order in file explorers.

##### _本地关系_（已启用）

将关系定义与各个表一起存储，而不是集中存放在一个位置。 This makes it easier to see which relationships belong to each table when using version control.

##### _本地透视_（已启用）

Store perspective membership with individual objects instead of in a central location. This reduces merge conflicts in version control.

##### _本地翻译_（已启用）

将翻译与各个对象一起存储，而不是集中保存在一个位置。 This reduces merge conflicts in version control.

##### _级别_

Select which object types to serialize at different folder levels. 这让你可以将模型文件组织成分层结构。 The available levels are Data Sources, User Defined Functions (UDFs), Shared Expressions, Perspectives, Relationships, Roles, Tables, Columns, Hierarchies, Measures, Partitions, Calculation Items and Translations.

##### _忽略推断对象_（已启用）

不要序列化由引擎自动推断的对象。 This reduces clutter in saved metadata.

##### _忽略推断属性_（已启用）

不要序列化由引擎自动推断的属性。 This keeps saved metadata clean and focused on explicitly set values.

##### _忽略时间戳_（已启用）

Don't serialize timestamp metadata. This is highly recommended for version control as it prevents unnecessary changes in every commit.

##### _忽略 Lineage tag_（已禁用）

不要序列化 Power BI 的 Lineage tag 元数据。 Enable this if you don't want lineage information in your saved metadata.

##### _忽略隐私设置_（已禁用）

不要序列化数据源隐私设置。 Enable this if you manage privacy settings separately.

##### _包含敏感数据_（已禁用）

Include sensitive information like passwords in serialized metadata. This is not recommended for security reasons.

##### _忽略增量刷新分区_（已禁用）

Don't serialize partitions created by incremental refresh policies. Enable this if you want incremental refresh to be managed separately from your saved metadata.

##### _拆分多行字符串_（已启用）

将较长的字符串值拆分为多行，便于在版本控制中阅读。 This makes it easier to see changes in DAX expressions and other long text properties.

##### _排序数组_（已禁用）

Sort array elements alphabetically for consistent serialization. 这可以减少版本控制中无意义的差异，但也可能改变某些元素的逻辑顺序。

### TMDL 序列化设置

##### _缩进模式_（制表符）

选择在 TMDL 文件中使用制表符或空格进行缩进。 Tabs are the default and recommended option.

##### _缩进空格数_（4）

使用空格时，指定每级缩进的空格数。

<a name="miscellaneous"></a>

## AI Features

The parent page carries the two settings that apply to every AI feature, the chat and the [MCP server](xref:mcp-server) alike.

##### _Check for knowledge base updates on startup_ (enabled)

The AI Assistant searches a local copy of the Tabular Editor documentation. When checked, Tabular Editor looks for a newer copy at start-up and downloads it if one is available. This is the only outbound request any AI feature makes on its own.

##### Audit log

**Open audit folder** opens this computer's record of what the AI Assistant and the MCP server did: permission decisions, which tools were called and how each one ended, and the full text of any script that was run or handed over for review. Prompts, replies and data values are never recorded. The record is an Enterprise Edition feature: on Desktop and Business nothing is recorded and the button is not shown. See @ai-audit-log.

## AI Features > AI Assistant

Connection settings for the AI Assistant chat. The **AI Provider** child page renders here. See @ai-assistant for what each provider needs.

##### _Choose provider_ (None)

Which AI provider the chat talks to: **OpenAI**, **Anthropic**, **Azure OpenAI** or **Custom (OpenAI-compatible)**. The fields below change with your choice. An administrator can lock this to a single provider, or narrow the list, by policy.

##### _Base URL_ / _Service endpoint_

Where requests are sent. OpenAI and Anthropic supply a default and the field is optional. Azure OpenAI and Custom have no default, so an endpoint is required.

##### _API Key_

Your own key for the chosen provider. It is stored encrypted on this machine in `Preferences.json`. Tabular Editor ships no built-in key and never proxies your requests.

##### _OpenAI Organization ID_ and _OpenAI Project ID_

Optional, and shown for the OpenAI provider only. Use them where your OpenAI account bills or scopes usage per organization or project.

##### _Model name_ (_Deployment_ for Azure OpenAI)

Which model to use. For OpenAI and Anthropic this is a dropdown filled from an online catalog, so it is empty until the catalog has been fetched once on this machine. For Azure OpenAI the field is labelled **Deployment** and takes the name you gave the deployment, which is not necessarily the name of the underlying model. Leaving it blank uses the provider's default, except for Azure OpenAI and Custom, which have none.

## AI Features > AI Assistant > Preferences

How the chat behaves. See @ai-assistant for the detail behind each group.

### 聊天显示

##### _Show selection context indicator_ (enabled)

Show which model object is currently selected above the chat, so you can see what the assistant will treat as context.

##### _Show custom instructions indicator_ (enabled)

Show which [Custom Instructions](xref:ai-assistant#custom-instructions) were applied above each reply.

##### _Show knowledge base search indicator_ (enabled)

Show progress while the assistant searches the knowledge base.

### Context Compaction

##### _Auto compact_ (enabled)

Summarize the older part of a conversation automatically as it approaches the model's context limit, so a long conversation can carry on.

##### _Auto compact threshold %_ (80)

How full the context window gets before compaction runs, as a percentage of the _model's own_ window rather than a fixed number of tokens. Values outside 50 to 100 have no further effect.

### C# Script

##### _Allow AI assistant to run C# scripts directly_ (disabled)

Let the assistant carry out the model change you asked for, instead of writing a script and opening it for you to run. Only scripts the safety analysis considers safe are run this way, meaning scripts that touch model objects and nothing else; anything reaching for files, the network or an external assembly is still handed to you for review. Each run lands as a single undo step.

This setting is unavailable until **Model metadata** is set to **Write** on the [Permissions](#ai-features--permissions) page, and it becomes available as soon as you change that dropdown, without closing the dialog. It is also unavailable, with a tooltip saying so, where an administrator has set the `DisableCSharpScripts` [policy](xref:policies). It is off by default deliberately: **Model metadata > Write** is also what an agent needs over the MCP server, and granting it there must not silently change what the chat does. See [Letting the assistant change your model](xref:ai-assistant#letting-the-assistant-change-your-model).

##### _Preview changes_ (enabled)

Show the script preview dialog before a change the assistant made stands, so you can see every model metadata change and accept or cancel it. Cancelling puts the model back and tells the assistant you rejected the change.

## AI Features > MCP Server

Settings for the [MCP server](xref:mcp-server), which lets an external agent such as Claude Code, GitHub Copilot or Cursor work on the model you have open.

![MCP Server preferences](~/content/assets/images/pref-mcp-server.png)

##### _Enable MCP Server_ (enabled)

Whether the MCP server is available at all. Clearing it stops a running server and removes both the **Tools > MCP Server...** menu item and the status bar indicator.

##### _Start MCP server automatically_ (disabled)

Start the server when Tabular Editor starts, so an agent can connect without you starting it by hand. If the port is in use at start-up, the server does not start and no prompt is shown.

##### _Require access token_ (disabled)

Make agents present a bearer token, shown in the **Tools > MCP Server...** dialog. The server listens on the loopback interface only, so this matters most on a machine where several people are signed in at once, such as a Remote Desktop or Citrix host, where every session can reach `127.0.0.1`. Administrators can enforce it with the `RequireMcpAccessToken` [policy](xref:policies).

##### _Port_ (42100)

The loopback port the server listens on, from 1024 to 49151. Changing it invalidates existing agent registrations, which point at a fixed address. If the port is taken when you start the server by hand, Tabular Editor offers the next free port it finds.

## AI Features > Permissions

One standing grant per resource, governing both the AI Assistant chat and any agent connected over the MCP server. The chat can additionally ask for something a grant does not cover; an agent cannot, so for MCP the grants apply as they stand and only change when the server restarts.

![AI Features Permissions preferences](~/content/assets/images/pref-ai-permissions.png)

| Resource                   | 级别                  | 默认值   | What it covers                                                                                                                                                     |
| -------------------------- | ------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Model metadata**         | Deny / Read / Write | Read  | Tables, columns, measures, expressions, descriptions and relationships, plus VertiPaq Analyzer statistics. Write allows changes through C# scripts |
| **Model data**             | Deny / Read         | Deny  | Data values from your model, such as DAX query results. There is no write level                                                                    |
| **Best Practice Analyzer** | Deny / Read / Write | Read  | Read lists rules and runs the analysis; Write adds or modifies rules                                                                                               |
| **Documents**              | Deny / Read / Write | Write | Your open C# script and DAX query tabs. Read is their contents; Write creates or modifies them                                                     |
| **Macros**                 | Deny / Read / Write | Write | Your macro library                                                                                                                                                 |

**Write** covers Read, so there is no need to grant both. **Model data** is the one resource denied by default, because metadata describes your model while data _is_ its contents.

In the Enterprise, Consultancy and Trial editions an administrator can cap any of these by [policy](xref:policies), separately for the chat and for the MCP server. A capped dropdown is shown read-only. See @ai-assistant for how the chat asks for what a grant does not cover, and @mcp-server for what an agent sees.

## Tabular Editor > Miscellaneous

![Miscellaneous preferences](~/content/assets/images/pref-miscellaneous.png)

### 元数据同步

These settings control how Tabular Editor 3 deals with model metadata that changes outside the application. The first three cover a model loaded from a database on an instance of Analysis Services and rely on an Analysis Services trace. **Automatically reload from disk** covers a model loaded from a file or a folder, and watches those files directly.

##### _当本地元数据与已部署模型不同步时发出警告_（已启用）

勾选后，只要你对模型进行了尚未保存到 Analysis Services 的本地更改，Tabular Editor 内就会显示一条信息栏。 For example, if you're wondering why a DAX query or a Pivot Grid does not produce the expected result, this could be due to a measure expression being changed in Tabular Editor without saving the change to Analysis Services. The bar disappears when you hit save (Ctrl+S).

##### _跟踪外部模型更改_（已启用）

就像 Power BI Desktop 能检测到外部工具对 Data model 做出的更改一样，Tabular Editor 也能做到。此选项仅适用于 Analysis Services 的本地实例（即与 Tabular Editor 运行在同一台计算机上的 msmdsrv.exe 进程）。 When checked, Tabular Editor starts a trace on Analysis Services and notifies you if external changes are made.

##### _自动刷新本地 Tabular Object Model 元数据_（已启用）

When the tracing mechanism as described above is enabled, this option allows Tabular Editor to automatically refresh the model metadata when an external change is detected. This is useful if you often switch back and forth between Power BI Desktop and Tabular Editor 3.

##### _Automatically reload from disk_ (enabled)

When checked, Tabular Editor watches the metadata files the model was loaded from and reloads the model when another application changes them. Unlike the two settings above, this doesn't involve an Analysis Services trace: it watches the files themselves, so it covers a model loaded from a `.bim` file or from a folder, whether or not a server is involved. If the model has unsaved changes, Tabular Editor asks you which copy to keep. See [Auto-reload from disk](xref:auto-reload).

##### _清理遗留的 Tabular Editor 跟踪_

通常，Tabular Editor 3 会自动停止并移除因上述设置而启动的所有 AS 跟踪。 However, if the application was shut down prematurely, the traces may never be stopped. By clicking this button, all AS traces started by any instance of Tabular Editor will be removed.

> [!NOTE]
> 清理按钮只有在 Tabular Editor 连接到 Analysis Services 实例时才可用。

## 数据浏览 > Pivot Grid

![Pivot Grid preferences](~/content/assets/images/pref-pivot-grid.png)

### Basic

##### _自动刷新 Pivot Grid_ (已启用)

Automatically refresh pivot grids when model changes are saved. Just like with DAX queries, this allows you to immediately see the impact of changes to measures.

##### _Pivot Grid 字段不匹配时发出警告_（已启用）

当 Pivot Grid 的字段定义与当前模型不匹配时显示警告。 This can happen if you've deleted or renamed fields used in a saved pivot grid.

### Field Headers

##### _Pivot header word wrap_ (enabled)

Enable word wrapping in pivot grid headers. This makes long field names more readable.

### 字段列表

##### _始终显示 Pivot Grid 字段列表_（已启用）

默认保持 Pivot Grid 字段列表可见。 Disable this if you prefer more screen space for the pivot grid itself.

##### _在透视表自定义中显示所有字段_（已启用）

默认在 Pivot Grid 字段列表中显示所有可用字段，包括隐藏字段。

##### _Pivot Grid 自定义默认布局_ (StackedDefault)

选择 Pivot Grid 字段列表的默认布局。可选项包括：

- **StackedDefault**：字段和区域显示在同一个堆叠面板中
- **StackedSideBySide**：字段和区域显示在并排面板中
- **TopPanelOnly**：字段列表仅在顶部显示
- **BottomPanelOnly2by2**: 底部以 2x2 网格显示字段列表
- **BottomPanelOnly1by4**：底部 1x4 布局的字段列表

## Data Browsing > DAX Query

![DAX Query preferences](~/content/assets/images/pref-dax-query.png)

### Basic

##### _Automatically execute DAX queries by default_ (enabled)

New DAX queries open with **Auto-execute** enabled, so the query re-runs whenever changes are made to the deployed semantic model. Turn it off if you would rather execute each query yourself.

##### _Keep existing sorting and filtering in the result grid_ (WhenQueryUnchanged)

控制重新执行查询时是否保留网格筛选和排序：

- **Never**: sorting and filtering are always reset when a query is executed
- **WhenQueryUnchanged**: sorting and filtering are reset only when the query is modified
- **Always**: sorting and filtering are never reset if the columns still exist

### Query settings

##### _Smart selection_ (enabled)

When you execute part of a query, Tabular Editor turns that selection into a valid DAX query on your behalf, wrapping a scalar expression in curly braces and adding the `DEFINE` section or the `EVALUATE` keyword when they are not part of the selection.

##### _Row limit_ (1,000)

Wraps every `EVALUATE` statement in a `TOPN` call, to keep an accidental query over a large table from running for a long time or exhausting memory. Set it to `0` to remove the limit entirely.

### Code Generation

##### _Use comments as separators_ (enabled)

Insert comments into generated object definitions, for example the `DEFINE` block produced by **Define object in query**, to make them easier to read.

## Data Browsing > Table Preview

![Table Preview preferences](~/content/assets/images/pref-table-preview.png)

### Basic

##### _Automatically refresh table previews by default_ (enabled)

New table previews open with **Auto-refresh** enabled, so the preview refreshes whenever changes are made to the deployed semantic model. This is useful when debugging: update an expression in one window while a preview of the same table is open in another.

##### _Sort table preview columns alphabetically_ (disabled)

When checked, table preview columns are sorted alphabetically by name, matching the order the @tom-explorer-view lists a table's columns in. When unchecked (the default), columns appear in the order the engine returns them, which is roughly internal column order and can look arbitrary.

##### _Max. values in filter dropdown_ (5,000)

Maximum number of distinct values listed in a column's filter dropdown. On a column with more distinct values than this, the values beyond the limit are not listed and cannot be ticked directly. Raising it lists more values at the cost of a heavier query each time the dropdown is opened. Accepts 100 to 1,000,000.

##### _Max. rows to sort without an attribute hierarchy_ (100,000)

Upper bound on the number of rows Tabular Editor sorts by a column that has no attribute hierarchy to sort on.

### DirectQuery

##### _Row limit_ (100)

Maximum number of rows to retrieve for a table preview in DirectQuery mode. Raise it if you need to see more data, bearing in mind that every row is fetched from the underlying source.

### 行为

##### _Track selected column in TOM Explorer_ (enabled)

When you select a column in the @tom-explorer-view, the open table preview scrolls that column into view and highlights it, which is the quickest way to find one column of a very wide table. The same setting can be turned on and off for a single preview with **Track selected column** on the Table Preview toolbar.

## DAX编辑器 > 常规

![Dax 编辑器 常规](~/content/assets/images/dax-editor-general.png)

Tabular Editor 3 的 DAX编辑器可高度自定义。 This page provides settings for general configuration of the DAX editor:

##### _行号_（已启用）

在编辑器左侧边距显示行号。

##### _代码折叠_（已启用）

在 DAX 代码中启用可折叠区域，以提升可读性。 Make sure you try out this feature!

##### _显示空白字符_（已禁用）

Show dots for spaces and arrows for tabs. This can be helpful when diagnosing indentation issues.

##### _Indentation guides_ (enabled)

显示竖线以标示缩进层级。

##### _使用制表符_（已禁用）

When checked, a tab character (`\t`) is inserted whenever the TAB button is hit. Otherwise, a number of spaces corresponding to the _Indent width_ setting is inserted.

##### _注释样式_（斜杠）

DAX 支持使用斜杠（`//`）或连字符（`--`）的行注释。 This setting determines which style of comment is used when Tabular Editor 3 generates DAX code.

##### _DAX 函数文档_

使用此设置指定：当光标位于某个 DAX 函数上并按下 F12 时，默认浏览器要打开的 URL。 Options include https://dax.guide (recommended) and Microsoft's official documentation.

### DAX 设置

##### _Locale_

设置 DAX 函数和格式所使用的区域设置。

##### _Analysis Services 版本设置_

只有当 Tabular Editor 3 无法确定所使用的 Analysis Services 版本时，这些设置才会用得上，比如直接加载 Model.bim 文件时就是这样。 In this case, Tabular Editor tries to guess which version the model will be deployed to, based on the compatibility level. If Tabular Editor reports incorrect semantic/syntax errors, you may need to tweak these settings.

## DAX编辑器 > 自动格式化

![自动格式化设置](~/content/assets/images/auto-formatting-settings.png)

DAX编辑器 **非常** 强大，能在你输入的同时帮你写出漂亮、易读的 DAX 代码。

##### _输入时自动格式化代码_（已启用）

这个选项会在发生某些按键操作时，自动应用特定的格式规则。 For example, when a parenthesis is closed, this feature will ensure that everything within the parentheses is formatted according to the other settings on this page.

##### _自动格式化函数调用_（已启用）

此选项专门控制：当输入右括号时，是否对函数调用（参数与括号之间的空格）进行自动格式化。

##### _自动缩进_（已启用）

这个选项会在函数调用内插入换行时，自动缩进函数参数。

##### _Auto-brace_ (enabled)

当输入左括号或引号时，此选项会自动插入对应的右括号或引号。

##### _Wrap selection_ (enabled)

When enabled, this option automatically wraps the current selection with the closing brace, when an opening brace is entered.

### 格式化规则

这些设置用于控制 DAX 代码中空白字符的格式：既包括自动格式化时的处理，也包括手动格式化代码时的处理。

##### _函数后加空格_（已禁用）

# [已启用](#tab/space-after-function-on)

```DAX
SUM ( 'Sales'[Amount] )
```

# [已禁用](#tab/space-after-function-off)

```DAX
SUM( 'Sales'[Amount] )
```

***

##### _函数后换行_（已禁用）

仅在函数调用需要拆分为多行时生效。

# [已启用](#tab/newline-after-function-on)

```DAX
SUM
(
    'Sales'[Amount]
)
```

# [已禁用](#tab/newline-after-function-off)

```DAX
SUM(
    'Sales'[Amount]
)
```

***

##### _Pad parentheses_ (enabled)

# [已启用](#tab/pad-parentheses-on)

```DAX
SUM( Sales[Amount] )
```

# [已禁用](#tab/pad-parentheses-off)

```DAX
SUM(Sales[Amount])
```

***

##### _长格式行长度限制_（120）

在使用 **格式化 DAX（长行）** 选项时，表达式在被拆分为多行之前，单行可保留的最大字符数。

##### _短格式行长度限制_（60）

使用 **Format DAX (short lines)** 选项时，表达式在拆分为多行之前，每行最多保留的字符数。

### Casings and Quotes

除了格式化 DAX 代码的空白字符外，Tabular Editor 3 还可以修正对象引用，以及函数/关键字的大小写。

##### _修正度量值/列限定符_（已启用）

选中后，会自动从度量值引用中移除表前缀，并在列引用中自动插入表前缀。

##### _Preferred keyword casing_ (UPPER)

此设置可让你更改关键字的大小写形式，例如 `ORDER BY`、`VAR`、`EVALUATE` 等。 It also governs the fixed keyword _values_ auto-complete offers for functions that take them: `ASC` and `DESC`, `KEEP`, `FIRST`, `LAST` and `DEFAULT`, the `CROSSFILTER` directions and `LOOKUP`'s `EXPLICIT` and `INFERRED`. Choose **Capitalize first letter only** to be offered `Explicit` rather than `EXPLICIT`.

##### _Preferred function casing_ (UPPER)

此设置可让你更改函数名称的大小写形式，例如 `CALCULATE(...)`、`SUM(...)` 等。

##### _修正关键字/函数大小写_（已启用）

选中后，无论是自动格式化还是手动格式化代码，都会自动更正关键字和函数的大小写。

##### _修正对象引用大小写_（已启用）

DAX is a case-insensitive language. When this is enabled, references to tables, columns and measures are automatically corrected such that the casing matches the physical name of the referenced objects.

##### _始终为表名加引号_（已禁用）

在 DAX 中，引用某些表名时不需要用单引号括起来。 However, if you prefer table references to always be quoted, you can check this option.

##### _扩展列始终加前缀_（已禁用）

Extension columns can be defined without a table name. 选中后，DAX编辑器将始终为扩展列添加表前缀。

## DAX编辑器 > Code Assist

![DAX Editor Code Assist preferences](~/content/assets/images/pref-dax-code-assist.png)

在此页面上，你可以配置两项最重要的 Code Assist 功能：调用提示（也称“参数信息”）和自动完成。

##### _自动完成触发方式_

Control when the auto-complete list appears. Options include automatic triggering after typing a certain number of characters, or manual triggering with CTRL+Space.

##### _Calltip trigger_

Control when parameter information appears. Options include automatic triggering when opening a function parenthesis, or manual triggering.

##### _增量搜索_（已启用）

Enable fuzzy/incremental searching in auto-complete. This allows you to find items by typing parts of their name, not just the beginning.

##### _建议表名_（已启用）

在自动完成建议中包含表名。

##### _始终为表名加引号_（已禁用）

在建议中自动为表名加引号，即使并非必需。

##### _仅显示首字母_（已禁用）

Only show items starting with the typed letter. Disable this to use incremental search instead.

## DAX编辑器 > 代码操作

![DAX Editor Code Actions preferences](~/content/assets/images/pref-dax-code-actions.png)

配置自动代码改进建议：

##### _变量前缀_

定义变量名可接受的前缀（例如 `_`、`__`、`var_`、`var`、`v_`、`v`、`VAR_`）。 Code actions will suggest adding these prefixes to variable names that don't follow the convention.

##### _列前缀_

定义临时列名可接受的前缀（例如 `@`、`_`、`x`、`x_`）。 Code actions will suggest adding these prefixes to temporary column names that don't follow the convention.

## SQL 编辑器 / M 编辑器 / C# 编辑器

<!-- IMAGE NEEDED: pref-code-editors.png
     One of the SQL Editor, M Editor and C# Editor preferences pages. The three share a
     layout, so a single shot covers the section.
     Alt text: "The code editor preferences page, shared by the SQL, M and C# editors" -->

SQL、M（Power Query）和 C# Script 编辑器也提供类似的配置选项，包括：

- 语法高亮和配色方案
- 自动格式化选项
- Code Assist 和自动完成功能
- 注释样式和缩进偏好

每个编辑器都可以单独自定义，以符合你偏好的代码风格。

## DAX Formatter

<!-- IMAGE NEEDED: pref-dax-formatter.png
     The DAX Formatter preferences page at its default settings.
     Alt text: "The DAX Formatter preferences page" -->

##### _DAX formatter 同意_（已禁用）

同意将 DAX 代码发送到外部 DAX 格式化服务 (www.daxformatter.com)。 When enabled, you can use this service to format DAX code according to community standards.

##### _DAX formatter 请求超时_（5000）

DAX formatter 请求的超时时间，单位为毫秒。 Increase this if you frequently get timeout errors when using the DAX formatter.

## DAX优化器集成

<!-- IMAGE NEEDED: pref-dax-optimizer.png
     The DAX Optimizer Integration preferences page at its default settings.
     Alt text: "The DAX Optimizer Integration preferences page" -->

配置 DAX优化器集成（仅企业版）：

##### _自动连接_（null/提示）

在可用时自动连接到 DAX优化器。 When not set, you will be prompted the first time.

##### _对 VPAX 文件进行混淆处理_（已启用）

发送到 DAX优化器时对模型元数据进行匿名化处理。 This protects sensitive information like table and column names while still allowing analysis.

##### _混淆字典目录_（`%LocalAppData%\TabularEditor3\DaxOptimizer`）

指定混淆字典的存储位置。 The dictionary maintains consistent obfuscation across multiple analyses.

## VertiPaq分析器

![VertiPaq Analyzer preferences](~/content/assets/images/pref-vertipaq-analyzer.png)

##### _包含 TOM 元数据_（已启用）

在 VertiPaq分析器的统计信息中包含 Tabular Object Model 元数据。 This provides richer information about your model structure.

##### _从数据读取统计信息_（已启用）

通过扫描实际数据来读取统计信息（更准确，但更慢）。 When disabled, only metadata is used.

##### _Direct Lake 提取模式_（ResidentOnly）

如何从 Direct Lake 模型中提取统计信息：

- **ResidentOnly**：仅分析当前已加载到内存中的数据
- **All**：包含未驻留的数据（更慢，可能触发数据加载）

##### _从动态管理视图读取统计信息_（已禁用）

使用 DMV 收集统计信息（更快，但准确性较低）。 This is an alternative to reading from data.

##### _关系采样行数_（3）

Number of rows to sample when analyzing relationships. Higher values provide more accuracy but take longer.

##### _列批次大小_（50）

Number of columns to analyze in each batch. Adjust this based on your model size and performance requirements.

## Power BI 集成

![Power BI Integration preferences](~/content/assets/images/pref-power-bi.png)

##### _Power BI 端点基础 URL_（`https://api.powerbi.com`）

用于 Power BI API 调用的基础 URL。 Change this if you're working with a sovereign cloud or custom environment.

##### _Fabric 端点基础 URL_（`https://api.fabric.microsoft.com`）

用于调用 Microsoft Fabric API 的基础 URL。 Change this if you're working with a sovereign cloud or custom environment.

##### _使用嵌入式浏览器进行身份验证_（已启用）

使用嵌入式浏览器进行 OAuth 身份验证，而不是系统浏览器。 This provides a more integrated experience.

## 代理设置

![Proxy Settings preferences](~/content/assets/images/pref-proxy-settings.png)

##### _代理类型_（无）

Choose between:

- **无**：不配置代理
- **系统**：使用系统代理设置
- **自定义**：指定自定义代理配置

##### _代理地址_

代理服务器的地址（例如 `http://proxy.company.com:8080`）。

##### _Proxy user_

如需代理身份验证，请输入用户名。

##### _代理密码_

用于代理身份验证的密码（加密存储）。

##### _使用默认凭据_（已启用）

Use the current Windows credentials for proxy authentication. 其行为与 [Power BI Desktop 一致](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy)。

##### _对本地地址绕过代理_（已启用）

对本地地址绕过代理。 This is recommended for performance.

##### _Proxy bypass list_

应绕过代理的地址列表（例如 `localhost;*.company.local`）。

## 后续步骤

如需查看最常调整的偏好设置的易用指南，请参阅入门指南（Personalizing TE3）[xrefid: personalizing-te3]。
