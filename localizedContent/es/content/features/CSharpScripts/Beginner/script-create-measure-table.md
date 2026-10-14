---
uid: script-create-measure-table
title: Crear tabla de medidas
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Crear tabla de medidas

## Objetivo del script

Los scripts crean una tabla de medidas oculta que contiene una columna oculta

## Script

### Crear tabla de medidas

```csharp
// Create a calculated table with a single column which is hidden:
var table = Model.AddCalculatedTable("Model Measures", "{0}");
table.Columns[0].IsHidden = true;
```