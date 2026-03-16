---
uid: import-tables
title: 导入表
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

Tabular Editor 3 内置 **表导入向导**，可帮助你在模型中创建数据源，并从 SQL Server 数据库等关系型数据源导入表/视图。

![表导入向导](~/content/assets/images/import-tables-wizard.png)

## TOM 数据源类型

根据你使用的 Analysis Services 版本，在模型元数据中定义数据源的方式也不同：

- **提供程序（又称旧版）**：在所有 Analysis Services 版本和所有兼容级别中均可用。 支持的数据源范围有限，主要通过 OLE DB/ODBC 驱动程序访问关系型数据源。 分区通常使用 SQL 语句定义，并以原生方式在数据源上执行。 凭据在 Tabular Object Model 的 Provider数据源对象中进行管理，并在服务器端存储和加密。
- **结构化（又称 Power Query）**：自 SQL Server 2017 起可用（兼容级别 1400+）。 支持的数据源范围比旧版提供程序更广。 分区通常使用 M（Power Query）表达式定义。 凭据在 Tabular Object Model 的 Structured数据源对象中进行管理，并且每次部署到 Analysis Services 时都需要指定。
- **隐式数据源**：仅用于 Power BI 语义模型。 模型中不会创建显式的数据源对象。 取而代之的是，M（Power Query）表达式会隐式定义数据源。 凭据不存储在 Tabular Object Model 中，而是由 Power BI Desktop 或 Power BI 服务进行管理。

> [!NOTE]
> Tabular Editor 2.x 的“表导入向导”和“更新表架构”功能仅支持包含 SQL 分区的旧版数据源。 换句话说，不支持 Power Query 分区。 因此，通常建议使用 Legacy 旧版数据源，因为它们能在各类开发者工具之间实现最高程度的互操作性。

## 导入新表

在导入表时（模型菜单 > 导入表...），Tabular Editor 会显示上面提到的选项（用于创建新的数据源），以及模型中已存在的数据源列表。 如果要导入的表在模型中已指定的某个数据源中可用，请避免创建新的数据源。

> [!TIP]
> 语义模型通常被视为关系型 Warehouse 中经过优化、驻留内存的语义缓存。 因此，理想情况下，一个模型最好只包含一个数据源，这个数据源指向基于 SQL 的 Warehouse 或数据集市。

## 创建新的数据源

如果你需要创建新的数据源，Tabular Editor 会提供一份受支持的数据源列表：

![创建新数据源](~/content/assets/images/create-new-source.png)

