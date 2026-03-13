---
uid: script-show-data-source-dependencies
title: Mostrar las dependencias del origen de datos
author: David Bojsen
updated: 2023-09-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Mostrar las dependencias del origen de datos

## Propósito del script

El script devuelve las tablas que hacen referencia al origen de datos explícito (heredado) seleccionado. Esto facilita determinar dónde se utiliza el origen de datos seleccionado.

## Secuencia de comandos

### Mostrar las dependencias del origen de datos

```csharp
//El script devuelve las tablas que hacen referencia al origen de datos explícito (heredado) seleccionado.
if (Model.DataSources.Count == 0)
{
    Info("Este modelo no contiene ningún origen de datos; está vacío o usa orígenes de datos implícitos");
    return;
}
// Comprueba que se haya seleccionado un origen de datos
DataSource selectedDatasource = null;

if (Selected.DataSources.Count == 1)
    selectedDatasource = Selected.DataSource;
else
    selectedDatasource = SelectObject<DataSource>(Model.DataSources, null, "Selecciona el origen de datos del que quieres ver las dependencias");

// Orígenes heredados
var legacyTables = Model.Tables.Where(t => t.Source == selectedDatasource.Name).ToList();

// Orígenes M
var mTables = Model.Tables.Where(t => t.Partitions.Any(p => p.Expression.Contains($"= #\"{selectedDatasource.Name}\","))).ToList();

// unir listas
var allTables = legacyTables.Union(mTables).OrderBy(t => t.Name);

// Mostrar el resultado
var tableString = string.Join("\r\n", allTables.Select(t => t.Name));
Info($"El origen de datos {selectedDatasource.Name} se usa en las siguientes tablas:\r\n" + tableString);
```

### Explicación

Este fragmento toma el origen de datos seleccionado y recorre el modelo para recopilar las particiones en las que se utiliza ese origen de datos.

## Salida de ejemplo

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-show-data-source-dependencies-output.png" alt="Example of the dialog pop-up that informs the user which tables use the selected data source" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figura 1:</strong> Ejemplo del cuadro de diálogo emergente que informa al usuario de qué tablas utilizan el origen de datos seleccionado.</figcaption>
</figure>