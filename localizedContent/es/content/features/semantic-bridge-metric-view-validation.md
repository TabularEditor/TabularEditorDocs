---
uid: semantic-bridge-metric-view-validation
title: Validación de Metric View en Semantic Bridge
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

# Validación de Semantic Bridge

<!--
SUMMARY: Describes the validation framework for Metric Views in the Semantic Bridge, including built-in validation rules, diagnostic messages (errors/warnings/info), and how validation integrates with the import workflow.
-->

Hay un marco de validación integrado en el Semantic Bridge que permite a los usuarios validar y definir reglas para comprobar una Metric View antes de importarla en Tabular.
This diagnostic reporting is shared at every stage of the translation pipeline,
from first deserializing the Metric View, through to errors in translation to DAX and Tabular.

> [!NOTE]
> El Semantic Bridge está actualmente en versión preliminar pública, por lo que las interfaces pueden cambiar a medida que la funcionalidad madura.
> Por ahora, la única interfaz para la validación es a través de scripts de C#.

## Proceso de validación

Hay varias fases de validación

1. al deserializar YAML para comprobar que representa un Metric View válido
2. al actuar sobre el Metric View cargado
3. al traducir el Metric View a Tabular

The first and third are automatic and internal to the Semantic Bridge,
but the second is where users can provide their own validation rules.

La validación es el proceso de evaluar cada regla de validación de un conjunto sobre todos los objetos del Metric View.
Una regla de validación se define para aplicarse a un único tipo de objeto de Metric View; por ejemplo, un `Join` o un `Measure`.
Una vez completada la validación, se devuelven al usuario todos los diagnósticos de los incumplimientos de reglas para que actúe en consecuencia.

## Built-in diagnostic codes

The first and third phases raise their own diagnostics, with codes the Semantic Bridge defines. They reach you the same way your own rules' diagnostics do: each carries a `Severity`, a `Code`, a `Path`, a `Context` and a `Message`.

Severity is one of `Error`, `Warning` or `Information`. An `Error` stops the operation. A `Warning` means the Bridge carried on having made a decision for you, and is telling you what it decided.

### Reading the YAML

| Code                                                               | Severity    | Raised when                                                                                                                                                                   |
| ------------------------------------------------------------------ | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `METRIC_VIEW_FIELDS_AND_DIMENSIONS_BOTH_PRESENT`                   | Error       | The view declares both `fields:` and `dimensions:` at the top level. They are aliases for one another; use one                                                |
| `METRIC_VIEW_DUPLICATE_NAME`                                       | Error       | Two objects in the same collection claim the same name. Matching is case-insensitive                                                                          |
| `METRIC_VIEW_DEPRECATED_DIMENSIONS_KEYWORD`                        | Advertencia | A view at YAML spec 1.1 or later uses `dimensions:`. `fields:` is the canonical form; both keep working. Raised once per file |
| `METRIC_VIEW_FIELDS_KEYWORD_PRE_V11`                               | Advertencia | A view below spec 1.1 uses `fields:`. `dimensions:` is canonical at that version; both are accepted                                           |
| `MISSING_VERSION`                                                  | Advertencia | The YAML has no `version` property. A default is assumed                                                                                                      |
| `UNKNOWN_JOIN_CARDINALITY`                                         | Advertencia | A join declares a cardinality other than `many_to_one` or `one_to_many`. `many_to_one` is assumed                                                             |
| `MISSING_FORMAT_TYPE`, `UNKNOWN_FORMAT_TYPE`                       | Advertencia | A format has no type, or one the Bridge does not recognize. The format is ignored                                                                             |
| `MISSING_DATE_FORMAT`, `UNKNOWN_DATE_FORMAT`                       | Advertencia | Defaults to `year_month_day`                                                                                                                                                  |
| `MISSING_TIME_FORMAT`, `UNKNOWN_TIME_FORMAT`                       | Advertencia | Defaults to `locale_hour_minute_second`                                                                                                                                       |
| `MISSING_DECIMAL_TYPE`, `UNKNOWN_DECIMAL_TYPE`                     | Advertencia | Defaults to `all`                                                                                                                                                             |
| `MISSING_SEMIADDITIVE`, `UNKNOWN_SEMIADDITIVE`                     | Advertencia | Defaults to `Last`                                                                                                                                                            |
| `MISSING_MATERIALIZATION_MODE`, `UNKNOWN_MATERIALIZATION_MODE`     | Advertencia | Defaults to `relaxed`                                                                                                                                                         |
| `MISSING_MATERIALIZED_VIEW_TYPE`, `UNKNOWN_MATERIALIZED_VIEW_TYPE` | Advertencia | Defaults to `unaggregated`                                                                                                                                                    |
| `VERSION_MISMATCH`                                                 | Advertencia | The declared version does not match what was found                                                                                                                            |

### Mapping the Metric View

Every code in this group is a `Warning` except where noted. The object is still created, but something about it did not survive intact.

