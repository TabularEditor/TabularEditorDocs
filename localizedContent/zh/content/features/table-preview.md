---
uid: table-preview
title: 表格预览
author: Morten Lønskov
updated: 2026-09-14
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

# Table Preview

A **Table Preview** shows the contents of one table, row by row, without writing a query. Right-click a table in the @tom-explorer-view and choose **Preview data**, or select the table and press **Ctrl+R**.

![预览数据](~/content/assets/images/preview-data-big.png)

You can open a preview of several tables at once and arrange them however you like. Each preview is an ordinary document, so it can be docked, floated or moved to a second monitor.

## Reading the grid

Tabular Editor executes a DAX query that returns only as many rows as the view can show, then pages in more as you scroll. How far you can scroll depends on the storage mode and the engine:

| 表                                                                                                          | Scrolling                                                                                      |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Import, on an engine that supports [`WINDOW`](https://dax.guide/window), where the table has a primary key | The full table. Paging uses `WINDOW` against the primary key                   |
| Import, without `WINDOW` support or without a primary key                                                  | The first rows only; the preview says that scrolling is disabled                               |
| DirectQuery                                                                                                | The first rows only, up to the **Row limit** preference; an informational message explains why |

Preview metadata is cached for the session, so reopening a preview does not re-query the server. Use **Refresh Preview** to re-read it if for example the model has been processed outside Tabular Editor.

If a calculated column is in an invalid state, its cells read _(Calculation needed)_. Use **Calculate Table** on the toolbar, or **Recalculate table...** on the column's right-click menu, to bring it up to date.

![重新计算表格](~/content/assets/images/recalculate-table.png)

## Column order

By default, columns appear in the order the engine returns them, which is roughly internal column order and often looks arbitrary. Tick _Sort table preview columns alphabetically_ under @preferences to have them follow the same order the TOM Explorer uses instead.

## Finding a column in a wide table

Selecting a column in the @tom-explorer-view scrolls the preview to that column and highlights it. 该功能默认开启。你可以在工具栏上取消 **跟踪所选列**，仅对单个预览关闭；也可以在 @偏好 中为所有预览关闭。

## 工具栏

**表格预览** 工具栏和对应的 **表格预览** 菜单包含相同的命令：

| 命令                                                          | 作用                                                 |
| ----------------------------------------------------------- | -------------------------------------------------- |
| **身份模拟...** | 选择预览查询运行时使用的身份，以查看特定用户会看到的数据                       |
| **刷新预览**                                                    | 重新读取该表，并丢弃缓存的元数据                                   |
| **自动刷新**                                                    | 每当已部署的模型发生更改时，自动刷新此预览。新建预览的默认设置来自 @偏好 |
| **跟踪所选列**                                                   | 如上所述，跟随 TOM Explorer 中的列选择                         |
| **计算表格**                                                    | 重新计算该表的计算列                                         |

## 右键菜单

除了标准网格命令（排序、筛选、自动调整列宽、列选择器）之外，预览网格还增加了：

| 命令                                                                           | 显示位置                                                 | 作用                                                                                                 |
| ---------------------------------------------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **锁定列宽**                                                                     | 列标题                                                  | 防止在滚动并分页加载更多行时，网格自动重新调整列宽                                                                          |
| **编辑表达式...**                 | 计算列的列标题                                              | 在 **表达式编辑器** 中打开该列的 DAX 表达式                                                                        |
| **Recalculate table...**     | Header of a calculated column that is not up to date | Recalculates the table                                                                             |
| **Show actual DAX query...** | Anywhere in the grid                                 | Opens a new, editable [DAX query](xref:dax-query) document containing the query behind the preview |

### Show actual DAX query

**Show actual DAX query...** takes the query the preview is running, including whatever filter and sort you have applied in the grid, formats it and opens it as a new DAX Query document. It is not executed for you; edit it and run it when you are ready.

The paging wrappers are deliberately left out, so what you get is the query over the data you are looking at rather than the query over one screenful of it.

> [!NOTE]
> The **DAX Query** view has a command of the same name on its results grid, but it does something different: it shows the last executed query in a read-only window rather than opening a new document.

## Filtering

Each column header carries a filter dropdown listing the column's distinct values. On a column with many distinct values the list is capped by _Max. values in filter dropdown_ under @preferences, 5,000 by default. Values beyond the cap are not listed and cannot be ticked directly. Raise the cap if you need them, bearing in mind that opening the dropdown then runs a heavier query.

## 偏好设置

Every setting mentioned on this page lives under **Tools > Preferences > Data Browsing > Table Preview**. See @preferences for the full list.

## 后续步骤

- @dax-query
- @pivot-grid
- @tom-explorer-view
