---
uid: import-tables
title: 导入表
author: Morten Lønskov
updated: 2026-09-14
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

Tabular Editor 3 内置 **表导入向导**，可帮助你在模型中创建数据源，并从 SQL Server 数据库等关系型数据源导入表/视图。

![表导入向导](~/content/assets/images/import-tables-wizard.png)

## TOM 数据源类型

根据你使用的 Analysis Services 版本，在模型元数据中定义数据源的方式也不同：

- **Provider (aka. Legacy)**: Available in every version of Analysis Services and every compatibility level. Supports a limited range of sources, primarily relational through OLE DB/ODBC drivers. Partitions are usually defined using a SQL statement, which is executed natively against the source. Credentials are managed in the Provider Data Source object in the Tabular Object Model and stored and encrypted server-side.
- **结构化（又称 Power Query）**：自 SQL Server 2017 起可用（兼容级别 1400+）。 Supports a wider range of data sources than Legacy providers. Partitions are usually defined using M (Power Query) expressions. Credentials are managed in the Structured Data Source object in the Tabular Object Model and need to be specified upon every deployment to Analysis Services.
- **隐式数据源**：仅用于 Power BI 语义模型。 No explicit Data Source object is created in the model. Instead, the M (Power Query) expression implicitly defines the data source. Credentials are not stored in the Tabular Object Model, but are managed by Power BI Desktop or the Power BI Service.

> [!NOTE]
> Tabular Editor 2.x 的“表导入向导”和“更新表架构”功能仅支持包含 SQL 分区的旧版数据源。 In other words, there is no support for Power Query partitions. For this reason, Legacy data sources are usually recommended, as they provide the highest level of interoperability between the developer tools.

## 导入新表

在导入表时（模型菜单 > 导入表...），Tabular Editor 会显示上面提到的选项（用于创建新的数据源），以及模型中已存在的数据源列表。 Avoid creating new data sources if the tables you want to import are available in one of the data sources already specified in the model.

> [!TIP]
> 语义模型通常被视为关系型 Warehouse 中经过优化、驻留内存的语义缓存。 For this reason, a model should ideally only contain a single data source, which would point to a SQL-based data warehouse or data mart.

## 创建新的数据源

如果你需要创建新的数据源，Tabular Editor 会提供一份受支持的数据源列表：

![创建新数据源](~/content/assets/images/create-new-source.png)

