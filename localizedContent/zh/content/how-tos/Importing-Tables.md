---
uid: importing-tables-te2
title: 在 TE2 中导入表
author: Daniel Otykier
updated: 2020-05-03
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      none: true
---

# 在 Tabular Editor 2 中导入表

If you already have a Legacy Data Source in your model, you can right click it, and choose "Import Tables...". Tabular Editor will attempt to connect using the data provider and credentials specified in the Data Source. If successful, you should get a list of all the databases, tables and views accessible through the Data Source:

![image](~/content/assets/images/importing-tables-01.png)

Clicking a table or view on the left-hand side will display a preview of the data on the right. 你可以取消选择不想包含的列。不过，[数据导入最佳实践](https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/)建议始终使用视图，并且只在这些视图中包含 Tabular 模型所需的列。 The UI will show you the resulting SQL query. By default, Tabular Editor will import a table/view using `SELECT * FROM ...`, but if you toggle any column in the preview, the resulting query will include an explicit list of columns. To switch back to `SELECT * FROM ...`, toggle the "Select all columns" checkbox in the upper right corner.

你可以一次选择多个表/视图进行导入。 When you click "Import", all selected tables/views will be imported as new tables with all columns populated from the metadata. A single partition will be created on each table, holding the resulting SQL query from the UI.

That's it! 再也不用在 Tabular Editor 和 SSDT 之间来回切换了。

## 关于旧式数据源与 Structured数据源的说明

