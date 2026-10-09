---
uid: drag-drop
title: Drag and drop objects
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# Drag and drop objects

Drag and drop in the @tom-explorer-view moves objects between display folders, tables, hierarchies, calculation groups and table groups. A drag always moves an object, and no modifier key turns it into a copy. While you drag, the move cursor shows where a drop is allowed and the no-drop cursor shows where it isn't. **Duplicate**, described in @duplicate-and-batch, copies an object.

## Move display folders

Drag a display folder onto another folder to move it. Every object and subfolder in it moves with it, and the subfolder structure is kept.

<!-- IMAGE NEEDED: drag-drop-display-folders.gif
     An animation of a display folder being dragged onto another folder in the TOM Explorer,
     with the measures and subfolders beneath it following. Needs a model with at least two
     levels of nesting so the shape is visibly preserved.
     Alt text: "A display folder being dragged onto another folder in the TOM Explorer" -->

You can also:

- Select several objects with **Ctrl+click** or **Shift+click** and drag them together. You can mix measures, columns, hierarchies and folders if they're in the same table.
- Drop objects on the table node to move them out of their folder to the top level of the table.
- Drop a folder onto another folder to nest it. You can't drop a folder into one of its own subfolders.

Each drop is one undo step (**Ctrl+Z**), however many objects it moves.

A display folder is a string property on each object, with `\` separating the levels: `Sales\Ratios` is the Ratios folder inside Sales. To show an object in more than one folder, separate the paths with `;`.

## Move an object to another table

Drag measures and calculated columns onto another table or, in Tabular Editor 3, onto a display folder in that table to move them there, which isn't possible for other object types.

In Tabular Editor 3, the move keeps the object's:

- translations of its name and description
- perspective membership, unless you select **Inherit table membership when an object is pasted/moved to a table** under **Tools > Preferences > Tabular Editor > Modeling Operations**, which gives the object the destination table's perspective membership
- KPI, for a measure that has one
- error and warning indicators, so an invalid expression stays marked as invalid after the move

> [!WARNING]
> When you move a calculated column to another table, no confirmation appears, and the following are changed:
>
> - relationships that use the column are deleted
> - hierarchy levels based on the column are deleted
> - the column is removed from calendars and variations
> - `SortByColumn` references to the column are cleared
>
> Press **Ctrl+Z** to undo the move and all of these changes in one step.

DAX that refers to the column by its old table, such as `'Reseller Sales'[Margin]`, isn't rewritten and returns an error. Measure references are written as `[Measure]` without a table and aren't affected. After a move, run the [Best Practice Analyzer](xref:using-bpa) or check the @messages-view to find the broken references.

## Build hierarchies and order calculation items

- Drag one or more columns onto a hierarchy to add them as levels. Drop between two existing levels to choose the position. You can't add a column that's already a level of that hierarchy.
- Drag levels within a hierarchy to reorder them, or onto another hierarchy in the same table to move them there.
- Drag calculation items to reorder them in their calculation group, or onto another calculation group to move them.

## Group tables

> [!NOTE]
> Table groups are available in Tabular Editor 3 only.

Drag one or more tables onto a table group to move them into it, or onto another table to move them into that table's group. Dropping tables onto a table that isn't in a group removes them from their group. Table groups organize the TOM Explorer and are stored as an annotation, which Power BI and Analysis Services ignore.

## Display folders and translations

A drag changes the display folder only for the translation selected in the TOM Explorer:

- With no translation selected (the default), the drag changes the untranslated display folder. Translated display folders aren't changed, so translated views still show the objects in the old folder.
- With a culture selected in the TOM Explorer's translation dropdown, the drag changes that culture's translated display folder and leaves the untranslated display folder unchanged.

Update the translations in the @metadata-translation-editor, or with the fix of the [Translate display folders for all cultures](xref:kb.bpa-translate-display-folders) Best Practice Analyzer rule, which copies the untranslated value into every culture.

## What can be dragged, and where it can go

| Drag | Onto | Result |
|---|---|---|
| Measures, columns, hierarchies, folders | A display folder in the same table | Objects move into that folder |
| Measures, columns, hierarchies, folders | The table node | Objects leave their folder |
| Measures, calculated columns | Another table, or a folder in it (folder: Tabular Editor 3 only) | Objects move to that table |
| Columns | A hierarchy or one of its levels | Columns are added as levels |
| Levels | The same hierarchy, or another one in the table | Levels are reordered or moved |
| Calculation items | Their group, or another calculation group | Items are reordered or moved |
| Tables (Tabular Editor 3 only) | A table group, or another table | Tables move to that group |

The following limits apply:

- Partitions, roles, perspectives, relationships, data sources and shared expressions can't be dragged.
- In Tabular Editor 3.27.0 and later, objects deleted since the last save are shown struck through in the tree, and you can't drag them or drop onto them.
- Display folders and table groups accept drops only while they're switched on in the TOM Explorer toolbar.

## Make the same changes from a script

A script moves objects between display folders by setting the `DisplayFolder` string. Use `\\` in a regular C# string, or a verbatim string:

```csharp
Selected.Measures.SetDisplayFolder(@"Sales\Ratios");
Model.Tables["Sales"].Measures["Margin %"].DisplayFolder = @"Sales\Ratios";
Model.Tables["Sales"].Measures["Margin %"].TranslatedDisplayFolders["da-DK"] = @"Salg\Nøgletal";
```

`MoveTo` moves a measure to another table and keeps its error indicators:

```csharp
Model.Tables["Sales"].Measures["Margin %"].MoveTo(Model.Tables["Reseller Sales"]);
```

The scripting API has no method to move a calculated column to another table. In Tabular Editor 3, setting `TableGroup` moves a table to a table group: `Model.Tables["Sales"].TableGroup = "Facts";`, in a script you run as described in @csharp-scripts.

## Drag to other views

You can also drag objects from the TOM Explorer to:

- the DAX or C# editor, to insert the object's fully qualified name. See @dax-editor.
- an open model diagram, to add tables to it. In the diagram, drag a column onto a column in another table to create a relationship. See @diagram-view.
- a [pivot grid](xref:pivot-grid), to add columns, measures or hierarchies as fields.

The model diagram and pivot grid are available in Tabular Editor 3 only.
