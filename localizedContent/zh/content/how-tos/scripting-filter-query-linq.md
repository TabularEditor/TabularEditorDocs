---
uid: how-to-filter-query-objects-linq
title: 如何使用 LINQ 筛选和查询对象
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用 LINQ 筛选和查询对象

C# Script 使用标准 LINQ 方法来筛选、搜索和转换 TOM 对象集合。 这些模式是一些基本构件。 在 `foreach` 循环中使用返回集合的方法，在 `if` 条件中使用返回布尔值的方法，在变量赋值中使用返回标量的方法。

## 快速参考

```csharp
// Filter -- returns a collection for use in foreach or further chaining
Model.AllMeasures.Where(m => m.Name.EndsWith("Amount"));

// Find one -- returns a single object for assignment to a variable
var table = Model.Tables.First(t => t.Name == "Sales");
var tableOrNull = Model.Tables.FirstOrDefault(t => t.Name == "Sales");

// Existence checks -- returns bool for use in if conditions
if (table.Measures.Any(m => m.IsHidden)) { /* ... */ }
if (table.Columns.All(c => c.Description != "")) { /* ... */ }

// Count
var count = Model.AllColumns.Count(c => c.DataType == DataType.String);

// Project -- returns a List<string> of only the measure names
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Sort
var sorted = Model.AllMeasures.OrderBy(m => m.Name);

// Mutate
Model.AllMeasures.Where(m => m.FormatString == "").ForEach(m => m.FormatString = "0.00");

// Type filter
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();

// Materialize before modifying the collection
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

## 使用 Where 进行筛选

`Where()` 返回所有满足谓词条件的对象。 使用 `&&` 和 `||` 组合多个条件。

```csharp
// Columns with no description in a specific table
var undocumented = Model.Tables["Sales"].Columns
    .Where(c => string.IsNullOrEmpty(c.Description));
```

> [!WARNING]
> 使用 `Contains()` 进行字符串匹配时，会在表达式中的任意位置查找文本，包括字符串字面量和注释内部。 若要检测实际使用的 DAX 函数，改为分析令牌化后的表达式。

> [!TIP]
> 使用 `Contains()` 检查表达式内容时，可以考虑使用不区分大小写的比较：`m.Expression.Contains("calculate", StringComparison.OrdinalIgnoreCase)`。

## 查找单个对象

`First()` 返回第一个匹配项；如果不存在，则会引发异常。 `FirstOrDefault()` 会返回 null，而不是引发异常。

```csharp
// Throws if "Sales" does not exist
var sales = Model.Tables.First(t => t.Name == "Sales");

// Returns null if not found (safe)
var table = Model.Tables.FirstOrDefault(t => t.Name == "Sales");
if (table == null) { Error("Table not found."); return; } // return exits the script
```

## 存在性和计数检查

```csharp
// Are all columns documented?
var allDocs = table.Columns.All(c => !string.IsNullOrEmpty(c.Description));

// How many string columns?
var count = Model.AllColumns.Count(c => c.DataType == DataType.String);
```

## 使用 Select 进行投影

`Select()` 会转换每个元素。 可以用它来提取属性值或构建新结构。

```csharp
// List of measure names only (returns List<string>)
var names = Model.AllMeasures.Select(m => m.Name).ToList();

// Table name + measure count pairs
var summary = Model.Tables.Select(t => new { t.Name, Count = t.Measures.Count() });
```

## 使用 ForEach 进行更改

`ForEach()` 扩展方法会对每个元素执行一个操作。

```csharp
// Set format string on all currency measures
Model.AllMeasures
    .Where(m => m.Name.EndsWith("Amount"))
    .ForEach(m => m.FormatString = "#,##0.00");

// Move all measures in a table to a display folder
Model.Tables["Sales"].Measures.ForEach(m => m.DisplayFolder = "Sales Metrics");
```

## 在修改集合之前先将其物化

当你在循环中修改对象（删除、添加、移动）时，实际上是在改变正在迭代的集合。 一定要先调用 `.ToList()` 或 `.ToArray()` 来创建快照。

```csharp
// WRONG: modifying collection during iteration
table.Measures.Where(m => m.IsHidden).ForEach(m => m.Delete()); // throws

// CORRECT: materialize first, then modify
table.Measures.Where(m => m.IsHidden).ToList().ForEach(m => m.Delete());
```

> [!WARNING]
> 如果不先将结果物化，就会出现：`"Collection was modified; enumeration operation may not complete."` 这适用于任何修改，而不仅是删除。

## 合并集合

使用 `Concat()` 合并集合，并使用 `Distinct()` 去重。

```csharp
// All hidden objects (measures + columns) in a table
var hidden = table.Measures.Where(m => m.IsHidden).Cast<ITabularNamedObject>()
    .Concat(table.Columns.Where(c => c.IsHidden).Cast<ITabularNamedObject>());

// All unique tables referenced by selected measures
var tables = Selected.Measures
    .Select(m => m.Table)
    .Distinct();
```

## Dynamic LINQ 等效写法

在 BPA 规则表达式中，语法与 C# LINQ 不同。 Dynamic LINQ 没有 lambda 箭头 =>，使用关键字运算符，并将枚举按字符串进行比较。

| C# LINQ（脚本）                                   | Dynamic LINQ（BPA / 资源管理器筛选）         |
| --------------------------------------------- | ----------------------------------- |
| `m.IsHidden`                                  | `IsHidden`                          |
| `m.DataType == DataType.String`               | `DataType = "String"`               |
| `&&` / `\\\|\\\|` / `!`                   | `and` / `or` / `not`                |
| `==` / `!=`                                   | `=` / `!=` 或 `<>`                   |
| `table.Columns.Count(c => c.IsHidden)`        | `Columns.Count(IsHidden)`           |
| `table.Measures.Any(m => m.IsHidden)`         | `Measures.Any(IsHidden)`            |
| `table.Columns.All(c => c.Description != "")` | `Columns.All(Description != "")`    |
| `string.IsNullOrEmpty(m.Description)`         | `String.IsNullOrEmpty(Description)` |

> [!NOTE]
> 动态 LINQ 表达式会针对上下文中的单个对象进行求值。 没有与 `Model.AllMeasures` 或跨表查询等效的功能。 每条 BPA 规则都会针对其作用域内的每个对象对其表达式求值一次。

## 另见

- @advanced-scripting
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-dynamic-linq-vs-csharp-linq
