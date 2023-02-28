---
uid: script-count-rows
title: Count Table Rows
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Count Rows in a Table

## Script Purpose
If you want to see how many rows are loaded to a table, or quickly check if the table has been loaded, at all.
This script requires connection to a remote model or connection via Workspace Mode.

## Script

### Count the rows in the selected table
```csharp
// This script counts rows in a selected table and displays the result in a pop-up info box.
// It does not write any changes to this model.
//
// Use this script when you want to check whether a table was loaded or how many rows it has.
//
// Get table name
string _TableName = 
    Selected.Table.DaxObjectFullName;

// Count table rows
string _dax = 
    "{ FORMAT( COUNTROWS (" + _TableName + "), \"#,##0\" ) }";

// Evaluate DAX
string _TableRows = 
    Convert.ToString(EvaluateDax( _dax ));

// Return output in pop-up
Info ( "Number of rows in " + _TableName + ": " + _TableRows);
```
### Explanation
This snippet goes through the model and counts the different object types, displaying them in a hierarchical "node and tree" format that is manually constructed. 
You can comment out 

## Example Output
<br>
<img src="~/images/Cscripts/script-count-rows-output.png" alt="Image description" id="count-rows-output">
<script>
    var img = document.getElementById("count-rows-output");
    img.style.width = "400px";
</script>