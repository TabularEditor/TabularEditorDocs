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

## Objetivo del script

Este script crea grupos de tablas predeterminados en Tabular Editor 3.

## Script

### Título del script

```csharp
// Loop through all tables:
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Calculation Groups";
    }
    else if (!table.UsedInRelationships.Any() && table.Measures.Any(m => m.IsVisible))
    {
        // Tables containing visible measures, but no relationships to other tables
        table.TableGroup = "Measure Groups";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table) && table.UsedInRelationships.Any())
    {
        // Tables exclusively on the "many" side of relationships:
        table.TableGroup = "Facts";
    }
    else if (!table.UsedInRelationships.Any() && table is CalculatedTable && !table.Measures.Any())
    {
        // Tables without any relationships, that are Calculated Tables and do not have measures:
        table.TableGroup = "Parameter Tables";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // Tables on the "one" side of relationships:
        table.TableGroup = "Dimensions";
    }
    else
    {
        // All other tables:
        table.TableGroup = "Misc";
    }
}
```

### Explicación

El script recorre todas las tablas del modelo y asigna un grupo de tablas en función de determinadas propiedades.

