---
uid: script-show-data-source-dependencies
title: Show Data Source Dependencies
author: David Bojsen
updated: 2023-09-12
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Show Data Source Dependencies

## Script Purpose
The script outputs the tables that reference the selected explicit (legacy) data source. This will make it easier to determine where a selected data source is used. 

## Script

### Count the rows in the selected table
```csharp
//The script outputs the tables that reference the selected explicit (legacy) data source.
if (Model.DataSources.Count == 0)
{
    Info("This model doesn't contain any data sources, it is either empty or using implicit datasources");
    return;
}
// Checks that a data source is selected
DataSource selectedDatasource = null;

if (Selected.DataSources.Count == 1)
    selectedDatasource = Selected.DataSource;
else
    selectedDatasource = SelectObject<DataSource>(Model.DataSources, null, "Select which datasource to see dependencies for");

// Legacy sources
var legacyTables = Model.Tables.Where(t => t.Source == selectedDatasource.Name).ToList();

// M sources
var mTables = Model.Tables.Where(t => t.Partitions.Any(p => p.Expression.Contains($"= #\"{selectedDatasource.Name}\","))).ToList();

// join arrays
var allTables = legacyTables.Union(mTables).OrderBy(t => t.Name);

// Present result
var tableString = string.Join("\r\n", allTables.Select(t => t.Name));
Info($"Datasource {selectedDatasource.Name} is referenced from the following tables:\r\n" + tableString);
```
### Explanation
This snippet takes the selected data source and goes through the model to collect the partitions where that data source is used. 

## Example Output

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/images/Cscripts/script-show-data-source-dependencies-output.png" alt="Example of the dialog pop-up that informs the user which tables use the selected data source" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Example of the dialog pop-up that informs the user which tables use the selected data source.</figcaption>
</figure>