---
uid: script-create-measure-table
title: Create Measure Table
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Title

## Script Purpose
The scripts creates a hidden measure table containing one hidden column


## Script

### Script Title
```csharp
// Create a calculated table with a single column which is hidden:
var table = Model.AddCalculatedTable("Model Measures", "{0}");
table.Columns[0].IsHidden = true;
```