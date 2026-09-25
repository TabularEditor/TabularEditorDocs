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

The TOM hierarchy uses inheritance. `Column` is an abstract base with subtypes `DataColumn`, `CalculatedColumn` and `CalculatedTableColumn`. `Table` has subtypes `CalculatedTable` and `CalculationGroupTable`. Use the base type when working with shared properties like `Name`, `Description`, `IsHidden`, `FormatString` or `DisplayFolder`. Cast to a concrete subtype when you need type-specific properties, such as `Expression` on `CalculatedColumn` or `SourceColumn` on `DataColumn`.

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
> 在 Tabular Editor 2 中，带变量声明的模式匹配（`col is CalculatedColumn cc`）需要 Roslyn 编译器。 Configure it under **File > Preferences > General > Compiler path**. See [Compiling with Roslyn](xref:advanced-scripting#compiling-with-roslyn) for details. Tabular Editor 3 supports this by default.

## 类型层次结构

TOMWrapper 中的关键继承关系如下：

| 基类型                                                                                                             | 子类型                                                                                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (xref:TabularEditor.TOMWrapper.Column)       | (xref:TabularEditor.TOMWrapper.DataColumn), (xref:TabularEditor.TOMWrapper.CalculatedColumn), (xref:TabularEditor.TOMWrapper.CalculatedTableColumn)     |
| (xref:TabularEditor.TOMWrapper.Table)        | (xref:TabularEditor.TOMWrapper.CalculatedTable), (xref:TabularEditor.TOMWrapper.CalculationGroupTable)                                                                                                                     |
| 分区 (xref:TabularEditor.TOMWrapper.Partition) | 分区子类型：(xref:TabularEditor.TOMWrapper.MPartition), (xref:TabularEditor.TOMWrapper.EntityPartition), (xref:TabularEditor.TOMWrapper.PolicyRangePartition) |
| (xref:TabularEditor.TOMWrapper.DataSource)   | (xref:TabularEditor.TOMWrapper.ProviderDataSource), (xref:TabularEditor.TOMWrapper.StructuredDataSource)                                                                                                                   |

## 按类型筛选集合

`OfType<T>()` 可用于任何集合，并返回一个经过筛选的序列，其中只包含指定类型的项。 It returns an empty sequence if no items match.

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

Pattern matching does two things: it checks whether a value is a given type and optionally casts it into a new variable. `x is Type xx` 这种形式会判断“`x` 是否为 `Type` 类型？”，如果为真，就会将 `xx` 作为该确切类型的变量供你使用。

这等同于：

```csharp
if (col is CalculatedColumn)
{
    var cc = (CalculatedColumn)col; // explicit cast
    // use cc...
}
```

如果你只需要布尔判断，使用不带变量的 `x is Type`。 If you also need subtype-specific properties, use `x is Type xx`.

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

In BPA rules, type filtering is handled by the rule's **Applies to** scope. Set it to the target object type (e.g., **Calculated Columns**) rather than filtering by type in the expression. Dynamic LINQ 不支持 C# 风格的类型转换。

## 常见陷阱

> [!IMPORTANT]
>
> - `Column` 是抽象类型，但你无需进行类型转换，也可以访问基类型上定义的所有属性（`Name`、`DataType`、`FormatString`、`IsHidden`、`Description`、`DisplayFolder`）。 Only cast to a subtype when you need subtype-specific properties like `Expression` on `CalculatedColumn`.
> - `OfType<T>()` both filters and casts. `Where(x => x is T)` 只会筛选，结果仍然是基类型。 Prefer `OfType<T>()` when you need access to subtype properties.
> - 计算表格的列会自动管理。 Edit the calculated table's `Expression` to add or change columns. You cannot add them directly.

## 另请参阅

- @C# 脚本
- @using-bpa-sample-rules-expressions
- @how-to-navigate-tom-hierarchy
- @how-to-tom-interfaces
