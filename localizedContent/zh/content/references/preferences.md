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

不同组织的 Tabular Data model 开发流程和工作流差异很大。为了确保该工具尽可能适配这些工作流，Tabular Editor 3 高度可定制——不仅是用户界面的外观和体验，还涵盖更高级的主题，比如 Web 代理、更新和反馈、行数限制、超时、架构比较偏好等。

本文介绍 Tabular Editor 3 的“偏好设置”对话框，以及你可以通过该对话框控制的设置。

要打开“偏好设置”对话框，请依次选择 **工具 > 偏好**。

> [!NOTE]
> 所有 Tabular Editor 偏好设置都会针对每个 Windows 用户配置文件分别存储在 `%localappdata%\\TabularEditor3` 文件夹中。只需复制该文件夹中的内容，即可将你的设置迁移到另一台机器。

> [!TIP]
> 在“偏好”对话框顶部使用搜索框，可快速找到特定设置。

## Tabular Editor > 功能

![Pref General Features](~/content/assets/images/pref-general-features.png)

### Power BI

##### _允许不受支持的编辑_（已禁用）

仅当将 Tabular Editor 3 作为 Power BI Desktop 的外部工具使用时，此选项才适用。勾选后，连接到 Power BI Desktop 实例时，你就能编辑所有 TOM Data model 建模属性。通常建议保持未选中，以免不小心修改 Power BI 文件中 [Power BI Desktop 不支持](xref:desktop-limitations) 的内容。

##### _隐藏自动日期/时间警告_（已禁用）

勾选后，将不再显示有关 Power BI 自动日期/时间表的警告。当 Power BI Desktop 中启用“自动日期/时间”设置时，会创建计算表格，从而触发 Tabular Editor 3 内置 DAX 分析器的警告。

##### _在 DAX 首行换行_（已禁用）

在 Power BI Desktop 中，由于公式栏显示 DAX 代码的方式，通常会在 DAX 表达式的第一行插入换行。如果你经常在 Tabular Editor 和 Power BI Desktop 之间来回切换，可考虑启用此选项，让 Tabular Editor 3 自动插入该换行。

##### _仅适用于多行 DAX 表达式_（已启用）

启用“DAX 首行换行”后，此子设置用于控制是否仅对多行 DAX 表达式添加换行。勾选后，单行表达式将保持不变。

##### _默认 Power BI 身份验证模式_（集成）

选择连接到 Power BI Dataset 时要使用的默认身份验证方法（集成、ServicePrincipal 或 MasterUser）。

### Best Practice Analyzer

##### _在后台扫描最佳实践违规项_（已启用）

如果未勾选，你需要在 Best Practice Analyzer 工具窗口中手动运行一次“最佳实践分析”，才能查看是否存在违规项。勾选后，只要发生更改，就会在后台线程中持续执行扫描。对于非常大的模型，或包含非常复杂的最佳实践规则的模型，这可能会引发问题。

##### _内置 BPA 规则_（新用户默认启用）

选择启用、禁用，或在使用 Tabular Editor 内置的 Best Practice Analyzer 规则前提示你确认。内置规则覆盖格式设置、元数据、模型布局、DAX 表达式以及翻译等方面的关键最佳实践。新安装将默认启用内置规则。

### 通知

##### _数据刷新通知_（已启用）

勾选后，数据刷新操作完成时会显示通知。

### DAX 公式自动修正

##### _启用公式修复_（已启用）

当对象被重命名或移动时，自动调整 DAX 表达式中的引用。这个功能可确保你在重新组织模型时，DAX 代码仍然有效。

##### _粘贴时启用公式修复_（已启用）

在粘贴对象时，自动调整 DAX 表达式中的引用。在表或模型之间复制度量值或计算列时很有用。

### Direct Lake

##### _保存时自动刷新_（已启用）

保存更改时自动刷新 Direct Lake 表，确保数据为最新。这可确保你的 Direct Lake 模型与底层数据源保持同步。

## Tabular Editor > 更新与反馈

