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

# Import a Metric View and view diagnostics

This how-to demonstrates importing a loaded Metric View into a Tabular model with a C# script, and reviewing the diagnostic messages the import produces.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Each example below imports into the open Tabular model.
> To run more than one, we recommend that you undo the import after each example (Edit>Undo in the menu, or CTRL-z in the TOM Explorer).
> If you run each import one after the other, you will get multiple translated copies of the Metric View.

## Import the loaded Metric View

`ImportToTabular` translates the currently loaded Metric View into the open Tabular model.
The Databricks hostname and HTTP path are used when we build the M partition expressions;
for a quick test you can pass placeholder values and fix them before refreshing data.

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

Note that the number of fields imported includes join keys and implicit column references from the Metric View definition,
so it is larger than the number of explicit `Fields` in the Metric View definition.

## Review the last import's diagnostics

The diagnostics from the most recent import are available at any time through `ImportDiagnostics`, including after an import done through the GUI.

```csharp {compile}
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
    Output($"[{d.Severity}] {d.Code}: {d.Message}");
```

## See a translation diagnostic

Some Metric View constructs cannot be translated to Tabular.
A window measure, for example, is not translated to DAX:
the import creates a placeholder TOM measure with the original Metric View definition in a comment
and reports a diagnostic warning to you.

Add a window spec to a measure, then import to see the diagnostic:

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

- [Import a Metric View from a file](xref:semantic-bridge-metric-view-import-from-file)
- [Load and inspect a Metric View](xref:semantic-bridge-load-inspect)
- [验证指标视图](xref:semantic-bridge-validate-default)

## 另见

- [Semantic Bridge 概览](xref:semantic-bridge)
