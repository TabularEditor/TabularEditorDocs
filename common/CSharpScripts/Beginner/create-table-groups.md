---
uid: create-table-groups
title: Create Table Groups
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  versions:
    - version: 3.x
---
# Create Table Groups

## Script Purpose
This script creates default table groups within Tabular Editor 3.

## Script

### Script Title
```csharp
// Loop through all tables:
foreach(var table in Model.Tables)
{

    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Calculation Groups";
    }
    else if (table.IsHidden && table.Measures.Any(m => m.IsVisible))
    {
        // Hidden tables containing visible measures:
        table.TableGroup = "Measure Groups";
    }
    else if (table.UsedInRelationships.All(r => r.FromTable == table))
    {
        // Tables exclusively on the "many" side of relationships:
        table.TableGroup = "Facts";
    }
    else if (table.UsedInRelationships.Any(r => r.ToTable == table))
    {
        // Tables on the "one" side of relationships:
        table.TableGroup = "Dimensions";
    }
    else if (!table.UsedInRelationships.Any())
    {
        // Tables without any relationships:

        table.TableGroup = "Parameter Tables";
    }
    else
    {
        // All other tables:
        table.TableGroup = "Misc";
    }
}
```
### Explanation
The scripts loops through all tables in the model assigning a table group according to specific properties. 

