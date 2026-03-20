---
uid: semantic-bridge-import
title: 导入指标视图并查看诊断信息
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

# 导入指标视图并查看诊断信息

本教程演示如何使用 C# Script 将指标视图导入表格模型，以及如何查看导入过程中输出的诊断信息。

## 先决条件

导入之前，你必须先在 Tabular Editor 中打开一个表格模型。 可以是：

- 一个新的空模型
- 一个现有模型，你希望使用指标视图中的对象对其进行扩展

## 导入方法

有两种导入方法：

| 方法                        | 说明                |
| ------------------------- | ----------------- |
| `ImportToTabularFromFile` | 从指定文件路径加载，并一步完成导入 |
| `ImportToTabular`         | 导入当前已加载的指标视图      |

两种方法都需要：

- 目标 Tabular `Model`
- Databricks 主机名（用于 M 分区表达式）
- Databricks HTTP 路径（用于 M 分区表达式）

## 从文件导入

使用 `ImportToTabularFromFile` 一次完成加载和导入：

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "C:/MetricViews/sales-metrics.yaml",
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
if (success)
{
    sb.AppendLine("导入成功！");
    sb.AppendLine($"诊断信息： {diagnostics.Count}");
}
else
{
    sb.AppendLine("导入失败。");
    sb.AppendLine($"错误： {diagnostics.Count}");
}

Output(sb.ToString());
```

## 导入已加载的 Metric View

如果你已经加载了 Metric View（用于检查或修改），就用 `ImportToTabular`：

```csharp
// 先加载 Metric View
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");

// 可选：检查或修改
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"正在导入包含 {view.Dimensions.Count} 个维度和 {view.Measures.Count} 个度量值的 Metric View");

// 导入到 Tabular
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

if (success)
{
    sb.AppendLine("导入成功！");
}
else
{
    sb.AppendLine("导入失败。");
}

Output(sb.ToString());
```

## 使用占位符连接值

如果你在没有真实 Databricks 连接的情况下测试翻译，可以使用占位符值：

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "C:/MetricViews/sales-metrics.yaml",
    Model,
    "placeholder-host",
    "placeholder-path",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine("导入完成（使用占位符连接值）");
sb.AppendLine("注意：请在刷新数据之前更新 M 分区表达式。");
Output(sb.ToString());
```

## 导入后查看诊断信息

你可以随时通过 `ImportDiagnostics` 访问上一次导入的诊断信息。
此示例假定你之前已经运行过一次导入，可以通过 GUI 或 C# Script 进行。

```csharp
var diagnostics = SemanticBridge.MetricView.ImportDiagnostics;

var sb = new System.Text.StringBuilder();
sb.AppendLine("上次导入诊断信息");
sb.AppendLine("-----------------------");
sb.AppendLine("");
sb.AppendLine($"问题总数： {diagnostics.Count}");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

## 直接输出诊断信息

为了快速查看，你可以直接输出诊断信息集合：

```csharp
// 输出上一次导入的全部诊断信息
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

## 完整工作流示例

加载、验证并导入，并输出完整的诊断报告：

```csharp
var sb = new System.Text.StringBuilder();

// 加载 Metric View
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("Metric View 概览");
sb.AppendLine("-------------------");
sb.AppendLine($"来源： {view.Source}");
sb.AppendLine($"连接数： {view.Joins?.Count ?? 0}");
sb.AppendLine($"维度数： {view.Dimensions.Count}");
sb.AppendLine($"度量值数： {view.Measures.Count}");
sb.AppendLine("");

// 先验证
var validationDiags = SemanticBridge.MetricView.Validate().ToList();
sb.AppendLine("验证");
sb.AppendLine("----------");
sb.AppendLine($"问题数： {validationDiags.Count}");
sb.AppendLine("");

// 导入
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var importDiags
);

sb.AppendLine("导入结果");
sb.AppendLine("-------------");
sb.AppendLine($"是否成功： {success}");
sb.AppendLine($"诊断信息： {importDiags.Count}");
sb.AppendLine("");

if (importDiags.Count > 0)
{
    sb.AppendLine("导入问题：");
    foreach (var diag in importDiags)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Message}");
    }
}

Output(sb.ToString());
```

## 另见

- [Semantic Bridge 概览](xref:semantic-bridge)
- [验证指标视图](xref:semantic-bridge-validate-default)
- [加载并检查指标视图](xref:semantic-bridge-load-inspect)
