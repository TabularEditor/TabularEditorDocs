---
uid: semantic-bridge-remove-object
title: 从 Metric View 中移除对象
author: Greg Baldini
updated: 2026-07-02
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          none: true
        - edition: Enterprise
          full: true
---

# 从 Metric View 中移除对象

本操作指南演示如何删除 Metric View 字段和度量值。类似的方法适用于 Metric View 中的所有集合。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。早期版本不支持此处展示的 v1.1 Metric View 功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> 这里的每个移除脚本都会影响当前已加载的 Metric View。如果你想把这些脚本都运行一遍，请确保在每次移除操作前都先运行上面的 `Deserialize`。

## 按名称移除

获取要删除的 Metric View 字段，然后删除它。删除对象后，请勿再尝试修改它。你仍可读取已删除对象的属性。对同一对象多次调用 `Delete()` 是安全的；第一次之后，其余调用都不会执行任何操作。

```csharp {run id=removefield setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

var fieldToRemove = view.Fields["order_month"];
fieldToRemove.Delete();
fieldToRemove.Delete(); // note we can call Delete twice safely
sb.AppendLine($"Removed: {fieldToRemove.Name}");

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**输出：**

```
Fields before: 6
Removed: order_month
Fields after: 5
```

可以看到，虽然多次调用了 `Delete()`，但实际只移除了一次。

## 移除一个度量值

移除度量值的方法相同：先获取该度量值的引用，再删除它。

```csharp {run id=removemeasure setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Measures before: {view.Measures.Count}");

var measureToRemove = view.Measures["gross_margin"];
measureToRemove.Delete();
sb.AppendLine($"Removed: {measureToRemove.Name}");

sb.AppendLine($"Measures after: {view.Measures.Count}");
Output(sb.ToString());
```

**输出：**

```
Measures before: 6
Removed: gross_margin
Measures after: 5
```

## 移除多个 Metric View 字段

先筛选出要移除的字段，用 `ToList` 为它们创建快照，然后逐个删除。先创建快照可避免在遍历集合时修改该集合。

```csharp {run id=removemultiple setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

// Remove all date-related fields
string[] toRemove = ["order_date", "order_year", "order_month"];

foreach (var field in view.Fields.Where(f => toRemove.Contains(f.Name)).ToList())
{
    field.Delete();
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
sb.AppendLine();
sb.AppendLine("Remaining fields:");
sb.AppendLine("-----------------");
foreach (var field in view.Fields)
{
    sb.AppendLine($"  {field.Name}");
}

Output(sb.ToString());
```

**输出：**

```
Fields before: 6
Fields after: 3

Remaining fields:
-----------------
  product_name
  product_category
  customer_segment
```

## 从指定表中移除 Metric View 字段

移除所有引用日期表的 Metric View 字段。

> [!WARNING]
> 此示例无法保证会移除所有引用指定 Metric View Join 的 Metric View 字段，也无法保证只移除这些字段。
> Metric View 字段可能包含几乎任意的 SQL 表达式，也可能引用之前定义的 Metric View 字段。此示例仅用于说明。

```csharp {run id=remove-by-table setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Fields before: {view.Fields.Count}");

foreach (var field in view.Fields.Where(f => f.Expr.StartsWith("date.")).ToList())
{
    field.Delete();
    sb.AppendLine($"Removed: {field.Name} ({field.Expr})");
}

sb.AppendLine($"Fields after: {view.Fields.Count}");
Output(sb.ToString());
```

**输出：**

```
Fields before: 6
Removed: order_date (date.full_date)
Removed: order_year (date.year)
Removed: order_month (date.month_name)
Fields after: 3
```

## 后续步骤

- [向指标视图添加对象](xref:semantic-bridge-add-object)
- [重命名字段](xref:semantic-bridge-rename-objects)
- [将指标视图序列化为 YAML](xref:semantic-bridge-serialize)

## 另见

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
