---
uid: how-to-work-with-expressions
title: 如何使用表达式和 DAX 属性
author: Morten Lønskov
updated: 2026-04-10
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 如何使用表达式和 DAX 属性

度量值、计算列、计算项、KPI 和分区都有各自的表达式。 本文介绍如何读取、修改和生成 DAX 表达式，以及如何使用 `IExpressionObject` 接口。

## 快速参考

```csharp
// Read and set expressions
measure.Expression                                    // DAX formula string
measure.Expression = "SUM('Sales'[Amount])";          // set formula
measure.FormatString = "#,##0.00";                    // static format
measure.FormatStringExpression = "...";               // dynamic format (DAX)

// Calculated column
calcCol.Expression                                    // DAX formula

// Partition (M query)
partition.Expression                                  // M/Power Query expression

// DAX object names for code generation
column.DaxObjectFullName    // 'Sales'[Amount]
column.DaxObjectName        // [Amount]
measure.DaxObjectFullName   // 'Sales'[Revenue]
measure.DaxObjectName       // [Revenue]
table.DaxObjectFullName     // 'Sales'
table.DaxTableName          // 'Sales'

// Formatting
FormatDax(measure);         // queue for formatting
CallDaxFormatter();         // execute queued formatting

// Tokenizing
measure.Tokenize().Count    // DAX token count (complexity metric)
```

## 读取和修改度量值表达式

```csharp
var m = Model.AllMeasures.First(m => m.Name == "Revenue");

// Read the current DAX
var dax = m.Expression;

// Replace a table reference in the expression
m.Expression = m.Expression.Replace("'Old Table'", "'New Table'");

// Set format string
m.FormatString = "#,##0.00";
```

## DAX 对象的名称属性

每个 `IDaxObject`（表、列、度量值、层次结构）都具有一些属性，用于以适当加引号的 DAX 安全格式返回其名称。

| 属性                  | 列示例               | 度量值示例       | 表示例       |
| ------------------- | ----------------- | ----------- | --------- |
| `DaxObjectName`     | `[Amount]`        | `[Revenue]` | `'Sales'` |
| `DaxObjectFullName` | `'Sales'[Amount]` | `[Revenue]` | `'Sales'` |
| `DaxTableName`      | `'Sales'`         | `'Sales'`   | `'Sales'` |

> [!NOTE]
> 对于度量值，`DaxObjectFullName` 返回与 `DaxObjectName`（不带限定符）相同的值。 在 DAX 中，度量值不需要表名限定。 对于列，`DaxObjectFullName` 包含表前缀。

生成 DAX 时，请使用以下属性以避免引号错误：

```csharp
// Generate a SUM measure for each selected column
foreach (var col in Selected.Columns)
{
    col.Table.AddMeasure(
        "Sum of " + col.Name,
        "SUM(" + col.DaxObjectFullName + ")",
        col.DisplayFolder
    );
}
```

## IExpressionObject 接口

包含表达式的对象会实现 (xref:TabularEditor.TOMWrapper.IExpressionObject) 接口。 在 Tabular Editor 2 中，此接口仅提供 `Expression` 属性。 在 Tabular Editor 3 中，该接口新增了 `GetExpression()`、`SetExpression()` 和 `GetExpressionProperties()`，用于在单个对象上处理多种表达式类型。

```csharp
// Tabular Editor 2: use the Expression property directly
measure.Expression = "SUM('Sales'[Amount])";
var dax = measure.Expression;
```

> [!NOTE]
> 下面的 `GetExpression`/`SetExpression` 模式仅在 Tabular Editor 3 中可用。 在 Tabular Editor 2 中，直接在对象上访问 `Expression` 属性。

```csharp
// Tabular Editor 3 only: list all expression types on an object
var exprObj = (IExpressionObject)measure;
foreach (var prop in exprObj.GetExpressionProperties())
{
    var expr = exprObj.GetExpression(prop);
    if (!string.IsNullOrEmpty(expr))
        Info($"{prop}: {expr}");
}

// Set an expression by type
exprObj.SetExpression(ExpressionProperty.Expression, "SUM('Sales'[Amount])");
exprObj.SetExpression(ExpressionProperty.FormatStringExpression, "\"$#,##0.00\"");
```

