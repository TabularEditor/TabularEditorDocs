---
uid: dax-query
title: DAX 查询
author: Morten Lønskov
updated: 2025-08-27
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

# DAX 查询

Tabular Editor 内置 DAX 查询窗口，可针对语义模型编写并执行 DAX 查询。

DAX 查询的一个常见用例是由 [Power BI 性能分析器](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/) 生成的 DAX 查询：可以复制每个 Visual 的查询，用于故障排查、调试或更深入的性能分析。

连接到语义模型时，你可以通过 **文件 > 新建 > DAX 查询** 菜单或工具栏快捷方式打开该窗口。

![新建 Dax 查询](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

内置的上下文感知 DAX编辑器可确保在开始新查询时只提供两个有效的 DAX 关键字：DEFINE 或 EVALUATE（按 Ctrl+Space 可自行验证）

## DAX 查询选项

DAX 查询窗口提供五种不同的查询选项。

![Dax 查询工具栏](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)

1. **执行 (F5)**：如果有选中内容，则执行所选的 DAX；否则执行 DAX 查询编辑器中的整个查询。
2. **执行完整查询**：执行 DAX 查询编辑器中的整个查询
3. **执行所选内容 (Shift+F5)**：如果有选中内容，则执行所选内容。 否则，会执行光标当前位置的 EVALUATE 语句。
4. **停止**：此按钮用于取消当前正在执行的查询。
5. **自动执行查询**：用于跟踪已连接的语义模型，并在模型发生变化时自动更新查询结果。 例如，修改某个度量值时，它可以帮助你了解结果会如何变化。
6. **保留排序和筛选**：用于控制在执行查询时，结果网格（一个或多个）中排序和筛选状态的保留方式。 提供三种偏好：
   - **从不**：每次运行查询时都会重置排序和筛选。
   - **当查询被修改时**：仅当查询结构发生变化时才会重置排序和筛选。
   - **始终**：只要新查询中仍包含这些列，就会保留排序和筛选。

“自动执行查询”和“保留排序和筛选”偏好的默认值可在“偏好设置”对话框中配置：**工具 > 偏好设置…… > 数据浏览 > DAX 查询** > 基本。

### 使用 DAX 查询添加或更新度量值、列和表

Tabular Editor（3.12.0 及更高版本）支持通过 DAX 查询窗口直接添加或更改度量值。

从 Tabular Editor 3.23.0 起，“应用”和“应用选择”也会处理 DEFINE COLUMN 和 DEFINE TABLE 语句。 Tabular Editor 会在模型中创建相应的计算列/计算表；如果它们已存在，则会更新其表达式。

将 DAX 查询中 DEFINE 的度量值、列和表应用到模型有四个选项：

![Dax 查询应用度量值](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

“应用”选项会将查询中通过 DEFINE 显式定义的所有度量值、列或表的 DAX 表达式同步到相应对象的定义中。 任何尚不存在的度量值、列或表都会被创建。

“应用度量值并同步”会将 DAX 表达式应用到度量值、列或表的定义中，并保存模型。

“应用选择”和“应用选择并同步”只会应用查询编辑器当前所选范围内的度量值、列或表。

与 [DAX脚本功能](xrefid:dax-scripts) 不同，由于 DAX 查询语法不支持指定说明、显示文件夹等其他属性，所以这种方式只能更新度量值的“表达式”属性。

右键上下文菜单中也新增了“应用”选项。

![Dax 查询 右键应用](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

这些命令的快捷键为：

- 应用 (F7)
- 应用度量值并同步 (Shift+F7)
- 应用选择 (F8)
- 应用选择并同步 (Shift F7)

## DAX 查询示例

DAX 查询始终会返回一张结果表。最简单的 DAX 查询形式，就是对模型中的某张表进行求值。

```DAX
EVALUATE
Products
```

![Dax 查询 Evaluate 表](~/content/assets/images/features/dax_query_window/evaluate_table.png)

也可以返回某个度量值，但需要在度量值名称外用表构造器 {} 包裹，将标量值转换为一张 1x1 表。

```DAX
EVALUATE
{ [Invoice Lines] }
```

![Dax 查询 Evaluate 度量值](~/content/assets/images/features/dax_query_window/evaluate_measure.png)

### 多个 EVALUATE 语句

在同一个 DAX 查询中包含多个 EVALUATE 语句完全可行。 这种查询类型最常见于 Power BI 性能分析器的查询。

下面的语句会返回两张表，但会在结果窗格中分别显示在不同的结果标签页中。

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Dax 查询 Evaluate 多个表](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## 调试 DAX 查询

DAX 查询是可以运行 [DAX调试器](xrefid:dax-debugger) 的两个位置之一，另一个是 Pivot Grid。

DAX调试器使你能够理解 DAX 在单个单元格中是如何工作的。 要启动调试器，只需在目标单元格上右键单击并选择“调试单元格”，调试器将以所选单元格为上下文启动。

![Dax 查询 调试器](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## 导出 DAX 查询结果

Tabular Editor 3 从 3.16.0 版本开始，新增将 DAX 查询结果导出为 CSV 或 Excel 的功能。 运行 DAX 查询后，工具栏上会激活一个按钮，让你可以将结果以 CSV 或 Excel 格式保存到本地。

> [!TIP]
> 要导出超过 1001 行的数据，请在运行 DAX 查询后选择“单击以获取所有行”

![Dax 查询 导出数据](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
