---
uid: script-count-rows
title: 统计表行数
author: Kurt Buhler
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 统计表中的行数

## 脚本用途

如果你想查看某个表加载了多少行，或快速检查该表是否根本已加载。
This script requires connection to a remote model or connection via Workspace Mode.

## 脚本

### 统计所选表中的行数

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

### 说明

此代码片段会遍历模型并统计不同对象类型的数量，然后以手动构建的分层“节点和树”格式显示出来。
You can comment out

## 输出示例

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-rows-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>运行此脚本后会弹出信息框，用于告知用户所选表中的行数示例。</figcaption>
</figure>