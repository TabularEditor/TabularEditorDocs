---
uid: script-display-unique-column-values
title: Distinct Column Values
author: Morten Lønskov
updated: 2024-05-27
applies_to:
  products:
    - product: TE2
      full: true
    - product: TE3
      full: true
---
# Distinct Column Values

## Script Purpose
Display the distinct values in a column for quick data profiling and access.
Save as a Macro on the column level to have it quickly available. 

<br></br>

## Script

### Script Title
```csharp
// Construct the DAX expression to get all distinct column values, from the selected column:
var dax = string.Format("ALL({0})", Selected.Column.DaxObjectFullName);

// Evaluate the DAX expression against the connected model:
var result = EvaluateDax(dax);

// Output the DataTable containing the result of the DAX expression:
Output(result);
```
### Explanation
The script uses the ALL() DAX function against the selected columns and display the result in an output dialog box. 

