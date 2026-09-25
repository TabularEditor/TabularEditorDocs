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

要设置增量刷新，你必须为该表配置一项新的刷新策略。 This is easily done by configuring the Refresh Policy properties once _EnableRefreshPolicy_ is set to `True`:

> [!IMPORTANT]
> 使用 Tabular Editor 3 设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。
> For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

### 配置新的刷新策略

1. **连接到模型：** 连接到 Workspace 的 Power BI XMLA endpoint，并打开要配置增量刷新的 Dataset。
2. **创建 `RangeStart` 和 `RangeEnd` 参数：** 增量刷新要求先创建 `RangeStart` 和 `RangeEnd` 参数（[了解详情](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)）。 Add two new Shared Expressions in Tabular Editor:

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

4. **Copy Partition M Code**: Navigate to the table for which you want to configure incremental refresh. Fold it out and select your partition containing your Power Query M Expression. Copy your code to Notepad, you will need it in step 6.

5. **启用表刷新策略：** 在 _“Properties”_ 窗口中，将该表的 `EnableRefreshPolicy` 属性设置为 `True`：

<img src="~/content/assets/images/tutorials/incremental-refresh-enable-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

6. **Configure the Table Refresh:** Next, select the table for which you want to configure incremental refresh. In the **Expression Editor** window, Select **'Source Expression'** from the dropdown, insert your Power Query M Expression from step 4 and alter the Power Query M Expression such that there is a filter step on the date column for which you will enable incremental refresh.

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

