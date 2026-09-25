---
uid: 日历
title: 日历（增强时间智能）
author: Daniel Otykier 和 Maria José Ferreira
updated: 2026-01-22
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
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

# 日历（增强时间智能）

Power BI Desktop 2025 年九月版引入了一项新的公共预览功能：**增强型时间智能**（也称为 **基于日历的时间智能**）。该功能允许你在语义模型中定义自定义日历，从而支持在财年、零售（4-4-5、4-5-4、5-4-4）、ISO 以及其他非公历日历体系下进行时间智能计算。

与默认假设使用标准公历的经典时间智能函数不同，新的基于日历的函数会根据你在日期表中定义的明确列映射来确定其行为。这种方法还引入了周级别的时间智能计算，而这类计算此前很难实现。

有关基于日历的时间智能工作原理的更多信息，请参阅：

- [在 DAX 中引入基于日历的时间智能](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/)（SQLBI）
- [基于日历的时间智能预览](https://powerbi.microsoft.com/en-us/blog/calendar-based-time-intelligence-time-intelligence-tailored-preview/)（Microsoft）

## 定义日历

![创建日历](~/content/assets/images/tutorials/calendar-create.png)

1. 在模型中的某个表（通常是日期表）上单击鼠标右键，然后选择 **创建 > 日历...**。
2. 为你的日历命名，例如 `Fiscal`。

将日历添加到表后，它们会显示在 TOM Explorer 的 **Calendars** 节点下：

![TOM Explorer 中的日历](~/content/assets/images/tutorials/calendar-tom-explorer.png)

在 DAX 计算中使用日历之前，需要通过将表中的列映射到相应的时间单位类别来进行配置。

## 日历编辑器

Tabular Editor 3 2026 年一月版引入了专用的 **日历编辑器**，提供用于配置日历的完整界面。编辑器会以结构化网格显示所有时间单位类别，并提供实用的工具提示，同时进行实时验证，帮助避免配置错误。

### 打开日历编辑器

你可以通过以下任一方式打开日历编辑器：

- 在 TOM Explorer 中，双击表下的现有日历。
- 在 TOM Explorer 中，右键单击表下的现有日历，然后选择 **编辑日历...**。
- 在 TOM Explorer 中选择一个日历，然后打开 **日历** 菜单并选择 **编辑日历...**。
- 打开 **视图** 菜单并选择 **日历编辑器**。

![日历编辑器](~/content/assets/images/tutorials/calendar-editor.png)

### 日历编辑器布局

日历编辑器分为两个主要区域：

1. **日历网格（左侧面板）**
   一个垂直布局的网格，其中每个日历显示为一列，时间单位类别显示为各行。各行按年、季度、月、周和日分层组织。在此网格中，可以：

   - 在 **表** 行中选择日历应从中获取列的表（通常为日期表）。
   - 在每个单元格中通过下拉列表进行选择，将列映射到时间单位类别。
   - 通过图标和工具提示查看实时验证反馈。
   - 使用 **+ 添加日历** 列创建额外的日历（如果你的模型需要多个日历定义）。
   - 在网格中直接编辑名称即可重命名日历。
   - 在日历列上点击右键以删除日历。

2. **上下文面板（右侧面板）**
   一个会随你在日历网格中的选择而变化的详细信息面板：

   - **关联列**：当你选择一个已映射列的时间单位行时，此面板可让你选择额外的关联列。
   - **与时间相关的列**：当你选择网格底部的“与时间相关的列”行时，此面板可让你将列标记为时间相关。

![日历编辑器布局，显示日历网格和上下文面板](~/content/assets/images/tutorials/calendar-editor-parts.png)

### 将列映射到时间单位

日历网格会显示所有可用的时间单位类别。要将某列映射到某个时间单位，点击网格中某个日历列下对应的时间单位单元格。这会打开一个下拉列表，可在其中为该时间单位选择**主列**。

![从下拉列表选择列](~/content/assets/images/tutorials/calendar-dropdown-column-selection.png)

你不需要映射每个时间单位——只需映射适用于你的日历结构、且你的表中有相应列的那些即可。

时间单位分为 **完整** 类别（单独即可唯一标识一个周期）和 **部分** 类别（需要先映射其父时间单位）。将鼠标悬停在任意时间单位行上，即可查看工具提示，其中会说明预期的数据格式并提供示例。

![完整时间单位的工具提示，显示说明和示例](~/content/assets/images/tutorials/calendar-complete-time-unit-tooltip.png)

对于部分时间单位，工具提示还会显示必须映射的父时间单位：

![部分时间单位的工具提示，显示依赖关系](~/content/assets/images/tutorials/calendar-partial-time-unit-tooltip.png)

#### 示例：使用部分时间单位

在某些情况下，你的日期表可能没有能够唯一标识“季度”或“月份”等完整时间单位的列 (例如 "Q1 2024" 或 "2024 年一月")。相反，你可能有类似 `QuarterOfYear`（1-4）和 `MonthOfYear`（1-12）这样的列，它们只有与“年”列组合使用时才有意义。

在这种情况下，你可以将部分时间单位（`Quarter of Year`、`Month of Year`）与完整时间单位 `Year` 一起映射。这是有效的配置，因为这些不完整的时间单位可以从“年”的映射中获得完整上下文。

![使用部分时间单位的日历配置](~/content/assets/images/tutorials/calendar-simple-example.png)

> [!TIP]
> 在配置日历时，如需查看可用列及其值，请在 TOM Explorer 中右键单击日期表，然后选择 **Preview Data**。
>
> ![上下文菜单中的“Preview Data”选项](~/content/assets/images/tutorials/calendar-preview-data-button.png)
>
> 然后，你可以将“数据预览”窗口停靠在“日历编辑器”旁边，方便随时参考。
>
> ![停靠“数据预览”窗口](~/content/assets/images/tutorials/calendar-dock-example.png)
>
> 或者，你也可以使用 **DAX 查询** 窗口查询日期表，并将其与“日历编辑器”并排显示。

将日期表的表格预览窗口停靠好后，你就能在配置日历时直接看到列值：

![带日期表表格预览的日历编辑器](~/content/assets/images/tutorials/calendar-configured-example.png)

**完整时间单位：**

| 时间单位 | 说明      | 示例                  |
| ---- | ------- | ------------------- |
| 年    | 年份      | 2024、2025           |
| 季度   | 包含年份的季度 | Q1 2024、Q2 2025     |
| 月    | 包含年份的月份 | 2023 年一月，2024 年二月   |
| 周    | 包含年份的周次 | 2023年第50周，W50-2023  |
| 日期   | 日期      | 12/31/2025、4/3/2023 |

**部分时间单位**（需要先映射一个父时间单位）：

| 时间单位   | 说明      | 示例          | 需要 | 或需要以下之一                                                                                                                                                            |
| ------ | ------- | ----------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 年度季度   | 一年中的季度  | Q1，第2季度，YQ1 | 年  |                                                                                                                                                                    |
| 年度月份   | 一年中的月份  | 一月，M11，11   | 年  |                                                                                                                                                                    |
| 季度内月份  | 季度内的月份  | 1，QM2       | 季度 | <ul><li>年度季度 + 年</li></ul>                                                                                                                                         |
| 年度周次   | 一年中的周次  | 第50周，W50，50 | 年  |                                                                                                                                                                    |
| 季度内第几周 | 当季的第几周  | QW10，10     | 季度 | <ul><li>年度季度 + 年</li></ul>                                                                                                                                         |
| 当月第几周  | 当月的第几周  | MW2，2       | 月  | <ul><li>年度月份 + 年</li><li>季度内月份 + 季度</li><li>季度内月份 + 年度季度 + 年</li></ul>                                                                                             |
| 年内第几天  | 当年的第几天  | 365，D1      | 年  |                                                                                                                                                                    |
| 季度内第几天 | 当季的第几天  | QD2，50      | 季度 | <ul><li>年度季度 + 年</li></ul>                                                                                                                                         |
| 当月第几天  | 当月的第几天  | MD10，30     | 月  | <ul><li>年内月份 + 年</li><li>季度内月份 + 季度</li><li>季度内月份 + 年内季度 + 年</li></ul>                                                                                             |
| 星期几    | 一周中的某一天 | WD5、5       | 周  | <ul><li>年内周 + 年</li><li>季度内周 + 季度</li><li>季度内周 + 年内季度 + 年</li><li>月内周 + 月</li><li>月内周 + 年内月份 + 年</li><li>月内周 + 季度内月份 + 季度</li><li>月内周 + 季度内月份 + 年内季度 + 年</li></ul> |

### 关联列

当你将某列映射到一个时间单位时，该列会成为该时间单位的**主列**。也可以按需添加**关联列**，以不同格式表示同一时间单位。

例如，如果你将数值列 `MonthNumber`（包含值 1-12）映射到“年内月份”，你可能还想关联 `MonthName` 列（包含“January”“February”等）使用同一时间单位。两列表示的是同一概念，只是格式不同。

要添加关联列：

1. 在网格中选择一个已映射列的时间单位行。
2. 在右侧的**关联列**面板中，勾选要与该时间单位关联的列。

在进行时间智能计算时，关联列会获得与主列相同的筛选行为。

![日历编辑器中的“关联列”面板](~/content/assets/images/tutorials/calendar-associated-columns.png)

#### 按列排序列

当主时间单位列定义了一个 **按列排序** 列时，该 **按列排序** 列会自动被视为关联列。这可确保两列在进行时间智能计算时具有相同的筛选行为，并与 Analysis Services 处理日历配置的方式保持一致。

例如，如果你将 `MonthName` 列映射为“Month of Year”，且 `MonthName` 按 `MonthNumber` 列排序，则 `MonthNumber` 列会自动与该时间单位关联。你不需要手动将“按列排序”列添加到“关联列”面板中——日历编辑器会自动完成此操作。

### 时间相关列

除了将列映射到特定的时间单位类别外，你还可以将列标记为**时间相关**。时间相关列是指日期表中不属于某个特定时间单位类别，但在进行时间智能计算时仍应获得特殊处理的列。

时间相关列的示例包括：

- `IsHoliday` - 用于指示该日期是否为节假日的标志
- `IsWeekday` - 用于指示该日期是否为工作日的标志
- `FiscalPeriodName` - 用于描述会计期间的标签

**时间相关列的行为：**

- 在进行**横向偏移**（例如 `DATEADD` 或 `SAMEPERIODLASTYEAR`）时，会保留时间相关列上的 FILTER 筛选器，从而保持相同的粒度。
- 在进行**层级偏移**（例如 `DATESYTD` 或 `NEXTMONTH`）时，会清除时间相关列上的 FILTER 筛选器。

有关横向偏移和层级偏移的更多信息，请参阅 [Understanding lateral shift and hierarchical shift](https://www.sqlbi.com/articles/introducing-calendar-based-time-intelligence-in-dax/#:~:text=Understanding%20lateral%20shift%20and%20hierarchical%20shift)（SQLBI）。

要配置时间相关列：

1. 在日历网格底部，选择 **时间相关列** 行。
2. 在右侧的 **时间相关列** 面板中，勾选你想标记为时间相关的列。

![时间相关列面板](~/content/assets/images/tutorials/calendar-time-related-columns.png)

### 应用更改

在“日历编辑器”中所做的更改会应用到本地模型（但不会保存到磁盘），方式有两种：

- 点击工具栏中的 **Accept** 按钮，以将更改应用到本地模型。
- 当你从“日历编辑器”切换到其他位置（视图失去焦点）时，更改也会自动应用。

在离开前点击 **Cancel** 按钮，即可放弃尚未提交的更改。

要让这些更改生效，请保存模型。

## 实时验证

在配置日历时，日历编辑器会执行实时验证。验证反馈会通过网格中的图标和工具提示直接显示，帮助你在保存前识别并解决问题。

将强制执行以下规则：

1. **日历名称必须唯一**
   在语义模型中，每个日历的名称都必须唯一。如果你创建的日历名称重复，编辑器会自动追加后缀（例如“(1)”）以确保唯一性。

2. **时间单位依赖关系验证**
   部分时间单位要求其父时间单位也必须映射。例如，如果你将某列映射为“月中的日期”，则还必须将某列映射为“月”（或映射为“年中的月份” + “年”等）。编辑器会高亮显示缺少依赖项的单元格，并通过工具提示说明需要哪些父时间单位。

   ![依赖项错误，显示缺少父级时间单位](~/content/assets/images/tutorials/calendar-dependency-error.png)

3. **跨日历类别一致性**
   如果你的模型包含多个日历，则同一列在所有日历中必须关联到相同的时间单位类别。例如，如果你在一个日历中将 `FiscalYear` 列映射为“年”，则不能在另一个日历中将同一列映射为“年中的周”。

   ![跨日历类别冲突，显示“时间单位冲突”错误](~/content/assets/images/tutorials/calendar-cross-category-validation.png)

## 使用“列映射”对话框配置日历

作为日历编辑器的替代方案，你可以在 TOM Explorer 中右键单击日历，然后选择 **编辑列映射...** 来配置日历：

![编辑日历列映射](~/content/assets/images/edit-calendar-mappings.png)

此对话框允许你逐个添加列关联。点击 **Add Column Association**，然后选择 **Column Association**，以添加新的映射。对于每个关联，你都需要选择一列并将其分配给某个时间单位类别。你还可以通过展开 **Columns** 属性，为每个映射添加更多关联列。

![集合编辑器中的列关联](~/content/assets/images/tutorials/calendar-example.png)

#### 在“列映射”对话框中添加与时间相关的列

要通过这个对话框添加与时间相关的列，请点击 **添加列关联** 并选择 **列组**。这会创建一个时间相关列组，你可以在其中添加应视为时间相关的列（有关这些列行为方式的更多信息，请参阅[时间相关列](#time-related-columns)）。

![为与时间相关的列添加列组](~/content/assets/images/tutorials/calendar-collection-editor-column-group.png)

在大多数场景下，建议使用日历编辑器，因为它能更全面地呈现所有时间单位，提供实用的工具提示，并提供实时验证反馈。

## 在 DAX 中使用日历

定义好日历并映射其列后，你就可以在 DAX 计算中使用它。日历可与现有的 DAX 时间智能函数配合使用，这些函数以日期列作为输入（例如 [`TOTALYTD`](https://dax.guide/totalytd)、[`CLOSINGBALANCEMONTH`](https://dax.guide/closingbalancemonth) 和 [`DATEADD`](https://dax.guide/dateadd)）。

此外，还引入了 8 个用于按周的时间智能的新 DAX 函数。以下函数仅适用于日历：

- [`CLOSINGBALANCEWEEK`](https://dax.guide/closingbalanceweek)
- [`OPENINGBALANCEWEEK`](https://dax.guide/openingbalanceweek)
- [`STARTOFWEEK`](https://dax.guide/startofweek)
- [`ENDOFWEEK`](https://dax.guide/endofweek)
- [`NEXTWEEK`](https://dax.guide/nextweek)
- [`PREVIOUSWEEK`](https://dax.guide/previousweek)
- [`DATESWTD`](https://dax.guide/dateswtd)
- [`TOTALWTD`](https://dax.guide/totalwtd)

点击上面的链接，了解每个函数的更多信息。
