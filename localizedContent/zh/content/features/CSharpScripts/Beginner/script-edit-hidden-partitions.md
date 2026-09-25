---
uid: script-edit-hidden-partitions
title: 编辑隐藏分区
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 编辑隐藏分区

## 脚本用途

在 Tabular Editor 中，计算表格、计算组和字段参数不会显示分区。 This is on purpose as these should/can not generally be edited. The partition's properties can however still be accessed and edited with below script snippet.

## 脚本

```csharp
Selected.Table.Partitions[0].Output();
```

### 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/show-hidden-partitions.png" alt="An example of the output box that appears, letting the user view and edit hidden partitions in the model." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 输出窗口示例：该窗口会弹出，供用户查看并编辑模型中的隐藏分区。</figcaption>
</figure>