| Code                             | Raised when                                                                                                                                                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `JOIN_ON_EMPTY`                  | A join has no `on` clause. The dimension and its source are created, but no foreign-key / primary-key pair is wired                                                                                |
| `JOIN_ON_UNRECOGNIZED`           | A join's `on` clause is not a recognized equality between an upstream column and a dimension column. Again, no key pair                                                                            |
| `JOIN_ON_NO_SOURCE_SIDE`         | A join's `on` clause pairs no upstream column. Again, no key pair                                                                                                                                  |
| `ONE_TO_MANY_JOIN_UNTRANSLATED`  | A join declares `cardinality: one_to_many`, which the translator does not model. _The relationship is skipped_, so measures referencing its columns may be wrong or empty; review these by hand    |
| `DUPLICATE_JOIN_DIMENSION`       | A join would create a dimension whose name collides with an existing one. The duplicate is skipped. Join names must be unique across the view                                      |
| `UNRESOLVED_DIMENSION_REFERENCE` | A reference targets a dimension that is not declared as a join. A placeholder derived field is emitted, preserving the original reference                                                          |
| `STRUCT_REFERENCE_UNSUPPORTED`   | A dimension references a whole-row or nested struct value, which has no Tabular column equivalent. The column is emitted but will not resolve at refresh                                           |
| `FORMAT_TRANSLATION_LOSSY`       | A Databricks format spec cannot be expressed exactly as a Tabular format string                                                                                                                                    |
| `FIELD_COLLISION_RENAME`         | _Information._ A generated field name collided with a user-declared dimension, so the field was renamed. It stays in the model and still backs any relationship that referenced it |
| `MEASURE_REF_OUT_OF_CONTEXT`     | A `MEASURE(...)` reference appears in an expression that is not a measure                                                                                                                                          |
| `UNRESOLVED_MEASURE_REFERENCE`   | A `MEASURE(...)` reference names no declared measure. Falls back to the verbatim source                                                                                                            |
| `FIELD_CONFIGURATION_UNEXPECTED` | A field had a configuration the analyzer could not classify, and was imported as a derived fact field for safety. Verify the result                                                                |

### Expression diagnostics, by object kind

Expression problems report under their own code per object kind, so you can tell at a glance which kind of object failed:

| Kind   | Could not be translated           | Could not be parsed              |
| ------ | --------------------------------- | -------------------------------- |
| Campo  | `FIELD_EXPRESSION_UNTRANSLATED`   | `FIELD_EXPRESSION_PARSE_ERROR`   |
| Medida | `MEASURE_EXPRESSION_UNTRANSLATED` | `MEASURE_EXPRESSION_PARSE_ERROR` |
| Join   | `JOIN_EXPRESSION_UNTRANSLATED`    | `JOIN_EXPRESSION_PARSE_ERROR`    |

An _untranslated_ expression was understood but uses a construct with no DAX equivalent; the original is preserved as a comment. A _parse error_ means the expression could not be read at all, and the diagnostic's `Context` carries the parser's own message.

### Emitting to Tabular

| Code                               | Raised when                                                                                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `REFERENCE_FIELD_INVALID_SOURCE`   | A reference field points at a field id that is missing or is not a source field. A placeholder column is emitted          |
| `DERIVED_FIELD_UNTRANSLATED`       | A derived field's expression could not be translated to DAX. The original is preserved as a comment                       |
| `DERIVED_FIELD_NO_EXPRESSION`      | A derived field has no expression                                                                                                         |
| `MEASURE_UNTRANSLATED`             | A measure's expression could not be translated. The original is preserved as a comment                                    |
| `CALCULATED_MEASURE_NO_EXPRESSION` | A calculated measure has no source expression. A placeholder body is emitted                                              |
| `MEASURE_UNRESOLVED_AT_EMIT`       | A measure references a measure that has not been emitted. Falls back to the verbatim source                               |
| `TABLE_UNRESOLVED_AT_EMIT`         | A measure references a table that has not been emitted. Falls back to the verbatim source                                 |
| `COLUMN_UNRESOLVED_AT_EMIT`        | A measure references a field that has not been emitted as a column. Falls back to the verbatim source                     |
| `MEASURE_WINDOW_UNSUPPORTED`       | A measure uses an unsupported window specification. It is left inert, with the original definition preserved as a comment |

## Anatomía de una regla de validación

