---
uid: semantic-bridge-import
title: Import a Metric View and View Diagnostics
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

```csharp
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

**Output:**

```
<!-- TODO: capture import result from a run -->
```

## Review the last import's diagnostics

The diagnostics from the most recent import are available at any time through `ImportDiagnostics`, including after an import done through the GUI.

```csharp
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

## See a translation diagnostic

Some Metric View constructs cannot be translated to Tabular.
A window measure, for example, is not translated to DAX:
the import creates a placeholder TOM measure with the original Metric View definition in a comment
and reports a diagnostic warning to you.

Add a window spec to a measure, then import to see the diagnostic:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a window spec
view.Measures["total_revenue"].Window =
[
    new MetricView.Window
    {
        Order = "order_date",
        Range = "trailing 3 months",
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
sb.AppendLine($"TOM measure expression: {Model.AllMeasures.First(m => m.Name == "total_revenue").Expression}");
Output(sb.ToString());
```

**Output:**

```
<!-- TODO: capture from a run; expect a MEASURE_WINDOW_UNSUPPORTED warning -->
```

## See also

- [Semantic Bridge Overview](xref:semantic-bridge)
- [Import a Metric View from a file](xref:semantic-bridge-metric-view-import-from-file)
- [Validate a Metric View](xref:semantic-bridge-validate-default)
- [Load and Inspect a Metric View](xref:semantic-bridge-load-inspect)
