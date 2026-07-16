---
uid: semantic-bridge-validate-contextual-rules
title: Crear reglas de validación contextuales
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

# Crear reglas de validación contextuales

Este procedimiento muestra cómo crear reglas de validación que comprueben condiciones entre varios objetos mediante el contexto de validación.
Estas reglas son solo ilustrativas y no reflejan necesariamente requisitos técnicos estrictos de Metric Views ni de Semantic Bridge.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

## Cuándo usar reglas contextuales

Use reglas contextuales cuando necesite:

- Check that a name is not reused across different object types
- Acceder a información sobre objetos validados previamente

> [!NOTE]
> The validation process validates each Metric View object in order (joins, then fields, then measures), so the context consists only of those items already visited in the validation.

## El método MakeValidationRule

El método genérico `MakeValidationRule<T>` proporciona acceso al contexto de validación:

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(  // or Field, Join, View
    "rule_name",
    "category",

    // return an IEnumerable<DiagnosticMessage>;
    // an empty collection means the object passed
    (obj, context) => []
);
```

El parámetro `context` proporciona:

- `context.FieldNames` - names of fields already validated
- `context.MeasureNames` - nombres de las medidas ya validadas
- `context.JoinNames` - nombres de los joins ya validados
- `context.MakeError(code, message, object)` - create an error diagnostic for the given object
- `context.MakeWarning(code, message, object)` - create a warning diagnostic for the given object

Como creas el mensaje de diagnóstico en el cuerpo de la función de validación, puedes incluir en el mensaje detalles sobre el objeto actual que se está validando.

## Directiva `using` para los tipos de Metric View

Agrega esta directiva `using` para hacer referencia a los tipos de Metric View:

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Rule: a Metric View Measure name must not duplicate a Metric View Field name

Fields are validated before measures, so when a measure is checked, `context.FieldNames` already holds every field name.

```csharp {compile}
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

```csharp {compile}
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

## Por qué es mejor separar las reglas

Fíjate en que creamos dos reglas separadas en lugar de una regla combinada. Este es el enfoque recomendado porque:

1. **Mensajes de error más claros**: Cada regla genera un mensaje específico y útil
2. **Mantenimiento más sencillo**: Las reglas se pueden agregar, quitar o modificar de forma independiente
3. **Lógica más sencilla**: Cada regla comprueba exactamente una condición
4. **Mejor categorización**: Las reglas se pueden agrupar y filtrar según su finalidad

## Ejemplo completo

Este Metric View tiene conflictos de nombres que activarán ambas reglas contextuales:

```csharp {run id=complete setup=mv-sample after=none output=true}
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

**Salida:**

```
CONTEXTUAL VALIDATION RESULTS
-----------------------------

Found 2 issue(s):

[Error] Measure 'revenue' has the same name as a field
[Error] Measure 'customer' has the same name as a join
```

## Combinar con las reglas predeterminadas

You can run contextual rules alongside the default validation rules by calling `Validate` twice:

```csharp {run id=combined setup=mv-sample after=complete output=true}
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

**Salida**

```
Default rule issues: 0
Custom rule issues: 2
```

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
