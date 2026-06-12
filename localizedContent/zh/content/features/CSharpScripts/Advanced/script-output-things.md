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

另一种查看模型中对象及其配置概况的方法，是使用 C# 的 [`DataTable`](https://learn.microsoft.com/en-us/dotnet/api/system.data.datatable?view=net-8.0) 类将它们以网格形式输出。 这种技术非常灵活，你可以只把自己关心的信息作为 `DataTable` 的列添加进去。 此外，将 `DataTable` 传给 `Output()` 方法时，Tabular Editor 会自动以网格视图显示它，这对检查数据非常方便。 这种技术非常灵活，你可以只把自己关心的信息作为 `DataTable` 的列添加进去。 此外，将 `DataTable` 传给 `Output()` 方法时，Tabular Editor 会自动以网格视图显示它，这对检查数据非常方便。

## 脚本

### 显示度量值复杂度详情

```csharp
// 此脚本显示一个网格，其中包含模型中每个度量值的详细信息。
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

这段代码首先配置一个 `DataTable` 对象，包含我们希望在网格中显示的各个列。 我们为其中一些列显式指定 `typeof(int)`，以确保排序能够正确工作。 然后我们遍历模型中的所有度量值；对每个度量值，在 `DataTable` 中创建一行，并填入所需信息。 最后，我们将 `DataTable` 传给 `Output()` 方法，它会显示该网格。

显示的列包括：

- **Name**：度量值的名称。
- **Table**：该度量值所属表的名称。
- **表达式词元数量**: 度量值表达式中的词元数量。 这是衡量 DAX 复杂度的一个粗略指标。
- **表达式行数**：度量值表达式的行数，不计空行。
- **描述行数**: 度量值描述的行数，不计空行。
- **格式字符串**: 度量值的格式字符串表达式或格式字符串（如有）。

## 示例输出

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/script-output-things-example.png" alt="Example of the dialog pop-up that displays the grid." style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> 显示网格的对话框弹窗示例。 Tabular Editor 2 和 Tabular Editor 3 都允许对网格列进行排序，并将输出复制到剪贴板。 不过，Tabular Editor 3 还额外提供在网格中进行分组、筛选和搜索的功能。</figcaption>
</figure>