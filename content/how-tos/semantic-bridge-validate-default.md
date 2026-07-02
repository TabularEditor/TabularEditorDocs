---
uid: semantic-bridge-validate-default
title: Validate a Metric View with Default Rules
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
# Validate a Metric View with Default Rules

This how-to demonstrates validating a loaded Metric View using the built-in validation rules and interpreting the diagnostic messages.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Default validation rules

The Semantic Bridge includes built-in rules that validate a Metric View definition against rules defined in [the Databricks documentation](https://learn.microsoft.com/en-us/azure/databricks/business-semantics/).
These rules are automatically run upon deserialization, whether via `Deserialize` directly or any method that reads a Metric View, such as `Load` or `ImportToTabularFromFile`.
Diagnostics from those automatic runs remain available afterward through `SemanticBridge.MetricView.ImportDiagnostics`.
You can also run these rules on demand against the loaded Metric View, which this document covers.

## Run validation with default rules

Run [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) with no arguments to run the built-in rules against the loaded Metric View.

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validation complete: {diagnostics.Count} issue(s) found");
```

The sample Metric View is valid, so this reports no issues.

## Interpret diagnostic messages

Each diagnostic message contains:

- **Severity**: Error, Warning, or Information
- **Message**: Description of the issue
- **Path**: Location of the object in the Metric View hierarchy

```csharp
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

## Example with a validation error

Validation always runs against the currently loaded Metric View, so you can introduce a violation in a script and see it caught.
Here we clear a field's expression to trigger `FieldExprRequired`:

```csharp
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

**Output:**

```
<!-- TODO: capture from a run; expect one FieldExprRequired error -->
```

## Filter diagnostics by severity

You can filter diagnostics to focus on errors only:

```csharp
using System.Linq;
using TabularEditor.SemanticBridge.Orchestration;

var diagnostics = SemanticBridge.MetricView.Validate().ToList();
var errors = diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Errors: {errors.Count}");
sb.AppendLine($"Total issues: {diagnostics.Count}");
Output(sb.ToString());
```

## Next steps

- [Create simple validation rules](xref:semantic-bridge-validate-simple-rules)
- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules)

## See also

- [Semantic Bridge Validation](xref:semantic-bridge-metric-view-validation)
- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
