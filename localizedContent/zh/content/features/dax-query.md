---
uid: dax-query
title: DAX 查询
author: Morten Lønskov
updated: 2026-10-11
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

Tabular Editor 具有内置的 DAX 查询窗口，用于编写和执行针对语义模型的 DAX 查询。

DAX 查询的一个常见用例是 [Power BI 性能分析器](https://www.sqlbi.com/articles/introducing-the-power-bi-performance-analyzer/)生成的 DAX 查询，其中可以复制每个视觉对象的查询，用于故障排除、调试或详细的性能分析。

连接到语义模型时，可以通过以下三种方式中的任意一种打开该窗口：

- **“文件”>“新建”>“DAX 查询”**菜单
- 工具栏快捷方式
- @table-preview 右键菜单上的**显示实际 DAX 查询…**，这将打开一个新查询文档，其中包含预览背后的查询，包括筛选和排序

![新建DAX查询](~/content/assets/images/features/dax_query_window/create_new_dax_query.png)

内置的上下文感知 DAX 编辑器可确保在开始新查询时，仅提供两个有效的 DAX 关键字：DEFINE 或 EVALUATE（按 Ctrl+空格键自行验证）

## DAX 查询选项

DAX 查询窗口有六个不同的查询选项。

![DAX查询工具栏](~/content/assets/images/features/dax_query_window/dax_query_toolbar.png)


1. **执行 (F5)**：如果存在选定内容，则执行选定的DAX；否则，执行DAX查询编辑器中的完整查询。
2. **执行完整查询**：执行DAX查询编辑器中的完整查询。
3. **执行所选内容 (Shift+F5)**：如果存在所选内容，则执行该内容。否则，它将执行光标当前所在位置的 EVALUATE 语句。
4. **停止**：此按钮可取消当前查询的执行。
5. **自动执行查询**：它允许跟踪连接的语义模型，并在模型中发生任何更改时更新查询结果。这对于了解（例如）修改度量值后其结果如何变化很有帮助。
6. **保留排序和筛选**：它允许用户控制在执行查询时如何在结果网格中保留排序和筛选。有三种偏好可用：
   - **从不**：每次运行查询时，排序和过滤都会重置。
   - **当查询被修改时**：仅当查询结构发生变化时，才会重置排序和筛选。
   - **始终**：只要列在新查询中仍然存在，排序和筛选就会保持不变。

“自动执行查询”和“保留排序和筛选”偏好的默认值可以在“偏好”对话框中设置：**工具 > 偏好… > 数据浏览 > DAX 查询** > 基本。同一页面上的**切换模型时保持文档打开**部分控制着当您打开不同的模型时，打开的 DAX 查询会发生什么情况。请参阅[切换模型](#switching-models)。

### 切换模型

当您打开其他模型时，打开的 DAX 查询将保持打开状态并连接到新模型。如果选中了**默认自动执行 DAX 查询**，则查询将再次针对新模型运行；否则，查询将在您下次执行时针对新模型运行。如果新模型没有可供运行的数据库（例如，从不含工作区数据库的文件加载的模型），则查询将保持打开状态，且无法执行。

要<unused55><unused54>在打开其他模型时关闭 DAX 查询，请在**工具 > 首选项 > 数据浏览 > DAX 查询**下取消选中**打开其他模型时保持 DAX 查询打开**。此选项默认为选中状态。

### 使用 DAX 查询添加或更新度量值、列和表

Tabular Editor（3.12.0 及更高版本）具备直接通过 DAX 查询窗口添加或更改度量值的功能。

从 Tabular Editor 3.23.0 开始，“应用”和“应用所选内容”也会处理 DEFINE COLUMN 和 DEFINE TABLE 语句。Tabular Editor 将在您的模型中创建相应的计算列/表，或者如果它们已存在，则更新其表达式。

将 DAX 查询定义的度量值、列和表格应用于模型有四种选项： 

![DAX查询应用度量值](~/content/assets/images/features/dax_query_window/dax_query_apply_measure.png)

“应用”选项将查询中显式定义的所有度量值、列或表的 DAX 表达式同步到对象的定义。将创建所有尚不存在的度量值、列或表格。

“应用度量值并同步”将 DAX 表达式应用于度量值、列或表格的定义，并保存模型。

“应用选定内容”和“应用选定内容并同步”将仅应用查询编辑器当前选定内容中的度量值、列或表。

与[DAX脚本功能](xref:dax-scripts)不同，只能以这种方式更新度量值的表达式属性，因为DAX查询语法不支持指定其他属性，例如“描述”、“显示文件夹”等。

“应用”选项也已添加到右键单击上下文菜单中。

![DAX查询应用右键单击](~/content/assets/images/features/dax_query_window/dax_query_apply_measure_right_click.png)

这些命令的快捷键如下：

- 应用 (F7)
- 应用度量值并同步 (Shift+F7)
- 应用选定内容 (F8)
- 应用选定内容并同步 (Shift+F8)

## DAX 查询示例

DAX查询始终返回结果表，要创建的最简单的DAX查询形式是评估模型中表的查询。

```DAX
EVALUATE
Products
```

![DAX查询评估表](~/content/assets/images/features/dax_query_window/evaluate_table.png)

也可以返回 Measure 的值，但 Measure 名称前后需要使用表构造函数 {} ，以便将标量值转换为 1x1 表。

```DAX
EVALUATE
{ [Invoice Lines] }
```

![DAX查询EVALUATE度量值](~/content/assets/images/features/dax_query_window/evaluate_measure.png)

### 多个 EVALUATE 语句

完全可以在同一个 DAX 查询中包含多个 EVALUATE 语句。这种查询类型最常出现在 Power BI 性能分析器查询中。

在以下语句中返回两个表格，但作为结果窗格中单独的行选项卡。

```DAX
EVALUATE
Products

EVALUATE
Customers
```

![DAX查询评估多个表](~/content/assets/images/features/dax_query_window/multiple_evaluate_table.png)

## 调试 DAX 查询

DAX查询是可运行[DAX调试器](xref:dax-debugger)的两个位置之一，另一个是Pivot Grid。

DAX 调试器提供了了解 DAX 在单个单元格内如何工作的能力。要启动调试器，只需右键单击所需单元格，然后选择“调试单元格”，即可在所选单元格的上下文中启动调试器。

![DAX查询调试器](~/content/assets/images/features/dax_query_window/dax_query_open_dax_debugger.gif)

## 导出 DAX 查询结果

从 3.16.0 版本开始，Tabular Editor 3 引入了将 DAX 查询结果导出为 CSV 或 Excel 的新功能。运行 DAX 查询后，工具栏中会激活一个按钮，使用户能够以 CSV 或 Excel 格式将结果保存到本地。

> [!TIP]
> 要导出超过 1001 行，请在运行 DAX 查询后选择“单击以获取所有行”

![DAX查询导出数据](~/content/assets/images/features/dax_query_window/dax_query_export_data.png)
