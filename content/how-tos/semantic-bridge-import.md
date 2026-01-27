---
uid: semantic-bridge-import
title: Import a Metric View and View Diagnostics
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
# Import a Metric View and View Diagnostics

This how-to demonstrates how to import a Metric View into a Tabular model using C# scripts, and how to view diagnostic messages from the import process.

## Prerequisites

You must have a Tabular model open in Tabular Editor before importing. This can be:

- A new, empty model
- An existing model you want to enhance with objects from the Metric View

## Import methods

There are two import methods:

| Method                    | Description                                    |
|---------------------------|------------------------------------------------|
| `ImportToTabularFromFile` | Loads from a file path and imports in one step |
| `ImportToTabular`         | Imports the currently loaded Metric View       |

Both methods require:

- The target Tabular `Model`
- Databricks hostname (for M partition expressions)
- Databricks HTTP path (for M partition expressions)

## Import from file

Use `ImportToTabularFromFile` to load and import in one operation:

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
    sb.AppendLine("Import successful!");
    sb.AppendLine($"Diagnostics: {diagnostics.Count}");
}
else
{
    sb.AppendLine("Import failed.");
    sb.AppendLine($"Errors: {diagnostics.Count}");
}

Output(sb.ToString());
```

## Import a loaded Metric View

If you've already loaded a Metric View (for inspection or modification), use `ImportToTabular`:

```csharp
// Load the Metric View first
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");

// Optionally inspect or modify it
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Importing Metric View with {view.Dimensions.Count} dimensions and {view.Measures.Count} measures");

// Import to Tabular
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

if (success)
{
    sb.AppendLine("Import successful!");
}
else
{
    sb.AppendLine("Import failed.");
}

Output(sb.ToString());
```

## Using placeholder connection values

If you're testing the translation without a real Databricks connection, you can use placeholder values:

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "C:/MetricViews/sales-metrics.yaml",
    Model,
    "placeholder-host",
    "placeholder-path",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine("Import complete (with placeholder connection values)");
sb.AppendLine("Note: Update the M partition expressions before refreshing data.");
Output(sb.ToString());
```

## View diagnostics after import

You can access diagnostics from the last import at any time using `ImportDiagnostics`.
This example assumes that you have previously run an import, either via GUI or C# script.

```csharp
var diagnostics = SemanticBridge.MetricView.ImportDiagnostics;

var sb = new System.Text.StringBuilder();
sb.AppendLine("LAST IMPORT DIAGNOSTICS");
sb.AppendLine("-----------------------");
sb.AppendLine("");
sb.AppendLine($"Total issues: {diagnostics.Count}");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

## Output diagnostics directly

For quick inspection, you can output the diagnostics collection directly:

```csharp
// Output all diagnostics from the last import
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

## Complete workflow example

Load, validate, and import with full diagnostic reporting:

```csharp
var sb = new System.Text.StringBuilder();

// Load the Metric View
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("METRIC VIEW SUMMARY");
sb.AppendLine("-------------------");
sb.AppendLine($"Source: {view.Source}");
sb.AppendLine($"Joins: {view.Joins?.Count ?? 0}");
sb.AppendLine($"Dimensions: {view.Dimensions.Count}");
sb.AppendLine($"Measures: {view.Measures.Count}");
sb.AppendLine("");

// Validate first
var validationDiags = SemanticBridge.MetricView.Validate().ToList();
sb.AppendLine("VALIDATION");
sb.AppendLine("----------");
sb.AppendLine($"Issues: {validationDiags.Count}");
sb.AppendLine("");

// Import
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var importDiags
);

sb.AppendLine("IMPORT RESULT");
sb.AppendLine("-------------");
sb.AppendLine($"Success: {success}");
sb.AppendLine($"Diagnostics: {importDiags.Count}");
sb.AppendLine("");

if (importDiags.Count > 0)
{
    sb.AppendLine("Import issues:");
    foreach (var diag in importDiags)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Message}");
    }
}

Output(sb.ToString());
```

## See also

- [Semantic Bridge Overview](xref:semantic-bridge)
- [Validate a Metric View](xref:semantic-bridge-validate-default)
- [Load and Inspect a Metric View](xref:semantic-bridge-load-inspect)
