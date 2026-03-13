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

显示某列的去重值，便于快速进行数据概览和查阅。
可在列级别将其另存为宏，方便快速调用。

<br></br>

## 脚本

### 脚本标题

```csharp
// 构造 DAX 表达式，从所选列获取所有不重复的列值：
var dax = string.Format("ALL({0})", Selected.Column.DaxObjectFullName);

// 针对已连接的模型评估该 DAX 表达式：
var result = EvaluateDax(dax);

// 输出包含 DAX 表达式结果的 DataTable：
Output(result);
```

### 说明

该脚本对所选列应用 ALL() DAX 函数，并在输出对话框中显示结果。

