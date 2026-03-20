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
        - edition: 桌面版
          none: true
        - edition: 商业版
          partial: true
          note: "仅限 SQL Server Standard Edition"
        - edition: 企业版
          full: true
---

# 增量刷新

托管在 Power BI 服务中的 Dataset 可以在一个或多个表上设置 [增量刷新](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview)。 要在 Power BI 的 Dataset 上配置或修改增量刷新，你可以直接使用 Power BI 服务的 [XMLA endpoint](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla)；也可以按照下面的说明，使用连接到 XMLA endpoint 的 Tabular Editor 来操作：

> [!IMPORTANT]
> 在 Tabular Editor 3 中设置增量刷新仅适用于托管在 Power BI Datasets 服务中的 Dataset。 对于 Analysis Services，需要自定义[分区](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions)。

## 使用 Tabular Editor 从零开始设置增量刷新

1. 连接到你的 Workspace 的 Power BI XMLA R/W 终结点，然后打开你要配置增量刷新的 Dataset。
2. 增量刷新要求先创建 `RangeStart` 和 `RangeEnd` 参数（[更多信息](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)）。我们先在 Tabular Editor 中添加两个新的共享表达式：
   ![添加共享表达式](https://user-images.githubusercontent.com/8976200/121341006-8906e900-c920-11eb-97af-ee683ff40609.png)
3. 分别将它们命名为 `RangeStart` 和 `RangeEnd`，将它们的 `Kind` 属性设置为 "M"，并将表达式设置为以下内容（你填写的实际日期/时间无关紧要，因为在开始数据刷新时会由 Power BI 服务设置）：

  ```M
  #datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
  ```

![设置 Kind 属性](https://user-images.githubusercontent.com/8976200/121342389-dc2d6b80-c921-11eb-8848-b67950e55e36.png)
4。 接下来，选择要启用增量刷新的表
5。 将表的 `EnableRefreshPolicy` 属性设置为 "true"：
![启用刷新策略](https://user-images.githubusercontent.com/8976200/121339872-3842c080-c91f-11eb-8e63-a051b34fb36f.png)
6。 根据你需要的增量刷新策略，配置其余属性。 别忘了为 `SourceExpression` 属性指定一个 M 表达式（增量刷新的刷新策略创建的分区会添加该表达式；它应使用 `RangeStart` 和 `RangeEnd` 参数在源端筛选数据）。 “=”运算符只能应用于 RangeStart 或 RangeEnd 其中一个，不能同时用于两者，否则可能会产生重复数据。
![配置属性](https://user-images.githubusercontent.com/45298358/170603450-8232ad55-0b4a-4ead-b113-786a781f94ad.png)
7。 保存模型（Ctrl+S）。
8。 右键单击该表，然后选择“应用刷新策略”。
![应用刷新策略](https://user-images.githubusercontent.com/8976200/121342947-78577280-c922-11eb-82b5-a517fbe86c3e.png)

就这样！ 这时你会看到 Power BI 服务已经根据你指定的策略，自动为这张表生成了分区。

![生成的分区](https://user-images.githubusercontent.com/8976200/121343417-eef47000-c922-11eb-8731-1ac4dde916ef.png)

下一步是刷新这些分区中的数据。 你可以使用 Power BI 服务完成这一步；也可以在 [SQL Server Management Studio 中通过 XMLA/TMSL](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms) 分批刷新分区；甚至还可以使用 [Tabular Editor 的脚本](https://www.elegantbi.com/post/datarefreshintabulareditor)。

### 应用增量刷新策略后的完全刷新

如果你已对表应用了刷新策略，并希望执行完全刷新，则必须确保在脚本中将 [applyRefreshPolicy 设置为 false](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#override-incremental-refresh-behavior)。 这样可以确保对表中的所有分区执行完全刷新。
在我们的示例中，TMSL 命令如下所示：

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

你也可以使用 Tabular Editor 来修改通过 Power BI Desktop 设置的现有刷新策略。 在这种情况下，只需按上面的第 6-8 步操作即可。

## 使用 `EffectiveDate` 应用刷新策略

如果你希望在生成分区时覆盖当前日期（用于生成不同的滚动窗口范围），可以在 Tabular Editor 中使用一个小脚本，通过 [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) 参数来应用刷新策略。

选中启用增量刷新的表后，在 Tabular Editor 的“高级脚本”窗格中运行以下脚本，替代上面的步骤 8：

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![使用脚本应用刷新策略](https://user-images.githubusercontent.com/8976200/121344362-f9633980-c923-11eb-916c-44a35cf03a36.png)

## 使用 Tabular Editor 移除增量刷新

你可能需要从表中移除增量刷新的刷新策略。

1. 在 TOM 视图中选中该表，从 SourceExpression 属性中获取 M 代码，并将其另存一份。
2. 将 EnableRefreshPolicy 的值从 TRUE 改为 FALSE。
3. 右键单击该表，然后创建一个新的 M 分区。
4. 把上面步骤 1 中的 M 代码粘贴到该分区的表达式中。
5. 编辑 M 代码，删除包含 Table.SelectRows() 函数的步骤，该函数用于 RangeStart/RangeEnd 参数。
6. 删除所有历史分区。 它们的 SourceType 为“Policy Range”。
7. 刷新该表 (Tabular Editor 3)，或在服务中刷新 Dataset，以重新填充该表。
8. 可选：如果模型里没有其他表设置了增量刷新的刷新策略，可以删除 RangeStart/RangeEnd 共享表达式。
