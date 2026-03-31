---
uid: script-library-advanced
title: 高级 C# Script
author: Morten Lønskov
updated: 2026-02-20
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# C# Script 库：高级脚本

这些脚本更加高级，功能也更复杂，需要对 C# 语言和 TOM 有更深入的理解。 这些脚本更加高级，功能也更复杂，需要对 C# 语言和 TOM 有更深入的理解。 这些脚本更难修改，因此建议你在熟悉 Tabular Editor 中的 C# Script 基础后再使用。

<br>
<br>

| <div style="width:250px">脚本名称</div>                                                      | 用途                                                                      | 适用场景                                                   |
| ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------ |
| [统计模型对象数量](xref:script-count-things)                                                     | 统计模型中各类对象的数量。                                                           | 当你需要概览模型内容，或需要按类型统计对象数量时。                              |
| [在网格中输出对象详细信息](xref:script-output-things)                                                | 在网格视图中输出对象详细信息。                                                         | 当你需要在网格视图中输出对象详细信息以便检查时。                               |
| [创建日期表](xref:script-create-date-table)                                                   | 根据模型中选定的日期列创建带格式的日期表。                                                   | 当你需要基于模板创建新的日期表时。                                      |
| [创建 M 参数（自动替换）](xref:script-create-and-replace-parameter)                                | 创建新的 M 参数，并自动将其添加到 M 分区中。                                               | 当你想用动态 M 参数替换多个分区中的字符串（例如连接字符串）时。                      |
| [格式化 Power Query](xref:script-format-power-query)                                        | 使用 powerqueryformatter.com API 格式化所选 M 分区的 Power Query。 | 当 Power Query 很复杂，需要让它更便于阅读或修改时。                       |
| [实现增量刷新](xref:script-implement-incremental-refresh)                                      | 使用 UI 对话框中的参数自动配置增量刷新。                                                  | 当你需要实现增量刷新，但不太熟悉表设置中的相关配置时。                            |
| [删除出错的度量值](xref:script-remove-measures-with-error)                                       | 创建新的 M 参数，并自动将其添加到 M 分区。                                                | 当你想用动态 M 参数替换多个分区中的字符串（例如连接字符串）时。                      |
| [在所选度量值中查找/替换](xref:script-find-replace)                                                 | 在所选度量值的 DAX 中搜索子字符串，并将其替换为另一个子字符串。                                      | 当你需要在多个 DAX 度量值中快速查找/替换值时（例如 `CALCULATE` 筛选器或无效的对象引用）。 |
| [设置 Databricks 语义模型](xref:script-databricks-semantic-model-set-up)                       | 为表和列设置更友好的名称，并应用列最佳实践                                                   | 当需要让 Databricks 对象名称更友好、更易读时。                          |
| [创建 Databricks 关系](xref:script-create-databricks-relationships)                          | 根据 Databricks Unity Catalog 中的主键和外键定义创建关系                               | 当你想复用已在 Unity Catalog 中定义的 Databricks 关系时。             |
| [添加 Databricks 元数据描述](xref:script-add-databricks-metadata-descriptions)                  | 根据 Databricks Unity Catalog 更新表和列的描述                                    | 当你想重用已在 Unity Catalog 中定义的 Databricks 表和列注释时。          |
| [将 Direct Lake over SQL 转换为 Direct Lake over OneLake](xref:script-convert-dlsql-to-dlol) | 将 Direct Lake over SQL 模型的分区更改为 Direct Lake over OneLake                | 适用于轻松迁移到 Direct Lake over OneLake                      |
| [将导入模式转换为 DL/OL](xref:script-convert-import-to-dlol)                                     | 将导入模式模型的分区更改为 Direct Lake over OneLake                                  | 便于轻松迁移到 OneLake 上的 Direct Lake                         |
| [将 DL/OL 转换为导入模式](xref:script-convert-dlol-to-import)                                    | 将 OneLake 上的 Direct Lake 模型分区切换为导入模式                                    | 便于轻松从 OneLake 上的 Direct Lake 迁移到导入模式                   |
| [实现用户自定义聚合](xref:script-implement-user-defined-aggregations)                             | 自动为所选事实表配置用户自定义聚合。                                                      | 当您希望在不手动执行每个配置步骤的情况下实现用户自定义聚合模式时。                      |