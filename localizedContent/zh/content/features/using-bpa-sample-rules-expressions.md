---
uid: using-bpa-sample-rules-expressions
title: BPA 示例规则表达式
author: Morten Lønskov
updated: 2023-02-21
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 规则表达式示例

在本节中，你将看到一些可用于定义规则的 Dynamic LINQ 表达式示例。 The expression that is entered in the Rule Expression Editor, will be evaluated whenever focus leaves the textbox, and any syntax errors will be shown on top of the screen:

![image](~/content/assets/images/using-bpa-sample-rules-expressions-01.png)

你的规则表达式可以访问 TOM 中对象的任何公共属性。 If you try to access a property that does not exist on that type of object, an error will also be shown:

![image](~/content/assets/images/using-bpa-sample-rules-expressions-02.png)

“Column” 对象上不存在“Expression”，但如果我们将下拉列表切换为“计算列”，上面的语句就能正常工作：

![image](~/content/assets/images/using-bpa-sample-rules-expressions-03.png)

Dynamic LINQ 支持所有标准的算术、逻辑和比较运算符；通过“.”表示法，你可以访问任何对象的子属性和方法。

```
String.IsNullOrWhitespace(Expression) and not Name.StartsWith("Dummy")
```

将上述语句应用于计算列、计算表格或度量值时，会标记出 DAX 表达式为空且名称不以“Dummy”开头的对象。

Using LINQ, we can also work with collections of objects. 将以下表达式应用于表时，会找出那些包含超过 10 个未归入显示文件夹的列的表：

```
Columns.Count(DisplayFolder = "") > 10
```

每当我们使用某个 LINQ 方法遍历集合时，作为该 LINQ 方法参数的表达式都会在集合中的各个项目上进行求值。 Indeed, DisplayFolder is a property on columns that does not exist at the Table level.

Here, we see this rule in action on the Adventure Works tabular model. 注意：“Reseller”表会显示为违规，而“Reseller Sales”不会（后者的列已整理到显示文件夹中）：

![image](~/content/assets/images/using-bpa-sample-rules-expressions-04.png)

要在 LINQ 方法中引用父对象，可以用特殊的 "outerIt" 语法。 This rule, applied to tables, will find those that contain columns whose name does not start with the table name:

```
Columns.Any(not Name.StartsWith(outerIt.Name))
```

直接把这条规则应用到 Columns 列上可能更合理，这种情况下应写为：

```
not Name.StartsWith(Table.Name)
```

To compare against enumeration properties, simply pass the enumerated value as a string. 这条规则将找出所有名称以 "Key" 或 "ID" 结尾，但 SummarizeBy 属性未设置为 "None" 的列：

```
(Name.EndsWith("Key") or Name.EndsWith("ID")) and SummarizeBy <> "None"
```

## 查找未使用的对象

When building Tabular Models it is important to avoid high-cardinality columns at all costs. Typical culprits are system timestamps, technical keys, etc. that have been imported to the model by mistake. In general, we should make sure that the model only contains columns that are actually needed. Wouldn't it be nice if the Best Practice Analyzer could tell us which columns are likely not needed at all?

以下规则将 Report 满足以下条件的列：

- ...处于隐藏状态（或其父表被隐藏）
- ...未被任何 DAX 表达式引用（会考虑模型中的所有 DAX 表达式——甚至包括 drillthrough 和 RLS 筛选表达式）
- ...不参与任何关系
- ...未被用作任何其他列的“Sort By”列，即按列排序的列
- ...未用作任何层次结构的级别。

此 BPA 规则的 Dynamic LINQ 表达式为：

```
(IsHidden or Table.IsHidden)
and ReferencedBy.Count = 0 
and (not UsedInRelationships.Any())
and (not UsedInSortBy.Any())
and (not UsedInHierarchies.Any())
```

The same technique can be used to find unused measures. It's a little simpler, since measures can't participate in relationships, etc. So instead, let's spice things up a bit, by also considering whether any downstream objects that reference a given measure, are visible or not. That is, if measure [A] is referenced by measure [B], and both measure [A] and [B] are hidden, and no other DAX expressions refer to these two measures, we should let the developer know that it is safe to remove both of them:

```
(IsHidden or Table.IsHidden)
and not ReferencedBy.AllMeasures.Any(not IsHidden)
and not ReferencedBy.AllColumns.Any(not IsHidden)
and not ReferencedBy.AllTables.Any(not IsHidden)
and not ReferencedBy.Roles.Any()
```

## 修复对象

In some cases, it is possible to automatically fix the issues on objects satisfying the criteria of a rule. For example when it's just a matter of setting a simple property on the object. Take a closer look at the JSON behind the following rule:

```json
{
    "ID": "FKCOLUMNS_HIDDEN",
    "Name": "Hide foreign key columns",
    "Category": null,
    "Description": "Columns used on the Many side of a relationship should be hidden.",
    "Severity": 1,
    "Scope": "Column",
    "Expression": "Model.Relationships.Any(FromColumn = outerIt) and not IsHidden and not Table.IsHidden",
    "FixExpression": "IsHidden = true",
    "CompatibilityLevel": 1200
}
```

This rule finds all columns that are used in a relationship (on the "Many"/"From" side), but where the column or its parent table are not hidden. It is recommended that such columns are never shown, as users should filter data using the related (dimension) table instead. So the fix in this case, would be to set the columns IsHidden property to true, which is exactly what the "FixExpression" string above does. To see this in action, right-click any objects that violate the rule, and choose "Generate Fix Script". This puts a small script into the clipboard, which can be pasted into the Advanced Script Editor, from where you can easily review the code and execute it:

![image](~/content/assets/images/using-bpa-sample-rules-expressions-05.png)

记住：脚本执行后对模型所做的更改随时都能撤销（CTRL+Z）。
