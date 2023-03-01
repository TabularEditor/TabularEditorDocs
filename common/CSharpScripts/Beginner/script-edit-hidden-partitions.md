---
uid: script-edit-hidden-partitions
title: Edit Hidden Partitions
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  versions:
    - version: 2.x
    - version: 3.x
---
# Edit Hidden Partitions

## Script Purpose
Calculated Tables, Calculation Groups and Field Parameters do not have partitions displayed in Tabular Editor. This is on purpose as these should/can not generally be edited. The partition's properties can however still be accessed and edited with bellow script snippet.
## Script

```csharp
Selected.Table.Partitions[0].Output();
```


### Example Output
<br>
<img src="~/images/Cscripts/show-hidden-partitions.png" alt="Image description" id="show-hidden-partitions">
<script>
    var img = document.getElementById("show-hidden-partitions");
    img.style.width = "650px";
</script>