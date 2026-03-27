---
uid: general-introduction
title: 总体介绍和体系结构
author: Daniel Otykier
updated: 2021-09-30
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 总体介绍和体系结构

Tabular Editor 是一款用于开发表格模型的 Windows 桌面应用程序。 具体而言，该工具可用于编辑 Tabular Object Model (TOM) 元数据。 这个工具可以从文件或现有的 Analysis Services 数据库加载 TOM 元数据，也可以将更新后的 TOM 元数据部署到 Analysis Services。

> [!NOTE]
> 我们使用术语 **表格模型** 来同时表示 Analysis Services Tabular 模型和 Power BI Dataset，因为 Analysis Services Tabular 是 Power BI 使用的 Data model 引擎。 同样，当我们使用术语 **Analysis Services** 时，指的是“Analysis Services 的任何实例”，例如 SQL Server Analysis Services、Power BI Desktop，或 Power BI 服务的 XMLA 端点。

## Tabular Object Model (TOM) 元数据

一个 Data model 由多张表组成。 每张表有一列或多列，还可能包含度量值和层次结构。 通常，Data model 还会定义表之间的关系、包含连接详细信息的数据源，以及包含数据源表达式 (SQL 或 M 查询) 的表分区，用于加载数据等。 所有这些信息统称为 **模型元数据**，并以一种基于 JSON 的格式存储，该格式称为 **Tabular Object Model (TOM)**。

- 当使用 Visual Studio 创建表格模型时，用于表示 TOM 元数据的 JSON 会存储在名为 **Model.bim** 的文件中。
- 当使用 Power BI Desktop 创建 Data model 时，TOM 元数据会嵌入在 .pbix 或 .pbit 文件中 (因为这种文件格式还包含许多其他细节，例如 Visual 的定义、Bookmark 等，而这些与 Data model 本身无关)。

