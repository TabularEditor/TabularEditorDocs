---
uid: incremental-refresh-setup
title: 设置新的刷新策略
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

# 设置增量刷新

![增量刷新设置 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-setup-refresh-policy.png)

---

要设置增量刷新，你必须为该表配置一项新的刷新策略。 将 _EnableRefreshPolicy_ 设为 `True` 后，配置刷新策略属性即可：

> [!IMPORTANT]
> 使用 Tabular Editor 3 设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。
> 对于 Analysis Services，则需要自定义 [分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

### 配置新的刷新策略

1. **连接到模型：** 连接到 Workspace 的 Power BI XMLA endpoint，并打开要配置增量刷新的 Dataset。
2. **创建 `RangeStart` 和 `RangeEnd` 参数：** 增量刷新要求先创建 `RangeStart` 和 `RangeEnd` 参数（[了解详情](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)）。 在 Tabular Editor 中新增两个共享表达式：

<img src="~/content/assets/images/create-shared-expression-te3.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

3. **配置 `RangeStart` 和 `RangeEnd` 参数：** 分别将它们命名为 `RangeStart` 和 `RangeEnd`，把它们的 `Kind` 属性设置为 "M"，并将表达式设置为以下内容（你填写的实际日期/时间值无关紧要，因为在开始数据刷新时，Power BI Service 会设置它）：

```M
#datetime(2021, 6, 9, 0, 0, 0) 
   meta 
   [
      IsParameterQuery=true, 
      Type="DateTime", 
      IsParameterQueryRequired=true
   ]
```

<img src="~/content/assets/images/shared-expression-kind.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

4. **复制分区的 M 代码：** 定位到要配置增量刷新的表。 将其展开，并选择包含 Power Query M 表达式的分区。 把代码复制到记事本中，第 6 步会用到。

5. **启用表刷新策略：** 在 _“Properties”_ 窗口中，将该表的 `EnableRefreshPolicy` 属性设置为 `True`：

<img src="~/content/assets/images/tutorials/incremental-refresh-enable-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

6. **配置表的刷新：** 接下来，选择要为其配置增量刷新的表。 在 **表达式编辑器** 窗口中，从下拉列表中选择 **'Source Expression'**，插入第 4 步中的 Power Query M 表达式，并调整该 Power Query M 表达式，使其在将要启用增量刷新的日期列上包含一个筛选步骤。

   _下面是一个可用的筛选步骤示例：_

```M
// 筛选步骤必须能够折叠回数据源
// 在此之前的任何步骤都不应破坏查询折叠
#"增量刷新筛选步骤" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] >= #"RangeStart" and 
            [OrderDate] < #"RangeEnd"
    )
```

对于日期、字符串或整数类型的列，你仍然可以在保持查询折叠的同时进行筛选——只需使用函数将 `RangeStart` 或 `RangeEnd` 转换为相应的数据类型。 有关详细信息，请参阅[此处](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

7. **配置刷新策略：** 根据你所需的增量刷新策略配置其余属性。 记得为 `SourceExpression` 属性指定一个 M 表达式（该表达式会添加到由增量刷新的刷新策略创建的分区中，并应使用 `RangeStart` 和 `RangeEnd` 参数在源中筛选数据）。 = 运算符只能用于 RangeStart 或 RangeEnd 其中之一，不能同时用于两者，否则可能导致数据重复。

   - **Source Expression:** 将添加到由刷新策略创建的分区的 M 表达式。
   - **IncrementalWindowGranularity:** 增量（刷新）窗口的粒度。
   - **IncrementalWindowPeriods:** 需要刷新的周期数（按上面指定的粒度）。
   - **IncrementalWindowPeriodsOffset:** 设置为 `-1` 以启用 _“Only Refresh Complete Periods”_ 选项
   - **RollingWindowGranularity:** 滚动（归档）窗口的粒度。
   - **RollingWindowPeriods:** 需要归档的周期数（按上面指定的粒度）。
   - **Mode:** 是标准 `Import` 刷新策略还是 `Hybrid`，其中最后一个分区为 DirectQuery。
   - **PollingExpression:** 用于检测数据更改的有效 M 表达式。 有关 _Polling Expression_ 或其他刷新策略属性的更多信息，请参阅[此处](xref:incremental-refresh-about#overview-of-all-properties)。
8. **Apply Model Changes:** 保存模型（Ctrl+S）。
9. **应用刷新策略：** 右键单击该表，然后选择“应用刷新策略”。

<img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

**就这样！** 此时你应该会看到，Power BI 服务已根据你指定的策略，自动为表生成了分区。 剩下的就是刷新所有分区。

<img src="~/content/assets/images/generated-partitions-te3.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

10. **刷新所有分区：** 按住 Shift 键并单击，选中所有分区。 右键单击并选择 _刷新 > 完全刷新（分区）_。 你可以右键单击该表并选择 _“预览数据”_ 来查看结果。

   <img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

最后，你可以在 Power BI 服务中配置计划刷新。 Power BI 会自动为你的表进行分区处理。 你随时都可以连接到远程模型来查看并验证分区，例如使用 VertiPaq分析器。

-------------

### 使用整数日期键的增量刷新

如果你的日期列是整数数据类型，请用下面的内容替换上面步骤 4 中的筛选步骤：

1. **创建自定义函数：** 创建一个名为 `ConvertDatetimeToInt` 的共享表达式：

```M
   // A custom M function which will return a DateTime value as a YYYYMMDD integer
   (DateValue as datetime) => 
        Date.Year(DateValue) * 10000 + Date.Month(DateValue) * 100 + Date.Day(DateValue)
```

2. **创建筛选步骤：** 使用该自定义函数在筛选表达式中将 `RangeStart` 和 `RangeEnd` 转换为整数。 除此之外，该筛选步骤与日期列为 DateTime 类型时完全相同：

```M
let
   // 连接到你的数据源
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

// Load the table data
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // 进行应折叠回数据源的任何转换
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // 添加增量刷新筛选步骤
   //    The filter step must be able to fold back to the data source
   //    No steps before this should break query folding
   #"Incremental Refresh" = 
     Table.SelectRows(
       #"Remove Unnecessary Columns",
         each [OrderDateKey] >= ConvertDatetimeToInt(#"RangeStart")
         and  [OrderDateKey] < ConvertDatetimeToInt(#"RangeEnd")
     )
in
   #"Incremental Refresh" 
```

3. **按常规继续后续步骤：** 然后，你可以使用 _“应用刷新策略”_ 来配置并应用刷新策略，最后刷新所有分区。 刷新操作完成后，预览该表的数据以查看结果。

-------------

### 使用字符串日期键的增量刷新

如果你的日期列是字符串数据类型，你应该配置筛选步骤，在不破坏查询折叠的情况下解析日期列。 具体做法会因数据源以及日期格式而异。 下面是一个假设示例，订单日期采用“YYYY-MM-DD”格式：

```M
let
   // 连接到你的数据源
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

   // Load the table data
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // Make any transformations that should fold back to the    数据源
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // 添加增量刷新筛选步骤
   //    The filter step must be able to fold back to the   data source
   //    No steps before this should break query folding
   #"Incremental Refresh" = 
     Table.SelectRows(
       #"Remove Unnecessary Columns",
       each 

       // Converts "2022-01-09" to DateTime, for example
       DateTime.From(
         Date.FromText(
           [OrderDate], 
           [Format="yyyy-MM-dd"]
         )
       ) >= #"RangeStart"

       and 

       DateTime.From(
         Date.FromText(
           [OrderDate], 
           [Format="yyyy-MM-dd"]
         )
       ) < #"RangeEnd"      
     )
in
   #"Incremental Refresh" 
```

另请参阅 Power Query 中 `Date.FromText` 函数的文档：[此处](https://learn.microsoft.com/en-us/powerquery-m/date-fromtext)。 如果无法在保留查询折叠的同时内联转换日期列，也可以按下文所述，通过本机查询来配置增量刷新。

-------------

### 使用本机查询的增量刷新

如果你配置了本机查询，是否仍可配置并使用增量刷新取决于你的数据源。 若要自行尝试，请用以下步骤替换上面的步骤 4：

1. **编写并保存本机查询：** 在 SQL Server Management Studio 或 Azure Data Studio 中编写本机查询。 包含一个占位符 `WHERE` 子句，其中使用一个 DateTime 参数筛选 >=，并使用另一个 DateTime 参数筛选 <。

   <img src="~/content/assets/images/tutorials/incremental-refresh-native-query-sql.png" class="noscale" alt="刷新所有分区" style="width:650px !important"/>incremental-refresh-native-query-formatted.png

2. **在源表达式中替换本机查询字符串：** 复制该查询并替换现有查询；现有查询通常会充满诸如 (lf)（换行符）、(cr)（回车符）和 (n)（换行符）之类的字符。 这样可以让查询真正变得易读、可编辑，而不必借助 Power BI Desktop 的“本机查询”界面。

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-unformatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

例如，将 `Query` 参数中的上述文本替换为下面的内容：

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-formatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

3. **添加 `RangeStart` 和 `RangeEnd`：** 在 `WHERE` 子句中拼接 "RangeStart" 和 "RangeEnd"，替换占位字段，并使用 `Date.From` 将参数转换为日期，再通过 `Date.ToText` 将 `Format` 选项设为 `"yyyy-MM-dd`，把它们转换为字符串数据类型。 别忘了在拼接结果两侧加上单引号 `'`。 下面是最终查询的示例：

```M
// 支持查询折叠并可用于增量刷新的完整本机查询示例
let
    Source = Sql.Database("yoursql.database.windows.net", "YourDatabaseName", 
    [Query="

SELECT
    [OrderDateKey]
   ,[DueDateKey]
   ,SUM([OrderQuantity]) AS 'TotalOrderQuantity'
   ,SUM([SalesAmount]  ) AS 'TotalSalesAmount'
   ,[CustomerKey]
   ,[ProductKey]
FROM [DW_fact].[Internet Sales]
WHERE
   CONVERT(DATE, CONVERT(VARCHAR(8), [OrderDateKey])) 
   >= CONVERT(DATE, '" & Date.ToText(Date.From(#"RangeStart"), [Format="yyyy-MM-dd"]) & "')
   AND
   CONVERT(DATE, CONVERT(VARCHAR(8), [OrderDateKey])) 
   < CONVERT(DATE, '" & Date.ToText(Date.From(#"RangeEnd"), [Format="yyyy-MM-dd"]) & "')
GROUP BY
    [OrderDateKey]
   ,[DueDateKey]
   ,[CustomerKey]
   ,[ProductKey]

"])
in
   Source
```

4. **验证新的 M 表达式：** 在启用刷新策略之前，你可以先尝试保存对表的 M 表达式所做的更改，看看当你将 `RangeStart` 和 `RangeEnd` 设为特定值时，是否能得到预期结果。 如果是这样，你就可以按正常流程继续；只要你在 Power Query 中正确配置了这些步骤，Power BI 就能按预期处理分区。

   这可能不是必需的，但根据本机查询中的转换情况，你也可以尝试按 Chris Webb 的[这篇文章](https://blog.crossjoin.co.uk/2021/02/21/query-folding-on-sql-queries-in-power-query-using-value-nativequery-and-enablefoldingtrue/)所述，添加参数 `[EnableFolding = True]`。

5. **按正常流程继续后续步骤：** 然后你就可以用 _'Apply refresh policy'_ 配置并应用刷新策略，最后刷新所有分区。 刷新操作完成后，预览该表的数据以查看结果。