![Updates and Feedback preferences](~/content/assets/images/pref-updates-and-feedback.png)

### Updates

##### _Show "Get Started" page on updates_ (enabled)

When checked, the **Get Started** page opens automatically the first time you run Tabular Editor after it has been updated. It appears **on updates**, not on every start-up. You can open it at any time from **Help > Get Started**.

##### _启动时检查更新_（已启用）

勾选后，Tabular Editor 会在应用启动时检查是否有新版本。这可确保你及时了解最新功能和错误修复。

##### _Major updates only_ (disabled)

When checked, only major version updates trigger notifications. Minor and patch updates are ignored. This setting is only available while _Check for updates on start-up_ is checked.

The version you are running is shown below these settings, along with a **Check for updates** button that runs the check immediately.

### Managed by your organization

Where an administrator has configured [policies](xref:policies), a read-only **Managed by your organization** section is appended to this page listing every policy value Tabular Editor found, as `Name = value`. Hover over an entry to see which registry key and hive it came from.

A value Tabular Editor could not interpret is listed with an `(invalid)` marker rather than being left out. That marker is the fastest way to find the typo behind a policy that appears to do nothing, so check here first when a policy is not taking effect.

The section is absent when no policy applies. Settings that a policy locks or limits are shown read-only elsewhere in this dialog, and in the **Tools > MCP Server...** dialog, with a tooltip saying so.

### Usage Data and Feedback

##### _通过收集匿名使用数据帮助改进 Tabular Editor_（已启用）

数据不包含任何个人身份信息，也不包含有关你的 Data model 的结构或内容的任何信息。如果你仍希望退出遥测，请取消勾选此项。

##### _发送错误 Report_（已启用）

勾选后，如果发生崩溃，Tabular Editor 会显示发送崩溃 Report 的选项。崩溃 Report 在调试时非常有帮助，所以如果你不介意，就保持勾选吧！

## Tabular Editor > 部署

![Model Deployment preferences](~/content/assets/images/pref-model-deployment.png)

使用 Deployment Wizard 时，配置默认要部署的对象类型：

##### _部署数据源_（已禁用）

部署时包含数据源定义。如果你希望在部署模型更改的同时部署数据源连接字符串和设置，请启用此选项。

##### _部署分区_（已禁用）

部署时包含分区定义。如果你希望在部署模型更改的同时部署分区配置，请启用此选项。

##### _部署刷新策略分区_（已禁用）

部署时包含由增量刷新策略创建的分区。此选项用于控制是否部署由增量刷新策略创建的分区。

##### _部署模型角色_（已禁用）

部署时包含角色定义。若要部署行级安全性（RLS）和对象级安全性（OLS）角色，请启用此选项。

##### _部署模型角色成员_（已禁用）

部署时包含角色成员分配。若要部署安全角色的用户和组分配，请启用此选项。

##### _部署共享表达式_（已禁用）

部署时包含共享表达式（M 表达式）。如需部署 Power Query 共享表达式，请启用此选项。

### 部署元数据

##### _标注部署元数据_（已禁用）

在已部署的对象上添加部署时间戳和用户信息作为注释。这有助于跟踪模型更改是在什么时候、由谁部署的。

### 备份设置

##### _保存时备份_（已启用）

在本地保存更改时创建模型备份。如果需要回退更改，这会提供一道安全保障。

##### _备份保存位置_

指定用于存储保存备份的文件夹。默认情况下，除非指定位置，否则不会创建备份。

##### _部署时备份_（已启用）

在部署更改之前，为目标模型创建备份。这样可以在需要时还原到之前的版本。

##### _备份位置_

指定用于存储部署备份的文件夹。默认情况下，除非指定位置，否则不会创建备份。

## Tabular Editor > 默认设置

<!-- IMAGE NEEDED: pref-defaults.png
     The Tabular Editor > Defaults preferences page at its default settings.
     Alt text: "The Defaults preferences page" -->

##### _新模型兼容级别_（1600）

为新创建的模型设置默认兼容级别。 The choices are the same as in the **New Model** dialog:

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

