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
此脚本需要连接到远程模型，或通过工作区模式进行连接。

## 脚本

### 统计所选表中的行数

```csharp
// 此脚本会统计所选表中的行数，并在弹出信息框中显示结果。
// 它不会对该模型做任何更改。
//
// 当你想检查某个表是否已加载，或想知道它有多少行时，可用此脚本。
//
// 获取表名
string _TableName = 
    Selected.Table.DaxObjectFullName;

// 统计表行数
string _dax = 
    "{ FORMAT( COUNTROWS (" + _TableName + "), \"#,##0\" ) }";

// 评估 DAX
string _TableRows = 
    Convert.ToString(EvaluateDax( _dax ));

// 返回弹出窗口中的输出
Info ( "表 " + _TableName + " 的行数: " + _TableRows);
```

### 说明

此代码片段会遍历模型并统计不同对象类型的数量，然后以手动构建的分层“节点和树”格式显示出来。
你可以将其注释掉

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/Cscripts/script-count-rows-output.png" alt="Example of the dialog pop-up that informs the user of how many rows are in the selected table upon running the script." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong>运行此脚本后会弹出信息框，用于告知用户所选表中的行数示例。</figcaption>
</figure>