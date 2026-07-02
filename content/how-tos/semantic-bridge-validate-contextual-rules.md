---
uid: semantic-bridge-validate-contextual-rules
title: Create Contextual Validation Rules
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
# Create Contextual Validation Rules

This how-to demonstrates how to create validation rules that check conditions across multiple objects using the validation context.
These rules are for illustrative purposes only and do not necessarily reflect hard technical requirements of either Metric Views or the Semantic Bridge.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## When to use contextual rules

Use contextual rules when you need to:

- Check that a name is not reused across different object types
- Access information about previously validated objects

> [!NOTE]
> The validation process validates each Metric View object in order (joins, then fields, then measures), so the context consists only of those items already visited in the validation.

## The MakeValidationRule method

The generic `MakeValidationRule<T>` method provides access to the validation context:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(  // or Field, Join, View
    "rule_name",
    "category",

    // return an IEnumerable<DiagnosticMessage>;
    // an empty collection means the object passed
    (obj, context) => []
);
```

The `context` parameter provides:

- `context.FieldNames` - names of fields already validated
- `context.MeasureNames` - names of measures already validated
- `context.JoinNames` - names of joins already validated
- `context.MakeError(code, message, object)` - create an error diagnostic for the given object
- `context.MakeWarning(code, message, object)` - create a warning diagnostic for the given object

Because you create the diagnostic message in the body of the validation function, you can put details about the current object being validated into the message.

## Using directive for Metric View types

Add this using directive to reference Metric View types:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Rule: a Metric View Measure name must not duplicate a Metric View Field name

Fields are validated before measures, so when a measure is checked, `context.FieldNames` already holds every field name.

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNameRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_field_name",
    "naming",
    (measure, context) =>
        context.FieldNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_field_name_collision",
                $"Measure '{measure.Name}' has the same name as a field",
                measure)]
            : []
);
```

## Rule: a Metric View Measure name must not duplicate a Metric View Join name

Joins are validated first, so `context.JoinNames` holds every join name by the time measures are checked.

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotJoinRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_join_name",
    "naming",
    (measure, context) =>
        context.JoinNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_join_name_collision",
                $"Measure '{measure.Name}' has the same name as a join",
                measure)]
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

// Create a Metric View with names reused across object types
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    joins:
      - name: customer
        source: sales.dim.customer
        on: source.customer_id = customer.customer_id
        cardinality: many_to_one
    fields:
      # 'revenue' is also used as a measure name below
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
    measures:
      # measureNameRule violation - same name as the 'revenue' field
      - name: revenue
        expr: SUM(source.revenue)
      # measureNotJoinRule violation - same name as the 'customer' join
      - name: customer
        expr: COUNT(DISTINCT source.customer_id)
      # this measure is fine
      - name: order_count
        expr: COUNT(source.order_id)
    """);

var measureNameRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_field_name",
    "naming",
    (measure, context) =>
        context.FieldNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_field_name_collision",
                $"Measure '{measure.Name}' has the same name as a field",
                measure)]
            : []
);

var measureNotJoinRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_join_name",
    "naming",
    (measure, context) =>
        context.JoinNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_join_name_collision",
                $"Measure '{measure.Name}' has the same name as a join",
                measure)]
            : []
);

// Run validation with both rules
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNameRule,
    measureNotJoinRule
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

[Error] Measure 'revenue' has the same name as a field
[Error] Measure 'customer' has the same name as a join
```

## Combining with default rules

You can run contextual rules alongside the default validation rules by calling `Validate` twice:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var customRules = new[] {
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_field_name",
        "naming",
        (measure, context) =>
            context.FieldNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_field_name_collision",
                    $"Measure '{measure.Name}' has the same name as a field",
                    measure)]
                : []),
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_join_name",
        "naming",
        (measure, context) =>
            context.JoinNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_join_name_collision",
                    $"Measure '{measure.Name}' has the same name as a join",
                    measure)]
                : [])
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

**Output**

```
<!--TODO-->
```

## See also

- [Semantic Bridge Validation](xref:semantic-bridge-metric-view-validation)
- [Create Simple Validation Rules](xref:semantic-bridge-validate-simple-rules)
- [Validate with Default Rules](xref:semantic-bridge-validate-default)
