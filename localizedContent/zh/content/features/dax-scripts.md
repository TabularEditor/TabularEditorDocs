---
uid: dax-scripts
title: DAX脚本
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# DAX脚本

**DAX脚本**可让你在一个文档中查看和编辑多个对象的 DAX 表达式及其基本属性。 例如，当复杂的业务逻辑分散在多个度量值中时，这会很有用。

你可以为 TOM Explorer 中任何包含 DAX 表达式的对象生成 DAX 脚本。

要使用此功能，请在 TOM Explorer 中找到你希望汇总到同一文档中的对象。 选中多个对象，然后右键选择 **生成 DAX 脚本**。 系统会创建一个新文档，其中包含所有所选对象的 DAX 表达式和基本属性。 你也可以分别选择表对象或模型对象，为某个表内的所有对象或整个模型中的所有对象生成 DAX脚本。

![Dax 脚本](~/content/assets/images/dax-script.png)

通过 DAX脚本编辑对象与通过 **表达式编辑器** 编辑略有不同。 使用后者时，当你切换到其他对象时，改动会立即应用。 但在 DAX脚本中，改动不会自动应用，只有在你手动使用 **脚本 > 应用**（F5）选项后才会生效。 如果你已连接到某个 Analysis Services 实例，可以使用 **脚本 > 应用并同步**（SHIFT+F5）选项，同时应用改动并将更新后的模型元数据保存到 Analysis Services。

你可以使用常用的键盘快捷键（Ctrl+Z / Ctrl+Y）撤销/重做在 DAX脚本里做的改动。

## 多个 DAX脚本

如果你更喜欢同时打开多个文档窗口，而不是只打开一个窗口，那么可以按需创建任意数量的 DAX脚本。 这样一来，你就可以使用常见的 IDE 功能，将文档并排显示、分布在不同显示器上等。 注意：当你在 TOM 中更改对象的表达式/属性时，DAX脚本窗口中的代码不会自动更新。 换句话说，如果你有两个或多个 DAX 脚本都包含同一对象(s)的定义，那么最后应用 (F5) 的脚本始终会覆盖通过其他 DAX 脚本所做的更改，或在 **属性视图** 中直接做的更改。

## 使用 DAX脚本文件

DAX脚本可以保存为文本文件，文件扩展名为 `.te3daxs`。 要将 DAX脚本保存为文件，只需使用 **文件 > 保存**（Ctrl+S）。 要从文本文件打开 DAX脚本，请使用 **文件 > 打开 > 文件...**（Ctrl+O）。

> [!NOTE]
> DAX脚本并不特定于某个模型。但由于 DAX 表达式可能会引用模型中定义的度量值、列和表，因此无法保证任何 DAX脚本都能应用到任何模型。 DAX脚本主要用于在特定 Data model 的上下文中，在单个文档里处理多个 DAX 对象。

## DAX脚本编辑器

DAX脚本编辑器具备 Tabular Editor 3 中其他位置所使用的 DAX 编辑器的全部功能。 例如自动完成、自动格式化、参数提示等。

此外，为了便于管理大型 DAX脚本，DAX脚本视图顶部会显示两个下拉列表。 左侧的下拉列表可让你在脚本中定义的对象之间跳转；右侧的下拉列表可让你在当前对象的各个属性之间跳转。

![Dax脚本导航](~/content/assets/images/dax-script-navigation.png)

## 定义度量值

如果你想在脚本中包含某个被引用但尚未在脚本中定义的度量值定义，可以在度量值引用上右键单击，然后选择“定义度量值”或“定义度量值及其依赖项”选项。

![定义度量值及依赖项](~/content/assets/images/define-measure-with-deps.png)

## 快捷键

要将脚本应用到模型，请使用以下快捷键：

- **F5**：将整个脚本应用到本地模型元数据中
- **Shift+F5**：将整个脚本应用到本地模型元数据中，然后将模型元数据保存回源
- **F8**：将当前选中的脚本部分应用到本地模型元数据中
- **Shift+F8**：将当前选中的脚本部分应用到本地模型元数据中，然后将模型元数据保存回源

## 支持的 DAX 对象

Tabular Editor 3 支持使用 DAX脚本编辑以下类型的对象：

- 度量值（包括 KPI）
- 计算列
- 计算表格
- 计算组（包括计算项）

# DAX脚本语法

DAX脚本的语法如下：

```dax
<DAX script>:
MEASURE '表名称'[度量值名称] [= [<DAX expression>]]
    [<Measure properties>]

COLUMN '表名称'[列名称] [= [<DAX expression>]]
    [<Column properties>]

TABLE '表名称' [= [<DAX expression>]]
    [<Table properties>]

CALCULATIONGROUP '表名称'[列名称]
    [<Calculation Group properties>]
    CALCULATIONITEM "项 1" [= [<DAX expression>]]
        [<Calculation Item properties>]
    CALCULATIONITEM "项 2" [= [<DAX expression>]]
        [<Calculation Item properties>]
    ...

<Measure properties>:
    DetailRows = [<DAX expression>]
    DisplayFolder = ["string"]
    FormatString = ["string" / <DAX expression>]
    Description = ["string"]
    Visible = TRUE/FALSE
    KpiStatusExpression = [<DAX expression>]
    KpiStatusDescription = ["string"]
    KpiStatusGraphic = ["string"]
    KpiTrendExpression = [<DAX expression>]
    KpiTrendDescription = ["string"]
    KpiTrendGraphic = ["string"]
    KpiTargetExpression = [<DAX expression>]
    KpiTargetDescription = ["string"]
    KpiTargetFormatString = ["string"]

<Column properties>:
    DisplayFolder = ["string"]
    FormatString = ["string"]
    Description = ["string"]
    Visible = TRUE / FALSE
    Datatype = BOOLEAN / DOUBLE / INTEGER / DATETIME / CURRENCY / STRING

<Table properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    DetailRows = [<DAX expression>]

<Calculation Group properties>:
    Description = ["string"]
    Visible = TRUE / FALSE
    Precedence = <integer value>

<Calculation Item properties>
    Description = ["string"]
    Ordinal = <integer value>
    FormatString = [<DAX expression>]
```

