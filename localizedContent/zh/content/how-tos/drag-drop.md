---
uid: drag-drop
title: 拖放对象
author: Morten Lønskov
updated: 2026-09-15
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 拖放对象

You reorganise a model in the @tom-explorer-view, the same tree you use to browse it. Pick objects up where you find them, drop them where they belong. There's no separate modelling surface to switch into first, and nothing is out of reach because the view you're in doesn't happen to draw it.

The gesture is always a move. Tabular Editor shows the move cursor when a drop is allowed and the no-drop cursor when it isn't, and there's no modifier key that turns a drag into a copy. To copy an object, use **Duplicate** instead, described in @duplicate-and-batch.

## Reorganising display folders

Drag a display folder and every object underneath it comes along, including nested subfolders, which keep their shape. This is the reason the feature exists: restructuring the folder layout of a large model is one gesture per folder rather than one edit per measure.

<!-- IMAGE NEEDED: drag-drop-display-folders.gif
     An animation of a display folder being dragged onto another folder in the TOM Explorer,
     with the measures and subfolders beneath it following. Needs a model with at least two
     levels of nesting so the shape is visibly preserved.
     Alt text: "A display folder being dragged onto another folder in the TOM Explorer" -->

Everything else in the tree moves the same way:

- Select several objects with **Ctrl+click** or **Shift+click** and drag them together. You can mix measures, columns, hierarchies and folders as long as they're in the same table.
- Drop objects on the **table node** itself to take them out of their folder and back to the top level of the table.
- Drop a folder into a folder to nest it. Tabular Editor refuses a drop into the folder's own subfolder, so you can't lose a branch inside itself.

Each drop is a single **Edit > Undo** step, however many objects it touched.

Display folders are nothing more than a string property on each object, with `\` separating the levels, so `Sales\Ratios` is the _Ratios_ folder inside _Sales_. An object can sit in more than one folder at once by separating the paths with `;`.

## Moving an object to another table

Measures and calculated columns can be dragged to a different table, either onto the table node or straight into one of its display folders. No other object type can cross tables this way.

What comes with the object:

- **Translations** of its name and description.
- **Perspective membership.** By default the object keeps the perspectives it was in. Tick _Inherit table membership when object pasted or moved to table_ under **Tools > Preferences > Tabular Editor** to have it adopt the destination table's membership instead.
- **The KPI**, for a measure that has one.
- **Error and warning indicators.** An expression that was invalid before the move is still marked as invalid afterwards, rather than looking clean until you next edit it.

> [!WARNING]
> Moving a **calculated column** to another table removes the things that depended on it in its old position. Any relationship it takes part in is deleted, any hierarchy level built on it is deleted, it's dropped from calendars and variations, and a _Sort by column_ pointing at it is cleared. You aren't asked to confirm this. **Edit > Undo** puts all of it back as one step, so check the model before you do anything else.

DAX that refers to the column by its old table, such as `'Reseller Sales'[Margin]`, isn't rewritten and keeps pointing at the table the column has left. Measure references are written as `[Measure]` without a table, so they're unaffected. Run @using-bpa or check the @messages-view after a move to catch what broke.

## Building hierarchies and ordering calculation items

- Drag one or more **columns onto a hierarchy** to add them as levels. Drop between two existing levels to choose the position. A column that's already a level of that hierarchy is refused.
- Drag **levels** within a hierarchy to reorder them, or onto another hierarchy in the same table to move them there.
- Drag **calculation items** to reorder them inside their calculation group, or onto another calculation group to move them.

## Grouping tables

In Tabular Editor 3 you can drag one or more tables onto a **table group** to put them in it. Dropping tables onto another table gives them whatever group that table is in, which is also how you take tables out of a group: drop them on a table that isn't in one.

Table groups are a Tabular Editor convenience for organising the tree. They're stored as an annotation and aren't part of the model metadata, so they don't appear in Power BI or Analysis Services.

## Display folders and translations

A drag changes the display folder _for the translation you're currently viewing_ in the TOM Explorer, and only that one.

- With no translation selected, which is the default, the drag writes the untranslated display folder. Translated display folder names are left exactly as they were, so in those cultures the objects stay in the old folder.
- With a culture selected in the TOM Explorer's translation dropdown, the drag writes that culture's translated display folder and leaves the untranslated one alone.

So reorganising folders in the default view doesn't carry the translations with it. Bring them back into line in the @metadata-translation-editor, or run the built-in Best Practice Analyzer rule for objects that have a display folder but no translated display folder, whose fix copies the untranslated value into every culture.

Moving an object to another table is the exception: its own translations are preserved across the move.

## What can be dragged, and where it can go

| Drag                                    | Onto                                            | 结果                            |
| --------------------------------------- | ----------------------------------------------- | ----------------------------- |
| Measures, columns, hierarchies, folders | A display folder in the same table              | Objects move into that folder |
| The same                                | The table node                                  | Objects leave their folder    |
| Measures, calculated columns            | Another table, or a folder in it                | Objects move to that table    |
| 列                                       | A hierarchy or one of its levels                | Columns are added as levels   |
| 级别                                      | The same hierarchy, or another one in the table | Levels are reordered or moved |
| 计算项                                     | Their group, or another calculation group       | Items are reordered or moved  |
| 表                                       | A table group, or another table                 | Tables take on that group     |

Partitions, roles, perspectives, relationships, data sources and shared expressions can't be dragged. Objects deleted since the last save, shown struck through in the tree, can't be dragged either, and can't be used as a drop target. Objects only appear where the tree is set up to show them, so display folders and table groups have to be switched on in the toolbar before you can drop onto them.

## Doing the same from a script

Display folders are a property, so a script sets the string directly. Use `\\` in a regular C# string, or a verbatim string:

```csharp
Selected.Measures.SetDisplayFolder(@"Sales\Ratios");
Model.Tables["Sales"].Measures["Margin %"].DisplayFolder = @"Sales\Ratios";
Model.Tables["Sales"].Measures["Margin %"].TranslatedDisplayFolders["da-DK"] = @"Salg\Nøgletal";
```

A measure moves between tables with `MoveTo`, which keeps its error indicators exactly as the drag does:

```csharp
Model.Tables["Sales"].Measures["Margin %"].MoveTo(Model.Tables["Reseller Sales"]);
```

Calculated columns have no `MoveTo`. Use the same action the tree uses:

```csharp
var column = Model.Tables["Sales"].Columns["Margin"];
column.Handler.Actions.MoveObject(column, Model.Tables["Reseller Sales"], false, null);
```

Table groups are a property too: `Model.Tables["Sales"].TableGroup = "Facts";`. See @csharp-scripts for how to run any of this.

## Dragging elsewhere in the application

The TOM Explorer is the only place a drag changes model structure, but it's the source for several other drops:

- Drag an object into the DAX or C# editor to insert its fully qualified name, rather than typing it. See @dax-editor.
- Drag tables from the tree onto an open model diagram to add them to it. Inside the diagram, drag a column onto a column in another table to create a relationship between them. See @diagram-view.
- Drag columns, measures or hierarchies onto a pivot grid to add them as fields.
