---
uid: object-properties-hierarchies
title: Hierarchy and level properties
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
# Hierarchy and level properties

<!--
SUMMARY: Reference for the properties of hierarchies and their levels.
-->

This page covers the properties of user-defined hierarchies and of the levels in them. For properties that most objects share, see @object-properties-common.

## Hierarchy

A hierarchy is a named, ordered list of columns from one table that report authors drill down through in visuals and PivotTables, for example `Year` > `Quarter` > `Month` > `Date` or `Category` > `Subcategory` > `Product`. Each step is a level. Hierarchies don't change how the data is stored or calculated.

All the levels of a hierarchy must come from the table the hierarchy belongs to. To build a hierarchy across tables, first bring the columns into one table, for example with calculated columns that use [RELATED](https://dax.guide/related).

In the **TOM Explorer**, you add levels to a hierarchy by dragging columns onto it. See @drag-drop.

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

### Hide Members
`HideMembers` · HierarchyHideMembersType · Options · compatibility level 1400+

Whether client tools hide members with a blank value. Use it for *ragged* hierarchies, where some branches have fewer levels than others. In a geography hierarchy `Country` > `State` > `City`, for example, some countries have no states, and with `Default` the user sees an empty member at the `State` level between the country and its cities. The **Properties** view shows `HideMembers` at compatibility level 1400 or higher.

| Value | Meaning |
|---|---|
| `Default` | Shows all members, including blank ones. Use it for a balanced hierarchy. |
| `HideBlankMembers` | Hides a member when its value is blank, and its child members appear directly under the parent. |

Only blank members are hidden, and a placeholder value such as `N/A` still appears. Excel respects this property. Power BI ignores it and shows the blank members.

<!-- TODO (not verifiable from TE3 source): whether the engine treats an empty string as blank (Excel hiding real BLANK() members is confirmed on SSAS 2025). -->

## Level

A level is one step in a hierarchy. Each level points to a column of the hierarchy's table and has its own name, which can differ from the column's name. For example, a level named `Month` can point to a column named `MonthName`.

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

Levels have no `IsHidden` or `DisplayFolder` of their own and follow their hierarchy in perspectives. If you translate the hierarchy's name, translate its level names too. The Best Practice Analyzer (BPA) rule @kb.bpa-translate-hierarchy-levels flags levels of visible hierarchies that have no translated name in one or more of the model's cultures.

### Column
`Column` · Column · Basic

The column that provides the values of the level. It must be a column of the same table as the hierarchy, and a column can be used once in the same hierarchy. The level shows the column's values in the column's sort order. To show months in calendar order, set `SortByColumn` on the month name column (see @object-properties-columns).

A hidden column still works in a hierarchy. Hide the level columns to have users browse the data through the hierarchy.

### Ordinal
`Ordinal` · int · Basic

The position of the level within the hierarchy, starting at `0` for the top level. The ordinals of the levels in a hierarchy must be `0`, `1`, `2` and so on, without gaps or duplicates.

Tabular Editor 3 keeps the ordinals numbered:

- when you drag levels into a different order in the **TOM Explorer**, Tabular Editor renumbers all levels of the hierarchy
- when you delete a level, Tabular Editor renumbers the remaining levels to close the gap
- when you type a new `Ordinal` in the **Properties** view, Tabular Editor moves the level to that position and renumbers the other levels
- when you add a level, it goes to the bottom of the hierarchy, unless you drop the column between two existing levels

You can set `Ordinal` for one level at a time. Tabular Editor 2 renumbers level ordinals in the same way when you drag levels into a different order and when you delete a level.

You can also drag levels onto another hierarchy in the same table to move them there. See @drag-drop.
