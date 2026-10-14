---
uid: semantic-bridge-import
title: 导入指标视图并查看诊断信息
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

# 导入指标视图并查看诊断信息

这篇操作指南演示如何使用 C# Script 将已加载的指标视图导入到表格模型中，以及如何查看导入产生的诊断信息。

> [!NOTE]
> 这些操作指南面向 Tabular Editor 3.26.2 及更高版本。早期版本不支持此处展示的 v1.1 指标视图功能。

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> 下面的每个示例都会导入到当前打开的表格模型中。如果要运行多个示例，建议在每个示例之后撤销导入（菜单中选择 Edit>Undo，或在 TOM Explorer 中按 CTRL-z）。如果依次执行每次导入，就会生成多个已转换的指标视图副本。

## 导入已加载的指标视图

`ImportToTabular` 会将当前加载的指标视图转换为当前打开的表格模型。构建 M 分区表达式时会用到 Databricks 主机名和 HTTP 路径；
如需快速测试，可以先传入占位值，再在刷新数据前修正。

```csharp {run id=import setup=mv-sample after=none output=true}
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Imported {Model.AllColumns.Count()} fields and {Model.AllMeasures.Count()} measures.");
sb.AppendLine(success ? "Import successful." : "Import failed.");
sb.AppendLine($"Diagnostics: {diagnostics.Count}");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
Output(sb.ToString());
```

**输出：**

```
Imported 15 fields and 6 measures.
Import successful.
Diagnostics: 0
```

注意，导入的字段数包括联接键和指标视图定义中的隐式列引用，
因此会大于指标视图定义中显式 `Fields` 的数量。

## 查看最近一次导入的诊断信息

最近一次导入产生的诊断信息可随时通过 `ImportDiagnostics` 获取，即使该次导入是通过 GUI 执行的也一样。

```csharp {compile}
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
    Output($"[{d.Severity}] {d.Code}: {d.Message}");
```

## 查看翻译诊断信息

某些指标视图中的结构无法转换为 Tabular。例如，窗口度量值不会转换为 DAX：
导入时会创建一个占位 TOM 度量值，并在注释中保留原始指标视图定义，
同时向你 Report 一条诊断警告。

向某个度量值添加窗口规范，然后导入以查看诊断信息：

```csharp {run id=window-diagnostic setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a window spec
view.Measures["total_revenue"].Window =
[
    new MetricView.Window
    {
        Order = "order_date",
        Range = "trailing 3 month",
        Semiadditive = MetricView.Window.SemiadditiveType.Last
    }
];

var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine(success ? "Import succeeded with issues." : "Import failed.");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
// note that we search for the DisplayName, as that is what is translated to TOM
sb.AppendLine($"TOM measure expression: {Model.AllMeasures.First(m => m.Name == "Total Revenue").Expression}");
Output(sb.ToString());
```

**输出：**

```
Import succeeded with issues.
  [Warning] MEASURE_WINDOW_UNSUPPORTED: Measure 'Total Revenue' uses a window specification that is not currently supported; it has been left inert with the original definition preserved as a comment.
TOM measure expression: // This measure uses a window specification (windowed / cumulative / semiadditive),
// which is not currently supported when importing Databricks Metric Views.
// The measure has been left blank - review the details below and author the DAX
// manually. The translated DAX does NOT account for the window spec; you will most
// likely need to wrap it in CALCULATE (or similar) to apply the windowing.
//
// Original source expression (Databricks SQL):
/*
SUM(revenue)
*/
//
// Suggested DAX translation (window spec NOT applied):
/*
SUM('Fact'[revenue])
*/
//
// Window specification:
/*
- order: order_date
  range: trailing 3 month
  semiadditive: last

*/
```

## 后续步骤

- [从文件导入指标视图](xref:semantic-bridge-metric-view-import-from-file)
- [加载并查看指标视图](xref:semantic-bridge-load-inspect)
- [验证指标视图](xref:semantic-bridge-validate-default)

## 另请参阅

- [Semantic Bridge 概述](xref:semantic-bridge)
