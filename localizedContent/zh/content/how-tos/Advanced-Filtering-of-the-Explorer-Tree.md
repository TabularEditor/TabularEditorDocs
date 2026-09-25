---
uid: advanced-filtering-explorer-tree
title: 高级对象筛选
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      partial: true
---

# 高级对象筛选

本文介绍如何在 Tabular Editor 中使用“Filter”文本框——在浏览复杂模型时，这是一个非常实用的功能。

## 筛选模式

从 [2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4) 起，Tabular Editor 允许你决定筛选器如何应用于层级结构中的对象，以及搜索结果的显示方式。 This is controlled using the three right-most toolbar buttons next to the Filter button:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-01.png)

- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-02.png) **Hierarchical by parent**: The search will apply to _parent_ objects, that is Tables and Display Folders (if those are enabled). All child items will be displayed, when a parent item matches the search criteria.
- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-03.png) **Hierarchical by children**: The search will apply to _child_ objects, that is Measures, Columns, Hierarchies, etc. Parent objects will only be displayed if they have at least one child object matching the search criteria.
- ![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-04.png) **Flat**: The search will apply to all objects, and results will be displayed in a flat list. Objects that contain child items will still display these in a hierarchical manner.

## 简单搜索

在“Filter”文本框中输入任意内容，然后按 [Enter]，即可在对象名称中进行不区分大小写的简单搜索。 For example, typing "sales" in the Filter textbox, using the "By Parent" filtering mode, will produce the following results:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-05.png)

Expanding any of the tables will reveal all measures, columns, hierarchies and partitions of the table. If we change the filtering mode to "By Child", the results will look like this:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-06.png)

注意，“Employee”表现在也出现在列表中，因为它有几个子项（本例中是列）包含“sales”这个词。

## 通配符搜索

When typing in a string in the Filter textbox, you can use the wildcard `?` to denote any single character, and `*` to denote any sequence of characters (zero or more). So typing `*sales*` would produce exactly the same results as shown above, however typing `sales*` will only show objects whose name _starts_ with the word "sales" (again, this is case-insensitive).

按父级搜索 `sales*`：

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-07.png)

按子级搜索 `sales*`：

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-08.png)

平铺模式下搜索 `sales*`（按 [Ctrl]+[F1] 切换信息列，以显示每个对象的详细信息）：

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-09.png)

Wildcards can be placed anywhere in the string, and you can include as many as you need. If that's not complex enough, read on...

## 动态 LINQ 搜索

You can also use [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) to search for objects, which is the same thing you do when creating [Best Practice Analyzer rules](xref:best-practice-analyzer). To enable Dynamic LINQ mode in the filter box, simply put a `:` (colon) in front of your search string. For example, to view all objects whose name end with "Key" (case-sensitive) write:

```
:Name.EndsWith("Key")
```

...and hit [Enter]. In "Flat" filtering mode, the result looks like this:

![image](~/content/assets/images/advanced-filtering-of-the-explorer-tree-10.png)

在动态 LINQ 中进行不区分大小写的搜索，你可以先用类似下面的方式转换输入字符串：

```
:Name.ToUpper().EndsWith("KEY")
```

或者也可以传入 [StringComparison](https://docs.microsoft.com/en-us/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_) 参数，例如：

```
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

You are not restricted to searching within the names of objects. 动态 LINQ 的搜索字符串可以按需写得很复杂，用于匹配对象的任意属性（以及子属性）。 So if you want to find all objects having an expression that contains the word "TODO", you would use the following search filter:

```
:Expression.ToUpper().Contains("TODO")
```

再举一例，下面将显示模型中所有未被任何其他对象引用的隐藏度量值：

```
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
```

You can also use Regular Expressions. 下面会查找所有名称包含“Number”或“Amount”的列：

```
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

Note, that the display options (the toolbar buttons directly above the tree), may affect the results when using "By Parent" and "By Child" filtering mode. For example, the above LINQ filter only returns columns, but if your display options are currently set to not show columns, nothing will be displayed.
