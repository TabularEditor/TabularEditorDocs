---
uid: incremental-refresh-modify
title: 修改现有刷新策略
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

# 修改增量刷新

![增量刷新 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-modify-a-refresh-policy.png)

---

**Incremental Refresh is changed by adjusting the Refresh Policy properties.** Depending on what you want to change, you will adjust a different property. A full overview of these properties is [here](xref:incremental-refresh-about#overview-of-all-properties).

> [!IMPORTANT]
> 使用 Tabular Editor 3 设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。 For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

---

## 更改增量刷新

下面是修改现有刷新策略的一般步骤：

1. **连接：** 连接到模型。

2. **选择表：** 选择已配置增量刷新的表。

3. **找到“刷新策略”属性：** 在 _Properties_ 窗口中，进入 _刷新策略_ 部分。

   <img src="~/content/assets/images/tutorials/Incremental-refresh-properties.png" class="noscale" alt="Properties of Incremental Refresh" style="width:704px !important"/>

4. **Change the property:** Change the **Property** specified in the below sections, depending on what you want to change. 有关所有刷新策略属性及其作用的概览，请参阅[此处](xref:incremental-refresh-about#overview-of-all-properties)。

5. **应用更改：** 部署模型更改。

6. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。

   <img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

7. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

   <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

以下是对现有“刷新策略”可能进行的常见更改概览：

### 扩展或缩小已归档数据的窗口

**目的：** 增加或减少模型中的数据量。

**属性：** <span style="color:#BC4A47">_RollingWindowPeriods_</span>。 Increase to extend the window (more data); decrease to reduce the window (less data).

**注意：** 你也可以更改 <span style="color:#BC4A47">_RollingWindowGranularity_</span> 来进行更细粒度的选择，例如从 3 年改为 36 个月。

<br></br>

---

<br></br>

### 扩展或缩小已刷新数据的窗口

**目的：** 在计划刷新操作中，增加或减少要刷新的数据量。

**属性：** <span style="color:#455C86">_IncrementalWindowPeriods_</span>。 Increase to extend the window (more data); decrease to reduce the window (less data).

**注意：** 你也可以更改 <span style="color:#455C86">_IncrementalWindowGranularity_</span> 来进行更细粒度的选择，例如从 3 年改为 36 个月。

<br></br>

---

<br></br>

### 仅刷新完整周期

**目的：** 从 <span style="color:#BC4A47">滚动窗口</span> 中排除不完整（未完成）的周期

**属性：** <span style="color:#455C86">_IncrementalWindowPeriodsOffset_</span>。 Set the value to `-1` to offset the period by 1, excluding the current period.

**注意：** 你还可以进一步偏移该窗口，例如只刷新最近一个完整周期之前的那些周期。

<br></br>

---

<br></br>

### 更改增量刷新模式

**目的：** 用于将表从 `Import` 切换到 `Hybrid`，或反向切换。

**属性：** _Mode_

**注意：** 按以下流程更改增量刷新模式：

1. 将 _Mode_ 设置为所需的 `Import` 或 `Hybrid` 值
2. 右键单击该表，然后选择 _应用刷新策略_
3. 部署模型更改
4. Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

> [!NOTE]
> It is recommended to check that the Rolling Window is appropriately set for the selected _Mode_. When switching from `Import` to `Hybrid` Mode, the latest Policy Range Partition will become the DirectQuery partition. You may wish to opt for a more fine-grain window, to limit the amount of data queried with DirectQuery.

<br></br>

---

<br></br>

### 配置“检测数据更改”

**目的：** 设置为：当日期列（例如 _LastUpdate_）的值发生变化时，刷新已归档数据。

**Property:** _PollingExpression_. Add a valid M Expression which returns a maximum date value for a column. All records containing that date will be refreshed, irrespective of their partition.

**注意：** 按以下流程配置“检测数据更改”：

1. 选中该表后，在 _表达式编辑器_ 窗口中，从左上角下拉列表中选择 _Polling Expression_
2. 复制下面的 M 表达式，并将 _LastUpdate_ 替换为所需的列名。

```M
// Retrieves the maximum value of the column [LastUpdate]
// Replace LastUpdate with your own column name
// The data will refresh for any records where the value in this column
//    equals the maximum value in the column across the entire table
let
    #"maxLastUpdate" =
        List.Max(
            // Replace the below with your column and table name
            Orders[LastUpdate] 
        ),

    accountForNu11 =
        if #"maxLastUpdate" = null
        then #datetime(1901, 01, 01, 00, 00, 00)
        else #"maxLastUpdate"
in
    accountForNu11
```

3. 右键单击该表，然后选择 _应用刷新策略_
4. 部署模型更改
5. Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

> [!WARNING]
> 如果某个值等于该列中的最大值，则相关记录都会更新。 It does not necessarily update explicitly  because the value has changed, or if the value equals the refresh date.

<br></br>

---

<br></br>

### 使用 `EffectiveDate` 应用刷新策略

如果你想在生成分区时覆盖当前日期（用于生成不同的滚动窗口范围），可以在 Tabular Editor 中使用一个小脚本，通过 [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) 参数来应用刷新策略。

选中增量刷新表后，在 Tabular Editor 的 _“New C# Script”_ 窗格中运行以下脚本，而不是通过右键单击表来应用刷新策略。

```csharp
// Todo: replace with your effective date
var effectiveDate = new DateTime(2020, 1, 1);  
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

<br></br>

<img src="~/content/assets/images/effective-date-te3.png" class="noscale" alt="Effective Date" style="width:700px !important"/>

<br></br>

---

<br></br>

### 禁用增量刷新

**Purpose:** To disable a refresh policy because it is not needed or the use-case no longer fits.

**属性：** _EnableRefreshPolicy_

**注意：** 要禁用增量刷新，按以下步骤操作：

1. **Copy the _Source Expression_:** With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown. 将 _源表达式_ 复制到单独的文本编辑器窗口中。
2. **禁用刷新策略：** 将 _EnableRefreshPolicy_ 更改为 `False`
3. **移除所有 Policy Range 分区：** 选择并删除所有 Policy Range 分区
4. **创建新的 M 分区：** 右键单击表，然后选择 _创建 > 新建分区_。 Set the partition _kind_ property to `M`.
5. **粘贴 _源表达式_：** 选中新分区后，将 **步骤 6** 中的 _源表达式_ 复制到 _表达式编辑器_，并将其作为 _M 表达式_ 粘贴。
6. **应用更改：** 部署模型的更改。
7. **Refresh the Table:** Select and right-click the table. Select _Refresh > Full refresh (table)_. You can right-click the table and select _'Preview data'_ to see the result.
