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

## Propósito del script

Muestra los valores distintos de una columna para perfilar datos rápidamente y acceder a ellos.
Guárdalo como una macro a nivel de columna para tenerlo disponible rápidamente.

<br></br>

## Script

### Título del script

```csharp
// Construye la expresión DAX para obtener todos los valores distintos de la columna, a partir de la columna seleccionada:
var dax = string.Format("ALL({0})", Selected.Column.DaxObjectFullName);

// Evalúa la expresión DAX contra el modelo conectado:
var result = EvaluateDax(dax);

// Muestra el DataTable que contiene el resultado de la expresión DAX:
Output(result);
```

### Explicación

El script usa la función DAX ALL() sobre las columnas seleccionadas y muestra el resultado en un cuadro de diálogo de salida.

