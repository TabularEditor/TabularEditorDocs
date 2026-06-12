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
> 使用 Tabular Editor 3 设置增量刷新仅限于托管在 Power BI Datasets 服务中的数据集。 在 Analysis Services 中，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。 在 Analysis Services 中，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

---

**当在已配置增量刷新的表中添加或删除列时，必须更新表架构。** 通常，这与更新单分区表的表架构遵循的流程相同。 Tabular Editor 可以自动为你检测并更新架构： Tabular Editor 可以自动为你检测并更新架构：

1. **检测架构更改：** 右键单击该表，然后选择 _“更新表架构...”_。

  <img src="~/content/assets/images/tutorials/incremental-refresh-update-table-schema.png" class="noscale" alt="Update Table Schema" style="width:450px !important"/>

2. **应用检测到的架构更改：** 在 _“应用架构更改”_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击该表，然后选择 _“应用刷新策略”_。

  <img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

5. **刷新所有分区：** 按住 Shift 键并单击，以选中所有分区。 右键单击并选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表并选择 _“预览数据”_ 来查看结果。

  <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

### 使用增量刷新时的架构更新注意事项

- 对于增量刷新，最重要的一点是：**必须刷新所有分区**。<br />为此，**选中所有分区，然后右键单击。 选择 _刷新 > 完全刷新（分区）_**。

- 第二点需要注意的是：**可能需要更新 _源表达式_ 和 _轮询表达式_，以反映架构更改**。 如果不更新这些 M 表达式，可能会导致刷新错误。 示例：
  - `Table.TransformColumnTypes` 步骤引用了一个将在更新后的架构中被删除的列。
  - `Table.SelectColumns` 步骤列出了要保留的列；新列没有添加到该列表中。

<div class="WARNING">
  <h5>在更新表架构之前检查 M 表达式</h5>
  <p>如果架构更改源自数据源，你可能仍需要修改 Power Query 的 <b><em>源表达式</em></b> 或 <b><em>轮询表达式</em></b>。 建议在使用 <em>'更新表架构...'</em> 之前仔细检查这些表达式 建议在使用 <em>'更新表架构...'</em> 之前仔细检查这些表达式</p>
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
5. **刷新所有分区：** 按住 Shift 并单击以选择所有分区。 右键单击并选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表并选择 _'预览数据'_ 来查看结果。

# [Power Query](#tab/removingfrompq)

对于通过 **Power Query** 删除的列（即使用 `Table.RemoveColumns`），按以下步骤操作：

1. **检测架构更改：** 右键单击该表，然后选择 _'更新表架构...'_。
2. **应用检测到的架构更改：** 在 _'应用架构更改'_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。
5. **刷新所有分区：** 按住 Shift 键并单击，即可选中所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表，然后选择 _“预览数据”_ 以查看结果。

# [不受支持的数据源](#tab/removingfromunsupportedsource)

如果你在表的上下文菜单中使用 _“更新表架构...”_ 时__无法自动更新表架构__，请按以下步骤操作。 无论列是在数据源中删除，还是在 Power Query 中删除，这些步骤都相同。

1. **选择源表达式：** 选中该表后，在 _表达式编辑器_ 窗口中，从左上角的下拉列表中选择 _源表达式_。
2. **更新 Power Query 表达式：** 如适用，请检查并删除对已移除列的任何命名引用。 如果该列是通过 Power Query 排除的，你可以在此进行相应更改。
3. **手动更新架构：** 从表中删除该数据列对象。
4. **应用更改：** 部署模型更改。
5. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。
6. **刷新所有分区：** 按住 Shift 键并单击，即可选中所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表，然后选择 _“预览数据”_ 以查看结果。

***

<div class="NOTE">
  <h5>已删除的列对象仍可能被查询</h5>
  <p>从模型中删除列对象，并不会阻止它们被查询——只要它们仍存在于数据源中，且没有在 Native Query 或 <b><em>Source Expression</em></b> 中删除。 已查询但未使用的列会对刷新时间和资源使用产生负面影响。 建议同时从元数据中删除这些列，并在数据源（例如视图）或 <b><em>Source Expression</em></b> 中将其移除。 已查询但未使用的列会对刷新时间和资源使用产生负面影响。 建议同时从元数据中删除这些列，并在数据源（例如视图）或 <b><em>Source Expression</em></b> 中将其移除。</p>
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
5. **刷新所有分区：** 按住 Shift 键并单击以选择所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 可右键单击该表并选择 _“预览数据”_ 查看结果。

# [Power Query](#tab/addingfrompq)

对于通过 **Power Query** 移除的列（即使用 `Table.AddColumns`），请按以下步骤操作：

1. **检测架构更改：** 右键单击表，然后选择 _“更新表架构...”_。
2. **应用检测到的架构更改：** 在 _“应用架构更改”_ 对话框中，确认所需的架构更改。
3. **应用更改：** 部署模型更改。
4. **应用刷新策略：** 右键单击表，然后选择 _应用刷新策略_。
5. **刷新所有分区：** 按住 Shift 键并单击以选择所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 可右键单击该表并选择 _“预览数据”_ 查看结果。

# [不支持的数据源](#tab/addingfromunsupportedsource)

如果你在表的上下文菜单中使用 _“更新表架构...”_ 时__无法自动更新表架构__，请按以下步骤操作。 无论列是在数据源中删除，还是在 Power Query 中删除，这些步骤都相同。 无论列是在数据源中删除还是在 Power Query 中删除，这些步骤都相同。

1. **选择源表达式：** 选中表后，在 _表达式编辑器_ 窗口中，从左上角的下拉列表中选择 _源表达式_。
2. **更新 Power Query 表达式：** 如适用，检查并删除对已移除列的所有命名引用。 如果该列是通过 Power Query 排除的，可在此进行相应更改。 **更新 Power Query 表达式：** 如适用，请检查并删除对已移除列的任何命名引用。 如果该列是通过 Power Query 排除的，你可以在此进行相应更改。
3. **手动更新架构：** 右键单击表，然后选择 _创建 > 数据列_。 为该列设置合适的名称。 为该列设置合适的名称。
4. **配置新列：** 将该列的 `data type` 属性设置为合适的值。 将 `Source Column` 属性设置为与源一致。 还可以配置其他附加属性（例如 `Format String`、`SummarizeBy`、`Data Category`...） 将 `Source Column` 属性设置为与源一致。 还可以配置其他附加属性（例如 `Format String`、`SummarizeBy`、`Data Category`...） 并可将该列添加到相应的显示文件夹中。
5. **应用更改：** 部署模型的更改。
6. **应用刷新策略：** 右键单击表，然后选择 _应用刷新策略_。
7. **刷新所有分区：** 按住 Shift 键并单击，以选择所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 你可以右键单击表，然后选择 _'预览数据'_ 来查看结果。

***