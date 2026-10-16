---
uid: script-display-unique-column-values
title: Valores únicos de la columna
author: Morten Lønskov
updated: 2024-05-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Valores únicos de la columna

## Objetivo del script

Muestra los valores distintos de una columna para perfilar datos rápidamente y acceder a ellos.
Guárdalo como una macro a nivel de columna para tenerlo disponible rápidamente.

<br></br>

## Script

### Título del script

```csharp
// Construct the DAX expression to get all distinct column values, from the selected column:
var dax = string.Format("ALL({0})", Selected.Column.DaxObjectFullName);

// Evaluate the DAX expression against the connected model:
var result = EvaluateDax(dax);

// Output the DataTable containing the result of the DAX expression:
Output(result);
```

### Explicación

El script usa la función DAX ALL() sobre las columnas seleccionadas y muestra el resultado en un cuadro de diálogo de salida.

