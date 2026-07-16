---
uid: semantic-bridge-metric-view-handle-failures
title: Solucionar errores comunes
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

# Solucionar errores comunes

Este procedimiento muestra cómo gestionar varios modos de fallo habituales al trabajar con Metric Views en C# Script:
YAML no válido, archivos ausentes, operaciones sin ningún Metric View cargado y una importación que no finaliza.

> [!NOTE]
> Estas guías están orientadas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de Metric View v1.1 que se muestran aquí.

## Fallo al cargar o deserializar

`Load` y `Deserialize` generan `System.IO.InvalidDataException` cuando la entrada no representa un YAML de Metric View válido.
La excepción en sí solo indica que la carga falló;
los motivos concretos se recogen en `ImportDiagnostics`.
Si se produce un error, el Metric View actual (`SemanticBridge.MetricView.Model`) se establece en `null`.

```csharp {run id=failed-deserialize setup=none after=none output=true}
try
{
    // This Metric View is missing the required `source`, so it fails to deserialize.
    SemanticBridge.MetricView.Deserialize("""
        version: 1.1
        fields:
          - name: revenue
            expr: source.revenue
        """);
}
catch (System.IO.InvalidDataException)
{
    var sb = new System.Text.StringBuilder();
    sb.AppendLine("Could not load the Metric View:");
    foreach (var diag in SemanticBridge.MetricView.ImportDiagnostics)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
    }
    Output(sb.ToString());
}
```

**Salida**

```
Could not load the Metric View:
  [Error] VIEW_SOURCE_REQUIRED: View source cannot be empty
```

> [!NOTE]
> `Load` lee desde una ruta de archivo, por lo que una ruta que no existe genera `System.IO.FileNotFoundException` en lugar de `InvalidDataException`.
> Captura esa excepción (o una `System.Exception` más general) al cargar desde una ruta.

## Evita operar sin un Metric View cargado

`Validate`, `Serialize`, `Save` e `ImportToTabular` generan `System.InvalidOperationException` si no hay ningún Metric View cargado.
`Model` es `null` cuando no hay nada cargado, por lo que conviene comprobarlo antes.

Ejecuta este script en una instancia nueva de Tabular Editor 3 para asegurarte de que no haya ningún Metric View cargado:

```csharp {run id=guard-no-model setup=none after=none output=true}
if (SemanticBridge.MetricView.Model == null)
{
    Output("No Metric View is loaded. Load or deserialize one first.");
}
else
{
    var diagnostics = SemanticBridge.MetricView.Validate();
    Output($"Found {diagnostics.Count()} issue(s).");
}
```

**Salida**

```
No Metric View is loaded. Load or deserialize one first.
```

Sin esta comprobación, llamar a `SemanticBridge.MetricView.Validate()` sin nada cargado genera `InvalidOperationException`.

## Una importación que no se completa

`ImportToTabular` y `ImportToTabularFromFile` devuelven `false` cuando la importación no puede completarse, en lugar de generar una excepción.
Comprueba el valor devuelto y lee los diagnósticos de `out` para ver por qué.

El ejemplo siguiente deserializa una vista de métricas válida,
y luego deja en blanco la expresión de un campo, lo que genera un error de validación.
Como `failOnValidationErrors` está configurado de forma predeterminada en `true`,
la importación se detiene antes de traducir y devuelve `false`,
con los motivos en los diagnósticos de `out`.
Debe haber un modelo tabular abierto.

```csharp {run id=import-incomplete setup=none after=none output=true}
// Load a valid Metric View, then make it invalid
SemanticBridge.MetricView.Deserialize("""
    version: 1.1
    source: sales.fact.orders
    fields:
      - name: order_year
        expr: source.order_year
    measures:
      - name: total_revenue
        expr: SUM(source.revenue)
    """);

var view = SemanticBridge.MetricView.Model;
view.Fields["order_year"].Expr = ""; // an empty expression is invalid

var success = SemanticBridge.MetricView.ImportToTabular(
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
if (success)
{
    sb.AppendLine("Import complete.");
}
else
{
    sb.AppendLine("Import did not complete:");
    foreach (var diag in diagnostics)
    {
        sb.AppendLine($"  [{diag.Severity}] {diag.Code}: {diag.Message}");
    }
}
Output(sb.ToString());
```

**Salida**

```
Import did not complete:
  [Error] FIELD_EXPR_REQUIRED: Field 'order_year' expr cannot be empty
```

Use `failOnValidationErrors: false` bajo su propia responsabilidad si desea importar a pesar de los problemas de validación.
Si no hay ninguna vista de métricas cargada al llamar a este método,
se lanza `InvalidOperationException`, como se describe arriba.

## Pasos a seguir

- [Cargar e inspeccionar una vista de métricas](xref:semantic-bridge-load-inspect)
- [Validar una vista de métricas](xref:semantic-bridge-validate-default)
- [Importar una vista de métricas y ver los diagnósticos](xref:semantic-bridge-import)

## Ver también

- [Información general de Semantic Bridge](xref:semantic-bridge)
