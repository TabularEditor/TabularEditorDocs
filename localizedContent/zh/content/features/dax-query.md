---
uid: dax-query
title: DAX 查询
author: Morten Lønskov
updated: 2026-11-13
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

连接到语义模型时，可通过以下三种方式之一打开该窗口：

- **文件 > 新建 > DAX 查询** 菜单项
- 工具栏快捷按钮
- 在 @table-preview 的右键菜单中选择 **显示实际 DAX 查询...**，将打开一个新的查询文档，其中包含该预览背后的查询，包括筛选和排序

![新建 Dax 查询](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

内置的上下文感知 DAX编辑器可确保在开始新查询时只提供两个有效的 DAX 关键字：DEFINE 或 EVALUATE（按 Ctrl+Space 可自行验证）

## DAX 查询选项

DAX 查询窗口提供六种不同的查询选项。

![Dax 查询工具栏](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)

1. **执行 (F5)**：如果有选中内容，则执行所选的 DAX；否则执行 DAX 查询编辑器中的整个查询。
2. **执行完整查询**：执行 DAX 查询编辑器中的整个查询
3. **执行所选内容 (Shift+F5)**：如果有选中内容，则执行所选内容。否则，会执行光标当前位置的 EVALUATE 语句。
4. **停止**：此按钮用于取消当前正在执行的查询。
5. **自动执行查询**：用于跟踪已连接的语义模型，并在模型发生变化时自动更新查询结果。例如，修改某个度量值时，它可以帮助你了解结果会如何变化。
6. **保留排序和筛选**：用于控制在执行查询时，结果网格（一个或多个）中排序和筛选状态的保留方式。提供三种偏好：
   - **从不**：每次运行查询时都会重置排序和筛选。
   - **当查询被修改时**：仅当查询结构发生变化时才会重置排序和筛选。
   - **始终**：只要新查询中仍包含这些列，就会保留排序和筛选。

“自动执行查询”和“保留排序和筛选”首选项的默认值可以在“首选项”对话框的“工具”>“首选项”>“数据浏览”>“DAX 查询”中的“基本”部分进行设置。同一页面上的**切换模型时保持文档打开**部分控制着在您打开其他模型时已打开的 DAX 查询会发生什么。请参阅[切换模型](#switching-models)。

### 切换模型

当您打开不同的模型时，打开的 DAX 查询将保持打开状态并连接到新模型。如果选中了**默认自动执行 DAX 查询**，则查询将再次针对新模型运行；否则，查询将在您下次执行时针对新模型运行。如果新模型没有可供运行的数据库（例如，从不含工作区数据库的文件加载的模型），则查询将保持打开状态，且无法执行。

若要在打开其他模型时关闭 DAX 查询，请在**工具 > 首选项 > 数据浏览 > DAX 查询**下取消选中**打开其他模型时保持 DAX 查询打开**。此选项默认为选中状态。

### 使用 DAX 查询添加或更新度量值、列和表

您可以直接通过“DAX 查询”窗口添加或更改度量值。

“应用”和“应用所选内容”也会处理 DEFINE COLUMN 和 DEFINE TABLE 语句。Tabular Editor 将在您的模型中创建相应的计算列/表，或者如果它们已存在，则更新其表达式。

将 DAX 查询中 DEFINE 的度量值、列和表应用到模型有四个选项：

![Dax 查询应用度量值](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

“应用”选项会将查询中通过 DEFINE 显式定义的所有度量值、列或表的 DAX 表达式同步到相应对象的定义中。任何尚不存在的度量值、列或表都会被创建。

“应用度量值并同步”会将 DAX 表达式应用到度量值、列或表的定义中，并保存模型。

“应用选择”和“应用选择并同步”只会应用查询编辑器当前所选范围内的度量值、列或表。

与 [DAX脚本功能](xref:dax-scripts) 不同，由于 DAX 查询语法不支持指定 Description、显示文件夹等其他属性，因此这种方式只能更新度量值的表达式属性。

右键上下文菜单中也新增了“应用”选项。

![Dax 查询 右键应用](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

这些命令的快捷键为：

- 应用 (F7)
- 应用度量值并同步 (Shift+F7)
- 应用选择 (F8)
- 应用所选内容并同步 (Shift+F8)

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

在同一个 DAX 查询中包含多个 EVALUATE 语句完全可行。这种查询类型最常见于 Power BI 性能分析器的查询。

下面的语句会返回两张表，但会在结果窗格中分别显示在不同的结果标签页中。

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![Dax 查询 Evaluate 多个表](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## 调试 DAX 查询

DAX 查询是可以运行 [DAX 调试器](xref:dax-debugger) 的两个位置之一；另一个是 Pivot Grid。

DAX调试器使你能够理解 DAX 在单个单元格中是如何工作的。要启动调试器，只需在目标单元格上右键单击并选择“调试单元格”，调试器将以所选单元格为上下文启动。

调试器将单步执行查询使用 `DEFINE MEASURE` 或 `DEFINE FUNCTION` 定义的度量值和函数，并且在您停止调试之前，查询将处于只读状态。查询重新定义的度量值或函数仅适用于查询自身的代码，而使用该度量值或函数的模型度量值则保留模型的定义。请参阅[DAX查询中定义的代码](xref:dax-debugger#code-defined-in-the-dax-query)。

![Dax 查询 调试器](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## 导出 DAX 查询结果

您可以将 DAX 查询的结果导出为 CSV 或 Excel。运行DAX查询后，工具栏中会激活一个按钮，使用户能够以CSV或Excel格式将结果保存到本地。

> [!TIP]
> 要导出超过 1001 行的数据，请在运行 DAX 查询后选择“单击以获取所有行”

![Dax 查询 导出数据](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
