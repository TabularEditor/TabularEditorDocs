---
uid: semantic-bridge-validate-simple-rules
title: Crear reglas de validación sencillas
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

# Crear reglas de validación sencillas

Esta guía muestra cómo crear reglas de validación sencillas basadas en predicados para aplicar convenciones de nomenclatura y requisitos estructurales.
Estas reglas se incluyen solo con fines ilustrativos y no reflejan necesariamente requisitos técnicos estrictos ni de Metric Views ni del Semantic Bridge.

## Los cuatro métodos auxiliares para reglas

Hay un método auxiliar para cada tipo de objeto de Metric View:

- `MakeValidationRuleForView`: reglas para el objeto View raíz
- `MakeValidationRuleForJoin`: reglas para objetos Join
- `MakeValidationRuleForDimension`: reglas para objetos Dimension
- `MakeValidationRuleForMeasure`: reglas para objetos de medida

Cada método auxiliar acepta cuatro parámetros:

1. **name**: identificador único de la regla
2. **category**: agrupación de reglas relacionadas
3. **message**: mensaje de error cuando se infringe la regla
4. **isInvalid**: una función que devuelve `true` si el objeto no es válido

## Regla para el objeto View

Compruebe que el valor de la versión de Metric View sea el esperado:

```csharp
var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "La versión de Metric View debe ser 0,1 o 1,1; solo se admiten 0,1 y 1,1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);
```

## Regla para Metric View Join

Compruebe que los orígenes de join de Metric View utilicen nombres de tabla totalmente cualificados (contienen un punto):

```csharp
var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "El origen del join debe ser un nombre de tabla totalmente cualificado (p. ej., `catalog.schema.table`)",
    (join) => !join.Source.Contains('.')
);
```

## Regla para la dimensión de Metric View

Compruebe que los nombres de las dimensiones de Metric View no contengan guiones bajos:

```csharp
var dimensionNameRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Los nombres de las dimensiones deben usar espacios, no guiones bajos",
    (dim) => dim.Name.Contains('_')
);
```

## Regla para la medida de Metric View

Compruebe que las expresiones de las medidas de Metric View no contengan SELECT (para evitar subconsultas accidentales):

```csharp
var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "Las expresiones de las medidas no deben contener subconsultas SELECT",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);
```

## Ejemplo completo

Esta Metric View tiene infracciones en cada una de las reglas definidas anteriormente:

```csharp
// Cree una Metric View con infracciones para cada regla
SemanticBridge.MetricView.Deserialize("""
    version: 0.2 # 0,2
    source: sales.fact.orders
    joins:
      # infracción de joinSourceRule: no está totalmente cualificado
      - name: customer
        source: customer_table
        on: source.customer_id = customer.customer_id
    dimensions:
      # infracciones de dimensionNameRule: contiene guiones bajos
      - name: product_name
        expr: source.product_name
      - name: order_date
        expr: source.order_date
      # Este está bien
      - name: Category
        expr: source.category
    measures:
      # infracción de measureExprRule: contiene una subconsulta SELECT
      - name: complex_calc
        expr: (SELECT MAX(price) FROM products)
      # Este está bien
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var versionRule = SemanticBridge.MetricView.MakeValidationRuleForView(
    "version_check",
    "structure",
    "La versión de Metric View debe ser 0,1 o 1,1; solo se admiten 0,1 y 1,1",
    (view) => view.Version != "0.1" && view.Version != "1.1"
);

var joinSourceRule = SemanticBridge.MetricView.MakeValidationRuleForJoin(
    "qualified_source",
    "structure",
    "El origen del join debe ser un nombre de tabla totalmente cualificado (p. ej., `catalog.schema.table`)",
    (join) => !join.Source.Contains('.')
);

var dimensionNameRule = SemanticBridge.MetricView.MakeValidationRuleForDimension(
    "no_underscores",
    "naming",
    "Los nombres de las dimensiones deben usar espacios, no guiones bajos",
    (dim) => dim.Name.Contains('_')
);

var measureExprRule = SemanticBridge.MetricView.MakeValidationRuleForMeasure(
    "no_select_subquery",
    "structure",
    "Las expresiones de las medidas no deben contener subconsultas SELECT",
    (measure) => measure.Expr.ToUpper().Contains("SELECT")
);

// Ejecute la validación con reglas personalizadas
var diagnostics = SemanticBridge.MetricView.Validate([
    versionRule,
    joinSourceRule,
    dimensionNameRule,
    measureExprRule
]).ToList();

// Muestre los resultados
var sb = new System.Text.StringBuilder();
sb.AppendLine("RESULTADOS DE LA VALIDACIÓN PERSONALIZADA");
sb.AppendLine("-------------------------");
sb.AppendLine("");
sb.AppendLine($"Se han encontrado {diagnostics.Count} problema(s):");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Path}: {diag.Message}");
}

Output(sb.ToString());
```

**Salida:**

```
RESULTADOS DE LA VALIDACIÓN PERSONALIZADA
-------------------------

Se han encontrado 5 problema(s):

[Error] MetricView: La versión de Metric View debe ser 0,1 o 1,1
[Error] MetricView.Joins['customer']: El origen del join debe ser un nombre de tabla totalmente cualificado (p. ej., `catalog.schema.table`)
[Error] MetricView.Dimensions['product_name']: Los nombres de las dimensiones deben usar espacios, no guiones bajos
[Error] MetricView.Dimensions['order_date']: Los nombres de las dimensiones deben usar espacios, no guiones bajos
[Error] MetricView.Measures['complex_calc']: Las expresiones de las medidas no deben contener subconsultas SELECT
```

## Próximos pasos

- [Cree reglas de validación contextuales](xref:semantic-bridge-validate-contextual-rules) para comprobaciones entre objetos, como la detección de duplicados

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
- [Valide con reglas predeterminadas](xref:semantic-bridge-validate-default)
