---
uid: script-display-unique-column-values
title: 列的唯一值
author: Morten Lønskov
updated: 2024-05-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 列的唯一值

## 脚本用途

Display the distinct values in a column for quick data profiling and access.
可在列级别将其另存为宏，方便快速调用。

<br></br>

## 脚本

### 脚本标题

```csharp
// Construct the DAX expression to get all distinct column values, from the selected column:
var dax = string.Format("ALL({0})", Selected.Column.DaxObjectFullName);

// Evaluate the DAX expression against the connected model:
var result = EvaluateDax(dax);

// Output the DataTable containing the result of the DAX expression:
Output(result);
```

### 说明

该脚本对所选列应用 ALL() DAX 函数，并在输出对话框中显示结果。