> [!TIP]
> 用过 TMDL 的人肯定注意到，DAX脚本语法和 TMDL 语法有一些相似之处。 事实上，TMDL 的灵感正是来自 DAX脚本。 不过，为了保持简单，DAX脚本有意只支持那些关联了一个或多个 DAX 表达式的对象。 此外，DAX脚本语法的设计是为了兼容 DAX 查询的 `DEFINE` 部分（只要 DAX脚本不指定任何对象属性）。 而 TMDL 用于定义整个模型元数据，并不局限于 DAX 对象。 不过，TMDL 代码块无法直接用于 DAX 查询，因为 TMDL 中用于定义对象名称的语法在 DAX 中并不合法。

## 示例 1：度量值

例如，下面的脚本在 `'Internet Sales'` 表中定义了 `[Internet Total Sales]` 度量值。 除了度量值的 DAX 表达式之外，该脚本还包含了度量值说明和格式字符串。

```dax
----------------------------------
-- 度量值：[Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "返回所有 Internet Sales 的销售额总和"
    FormatString = "\$#,0.00;(\$#,0.00);\$#,0.00"
```

## 示例 2：带状态和目标 KPI 的度量值

下面的 DAX脚本定义了 `[Internet Current Quarter Sales Performance]` 度量值，其中包含一个带状态表达式和目标表达式的 KPI。 该状态 KPI 使用“Shapes”图形。

```dax
--------------------------------------------------------
-- 度量值：[Internet Current Quarter Sales Performance]
--------------------------------------------------------
MEASURE 'Internet Sales'[Internet Current Quarter Sales Performance] =
    IFERROR(
        [Internet Current Quarter Sales] / [Internet Previous Quarter Sales Proportion to QTD],
        BLANK()
    )
    , KpiStatusExpression =
        VAR x = [Internet Current Quarter Sales Performance]
        RETURN
            IF(
                ISBLANK( x ),
                BLANK(),
                IF(x < 1, -1, IF(x < 1.07, 0, 1))
            )
    , KpiStatusGraphic = "Shapes"
    , KpiTargetExpression = 1.1
```

## 示例 3：计算组

下面的 DAX 脚本定义了 `'Time Intelligence'` 计算组，其中包含 `[Period]` 列。 该计算组包含 6 个计算项，用于执行各种时间计算。 注意 `"YoY %"` 这一项使用了不同的格式字符串。

```dax
-----------------------------------------
-- 计算组：'Time Intelligence'
-----------------------------------------
CALCULATIONGROUP 'Time Intelligence'[Period]
    Description = "用此表执行时间计算"

    CALCULATIONITEM "Current" = SELECTEDMEASURE()
        Ordinal = 0

    CALCULATIONITEM "MTD" = TOTALMTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 1

    CALCULATIONITEM "YTD" = TOTALYTD(SELECTEDMEASURE(), 'Calendar'[Date])
        Ordinal = 2

    CALCULATIONITEM "PY" = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 3

    CALCULATIONITEM "YoY" = 
        SELECTEDMEASURE()
         - CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        Ordinal = 4

    CALCULATIONITEM "YoY %" = 
        VAR lastYear = 
            CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Calendar'[Date]))
        RETURN
            DIVIDE(
                SELECTEDMEASURE() - lastYear,
                lastYear
            )
        FormatString = "Percent"
        Ordinal = 5
```

# 未指定或为空的表达式与属性

从 Tabular Editor 3.16.0 起，可以在 DAX脚本中指定空表达式和空属性值，或者完全省略对象表达式。

例如，以下脚本会创建一个度量值：DAX 表达式为空、格式字符串为空，并且不设置显示文件夹。 如果该度量值已存在，它将被更新为：DAX 表达式为空、格式字符串为空，并且不设置显示文件夹。

```dax
MEASURE 'Internet Sales'[Internet Total Sales] =
    , Description = "TODO: 询问业务方该如何实现并设置格式。"
    , FormatString =
    , DisplayFolder =
```

注意：空表达式后面的属性之前，必须写 `,`（逗号）。 当前面的表达式不为空时，逗号是可选的。

如果你想保留度量值现有的 DAX 表达式，可以在对象名称后省略 `=` 符号：

```dax
MEASURE 'Internet Sales'[Internet Total Sales]
    DisplayFolder = "Totals"
```

上面的示例会将 `[Internet Total Sales]` 度量值的 `DisplayFolder` 设置为指定值，但会保留现有的 DAX 表达式。 对象上的所有其他属性，例如 `Description` 和 `FormatString`，将保持不变。

这些新特性让你更容易编写只更新对象特定属性的脚本，而无需指定完整的对象定义。 这样，脚本也更容易在不同模型之间复用。
