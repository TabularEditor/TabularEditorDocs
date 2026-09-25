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
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 设置增量刷新

![增量刷新设置 Visual 摘要](~/content/assets/images/tutorials/incremental-refresh-setup-refresh-policy.png)

---

要设置增量刷新，你必须为该表配置一项新的刷新策略。将 _EnableRefreshPolicy_ 设置为 `True` 后，只需配置刷新策略属性即可轻松完成：

> [!IMPORTANT]
> 使用 Tabular Editor 3 设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。对于 Analysis Services，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

### 配置新的刷新策略

1. **连接到模型：** 连接到 Workspace 的 Power BI XMLA endpoint，并打开要配置增量刷新的 Dataset。
2. **创建 `RangeStart` 和 `RangeEnd` 参数：** 增量刷新要求先创建 `RangeStart` 和 `RangeEnd` 参数（[了解详情](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)）。在 Tabular Editor 中新增两个共享表达式：

<img src="~/content/assets/images/create-shared-expression-te3.png" class="noscale" alt="应用刷新策略" style="width:400px !important"/>

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

<img src="~/content/assets/images/shared-expression-kind.png" class="noscale" alt="应用刷新策略" style="width:400px !important"/>

4. **复制分区 M 代码：** 导航到要配置增量刷新的表。展开该表，然后选择包含 Power Query M 表达式的分区。将代码复制到记事本中，第 6 步会用到。

5. **启用表刷新策略：** 在 _“Properties”_ 窗口中，将该表的 `EnableRefreshPolicy` 属性设置为 `True`：

<img src="~/content/assets/images/tutorials/incremental-refresh-enable-refresh-policy.png" class="noscale" alt="应用刷新策略" style="width:400px !important"/>

6. **配置表刷新：** 接下来，选择要配置增量刷新的表。在 **表达式编辑器** 窗口中，从下拉列表中选择 **'源表达式'**，插入第 4 步中的 Power Query M 表达式，并修改该 Power Query M 表达式，使其包含针对你要启用增量刷新的日期列的筛选步骤。

   _下面是一个可用的筛选步骤示例：_

```M
// The filter step must be able to fold back to the data source
// No steps before this should break query folding
#"Incremental Refresh Filter Step" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] >= #"RangeStart" and 
            [OrderDate] < #"RangeEnd"
    )
```

