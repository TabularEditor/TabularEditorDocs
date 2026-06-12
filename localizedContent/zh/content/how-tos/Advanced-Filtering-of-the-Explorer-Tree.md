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

从 [2.7.4](https://github.com/TabularEditor/TabularEditor/releases/tag/2.7.4) 起，Tabular Editor 允许你决定筛选器如何应用于层级结构中的对象，以及搜索结果的显示方式。 这通过紧挨着“Filter”按钮右侧的三个工具栏按钮来控制： 这通过紧挨着“Filter”按钮右侧的三个工具栏按钮来控制：

![image](https://user-images.githubusercontent.com/8976200/46567931-08a4b480-c93d-11e8-96fd-e197e87a0587.png)

- ![image](https://user-images.githubusercontent.com/8976200/46567944-44d81500-c93d-11e8-91e2-d9822078dba7.png) **按父级分层**：搜索将应用于 _父级_ 对象，即表和显示文件夹（如已启用）。 当父级项匹配搜索条件时，将显示其所有子项。 当父级项匹配搜索条件时，将显示其所有子项。
- ![image](https://user-images.githubusercontent.com/8976200/46567940-2ffb8180-c93d-11e8-9fba-84fbb79b6bb3.png) **按子级分层**：搜索将应用于 _子级_ 对象，即度量值、列、层级结构等。 父级对象仅在其至少有一个子对象匹配搜索条件时才会显示。 父级对象仅在其至少有一个子对象匹配搜索条件时才会显示。
- ![image](https://user-images.githubusercontent.com/8976200/46567941-37bb2600-c93d-11e8-9c02-86502f41bce8.png) **扁平**：搜索将应用于所有对象，结果以扁平列表显示。 包含子项的对象仍会以分层方式显示其子项。 包含子项的对象仍会以分层方式显示其子项。

## 简单搜索

在“Filter”文本框中输入任意内容，然后按 [Enter]，即可在对象名称中进行不区分大小写的简单搜索。 例如，在“Filter”文本框中输入“sales”，并使用“按父级”筛选模式，会得到如下结果： 例如，在“Filter”文本框中输入“sales”，并使用“按父级”筛选模式，会得到如下结果：

![image](https://user-images.githubusercontent.com/8976200/46568002-5f5ebe00-c93e-11e8-997b-7f89dfd92076.png)

展开任意表，你就能看到该表的所有度量值、列、层级结构和分区。 如果你把筛选模式改为“按子级”，结果会是这样：

![image](https://user-images.githubusercontent.com/8976200/46568016-9f25a580-c93e-11e8-9bc2-c0a16a890256.png)

注意，“Employee”表现在也出现在列表中，因为它有几个子项（本例中是列）包含“sales”这个词。

## 通配符搜索

在“筛选”文本框中输入字符串时，可使用通配符 `?` 表示任意单个字符，使用 `*` 表示任意长度的字符序列（可为空）。 因此，输入 `*sales*` 会得到与上面完全相同的结果；但输入 `sales*` 只会显示名称以“sales”开头的对象（同样不区分大小写）。

按父级搜索 `sales*`：

![image](https://user-images.githubusercontent.com/8976200/46568043-19eec080-c93f-11e8-8d81-2a6214bfa572.png)

按子级搜索 `sales*`：

![image](https://user-images.githubusercontent.com/8976200/46568117-f9733600-c93f-11e8-96ab-f87769b8097c.png)

平铺模式下搜索 `sales*`（按 [Ctrl]+[F1] 切换信息列，以显示每个对象的详细信息）：

![image](https://user-images.githubusercontent.com/8976200/46568118-042dcb00-c940-11e8-82d1-516207450559.png)

通配符可以放在字符串中的任意位置，并且你可以按需使用多个。 如果这还不够复杂，继续往下看……

## 动态 LINQ 搜索

你还可以使用 [Dynamic LINQ](https://github.com/kahanu/System.Linq.Dynamic/wiki/Dynamic-Expressions) 来搜索对象，这和你创建 [Best Practice Analyzer 规则](/Best-Practice-Analyzer) 时做的一样。 要在筛选框中启用动态 LINQ 模式，只需在搜索字符串前加上 `:`（冒号）。 例如，要查看所有名称以“Key”结尾的对象（区分大小写），请输入： 要在筛选框中启用动态 LINQ 模式，只需在搜索字符串前加上 `:`（冒号）。 例如，要查看所有名称以“Key”结尾的对象（区分大小写），请输入：

```
:Name.EndsWith("Key")
```

……然后按下 [Enter]。 在“平铺”筛选模式下，结果如下：

![image](https://user-images.githubusercontent.com/8976200/46568130-33dcd300-c940-11e8-903c-193e1acde0ad.png)

在动态 LINQ 中进行不区分大小写的搜索，你可以先用类似下面的方式转换输入字符串：

```
:Name.ToUpper().EndsWith("KEY")
```

或者也可以传入 [StringComparison](https://docs.microsoft.com/en-us/dotnet/api/system.string.endswith?view=netframework-4.7.2#System_String_EndsWith_System_String_System_StringComparison_) 参数，例如：

```
:Name.EndsWith("Key", StringComparison.InvariantCultureIgnoreCase)
```

你不必只在对象名称中进行搜索。 你不必只在对象名称中进行搜索。 动态 LINQ 的搜索字符串可以按需写得很复杂，用于匹配对象的任意属性（以及子属性）。 因此，如果你想找出所有表达式中包含“TODO”一词的对象，可以使用以下筛选条件： 因此，如果你想找出所有表达式中包含“TODO”一词的对象，可以使用以下筛选条件：

```
:Expression.ToUpper().Contains("TODO")
```

再举一例，下面将显示模型中所有未被任何其他对象引用的隐藏度量值：

```
:ObjectType="Measure" and (IsHidden or Table.IsHidden) and ReferencedBy.Count=0
```

你也可以使用正则表达式。 你也可以使用正则表达式。 下面会查找所有名称包含“Number”或“Amount”的列：

```
:ObjectType="Column" and RegEx.IsMatch(Name,"(Number)|(Amount)")
```

注意：显示选项（树形视图正上方的工具栏按钮）可能会在使用“按父项”和“按子项”筛选模式时影响结果。 例如，上面的 LINQ 筛选器只返回列，但如果你的显示选项当前设置为不显示列，那么就不会显示任何内容。
