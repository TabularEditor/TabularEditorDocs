---
uid: supported-files
title: 支持的文件类型
author: Morten Lønskov
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "桌面版不支持模型元数据文件"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 支持的文件类型

Tabular Editor 3 使用多种不同的文件格式和文档类型，其中一些并非 Analysis Services 或 Power BI 使用的格式。 This article provides an overview and a description of each of these file types.

![支持的文件类型](~/content/assets/images/file-types/te3-supported-file-types.png)

针对多种文件类型都提供了示例文件，基于 [learn.tabulareditor.com](https://tabulareditor.com/learn) 的课程 2“Business Case”。

## Dataset 文件类型

Tabular Editor 支持语义模型的四种文件类型：.bim、Power BI 文件 (.pbit 和 .pbip)、.json 和 .tmdl。 Each file type has different features and limitations, which are explained below.

Additionally, Tabular Editor 3 Business and Enterprise editions support **saving with supporting files** for Microsoft Fabric Git integration. This creates a folder structure containing .platform and definition.pbism metadata files alongside your model files, enabling seamless synchronization with Fabric workspaces. See [Save with supporting files](xref:save-with-supporting-files) for details.

> [!NOTE]
> 由于 **Tabular Editor 3 桌面版** 仅用于作为 Power BI Desktop 的外部工具，因此该版本不允许加载和保存语义模型文件。 You may however still use Tabular Editor 2.x for this purpose. See <xref:editions> to learn more about the difference between the Tabular Editor 3 editions.

### [表格模型文件 (.bim)](#tab/BIM)

.bim 文件是一个由嵌套 JSON 组成的单一文件，这种格式称为 TMSL。

这是 Microsoft 支持的语义模型的原始格式。

但它有一个明显缺点：由于它是一个单一的大文件，难以跟踪变更，也不利于采用 Git 源代码管理等良好的团队开发实践。

#### 文件夹中的.bim 文件

![支持的 BIM 文件类型](~/content/assets/images/file-types/te3-supported-file-bim.png)

[下载示例 .bim 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/bim-file-example.bim)

#### Fabric Git 集成：保存并附带支持文件

使用“**保存并附带支持文件**”选项（Business 和企业版）时，Tabular Editor 会创建与 Microsoft Fabric Git 集成兼容的文件夹结构：

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── model.bim
```

借助该结构，可将语义模型提交到 Git repository，并与 Fabric Workspace 同步。 See [Save with supporting files](xref:save-with-supporting-files) for complete documentation.

### [Power BI](#tab/PowerBI)

Tabular Editor 可以处理两种 Power BI 存储格式：

- Power BI 模板文件（.pbit）
- Power BI Project 文件夹（.pbip）

#### Power BI Project 文件夹（.pbip） _(预览)_

Power BI Project 文件夹于 2023 年六月推出，目前在 Power BI Desktop 中以预览功能提供（也称为“开发人员模式”）。 The storage format is an alternative way to store the contents of a .pbix file, in a format that is more friendly to version control and 3rd party reading/editing of the content.

> [!WARNING]
> 与 .pbix 文件一样，Power BI Project 文件夹除了 **元数据** 外，也可能包含模型 **数据**，因此应像对待 .pbix 文件一样，将该文件夹视为敏感内容并妥善保护。

At the root of the Power BI Project folders sits a .pbip file. 该文件本质上是一个指向 Power BI 报表定义文件的指针，而该报表定义文件又可能进一步指向 Power BI 数据集：要么是本地的同一文件夹结构中的数据集(stored as a model.bim file)，要么是发布到 Power BI 服务的数据集(in this case, the report is said to be in _Live connect_ mode)。 If a dataset (model.bim file) is present in the Power BI Project folder, Tabular Editor will be able to load this model metadata when opening the .pbip file.

要详细了解 Power BI Project 文件夹，请阅读微软的这篇官方博客文章：[这篇官方博客](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/)。

> [!IMPORTANT]
> 在将 Power BI 与 Tabular Editor 搭配使用时，建议使用 Power BI Project 文件，因为它支持[最广泛的建模操作](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring)。 Making other types of changes to the model metadata than those listed, may cause your model to become unloadable in Power BI Desktop, and in this case, Microsoft Support will not be able to help you.

#### Power BI 模板文件（.pbit）

Power BI 模板文件与 .pbix 文件类似，但区别在于它不包含任何模型 **数据**，只包含模型 **元数据**。 As such, this model metadata can be opened and edited in Tabular Editor.

> [!WARNING]
> 尽管从技术上讲，可以从 .pbit 文件加载模型元数据并将其保存回 .pbit 文件，但这种做法不受 Power BI Desktop 支持。 Tabular Editor will show a warning and block changes by default. Use Power BI Project folders instead, if you intend to make changes to your Power BI model through Tabular Editor.

### [表格模型文件夹（.json）](#tab/JSON)

Tabular Editor 允许你将 Dataset 对象保存为单独的 JSON 文件，这是一种自定义的序列化格式。

该格式会保留对象的结构和属性，例如表、列、度量值和关系。

这种格式从 Tabular Editor 早期起就已支持，是一种经过验证的方法，可将 Dataset 对象以单独文件的形式存储，但 Microsoft 并不支持这种做法。 Thereby enabling developers to track changes in source control and collaborate on building semantic models.

在 JSON 文件结构方面，Tabular Editor 2 与 3 完全兼容。

In order to save a semantic model to JSON you must use the 'Save to Folder' option when saving the first time. Subsequent saves to a model loaded from a JSON structured model maintains the setting. 你随时都可以通过“文件 > 另存为”把 JSON 格式的模型转换为 .bim 文件

![支持的文件类型：JSON](~/content/assets/images/file-types/te3-supported-file-json.png)

1. 整个模型包含一个 database.json 文件，并且每个 TOM 顶层对象都有自己的文件夹
2. 在 tables 目录中，每个表都有自己的文件夹
3. 单个表会保存为 TableName.json 文件，并包含用于度量值、列和分区的文件夹
4. 表中的每个度量值都有自己的 json 文件。

会创建到哪一层级的 json 对象由序列化设置控制。

一个度量值的单个 JSON 文件包含该度量值的所有属性：

![支持的文件类型：JSON 度量值文件](~/content/assets/images/file-types/te3-supported-file-json-measure.png)

想了解“保存到文件夹”和序列化设置的更多信息，可以查看：[保存到文件夹](xref:save-to-folder)

[下载 JSON 文件夹结构示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/json-model-example.zip)

### [TMDL](#tab/TMDL)

TMDL 是 Tabular Model Definition Language 的缩写，是一种新格式，使用类似 YAML 的语法，以更易读的方式定义和管理 Dataset。

Microsoft 于 2023 年四月将 TMDL 作为预览功能推出，旨在提供一种统一且一致的方式，以便跨不同平台和工具处理 Dataset。

TMDL 的设计目标是支持 Dataset 的源代码管理，让用户能够跟踪更改、协作，并围绕语义模型自动化工作流。

> [!Note]
> TMDL 目前处于预览阶段，这意味着它尚未完全稳定，可能会存在一些限制或问题。

![支持的文件类型：TMDL](~/content/assets/images/file-types/te3-supported-file-tmdl.png)

1. 整体序列化位于 TOM 的顶层对象级别
2. 每个表都是一个单独的文件
3. TMDL 文件由类似 YAML 的缩进结构构成，文件中包含各列和度量值。

想继续了解的话，可以看看：[TMDL](xref:tmdl)

[下载 TMDL 文件夹结构示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/tmdl-model-example.zip)

#### Fabric Git 集成：保存并附带支持文件

使用“**保存并附带支持文件**”选项（Business 和企业版）时，Tabular Editor 会创建与 Microsoft Fabric Git 集成兼容的文件夹结构：

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── definition/
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

在使用 Fabric Git 集成时，便于阅读的 TMDL 格式特别适合用于版本控制和代码审查。 See [Save with supporting files](xref:save-with-supporting-files) for complete documentation.

***

## Fabric Git 集成文件

使用**保存并附带支持文件**功能（Business 版和企业版）时，Tabular Editor 会创建 Microsoft Fabric Git 集成所需的额外元数据文件。 These files are automatically generated and managed by Tabular Editor.

### .platform

.platform 文件包含有关语义模型项的元数据，包括：

- **type**：将该项标识为 SemanticModel
- **displayName**：在 Fabric Workspace 中显示的名称（从 Database `Name` 属性同步）
- **description**：在 Fabric 中显示的说明（从 Database `Description` 属性同步）
- **logicalId**：自动生成的跨 Workspace 的标识符

这是一个 JSON 文件，除非你了解 Fabric 项目项的格式，否则不要手动编辑。

> [!NOTE]
> This synchronization applies to a model whose metadata carries a name or a description. A Power BI Project (PBIP) semantic model authored by Power BI Desktop carries neither in its TMDL: both live only in the `.platform` file.

### definition.pbism

该 definition.pbism 文件包含语义模型的整体定义和核心设置。 This file works alongside the model metadata (stored as either model.bim or in the definition/ folder) to provide complete semantic model information required by Microsoft Fabric.

Both files are automatically created when you check the **Save with supporting files** option during save operations. 生成的文件夹结构（带 .SemanticModel 后缀）可以提交到 Git repository，并与 Fabric Workspace 同步。

有关此功能的完整文档，请参阅[保存并包含支持文件](xref:save-with-supporting-files)。

## Tabular Editor 支持文件

支持文件是指 Analysis Services 或 Power BI 不会使用的文件。 Instead, these files all support different kinds of development workflow in Tabular Editor 3 and other tools.

打开并选中对应的文档或窗口后，你可以用 Ctrl+S 或“文件 > 保存”来单独保存任何辅助文件。

### User Options (.tmuo)

A `.tmuo` file holds your own, machine-local settings for one model: the workspace database, data source credential overrides, table import settings, refresh overrides and AI permission grants. It sits next to the model and is named after it and your Windows user name, so several developers can work on the same model without treading on one another.

Credentials inside it are encrypted with your Windows user key, which means the file cannot usefully be shared. Add `*.tmuo` to `.gitignore`.

See @user-options for the full contents and where the file is written for each model format.

### 关系图文件 (.te3diag)

.te3diag 文件是一种文件格式，用于存储使用 TE3 创建的模型关系图。

这些文件可用于记录模型结构与逻辑，方便参与同一项目的其他开发者查看与协作。 A .te3diag file can be saved in the same folder as the model file for easy access and reference.

关系图文件本质上以 JSON 格式存储，并保存在 Tabular Editor 3 扩展中。

[下载示例关系图文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### DAX 查询文件（.dax 或 .msdax）

DAX queries are expressions that can be used to manipulate and analyze data in semantic models. DAX 文件是包含一个或多个 DAX 查询的文本文件。

你可以在 Tabular Editor 3 中保存 DAX 文件，并在之后再次运行这些查询。 You can also open a DAX file in other tools that support DAX, such as [DAX Studio](https://daxstudio.org).

[下载示例 DAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### Pivot Grid 布局（.te3pivot）

These files contain the layout of a Pivot Grid in Tabular Editor 3. 它们是简单的 JSON 文件，用于指定 Pivot Grid 中显示哪些字段（度量值、列、层次结构），以及这些字段的排列方式。

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### DAX脚本（.te3daxs）

这些文件是已保存的 DAX脚本（不是查询），用来在 Tabular Editor 中一次处理多个 DAX 对象。 For example, modifying multiple measures in a semantic model.

### C# Script（.csx）

创建和编辑 C# Script 是 Tabular Editor 最能提升效率的功能之一。

这些脚本可以保存为扩展名为 .csc 的文件，并可加载到 Tabular Editor 中，也可以保存为宏。 A [MacroActions.json local setting file](xref:supported-files#macroactionsjson) is maintained by Tabular Editor.

This way, scripts can be reused without having to write them from scratch every time. [脚本库](xref:csharp-script-library) 是一个很好的去处，可在此查看并复用各类脚本示例；这些示例展示了 C# 的不同特性和功能。

[下载示例 C# Script 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### VertiPaq Analyzer 文件（.vpax）

在 Tabular Editor 中，你可以通过 VertiPaq Analyzer 功能导出和导入 .vpax 文件。 A .vpax file is a compressed file that contains information about the size and structure of your semantic model, but not the actual data.

You can use this file to analyze and optimize your model performance, without exposing sensitive data. 例如，你可以使用 [DAX optimizer](https://www.daxoptimizer.com/) 工具，基于 .vpax 文件获取改进 DAX 公式的建议。

[下载示例 DAX脚本文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

与其他受支持的文件类型不同，创建 .vpax 文件需要在 VertiPaq Analyzer 窗口中通过“导入”和“导出”按钮完成。

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[下载示例 VPAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> 如果你的模型元数据属于机密信息，那么 .vpax 文件也应视为机密，并仅在充分考虑这一点的情况下共享。 If you are concerned about protecting IP, Tabular Editor 3 has an option to obfuscate VPAX files.

#### Obfuscation

如果你需要将 VPAX 文件交付给第三方(例如顾问或工具供应商)，可以对文件进行混淆，以隐藏模型元数据。 This is done by selecting the 'Obfuscated Export...' option under the drop-down button next to the 'Export' button in the Vertipaq Analyzer window.

混淆后的 VPAX 文件使用 .ovpax 文件扩展名。

![Export obfuscated VPAX](~/content/assets/images/obfuscated-vpax.png)

有关 VertiPaq Analyzer 的更多文档，请参阅：[sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) 和 [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

有关 VPAX 文件混淆的更多信息，请参阅：[VPAX Obfuscator](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## 本地设置文件

Tabular Editor 会在 "%localappdata%\\TabularEditor3" 文件夹中维护多个本地文件。 These files are functionally relevant for Tabular Editor 3 and are useful to know.

在团队里共享这些文件会很有用，这样所有开发者都能用到相同的宏和 BPA 规则。

> [!TIP]
> 在 Windows 上，将受版本控制的文件同步到 "%localappdata%\TabularEditor3" 文件夹的原生方法之一，是使用 [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)。
>
> 把所需文件放在 Git 或 OneDrive 里，并为“%localappdata%\TabularEditor3”文件夹创建一个符号链接。不过要注意：如果有多个用户更新同一个文件版本，最后可能会出现同步问题。
> However, this is not supported by Tabular Editor directly, so implement it at your own discretion.

### AI audit log

Present only when the AI features component is installed. Tabular Editor writes a record of what the [AI Assistant](xref:ai-assistant) and the [MCP server](xref:mcp-server) did: which permissions were asked for and how they were answered, which tools ran and whether each one succeeded, failed or was refused, and the full text of any C# script that was run or handed over for review. Prompts, replies and data values from your model are never recorded.

Files are written one per day and kept for 30 days by default. Reach the folder with **Open audit folder** under **Tools > Preferences > AI Features**. Administrators can move it and change the retention period by [policy](xref:policies). See @ai-audit-log for what each record holds.

Unlike the other files in this folder, this one is a record rather than a setting. Do not share or sync it: it is a per-machine log, and the scripts it contains may reveal the structure of models you have worked on.

### MacroActions.json

This file stores all the macros that you have created or imported. 你可以将此文件分享给同事，或将其备份到版本控制系统中；也可以将它配置为与包含宏的远程 repository 同步（见上方提示）。

此文件包含软件中使用的每个宏的索引。 If you need to change the order or the name of any macro, you can edit this file manually with a text editor. However, be careful not to introduce any errors or inconsistencies in the file thereby corrupting so make sure to create a backup.

[下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)

### BPARules.json

该文件包含 [Best Practice Analyzer 规则](xref:using-bpa)以及修复表达式。 The only place to add and edit  fix expressions is inside this JSON file.
It is recommended to store the PBA rule file in version control, which also enables the possibility of running the BPA rules against the semantic model before deployment.

你可以在此处下载微软官方的 BPA 规则：[PBA Rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json

Contains all the servers a user has been connected to. It can be advisable to edit it manually to 'forget' past servers no longer relevant.

### Layouts.json

Layouts 文件会在启动 Tabular Editor 时自动生成。 It contains all information to how Tabular Editor 3's UI layout is configured.

> [!TIP]
> 删除此文件将重置 Tabular Editor 的布局。 If the Tabular Editor layout does not behave as expected a good first step is to backup this file somewhere else, delete the original and restart Tabular Editor 3.