创建新模型时，会在 Analysis Services 上自动创建一个 Workspace 数据库。这样便可在开发过程中立即测试并查询模型。

##### _默认保存模式_（AlwaysAsk）

选择保存时是始终保存为文件（.bim）、文件夹（多个 JSON 文件）、TMDL（Tabular Model Definition Language），还是每次保存都询问。选项：AlwaysAsk、File、Folder、TMDL。

##### _保存到磁盘时使用 PBIX 文件名_（已启用）

保存从 PBIX 文件加载的模型时，默认使用 PBIX 文件名。这可以保持 Power BI 文件与已保存模型元数据之间的命名一致性。

##### _为新模型创建用户选项_（已启用）

为新模型自动创建 .tmuo（Tabular Model User Options）文件。这些文件会存储用户特定的设置，例如图表布局和窗口位置。

## Tabular Editor > 键盘

![键盘映射](~/content/assets/images/keyboard-mappings.png)

为所有 Tabular Editor 命令配置键盘快捷键。使用搜索功能可以快速找到特定命令，并分配或修改其键盘快捷键，以符合您偏好的工作流程。

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

如果你希望 Tabular Editor 3 在删除任何对象时都提示你确认，就启用这个设置。否则，Tabular Editor 3 只会在删除多个对象时，或删除被其他对象引用的对象时提示你确认。

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

##### _包含翻译_（已启用）

随对象一起复制翻译元数据。启用后，复制对象上定义的任何翻译也会一并复制。

##### _包含透视_（已启用）

随对象一起复制其透视归属关系。启用后，复制的对象将与原对象属于相同的透视。

##### _包含 RLS_（已启用）

随对象一起复制行级安全性表达式。仅在复制已定义 RLS 规则的表时适用。

##### _包含 OLS_（已启用）

随对象一起复制对象级安全性设置。在复制带有 OLS 限制的对象时适用。

## Tabular Editor > 透视

<!-- IMAGE NEEDED: pref-perspectives.png
     The Tabular Editor > Perspectives preferences page at its default settings.
     Alt text: "The Perspectives preferences page" -->

控制如何处理透视成员资格：

##### _新对象继承透视成员资格_（已禁用）

新建对象会自动从其父对象继承透视成员资格。例如，新建的度量值会自动添加到与其父表相同的透视中。

##### _移动后的对象继承透视成员资格_（已禁用）

被移动的对象会从其新的父对象继承透视成员资格。这在重新组织模型结构时很有用。

##### _将表添加到透视时继承_（已启用）

将表添加到透视时，自动添加该表的所有对象（列、度量值、层次结构）。

##### _从透视中移除表时一并移除_（已启用）

从透视中移除表时，自动移除该表的所有对象。

## Tabular Editor > 架构比较

![Schema Compare preferences](~/content/assets/images/pref-schema-compare.png)

配置在更新表架构并进行架构比较时要忽略哪些更改：

##### _忽略导入模式更改_（已禁用）

不要标记导入模式属性的更改。如果希望在架构比较期间忽略导入模式、DirectQuery 模式和 Dual 模式之间的更改，请启用此选项。

##### _忽略数据类型更改_（已禁用）

不要标记列数据类型的更改。如果希望在架构比较期间忽略数据类型更改，请启用此选项。

##### _忽略描述更改_（已禁用）

不要标记对象描述的更改。如果你不想在架构比较中看到描述的更改，请启用此选项。

##### _忽略 decimal 与 double 之间的更改_（已禁用）

不要将 decimal 与 double 数据类型之间的更改标记为差异。在处理不会区分这些类型的数据源时，这很有用。

##### _优先使用 Analysis Services 架构检测器_（已禁用）

将 Analysis Services 元数据作为架构检测的权威依据。启用后，Tabular Editor 将直接查询 Analysis Services 实例，而不是使用数据源提供程序的架构信息。

## Tabular Editor > 保存到文件夹/文件

![Save to Folder preferences](~/content/assets/images/pref-save-to-folder.png)

### 序列化模式

##### _使用 TMDL 格式_（已禁用）

