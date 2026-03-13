---
uid: script-create-table-groups
title: Crear grupos de tablas
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      full: true
---

# Crear grupos de tablas

## Propósito del script

Este script crea grupos de tablas predeterminados en Tabular Editor 3.

## Secuencia de comandos

### Título del script

```csharp
// Recorrer todas las tablas:
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Calculation Groups";
    }
    else if (!table.UsedInRelationships.Any() && table.Measures.Any(m => m.IsVisible))
    {
        // Tablas que contienen medidas visibles, pero sin relaciones con otras tablas
        table.TableGroup = "Measure Groups";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // Tablas exclusivamente en el lado "muchos" de las relaciones:
        table.TableGroup = "Facts";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // Tablas sin ninguna relación, que son tablas calculadas y no tienen medidas:
        table.TableGroup = "Parameter Tables";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // Tablas en el lado "uno" de las relaciones:
        table.TableGroup = "Dimensions";
    }
    else
    {
        // Todas las demás tablas:
        table.TableGroup = "Misc";
    }
}
```

### Explicación

El script recorre todas las tablas del modelo y asigna un grupo de tablas en función de determinadas propiedades.

