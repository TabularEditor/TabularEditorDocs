---
uid: semantic-bridge-import
title: Importar una Vista de métricas y ver los diagnósticos
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

# Importar una Vista de métricas y ver los diagnósticos

Este procedimiento explica cómo importar una Vista de métricas a un modelo tabular mediante C# Scripts y cómo ver los mensajes de diagnóstico del proceso de importación.

## Requisitos previos

Antes de importar, debes tener un modelo tabular abierto en Tabular Editor. Puede ser:

- Un modelo nuevo y vacío
- Un modelo existente que quieras mejorar con objetos de la Vista de métricas

## Métodos de importación

Hay dos métodos de importación:

| Método                    | Descripción                                               |
| ------------------------- | --------------------------------------------------------- |
| `ImportToTabularFromFile` | Carga desde una ruta de archivo e importa en un solo paso |
| `ImportToTabular`         | Importa la Vista de métricas cargada actualmente          |

Ambos métodos requieren:

- El modelo tabular `Model` de destino
- Nombre de host de Databricks (para expresiones M de partición)
- Ruta HTTP de Databricks (para expresiones M de partición)

## Importar desde archivo

Use `ImportToTabularFromFile` para cargar e importar en una sola operación:

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "C:/MetricViews/sales-metrics.yaml",
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
if (success)
{
    sb.AppendLine("¡Importación correcta!");
    sb.AppendLine($"Diagnósticos: {diagnostics.Count}");
}
else
{
    sb.AppendLine("Error al importar.");
    sb.AppendLine($"Errores: {diagnostics.Count}");
}

Output(sb.ToString());
```

## Importar una Metric View cargada

Si ya has cargado una Metric View (para inspeccionarla o modificarla), usa `ImportToTabular`:

```csharp
// Primero, carga la Metric View
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");

// Opcionalmente, revísala o modifícala
var view = SemanticBridge.MetricView.Model;

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Importando la Metric View con {view.Dimensions.Count} dimensiones y {view.Measures.Count} medidas");

// Importar a Tabular
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

if (success)
{
    sb.AppendLine("¡Importación correcta!");
}
else
{
    sb.AppendLine("Error al importar.");
}

Output(sb.ToString());
```

## Usar valores de conexión ficticios

Si estás probando la traducción sin una conexión real a Databricks, puedes usar valores ficticios:

```csharp
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "C:/MetricViews/sales-metrics.yaml",
    Model,
    "placeholder-host",
    "placeholder-path",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine("Importación completada (con valores de conexión ficticios)");
sb.AppendLine("Nota: Actualiza las expresiones M de partición antes de actualizar los datos.");
Output(sb.ToString());
```

## Ver diagnósticos después de la importación

Puedes acceder a los diagnósticos de la última importación en cualquier momento usando `ImportDiagnostics`.
Este ejemplo supone que ya has ejecutado una importación, ya sea desde la interfaz gráfica o mediante un C# Script.

```csharp
var diagnostics = SemanticBridge.MetricView.ImportDiagnostics;

var sb = new System.Text.StringBuilder();
sb.AppendLine("DIAGN\u00d3STICOS DE LA \u00daLTIMA IMPORTACI\u00d3N");
sb.AppendLine("-------------------------------");
sb.AppendLine("");
sb.AppendLine($"Total de incidencias: {diagnostics.Count}");
sb.AppendLine("");

foreach (var diag in diagnostics)
{
    sb.AppendLine($"[{diag.Severity}] {diag.Message}");
}

Output(sb.ToString());
```

## Mostrar los diagnósticos directamente

Para una inspección rápida, puedes mostrar directamente la colección de diagnósticos:

```csharp
// Mostrar todos los diagnósticos de la última importación
SemanticBridge.MetricView.ImportDiagnostics.Output();
```

## Ejemplo de flujo de trabajo completo

Carga, valida e importa con un informe de diagnóstico completo:

```csharp
var sb = new System.Text.StringBuilder();

// Cargar la Metric View
SemanticBridge.MetricView.Load("C:/MetricViews/sales-metrics.yaml");
var view = SemanticBridge.MetricView.Model;

sb.AppendLine("RESUMEN DE LA METRIC VIEW");
sb.AppendLine("------------------------");
sb.AppendLine($"Origen: {view.Source}");
sb.AppendLine($"Uniones: {view.Joins?.Count ?? 0}");
sb.AppendLine($"Dimensiones: {view.Dimensions.Count}");
sb.AppendLine($"Medidas: {view.Measures.Count}");
sb.AppendLine("");

// Validar primero
var validationDiags = SemanticBridge.MetricView.Validate().ToList();
sb.AppendLine("VALIDACIÓN");
sb.AppendLine("----------");
sb.AppendLine($"Incidencias: {validationDiags.Count}");
sb.AppendLine("");

// Importar
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var importDiags
);

sb.AppendLine("RESULTADO DE LA IMPORTACIÓN");
sb.AppendLine("---------------------------");
sb.AppendLine($"Éxito: {success}");
sb.AppendLine($"Diagnósticos: {importDiags.Count}");
sb.AppendLine("");

if (importDiags.Count > 0)
{
    sb.AppendLine("Incidencias de la importación:");
    foreach (var diag in importDiags)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Message}");
    }
}

Output(sb.ToString());
```

## Ver también

- [Descripción general de Semantic Bridge](xref:semantic-bridge)
- [Validar una vista de métricas](xref:semantic-bridge-validate-default)
- [Cargar e inspeccionar una vista de métricas](xref:semantic-bridge-load-inspect)
