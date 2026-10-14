---
uid: udfs
title: DAX 用户自定义函数
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
    - product: Tabular Editor 3
      since: 3.23.0
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# DAX 用户自定义函数

语义模型支持 DAX 用户自定义函数（DAX UDF）。该功能在 Power BI Desktop 2025 年九月更新中进入预览，并自 Power BI 于 2026 年六月发布以来[正式发布](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738)。

DAX UDF 是一种可重用的 DAX 函数，你可以在模型中的任何 DAX 表达式中调用它，包括在其他函数中。如需了解 Tabular Editor 3 中 DAX UDF 的入门内容，请参阅这篇博客文章 [如何开始在 Tabular Editor 3 中使用 UDF](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3)。

## 理解 DAX UDF

DAX UDF 包含一个参数列表，以及一个根据这些参数计算结果的 DAX 表达式。参数可以是标量值、表或对模型对象的引用；结果可以是标量值或表。

想详细了解 DAX UDF 的工作原理，可以看看 SQLBI 的这篇文章 [DAX 中的用户自定义函数简介](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/)。

## 前提条件

DAX UDF 要求模型的兼容级别为 **1702 或更高**。

## 创建第一个 DAX UDF

### 第 1 步：设置模型

检查模型的兼容级别：

1. 在 Tabular Editor 3 中打开模型。
2. 在 **TOM Explorer** 中选择根节点（**Model**）。
3. 在 **Properties** 窗格中，展开 **Database** 属性，然后确认 **兼容级别** 为 **1702** 或更高。
4. 如果低于该值，请更新兼容级别并保存模型。

![设置兼容级别](~/content/assets/images/tutorials/udfs-cl1702.png)

### 步骤 2：添加新函数

1. 在 **TOM Explorer** 中，找到模型下的 **Functions** 文件夹。
2. 右键单击 **Functions** 文件夹。
3. 选择 **Create > User-Defined Function**。
4. 为函数命名。名称可以包含下划线和句点，但不能包含空格或其他特殊字符。

![创建 DAX UDF](~/content/assets/images/tutorials/new-udf.png)

通过 **Model > Add User-Defined Function** 也可以添加 DAX UDF。

你也可以在 DAX 查询的 **DEFINE** 部分，通过 **Query > Apply**（**F7**）创建 DAX UDF。如果你只想应用查询中的部分定义，选中它们后按 **F8**（**Apply Selection**）。

![从 DAX 查询创建 DAX UDF](~/content/assets/images/tutorials/udf-from-query.png)

### 步骤 3：定义你的函数

在 **表达式编辑器** 中输入函数定义，例如下面这个将两个数字相加的函数：

```dax
// Adds two numbers together
(
    x, // The first number
    y  // The second number
)
=> x + y
```

> [!TIP]
> 表达式编辑器中的 **Use correct UDF syntax** 代码操作会将表达式重写为有效的 DAX UDF 语法。

## DAX UDF 语法与结构

### 基本语法

DAX UDF 定义采用以下结构：

```dax
FUNCTION FunctionName =
    // Optional comment describing the function
    (
        parameter1, // Parameter description
        parameter2, // Parameter description
        // ... more parameters
    )
    => expression_using_parameters
```

### 参数求值模式

每个参数要么是 **按值传递**，要么是 **按引用传递**；除非另有指定，否则默认为按值传递。

按值传递的参数的行为类似于使用 `VAR` 定义的 DAX 变量：调用函数时，参数只会计算一次，函数内部对该参数的每次引用都会返回该值。

按引用传递的参数的行为类似于度量值：函数内部对该参数的每次引用都会在其出现位置的评估语境中进行计算。

在参数名称后加上冒号 (`:`) 来设置模式，后接 `VAL`（按值传递）或 `EXPR`（按引用传递）；如果省略不写，则参数默认为 `VAL`：

```dax
(
    x: VAL,   // Pass-by-value parameter - the DAX expression is evaluated once when the function is called, and the result is "copied" into the function
    y: EXPR   // Pass-by-reference parameter - can be any DAX expression which will observe whatever context the parameter is later referenced under
)
=>
ROW(
    "x", x,
    "x modified", CALCULATE(x, Product[Color] = "Red"),
    "y", y, 
    "y modified", CALCULATE(y, Product[Color] = "Red")
)
```

如果调用此函数时，两个参数都传入相同的度量值引用，例如 `MyFunction([Some Measure], [Some Measure])`，那么只有 `y` 的结果会随筛选语境而变化：

![按值传递 vs 按引用传递](~/content/assets/images/tutorials/udf-pass-by-ref.png)

如需约束可选的参数类型，请在评估模式前加上数据类型，例如 `x: INT64 VAL` 或 `y: TABLE EXPR`。如果指定了类型，参数会隐式转换为该类型，Tabular Editor 3 还会在编写调用该函数的代码时，根据该类型提供自动补全建议。

