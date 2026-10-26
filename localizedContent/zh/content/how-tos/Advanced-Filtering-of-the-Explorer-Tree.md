---
uid: advanced-filtering-explorer-tree
title: 高级对象筛选
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# 高级对象筛选

资源管理器树中的**筛选**文本框按名称、通配符模式或动态 LINQ 表达式筛选树中显示的对象。

## 筛选模式

[Tabular Editor 2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4) 中新增的**筛选**按钮旁边的三个最右侧工具栏按钮用于设置筛选器应用于对象层次结构的方式以及结果的显示方式。

![Explorer工具栏中的筛选文本框和筛选模式按钮](~/content/assets/images/advanced-filtering-of-the-explorer-tree-01.png)

* ![按父级分层按钮](~/content/assets/images/advanced-filtering-of-the-explorer-tree-02.png) **按父级分层**：搜索适用于父级对象，即表格，并显示文件夹（如果显示）。当父级匹配时，将显示其所有子级。
* ![按子级分层按钮](~/content/assets/images/advanced-filtering-of-the-explorer-tree-03.png) **按子级分层**：搜索适用于子级对象，例如度量值、列和层次结构。只有当至少一个子级匹配时，才会显示父级。
* ![扁平按钮](~/content/assets/images/advanced-filtering-of-the-explorer-tree-04.png) **扁平**：搜索适用于所有对象，结果以扁平列表的形式显示。具有子项的对象仍按层次结构显示子项。

## 简单搜索

在**筛选器**文本框中输入文本，然后按**Enter**键，即可对对象名称进行不区分大小写的搜索。例如，在“按父级”模式下搜索“sales”将得到以下结果：

![“按父级”模式下的“销售”搜索结果](~/content/assets/images/advanced-filtering-of-the-explorer-tree-05.png)

展开表将显示其所有度量值、列、层次结构和分区。在“按子级”模式下，相同的搜索将返回以下结果：

![“按子级”模式下的“销售”搜索结果](~/content/assets/images/advanced-filtering-of-the-explorer-tree-06.png)

“Employee”表现在显示出来，因为其部分列包含“sales”一词。

## 通配符搜索

在**筛选条件**文本框中，`?`匹配任意单个字符，`*`匹配任意零个或多个字符的序列，并且与简单搜索一样，匹配不区分大小写。`*sales*`给出与上述相同的结果，而`sales*`仅显示名称以“sales”开头的对象。

在“按父级”模式下搜索“sales*”将得到以下结果：

![在“按父级”模式下搜索“sales*”的结果](~/content/assets/images/advanced-filtering-of-the-explorer-tree-07.png)

在“按子级”模式下进行相同的搜索，将得到以下结果：

![在“按子级”模式下搜索“sales*”的结果](~/content/assets/images/advanced-filtering-of-the-explorer-tree-08.png)

对“sales*”进行扁平搜索，显示信息列（**Ctrl+F1**），以查看每个对象的详细信息：

![sales* 的平面搜索结果，信息列显示父级和类型](~/content/assets/images/advanced-filtering-of-the-explorer-tree-09.png)

您可以在字符串的任何位置放置任意数量的通配符。

## 动态 LINQ 搜索

筛选器还接受 [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) 表达式，即 [Best Practice Analyzer 规则](xref:best-practice-analyzer)使用的语法。使用“`:`”（冒号）开头搜索字符串，以切换到动态 LINQ 模式。例如，此筛选器显示所有名称以“Key”结尾的对象（区分大小写）：

```text
:Name.EndsWith("Key")
```

按 **Enter** 应用筛选器，在“扁平”模式下将得到以下结果：

![对以“Key”结尾的名称应用动态 LINQ 筛选器的平面结果](~/content/assets/images/advanced-filtering-of-the-explorer-tree-10.png)

对于动态 LINQ 中的不区分大小写的搜索，请转换字符串：

```text
:Name.ToUpper().EndsWith("KEY")
```

或者，您可以提供 [StringComparison](https://docs.microsoft.com/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_) 参数，例如：

```text
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

动态 LINQ 筛选器可以评估对象的任何属性，包括子属性。例如，此筛选器会查找表达式中包含“TODO”一词的所有对象：

```text
:Expression.ToUpper().Contains("TODO")
```

此筛选器显示模型中所有未被其他对象引用的隐藏度量值：

```text
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
```

正则表达式也适用，例如以下筛选器可查找名称中包含“Number”或“Amount”的所有列：

```text
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

在“按父级”和“按子级”模式下，显示选项（位于树正上方的工具栏按钮）也会筛选结果。例如，上面的筛选器仅返回列，因此，如果显示选项隐藏列，则树将不显示任何内容。
