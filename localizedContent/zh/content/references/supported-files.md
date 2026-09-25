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

Tabular Editor 3 使用多种不同的文件格式和文档类型，其中一些并非 Analysis Services 或 Power BI 使用的格式。本文将概述这些文件类型，并逐一介绍它们。

![支持的文件类型](~/content/assets/images/file-types/te3-supported-file-types.png)

针对多种文件类型都提供了示例文件，基于 [learn.tabulareditor.com](https://tabulareditor.com/learn) 的课程 2“Business Case”。

## Dataset 文件类型

Tabular Editor 支持语义模型的四种文件类型：.bim、Power BI 文件 (.pbit 和 .pbip)、.json 和 .tmdl。每种文件类型都有各自的特性和限制，下面将逐一说明。

此外，Tabular Editor 3 商业版和企业版支持在进行 Microsoft Fabric Git 集成时使用的 **连同支持文件一起保存** 功能。这会创建一个文件夹结构，在模型文件旁边生成 .platform 和 definition.pbism 元数据文件，从而实现与 Fabric Workspace 的无缝同步。有关详细信息，请参阅[连同支持文件一起保存](xref:save-with-supporting-files)。

> [!NOTE]
> 由于 **Tabular Editor 3 桌面版** 仅用于作为 Power BI Desktop 的外部工具，因此该版本不允许加载和保存语义模型文件。不过，你仍然可以使用 Tabular Editor 2.x 来实现此目的。要详细了解 Tabular Editor 3 各版本之间的差异，请参阅 <xref:editions>。

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

借助该结构，可将语义模型提交到 Git repository，并与 Fabric Workspace 同步。有关完整文档，请参阅[连同支持文件一起保存](xref:save-with-supporting-files)。

### [Power BI](#tab/PowerBI)

Tabular Editor 可以处理两种 Power BI 存储格式：

- Power BI 模板文件（.pbit）
- Power BI Project 文件夹（.pbip）

#### Power BI Project 文件夹（.pbip） _(预览)_

Power BI Project 文件夹于 2023 年六月推出，目前在 Power BI Desktop 中以预览功能提供（也称为“开发人员模式”）。这种存储格式是保存 .pbix 文件内容的另一种方式，其格式更适合进行版本控制，也更便于第三方读取和编辑内容。

> [!WARNING]
> 与 .pbix 文件一样，Power BI Project 文件夹除了 **元数据** 外，也可能包含模型 **数据**，因此应像对待 .pbix 文件一样，将该文件夹视为敏感内容并妥善保护。

Power BI Project 文件夹的根目录下有一个 .pbip 文件。该文件本质上是一个指向 Power BI 报表定义文件的指针，而该报表定义文件又可能进一步指向 Power BI 数据集：要么是本地的同一文件夹结构中的数据集(stored as a model.bim file)，要么是发布到 Power BI 服务的数据集(in this case, the report is said to be in _Live connect_ mode)。如果 Power BI Project 文件夹中包含 Dataset（model.bim 文件），Tabular Editor 在打开 .pbip 文件时即可加载该模型的元数据。

要详细了解 Power BI Project 文件夹，请阅读微软的这篇官方博客文章：[这篇官方博客](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/)。

> [!IMPORTANT]
> 在将 Power BI 与 Tabular Editor 搭配使用时，建议使用 Power BI Project 文件，因为它支持[最广泛的建模操作](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring)。对模型元数据进行上述列表之外的其他类型更改，可能会导致你的模型无法在 Power BI Desktop 中加载；在这种情况下，Microsoft 支持将无法为你提供帮助。

#### Power BI 模板文件（.pbit）

Power BI 模板文件与 .pbix 文件类似，但区别在于它不包含任何模型 **数据**，只包含模型 **元数据**。因此，可以在 Tabular Editor 中打开和编辑此模型元数据。

> [!WARNING]
> 尽管从技术上讲，可以从 .pbit 文件加载模型元数据并将其保存回 .pbit 文件，但这种做法不受 Power BI Desktop 支持。默认情况下，Tabular Editor 会显示警告并阻止更改。如果你打算通过 Tabular Editor 修改 Power BI 模型，请改用 Power BI Project 文件夹。

### [表格模型文件夹（.json）](#tab/JSON)

Tabular Editor 允许你将 Dataset 对象保存为单独的 JSON 文件，这是一种自定义的序列化格式。

该格式会保留对象的结构和属性，例如表、列、度量值和关系。

这种格式从 Tabular Editor 早期起就已支持，是一种经过验证的方法，可将 Dataset 对象以单独文件的形式存储，但 Microsoft 并不支持这种做法。从而使开发人员能够在版本控制中跟踪更改，并协作构建语义模型。

在 JSON 文件结构方面，Tabular Editor 2 与 3 完全兼容。

要将语义模型保存为 JSON，首次保存时必须使用“保存到文件夹”选项。之后对从 JSON 结构化模型加载的模型进行保存时，会沿用该设置。你随时都可以通过“文件 > 另存为”把 JSON 格式的模型转换为 .bim 文件

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

在使用 Fabric Git 集成时，便于阅读的 TMDL 格式特别适合用于版本控制和代码审查。有关完整文档，请参阅[连同支持文件一起保存](xref:save-with-supporting-files)。

***

## Fabric Git 集成文件

使用**保存并附带支持文件**功能（Business 版和企业版）时，Tabular Editor 会创建 Microsoft Fabric Git 集成所需的额外元数据文件。这些文件由 Tabular Editor 自动生成和管理。

### .platform

.platform 文件包含有关语义模型项的元数据，包括：

- **type**：将该项标识为 SemanticModel
- **displayName**：在 Fabric Workspace 中显示的名称（从 Database `Name` 属性同步）
- **description**：在 Fabric 中显示的说明（从 Database `Description` 属性同步）
- **logicalId**：自动生成的跨 Workspace 的标识符

这是一个 JSON 文件，除非你了解 Fabric 项目项的格式，否则不要手动编辑。

> [!NOTE]
> 这种同步适用于元数据包含名称或描述的模型。由 Power BI Desktop 创建的 Power BI Project (PBIP) 语义模型在其 TMDL 中既不包含名称，也不包含描述：两者只存在于 `.platform` 文件中。

### definition.pbism

该 definition.pbism 文件包含语义模型的整体定义和核心设置。这个文件会与模型元数据（存储在 model.bim 或 definition/ 文件夹中）一起使用，提供 Microsoft Fabric 所需的完整语义模型信息。

在保存时勾选 **Save with supporting files** 选项后，这两个文件会自动创建。生成的文件夹结构（带 .SemanticModel 后缀）可以提交到 Git repository，并与 Fabric Workspace 同步。

有关此功能的完整文档，请参阅[保存并包含支持文件](xref:save-with-supporting-files)。

## Tabular Editor 支持文件

支持文件是指 Analysis Services 或 Power BI 不会使用的文件。这些文件则用于支持 Tabular Editor 3 和其他工具中的不同开发工作流。

打开并选中对应的文档或窗口后，你可以用 Ctrl+S 或“文件 > 保存”来单独保存任何辅助文件。

### 用户选项（.tmuo）

`.tmuo` 文件存储针对某个模型的、仅在本机生效的个人设置，包括：Workspace 数据库、数据源凭据覆盖、表导入设置、刷新覆盖项以及 AI 权限授予。这个文件和模型放在同一位置，并以模型名称和你的 Windows 用户名命名，这样多个开发者就能在不互相干扰的情况下处理同一个模型。

里面的凭据会使用你的 Windows 用户密钥加密，所以这个文件实际上没法共享使用。将 `*.tmuo` 添加到 `.gitignore`。

有关完整内容以及每种模型格式下这个文件的写入位置，见 @user-options。

### 关系图文件 (.te3diag)

.te3diag 文件是一种文件格式，用于存储使用 TE3 创建的模型关系图。

这些文件可用于记录模型结构与逻辑，方便参与同一项目的其他开发者查看与协作。可以将 .te3diag 文件保存在与模型文件相同的文件夹中，便于访问和查阅。

关系图文件本质上以 JSON 格式存储，并保存在 Tabular Editor 3 扩展中。

[下载示例关系图文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### DAX 查询文件（.dax 或 .msdax）

DAX 查询是一类表达式，可用于操作和分析语义模型中的数据。 DAX 文件是包含一个或多个 DAX 查询的文本文件。

你可以在 Tabular Editor 3 中保存 DAX 文件，并在之后再次运行这些查询。你也可以在其他支持 DAX 的工具中打开 DAX 文件，例如 [DAX Studio](https://daxstudio.org)。

[下载示例 DAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### Pivot Grid 布局（.te3pivot）

这些文件包含 Tabular Editor 3 中 Pivot Grid 的布局。它们是简单的 JSON 文件，用于指定 Pivot Grid 中显示哪些字段（度量值、列、层次结构），以及这些字段的排列方式。

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### DAX脚本（.te3daxs）

这些文件是已保存的 DAX脚本（不是查询），用来在 Tabular Editor 中一次处理多个 DAX 对象。例如，修改语义模型中的多个度量值。

### C# Script（.csx）

创建和编辑 C# Script 是 Tabular Editor 最能提升效率的功能之一。

这些脚本可以保存为扩展名为 .csc 的文件，并可加载到 Tabular Editor 中，也可以保存为宏。 Tabular Editor 会维护一个用于存储宏的 [MacroActions.json 本地设置文件](xref:supported-files#macroactionsjson)。

这样，脚本就可以重复使用，而不必每次都从头编写。[脚本库](xref:csharp-script-library) 是一个很好的去处，可在此查看并复用各类脚本示例；这些示例展示了 C# 的不同特性和功能。

[下载示例 C# Script 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### VertiPaq Analyzer 文件（.vpax）

在 Tabular Editor 中，你可以通过 VertiPaq Analyzer 功能导出和导入 .vpax 文件。 .vpax 文件是一种压缩文件，包含有关你的语义模型大小和结构的信息，但不包含实际数据。

你可以用这个文件分析并优化模型性能，而不会暴露敏感数据。例如，你可以使用 [DAX optimizer](https://www.daxoptimizer.com/) 工具，基于 .vpax 文件获取改进 DAX 公式的建议。

[下载示例 DAX脚本文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

与其他受支持的文件类型不同，创建 .vpax 文件需要在 VertiPaq Analyzer 窗口中通过“导入”和“导出”按钮完成。

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[下载示例 VPAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> 如果你的模型元数据属于机密信息，那么 .vpax 文件也应视为机密，并仅在充分考虑这一点的情况下共享。如果你担心知识产权泄露，Tabular Editor 3 提供了一个用于混淆 VPAX 文件的选项。

#### 混淆

如果你需要将 VPAX 文件交付给第三方(例如顾问或工具供应商)，可以对文件进行混淆，以隐藏模型元数据。具体做法是：在 Vertipaq Analyzer 窗口中，点击“导出”按钮旁边的下拉按钮，然后选择“混淆导出...”选项。

混淆后的 VPAX 文件使用 .ovpax 文件扩展名。

![导出已混淆的 VPAX](~/content/assets/images/obfuscated-vpax.png)

有关 VertiPaq Analyzer 的更多文档，请参阅：[sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) 和 [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

有关 VPAX 文件混淆的更多信息，请参阅：[VPAX Obfuscator](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## 本地设置文件

Tabular Editor 会在 "%localappdata%\\TabularEditor3" 文件夹中维护多个本地文件。这些文件与 Tabular Editor 3 的功能相关，值得了解。

在团队里共享这些文件会很有用，这样所有开发者都能用到相同的宏和 BPA 规则。

> [!TIP]
> 在 Windows 上，将受版本控制的文件同步到 "%localappdata%\TabularEditor3" 文件夹的原生方法之一，是使用 [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)。
>
> 把所需文件放在 Git 或 OneDrive 里，并为“%localappdata%\TabularEditor3”文件夹创建一个符号链接。不过要注意：如果有多个用户更新同一个文件版本，最后可能会出现同步问题。不过，Tabular Editor 不直接支持这一点，所以要不要这样做请你自行斟酌。

### AI 审计日志

仅在安装了 AI 功能组件时显示。 Tabular Editor 会记录 [AI 助手](xref:ai-assistant) 和 [MCP 服务器](xref:mcp-server) 执行过的操作：请求了哪些权限以及如何回应；运行了哪些工具，以及每个工具是成功、失败还是被拒绝；以及任何已运行或提交供审核的 C# Script 的完整文本。绝不会记录提示词、回复或你模型中的数据值。

文件按天生成，每天一个，默认保留 30 天。在 **工具 > 偏好 > AI 功能** 下点击 **打开审计文件夹**，即可打开该文件夹。管理员可以通过 [策略](xref:policies) 移动该文件夹并更改保留期限。有关每条记录包含的内容，请参阅 @ai-audit-log。

与此文件夹中的其他文件不同，这个文件保存的是记录，而不是设置。不要共享或同步它：这是每台计算机各自的日志，其中包含的脚本可能会暴露你处理过的模型结构。

### MacroActions.json

此文件存储你创建或导入的所有宏。你可以将此文件分享给同事，或将其备份到版本控制系统中；也可以将它配置为与包含宏的远程 repository 同步（见上方提示）。

此文件包含软件中使用的每个宏的索引。如果需要更改某个宏的顺序或名称，可以使用文本编辑器手动编辑此文件。不过务必小心，避免在文件中引入错误或不一致而导致文件损坏；编辑前请先创建备份。

[下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)

### BPARules.json

该文件包含 [Best Practice Analyzer 规则](xref:using-bpa)以及修复表达式。添加和编辑修复表达式的唯一位置就是这个 JSON 文件。建议将 BPA 规则文件纳入版本控制，这样也可以在部署前对语义模型运行 BPA 规则。

你可以在此处下载微软官方的 BPA 规则：[PBA Rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json

包含用户连接过的所有服务器。有时可以手动编辑它，让它“忘记”那些不再相关的旧服务器。

### Layouts.json

Layouts 文件会在启动 Tabular Editor 时自动生成。其中包含 Tabular Editor 3 的 UI 布局配置方式的全部信息。

> [!TIP]
> 删除此文件将重置 Tabular Editor 的布局。如果 Tabular Editor 的布局表现不符合预期，一个不错的第一步是先将此文件备份到别处，删除原文件，然后重启 Tabular Editor 3。
