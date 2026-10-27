---
uid: supported-files
title: 支持的文件类型
author: Morten Lønskov
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          partial: true
          note: "Desktop Edition does not support model metadata files"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# 支持的文件类型

Tabular Editor 3 使用多种不同的文件格式和文档类型，其中一些文件格式和文档类型并非 Analysis Services 或 Power BI 所使用。本文概述并介绍了每种文件类型。

![支持的文件类型](~/content/assets/images/file-types/te3-supported-file-types.png)

根据 [learn.tabulareditor.com](https://tabulareditor.com/learn) 课程 2 业务案例，每种文件类型均提供示例文件。

## 数据集文件类型

Tabular Editor 支持四种语义模型文件类型：.bim、Power BI 文件（.pbit 和 .pbip）、.json 和 .tmdl。每种文件类型都有不同的功能和限制，具体说明如下。

此外，Tabular Editor 3 Business 和 Enterprise 版本支持**保存时包含支持文件**，以实现 Microsoft Fabric Git 集成。这将创建一个文件夹结构，其中包含 .platform 和 definition.pbism 元数据文件以及您的模型文件，从而实现与 Fabric 工作区的无缝同步。请参阅[保存时包含支持文件](xref:save-with-supporting-files)了解详情。

> [!NOTE]
> 由于 **Tabular Editor 3 Desktop 版本**仅用于作为 Power BI Desktop 的外部工具，因此此版本不允许加载和保存语义模型文件。但是，您仍可为此目的使用 Tabular Editor 2.x。请参阅<xref:editions>，详细了解 Tabular Editor 3 各版本之间的差异。

### [表格模型文件 (.bim)](#tab/BIM)
.bim 文件是一个由嵌套 JSON 组成的单个文件，称为 TMSL。 

这是 Microsoft 支持的语义模型的原始格式。 

但是，它有一个很大的缺点：由于它是一个大型的单个文件，因此难以跟踪更改，也难以使用 Git 源代码管理等良好的团队开发实践。

**文件夹中的 .bim 文件**

![支持的文件类型 BIM](~/content/assets/images/file-types/te3-supported-file-bim.png)

[下载 .bim 示例文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/bim-file-example.bim)

**保存时包含用于 Fabric Git 集成的支持文件**

使用**保存时包含支持文件**选项（Business 和 Enterprise 版本）时，Tabular Editor 会创建与 Microsoft Fabric Git 集成兼容的文件夹结构：

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── model.bim
```

此结构使您能够将语义模型提交到 Git 仓库，并将其与 Fabric 工作区同步。请参阅[保存时包含支持文件](xref:save-with-supporting-files)，以获取完整文档。


### [Power BI](#tab/PowerBI)

Tabular Editor 可以处理两种类型的 Power BI 存储格式：

- Power BI 模板文件（.pbit）
- Power BI Project 文件夹（.pbip）



**Power BI Project 文件夹 (.pbip)（预览）**

Power BI Project 文件夹于 2023 年 6 月推出，在 Power BI Desktop 中作为预览功能（也称为“开发者模式”）提供。该存储格式是存储 .pbix 文件内容的另一种方式，其格式对于版本控制以及第三方读取/编辑内容更加友好。

> [!WARNING]
> 与 .pbix 文件一样，Power BI Project 文件夹除了包含**元数据**外，还可能包含模型**数据**，因此应像对待 .pbix 文件一样将该文件夹视为敏感文件。

Power BI Project 文件夹的根目录中有一个 .pbip 文件。该文件本质上是指向 Power BI 报表定义文件的指针，该文件随后又可能指向 Power BI 数据集，该数据集可能位于本地的相同文件夹结构中（存储为 model.bim 文件），也可能是发布到 Power BI 服务的
数据集（在这种情况下，该报表被认为是处于*实时连接*模式）。如果 Power BI Project 文件夹中存在数据集（model.bim 文件），则 Tabular Editor 将能够在打开 .pbip 文件时加载此模型元数据。

要了解有关 Power BI Project 文件夹的更多信息，请阅读[Microsoft 的这篇官方博客文章](https://powerbi.microsoft.com/en-us/blog/deep-dive-into-power-bi-desktop-developer-mode-preview/)。

> [!IMPORTANT]
> 在将 Power BI 与 Tabular Editor 一起使用时，Power BI Project 文件是推荐的格式，因为它支持[最广泛的建模操作](https://learn.microsoft.com/power-bi/developer/projects/projects-overview#model-authoring)。对模型元数据进行所列类型以外的其他类型的更改，可能会导致您的模型在 Power BI Desktop 中无法加载，在这种情况下，Microsoft 支持将无法为您提供帮助。

**Power BI模板文件（.pbit）**

Power BI模板文件与.pbix文件类似，但不同之处在于它们不包含任何模型**数据**，只包含模型**元数据**。因此，可以在 Tabular Editor 中打开和编辑此模型元数据。

> [!WARNING]
> 虽然从技术上来说，可以从 .pbit 文件加载模型元数据并将其保存到 .pbit 文件，但 Power BI Desktop 不支持此方法。默认情况下，Tabular Editor 将显示警告并阻止更改。如果您打算通过 Tabular Editor 对 Power BI 模型进行更改，请改用 Power BI Project 文件夹。

### [表格模型文件夹 (.json)](#tab/JSON)

Tabular Editor 允许您将数据集对象保存为单独的 JSON 文件，这是一种自定义序列化格式。 

此格式保留了您的对象（例如表、列、度量值和关系）的结构和属性。

Tabular Editor 从早期开始就支持此格式，这是一种经过验证的方法，可将您的数据集对象存储为单个文件，但 Microsoft 不支持此方法。从而使开发人员能够跟踪源代码控制中的更改，并协作构建语义模型。

在 JSON 文件结构方面，Tabular Editor 2 和 3 之间完全兼容。

要将语义模型保存为 JSON，您必须在首次保存时使用“保存到文件夹”选项。随后将模型保存为从 JSON 结构化模型加载的模型时，将保留该设置。始终可以使用“文件 > 另存为”将 JSON 格式的模型转换为 .bim 文件。


![支持的文件类型 JSON](~/content/assets/images/file-types/te3-supported-file-json.png)

1. 整体模型具有一个数据库 JSON，每个 TOM 标题都有自己的文件夹
2. 在表格中，每个表格都存在于其各自的文件夹中
3. 单个表作为 TableName json 文件，其中包含度量值、列和分区的文件夹
4. 表格上的每个度量值都有自己的 json 文件。

将要创建的 JSON 对象的深度由序列化设置处理。 

一个度量值的单个 JSON 文件包含该度量的所有属性：
 
![支持的文件类型 JSON 文件](~/content/assets/images/file-types/te3-supported-file-json-measure.png)


有关“保存到文件夹”和序列化设置的更多信息，请参阅：[保存到文件夹](xref:save-to-folder)

[下载 JSON 文件夹结构示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/json-model-example.zip)

### [TMDL](#tab/TMDL)

TMDL 代表表格模型定义语言，它是一种新格式，用于使用类似 YAML 的语法以人类可读的格式定义和管理数据集。 

Microsoft 于 2023 年 4 月推出了 TMDL 预览功能，旨在提供一种统一且一致的方式，以便在不同平台和工具上处理数据集。 

TMDL 旨在支持数据集源代码管理，使用户能够使用语义模型跟踪更改、进行协作并自动化工作流。 
> [!NOTE]
> TMDL 处于预览阶段，这意味着它并不完全稳定，可能存在一些限制或问题。 

![支持的文件类型 TMDL](~/content/assets/images/file-types/te3-supported-file-tmdl.png)

1. 整体序列化位于 TOM 的顶层对象级别
2. 每个表都是一个单独的文件
3. TMDL 文件由类似 YAML 的缩进组成，其中包含文件内的每一列和度量值。

如需进一步阅读，请参阅：[TMDL](xref:tmdl)

[下载 TMDL 文件夹结构示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/tmdl-model-example.zip)

**保存时包含用于 Fabric Git 集成的支持文件**

使用**保存时包含支持文件**选项（Business 和 Enterprise 版本）时，Tabular Editor 会创建与 Microsoft Fabric Git 集成兼容的文件夹结构：

```
DatabaseName.SemanticModel/
├── .platform
├── definition.pbism
└── definition/
    ├── database.tmdl
    ├── tables.tmdl
    └── ...
```

在使用 Fabric Git 集成时，人类可读的 TMDL 格式特别适合版本控制和代码评审。请参阅[保存时包含支持文件](xref:save-with-supporting-files)，了解完整文档。

***

## Fabric Git 集成文件

使用**保存时包含支持文件**功能（Business 和 Enterprise 版本）时，Tabular Editor 会创建 Microsoft Fabric Git 集成所需的其他元数据文件。这些文件由 Tabular Editor 自动生成和管理。

### .platform

.platform 文件包含有关语义模型项的元数据，包括：
- **type**：将项目标识为 SemanticModel
- **displayName**：在 Fabric 工作区中显示的名称（从数据库的 `Name` 属性同步）
- **description**：在 Fabric 中显示的说明（从数据库的 `Description` 属性同步）
- **logicalId**：自动生成的跨工作区标识符

此文件是 JSON 文件，除非您了解 Fabric 项目格式，否则不应手动编辑。

> [!NOTE]
> 此同步适用于元数据带有名称或描述的模型。由 Power BI Desktop 创建的 Power BI Project (PBIP) 语义模型在其 TMDL 中不包含名称或描述：两者仅存在于 `.platform` 文件中。

### definition.pbism

definition.pbism 文件包含语义模型的整体定义和核心设置。此文件与模型元数据（以 model.bim 或在 definition/ 文件夹中存储）配合使用，以提供 Microsoft Fabric 所需的完整语义模型信息。

在保存操作期间选中**保存时包含支持文件**选项时，这两个文件都会自动创建。生成的文件夹结构（带有 .SemanticModel 后缀）可以提交到 Git 存储库并与 Fabric 工作区同步。

有关此功能的完整文档，请参阅[保存时包含支持文件](xref:save-with-supporting-files)。

## Tabular Editor 支持文件

支持文件是指 Analysis Services 或 Power BI 不使用的文件。相反，这些文件都支持 Tabular Editor 3 和其他工具中的各种开发工作流。

在相应文档或窗口打开并处于焦点状态时，可以使用 Ctrl+S 或“文件 > 保存”分别保存所有支持文件。 

### 用户选项 (.tmuo)

`.tmuo`文件包含您自己针对一个模型的计算机本地设置：工作区数据库、数据源凭据覆盖、表导入设置、刷新覆盖和 AI 权限授予。它位于模型旁边，并以模型和您的Windows用户名命名，因此多名开发人员可以处理同一模型，而不会相互干扰。

其中的凭据使用您的 Windows 用户密钥进行加密，这意味着该文件无法有意义地共享。将 `*.tmuo` 添加到 `.gitignore`。

请参阅 @user-options，了解完整内容以及针对每种模型格式写入该文件的位置。

### 图表文件 (.te3diag)

.te3diag 文件是一种文件格式，用于存储使用 TE3 创建的模型的图表。 

这些文件对于为从事同一项目的其他开发人员记录模型结构和逻辑非常有用。.te3diag 文件可以与模型文件保存在同一文件夹中，以便于访问和参考。

关系图文件实际上是存储在 Tabular Editor 3 扩展中的 JSON。

[下载图表文件示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/te3-diagram.te3diag)

### DAX 查询文件（.dax 或 .msdax）

DAX 查询是可用于操作和分析语义模型中数据的表达式。DAX 文件是一个包含一个或多个 DAX 查询的文本文件。 

您可以在 Tabular Editor 3 中保存 DAX 文件，稍后使用该文件再次运行查询。您还可以在其他支持 DAX 的工具（例如 [DAX Studio](https://daxstudio.org)）中打开 DAX 文件。

[下载示例 DAX 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-query-example.dax)

这些文件只能在 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时打开。

### Pivot Grid布局（.te3pivot）

这些文件包含 Tabular Editor 3 中 Pivot Grid 的布局。它们是简单的 JSON 文件，用于指定在 Pivot Grid 中显示哪些字段（度量值、列、层次结构）以及如何排列这些字段。

这些文件只能在 Tabular Editor 3 连接到 Analysis Services 实例或 Power BI/Fabric XMLA endpoint 时打开。

### DAX 脚本 (.te3daxs)

这些文件是已保存的 DAX 脚本（而非查询），用于在 Tabular Editor 中一次性操作多个 DAX 对象。例如，修改语义模型中的多个 Measure。

### C# 脚本 (.csx)

创建和编辑 C# 脚本是 Tabular Editor 最重要的生产力功能之一。

这些脚本可以保存为具有 .csc 扩展名的文件并加载到 Tabular Editor 中，也可以保存为宏。[MacroActions.json 本地设置文件](xref:supported-files#macroactionsjson)由 Tabular Editor 维护。

这样，脚本就可以重复使用，而无需每次都从头开始编写。[脚本库](xref:csharp-script-library)是研究和重用各种脚本示例的理想场所，因为这些示例展示了 C# 的不同特性和功能。 

[下载C# Script文件示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/create-sum-measures-csharp.csx)

### Vertipaq Analyzer 文件（.vpax）

使用 Tabular Editor，您可以使用 Vertipaq Analyzer 功能导出和导入 .vpax 文件。.vpax 文件是一个压缩文件，其中包含有关你语义模型的大小和结构的信息，但不包含实际数据。 

您可以使用此文件分析和优化模型性能，而不会泄露敏感数据。例如，您可以使用 [DAX 优化器](https://www.daxoptimizer.com/) 工具，根据 .vpax 文件获取有关如何改进 DAX 公式 的建议。

[下载DAX脚本文件示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/dax-script-example.te3daxs)

与其他支持的文件类型不同，创建 .vpax 文件是在 Vertipaq Analyzer 窗口中使用“导入”和“导出”按钮完成的。 

![VPAX](~/content/assets/images/file-types/te3-supported-file-vpax.png)

[下载 VPAX 文件示例](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/vpaq-example.vpax)

> [!WARNING]
> 如果您的模型元数据是机密的，则 .vpax 文件也应被视为机密，并且仅在考虑到这一点的情况下进行共享。如果您担心知识产权的保护，Tabular Editor 3 提供了一个混淆 VPAX 文件的选项。

### 混淆的 VPAX 文件 (.ovpax)

如果需要将 VPAX 文件移交给第三方（例如顾问或工具供应商），您可以对文件进行混淆以隐藏模型元数据。要执行此操作，请在 Vertipaq Analyzer 窗口中“导出”按钮旁边的下拉按钮下选择“混淆导出…”选项。

混淆的 VPAX 文件使用 .ovpax 文件扩展名。

![导出混淆的 VPAX](~/content/assets/images/obfuscated-vpax.png)

有关 Vertipaq Analyzer 的更多文档，请参阅：[sqlbi Vertipaq Analyzer](https://www.sqlbi.com/tools/vertipaq-analyzer) 和 [sqlbi 文档：Vertipaq Analyzer](https://docs.sqlbi.com/vertipaq-analyzer/)

有关 VPAX 文件混淆的更多信息，请参阅：[VPAX 混淆器](https://www.sqlbi.com/blog/marco/2024/03/15/vpax-obfuscator-a-library-to-obfuscate-vpax-files/)

## 本地设置文件

Tabular Editor 在“%localappdata%\TabularEditor3”文件夹中维护多个本地文件。这些文件与 Tabular Editor 3 的功能相关，了解这些文件很有用。

在团队中共享这些文件可能很有帮助，这样所有开发人员都将拥有相同的宏和 BPA 规则。

> [!TIP]
> 将版本控制文件同步到“%localappdata%\TabularEditor3”文件夹的 Windows 原生方式是使用 [SymLink](https://www.howtogeek.com/16226/complete-guide-to-symbolic-links-symlinks-on-windows-or-linux/)。
>
> 将所需文件存储在 Git 或 OneDrive 中，并创建指向“%localappdata%\TabularEditor3”文件夹的符号链接，但请注意，如果多位用户更新同一文件版本，这可能会导致同步问题。
> 但是，Tabular Editor 不直接支持此操作，因此请自行决定是否实施。 


### AI 审计日志

仅在安装了 AI 功能组件时显示。Tabular Editor 会记录[AI 助手](xref:ai-assistant)和[MCP 服务器](xref:mcp-server)的操作：请求了哪些权限以及如何回应这些请求，运行了哪些工具以及每个工具是成功、失败还是被拒绝，以及任何已运行或移交审核的 C# 脚本的完整文本。绝不会记录来自您模型的提示、回复和数据值。

默认情况下，每天写入一个文件，并保留 30 天。通过 **工具 > 首选项 > AI 功能** 下的 **打开审计文件夹** 进入该文件夹。管理员可以通过[策略](xref:policies)移动该文件夹并更改保留期。请参阅 @ai-audit-log，了解每条记录包含的内容。

与此文件夹中的其他文件不同，此文件是记录，而不是设置。请勿共享或同步此文件：它是一份每台机器的日志，其中包含的脚本可能会揭示您所处理的模型的结构。

### MacroActions.json
此文件存储您已创建或导入的所有宏。与同事共享此文件或将其备份到版本控制系统中可能很有用，也可以将其配置为与包含宏的远程存储库同步（请参阅上面的提示）。

此文件包含软件中使用的每个宏的索引。如果您需要更改任何宏的顺序或名称，您可以使用文本编辑器手动编辑此文件。但是，请注意不要在文件中引入任何错误或不一致之处，从而导致文件损坏，因此请务必创建备份。

[下载示例 MacroActions 文件](https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/MacroActions.json)


### BPARules.json
该文件包含[Best Practice Analyzer 规则](xref:using-bpa)和修复表达式。添加和编辑修复表达式的唯一位置是此 JSON 文件中。
建议将 PBA 规则文件存储在版本控制中，这样也可以在部署前对语义模型运行 BPA 规则。 

您可以在此处下载官方 Microsoft BPA 规则：[PBA 规则](https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json)

### RecentServers.json
包含您已连接的服务器，其中为每台服务器保存了身份验证类型、用户名、模式和状态栏颜色，以及已固定的服务器列表。密码不会被存储。要移除或固定服务器，请在连接对话框的**服务器**列表中右键单击该服务器。请参阅[最近访问的服务器和已固定的服务器](xref:xmla-as-connectivity#recent-and-pinned-servers)。

### Layouts.json
启动应用程序时，Tabular Editor 会自动生成 Layouts 文件。它包含有关如何配置 Tabular Editor 3 的 UI 布局的所有信息。

> [!TIP]
> 删除此文件将重置 Tabular Editor 的布局。如果 Tabular Editor 布局未按预期表现，一个很好的第一步是将此文件备份到其他位置，删除原文件，然后重启 Tabular Editor 3。
