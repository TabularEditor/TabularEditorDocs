---
uid: useful-script-snippets
title: 实用脚本片段
author: Daniel Otykier
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

# 实用脚本片段

这里汇总了一些小脚本片段，帮助你开始使用 Tabular Editor 的 [高级脚本功能](/Advanced-Scripting)。 其中许多脚本都适合保存为 [自定义操作](/Custom-Actions)，这样你就能从上下文菜单中轻松重复使用它们。'

另外，也别忘了看看我们的脚本库 @csharp-script-library，里面有更多贴近实战的示例，展示你可以用 Tabular Editor 的脚本能力做些什么。

***

## 从列创建度量值

```csharp
// 为每个当前选中的列创建一个 SUM 度量值，并隐藏该列。
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Sum of " + c.Name,                    // 名称
        "SUM(" + c.DaxObjectFullName + ")",    // DAX 表达式
        c.DisplayFolder                        // 显示文件夹
    );
    
    // 为新度量值设置格式字符串：
    newMeasure.FormatString = "0.00";

    // 提供一些说明文档：
    newMeasure.Description = "此度量值是对列求和 " + c.DaxObjectFullName;

    // 隐藏基础列：
    c.IsHidden = true;
}
```

此片段使用 `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` 函数，在表上创建一个新的度量值。 我们使用 `DaxObjectFullName` 属性来获取列的完全限定名称，用于 DAX 表达式：`'TableName'[ColumnName]`。

***

## 生成时间智能度量值

首先，为各个时间智能汇总分别创建自定义操作。 例如：

```csharp
// 为每个选中的度量值创建一个 TOTALYTD 度量值。
foreach(var m in Selected.Measures) {
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // 名称
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX 表达式
        m.DisplayFolder                                        // 显示文件夹
    );
}
```

这里我们使用 `DaxObjectName` 属性来生成用于 DAX 表达式的非限定引用，因为这是一个度量值：`[MeasureName]`。 将其保存为名为 "Time Intelligence\Create YTD measure" 的自定义操作，并将其应用于度量值。 按同样方式为 MTD、LY，以及你需要的其他项创建操作。 然后，创建下面这个新操作：

```csharp
// 调用所有时间智能自定义操作:
CustomAction(@"Time Intelligence\\Create YTD measure");
CustomAction(@"Time Intelligence\\Create MTD measure");
CustomAction(@"Time Intelligence\\Create LY measure");
```

这展示了如何在另一个操作内部执行一个（或多个）自定义操作（注意避免循环引用——这会导致 Tabular Editor 崩溃）。 将其另存为新的自定义操作“时间智能\以上全部”，即可一键生成所有时间智能度量值：

