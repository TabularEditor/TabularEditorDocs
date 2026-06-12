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
// 为当前选中的每一列创建一个 SUM 度量值，并隐藏该列。
foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "求和 " + c.Name,                    // 名称
        "SUM(" + c.DaxObjectFullName + ")",    // DAX 表达式
        c.DisplayFolder                        // 显示文件夹
    );
    
    // 为新度量值设置格式：
    newMeasure.FormatString = "0.00";

    // 添加说明：
    newMeasure.Description = "此度量值为列 " + c.DaxObjectFullName + " 的总和";

    // 隐藏基础列：
    c.IsHidden = true;
}
```

### 说明

此代码片段使用 `<Table>.AddMeasure(<name>, <expression>, <displayFolder>)` 函数在表上创建新的度量值。 我们使用 `DaxObjectFullName` 属性获取列的完全限定名称，用于 DAX 表达式：`'TableName'[ColumnName]`。 我们使用 `DaxObjectFullName` 属性获取列的完全限定名称，用于 DAX 表达式：`'TableName'[ColumnName]`。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/create-sum-measures-from-columns.png" alt="Example of measures created with the script" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 使用此脚本创建的度量值示例。</figcaption>
</figure>