Validation rules are all instances of [`IMetricViewValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Interfaces.IMetricViewValidationRule).
En lugar de profundizar en esa interfaz, es más fácil entender y trabajar con las reglas de validación mediante los métodos auxiliares:

- [`MakeValidationRuleForField`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForField%2A)
- [`MakeValidationRuleForJoin`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForJoin%2A)
- [`MakeValidationRuleForMeasure`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForMeasure%2A)
- [`MakeValidationRuleForView`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRuleForView%2A)
- [`MakeValidationRule`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.MakeValidationRule%2A)

Las cuatro primeras son específicas para crear una regla para el tipo de objeto indicado en su nombre.
Ofrecen una interfaz simplificada en la que proporcionas:

- `name`: un nombre corto y único para identificar la regla
- `category`: útil para agrupar reglas similares, pero en última instancia es completamente opcional
- `message`: el texto que se mostrará en el mensaje de diagnóstico cuando se incumpla esta regla
- `isInvalid`: una función que tomará el objeto de Metric View como argumento y devolverá `true` si ese objeto no es válido

El nombre y la categoría están pensados para facilitar el trabajo con colecciones de reglas, como se hace en scripts de C# que utilizan reglas personalizadas.

Each of these helpers also has an overload with a final `minVersion` argument.
This argument would take a version string, such as "0.1" or "1.1".
Rules with `minVersion` set are only evaluated for Metric Views at or above that version.

Esto se entiende mejor con un ejemplo:

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
La regla se llama (irónicamente) "no_underscores".
Tiene la categoría "naming", para indicar que tiene que ver con cómo nombramos las cosas.
The message you will see when the rule is violated is, "Do not include underscores in field names. Use nombres fáciles de leer con espacios."
The last argument defines a function that will be called for each Metric View field in the model; its body is a boolean expression that returns `true` for a Metric View field with an underscore in its `Name` property.

Aquí tienes un script completo que define una Metric View en línea y luego la deserializa y la valida, mostrando cómo se usa esta regla.

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

**Salida**

```
[Error] no_underscores Model.Fields["first_field"]
     Do not include underscores in field names. Use user-friendly names with spaces.
```

You can see that one of the Metric View fields has an underscore in its name.
Al ejecutar el script, verás un único mensaje de diagnóstico después de validar con la regla que definimos.
Puedes ver los detalles que se proporcionan en el mensaje de diagnóstico:

- Code: the name you assign to your rule
- Context: not set by these helpers
- Mensaje: el mensaje que definiste en la regla
- Ruta: una representación de dónde se encuentra ese objeto en la Vista de métricas
- Gravedad: se establece en Error de forma predeterminada con estos métodos auxiliares

![salida de un campo que infringe la regla de validación](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation.png)

Si quieres más control sobre el mensaje de diagnóstico y más flexibilidad en la función de validación, puedes usar `MakeValidationRule` mencionado arriba para crear una regla de validación contextual.

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

**Salida**

```
[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

This helper method requires you to pass the object type as a type parameter, and the validation function now is a two-parameter function, defined with the signature `(metricViewObject, context)`.
El primer parámetro es el objeto de Metric View para el que se evalúa la regla.
The second parameter is an [`IReadOnlyValidationContext`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.Validation.IReadOnlyValidationContext).
This context object holds collections with the names of already-checked objects;
this means we can use it to inspect only objects already validated.
The context object also has helper methods to make a new diagnostic message;
the benefit here is that your message doesn't have to be a hard-coded string,
but can include properties of the object you are checking.
We use `MakeError`, and the context object also includes a `MakeWarning`.
You can see in this example that we include in the message both the offending field and the field it aliases.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation2.png)

## Buenas prácticas para reglas de validación

Es recomendable crear muchas reglas simples, en lugar de menos reglas más complejas.
El proceso de validación es muy ligero, así que no hay problemas de rendimiento por tener muchas reglas.
For example, if you want to make sure that Metric View field names are not `camelCased`, not `kebab-cased` and not `snake_cased`, it is better to make three separate rules, rather than trying to check for each of those conditions in a single rule.
Esto permite que cada regla sea simple y que los mensajes sean muy específicos y, por tanto, más fáciles de solucionar.

En general, cuando ya tienes una regla que detecta un problema concreto, es mejor dejarla tal cual en vez de editarla.
Si ves que a la regla le falta alguna condición que te gustaría detectar, solo tienes que añadir una regla nueva, pequeña y simple para cubrir esa condición.

Puedes guardar muchas reglas distintas en un C# Script para reutilizarlas con diferentes Metric Views.
Como [una Metric View cargada es accesible desde varios scripts](xref:semantic-bridge-metric-view-object-model#loading-and-accessing-the-metric-view), puedes guardar varios archivos C# Script que solo definan reglas y luego llamar a `SemanticBridge.MetricView.Validate` y reutilizar esos scripts de validación fácilmente.
See the image below, where the script on the left, "deserialize-mv.csx" has already been run, to load a Metric View to Tabular Editor.
Después, se ejecuta el segundo script, a la derecha, "run-rules.csx", para validar.
Este segundo script podría ser uno que tengas siempre a mano para todas tus Metric Views.

![salida de un campo que infringe la regla de validación más compleja](~/content/assets/images/features/semantic-bridge/semantic-bridge-metric-view-validation3.png)

Los scripts se copian a continuación por comodidad, pero no son más que reorganizaciones de los scripts que vimos anteriormente.

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

**Salida**

```
[Error] no_underscores Model.Fields["repeat_customer"]
     Do not include underscores in field names. Use user-friendly names with spaces.

[Error] field_alias Model.Fields["repeat_customer"]
     Field 'repeat_customer' reuses source expression 'source.customer_id', already used by field 'customer'.
```

## Referencias

- @semantic-bridge-metric-view-object-model
- @semantic-bridge-metric-view-fields-and-dimensions
- @semantic-bridge-how-tos
