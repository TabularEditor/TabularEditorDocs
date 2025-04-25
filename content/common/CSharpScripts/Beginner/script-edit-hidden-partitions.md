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
Calculated Tables, Calculation Groups and Field Parameters do not have partitions displayed in Tabular Editor. This is on purpose as these should/can not generally be edited. The partition's properties can however still be accessed and edited with below script snippet.
## Script

```csharp
Selected.Table.Partitions[0].Output();
```


### Example Output

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/show-hidden-partitions.png" alt="An example of the output box that appears, letting the user view and edit hidden partitions in the model." style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> An example of the output box that appears, letting the user view and edit hidden partitions in the model.</figcaption>
</figure>