As there is currently no way for Tabular Editor 2 to infer the metadata returned from M (Power Query) expressions, this UI only supports Legacy (aka. Provider) Data Sources. If you must use Structured Data Sources, you can still use a temporary Legacy connection to import the table schema initially (assuming your data source can be accessed through SQL, OLE DB or ODBC), and then manually switch the partitions on the imported tables, to use the Structured Data Sources. If you are importing data from "exotic" data sources, such as web services, Azure Data Lake Storage, etc. schema metadata can not be imported automatically, but [there is an option for providing the metadata information through the clipboard](#power-query-data-sources).

不过，总的来说，建议对以下类型的数据源始终使用 Legacy 连接：

- SQL Server 数据库
- Azure SQL 数据库
- Azure SQL Data Warehouse
- Azure Databricks（通过 ODBC）
- 任何关系型 OLE DB 数据源
- 任何关系型 ODBC 数据源

若要使用 Azure Active Directory 并启用 MFA 进行身份验证，请参阅此处。

## 在没有现有数据源的情况下导入

如果你的模型尚未包含任何数据源，可以在“模型”菜单中点击“导入表...”来导入表。 The resulting UI looks like this:

![image](~/content/assets/images/importing-tables-02.png)

保持选择“创建新的数据源并将其添加到模型中”，点击“下一步”时会显示连接对话框界面。 This dialog lets you specify the connection details:

![image](~/content/assets/images/importing-tables-03.png)

点击“确定”后，将在你的模型中创建一个使用所指定连接的（Legacy）数据源，并跳转到上方所示的导入页面。

列表中的下一个选项“使用临时连接”不会在模型中添加新的数据源。 This means that you are responsible for assigning a Data Source to the partitions of the newly imported table, before deploying the model.

The last option, "Manually import metadata from another application", is used when you want to import a new table based on a list of column metadata. This is useful for Structured (Power Query) Data Sources, [see below](#power-query-data-sources).

## SQL 功能

对于非 SQL Server 数据源（更准确地说，不使用 Native SQL Client 驱动程序的数据源），请留意屏幕底部附近的两个下拉框：

![image](~/content/assets/images/importing-tables-04.png)

“使用以下方式减少行数”下拉框可让你指定从数据源查询预览数据时使用哪种行数限制子句，因为表导入向导只会从源表或视图中检索 200 行数据。 You can choose between the most common row reduction clauses, such as "TOP", "LIMIT", "FETCH FIRST", etc.

The "Identifier quotes"-dropdown lets you specify how object names (column, tables) should be quoted in the generated SQL statements. This applies to both the data preview, as well as the SQL statement used in the table partition query, when the table is imported to the tabular model. By default, square brackets are used, but this can be changed to other common types of identifier quotes.

## 更改表的数据源

Another way to bring up the import page, is to right-click on an existing table (that uses a Legacy Data Source), and choose "Select Columns...". If that table was previously imported using the UI, the import page should show up with the source table/view and imported columns pre-selected. You may add/remove columns or even choose an entirely different table to be imported in place of the table you selected in your model. Keep in mind that any columns in your table, that were deselected or no longer exists in your source table/view will be removed from your model. You can always undo operations such as this using CTRL+Z.

## 刷新表元数据

As of version 2.8, Tabular Editor has a new UI feature that lets you easily check for schema drift. That is, detecting columns that had their data type changed, or were added or removed to source tables and views. This check may be invoked at the Model level (again, this only applies to Legacy Data Sources), at the Data Source level, at the Table level or at the Partition level. This is done by right-clicking the object and choosing "Refresh Table Metadata..."

![image](~/content/assets/images/importing-tables-05.png)

Changes are detected based on the "Source Column" and "Data Type" properties of all data columns on the respective tables. If any changes are detected, Tabular Editor will display the above UI, detailing the changes. 你可以取消勾选不想应用到模型中的变更，但要注意，某些变更可能会导致处理错误（例如源表/视图/查询中不存在的源列）。

This mechanism (as well as the Import Table UI) uses the FormatOnly-flag, when querying the metadata from the source. This means that you can have table partitions that use Stored Procedures. The FormatOnly-flag ensures that the Stored Proc is never executed directly. Instead, static analysis is performed by the server, in order to return only metadata describing the result set that would be returned from the Stored Proc upon execution. Depending on your RDBMS, there may be some limitations of the FormatOnly-flag when used with Stored Procedures. For more information on this topic when using SQL Server as a data source, please see [this article](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-describe-first-result-set-transact-sql?view=sql-server-2017#remarks).

### CLI 支持

You can perform a schema check at the model level from the command line by using the `-SC` flag. Note that the schema check, when executed through the CLI, will only report mapping issues. It will not make any changes to your model. 如果你在 CI/CD 流水线中使用 Tabular Editor，这会很有用，因为映射问题可能会在将模型部署到测试/生产环境后引发问题。

### 忽略对象

As of Tabular Editor 2.9.8, you can exclude objects from schema checks / metadata refresh. This is controlled by setting an annotation on the objects that you wish to leave out. As the annotation name, use the codes listed below. You can leave the annotation value blank or set it to "1", "true" or "yes". Setting the annotation value to "0", "false" or "no" will effectively disable the annotation, as if it didn't exist:

**表标志：**

- `TabularEditor_SkipSchemaCheck`：让 Tabular Editor 完全跳过对该表的架构检查。
- `TabularEditor_IgnoreSourceColumnAdded`：Tabular Editor 将忽略该表中未映射到任何表列的新增列。
- `TabularEditor_IgnoreDataTypeChange`：Tabular Editor 将忽略该表中任意列的数据类型不匹配问题。
- `TabularEditor_IgnoreMissingSourceColumn`：Tabular Editor 将忽略导入列在源端显然找不到对应源列的情况。

**列标志：**

- `TabularEditor_IgnoreDataTypeChange`：Tabular Editor 将忽略此特定列的数据类型不匹配问题。
- `TabularEditor_IgnoreMissingSourceColumn`：Tabular Editor 将忽略此特定列在源端显然缺失对应源列的情况。

这些标志会同时影响通过 UI 和 CLI 进行的架构检查。

### 将警告视为错误

默认情况下，当某个分区查询无法执行，或导入表包含一个在源查询中找不到任何对应列的列时，CLI 会 Report 错误。 The CLI will report a warning when a column's data type does not match the column in the source query, or if the source query contains columns that are not mapped to any columns in the imported table. The CLI will also report a warning when source queries of different partitions on the same table, do not return the same columns.

从 Tabular Editor 2.14.1 版本开始，你可以更改 CLI 的行为，使上面列出的所有警告都以错误的形式 Report。 To do this, add the following annotation at the **model** level:

- `TabularEditor_SchemaCheckNoWarnings`：让 Tabular Editor 将所有架构检查警告都视为错误。

## 启用 MFA 的 Azure Active Directory

如果你想从 Azure SQL 数据库或 Azure Synapse SQL 池导入表，很可能需要 Azure Active Directory 多因素身份验证。 Unfortunately, this is not supported by the SQL Native Client provider used in .NET Framework. Instead, use the MSOLEDBSQL provider (which also has the benefit that it is generally faster than the native client, when Analysis Services reads data from the table). Make sure you have the [latest (x86) version](https://docs.microsoft.com/en-us/sql/connect/oledb/download-oledb-driver-for-sql-server?view=sql-server-ver15) of this driver installed, to make this work on your local machine.

下面是将数据源设置为支持 MFA 的分步说明：

1. 创建一个新的旧版数据源，并将其添加到模型中。 Model > New Data Source (Legacy)
2. 将 Provider 属性设置为 `System.Data.OleDb`，并使用如下所示的连接字符串，将服务器、数据库和用户名替换为正确的值：

### 适用于 Synapse SQL 池：

```
Provider=MSOLEDBSQL;Data Source=<synapse workspace name>-ondemand.sql.azuresynapse.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

### 适用于 Azure SQL 数据库：

```
Provider=MSOLEDBSQL;Data Source=<sql server name>.database.windows.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

3. To import tables from this source, right-click on the data source and choose "Import Tables...", the Import Table Wizard UI should appear showing a list of tables/views from the source. Note, that for Synapse SQL pools, you may have to specify "TOP (without NOLOCK)" as a row clause, in order for the data preview to work.
4. When deploying your model to Analysis Services, you will most likely need to specify other credentials, such as a Service Principal application ID and secret or a SQL account, in order for Analysis Services to authenticate itself against the source when refreshing table data. This can be specified using TMSL or SSMS post-deployment, or you can set this up as [part of your CI/CD deployment pipeline](https://tabulareditor.com/blog/youre-deploying-it-wrong-as-edition-part-5#creating-your-first-release-pipeline).

## 手动导入架构/元数据

如果你使用的数据源不受“导入表”向导支持，可以选择手动导入元数据。 This option provides a UI where you can enter or paste in a table schema on the left hand side, which will be automatically parsed for column name and data type information. Alternatively, you can manually type each column name on the right hand side and choose a data type in the drop down. Either way, this is faster than manually creating a table and adding individual data columns through the main UI. When you're done, hit "Import!", adjust the table name and partition expression.

When parsing the text on the left hand side, Tabular Editor searches for certain keywords, in order to determine how the information is structured. 它在解析数据时相当宽容，因此你可以例如直接粘贴 CREATE TABLE SQL 脚本中的列清单，或粘贴下文所述的 Power Query `Table.Schema(...)` 函数输出。 The only requirements is that each line of text represents one column of source data.

![image](~/content/assets/images/importing-tables-06.png)

## Power Query 数据源

由于没有官方支持的方式来执行或验证 Power Query/M 表达式，Tabular Editor 对 Power Query 数据源仅提供有限支持。 As of 2.9.0, you may use the "Manually import metadata from another application"-option of the Import Table Wizard, as described above, to import a schema from a Power Query query in Excel or Power BI Desktop. The workflow is the following:

- 首先，确保你的模型包含一个 Power Query 数据源。 Right-click Data Sources > New Data Source (Power Query). If you're going to load data from a SQL Server, specify "tds" as the protocol and fill out the Database, Server and AuthenticationKind properties.
  ![image](~/content/assets/images/importing-tables-07.png)
- 对于其他类型的数据源，可能更方便的做法是先在 SSDT 中创建初始模型和前几张表，以弄清楚数据源应如何配置；之后在添加更多表时再使用下面的技巧。
- 在 Excel 或 Power BI Desktop 里使用 Power Query 连接到源数据，并应用需要的转换。
- Using Power Query's Advanced Editor, add a step that uses the `Table.Schema(...)` [M function](https://docs.microsoft.com/en-us/powerquery-m/table-schema) on the previous output:
  ![image](~/content/assets/images/importing-tables-08.png)
- Select the full output preview, copy it into the clipboard (CTRL+A, CTRL+C) and paste it into the schema/metadata textbox in the Import Tables Wizard:
  ![image](~/content/assets/images/importing-tables-09.png)
- 单击“Import!”，并为表指定一个合适的名称。
- 最后，将你在 Excel/Power BI 中使用的原始 M 表达式（即在用 `Table.Schema(...)` 函数修改之前的版本）粘贴到新建表的分区中。 Modify the M expression to point to the source you specified in the first step:
  ![image](~/content/assets/images/importing-tables-10.png)
