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

本操作指南演示如何使用内置验证规则验证已加载的指标视图，并解读诊断信息。

> [!NOTE]
> 这些操作指南适用于 Tabular Editor 3.26.2 及更高版本。
> 较早版本不支持此处展示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

## 默认验证规则

Semantic Bridge 包含内置规则，可依据 [指标视图文档](https://learn.microsoft.com/azure/databricks/business-semantics/) 中定义的规则来验证指标视图定义。
这些规则会在反序列化时自动运行——无论是直接调用 `Deserialize`，还是通过任何读取指标视图的方法(如 `Load` 或 `ImportToTabularFromFile`)。
这些自动运行产生的诊断信息随后仍可通过 `SemanticBridge.MetricView.ImportDiagnostics` 获取。
你也可以按需对已加载的指标视图运行这些规则，本文将介绍这一做法。

## 使用默认规则执行验证

运行不带参数的 [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate)，即可对已加载的指标视图运行内置规则。

```csharp {run id=validate-count setup=mv-sample after=none output=true}
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validation complete: {diagnostics.Count} issue(s) found");
```

**输出**

```
验证完成：发现 0 个问题(s)
```

示例指标视图有效，因此此处的 Report 不会显示任何问题。

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
验证结果
------------------

未发现任何问题。
```

## 包含验证错误的示例

验证始终针对当前已加载的指标视图运行，因此你可以在脚本中故意引入违规，并确认它会被检测出来。
这里我们将某个字段的表达式清空，以触发 `FieldExprRequired`：

```csharp {run id=error-example setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = "";

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

**输出：**

```
验证结果
------------------

[错误] 字段 'order_year' 的 expr 不能为空
  路径：Model.Fields["order_year"].Expr
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
错误：0
问题总数：0
```

## 后续步骤

- [创建简单验证规则](xref:semantic-bridge-validate-simple-rules)
- [创建上下文验证规则](xref:semantic-bridge-validate-contextual-rules)

## 另见

- [Semantic Bridge 验证](xref:semantic-bridge-metric-view-validation)
- [指标视图对象模型](xref:semantic-bridge-metric-view-object-model)
