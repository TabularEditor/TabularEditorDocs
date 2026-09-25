---
uid: udfs
title: DAX 用户自定义函数
author: Daniel Otykier
updated: 2026-09-14
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

DAX User-Defined Functions (UDFs) are a capability of semantic models. The feature entered preview with the September 2025 update of Power BI Desktop and is [generally available](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) since the June 2026 release of Power BI.

The feature lets you create reusable DAX functions that you can invoke from within any DAX expression of your model, even other functions. 这个强大的功能可帮助你保持一致性、减少代码重复，并创建更易维护的 DAX 表达式。

Tabular Editor 3 自 3.23.0 版本起支持 UDFs。不过，我们建议使用 [3.23.1](xref:release-3-23-1)（或更高版本），以获得多项 bug 修复与改进。

如需更详细了解 Tabular Editor 3 中 UDF 的入门内容，请参阅[这篇博客文章](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3)。

## 理解 UDFs

你可以将 UDFs 理解为自定义 DAX 函数：定义一次，即可在整个模型中反复使用。 You define which parameters the function accepts, which can be both scalar- or table-valued, or even references to objects, and then you provide the DAX expression that uses those parameters to compute a result, which can also be scalar- or table-valued.

如需进一步了解 DAX UDF 的工作原理，我们推荐阅读 [SQLBI 的这篇文章](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/)。

## 前提条件

在 Tabular Editor 3 中创建和使用 UDFs 之前，确保满足以下条件：

- Your model compatibility level is **1702 or higher**.

## 创建你的第一个 UDF

### 第 1 步：设置模型

首先，确认你的模型兼容级别满足 UDF 的要求：

1. 在 Tabular Editor 3 中打开你的模型
2. 在 **TOM Explorer** 中选择根节点（“Model”）
3. 在 **Properties** 面板中，展开 **Database** 属性，然后确认 **兼容级别** 已设置为 **1702** 或更高
4. 如有需要，更新兼容级别并保存你的模型

![设置兼容级别](~/content/assets/images/tutorials/udfs-cl1702.png)

### 步骤 2：添加新函数

1. 在 **TOM Explorer** 中，找到模型下的 **Functions** 文件夹
2. 右键单击 **Functions** 文件夹
3. 选择 **Create > User-Defined Function**
4. 为函数取一个有描述性的名称（不允许空格和特殊字符；允许使用下划线和句点）

![创建 UDF](~/content/assets/images/tutorials/new-udf.png)

你也可以通过 **Model > Add User-Defined Function** 菜单选项添加 UDF。

另外，你也可以在 DAX 查询的 **DEFINE** 部分直接创建 UDF：按下 F7（Apply），或使用 **Query > Apply** 菜单选项。 If your query contains multiple query-scoped definitions, you can also select just a subset of them and hit F8 (Apply Selection).

![从 DAX 查询创建 UDF](~/content/assets/images/tutorials/udf-from-query.png)

### 步骤 3：定义你的函数

在 **表达式编辑器** 中，使用正确的 UDF 语法定义你的函数。

下面是一个将两个数字相加的基础示例：

```dax
// Adds two numbers together
(
    x, // The first number
    y  // The second number
)
=> x + y
```

> [!TIP]
> 如果你需要语法结构方面的帮助，可以在表达式编辑器中使用 **“Use correct UDF syntax”** 代码操作。

## UDF 语法与结构

### 基本语法

UDF 通常采用以下结构：

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

A key aspect of UDFs is that parameters can be defined in one of two modes, **pass-by-value** and **pass-by-reference**. By default, and unless you specify otherwise, a parameter will by **pass-by-value**. 这意味着该参数在 UDF 表达式内部的行为与 DAX 变量基本一致（即使用 `VAR` 关键字定义的变量）。 In other words, when the UDF is called, the parameter values are "copied" into the function and any reference to that parameter inside the function will always return the same value.

In contrast, **pass-by-reference** parameters behave more like measures. 也就是说，在函数内部对该参数进行求值的结果，可能会因评估语境不同而变化。

To specify the evaluation mode, include a parameter specification after the parameter name, separated by a colon (`:`). The specification can be either `VAL` or `EXPR` for "pass-by-value" and "pass-by-reference", respectively. As mentioned above, "pass-by-value" is the default, so `VAL` is implicit if not specified. For example:

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

在调用上述函数时，如果为每个参数都传入一个度量值引用，例如 `MyFunction([Some Measure], [Some Measure])`，则如下方截图所示，`y` 参数会根据当前筛选语境产生不同的结果：

![按值传递 vs 按引用传递](~/content/assets/images/tutorials/udf-pass-by-ref.png)

