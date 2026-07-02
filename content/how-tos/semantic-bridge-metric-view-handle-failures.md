---
uid: semantic-bridge-metric-view-handle-failures
title: Handle Common Failures
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
# Handle common failures

This how-to shows how to handle several common failure modes when working with Metric Views in C# scripts:
invalid YAML, missing files, operations with no loaded metric view, and an import that does not complete.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## A failed load or deserialize

`Load` and `Deserialize` throw `System.IO.InvalidDataException` when the input does not represent valid Metric View YAML.
The exception itself only signals that loading failed;
the specific reasons are captured in `ImportDiagnostics`.
On failure, the current Metric View (`SemanticBridge.MetricView.Model`) is set to `null`.

```csharp
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

**Output**

```
todo
```

> [!NOTE]
> `Load` reads from a file path, so a path that does not exist throws `System.IO.FileNotFoundException` instead of `InvalidDataException`.
> Catch that (or a broader `System.Exception`) when loading by path.

## Guard against no loaded Metric View

`Validate`, `Serialize`, `Save`, and `ImportToTabular` throw `System.InvalidOperationException` if no Metric View is loaded.
`Model` is `null` when nothing is loaded, so guard against it.

Run this script in a fresh Tabular Editor 3 instance to ensure you have no loaded Metric View:

```csharp
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

**Output**

```
todo
```

Without the guard, calling `SemanticBridge.MetricView.Validate()` with nothing loaded throws `InvalidOperationException`.

## An import that does not complete

`ImportToTabular` and `ImportToTabularFromFile` return `false` when the import cannot complete, rather than throwing an exception.
Check the return value and read the `out` diagnostics to see why.

The example below deserializes a valid Metric View,
then edits a field's expression to be blank, which yields a validation error.
Because `failOnValidationErrors` defaults to `true`,
the import stops before translating and returns `false`,
with the reasons in the `out` diagnostics.
A Tabular model must be open.

```csharp
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

**Output**

```
todo
```

Pass `failOnValidationErrors: false` at your own risk if you'd like to import despite validation issues.
If no Metric View is loaded when you call this,
it throws `InvalidOperationException` as described above.

## Next steps

- [Load and inspect a Metric View](xref:semantic-bridge-load-inspect)
- [Validate a Metric View](xref:semantic-bridge-validate-default)
- [Import a Metric View and view diagnostics](xref:semantic-bridge-import)

## See also

- [Semantic Bridge Overview](xref:semantic-bridge)
