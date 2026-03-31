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

托管在 Power BI 服务中的 Dataset 可以为一个或多个数据表配置[增量刷新](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview)。 **增量刷新的目的，是通过仅检索最近/发生变化的数据来实现更快、更高效的刷新，以“增量”的方式刷新表。** 为此，表会被自动划分为多个分区：只有最近或发生变化的数据会被 <span style="color:#01a99d">刷新（“热”分区）</span>，甚至还可以 <span style="color:#8d7bae">实时检索（[“混合表格”中的“Direct Query”分区](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)）</span>；而 <span style="color:#939799">较旧、静态的数据会被归档（“冷”分区）。</span>

_可在 Tabular Editor 中轻松配置并修改增量刷新。_

> [!NOTE]
> 配置增量刷新可为 Data model 带来以下好处：
>
> - 减少刷新时间和资源消耗
> - 计划刷新耗时更短、更可靠

> [!IMPORTANT]
> 在 Tabular Editor 3 中配置增量刷新仅适用于托管在 Power BI Dataset 服务中的 Dataset。 对于 Analysis Services，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

---

### 它是如何工作的？

为创建这些分区，Power BI 会在 Power Query 中使用 `RangeStart` 和 `RangeEnd` 这两个 _datetime_ 参数。 这些参数会用于表分区的 M 表达式中的筛选步骤，对表中的日期时间列进行筛选。 即使是日期、字符串或整数类型的列，也可以通过使用函数将 `RangeStart`、`RangeEnd` 或日期列转换为合适的数据类型，在保持查询折叠的同时进行筛选。 有关更多信息，请参见[这里](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

下面给出一个示例。 已针对表 _'Orders'_ 的 _[Order Date]_ 列应用增量刷新：

# [仅筛选步骤](#tab/filterstep)

```M
// 增量刷新筛选步骤最好能够折叠回数据源
// 在此之前的任何步骤都不应破坏查询折叠
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
    // 数据源最好支持查询折叠
    Source = Sql.Database(#"ServerParameter", #"DatabaseParameter"),

    Navigation = 
        Source{ 
            [ Schema="DW_fact", Item="Internet Sales" ] 
        } [Data],

    // 增量刷新筛选步骤最好能够折叠回数据源
    // 在此之前的任何步骤都不应破坏查询折叠
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
// RangeStart 参数的初始值是什么并不重要
// 该参数的数据类型必须为 "datetime"
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
// RangeEnd 参数的初始值是什么并不重要
// 该参数的数据类型必须为 "datetime"
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
> 增量刷新专为支持 [Power Query 查询折叠](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=Incremental%20refresh%20is%20designed%20for%20data%20sources%20that%20support%20query%20folding) 的数据源而设计。 理想情况下，在应用筛选步骤之前不应破坏 [查询折叠](https://learn.microsoft.com/en-us/power-query/step-folding-indicators)。
> 最终查询并不要求必须折叠，除非在实现使用 DirectQuery 的 [混合表格](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#:~:text=However%2C%20if%20the%20incremental%20refresh%20policy%20includes%20getting%20real%2Dtime%20data%20with%20DirectQuery%2C%20non%2Dfolding%20transformations%20can%27t%20be%20used.) 时。

---

### 什么是刷新策略？

_刷新策略_ 决定数据如何分区，以及这些策略范围分区中哪些会在刷新时更新。 它由一组可设置或更改的表 TOM 属性组成。

> [!WARNING]
> **Power BI Desktop 限制：** 不支持在连接到本地 Power BI Desktop 模型时配置增量刷新。 要为本地 Power BI Desktop 模型配置增量刷新，请使用 Power BI Desktop 用户界面。

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

在 Power BI Desktop 中，这些属性的名称有所不同。 下面概述了这些属性与 Power BI Desktop 用户界面的对应关系。

![增量刷新刷新策略窗口属性](~/content/assets/images/tutorials/incremental-refresh-window-properties.png)

---

#### 高级属性

增量刷新的具体行为会因所配置的属性而异。 下面概述了不同的增量刷新配置：

# [标准（导入）](#tab/import)

在增量刷新的标准配置中，所有分区都会导入到内存中。 <span style="color:#BC4A47">滚动窗口</span>中的分区会被归档，而<span style="color:#455C86">增量窗口</span>中的分区会被刷新。

# [混合](#tab/hybrid)

在增量刷新的 <span style="color:#01a99d">**_[hybrid](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)_**</span> 配置中，会通过 DirectQuery 对 Dataset 的 <span style="color:#455C86">增量窗口</span>内策略范围中最新的分区进行实时查询。

这通过将 <em>Mode</em> 属性设置为 <code>Hybrid</code> 来配置。

![增量刷新刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-mode-pbi-match.png)

# [仅刷新完整周期](#tab/completeperiods)

在此配置中，策略范围不会包含<span style="color:#BC4A47">滚动窗口</span>中的当前周期。

在增量刷新的标准配置中，当前周期始终位于<span style="color:#455C86">增量窗口</span>中。 这可能并非你期望的行为，因为数据会在每次刷新时发生变化。 如果用户不希望在一天未结束时看到不完整的数据，你可以配置“仅刷新完整周期”。

这通过 <em>IncrementalPeriodsOffset</em> 属性来配置。 在上面的示例中，针对 <code>-1</code> 这个值，当 <em>IncrementalGranularity</em> 为 <code>Day</code> 时，会将当前日期从 <span style="color:#455C86">增量窗口</span> 中排除，从而也排除在数据范围之外；只会刷新完整的天数。

![增量刷新刷新策略窗口](~/content/assets/images/tutorials/incremental-refresh-period-offset-pbi-match.png)

# [检测数据更改](#tab/datachanges)

在此配置中，并不会刷新<span style="color:#455C86">增量窗口</span>中的所有记录。 相反，仅在记录发生更改时才会刷新。 在使用增量刷新时，“检测数据更改”可以进一步优化刷新性能。 若要识别数据更改，可以使用 _Polling Expression_。 Polling Expression 是一个单独的属性，需要有效的 M Expression，用来从日期列表中找出最大日期。

通常，你会在表的 DateTime 列上使用 Polling Expression，来找出最新日期。 如果有记录与该日期匹配，则会刷新这些记录。 一个常见示例是使用类似 [LastUpdateDt] 的列，用当前 DateTime 值标记已更新或新增的记录。 所有值等于最新 [LastUpdateDt] 的记录都会被刷新。

> [!NOTE]
> 已归档分区中的记录 _不会_ 被刷新。

下面是一个有效的 `Polling Expression` 属性示例。 在 Tabular Editor 中为模型配置 _检测数据更改_ 时，你可以将其用作模板：

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

<a name="overview-of-all-properties"></a>

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
                <td class="formatting"><code>True</code> 或 <code>False</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">增量刷新周期</td>
                <td class="formatting">增量窗口的粒度。<br /><br>示例：<br /><em>"在刷新日期之前的最近 30 <strong><em>天</em></strong>内刷新数据。"</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> or <code>Year</code>。 必须小于或等于 IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">增量刷新周期数</td>
                <td class="formatting">增量窗口包含的周期数量。<br /><br>示例：<br /><em>"在刷新日期之前的最近 <strong><em>30</em></strong> 天内刷新数据。"</em></td>
                <td class="formatting">一个整数，表示 <em>IncrementalGranularity</em> 周期的数量。 必须定义一个总周期，且小于 <em>RollingWindowPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">仅刷新完整的天</td>
                <td class="formatting">应用于 <em>IncrementalPeriods</em> 的偏移量。<br /><br>示例如下：<br /><em>IncrementalPeriodsOffset</em> = <code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"只刷新从刷新日期前一天开始往前数最近 30 天的数据。</em></td>
                <td class="formatting">一个整数，表示将增量窗口按 <em>IncrementalGranularity</em> 的周期数进行平移。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="refreshpolicymode"><b><em>模式</b></em></span></td>
                <td class="formatting">使用 DirectQuery 实时获取最新数据</td>
                <td class="formatting">指定增量刷新是仅配置为导入分区，还是同时包含一个 DirectQuery 分区，以生成 <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables">“混合表格”</a>。</td>
                <td class="formatting"><code>Import</code> 或 <code>Hybrid</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><b><em>PolicyType</b></em></td>
                <td class="formatting">不适用</td>
                <td class="formatting">指定刷新策略的类型。</td>
                <td class="formatting">只能包含一个值：<code>Basic</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(可选)</em></span></td>
                <td class="formatting">检测数据更改</td>
                <td class="formatting">用于检测特定列（例如 <em>LastUpdateDate</em>）变更的 M 表达式<br /><br>在 Tabular Editor 中，<strong>从左上角的下拉菜单中选择该项后，即可在 <em>表达式编辑器</em> 窗口中查看并修改 <em>PollingExpression</em></strong>。</td>。
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
                <td class="formatting">是否为这个表启用刷新策略。<br /><br>在 Tabular Editor 中，只有把这个值设置为 <code>True</code>，其他刷新策略属性才会显示。</td>
                <td class="formatting"><code>True</code> 或 <code>False</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalgranularity"><em><b>IncrementalGranularity</b></em></span></td>
                <td class="formatting">增量刷新周期</td>
                <td class="formatting">增量窗口的粒度。<br /><br>示例：<br /><em>“在刷新日期之前，刷新最近 30 <strong><em>天</em></strong>的数据。”</em></td>
                <td class="formatting"><code>Day</code>、<code>Month</code>、<code>Quarter</code> 或 <code>Year</code>。 必须小于或等于 IncrementalGranularity 的值。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementalperiods"><em><b>IncrementalPeriods</b></em></span></td>
                <td class="formatting">增量刷新周期数</td>
                <td class="formatting">增量窗口包含的周期数。<br /><br>示例：<br /><em>“在刷新日期之前，刷新最近 <strong><em>30</em></strong> 天的数据。”</em></td>
                <td class="formatting">一个整数，表示 <em>IncrementalGranularity</em> 周期的数量。 必须定义一个小于 <em>RollingWindowPeriods</em> 的总周期</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#455C86" id="incrementaloffset"><b><em>IncrementalPeriodsOffset</b></em></span></td>
                <td class="formatting">仅刷新完整的天</td>
                <td class="formatting">要应用于 <em>IncrementalPeriods</em> 的偏移量。<br /><br>示例：<br /><em>IncrementalPeriodsOffset</em>=<code>-1</code>; <br /><em>IncrementalPeriods</em> = <code>30</code>;<br /><em>IncrementalGranularity</em> = <code>Day</code>: <br /><em>"仅刷新最近 30 天的数据，从刷新日期的前一天开始。"</em></td>
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
                <td class="formatting">不适用</td>
                <td class="formatting">指定刷新策略的类型。</td>
                <td class="formatting">只能包含一个值：<code>Basic</code>。</td>
            </tr>
            <tr>
                <td class="formatting"><span id="pollingexpression"><b><em>PollingExpression</b><br />(Optional)</em></span></td>
                <td class="formatting">检测数据更改</td>
                <td class="formatting">用于检测特定列的数据变化的 M 表达式，例如 <em>LastUpdateDate</em><br /><br>在 Tabular Editor 中，<strong>在左上角的下拉菜单中选择后，可在 <em>Expression Editor</em> 表达式编辑器窗口中查看并修改 <em>Polling Expression</em></strong>。</td><td class="formatting">一个有效的 M 表达式，返回某列中最新日期的标量值。 增量窗口内的热分区中，该列包含该值的所有记录都会被刷新。<br><br>归档分区中的记录<i>不会</i>被刷新。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollinggranularity"><b><em>RollingWindowGranularity</b></em></span></td>
                <td class="formatting">数据归档周期</td>
                <td class="formatting">滚动窗口的粒度。<br /><br>示例：<br /><em>"从刷新日期往前 3 <strong><em>年</em></strong>开始归档数据。"</em></td>
                <td class="formatting"><code>Day</code>、<code>Month</code>、<code>Quarter</code> 或 <code>Year</code>。 必须大于或等于 IncrementalGranularity。</td>
            </tr>
            <tr>
                <td class="formatting"><span style="color:#BC4A47" id="rollingperiods"><b><em>RollingWindowPeriods</b></em></span></td>
                <td class="formatting">归档数据周期数</td>
                <td class="formatting">滚动窗口的周期数。<br /><br>示例：<br /><em>“从刷新日期往前 <strong><em>3</em></strong> 年开始归档数据。”</em></td>
                <td class="formatting">一个整数，表示 <em>RollingWindowGranularity</em> 周期的数量。 必须定义一个总周期，其长度大于   <em>IncrementalPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><b><em>SourceExpression</b></td>
                <td class="formatting">Power Query 源表达式</td>
                <td class="formatting">表数据源的 M 表达式。 这里存放原始表的 M 表达式；任何现有的 Power Query 转换也需要在这里进行修改。<br /><br>在 Tabular Editor 中，<strong>从左上角的下拉菜单选择 <em>Source Expression</em> 后，即可在 <em>表达式编辑器</em> 中查看并修改</strong>。</td>
                <td class="formatting">一个有效的 M 表达式，其中包含筛选步骤，并且正确使用 <code>RangeStart</code> 和 <code>RangeEnd</code>。</td>
            </tr>
        </tbody>
    </table>
</div>