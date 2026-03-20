---
uid: script-library-advanced
title: 高级 C# 脚本
author: Morten Lønskov
updated: 2026-02-20
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# C# Script 库: 高级脚本

这些脚本更高级，功能更复杂，需要对 C# 语言和 TOM 有更深入的理解。 它们更难修改，因此建议在你已熟悉 Tabular Editor 中 C# Script 的基础之后再使用。

<br>
<br>

| <div style="width:250px">脚本名称</div>                                     | 用途                                                                       | 使用场景                                                   |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------ |
| [统计模型对象](xref:script-count-things)                                      | 按类型统计模型中各类对象的数量。                                                         | 当你需要概览模型内容，或想按类型统计对象数量时。                               |
| [在网格中输出对象详细信息](xref:script-output-things)                               | 以网格视图输出对象详细信息。                                                           | 当你需要在网格视图中输出对象详细信息以便检查时。                               |
| [创建日期表](xref:script-create-date-table)                                  | 基于模型中选定的日期列创建格式化的日期表。                                                    | 当你需要基于模板创建新的日期表时。                                      |
| [创建 M 参数（自动替换）](xref:script-create-and-replace-parameter)               | 创建新的 M 参数，并自动将其添加到 M 分区。                                                 | 当你想用动态 M 参数替换多个分区中的字符串（例如连接字符串）时。                      |
| [格式化 Power Query](xref:script-format-power-query)                       | 使用 powerqueryformatter.com API 格式化所选 M 分区中的 Power Query。 | 当 Power Query 很复杂，需要提高可读性以便阅读或修改时。                     |
| [实施增量刷新](xref:script-implement-incremental-refresh)                     | 通过 UI 对话框中的参数自动配置增量刷新。                                                   | 当你需要实施增量刷新，但不太熟悉表设置中的配置方式时。                            |
| [删除包含错误的度量值](xref:script-remove-measures-with-error)                    | 创建新的 M 参数，并自动将其添加到 M 分区。                                                 | 当你想用动态 M 参数替换多个分区中的字符串（例如连接字符串）时。                      |
| [在所选度量值中查找/替换](xref:script-find-replace)                                | 在所选度量值的 DAX 中搜索子字符串，并替换为另一个子字符串。                                         | 当你需要在多个 DAX 度量值中快速查找/替换值时（例如 `CALCULATE` 筛选器或失效的对象引用）。 |
| [Databricks 语义模型设置](xref:script-databricks-semantic-model-set-up)       | 为表和列指定友好名称，并设置列最佳实践                                                      | 当你需要让 Databricks 对象名称更便于用户理解时。                         |
| [创建 Databricks 关系](xref:script-create-databricks-relationships)         | 基于 Databricks Unity Catalog 中的主键和外键定义创建关系                                | 当你想复用 Unity Catalog 中已定义的 Databricks 关系时。              |
| [添加 Databricks 元数据说明](xref:script-add-databricks-metadata-descriptions) | 基于 Databricks Unity Catalog 更新表和列说明                                      | 当你想复用 Unity Catalog 中已定义的 Databricks 表和列注释时。           |
| [将 DL/SQL 转换为 DL/OL](xref:script-convert-dlsql-to-dlol)                 | 将 Direct Lake over SQL 模型的分区更改为 Direct Lake over OneLake                 | 可用于轻松迁移到 Direct Lake over OneLake                      |
| [将导入模式转换为 DL/OL](xref:script-convert-dlsql-to-dlol)                     | 将 Import 模型的分区更改为基于 OneLake 的 Direct Lake                                | 有助于轻松迁移到基于 OneLake 的 Direct Lake                       |
| [实现用户定义的聚合](xref:script-implement-user-defined-aggregations)            | 自动为所选事实表配置用户定义的聚合。                                                       | 当需要实现用户定义的聚合模式，但又不想手动执行每个配置步骤时。                        |