Tabular Editor 3 会根据声明的参数类型验证实参。如果调用 DAX UDF 时传入的参数与其参数类型不匹配，例如在需要 `TABLEREF` 参数的位置传入标量值，Semantic Analyzer 会 Report 警告或错误。

有关完整的约束列表，请参阅 [Microsoft 的 DAX UDF 规范](https://learn.microsoft.com/dax/best-practices/dax-user-defined-functions)。

### 带默认表达式的可选参数

Tabular Editor 3.26.2 及更高版本支持带默认表达式的可选参数。如需将参数设为可选，请在参数名称以及任何类型或评估模式提示之后追加 `= expression`。如果调用方省略该参数，则会使用默认表达式提供该值。

```dax
FUNCTION AddTax =
    (
        amount: NUMERIC,        // Required parameter
        taxRate: NUMERIC = 0.1  // Optional parameter, defaults to 10%
    )
    => amount * (1 + taxRate)
```

调用 `AddTax(10)` 会返回 `11`，而 `AddTax(10, 0.25)` 会返回 `12.5`。

可选参数遵循以下规则：

- 调用者可以将某个实参留空，以使用其默认值。例如，`MyFunc(1,,3)` 省略了第二个实参。最少参数个数由最右侧必需参数的位置决定。
- 默认表达式只能引用函数定义位置可见的名称（列、表、度量值、函数），且不能引用同一函数的其他参数。
- 只有在使用默认表达式时，才会根据参数的类型提示强制进行类型检查；如果显式传入参数，则会检查传入的实参是否符合该提示。

## 在模型中使用 DAX UDF

### 在对象表达式中

你可以在模型中的任何 DAX 表达式中调用 DAX UDF，并且在你输入时，自动补全会提示 DAX UDF。

### 在 DAX脚本中

DAX 脚本可以通过 **DEFINE** 定义并调用 DAX UDF：

```dax
-- Function: MyFuncRenamed
FUNCTION MyFuncRenamed =
    // Adds two numbers together
    (
        x: INT64, // The first number
        y: INT64  // The second number
    )
    => x + y

-- Measure: [New Measure]
MEASURE 'Date'[New Measure] = MyFuncRenamed(1,2)
```

### 在 DAX 查询中

除了将查询的 **DEFINE** 部分中的 DAX UDF 应用到模型之外，你还可以在 DAX 查询中右键单击函数调用，然后选择 **Define Function**，将函数定义添加到 **DEFINE** 部分：

![从查询中执行 Define Function](~/content/assets/images/tutorials/udf-define.png)

DAX UDF 调用的右键菜单包含以下命令：

- **窥视定义** (**Alt+F12**)：在光标下方打开一个只读编辑器，显示函数定义。
- **转到定义** (**F12**)：如果当前查询或脚本定义了该函数，则在编辑器中转到该函数定义；否则转到 **函数** 文件夹中的该函数。
- **Inline Function**：用函数主体替换该调用，并将参数替换为对应的实参。
- **Define Function**（仅适用于 DAX 脚本和 DAX 查询）：如果 **DEFINE** 部分中还没有该函数定义，就会将其添加进去。
- **Define Function with dependencies**（仅适用于 DAX 脚本和 DAX 查询）：还会添加该函数所调用的 DAX UDF 的定义。

## DAX 组件管理器

[DAX 组件管理器](xref:dax-package-manager)在 Tabular Editor 3.24.0 及更高版本中可用，可用于查找、安装和管理 DAX UDF 库，并支持 [DaxLib](https://daxlib.org) 订阅源。

系统管理员可以通过指定 [组策略](xref:policies) 来禁用对 DAX 组件管理器的访问。

## 高级功能

### 公式自动修正

当你重命名某个 DAX UDF 时，Tabular Editor 3 会像处理度量值和其他对象一样，更新模型中所有对它的引用。

### 窥视定义

**窥视定义**无需离开当前文档，即可在光标下方显示 DAX UDF 的定义。

![DAX UDF 的窥视定义](~/content/assets/images/tutorials/udf-peek-definition.png)

### 依赖项视图

对于 DAX UDF，**DAX 依赖关系**视图（**Shift+F12**）会显示：

- **依赖该函数的对象**：调用该函数的度量值、列和其他对象
- **该函数依赖的对象**：该函数引用的度量值、列和其他对象

### 批量重命名

TOM Explorer 的右键菜单中的 **批量重命名**（**F2**）可借助搜索和替换模式以及可选的正则表达式，一次重命名多个选中的 DAX UDF。

### 命名空间

DAX 没有命名空间，因此给 DAX UDF 取名时，要使用含义明确且能表明函数来源的名称，并用 `.` 作为命名空间分隔符，例如 `DaxLib.Convert.CelsiusToFahrenheit`。 TOM Explorer 会以层级结构显示按这种方式命名的 DAX UDF。要打开或关闭该层级结构，请使用 TOM Explorer 上方工具栏中的 **Group User-Defined Functions by namespace**。该按钮只会在兼容级别为 1702 或更高的模型中显示。

![按命名空间分组的 DAX UDF](~/content/assets/images/udf-namespaces-tom-explorer.png)

每个 DAX UDF 还有一个 `Namespace` 属性，可在不更改其名称的情况下设置它在 TOM Explorer 层级结构中的位置，类似于度量值的显示文件夹。例如，如果你通过批量重命名去掉名称中的命名空间，可以设置 `Namespace`，让它们在 TOM Explorer 中继续保持分组。

> [!NOTE]
> `Namespace` 属性不会影响 DAX 代码，因此调用 DAX UDF 时，要使用其完整名称，包括所有命名空间部分。

## DAX UDF 与源代码管理

如果你将模型存储为文件夹结构，Tabular Editor 可以将每个 DAX UDF 写入各自的文件。如果不使用这种序列化级别，所有函数都会存储在 `Database.json` 中，而对不同函数的并行编辑可能会在该文件中产生冲突。

在 **模型 > 序列化选项...** 下选择 **用户定义函数（UDFs）** 级别。对于首次保存到文件夹的模型，请在 **Tools > 偏好 > File Formats > Save-to-folder** 下选择该序列化级别（参见 [保存到文件夹](xref:save-to-folder#user-defined-functions-udfs)）。

## 最佳实践

### 命名规范

- 使用能说明函数用途的名称
- 用组织的首字母缩写作为 DAX UDF 的前缀，例如 `ACME.CalculateDiscount`
- 使用带分隔符（`.` 或 `_`）的复合名称，例如 `Finance.CalcProfit` 或 `My_CalcProfit`。复合名称不会与 Microsoft 日后新增的内置 DAX 函数发生冲突。参见 [内置 BPA 规则](xref:kb.bpa-udf-use-compound-names)

### 文档

- 添加注释，说明该函数的作用
- 记录每个参数的用途以及预期的数据类型
- 在注释中提供用法示例

```dax
// Calculates the percentage change between two values
// Usage: PercentChange(100, 110) returns 0.10 (10% increase)
(
    oldValue: DOUBLE,    // The original value
    newValue: DOUBLE     // The new value to compare against
)
=> DIVIDE(newValue - oldValue, oldValue)
```

Tabular Editor 3 会在自动补全建议和工具提示中显示这些注释。

![带注释的 DAX UDF 自动补全](~/content/assets/images/tutorials/udf-comment-tooltips.png)

## 常见使用场景

### 数学运算

```dax
// Calculate compound interest
(
    principal: DOUBLE,
    rate: DOUBLE,
    periods: INT64
)
=> principal * POWER(1 + rate, periods)
```

### 字符串处理

```dax
// Format a full name from first and last name components
(
    firstName: STRING,
    lastName: STRING
)
=> TRIM(firstName) & " " & TRIM(lastName)
```

### 日期计算

```dax
// Get the fiscal year based on a date (fiscal year starts July 1)
(
    inputDate: DATETIME
)
=> IF(MONTH(inputDate) >= 7, YEAR(inputDate) + 1, YEAR(inputDate))
```

### 业务逻辑

```dax
// Apply tiered discount based on quantity
(
    quantity: INT64
)
=> SWITCH(
    TRUE(),
    quantity >= 100, 0.15,
    quantity >= 50,  0.10,
    quantity >= 25,  0.05,
    0
)
```

## 故障排查

### 常见问题

**函数未出现在自动补全中**

按顺序检查以下各项：

1. 如果函数定义存在语义错误，例如缺少行语境或 `MATCHBY` 无效，则自动补全会隐藏该函数，但仍会显示其调用提示。修复函数中的错误。
2. 只有当 DAX UDF 的返回类型适用于你当前正在补全的参数时，自动补全才会显示它。返回类型会根据函数体推断：返回表的函数不会在需要标量的位置显示，反之亦然。例外：
   - 筛选器参数，例如 [`CALCULATE`](https://dax.guide/calculate) 的第二个及后续参数，可以接受以下任一项
   - 函数体为未类型化的 `EXPR` 参数的函数会在所有位置提供
3. Visual 计算 DAX UDF 仅会在 Visual 计算中出现，其他 DAX UDF 则只会在其外部出现。
4. 在函数自身的定义中，不会提示该函数。

**参数约束错误**

- 检查你指定的参数类型
- 检查实参是否与参数类型匹配
- 查看 Microsoft 文档，了解支持的约束类型

**部署后函数无法正常工作**

- 检查目标是否支持 DAX UDF，而 Power BI Service 自 2026 年六月版本起支持它们（请参阅[限制](#limitations)）。

## 限制

- DAX UDF 需要 1702 或更高的兼容级别。 Azure Analysis Services 和 SQL Server Analysis Services 不支持 DAX UDF。
- DAX UDF 不能递归（调用自身）。

> [!NOTE]
> 带默认表达式的可选参数随 DAX UDF 在 2026 年六月[正式可用](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738)时一同推出。 3.26.2 之前的 Tabular Editor 3 版本会将默认表达式语法误报为错误。
