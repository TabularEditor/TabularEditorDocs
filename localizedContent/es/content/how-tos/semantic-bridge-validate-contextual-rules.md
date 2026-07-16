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
> Estas guías prácticas están dirigidas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

## Cuándo usar reglas contextuales

Use reglas contextuales cuando necesite:

- Comprueba que no se reutilice un mismo nombre entre distintos tipos de objeto
- Acceder a información sobre objetos validados previamente

> [!NOTE]
> El proceso de validación revisa cada objeto de Metric View en orden (primero los joins, luego los campos y después las medidas), por lo que el contexto solo incluye los elementos que ya se han validado durante la validación.

## El método MakeValidationRule

El método genérico `MakeValidationRule<T>` proporciona acceso al contexto de validación:

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(  // o Field, Join, View
    "rule_name",
    "category",

    // devuelve un IEnumerable<DiagnosticMessage>;
    // una colección vacía significa que el objeto ha superado la validación
    (obj, context) => []
);
```

El parámetro `context` proporciona:

- `context.FieldNames` - nombres de los campos ya validados
- `context.MeasureNames` - nombres de las medidas ya validadas
- `context.JoinNames` - nombres de los joins ya validados
- `context.MakeError(code, message, object)` - crea un diagnóstico de error para el objeto especificado
- `context.MakeWarning(code, message, object)` - crea un diagnóstico de advertencia para el objeto especificado

Como creas el mensaje de diagnóstico en el cuerpo de la función de validación, puedes incluir en el mensaje detalles sobre el objeto actual que se está validando.

## Directiva `using` para los tipos de Metric View

Agrega esta directiva `using` para hacer referencia a los tipos de Metric View:

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;
```

## Regla: el nombre de una medida de Metric View no debe coincidir con el de un campo de Metric View

Los campos se validan antes que las medidas, así que, cuando se comprueba una medida, `context.FieldNames` ya contiene todos los nombres de los campos.

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNameRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_field_name",
    "naming",
    (measure, context) =>
        context.FieldNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_field_name_collision",
                $"La medida '{measure.Name}' tiene el mismo nombre que un campo",
                measure)]
            : []
);
```

## Regla: el nombre de una medida de Metric View no debe coincidir con el de un join de Metric View

Los joins se validan primero, por lo que `context.JoinNames` contiene todos los nombres de los joins cuando se comprueban las medidas.

```csharp {compile}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var measureNotJoinRule = SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
    "measure_not_join_name",
    "naming",
    (measure, context) =>
        context.JoinNames.Contains(measure.Name)
            ? [context.MakeError(
                "measure_join_name_collision",
                $"La medida '{measure.Name}' tiene el mismo nombre que un join",
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

// Crear una Metric View con nombres reutilizados entre tipos de objeto
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    joins:
      - name: customer
        source: sales.dim.customer
        on: source.customer_id = customer.customer_id
        cardinality: many_to_one
    fields:
      # 'revenue' también se usa como nombre de medida más abajo
      - name: revenue
        expr: source.revenue
      - name: quantity
        expr: source.quantity
    measures:
      # infracción de measureNameRule: mismo nombre que el campo 'revenue'
      - name: revenue
        expr: SUM(source.revenue)
      # infracción de measureNotJoinRule: mismo nombre que el join 'customer'
      - name: customer
        expr: COUNT(DISTINCT source.customer_id)
      # esta medida está bien
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
                $"La medida '{measure.Name}' tiene el mismo nombre que un campo",
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
                $"La medida '{measure.Name}' tiene el mismo nombre que un join",
                measure)]
            : []
);

// Ejecutar la validación con ambas reglas
var diagnostics = SemanticBridge.MetricView.Validate([
    measureNameRule,
    measureNotJoinRule
]).ToList();

// Mostrar resultados
var sb = new System.Text.StringBuilder();
sb.AppendLine("RESULTADOS DE VALIDACIÓN CONTEXTUAL");
sb.AppendLine("-----------------------------");
sb.AppendLine("");
sb.AppendLine($"Se encontraron {diagnostics.Count} problema(s):");
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

[Error] La medida 'revenue' tiene el mismo nombre que un campo
[Error] La medida 'customer' tiene el mismo nombre que un join
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
                    $"La medida '{measure.Name}' tiene el mismo nombre que un campo",
                    measure)]
                : []),
    SemanticBridge.MetricView.MakeValidationRule<MetricView.Measure>(
        "measure_not_join_name",
        "naming",
        (measure, context) =>
            context.JoinNames.Contains(measure.Name)
                ? [context.MakeError(
                    "measure_join_name_collision",
                    $"La medida '{measure.Name}' tiene el mismo nombre que un join",
                    measure)]
                : [])
};

// Ejecuta primero las reglas predeterminadas
var defaultDiagnostics = SemanticBridge.MetricView.Validate().ToList();

// Después ejecuta las reglas personalizadas
var customDiagnostics = SemanticBridge.MetricView.Validate(customRules).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Problemas de las reglas predeterminadas: {defaultDiagnostics.Count}");
sb.AppendLine($"Problemas de las reglas personalizadas: {customDiagnostics.Count}");
Output(sb.ToString());
```

**Salida**

```
Problemas de las reglas predeterminadas: 0
Problemas de las reglas personalizadas: 2
```

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
