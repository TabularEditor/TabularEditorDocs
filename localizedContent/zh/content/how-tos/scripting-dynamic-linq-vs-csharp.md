---
uid: how-to-dynamic-linq-vs-csharp-linq
title: Dynamic LINQ 与 C# LINQ 的区别
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Dynamic LINQ 与 C# LINQ 的区别

C# Script 使用标准的 C# LINQ，并使用 Lambda 表达式。 Best Practice Analyzer (BPA) 规则和 Explorer 树筛选器使用 [Dynamic LINQ](https://dynamic-linq.net/expression-language)，这是一种基于字符串的表达式语言，其语法与常规 LINQ 不同。 本文提供两者之间的对照翻译指南。

## 各自的使用场景

| 上下文                             | 语法                           |
| ------------------------------- | ---------------------------- |
| C# Script 和宏                    | C# LINQ                      |
| BPA 规则表达式                       | Dynamic LINQ                 |
| BPA 修复表达式                       | Dynamic LINQ（赋值时使用 `it.` 前缀） |
| **TOM Explorer** 树筛选器（`:` 前缀）\* | Dynamic LINQ                 |

\* 仅适用于 Tabular Editor 2。

## 语法对比

在 Dynamic LINQ 中，对象是隐式的——没有像 `m.` 或 `c.` 这样的 lambda 参数。 在 BPA 中，上下文由 **适用于** 范围设置决定，它会确定表达式是针对哪种对象类型求值的。

| 概念             | C# LINQ（脚本）                                | Dynamic LINQ（BPA / 筛选器）                  |
| -------------- | ------------------------------------------ | ---------------------------------------- |
| 逻辑与            | `&&`                                       | `and`                                    |
| 逻辑或            | `\\|\\|`                                 | `or`                                     |
| 逻辑非            | `!`                                        | `not`                                    |
| 等于             | `==`                                       | `=`                                      |
| 不等于            | `!=`                                       | `!=` 或 `<>`                              |
| 大于/小于          | `>`, `<`, `>=`, `<=`                       | `>`, `<`, `>=`, `<=`                     |
| 字符串包含          | `m.Name.Contains("Sales")`                 | `Name.Contains("Sales")`                 |
| 字符串以某内容开头      | `m.Name.StartsWith("Sum")`                 | `Name.StartsWith("Sum")`                 |
| 字符串以某内容结尾      | `m.Name.EndsWith("YTD")`                   | `Name.EndsWith("YTD")`                   |
| Null/空值/空字符串检查 | `string.IsNullOrEmpty(m.Description)`      | `String.IsNullOrEmpty(Description)`      |
| 空白字符检查         | `string.IsNullOrWhiteSpace(m.Description)` | `String.IsNullOrWhitespace(Description)` |
| 正则表达式匹配        | `Regex.IsMatch(m.Name, "pattern")`         | `RegEx.IsMatch(Name, "pattern")`         |

## 枚举值比较

C# 使用强类型的枚举值。 Dynamic LINQ 使用字符串表示形式。

| C# LINQ                                                             | Dynamic LINQ                                |
| ------------------------------------------------------------------- | ------------------------------------------- |
| `c.DataType == DataType.String`                                     | `DataType = "String"`                       |
| `p.SourceType == PartitionSourceType.M`                             | `SourceType = "M"`                          |
| `p.Mode == ModeType.DirectLake`                                     | `Mode = "DirectLake"`                       |
| `r.CrossFilteringBehavior == CrossFilteringBehavior.BothDirections` | `CrossFilteringBehavior = "BothDirections"` |

## Lambda 表达式与隐式上下文

C# LINQ 使用显式的 lambda 参数。 Dynamic LINQ 会在隐式的 `it` 上下文对象中对属性求值。

```csharp
// C# LINQ: explicit lambda parameter
Model.AllMeasures.Where(m => m.IsHidden && m.Description == "");
```

```
// Dynamic LINQ: implicit "it" -- properties are accessed directly
IsHidden and Description = ""
```

## 父对象导航

