---
uid: object-properties
title: Object properties reference
author: Jeroen ter Heerdt
updated: 2026-10-05
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

Every object in a semantic model, such as a table, a column or a measure, has a set of properties. These properties come from the Tabular Object Model (TOM), the object model that Analysis Services, Power BI and Fabric use to define semantic models. The @properties-view shows them, and C# scripts read and write them through the @api-index.

This reference describes each property that the Properties view shows. When Tabular Editor has a feature for a property, such as an editor, a Best Practice Analyzer (BPA) rule or a C# script, the entry links to it.

To change a property, select one or more objects in the @tom-explorer-view and edit the value in the Properties view. When you select several objects, the new value applies to all of them. See @editing-properties.

## How this reference is organized

@object-properties-common describes the properties that most objects have, such as `Name`, `Description` and `Annotations`. Each of the other pages covers one family of related objects:

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

Each page has a section per object. The section starts with links to the common properties of the object, followed by one entry per property. Within each object, the properties are listed by category, in the order the Properties view shows them when **Categorized** is selected. The categories are:

- **Basic**: the properties you change most often, such as the name, the description and the format string.
- **Metadata**: information about the object, such as the object type or the error message. Most of these properties are read-only.
- **Options**: properties that change how the object behaves, such as expressions, summarization or sort order.
- **Translations, Perspectives, Security**: per-culture translations, perspective membership and per-role security settings.

Some objects have other categories, such as **Data Access Options** on the model.

The heading of each entry is the property's name as shown in the Properties view. The line under the heading gives the property's TOM name, its type and its category:

> **Display name**
> `TomName` · type · Category

The TOM name is the name you use in a C# script. For a few properties, the Tabular Model Definition Language (TMDL) uses another name, for example TMDL saves a measure's `FormatStringExpression` as `formatStringDefinition`.

When they apply, these parts follow the category, in this order:

- **read-only**: you can't change the value.
- **compatibility level NNNN+**: the minimum compatibility level of the model, for example `compatibility level 1540+`.
- a marker for a property that Tabular Editor adds. See [Properties that Tabular Editor adds](#properties-that-tabular-editor-adds).

For example, the entry for Lineage Tag starts with:

> **Lineage Tag**
> `LineageTag` · string · Options · compatibility level 1540+

## Properties that depend on the model

The Properties view hides the properties that don't apply to the current model. Which properties appear depends on:

- the compatibility level of the model. Many properties need a minimum level, for example `LineageTag` needs 1540 or higher. To see or change the compatibility level, select the model and expand `Database` in the Properties view.
- the compatibility mode of the model. Some properties exist only for Power BI and Fabric models, or only for Analysis Services models.
- the state of the object. Some properties appear only when another property has a certain value. For example, the properties of a refresh policy appear only when the table has one.

## Properties that Tabular Editor adds

Almost every property in the Properties view is a TOM property, which is saved in the model and visible to every tool that reads the model. Tabular Editor adds a few properties of its own. The meta line marks them as follows:

| Marker | Meaning | Saved in the model? |
|---|---|---|
| *computed* | Tabular Editor calculates the value for display, for example `DaxObjectFullName` or `ObjectTypeName`. | No |
| *shortcut to …* | Shows or edits a TOM property of another object. For example, `SourceType` on a table shows the source type of the table's first partition. | Yes, as the TOM property it points to |
| *stored as an annotation* | Tabular Editor saves the value in an annotation on the object, for example `TableGroup`. | Yes, as an annotation that only Tabular Editor reads |

## See also

- @properties-view
- @tom-explorer-view
- @editing-properties
- @best-practice-analyzer
- @csharp-scripts
- @api-index
