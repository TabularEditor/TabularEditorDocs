---
uid: semantic-bridge-metric-view-validation
title: Semantic Bridge Metric View Validation
author: Greg Baldini
updated: 2026-09-14
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
This diagnostic reporting is shared at every stage of the translation pipeline,
from first deserializing the Metric View, through to errors in translation to DAX and Tabular.

> [!NOTE]
> The Semantic Bridge is currently in public preview, so interfaces may change as the feature matures.
> For now, the only interface to validation is through C# scripts.

## Validation process

There are several phases of validation

1. upon deserializing some YAML, to check that it represents a valid Metric View
2. acting on the loaded Metric View
3. upon translating the Metric View to Tabular

The first and third are automatic and internal to the Semantic Bridge,
but the second is where users can provide their own validation rules.

Validation is a process of evaluating each of a set of validation rules against all objects in the Metric View.
A validation rule is defined to apply to exactly one type of Metric View object, e.g. a `Join` or `Measure`.
After a validation is complete, all diagnostics from rule violations are returned to the user for further action.

## Built-in diagnostic codes

The first and third phases raise their own diagnostics, with codes the Semantic Bridge defines. They reach you the same way your own rules' diagnostics do: each carries a `Severity`, a `Code`, a `Path`, a `Context` and a `Message`.

Severity is one of `Error`, `Warning` or `Information`. An `Error` stops the operation. A `Warning` means the Bridge carried on having made a decision for you, and is telling you what it decided.

### Reading the YAML

| Code | Severity | Raised when |
|---|---|---|
| `METRIC_VIEW_FIELDS_AND_DIMENSIONS_BOTH_PRESENT` | Error | The view declares both `fields:` and `dimensions:` at the top level. They are aliases for one another; use one |
| `METRIC_VIEW_DUPLICATE_NAME` | Error | Two objects in the same collection claim the same name. Matching is case-insensitive |
| `METRIC_VIEW_DEPRECATED_DIMENSIONS_KEYWORD` | Warning | A view at YAML spec 1.1 or later uses `dimensions:`. `fields:` is the canonical form; both keep working. Raised once per file |
| `METRIC_VIEW_FIELDS_KEYWORD_PRE_V11` | Warning | A view below spec 1.1 uses `fields:`. `dimensions:` is canonical at that version; both are accepted |
| `MISSING_VERSION` | Warning | The YAML has no `version` property. A default is assumed |
| `UNKNOWN_JOIN_CARDINALITY` | Warning | A join declares a cardinality other than `many_to_one` or `one_to_many`. `many_to_one` is assumed |
| `MISSING_FORMAT_TYPE`, `UNKNOWN_FORMAT_TYPE` | Warning | A format has no type, or one the Bridge does not recognize. The format is ignored |
| `MISSING_DATE_FORMAT`, `UNKNOWN_DATE_FORMAT` | Warning | Defaults to `year_month_day` |
| `MISSING_TIME_FORMAT`, `UNKNOWN_TIME_FORMAT` | Warning | Defaults to `locale_hour_minute_second` |
| `MISSING_DECIMAL_TYPE`, `UNKNOWN_DECIMAL_TYPE` | Warning | Defaults to `all` |
| `MISSING_SEMIADDITIVE`, `UNKNOWN_SEMIADDITIVE` | Warning | Defaults to `Last` |
| `MISSING_MATERIALIZATION_MODE`, `UNKNOWN_MATERIALIZATION_MODE` | Warning | Defaults to `relaxed` |
| `MISSING_MATERIALIZED_VIEW_TYPE`, `UNKNOWN_MATERIALIZED_VIEW_TYPE` | Warning | Defaults to `unaggregated` |
| `VERSION_MISMATCH` | Warning | The declared version does not match what was found |

### Mapping the Metric View

Every code in this group is a `Warning` except where noted. The object is still created, but something about it did not survive intact.

| Code | Raised when |
|---|---|
| `JOIN_ON_EMPTY` | A join has no `on` clause. The dimension and its source are created, but no foreign-key / primary-key pair is wired |
| `JOIN_ON_UNRECOGNIZED` | A join's `on` clause is not a recognized equality between an upstream column and a dimension column. Again, no key pair |
| `JOIN_ON_NO_SOURCE_SIDE` | A join's `on` clause pairs no upstream column. Again, no key pair |
| `ONE_TO_MANY_JOIN_UNTRANSLATED` | A join declares `cardinality: one_to_many`, which the translator does not model. *The relationship is skipped*, so measures referencing its columns may be wrong or empty; review these by hand |
| `DUPLICATE_JOIN_DIMENSION` | A join would create a dimension whose name collides with an existing one. The duplicate is skipped. Join names must be unique across the view |
| `UNRESOLVED_DIMENSION_REFERENCE` | A reference targets a dimension that is not declared as a join. A placeholder derived field is emitted, preserving the original reference |
| `STRUCT_REFERENCE_UNSUPPORTED` | A dimension references a whole-row or nested struct value, which has no Tabular column equivalent. The column is emitted but will not resolve at refresh |
| `FORMAT_TRANSLATION_LOSSY` | A Databricks format spec cannot be expressed exactly as a Tabular format string |
| `FIELD_COLLISION_RENAME` | *Information.* A generated field name collided with a user-declared dimension, so the field was renamed. It stays in the model and still backs any relationship that referenced it |
| `MEASURE_REF_OUT_OF_CONTEXT` | A `MEASURE(...)` reference appears in an expression that is not a measure |
| `UNRESOLVED_MEASURE_REFERENCE` | A `MEASURE(...)` reference names no declared measure. Falls back to the verbatim source |
| `FIELD_CONFIGURATION_UNEXPECTED` | A field had a configuration the analyzer could not classify, and was imported as a derived fact field for safety. Verify the result |

