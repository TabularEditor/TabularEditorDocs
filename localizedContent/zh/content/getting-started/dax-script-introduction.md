---
uid: dax-script-introduction
title: 使用 DAX脚本功能
author: Daniel Otykier
updated: 2021-10-08
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

# 使用 DAX脚本功能

在[上一篇文章](xref:creating-and-testing-dax)中，你学习了如何在模型中添加和编辑计算对象，例如度量值、计算列等。

随着模型越来越复杂，在编写和维护业务逻辑时，你可能会发现，在 TOM Explorer 中导航或在各个度量值之间来回切换变得十分繁琐。 度量值之间出现很长的依赖链并不少见。因此，有时把构成业务逻辑的所有 DAX 代码集中到一个文档中会更方便。

这正是 Tabular Editor 3 新增 **DAX脚本** 功能的目的。

要使用此功能，请在 TOM Explorer 中找到你希望生成单一文档的对象。 多选这些对象，然后右键选择 **Script DAX**。 会创建一个新文档，其中包含所有选定对象的 DAX 表达式和基本属性。 你也可以分别选择某个表对象或模型对象，从而为表内的所有对象或整个模型内的所有对象生成 DAX脚本。

![Dax 脚本](~/content/assets/images/dax-script.png)

通过 DAX脚本编辑对象，与通过 **表达式编辑器** 编辑略有不同。 使用后者时，当你切换到另一个对象时，更改会立即生效。 而在 DAX脚本中，只有在你明确使用 **Script > Apply** (F5) 选项后，改动才会生效。 如果你已连接到 Analysis Services 实例，则可以使用 **Script > Apply & Sync** (SHIFT+F5) 选项，在应用更改的同时，将更新后的模型元数据保存到 Analysis Services。

## 使用 DAX脚本文件

DAX脚本可以保存为文本文件，文件扩展名为 `.te3daxs`。 要将 DAX脚本保存为文件，只需选择 **文件 > 保存** (Ctrl+S)。 要从文本文件打开 DAX脚本，只需选择 **文件 > 打开 > 文件...** (Ctrl+O)。

> [!NOTE]
> DAX脚本并不针对特定模型；但由于 DAX 表达式可能引用模型中定义的度量值、列和表，因此无法保证任何 DAX脚本都能应用于任意模型。 DAX脚本主要用于在特定 Data model 的上下文中，在单个文档中处理多个 DAX 对象。

## DAX脚本编辑器

DAX脚本编辑器具备 Tabular Editor 3 中其他位置使用的 DAX 编辑器的全部功能。 具体包括：自动补全、自动格式化、参数提示等。

此外，为了更轻松地管理较大的 DAX脚本，DAX脚本视图顶部会显示两个下拉列表。 左侧下拉列表可让你在脚本中定义的对象之间快速跳转；右侧下拉列表可让你在当前对象的各个属性之间快速跳转。

![Dax脚本导航](~/content/assets/images/dax-script-navigation.png)

## 定义度量值

如果你想在脚本中包含某个被引用、但尚未在脚本中定义的度量值定义，可以在度量值引用上右键，然后选择“定义度量值”或“定义度量值及其依赖项”选项。

![定义度量值及其依赖项](~/content/assets/images/define-measure-with-deps.png)

## 快捷键

要将脚本应用到模型，可以使用以下快捷键：

- **F5**：将整个脚本应用到本地模型元数据
- **Shift+F5**：将整个脚本应用到本地模型元数据，然后将模型元数据保存回源
- **F8**：将脚本中当前选中的部分应用到本地模型元数据
- **Shift+F8**：将脚本中当前选中的部分应用到本地模型元数据，然后将模型元数据保存回源

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
MEASURE 'Table name'[度量值名称] = <DAX expression>
    [<Measure properties>]

COLUMN 'Table name'[Column name] = <DAX expression>
    [<Column properties>]

TABLE 'Table name' = <DAX expression>
    [<Table properties>]

CALCULATIONGROUP 'Table name'[Column name]
    [<Calculation Group properties>]
    CALCULATIONITEM "Item 1" = <DAX expression>
        [<Calculation Item properties>]
    CALCULATIONITEM "Item 2" = <DAX expression>
        [<Calculation Item properties>]
    ...

<Measure properties>:
    DetailRows = <DAX expression>
    DisplayFolder = "string"
    FormatString = "string"
    Description = "string"
    Visible = TRUE/FALSE
    KpiStatusExpression = <DAX expression>
    KpiStatusDescription = "string"
    KpiStatusGraphic = "string"
    KpiTrendExpression = <DAX expression>
    KpiTrendDescription = "string"
    KpiTrendGraphic = "string"
    KpiTargetExpression = <DAX expression>
    KpiTargetDescription = "string"
    KpiTargetFormatString = "string"

<Column properties>:
    DisplayFolder = "string"
    FormatString = "string"
    Description = "string"
    Visible = TRUE / FALSE
    Datatype = BOOLEAN / DOUBLE / INTEGER / DATETIME / CURRENCY / STRING

<Table properties>:
    Description = "string"
    Visible = TRUE / FALSE
    DetailRows = <DAX expression>

<Calculation Group properties>:
    Description = "string"
    Visible = TRUE / FALSE
    Precedence = <integer value>

<Calculation Item properties>
    Description = "string"
    Ordinal = <integer value>
    FormatString = <DAX expression> 
```

## 示例 1：度量值

例如，下面的脚本在 `'Internet Sales'` 表上定义了 `[Internet Total Sales]` 度量值。 除了度量值的 DAX 表达式外，该脚本还包括度量值的说明和格式字符串。

```dax
----------------------------------
-- 度量值: [Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "Returns the sum of all Internet Sales"
    FormatString = "\$#,0.00;(\$#,0.00);\$#,0.00"
```

## 示例 2：带状态与目标 KPI 的度量值

下面的 DAX 脚本定义了 `[Internet Current Quarter Sales Performance]` 度量值，其中包含一个带状态表达式和目标表达式的 KPI。 状态 KPI 使用“Shapes”图形。

```dax
--------------------------------------------------------
-- 度量值: [Internet Current Quarter Sales Performance]
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

下面的 DAX 脚本定义了包含 `[Period]` 列的 `'Time Intelligence'` 计算组。 该计算组包含 6 个计算项，用于执行不同的时间计算。 注意，`"YoY %"` 计算项使用了不同的格式字符串。

```dax
-----------------------------------------
-- 计算组: 'Time Intelligence'
-----------------------------------------
CALCULATIONGROUP 'Time Intelligence'[Period]
    Description = "Use this table to perform time calculations"

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

# 后续步骤

- @bpa
- @cs-scripts-and-macros
- @personalizing-te3