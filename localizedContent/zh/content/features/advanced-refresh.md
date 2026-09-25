---
uid: advanced-refresh
title: 高级刷新对话框
author: Daniel Otykier
updated: 2026-01-15
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.25.0
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 高级刷新对话框

**高级刷新**对话框可对数据刷新操作进行精细控制，使你能够配置刷新类型、并行度、增量刷新设置，以及覆盖配置文件。 This is useful when you need more control than the standard refresh menu options provide.

To open the Advanced Refresh dialog, go to **Model > Refresh model > Advanced...** or use the keyboard shortcut **Ctrl+Shift+F5**.

> [!Note]
> “高级刷新”对话框仅在商业版和企业版中可用。

![高级刷新菜单](~/content/assets/images/advanced-refresh-menu.png)

## 刷新范围

The refresh scope indicates which objects will be refreshed. 该范围取决于打开对话框时在 TOM Explorer 中选择的对象：

- **整个模型**：未选择任何特定的表或分区时
- **所选表**：选择一个或多个表时
- **所选分区**：选择一个或多个分区时

## 常规设置

![高级刷新对话框](~/content/assets/images/advanced-refresh.png)

### 刷新类型

“**刷新类型**”下拉列表用于选择要执行的刷新操作类型。 Available options depend on the refresh scope:

| 刷新类型     | 说明                                      | 可用性      |
| -------- | --------------------------------------- | -------- |
| **自动**   | 由 Analysis Services 根据对象的当前状态确定最合适的刷新类型 | 所有范围     |
| **完全**   | 删除所有数据，从数据源重新加载，并重新计算所有依赖对象             | 所有范围     |
| **清除**   | 删除所选对象的所有数据，但不重新加载                      | 所有范围     |
| **仅数据**  | 从数据源加载数据，但不会重新计算依赖对象                    | 所有范围     |
| **计算**   | 在不重新加载数据的情况下，重新计算所选对象及其所有依赖对象           | 所有范围     |
| **碎片整理** | 对范围内所有列的字典进行碎片整理                        | 仅限模型和表范围 |
| **追加**   | 将新数据追加到分区，而不处理现有数据                      | 仅适用于分区范围 |

### 最大并行度

The **Max Parallelism** setting controls how many objects can be processed simultaneously during the refresh operation. **0** 表示并行度不受限制；Analysis Services 会在资源允许的情况下尽可能并行处理对象。 Set a specific value to limit parallel operations, which can be useful when you want to reduce resource consumption on the server.

## 增量刷新设置

![增量刷新设置](~/content/assets/images/advanced-refresh-incremental-effective-date.png)

当刷新范围包含至少一个已配置 [增量刷新策略](xref:incremental-refresh-about) 的表时，就会显示 **增量刷新设置** 部分。 This section is not available at partition scope.

- **应用刷新策略**：选中后，刷新操作将遵循表(s)上定义的增量刷新策略，并根据该策略的滚动窗口设置创建和管理分区。
- **生效日期**：指定评估增量刷新策略时要使用的日期。 By default, this is the current date, but you can select a different date to simulate how the refresh would behave at a different point in time. This is useful for testing incremental refresh configurations.

## 刷新覆盖设置

Refresh overrides allow you to temporarily modify certain properties for the duration of a refresh operation without changing the actual model metadata. This eliminates the risk of accidentally leaving temporary modifications in your model.

### 刷新覆盖的使用场景

- **在开发期间限制数据**：覆盖分区查询，仅加载部分行（例如使用 TOP 或 WHERE 子句），从而在开发和测试期间加快刷新操作
- **从替代来源刷新**：从测试或开发数据库加载数据，而不是使用模型中配置的生产数据源
- **使用修改后的表达式进行测试**：覆盖共享表达式（M 参数）以测试不同配置

### Override profiles

覆盖配置文件会保存命名的 TMSL 覆盖配置，方便你在不同刷新操作中重复使用。

![覆盖配置文件编辑器](~/content/assets/images/advanced-refresh-edit-profile.png)

- **New...**: Creates a new override profile. You provide a profile name and the TMSL definition specifying the overrides.
- **编辑...**：修改所选覆盖配置文件。
- **删除**：删除所选覆盖配置文件。

该 TMSL 定义遵循 [TMSL 刷新命令规范](https://learn.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions)，使你能够覆盖以下对象的属性：

- 数据源
- 共享表达式
- 分区
- 数据列

> [!TIP]
> 有关可作为你自定义覆盖配置文件起点的详细示例和 TMSL 代码片段，请参阅 [刷新覆盖配置文件](xref:refresh-overrides)。

### 配置文件存储

Override profiles are stored per-model in the `UserOptions.tmuo` file. When working with model metadata saved on disk, the `.tmuo` file is stored alongside the model files. 通过 XMLA endpoint 直接连接到模型时，`.tmuo` 文件存储在 `%LocalAppData%\\TabularEditor3\\UserOptions` 下。

## 导出 TMSL 脚本

点击 **导出 TMSL 脚本...** 按钮会打开一个对话框，你可以在里面查看并复制生成的 TMSL 刷新命令。 This is useful when you want to:

- 通过其他工具（例如 SQL Server Management Studio）执行刷新命令
- 将刷新命令纳入自动化脚本或 CI/CD 管道
- 查看将发送到 Analysis Services 的确切 TMSL