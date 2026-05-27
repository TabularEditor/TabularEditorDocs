---
uid: how-to-use-selected-object
title: 如何使用 Selected 对象
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用 Selected 对象

`Selected` 对象可用于访问 @tom-explorer-view-reference 树中当前选中的内容。 用它来编写脚本，使脚本操作用户选中的对象，而不是写死对象名称。

## 快速参考

```csharp
// Singular (exactly one selected, throws if 0 or 2+)
Selected.Measure
Selected.Table
Selected.Column

// Guard clause
if (Selected.Measures.Count() == 0) { Error("Select at least one measure."); return; }

// Iterate and modify
foreach (var m in Selected.Measures)
    m.FormatString = "0.00";

// Using ForEach extension
Selected.Measures.ForEach(m => m.DisplayFolder = "KPIs");
```

复数访问器（零个或多个，可安全迭代）：

- `Selected.Measures`
- `Selected.Tables`
- `Selected.Columns`
- `Selected.Hierarchies`
- `Selected.Partitions`
- `Selected.Levels`
- `Selected.CalculationItems`
- `Selected.Roles`
- `Selected.DataSources`

## 单数与复数访问器

`Selected` 对象为每种对象类型同时提供单数和复数访问器。

| 访问器                 | 返回                           | 当数量不为 1 时的行为                    |
| ------------------- | ---------------------------- | ------------------------------- |
| `Selected.Measure`  | 单个 `Measure`：度量值             | 如果选中了 0 个或 2 个以上度量值，则引发异常       |
| `Selected.Measures` | `IEnumerable<Measure>`：度量值集合 | 返回的集合可能为空，但绝不会为 null。 可直接安全地迭代。 |

当脚本要求恰好一个对象时，使用 **单数** 形式。 当脚本需要处理零个或多个对象时，请使用 **复数** 形式。

## 卫语句

复数访问器会返回零个或多个对象。 集合为空时，脚本可能什么也不做；也可能要求至少选中一定数量的对象。 对于后者，请使用卫语句。

```csharp
// Require at least one measure
if (Selected.Measures.Count() == 0)
{
    Error("No measures selected. Select one or more measures and run again.");
    return;
}
```

```csharp
// Require exactly one table
if (Selected.Tables.Count() != 1)
{
    Error("Select exactly one table.");
    return;
}
var table = Selected.Table;
```

对于接受多种对象类型的脚本，可组合使用检查：

```csharp
if (Selected.Columns.Count() == 0 && Selected.Measures.Count() == 0)
{
    Error("Select at least one column or measure.");
    return;
}
```

## 遍历所选对象

复数访问器会返回一个集合，你可以使用 `foreach` 或 LINQ 对其进行遍历。

```csharp
// Set display folder on all selected measures
foreach (var m in Selected.Measures)
    m.DisplayFolder = "Sales Metrics";

// Hide all selected columns
Selected.Columns.ForEach(c => c.IsHidden = true);

// Add to a perspective
Selected.Measures.ForEach(m => m.InPerspective["Sales"] = true);
```

## 处理选定的表

当选中单个表时，使用 `Selected.Table` 向其中添加新对象。

```csharp
var t = Selected.Table;
t.AddMeasure("Row Count", "COUNTROWS(" + t.DaxObjectFullName + ")");
```

## 混合选择

当你需要处理所选内容中的多种对象类型时，可以直接遍历 `Selected`。 `Selected` 变量本身实现了 `IEnumerable<ITabularNamedObject>`。

```csharp
foreach (var desc in Selected.OfType<IDescriptionObject>())
{
    desc.Description = "Reviewed on " + DateTime.Today.ToString("yyyy-MM-dd");
}
```

有关 LINQ 筛选的更多信息，请参阅 @how-to-filter-query-objects-linq；有关基于接口的对象处理，请参阅 @how-to-tom-interfaces。

## 在选择对话框中使用 try/catch

使用 `SelectTable()`、`SelectColumn()` 或 `SelectMeasure()` 等辅助方法时，将它们放在 try/catch 中，以处理用户取消操作。

```csharp
try
{
    var table = SelectTable(Model.Tables, null, "Pick a table:");
    Info("You selected: " + table.Name);
}
catch
{
    Error("No table selected.");
}
```

> [!NOTE]
> `Selected` 对象仅在交互式上下文中可用（Tabular Editor UI 和宏）。 通过带有 `-S` 标志的 CLI 运行脚本时，`Selected` 表示由 `-O` 参数指定的对象；如果未指定任何对象，则为空。

## 另见

- @C# 脚本
- @advanced-scripting
- @how-to-navigate-tom-hierarchy
- @脚本帮助方法
