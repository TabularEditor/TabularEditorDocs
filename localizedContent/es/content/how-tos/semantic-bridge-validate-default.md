---
uid: semantic-bridge-validate-default
title: Validar una vista de métricas con las reglas predeterminadas
author: Greg Baldini
updated: 2026-04-17
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

# Validar una vista de métricas con las reglas predeterminadas

Esta guía muestra cómo validar una vista de métricas cargada con las reglas de validación integradas e interpretar los mensajes de diagnóstico.

## Reglas de validación predeterminadas

El Semantic Bridge incluye estas reglas de validación integradas:

| Regla                      | Descripción                                                                                                                            |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| JoinNameRequired           | La unión de la vista de métricas debe tener un nombre                                                                                  |
| UniqueJoinName             | Los nombres de las uniones de la vista de métricas deben ser únicos                                                                    |
| JoinSourceRequired         | La unión de la vista de métricas debe tener un origen                                                                                  |
| JoinOnOrUsingRequired      | La unión de la vista de métricas debe especificar `on` o `using`                                                                       |
| JoinOnOrUsingExclusivity   | Una unión de Metric View no puede especificar simultáneamente `on` y `using`                                                           |
| JoinOnFormat               | La cláusula `on` de la unión de Metric View debe ser una expresión de equiunión válida                                                 |
| JoinUsingColumnCOUNT       | La cláusula `using` del Metric View Join debe tener exactamente una columna (limitación de la vista previa pública) |
| DimensionNameRequired      | La dimensión de Metric View debe tener un nombre                                                                                       |
| UniqueDimensionName        | Los nombres de las dimensiones de Metric View deben ser únicos                                                                         |
| DimensionExprRequired      | La dimensión de Metric View debe tener una expresión                                                                                   |
| NombreDeMedidaRequerido    | La medida de Metric View debe tener un nombre                                                                                          |
| NombreDeMedidaUnico        | Los nombres de las medidas de Metric View deben ser únicos                                                                             |
| ExpresionDeMedidaRequerida | La medida de Metric View debe tener una expresión                                                                                      |

## Ejecutar la validación con las reglas predeterminadas

Llama a `Validate()` sin argumentos para usar las reglas de validación integradas.

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validación completada: se encontraron {diagnostics.Count} problema(s)");
```

## Interpreta los mensajes de diagnóstico

Cada mensaje de diagnóstico contiene:

- **Gravedad**: Error, Advertencia o Información
- **Mensaje**: Descripción del problema
- **Ruta**: Ubicación del objeto en la jerarquía de Metric View

```csharp
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine("RESULTADOS DE LA VALIDACIÓN");
sb.AppendLine("------------------");
sb.AppendLine("");

if (diagnostics.Count == 0)
{
    sb.AppendLine("No se encontraron problemas.");
}
else
{
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"[{diag.Severity}] {diag.Message}");
        sb.AppendLine($"  Ruta: {diag.Path}");
        sb.AppendLine("");
    }
}

Output(sb.ToString());
```

## Ejemplo con errores de validación

Algunas reglas (campos obligatorios) se aplican durante la deserialización.
Las reglas restantes comprueban si hay duplicados y problemas estructurales después de la deserialización.

Esta Metric View muestra infracciones que `Validate()` detecta:

```csharp
SemanticBridge.MetricView.Deserialize("""
    version: 0.1
    source: sales.fact.orders
    joins:
      # UniqueJoinName - nombre duplicado 'customer'
      - name: customer
        source: sales.dim.customer
        on: customer_id = customer.customer_id
      - name: customer
        source: sales.dim.customer_backup
        on: customer_id = customer_backup.customer_id
      # JoinOnOrUsingRequired - no se especifica ni on ni using
      - name: date
        source: sales.dim.date
    dimensions:
      # UniqueDimensionName - nombre duplicado 'category'
      - name: category
        expr: product.category
      - name: category
        expr: product.subcategory
      - name: product_name
        expr: product.product_name
    measures:
      # UniqueMeasureName - nombre duplicado 'total'
      - name: total
        expr: SUM(revenue)
      - name: total
        expr: SUM(quantity)
      - name: order_count
        expr: COUNT(order_id)
    """);

var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
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
Se encontraron 6 problema(s):

[Error] La unión 'customer' debe usar una condición de igualdad simple con prefijos de tabla (p. ej., 'source.column = dimension.column')
[Error] Nombre de unión duplicado: 'customer'
[Error] La unión 'customer' debe usar una condición de igualdad simple con prefijos de tabla (p. ej., 'source.column = dimension.column')
[Error] La unión 'date' debe especificar una cláusula 'on' o 'using'
[Error] Nombre de dimensión duplicado: 'category'
[Error] Nombre de medida duplicado: 'total'
```

## Filtrar diagnósticos por gravedad

Puedes filtrar los diagnósticos para centrarte solo en los errores:

```csharp
using System.Linq;
using TabularEditor.SemanticBridge.Orchestration;

var diagnostics = SemanticBridge.MetricView.Validate().ToList();
var errors = diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Errores: {errors.Count}");
sb.AppendLine($"Total de problemas: {diagnostics.Count}");
Output(sb.ToString());
```

## Siguientes pasos

- [Crear reglas de validación simples](xref:semantic-bridge-validate-simple-rules) para aplicar tus propias convenciones
- [Crear reglas de validación contextuales](xref:semantic-bridge-validate-contextual-rules) para comprobaciones entre objetos

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