使用 Tabular Model Definition Language（TMDL）格式而非 JSON 来保存模型元数据。 TMDL 是推荐用于版本控制与协作的现代格式。

##### _使用推荐的序列化设置_（已启用）

应用基于文件夹的序列化推荐设置（会覆盖自定义设置）。启用后，Tabular Editor 会使用将模型保存到文件夹的最佳实践，并针对版本控制进行优化。

### 传统（JSON）序列化设置

##### _为文件名添加前缀_（已禁用）

为文件名添加数字前缀以便排序。这有助于在文件资源管理器中保持一致的文件顺序。

##### _本地关系_（已启用）

将关系定义与各个表一起存储，而不是集中存放在一个位置。在使用版本控制时，这样更容易看清每个表分别包含哪些关系。

##### _本地透视_（已启用）

将透视成员关系与各个对象一起存储，而不是集中存放在一个位置。这会减少版本控制中的合并冲突。

##### _本地翻译_（已启用）

将翻译与各个对象一起存储，而不是集中保存在一个位置。这会减少版本控制中的合并冲突。

##### _级别_

选择在不同文件夹层级要序列化的对象类型。这让你可以将模型文件组织成分层结构。 The available levels are Data Sources, User Defined Functions (UDFs), Shared Expressions, Perspectives, Relationships, Roles, Tables, Columns, Hierarchies, Measures, Partitions, Calculation Items and Translations.

##### _忽略推断对象_（已启用）

不要序列化由引擎自动推断的对象。这能减少已保存元数据的杂乱。

##### _忽略推断属性_（已启用）

不要序列化由引擎自动推断的属性。这能让已保存的元数据保持整洁，并专注于显式设置的值。

##### _忽略时间戳_（已启用）

不要序列化时间戳元数据。强烈建议在版本控制中启用此项，因为它可以避免每次提交都产生不必要的变更。

##### _忽略 Lineage tag_（已禁用）

不要序列化 Power BI 的 Lineage tag 元数据。如果你不希望已保存的元数据中包含 Lineage tag 信息，就启用此项。

##### _忽略隐私设置_（已禁用）

不要序列化数据源隐私设置。如果你单独管理隐私设置，请启用此项。

##### _包含敏感数据_（已禁用）

在序列化的元数据中包含密码等敏感信息。出于安全原因，不建议这样做。

##### _忽略增量刷新分区_（已禁用）

不要序列化由增量刷新策略创建的分区。如果希望增量刷新与已保存的元数据分开管理，请启用此选项。

##### _拆分多行字符串_（已启用）

将较长的字符串值拆分为多行，便于在版本控制中阅读。这样更容易看清 DAX 表达式和其他长文本属性的改动。

##### _排序数组_（已禁用）

按字母顺序对数组元素排序，以获得一致的序列化结果。这可以减少版本控制中无意义的差异，但也可能改变某些元素的逻辑顺序。

### TMDL 序列化设置

##### _缩进模式_（制表符）

选择在 TMDL 文件中使用制表符或空格进行缩进。制表符是默认且推荐的选项。

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

勾选后，只要你对模型进行了尚未保存到 Analysis Services 的本地更改，Tabular Editor 内就会显示一条信息栏。例如，如果你在排查某个 DAX 查询或 Pivot Grid 为何未产生预期结果，原因可能是你在 Tabular Editor 中更改了某个度量值表达式，但没有将更改保存到 Analysis Services。当你按下保存（Ctrl+S）时，该提示条就会消失。

##### _跟踪外部模型更改_（已启用）

就像 Power BI Desktop 能检测到外部工具对 Data model 做出的更改一样，Tabular Editor 也能做到。这个选项只适用于 Analysis Services 的本地实例（也就是在和 Tabular Editor 同一台机器上运行的 msmdsrv.exe 进程）。勾选后，Tabular Editor 会在 Analysis Services 上启动跟踪，并在检测到外部更改时通知你。

##### _自动刷新本地 Tabular Object Model 元数据_（已启用）

