---
uid: udfs
title: DAX 用户自定义函数
author: Daniel Otykier
updated: 2026-03-19
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

DAX 用户自定义函数 (UDFs) 是语义模型的一项新功能，在 Power BI Desktop 的 2025 年九月更新中引入。

该功能让你能够创建可复用的 DAX 函数，并可在模型中的任何 DAX 表达式里调用，甚至在其他函数中也能调用。 这个强大的功能可帮助你保持一致性、减少代码重复，并创建更易维护的 DAX 表达式。

Tabular Editor 3 自 3.23.0 版本起支持 UDFs。不过，我们建议使用 [3.23.1](xref:release-3-23-1)（或更高版本），以获得多项 bug 修复与改进。

如需更详细了解 Tabular Editor 3 中 UDF 的入门内容，请参阅[这篇博客文章](https://tabulareditor.com/blog/how-to-get-started-using-udfs-in-tabular-editor-3)。

## 理解 UDFs

你可以将 UDFs 理解为自定义 DAX 函数：定义一次，即可在整个模型中反复使用。 你可以定义函数要接受哪些参数；这些参数既可以是标量值或表值，也可以是对对象的引用。然后，你需要提供一个使用这些参数来计算结果的 DAX 表达式，而结果同样可以是标量值或表值。

如需进一步了解 DAX UDF 的工作原理，我们推荐阅读 [SQLBI 的这篇文章](https://www.sqlbi.com/articles/introducing-user-defined-functions-in-dax/)。

## 前提条件

在 Tabular Editor 3 中创建和使用 UDFs 之前，确保满足以下条件：

- 你的模型兼容级别为 **1702 或更高**

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

另外，你也可以在 DAX 查询的 **DEFINE** 部分直接创建 UDF：按下 F7（Apply），或使用 **Query > Apply** 菜单选项。 如果查询包含多个查询作用域的定义，你也可以只选择其中一部分，然后按 F8（Apply Selection）。

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

UDF 的一个关键特性是，参数可采用两种模式定义：**按值传递**和 **按引用传递**。 默认情况下，除非你另有指定，参数将采用**按值传递**。 这意味着该参数在 UDF 表达式内部的行为与 DAX 变量基本一致（即使用 `VAR` 关键字定义的变量）。 换句话说，当调用 UDF 时，参数值会被“复制”到函数中，函数内部对该参数的任何引用都会始终返回相同的值。

相比之下，**按引用传递**参数的行为更像度量值。 也就是说，在函数_内部_对该参数进行求值的结果，可能会因评估语境不同而变化。

要指定求值模式，请在参数名后添加参数规格，并用冒号（`:`）分隔。 该说明可以是 `VAL` 或 `EXPR`，分别对应“按值传递”和“按引用传递”。 如上所述，“按值传递”是默认值，因此未指定时会隐式采用 `VAL`。 例如：

```dax
(
    x: VAL,   // 按值传递参数 - DAX 表达式在调用函数时仅求值一次，结果会被“复制”到函数中
    y: EXPR   // 按引用传递参数 - 可以是任意 DAX 表达式，之后在引用该参数时会遵循当时的上下文
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

可用约束的完整列表，请参阅 [Microsoft 的 UDF 规范](https://learn.microsoft.com/en-us/dax/best-practices/dax-user-defined-functions)。

## 在模型中使用 UDF

### 在对象表达式中

创建 UDF 之后，你可以在整个模型中的任何 DAX 表达式里使用它。 你输入时，Tabular Editor 3 的自动完成功能会提示你已定义的 UDF。

### 在 DAX脚本中

在使用 DAX脚本时，也可以使用 UDF：

```dax
-- Function: MyFuncRenamed
FUNCTION MyFuncRenamed =
    // 将两个数字相加
    (
        x: INT64, // 第一个数字
        y: INT64  // 第二个数字
    )
    => x + y

-- 度量值: [New Measure]
MEASURE 'Date'[New Measure] = MyFuncRenamed(1,2)
```

### 在 DAX 查询中

Tabular Editor 3 新增了用于在 DAX 查询中使用 UDF 的强大功能。 我们在上文已经提到，你可以从 DAX 查询的 **DEFINE** 部分“应用”某个 UDF，使其成为模型的永久组成部分。 此外，在 DAX 查询中使用 UDF 时，你可以在函数调用处右键并选择 **Define Function**，即可自动在查询的 **DEFINE** 部分生成函数定义：

![从查询中执行 Define Function](~/content/assets/images/tutorials/udf-define.png)

从上方截图可以看出，在 UDF 调用处右键可使用以下选项：

- **窥视定义**（Alt+F12）：在当前光标位置下方打开一个嵌套的只读编辑器，显示该函数的定义
- **转到定义**（F12）：导航到模型中 **Functions** 文件夹内的函数定义；如果该函数是在当前查询或脚本中定义的，则导航到编辑器内的函数定义
- **Inline Function**：将函数调用替换为实际的函数定义，并将形参替换为传入函数的实际参数值
- **Define Function**（仅适用于 DAX 脚本或 DAX 查询）：如果查询的 **DEFINE** 部分还没有该函数定义，就会在其中生成函数定义
- **Define Function with dependencies**（仅适用于 DAX 脚本或 DAX 查询）：与上面类似，但还会为该函数依赖的其他 UDF 一并生成定义

## DAX 组件管理器

Tabular Editor 3.24.0 引入了一项名为 **DAX 组件管理器** 的新功能，让你可以直接在 Tabular Editor 中轻松发现、安装和管理 DAX UDF 库。 在首次发布时，组件管理器支持热门的 [DaxLib](https://daxlib.org) 源，其中包含覆盖多种场景的大量实用 UDF。

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

<a name="namespaces"></a>

### 命名空间

DAX 中并没有“命名空间”的概念，但我们建议为 UDF 命名时尽量避免歧义，并让 UDF 的来源一目了然。 例如 `DaxLib.Convert.CelsiusToFahrenheit`（使用“.” 作为命名空间分隔符）。 当 UDF 采用这种命名方式时，TOM Explorer 会根据名称以层级结构显示 UDF。 你可以使用 TOM Explorer 上方工具栏中的 **Group User-Defined Functions by namespace** 切换按钮，按命名空间对 UDF 的显示进行分组（注意：仅当处理兼容级别为 1702 或更高的模型时，才会显示该按钮）。

![按命名空间分组的 DAX UDF](~/content/assets/images/udf-namespaces-tom-explorer.png)

在 Tabular Editor 中，UDF 还有一个“Namespace” _属性_，让你可以为每个 UDF 单独自定义命名空间，而不用更改实际的 UDF 对象名称。 这与度量值的显示文件夹非常相似。 例如，如果你想对多个 UDF 执行批量重命名 (F2)，去掉名称中的命名空间，但仍希望它们在 TOM Explorer 中保持良好的层级组织，那么将“Namespace”属性设置为不同于可从 UDF 名称中推断出的值就会很有用。

> [!NOTE]
> Tabular Editor 里的这个组织功能不会影响 DAX 代码。 调用 UDF 时，你仍然需要输入完整的 UDF 名称，包括所有命名空间部分。

## 最佳实践

### 命名规范

- 使用具有描述性的名称，清晰表明函数用途
- 可考虑用组织的首字母缩写作为 UDF 前缀（例如 `ACME.CalculateDiscount`）
- 避免使用过于通用的名称，以免与未来的 DAX 函数发生冲突
- 使用带分隔符字符（`.` 或 `_`）的复合名称。 例如，`Finance.CalcProfit` 或 `My_CalcProfit`。 这样即使 Microsoft 引入同名的内置 DAX 函数，你的 UDF 也不会因此失效。 有关详细信息，请参阅[内置 BPA 规则](xref:kb.bpa-udf-use-compound-names)

### 文档

- 始终添加注释，说明该函数的作用
- 记录每个参数的用途以及预期的数据类型
- 在注释中提供用法示例

```dax
// 计算两个值之间的百分比变化
// 用法：PercentChange(100, 110) 返回 0.10（增加 10%）
(
    oldValue: DOUBLE,    // 原始值
    newValue: DOUBLE     // 用于对比的新值
)
=> DIVIDE(newValue - oldValue, oldValue)
```

Tabular Editor 3 会自动识别所有注释，并在自动完成建议和工具提示中以合适的方式显示。

![带注释的 UDF 自动完成](~/content/assets/images/tutorials/udf-comment-tooltips.png)

## 常见使用场景

### 数学运算

```dax
// 计算复利
(
    principal: DOUBLE,
    rate: DOUBLE,
    periods: INT64
)
=> principal * POWER(1 + rate, periods)
```

### 字符串处理

```dax
// 将名字和姓氏组合成完整姓名
(
    firstName: STRING,
    lastName: STRING
)
=> TRIM(firstName) & " " & TRIM(lastName)
```

### 日期计算

```dax
// 根据日期获取财政年度（财年从七月1日开始）
(
    inputDate: DATETIME
)
=> IF(MONTH(inputDate) >= 7, YEAR(inputDate) + 1, YEAR(inputDate))
```

### 业务逻辑

```dax
// 根据数量应用阶梯折扣
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

- 确认函数已成功保存
- 检查函数定义中是否存在语法错误
- 确保在兼容的上下文中使用该函数

**参数约束错误**

- 检查你指定的参数类型
- 确保你向函数传递的是兼容的值
- 查看 Microsoft 文档，了解支持的约束类型

**部署后函数无法正常工作**

- 确认目标环境支持 UDF（兼容级别 1702+）。 截至 2025 年九月十六日，Power BI 服务尚不支持 UDF，Azure Analysis Services 和 SQL Server Analysis Services 也同样不支持。

## 局限性

- UDF 目前为预览功能，在某些部署场景中可能会有局限
- 并非所有 Power BI 环境都支持 UDF（需要特定构建版本）
- UDF 不能递归（调用自身）
- UDF 不支持可选参数、带默认值的参数或参数重载

---

Tabular Editor 3 中的 UDF 提供了一种强大方式，可用于创建可复用、易维护的 DAX 代码。 遵循这些指南和最佳实践，你可以构建一个函数库，从而提升模型一致性并缩短开发时间。