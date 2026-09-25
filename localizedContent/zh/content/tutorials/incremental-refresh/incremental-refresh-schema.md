---
uid: incremental-refresh-schema
title: 在使用增量刷新的表中添加或删除列
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 修改增量刷新表的架构

![增量刷新工作区模式 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-update-schema-header.png)

---

> [!IMPORTANT]
> 使用 Tabular Editor 3 设置增量刷新仅限于托管在 Power BI Datasets 服务中的数据集。 For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

---

**当在已配置增量刷新的表中添加或删除列时，必须更新表架构。** 通常，这与更新单分区表的表架构遵循的流程相同。 Tabular Editor can detect and update the schema for you, automatically:

1. **检测架构更改：** 右键单击该表，然后选择 _“更新表架构...”_。

<img src="~/content/assets/images/tutorials/incremental-refresh-update-table-schema.png" class="noscale" alt="Update Table Schema" style="width:450px !important"/>

2. **应用检测到的架构更改：** 在 _“应用架构更改”_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击该表，然后选择 _“应用刷新策略”_。

<img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

5. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

<img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

### 使用增量刷新时的架构更新注意事项

- For Incremental Refresh, the main consideration is that **all partitions must be refreshed**.<br />To do this, **select and right-click all partitions. Select _Refresh > Full refresh (partition)_**.

- A second consideration is **the _Source Expression_ and _Polling Expression_ may need to be updated to reflect schema changes**. Not updating these M Expressions may result in refresh errors. 示例：
  - `Table.TransformColumnTypes` 步骤引用了一个将在更新后的架构中被删除的列。
  - `Table.SelectColumns` 步骤列出了要保留的列；新列没有添加到该列表中。

<div class="WARNING">
  <h5>CHECK M EXPRESSIONS BEFORE UPDATING THE TABLE SCHEMA</h5>
  <p>如果架构更改源自数据源，你可能仍需要修改 Power Query 的 <b><em>源表达式</em></b> 或 <b><em>轮询表达式</em></b>。 It is recommended that you carefully check these expressions before using <em>'Update table schema...'</em></p>
</div>

---

### 删除列

根据列是从哪里删除的，可能需要遵循略有不同的流程：

# [受支持的数据源](#tab/removingfromsource)

对于在 **数据源** 中删除的列（即从 Power BI 访问的视图中移除），按以下步骤操作：

1. **检测架构更改：** 右键单击该表，然后选择 _'更新表架构...'_。
2. **应用检测到的架构更改：** 在 _'应用架构更改'_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。
5. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

# [Power Query](#tab/removingfrompq)

对于通过 **Power Query** 删除的列（即使用 `Table.RemoveColumns`），按以下步骤操作：

1. **检测架构更改：** 右键单击该表，然后选择 _'更新表架构...'_。
2. **应用检测到的架构更改：** 在 _'应用架构更改'_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。
5. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

# [不受支持的数据源](#tab/removingfromunsupportedsource)

如果无法通过表的上下文菜单中的 _“更新表架构...”_ 来 **自动更新表架构**，请按以下步骤操作。 These steps are the same for both columns removed in the data source or in Power Query.

1. **选择源表达式：** 选中该表后，在 _表达式编辑器_ 窗口中，从左上角的下拉列表中选择 _源表达式_。
2. **更新 Power Query 表达式：** 如适用，检查并删除对已移除列的所有命名引用。如果该列是通过 Power Query 排除的，可在此进行相应更改。
3. **手动更新架构：** 从表中删除该数据列对象。
4. **应用更改：** 部署模型更改。
5. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。
6. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

***

<div class="NOTE">
  <h5>DELETED COLUMN OBJECTS MAY STILL BE QUERIED</h5>
  <p>从模型中删除列对象，并不会阻止它们被查询——只要它们仍存在于数据源中，且没有在 Native Query 或 <b><em>Source Expression</em></b> 中删除。 Columns queried but not used can have a negative impact on refresh time and resource usage. It is recommended that you remove columns from both metadata and either data sources (i.e. views) or in the <b><em>Source Expression</em></b>.</p>
</div>

---

### 添加列

根据列的添加位置，你可能需要遵循略有不同的流程：

# [受支持的数据源](#tab/addingfromsource)

对于在 **数据源** 中新增的列（也就是添加到 Power BI 访问的视图里的列），按以下步骤操作：

1. **检测架构更改：** 右键单击该表，然后选择 _“更新表架构...”_。
2. **应用检测到的架构更改：** 在 _“应用架构更改”_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击表，然后选择 _应用刷新策略_。
5. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

# [Power Query](#tab/addingfrompq)

对于通过 **Power Query** 移除的列（即使用 `Table.AddColumns`），请按以下步骤操作：

1. **检测架构更改：** 右键单击表，然后选择 _“更新表架构...”_。
2. **应用检测到的架构更改：** 在 _“应用架构更改”_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击表，然后选择 _应用刷新策略_。
5. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

# [不支持的数据源](#tab/addingfromunsupportedsource)

如果无法通过表的上下文菜单中的 _“更新表架构...”_ 来 **自动更新表架构**，请按以下步骤操作。 These steps are the same for both columns removed in the data source or in Power Query.

1. **选择源表达式：** 选中表后，在 _表达式编辑器_ 窗口中，从左上角的下拉列表中选择 _源表达式_。
2. **更新 Power Query 表达式：** 如适用，检查并删除对已移除列的所有命名引用。如果该列是通过 Power Query 排除的，可在此进行相应更改。
3. **手动更新架构：** 右键单击表，然后选择 _创建 > 数据列_。 Name the column appropriately.
4. **配置新列：** 将该列的 `data type` 属性设置为合适的值。 Set the `Source Column` property such that it matches the source. Any additional properties can also be configured (i.e. `Format String`, `SummarizeBy`, `Data Category`...) 并可将该列添加到相应的显示文件夹中。
5. **应用更改：** 部署模型的更改。
6. **应用刷新策略：** 右键单击表，然后选择 _应用刷新策略_。
7. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

***