除了指定求值模式之外，你还可以通过在求值模式前指定数据类型来约束参数类型，例如 `x: INT64 VAL` 或 `y: TABLE EXPR`。

这些类型说明是可选的，但一旦指定，它们会对传入函数的参数执行隐式类型转换；同时，也会影响在 Tabular Editor 3 中编写调用该函数的 DAX 代码时的自动完成建议。

Tabular Editor 3 validates arguments against the declared parameter types. If you call a UDF with an argument that does not match its parameter type, for example passing a scalar value where a `TABLEREF` parameter is expected, the Semantic Analyzer reports a warning or error.

可用约束的完整列表，请参阅 [Microsoft 的 UDF 规范](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)。

### Optional Parameters with Default Expressions

Starting from version 3.26.2, Tabular Editor 3 supports optional parameters with default expressions. Append `= expression` after the parameter name (and after any type or evaluation-mode hints) to make the parameter optional. When the caller omits the argument, the default expression supplies the value.

```dax
FUNCTION AddTax =
    (
        amount: NUMERIC,        // Required parameter
        taxRate: NUMERIC = 0.1  // Optional parameter, defaults to 10%
    )
    => amount * (1 + taxRate)
```

Calling `AddTax(10)` returns `11`, while `AddTax(10, 0.25)` returns `12.5`.

A few rules govern optional parameters:

- Callers can leave an argument empty to fall back to its default, e.g. `MyFunc(1,,3)` omits the second argument. The minimum number of arguments is determined by the position of the rightmost required parameter.
- A default expression can only reference names (columns, tables, measures, functions) visible where the function is defined, and it can't reference another parameter of the same function.
- Type checking against a parameter's type hint is enforced only when the default expression is used; an explicitly passed argument is checked against the hint instead.

## 在模型中使用 UDF

### 在对象表达式中

创建 UDF 之后，你可以在整个模型中的任何 DAX 表达式里使用它。 Tabular Editor 3's autocomplete will suggest your UDFs as you type.

### 在 DAX脚本中

在使用 DAX脚本时，也可以使用 UDF：

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

Tabular Editor 3 新增了用于在 DAX 查询中使用 UDF 的强大功能。 We already mentioned above how you can "apply" a UDF from the **DEFINE** section of a DAX query, to have it become a permanent part of your model. In addition, if using a UDF inside a DAX query, you can right-click on the function invocation and choose **Define Function** to automatically generate the function definition in the **DEFINE** section of your query:

![从查询中执行 Define Function](~/content/assets/images/tutorials/udf-define.png)

从上方截图可以看出，在 UDF 调用处右键可使用以下选项：

- **窥视定义**（Alt+F12）：在当前光标位置下方打开一个嵌套的只读编辑器，显示该函数的定义
- **转到定义**（F12）：导航到模型中 **Functions** 文件夹内的函数定义；如果该函数是在当前查询或脚本中定义的，则导航到编辑器内的函数定义
- **Inline Function**：将函数调用替换为实际的函数定义，并将形参替换为传入函数的实际参数值
- **Define Function**（仅适用于 DAX 脚本或 DAX 查询）：如果查询的 **DEFINE** 部分还没有该函数定义，就会在其中生成函数定义
- **Define Function with dependencies**（仅适用于 DAX 脚本或 DAX 查询）：与上面类似，但还会为该函数依赖的其他 UDF 一并生成定义

## DAX 组件管理器

