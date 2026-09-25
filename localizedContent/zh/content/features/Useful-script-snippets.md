---
uid: useful-script-snippets
title: 实用脚本片段
author: Daniel Otykier
updated: 2026-04-10
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

Here's a collection of small script snippets to get you started using the [Advanced Scripting functionality](xref:advanced-scripting) of Tabular Editor. Many of these scripts are useful to save as [Custom Actions](xref:custom-actions), so that you can easily reuse them from the context menu.

另外，也别忘了看看我们的脚本库 @csharp-script-library，里面有更多贴近实际场景的示例，展示了你可以如何利用 Tabular Editor 的脚本功能。

> [!TIP]
> For structured, pattern-by-pattern reference material on C# scripting and Dynamic LINQ, see the [Scripting Patterns](xref:how-to-navigate-tom-hierarchy) how-to series. For the complete TOM wrapper API, see the @api-index.

***

## 从列创建度量值

```csharp
// Creates a SUM measure for every currently selected column and hide the column.
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Sum of " + c.Name,                    // Name
        "SUM(" + c.DaxObjectFullName + ")",    // DAX expression
        c.DisplayFolder                        // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = "0.00";

    // Provide some documentation:
    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    // Hide the base column:
    c.IsHidden = true;
}
```

这个片段使用 `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` 函数，在表中创建一个新的度量值。 We use the `DaxObjectFullName` property to get the fully qualified name of the column for use in the DAX expression: `'TableName'[ColumnName]`.

***

## 生成时间智能度量值

首先，为每项时间智能聚合创建自定义操作。 For example:

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
}
```

这里我们使用 `DaxObjectName` 属性来生成用于 DAX 表达式的不带限定符的引用，因为这是一个度量值：`[MeasureName]`。 Save this as a Custom Action called "Time Intelligence\Create YTD measure" that applies to measures. Create similar actions for MTD, LY, and whatever else you need. Then, create the following as a new action:

```csharp
// Invoke all Time Intelligence Custom Actions:
CustomAction(@"Time Intelligence\Create YTD measure");
CustomAction(@"Time Intelligence\Create MTD measure");
CustomAction(@"Time Intelligence\Create LY measure");
```

This illustrates how you can execute one (or more) Custom Actions from within another action (beware of circular references - that will cause Tabular Editor to crash). Save this as a new Custom Action "Time Intelligence\All of the above", and you will have an easy way to generate all your Time Intelligence measures with a single click:

![image](~/content/assets/images/useful-script-snippets-01.png)

当然，你也可以将所有时间智能计算放入一个脚本中，如下所示：

```csharp
var dateColumn = "'Date'[Date]";