请注意，尤其是 Power BI，Analysis Services 和 Power BI 支持的数据源范围要广得多；不过，上面截图中列出的数据源，才是 Tabular Editor 为了自动导入表元数据(即列名和数据类型)而能够连接的数据源。 对于不在此列表中的数据源，Tabular Editor 3 仍然可以[利用 Analysis Services 更新表架构](#updating-table-schema-through-analysis-services)。

目前，Tabular Editor 3 原生支持以下数据源：

- SQL Server 数据库
- Azure SQL 数据库
- Azure Synapse Analytics（SQL 池和无服务器 SQL 池）
- Oracle
- ODBC
- OLE DB
- Snowflake\*
- Power BI Dataflow\*
- Databricks\*
- Fabric Lakehouse\*
- Fabric Warehouse\*
- Fabric SQL 数据库\*
- Fabric 镜像数据库\*

\*=这些数据源仅在 Power BI Data model 中作为隐式数据源受到支持。 它们在 SSAS / Azure AS 中不可用。

> [!TIP]
> 想了解如何连接到 Azure Databricks 的更多信息，可以看看 [连接到 Azure Databricks](xref:connecting-to-azure-databricks)。

从列表中选择某个数据源后，Tabular Editor 会显示一个连接详细信息对话框，让你指定服务器地址、凭据等与要创建的数据源相关的设置。 你指定的设置应该是 Tabular Editor 用来建立到该源的本地连接时要用的设置。 这些设置会保存在你的 @user-options 中。

![Sql Auth](~/content/assets/images/sql-auth.png)

如果你希望 Analysis Services 在连接时使用不同的凭据，可以在导入表之后，通过编辑 Tabular Object Model 中的数据源属性来指定。

## 选择要导入的对象

定义好数据源后，你可以从列表中选择表/视图，或指定要对该源执行的原生查询。

![Source Options](~/content/assets/images/source-options.png)

如果你选择第一个选项，Tabular Editor 将连接到该源并显示表和视图列表，你可以在下一页预览：

![Choose Source Objects](~/content/assets/images/choose-source-objects.png)

你可以在左侧勾选，以一次导入多个表/视图。 对于每个表/视图，你都可以取消勾选或勾选要导入的列。

> [!TIP]
> 如果你能控制源系统，我们建议始终在要导入的表之上创建一个视图。 在该视图中，确保更正将在语义模型中使用的名称、拼写等，并移除语义模型不需要的列（系统列、时间戳等）。
>
> 然后，在模型中从该视图导入所有列（本质上会生成一条 `SELECT * FROM ...` 语句）。 这样更易于维护，因为你只需在 Tabular Editor 中运行 Schema Update，就能判断源端是否有任何更改。

![Advanced Import](~/content/assets/images/advanced-import.png)

如果你使用左上角的下拉列表将预览模式切换为“Schema only”，就可以为每个源列更改导入的数据类型和列名。 例如，如果源数据使用浮点值，但你希望将数据以定点小数的形式导入，这会很有用。

![Confirm Selection](~/content/assets/images/confirm-selection.png)

在最后一页，确认你的选择，并选择要创建哪种类型的分区。 对于 Provider数据源，默认创建的分区类型是 `SQL`；而对于 Structured数据源，默认则为 `M`。

![Confirm Selection Direct Lake](~/content/assets/images/confirm-selection-direct-lake.png)

对于 Fabric 数据源，最后一页会显示一个下拉列表，供你选择将所选内容创建为 Direct Lake 或导入模式。

此时，你应该能看到表已导入，并且所有列、数据类型以及源列映射都已应用：

![Import Complete](~/content/assets/images/import-complete.png)

# 更新表架构

如果源中新增或更改了列，或者你最近修改了分区表达式或查询，你可以使用 Tabular Editor 的 **更新表架构** 功能来更新模型中的列元数据。

![Update Table Schema](~/content/assets/images/update-table-schema.png)

此菜单项既可在模型级别调用，也可对一组表甚至单个表分区调用。

使用此选项时，Tabular Editor 会连接到所有相关数据源（按需提示你输入凭据），以确定是否需要新增列，或修改或删除现有列。

> [!IMPORTANT]
> 如果之前导入到语义模型中的某个列在源中被删除或重命名，则必须更新语义模型中的表架构。 否则，数据刷新操作可能会失败。

![Schema Compare Dialog](~/content/assets/images/schema-compare-dialog.png)

在上面的截图中，Tabular Editor 检测到几列新增列、一处数据类型变更，以及两列在源中被重命名。 注意，列重命名的检测只对简单更改有效。 在其他情况下，名称更改通常会导致 Tabular Editor 将其检测为“删除了一列”并“新增了一列”。下面的 `Tax Amount` 列就是这种情况：它似乎在源中被重命名为 `TaxAmt`。

为避免破坏依赖 `[Tax Amount]` 列的现有 DAX 公式，你可以按住 Ctrl 键并单击“架构更改”对话框中的两行，然后右键单击，将“删除列”和“新增列”合并为一次 SourceColumn 更新操作：

![Combine Sourcecolumn Update](~/content/assets/images/combine-sourcecolumn-update.png)

如果你不希望将名称更改传播到已导入的列（而只是想更新 SourceColumn 属性，以反映数据源中已更改的名称），你可以在下拉列表中取消选择 `Name` 更新操作：

![Deselect Name](~/content/assets/images/deselect-name.png)

## 通过 Analysis Services 更新表架构

默认情况下，Tabular Editor 3 会尝试直接连接到数据源，以便更新已导入表的架构。 当然，这只在 Tabular Editor 3 支持该数据源时才有效。 如果你需要更新从 Tabular Editor 3 不支持的数据源导入的表的架构，可以在 **工具 > 偏好 > 架构比较** 下启用 **使用 Analysis Services 进行更改检测** 选项。 当某个分区或共享表达式的 M 表达式过于复杂，以至于 Tabular Editor 3 的内置架构检测功能无法处理时，也同样适用。 例如，内置架构检测不支持某些 M 函数。

![通过 As 更新表架构](~/content/assets/images/update-table-schema-through-as.png)

启用此选项后，当 Tabular Editor 3 连接到 Analysis Services 或 Power BI XMLA endpoint 时，即可更新从 Analysis Services 或 Power BI 支持的**任何**数据源导入的表的架构。

> [!NOTE]
> **使用 Analysis Services 进行更改检测** 选项仅在 Tabular Editor 3 连接到 Analysis Services 或 Power BI XMLA endpoint 时才会生效。 因此，建议你在开发模型时始终使用[工作区模式](xref:workspace-mode)。

启用“**使用 Analysis Services 进行更改检测**”选项后，当请求更新架构时，Tabular Editor 3 将使用以下技术：

1. 针对已连接的 Analysis Services 实例创建一个新的事务
2. 向模型添加一个新的临时表。 该表使用一个 Power Query 分区表达式，用于返回原始表达式的架构，而该原始表达式已请求更新架构。 这是通过 [`Table.Schema` M 函数](https://docs.microsoft.com/en-us/powerquery-m/table-schema)实现的。
3. Analysis Services 刷新该临时表。 Analysis Services 负责连接到数据源，以检索更新后的架构。
4. Tabular Editor 3 查询临时表的内容，以获取架构元数据。
5. 回滚该事务，使 Analysis Services 数据库或 Power BI 语义模型回到步骤 1 之前的原始状态。
6. 如果存在任何架构更改，Tabular Editor 3 会显示如上所示的“应用架构更改”对话框。

借助该技术，无论表背后的 M 查询有多复杂、使用了哪些函数，Tabular Editor 3 都可以从原本不受支持的数据源导入并更新表。

> [!NOTE]
> 如果你的 M 表达式通过 M [`Table.NestedJoin`](https://learn.microsoft.com/en-us/powerquery-m/table-nestedjoin) 函数等方式组合了多个来源的数据，你可能需要在 Power BI 服务中的语义模型里，将[**隐私级别**](https://powerbi.microsoft.com/en-us/blog/privacy-levels-for-cloud-data-sources/)从“私有”更改为“组织”。 否则，你可能会看到一条错误提示：`<Query> references other queries or steps, so it may not directly access a 数据源。 请重建此数据组合`。 即使未启用“**使用 Analysis Services 进行更改检测**”，也可能出现此错误，因为当 M 表达式复杂到超出 Tabular Editor 3 内置架构检测能力时，Tabular Editor 3 会自动回退到该检测机制。

### 通过 Analysis Services 导入新表

若要从原本不受支持的数据源导入表，你只要复制该数据源中的现有表，修改复制出来的表的分区查询里的 M 表达式，然后把更改保存到 Workspace 数据库，并按上文所述更新表架构。