启用上述跟踪机制后，这个选项会让 Tabular Editor 在检测到外部更改时自动刷新模型元数据。如果你经常在 Power BI Desktop 和 Tabular Editor 3 之间来回切换，这会很有用。

##### _Automatically reload from disk_ (enabled)

When checked, Tabular Editor watches the metadata files the model was loaded from and reloads the model when another application changes them. Unlike the two settings above, this doesn't involve an Analysis Services trace: it watches the files themselves, so it covers a model loaded from a `.bim` file or from a folder, whether or not a server is involved. If the model has unsaved changes, Tabular Editor asks you which copy to keep. See [Auto-reload from disk](xref:auto-reload).

##### _清理遗留的 Tabular Editor 跟踪_

通常，Tabular Editor 3 会自动停止并移除因上述设置而启动的所有 AS 跟踪。但如果应用程序过早关闭，这些跟踪可能就不会停止。点击此按钮后，将移除由任何 Tabular Editor 实例启动的所有 AS 跟踪。

> [!NOTE]
> 清理按钮只有在 Tabular Editor 连接到 Analysis Services 实例时才可用。

## 数据浏览 > Pivot Grid

![Pivot Grid preferences](~/content/assets/images/pref-pivot-grid.png)

### Basic

##### _自动刷新 Pivot Grid_ (已启用)

保存模型更改后自动刷新 Pivot Grid。与 DAX 查询类似，这使你能立即看到对度量值所做更改的影响。

##### _Pivot Grid 字段不匹配时发出警告_（已启用）

当 Pivot Grid 的字段定义与当前模型不匹配时显示警告。如果你删除或重命名了已保存的 Pivot Grid 中使用的字段，就可能出现这种情况。

### Field Headers

##### _Pivot Grid 标题自动换行_（已启用）

在 Pivot Grid 标题中启用自动换行。这样可以让较长的字段名更易读。

### 字段列表

##### _始终显示 Pivot Grid 字段列表_（已启用）

默认保持 Pivot Grid 字段列表可见。如果你希望为 Pivot Grid 本身留出更多屏幕空间，请禁用此选项。

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

Tabular Editor 3 的 DAX编辑器可高度自定义。本页面提供 DAX编辑器的常规配置选项：

##### _行号_（已启用）

在编辑器左侧边距显示行号。

##### _代码折叠_（已启用）

在 DAX 代码中启用可折叠区域，以提升可读性。一定要试试这个功能！

##### _显示空白字符_（已禁用）

用圆点表示空格，用箭头表示制表符。在诊断缩进问题时很有帮助。

##### _缩进引导线_（已启用）

显示竖线以标示缩进层级。

##### _使用制表符_（已禁用）

选中后，每次按下 TAB 键都会插入一个制表符字符（`\t`）。否则，会插入与 _缩进宽度_ 设置对应数量的空格。

##### _注释样式_（斜杠）

DAX 支持使用斜杠（`//`）或连字符（`--`）的行注释。这个设置决定 Tabular Editor 3 生成 DAX 代码时用哪种注释样式。

##### _DAX 函数文档_

使用此设置指定：当光标位于某个 DAX 函数上并按下 F12 时，默认浏览器要打开的 URL。可选项包括 https://dax.guide（推荐）以及 Microsoft 的官方文档。

### DAX 设置

##### _区域设置_

设置 DAX 函数和格式所使用的区域设置。

##### _Analysis Services 版本设置_

只有当 Tabular Editor 3 无法确定所使用的 Analysis Services 版本时，这些设置才会用得上，比如直接加载 Model.bim 文件时就是这样。在这种情况下，Tabular Editor 会根据兼容级别来推测模型将部署到的版本。如果 Tabular Editor 报告的语义/语法错误不正确，你可能需要调整这些设置。

## DAX编辑器 > 自动格式化

![自动格式化设置](~/content/assets/images/auto-formatting-settings.png)

DAX编辑器 **非常** 强大，能在你输入的同时帮你写出漂亮、易读的 DAX 代码。

##### _输入时自动格式化代码_（已启用）

