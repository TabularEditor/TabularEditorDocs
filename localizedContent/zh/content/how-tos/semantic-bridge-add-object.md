---
uid: semantic-bridge-add-object
title: 向 Metric View 添加对象
author: Greg Baldini
updated: 2025-01-27
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

本操作指南演示如何将新的 Metric View 维度（字段）添加到已加载的 Metric View 中。
类似的方法也适用于所有 Metric View 集合。

[!INCLUDE [deserialize](includes/sample-metricview-deserialize.md)]

## 创建新的 Metric View 维度对象

使用 Metric View 的 `Dimension` 构造函数来创建新的 Metric View 维度：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var newDimension = new MetricView.Dimension
{
    Name = "customer_city",
    Expr = "customer.city"
};
```

## 添加到 Metric View 中

Metric View 的 `Dimensions` 属性是一个 `IList<Dimension>`，因此可以使用 `Add()` 方法：

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Dimensions before adding: {SemanticBridge.MetricView.Model.Dimensions.Count}");

var newDimension = new MetricView.Dimension
{
    Name = "customer_city",
    Expr = "customer.city"
};

SemanticBridge.MetricView.Model.Dimensions.Add(newDimension);

sb.AppendLine($"Dimensions after adding: {SemanticBridge.MetricView.Model.Dimensions.Count}");
Output(sb.ToString());
```

**输出**

```
Dimensions before adding: 8
Dimensions after adding: 9
```

## 另见

- @semantic-bridge-remove-object
- @semantic-bridge-rename-objects
- @semantic-bridge-serialize
