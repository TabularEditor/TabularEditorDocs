---
uid: tmdl-per-object-serialization
title: Per-object TMDL serialization
author: Morten Lønskov
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.28.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "Opens per-object folders and saves them in the standard layout"
        - edition: Enterprise
          full: true
---
# Per-object TMDL serialization

Per-object TMDL serialization saves each column, measure, partition and hierarchy of a table, and each function, shared expression, data source and relationship of the model, to its own `.tmdl` file. A [Tabular Model Definition Language (TMDL)](xref:tmdl) folder in the standard layout keeps each table with all its objects in one file, and writes all functions to `functions.tmdl`, all shared expressions to `expressions.tmdl`, all data sources to `dataSources.tmdl` and all relationships to `relationships.tmdl`. With per-object files, a change to one measure shows in source control as a change to one file, and two developers who edit different measures of the same table edit different files.

Calculation items always stay in their table's file.

## Folder layout

The table's own file stays in the `tables` folder and keeps the table's properties, description, annotations, refresh policy and calculation items. The table objects you split out go in a folder named after the table, with one subfolder per object type. Functions, shared expressions, data sources and relationships go in one folder per type at the root of the TMDL folder:

```text
definition/
├── model.tmdl
├── expressions/
│   ├── Database.tmdl
│   └── Server.tmdl
├── functions/
│   └── Sales.MarginPct.tmdl
├── relationships/
│   └── 3a5c9e1d-7b2f-4c8a-9d6e-1f0b2a4c6e8d.tmdl
└── tables/
    ├── Sales.tmdl
    └── Sales/
        ├── columns/
        │   ├── Amount.tmdl
        │   └── Order Date.tmdl
        ├── measures/
        │   └── Total Amount.tmdl
        └── partitions/
            └── Sales.tmdl
```

A table or model with no objects of a type gets no folder for that type. Each table object file starts with a `ref table` line that binds the object to its table:

```tmdl
ref table Sales

	measure 'Total Amount' = SUM(Sales[Amount])
		formatString: #,0.00
```

The folder is standard TMDL. Power BI Desktop, Tabular Editor 2.26 or later and Tabular Editor 3.19 or later read it the same way they read a folder in the standard layout.

> [!WARNING]
> Don't open a per-object folder in Tabular Editor 3 earlier than 3.19 or Tabular Editor 2 earlier than 2.26. If the folder was saved with **Include metadata order** checked, those versions load shared expressions with empty text and fail to load a folder with per-object data source files. If you save the model from such a version, the shared expressions are saved without their text.

## Save a model with per-object files

1. Open **Tools &gt; Preferences &gt; File Formats &gt; Save-to-folder &gt; TMDL Serialization**.
2. Check **Save objects to separate files**.
3. In the tree below it, check the object types that get their own files.
4. Click **OK**.
5. Select **File &gt; Save to Folder** and choose a folder. If the folder dialog shows **Use serialization settings from annotations**, uncheck it.

**File &gt; Save to Folder** writes TMDL when **Save to Folder format** under **Tools &gt; Preferences &gt; File Formats &gt; Save-to-folder** is **TMDL**, the default.

![The TMDL Serialization preferences page with Save objects to separate files checked](~/content/assets/images/pref-tmdl-serialization.png)

For the model you have open, select **Model &gt; Serialization options...**, check **Save objects to separate files** and click **OK**. The next **Ctrl+S** writes the per-object layout.

