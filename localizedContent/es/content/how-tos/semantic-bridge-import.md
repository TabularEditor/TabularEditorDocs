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

# Importar una Vista de métricas y consultar los diagnósticos

Este procedimiento muestra cómo importar una Vista de métricas ya cargada en un modelo tabular mediante un C# Script y cómo revisar los mensajes de diagnóstico que genera la importación.

> [!NOTE]
> Estos procedimientos se aplican a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la Vista de métricas v1.1 que se muestran aquí.

[!INCLUDE [sample](includes/sample-metricview.md)]

> [!NOTE]
> Cada ejemplo siguiente se importa en el modelo tabular abierto.
> Si va a ejecutar más de uno, le recomendamos deshacer la importación después de cada ejemplo (Editar > Deshacer en el menú, o CTRL-z en el Explorador TOM).
> Si ejecuta cada importación una tras otra, obtendrá varias copias traducidas de la Vista de métricas.

## Importar la Vista de métricas cargada

`ImportToTabular` traduce la Vista de métricas cargada actualmente en el modelo tabular abierto.
El nombre de host de Databricks y la ruta HTTP se usan al compilar las expresiones M de partición;
para una prueba rápida, puedes pasar valores de marcador de posición y corregirlos antes de actualizar los datos.

```csharp {run id=import setup=mv-sample after=none output=true}
var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine($"Se importaron {Model.AllColumns.Count()} campos y {Model.AllMeasures.Count()} medidas.");
sb.AppendLine(success ? "Importación correcta." : "Importación fallida.");
sb.AppendLine($"Diagnósticos: {diagnostics.Count}");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
Output(sb.ToString());
```

**Salida:**

```
Se importaron 15 campos y 6 medidas.
Importación correcta.
Diagnósticos: 0
```

Tenga en cuenta que el número de campos importados incluye las claves de combinación y las referencias implícitas a columnas de la definición de la Vista de métricas,
por lo que es mayor que el número de `Fields` explícitos en la definición de la Vista de métricas.

## Revisar los diagnósticos de la última importación

Los diagnósticos de la importación más reciente están disponibles en cualquier momento mediante `ImportDiagnostics`, incluso después de una importación realizada desde la interfaz gráfica de usuario (GUI).

```csharp {compile}
foreach (var d in SemanticBridge.MetricView.ImportDiagnostics)
    Output($"[{d.Severity}] {d.Code}: {d.Message}");
```

## Ver un diagnóstico de traducción

Algunos elementos de una Vista de métricas no se pueden traducir a un modelo tabular.
Por ejemplo, una medida de ventana no se traduce a DAX:
la importación crea una medida TOM provisional con la definición original de la Vista de métricas en un comentario
y le devuelve una advertencia de diagnóstico.

Agregue una especificación de ventana a una medida y, después, impórtela para ver el diagnóstico:

```csharp {run id=window-diagnostic setup=mv-sample after=none output=true}
using MetricView = TabularEditor.SemanticBridge.Platforms.Databricks.MetricView;

var view = SemanticBridge.MetricView.Model;

// agregue una especificación de ventana
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
sb.AppendLine(success ? "Importación completada con incidencias." : "Importación fallida.");
foreach (var diag in diagnostics)
{
    sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
}
// tenga en cuenta que buscamos por DisplayName, ya que es lo que se traduce a TOM
sb.AppendLine($"Expresión TOM de la medida: {Model.AllMeasures.First(m => m.Name == "Total Revenue").Expression}");
Output(sb.ToString());
```

**Salida:**

```
Importación completada con incidencias.
  [Warning] MEASURE_WINDOW_UNSUPPORTED: La medida 'Total Revenue' usa una especificación de ventana que actualmente no se admite; se ha dejado sin efecto y se ha conservado la definición original como comentario.
Expresión TOM de la medida: // Esta medida usa una especificación de ventana (con ventana / acumulativa / semiadditiva),
// que actualmente no se admite al importar Vistas de métricas de Databricks.
// La medida se ha dejado vacía: revise los detalles siguientes y cree el DAX
// manualmente. La traducción a DAX NO tiene en cuenta la especificación de ventana; muy
// probablemente tendrá que encapsularla en CALCULATE (o algo similar) para aplicar la ventana.
//
// Expresión original de origen (Databricks SQL):
/*
SUM(revenue)
*/
//
// Traducción sugerida a DAX (la especificación de ventana NO se ha aplicado):
/*
SUM('Fact'[revenue])
*/
//
// Especificación de ventana:
/*
- order: order_date
  range: trailing 3 month
  semiadditive: last

*/
```

## Pasos a seguir

- [Importar una Vista de métricas desde un archivo](xref:semantic-bridge-metric-view-import-from-file)
- [Cargar e inspeccionar una vista de métricas](xref:semantic-bridge-load-inspect)
- [Validar una vista de métricas](xref:semantic-bridge-validate-default)

## Ver también

- [Descripción general de Semantic Bridge](xref:semantic-bridge)
