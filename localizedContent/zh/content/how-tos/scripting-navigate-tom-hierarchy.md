---
uid: how-to-navigate-tom-hierarchy
title: 如何导航 TOM 对象层次结构
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何导航 TOM 对象层次结构

每个 C# Script 都以 `Model` 对象或 @csharp-scripts 的 `Selected` 对象为起点。 它们提供 Tabular Editor 的 TOM 包装器，该包装器封装了 Microsoft Analysis Services Tabular Object Model (TOM)。 有关完整的包装器文档，请参阅 (xref:TabularEditor.TOMWrapper) API 参考。

## 快速参考

```csharp
// Direct path to a specific object
var table    = Model.Tables["Sales"];
var measure  = Model.Tables["Sales"].Measures["Revenue"];
var column   = Model.Tables["Sales"].Columns["Amount"];
var hierarchy = Model.Tables["Date"].Hierarchies["Calendar"];
var partition = Model.Tables["Sales"].Partitions["Sales-Part1"];

// Cross-table shortcut collections
Model.AllMeasures          // every measure across all tables
Model.AllColumns           // every column across all tables
Model.AllHierarchies       // every hierarchy across all tables
Model.AllPartitions        // every partition across all tables
Model.AllLevels            // every level across all hierarchies
Model.AllCalculationItems  // every calculation item across all calculation groups

// Top-level collections
Model.Tables               // all tables
Model.Relationships        // all relationships
Model.Perspectives         // all perspectives
Model.Roles                // all security roles
Model.Cultures             // all translation cultures
Model.DataSources          // all data sources
Model.CalculationGroups    // all calculation group tables
```

## 按名称访问对象

在任何集合中使用索引器 `["name"]`，即可按精确名称检索对象。 如果该名称不存在，将引发异常。

```csharp
var salesTable = Model.Tables["Sales"];
var revenueM  = salesTable.Measures["Revenue"];
var amountCol = salesTable.Columns["Amount"];
```

如果对象可能不存在，可以使用 `FirstOrDefault()`：

```csharp
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found"); return; } // return exits the script early
```

## 从子对象导航到父对象

每个对象都保存了对其父对象的引用。 使用这些引用可以沿层次结构向上遍历。

```csharp
var measure = Model.AllMeasures.First(m => m.Name == "Revenue");
var parentTable = measure.Table;          // Table that contains this measure
var model = measure.Model;                // The Model root

var level = Model.AllLevels.First();
var hierarchy = level.Hierarchy;           // parent hierarchy
var table = level.Table;                   // parent table (via hierarchy)

// Navigate up to Model and back down to a different table
var m = Model.AllMeasures.First(m => m.Name == "Revenue");
var otherCol = m.Table.Model.Tables["Product"].Columns.First();
```

> [!NOTE]
> 最后一个示例说明，你可以从任何子对象向上导航到 `Model`，再向下导航回模型中的任意表。

## 导航表的子对象

每个 `Table` 都提供其子对象的强类型集合。

```csharp
var table = Model.Tables["Sales"];

Output(table.Columns);                     // ColumnCollection
Output(table.Measures);                    // MeasureCollection
Output(table.Hierarchies);                 // HierarchyCollection
Output(table.Partitions);                  // PartitionCollection
```

## 使用谓词搜索

在任何集合中使用 LINQ 方法，按属性值查找对象。

```csharp
// Find all fact tables
var factTables = Model.Tables.Where(t => t.Name.StartsWith("Fact"));

// Find all hidden measures
var hiddenMeasures = Model.AllMeasures.Where(m => m.IsHidden);

// Find the first column with a specific data type
var dateCol = Model.AllColumns.First(c => c.DataType == DataType.DateTime);
```

## 计算组和计算项

计算组表是 `Table` 的一个子类型。 通过 `Model.CalculationGroups` 访问它们，并迭代其中的计算项。

```csharp
foreach (var cg in Model.CalculationGroups)
{
    foreach (var item in cg.CalculationItems)
    {
        Info(item.Name + ": " + item.Expression);
    }
}
```

## 关系

关系定义在 `Model` 上，而不是在表上。 每个关系都引用其源列/目标列和源表/目标表。

```csharp
foreach (var rel in Model.Relationships)
{
    var fromTable  = rel.FromTable;
    var fromColumn = rel.FromColumn;
    var toTable    = rel.ToTable;
    var toColumn   = rel.ToColumn;
}
```

## Dynamic LINQ 的等效写法

在 Best Practice Analyzer (BPA) 规则表达式和 **TOM Explorer** 树筛选器中，可直接访问当前上下文对象上的属性。 父级导航使用点表示法。

| C# Script                             | Dynamic LINQ（BPA）        |
| ------------------------------------- | ------------------------ |
| `measure.Table.Name`                  | `Table.Name`             |
| `column.Table.IsHidden`               | `Table.IsHidden`         |
| `table.Columns.Count()`               | `Columns.Count()`        |
| `table.Measures.Any(m => m.IsHidden)` | `Measures.Any(IsHidden)` |

> [!NOTE]
> BPA 规则中的 Dynamic LINQ 表达式每次只会针对单个对象求值。 你无法访问 `Model` 或跨表的集合。 使用规则的 **适用于** 作用域，选择该表达式要针对哪种对象类型运行。

## 另见

- @C# 脚本
- @advanced-scripting
- @how-to-filter-query-objects-linq
