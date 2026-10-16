---
uid: semantic-bridge-import
title: Importar una Vista de métricas y ver los diagnósticos
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

# Importar una vista de métricas y ver los diagnósticos

Este procedimiento muestra cómo importar una vista de métricas ya cargada en un modelo tabular mediante un C# Script y revisar los mensajes de diagnóstico que produce la importación.

> [!NOTE]
> Estos procedimientos se aplican a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la Vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Cada ejemplo a continuación se importa en el modelo tabular abierto.
> Si va a ejecutar más de uno, recomendamos deshacer la importación después de cada ejemplo (Editar>Deshacer en el menú o CTRL-z en el Explorador TOM).
> Si ejecutas cada importación una tras otra, obtendrás varias copias traducidas de la Vista de métricas.

## Importar la vista de métricas cargada

`ImportToTabular` traduce la Vista de métricas cargada actualmente en el modelo tabular abierto.
El nombre de host de Databricks y la ruta HTTP se usan al generar las expresiones M de las particiones;
para una prueba rápida, puede pasar valores de marcador de posición y corregirlos antes de actualizar los datos.

```csharp {run id=import setup=mv-sample after=none output=true}
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Imported {Model.AllColumns.Count()} fields and {Model.AllMeasures.Count()} measures.");
sb.AppendLine(success ? "Import successful." : "Import failed.");
sb.AppendLine($"Diagnostics: {diagnostics.Count}");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
Output(sb.ToString());
```

**Salida:**

```
Imported 15 fields and 6 measures.
Import successful.
Diagnostics: 0
```

Ten en cuenta que el número de campos importados incluye las claves de unión y las referencias implícitas a columnas de la definición de la Vista de métricas,
por lo que es mayor que el número de `Fields` explícitos en la definición de la Vista de métricas.

## Revisar los diagnósticos de la última importación

Los diagnósticos de la importación más reciente están disponibles en cualquier momento mediante `ImportDiagnostics`, incluso después de una importación realizada mediante la interfaz gráfica GUI.

```csharp {compile}
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
    Output($"[{d.Severity}] {d.Code}: {d.Message}");
```

## Ver un diagnóstico de traducción

Algunos elementos de la Vista de métricas no se pueden traducir a Tabular.
Una medida de ventana, por ejemplo, no se traduce a DAX:
la importación crea una medida TOM de marcador de posición con la definición original de la Vista de métricas en un comentario
y genera un Report de advertencia de diagnóstico.

Agregue una especificación de ventana a una medida y luego importe para ver el diagnóstico:

```csharp {run id=window-diagnostic setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// add a window spec
view.Measures["total_revenue"].Window =
[
    new MetricView.Window
    {
        Order = "order_date",
        Range = "trailing 3 month",
        Semiadditive = MetricView.Window.SemiadditiveType.Last
    }
];

var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine(success ? "Import succeeded with issues." : "Import failed.");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
// note that we search for the DisplayName, as that is what is translated to TOM
sb.AppendLine($"TOM measure expression: {Model.AllMeasures.First(m => m.Name == "Total Revenue").Expression}");
Output(sb.ToString());
```

**Salida:**

```
Import succeeded with issues.
  [Warning] MEASURE_WINDOW_UNSUPPORTED: Measure 'Total Revenue' uses a window specification that is not currently supported; it has been left inert with the original definition preserved as a comment.
TOM measure expression: // This measure uses a window specification (windowed / cumulative / semiadditive),
// which is not currently supported when importing Databricks Metric Views.
// The measure has been left blank - review the details below and author the DAX
// manually. The translated DAX does NOT account for the window spec; you will most
// likely need to wrap it in CALCULATE (or similar) to apply the windowing.
//
// Original source expression (Databricks SQL):
/*
SUM(revenue)
*/
//
// Suggested DAX translation (window spec NOT applied):
/*
SUM('Fact'[revenue])
*/
//
// Window specification:
/*
- order: order_date
  range: trailing 3 month
  semiadditive: last

*/
```

## Pasos a seguir

- [Importar una Metric View desde un archivo](xref:semantic-bridge-metric-view-import-from-file)
- [Cargar e inspeccionar una Metric View](xref:semantic-bridge-load-inspect)
- [Validar una vista de métricas](xref:semantic-bridge-validate-default)

## Ver también

- [Información general de Semantic Bridge](xref:semantic-bridge)