日期、字符串或整数类型的列仍可进行筛选，同时通过使用将 `RangeStart` 或 `RangeEnd` 转换为相应数据类型的函数来保持查询折叠。有关详细信息，请参阅 [此处](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

7. **配置刷新策略：** 根据所需的增量刷新策略配置其余属性。记得为 `SourceExpression` 属性指定一个 M 表达式（该表达式会添加到由增量刷新的刷新策略创建的分区中，并应使用 `RangeStart` 和 `RangeEnd` 参数在源中筛选数据）。 `=` 运算符只能用于 RangeStart 或 RangeEnd 其中之一，不能同时用于两者，否则可能会导致数据重复。

   - **Source Expression:** 将添加到由刷新策略创建的分区的 M 表达式。
   - **IncrementalWindowGranularity:** 增量（刷新）窗口的粒度。
   - **IncrementalWindowPeriods:** 需要刷新的周期数（按上面指定的粒度）。
   - **IncrementalWindowPeriodsOffset:** 设置为 `-1` 以启用 _“Only Refresh Complete Periods”_ 选项
   - **RollingWindowGranularity:** 滚动（归档）窗口的粒度。
   - **RollingWindowPeriods:** 需要归档的周期数（按上面指定的粒度）。
   - **Mode:** 是标准 `Import` 刷新策略还是 `Hybrid`，其中最后一个分区为 DirectQuery。
   - **PollingExpression:** 用于检测数据更改的有效 M 表达式。有关 _Polling Expression_ 或其他刷新策略属性的更多信息，请参阅[此处](xref:incremental-refresh-about#overview-of-all-properties)。

8. **Apply Model Changes:** 保存模型（Ctrl+S）。

9. **应用刷新策略：** 右键单击该表，然后选择“应用刷新策略”。

<img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="应用刷新策略" style="width:400px !important"/>

**就这样！** 此时你应该会看到，Power BI 服务已根据你指定的策略，自动为表生成了分区。剩下要做的就是刷新所有分区。

<img src="~/content/assets/images/generated-partitions-te3.png" class="noscale" alt="刷新所有分区" style="width:400px !important"/>

10. **刷新所有分区：** 按住 Shift 键并单击，选中所有分区。右键单击，然后选择 _刷新 > 完全刷新（分区）_。你可以在表上右键单击，然后选择 _“预览数据”_ 查看结果。

<img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="刷新所有分区" style="width:400px !important"/>

最后，你可以在 Power BI 服务中配置计划刷新。 Power BI 会自动处理表的分区。你可以随时连接到远程模型来查看并验证分区，例如使用 VertiPaq分析器。

-------------

### 使用整数日期键的增量刷新

如果你的日期列是整数数据类型，请用下面的内容替换上面步骤 4 中的筛选步骤：

1. **创建自定义函数：** 创建一个名为 `ConvertDatetimeToInt` 的共享表达式：

```M
   // A custom M function which will return a DateTime value as a YYYYMMDD integer
   (DateValue as datetime) => 
        Date.Year(DateValue) * 10000 + Date.Month(DateValue) * 100 + Date.Day(DateValue)
```

2. **创建筛选步骤：** 使用该自定义函数在筛选表达式中将 `RangeStart` 和 `RangeEnd` 转换为整数。除此之外，筛选步骤与 Date 列为 DateTime 列时完全相同：

```M
let
   // Connect to your data source
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

// Load the table data
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // Make any transformations that should fold back to the data source
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // Add incremental refresh filter step
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

3. **按正常流程继续后续步骤：** 然后你就可以用 _'Apply refresh policy'_ 配置并应用刷新策略，最后刷新所有分区。刷新操作完成后，预览表中的数据以查看结果。

-------------

### 使用字符串日期键的增量刷新

如果日期列的数据类型为 String，你应配置筛选步骤，以便在不破坏查询折叠的情况下解析 Date 列。这取决于你的数据源以及日期格式。下面是一个假设示例，其中 Order Date 的格式为“YYYY-MM-DD”：

```M
let
   // Connect to your data source
   Source = 
      Sql.Database(#"SqlEndpoint", #"Database"),

   // Load the table data
   Data = 
      Source{ [Schema="Factview", Item="Orders"] }[Data],

   // Make any transformations that should fold back to the    data source
   #"Remove Unnecessary Columns" = 
      Table.RemoveColumns ( 
         Data, 
         {
            "DWCreatedDate", 
            "Net Invoice Cost"
         } 
      ),

   // Add incremental refresh filter step
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

另请参阅 Power Query 中 `Date.FromText` 函数的文档：[此处](https://learn.microsoft.com/en-us/powerquery-m/date-fromtext)。如果无法在保留查询折叠的同时以内联方式转换 Date 列，也可以使用本机查询来配置增量刷新，如下节所述。

-------------

### 使用本机查询的增量刷新

如果你已配置本机查询，则仍有可能配置并使用增量刷新，具体取决于你的数据源。若要亲自尝试，请用以下步骤替代上文的步骤 4：

1. **编写并保存本机查询：** 在 SQL Server Management Studio 或 Azure Data Studio 中编写本机查询。包含一个占位符 `WHERE` 子句，用于筛选 >= 某个 DateTime 参数且 < 另一个 DateTime 参数的数据。

   <img src="~/content/assets/images/tutorials/incremental-refresh-native-query-sql.png" class="noscale" alt="刷新所有分区" style="width:650px !important"/>incremental-refresh-native-query-formatted.png

2. **替换源表达式中的本机查询字符串：** 复制该查询并替换现有查询；现有查询中会充满 (lf)（换行）、(cr)（回车）和 (n)（新行）之类的字符。这样一来，查询就会变得真正可读、可编辑，而无需借助 Power BI Desktop 的“本机查询”界面。

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-unformatted.png" class="noscale" alt="刷新所有分区" style="width:650px !important"/>

例如，将 `Query` 参数中的上述文本替换为下面的内容：

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-formatted.png" class="noscale" alt="刷新所有分区" style="width:650px !important"/>

3. **添加 `RangeStart` 和 `RangeEnd`：** 在 `WHERE` 子句中拼接 "RangeStart" 和 "RangeEnd"，替换占位字段，并使用 `Date.From` 将参数转换为日期，再通过 `Date.ToText` 将 `Format` 选项设为 `"yyyy-MM-dd`，把它们转换为字符串数据类型。不要忘记在拼接内容的两侧加上单引号 `'`。下面是最终查询的示例：

```M
// Example of a full native query that folds and works with Incremental Refresh
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

4. **验证新的 M 表达式：** 你可以在启用刷新策略之前先尝试保存对表的 M 表达式所做的更改，看看当 `RangeStart` 和 `RangeEnd` 设置为特定值时，是否能得到预期结果。如果可以，你就可以按正常流程继续；如果你已在 Power Query 中配置好这些步骤，Power BI 就能按预期处理分区。

   这可能不是必需的，但根据本机查询中的转换情况，你也可以尝试按 Chris Webb 的[这篇文章](https://blog.crossjoin.co.uk/2021/02/21/query-folding-on-sql-queries-in-power-query-using-value-nativequery-and-enablefoldingtrue/)所述，添加参数 `[EnableFolding = True]`。

5. **按正常流程继续后续步骤：** 然后你就可以用 _'Apply refresh policy'_ 配置并应用刷新策略，最后刷新所有分区。刷新操作完成后，预览表中的数据以查看结果。
