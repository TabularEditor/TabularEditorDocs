---
uid: desktop-limitations
title: Power BI Desktop 限制（已过时）
author: Morten Lønskov
updated: 2023-08-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# Power BI Desktop 的限制

将 Tabular Editor（任意版本）作为 [Power BI Desktop 的外部工具](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools) 使用时，有一些限制需要注意。

本文提到的限制同样适用于 Tabular Editor 2.x。

## 不支持的操作

自 2025 年六月的 Power BI Desktop 更新起，已不再存在任何不受支持的写入操作。 换句话说，第三方工具现在可以自由修改托管在 Power BI Desktop 中的语义模型的任何部分，包括添加和删除表与列、更改数据类型等。 因此，本文中的大部分信息已不再适用。 不过，如果你使用的是 2025 年六月更新之前的 Power BI Desktop 版本，请查看下方的 [数据建模操作](#data-modeling-operations) 部分中的限制。

更多信息请参阅 [官方博客文章](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/)。

## Power BI 文件类型

使用 Power BI 时，你通常会遇到三种常见的文件类型：

- **.pbix**（Power BI Report）
- **.pbit**（Power BI 模板）
- **.pbip**（Power BI Project）

这两个文件 **.pbix** 和 **.pbit** 都可以在 Power BI Desktop 中打开，并且基本上定义了与 Power BI Report 相关的所有内容：数据源、Power Query 转换、表格式 Data model、报表页面、Visual、Bookmark 等。

主要区别在于：**.pbix 和 .pbip 文件包含模型数据**，而 **.pbit 文件不包含任何数据**。 另外，**.pbix** 文件不以这种格式包含模型元数据，因此，**无法以任何方式将 .pbix 文件直接加载到 Tabular Editor 中**。 相反，你需要改用“外部工具”集成；这要求你按下文所述在 Power BI Desktop 中加载 .pbix 文件。

> [!WARNING]
> 尽管从技术上讲可以在 .pbit 文件中加载和保存模型元数据，但 Power BI Desktop 不支持这种做法。 因此，修改 .pbit 文件始终存在风险：可能导致 Power BI Desktop 无法加载该文件，或在加载后引发稳定性问题。 在这种情况下，Microsoft 支持将无法为你提供帮助。

> [!NOTE]
> 由于 **Tabular Editor 3 桌面版** 仅用于作为 Power BI Desktop 的外部工具，因此该版本不允许加载和保存 .pbit 文件。 不过，你仍然可以使用 Tabular Editor 2.x 来实现这一目的。 参阅 <xref:editions> 了解 Tabular Editor 3 各版本之间的差异。

## 外部工具架构

当 Power BI Desktop Report（.pbix 或 .pbit 文件）包含 Data model（也就是以 Import 或 DirectQuery 模式添加了一张或多张表）时，该 Data model 会托管在由 Power BI Desktop 管理的 Analysis Services 实例中。 外部工具可以出于不同目的连接到该 Analysis Services 实例。

> [!IMPORTANT]
> 使用 **Live Connection** 连接到 SSAS、Azure AS 或 Power BI Workspace 中 Dataset 的 Power BI Desktop Report 不包含 Data model。 因此，这些 Report **不能** 与 Tabular Editor 等外部工具一起使用。

外部工具可以通过 Power BI Desktop 分配的特定端口号，连接到由 Power BI Desktop 管理的 Analysis Services 实例。 当你从 Power BI Desktop 的“外部工具”功能区直接启动某个工具时，该端口号会作为命令行参数传递给外部工具。 对于 Tabular Editor 而言，这会使 Tabular Editor 加载 Data model。

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

连接到 Analysis Services 实例后，外部工具可以获取模型元数据信息，对 Data model 执行 DAX 或 MDX 查询，甚至还能通过 [Microsoft 提供的客户端库](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) 来更改模型元数据。 从这一点来看，由 Power BI Desktop 管理的 Analysis Services 实例与任何其他类型的 Analysis Services 实例没有区别。

## Data model 建模操作

不过，由于 Power BI Desktop 与 Analysis Services 的互操作方式所限，外部工具可对模型元数据应用的更改类型存在一些重要限制。 这些限制已在[外部工具官方文档](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)中列出，这里为方便起见再次说明：

### [2025 年六月之前](#tab/postjune2023)

**2025 年六月之前：通过第三方工具连接时的 Power BI Desktop 限制：**

| 对象          | 连接到 AS 实例                  |
| ----------- | -------------------------- |
| 表           | 否                          |
| 列           | 是的<sup>[1](#columns)</sup> |
| 计算表格        | 是的                         |
| 计算列         | 是的                         |
| 关系          | 是的                         |
| 度量值         | 是的                         |
| 模型 KPI      | 是的                         |
| 计算组         | 是的                         |
| 透视          | 是的                         |
| 翻译          | 是的                         |
| 行级安全性（RLS）  | 是的                         |
| 对象级安全性（OLS） | 是的                         |
| 注释          | 是的                         |
| M 表达式       | 否                          |

<a name="columns">1</a> - 使用外部工具连接到 AS 实例时，支持更改列的数据类型，但不支持重命名列。

Power BI Desktop 的_项目文件_支持更广泛的写入操作。 通过将 Tabular Editor 用作外部工具时不支持的那些对象和操作，可能可以通过编辑 Power BI Desktop 项目文件来实现。 请参阅 Microsoft 文档了解更多信息：[Power BI Desktop projects - Model authoring](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring)。

### [2023 年六月之前](#tab/prejune2023)

**2023 年六月之前，通过第三方工具连接时 Power BI Desktop 的限制：**

- 定义并编辑用于计算的度量值，包括格式字符串、KPI 和明细行设置。
- 添加计算组，以便在复杂模型中复用计算逻辑。
- 创建透视，用于定义面向特定业务域、聚焦的 Dataset 元数据视图。
- 应用元数据翻译，以便在单个 Dataset 中支持多语言版本。
- 添加 Dataset 角色，用于定义行级安全性 (RLS) 和对象级安全性 (OLS) 规则，以限制数据访问。
- 定义并编辑字段参数。

尽管不受支持，但事实证明，仍有不少操作可以应用，而且不会引发问题。 例如，在撰写本文时，使用外部工具为单个列设置“显示文件夹”“描述”“汇总方式”等属性，似乎完全可行。 因此，Tabular Editor 提供了一个选项，让高级用户可以进行尝试：即使连接到 Power BI Desktop Data model，也允许执行所有数据建模操作。 您可以在 **工具 > 偏好 > Power BI > 允许 _不受支持_ 的建模操作** 下启用此选项，但启用前务必了解其中的风险。

---

## Data model 限制

所有 Tabular Object Model (TOM) 元数据都只能以只读方式访问。 由于 Power BI Desktop 必须与外部修改保持同步，写入操作会受到限制。因此，除了上方各选项卡中提到的限制外，还不支持以下操作：

- 任何不在“支持的写入操作”范围内的 TOM 对象类型，例如表和列。
- 编辑 Power BI Desktop 模板 (PBIT) 文件。
- Report 级或数据级翻译。
- 尚不支持重命名表和列
- 向已在 Power BI Desktop 中加载的 Dataset 发送处理命令

> [!NOTE]
> 由 Power BI Desktop 管理的 Analysis Services 实例不会对允许进行的 Data model 建模操作施加强制限制。 需要由外部工具确保不会进行任何不受支持的更改。 忽略这一点可能会导致结果无法预测、.pbix/.pbit Report 文件损坏，或让 Power BI Desktop 变得不稳定。

> [!IMPORTANT]
> 对 Data model 的更改可能会破坏你的 Power BI Report Visual。 例如，如果将某个度量值从一张表移动到另一张表，那么任何使用该度量值的 Visual 都需要更新。 Kurt Buhler 在这篇博客中介绍了如何用更少手动操作的方式修复这些错误：[修复 Power BI “一个或多个字段存在问题”](https://data-goblins.com/power-bi/something-is-wrong-with-one-or-more-fields)

# Tabular Editor 与 Power BI Desktop

将 Tabular Editor（任何版本）作为 Power BI Desktop 的外部工具使用时，上述列表中所有不受支持的操作默认都会被禁用。 换句话说，Tabular Editor 不允许你在 Power BI Desktop 模型上添加或重命名表、列，执行刷新等操作。

虽然不受支持，但事实证明仍有不少操作可以应用，而且不会引发问题。 因此，Tabular Editor 提供了一个选项，允许高级用户进行试验：即使连接到 Power BI Desktop Data model，也允许执行所有数据建模操作。 你可以在 **工具 > 偏好 > Power BI > 允许 _不受支持的_ 建模操作** 中启用此选项，但在启用前一定要先了解相关风险。

> [!NOTE]
> 在 Tabular Editor 2.x 中，此设置位于 **文件 > 偏好 > 允许不受支持的 Power BI 功能（实验性）**

启用该功能后，Tabular Editor 将不再阻止任何建模操作，而是为你提供对所有 TOM 对象及其属性的完整读/写访问权限。 在该功能启用期间，每当你在 Tabular Editor 中打开 Power BI Desktop 模型时，都会看到一个警告提示：

![启用不受支持的建模操作时显示的警告](~/content/assets/images/pbi-desktop-warning.png)

> [!WARNING]
> 如果由于通过外部工具进行了不受支持的更改，导致你的 .pbix 或 .pbit 文件损坏或引发 Power BI Desktop 不稳定，Microsoft 支持将无法为你提供帮助。 因此，在启动任何允许更改你的 Data model 的外部工具之前，一定要先备份你的 .pbix 或 .pbit 文件。
