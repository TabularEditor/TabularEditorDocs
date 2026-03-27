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
      partial: true
---

# 在 Tabular Editor 2 中导入表

如果你的模型中已经有旧式数据源，你可以右键单击它，然后选择“导入表...”。 Tabular Editor 会尝试使用数据源中指定的数据提供程序和凭据进行连接。 如果连接成功，你将看到通过该数据源可访问的所有数据库、表和视图的列表：

![image](https://user-images.githubusercontent.com/8976200/49701892-35ea3900-fbf2-11e8-951a-8858179426c6.png)

单击左侧的表或视图，会在右侧显示数据预览。 你可以取消选择不想包含的列。不过，[数据导入最佳实践](https://www.sqlbi.com/articles/data-import-best-practices-in-power-bi/)建议始终使用视图，并且只在这些视图中包含 Tabular 模型所需的列。 界面会显示生成的 SQL 查询。 默认情况下，Tabular Editor 会使用 `SELECT * FROM ...` 导入表/视图；但如果你在预览中勾选或取消勾选任意列，生成的查询将包含一份显式的列列表。 要切回 `SELECT * FROM ...`，请在右上角勾选或取消勾选“选择所有列”复选框。

你可以一次选择多个表/视图进行导入。 当你单击“导入”时，所有选中的表/视图都会作为新表导入，并从元数据中填充所有列信息。 每个表都会创建一个分区，用于保存界面生成的 SQL 查询。

就这么简单！ 再也不用在 Tabular Editor 和 SSDT 之间来回切换了。

## 关于旧式数据源与 Structured数据源的说明

由于 Tabular Editor 目前无法推断 M（Power Query）表达式返回的元数据，因此该界面仅支持旧式（也称 Provider）数据源。 如果你必须使用 Structured数据源，仍然可以先使用临时的旧式连接来初始导入表架构（前提是你的数据源可通过 SQL、OLE DB 或 ODBC 访问），然后再手动将已导入表的分区切换为使用 Structured数据源。 如果你要从“特殊”的数据源导入数据，例如 Web 服务、Azure Data Lake Storage 等，则无法自动导入架构元数据，但[可以通过剪贴板提供元数据信息](/Importing-Tables#power-query-data-sources)。

不过，总的来说，建议对以下类型的数据源始终使用 Legacy 连接：

- SQL Server 数据库
- Azure SQL 数据库
- Azure SQL Data Warehouse
- Azure Databricks（通过 ODBC）
- 任何关系型 OLE DB 数据源
- 任何关系型 ODBC 数据源

若要使用 Azure Active Directory 并启用 MFA 进行身份验证，请参阅此处。

## 在没有现有数据源的情况下导入

如果你的模型尚未包含任何数据源，可以在“模型”菜单中点击“导入表...”来导入表。 界面如下：

![image](https://user-images.githubusercontent.com/8976200/49702141-74cdbe00-fbf5-11e8-8a88-5bc2a0a6c80d.png)

保持选择“创建新的数据源并将其添加到模型中”，点击“下一步”时会显示连接对话框界面。 在此对话框中，你可以指定连接信息：

![image](https://user-images.githubusercontent.com/8976200/49702167-a5adf300-fbf5-11e8-8d06-d6670ad456d4.png)

点击“确定”后，将在你的模型中创建一个使用所指定连接的（Legacy）数据源，并跳转到上方所示的导入页面。

列表中的下一个选项“使用临时连接”不会在模型中添加新的数据源。 这意味着在部署模型之前，你需要自行将数据源分配给新导入表的分区。

最后一个选项“从另一个应用程序手动导入元数据”，用于在你希望基于列元数据列表导入新表时使用。 这对结构化（Power Query）数据源很有用，[见下文](/Importing-Tables#power-query-data-sources)。

## SQL 功能

对于非 SQL Server 数据源（更准确地说，不使用 Native SQL Client 驱动程序的数据源），请留意屏幕底部附近的两个下拉框：

![image](https://user-images.githubusercontent.com/8976200/51613859-b952b600-1f24-11e9-8fd7-7c5269aaab26.png)

“使用以下方式减少行数”下拉框可让你指定从数据源查询预览数据时使用哪种行数限制子句，因为表导入向导只会从源表或视图中检索 200 行数据。 你可以在最常见的行数限制子句之间进行选择，例如“TOP”“LIMIT”“FETCH FIRST”等。

“标识符引号”下拉列表用于指定在生成的 SQL 语句中，对象名称（列、表）应如何加引号。 这同样适用于数据预览，以及在将表导入表格模型时，用于表分区查询的 SQL 语句。 默认使用方括号，但你也可以将其更改为其他常见的标识符引号类型。

## 更改表的数据源

打开导入页面的另一种方式是：在现有表（使用旧版数据源）上右键单击，然后选择“选择列...”。 如果该表之前是通过 UI 导入的，那么导入页面应会显示出来，并预先选中源表/视图以及已导入的列。 你可以添加/移除列，甚至选择完全不同的表来替换模型中你所选的那张表进行导入。 注意：表中任何被取消选择的列，或在源表/视图中已不存在的列，都会从你的模型中移除。 你始终可以使用 CTRL+Z 撤销此类操作。

<a name="refreshing-table-metadata"></a>

## 刷新表元数据

从 2.8 版本开始，Tabular Editor 新增了一项 UI 功能，让你可以更轻松地检查架构漂移。 即检测列的数据类型是否发生更改，或源表和视图中是否新增或删除了列。 你可以在模型级别（同样仅适用于旧版数据源）、数据源级别、表级别或分区级别触发此检查。 做法是右键单击该对象，然后选择“刷新表元数据...”……

![image](https://user-images.githubusercontent.com/8976200/49702346-7e582580-fbf7-11e8-9a62-04c6963179e5.png)

变更检测基于各表中所有数据列的“源列”和“数据类型”属性。 如果检测到任何变更，Tabular Editor 将显示上述 UI，并详细列出这些变更。 你可以取消勾选不想应用到模型中的变更，但要注意，某些变更可能会导致处理错误（例如源表/视图/查询中不存在的源列）。

该机制（以及导入表 UI）在从数据源查询元数据时会使用 FormatOnly-flag。 这意味着你可以让表分区使用存储过程。 FormatOnly-flag 可确保不会直接执行该存储过程。 取而代之的是，服务器会执行静态分析，仅返回元数据，用于描述该存储过程在执行时会返回的结果集。 取决于所使用的 RDBMS，FormatOnly-flag 与存储过程一起使用时可能存在一些限制。 有关在以 SQL Server 作为数据源时的更多信息，请参阅[这篇文章](https://docs.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-describe-first-result-set-transact-sql?view=sql-server-2017#remarks)。

### CLI 支持

你可以通过命令行使用 `-SC` 标志，在模型级别执行架构检查。 注意，通过 CLI 执行架构检查时，只会 Report 映射问题。 它不会对你的模型做任何更改。 如果你在 CI/CD 流水线中使用 Tabular Editor，这会很有用，因为映射问题可能会在将模型部署到测试/生产环境后引发问题。

<a name="ignoring-objects"></a>

### 忽略对象

从 Tabular Editor 2.9.8 开始，你可以在架构检查或元数据刷新时排除对象。 这可以通过在你希望排除的对象上设置注释来控制。 注释名称请使用下面列出的代码。 注释值可以留空，或设置为 "1"、"true" 或 "yes"。 将注释值设置为 "0"、"false" 或 "no" 会等效于禁用该注释，就像它不存在一样：

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

默认情况下，当某个分区查询无法执行，或导入表包含一个在源查询中找不到任何对应列的列时，CLI 会 Report 错误。 当某列的数据类型与源查询中的列不一致，或源查询包含未映射到导入表任何列的列时，CLI 会 Report 警告。 当同一张表的不同分区的源查询返回的列不一致时，CLI 也会 Report 警告。

从 Tabular Editor 2.14.1 版本开始，你可以更改 CLI 的行为，使上面列出的所有警告都以错误的形式 Report。 要实现这一点，请在 **模型** 级别添加以下注释：

- `TabularEditor_SchemaCheckNoWarnings`：让 Tabular Editor 将所有架构检查警告都视为错误。

## 启用 MFA 的 Azure Active Directory

如果你想从 Azure SQL 数据库或 Azure Synapse SQL 池导入表，很可能需要 Azure Active Directory 多因素身份验证。 遗憾的是，.NET Framework 中使用的 SQL Native Client 提供程序不支持这种方式。 请改用 MSOLEDBSQL 提供程序（另外一个好处是，当 Analysis Services 从表中读取数据时，它通常比 SQL Native Client 更快）。 要让它在你的本机上正常工作，记得安装这个驱动程序的[最新（x86）版本](https://docs.microsoft.com/en-us/sql/connect/oledb/download-oledb-driver-for-sql-server?view=sql-server-ver15)。

下面是将数据源设置为支持 MFA 的分步说明：

1. 创建一个新的旧版数据源，并将其添加到模型中。 模型 > 新建数据源（旧版）
2. 将 Provider 属性设置为 `System.Data.OleDb`，并使用如下所示的连接字符串，将服务器、数据库和用户名替换为正确的值：

### 适用于 Synapse SQL 池：

```
Provider=MSOLEDBSQL;Data Source=<synapse workspace name>-ondemand.sql.azuresynapse.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

### 适用于 Azure SQL 数据库：

```
Provider=MSOLEDBSQL;Data Source=<sql server name>.database.windows.net;User ID=daniel@adventureworks.com;Database=<database name>;Authentication=ActiveDirectoryInteractive
```

3. 要从该数据源导入表，请右键单击该数据源并选择“导入表...”。随后会打开“导入表”向导界面，显示来自该数据源的表/视图列表。 注意：对于 Synapse SQL 池，你可能需要将行子句指定为“TOP (without NOLOCK)”，以便数据预览正常工作。
4. 将模型部署到 Analysis Services 时，你很可能需要指定其他凭据，例如服务主体应用程序 ID 和机密或 SQL 帐户，以便 Analysis Services 在刷新表数据时能够针对源完成身份验证。 这可以在部署后通过 TMSL 或 SSMS 来指定；也可以将其作为[CI/CD 部署流水线的一部分](https://tabulareditor.com/blog/youre-deploying-it-wrong-as-edition-part-5#creating-your-first-release-pipeline)进行设置。

## 手动导入架构/元数据

如果你使用的数据源不受“导入表”向导支持，可以选择手动导入元数据。 此选项提供一个界面：你可以在左侧输入或粘贴表架构，系统会自动解析其中的列名和数据类型信息。 或者，你也可以在右侧手动逐列输入列名，并在下拉列表中选择数据类型。 无论哪种方式，都比在主界面中手动创建表并逐个添加数据列更快。 完成后，点击“Import!”，并调整表名称和分区表达式。

在解析左侧文本时，Tabular Editor 会搜索某些关键字，以确定这些信息的结构。 它在解析数据时相当宽容，因此你可以例如直接粘贴 CREATE TABLE SQL 脚本中的列清单，或粘贴下文所述的 Power Query `Table.Schema(...)` 函数输出。 唯一的要求是：每行文本都代表源数据中的一列。

![image](https://user-images.githubusercontent.com/8976200/70419758-6f07f400-1a66-11ea-838d-9a587c8021ca.png)

## Power Query 数据源

由于没有官方支持的方式来执行或验证 Power Query/M 表达式，Tabular Editor 对 Power Query 数据源仅提供有限支持。 自 2.9.0 起，你可以使用上文所述的“导入表向导”中的“从另一个应用程序手动导入元数据”选项，从 Excel 或 Power BI Desktop 中的 Power Query 查询导入架构。 工作流如下：

- 首先，确保你的模型包含一个 Power Query 数据源。 右键单击“数据源”>“新建数据源 (Power Query)”。 如果你要从 SQL Server 加载数据，将协议指定为“tds”，并填写 Database、Server 和 AuthenticationKind 属性。
  ![image](https://user-images.githubusercontent.com/8976200/70418811-6dd5c780-1a64-11ea-8332-d074c6b2d5c2.png)
- 对于其他类型的数据源，可能更方便的做法是先在 SSDT 中创建初始模型和前几张表，以弄清楚数据源应如何配置；之后在添加更多表时再使用下面的技巧。
- 在 Excel 或 Power BI Desktop 里使用 Power Query 连接到源数据，并应用需要的转换。
- 在 Power Query 的“高级编辑器”中，添加一个步骤，对上一步的输出调用 `Table.Schema(...)` [M 函数](https://docs.microsoft.com/en-us/powerquery-m/table-schema)：
  ![image](https://user-images.githubusercontent.com/8976200/70416018-5562ae80-1a5e-11ea-8962-529304ce83f0.png)
- 选择完整的输出预览，将其复制到剪贴板（CTRL+A、CTRL+C），然后粘贴到“导入表向导”中的架构/元数据文本框里：
  ![image](https://user-images.githubusercontent.com/8976200/70416817-2e0ce100-1a60-11ea-9e2b-430cecf88d0a.png)
- 单击“Import!”，并为表指定一个合适的名称。
- 最后，将你在 Excel/Power BI 中使用的原始 M 表达式（即在用 `Table.Schema(...)` 函数修改之前的版本）粘贴到新建表的分区中。 修改该 M 表达式，使其指向你在第一步中指定的源：
  ![image](https://user-images.githubusercontent.com/8976200/70418985-dae95d00-1a64-11ea-8bfb-8dda16c33742.png)
