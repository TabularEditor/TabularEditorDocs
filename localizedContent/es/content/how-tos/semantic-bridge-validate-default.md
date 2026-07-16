---
uid: semantic-bridge-validate-default
title: Validar una vista de métricas con las reglas predeterminadas
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

# Validar una vista de métricas con las reglas predeterminadas

Esta guía muestra cómo validar una vista de métricas cargada con las reglas de validación integradas e interpretar los mensajes de diagnóstico.

> [!NOTE]
> Estas guías están dirigidas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Reglas de validación predeterminadas

El Semantic Bridge incluye reglas integradas que validan la definición de una vista de métricas según las reglas establecidas en [la documentación de Metric View](https://learn.microsoft.com/azure/databricks/business-semantics/).
Estas reglas se ejecutan automáticamente durante la deserialización, ya sea llamando directamente a `Deserialize` o mediante cualquier método que lea una vista de métricas, como `Load` o `ImportToTabularFromFile`.
Los diagnósticos de esas ejecuciones automáticas siguen estando disponibles después, a través de `SemanticBridge.MetricView.ImportDiagnostics`.
También puedes ejecutar estas reglas a demanda sobre la vista de métricas cargada, que es lo que se describe en este documento.

## Ejecutar la validación con las reglas predeterminadas

Ejecuta [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) sin argumentos para aplicar las reglas integradas a la vista de métricas cargada.

```csharp {run id=validate-count setup=mv-sample after=none output=true}
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validación completada: se encontraron {diagnostics.Count} problema(s)");
```

**Salida**

```
Validación completada: se han encontrado 0 problema(s)
```

La vista de métricas de ejemplo es válida, por lo que el Report no indica ningún problema.

## Interpreta los mensajes de diagnóstico

Cada mensaje de diagnóstico contiene:

- **Gravedad**: Error, Advertencia o Información
- **Mensaje**: Descripción del problema
- **Ruta**: Ubicación del objeto en la jerarquía de Metric View

```csharp {run id=interpret setup=mv-sample after=none output=true}
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

**Salida**

```
RESULTADOS DE LA VALIDACIÓN
------------------

No se encontraron problemas.
```

## Ejemplo con un error de validación

La validación siempre se ejecuta sobre la vista de métricas cargada en ese momento, por lo que puedes introducir una infracción en un script y ver cómo se detecta.
Aquí vaciamos la expresión de un campo para desencadenar `FieldExprRequired`:

```csharp {run id=error-example setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = "";

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

**Salida:**

```
RESULTADOS DE LA VALIDACIÓN
------------------

[Error] La expresión del campo 'order_year' no puede estar vacía
  Ruta: Model.Fields["order_year"].Expr
```

## Filtrar diagnósticos por gravedad

Puedes filtrar los diagnósticos para centrarte solo en los errores:

```csharp {run id=filter-severity setup=mv-sample after=none output=true}
using System.Linq;
using TabularEditor.SemanticBridge.Orchestration;

var diagnostics = SemanticBridge.MetricView.Validate().ToList();
var errors = diagnostics.Where(d => d.Severity == DiagnosticSeverity.Error).ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Errores: {errors.Count}");
sb.AppendLine($"Total de problemas: {diagnostics.Count}");
Output(sb.ToString());
```

**Salida**

```
Errores: 0
Problemas totales: 0
```

## Siguientes pasos

- [Crear reglas de validación sencillas](xref:semantic-bridge-validate-simple-rules)
- [Crear reglas de validación contextuales](xref:semantic-bridge-validate-contextual-rules)

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