Columns that are of date, string or integer types can still be filtered while maintaining query folding using functions that convert `RangeStart` or `RangeEnd` to the appropriate data type. For more information about this, see [here](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview#supported-data-sources)

7. **Configure Refresh Policy:** Configure the remaining properties according to the incremental refresh policy you need. 记得为 `SourceExpression` 属性指定一个 M 表达式（该表达式会添加到由增量刷新的刷新策略创建的分区中，并应使用 `RangeStart` 和 `RangeEnd` 参数在源中筛选数据）。 The = operator should only be applied to either RangeStart or RangeEnd, but not both, as data may be duplicated.

   - **Source Expression:** 将添加到由刷新策略创建的分区的 M 表达式。
   - **IncrementalWindowGranularity:** 增量（刷新）窗口的粒度。
   - **IncrementalWindowPeriods:** 需要刷新的周期数（按上面指定的粒度）。
   - **IncrementalWindowPeriodsOffset:** 设置为 `-1` 以启用 _“Only Refresh Complete Periods”_ 选项
   - **RollingWindowGranularity:** 滚动（归档）窗口的粒度。
   - **RollingWindowPeriods:** 需要归档的周期数（按上面指定的粒度）。
   - **Mode:** 是标准 `Import` 刷新策略还是 `Hybrid`，其中最后一个分区为 DirectQuery。
   - **PollingExpression:** A valid M Expression configured to detect data changes. 有关 _Polling Expression_ 或其他刷新策略属性的更多信息，请参阅[此处](xref:incremental-refresh-about#overview-of-all-properties)。

8. **Apply Model Changes:** 保存模型（Ctrl+S）。

9. **应用刷新策略：** 右键单击该表，然后选择“应用刷新策略”。

<img src="~/content/assets/images/tutorials/incremental-refresh-apply-refresh-policy.png" class="noscale" alt="Apply Refresh Policy" style="width:400px !important"/>

**就这样！** 此时你应该会看到，Power BI 服务已根据你指定的策略，自动为表生成了分区。 All that's left is to refresh all the partitions.

<img src="~/content/assets/images/generated-partitions-te3.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

10. **Refresh all partitions:** Shift-click to select all partitions. Right-click and select _Refresh > Full refresh (partition)_. You can right-click the table and select _'Preview data'_ to see the result.

<img src="~/content/assets/images/tutorials/incremental-refresh-refresh-all-partitions.png" class="noscale" alt="Refresh All Partitions" style="width:400px !important"/>

Finally, you can configure the scheduled refresh in Power BI Service. Power BI will automatically handle the partitioning of your table. You can always connect to the remote model to view and validate the partitions, i.e. using the VertiPaq Analyzer.

-------------

### 使用整数日期键的增量刷新

如果你的日期列是整数数据类型，请用下面的内容替换上面步骤 4 中的筛选步骤：

1. **创建自定义函数：** 创建一个名为 `ConvertDatetimeToInt` 的共享表达式：

```M
   // A custom M function which will return a DateTime value as a YYYYMMDD integer
   (DateValue as datetime) => 
        Date.Year(DateValue) * 10000 + Date.Month(DateValue) * 100 + Date.Day(DateValue)
```

2. **创建筛选步骤：** 使用该自定义函数在筛选表达式中将 `RangeStart` 和 `RangeEnd` 转换为整数。 The filter step is otherwise identical to if the Date column would be a DateTime column:

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

3. **按正常流程继续后续步骤：** 然后你就可以用 _'Apply refresh policy'_ 配置并应用刷新策略，最后刷新所有分区。 Preview the data of the table after the refresh operations complete to see the result.

-------------

### 使用字符串日期键的增量刷新

If your date column is of String data type, you should configure your filter step to parse the Date column without breaking query folding. This will vary depending on your source and how the date is formatted. Below is a hypothetical example for an Order Date formatted 'YYYY-MM-DD':

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

另请参阅 Power Query 中 `Date.FromText` 函数的文档：[此处](https://learn.microsoft.com/en-us/powerquery-m/date-fromtext)。 Should it not be possible to convert the Date column in-line while preserving query folding, it is also possible to configure incremental refresh with a native query, as described in the section, below.

-------------

### 使用本机查询的增量刷新

If you have configured a native query, it may still be possible to configure and use incremental refresh, depending on your data source. To try this for yourself, you need to follow the following steps in the place of Step 4, above:

1. **Author and Save the Native Query:** Write your native query in SQL Server Management Studio or Azure Data Studio. Include a placeholder `WHERE` clause which filters >= a DateTime parameter, and < another DateTime parameter.

   <img src="~/content/assets/images/tutorials/incremental-refresh-native-query-sql.png" class="noscale" alt="刷新所有分区" style="width:650px !important"/>incremental-refresh-native-query-formatted.png

2. **Replace the Native Query String in the Source Expression:** Copy the query and replace the existing query, which will be full of characters like (lf) (line feed), (cr) (carriage return) and (n) (new line). Doing this makes the query actually readable and editable without resorting to the Native Query user interface of Power BI Desktop.

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-unformatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

例如，将 `Query` 参数中的上述文本替换为下面的内容：

<img src="~/content/assets/images/tutorials/incremental-refresh-native-query-formatted.png" class="noscale" alt="Refresh All Partitions" style="width:650px !important"/>

3. **添加 `RangeStart` 和 `RangeEnd`：** 在 `WHERE` 子句中拼接 "RangeStart" 和 "RangeEnd"，替换占位字段，并使用 `Date.From` 将参数转换为日期，再通过 `Date.ToText` 将 `Format` 选项设为 `"yyyy-MM-dd`，把它们转换为字符串数据类型。 Don't forget to include single quotes `'` on either side of the concatenation. Below is an example of what the final query would look like:

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

4. **Validate the new M Expression:** You can attempt to save the changes to the table M Expression prior to enabling the refresh policy, to see if you get the expected results when setting the `RangeStart` and `RangeEnd` to specific values. If so, you can proceed as normal; Power BI will be able to handle the partitioning as expected if you configured the steps in Power Query.

   这可能不是必需的，但根据本机查询中的转换情况，你也可以尝试按 Chris Webb 的[这篇文章](https://blog.crossjoin.co.uk/2021/02/21/query-folding-on-sql-queries-in-power-query-using-value-nativequery-and-enablefoldingtrue/)所述，添加参数 `[EnableFolding = True]`。

5. **按正常流程继续后续步骤：** 然后你就可以用 _'Apply refresh policy'_ 配置并应用刷新策略，最后刷新所有分区。 Preview the data of the table after the refresh operations complete to see the result.
