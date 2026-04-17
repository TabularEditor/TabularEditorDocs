---
uid: semantic-bridge-validate-default
title: 使用默认规则验证指标视图
author: Greg Baldini
updated: 2026-04-17
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

# 使用默认规则验证指标视图

本操作指南演示如何使用内置验证规则验证已加载的指标视图，并解读诊断信息。

## 默认验证规则

Semantic Bridge 内置以下验证规则：

| 规则                       | 说明                                                                                                          |
| ------------------------ | ----------------------------------------------------------------------------------------------------------- |
| JoinNameRequired         | 指标视图联接必须有名称                                                                                                 |
| UniqueJoinName           | 指标视图联接名称必须唯一                                                                                                |
| JoinSourceRequired       | 指标视图联接必须指定来源                                                                                                |
| JoinOnOrUsingRequired    | 指标视图联接必须指定 `on` 或 `using` 之一                                                                                |
| JoinOnOrUsingExclusivity | 指标视图的 Join 不能同时指定 `on` 和 `using`                                                                            |
| JoinOnFormat             | 指标视图 Join 的 `on` 子句必须是有效的等值连接条件                                                                             |
| JoinUsingColumnCOUNT     | Metric View Join `using` clause must have exactly one column (public preview limitation) |
| DimensionNameRequired    | 指标视图的维度必须有名称                                                                                                |
| UniqueDimensionName      | 指标视图的维度名称必须唯一                                                                                               |
| DimensionExprRequired    | 指标视图的维度必须有表达式                                                                                               |
| 度量值名称必填                  | 指标视图的度量值必须有名称                                                                                               |
| 度量值名称唯一                  | 指标视图的度量值名称必须唯一                                                                                              |
| 度量值表达式必填                 | 指标视图的度量值必须有表达式                                                                                              |

## 使用默认规则执行验证

不带参数调用 `Validate()` 即可使用内置验证规则。

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validation complete: {diagnostics.Count} issue(s) found");
```

## 解读诊断信息

每条诊断信息包含：

- **严重性**：错误、警告或信息
- **信息**：问题描述
- **路径**：对象在指标视图层级结构中的位置

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine("验证结果");
sb.AppendLine("------------------");
sb.AppendLine("");

if (diagnostics.Count == 0)
{
    sb.AppendLine("未发现任何问题。");
}
else
{
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"[{diag.Severity}] {diag.Message}");
        sb.AppendLine($"  路径: {diag.Path}");
        sb.AppendLine("");
    }
}

Output(sb.ToString());
```

## 包含验证错误的示例

有些规则（必填字段）会在反序列化时强制执行。
其余规则会在反序列化后检查重复项和结构问题。

这个指标视图展示了 `Validate()` 能捕获的违规情况：

```csharp
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    joins:
      # UniqueJoinName - 名称重复：'customer'
      - name: customer
        source: sales.dim.customer
        on: customer_id = customer.customer_id
      - name: customer
        source: sales.dim.customer_backup
        on: customer_id = customer_backup.customer_id
      # JoinOnOrUsingRequired - 未指定 on 或 using 子句
      - name: date
        source: sales.dim.date
    dimensions:
      # UniqueDimensionName - 名称重复：'category'
      - name: category
        expr: product.category
      - name: category
        expr: product.subcategory
      - name: product_name
        expr: product.product_name
    measures:
      # UniqueMeasureName - 度量值名称重复：'total'
      - name: total
        expr: SUM(revenue)
      - name: total
        expr: SUM(quantity)
      - name: order_count
        expr: COUNT(order_id)
    """);

var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"发现 {diagnostics.Count} 个问题：");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

**输出：**

```
共发现 6 个问题(s):

[Error] 联接 'customer' 必须使用带表前缀的简单相等条件（例如 'source.column = dimension.column'）
[Error] 联接名称重复：'customer'
[Error] 联接 'customer' 必须使用带表前缀的简单相等条件（例如 'source.column = dimension.column'）
[Error] 联接 'date' 必须指定 'on' 或 'using' 子句之一
[Error] 维度名称重复：'category'
[Error] 度量值名称重复：'total'
```

## 按严重性筛选诊断信息

你可以筛选诊断信息，只查看错误：

```csharp
using System.Linq;
using TabularEditor.SemanticBridge.Orchestration;

var diagnostics = SemanticBridge.MetricView.Validate().ToList();
var errors = diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"错误数： {errors.Count}");
sb.AppendLine($"问题总数： {diagnostics.Count}");
Output(sb.ToString());
```

## 后续步骤

- [创建简单验证规则](xref:semantic-bridge-validate-simple-rules)，以强制遵循你自己的约定
- [创建上下文验证规则](xref:semantic-bridge-validate-contextual-rules)，用于跨对象的检查

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
