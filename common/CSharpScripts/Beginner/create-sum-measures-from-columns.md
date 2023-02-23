---
uid: create-sum-measures-from-columns
title: Create SUM Measure from Column
author: Morten Lønskov
updated: 2023-02-22
applies_to:
  editions:
    - edition: TE2
    - edition: TE3 Desktop
    - edition: TE3 Business
    - edition: TE3 Enterprise
---
# Create SUM Measure from Column

## Script Purpose
If you want to quickly create a number of measures that SUM over the columns that you select then this script with do it for you. 

## Script

### Create measures from columns
```csharp
// Creates a SUM measure for every currently selected column and hide the column.
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "Sum of " + c.Name,                    // Name
        "SUM(" + c.DaxObjectFullName + ")",    // DAX expression
        c.DisplayFolder                        // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = "0.00";

    // Provide some documentation:
    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    // Hide the base column:
    c.IsHidden = true;
}
```
### Explanation
This snippet uses the `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` function to create a new measure on the table. We use the `DaxObjectFullName` property to get the fully qualified name of the column for use in the DAX expression: `'TableName'[ColumnName]`.

## Example Output
![Edit Hidden Partitions](~/images/Cscripts/create-sum-measures-from-columns.png)


