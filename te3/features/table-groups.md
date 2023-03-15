---
uid: table-groups
title: Table Groups
author: Daniel Otykier
updated: 2023-03-08
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# Table Groups

Table Groups is a new feature, available in Tabular Editor 3 starting from [version 3.5.0](xref:release-3-5-0). The feature lets you quickly organise tables into folders, making it easier than ever to manage and navigate large, complex models, in Tabular Editor 3's [TOM Explorer](xref:tom-explorer-view).

![Table groups](~/images/user-interface/table-groups.png)

You can set up Table Groups either by right-clicking on a table and choosing the **Create > Table group** menu option, or by specifying a name for the Table Group in the **Properties View**, while selecting one or more tables.

Tables can be moved around between Table Groups by dragging and dropping in the TOM Explorer. Note that, unlike Display Folders for measures, columns and hierarchies, Table Groups cannot be nested.

Right-clicking on a Table Group in the TOM Explorer, gives you the same context menu options, as if you had selected the table(s) within that Table Group.

> [!NOTE]
> Table Groups is a Tabular Editor-exclusive feature. Client tools (such as Excel, Power BI Desktop, etc.) will not observe Table Groups, as the [CSDL format](https://learn.microsoft.com/en-us/ef/ef6/modeling/designer/advanced/edmx/csdl-spec), which specifies the conceptual schema of the data model, does not support Table Groups.

## Metadata and scripting

Tabular Editor uses an annotation on each table, to specify which Table Group that table belongs to. The name of the annotation is `TabularEditor_TableGroup`. However, when scripting changes to the model using C# scripts, you can modify the Table Group directly through the new `Table.TableGroup` (string) property.

Below is an example of a C# script, that loops through all tables of a model, organizing them into Table Groups based on their type and usage:

```csharp
// Loop through all tables:
foreach(var table in Model.Tables)
{
    if (table is CalculationGroupTable)
    {
        table.TableGroup = "Calculation Groups";
    }
    else if (!table.UsedInRelationships.Any())
    {
        // Tables without any relationships:
        table.TableGroup = "Parameter Tables";
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
    else
    {
        // All other tables:
        table.TableGroup = "Misc";
    }
}
```