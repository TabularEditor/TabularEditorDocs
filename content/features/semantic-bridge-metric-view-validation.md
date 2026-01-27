---
uid: semantic-bridge-metric-view-validation
title: Semantic Bridge Metric View Validation
author: Greg Baldini
updated: 2025-01-23
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
# Semantic Bridge Validation

<!--
SUMMARY: Describes the validation framework for Metric Views in the Semantic Bridge, including built-in validation rules, diagnostic messages (errors/warnings/info), and how validation integrates with the import workflow.
-->

There is a validation framework built into the Semantic Bridge to allow users to validate and define rules to check a Metric View before importing it to Tabular.
This validation is shared at every stage of the translation pipeline, from first deserializing the Metric View, through to errors in translation to DAX and Tabular.

> [!NOTE]
> The Semantic Bridge is currently in its MVP phase, so interfaces may change as the feature matures.
> For now, the only interface to validation is through C# scripts.

## Validation process

There are several phases of validation

1. upon deserializing some YAML, to check that it represents a valid Metric View
2. acting on the loaded Metric View
3. upon translating the Metric View to Tabular

The first and third are automatic and internal to the Semantic Bridge, but the second is where users can provide their own validation rules.

Validation is a process of evaluating each of a set of validation rules against all objects in the Metric View.
A validation rule is defined to apply to exactly one type of Metric View object, e.g. a `Join` or `Measure`.
After a validation is complete, all diagnostics from rule violations are returned to the user for further action.

## Anatomy of a validation rule

Validation rules are all instances of [`IMetricViewValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule.html).
Rather than dig into that interface, it is easier to understand and work with validation rules with the helper methods:

- [`MakeValidationRuleForDimension`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForDimension_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Dimension_System_Boolean__)
- [`MakeValidationRuleForJoin`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForJoin_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Join_System_Boolean__)
- [`MakeValidationRuleForMeasure`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForMeasure_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Measure_System_Boolean__)
- [`MakeValidationRuleForView`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRuleForMeasure_System_String_System_String_System_String_System_Func_TabularEditor_SemanticBridge_Platforms_Databricks_MetricView_Measure_System_Boolean__)
- [`MakeValidationRule`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.html#TabularEditor_SemanticBridge_Platforms_Databricks_DatabricksMetricViewService_MakeValidationRule__1_System_String_System_String_System_Func___0_TabularEditor_SemanticBridge_Platforms_Databricks_Validation_IReadOnlyValidationContext_System_Collections_Generic_IEnumerable_TabularEditor_SemanticBridge_Orchestration_DiagnosticMessage___)

The first are all special purpose to make a rule for the object type in their name.
They offer a simplified interface where you provide:

- `name`: a short, unique name to identify the rule
- `category`: useful for grouping similar rules together, but ultimately completely optional
- `message`: the message that will be shown in the diagnostic message when this rule is violated
- `isInvalid`: a function that will take the Metric View object as an argument, and will return `true` if that object is invalid

This is easier to understand with an example:

```csharp
// create a rule to check for underscores in dimension names
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
	"no_underscores",
	"naming",
	"Do not include undercores in dimension names. Use user-friendly names with spaces.",
	(dimension) => dimension.Name.Contains('_')
	);
```

This makes a rule that will apply to all [Metric View `Dimension`s](/api/TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Dimension.html).
The rule is named (ironically) "no_underscores".
It has a category of "naming", to indicate that it has to do with how we name things.
The message you will see when the rule is violated is, "Do not include underscores in dimension names. Use user-friendly names with spaces."
The last argument defines a function that will be called for each dimension in the model; its body is a boolean expression that returns `true` for a dimension with an underscore in its `Name` property.

Here's a full script that defines a Metric View inline, and then deserializes and validates it, showing how this rule is used.

```csharp
// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// create a new validation rule
var myRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Do not include undercores in dimension names. Use user-friendly names with spaces.",
    (dimension) => dimension.Name.Contains('_')
    );

// run validation with the rule defined above and output the diagnostic messages
Output(SemanticBridge.MetricView.Validate([myRule]));
```

You can see that one of the fields defined as a Metric View dimension has an underscore in its name.
When you run the script, you can see one diagnostic message after validating with the rule we defined.
You can see the details that are provided in the diagnostic message:

- Code, Context: not used when you use one of these helper methods to make your rule
- Message: the message you defined in the rule
- Path: a representation of where you find that object in the Metric View
- Severity: set to Error by default with these simplified helpers

![output from one field violating the validation rule](/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

If you want more control over the diagnostic message and more flexibility in the function for your validation, you can use `MakeValidationRule` mentioned above to make a contextual validation rule.

```csharp
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);

// create a new validation rule
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} appears more than once as a dimension")]
            : []
    );

// run validation with the rule defined above and output the diagnostic messages
Output(SemanticBridge.MetricView.Validate([myRule]));
```

This helper method requires you to pass the object type as a type parameter, and the validation function now is a two-parameter function, defined with the signature `(objectType, context)`.
The first parameter is the Metric View object that the rule is evaluated for.
The second parameter is an [`IReadOnlyValidationContext`](/api/TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext.html).
This context object holds collections with the names of already-checked objects; this makes it useful to check for duplicate names.
The context object also has a helper method to make a new diagnostic message; the benefit here is that your message doesn't have to be a hard-coded string, but can include properties of the object you are checking.
You can see in this example that we include the duplicated Metric View dimension name in the message.

![output from one field violating the more complex validation rule](/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Validation rule best practices

It is a good idea to make many simple rules, rather than fewer, more complex rules.
The validation process is very light-weight, so there are not performance concerns from a proliferation of rules.
For example, if you want to make sure that dimension names are not `camelCased`, not `kebab-cased` and not `snake_cased`, it is better to make three separate rules, rather than trying to check for each of those conditions in a single rule.
This allows each rule to be simple, and for the messages to be very specific, and therefore more easily actionable.

In general, once you have a rule that catches a specific issue, it is better to leave that alone, rather than editing it.
If you find that the rule is missing some condition you'd like to catch, just add a new small, simple rule to catch that new condition.

You can save many different rules in a C# script for re-use with different Metric Views.
Because [a loaded Metric View is accessible in multiple scripts](xref:semantic-bridge-metric-view-object-model) you can save C# scripts that only define rules and then call `SemanticBridge.MetricView.Validate`, and re-use those validation scripts easily.
See the image below, where the script on the left, "load-mv.csx" has already been run, to load a Metric View to Tabular Editor.
Then, the second script, on the right, "run-rules.csx", is run second to validate.
This second script could be one that you keep around for all of your Metric Views.


![output from one field violating the more complex validation rule](/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

The scripts are copied below for convenience, but are just rearrangements of scripts we saw above.

**"load-mv.csx"**

```csharp
// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: database.schema.table
    dimensions:
      - name: same_field
        expr: source.same_field
      - name: same_field
        expr: source.same_field
    """);
```

**"run-rules.csx"**

```csharp
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

//create a simple validation rule
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Do not include undercores in dimension names. Use user-friendly names with spaces.",
    (dimension) => dimension.Name.Contains('_')
    );

// create a contextual validation rule
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Dimension>(
    "no_duplicate_dimensions",
    "naming",
    (dimension, context) =>
        context.DimensionNames.Contains(dimension.Name)
            ? [context.MakeError($"{dimension.Name} appears more than once as a dimension")]
            : []
    );

// run validation with the rules defined above and output the diagnostic messages
Output(SemanticBridge.MetricView.Validate([simpleRule, contextualRule]));
```
