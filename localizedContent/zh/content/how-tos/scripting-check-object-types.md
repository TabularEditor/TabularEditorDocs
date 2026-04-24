---
uid: how-to-check-object-types
title: 如何检查对象类型
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何检查对象类型

TOM 层级结构采用继承机制。 `Column` 是一个抽象基类，其子类型包括 `DataColumn`、`CalculatedColumn` 和 `CalculatedTableColumn`。 `Table` 的子类型包括 `CalculatedTable` 和 `CalculationGroupTable`。 在处理 `Name`、`Description`、`IsHidden`、`FormatString` 或 `DisplayFolder` 等共享属性时，请使用基类型。 当需要特定类型的属性时，请将其强制转换为具体子类型，例如 `CalculatedColumn` 的 `Expression` 或 `DataColumn` 的 `SourceColumn`。

## 快速参考

```csharp
// Pattern matching -- checks type AND casts in one step
if (col is CalculatedColumn cc)
    Info(cc.Expression);  // Expression is only on CalculatedColumn, not base Column

// Filter a collection by type
var calcCols = Model.AllColumns.OfType<CalculatedColumn>();
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// Runtime type name (use only for display/logging, not for logic)
var typeName = obj.GetType().Name;   // "DataColumn", "Measure", etc.
```

> [!NOTE]
> 在 Tabular Editor 2 中，带变量声明的模式匹配（`col is CalculatedColumn cc`）需要 Roslyn 编译器。 在 **File > 偏好 > General > Compiler path** 下进行配置。 详情请参阅 [使用 Roslyn 编译](xref:advanced-scripting#compiling-with-roslyn)。 Tabular Editor 3 默认支持此功能。 在 **File > 偏好 > General > Compiler path** 下进行配置。 详情请参阅 [使用 Roslyn 编译](xref:advanced-scripting#compiling-with-roslyn)。 Tabular Editor 3 默认支持此功能。

## 类型层次结构

TOMWrapper 中的关键继承关系如下：

| 基类型                                                                                                             | 子类型                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (xref:TabularEditor.TOMWrapper.Column)       | (xref:TabularEditor.TOMWrapper.DataColumn), (xref:TabularEditor.TOMWrapper.CalculatedColumn), (xref:TabularEditor.TOMWrapper.CalculatedTableColumn)     |
| (xref:TabularEditor.TOMWrapper.Table)        | (xref:TabularEditor.TOMWrapper.CalculatedTable), (xref:TabularEditor.TOMWrapper.CalculationGroupTable)                                                                                                                     |
| 分区 (xref:TabularEditor.TOMWrapper.Partition) | 分区子类型：(xref:TabularEditor.TOMWrapper.MPartition), (xref:TabularEditor.TOMWrapper.EntityPartition), (xref:TabularEditor.TOMWrapper.PolicyRangePartition) |
| (xref:TabularEditor.TOMWrapper.DataSource)   | (xref:TabularEditor.TOMWrapper.ProviderDataSource), (xref:TabularEditor.TOMWrapper.StructuredDataSource)                                                                                                                   |

## 按类型筛选集合

`OfType<T>()` 可用于任何集合，并返回一个经过筛选的序列，其中只包含指定类型的项。 如果没有匹配项，它会返回空序列。 如果没有匹配项，它会返回空序列。

```csharp
// All calculated columns in the model (empty if model has none)
var calculatedColumns = Model.AllColumns.OfType<CalculatedColumn>();

// All M partitions (Power Query)
var mPartitions = Model.AllPartitions.OfType<MPartition>();

// All calculation group tables
var calcGroups = Model.Tables.OfType<CalculationGroupTable>();

// All regular tables (exclude calculation groups and calculated tables)
var regularTables = Model.Tables.Where(t => t is not CalculationGroupTable && t is not CalculatedTable);
```

## 使用 is 进行模式匹配

模式匹配会做两件事：检查某个值是否为给定类型，并可选择将其转换后赋给一个新变量。 模式匹配会做两件事：检查某个值是否为给定类型，并可选择将其转换后赋给一个新变量。 `x is Type xx` 这种形式会判断“`x` 是否为 `Type` 类型？”，如果为真，就会将 `xx` 作为该确切类型的变量供你使用。

这等同于：

```csharp
if (col is CalculatedColumn)
{
    var cc = (CalculatedColumn)col; // explicit cast
    // use cc...
}
```

如果你只需要布尔判断，使用不带变量的 `x is Type`。 如果你还需要访问子类型特有的属性，用 `x is Type xx`。 如果你还需要访问子类型特有的属性，用 `x is Type xx`。

```csharp
foreach (var col in Model.AllColumns)
{
    // Expression is only available on CalculatedColumn, not the base Column type
    if (col is CalculatedColumn cc)
        Info($"{cc.Name}: {cc.Expression}");
    else if (col is DataColumn dc)
        Info($"{dc.Name}: data column in {dc.Table.Name}");
}
```

## Dynamic LINQ 中的等效写法

在 BPA 规则中，类型筛选是通过规则的 **Applies to** 范围来处理的。 把它设置为目标对象类型（例如 **计算列**），不要在表达式中按类型筛选。 在 BPA 规则中，类型筛选是通过规则的 **Applies to** 范围来处理的。 把它设置为目标对象类型（例如 **计算列**），不要在表达式中按类型筛选。 Dynamic LINQ 不支持 C# 风格的类型转换。

## 常见陷阱

> [!IMPORTANT]
>
> - `Column` 是抽象类型，但你无需进行类型转换，也可以访问基类型上定义的所有属性（`Name`、`DataType`、`FormatString`、`IsHidden`、`Description`、`DisplayFolder`）。 只有在你需要子类型特有的属性（例如 `CalculatedColumn` 上的 `Expression`）时，才将其转换为该子类型。 只有在你需要子类型特有的属性（例如 `CalculatedColumn` 上的 `Expression`）时，才将其转换为该子类型。
> - `OfType<T>()` 会同时进行筛选和类型转换。 `OfType<T>()` 会同时进行筛选和类型转换。 `Where(x => x is T)` 只会筛选，结果仍然是基类型。 当你需要访问子类型属性时，优先使用 `OfType<T>()`。 当你需要访问子类型属性时，优先使用 `OfType<T>()`。
> - 计算表格的列会自动维护。 要添加或更改列，就编辑计算表格的 `Expression`。 你不能直接添加这些列。

## 另见

- @C# 脚本
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-tom-interfaces