![image](https://user-images.githubusercontent.com/8976200/36632257-5565c8ca-197c-11e8-8498-82667b6e1049.png)

当然，您也可以将所有时间智能计算放入一个脚本中，如下所示：

```csharp
var dateColumn = "'Date'[Date]";

// 为每个所选度量值创建时间智能度量值：
foreach(var m in Selected.Measures) {
    // Year-to-date:
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // 显示文件夹
    );
    
    // Previous year:
    m.Table.AddMeasure(
        m.Name + " PY",                                       // Name
        "CALCULATE(" + m.DaxObjectName + ", SAMEPERIODLASTYEAR(" + dateColumn + "))",     // DAX expression
        m.DisplayFolder                                        // 显示文件夹
    );    
    
    // Year-over-year
    m.Table.AddMeasure(
        m.Name + " YoY",                                       // Name
        m.DaxObjectName + " - [" + m.Name + " PY]",            // DAX expression
        m.DisplayFolder                                        // 显示文件夹
    );
    
    // Year-over-year %:
    m.Table.AddMeasure(
        m.Name + " YoY%",                                       // Name
        "DIVIDE([" + m.Name + " YoY], [" + m.Name + " PY])",    // DAX expression
        m.DisplayFolder                                         // 显示文件夹
    ).FormatString = "0.0 %";                                   // Set format string as percentage
    
    // Quarter-to-date:
    m.Table.AddMeasure(
        m.Name + " QTD",                                            // Name
        "TOTALQTD(" + m.DaxObjectName + ", " + dateColumn + ")",    // DAX expression
        m.DisplayFolder                                             // 显示文件夹
    );
    
    // Month-to-date:
    m.Table.AddMeasure(
        m.Name + " MTD",                                       // Name
        "TOTALMTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // 显示文件夹
    );
}
```

### 包含其他属性

如果您想为新建的度量值设置其他属性，可以将上述脚本修改如下：

```csharp
// 为每个所选度量值创建一个 TOTALYTD 度量值。
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // 显示文件夹
    );
    newMeasure.FormatString = m.FormatString;               // 从原始度量值复制格式字符串
    foreach(var c in Model.Cultures) {
        newMeasure.TranslatedNames[c] = m.TranslatedNames[c] + " YTD"; // 为每个区域设置复制翻译名称
        newMeasure.TranslatedDisplayFolders[c] = m.TranslatedDisplayFolders[c]; // 复制翻译后的显示文件夹
    }
}
```

***

## 设置默认翻译

有时，为所有（可见的）对象应用默认翻译会很方便。 在这种情况下，默认翻译就是对象的原始名称/说明/显示文件夹。 这样做的一个好处是：以 JSON 格式导出翻译时会包含所有翻译对象，即可用于 [SSAS Tabular Translator](https://www.sqlbi.com/tools/ssas-tabular-translator/)。

下面的脚本会遍历模型中的所有区域设置；对每个可见对象，如果还没有翻译，就会为其分配默认值：

```csharp
// 将默认翻译应用到模型中所有区域设置下的所有（可见）可翻译对象：
foreach(var culture in Model.Cultures)
{
    ApplyDefaultTranslation(Model, culture);
    foreach(var perspective in Model.Perspectives)
        ApplyDefaultTranslation(perspective, culture);
    foreach(var table in Model.Tables.Where(t => t.IsVisible))
        ApplyDefaultTranslation(table, culture);
    foreach(var measure in Model.AllMeasures.Where(m => m.IsVisible))
        ApplyDefaultTranslation(measure, culture);
    foreach(var column in Model.AllColumns.Where(c => c.IsVisible))
        ApplyDefaultTranslation(column, culture);
    foreach(var hierarchy in Model.AllHierarchies.Where(h => h.IsVisible))
        ApplyDefaultTranslation(hierarchy, culture);
    foreach(var level in Model.AllLevels.Where(l => l.Hierarchy.IsVisible))
        ApplyDefaultTranslation(level, culture);
}

void ApplyDefaultTranslation(ITranslatableObject obj, Culture culture)
{
    // 仅在尚不存在翻译时才应用默认翻译：
    if(string.IsNullOrEmpty(obj.TranslatedNames[culture]))
    {
        // 默认名称翻译：
        obj.TranslatedNames[culture] = obj.Name;

        // 默认说明翻译：
        var dObj = obj as IDescriptionObject;
        if(dObj != null && string.IsNullOrEmpty(obj.TranslatedDescriptions[culture])
            && !string.IsNullOrEmpty(dObj.Description))
        {
            obj.TranslatedDescriptions[culture] = dObj.Description;
        }

        // 默认显示文件夹翻译：
        var fObj = obj as IFolderObject;
        if(fObj != null && string.IsNullOrEmpty(fObj.TranslatedDisplayFolders[culture])
            && !string.IsNullOrEmpty(fObj.DisplayFolder))
        {
            fObj.TranslatedDisplayFolders[culture] = fObj.DisplayFolder;
        }
    }
}
```

***

## 处理透视

度量值、列、层级结构和表都提供 `InPerspective` 属性。该属性会为模型中的每个透视保存一个 True/False 值，用于指示给定对象是否属于该透视。 例如：

```csharp
foreach(var measure in Selected.Measures)
{
    measure.InPerspective["Inventory"] = true;
    measure.InPerspective["Reseller Operation"] = false;
}
```

上面的脚本确保所有选中的度量值在 "Inventory" 透视中可见，并在 "Reseller Operation" 透视中隐藏。

除了获取/设置单个透视中的成员关系之外，`InPerspective` 属性还支持以下方法：

- `<<object>>.InPerspective.None()` - 将对象从所有透视中移除。
- `<<object>>.InPerspective.All()` - 将对象包含在所有透视中。
- `<<object>>.CopyFrom(string[] perspectives)` - 将对象包含在所有指定的透视中（包含透视名称的字符串数组）。
- `<<object>>.CopyFrom(perspectiveIndexer perspectives)` - 从另一个 `InPerspective` 属性复制透视包含关系。

后者可用于将一个对象的透视成员关系复制到另一个对象。 例如，假设你有一个基准度量值 [Reseller Total Sales]，并希望确保当前选中的所有度量值都在与该基准度量值相同的透视中可见。 下面的脚本即可实现：

```csharp
var baseMeasure = Model.Tables["Reseller Sales"].Measures["Reseller Total Sales"];

foreach(var measure in Selected.Measures)
{
    /* 如果你希望在 'baseMeasure' 被隐藏的那些透视中，也隐藏 'measure'，
       请取消注释下面这一行： */
    // measure.InPerspective.None();

    measure.InPerspective.CopyFrom(baseMeasure.InPerspective);
}
```

在通过代码生成新对象时，也可以使用这种技巧。 例如，如果我们希望确保自动生成的时间智能度量值只在其基础度量值所在的透视中可见，我们可以在上一节脚本的基础上扩展为：

```csharp
// 为每个选中的度量值创建一个 TOTALYTD 度量值。
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // 名称
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX 表达式
        m.DisplayFolder                                        // 显示文件夹
    );
    newMeasure.InPerspective.CopyFrom(m.InPerspective);        // 从基础度量值复制透视设置
}
```

***

## 生成分区

如果你需要为某个表进行自定义分区，C# Script 可以帮助你快速生成大量分区。 基本思路是：在表上添加一个注释，其中包含要作为每个分区模板的 SQL 或 M 查询。 脚本随后会按需替换筛选参数。 例如，使用 SQL 分区时，我们可以添加一个名为 `PartitionTemplateSQL` 的注释，并将其值设置为 `SELECT * FROM fact_ResellerSales WHERE CalendarID BETWEEN {0} AND {1}`。 在生成最终分区时，脚本会用实际值替换 `{0}` 和 `{1}` 占位符。 在这个例子中，`CalendarID` 是一个整数。但一般来说，你需要自行确保最终生成的字符串是有效的 SQL（或 M）查询。

![](https://user-images.githubusercontent.com/8976200/70135273-07c6fa00-168a-11ea-84f6-90f0b3498ed8.png)

这里的示例每月生成一个分区。 选择一个已分配 `PartitionTemplateSQL` 注释的表，然后运行脚本。

```csharp
var firstPartition = new DateTime(2018,1,1); // 第一个分区日期
var lastPartition = new DateTime(2020,12,1); // 最后一个分区日期

var templateSql = Selected.Table.GetAnnotation("PartitionTemplateSQL");
if(string.IsNullOrEmpty(templateSql)) throw new Exception("No partition template!");

var currentPartition = firstPartition;
while(currentPartition <= lastPartition)
{
    // 基于 currentPartition 日期，计算起止 CalendarID（整数值）：
    var calendarIdFrom = currentPartition.ToString("yyyyMMdd");
    var calendarIdTo = currentPartition.AddMonths(1).AddDays(-1).ToString("yyyyMMdd");
    
    // 为分区确定一个唯一名称——因为我们按月分区，所以直接使用 yyyyMM：
    var partitionName = Selected.Table.Name + "_" + currentPartition.ToString("yyyyMM");
    
    // 将分区模板 SQL 中的占位符值替换为实际值：
    var partitionQuery = string.Format(templateSql, calendarIdFrom, calendarIdTo);
    
    // 创建分区（如果你使用的是 M 查询模板而不是 SQL，请改用 .AddMPartition）：
    Selected.Table.AddPartition(partitionName, partitionQuery);
    
    // 递增到下一个月（如需更多或更少的分区，可改为 .AddDays、.AddYears 等）：
    currentPartition = currentPartition.AddMonths(1);
}
```

***

## 将对象属性导出到文件

在某些工作流中，使用 Excel 批量编辑多个对象属性会很有用。 使用以下代码片段将一组标准属性导出到 .TSV 文件，之后还可以再导入（见下文）。

```csharp
// 导出当前选中对象的属性:
var tsv = ExportProperties(Selected);
SaveFile("Exported Properties 1.tsv", tsv);
```

生成的 .TSV 文件在 Excel 中打开后如下所示：
![image](https://user-images.githubusercontent.com/8976200/36632472-e8e96ef6-197e-11e8-8285-6816b09ad036.png)
第一列（Object）中的内容是该对象的引用。 如果修改了这一列的内容，后续导入属性时可能无法正常工作。 若要更改对象名称，只需修改第二列（Name）的值。

默认情况下，文件会保存到与 TabularEditor.exe 所在相同的文件夹。 默认情况下，仅导出以下属性（是否适用取决于导出对象的类型）：

- 名称
- 描述
- 源列
- 表达式
- 格式字符串
- 数据类型

要导出不同的属性，请将要导出的属性名称以逗号分隔，作为 `ExportProperties` 的第二个参数提供：

```csharp
// 导出当前选中表中所有度量值的名称和明细行表达式:
var tsv = ExportProperties(Selected.Table.Measures, "Name,DetailRowsExpression");
SaveFile("Exported Properties 2.tsv", tsv);
```

可用的属性名称可在 [TOM API 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.aspx) 中查看。 这些名称大多与 Tabular Editor 属性网格中显示的名称一致：采用 CamelCase，并移除了空格（也有少数例外，例如，“Hidden” 属性在 TOM API 中名为 `IsHidden`）。

要导入属性，请使用以下代码片段：

```csharp
// 导入并应用指定文件中的属性:
var tsv = ReadFile("Exported Properties 1.tsv");
ImportProperties(tsv);
```

### 导出带索引的属性

从 Tabular Editor 2.11.0 开始，`ExportProperties` 和 `ImportProperties` 方法支持带索引的属性。 带索引的属性是指除了属性名之外，还需要一个键的属性。 例如：`myMeasure.TranslatedNames`。 该属性表示为 `myMeasure` 提供名称翻译的所有字符串集合。 在 C# 中，你可以使用索引运算符访问特定区域设置的译名：`myMeasure.TranslatedNames["da-DK"]`。

简而言之，你现在可以导出 Tabular 模型中对象的所有翻译、透视信息、注释、扩展属性，以及行级安全性和对象级安全性信息。

例如，下面的脚本会生成一个 TSV 文件，包含模型中的所有度量值，以及每个度量值在哪些透视中可见：

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective");
SaveFile(@"c:\Project\MeasurePerspectives.tsv", tsv);
```

在 Excel 中打开后，这个 TSV 文件如下所示：

![image](https://user-images.githubusercontent.com/8976200/85208532-956dec80-b331-11ea-8568-32dbd4cc5516.png)

如上所示，你可以直接在 Excel 中修改内容，保存后再使用 `ImportProperties` 将更新后的值导入回 Tabular Editor。

如果你只想列出某一个或少数几个特定的透视，可以在调用 `ExportProperties` 时的第二个参数中指定它们：

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective[Inventory]");
SaveFile(@"c:\Project\MeasurePerspectiveInventory.tsv", tsv);
```

同样地，翻译、批注等也是如此。 例如，如果您想查看应用到表、列、层次结构、级别和度量值的所有丹麦语翻译：

```csharp
// Construct a list of objects:
var objects = new List<TabularNamedObject>();
objects.AddRange(Model.Tables);
objects.AddRange(Model.AllColumns);
objects.AddRange(Model.AllHierarchies);
objects.AddRange(Model.AllLevels);
objects.AddRange(Model.AllMeasures);

var tsv = ExportProperties(objects, "Name,TranslatedNames[da-DK],TranslatedDescriptions[da-DK],TranslatedDisplayFolders[da-DK]");
SaveFile(@"c:\Project\ObjectTranslations.tsv", tsv);
```

***

## 生成文档

上面展示的 `ExportProperties` 方法也可用于记录您的模型的全部或部分内容。 下面的代码片段会从表格模型中的所有可见度量值或列提取一组属性，并将其保存为 TSV 文件：

```csharp
// Construct a list of all visible columns and measures:
var objects = Model.AllMeasures.Where(m => !m.IsHidden && !m.Table.IsHidden).Cast<ITabularNamedObject>()
      .Concat(Model.AllColumns.Where(c => !c.IsHidden && !c.Table.IsHidden));

// Get their properties in TSV format (tabulator-separated):
var tsv = ExportProperties(objects,"Name,ObjectType,Parent,Description,FormatString,DataType,Expression");

// (Optional) Output to screen (can then be copy-pasted into Excel):
// tsv.Output();

// ...or save the TSV to a file:
SaveFile("documentation.tsv", tsv);
```

***

## 从文件生成度量值

上述导出/导入属性的技巧，适用于你想要对模型中_已有_对象的属性进行批量编辑的场景。 如果你想导入一份尚不存在的度量值列表呢？

假设你有一个 TSV（制表符分隔值）文件，其中包含你希望导入到现有表格模型中的度量值名称、说明和 DAX 表达式。 你可以使用下面的脚本读取该文件，将其拆分为行与列，并生成这些度量值。 该脚本还会为每个度量值设置一个特殊注释，以便删除之前通过同一脚本创建的度量值。

```csharp
var targetTable = Model.Tables["Program"];  // 应保存度量值的表的名称
var measureMetadata = ReadFile(@"c:\Test\MyMeasures.tsv");   // c:\Test\MyMeasures.tsv 是一个包含标题行和 3 列：Name、Description、Expression 的制表符分隔文件

// 删除目标表中所有带有值为 "1" 的 "AUTOGEN" 注释的度量值：
foreach(var m in targetTable.Measures.Where(m => m.GetAnnotation("AUTOGEN") == "1").ToList())
{
    m.Delete();
}

// 按 CR 和 LF 字符将文件拆分为行：
var tsvRows = measureMetadata.Split(new[] {'\r','\n'},StringSplitOptions.RemoveEmptyEntries);

// 遍历所有行，但跳过第一行：
foreach(var row in tsvRows.Skip(1))
{
    var tsvColumns = row.Split('\t');     // 假设文件使用制表符作为列分隔符
    var name = tsvColumns[0];             // 第 1 列包含度量值名称
    var description = tsvColumns[1];      // 第 2 列包含度量值说明
    var expression = tsvColumns[2];       // 第 3 列包含度量值表达式

    // 这假设模型中尚不存在同名的度量值（如果存在，新度量值将获得一个数字后缀）：
    var measure = targetTable.AddMeasure(name);
    measure.Description = description;
    measure.Expression = expression;
    measure.SetAnnotation("AUTOGEN", "1");  // 在该度量值上设置一个特殊注释，以便下次执行脚本时找到并删除它。
}
```

如果你需要将此流程自动化，请将上面的脚本保存到文件中，然后按如下方式使用 [Tabular Editor CLI](/Command-line-Options)：

```powershell
start /wait TabularEditor.exe "<path to bim file>" -S "<path to script file>" -B "<path to modified bim file>"
```

例如：

```powershell
start /wait TabularEditor.exe "c:\Projects\AdventureWorks\Model.bim" -S "c:\Projects\AutogenMeasures.cs" -B "c:\Projects\AdventureWorks\Build\Model.bim"
```

……或者，如希望针对已部署的数据库运行该脚本：

```powershell
start /wait TabularEditor.exe "localhost" "AdventureWorks" -S "c:\Projects\AutogenMeasures.cs" -D "localhost" "AdventureWorks" -O
```

***

## 从分区源元数据创建数据列

> [!NOTE]
> The `RefreshDataColumns()` method described below is only available in **Tabular Editor 2**. In Tabular Editor 3, use the **Import Table...** feature instead.

如果某个表使用基于 OLE DB 提供程序数据源的查询分区，我们可以通过执行以下代码片段自动刷新该表的列元数据：

```csharp
Model.Tables["Reseller Sales"].RefreshDataColumns();
```

这在向模型中添加新表时很有用，可以避免在表上逐个手动创建每个数据列。 上面的代码片段假设可以在本地访问分区源，并使用“Reseller Sales”表分区源的现有连接字符串。 上面的代码片段会从分区查询中提取架构，并为源查询中的每一列在表上添加一个数据列。

如果需要为此操作提供不同的连接字符串，也可以在代码片段中指定：

```csharp
var source = Model.DataSources["DWH"] as ProviderDataSource;
var oldConnectionString = source.ConnectionString;
source.ConnectionString = "...";   // Enter the connection string you want to use for metadata refresh
Model.Tables["Reseller Sales"].RefreshDataColumns();
source.ConnectionString = oldConnectionString;
```

这假设“Reseller Sales”表的分区使用名为“DWH”的 Provider数据源。

***

## 格式化 DAX 表达式

更多信息请参阅 [FormatDax](/FormatDax)。

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
Selected.Measures.FormatDax();
```

替代语法：

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
foreach(var m in Selected.Measures)
    m.FormatDax();
```

***

## 为表生成源列列表

以下脚本会为当前选中的表输出一份格式良好的源列列表。 如果你想把使用 `SELECT *` 的分区查询替换为显式列清单，这会很有用。

```csharp
string.Join(",\r\n", 
    Selected.Table.DataColumns
        .OrderBy(c => c.SourceColumn)
        .Select(c => "[" + c.SourceColumn + "]")
    ).Output();
```

***

## 自动创建关系

如果你的团队始终遵循一套固定的命名规范，你会很快发现脚本能发挥更大的作用。

以下脚本在一个或多个事实表上执行时，会根据列名自动创建到所有相关维度表的关系。 脚本会查找事实表中名称符合 `xxxyyyKey` 模式的列，其中 xxx 是可选的限定词，用于角色扮演用途，yyy 是维度表名称。 在维度表上，必须存在名为 `yyyKey` 的列，并且其数据类型要与事实表上的对应列相同。 例如，名为“ProductKey”的列会与 Product 表中的“ProductKey”列建立关系。 你可以指定一个不同的列名后缀来替代“Key”。

如果事实表与维度表之间已存在关系，脚本会将新创建的关系设为非活动状态。

```csharp
var keySuffix = "Key";

// Loop through all currently selected tables (assumed to be fact tables):
foreach(var fact in Selected.Tables)
{
    // Loop through all SK columns on the current table:
    foreach(var factColumn in fact.Columns.Where(c => c.Name.EndsWith(keySuffix)))
    {
        // Find the dimension table corresponding to the current SK column:
        var dim = Model.Tables.FirstOrDefault(t => factColumn.Name.EndsWith(t.Name + keySuffix));
        if(dim != null)
        {
            // Find the key column on the dimension table:
            var dimColumn = dim.Columns.FirstOrDefault(c => factColumn.Name.EndsWith(c.Name));
            if(dimColumn != null)
            {
                // Check whether a relationship already exists between the two columns:
                if(!Model.Relationships.Any(r => r.FromColumn == factColumn && r.ToColumn == dimColumn))
                {
                    // If relationships already exists between the two tables, new relationships will be created as inactive:
                    var makeInactive = Model.Relationships.Any(r => r.FromTable == fact && r.ToTable == dim);

                    // Add the new relationship:
                    var rel = Model.AddRelationship();
                    rel.FromColumn = factColumn;
                    rel.ToColumn = dimColumn;
                    factColumn.IsHidden = true;
                    if(makeInactive) rel.IsActive = false;
                }
            }
        }
    }
}
```

***

## 创建 DumpFilters 度量值

受[这篇文章](https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/)启发，下面的脚本会在当前所选表中创建一个名为 [DumpFilters] 的度量值：

```csharp
var dax = "VAR MaxFilters = 3 RETURN ";
var dumpFilterDax = @"IF (
    ISFILTERED ( {0} ), 
    VAR ___f = FILTERS ( {0} )
    VAR ___r = COUNTROWS ( ___f )
    VAR ___t = TOPN ( MaxFilters, ___f, {0} )
    VAR ___d = CONCATENATEX ( ___t, {0}, "", "" )
    VAR ___x = ""{0} = "" & ___d 
        & IF(___r > MaxFilters, "", ... ["" & ___r & "" items selected]"") & "" ""
    RETURN ___x & UNICHAR(13) & UNICHAR(10)
)";

// 遍历模型的所有列，构建完整的 DAX 表达式：
bool first = true;
foreach(var column in Model.AllColumns)
{
    if(!first) dax += " & ";
    dax += string.Format(dumpFilterDax, column.DaxObjectFullName);
    if(first) first = false;
}

// 将度量值添加到当前选中的表：
Selected.Table.AddMeasure("DumpFilters", dax);
```

***

## 将 CamelCase 转换为 Proper Case

在关系数据库中，列和表常见的一种命名方式是 CamelCase。 也就是说，名称不包含空格，每个单词都以大写字母开头。 在 Tabular 模型中，未隐藏的表和列会对业务用户可见，因此通常更适合采用更“易读”的命名方式。 下面的脚本会将 CamelCase 命名转换为 Proper Case。 连续的大写字母序列会保持原样（缩写）。 例如，该脚本会转换以下内容：

- `CustomerWorkZipcode` 转为 `Customer Work Zipcode`
- `CustomerAccountID` 转为 `Customer Account ID`
- `NSASecurityID` 转为 `NSA Security ID`

强烈建议将此脚本保存为适用于所有对象类型的自定义操作（关系、KPI、表格权限和翻译除外，因为这些对象没有可编辑的“Name”属性）：

```csharp
foreach(var obj in Selected.OfType<ITabularNamedObject>()) {
    var oldName = obj.Name;
    var newName = new System.Text.StringBuilder();
    for(int i = 0; i < oldName.Length; i++) {
        // 首字母始终大写：
        if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

        // 两个大写字母后面紧跟一个小写字母的序列，需要在第一个字母后插入空格：
        else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }

        // 其他所有“小写字母 + 大写字母”的序列，需要在第一个字母后插入空格：
        else if(i + 1 < oldName.Length && char.IsLower(oldName[i]) && char.IsUpper(oldName[i+1]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }
        else
        {
            newName.Append(oldName[i]);
        }
    }
    obj.Name = newName.ToString();
}
```

***

## 导出表与度量值之间的依赖关系

假设你有一个庞大而复杂的模型，并且想知道哪些度量值可能会受到基础数据变更的影响。

下面的脚本会遍历模型中的所有度量值，并为每个度量值输出它所依赖的表清单——包括直接依赖与间接依赖。 该列表会以制表符分隔的文件形式输出。

```csharp
string tsv = "Measure\tDependsOnTable"; // TSV 文件表头行

// 遍历所有度量值：
foreach(var m in Model.AllMeasures) {

    // 获取该度量值引用的 ALL 对象列表（既包括直接引用，也包括通过其他度量值间接引用）：
    var allReferences = m.DependsOn.Deep();

    // 将引用列表筛选为仅包含表的引用。对于列引用，获取该列所属的表。
    // 最后，仅保留不重复的表：
    var allTableReferences = allReferences.OfType<Table>()
        .Concat(allReferences.OfType<Column>().Select(c => c.Table)).Distinct();

    // 输出 TSV 行——每个表引用一行：
    foreach(var t in allTableReferences)
        tsv += string.Format("\r\n{0}\t{1}", m.Name, t.Name);
}
    
tsv.Output();   
// SaveFile("c:\\MyProjects\\SSAS\\MeasureTableDependencies.tsv", tsv); // 取消注释此行即可将输出保存到文件
```

***

## 设置聚合（仅限 Power BI Dataset）

自 [Tabular Editor 2.11.3](https://github.com/TabularEditor/TabularEditor/releases/tag/2.11.3) 起，你可以在列上设置 `AlternateOf` 属性，从而在模型中定义聚合表。 该功能可通过 Power BI 服务的 XMLA endpoint 用于 Power BI Dataset（兼容级别 1460 或更高）。

选中一组列并运行下面的脚本，以初始化它们的 `AlternateOf` 属性：

```csharp
foreach(var col in Selected.Columns) col.AddAlternateOf();
```

依次逐列处理，将其映射到基础列，并相应设置汇总方式（Sum/Min/Max/GroupBy）。 或者，如果你想自动化此流程，并且你的聚合表列与基础表列的名称完全相同，可以使用下面的脚本，它会为你自动映射这些列：

```csharp
// 在树中选择两张表（Ctrl+单击）。假定聚合表是列数最少的那一张。
// 此脚本会为聚合表上的所有列设置 AlternateOf 属性。要使脚本生效，聚合表列必须
// 与基础表列同名。
var aggTable = Selected.Tables.OrderBy(t => t.Columns.Count).First();
var baseTable = Selected.Tables.OrderByDescending(t => t.Columns.Count).First();

foreach(var col in aggTable.Columns)
{
    // 脚本会将汇总类型设置为 "Group By"，除非该列使用的数据类型为 decimal/double：
    var summarization = SummarizationType.GroupBy;
    if(col.DataType == DataType.Double || col.DataType == DataType.Decimal)
        summarization = SummarizationType.Sum;
    
    col.AddAlternateOf(baseTable.Columns[col.Name], summarization);
}
```

运行脚本后，你应该会看到聚合表上的所有列都已分配 `AlternateOf` 属性（见下方屏幕截图）。 请记住，基础表分区必须使用 DirectQuery，聚合才能生效。

![image](https://user-images.githubusercontent.com/8976200/85851134-6ed70800-b7ae-11ea-82eb-37fcaa2ca9c4.png)

***

## 查询 Analysis Services

从版本 [2.12.1](https://github.com/TabularEditor/TabularEditor/releases/tag/2.12.1) 开始，Tabular Editor 现已提供多种辅助方法，可针对你的模型执行 DAX 查询并对 DAX 表达式求值。 这些方法仅在模型元数据直接从 Analysis Services 实例加载时才适用，例如使用“File > Open > From DB...”选项，或使用 Tabular Editor 的 Power BI 外部工具集成功能时。

可用的方法如下：

| 方法                                                            | 说明                                                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void ExecuteCommand(string tmslOrXmla, bool isXmla = false)` | 此方法会将指定的 TMSL 或 XMLA 脚本传递给已连接的 Analysis Services 实例。 当你需要在 AS 实例上刷新某张表的数据时，这个方法很有用。 请注意，如果你使用此方法对模型进行元数据更改，你的本地模型元数据将与 AS 实例上的元数据不同步；下次尝试保存模型元数据时，可能会收到版本冲突警告。 如果要发送 XMLA 脚本，请将 `isXmla` 参数设置为 `true`。                                                                                             |
| `IDataReader ExecuteReader(string dax)`                       | 对已连接的 AS 数据库执行指定的 DAX _查询_，并返回生成的 [AmoDataReader](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.amodatareader?view=analysisservices-dotnet) 对象。 DAX 查询包含一个或多个 [`EVALUATE`](https://dax.guide/EVALUATE) 语句。 请注意，你不能同时打开多个数据读取器。 如果你忘记显式关闭或释放读取器，Tabular Editor 会自动将其关闭。    |
| `DataSet ExecuteDax(string dax)`                              | 对已连接的 AS 数据库执行指定的 DAX _查询_，并返回一个 [DataSet](https://docs.microsoft.com/en-us/dotnet/api/system.data.dataset?view=netframework-4.6) 对象，其中包含查询返回的数据。 DAX 查询包含一个或多个 [`EVALUATE`](https://dax.guide/EVALUATE) 语句。 返回的 DataSet 对象中，每个 `EVALUATE` 语句都会对应一个 DataTable。 不建议返回非常大的数据表，因为它们可能会导致内存不足或其他稳定性错误。 |
| `object EvaluateDax(string dax)`                              | 针对已连接的 AS 数据库执行指定的 DAX _表达式_，并返回一个表示结果的对象。 如果 DAX 表达式是标量，则会返回相应类型的对象（string、long、decimal、double、DateTime）。 如果 DAX 表达式为表值，则会返回 [DataTable](https://docs.microsoft.com/en-us/dotnet/api/system.data.datatable?view=netframework-4.6)。                                                                |

这些方法的作用域在 `Model.Database` 对象下，但也可以不加任何前缀直接执行。

Darren Gosbell 在[这里](https://darren.gosbell.com/2020/08/the-best-way-to-generate-data-driven-measures-in-power-bi-using-tabular-editor/)介绍了一个有趣的用例：使用 `ExecuteDax` 方法生成数据驱动的度量值。

另一种做法是创建一个可复用的脚本，用于刷新某个表。 例如，要执行重新计算，请使用以下代码：

```csharp
var type = "calculate";
var database = Model.Database.Name;
var table = Selected.Table.Name;
var tmsl = "{ \"refresh\": { \"type\": \"%type%\", \"objects\": [ { \"database\": \"%db%\", \"table\": \"%table%\" } ] } }"
    .Replace("%type%", type)
    .Replace("%db%", database)
    .Replace("%table%", table);

ExecuteCommand(tmsl);
```

### 清除 Analysis Services 引擎缓存

从 Tabular Editor 2.16.6 或 Tabular Editor 3.2.3 开始，你可以使用以下语法向 Analysis Services 发送原始 XMLA 命令。 下面的示例演示了如何使用它来清除 AS 引擎缓存：

```csharp
var clearCacheXmla = string.Format(@"<ClearCache xmlns=""http://schemas.microsoft.com/analysisservices/2003/engine"">  
  <Object>
    <DatabaseID>{0}</DatabaseID>
  </Object>
</ClearCache>", Model.Database.ID);

ExecuteCommand(clearCacheXmla, isXmla: true);
```

### 可视化查询结果

也可以使用 `Output` 辅助方法，直接将 `EvaluateDax` 返回的 DAX 表达式结果可视化：

```csharp
EvaluateDax("1 + 2").Output(); // An integer
EvaluateDax("\"Hello from AS\"").Output(); // A string
EvaluateDax("{ (1, 2, 3) }").Output(); // A table
```

![image](https://user-images.githubusercontent.com/8976200/91638299-bbd59580-ea0e-11ea-882b-55bff73c30fb.png)

……或者，如果想返回当前选中度量值的值：

```csharp
EvaluateDax(Selected.Measure.DaxObjectFullName).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638367-6f3e8a00-ea0f-11ea-90cd-7d2e4cff6e31.png)

下面是一个更高级的示例，可一次选择并对多个度量值求值：

```csharp
var dax = "ROW(" + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638356-546c1580-ea0f-11ea-8302-3e40829e00dd.png)

如果确实很熟练，可以使用 SUMMARIZECOLUMNS 或其他 DAX 函数，将选中的度量值按某个列进行切片并可视化：

```csharp
var dax = "SUMMARIZECOLUMNS('Product'[Color], " + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](https://user-images.githubusercontent.com/8976200/91638389-9b5a0b00-ea0f-11ea-819f-d3eee3ddfa71.png)

请记住，你可以点击脚本编辑器正上方的“+”图标，将这些脚本保存为自定义操作。 这样一来，你就能获得一套便于复用的 DAX 查询集合，并且可以直接在 Tabular Editor 的上下文菜单中执行和可视化：

![image](https://user-images.githubusercontent.com/8976200/91638790-305e0380-ea12-11ea-9d84-313f4388496f.png)

### 导出数据

你可以使用下面的脚本来执行一个 DAX 查询，并将结果流式写入文件（脚本使用制表符分隔格式）：

```csharp
using System.IO;

// 此脚本会执行一个 DAX 查询，并以制表符分隔的格式将结果写入文件：

var dax = "EVALUATE 'Customer'";
var file = @"c:\temp\file.csv";
var columnSeparator = "\t";

using(var daxReader = ExecuteReader(dax))
using(var fileWriter = new StreamWriter(file))
{
    // 写入列标题：
    fileWriter.WriteLine(string.Join(columnSeparator, Enumerable.Range(0, daxReader.FieldCount - 1).Select(f => daxReader.GetName(f))));

    while(daxReader.Read())
    {
        var rowValues = new object[daxReader.FieldCount];
        daxReader.GetValues(rowValues);
        var row = string.Join(columnSeparator, rowValues.Select(v => v == null ? "" : v.ToString()));
        fileWriter.WriteLine(row);
    }
}
```

如果你想到了这些方法的其他有趣用法，请考虑在[社区脚本 repository](https://github.com/TabularEditor/Scripts)中分享。 谢谢！

***

## 替换 Power Query 服务器和数据库名称

从基于 SQL Server 的数据源导入数据的 Power BI Dataset，通常会包含类似下面这样的 M 表达式。 Tabular Editor 很遗憾没有用于“解析”这类表达式的机制。不过，如果我们想在不知道原始值的情况下，将其中的服务器和数据库名称替换为其他内容，可以利用这样一个事实：这些值都被双引号括起来：

```M
let
    Source = Sql.Databases("devsql.database.windows.net"),
    AdventureWorksDW2017 = Source{[Name="AdventureWorks"]}[Data],
    dbo_DimProduct = AdventureWorksDW2017{[Schema="dbo",Item="DimProduct"]}[Data]
in
    dbo_DimProduct
```

下面的脚本会将第一个双引号中的值替换为服务器名称，并将第二个双引号中的值替换为数据库名称。 这两个替换值都从环境变量中读取：

```csharp
// 此脚本用于将所有 Power Query 分区中的服务器和数据库名称，
// 统一替换为通过环境变量提供的值：
var server = "\"" + Environment.GetEnvironmentVariable("SQLServerName") + "\"";
var database = "\"" + Environment.GetEnvironmentVariable("SQLDatabaseName") + "\"";

// 此函数会从 M 表达式中提取所有被引号括起来的值，并以字符串列表形式返回
// （按出现顺序）。但如果某个引号前面紧跟井号（#），则忽略该引号中的值：
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // 服务器名通常是遇到的第一个字符串
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // 数据库名通常是遇到的第二个字符串

// 遍历模型中的所有分区，将分区里原有的服务器和数据库名称替换为
// 环境变量中指定的值：
foreach(var p in Model.AllPartitions.OfType<MPartition>())
{
    if (p.Expression.Contains("Source = Sql.Database"))
        {
            var oldServer = "\"" + GetServer(p.Expression) + "\"";
            var oldDatabase = "\"" + GetDatabase(p.Expression) + "\"";
            p.Expression = p.Expression.Replace(oldServer, server).Replace(oldDatabase, database);
       }
}
```

***

## 将 Power Query 数据源和分区替换为 Legacy

如果你在处理一个基于 Power BI 的模型，并且该模型的分区使用 Power Query（M）表达式来访问基于 SQL Server 的数据源，那么你将无法使用 Tabular Editor 2 的数据导入向导，也无法执行架构检查（即，将导入的列与数据源中的列进行对比）。

要解决这个问题，你可以在模型上运行下面的脚本：它会将 Power Query 分区替换为对应的原生 SQL 查询分区，并在模型上创建一个 Legacy（提供程序）数据源，从而让 Tabular Editor 2 的“导入数据”向导可以正常工作：

脚本有两个版本：第一个版本为创建的 Legacy 数据源使用 MSOLEDBSQL 提供程序，并将凭据硬编码在脚本中。 这对于本地开发很有用。 第二个示例使用 SQLNCLI 提供程序，该提供程序在 Azure DevOps 的 Microsoft 托管构建代理上可用，并从环境变量中读取凭据以及服务器和数据库名称，因此适合集成到 Azure Pipelines 中。

MSOLEDBSQL 版本：从 M 分区读取连接信息，并通过 Azure AD 提示输入用户名和密码：

```csharp
#r "Microsoft.VisualBasic"

// 此脚本会将该模型上的所有 Power Query 分区替换为一个
// 使用所提供连接字符串、并采用 INTERACTIVE
// AAD 身份验证的 Legacy 分区。脚本假定所有 Power Query 分区
// 都从同一个基于 SQL Server 的数据源加载数据。

// 请提供以下信息：
var authMode = "ActiveDirectoryInteractive";
var userId = Microsoft.VisualBasic.Interaction.InputBox("输入你的 AAD 用户名", "用户名", "name@domain.com", 0, 0);
if(userId == "") return;
var password = ""; // 使用 ActiveDirectoryInteractive 身份验证时请留空

// 此函数会从 M 表达式中提取所有被引号括起来的值，并以字符串列表形式返回
// （按出现顺序）。但如果某个引号前面紧跟井号（#），则忽略该引号中的值：
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // 服务器名通常是遇到的第一个字符串
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // 数据库名通常是遇到的第二个字符串
var GetSchema = new Func<string, string>(m => split(m)[2]);    // 架构名通常是遇到的第三个字符串
var GetTable = new Func<string, string>(m => split(m)[3]);     // 表名通常是遇到的第四个字符串

var server = GetServer(Model.AllPartitions.OfType<MPartition>().First().Expression);
var database = GetDatabase(Model.AllPartitions.OfType<MPartition>().First().Expression);

// 向模型添加一个 Legacy 数据源：
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.OleDb";
ds.ConnectionString = string.Format(
    "Provider=MSOLEDBSQL;Data Source={0};Initial Catalog={1};Authentication={2};User ID={3};Password={4}",
    server,
    database,
    authMode,
    userId,
    password);

// 从所有表中移除 Power Query 分区，并将其替换为一个 Legacy 分区：
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```

SQLNCLI 版本：从环境变量读取连接信息：

```csharp
// 此脚本会将此模型中的所有 Power Query 分区替换为
// 一个传统分区，并从对应的环境变量中读取 SQL Server 名称、数据库名称、用户名
// 和密码。脚本假定
// 所有 Power Query 分区都从同一个基于 SQL Server 的
// 数据源加载数据。

var server = Environment.GetEnvironmentVariable("SQLServerName");
var database = Environment.GetEnvironmentVariable("SQLDatabaseName");
var userId = Environment.GetEnvironmentVariable("SQLUserName");
var password = Environment.GetEnvironmentVariable("SQLUserPassword");

// 此函数会从 M 表达式中提取所有加引号的值，返回一个字符串列表。
// 列表包含提取到的值（按顺序），但会忽略这样的加引号值：引号前紧跟一个井号 (#)。
var split = new Func<string, List<string>>(m => { 
    var result = new List<string>();
    var i = 0;
    foreach(var s in m.Split('"')) {
        if(s.EndsWith("#") && i % 2 == 0) i = -2;
        if(i >= 0 && i % 2 == 1) result.Add(s);
        i++;
    }
    return result;
});
var GetServer = new Func<string, string>(m => split(m)[0]);    // 服务器名称通常是第一个匹配到的字符串
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // 数据库名称通常是第二个匹配到的字符串
var GetSchema = new Func<string, string>(m => split(m)[2]);    // 架构名称通常是第三个匹配到的字符串
var GetTable = new Func<string, string>(m => split(m)[3]);     // 表名称通常是第四个匹配到的字符串

// 向模型添加一个传统数据源：
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.SqlClient";
ds.ConnectionString = string.Format(
    "Server={0};Initial Catalog={1};Persist Security Info=False;User ID={2};Password={3}",
    server,
    database,
    userId,
    password);

// 从所有表中删除 Power Query 分区，并用单个传统分区替换：
foreach(var t in Model.Tables.Where(t => t.Partitions.OfType<MPartition>().Any()))
{
    var mPartitions = t.Partitions.OfType<MPartition>();
    if(!mPartitions.Any()) continue;
    var schema = GetSchema(mPartitions.First().Expression);
    var table = GetTable(mPartitions.First().Expression);
    t.AddPartition(t.Name, string.Format("SELECT * FROM [{0}].[{1}]", schema, table));
    foreach(var p in mPartitions.ToList()) p.Delete();
}
```
