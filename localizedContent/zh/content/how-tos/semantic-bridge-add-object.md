---
uid: semantic-bridge-add-object
title: 向 Metric View 添加对象
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

# 向 Metric View 添加对象

这篇操作指南演示如何向已加载的指标视图添加新对象并设置其属性。类似的方法也适用于所有 Metric View 集合。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。较早版本不支持此处展示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 添加字段

使用 [`AddField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddField%2A) 创建并返回一个新的 `Field` 对象，供你进一步操作。

```csharp {run id=addfield setup=mv-sample after=none output=true}
var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

sb.AppendLine($"Fields before adding: {view.Fields.Count}");

var field = view.AddField("customer_city", "customer.city");

sb.AppendLine($"Fields after adding: {view.Fields.Count}");
Output(sb.ToString());
```

**输出**

```
Fields before adding: 6
Fields after adding: 7
```

## 添加并配置 `Join`

[`AddJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddJoin%2A)
与 `AddField` 的工作方式类似：它会构造该对象，将其添加到指标视图，并返回该对象，以便你设置更多属性。使用 [`JoinCardinality`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.JoinCardinality) 枚举设置基数。

```csharp {run id=addjoin setup=mv-sample after=none output=false}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a join, then set its remaining properties
var supplier = view.AddJoin("supplier", "sales.dim.supplier");
supplier.On = "source.supplier_id = supplier.supplier_id";
supplier.Cardinality = MetricView.JoinCardinality.ManyToOne;
```

在任何现有的 `Join` 上也可以调用 `AddJoin` 方法。你可以用它来创建嵌套联接，例如 `supplier.AddJoin("region", "sales.dim.region")`，
用于对雪花维度建模。

## 添加并配置 `度量值`

[`AddMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.View.AddMeasure%2A) 的工作方式与其他 `Add` 方法类似。

某些属性，例如字段或度量值的 `Format`，有各自的类型，你需要构造这些类型来设置该属性。创建你需要的 [`Format`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Format) 变体，例如 `Format.Currency` 或 `Format.Percentage`，并将其赋值。

```csharp {run id=addmeasure setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var sb = new System.Text.StringBuilder();
var view = SemanticBridge.MetricView.Model;

// add a new measure, then give it a currency format
var totalCost = view.AddMeasure("total_cost", "SUM(cost)");
totalCost.Format = new MetricView.Format.Currency { CurrencyCode = "USD" };

// read the format back off the measure
sb.AppendLine($"{totalCost.Name} format: {totalCost.Format}");
Output(sb.ToString());
```

**输出**

```
total_cost format: Currency { Type = Currency, DecimalPlaces = , HideGroupSeparator = , Abbreviation = , CurrencyCode = USD }
```

## 后续步骤

- [从指标视图中删除对象](xref:semantic-bridge-remove-object)
- [重命名字段](xref:semantic-bridge-rename-objects)
- [将指标视图序列化为 YAML](xref:semantic-bridge-serialize)

## 另请参阅

- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
