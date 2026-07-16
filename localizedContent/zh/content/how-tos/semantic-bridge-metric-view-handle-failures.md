---
uid: semantic-bridge-metric-view-handle-failures
title: 处理常见故障
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

# 处理常见故障

本操作指南介绍在 C# Script 中使用 Metric View 时，如何应对几种常见的故障模式：YAML 无效、文件缺失、在未加载 Metric View 的情况下执行操作，以及导入未能完成。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 更早版本不支持此处展示的 v1.1 Metric View 功能。

## 加载或反序列化失败

如果输入不是有效的 Metric View YAML，`Load` 和 `Deserialize` 会引发 `System.IO.InvalidDataException`。
该异常本身只表示加载失败；
具体原因记录在 `ImportDiagnostics` 中。
失败时，当前 Metric View（`SemanticBridge.MetricView.Model`）会被设置为 `null`。

```csharp {run id=failed-deserialize setup=none after=none output=true}
try
{
    // This Metric View is missing the required `source`, so it fails to deserialize.
    SemanticBridge.MetricView.Deserialize("""
        version: 1.1
        fields:
          - name: revenue
            expr: source.revenue
        """);
}
catch (System.IO.InvalidDataException)
{
    var sb = new System.Text.StringBuilder();
    sb.AppendLine("Could not load the Metric View:");
    foreach (var diag in SemanticBridge.MetricView.ImportDiagnostics)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
    }
    Output(sb.ToString());
}
```

**输出**

```
Could not load the Metric View:
  [Error] VIEW_SOURCE_REQUIRED: View source cannot be empty
```

> [!NOTE]
> `Load` 从文件路径读取，因此如果路径不存在，抛出的将是 `System.IO.FileNotFoundException`，而不是 `InvalidDataException`。
> 通过路径加载时，请捕获该异常（或更通用的 `System.Exception`）。

## 避免在未加载 Metric View 的情况下执行操作

如果未加载 Metric View，`Validate`、`Serialize`、`Save` 和 `ImportToTabular` 会引发 `System.InvalidOperationException`。
未加载任何内容时，`Model` 为 `null`，所以要先做检查。

在全新的 Tabular Editor 3 实例中运行此脚本，以确保当前未加载任何 Metric View：

```csharp {run id=guard-no-model setup=none after=none output=true}
if (SemanticBridge.MetricView.Model == null)
{
    Output("No Metric View is loaded. Load or deserialize one first.");
}
else
{
    var diagnostics = SemanticBridge.MetricView.Validate();
    Output($"Found {diagnostics.Count()} issue(s).");
}
```

**输出**

```
No Metric View is loaded. Load or deserialize one first.
```

如果不先做检查，在未加载任何内容时调用 `SemanticBridge.MetricView.Validate()` 会引发 `InvalidOperationException`。

## 导入无法完成

当导入无法完成时，`ImportToTabular` 和 `ImportToTabularFromFile` 会返回 `false`，而不是引发异常。
检查返回值，并读取 `out` 参数中的诊断信息以了解原因。

下面的示例先反序列化一个有效的 Metric View，
然后把某个字段的表达式清空，从而触发验证错误。
由于 `failOnValidationErrors` 默认为 `true`，
导入会在翻译前停止并返回 `false`，
原因会在 `out` 诊断信息中给出。
必须先打开一个表格模型。

```csharp {run id=import-incomplete setup=none after=none output=true}
// Load a valid Metric View, then make it invalid
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    fields:
      - name: order_year
        expr: source.order_year
    measures:
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = ""; // an empty expression is invalid

var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
if (success)
{
    sb.AppendLine("Import complete.");
}
else
{
    sb.AppendLine("Import did not complete:");
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
    }
}
Output(sb.ToString());
```

**输出**

```
Import did not complete:
  [Error] FIELD_EXPR_REQUIRED: Field 'order_year' expr cannot be empty
```

若希望在存在验证问题时仍继续导入，请自行承担风险，传入 `failOnValidationErrors: false`。
如果调用此方法时未加载任何指标视图，
将如上所述抛出 `InvalidOperationException`。

## 后续步骤

- [加载并检查指标视图](xref:semantic-bridge-load-inspect)
- [验证指标视图](xref:semantic-bridge-validate-default)
- [导入指标视图并查看诊断信息](xref:semantic-bridge-import)

## 另见

- [Semantic Bridge 概述](xref:semantic-bridge)