这个选项会在发生某些按键操作时，自动应用特定的格式规则。例如，当输入右括号时，此功能会确保括号内的内容按照本页的其他设置进行格式化。

##### _自动格式化函数调用_（已启用）

此选项专门控制：当输入右括号时，是否对函数调用（参数与括号之间的空格）进行自动格式化。

##### _自动缩进_（已启用）

这个选项会在函数调用内插入换行时，自动缩进函数参数。

##### _自动补全括号/引号_（已启用）

启用后，输入左括号或左引号时会自动补全对应的右括号或右引号。

##### _包裹选区_（已启用）

启用后，输入左括号时，会自动在当前选区外加上对应的括号。

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

##### _括号内补空格_（已启用）

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

### 大小写与引号

除了格式化 DAX 代码的空白字符外，Tabular Editor 3 还可以修正对象引用，以及函数/关键字的大小写。

##### _修正度量值/列限定符_（已启用）

选中后，会自动从度量值引用中移除表前缀，并在列引用中自动插入表前缀。

##### _首选关键字大小写_（大写）

此设置允许你更改关键字使用的大小写，例如 `ORDER BY`、`VAR`、`EVALUATE` 等。 It also governs the fixed keyword _values_ auto-complete offers for functions that take them: `ASC` and `DESC`, `KEEP`, `FIRST`, `LAST` and `DEFAULT`, the `CROSSFILTER` directions and `LOOKUP`'s `EXPLICIT` and `INFERRED`. Choose **Capitalize first letter only** to be offered `Explicit` rather than `EXPLICIT`.

##### _首选函数大小写_（大写）

此设置允许你更改函数使用的大小写，例如 `CALCULATE(...)`、`SUM(...)` 等。

##### _修正关键字/函数大小写_（已启用）

选中后，无论是自动格式化还是手动格式化代码，都会自动更正关键字和函数的大小写。

##### _修正对象引用大小写_（已启用）

DAX 是一门大小写不敏感的语言。启用后，会自动更正对表、列和度量值的引用，使其大小写与所引用对象的实际名称一致。

##### _始终为表名加引号_（已禁用）

在 DAX 中，引用某些表名时不需要用单引号括起来。不过，如果你希望表引用始终带引号，可以选中此选项。

##### _扩展列始终加前缀_（已禁用）

扩展列可以在定义时不带表名。选中后，DAX编辑器将始终为扩展列添加表前缀。

## DAX编辑器 > Code Assist

![DAX Editor Code Assist preferences](~/content/assets/images/pref-dax-code-assist.png)

在此页面上，你可以配置两项最重要的 Code Assist 功能：调用提示（也称“参数信息”）和自动完成。

##### _自动完成触发方式_

控制自动完成列表何时显示。选项包括：输入达到指定字符数后自动触发，或使用 CTRL+Space 手动触发。

##### _调用提示触发方式_

控制参数信息何时显示。选项包括在输入函数左括号时自动触发，或手动触发。

##### _增量搜索_（已启用）

在自动完成中启用模糊/增量搜索。这样你就可以通过输入名称的一部分来查找项目，而不仅限于从开头匹配。

##### _建议表名_（已启用）

在自动完成建议中包含表名。

##### _始终为表名加引号_（已禁用）

在建议中自动为表名加引号，即使并非必需。

##### _仅显示首字母_（已禁用）

只显示以所输入字母开头的项目。禁用此项即可改用增量搜索。

## DAX编辑器 > 代码操作

![DAX Editor Code Actions preferences](~/content/assets/images/pref-dax-code-actions.png)

配置自动代码改进建议：

##### _变量前缀_

定义变量名可接受的前缀（例如 `_`、`__`、`var_`、`var`、`v_`、`v`、`VAR_`）。代码操作会建议为不符合规范的变量名称添加这些前缀。

##### _列前缀_

定义临时列名可接受的前缀（例如 `@`、`_`、`x`、`x_`）。代码操作会建议为不符合规范的临时列名称添加这些前缀。

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

