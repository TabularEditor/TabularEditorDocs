---
uid: object-properties-calendars
title: 日历属性
author: Jeroen ter Heerdt
updated: 2026-10-05
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

# 日历属性

<!--
SUMMARY: Reference for the properties of calendars, time unit column associations and time-related column groups, used by calendar-based time intelligence.
-->

[!include[ai-assisted](../../includes/ai-assisted.partial.md)]

本页列出了日历以及构成日历的两类列组的属性。有关大多数对象共享的属性，请参见 @object-properties-common。

日历是 _基于日历的时间智能_ 背后的对象，_基于日历的时间智能_ 也称为 _增强型时间智能_。日历会告诉 DAX 时间智能函数：日期表中的哪些列保存年份、季度、月份、周等信息。有了日历，`TOTALYTD` 和 `DATEADD` 等函数就可以配合财务日历、零售日历（4-4-5）以及其他非公历使用，并且 `TOTALWTD` 等基于周的函数也随之可用。

日历由以下列组构成：

- **时间单位列关联**会将一列以及可选的其他关联列映射到某个时间单位，例如 **年** 或 **年中的月份**
- **时间相关列组**列出与时间相关但不属于某个时间单位的列，例如 `IsHoliday` 标志

这三个对象都需要 1701 或更高的兼容级别。在 Tabular Editor 3 中，**日历编辑器**会在一个网格中显示整个日历，并在你编辑时实时显示其中的错误。参见 @calendars。

## 日历

日历属于某个表，通常是日期表，并定义一种划分时间的方式，例如 `Gregorian` 或 `Fiscal`。一个表可以有多个日历。在 DAX 中，你可以用日历名称代替日期列来引用日历，例如：

```dax
TOTALYTD ( [Sales Amount], 'Fiscal' )
```

日历名称在整个模型中必须唯一。

Best Practice Analyzer (BPA) 规则 @kb.bpa-date-table-exists 会标记既没有日历、也没有标记为日期表的模型。

### 通用属性