### Expression diagnostics, by object kind

Expression problems report under their own code per object kind, so you can tell at a glance which kind of object failed:

| Kind | Could not be translated | Could not be parsed |
|---|---|---|
| Field | `FIELD_EXPRESSION_UNTRANSLATED` | `FIELD_EXPRESSION_PARSE_ERROR` |
| Measure | `MEASURE_EXPRESSION_UNTRANSLATED` | `MEASURE_EXPRESSION_PARSE_ERROR` |
| Join | `JOIN_EXPRESSION_UNTRANSLATED` | `JOIN_EXPRESSION_PARSE_ERROR` |

An *untranslated* expression was understood but uses a construct with no DAX equivalent; the original is preserved as a comment. A *parse error* means the expression could not be read at all, and the diagnostic's `Context` carries the parser's own message.

### Emitting to Tabular

| Code | Raised when |
|---|---|
| `REFERENCE_FIELD_INVALID_SOURCE` | A reference field points at a field id that is missing or is not a source field. A placeholder column is emitted |
| `DERIVED_FIELD_UNTRANSLATED` | A derived field's expression could not be translated to DAX. The original is preserved as a comment |
| `DERIVED_FIELD_NO_EXPRESSION` | A derived field has no expression |
| `MEASURE_UNTRANSLATED` | A measure's expression could not be translated. The original is preserved as a comment |
| `CALCULATED_MEASURE_NO_EXPRESSION` | A calculated measure has no source expression. A placeholder body is emitted |
| `MEASURE_UNRESOLVED_AT_EMIT` | A measure references a measure that has not been emitted. Falls back to the verbatim source |
| `TABLE_UNRESOLVED_AT_EMIT` | A measure references a table that has not been emitted. Falls back to the verbatim source |
| `COLUMN_UNRESOLVED_AT_EMIT` | A measure references a field that has not been emitted as a column. Falls back to the verbatim source |
| `MEASURE_WINDOW_UNSUPPORTED` | A measure uses an unsupported window specification. It is left inert, with the original definition preserved as a comment |

## Anatomy of a validation rule

Validation rules are all instances of [`IMetricViewValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule).
Rather than dig into that interface, it is easier to understand and work with validation rules with the helper methods:

- [`MakeValidationRuleForField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForField%2A)
- [`MakeValidationRuleForJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForJoin%2A)
- [`MakeValidationRuleForMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForMeasure%2A)
- [`MakeValidationRuleForView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForView%2A)
- [`MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A)

The first four are all special purpose to make a rule for the object type in their name.
They offer a simplified interface where you provide:

- `name`: a short, unique name to identify the rule
- `category`: useful for grouping similar rules together, but ultimately completely optional
- `message`: the message that will be shown in the diagnostic message when this rule is violated
- `isInvalid`: a function that will take the Metric View object as an argument, and will return `true` if that object is invalid

The name and category are intended to make it easier to deal with collections of rules, as you will do in C# scripts that utilize custom rules.

Each of these helpers also has an overload with a final `minVersion` argument.
This argument would take a version string, such as "0.1" or "1.1".
Rules with `minVersion` set are only evaluated for Metric Views at or above that version.

This is easier to understand with an example:

```csharp {compile}
// create a rule to check for underscores in field names
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
	"no_underscores",
	"naming",
	"Do not include underscores in field names. Use user-friendly names with spaces.",
	(field) => field.Name.Contains('_')
	);
```

This makes a rule that will apply to all [Metric View `Field`s](xref:TabularEditor.SemanticBridge.Platforms.Databricks.MetricView.Field).
The rule is named (ironically) "no_underscores".
It has a category of "naming", to indicate that it has to do with how we name things.
The message you will see when the rule is violated is, "Do not include underscores in field names. Use user-friendly names with spaces."
The last argument defines a function that will be called for each Metric View field in the model; its body is a boolean expression that returns `true` for a Metric View field with an underscore in its `Name` property.

Here's a full script that defines a Metric View inline, and then deserializes and validates it, showing how this rule is used.

