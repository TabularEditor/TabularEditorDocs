---
uid: script-create-sum-measures-from-columns
title: 从列创建 SUM 度量值
author: Morten Lønskov
updated: 2023-02-22
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 从列创建 SUM 度量值

## 脚本用途

如果您想快速为所选列批量创建使用 SUM 汇总的度量值，此脚本即可帮您完成。

## 脚本

### 从列创建度量值

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

### 说明

这个片段使用 `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` 函数，在表中创建一个新的度量值。 We use the `DaxObjectFullName` property to get the fully qualified name of the column for use in the DAX expression: `'TableName'[ColumnName]`.

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/create-sum-measures-from-columns.png" alt="Example of measures created with the script" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 使用此脚本创建的度量值示例。</figcaption>
</figure>