两者都使用点号表示法，但在 C# 中必须显式指定 lambda 参数。

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.Table.IsHidden);
```

```
// Dynamic LINQ
Table.IsHidden
```

## 集合方法

C# LINQ 在集合方法中使用 lambda 表达式。 Dynamic LINQ 在集合方法中使用隐式上下文，并用 `outerIt` 引用父对象。

```csharp
// C# LINQ: count columns with no description
Model.Tables.Where(t => t.Columns.Count(c => c.Description == "") > 5);
```

```
// Dynamic LINQ: same logic
Columns.Count(Description = "") > 5
```

### `outerIt` 关键字

在 Dynamic LINQ 的嵌套集合方法中，`it` 指的是内层对象（例如列）。 使用 `outerIt` 引用外层对象（例如表）。

```
// BPA rule on Tables: find tables where any column name matches the table name
Columns.Any(Name = outerIt.Name)
```

在 C# 中，外层 lambda 参数 `t` 在内层 lambda 的整个函数体中始终都在作用域内。 内层 lambda `c => c.Name == t.Name` 可以直接引用 `t`，因为它被闭包捕获了。

```csharp
// C# equivalent -- t is accessible inside the inner lambda via closure
Model.Tables.Where(t => t.Columns.Any(c => c.Name == t.Name));
```

## 类型筛选

C# 使用 `OfType<T>()` 或 `is`。 在 BPA 中，规则的 **适用于** 范围负责进行类型筛选。 无需在表达式本身中进行类型检查。

| C# LINQ                                        | Dynamic LINQ 写法           |
| ---------------------------------------------- | ------------------------- |
| `Model.AllColumns.OfType<CalculatedColumn>()`  | 将 BPA 规则的适用范围设置为 **计算列**  |
| `Model.Tables.OfType<CalculationGroupTable>()` | 将 BPA 规则的适用范围设置为 **计算组表** |

## 依赖属性

这些属性在两种语法中的工作方式完全相同，但 Dynamic LINQ 省略了对象前缀。

| C# LINQ                       | Dynamic LINQ                |
| ----------------------------- | --------------------------- |
| `m.ReferencedBy.Count == 0`   | `ReferencedBy.Count = 0`    |
| `m.DependsOn.Any()`           | `DependsOn.Any()`           |
| `c.UsedInRelationships.Any()` | `UsedInRelationships.Any()` |
| `c.ReferencedBy.AnyVisible`   | `ReferencedBy.AnyVisible`   |

## 注释方法

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.HasAnnotation("AUTOGEN"));
```

```
// Dynamic LINQ
HasAnnotation("AUTOGEN")
```

| C# LINQ                             | Dynamic LINQ                     |
| ----------------------------------- | -------------------------------- |
| `m.GetAnnotation("key") == "value"` | `GetAnnotation("key") = "value"` |
| `m.HasAnnotation("key")`            | `HasAnnotation("key")`           |

## 透视与翻译索引器

```csharp
// C# LINQ
Model.AllMeasures.Where(m => m.InPerspective["Sales"]);
```

```
// Dynamic LINQ
InPerspective["Sales"]
```

| C# LINQ                                            | Dynamic LINQ                                     |
| -------------------------------------------------- | ------------------------------------------------ |
| `m.InPerspective["Sales"]`                         | `InPerspective["Sales"]`                         |
| `!m.InPerspective["Sales"]`                        | `not InPerspective["Sales"]`                     |
| `string.IsNullOrEmpty(m.TranslatedNames["da-DK"])` | `String.IsNullOrEmpty(TranslatedNames["da-DK"])` |

## BPA 修复表达式

在修复表达式中，使用 `it.` 作为赋值目标。 `it` 指的是违反该规则的那个特定对象——也就是 BPA 结果列表中高亮显示的同一个对象。

例如，如果有一条 BPA 规则，其表达式为 `IsHidden and String.IsNullOrWhitespace(Description)`，并应用于 **度量值**，则每个匹配的度量值都会显示在 BPA 结果中。 应用修复时，`it` 指的就是那个特定的度量值：

```
// Set the description on the violating measure
it.Description = "TODO: Add description"

// Unhide the violating object
it.IsHidden = false
```

虽然修复表达式没有直接对应的 C# LINQ 写法，但你可以在脚本中实现相同的效果：

```csharp
foreach (var m in Model.AllMeasures.Where(m => m.IsHidden && string.IsNullOrWhiteSpace(m.Description)))
{
    m.Description = "TODO: Add description";
}
```

## 完整示例：同一条规则的两种语法

**目标：** 找出已隐藏、无引用且无描述的度量值。

C# Script：

```csharp
var unused = Model.AllMeasures
    .Where(m => m.IsHidden
        && m.ReferencedBy.Count == 0
        && string.IsNullOrWhiteSpace(m.Description));

foreach (var m in unused)
    Info(m.DaxObjectFullName);
```

BPA 规则表达式（应用于度量值）：

```
IsHidden and ReferencedBy.Count = 0 and String.IsNullOrWhitespace(Description)
```

## 另见

- @using-bpa-sample-rules-expressions
- @advanced-filtering-explorer-tree
- @最佳实践分析器
- @how-to-filter-query-objects-linq
