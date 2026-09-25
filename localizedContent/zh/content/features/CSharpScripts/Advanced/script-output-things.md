---
uid: script-output-things
title: 以网格形式输出对象详细信息
author: Daniel Otykier
updated: 2024-12-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 以网格形式输出对象详细信息

## 脚本用途

另一种查看模型中对象及其配置概况的方法，是使用 C# 的 [`DataTable`](https://learn.microsoft.com/en-us/dotnet/api/system.data.datatable?view=net-8.0) 类将它们以网格形式输出。 This is a very flexible technique, as you can add only the information you are interested in, as columns of the `DataTable`. Moreover, when passing a `DataTable` to the `Output()` method, Tabular Editor will automatically display it in a grid view, which is very convenient for inspecting the data.

## 脚本

### 显示度量值复杂度详情

```csharp
// This script displays a grid with details about each measure in the model.
using System.Data;

var result = new DataTable();
result.Columns.Add("Name");
result.Columns.Add("Table");
result.Columns.Add("Expression token count", typeof(int));
result.Columns.Add("Expression line count", typeof(int));
result.Columns.Add("Description line count", typeof(int));
result.Columns.Add("Format String");

foreach(var m in Model.AllMeasures)
{
    var row = new object[]
    {
        m.DaxObjectName,    // Name
        m.Table.Name,       // Table
        m.Tokenize().Count, // Token count
        m.Expression.Split(new []{'\n'}, StringSplitOptions.RemoveEmptyEntries).Length,
        m.Description.Split(new []{'\n'}, StringSplitOptions.RemoveEmptyEntries).Length,
        m.FormatStringExpression ?? m.FormatString
    };
    result.Rows.Add(row);
}

Output(result);
```

### 说明

This snippet first configures a `DataTable` object with the columns we want to display in the grid. We explicitly specify the `typeof(int)` for some of the columns, to ensure that sorting works correctly. We then iterate over all measures in the model, and for each measure, we create a new row in the `DataTable` with the desired information. Finally, we pass the `DataTable` to the `Output()` method, which will display the grid.

显示的列包括：

- **Name**：度量值的名称。
- **Table**：该度量值所属表的名称。
- **Expression token count**: The number of tokens in the measure expression. This is a rough measure of DAX complexity.
- **表达式行数**：度量值表达式的行数，不计空行。
- **描述行数**: 度量值描述的行数，不计空行。
- **格式字符串**: 度量值的格式字符串表达式或格式字符串（如有）。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/script-output-things-example.png" alt="Example of the dialog pop-up that displays the grid." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Example of the dialog pop-up that displays the grid. Both Tabular Editor 2 and Tabular Editor 3 will let you sort the grid columns as well as copy the output to the clipboard. However, Tabular Editor 3 also has additional features for grouping, filtering, and searching within the grid.</figcaption>
</figure>