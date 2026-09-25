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

**DAX脚本**可让你在一个文档中查看和编辑多个对象的 DAX 表达式及其基本属性。 This is useful, for example, when complex business logic is spread out across multiple measures.

你可以为 TOM Explorer 中任何包含 DAX 表达式的对象生成 DAX 脚本。

To use this feature, locate the objects for which you would like to generate a single document, in the TOM Explorer. Multi-select the objects, then right-click and choose **Script DAX**. A new document is created, containing the DAX expressions and basic properties of all the selected objects. 你也可以分别选择某个表对象或模型对象，从而为表内的所有对象或整个模型内的所有对象生成 DAX脚本。

![Dax 脚本](~/content/assets/images/dax-script.png)

Editing objects through a DAX script is slightly different than editing through the **Expression Editor**. With the latter, changes are applied immediately when you navigate to a different object. In a DAX script, however, changes are not applied until you explicitly do so by using the **Script > Apply** (F5) option. If you are connected to an instance of Analysis Services, you can use the **Script > Apply & Sync** (SHIFT+F5) option to simultaneously apply the changes and save the updated model metadata to Analysis Services.

你可以使用常用的键盘快捷键（Ctrl+Z / Ctrl+Y）撤销/重做在 DAX脚本里做的改动。

## 多个 DAX脚本

如果你更喜欢同时打开多个文档窗口，而不是只打开一个窗口，那么可以按需创建任意数量的 DAX脚本。 This way, you can use the usual IDE features to place the documents side by side, on different monitors, etc. Be aware, that the code within DAX script windows is not updated automatically when changes are made to the object expression/properties in the TOM. So in other words, if you have two or more DAX scripts containing the definition of the same object(s), then the last script to be applied (F5), will always override any changes made through other DAX scripts, or directly through the **Properties View**.

## 使用 DAX脚本文件

DAX脚本可以保存为文本文件，文件扩展名为 `.te3daxs`。 To save a DAX script as a file, simply use the **File > Save** (Ctrl+S) option. To open a DAX script from a text file, use the **File > Open > File...** (Ctrl+O) option.

> [!NOTE]
> DAX脚本并不特定于某个模型。但由于 DAX 表达式可能会引用模型中定义的度量值、列和表，因此无法保证任何 DAX脚本都能应用到任何模型。 DAX scripts are mostly useful for working with several DAX objects within a single document, in the context of a specific data model.

## DAX脚本编辑器

DAX脚本编辑器具备 Tabular Editor 3 中其他位置所使用的 DAX 编辑器的全部功能。 Specifically, auto-complete, auto-formatting, calltips, etc.

此外，为了便于管理大型 DAX脚本，DAX脚本视图顶部会显示两个下拉列表。 The dropdown on the left allows you to jump between objects defined in the script, whereas the dropdown on the right allows you to jump between properties on the current object.

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
MEASURE 'Table name'[Measure name] [= [<DAX expression>]]
    [<Measure properties>]

COLUMN 'Table name'[Column name] [= [<DAX expression>]]
    [<Column properties>]

TABLE 'Table name' [= [<DAX expression>]]
    [<Table properties>]

CALCULATIONGROUP 'Table name'[Column name]
    [<Calculation Group properties>]
    CALCULATIONITEM "Item 1" [= [<DAX expression>]]
        [<Calculation Item properties>]
    CALCULATIONITEM "Item 2" [= [<DAX expression>]]
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
> 用过 TMDL 的人肯定注意到，DAX脚本语法和 TMDL 语法有一些相似之处。 In fact, TMDL was inspired by DAX scripts. However, to keep things simple, DAX scripts intentionally supports only objects that have one or more DAX expressions associated with them. Moreover, the DAX script syntax is designed to be compatible with the `DEFINE` section of a DAX query (provided the DAX script does not specify any object properties). TMDL, on the other hand, is used to define the entire model metadata, and is not limited to DAX objects. However, blocks of TMDL code cannot be readily used in a DAX query as the syntax for defining object names in TMDL, is not valid in DAX.

## 示例 1：度量值

例如，下面的脚本在 `'Internet Sales'` 表中定义了 `[Internet Total Sales]` 度量值。 In addition to the DAX expression of the measure, the script also includes the measure description and format string.

```dax
----------------------------------
-- Measure: [Internet Total Sales]
----------------------------------
MEASURE 'Internet Sales'[Internet Total Sales] = SUM('Internet Sales'[Sales Amount])
    Description = "Returns the sum of all Internet Sales"
    FormatString = "\$#,0.00;(\$#,0.00);\$#,0.00"
```

## 示例 2：带状态和目标 KPI 的度量值

下面的 DAX脚本定义了 `[Internet Current Quarter Sales Performance]` 度量值，其中包含一个带状态表达式和目标表达式的 KPI。 The status KPI uses the "Shapes" graphic.

```dax
--------------------------------------------------------
-- Measure: [Internet Current Quarter Sales Performance]
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

下面的 DAX 脚本定义了 `'Time Intelligence'` 计算组，其中包含 `[Period]` 列。 The calculation group contains 6 calculation items that performs various time calculations. Notice how the `"YoY %"` item applies a different format string.

```dax
-----------------------------------------
-- Calculation Group: 'Time Intelligence'
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

# 未指定或为空的表达式与属性

从 Tabular Editor 3.16.0 起，可以在 DAX脚本中指定空表达式和空属性值，或者完全省略对象表达式。

例如，以下脚本会创建一个度量值：DAX 表达式为空、格式字符串为空，并且不设置显示文件夹。 If the measure already exists, it will be updated to have an empty DAX expression, an empty format string and no Display Folder.

```dax
MEASURE 'Internet Sales'[Internet Total Sales] =
    , Description = "TODO: Ask business how this should be implemented and formatted."
    , FormatString =
    , DisplayFolder =
```

Note that the `,` (comma) before properties following an empty expression is mandatory. Commas are optional when the preceding expression is non-empty.

如果你想保留度量值现有的 DAX 表达式，可以在对象名称后省略 `=` 符号：

```dax
MEASURE 'Internet Sales'[Internet Total Sales]
    DisplayFolder = "Totals"
```

上面的示例会将 `[Internet Total Sales]` 度量值的 `DisplayFolder` 设置为指定值，但会保留现有的 DAX 表达式。 All other properties on the object, such as `Description` and `FormatString`, will remain unchanged.

这些新特性让你更容易编写只更新对象特定属性的脚本，而无需指定完整的对象定义。 This way, scripts can more easily be reused across different models.
