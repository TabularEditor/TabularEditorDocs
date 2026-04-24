---
uid: script-library-beginner
title: 入门 C# 脚本
author: Morten Lønskov
updated: 2023-02-27
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# C# Script 库：入门脚本

这些脚本更基础，易于理解和修改。 它们的范围明确、复杂度有限；使用、理解和修改这些脚本，不需要具备扎实的 C# 语言基础。 因此，在 Tabular Editor 中开始编写 C# Script 时，这是一个很好的起点。

<br>
<br>

| <div style="width:250px">脚本名称</div>                       | 用途                                                                                                            | 使用场景                                             |
| --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [统计表行数](xref:script-count-rows)                           | 计算所选表的 COUNTROWS ( 'Table' ) 结果。                                                           | 当你想检查表中有多少行，或确认其是否已加载时。                          |
| [从列创建求和度量值](xref:script-create-sum-measures-from-columns) | 从任意选定的列创建 SUM ( 'Table'[Column] ) 度量值。 | 当新表/模型中有很多列，需要一次性创建大量度量值时。                       |
| [创建度量值表](xref:script-create-measure-table)                | 创建度量值表                                                                                                        | 当你想创建一个空表，用作整理度量值的专用表时                           |
| [创建表格组](xref:script-create-table-groups)                  | 将模型按表格组进行组织                                                                                                   | 当你想使用 Tabular Editor 3 的表格组功能来自动整理表格时            |
| [创建 M 参数](xref:script-create-m-parameter)                 | 在“共享表达式”中创建一个新的 M 参数                                                                                          | 当你需要创建一个参数，以便在其他 Power Query 查询中使用（M 分区/共享表达式）。  |
| [编辑隐藏分区](xref:script-edit-hidden-partitions)              | 在 Calc 中显示隐藏分区的属性。 组与 Calc。 表                                                                                 | 当你需要查看或编辑这些隐藏分区的 TOM 属性时。                        |
| [格式化数值度量值](xref:script-format-numeric-measures)           | 格式化所选度量值                                                                                                      | 当你想快速将格式字符串应用到当前选中的度量值时                          |
| [显示数据源依赖关系](xref:script-show-data-source-dependencies)    | 显示数据源的依赖关系                                                                                                    | 对于显式（旧式）数据源，往往很难准确知道它们被用在了哪里。 此脚本会显示哪些分区引用了所选数据源 |
| [创建字段参数](xref:create-field-parameter)                     | 快速创建字段参数表                                                                                                     | 选择需要包含在字段参数中的对象，其余工作由脚本完成                        |
| [显示唯一列值](xref:script-display-unique-column-values)        | 显示列中的唯一值                                                                                                      | 当你想查看当前选中列的唯一值时                                  |