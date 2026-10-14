---
uid: incremental-refresh-policy
title: 增量刷新
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          partial: true
          note: "仅限 SQL Server Standard Edition"
        - edition: Enterprise
          full: true
---

# 增量刷新

Datasets hosted in the Power BI service can have [Incremental Refresh](https://docs.microsoft.com/power-bi/connect-data/incremental-refresh-overview) set up on one or more tables. To configure or modify Incremental Refresh on a Power BI dataset, you can either use the [XMLA endpoint of the Power BI service directly](https://docs.microsoft.com/power-bi/connect-data/incremental-refresh-xmla), or you can use Tabular Editor connected to the XMLA endpoint, as described below:

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。 For Analysis Services custom [partitioning](https://learn.microsoft.com/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

## 使用 Tabular Editor 从零开始设置增量刷新

1. 连接到你的 Workspace 的 Power BI XMLA R/W 终结点，然后打开你要配置增量刷新的 Dataset。
2. Incremental refresh requires the `RangeStart` and `RangeEnd` parameters to be created ([more information](https://docs.microsoft.com/power-bi/connect-data/incremental-refresh-configure#create-parameters)), so let's start by adding two new Shared Expressions in Tabular Editor:
   ![Add shared expressions](~/content/assets/images/incremental-refresh2-01.png)
3. 分别将它们命名为 `RangeStart` 和 `RangeEnd`，将它们的 `Kind` 属性设置为 "M"，并将表达式设置为以下内容（你填写的实际日期/时间无关紧要，因为在开始数据刷新时会由 Power BI 服务设置）：

```M
#datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```

![设置 Kind 属性](~/content/assets/images/incremental-refresh2-02.png)
4。接下来，选择要启用增量刷新的表
5。将表的 `EnableRefreshPolicy` 属性设置为 "true"：
![启用刷新策略](~/content/assets/images/incremental-refresh2-03.png)
6。根据你需要的增量刷新策略，配置其余属性。记得为 `SourceExpression` 属性指定一个 M 表达式（该表达式会添加到由增量刷新的刷新策略创建的分区中，并应使用 `RangeStart` 和 `RangeEnd` 参数在源中筛选数据）。 “=”运算符只能应用于 RangeStart 或 RangeEnd 其中一个，不能同时用于两者，否则可能会产生重复数据。
![配置属性](~/content/assets/images/incremental-refresh2-04.png)
7。保存模型（Ctrl+S）。
8. 右键单击该表，然后选择“应用刷新策略”。
![应用刷新策略](~/content/assets/images/incremental-refresh2-05.png)

就这样！这时你会看到 Power BI 服务已经根据你指定的策略，自动为这张表生成了分区。

![已生成的分区](~/content/assets/images/incremental-refresh2-06.png)

下一步是刷新这些分区中的数据。 You can use the Power BI service for that, or you can refresh the partitions in batches using [XMLA/TMSL through SQL Server Management Studio](https://docs.microsoft.com/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms), or even using [Tabular Editor's scripting](https://www.elegantbi.com/post/datarefreshintabulareditor).

### 应用增量刷新策略后的完全刷新

If you have applied a refresh policy to your table and wish to perform a full refresh, you must ensure that you set [applyRefreshPolicy to false](https://learn.microsoft.com/power-bi/connect-data/incremental-refresh-xmla#override-incremental-refresh-behavior) in your script. 这样可以确保对表中的所有分区执行完全刷新。在我们的示例中，TMSL 命令如下所示：

```
{
"refresh": {
  "type": "full",
  "applyRefreshPolicy": false
  "objects": [
    {
      "database": "AdventureWorks",
      "table": "Internet Sales"
    }
  ]
}
}
```

## 修改现有刷新策略

你也可以使用 Tabular Editor 来修改通过 Power BI Desktop 设置的现有刷新策略。在这种情况下，只需按上面的第 6-8 步操作即可。

## 使用 `EffectiveDate` 应用刷新策略

If you want to generate partitions while overriding the current date (for purposes of generating different rolling window ranges), you can use a small script in Tabular Editor to apply the refresh policy with the [EffectiveDate](https://docs.microsoft.com/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) parameter.

选中启用增量刷新的表后，在 Tabular Editor 的“高级脚本”窗格中运行以下脚本，替代上面的步骤 8：

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![使用脚本应用刷新策略](~/content/assets/images/incremental-refresh2-07.png)

## 使用 Tabular Editor 移除增量刷新

你可能需要从表中移除增量刷新的刷新策略。

1. 在 TOM 视图中选中该表，从 SourceExpression 属性中获取 M 代码，并将其另存一份。
2. 将 EnableRefreshPolicy 的值从 TRUE 改为 FALSE。
3. 右键单击该表，然后创建一个新的 M 分区。
4. 把上面步骤 1 中的 M 代码粘贴到该分区的表达式中。
5. 编辑 M 代码，删除包含 Table.SelectRows() 函数的步骤，该函数用于 RangeStart/RangeEnd 参数。
6. 删除所有历史分区。它们的 SourceType 为“Policy Range”。
7. 刷新该表 (Tabular Editor 3)，或在服务中刷新 Dataset，以重新填充该表。
8. 可选：如果模型里没有其他表设置了增量刷新的刷新策略，可以删除 RangeStart/RangeEnd 共享表达式。
