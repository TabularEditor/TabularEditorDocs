---
uid: semantic-bridge-validate-contextual-rules
title: Create Contextual Validation Rules
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
# Create Contextual Validation Rules

This how-to demonstrates how to create validation rules that check conditions across multiple objects using the validation context.
These rules are for illustrative purposes only and do not necessarily reflect hard technical requirements of either Metric Views or the Semantic Bridge.

## When to use contextual rules

Use contextual rules when you need to:

- Detect duplicate names across objects
- Check that names don't conflict between different object types
- Access information about previously validated objects

> [!NOTE]
> The validation process validates each Metric View object in order, so the context consists only of those items already visited in the validation.

## The MakeValidationRule method

The generic `MakeValidationRule<T>` method provides access to the validation context:

```csharp
SemanticBridge.MetricView.MakeValidationRule<IMetricViewObjectType>(
    "rule_name",
    "category",
    (obj, context) => {
        // Return IEnumerable<DiagnosticMessage>
        // Empty collection means validation passed
    }
);
```

The `context` parameter provides:

- `context.DimensionNames` - names of dimensions already validated
- `context.MeasureNames` - names of measures already validated
- `context.JoinNames` - names of joins already validated
- `context.MakeError(message)` - create an error diagnostic
- `context.MakeError(message, property)` - create an error diagnostic, calling out the specific property with an error

Because you create the diagnostic message in the body of the validation function, you can put details about the current object being validated into the message.

## Using directive for Metric View types

Add this using directive to reference Metric View types:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Rule: Metric View Measure name must not duplicate a Metric View dimension name

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"Measure '{measure.Name}' has the same name as a dimension")]
            : []
);
```

## Rule: Metric View Measure name must not duplicate another Metric View measure

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"Measure '{measure.Name}' is defined more than once")]
            : []
);
```

## Why separate rules are better

Notice that we created two separate rules instead of one combined rule. This is the recommended approach because:

1. **Clearer error messages**: Each rule produces a specific, actionable message
2. **Easier maintenance**: Rules can be added, removed, or modified independently
3. **Simpler logic**: Each rule checks exactly one condition
4. **Better categorization**: Rules can be grouped and filtered by purpose

## Complete example

This Metric View has naming conflicts that will trigger both contextual rules:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// Create a Metric View with naming conflicts
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    dimensions:
      # 'revenue' is used as both a dimension and measure name
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
      - name: order_date
        expr: source.order_date
    measures:
      # measureNotDimensionRule violation - same name as dimension
      - name: revenue
        expr: SUM(source.revenue)
      # noDuplicateMeasureRule violation - 'total_quantity' appears twice
      - name: total_quantity
        expr: SUM(source.quantity)
      - name: total_quantity
        expr: COUNT(source.order_id)
      # This one is fine
      - name: order_count
        expr: COUNT(source.order_id)
    """);

// Define contextual rules
var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"Measure '{measure.Name}' has the same name as a dimension")]
            : []
);

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"Measure '{measure.Name}' is defined more than once")]
            : []
);

// Run validation
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNotDimensionRule,
    noDuplicateMeasureRule
]).ToList();

// Output results
var sb = new System.Text.StringBuilder();
sb.AppendLine("CONTEXTUAL VALIDATION RESULTS");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
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
CONTEXTUAL VALIDATION RESULTS
-----------------------------

Found 2 issue(s):

[Error] Measure 'revenue' has the same name as a dimension
[Error] Measure 'total_quantity' is defined more than once
```

## Combining with default rules

You can run contextual rules alongside the default validation rules:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var customRules = new[] {
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_dimension_name",
        "naming",
        (measure, context) =>
            context.DimensionNames.Contains(measure.Name)
                ? [context.MakeError($"Measure '{measure.Name}' has the same name as a dimension")]
                : []
    )
};

// Run default rules first
var defaultDiagnostics = SemanticBridge.MetricView.Validate().ToList();

// Then run custom rules
var customDiagnostics = SemanticBridge.MetricView.Validate(customRules).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Default rule issues: {defaultDiagnostics.Count}");
sb.AppendLine($"Custom rule issues: {customDiagnostics.Count}");
Output(sb.ToString());
```

## See also

- [Semantic Bridge Validation](xref:semantic-bridge-metric-view-validation)
- [Create Simple Validation Rules](xref:semantic-bridge-validate-simple-rules)
- [Validate with Default Rules](xref:semantic-bridge-validate-default)