借助名为 [AMO/TOM](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 的客户端库，Tabular Editor 能够从这种基于 JSON 的格式加载元数据，并将其保存回该格式。 此外，该客户端库还允许 Tabular Editor 直接连接到任何 Analysis Services 实例，以便从现有数据库获取模型元数据。 下图对此进行了说明。

![架构](~/content/assets/images/architecture.png)

> [!NOTE]
> 在上文段落中，我们使用术语 **database** 来表示已部署到 Analysis Services 的模型。 在 Power BI 服务中，术语 **dataset** 用来表示同一事物，即表格模型。

Tabular Editor 可从以下来源加载模型元数据：

- [1] Model.bim 文件
- [2] Database.json 文件（更多信息见 @parallel-development）
- [3] .pbit 文件（Power BI 模板）
- [4] SQL Server Analysis Services（表格模式）上的数据库
- [5] Azure Analysis Services 上的数据库
- [6] Power BI Premium\* Workspace 中的 Dataset
- [7] Import/DirectQuery 模式下的 Power BI Desktop Report

\*要启用 [XMLA 端点](https://docs.microsoft.com/en-us/power-bi/admin/service-premium-connect-tools)，必须拥有 Power BI Premium/Embedded 容量或 Power BI Premium-Per-User。 任何第三方工具要连接到 Power BI Dataset，都必须启用 XMLA 端点。

> [!IMPORTANT]
> Tabular Editor 2.x 支持以上 1-7 的所有来源。 Tabular Editor 3 仅支持其中部分来源，具体取决于你使用的是哪种 [Tabular Editor 3 版本](xref:editions)。

在 Tabular Editor 中加载模型元数据后，你可以自由添加/编辑/删除 **对象**，并更改 **对象属性**。 在你明确保存模型之前，修改不会写回到源。你可以选择 **File > Save**，或按 CTRL+S。 如果模型元数据是从文件源加载的（以上来源 1-3），该文件会被更新。 如果模型元数据是从 Analysis Services 加载的（以上来源 4-7），更改会保存回 Analysis Services。 注意，某些更改可能会导致对象进入最终用户无法再查询的状态。 例如，如果你在表中添加了一列，在用户能够查询该表内容或任何依赖于该表的度量值之前，你需要先 [刷新表](xref:refresh-preview-query#refreshing-data)。

> [!WARNING]
> 将模型元数据的更改保存回 Power BI Desktop（以上来源 7）时，会有一些限制。 更多信息见 @desktop-limitations。

### TOM 对象和属性

TOM 元数据由 **对象** 和 **属性** 组成。

TOM **对象** 示例：

- 数据源
- 表
- 分区
- 度量值
- KPI
- 列
- 模型角色

TOM **对象属性**示例：

- `Name`（文本）
- `显示文件夹`（文本）
- `Description`（文本）
- `Hidden`（true/false）
- `Summarize By`（可选项之一：None、Sum、Min、Max、...）

大多数属性都是简单值（文本、true/false、从选项中选择其一，也称为。 枚举），但属性也可以引用其他对象（例如，`Sort By Column` 属性应引用一列）。 属性也可以是对象数组，例如模型角色对象上的 `Members` 属性。

Tabular Editor 通常沿用 [Microsoft.AnalysisServices.Tabular 命名空间](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular?view=analysisservices-dotnet) 中定义的对象和属性名称。 如果你想进一步了解特定的 TOM 对象或属性，请始终查阅命名空间文档。 例如，要了解“Summarize By”这一列属性的作用，先在 Microsoft 文档中找到“Column”类，然后展开“Properties”，再滚动到“SummarizeBy”。 然后你会看到[这篇文章](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.tabular.column.summarizeby?view=analysisservices-dotnet)。

![Microsoft 文档中的 SummarizeBy](~/content/assets/images/asdocs-summarizyby.png)

### 编辑属性值

Tabular Editor 的两个版本都会以层级视图显示对象模型元数据，这个视图称为 **TOM Explorer**，其结构大致对应 JSON 元数据的层级结构：

![TOM Explorer](~/content/assets/images/tom-explorer.png)

通常情况下，Tabular Editor 允许你先在 TOM Explorer 中选择一个对象（按住 SHIFT 或 CTRL 可一次选择多个对象），然后直接在 **属性视图** 中编辑属性值（见下图）。

![属性视图](~/content/assets/images/properties-view.png)

Tabular Editor 不会对修改后的属性值进行显式验证，除了少数基本规则（例如，对象名称不能为空、度量值名称必须唯一等）。 作为表格模型开发人员，你需要自己清楚应设置哪些属性，以及应使用什么值。

如果你在编辑属性值时出错，随时都可以按 CTRL+Z（编辑 > 撤销）撤销上一次属性更改。

## 架构

如上所述，Tabular Editor 有两种不同的运行模式：来自文件的元数据（即 **文件模式**）以及来自 Analysis Services 的元数据（即 **连接模式**）。 此外，Tabular Editor 3 引入了一种混合方式，称为 [**工作区模式**](xref:workspace-mode)。

在继续之前，了解这些模式之间的差异很重要：

- 在 **文件模式** 下，Tabular Editor 会从磁盘上的文件加载并将所有模型元数据保存回该文件。 在此模式下，Tabular Editor 无法与模型 **数据** 交互（也就是说，不支持表格预览、DAX 查询、Pivot Grid 以及数据刷新操作）。 该模式可完全离线使用，即使没有可用的 Analysis Services 实例也可以。 支持的模型元数据文件格式包括：
  - Model.bim（与 Visual Studio 使用的格式相同）
  - Database.json（仅 Tabular Editor 使用的文件夹结构格式）
  - .pbit（Power BI 模板）
- 在 **连接模式** 下，Tabular Editor 会从 Analysis Services 加载模型元数据，并将元数据保存回 Analysis Services。 在此模式下，可以使用 Tabular Editor 3 与模型 **数据** 交互（表格预览、DAX 查询、Pivot Grid 和数据刷新）。 该模式需要连接到某个 Analysis Services 实例。
- 在 **工作区模式** 下，Tabular Editor 3 会从磁盘上的文件加载模型元数据，并将元数据部署到 Analysis Services。 后续保存（CTRL+S）时，更新会同时写入磁盘和已连接的 Analysis Services 实例。 你也可以像在 **连接模式** 下一样与模型 **数据** 交互。

### 元数据同步

与标准工具（Visual Studio、Power BI Desktop）相比，Tabular Editor 的一大优势在于：模型元数据只有在你主动保存时才会写入。 换句话说，你可以对对象和属性进行多次修改，而不必在每次更改之间都等待某个 Analysis Services 实例完成同步。 同步 Analysis Services 数据库可能需要几秒钟才能完成，具体取决于 Data model 的大小和复杂程度。 在 Power BI Desktop 中，每当屏幕上出现那个臭名昭著的“Working on it”加载动画时，就会进行这种同步。 在 Tabular Editor 中，只有当你显式保存更改（CTRL+S）时才会进行同步。

当然，缺点是：在测试任何元数据修改带来的影响之前，你必须记得先显式保存这些更改。

## 后续步骤

- @installation-activation-basic
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2