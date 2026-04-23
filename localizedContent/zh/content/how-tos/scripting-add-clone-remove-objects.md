---
uid: how-to-add-clone-remove-objects
title: 如何添加、克隆和删除对象
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何添加、克隆和删除对象

C# Script 可用于创建新的模型对象、克隆现有对象以及删除对象。 本文介绍 Add、Clone 和 Delete 的常用模式。

## 快速参考

```csharp
var table = Model.Tables["Sales"];
var measure = table.Measures["Revenue"];

// Add objects -- all parameters after the first are optional.
// See sections below for parameter details.
table.AddMeasure("Name", "DAX Expression", "Display Folder");
table.AddCalculatedColumn("Name", "DAX Expression", "Display Folder");
table.AddDataColumn("Name", "SourceColumn", "Display Folder", DataType.String);
table.AddHierarchy("Name", "Display Folder", table.Columns["Year"], table.Columns["Month"]);
Model.AddCalculatedTable("Name", "DAX Expression");
Model.AddPerspective("Name");
Model.AddRole("Name");
Model.AddTranslation("da-DK");

// Relationships
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many (N) side
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one (1) side

// Clone
var clone = measure.Clone("New Name");                         // same table
var cloneToOther = measure.Clone("New Name", true, Model.Tables["Reporting"]); // different table

// Delete (always materialize with ToList() before modifying a collection in a loop)
measure.Delete();
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## 添加度量值

`AddMeasure()` 会在表上创建并返回一个新的 `Measure` 度量值。 第一个参数是名称，第二个是 DAX 表达式，第三个是显示文件夹。 除第一个参数外，其他参数都是可选的。

将返回的对象保存到变量中，以便设置其他属性。 所有 `Add*` 方法都遵循这一模式。

```csharp
var table = Model.Tables["Sales"];

// Create a measure and set properties on the returned object
var m = table.AddMeasure(
    "Revenue",                   // name
    "SUM('Sales'[Amount])"       // DAX expression
);
m.FormatString = "#,##0.00";
m.Description = "Total sales amount";

// With display folder
var m2 = table.AddMeasure(
    "Cost",                      // name
    "SUM('Sales'[Cost])",        // DAX expression
    "Financial"                  // display folder
);
```

## 添加列

```csharp
// Calculated column -- first parameter is the name, second is a DAX expression
var cc = table.AddCalculatedColumn(
    "Profit",                              // name
    "'Sales'[Amount] - 'Sales'[Cost]"      // DAX expression
);
cc.DataType = DataType.Decimal;
cc.FormatString = "#,##0.00";

// Data column -- maps to a source column in the partition query
var dc = table.AddDataColumn(
    "Region",              // name
    "RegionName",          // source column name
    "Geography",           // display folder
    DataType.String        // data type
);
```

> [!WARNING]
> 添加数据列不会修改表的分区查询。 你必须单独更新 M 表达式或 SQL 查询，以包含与 `sourceColumn` 参数匹配的源列。

## 添加层次结构

`levels` 参数是可变参数。 在一次调用中传入任意数量的列，即可自动创建相应的级别。

```csharp
var dateTable = Model.Tables["Date"];
var h = dateTable.AddHierarchy(
    "Calendar",                        // name
    "",                                // display folder
    dateTable.Columns["Year"],         // level 1
    dateTable.Columns["Quarter"],      // level 2
    dateTable.Columns["Month"]         // level 3
);
```

或者逐个添加级别：

```csharp
var h = dateTable.AddHierarchy("Fiscal");
h.AddLevel(dateTable.Columns["FiscalYear"]);
h.AddLevel(dateTable.Columns["FiscalQuarter"]);
h.AddLevel(dateTable.Columns["FiscalMonth"]);
```

## 添加计算表格

```csharp
var ct = Model.AddCalculatedTable(
    "DateKey List",                    // name
    "VALUES('Date'[DateKey])"          // DAX expression
);
```

## 添加关系

`AddRelationship()` 会创建并返回一个空关系。 你必须明确设置相关列。

`FromColumn` 是多端 (N)，`ToColumn` 是一端 (1)。 Tabular Editor 不会自动检测关系方向。 一个好记的助记法：F 表示 From，F 也表示 Fact table（多的一侧）。

新建关系默认使用 `CrossFilteringBehavior.OneDirection`，并且 `IsActive = true`。 仅在需要设置为其他值时才修改它们。

```csharp
var rel = Model.AddRelationship();
rel.FromColumn = Model.Tables["Sales"].Columns["ProductKey"];   // many side (fact)
rel.ToColumn = Model.Tables["Product"].Columns["ProductKey"];   // one side (dimension)

// Only set these if you need non-default values:
// rel.CrossFilteringBehavior = CrossFilteringBehavior.BothDirections;
// rel.IsActive = false;
```

## 克隆对象

`Clone()` 会创建一个包含所有属性、注释和翻译的副本。

```csharp
// Clone within the same table
var original = Model.AllMeasures.First(m => m.Name == "Revenue");
var copy = original.Clone("Revenue Copy");

// Clone to a different table (with translations)
var copy2 = original.Clone("Revenue Copy", true, Model.Tables["Reporting"]);
```

## 从列生成度量值

一种常见模式：遍历所选列并创建派生度量值。 注意这里用了 `DaxObjectFullName`。它会返回完全限定且已正确加引号的 DAX 引用（例如 `'Sales'[Amount]`），以避免引号错误。

```csharp
foreach (var col in Selected.Columns)
{
    var m = col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
    m.FormatString = "0.00";
    col.IsHidden = true;
}
```

## 删除对象

对任何命名对象调用 `Delete()` 即可将其删除。 在循环中修改集合时（删除、添加或移动对象），务必先调用 `.ToList()`，将当前集合物化为一个快照。

```csharp
// Delete a single object
Model.AllMeasures.First(m => m.Name == "Temp").Delete();

// Delete multiple objects safely
Model.AllMeasures
    .Where(m => m.HasAnnotation("DEPRECATED"))
    .ToList()
    .ForEach(m => m.Delete());
```

## 常见陷阱

> [!WARNING]
>
> - 在循环中修改对象之前，务必先调用 `.ToList()` 或 `.ToArray()`。 否则，在枚举过程中修改集合会导致：`"Collection was modified; enumeration operation may not complete."`
> - `AddRelationship()` 会创建一个不完整的关系。 必须同时为 `FromColumn` 和 `ToColumn` 赋值，模型才能通过验证。
> - `Column` 是抽象类，但无需强制转换也可以访问所有基类属性（`Name`、`DataType`、`FormatString`、`IsHidden`）。 只有在需要访问特定类型的属性时，才将其强制转换为子类型。
> - `Clone()` 会复制所有元数据，包括注释、翻译以及透视成员资格。 克隆后删除不需要的元数据。

## 另见

- @实用脚本片段
- @从列创建求和度量值
- @how-to-navigate-tom-hierarchy
- @how-to-use-selected-object
- (xref:TabularEditor.TOMWrapper.Measure) -- 度量值 API 参考
- (xref:TabularEditor.TOMWrapper.Column) -- 列 API 参考
- (xref:TabularEditor.TOMWrapper.Hierarchy) -- 层次结构 API 参考
- (xref:TabularEditor.TOMWrapper.SingleColumnRelationship) -- 关系 API 参考
