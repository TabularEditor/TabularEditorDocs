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

## Propósito del script

Los scripts crean una tabla de medidas oculta que contiene una columna oculta

## Script

### Crear tabla de medidas

```csharp
// Crear una tabla calculada con una sola columna que estará oculta:
var table = Model.AddCalculatedTable("Medidas del modelo", "{0}");
table.Columns[0].IsHidden = true;
```