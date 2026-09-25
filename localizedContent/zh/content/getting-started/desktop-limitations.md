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
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# Power BI Desktop 的限制

将 Tabular Editor（任意版本）作为 [Power BI Desktop 的外部工具](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools) 使用时，有一些限制需要注意。

本文提到的限制同样适用于 Tabular Editor 2.x。

## 不支持的操作

自 2025 年六月的 Power BI Desktop 更新起，已不再存在任何不受支持的写入操作。 In other words, third party tools can now freely modify any aspect of the semantic model hosted in Power BI Desktop, including adding and removing tables and columns, changing data types, etc. As such, most of the information in this article is no longer relevant. However, if you're using a version of Power BI Desktop prior to the June 2025 update, please view the limitations in the [Data modeling operations](#data-modeling-operations) section below.

更多信息请参阅 [官方博客文章](https://powerbi.microsoft.com/en-us/blog/open-and-edit-any-semantic-model-with-power-bi-tools/)。

## Power BI 文件类型

使用 Power BI 时，你通常会遇到三种常见的文件类型：

- **.pbix**（Power BI Report）
- **.pbit**（Power BI 模板）
- **.pbip**（Power BI Project）

这两个文件 **.pbix** 和 **.pbit** 都可以在 Power BI Desktop 中打开，并且基本上定义了与 Power BI Report 相关的所有内容：数据源、Power Query 转换、表格式 Data model、报表页面、Visual、Bookmark 等。

主要区别在于：**.pbix 和 .pbip 文件包含模型数据**，而 **.pbit 文件不包含任何数据**。 In addition, a **.pbix** file does not contain the model metadata in this format, and therefore, **a .pbix file cannot be loaded directly in Tabular Editor** in any way. Instead, you will have to rely on the External Tools integration, which requires you to load the .pbix file in Power BI Desktop, as described below.

> [!WARNING]
> 尽管从技术上讲可以在 .pbit 文件中加载和保存模型元数据，但 Power BI Desktop 不支持这种做法。 As such, there is always a risk of making changes to the .pbit file which would cause the file to become unloadable in Power BI Desktop, or cause stability issues once loaded. In this case, Microsoft support will be unable to assist you.

> [!NOTE]
> 由于 **Tabular Editor 3 桌面版** 仅用于作为 Power BI Desktop 的外部工具，因此该版本不允许加载和保存 .pbit 文件。 You may however still use Tabular Editor 2.x for this purpose. See <xref:editions> to learn more about the difference between the Tabular Editor 3 editions.

## 外部工具架构

当 Power BI Desktop Report（.pbix 或 .pbit 文件）包含 Data model（也就是以 Import 或 DirectQuery 模式添加了一张或多张表）时，该 Data model 会托管在由 Power BI Desktop 管理的 Analysis Services 实例中。 External Tools may connect to this instance of Analysis Services for different purposes.

> [!IMPORTANT]
> 使用 **Live Connection** 连接到 SSAS、Azure AS 或 Power BI Workspace 中 Dataset 的 Power BI Desktop Report 不包含 Data model。 As such, these reports **cannot** be used with external tools such as Tabular Editor.

外部工具可以通过 Power BI Desktop 分配的特定端口号，连接到由 Power BI Desktop 管理的 Analysis Services 实例。 When a tool is launched directly from the "External Tools" ribbon in Power BI Desktop, this port number is passed to the external tool as a command line argument. In Tabular Editor's case, this causes the data model to be loaded in Tabular Editor.

<img class="noscale" src="~/content/assets/images/external-tool-architecture.png" />

连接到 Analysis Services 实例后，外部工具可以获取模型元数据信息，对 Data model 执行 DAX 或 MDX 查询，甚至还能通过 [Microsoft 提供的客户端库](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) 来更改模型元数据。 In this regard, the Analysis Services instance managed by Power BI Desktop is no different from any other type of Analysis Services instance.

## Data model 建模操作

However, due to the way Power BI Desktop interoperates with Analysis Services, there are a few important limitations to the type of changes external tools may apply to the model metadata. 这些限制已在[外部工具官方文档](https://docs.microsoft.com/en-us/power-bi/transform-model/desktop-external-tools#data-modeling-operations)中列出，这里为方便起见再次说明：

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

Power BI Desktop 的项目文件支持更广泛的写入操作。通过将 Tabular Editor 用作外部工具时不支持的那些对象和操作，可能可以通过编辑 Power BI Desktop 项目文件来实现。 Please refer to Microsoft documentation to learn more: [Power BI Desktop projects - Model authoring](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview#model-authoring).

### [2023 年六月之前](#tab/prejune2023)

**2023 年六月之前，通过第三方工具连接时 Power BI Desktop 的限制：**

- 定义并编辑用于计算的度量值，包括格式字符串、KPI 和明细行设置。
- 添加计算组，以便在复杂模型中复用计算逻辑。
- 创建透视，用于定义面向特定业务域、聚焦的 Dataset 元数据视图。
- 应用元数据翻译，以便在单个 Dataset 中支持多语言版本。
- 添加 Dataset 角色，用于定义行级安全性 (RLS) 和对象级安全性 (OLS) 规则，以限制数据访问。
- 定义并编辑字段参数。

Though unsupported, it turns out that a number of operations can still be applied without causing issues. For example, setting properties such as Display Folder, Description, Summarization, etc. on individual columns using an external tool seems to work just fine at the time of writing. For this reason, Tabular Editor has an option that allows advanced users to experiment, by allowing all data modeling operations even when connected to a Power BI Desktop model. You can enable this option under **Tools > Preferences > Power BI > Allow _unsupported_ modeling operations**, but make sure you understand the risks involved before doing so.

---

## Data model 限制

All Tabular Object Model (TOM) metadata can be accessed for read-only. Write operations are limited because Power BI Desktop must remain in-sync with the external modifications, therefore the following operations are not supported, in addition to those mentioned in the tabs above:

- 任何不在“支持的写入操作”范围内的 TOM 对象类型，例如表和列。
- 编辑 Power BI Desktop 模板 (PBIT) 文件。
- Report 级或数据级翻译。
- 尚不支持重命名表和列
- 向已在 Power BI Desktop 中加载的 Dataset 发送处理命令

> [!NOTE]
> 由 Power BI Desktop 管理的 Analysis Services 实例不会对允许进行的 Data model 建模操作施加强制限制。 It is up to the External Tool to ensure that no unsupported changes are made. Ignoring this may lead to unpredictable results, corrupt .pbix/.pbit report files or Power BI Desktop becoming unstable.

> [!IMPORTANT]
> 对 Data model 的更改可能会破坏你的 Power BI Report Visual。 If, for example, a measure is moved from one table to another, any visual using that measure will need to be updated. Kurt Buhler has a blog on how to fix these errors in a less manual way here: [Fix Power BI "Something is wrong with one or more fields"](https://data-goblins.com/power-bi/something-is-wrong-with-one-or-more-fields)

# Tabular Editor 与 Power BI Desktop

将 Tabular Editor（任何版本）作为 Power BI Desktop 的外部工具使用时，上述列表中所有不受支持的操作默认都会被禁用。 In other words, Tabular Editor will not allow you to add or rename tables, columns, perform refreshes etc. on a Power BI Desktop model.

Though unsupported, it turns out that a number of operations can still be applied without causing issues. For this reason, Tabular Editor has an option that allows advanced users to experiment, by allowing all data modeling operations even when connected to a Power BI Desktop model. You can enable this option under **Tools > Preferences > Power BI > Allow _unsupported_ modeling operations**, but make sure you understand the risks involved before doing so.

> [!NOTE]
> 在 Tabular Editor 2.x 中，此设置位于 **文件 > 偏好 > 允许不受支持的 Power BI 功能（实验性）**

启用该功能后，Tabular Editor 将不再阻止任何建模操作，而是为你提供对所有 TOM 对象及其属性的完整读/写访问权限。 While the feature is enabled, you will see a warning prompt whenever you open a Power BI Desktop model in Tabular Editor:

![启用不受支持的建模操作时显示的警告](~/content/assets/images/pbi-desktop-warning.png)

> [!WARNING]
> 如果由于通过外部工具进行了不受支持的更改，导致你的 .pbix 或 .pbit 文件损坏或引发 Power BI Desktop 不稳定，Microsoft 支持将无法为你提供帮助。 For this reason, **always** keep a backup of your .pbix or .pbit file before launching any External Tool that allows making changes to your data model.
