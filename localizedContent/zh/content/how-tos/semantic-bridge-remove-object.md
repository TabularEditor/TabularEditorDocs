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

This how-to demonstrates removing Metric View fields and measures.
类似的方法适用于 Metric View 中的所有集合。

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> 这里的每个移除脚本都会影响当前已加载的 Metric View。
> 如果你想把这些脚本都运行一遍，请确保在每次移除操作前都先运行上面的 `Deserialize`。

## 按名称移除

Get the Metric View field and delete it.
After you delete an object, you should not attempt to modify it.
You can still read properties off of the deleted object.
It is safe to call `Delete()` on an object multiple times; after the first, these are no-ops.

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

Observe that there are multiple calls to `Delete()` but only one removal.

## Remove a measure

Measures are removed the same way: get a reference to the measure and delete it.

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

## Remove multiple Metric View fields

Filter to the fields you want to remove, snapshot them with `ToList`, then delete each one.
Snapshotting first avoids modifying the collection while iterating it.

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

## Remove Metric View fields from a specific table

Remove all Metric View fields that reference the date table.

> [!WARNING]
> This example is not guaranteed to remove all and exclusively Metric View fields which reference a given Metric View Join.
> Metric View fields may include near-arbitrary SQL expressions, and may also reference previously defined Metric View fields.
> 此示例仅用于说明。

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

- [Add objects to a Metric View](xref:semantic-bridge-add-object)
- [Rename a field](xref:semantic-bridge-rename-objects)
- [Serialize a Metric View to YAML](xref:semantic-bridge-serialize)

## 另请参阅

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