- [名称](xref:object-properties-common#name)
- [描述](xref:object-properties-common#description)
- [对象类型](xref:object-properties-common#object-type)
- [Lineage tag](xref:object-properties-common#lineage-tag)
- [Source Lineage tag](xref:object-properties-common#source-lineage-tag)

### 日历列组

`CalendarColumnGroups` · CalendarColumnGroupCollection · 基本 · 只读

组成该日历的列组，包括其时间单位列关联和与时间相关的列组。这是该集合的 Tabular Object Model (TOM) 名称。在 **属性视图** 中，该集合显示为 `ColumnMappings`。在 C# Script 中，你可以使用这两个名称中的任意一个。

### 列映射

`ColumnMappings` · CalendarColumnGroupCollection · 基本 · 只读 · _快捷方式：指向_ **日历列组**

与 `CalendarColumnGroups` 是同一个集合，只是用了 **属性视图** 中显示的名称。你可以添加、更改和删除集合中的组。在 Tabular Editor 3 中，在 @tom-explorer-view 里双击日历，即可打开 **日历编辑器**。属性旁的 **...** 按钮，以及在 **TOM Explorer** 中右键单击日历后菜单里的 **编辑列映射...**，都会打开集合编辑器。

## 时间单位列关联

时间单位列关联会将表中的某一列映射到日历中的某个时间单位，例如将 `Fiscal Year` 列映射到 **Year**，或将 `Month Name` 列映射到 **Month of Year**。映射到该时间单位的列称为 _主列_。你可以添加用于以另一种格式表示相同时间单位的 _关联列_，例如在月份名称旁边添加月份编号。

每个时间单位在每个日历中只能映射一次。**日历编辑器** 为每个时间单位显示一行；如果该日历已映射该时间单位，C# Script 中的 `AddTimeUnit` 方法会失败。一列在一个日历中只能属于一个时间单位，并且在模型的每个日历中都必须映射到同一个时间单位。当某列在两个日历中映射到不同的时间单位，或者某个主列的排序列又是另一个时间单位的主列时，Tabular Editor 3 的 **日历编辑器** 会显示错误。

### 通用属性

- [对象类型](xref:object-properties-common#object-type)

### 主列

`PrimaryColumn` · 列 · 基本

包含此时间单位值的列。其值必须与该时间单位匹配：映射到 **Month** 的列用于标识包含年份的月份，例如 `January 2025`；而映射到 **Month of Year** 的列仅标识月份本身，例如 `January` 或 `1`。

如果主列设置了 `SortByColumn`，引擎也会将该排序列视为关联列，你无需再添加它。

若要在映射列时查看其值，请打开日期表的 @table-preview，并将其停靠在 **日历编辑器** 旁边。

### 时间单位

`TimeUnit` · 时间单位 · 基本

主列所表示的时间单位。_完整_ 的时间单位可单独标识一个时间段。_部分_ 的时间单位只能与更大的时间单位一起才能标识一个时间段，而日历也必须映射该更大的时间单位。例如，**Month of Year** 需要 **年**。

| 值                   | 类型                 | 含义              | 示例值                  |
| ------------------- | ------------------ | --------------- | -------------------- |
| `年`                 | 完整                 | 年份。             | `2024`、`FY2025`      |
| `Semester`          | 完整                 | 包含年份的半年。        | `H1 2024`            |
| `SemesterOfYear`    | 部分，需要 `年`          | 年内的半年。          | `H1`、`1`             |
| `季度`                | 完整                 | 包含年份的季度。        | `Q1 2024`            |
| `QuarterOfYear`     | 不完整，需要搭配 `Year`    | 一年中的季度。         | `Q1`, `1`            |
| `QuarterOfSemester` | 不完整，需搭配 `Semester` | 半年中的季度。         | `1`, `2`             |
| `月`                 | 完整                 | 包含年份的月份。        | `2024年一月`, `2024-01` |
| `MonthOfYear`       | 不完整，需搭配 `Year`     | 一年中的月份。         | `一月`、`1`             |
| `MonthOfSemester`   | 不完整，需搭配 `Semester` | 半年中的月份。         | 从 `1` 到 `6`          |
| `MonthOfQuarter`    | 部分，需要 `Quarter`    | 季度中的第几个月。       | `1` 到 `3`            |
| `周`                 | 完整                 | 包含年份的周次。        | `W50-2023`           |
| `年内周次`              | 部分，需要 `Year`       | 一年中的第几周。        | `W50`、`50`           |
| `半年内周次`             | 部分，需要 `Semester`   | 半年中的第几周。        | `1` 到 `27`           |
| `季度内周次`             | 部分，需要 `Quarter`    | 季度中的第几周。        | `1` 到 `14`           |
| `月内周次`              | 部分，需要 `Month`      | 月份中的第几周。        | `1` 到 `6`            |
| `日期`                | 完整                 | 日期。             | `2025-12-31`         |
| `DayOfYear`         | 不完整，需要 `Year`      | 当年的第几天。         | `1` 到 `366`          |
| `DayOfSemester`     | 不完整，需要 `Semester`  | 半年中的第几天。        | `1` 到 `184`          |
| `DayOfQuarter`      | 不完整，需要 `Quarter`   | 当季的第几天。         | `1` 到 `92`           |
| `DayOfMonth`        | 不完整，需要 `Month`     | 当月的第几天。         | `1` 到 `31`           |
| `DayOfWeek`         | 不完整，需要 `Week`      | 当周的第几天。         | `1` 到 `7`            |
| `Unknown`           |                    | 未设置时间单位。不是有效选项。 |                      |

部分时间单位也可以通过与其他部分时间单位组合来确定其更大的单位。例如，只要有 **年内月份** 和 **年**，就足以确定 **月内日**。查看 @calendars 中的依赖关系表。

TOM 定义了半年时间单位（`Semester`、`SemesterOfYear`、`QuarterOfSemester`、`MonthOfSemester`、`WeekOfSemester` 和 `DayOfSemester`），但 Power BI 不会把它们列为日历类别。 Tabular Editor 3 会在 **属性视图** 的 **时间单位** 下拉列表以及 **日历编辑器** 中隐藏这些项，并且还会从下拉列表中隐藏 `Unknown`。只有当 C# Script 或其他工具设置了这些值时，你才会看到这些值。

引擎支持半年时间单位。在 Power BI Desktop 中，使用半年时间单位构建的日历是可接受的，例如 **年**、**半年**、**年内半年**、**月** 和 **日期**，并且 `DATESYTD` 和 `SAMEPERIODLASTYEAR` 等时间智能函数也能与其配合使用。引擎会拒绝以下情况：同一个时间单位在一个日历中被映射两次，或者同一表中的两个日历将同一列映射到不同的时间单位。

表中的依赖关系也适用于半年时间单位。保存时，引擎会接受不满足这些依赖关系的日历，例如仅包含 **年内半年** 和 **日期** 的日历。当查询使用该日历时，引擎才会应用这些依赖关系：只有在更大单位也已映射时，子单位才会生效，因此只有同时映射了 **半年**，**半年内季度** 才能作为该日历的季度使用。如果时间智能函数需要某个日历没有的单位，就会报错，例如：“'DATESYTD' 使用日历 'Fiscal'，而该日历未定义此操作所需的所有类别。至少要确保已标记 'Year' 类别"。基于年份的函数，例如 `DATESYTD` 和 `SAMEPERIODLASTYEAR`，始终需要 **年** 单位，而 **半年** 不算作 **年** 单位。

### 关联列

`AssociatedColumns` · AssociatedColumnCollection · 选项 · 只读

以不同格式保存与主列相同时间单位的其他列。例如，当 `Month Number` 是 **年内月份** 的主列时，你可以将 `Month Name` 和 `Month Short Name` 添加为关联列。时间智能函数会将对这些列中任意一列的筛选视同为对主列的筛选。

你可以在该集合中添加和删除列，例如在 **日历编辑器** 的 **关联列** 面板中。

## 时间相关列组

时间相关列组会列出用于描述日期、但不映射到某个时间单位的列，例如 `IsHoliday`、`IsWorkingDay` 或 `Fiscal Period Name`。时间智能函数会根据其执行的位移类型来处理这些列上的筛选：

- _横向位移_，只有 `DATEADD` 和 `SAMEPERIODLASTYEAR` 会这样做，它会保留这些列上的筛选，因此本月的工作日会移动到去年同月的工作日
- _层级位移_，所有其他时间智能函数都会这样做，例如 `DATESYTD` 或 `NEXTMONTH`，会移除这些列上的筛选

所有时间智能函数都会保留该表中那些完全未被日历提及的列上的筛选——无论是作为时间单位，还是作为时间相关列组的一部分。仅当你希望层级偏移清除该列上的筛选器时，才将此列添加到时间相关组中。

当表中有多个日历时，引擎会对该表中的每个日历应用这些规则，包括函数未使用的日历。

### 通用属性

- [对象类型](xref:object-properties-common#object-type)

### 列

`Columns` · AssociatedColumnCollection · 选项 · 只读

组中的列。你可以在该集合中添加和删除列，例如在 **日历编辑器** 的 **时间相关列** 面板中。