Tabular Editor stores the choice in the `TabularEditor_SerializeOptions` annotation in `model.tmdl` as `"TmdlApplySerializationDepth": true`, together with the checked object types. **File &gt; Save** (**Ctrl+S**) reads the annotation and keeps the layout, regardless of your preferences. For more on the annotation, see [Serialization model annotation](xref:save-to-folder#serialization-model-annotation).

> [!NOTE]
> **Save objects to separate files** is off by default. A TMDL folder saved by Power BI Desktop or by an earlier version of Tabular Editor has no `TmdlApplySerializationDepth` in its annotation, and **Ctrl+S** keeps it in the standard layout.

### Object types

Each checked row in the tree moves one object type into its own files:


| Row                               | Folder                       | Note                                                        |
| --------------------------------- | ---------------------------- | ----------------------------------------------------------- |
| **Data Sources**                  | `dataSources`                |                                                             |
| **User Defined Functions (UDFs)** | `functions`                  |                                                             |
| **Shared Expressions**            | `expressions`                |                                                             |
| **Relationships**                 | `relationships`              |                                                             |
| **Tables &gt; Columns**           | `tables/<table>/columns`     | Checking or unchecking it does the same to **Hierarchies**. |
| **Tables &gt; Hierarchies**       | `tables/<table>/hierarchies` | Checking or unchecking it does the same to **Columns**.     |
| **Tables &gt; Measures**          | `tables/<table>/measures`    |                                                             |
| **Tables &gt; Partitions**        | `tables/<table>/partitions`  |                                                             |


**Tables**, **Perspectives**, **Roles** and **Translations** show checked and greyed. The standard TMDL layout already writes each table, perspective, role and culture to a file of its own. The tree has no row for calculation items.

### File names

Each file and table folder is named after its object. Characters that aren't valid in Windows file names (`" < > | : * ? / \`) are encoded in the name.

When you rename an object, the next save removes the old file and writes a file with the new name. When you delete a table, the next save removes its file and its folder.

## Reuse a model's stored settings

When you select **File &gt; Save to Folder** for a model that has a `TabularEditor_SerializeOptions` annotation, the folder dialog shows **Use serialization settings from annotations**. Check it to save with the model's stored settings, including its per-object layout. Uncheck it to save with your preferences and write them to the annotation.

If the model comes from a Database.json folder and you check **Use serialization settings from annotations**, its serialization depth carries over to the TMDL folder when **Save objects to separate files** is checked on the **TMDL Serialization** page or the model's annotation contains `TmdlApplySerializationDepth`. Calculation items stay in their table's file whatever the depth.

## Return to the standard layout

1. Select **Model &gt; Serialization options...**.
2. Uncheck **Save objects to separate files** and click **OK**.
3. Press **Ctrl+S**.
4. Click **Yes** in the **Per-object TMDL serialization** warning.

Tabular Editor rewrites the folder with one file per table and one file each for functions, shared expressions, data sources and relationships, and removes `TmdlApplySerializationDepth` from the annotation. The model's other serialization settings, including TMDL formatting, stay in the annotation.

## Save warning

Any save that writes the standard layout over a folder with per-object files shows the **Per-object TMDL serialization** warning first. This applies to **File &gt; Save**, **File &gt; Save to Folder** and saves in [workspace mode](xref:workspace-mode). The warning reads:

> Your model is currently serialized per object. Saving now will revert your files to the standard TMDL serialization. Please refer to this documentation for details.
>
> Do you wish to continue?

The link in the warning opens this page.

![The Per-object TMDL serialization warning shown before a save writes the standard layout](~/content/assets/images/tmdl-per-object-save-warning.png)


| Answer  | Result                                                                                                            |
| ------- | ----------------------------------------------------------------------------------------------------------------- |
| **Yes** | The folder is rewritten in the standard layout, and `TmdlApplySerializationDepth` is removed from the annotation. |
| **No**  | Nothing is written and the save is cancelled. In workspace mode, the workspace database isn't updated either.     |


After a **Yes**, the folder stays in the standard layout when you open it again in Tabular Editor 3 Enterprise Edition, until you check **Save objects to separate files** again.

## Edition and tool support


| Tool                                | Opens a per-object folder | Saves per-object files                                      |
| ----------------------------------- | ------------------------- | ----------------------------------------------------------- |
| Tabular Editor 3 Enterprise Edition | Yes                       | Yes                                                         |
| Tabular Editor 3 Business Edition   | Yes                       | No. Saves write the standard layout after the save warning. |
| Tabular Editor 3 Desktop Edition    | No                        | No.                                                         |
| Power BI Desktop                    | Yes                       | No. Saves write the standard layout without a warning.      |


In Business Edition, **Save objects to separate files** and the object type tree don't appear on the **TMDL Serialization** page or in **Model &gt; Serialization options...**.

> [!WARNING]
> If anyone saves a per-object folder with a tool that writes the standard layout, every table file and every per-object file changes in source control.

## Object order

Functions, shared expressions, data sources and relationships keep their order when **Include metadata order** is checked: the save writes a `ref` line for each of them to `model.tmdl`, for example:

```tmdl
ref expression Server
ref expression Database
ref function 'Sales.MarginPct'
```

Columns, measures, partitions and hierarchies in their own files load in file name order when you open the folder, and **Include metadata order** has no effect on them.

## See also

- @tmdl
- @save-to-folder
- @save-with-supporting-files
- @parallel-development