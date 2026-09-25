---
uid: incremental-refresh-about
title: 什么是刷新策略？
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

# 什么是刷新策略？

![增量刷新 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-header.png)

---

Datasets hosted in the Power BI service can have [Incremental Refresh](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) configured for one or more data tables. **增量刷新的目的，是通过仅检索最近/发生变化的数据来实现更快、更高效的刷新，以“增量”的方式刷新表。** 为此，表会被自动划分为多个分区：只有最近或发生变化的数据会被 <span style="color:#01a99d">刷新（“热”分区）</span>，甚至还可以 <span style="color:#8d7bae">实时检索（[“混合表格”中的“Direct Query”分区](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)）</span>；而 <span style="color:#939799">较旧、静态的数据会被归档（“冷”分区）。</span>

_可在 Tabular Editor 中轻松配置并修改增量刷新。_

> [!NOTE]
> 配置增量刷新可为 Data model 带来以下好处：
>
> - 减少刷新时间和资源消耗
> - 计划刷新耗时更短、更可靠

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅限于托管在 Power BI Dataset 服务中的数据集。 For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

---

### 它是如何工作的？

为创建这些分区，Power BI 会在 Power Query 中使用 `RangeStart` 和 `RangeEnd` 这两个 _datetime_ 参数。 These parameters are used in a filter step of the table partition M Expression, filtering a table datetime column. Columns that are of date, string or integer types can still be filtered while maintaining query folding using functions that convert `RangeStart`, `RangeEnd` or the date column to the appropriate data type. For more information about this, see [here](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

An example is given below. 已针对表 _'Orders'_ 的 _[Order Date]_ 列应用增量刷新：

# [仅筛选步骤](#tab/filterstep)

```M
// The filter step should ideally be able to fold back to the data source
// No steps before this should break query folding
#"Incremental Refresh Filter Step" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] >= #"RangeStart" and 
            [OrderDate] < #"RangeEnd"
    )
```

# [完整 M 表达式](#tab/fullexp)

```M
let
    // The data source should ideally support Query Folding
    Source = Sql.Database(#"ServerParameter", #"DatabaseParameter"),

    Navigation = 
        Source{ 
            [ Schema="DW_fact", Item="Internet Sales" ] 
        } [Data],

    // The filter step should ideally be able to fold back to the data source
    // No steps before this should break query folding
    #"Incremental Refresh Filter Step" = 
        Table.SelectRows(
            Navigation,
            each 
                [OrderDate] >= #"RangeStart" and 
                [OrderDate] < #"RangeEnd"
        )
in
    #"Incremental Refresh Filter Step"
```

# [RangeStart](#tab/rangestart)

```M
// It does not matter what the initial value is for the RangeStart parameter
// The parameter must be of data type "datetime"
#datetime(2022, 12, 01, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```

# [RangeEnd](#tab/rangend)

```M
// It does not matter what the initial value is for the RangeEnd parameter
// The parameter must be of data type "datetime"
#datetime(2022, 12, 31, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```

***

> [!WARNING]
> 增量刷新专为支持 [Power Query 查询折叠](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=Incremental%20refresh%20is%20designed%20for%20data%20sources%20that%20support%20query%20folding) 的数据源而设计。 Ideally, [query folding shouldn't be broken](https://learn.microsoft.com/en-us/power-query/step-folding-indicators) before the filter step is applied.
> There's no explicit requirement for the final query to fold, except when implementing [Hybrid Tables](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=However%2C%20if%20the%20incremental%20refresh%20policy%20includes%20getting%20real%2Dtime%20data%20with%20DirectQuery%2C%20non%2Dfolding%20transformations%20can%27t%20be%20used.).

---

### 什么是刷新策略？

_刷新策略_ 决定数据如何分区，以及这些策略范围分区中哪些会在刷新时更新。 It consists of a set of table TOM properties which can be setup or changed.

> [!WARNING]
> **Power BI Desktop 限制：** 不支持在连接到本地 Power BI Desktop 模型时配置增量刷新。 To configure incremental refresh for a local Power BI Desktop model, use the Power BI Desktop user interface.

---

### 刷新策略属性

<img src="~/content/assets/images/tutorials/Incremental-refresh-properties.png" class="noscale" alt="Properties of Incremental Refresh"  style="width:704px !important"/>

一个基础的刷新策略由四类不同的属性组成：

1. <span style="color:#455C86">**增量窗口**</span> **属性**：在该时间窗口内，数据会保持 <span style="color:#455C86">_最新_</span>。
2. <span style="color:#BC4A47">**滚动窗口**</span> **属性**：在该时间窗口内，数据会被 <span style="color:#BC4A47">_归档_</span>。
3. **源表达式**：定义表架构以及该表的 Power Query 转换。
4. **模式**：是否使用 `Import` 表或 `Hybrid` 表。

![增量刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-policy-windows.png)

---

#### 与 Power BI Desktop 对比

在 Power BI Desktop 中，这些属性的名称有所不同。 Below is an overview of how the properties match the Power BI Desktop user interface.

![增量刷新刷新策略窗口属性](~/content/assets/images/tutorials/incremental-refresh-window-properties.png)

---

#### 高级属性

Depending on the configured properties, Incremental Refresh may function differently. Below is an overview of the different Incremental Refresh configurations:

# [标准（导入）](#tab/import)

在增量刷新的标准配置中，所有分区都会导入到内存中。 Partitions in the <span style="color:#BC4A47">rolling window</span> are archived, while those in the <span style="color:#455C86">incremental window</span> are refreshed.

# [混合](#tab/hybrid)

在增量刷新的 <span style="color:#01a99d">**_[hybrid](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)_**</span> 配置中，会通过 DirectQuery 对 Dataset 的 <span style="color:#455C86">增量窗口</span>内策略范围中最新的分区进行实时查询。

这通过将 <em>Mode</em> 属性设置为 <code>Hybrid</code> 来配置。

![增量刷新刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-mode-pbi-match.png)

# [仅刷新完整周期](#tab/completeperiods)

在此配置中，策略范围不会包含<span style="color:#BC4A47">滚动窗口</span>中的当前周期。

In the standard configuration of Incremental Refresh, the current period is always in the <span style="color:#455C86">incremental window</span>. This might not be the desired behavior, as the data will change with each refresh. If the users do not expect to see partial data for a partial day, you can configure 'Only Refresh Complete Periods'.

This is configured with the <em>IncrementalPeriodsOffset</em> property. 在上面的示例中，针对 <code>-1</code> 这个值，当 <em>IncrementalGranularity</em> 为 <code>Day</code> 时，会将当前日期从 <span style="color:#455C86">增量窗口</span> 中排除，从而也排除在数据范围之外；只会刷新完整的天数。

![增量刷新刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-period-offset-pbi-match.png)

# [检测数据更改](#tab/datachanges)

In this configuration, not all records are refreshed in the <span style="color:#455C86">incremental window</span>. Instead, records are only refreshed if they change. Detect data changes can further optimize refresh performance when using incremental refresh. To identify data changes you use a _Polling Expression_. A Polling Expression is a separate property that expects a valid M Expression to identify a maximum date from a list of dates.

Typically, you use the Polling Expression on a DateTime column of a table to identify the latest date. If any records match that date, they'll be refreshed. A common example is using a column like [LastUpdateDt] to label records that were updated or added with the current DateTime value. Any records that have values equal to the latest [LastUpdateDt] are refreshed.

> [!NOTE]
> 已归档分区中的记录 _不会_ 被刷新。

An example of a valid `Polling Expression` property is below. 在 Tabular Editor 中为模型配置 _检测数据更改_ 时，你可以将其用作模板：

```M
// Retrieves the maximum value of the column [LastUpdateDt]
let
    #"maxDateOfLastUpdate" =
        List.max(
            Orders[LastUpdateDt]
        ),

    accountForNu11 =
        if #"maxDateOfLastUpdate" = null
        then #datetime(1901, 01, 01, 00, 00, 00)
        else #"maxDateOfLastUpdate"
in
    accountForNu11
```

![增量刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-detect-changes-pbi-match.png)

***

#### 所有属性概览

_下面概述了 Data model 中用于配置增量刷新的 TOM 属性：_

<!-- Specific styling for the below table -->

<style>
    th.formatting {
        text-align: center; 
        vertical-align: middle!important;
        border-left: none!important; 
        border-right: none!important;
    }
    td.formatting {
        height:120px;
        vertical-align: middle!important;
        border-left: none!important;
        border-right: none!important;
    }
</style>

<!-- Refresh Policy TOM Properties table -->

<div class="table-responsive" id="RefreshPolicyPropertiesOverview">
    <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th class="formatting">属性名称</th>
                <th class="formatting">Power BI Desktop 中的对应项</th>
                <th class="formatting">说明</th>
                <th class="formatting">期望值</th>
            </tr>
        </thead>
        <tbody style="font-size:80%;">
            <tr>
                <td class="formatting"><span id="enablerefreshpolicy"><em><b>EnableRefreshPolicy</b></em></a></span></td>
                <td class="formatting">对此表进行增量刷新</td>
                <td class="formatting">是否为该表启用刷新策略。<br /><br>在 Tabular Editor 中，只有当此值设置为 <code>True</code> 时，其他刷新策略属性才会显示。</td>
                <td class="formatting"><code>True</code> or <code>False</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">Incremental Refresh Period</td>
                <td class="formatting">The granularity of the incremental window.<br /><br>示例：<br /><em>"在刷新日期之前的最近 30 <strong><em>天</em></strong>内刷新数据。"</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> or <code>Year</code>。 Must be smaller than or equal to the IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">增量刷新周期数</td>
                <td class="formatting">增量窗口包含的周期数量。<br /><br>示例：<br /><em>"在刷新日期之前的最近 <strong><em>30</em></strong> 天内刷新数据。"</em></td>
                <td class="formatting">一个整数，表示 <em>IncrementalGranularity</em> 周期的数量。 Must define a total period smaller than the <em>RollingWindowPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">Only refresh complete days</td>
                <td class="formatting">The offset to be applied to <em>IncrementalPeriods</em>.<br /><br>示例：<br /><em>IncrementalPeriodsOffset</em>=<code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"仅刷新最近 30 天的数据，从刷新日期的前一天开始。"</em></td>
                <td class="formatting">一个整数，表示将增量窗口按 <em>IncrementalGranularity</em> 的周期数进行平移。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="refreshpolicymode"><b><em>Mode</b></em></span></td>
                <td class="formatting">Get the latest data in real time with DirectQuery</td>
                <td class="formatting">Specifies whether Incremental Refresh is configured with only import partitions or also a DirectQuery partition, to result in a <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables">"Hybrid Table"</a>.</td>
                <td class="formatting"><code>Import</code> or <code>Hybrid</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><b><em>PolicyType</b></em></td>
                <td class="formatting">不适用</td>
                <td class="formatting">指定刷新策略的类型。</td>
                <td class="formatting">Can only contain a single value: <code>Basic</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(可选)</em></span></td>
                <td class="formatting">检测数据更改</td>
                <td class="formatting">用于检测特定列（例如 <em>LastUpdateDate</em>）变更的 M 表达式<br /><br>在 Tabular Editor 中，<strong>从左上角的下拉菜单中选择该项后，即可在 <em>表达式编辑器</em> 窗口中查看并修改 <em>PollingExpression</em></strong>。</td>.
                <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th class="formatting">属性名称</th>
                <th class="formatting">Power BI Desktop 对应项</th>
                <th class="formatting">说明</th>
                <th class="formatting">预期值</th>
            </tr>
        </thead>
        <tbody style="font-size:80%;">
            <tr>
                <td class="formatting"><span id="enablerefreshpolicy"><em><b>EnableRefreshPolicy</b></em></a></span></td>
                <td class="formatting">对该表进行增量刷新</td>
                <td class="formatting">Whether a refresh policy is enabled for the table.<br /><br>In Tabular Editor, other Refresh Policy properties will only be visible if this value is set to <code>True</code>.</td>
                <td class="formatting"><code>True</code> 或 <code>False</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">增量刷新周期</td>
                <td class="formatting">The granularity of the incremental window.<br /><br>示例：<br /><em>“在刷新日期之前，刷新最近 30 <strong><em>天</em></strong>的数据。”</em></td>
                <td class="formatting"><code>Day</code>、<code>Month</code>、<code>Quarter</code> 或 <code>Year</code>。 Must be smaller than or equal to the IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">增量刷新周期数</td>
                <td class="formatting">The number of periods for the incremental window.<br /><br>Example:<br /><em>"Refresh data in the last <strong><em>30</em></strong> days before refresh date."</em></td>
                <td class="formatting">An integer of the number of <em>IncrementalGranularity</em> periods. 必须定义一个小于 <em>RollingWindowPeriods</em> 的总周期</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">仅刷新完整的天</td>
                <td class="formatting">The offset to be applied to <em>IncrementalPeriods</em>.<br /><br>示例：<br /><em>IncrementalPeriodsOffset</em>=<code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"仅刷新最近 30 天的数据，从刷新日期的前一天开始。"</em></td>
                <td class="formatting">一个整数，表示将增量窗口按 <em>IncrementalGranularity</em> 周期平移的数量。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="refreshpolicymode"><b><em>Mode</b></em></span></td>
                <td class="formatting">使用 DirectQuery 实时获取最新数据</td>
                <td class="formatting">指定增量刷新是只配置导入分区，还是同时配置 DirectQuery 分区，从而形成 <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables">“混合表格”</a>。</td>
                <td class="formatting"><code>Import</code> 或 <code>Hybrid</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><b><em>PolicyType</b></td>
                <td class="formatting">N/A</td>
                <td class="formatting">指定刷新策略的类型。</td>
                <td class="formatting">只能包含一个值：<code>Basic</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(Optional)</em></span></td>
                <td class="formatting">检测数据更改</td>
                <td class="formatting">用于检测特定列的数据变化的 M 表达式，例如 <em>LastUpdateDate</em><br /><br>在 Tabular Editor 中，<strong>在左上角的下拉菜单中选择后，可在 <em>Expression Editor</em> 表达式编辑器窗口中查看并修改 <em>Polling Expression</em></strong>。</td><td class="formatting">A valid M Expression that returns a scalar value of the latest date in a column. 增量窗口内的热分区中，该列包含该值的所有记录都会被刷新。<br><br>Records in archived partitions are <i>not</i> refreshed.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollinggranularity"><b><em>RollingWindowGranularity</b></em></span></td>
                <td class="formatting">数据归档周期</td>
                <td class="formatting">The granularity of the rolling window.<br /><br>示例：<br /><em>"从刷新日期往前 3 <strong><em>年</em></strong>开始归档数据。"</em></td>
                <td class="formatting"><code>Day</code>、<code>Month</code>、<code>Quarter</code> 或 <code>Year</code>。 Must be larger than or equal to the IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollingperiods"><b><em>RollingWindowPeriods</b></em></span></td>
                <td class="formatting">归档数据周期数</td>
                <td class="formatting">The number of periods for the rolling window.<br /><br>Example:<br /><em>"Archive data starting <strong><em>3</em></strong> years before refresh date."</em></td>
                <td class="formatting">一个整数，表示 <em>RollingWindowGranularity</em> 周期的数量。必须定义一个总周期，其长度大于   <em>IncrementalPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><b><em>SourceExpression</b></td>
                <td class="formatting">Power Query 源表达式</td>
                <td class="formatting">The M Expression for the table data source. 这里存放原始表的 M 表达式；任何现有的 Power Query 转换也需要在这里进行修改。<br /><br>In Tabular Editor, <strong>the <em>Source Expression</em> can be viewed and modified from the <em>Expression Editor</em></strong> by selecting it from the dropdown menu in the top-left.</td>
                <td class="formatting">一个有效的 M 表达式，其中包含筛选步骤，并且正确使用 <code>RangeStart</code> 和 <code>RangeEnd</code>。</td>
            </tr>
        </tbody>
    </table>
</div>