---
uid: script-edit-hidden-partitions
title: Edit Hidden Partitions
author: Morten Lønskov
updated: 2023-02-21

---

# Script Purpose
Calculated Tables, Calculation Groups and Field Parameters do not have partitions displayed in Tabular Editor. This is on purpose as these should/can not generally be edited. The partition's properties can however still be accessed and edited with bellow script snippet.
# Script

```csharp
Selected.Table.Partitions[0].Output();
```


## Example Output
![Edit Hidden Partitions](~/images/Cscripts/show-hidden-partitions.png)

