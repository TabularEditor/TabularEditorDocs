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

在本节中，你将看到一些可用于定义规则的 Dynamic LINQ 表达式示例。 在规则表达式的“表达式编辑器”中输入的表达式会在文本框失去焦点时进行求值，任何语法错误都会显示在屏幕顶部：

![image](https://cloud.githubusercontent.com/assets/8976200/25380170/9f01634e-29af-11e7-952e-e10a1f28df32.png)

你的规则表达式可以访问 TOM 中对象的任何公共属性。 如果你尝试访问该对象类型上不存在的属性，也会显示错误：

![image](https://cloud.githubusercontent.com/assets/8976200/25381302/798bab98-29b3-11e7-931e-789e5286fc45.png)

“Column” 对象上不存在“Expression”，但如果我们将下拉列表切换为“计算列”，上面的语句就能正常工作：

![image](https://cloud.githubusercontent.com/assets/8976200/25380451/87b160da-29b0-11e7-8e2e-c4e47593007d.png)

Dynamic LINQ 支持所有标准的算术、逻辑和比较运算符；通过“.”表示法，你可以访问任何对象的子属性和方法。

```
String.IsNullOrWhitespace(Expression) and not Name.StartsWith("Dummy")
```

将上述语句应用于计算列、计算表格或度量值时，会标记出 DAX 表达式为空且名称不以“Dummy”开头的对象。

使用 LINQ，我们也可以处理对象集合。 将以下表达式应用于表时，会找出那些包含超过 10 个未归入显示文件夹的列的表：

```
Columns.Count(DisplayFolder = "") > 10
```

每当我们使用某个 LINQ 方法遍历集合时，作为该 LINQ 方法参数的表达式都会在集合中的各个项目上进行求值。 确实，DisplayFolder 是列上的一个属性，在表级别并不存在。

在这里，我们可以看到这条规则在 Adventure Works 表格模型上的实际效果。 注意：“Reseller”表会显示为违规，而“Reseller Sales”不会（后者的列已整理到显示文件夹中）：

![image](https://cloud.githubusercontent.com/assets/8976200/25380809/d9d1c3a4-29b1-11e7-839e-29450ad39c8a.png)

要在 LINQ 方法中引用父对象，可以用特殊的 "outerIt" 语法。 将这条规则应用于表时，会找出那些包含列名不以表名开头的列的表：

```
Columns.Any(not Name.StartsWith(outerIt.Name))
```

直接把这条规则应用到 Columns 列上可能更合理，这种情况下应写为：

```
not Name.StartsWith(Table.Name)
```

要与枚举属性进行比较，只需将枚举值作为字符串传入即可。 这条规则将找出所有名称以 "Key" 或 "ID" 结尾，但 SummarizeBy 属性未设置为 "None" 的列：

```
(Name.EndsWith("Key") or Name.EndsWith("ID")) and SummarizeBy <> "None"
```

## 查找未使用的对象

在构建表格模型时，务必避免高基数列。 常见的原因包括误将系统时间戳、技术键等导入模型。 总体来说，我们应确保模型只包含真正需要的列。 如果 Best Practice Analyzer 能告诉我们哪些列很可能完全不需要，那不是很好吗？

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

同样的技巧也可以用来查找未使用的度量值。 这会更简单一些，因为度量值无法参与关系等。 不过我们可以把事情做得更有意思一点：同时考虑引用某个度量值的下游对象是否可见。 也就是说，如果度量值 [A] 被度量值 [B] 引用，且度量值 [A] 和 [B] 都处于隐藏状态，并且没有其他 DAX 表达式引用这两个度量值，那么应告知开发者：可以安全地将它们一并移除：

```
(IsHidden or Table.IsHidden)
and not ReferencedBy.AllMeasures.Any(not IsHidden)
and not ReferencedBy.AllColumns.Any(not IsHidden)
and not ReferencedBy.AllTables.Any(not IsHidden)
and not ReferencedBy.Roles.Any()
```

## 修复对象

在某些情况下，可以自动修复满足某条规则条件的对象上的问题。 例如，只需要在对象上设置一个简单属性时。 仔细看看下面这条规则背后的 JSON：

```json
{
    "ID": "FKCOLUMNS_HIDDEN",
    "Name": "隐藏外键列",
    "Category": null,
    "Description": "关系中位于多端使用的列应隐藏。",
    "Severity": 1,
    "Scope": "Column",
    "Expression": "Model.Relationships.Any(FromColumn = outerIt) and not IsHidden and not Table.IsHidden",
    "FixExpression": "IsHidden = true",
    "Compatibility": [
      1200,
      1400
    ],
    "IsValid": false
}
```

这条规则会找出所有在关系("Many"/"From" 端)使用的列，但这些列或其父表并未隐藏。 建议永远不要显示此类列，因为用户应该改用相关的（维度）表来筛选数据。 因此，这里的修复方式就是将列的 IsHidden 属性设置为 true，而上面的 "FixExpression" 字符串正是这么做的。 要看看实际效果的话，在任何违反这条规则的对象上右键，然后选择“生成修复脚本”。 这会将一小段脚本复制到剪贴板，你可以将其粘贴到高级脚本编辑器中，然后就能轻松检查代码并执行：

![image](https://cloud.githubusercontent.com/assets/8976200/25298489/9035bab6-26f5-11e7-8134-8502daaf4132.png)

记住：脚本执行后对模型所做的更改随时都能撤销（CTRL+Z）。
