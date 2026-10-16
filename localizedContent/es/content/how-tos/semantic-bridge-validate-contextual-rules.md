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
Estas reglas se incluyen solo con fines ilustrativos y no reflejan necesariamente requisitos técnicos estrictos ni de Metric Views ni del Semantic Bridge.

> [!NOTE]
> Estos procedimientos se aplican a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

## Cuándo usar reglas contextuales

Use reglas contextuales cuando necesite:

- Comprueba que no se reutilice un nombre en distintos tipos de objeto
- Acceder a información sobre objetos validados previamente

> [!NOTE]
> El proceso de validación valida cada objeto de Metric View en orden (primero los joins, luego los campos y después las medidas), por lo que el contexto solo incluye los elementos que ya se han procesado durante la validación.

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

- `context.FieldNames` - nombres de los campos ya validados
- `context.MeasureNames` - nombres de las medidas ya validadas
- `context.JoinNames` - nombres de los joins ya validados
- `context.MakeError(code, message, object)` - crea un diagnóstico de error con un código y mensajes para el objeto especificado
- `context.MakeWarning(code, message, object)` - crea un diagnóstico de advertencia con un código y mensajes para el objeto especificado

Como creas el mensaje de diagnóstico en el cuerpo de la función de validación, puedes incluir en el mensaje detalles sobre el objeto actual que se está validando.

## Directiva `using` para los tipos de Metric View

Agrega esta directiva `using` para hacer referencia a los tipos de Metric View:

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Regla: El nombre de una medida de Metric View no debe duplicar el nombre de un campo de Metric View

Los campos se validan antes que las medidas, de modo que, cuando se comprueba una medida, `context.FieldNames` ya contiene todos los nombres de los campos.

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

## Regla: El nombre de una medida de Metric View no debe duplicar el nombre de un join de Metric View

Los joins se validan primero, por lo que `context.JoinNames` ya contiene todos los nombres de los joins cuando se comprueban las medidas.

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

Puedes ejecutar reglas contextuales junto con las reglas de validación predeterminadas llamando a `Validate` dos veces:

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
