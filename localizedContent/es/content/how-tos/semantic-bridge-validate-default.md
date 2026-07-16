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

This how-to demonstrates validating a loaded Metric View using the built-in validation rules and interpreting the diagnostic messages.

> [!NOTE]
> These how-tos target Tabular Editor 3.26.2 and later.
> Earlier versions do not support the v1.1 Metric View features shown here.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Reglas de validación predeterminadas

The Semantic Bridge includes built-in rules that validate a Metric View definition against rules defined in [the Metric View documentation](https://learn.microsoft.com/azure/databricks/business-semantics/).
These rules are automatically run upon deserialization, whether via `Deserialize` directly or any method that reads a Metric View, such as `Load` or `ImportToTabularFromFile`.
Diagnostics from those automatic runs remain available afterward through `SemanticBridge.MetricView.ImportDiagnostics`.
You can also run these rules on demand against the loaded Metric View, which this document covers.

## Ejecutar la validación con las reglas predeterminadas

Run [`SemanticBridge.MetricView.Validate();`](xref:TabularEditor.SemanticBridge.Platforms.Databricks.DatabricksMetricViewService.Validate) with no arguments to run the built-in rules against the loaded Metric View.

```csharp {run id=validate-count setup=mv-sample after=none output=true}
var diagnostics = SemanticBridge.MetricView.Validate().ToList();

Output($"Validación completada: se encontraron {diagnostics.Count} problema(s)");
```

**Salida**

```
Validation complete: 0 issue(s) found
```

The sample Metric View is valid, so this reports no issues.

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
VALIDATION RESULTS
------------------

No issues found.
```

## Example with a validation error

Validation always runs against the currently loaded Metric View, so you can introduce a violation in a script and see it caught.
Here we clear a field's expression to trigger `FieldExprRequired`:

```csharp {run id=error-example setup=mv-sample after=none output=true}
var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = "";

var diagnostics = SemanticBridge.MetricView.Validate().ToList();

var sb = new System.Text.StringBuilder();
sb.AppendLine("VALIDATION RESULTS");
sb.AppendLine("------------------");
sb.AppendLine("");

if (diagnostics.Count == 0)
{
    sb.AppendLine("No issues found.");
}
else
{
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"[{diag.Severity}] {diag.Message}");
        sb.AppendLine($"  Path: {diag.Path}");
        sb.AppendLine("");
    }
}

Output(sb.ToString());
```

**Salida:**

```
VALIDATION RESULTS
------------------

[Error] Field 'order_year' expr cannot be empty
  Path: Model.Fields["order_year"].Expr
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
Errors: 0
Total issues: 0
```

## Siguientes pasos

- [Create simple validation rules](xref:semantic-bridge-validate-simple-rules)
- [Create contextual validation rules](xref:semantic-bridge-validate-contextual-rules)

## Ver también

- [Validación de Semantic Bridge](xref:semantic-bridge-metric-view-validation)
- [Modelo de objetos de la Metric View](xref:semantic-bridge-metric-view-object-model)
