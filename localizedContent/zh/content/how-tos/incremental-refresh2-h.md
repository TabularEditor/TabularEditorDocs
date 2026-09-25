---
uid: incremental-refresh-policy
title: 增量刷新
author: Daniel Otykier
updated: 2021-02-15
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

Datasets hosted in the Power BI service can have [Incremental Refresh](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) set up on one or more tables. 要在 Power BI 的 Dataset 上配置或修改增量刷新，你可以直接使用 Power BI 服务的 [XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla)；也可以按照下面的说明，使用连接到 XMLA endpoint 的 Tabular Editor 来操作：

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。 For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

## 使用 Tabular Editor 从零开始设置增量刷新

1. 连接到你的 Workspace 的 Power BI XMLA R/W 终结点，然后打开你要配置增量刷新的 Dataset。
2. Incremental refresh requires the `RangeStart` and `RangeEnd` parameters to be created ([more information](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)), so let's start by adding two new Shared Expressions in Tabular Editor:
   ![Add shared expressions](~/content/assets/images/incremental-refresh2-01.png)
3. 分别将它们命名为 `RangeStart` 和 `RangeEnd`，将它们的 `Kind` 属性设置为 "M"，并将表达式设置为以下内容（你填写的实际日期/时间无关紧要，因为在开始数据刷新时会由 Power BI 服务设置）：

```M
#datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
```

![Set kind property](~/content/assets/images/incremental-refresh2-02.png)
4. Next, select the table on which you want to enable incremental refresh
5. Set the `EnableRefreshPolicy` property on the table to "true":
![Enable Refresh Policy](~/content/assets/images/incremental-refresh2-03.png)
6. Configure the remaining properties according to the incremental refresh policy you need. 记得为 `SourceExpression` 属性指定一个 M 表达式（该表达式会添加到由增量刷新的刷新策略创建的分区中，并应使用 `RangeStart` 和 `RangeEnd` 参数在源中筛选数据）。 The = operator should only be applied to either RangeStart or RangeEnd, but not both, as data may be duplicated.
![Configure Properties](~/content/assets/images/incremental-refresh2-04.png)
7. Save your model (Ctrl+S).
8. Right-click on the table and choose "Apply Refresh Policy".
![Apply Refresh Policy](~/content/assets/images/incremental-refresh2-05.png)

That's it! 这时你会看到 Power BI 服务已经根据你指定的策略，自动为这张表生成了分区。

![Generated Partitions](~/content/assets/images/incremental-refresh2-06.png)

The next step is to refresh the data in the partitions. 你可以使用 Power BI 服务完成这一步；也可以在 [SQL Server Management Studio 中通过 XMLA/TMSL](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms) 分批刷新分区；甚至还可以使用 [Tabular Editor 的脚本](https://www.elegantbi.com/post/datarefreshintabulareditor)。

### 应用增量刷新策略后的完全刷新

如果你已对表应用了刷新策略，并希望执行完全刷新，则必须确保在脚本中将 [applyRefreshPolicy 设置为 false](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#override-incremental-refresh-behavior)。 This will ensure that you perform a full refresh of all the partitions in your table.
The TMSL Command would in our example look like this:

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

你也可以使用 Tabular Editor 来修改通过 Power BI Desktop 设置的现有刷新策略。 Simply follow step 6-8 above in this case.

## 使用 `EffectiveDate` 应用刷新策略

如果你希望在生成分区时覆盖当前日期（用于生成不同的滚动窗口范围），可以在 Tabular Editor 中使用一个小脚本，通过 [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) 参数来应用刷新策略。

选中启用增量刷新的表后，在 Tabular Editor 的“高级脚本”窗格中运行以下脚本，替代上面的步骤 8：

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![Use scripts to apply refresh policy](~/content/assets/images/incremental-refresh2-07.png)

## 使用 Tabular Editor 移除增量刷新

你可能需要从表中移除增量刷新的刷新策略。

1. 在 TOM 视图中选中该表，从 SourceExpression 属性中获取 M 代码，并将其另存一份。
2. 将 EnableRefreshPolicy 的值从 TRUE 改为 FALSE。
3. 右键单击该表，然后创建一个新的 M 分区。
4. 把上面步骤 1 中的 M 代码粘贴到该分区的表达式中。
5. 编辑 M 代码，删除包含 Table.SelectRows() 函数的步骤，该函数用于 RangeStart/RangeEnd 参数。
6. Delete all of the historical partitions. They have a SourceType of "Policy Range".
7. 刷新该表 (Tabular Editor 3)，或在服务中刷新 Dataset，以重新填充该表。
8. 可选：如果模型里没有其他表设置了增量刷新的刷新策略，可以删除 RangeStart/RangeEnd 共享表达式。
