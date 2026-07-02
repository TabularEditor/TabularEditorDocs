---
uid: semantic-bridge-validate-simple-rules
title: Create Simple Validation Rules
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
# Create Simple Validation Rules

This how-to demonstrates how to create simple predicate-based validation rules to enforce naming conventions and structural requirements.
These rules are for illustrative purposes only and do not necessarily reflect hard technical requirements of either Metric Views or the Semantic Bridge.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## The four rule helpers

There is a helper method for each type of Metric View object:

- `MakeValidationRuleForView` - rules for the root View object
- `MakeValidationRuleForJoin` - rules for Join objects
- `MakeValidationRuleForField` - rules for Field objects
- `MakeValidationRuleForMeasure` - rules for Measure objects

Each helper takes four parameters:

1. **name**: unique identifier for the rule
2. **category**: grouping for related rules
3. **message**: error message when the rule is violated
4. **isInvalid**: a function returning `true` if the object is invalid

## Rule for View

Check that the Metric View version is the expected value:

```csharp
var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View version must be 0.1 or 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);
```

## Rule for Metric View Join

Check that Metric View join sources use fully qualified table names (contain a dot):

```csharp
var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "Join source must be a fully qualified table name (e.g., `catalog.schema.table`)",
    (join) => !join.Source.Contains('.')
);
```

## Rule for Metric View Field

Check that Metric View field names do not contain underscores:

```csharp
var fieldNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Field names should use spaces, not underscores",
    (field) => field.Name.Contains('_')
);
```

## Rule for Metric View Measure

Check that Metric View measure expressions do not contain SELECT (to avoid accidental subqueries):

```csharp
var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "Measure expressions should not contain SELECT subqueries",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);
```

## Rules for specific Metric View versions

Each helper has an overload that takes a final `minVersion` argument, a string such as "0.1" or "1.1".
Rules defined with a `minVersion` only run against Metric Views at or above that version.
This is useful for a rule that checks a property introduced in a later version,
such as `display_name` (added in v1.1):

```csharp
var displayNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "field_display_name_required",
    "naming",
    "Fields should have a display name set",
    (field) => string.IsNullOrEmpty(field.DisplayName),
    "1.1"
);
```

## Complete example

This Metric View has violations for each of the rules defined above:

```csharp
// Create a Metric View with violations for each rule
SemanticBridge.MetricView.Deserialize("""
    version: 0.2
    source: sales.fact.orders
    joins:
      # joinSourceRule violation - not fully qualified
      - name: customer
        source: customer_table
        on: source.customer_id = customer.customer_id
    fields:
      # fieldNameRule violations - contains underscores
      - name: product_name
        expr: source.product_name
      - name: order_date
        expr: source.order_date
      # This one is fine
      - name: Category
        expr: source.category
    measures:
      # measureExprRule violation - contains SELECT subquery
      - name: complex_calc
        expr: (SELECT MAX(price) FROM products)
      # This one is fine
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "Metric View version must be 0.1 or 1.1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);

var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "Join source must be a fully qualified table name (e.g., `catalog.schema.table`)",
    (join) => !join.Source.Contains('.')
);

var fieldNameRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Field names should use spaces, not underscores",
    (field) => field.Name.Contains('_')
);

var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "Measure expressions should not contain SELECT subqueries",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);

// Run validation with custom rules
var diagnostics = SemanticBridge.MetricView.Validate([
    versionRule,
    joinSourceRule,
    fieldNameRule,
    measureExprRule
]).ToList();

// Output results
var sb = new System.Text.StringBuilder();
sb.AppendLine("CUSTOM VALIDATION RESULTS");
sb.AppendLine("-------------------------");
sb.AppendLine("");
sb.AppendLine($"Found {diagnostics.Count} issue(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Path}: {diag.Message}");
}

Output(sb.ToString());
```

**Output:**

```
CUSTOM VALIDATION RESULTS
-------------------------

Found 5 issue(s):

[Error] Model: Metric View version must be 0.1 or 1.1
[Error] Model.Joins["customer"]: Join source must be a fully qualified table name (e.g., `catalog.schema.table`)
[Error] Model.Fields["product_name"]: Field names should use spaces, not underscores
[Error] Model.Fields["order_date"]: Field names should use spaces, not underscores
[Error] Model.Measures["complex_calc"]: Measure expressions should not contain SELECT subqueries
```

## Next steps

- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules)

## See also

- [Semantic Bridge Validation](xref:semantic-bridge-metric-view-validation)
