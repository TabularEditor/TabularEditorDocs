---
uid: script-create-measure-table
title: 创建度量值表
author: Morten Lønskov
updated: 2023-11-29
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 创建度量值表

## 脚本用途

该脚本会创建一个隐藏的度量值表，其中包含一个隐藏列

## 脚本

### 创建度量值表

```csharp
// 创建一个仅包含一列且该列被隐藏的计算表格：
var table = Model.AddCalculatedTable("Model Measures", "{0}");
table.Columns[0].IsHidden = true;
```