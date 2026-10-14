---
uid: object-properties-functions
title: 函数和集的属性
author: Jeroen ter Heerdt
updated: 2026-10-05
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "支持函数和集合，但不支持 Namespace、PackageId 或 PackageVersion"
    - product: Tabular Editor 3
      since: 3.23.0
      note: "用户定义函数需要 3.23.0 或更高版本。所有版本均支持集合。"
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 函数和集的属性

<!--
SUMMARY: Reference for the properties of DAX user-defined functions and of sets.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页列出了 DAX 用户定义函数和集的属性。有关大多数对象共有的属性，参见 @object-properties-common。

## 函数

用户定义函数 (UDF) 是一种可重用的 DAX 函数，只需在模型中定义一次，就可以在任何 DAX 表达式中调用，包括其他函数。它接受参数，参数可以是值、表，或对列和度量值的引用，并返回一个值或一张表。 UDF 属于模型，**TOM Explorer** 会在 **Functions** 文件夹下列出它们。

UDF 需要 1702 或更高的兼容级别。 Azure Analysis Services 和 SQL Server Analysis Services 不支持它们。完整介绍参见 @udfs。

Tabular Editor 2 也支持 UDF，并会在 **Functions** 文件夹下列出它们。要在 Tabular Editor 2 中添加一个，请右键单击该文件夹，然后选择 **New User-Defined Function**。 Tabular Editor 2 没有 `Namespace`、`PackageId` 和 `PackageVersion` 属性。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [隐藏](xref:object-properties-common#hidden)
- [批注](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [已更改的属性](xref:object-properties-common#changed-properties)
- [错误消息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [Source Lineage tag](xref:object-properties-common#source-lineage-tag)

在 DAX 中，你是通过函数名来调用函数的，因此名称中不能包含空格。可以包含点号和下划线。使用 `Finance.Margin` 或 `ACME_Margin` 之类的复合名称，以避免与 Microsoft 日后新增的内置 DAX 函数发生冲突。参见 @kb.bpa-udf-use-compound-names。当你重命名函数时，Tabular Editor 3 会更新整个模型中对该函数的所有引用，效果与 @formula-fix-up-dependencies 处理度量值和列时相同。

### 命名空间

`Namespace` · 字符串 · 基本 · _存储为批注_ (`TE_Group`)

启用按命名空间对用户定义函数分组后，该函数会显示在 @tom-explorer-view 中对应的组下。使用 **TOM Explorer** 上方的切换按钮启用分组。 Tabular Editor 按以下顺序确定命名空间：

1. 如果函数具有 `TE_Group` 批注，则该值就是命名空间
2. 否则，如果函数名称包含点号，命名空间就是最后一个点号之前的部分，因此 `DaxLib.Convert.CelsiusToFahrenheit` 的命名空间是 `DaxLib.Convert`
3. 否则，如果函数具有 `DAXLIB_PackageId` 批注（参见 [PackageId](#packageid)），命名空间就是组件 ID
4. 否则，命名空间为空

无需重命名函数，也可以设置不同的命名空间。 Tabular Editor 会将其存储在函数的 `TE_Group` 批注中，并随模型一起保存。若要改回根据名称确定命名空间，请重置该属性或清除此值。和显示文件夹一样，命名空间只会在 **TOM Explorer** 中起组织作用；在 DAX 中，你始终使用函数的全名来调用它。

例如，如果你[批量重命名](xref:duplicate-and-batch)一组函数，去掉其名称中的 `DaxLib.Convert.` 前缀，可将它们的命名空间设置为 `DaxLib.Convert`，以便继续归为一组。

### PackageId

`PackageId` · 字符串 · 元数据 · 只读 · _作为注解存储_ (`DAXLIB_PackageId`)

函数所属 [DaxLib](https://daxlib.org) 组件的 ID，从该函数的 `DAXLIB_PackageId` 注解中读取。 DaxLib 组件会在其函数上添加此注解。只有当函数带有此注解时，**属性视图**才会显示 `PackageId` 和 `PackageVersion`，因此你自己编写的函数不会显示这两个属性。

Tabular Editor 3 中的 DAX 组件管理器在安装函数时会移除 `DAXLIB_` 注解，并通过扩展属性跟踪该组件，详见 [PackageVersion](#packageversion)。如果某个 DaxLib 组件中的函数在未通过 DAX 组件管理器的情况下被添加到模型中，你就会在这些函数上看到这些属性。见 @dax-package-manager。

### PackageVersion

`PackageVersion` · 字符串 · 元数据 · 只读 · _作为注解存储_ (`DAXLIB_PackageVersion`)

函数所属 DaxLib 组件的版本，从该函数的 `DAXLIB_PackageVersion` 注解中读取。

DAX 组件管理器不使用 `PackageId` 和 `PackageVersion`。它通过扩展属性跟踪已安装的组件。在模型级别，`TabularEditor_ModelDaxPkgTable` 和 `TabularEditor_ModelDaxPkgSeq` 列出已安装的组件。在每个函数上，`TabularEditor_ObjDaxPkgHandle` 记录该函数属于哪个组件，`TabularEditor_ObjDaxPkgContentHash` 记录该函数在安装时的表达式内容。如果你修改了来自某个组件的函数表达式，之后在更新或删除该组件时会出现提示，询问如何处理这个已更改的函数。

若要让 DAX 组件管理器停止跟踪某个函数，请删除它的 `TabularEditor_ObjDaxPkgHandle` 和 `TabularEditor_ObjDaxPkgContentHash` 这两个扩展属性。这样一来，删除该组件时就不会再删除该函数，而且该组件仍会显示为已安装。如果你之后更新或重新安装该组件，系统会针对与现有同名函数的冲突显示提示。如果你只删除 `TabularEditor_ObjDaxPkgContentHash`，该函数会被视为已更改，并且每次更新都会对此显示提示。 DAX 组件管理器文档警告，手动更改这些扩展属性可能导致意外行为。

### 表达式

`Expression` · 字符串 · 选项

以 Lambda 表示法编写的函数参数列表与主体：参数放在括号中，然后是 `=>`，再后面是使用这些参数的 DAX 表达式。例如：

```dax
// Returns the relative change between two values
(
    oldValue: NUMERIC,  // The original value
    newValue: NUMERIC   // The value to compare against
)
=> DIVIDE ( newValue - oldValue, oldValue )
```

每个参数都可以指定一种类型，例如 `NUMERIC`、`STRING` 或 `TABLE`，并设置求值模式。 `VAL` 是默认模式，会在函数运行前将参数求值一次，就像变量一样。 `EXPR` 传递的是表达式本身；它会在函数使用它的上下文中进行求值，就像度量值一样。带有 `= expression` 的参数为可选参数。完整语法请参见 @udfs。

调用函数时，Tabular Editor 3 会在自动完成建议和工具提示中显示表达式里的注释。

在 Tabular Editor 3 中，你可以在 @dax-scripts 文档中使用 `FUNCTION` 关键字，将函数与其他对象一起编辑。你也可以在 @dax-query 的 `DEFINE` 部分编写函数，并应用该查询将函数添加到模型中。

## Set

Set 隶属于某个表，并包含一个 DAX 表达式。 Tabular Object Model (TOM) 将其描述为 _计算集_。 Set 仅在兼容级别为 1400 或更高的 Power BI 和 Fabric 模型中受支持。在 Analysis Services 兼容模式的模型中，TOM 库会拒绝新建 Set，并返回错误 "is not supported at AnalysisServices mode"。

Set 不会显示在 **TOM Explorer** 中。要添加、编辑或删除表的 Set，选择该表，然后点击其 `Sets` 属性的 **...** 按钮（见 @object-properties-tables）。对于处于 Power BI 兼容模式且兼容级别为 1400 或更高的模型，**属性视图** 才会显示该属性。

<!-- TODO (not verifiable from TE3 source): what a Set is used for. TOM only describes it as a "calculated set" on a table with a DAX expression that can be static or dynamic. It looks like the equivalent of an MDX named set (for example for Excel PivotTables), but that isn't documented. Confirm with the TE/TOM team. -->

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [显示文件夹](xref:object-properties-common#display-folder)
- [隐藏](xref:object-properties-common#hidden)
- [注释](xref:object-properties-common#annotations)
- [扩展属性](xref:object-properties-common#extended-properties)
- [错误信息](xref:object-properties-common#error-message)
- [对象类型](xref:object-properties-common#object-type)
- [状态](xref:object-properties-common#state)
- [已翻译的显示文件夹](xref:object-properties-common#translated-display-folders)

### 表达式

`Expression` · 字符串 · 选项

定义该集合的 DAX 表达式。

<!-- TODO (not verifiable from TE3 source): what kind of DAX expression a set expects (a table expression that returns the members of the set?); add an example. TOM only says "The DAX expression that is evaluated for the calculated set." -->

### 动态

`IsDynamic` · 布尔值 · 选项

指定该集合是静态还是动态。静态集合只求值一次，其成员不会随查询中的筛选器而变化。动态集合会在每次查询时、在该查询的上下文中进行求值，其成员可能会随筛选器而变化。

<!-- TODO (not verifiable from TE3 source): the static/dynamic behavior. It's based on how named sets work in MDX; TOM only says "Indicates whether the set is static or dynamic". -->
