---
uid: object-properties
title: Object properties reference
author: Jeroen ter Heerdt
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Object properties reference

<!--
SUMMARY: Reference for every property that Tabular Editor shows in the Properties view, grouped by object type.
-->

Every object in a semantic model, such as a table, a column or a measure, is described by a set of properties. These properties come from the Tabular Object Model (TOM), the object model that Analysis Services, Power BI and Fabric use to define semantic models. Tabular Editor shows them in the @properties-view, and C# scripts read and write them through the @api-index.

This reference covers every property that the Properties view shows, what it does, and when you would change it. Where Tabular Editor has a feature that helps you work with a property, such as an editor, a Best Practice Analyzer rule or a C# script, the property links to it.

To change a property, select one or more objects in the @tom-explorer-view and edit the value in the Properties view. When you select several objects, you can change a property for all of them at once. See @editing-properties.

## How this reference is organized

Properties that almost every object has, such as **Name**, **Description** and **Annotations**, are described once on @object-properties-common. The other pages cover one family of related objects each:

| Page | Objects |
|---|---|
| @object-properties-common | Properties shared by most objects |
| @object-properties-model | Model |
| @object-properties-tables | Table, calculated table, calculation group table |
| @object-properties-columns | Data column, calculated column, calculated table column, alternate of, variation |
| @object-properties-measures | Measure, KPI |
| @object-properties-calculation-groups | Calculation group, calculation item |
| @object-properties-hierarchies | Hierarchy, level |
| @object-properties-relationships | Relationship |
| @object-properties-partitions | Partition, M partition, entity partition, policy range partition, refresh policy, data coverage definition |
| @object-properties-data-sources | Provider and structured data sources, shared expression, query group, data binding hint |
| @object-properties-security | Role, table permission, role members |
| @object-properties-perspectives-cultures | Perspective, culture |
| @object-properties-calendars | Calendar, time-related column group, time unit column association |
| @object-properties-functions | User-defined function, set |

On each page, properties are grouped by the category they appear under in the Properties view when **Categorized** is selected:

- **Basic**: the properties you change most often, such as name, description and format string.
- **Metadata**: information about the object. Most of these are read-only, such as the object type or the error message.
- **Options**: properties that change how the object behaves, such as expressions, summarization or sort order.
- **Translations, Perspectives, Security**: per-culture translations, perspective membership and per-role security settings.

Each property lists its name as shown in the Properties view, its name in TOM (the name you use in a C# script), and its type:

> **Display name**
> `TomName` · type

When the display name and the TOM name are the same, only the TOM name is shown. The TOM name is the one Tabular Editor's scripting API uses. For a few properties, the underlying TOM object is nested differently, for example a measure's **Format String Expression** is saved as `formatStringDefinition` in TMDL.

## Properties that depend on the model

The Properties view hides properties that don't apply to the current model. What you see depends on:

- **Compatibility level.** Many properties need a minimum compatibility level of the model, for example **Lineage Tag** needs 1540 or higher. This reference lists the minimum level where one applies. To see or change the compatibility level, select the model and look at **Compatibility Level** under the **Database** property.
- **Compatibility mode.** Some properties exist only for Power BI and Fabric models, or only for Analysis Services models.
- **Object state.** Some properties only appear when another property has a certain value. For example, the properties of a refresh policy only appear when the table has one.

## Properties that Tabular Editor adds

Almost every property in the Properties view is a TOM property, saved in the model and visible to every tool that reads it. A few properties are added by Tabular Editor to make the model easier to work with. These properties are marked with:

| Marker | Meaning | Saved in the model? |
|---|---|---|
| *computed* | Tabular Editor works the value out for display, for example **DAX identifier** or **Object Type**. | No |
| *shortcut to …* | Shows or edits a TOM property that belongs to another object, so you don't have to select that object first. For example, **Source Type** on a table shows the source type of the table's first partition. | Yes, as the TOM property it points to |
| *stored as an annotation* | Tabular Editor saves the value in an annotation on the object, for example **Table Group**. | Yes, but only Tabular Editor uses it |

## See also

- @properties-view
- @tom-explorer-view
- @editing-properties
- @best-practice-analyzer
- @csharp-scripts
- @api-index
