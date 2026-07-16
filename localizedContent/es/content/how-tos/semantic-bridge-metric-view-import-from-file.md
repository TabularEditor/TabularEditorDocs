---
uid: semantic-bridge-metric-view-import-from-file
title: Importar una vista de métricas desde un archivo
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

# Importar una vista de métricas desde un archivo

Esta guía práctica muestra cómo importar una vista de métricas en un modelo tabular directamente desde un archivo YAML.

> [!NOTE]
> Estas guías están dirigidas a Tabular Editor 3.26.2 y versiones posteriores.
> Las versiones anteriores no admiten las características de la vista de métricas v1.1 que se muestran aquí.

## Obtener la vista de métricas de ejemplo

Guarda la vista de métricas de ejemplo (más abajo) en un archivo local.
Tendrás que sustituir el marcador de posición del ejemplo siguiente por esta ruta.
En esta guía práctica en concreto, solo tienes que guardar el archivo; no hace falta ejecutar `Load` ni `Deserialize`.

[!INCLUDE [sample](includes/sample-metricview.md)]

## Importar desde archivo

`ImportToTabularFromFile` carga el YAML desde el disco y lo importa al modelo abierto en un solo paso.
Sustituye el marcador de posición del script siguiente (`<PLACEHOLDER>`) por la ruta donde guardaste el YAML.
El nombre de host de Databricks y la ruta HTTP se usan para crear las expresiones M de las particiones; para una prueba rápida, puedes pasar valores provisionales y corregirlos antes de actualizar los datos.

```csharp {compile}
var success = SemanticBridge.MetricView.ImportToTabularFromFile(
    "<PLACEHOLDER>",
    Model,
    "your-workspace.azuredatabricks.net",
    "/sql/1.0/warehouses/abc123def456",
    out var diagnostics
);

var sb = new System.Text.StringBuilder();
sb.AppendLine(success ? "Import successful!" : "Import failed.");
sb.AppendLine($"Diagnostics: {diagnostics.Count}");
Output(sb.ToString());
```

## Pasos a seguir

- [Cargar e inspeccionar una vista de métricas](xref:semantic-bridge-load-inspect)
- [Importar una vista de métricas y ver los diagnósticos](xref:semantic-bridge-import)

## Ver también

- [Información general de Semantic Bridge](xref:semantic-bridge)