Tabular Editor 3.24.0 引入了一项名为 **DAX 组件管理器** 的新功能，让你可以直接在 Tabular Editor 中轻松发现、安装和管理 DAX UDF 库。 At launch, the package manager supports the popular [DaxLib](https://daxlib.org) feed, which contains a wide range of useful UDFs for various scenarios.

系统管理员可以通过指定 [组策略](xref:policies) 来禁用对 DAX 组件管理器的访问。

## 高级功能

### 公式修复

当你重命名某个 UDF 时，Tabular Editor 3 会像处理度量值和其他对象一样，自动更新模型中所有相关引用。

### 窥视定义

**窥视定义** 功能支持 UDF，让你无需离开当前上下文就能快速查看函数实现。

![UDF 的窥视定义](~/content/assets/images/tutorials/udf-peek-definition.png)

### 依赖项视图

UDF 会显示在 **DAX 依赖项**（Shift+F12）视图中，同时展示：

- **依赖该函数的对象**：哪些度量值、列等使用了该 UDF
- **该函数依赖的对象**：该 UDF 引用了哪些度量值、列等

### 批量重命名

在 TOM Explorer 中选择多个 UDF 后，你可以在右键上下文菜单中使用 **批量重命名** (F2)，通过“查找和替换”模式一次性为它们全部重命名，并可选择使用正则表达式。

### 命名空间

DAX 中并不存在“命名空间”的概念，但我们仍建议为 UDF 命名时尽量避免歧义，并清晰体现 UDF 的来源。 For example `DaxLib.Convert.CelsiusToFahrenheit` (using '.' as namespace separators). When a UDF is named this way, the TOM Explorer will display the UDF in a hierarchy based on the names. 你可以使用 TOM Explorer 上方工具栏中的 **Group User-Defined Functions by namespace** 切换按钮，按命名空间对 UDF 的显示进行分组（注意：仅当处理兼容级别为 1702 或更高的模型时，才会显示该按钮）。

![按命名空间分组的 DAX UDF](~/content/assets/images/udf-namespaces-tom-explorer.png)

In Tabular Editor, UDFs also have a "Namespace" _property_, allowing you to customize the namespace of each UDF individually, without changing the actual UDF object name. This is very similar to Display Folders for measures. 例如，如果你想对多个 UDF 执行批量重命名 (F2)，去掉名称中的命名空间，但仍希望它们在 TOM Explorer 中保持良好的层级组织，那么将“Namespace”属性设置为不同于可从 UDF 名称中推断出的值就会很有用。

> [!NOTE]
> Tabular Editor 里的这个组织功能不会影响 DAX 代码。 You still need to type out the full UDF name when calling a UDF, including any namespace parts.

## UDFs and source control

If you store your model as a folder structure, Tabular Editor can write each UDF to its own file instead of keeping them all inside `database.json`. Two developers editing two different functions then change two different files, and Git has nothing to merge.

Select the **User Defined Functions (UDFs)** level under **Model > Serialization options...**, or under **Tools > Preferences > File Formats > Save-to-folder** for a model you save to a folder for the first time. See [Save to folder](xref:save-to-folder#user-defined-functions-udfs).

## 最佳实践

### 命名规范

- 使用具有描述性的名称，清晰表明函数用途
- 可考虑用组织的首字母缩写作为 UDF 前缀（例如 `ACME.CalculateDiscount`）
- 避免使用过于通用的名称，以免与未来的 DAX 函数发生冲突
- Use compound names with a separator character (`.` or `_`). For example, `Finance.CalcProfit` or `My_CalcProfit`. This prevents your UDF from breaking if Microsoft introduces a built-in DAX function with the same name. See the [built-in BPA rule](xref:kb.bpa-udf-use-compound-names) for more details

### 文档

- 始终添加注释，说明该函数的作用
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

Tabular Editor 3 会自动识别所有注释，并在自动完成建议和工具提示中以合适的方式显示。

![带注释的 UDF 自动完成](~/content/assets/images/tutorials/udf-comment-tooltips.png)

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

Tabular Editor decides what to offer from the function's own definition and from where your cursor is. Work through these in order:

1. **The function's definition has a semantic error.** A UDF whose body does not analyze cleanly, one that needs a row context it has not been given or misuses `MATCHBY`, cannot be validly invoked, so it is left out of the suggestion list entirely. Open the function and clear the error. Its calltip still works, which is why this is easy to miss.
2. **The return type does not fit the argument you are completing.** The return type is inferred from the body, not declared. A UDF that returns a table is not offered where a scalar is expected, and one that returns a scalar is not offered where a table is expected. Filter arguments, for instance the second and later arguments of [`CALCULATE`](https://dax.guide/calculate), accept either. A function whose body is an untyped `EXPR` parameter fits everywhere.
3. **Visual calculation mismatch.** A UDF written for visual calculations is only offered inside another visual calculation, and vice versa.
4. **It is the function you are editing.** A function is not offered inside its own definition.

**参数约束错误**

- 检查你指定的参数类型
- 确保你向函数传递的是兼容的值
- 查看 Microsoft 文档，了解支持的约束类型

**部署后函数无法正常工作**

- Verify your target environment supports UDFs (compatibility level 1702+). The Power BI Service supports UDFs as of the June 2026 release. Azure Analysis Services and SQL Server Analysis Services don't support UDFs.

## 限制

- UDFs require compatibility level 1702 or higher; Azure Analysis Services and SQL Server Analysis Services don't support them
- UDF 不能递归（调用自身）

> [!NOTE]
> With the [general availability](https://community.fabric.microsoft.com/t5/Power-BI-Updates-Blog/DAX-User-Defined-Functions-Generally-Available/ba-p/5185738) of UDFs in June 2026, UDFs support optional parameters with default expressions. Tabular Editor 3 supports this syntax since version 3.26.2. Older versions display a false error message when you use the default expression syntax.

---

Tabular Editor 3 中的 UDF 提供了一种强大方式，可用于创建可复用、易维护的 DAX 代码。 By following these guidelines and best practices, you can build a library of functions that will improve your model's consistency and reduce development time.
