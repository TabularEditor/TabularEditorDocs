---
uid: script-library-beginner
title: Beginner C# Scripts
author: Morten Lønskov
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# C# Script Library: Beginner Scripts

These are more basic scripts that are easy to understand or modify. They have a defined scope and limited complexity; you don't need a reasonable knowledge of the C# language to use, understand and modify these scripts. They are thus a good place to start when beginning to author C# Scripts in Tabular Editor.

<br>
<br>

| <div style="width:250px">Script Name</div> | Purpose | Use-case |
| --- | --- | --- |
| [Count Table Rows](xref:script-count-rows) | Evaluates a COUNTROWS ( 'Table' ) of a selected table. | When you want to check how many rows are in a table, or if it's been loaded. |
| [Create Sum Measures from Columns](xref:script-create-sum-measures-from-columns) | Create SUM ( 'Table'[Column] ) measures from any selected column. | When you have many columns in a new table / model and must make many measures at once. |
| [Create Measure Table](xref:script-create-measure-table) | Create a measure table | When you want to create an empty table to use as an organizing measure table|
| [Create Table Groups](xref:script-create-table-groups) | Organize the model into Table Groups | When you want to have an automatic organization of your tables using the table group feature of Tabular Editor 3 |
| [Create M Parameter](xref:script-create-m-parameter) | Create a new M Parameter in 'Shared Expressions' | When you want to create a parameter to use in other Power Query queries (M Partitions / Shared Expressions). |
| [Edit Hidden Partitions](xref:script-edit-hidden-partitions) | Reveals the properties of hidden partitions in Calc. Groups & Calc. Tables | When you need to see or edit the TOM properties of these hidden partitions. | 
| [Format Numeric Measures](xref:script-format-numeric-measures) | Formats the chosen measures | When you want to quickly apply a format string to the currently selected measures |
| [Show Data Source Dependencies](xref:script-show-data-source-dependencies) | Shows dependencies for data sources | For explicit (legacy) data sources it can be hard to know exactly where they are used. This script shows you which partition reference the chosen data source |
| [Create Field Parameters](xref:create-field-parameter) | Quickly create a field parameter table | Choose the objects that should be in the field parameter and the script will take care of the rest |
| [Display Unique Column Values](xref:script-display-unique-column-values) | Display unique values in a column | When you want to see the unique values in the currently selected column |