同意将 DAX 代码发送到外部 DAX 格式化服务 (www.daxformatter.com)。启用后，你可以使用此服务按社区标准格式化 DAX 代码。

##### _DAX formatter 请求超时_（5000）

DAX formatter 请求的超时时间，单位为毫秒。如果你在使用 DAX formatter 时经常遇到超时错误，可以把这个值调大。

## DAX优化器集成

<!-- IMAGE NEEDED: pref-dax-optimizer.png
     The DAX Optimizer Integration preferences page at its default settings.
     Alt text: "The DAX Optimizer Integration preferences page" -->

配置 DAX优化器集成（仅企业版）：

##### _自动连接_（null/提示）

在可用时自动连接到 DAX优化器。如果未设置，首次使用时会提示你。

##### _对 VPAX 文件进行混淆处理_（已启用）

发送到 DAX优化器时对模型元数据进行匿名化处理。这能保护表名、列名等敏感信息，同时仍允许进行分析。

##### _混淆字典目录_（`%LocalAppData%\TabularEditor3\DaxOptimizer`）

指定混淆字典的存储位置。该字典可在多次分析之间保持一致的混淆结果。

## VertiPaq分析器

![VertiPaq Analyzer preferences](~/content/assets/images/pref-vertipaq-analyzer.png)

##### _包含 TOM 元数据_（已启用）

在 VertiPaq分析器的统计信息中包含 Tabular Object Model 元数据。这会为你的模型结构提供更丰富的信息。

##### _从数据读取统计信息_（已启用）

通过扫描实际数据来读取统计信息（更准确，但更慢）。禁用后，将仅使用元数据。

##### _Direct Lake 提取模式_（ResidentOnly）

如何从 Direct Lake 模型中提取统计信息：

- **ResidentOnly**：仅分析当前已加载到内存中的数据
- **All**：包含未驻留的数据（更慢，可能触发数据加载）

##### _从动态管理视图读取统计信息_（已禁用）

使用 DMV 收集统计信息（更快，但准确性较低）。这是读取数据统计信息的替代方案。

##### _关系采样行数_（3）

分析关系时要采样的行数。数值越高越准确，但耗时更长。

##### _列批次大小_（50）

每批要分析的列数。可根据模型大小和性能需求进行调整。

## Power BI 集成

![Power BI Integration preferences](~/content/assets/images/pref-power-bi.png)

##### _Power BI 端点基础 URL_（`https://api.powerbi.com`）

用于 Power BI API 调用的基础 URL。如果你使用的是主权云或自定义环境，请更改此项。

##### _Fabric 端点基础 URL_（`https://api.fabric.microsoft.com`）

用于调用 Microsoft Fabric API 的基础 URL。如果你使用的是主权云或自定义环境，请更改此项。

##### _使用嵌入式浏览器进行身份验证_（已启用）

使用嵌入式浏览器进行 OAuth 身份验证，而不是系统浏览器。这将带来更紧密的集成体验。

## 代理设置

![Proxy Settings preferences](~/content/assets/images/pref-proxy-settings.png)

##### _代理类型_（无）

可在以下选项中选择：

- **无**：不配置代理
- **系统**：使用系统代理设置
- **自定义**：指定自定义代理配置

##### _代理地址_

代理服务器的地址（例如 `http://proxy.company.com:8080`）。

##### _代理用户名_

如需代理身份验证，请输入用户名。

##### _代理密码_

用于代理身份验证的密码（加密存储）。

##### _使用默认凭据_（已启用）

使用当前 Windows 凭据进行代理身份验证。其行为与 [Power BI Desktop 一致](https://docs.microsoft.com/en-us/power-bi/connect-data/desktop-troubleshooting-sign-in#using-default-system-credentials-for-web-proxy)。

##### _对本地地址绕过代理_（已启用）

对本地地址绕过代理。建议启用以提升性能。

##### _代理例外列表_

应绕过代理的地址列表（例如 `localhost;*.company.local`）。

## 后续步骤

如需查看最常调整的偏好设置的易用指南，请参阅入门指南（Personalizing TE3）[xrefid: personalizing-te3]。
