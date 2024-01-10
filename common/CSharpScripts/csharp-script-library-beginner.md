---
uid: script-library-beginner
title: Beginner C# Scripts
updated: 2023-02-27
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---

# C# Script Library: Beginner Scripts

These are more basic scripts that are easy to understand or modify. They have a defined scope and limited complexity; you don't need a reasonable knowledge of the C# language to use, understand and modify these scripts. They are thus a good place to start when beginning to author C# Scripts in Tabular Editor.

<br>
<br>

| <div style="width:250px">Script Name</div> | Purpose | Use-case |
| --- | --- | --- |
| [Count Table Rows](Beginner/script-count-rows.md) | Evaluates a COUNTROWS ( 'Table' ) of a selected table. | When you want to check how many rows are in a table, or if it's been loaded. |
| [Count Model Objects](Beginner/script-count-things.md) | Counts all the different objects by type in a model. | When you need an overview of the model contents or want to count objects by type. | 
| [Create Sum Measures from Columns](Beginner/script-create-sum-measures-from-columns.md) | Create SUM ( 'Table'[Column] ) measures from any selected column. | When you have many columns in a new table / model and must make many measures at once. |
| [Create M Parameter](Beginner/script-create-m-parameter.md) | Create a new M Parameter in 'Shared Expressions' | When you want to create a parameter to use in other Power Query queries (M Partitions / Shared Expressions). |
| [Edit Hidden Partitions](Beginner/script-edit-hidden-partitions.md) | Reveals the properties of hidden partitions in Calc. Groups & Calc. Tables | When you need to see or edit the TOM properties of these hidden partitions. | 
| [Find & Replace in Selected Measures](Beginner/script-find-replace-selected-measures.md) | Searches for a substring in the DAX of selected measures, replacing with another substring. | When you need to quickly find/replace values in multiple DAX measures (i.e. `CALCULATE` filter or broken object references). | 
| [Create Measure Table](Beginner/script-create-measure-table.md) | Create a measure table | When you want to create an empty table to use as a organizing measure table|
| [Create Table Groups](Beginner/script-create-table-groups.md) | Organize the model into Table Groups | When you want to have an automatic organization of your tables using the table group feature of Tabular Editor 3 |
| [Format Numeric Measures](Beginner/script-format-numeric-measures.md) | Formats the chosen measures | When you want quickly have your selected measures to have a format string |
| [Show Data Source Dependencies](Beginner/script-show-data-source-dependencies.md) | Shows dependencies for data sources | For explicit (legacy) data sources it can be hard to know exactly where they are used. This script shows you which partition reference the chosen data source |


