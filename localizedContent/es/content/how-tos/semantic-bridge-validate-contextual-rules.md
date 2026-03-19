---
uid: semantic-bridge-validate-contextual-rules
title: Crear reglas de validación contextuales
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

# Crear reglas de validación contextuales

Este procedimiento muestra cómo crear reglas de validación que comprueben condiciones entre varios objetos mediante el contexto de validación.
Estas reglas son solo ilustrativas y no reflejan necesariamente requisitos técnicos estrictos de Metric Views ni de Semantic Bridge.

## Cuándo usar reglas contextuales

Use reglas contextuales cuando necesite:

- Detectar nombres duplicados entre objetos
- Comprobar que los nombres no entren en conflicto entre distintos tipos de objeto
- Acceder a información sobre objetos validados previamente

> [!NOTE]
> El proceso de validación revisa cada objeto de Metric View en orden, por lo que el contexto solo incluye los elementos que ya se han visitado durante la validación.

## El método MakeValidationRule

El método genérico `MakeValidationRule<T>` proporciona acceso al contexto de validación:

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

El parámetro `context` proporciona:

- `context.DimensionNames` - nombres de las dimensiones ya validadas
- `context.MeasureNames` - nombres de las medidas ya validadas
- `context.JoinNames` - nombres de los joins ya validados
- `context.MakeError(message)` - crea un diagnóstico de error
- `context.MakeError(message, property)` - crea un diagnóstico de error e indica la propiedad específica con un error

Como creas el mensaje de diagnóstico en el cuerpo de la función de validación, puedes incluir en el mensaje detalles sobre el objeto actual que se está validando.

## Directiva `using` para los tipos de Metric View

Agrega esta directiva `using` para hacer referencia a los tipos de Metric View:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Regla: El nombre de una medida de Metric View no debe duplicar el nombre de una dimensión de Metric View

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"La medida '{measure.Name}' tiene el mismo nombre que una dimensión")]
            : []
);
```

## Regla: El nombre de una medida de Metric View no debe duplicar otra medida de Metric View

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"La medida '{measure.Name}' está definida más de una vez")]
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

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

// Crear una Metric View con conflictos de nombres
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    dimensions:
      # 'revenue' se usa tanto como nombre de dimensión como de medida
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
      - name: order_date
        expr: source.order_date
    measures:
      # infracción de measureNotDimensionRule: mismo nombre que una dimensión
      - name: revenue
        expr: SUM(source.revenue)
      # infracción de noDuplicateMeasureRule: 'total_quantity' aparece dos veces
      - name: total_quantity
        expr: SUM(source.quantity)
      - name: total_quantity
        expr: COUNT(source.order_id)
      # Este está bien
      - name: order_count
        expr: COUNT(source.order_id)
    """);

// Definir reglas contextuales
var measureNotDimensionRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_dimension_name",
    "naming",
    (measure, context) =>
        context.DimensionNames.Contains(measure.Name)
            ? [context.MakeError($"La medida '{measure.Name}' tiene el mismo nombre que una dimensión")]
            : []
);

var noDuplicateMeasureRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "no_duplicate_measures",
    "naming",
    (measure, context) =>
        context.MeasureNames.Contains(measure.Name)
            ? [context.MakeError($"La medida '{measure.Name}' está definida más de una vez")]
            : []
);

// Ejecutar la validación
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNotDimensionRule,
    noDuplicateMeasureRule
]).ToList();

// Mostrar resultados
var sb = new System.Text.StringBuilder();
sb.AppendLine("RESULTADOS DE VALIDACIÓN CONTEXTUAL");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
sb.AppendLine($"Se encontraron {diagnostics.Count} incidencia(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

**Salida:**

```
RESULTADOS DE VALIDACIÓN CONTEXTUAL
-----------------------------

Se encontraron 2 problema(s):

[Error] La medida 'revenue' tiene el mismo nombre que una dimensión
[Error] La medida 'total_quantity' está definida más de una vez
```

## Combinar con las reglas predeterminadas

Puedes ejecutar reglas contextuales junto con las reglas de validación predeterminadas:

```csharp
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var customRules = new[] {
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_dimension_name",
        "naming",
        (measure, context) =>
            context.DimensionNames.Contains(measure.Name)
                ? [context.MakeError($"La medida '{measure.Name}' tiene el mismo nombre que una dimensión")]
                : []
    )
};

// Ejecuta primero las reglas predeterminadas
var defaultDiagnostics = SemanticBridge.MetricView.Validate().ToList();

// Después ejecuta las reglas personalizadas
var customDiagnostics = SemanticBridge.MetricView.Validate(customRules).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Incidencias de las reglas predeterminadas: {defaultDiagnostics.Count}");
sb.AppendLine($"Incidencias de las reglas personalizadas: {customDiagnostics.Count}");
Output(sb.ToString());
```

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
- [Crear reglas de validación sencillas](xref:semantic-bridge-validate-simple-rules)
- [Validar con reglas predeterminadas](xref:semantic-bridge-validate-default)