```csharp {run id=simple setup=none after=none output=true}
// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: first_field
        expr: source.first_field
      - name: another field with no underscores
        expr: source.another_field_with_no_underscores
    """);

// create a new validation rule
var myRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// run validation with the rule defined above and output the diagnostic messages
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Output**

```
[Error] no_underscores Model.Fields["first_field"]
     Do not include underscores in field names. Use user-friendly names with spaces.
```

You can see that one of the Metric View fields has an underscore in its name.
When you run the script, you can see one diagnostic message after validating with the rule we defined.
You can see the details that are provided in the diagnostic message:

- Code: the name you assign to your rule
- Context: not set by these helpers
- Message: the message you defined in the rule
- Path: a representation of where you find that object in the Metric View
- Severity: set to Error by default with these helpers

![output from one field violating the validation rule](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

If you want more control over the diagnostic message and more flexibility in the function for your validation, you can use `MakeValidationRule` mentioned above to make a contextual validation rule.

```csharp {run id=contextual setup=none after=none output=true}
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);

// create a new validation rule
var myRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// run validation with the rule defined above and output the diagnostic messages
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([myRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Output**

```
[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

This helper method requires you to pass the object type as a type parameter, and the validation function now is a two-parameter function, defined with the signature `(metricViewObject, context)`.
The first parameter is the Metric View object that the rule is evaluated for.
The second parameter is an [`IReadOnlyValidationContext`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext).
This context object holds collections with the names of already-checked objects;
this means we can use it to inspect only objects already validated.
The context object also has helper methods to make a new diagnostic message;
the benefit here is that your message doesn't have to be a hard-coded string,
but can include properties of the object you are checking.
We use `MakeError`, and the context object also includes a `MakeWarning`.
You can see in this example that we include in the message both the offending field and the field it aliases.

![output from one field violating the more complex validation rule](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Validation rule best practices

It is a good idea to make many simple rules, rather than fewer, more complex rules.
The validation process is very light-weight, so there are not performance concerns from a proliferation of rules.
For example, if you want to make sure that Metric View field names are not `camelCased`, not `kebab-cased` and not `snake_cased`, it is better to make three separate rules, rather than trying to check for each of those conditions in a single rule.
This allows each rule to be simple, and for the messages to be very specific, and therefore more easily actionable.

In general, once you have a rule that catches a specific issue, it is better to leave that alone, rather than editing it.
If you find that the rule is missing some condition you'd like to catch, just add a new, small, simple rule to catch that new condition.

You can save many different rules in a C# script for re-use with different Metric Views.
Because [a loaded Metric View is accessible in multiple scripts](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view) you can save C# scripts that only define rules and then call `SemanticBridge.MetricView.Validate`, and re-use those validation scripts easily.
See the image below, where the script on the left, "deserialize-mv.csx" has already been run, to load a Metric View to Tabular Editor.
Then, the second script, on the right, "run-rules.csx", is run second to validate.
This second script could be one that you keep around for all of your Metric Views.


![output from one field violating the more complex validation rule](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

The scripts are copied below for convenience, but are just rearrangements of scripts we saw above.

**"deserialize-mv.csx"**

```csharp {run id=deserialize setup=none after=none output=false}
// create a new simple Metric View
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: database.schema.table
    fields:
      - name: customer
        expr: source.customer_id
      - name: repeat_customer
        expr: source.customer_id
    """);
```

**"run-rules.csx"**

```csharp {run id=run-rules setup=none after=deserialize output=true}
// necessary to use the Metric View object model
// aliasing to avoid conflicts with same-named TOM objects
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

//create a simple validation rule
var simpleRule = SemanticBridge.MetricView.MakeValidationRuleForField(
    "no_underscores",
    "naming",
    "Do not include underscores in field names. Use user-friendly names with spaces.",
    (field) => field.Name.Contains('_')
    );

// create a contextual validation rule
var contextualRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Field>(
    "no_aliased_fields",
    "modeling",
    (field, context) =>
    {
        var original = context.FieldNames.FirstOrDefault(seen => field.View.Fields[seen].Expr == field.Expr);
        return original == null
            ? []
            : [context.MakeError(
                "field_alias",
                $"Field '{field.Name}' reuses source expression '{field.Expr}', already used by field '{original}'.",
                field)];
    });

// run validation with the rules defined above and output the diagnostic messages
var sb = new System.Text.StringBuilder();
foreach (var d in SemanticBridge.MetricView.Validate([simpleRule, contextualRule]))
{
    sb.AppendLine($"[{d.Severity}] {d.Code} {d.Path}");
    sb.AppendLine($"    {d.Context} {d.Message}");
    sb.AppendLine();
}
Output(sb.ToString());
```

**Output**

```
[Error] no_underscores Model.Fields["repeat_customer"]
     Do not include underscores in field names. Use user-friendly names with spaces.

[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

## References

- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
