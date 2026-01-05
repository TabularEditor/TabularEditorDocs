---
uid: script-library-advanced
title: Advanced C# Scripts
author: Morten Lønskov
updated: 2025-09-04
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# C# Script Library: Advanced Scripts

These are more advanced scripts with sophisticated functionalities requiring a more advanced understanding of the C# language and TOM. They are more difficult to modify and thus recommended only once you have become comfortable with the foundations of C# Scripting in Tabular Editor.

<br>
<br>

| <div style="width:250px">Script Name</div> | Purpose | Use-case |
| --- | --- | --- |
| [Count Model Objects](xref:script-count-things) | Counts all the different objects by type in a model. | When you need an overview of the model contents or want to count objects by type. | 
| [Output Object Details in a Grid](xref:script-output-things) | Outputs object details in a grid view. | When you need to output object details in a grid view for inspection. |
| [Create Date Table](xref:script-create-date-table) | Creates a formatted Date table based on selected Date columns in the model. | When you need to create a new date table based on a template. |
| [Create M Parameter (Auto-Replace)](xref:script-create-and-replace-parameter) | Creates a new M Parameter and automatically adds it to M Partitions. | When you want to replace strings in multiple partitions (i.e. connection strings) with a dynamic M Parameter. |

| [Format Power Query](xref:script-format-power-query) | Formats the Power Query of a selected M Partition by using the powerqueryformatter.com API. | When you have complex Power Query and need to make it more readable for reading or making changes. |
| [Implement Incremental Refresh](xref:script-implement-incremental-refresh) | Configures Incremental Refresh automatically using parameters from a UI dialogue box. | When you need to implement incremental refresh but aren't comfortable with the configuration in the table settings. |
| [Remove Measures with Errors](xref:script-remove-measures-with-error) | Creates a new M Parameter and automatically adds it to M Partitions. | When you want to replace strings in multiple partitions (i.e. connection strings) with a dynamic M Parameter. |
| [Find & Replace in Selected Measures](xref:script-find-replace) | Searches for a substring in the DAX of selected measures, replacing with another substring. | When you need to quickly find/replace values in multiple DAX measures (i.e. `CALCULATE` filter or broken object references). |
| [Databricks Semantic Model Set-up](xref:script-databricks-semantic-model-set-up) | Friendly name tables and columns and set column best practices | When your Databricks object names need making more user friendly. |
| [Create Databricks Relationships](xref:script-create-databricks-relationships) | Create relationships based on primary and foreign key definitions in Databricks Unity Catalog | When you want to re-use Databricks relationship definitions that have already been defined in Unity Catalog. |
| [Add Databricks Metadata Descriptions](xref:script-add-databricks-metadata-descriptions) | Update table and column descriptions based on Databricks Unity Catalog | When you want to re-use Databricks table and column comments that have already been defined in Unity Catalog. |
| [Convert DL/SQL to DL/OL](xref:script-convert-dlsql-to-dlol) | Changes the partitions of a Direct Lake over SQL model to Direct Lake over OneLake | Useful for easily migrating to Direct Lake over OneLake |
| [Convert Import to DL/OL](xref:script-convert-dlsql-to-dlol) | Changes the partitions of a Import model to Direct Lake over OneLake | Useful for easily migrating to Direct Lake over OneLake |