`ExpressionProperty` 枚举（仅限 Tabular Editor 3）包括：

| 值                        | 适用于         |
| ------------------------ | ----------- |
| `Expression`             | 度量值、计算列、计算项 |
| `DetailRowsExpression`   | 度量值         |
| `FormatStringExpression` | 度量值、计算项     |
| `TargetExpression`       | KPI         |
| `StatusExpression`       | KPI         |
| `TrendExpression`        | KPI         |
| `MExpression`            | M 分区        |

## 格式化 DAX

`FormatDax()` 会将对象加入格式化队列。 格式化会在脚本结束时自动执行。 仅当你需要在脚本执行中途获取格式化结果时，才调用 `CallDaxFormatter()`。

```csharp
// Typical usage -- formatting happens automatically after the script ends
foreach (var m in Model.AllMeasures)
    FormatDax(m);

// Advanced: force formatting mid-script to read the result
var before = Selected.Measure.Expression;
FormatDax(Selected.Measure);
CallDaxFormatter();                      // format NOW, not at script end
var after = Selected.Measure.Expression; // now contains the formatted DAX
```

## 令牌化

`Tokenize()` 会返回表达式中的 DAX 令牌。 令牌提供了一种不受空白字符和格式影响的可靠表示形式。 当你需要分析 DAX 表达式的结构，且分析需求超出内置依赖项跟踪和重命名功能所能提供的范围时，请使用令牌化。

```csharp
foreach (var m in Model.AllMeasures.OrderByDescending(m => m.Tokenize().Count))
    Info($"{m.Name}: {m.Tokenize().Count} tokens");
```

## 在表达式中查找和替换

使用 `Replace()` 进行字符串替换时，操作对象是原始表达式文本，包括字符串字面量和注释中的内容。 如果要有针对性地替换特定 DAX 构造（表引用、列引用），请改为分析令牌化后的表达式。

```csharp
// Replace a column reference across all measures
foreach (var m in Model.AllMeasures.Where(m => m.Expression.Contains("[Old Column]")))
{
    m.Expression = m.Expression.Replace("[Old Column]", "[New Column]");
}
```

## Dynamic LINQ 等效写法

在 BPA 规则表达式中，可直接通过上下文对象访问表达式属性。

| C# Script                                 | Dynamic LINQ (BPA)   |
| ----------------------------------------- | --------------------------------------- |
| `string.IsNullOrWhiteSpace(m.Expression)` | `String.IsNullOrWhitespace(Expression)` |
| `m.Expression.Contains("CALCULATE")`      | `Expression.Contains("CALCULATE")`      |
| `m.FormatString == ""`                    | `FormatString = ""`                     |
| `m.Expression.StartsWith("SUM")`          | `Expression.StartsWith("SUM")`          |

> [!TIP]
> 用 `Contains()` 或 `StartsWith()` 检查表达式内容时，记得使用不区分大小写的比较，以避免因格式差异而漏掉匹配项：`m.Expression.Contains("CALCULATE", StringComparison.OrdinalIgnoreCase)`。

## 常见陷阱

> [!IMPORTANT]
>
> - `DataColumn` 没有 `Expression` 属性。 只有 `CalculatedColumn`、`度量值`、`CalculationItem` 和 `分区` 具有表达式。 在 `DataColumn` 上访问 `Expression` 时，会因所处上下文不同而引发编译错误或运行时异常。
> - `DaxObjectName` 返回未限定名称（例如 `[Revenue]`），而 `DaxObjectFullName` 包含表名前缀（例如 `'Sales'[Revenue]`）。 在 DAX 中引用列时使用 `DaxObjectFullName`，在引用度量值且表限定可选时使用 `DaxObjectName`。
> - Tabular Editor 2 中的 `FormatDax()` 会调用外部的 daxformatter.com API，因此需要联网。 Tabular Editor 3 默认使用内置格式化程序。 要在 TE3 中使用 daxformatter.com，请在偏好中启用它。

## 另见

- @C# 脚本
- @using-bpa-sample-rules-expressions
- @how-to-filter-query-objects-linq
- @script-find-replace
