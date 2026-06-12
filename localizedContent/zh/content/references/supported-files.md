---
uid: supported-files
title: 支持的文件类型
author: Morten Lønskov
updated: 2023-10-17
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

<a name="supported-file-types"></a>

# 支持的文件类型

Tabular Editor 3 使用多种不同的文件格式和文档类型，其中一些并非 Analysis Services 或 Power BI 使用的格式。 本文将概述并逐一介绍这些文件类型。 本文将概述并逐一介绍这些文件类型。

![支持的文件类型](~/content/assets/images/file-types/te3-supported-file-types.png)

针对多种文件类型都提供了示例文件，基于 [learn.tabulareditor.com](https://tabulareditor.com/learn) 的课程 2“Business Case”。

## Dataset 文件类型

Tabular Editor 支持语义模型的四种文件类型：.bim、Power BI 文件 (.pbit 和 .pbip)、.json 和 .tmdl。 每种文件类型都有不同的功能与限制，下面将逐一说明。 每种文件类型都有不同的功能与限制，下面将逐一说明。

此外，Tabular Editor 3 的 Business 版和企业版支持通过“**保存并附带支持文件**”方式实现 Microsoft Fabric 的 Git 集成。 这会创建一个文件夹结构，在模型文件旁边包含 .platform 和 definition.pbism 元数据文件，从而支持与 Fabric Workspace 无缝同步。 详情见[保存并附带支持文件](xref:save-with-supporting-files)。

> [!NOTE]
> 由于 **Tabular Editor 3 桌面版** 仅用于作为 Power BI Desktop 的外部工具，因此该版本不允许加载和保存语义模型文件。 不过，你仍然可以使用 Tabular Editor 2.x 来实现此目的。 参阅 <xref:editions> 了解 Tabular Editor 3 各版本之间的差异。 不过，你仍然可以使用 Tabular Editor 2.x 来实现此目的。 参阅 <xref:editions> 了解 Tabular Editor 3 各版本之间的差异。

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

借助该结构，可将语义模型提交到 Git repository，并与 Fabric Workspace 同步。 完整文档见[保存并附带支持文件](xref:save-with-supporting-files)。 完整文档见[保存并附带支持文件](xref:save-with-supporting-files)。

### [Power BI](#tab/PowerBI)

Tabular Editor 可以处理两种 Power BI 存储格式：

- Power BI 模板文件（.pbit）
- Power BI Project 文件夹（.pbip）

#### Power BI Project 文件夹（.pbip） _(预览)_

Power BI Project 文件夹于 2023 年六月推出，目前在 Power BI Desktop 中以预览功能提供（也称为“开发人员模式”）。 这种存储格式是一种替代方案，用更利于版本控制以及第三方读取/编辑的形式来存储 .pbix 文件内容。 这种存储格式是一种替代方案，用更利于版本控制以及第三方读取/编辑的形式来存储 .pbix 文件内容。

> [!WARNING]
> 与 .pbix 文件一样，Power BI Project 文件夹除了 **元数据** 外，也可能包含模型 **数据**，因此应像对待 .pbix 文件一样，将该文件夹视为敏感内容并妥善保护。

Power BI Project 文件夹的根目录下有一个 .pbip 文件。 Power BI Project 文件夹的根目录下有一个 .pbip 文件。 该文件本质上是一个指向 Power BI 报表定义文件的指针，而该报表定义文件又可能进一步指向 Power BI 数据集：要么是本地的同一文件夹结构中的数据集(stored as a model.bim file)，要么是发布到 Power BI 服务的数据集(in this case, the report is said to be in _Live connect_ mode)。 如果 Power BI Project 文件夹中存在数据集(model.bim 文件)，Tabular Editor 将能够在打开 .pbip 文件时加载该模型元数据。 如果 Power BI Project 文件夹中存在数据集(model.bim 文件)，Tabular Editor 将能够在打开 .pbip 文件时加载该模型元数据。

要详细了解 Power BI Project 文件夹，请阅读微软的这篇官方博客文章：[这篇官方博客](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/)。

> [!IMPORTANT]
> 在将 Power BI 与 Tabular Editor 搭配使用时，建议使用 Power BI Project 文件，因为它支持[最广泛的建模操作](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring)。 对模型元数据进行除上述列表以外的其他更改，可能会导致 Power BI Desktop 无法加载你的模型；一旦出现这种情况，Microsoft 支持也无法为你提供帮助。 对模型元数据进行除上述列表以外的其他更改，可能会导致 Power BI Desktop 无法加载你的模型；一旦出现这种情况，Microsoft 支持也无法为你提供帮助。

#### Power BI 模板文件（.pbit）

Power BI 模板文件与 .pbix 文件类似，但区别在于它不包含任何模型 **数据**，只包含模型 **元数据**。 因此，这些模型元数据可以在 Tabular Editor 中打开并编辑。 因此，这些模型元数据可以在 Tabular Editor 中打开并编辑。

> [!WARNING]
> 尽管从技术上讲，可以从 .pbit 文件加载模型元数据并将其保存回 .pbit 文件，但这种做法不受 Power BI Desktop 支持。 Tabular Editor 默认会显示警告并阻止更改。 如果你打算通过 Tabular Editor 修改 Power BI 模型，请改用 Power BI Project 文件夹。 Tabular Editor 默认会显示警告并阻止更改。 如果你打算通过 Tabular Editor 修改 Power BI 模型，请改用 Power BI Project 文件夹。

### [表格模型文件夹（.json）](#tab/JSON)

Tabular Editor 允许你将 Dataset 对象保存为单独的 JSON 文件，这是一种自定义的序列化格式。

该格式会保留对象的结构和属性，例如表、列、度量值和关系。

这种格式从 Tabular Editor 早期起就已支持，是一种经过验证的方法，可将 Dataset 对象以单独文件的形式存储，但 Microsoft 并不支持这种做法。 从而让开发人员能够在源代码管理中跟踪更改，并协作构建语义模型。 从而让开发人员能够在源代码管理中跟踪更改，并协作构建语义模型。

在 JSON 文件结构方面，Tabular Editor 2 与 3 完全兼容。

要将语义模型保存为 JSON，首次保存时必须选择“保存到文件夹”选项。 此后，对从 JSON 结构化模型加载的模型进行后续保存时，会保留该设置。 要将语义模型保存为 JSON，首次保存时必须选择“保存到文件夹”选项。 此后，对从 JSON 结构化模型加载的模型进行后续保存时，会保留该设置。 你随时都可以通过“文件 > 另存为”把 JSON 格式的模型转换为 .bim 文件

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
    └── ……
```

在使用 Fabric Git 集成时，便于阅读的 TMDL 格式特别适合用于版本控制和代码审查。 完整文档见[保存并附带支持文件](xref:save-with-supporting-files)。 完整文档见[保存并附带支持文件](xref:save-with-supporting-files)。

***

## Fabric Git 集成文件

使用**保存并附带支持文件**功能（Business 版和企业版）时，Tabular Editor 会创建 Microsoft Fabric Git 集成所需的额外元数据文件。 这些文件由 Tabular Editor 自动生成并管理。 这些文件由 Tabular Editor 自动生成并管理。

### .platform

.platform 文件包含有关语义模型项的元数据，包括：

- **type**：将该项标识为 SemanticModel
- **displayName**：在 Fabric Workspace 中显示的名称（从 Database `Name` 属性同步）
- **description**：在 Fabric 中显示的说明（从 Database `Description` 属性同步）
- **logicalId**：自动生成的跨 Workspace 的标识符

这是一个 JSON 文件，除非你了解 Fabric 项目项的格式，否则不要手动编辑。

### definition.pbism

该 definition.pbism 文件包含语义模型的整体定义和核心设置。 此文件与模型元数据（存储为 model.bim 或位于 definition/ 文件夹中）配合使用，为 Microsoft Fabric 提供所需的完整语义模型信息。 此文件与模型元数据（存储为 model.bim 或位于 definition/ 文件夹中）配合使用，为 Microsoft Fabric 提供所需的完整语义模型信息。

在保存操作中勾选 **保存并包含支持文件** 选项后，这两个文件会自动创建。 在保存操作中勾选 **保存并包含支持文件** 选项后，这两个文件会自动创建。 生成的文件夹结构（带 .SemanticModel 后缀）可以提交到 Git repository，并与 Fabric Workspace 同步。

有关此功能的完整文档，请参阅[保存并包含支持文件](xref:save-with-supporting-files)。

## Tabular Editor 支持文件

支持文件是指 Analysis Services 或 Power BI 不会使用的文件。 相反，这些文件用于支持 Tabular Editor 3 以及其他工具中的不同开发工作流。 相反，这些文件用于支持 Tabular Editor 3 以及其他工具中的不同开发工作流。

打开并选中对应的文档或窗口后，你可以用 Ctrl+S 或“文件 > 保存”来单独保存任何辅助文件。

<a name="diagram-file-te3diag"></a>

### 关系图文件 (.te3diag)

.te3diag 文件是一种文件格式，用于存储使用 TE3 创建的模型关系图。

这些文件可用于记录模型结构与逻辑，方便参与同一项目的其他开发者查看与协作。 为了方便你访问和查阅，你可以把 .te3diag 文件保存在和模型文件同一个文件夹里。 为了方便你访问和查阅，你可以把 .te3diag 文件保存在和模型文件同一个文件夹里。

关系图文件本质上以 JSON 格式存储，并保存在 Tabular Editor 3 扩展中。

[下载示例关系图文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### DAX 查询文件（.dax 或 .msdax）

DAX 查询是可用于处理和分析语义模型中数据的表达式。 DAX 查询是可用于处理和分析语义模型中数据的表达式。 DAX 文件是包含一个或多个 DAX 查询的文本文件。

你可以在 Tabular Editor 3 中保存 DAX 文件，并在之后再次运行这些查询。 你也可以在其他支持 DAX 的工具中打开 DAX 文件，例如 [DAX Studio](https://daxstudio.org)。 你也可以在其他支持 DAX 的工具中打开 DAX 文件，例如 [DAX Studio](https://daxstudio.org)。

[下载示例 DAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### Pivot Grid 布局（.te3pivot）

这些文件包含 Tabular Editor 3 中 Pivot Grid 的布局。 这些文件包含 Tabular Editor 3 中 Pivot Grid 的布局。 它们是简单的 JSON 文件，用于指定 Pivot Grid 中显示哪些字段（度量值、列、层次结构），以及这些字段的排列方式。

只有当 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时，才能打开这些文件。

### DAX脚本（.te3daxs）

这些文件是已保存的 DAX脚本（不是查询），用来在 Tabular Editor 中一次处理多个 DAX 对象。 例如，修改语义模型中的多个度量值。 例如，修改语义模型中的多个度量值。

### C# Script（.csx）

创建和编辑 C# Script 是 Tabular Editor 最能提升效率的功能之一。

这些脚本可以保存为扩展名为 .csc 的文件，并可加载到 Tabular Editor 中，也可以保存为宏。 Tabular Editor 会维护一个 [MacroActions.json 本地设置文件](xref:supported-files#macroactionsjson)。 Tabular Editor 会维护一个 [MacroActions.json 本地设置文件](xref:supported-files#macroactionsjson)。

这样，你就能复用脚本，而不必每次都从头编写。 这样，你就能复用脚本，而不必每次都从头编写。 [脚本库](xref:csharp-script-library) 是一个很好的去处，可在此查看并复用各类脚本示例；这些示例展示了 C# 的不同特性和功能。

[下载示例 C# Script 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### VertiPaq Analyzer 文件（.vpax）

在 Tabular Editor 中，你可以通过 VertiPaq Analyzer 功能导出和导入 .vpax 文件。 .vpax 文件是一个压缩文件，包含有关语义模型大小和结构的信息，但不包含实际数据。 .vpax 文件是一个压缩文件，包含有关语义模型大小和结构的信息，但不包含实际数据。

你可以用该文件来分析并优化模型性能，同时不暴露敏感数据。 你可以用该文件来分析并优化模型性能，同时不暴露敏感数据。 例如，你可以使用 [DAX optimizer](https://www.daxoptimizer.com/) 工具，基于 .vpax 文件获取改进 DAX 公式的建议。

[下载示例 DAX脚本文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

与其他受支持的文件类型不同，创建 .vpax 文件需要在 VertiPaq Analyzer 窗口中通过“导入”和“导出”按钮完成。

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[下载示例 VPAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> 如果你的模型元数据属于机密信息，那么 .vpax 文件也应视为机密，并仅在充分考虑这一点的情况下共享。 如果你担心保护知识产权，Tabular Editor 3 提供了一个选项，可对 VPAX 文件进行混淆处理。 如果你担心保护知识产权，Tabular Editor 3 提供了一个选项，可对 VPAX 文件进行混淆处理。

#### 混淆

如果你需要将 VPAX 文件交付给第三方(例如顾问或工具供应商)，可以对文件进行混淆，以隐藏模型元数据。 做法是：在 VertiPaq Analyzer 窗口中，点击“导出”按钮旁的下拉按钮，然后选择“混淆导出...”。 做法是：在 VertiPaq Analyzer 窗口中，点击“导出”按钮旁的下拉按钮，然后选择“混淆导出...”。

混淆后的 VPAX 文件使用 .ovpax 文件扩展名。

![Export obfuscated VPAX](~/content/assets/images/obfuscated-vpax.png)

有关 VertiPaq Analyzer 的更多文档，请参阅：[sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) 和 [sqlbi Docs: Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

有关 VPAX 文件混淆的更多信息，请参阅：[VPAX Obfuscator](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## 本地设置文件

Tabular Editor 会在 "%localappdata%\\TabularEditor3" 文件夹中维护多个本地文件。 这些文件在功能上与 Tabular Editor 3 密切相关，了解它们会很有帮助。 这些文件在功能上与 Tabular Editor 3 密切相关，了解它们会很有帮助。

在团队里共享这些文件会很有用，这样所有开发者都能用到相同的宏和 BPA 规则。

> [!TIP]
> 在 Windows 上，将受版本控制的文件同步到 "%localappdata%\TabularEditor3" 文件夹的原生方法之一，是使用 [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)。
>
> 把所需文件放在 Git 或 OneDrive 里，并为“%localappdata%\TabularEditor3”文件夹创建一个符号链接。不过要注意：如果有多个用户更新同一个文件版本，最后可能会出现同步问题。
> 不过，Tabular Editor 本身并不直接支持这种方式，因此是否采用请自行斟酌。
> 不过，Tabular Editor 本身并不直接支持这种方式，因此是否采用请自行斟酌。

### MacroActions.json

此文件存储你创建或导入的所有宏。 此文件存储你创建或导入的所有宏。 你可以将此文件分享给同事，或将其备份到版本控制系统中；也可以将它配置为与包含宏的远程 repository 同步（见上方提示）。

此文件包含软件中使用的每个宏的索引。 如果你需要调整任意宏的顺序或名称，可以使用文本编辑器手动编辑此文件。 不过要注意，避免在文件中引入错误或不一致，否则可能导致文件损坏；请务必先备份。 如果你需要调整任意宏的顺序或名称，可以使用文本编辑器手动编辑此文件。 不过要注意，避免在文件中引入错误或不一致，否则可能导致文件损坏；请务必先备份。

[下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)

### BPARules.json

该文件包含 [Best Practice Analyzer 规则](xref:using-bpa)以及修复表达式。 唯一可以添加和编辑修复表达式的地方是在此 JSON 文件中。
建议把 BPA 规则文件放进版本控制系统，这样也能在部署前对语义模型运行 BPA 规则。 唯一可以添加和编辑修复表达式的地方是在此 JSON 文件中。
建议把 BPA 规则文件放进版本控制系统，这样也能在部署前对语义模型运行 BPA 规则。

你可以在此处下载微软官方的 BPA 规则：[PBA Rules](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json

包含用户曾连接过的所有服务器。 你可以考虑手动编辑它，以“忘记”那些不再相关的历史服务器。

### Layouts.json

Layouts 文件会在启动 Tabular Editor 时自动生成。 它包含 Tabular Editor 3 的 UI 布局配置所需的全部信息。 它包含 Tabular Editor 3 的 UI 布局配置所需的全部信息。

> [!TIP]
> 删除此文件将重置 Tabular Editor 的布局。 如果 Tabular Editor 的布局表现不符合预期，你可以先把这个文件备份到别的地方，删掉原文件，然后重启 Tabular Editor 3。 如果 Tabular Editor 的布局表现不符合预期，你可以先把这个文件备份到别的地方，删掉原文件，然后重启 Tabular Editor 3。