请注意，尤其是 Power BI，Analysis Services 和 Power BI 支持的数据源范围要广得多；不过，上面截图中列出的数据源，才是 Tabular Editor 为了自动导入表元数据(即列名和数据类型)而能够连接的数据源。 For data sources not on this list, Tabular Editor 3 can still [update table schema by utilising Analysis Services](#updating-table-schema-through-analysis-services).

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
- Fabric Lakehouse
- Fabric Warehouse
- Fabric SQL Database
- Fabric Mirrored Database

\*=这些数据源仅在 Power BI Data model 中作为隐式数据源受到支持。 They are not available in SSAS / Azure AS.

> [!TIP]
> 想了解如何连接到 Azure Databricks 的更多信息，可以看看 [连接到 Azure Databricks](xref:connecting-to-azure-databricks)。

After choosing one of the data sources on the list, Tabular Editor displays a connection details dialog, allowing you to specify server addresses, credentials, etc., specific to the data source you want to create. The settings that you specify should be those that Tabular Editor should use for establishing a local connection to the source. These settings are saved in your @user-options.

![Sql Auth](~/content/assets/images/sql-auth.png)

如果你希望 Analysis Services 在连接时使用不同的凭据，可以在导入表之后，通过编辑 Tabular Object Model 中的数据源属性来指定。

## Connecting to a data source

Each source type has its own connection dialog, and the authenticators on offer differ between them. The choice matters beyond the first connection, because some authenticators need a person at the keyboard and so cannot be used for a scheduled refresh.

See @connectivity for the full list, and the page for your source:

- @connect-sql-server, covering Azure SQL and Synapse
- @connect-snowflake, including key pair authentication for unattended work
- @connect-databricks
- @connect-oracle
- @connect-odbc, which is also how PostgreSQL, MySQL, MariaDB and IBM Db2 are reached
- @connect-oledb
- @connect-onelake
- @connect-dataflows

Credentials are stored per user and per model in the [user options](xref:user-options) file, encrypted with your Windows account key, and never become part of the model metadata.

## 选择要导入的对象

定义好数据源后，你可以从列表中选择表/视图，或指定要对该源执行的原生查询。

![Source Options](~/content/assets/images/source-options.png)

如果你选择第一个选项，Tabular Editor 将连接到该源并显示表和视图列表，你可以在下一页预览：

![Choose Source Objects](~/content/assets/images/choose-source-objects.png)

你可以在左侧勾选，以一次导入多个表/视图。 For each table/view, you may deselect/select columns to import.

> [!TIP]
> If you are in control of the source, we recommend always creating a view on top of the tables you wish to import. In the view, make sure to correct any names, spellings, etc., to be used in the Semantic Model, and get rid of any columns not needed by the Semantic Model (system columns, timestamps, etc.).
>
> 然后，在模型中从该视图导入所有列（本质上会生成一条 `SELECT * FROM ...` 语句）。 This makes maintenance easier, as you only need to run a Schema Update in Tabular Editor to determine if anything was changed in the source.

![Advanced Import](~/content/assets/images/advanced-import.png)

如果你使用左上角的下拉列表将预览模式切换为“Schema only”，就可以为每个源列更改导入的数据类型和列名。 This may be useful for example if your source using floating-point values, but you want the data to be imported as fixed-decimal.

![Confirm Selection](~/content/assets/images/confirm-selection.png)

On the last page, confirm your selection and choose which type of partitions to create. 对于 Provider数据源，默认创建的分区类型是 `SQL`；而对于 Structured数据源，默认则为 `M`。

![Confirm Selection Direct Lake](~/content/assets/images/confirm-selection-direct-lake.png)

对于 Fabric 数据源，最后一页会显示一个下拉列表，供你选择将所选内容创建为 Direct Lake 或导入模式。

此时，你应该能看到表已导入，并且所有列、数据类型以及源列映射都已应用：

![Import Complete](~/content/assets/images/import-complete.png)

Columns are created in the order they appear in the source table. Importing the same table twice therefore produces the same column order both times.

> [!NOTE]
> Creating Import tables from a **Fabric Lakehouse** or **Fabric Warehouse** reads the table's schema through the SQL analytics endpoint carried on the data source. Where no endpoint can be determined and none is given in the import settings, Tabular Editor reports an error naming what it needs: the SQL endpoint as the server, or a workspace id and item id. It does not create a table with no columns.

## 更新表架构

如果源中新增或更改了列，或者你最近修改了分区表达式或查询，你可以使用 Tabular Editor 的 **更新表架构** 功能来更新模型中的列元数据。

![Update Table Schema](~/content/assets/images/update-table-schema.png)

此菜单项既可在模型级别调用，也可对一组表甚至单个表分区调用。

When using this option, Tabular Editor will connect to all the relevant data sources (prompting for credentials as needed), to determine whether columns need to be added, modified or removed. Columns follow the source table's own column order, so a schema update does not shuffle them.

> [!IMPORTANT]
> 如果之前导入到语义模型中的某个列在源中被删除或重命名，则必须更新语义模型中的表架构。 Otherwise, data refresh operations may fail.

![Schema Compare Dialog](~/content/assets/images/schema-compare-dialog.png)

In the screenshot above, Tabular Editor detected two new columns in the source that have not yet been imported (`Color` and `Material`), and flagged two existing columns for removal (`Colour` and `Substance Type`) because their names no longer match any column in the source. Detection of a column rename only works for simple changes; here, the names differ enough that Tabular Editor reports a removal and an addition rather than a rename - `Colour` has in fact been renamed to `Color` in the source, and `Substance Type` to `Material`.

To avoid breaking existing DAX formulas that rely on the `[Colour]` column, you can hold down the Ctrl button and click on the `Color` (import) and `Colour` (remove) rows in the Schema Change dialog, then right-click in order to combine the column removal and column addition into a single SourceColumn update operation:

![Combine Sourcecolumn Update](~/content/assets/images/combine-sourcecolumn-update.png)

如果你不希望将名称更改传播到已导入的列（而只是想更新 SourceColumn 属性，以反映数据源中已更改的名称），你可以在下拉列表中取消选择 `Name` 更新操作：

![Deselect Name](~/content/assets/images/deselect-name.png)

## 通过 Analysis Services 更新表架构

By default, Tabular Editor 3 attempts to connect directly to the data source for the purposes of updating the imported table schema. Naturally, this only works when the data source is supported by Tabular Editor 3. 如果你需要更新从 Tabular Editor 3 不支持的数据源导入的表的架构，可以在 **工具 > 偏好 > 架构比较** 下启用 **使用 Analysis Services 进行更改检测** 选项。 This also applies when the M expression of a partition or shared expression is too complex for Tabular Editor 3's built-in schema detection feature. For example, the built-in schema detection does not support certain M functions.

![通过 As 更新表架构](~/content/assets/images/update-table-schema-through-as.png)

启用此选项后，当 Tabular Editor 3 连接到 Analysis Services 或 Power BI XMLA endpoint 时，即可更新从 Analysis Services 或 Power BI 支持的**任何**数据源导入的表的架构。

> [!NOTE]
> **使用 Analysis Services 进行更改检测** 选项仅在 Tabular Editor 3 连接到 Analysis Services 或 Power BI XMLA endpoint 时才会生效。 For this reason, we recommend that developers always use the [Workspace Mode](xref:workspace-mode) when developing models.

启用“**使用 Analysis Services 进行更改检测**”选项后，当请求更新架构时，Tabular Editor 3 将使用以下技术：

1. 针对已连接的 Analysis Services 实例创建一个新的事务
2. A new temporary table is added to the model. 该表使用一个 Power Query 分区表达式，用于返回原始表达式的架构，而该原始表达式已请求更新架构。 This is done using the [`Table.Schema` M function](https://docs.microsoft.com/en-us/powerquery-m/table-schema).
3. Analysis Services 刷新该临时表。 Analysis Services takes care of connecting to the data source in order to retrieve the updated schema.
4. Tabular Editor 3 查询临时表的内容，以获取架构元数据。
5. 回滚该事务，使 Analysis Services 数据库或 Power BI 语义模型回到步骤 1 之前的原始状态。
6. 如果存在任何架构更改，Tabular Editor 3 会显示如上所示的“应用架构更改”对话框。

借助该技术，无论表背后的 M 查询有多复杂、使用了哪些函数，Tabular Editor 3 都可以从原本不受支持的数据源导入并更新表。

> [!NOTE]
> 如果你的 M 表达式通过 M [`Table.NestedJoin`](https://learn.microsoft.com/en-us/powerquery-m/table-nestedjoin) 函数等方式组合了多个来源的数据，你可能需要在 Power BI 服务中的语义模型里，将[**隐私级别**](https://powerbi.microsoft.com/en-us/blog/privacy-levels-for-cloud-data-sources/)从“私有”更改为“组织”。 Otherwise, you may see an error indicating that `<Query> references other queries or steps, so it may not directly access a data source. Please rebuild this data combination.`. This error may also occur even if **Use Analysis Services for change detection** is not enabled, as Tabular Editor 3 will automatically fall back to this detection mechanism when the M expression is too complex for Tabular Editor 3's built-in schema detection.

### 通过 Analysis Services 导入新表

若要从原本不受支持的数据源导入表，你只要复制该数据源中的现有表，修改复制出来的表的分区查询里的 M 表达式，然后把更改保存到 Workspace 数据库，并按上文所述更新表架构。
