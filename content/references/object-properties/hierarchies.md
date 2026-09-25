---
uid: object-properties-hierarchies
title: Hierarchy and level properties
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
# Hierarchy and level properties

<!--
SUMMARY: Reference for the properties of hierarchies and their levels.
-->

This page covers the properties of user-defined hierarchies and of the levels in them. For properties that most objects share, see @object-properties-common.

## Hierarchy

A hierarchy is a named, ordered list of columns from one table that report authors can drill down through, for example `Year` > `Quarter` > `Month` > `Date` or `Category` > `Subcategory` > `Product`. Each step is a level. Hierarchies make it easier to build drill-down visuals and PivotTables, but they don't change how the data is stored or calculated.

All the levels of a hierarchy must come from the table the hierarchy belongs to. To build a hierarchy across tables, first bring the columns into one table, for example with calculated columns that use `RELATED`.

In the TOM Explorer, you add levels to a hierarchy by dragging columns onto it. See @drag-drop.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Display Folder](xref:object-properties-common#display-folder)
- [Hidden](xref:object-properties-common#hidden)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [Error Message](xref:object-properties-common#error-message)
- [Object Type](xref:object-properties-common#object-type)
- [State](xref:object-properties-common#state)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Translated Display Folders](xref:object-properties-common#translated-display-folders)
- [Synonyms](xref:object-properties-common#synonyms)
- [Shown in Perspective](xref:object-properties-common#shown-in-perspective)

### Options

#### Hide Members
`HideMembers` · HierarchyHideMembersType · compatibility level 1400+

Whether client tools hide members with a blank value. Use it for *ragged* hierarchies, where some branches have fewer levels than others. For example, in a geography hierarchy `Country` > `State` > `City`, some countries have no states. Without hiding, the user sees an empty member at the `State` level between the country and its cities.

| Value | Meaning |
|---|---|
| `Default` | Show all members, including blank ones. Use this for a regular, balanced hierarchy. |
| `HideBlankMembers` | Hide a member when its value is blank, so the child members appear directly under the parent. |

For the hiding to work, the missing levels must really be blank, not a placeholder such as `N/A`. Excel respects this property. Power BI doesn't, and shows the blank members anyway.

The Properties view only shows **Hide Members** at compatibility level 1400 or higher.

<!-- TODO (not verifiable from TE3 source): whether the engine treats an empty string as blank (Excel hiding real BLANK() members is confirmed on SSAS 2025). -->

## Level

A level is one step in a hierarchy. Each level points to a column of the hierarchy's table, and has its own name, which can differ from the column's name. For example, a level named `Month` can point to a column named `MonthName`.

### Common properties

- [Name](xref:object-properties-common#name)
- [Description](xref:object-properties-common#description)
- [Annotations](xref:object-properties-common#annotations)
- [Extended Properties](xref:object-properties-common#extended-properties)
- [Changed Properties](xref:object-properties-common#changed-properties)
- [Object Type](xref:object-properties-common#object-type)
- [Lineage Tag](xref:object-properties-common#lineage-tag)
- [Source Lineage Tag](xref:object-properties-common#source-lineage-tag)
- [Translated Names](xref:object-properties-common#translated-names)
- [Translated Descriptions](xref:object-properties-common#translated-descriptions)
- [Synonyms](xref:object-properties-common#synonyms)

Levels don't have their own **Hidden** or **Display Folder**, and they aren't added to perspectives separately: they follow their hierarchy. Level names can be translated, and they should be, if the hierarchy's name is. The Best Practice Analyzer rule @kb.bpa-translate-hierarchy-levels flags levels of visible hierarchies that have no translated name in one or more of the model's cultures.

### Basic

#### Column
`Column` · Column

The column that provides the values of the level. It must be a column of the same table as the hierarchy, and a column can only be used once in the same hierarchy. The level shows the column's values in the column's sort order, so to show months in calendar order, set **Sort By Column** on the month name column (see @object-properties-columns).

You can hide the column itself and still use it in a hierarchy. This is a common way to make users browse the data through the hierarchy instead of through the separate columns.

#### Ordinal
`Ordinal` · int

The position of the level within the hierarchy, starting at `0` for the top level. The ordinals of the levels in a hierarchy must be `0`, `1`, `2` and so on, without gaps or duplicates.

You don't normally set the value by hand. Tabular Editor 3 keeps the ordinals numbered for you:

- When you drag levels into a different order in the TOM Explorer, Tabular Editor renumbers all levels of the hierarchy.
- When you delete a level, Tabular Editor renumbers the remaining levels to close the gap.
- When you type a new **Ordinal** in the Properties view, Tabular Editor moves the level to that position and renumbers the other levels.
- When you add a level, it goes to the bottom of the hierarchy, unless you drop the column between two existing levels.

You can only set **Ordinal** for one level at a time.

Tabular Editor 2 renumbers level ordinals in the same way when you drag levels into a different order and when you delete a level.

You can also drag levels onto another hierarchy in the same table to move them there. See @drag-drop.
