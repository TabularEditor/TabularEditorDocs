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
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 修改增量刷新

![增量刷新 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-modify-a-refresh-policy.png)

---

**通过调整刷新策略属性来更改增量刷新。** 具体要更改哪一项，就调整相应的属性。 这些属性的完整概览见[此处](xref:incremental-refresh-about#overview-of-all-properties)。

> [!IMPORTANT]
> 在 Tabular Editor 3 中配置增量刷新仅限于托管在 Power BI Datasets 服务中的 Dataset。 对于 Analysis Services，必须进行自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

---

## 更改增量刷新

下面是修改现有刷新策略的一般步骤：

1. **连接：** 连接到模型。

2. **选择表：** 选择已配置增量刷新的表。

3. **找到“刷新策略”属性：** 在 _Properties_ 窗口中，进入 _刷新策略_ 部分。

    <img src="~/content/assets/images/tutorials/Incremental-refresh-properties.png" class="noscale" alt="Properties of Incremental Refresh" style="width:704px !important"/>

4. **更改属性：** 根据要更改的内容，在下方各节中修改指定的 **Property**。 有关所有刷新策略属性及其作用的概览，请参阅[此处](xref:incremental-refresh-about#overview-of-all-properties)。

5. **应用更改：** 部署模型更改。

6. **应用刷新策略：** 右键单击该表，然后选择 _应用刷新策略_。

    <img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:450px !important"/>

7. **刷新所有分区：** 按住 Shift 键并单击，以选中所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表并选择 _“预览数据”_ 来查看结果。

    <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:450px !important"/>

---

以下是对现有“刷新策略”可能进行的常见更改概览：

### 扩展或缩小已归档数据的窗口

**目的：** 增加或减少模型中的数据量。

**属性：** <span style="color:#BC4A47">_RollingWindowPeriods_</span>。 增大该值可扩展窗口（更多数据）；减小该值可缩小窗口（更少数据）。

**注意：** 你也可以更改 <span style="color:#BC4A47">_RollingWindowGranularity_</span> 来进行更细粒度的选择，例如从 3 年改为 36 个月。

<br></br>

---

<br></br>

### 扩展或缩小已刷新数据的窗口

**目的：** 在计划刷新操作中，增加或减少要刷新的数据量。

**属性：** <span style="color:#455C86">_IncrementalWindowPeriods_</span>。 增大该值可扩展窗口（更多数据）；减小该值可缩小窗口（更少数据）。

**注意：** 你也可以更改 <span style="color:#455C86">_IncrementalWindowGranularity_</span> 来进行更细粒度的选择，例如从 3 年改为 36 个月。

<br></br>

---

<br></br>

### 仅刷新完整周期

**目的：** 从 <span style="color:#BC4A47">滚动窗口</span> 中排除不完整（未完成）的周期

**属性：** <span style="color:#455C86">_IncrementalWindowPeriodsOffset_</span>。 将值设为 `-1`，即可将周期偏移 1，从而排除当前周期。

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
4. 按住 Shift 键并单击以选择所有分区。 右键单击并选择 _刷新 > 完全刷新（分区）_。 也可以右键单击该表，然后选择 _“预览数据”_ 查看结果。

> [!NOTE]
> 建议检查滚动窗口是否针对所选 _Mode_ 设置得当。 从 `Import` 模式切换到 `Hybrid` 模式时，最新的策略范围分区将变为 DirectQuery 分区。 可以考虑选择更细粒度的窗口，以限制通过 DirectQuery 查询的数据量。

<br></br>

---

<br></br>

### 配置“检测数据更改”

**目的：** 设置为：当日期列（例如 _LastUpdate_）的值发生变化时，刷新已归档数据。

**属性：** _PollingExpression_。 添加一个有效的 M 表达式，用于返回某列的最大日期值。 所有包含该日期的记录都会被刷新，无论它们属于哪个分区。

**注意：** 按以下流程配置“检测数据更改”：

1. 选中该表后，在 _表达式编辑器_ 窗口中，从左上角下拉列表中选择 _Polling Expression_
2. 复制下面的 M 表达式，并将 _LastUpdate_ 替换为所需的列名。

```M
// 获取列 [LastUpdate] 的最大值
// 将 LastUpdate 替换为你自己的列名
// 对于该列中值等于该列在整个表中最大值的任何记录，
//    都将触发数据刷新
let
    #"maxLastUpdate" =
        List.Max(
            // 将下面替换为你的列名和表名
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
5. 按住 Shift 键并单击以选择所有分区。 右键单击，然后选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表并选择 _“预览数据”_ 来查看结果。

> [!WARNING]
> 如果某个值等于该列中的最大值，则相关记录都会更新。 并不一定会因为该值发生变化而更新，也不一定会因为该值等于刷新日期而更新。

<br></br>

---

<br></br>

### 使用 `EffectiveDate` 应用刷新策略

如果你想在生成分区时覆盖当前日期（用于生成不同的滚动窗口范围），可以在 Tabular Editor 中使用一个小脚本，通过 [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) 参数来应用刷新策略。

选中增量刷新表后，在 Tabular Editor 的 _“New C# Script”_ 窗格中运行以下脚本，而不是通过右键单击表来应用刷新策略。

```csharp
// Todo: 替换为你的生效日期
var effectiveDate = new DateTime(2020, 1, 1);  
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

<br></br>

<img src="~/content/assets/images/effective-date-te3.png" class="noscale" alt="Effective Date" style="width:700px !important"/>

<br></br>

---

<br></br>

### 禁用增量刷新

**目的：** 在不需要刷新策略或使用场景不再适用时，将其禁用。

**属性：** _EnableRefreshPolicy_

**注意：** 要禁用增量刷新，按以下步骤操作：

1. **复制 _源表达式_：** 选中表后，在 _表达式编辑器_ 窗口中，从左上角下拉列表选择 _源表达式_。 将 _源表达式_ 复制到单独的文本编辑器窗口中。
2. **禁用刷新策略：** 将 _EnableRefreshPolicy_ 更改为 `False`
3. **移除所有 Policy Range 分区：** 选择并删除所有 Policy Range 分区
4. **创建新的 M 分区：** 右键单击表，然后选择 _创建 > 新建分区_。 将分区的 _kind_ 属性设置为 `M`。
5. **粘贴 _源表达式_：** 选中新分区后，将 **步骤 6** 中的 _源表达式_ 复制到 _表达式编辑器_，并将其作为 _M 表达式_ 粘贴。
6. **应用更改：** 部署模型的更改。
7. **刷新表：** 选中表格并右键单击。 选择 _刷新 > 完全刷新（表）_。 你可以右键单击表格，并选择 _“预览数据”_ 来查看结果。
