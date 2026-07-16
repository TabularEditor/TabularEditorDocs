---
uid: semantic-bridge-validate-default
title: 使用默认规则验证指标视图
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

# 使用默认规则验证指标视图

This how-to demonstrates validating a loaded Metric View using the built-in validation rules and interpreting the diagnostic messages.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## 默认验证规则

The Semantic Bridge includes built-in rules that validate a Metric View definition against rules defined in [the Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/).
These rules are automatically run upon deserialization, whether via `Deserialize` directly or any method that reads a Metric View, such as `Load` or `ImportToTabularFromFile`.
Diagnostics from those automatic runs remain available afterward through `SemanticBridge.MetricView.ImportDiagnostics`.
You can also run these rules on demand against the loaded Metric View, which this document covers.

## 使用默认规则执行验证

Run [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) with no arguments to run the built-in rules against the loaded Metric View.

```csharp {run id=validate-count setup=mv-sample after=none output=true}
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validation complete: {diagnostics.Count} issue(s) found");
```

**输出**

```
Validation complete: 0 issue(s) found
```

The sample Metric View is valid, so this reports no issues.

## 解读诊断信息

每条诊断信息包含：

- **严重性**：错误、警告或信息
- **信息**：问题描述
- **路径**：对象在指标视图层级结构中的位置

```csharp {run id=interpret setup=mv-sample after=none output=true}
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

**输出**

```
VALIDATION RESULTS
------------------

No issues found.
```

## Example with a validation error

Validation always runs against the currently loaded Metric View, so you can introduce a violation in a script and see it caught.
Here we clear a field's expression to trigger `FieldExprRequired`:

```csharp {run id=error-example setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = "";

var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine("VALIDATION RESULTS");
sb.AppendLine("------------------");
sb.AppendLine("");

if (diagnostics.Count == 0)
{
    sb.AppendLine("No issues found.");
}
else
{
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"[{diag.Severity}] {diag.Message}");
        sb.AppendLine($"  Path: {diag.Path}");
        sb.AppendLine("");
    }
}

Output(sb.ToString());
```

**输出：**

```
VALIDATION RESULTS
------------------

[Error] Field 'order_year' expr cannot be empty
  Path: Model.Fields["order_year"].Expr
```

## 按严重性筛选诊断信息

你可以筛选诊断信息，只查看错误：

```csharp {run id=filter-severity setup=mv-sample after=none output=true}
using System.Linq;
using TabularEditor.SemanticBridge.Orchestration;

var diagnostics = SemanticBridge.MetricView.Validate().ToList();
var errors = diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"错误数： {errors.Count}");
sb.AppendLine($"问题总数： {diagnostics.Count}");
Output(sb.ToString());
```

**输出**

```
Errors: 0
Total issues: 0
```

## 后续步骤

- [Create simple validation rules](xref:semantic-bridge-validate-simple-rules)
- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules)

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