// Creates time intelligence measures for every selected measure:
foreach(var m in Selected.Measures) {
    // Year-to-date:
    m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    
    // Previous year:
    m.Table.AddMeasure(
        m.Name + " PY",                                       // Name
        "CALCULATE(" + m.DaxObjectName + ", SAMEPERIODLASTYEAR(" + dateColumn + "))",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );    
    
    // Year-over-year
    m.Table.AddMeasure(
        m.Name + " YoY",                                       // Name
        m.DaxObjectName + " - [" + m.Name + " PY]",            // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    
    // Year-over-year %:
    m.Table.AddMeasure(
        m.Name + " YoY%",                                       // Name
        "DIVIDE([" + m.Name + " YoY], [" + m.Name + " PY])",    // DAX expression
        m.DisplayFolder                                         // Display Folder
    ).FormatString = "0.0 %";                                   // Set format string as percentage
    
    // Quarter-to-date:
    m.Table.AddMeasure(
        m.Name + " QTD",                                            // Name
        "TOTALQTD(" + m.DaxObjectName + ", " + dateColumn + ")",    // DAX expression
        m.DisplayFolder                                             // Display Folder
    );
    
    // Month-to-date:
    m.Table.AddMeasure(
        m.Name + " MTD",                                       // Name
        "TOTALMTD(" + m.DaxObjectName + ", " + dateColumn + ")",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
}
```

### 包含附加属性

如果你想为新建的度量值设置其他属性，可以将上述脚本修改如下：

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    newMeasure.FormatString = m.FormatString;               // Copy format string from original measure
    foreach(var c in Model.Cultures) {
        newMeasure.TranslatedNames[c] = m.TranslatedNames[c] + " YTD"; // Copy translated names for every culture
        newMeasure.TranslatedDisplayFolders[c] = m.TranslatedDisplayFolders[c]; // Copy translated display folders
    }
}
```

***

## 设置默认翻译

Sometimes it is useful to have default translations applied to all (visible) objects. In this case, a default translation is just the original name/description/display folder of an object. 这样做的一个好处是：以 JSON 格式导出翻译时，会包含所有翻译对象，即可用于 [SSAS Tabular Translator](https://www.sqlbi.com/tools/ssas-tabular-translator/)。

以下脚本会遍历模型中的所有区域设置；对于每个可见对象，若尚无翻译，则会为其赋予默认值：

```csharp
// Apply default translations to all (visible) translatable objects, across all cultures in the model:
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
    // Only apply the default translation when a translation does not already exist:
    if(string.IsNullOrEmpty(obj.TranslatedNames[culture]))
    {
        // Default name translation:
        obj.TranslatedNames[culture] = obj.Name;

        // Default description translation:
        var dObj = obj as IDescriptionObject;
        if(dObj != null && string.IsNullOrEmpty(obj.TranslatedDescriptions[culture])
            && !string.IsNullOrEmpty(dObj.Description))
        {
            obj.TranslatedDescriptions[culture] = dObj.Description;
        }

        // Default display folder translation:
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

度量值、列、层次结构和表都公开了 `InPerspective` 属性。该属性会为模型中的每个透视保存一个 True/False 值，用于指示给定对象是否属于该透视。 So for example:

```csharp
foreach(var measure in Selected.Measures)
{
    measure.InPerspective["Inventory"] = true;
    measure.InPerspective["Reseller Operation"] = false;
}
```

上述脚本可确保所有选中的度量值在 "Inventory" 透视中可见，并在 "Reseller Operation" 透视中隐藏。

除了获取/设置单个透视中的成员关系外，`InPerspective` 属性还支持以下方法：

- `<<object>>.InPerspective.None()` - 将对象从所有透视中移除。
- `<<object>>.InPerspective.All()` - 将对象加入所有透视。
- `<<object>>.CopyFrom(string[] perspectives)` - 将对象加入所有指定的透视中（包含透视名称的字符串数组）。
- `<<object>>.CopyFrom(perspectiveIndexer perspectives)` - 从另一个 `InPerspective` 属性复制透视包含关系。

The latter may be used to copy perspective memberships from one object to another. For example, say have a base measure [Reseller Total Sales], and you want to make sure that all currently selected measures are visible in the same perspectives as this base measure. The following script does the trick:

```csharp
var baseMeasure = Model.Tables["Reseller Sales"].Measures["Reseller Total Sales"];

foreach(var measure in Selected.Measures)
{
    /* Uncomment the line below, if you want 'measure' to be hidden
       from perspectives that 'baseMeasure' is hidden in: */
    // measure.InPerspective.None();

    measure.InPerspective.CopyFrom(baseMeasure.InPerspective);
}
```

This technique can be used also when generating new objects from code. 例如，如果我们希望确保自动生成的时间智能度量值只在与其基础度量值相同的透视中可见，可以在上一节的脚本基础上扩展如下：

```csharp
// Creates a TOTALYTD measure for every selected measure.
foreach(var m in Selected.Measures) {
    var newMeasure = m.Table.AddMeasure(
        m.Name + " YTD",                                       // Name
        "TOTALYTD(" + m.DaxObjectName + ", 'Date'[Date])",     // DAX expression
        m.DisplayFolder                                        // Display Folder
    );
    newMeasure.InPerspective.CopyFrom(m.InPerspective);        // Apply perspectives from the base measure
}
```

***

## Generating partitions

如果你需要对某个表进行自定义分区，C# Script 可以帮你快速生成大量分区。 The basic idea is to add an annotation to your table, containing the SQL or M query to use as a template for each partition. The script will then swap in filter parameters as needed. For example, using SQL partitions, we could add an annotation named `PartitionTemplateSQL` and set its value to `SELECT * FROM fact_ResellerSales WHERE CalendarID BETWEEN {0} AND {1}`. The `{0}` and `{1}` placeholders will be replaced by our script, when generating the final partitions. In this case, `CalendarID` is an integer, but in general, it is your job to ensure that the resulting string is a valid SQL (or M) query.

![](~/content/assets/images/useful-script-snippets-02.png)

The example here generates one partition per month. 选择一个带有 `PartitionTemplateSQL` 分区注释的表，然后运行该脚本。

```csharp
var firstPartition = new DateTime(2018,1,1); // First partition date
var lastPartition = new DateTime(2020,12,1); // Last partition date

var templateSql = Selected.Table.GetAnnotation("PartitionTemplateSQL");
if(string.IsNullOrEmpty(templateSql)) throw new Exception("No partition template!");

var currentPartition = firstPartition;
while(currentPartition <= lastPartition)
{
    // Calculate the from and to CalendarID's (integer values) based on the currentPartition date:
    var calendarIdFrom = currentPartition.ToString("yyyyMMdd");
    var calendarIdTo = currentPartition.AddMonths(1).AddDays(-1).ToString("yyyyMMdd");
    
    // Determine a unique name for the partition - since we're partitioning at a monthly level, we just use yyyyMM:
    var partitionName = Selected.Table.Name + "_" + currentPartition.ToString("yyyyMM");
    
    // Swap in the placeholder values in the partition template SQL:
    var partitionQuery = string.Format(templateSql, calendarIdFrom, calendarIdTo);
    
    // Create the partition (use .AddMPartition if you used an M query template instead of SQL):
    Selected.Table.AddPartition(partitionName, partitionQuery);
    
    // Increment to next month (change this to .AddDays, .AddYears, etc. if you need more or fewer partitions):
    currentPartition = currentPartition.AddMonths(1);
}
```

***

## 将对象属性导出到文件

For some workflows, it may be useful to edit multiple object properties in bulk using Excel. Use the following snippet to export a standard set of properties to a .TSV file, which can then be subsequently imported (see below).

```csharp
// Export properties for the currently selected objects:
var tsv = ExportProperties(Selected);
SaveFile("Exported Properties 1.tsv", tsv);
```

The resulting .TSV file looks like this, when opened in Excel:
![image](~/content/assets/images/useful-script-snippets-03.png)
The contents of the first column (Object) is a reference to the object. If the contents of this column is changed, subsequent import of the properties might not work correctly. To change the name of an object, only change the value in the second column (Name).

默认情况下，文件会保存到 TabularEditor.exe 所在的文件夹中。 By default, only the following properties are exported (where applicable, depending on the type of object exported):

- 名称
- 描述
- 源列
- 表达式
- 格式字符串
- 数据类型

要导出不同的属性，请提供以逗号分隔的属性名称列表，作为 `ExportProperties` 的第 2 个参数：

```csharp
// Export the names and Detail Rows Expressions for all measures on the currently selected table:
var tsv = ExportProperties(Selected.Table.Measures, "Name,DetailRowsExpression");
SaveFile("Exported Properties 2.tsv", tsv);
```

可用的属性名称可在 [TOM API 文档](https://msdn.microsoft.com/en-us/library/microsoft.analysisservices.tabular.aspx) 中找到。 These are mostly identical to the names shown in the Tabular Editor property grid in CamelCase and with spaces removed (with a few exceptions, for example, the "Hidden" property is called `IsHidden` in the TOM API).

要导入属性，请使用以下代码片段：

```csharp
// Imports and applies the properties in the specified file:
var tsv = ReadFile("Exported Properties 1.tsv");
ImportProperties(tsv);
```

### 导出带索引的属性

As of Tabular Editor 2.11.0, the `ExportProperties` and `ImportProperties` methods support indexed properties. Indexed properties are properties that take a key in addition to the property name. One example is `myMeasure.TranslatedNames`. This property represents the collection of all strings applied as name translations for `myMeasure`. In C#, you can access the translated caption of a specific culture using the indexing operator: `myMeasure.TranslatedNames["da-DK"]`.

简而言之，你现在可以导出 Tabular 模型中对象的所有翻译、透视信息、注释、扩展属性，以及行级和对象级安全性信息。

例如，以下脚本会生成一个 TSV 文件，其中包含模型中所有度量值以及每个度量值在哪些透视中可见的信息：

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective");
SaveFile(@"c:\Project\MeasurePerspectives.tsv", tsv);
```

在 Excel 中打开后，TSV 文件如下所示：

![image](~/content/assets/images/useful-script-snippets-04.png)

正如上面所示，你可以在 Excel 中进行修改，保存后，再使用 `ImportProperties` 将更新后的值加载回 Tabular Editor。

如果你只想列出某一个或少数几个特定的透视，可以在调用 `ExportProperties` 时在第 2 个参数中指定：

```csharp
var tsv = ExportProperties(Model.AllMeasures, "Name,InPerspective[Inventory]");
SaveFile(@"c:\Project\MeasurePerspectiveInventory.tsv", tsv);
```

Similarly, for translations, annotations, etc. 例如，如果你想查看应用于表、列、层次结构、级别和度量值的所有丹麦语翻译：

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

The `ExportProperties` method shown above, can also be used if you want to document all or parts of your model. 下面的代码片段会从 Tabular 模型中所有可见的度量值或列中提取一组属性，并将其保存为 TSV 文件：

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

如果你想批量编辑模型中现有对象的属性，上述导出/导入属性的方法会很有用。 What if you want to import a list of measures that do not already exist?

假设你有一个 TSV（制表符分隔值）文件，其中包含要导入到现有 Tabular 模型中的度量值名称、说明和 DAX 表达式。 You can use the following script to read in the file, split it out into rows and columns, and generate the measures. The script also assigns a special annotation to each measure, so that it can delete measures that were previously created using the same script.

```csharp
var targetTable = Model.Tables["Program"];  // Name of the table that should hold the measures
var measureMetadata = ReadFile(@"c:\Test\MyMeasures.tsv");   // c:\Test\MyMeasures.tsv is a tab-separated file with a header row and 3 columns: Name, Description, Expression

// Delete all measures from the target table that have an "AUTOGEN" annotation with the value "1":
foreach(var m in targetTable.Measures.Where(m => m.GetAnnotation("AUTOGEN") == "1").ToList())
{
    m.Delete();
}

// Split the file into rows by CR and LF characters:
var tsvRows = measureMetadata.Split(new[] {'\r','\n'},StringSplitOptions.RemoveEmptyEntries);

// Loop through all rows but skip the first one:
foreach(var row in tsvRows.Skip(1))
{
    var tsvColumns = row.Split('\t');     // Assume file uses tabs as column separator
    var name = tsvColumns[0];             // 1st column contains measure name
    var description = tsvColumns[1];      // 2nd column contains measure description
    var expression = tsvColumns[2];       // 3rd column contains measure expression

    // This assumes that the model does not already contain a measure with the same name (if it does, the new measure will get a numeric suffix):
    var measure = targetTable.AddMeasure(name);
    measure.Description = description;
    measure.Expression = expression;
    measure.SetAnnotation("AUTOGEN", "1");  // Set a special annotation on the measure, so we can find it and delete it the next time the script is executed.
}
```

If you need to automate this process, save the above script into a file and use the [Tabular Editor CLI](xref:command-line-options) as follows:

```powershell
start /wait TabularEditor.exe "<path to bim file>" -S "<path to script file>" -B "<path to modified bim file>"
```

比如：

```powershell
start /wait TabularEditor.exe "c:\Projects\AdventureWorks\Model.bim" -S "c:\Projects\AutogenMeasures.cs" -B "c:\Projects\AdventureWorks\Build\Model.bim"
```

……或者，如果你想针对已部署的数据库运行该脚本：

```powershell
start /wait TabularEditor.exe "localhost" "AdventureWorks" -S "c:\Projects\AutogenMeasures.cs" -D "localhost" "AdventureWorks" -O
```

***

## 根据分区源元数据创建数据列

> [!NOTE]
> 下文所述的 `RefreshDataColumns()` 方法仅在 **Tabular Editor 2** 中可用。 In Tabular Editor 3, use the **Import Table...** feature instead.

如果某个表使用基于 OLE DB Provider数据源的查询分区，我们可以通过执行以下代码片段来自动刷新该表的列元数据：

```csharp
Model.Tables["Reseller Sales"].RefreshDataColumns();
```

This is useful when adding new tables to a model, to avoid having to create every Data Column on the table manually. The snippet above assumes that the partition source can be accessed locally, using the existing connection string of the Partition Source for the 'Reseller Sales' table. The snippet above will extract the schema from the partition query, and add a Data Column to the table for every column in the source query.

如果需要为此操作提供另一条连接字符串，也可以在该代码片段中进行设置：

```csharp
var source = Model.DataSources["DWH"] as ProviderDataSource;
var oldConnectionString = source.ConnectionString;
source.ConnectionString = "...";   // Enter the connection string you want to use for metadata refresh
Model.Tables["Reseller Sales"].RefreshDataColumns();
source.ConnectionString = oldConnectionString;
```

这里假定“Reseller Sales”表的分区使用名为“DWH”的 Provider数据源。

***

## 格式化 DAX 表达式

Please see [FormatDax](xref:script-helper-methods) for more information.

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
Selected.Measures.FormatDax();
```

另一种语法：

```csharp
// Works in Tabular Editor version 2.13.0 or newer:
foreach(var m in Selected.Measures)
    m.FormatDax();
```

***

## 生成表的源列列表

下面的脚本会为当前选定的表输出一份格式良好的源列清单。 This may be useful if you want to replace partition queries that use `SELECT *` with explicit columns.

```csharp
string.Join(",\r\n", 
    Selected.Table.DataColumns
        .OrderBy(c => c.SourceColumn)
        .Select(c => "[" + c.SourceColumn + "]")
    ).Output();
```

***

## 自动生成关系

如果你的团队一直采用一套固定的命名约定，你很快就会发现脚本的威力会更大。

The following script, when executed on one or more fact tables, will automatically create relationships to all relevant dimension tables, based on column names. 脚本会查找事实表中名称符合 `xxxyyyKey` 模式的列，其中 xxx 是用于角色扮演维度的可选限定符，yyy 是维度表名称。 On the dimension table, a column named `yyyKey` must exist and have the same data type as the column on the fact table. For example, a column named "ProductKey" will be related to the "ProductKey" column on the Product table. You can specify a different column name suffix to use in place of "Key".

如果事实表与维度表之间已经存在关系，脚本会将新关系创建为非活动状态。

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

受[这篇文章](https://www.sqlbi.com/articles/displaying-filter-context-in-power-bi-tooltips/)启发，下面的脚本会在当前选中的表上创建一个名为 [DumpFilters] 的度量值：

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

// Loop through all columns of the model to construct the complete DAX expression:
bool first = true;
foreach(var column in Model.AllColumns)
{
    if(!first) dax += " & ";
    dax += string.Format(dumpFilterDax, column.DaxObjectFullName);
    if(first) first = false;
}

// Add the measure to the currently selected table:
Selected.Table.AddMeasure("DumpFilters", dax);
```

***

## 将 CamelCase 转换为 Proper Case

在关系数据库中，列和表常用的一种命名方式是 CamelCase。 That is, names do not contain any spaces and individual words start with a capital letter. In a Tabular model, tables and columns that are not hidden, will be visible to business users, and so it would often be preferable to use a "prettier" naming scheme. The following script will convert CamelCased names to Proper Case. Sequences of uppercase letters are kept as-is (acronyms). For example, the script will convert the following:

- `CustomerWorkZipcode` 转换为 `Customer Work Zipcode`
- `CustomerAccountID` 转换为 `Customer Account ID`
- `NSASecurityID` 转换为 `NSA Security ID`

强烈建议将该脚本保存为适用于所有对象类型的自定义操作（关系、KPI、表格权限和翻译除外，因为这些对象没有可编辑的“Name”属性）：

```csharp
foreach(var obj in Selected.OfType<ITabularNamedObject>()) {
    var oldName = obj.Name;
    var newName = new System.Text.StringBuilder();
    for(int i = 0; i < oldName.Length; i++) {
        // First letter should always be capitalized:
        if(i == 0) newName.Append(Char.ToUpper(oldName[i]));

        // A sequence of two uppercase letters followed by a lowercase letter should have a space inserted
        // after the first letter:
        else if(i + 2 < oldName.Length && char.IsLower(oldName[i + 2]) && char.IsUpper(oldName[i + 1]) && char.IsUpper(oldName[i]))
        {
            newName.Append(oldName[i]);
            newName.Append(" ");
        }

        // All other sequences of a lowercase letter followed by an uppercase letter, should have a space
        // inserted after the first letter:
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

## 导出表与度量值的依赖关系

假设你有一个大型且复杂的模型，并希望了解哪些度量值可能会受到底层数据变更的影响。

下面的脚本会遍历模型中的所有度量值，并针对每个度量值输出其依赖的表列表——包括直接依赖和间接依赖。 The list is outputted as a Tab-separated file.

```csharp
string tsv = "Measure\tDependsOnTable"; // TSV file header row

// Loop through all measures:
foreach(var m in Model.AllMeasures) {

    // Get a list of ALL objects referenced by this measure (both directly and indirectly through other measures):
    var allReferences = m.DependsOn.Deep();

    // Filter the previous list of references to table references only. For column references, let's get th
    // table that each column belongs to. Finally, keep only distinct tables:
    var allTableReferences = allReferences.OfType<Table>()
        .Concat(allReferences.OfType<Column>().Select(c => c.Table)).Distinct();

    // Output TSV rows - one for each table reference:
    foreach(var t in allTableReferences)
        tsv += string.Format("\r\n{0}\t{1}", m.Name, t.Name);
}
    
tsv.Output();   
// SaveFile("c:\\MyProjects\\SSAS\\MeasureTableDependencies.tsv", tsv); // Uncomment this line to save output to a file
```

***

## 设置聚合（仅适用于 Power BI Dataset）

As of [Tabular Editor 2.11.3](https://github.com/TabularEditor/TabularEditor/releases/tag/2.11.3), you can now set the `AlternateOf` property on a column, enabling you to define aggregation tables on your model. This feature is enabled for Power BI Datasets (Compatibility Level 1460 or higher) through the Power BI Service XMLA endpoint.

选择一组列并运行以下脚本，以初始化这些列的 `AlternateOf` 属性：

```csharp
foreach(var col in Selected.Columns) col.AddAlternateOf();
```

Work your way through the columns one by one, to map them to the base column and set the summarization accordingly (Sum/Min/Max/GroupBy). 或者，如果你想自动化此流程，并且聚合表中的列与基础表中的列名称完全相同，可以使用下面的脚本，它会为你自动映射这些列：

```csharp
// Select two tables in the tree (ctrl+click). The aggregation table is assumed to be the one with fewest columns.
// This script will set up the AlternateOf property on all columns on the aggregation table. Agg table columns must
// have the same name as the base table columns for this script to work.
var aggTable = Selected.Tables.OrderBy(t => t.Columns.Count).First();
var baseTable = Selected.Tables.OrderByDescending(t => t.Columns.Count).First();

foreach(var col in aggTable.Columns)
{
    // The script will set the summarization type to "Group By", unless the column uses data type decimal/double:
    var summarization = SummarizationType.GroupBy;
    if(col.DataType == DataType.Double || col.DataType == DataType.Decimal)
        summarization = SummarizationType.Sum;
    
    col.AddAlternateOf(baseTable.Columns[col.Name], summarization);
}
```

运行脚本后，你应该会看到聚合表上的所有列都已设置了 `AlternateOf` 属性（见下方截图）。 Keep in mind, that the base table partition must use DirectQuery for aggregations to work.

![image](~/content/assets/images/useful-script-snippets-05.png)

***

## 查询 Analysis Services

自版本 [2.12.1](https://github.com/TabularEditor/TabularEditor/releases/tag/2.12.1) 起，Tabular Editor 提供了多种辅助方法，用于针对你的模型执行 DAX 查询并对 DAX 表达式求值。这些方法仅在模型元数据直接从 Analysis Services 实例加载时才适用，例如使用 "File > Open > From DB..." 选项，或使用 Tabular Editor 与 Power BI 外部工具的集成功能时。

以下方法可用：

| 方法                                                            | 描述                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `void ExecuteCommand(string tmslOrXmla, bool isXmla = false)` | This methods passes the specified TMSL or XMLA script to the connected instance of Analysis Services. This is useful when you want to refresh data in a table on the AS instance. Note that if you use this method to perform metadata changes to your model, your local model metadata will become out-of-sync with the metadata on the AS instance, and you may receive a version conflict warning the next time you try to save the model metadata. Set the `isXmla` parameter to `true` if  sending an XMLA script. |
| `IDataReader ExecuteReader(string dax)`                       | 在已连接的 AS 数据库上执行指定的 DAX _查询_，并返回得到的 [AmoDataReader](https://docs.microsoft.com/en-us/dotnet/api/microsoft.analysisservices.amodatareader?view=analysisservices-dotnet) 对象。 A DAX query contains one or more [`EVALUATE`](https://dax.guide/EVALUATE) statements. Note that you can not have multiple open data readers at once. Tabular Editor will automatically close them in case you forget to explicitly close or dispose the reader.                                                                                               |
| `Dataset ExecuteDax(string dax)`                              | 在已连接的 AS 数据库上执行指定的 DAX _查询_，并返回一个 [Dataset](https://docs.microsoft.com/en-us/dotnet/api/system.data.dataset?view=netframework-4.6) 对象，其中包含查询返回的数据。 A DAX query contains one or more [`EVALUATE`](https://dax.guide/EVALUATE) statements. The resulting DataSet object contains one DataTable for each `EVALUATE` statement. Returning very large data tables is not recommended as they may cause out-of-memory or other stability errors.                                                                                              |
| `object EvaluateDax(string dax)`                              | Executes the specified DAX _expression_ against the connected AS database and returns an object representing the result. If the DAX expression is scalar, an object of the relevant type is returned (string, long, decimal, double, DateTime). 如果 DAX 表达式为表值，则会返回一个 [DataTable](https://docs.microsoft.com/en-us/dotnet/api/system.data.datatable?view=netframework-4.6)。                                                                                                                                                           |

Call these methods directly, without any prefix. Up to Tabular Editor 3.26.x they could also be reached through the `Model.Database` object; from 3.27.0 they cannot, so `Model.Database.ExecuteCommand(tmsl)` no longer compiles and `ExecuteCommand(tmsl)` is the form to use.

Darren Gosbell 在 [此处](https://darren.gosbell.com/2020/08/the-best-way-to-generate-data-driven-measures-in-power-bi-using-tabular-editor/) 介绍了一个有趣的用例：如何使用 `ExecuteDax` 方法生成数据驱动的度量值。

另一种做法是创建一个可复用的脚本，用于刷新某个表。 For example, to perform a recalculation, use this:

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

### 清除 Analysis Services 引擎的缓存

从 Tabular Editor 2.16.6 或 Tabular Editor 3.2.3 起，你可以使用以下语法向 Analysis Services 发送原始 XMLA 命令。 The example below shows how this can be used to clear the AS engine cache:

```csharp
var clearCacheXmla = string.Format(@"<ClearCache xmlns=""http://schemas.microsoft.com/analysisservices/2003/engine"">  
  <Object>
    <DatabaseID>{0}</DatabaseID>
  </Object>
</ClearCache>", Model.Database.ID);

ExecuteCommand(clearCacheXmla, isXmla: true);
```

### 可视化查询结果

你也可以使用 `Output` 辅助方法，直接将 `EvaluateDax` 返回的 DAX 表达式结果可视化：

```csharp
EvaluateDax("1 + 2").Output(); // An integer
EvaluateDax("\"Hello from AS\"").Output(); // A string
EvaluateDax("{ (1, 2, 3) }").Output(); // A table
```

![image](~/content/assets/images/useful-script-snippets-06.png)

...或者，如果你想返回当前选中度量值的值：

```csharp
EvaluateDax(Selected.Measure.DaxObjectFullName).Output();
```

![image](~/content/assets/images/useful-script-snippets-07.png)

下面是一个更高级的示例，可让你一次选择并对多个度量值求值：

```csharp
var dax = "ROW(" + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](~/content/assets/images/useful-script-snippets-08.png)

如果你已经非常熟练，可以使用 SUMMARIZECOLUMNS 或其他 DAX 函数，将选中的度量值按某一列切片并可视化：

```csharp
var dax = "SUMMARIZECOLUMNS('Product'[Color], " + string.Join(",", Selected.Measures.Select(m => "\"" + m.Name + "\", " + m.DaxObjectFullName).ToArray()) + ")";
EvaluateDax(dax).Output();
```

![image](~/content/assets/images/useful-script-snippets-09.png)

Remember you can save these scripts as Custom Actions by clicking the "+" icon just above the script editor. 这样，你就能拥有一套易于复用的 DAX 查询集合，可直接在 Tabular Editor 的上下文菜单中执行并可视化：

![image](~/content/assets/images/useful-script-snippets-10.png)

### 数据导出

你可以使用下面的脚本通过 EVALUATE 执行一个 DAX 查询，并将结果流式写入文件（脚本使用制表符分隔格式）：

```csharp
using System.IO;

// This script evaluates a DAX query and writes the results to file using a tab-separated format:

var dax = "EVALUATE 'Customer'";
var file = @"c:\temp\file.csv";
var columnSeparator = "\t";

using(var daxReader = ExecuteReader(dax))
using(var fileWriter = new StreamWriter(file))
{
    // Write column headers:
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

如果你想到了这些方法的其他有趣用法，欢迎在[社区脚本 repository](https://github.com/TabularEditor/Scripts)中分享。 Thanks!

***

## 替换 Power Query 的服务器和数据库名称

Power BI Dataset that import data from SQL Server-based datasources, often contain M expressions that look like the following. Tabular Editor does unfortunately not have any mechanism for "parsing" such an expression, but if we wanted to replace the server and database names in this expression with something else, without knowing the original values, we can exploit the fact that the values are enclosed in double quotes:

```M
let
    Source = Sql.Databases("devsql.database.windows.net"),
    AdventureWorksDW2017 = Source{[Name="AdventureWorks"]}[Data],
    dbo_DimProduct = AdventureWorksDW2017{[Schema="dbo",Item="DimProduct"]}[Data]
in
    dbo_DimProduct
```

以下脚本会将双引号中第一次出现的值替换为服务器名称，并将双引号中第二次出现的值替换为数据库名称。 Both replacement values are read from environment variables:

```csharp
// This script is used to replace the server and database names across
// all power query partitions, with the ones provided through environment
// variables:
var server = "\"" + Environment.GetEnvironmentVariable("SQLServerName") + "\"";
var database = "\"" + Environment.GetEnvironmentVariable("SQLDatabaseName") + "\"";

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
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
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string

// Loop through all partitions on the model, replacing the server and database names from the partitions
// with the ones specified in environment variables:
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

## 用 Legacy 替换 Power Query 数据源和分区

如果你正在处理一个基于 Power BI 的模型，且该模型的分区使用 Power Query（M）表达式来访问基于 SQL Server 的数据源，那么很遗憾，你将无法使用 Tabular Editor 2 的“数据导入”向导，也无法执行架构检查（即比较已导入的列与数据源中的列）。

要解决这个问题，你可以在模型上运行下面的脚本：它会将 Power Query 分区替换为对应的原生 SQL 查询分区，并在模型中创建一个 Legacy（提供程序）数据源，这样就能使用 Tabular Editor 2 的“数据导入”向导：

There are two versions of the script: The first one uses the MSOLEDBSQL provider for the created legacy data source, and hardcoded credentials. This is useful for local development. The second one uses the SQLNCLI provider, which is available on Microsoft-hosted build agents on Azure DevOps, and reads credentials and server/database names from environment variables, making the script useful for integration in Azure Pipelines.

MSOLEDBSQL 版本：从 M 分区读取连接信息，并通过 Azure AD 提示你输入用户名和密码：

```csharp
#r "Microsoft.VisualBasic"

// This script replaces all Power Query partitions on this model with a
// legacy partition using the provided connection string with INTERACTIVE
// AAD authentication. The script assumes that all Power Query partitions
// load data from the same SQL Server-based data source.

// Provide the following information:
var authMode = "ActiveDirectoryInteractive";
var userId = Microsoft.VisualBasic.Interaction.InputBox("Type your AAD user name", "User name", "name@domain.com", 0, 0);
if(userId == "") return;
var password = ""; // Leave blank when using ActiveDirectoryInteractive authentication

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
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
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string
var GetSchema = new Func<string, string>(m => split(m)[2]);    // Schema name is usually the 3rd encountered string
var GetTable = new Func<string, string>(m => split(m)[3]);     // Table name is usually the 4th encountered string

var server = GetServer(Model.AllPartitions.OfType<MPartition>().First().Expression);
var database = GetDatabase(Model.AllPartitions.OfType<MPartition>().First().Expression);

// Add a legacy data source to the model:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.OleDb";
ds.ConnectionString = string.Format(
    "Provider=MSOLEDBSQL;Data Source={0};Initial Catalog={1};Authentication={2};User ID={3};Password={4}",
    server,
    database,
    authMode,
    userId,
    password);

// Remove Power Query partitions from all tables and replace them with a single Legacy partition:
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

SQLNCLI 版本：从环境变量中读取连接信息：

```csharp
// This script replaces all Power Query partitions on this model with a
// legacy partition, reading the SQL server name, database name, user name
// and password from corresponding environment variables. The script assumes
// that all Power Query partitions load data from the same SQL Server-based
// data source.

var server = Environment.GetEnvironmentVariable("SQLServerName");
var database = Environment.GetEnvironmentVariable("SQLDatabaseName");
var userId = Environment.GetEnvironmentVariable("SQLUserName");
var password = Environment.GetEnvironmentVariable("SQLUserPassword");

// This function will extract all quoted values from the M expression, returning a list of strings
// with the values extracted (in order), but ignoring any quoted values where a hashtag (#) precedes
// the quotation mark:
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
var GetServer = new Func<string, string>(m => split(m)[0]);    // Server name is usually the 1st encountered string
var GetDatabase = new Func<string, string>(m => split(m)[1]);  // Database name is usually the 2nd encountered string
var GetSchema = new Func<string, string>(m => split(m)[2]);    // Schema name is usually the 3rd encountered string
var GetTable = new Func<string, string>(m => split(m)[3]);     // Table name is usually the 4th encountered string

// Add a legacy data source to the model:
var ds = Model.AddDataSource("AzureSQL");
ds.Provider = "System.Data.SqlClient";
ds.ConnectionString = string.Format(
    "Server={0};Initial Catalog={1};Persist Security Info=False;User ID={2};Password={3}",
    server,
    database,
    userId,
    password);

// Remove Power Query partitions from all tables and replace them with a single Legacy partition:
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
