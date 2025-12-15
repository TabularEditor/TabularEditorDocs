---
uid: script-create-measure-table
title: Create Measure Table
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---
# Create Measure Table

## Script Purpose
The scripts creates a hidden measure table containing one hidden column


## Script

### Create Measure Table
```csharp
// Create a calculated table with a single column which is hidden:
var table = Model.AddCalculatedTable("Model Measures", "{0}");
table.Columns[0].IsHidden = true;
```