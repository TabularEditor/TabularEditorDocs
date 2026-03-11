---
uid: semantic-bridge-validate-default
title: Validate a Metric View with Default Rules
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
# Validate a Metric View with Default Rules

This how-to demonstrates how to validate a loaded Metric View using the built-in validation rules and interpret the diagnostic messages.

## Default validation rules

The Semantic Bridge includes these built-in validation rules:

| Rule                     | Description                                                                   |
|--------------------------|-------------------------------------------------------------------------------|
| JoinNameRequired         | Metric View Join must have a name                                             |
| UniqueJoinName           | Metric View Join names must be unique                                         |
| JoinSourceRequired       | Metric View Join must have a source                                           |
| JoinOnOrUsingRequired    | Metric View Join must specify either `on` or `using`                          |
| JoinOnOrUsingExclusivity | Metric View Join cannot specify both `on` and `using`                         |
| JoinOnFormat             | Metric View Join `on` clause must be a valid equijoin expression              |
| JoinUsingColumnCount     | Metric View Join `using` clause must have exactly one column (MVP limitation) |
| DimensionNameRequired    | Metric View Dimension must have a name                                        |
| UniqueDimensionName      | Metric View Dimension names must be unique                                    |
| DimensionExprRequired    | Metric View Dimension must have an expression                                 |
| MeasureNameRequired      | Metric View Measure must have a name                                          |
| UniqueMeasureName        | Metric View Measure names must be unique                                      |
| MeasureExprRequired      | Metric View Measure must have an expression                                   |

## Run validation with default rules

Call `Validate()` with no arguments to use the built-in validation rules.

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validation complete: {diagnostics.Count} issue(s) found");
```

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

## Example with validation errors

Some rules (required fields) are enforced during deserialization.
The remaining rules check for duplicates and structural issues after deserialization.

This Metric View demonstrates violations that are caught by `Validate()`:

```csharp
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    joins:
      # UniqueJoinName - duplicate name 'customer'
      - name: customer
        source: sales.dim.customer
        on: customer_id = customer.customer_id
      - name: customer
        source: sales.dim.customer_backup
        on: customer_id = customer_backup.customer_id
      # JoinOnOrUsingRequired - neither on nor using
      - name: date
        source: sales.dim.date
    dimensions:
      # UniqueDimensionName - duplicate name 'category'
      - name: category
        expr: product.category
      - name: category
        expr: product.subcategory
      - name: product_name
        expr: product.product_name
    measures:
      # UniqueMeasureName - duplicate name 'total'
      - name: total
        expr: SUM(revenue)
      - name: total
        expr: SUM(quantity)
      - name: order_count
        expr: COUNT(order_id)
    """);

var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Found {diagnostics.Count} issue(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

**Output:**

```
Found 6 issue(s):

[Error] Join 'customer' must use a simple equality condition with table prefixes (e.g. 'source.column = dimension.column')
[Error] Duplicate join name: 'customer'
[Error] Join 'customer' must use a simple equality condition with table prefixes (e.g. 'source.column = dimension.column')
[Error] Join 'date' must specify either 'on' or 'using' clause
[Error] Duplicate dimension name: 'category'
[Error] Duplicate measure name: 'total'
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

- [Create simple validation rules](xref:semantic-bridge-validate-simple-rules) to enforce your own conventions
- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules) for cross-object checks

## See also

- [Semantic Bridge Validation](xref:semantic-bridge-metric-view-validation)
- [Metric View Object Model](xref:semantic-bridge-metric-view-object-model)
