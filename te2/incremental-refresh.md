---
uid: incremental-refresh-policy
title: Incremental Refresh
author: Daniel Otykier
updated: 2021-02-15
---
# Incremental Refresh

Datasets hosted in the Power BI service can have [Incremental Refresh](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) set up on one or more tables. To configure or modify Incremental Refresh on a Power BI dataset, you can either use the [XMLA endpoint of the Power BI service directly](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla), or you can use Tabular Editor connected to the XMLA endpoint, as described below:

> [!IMPORTANT]
> Setting up Incremental Refresh with Tabular Editor 3 is limited to dataset hosted in the Power BI Datasets service. For Analysis Services custom [partitioning](https://learn.microsoft.com/en-us/analysis-services/tabular-models/partitions-ssas-tabular?view=asallproducts-allversions) is required.

## Setting up Incremental Refresh from scratch with Tabular Editor

1. Connect to the Power BI XMLA R/W endpoint of your workspace, and open the dataset on which you want to configure Incremental Refresh.
2. Incremental refresh requires the `RangeStart` and `RangeEnd` parameters to be created ([more information](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-configure#create-parameters)), so let's start by adding two new Shared Expressions in Tabular Editor:
  ![Add shared expressions](https://user-images.githubusercontent.com/8976200/121341006-8906e900-c920-11eb-97af-ee683ff40609.png)
3. Name them `RangeStart` and `RangeEnd` respectively, set their `Kind` property to "M" and set their expression to the following (the actual date/time value you specify doesn't matter, as it will be set by the PBI service when starting the data refresh):
  ```M
  #datetime(2021, 6, 9, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime", IsParameterQueryRequired=true]
  ```
  ![Set kind property](https://user-images.githubusercontent.com/8976200/121342389-dc2d6b80-c921-11eb-8848-b67950e55e36.png)
4. Next, select the table on which you want to enable incremental refresh
5. Set the `EnableRefreshPolicy` property on the table to "true":
  ![Enable Refresh Policy](https://user-images.githubusercontent.com/8976200/121339872-3842c080-c91f-11eb-8e63-a051b34fb36f.png)
6. Configure the remaining properties according to the incremental refresh policy you need. Remember to specify an M expression for the `SourceExpression` property (this is the expression that will be added to partititions created by the incremental refresh policy, which should use the `RangeStart` and `RangeEnd` parameters to filter the data in the source). The = operator should only be applied to either RangeStart or RangeEnd, but not both, as data may be duplicated.
  ![Configure Properties](https://user-images.githubusercontent.com/45298358/170603450-8232ad55-0b4a-4ead-b113-786a781f94ad.png)
7. Save your model (Ctrl+S).
8. Right-click on the table and choose "Apply Refresh Policy".
  ![Apply Refresh Policy](https://user-images.githubusercontent.com/8976200/121342947-78577280-c922-11eb-82b5-a517fbe86c3e.png)

That's it! At this point, you should see that the Power BI service has automatically generated the partitions on your table, based on the policy you specified.

![Generated Partitions](https://user-images.githubusercontent.com/8976200/121343417-eef47000-c922-11eb-8731-1ac4dde916ef.png)

The next step is to refresh the data in the partitions. You can use the Power BI service for that, or you can refresh the partitions in batches using [XMLA/TMSL through SQL Server Management Studio](https://docs.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#refresh-management-with-sql-server-management-studio-ssms), or even using [Tabular Editor's scripting](https://www.elegantbi.com/post/datarefreshintabulareditor).

### Full refresh with incremental refresh policy applied
If you have applied a refresh policy to your table and wish to perform a full refresh, you must ensure that you set [applyRefreshPolicy to false](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-xmla#override-incremental-refresh-behavior) in your script. This will ensure that you perform a full refresh of all the partitions in your table. 
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
## Modifying existing refresh policies

You can also use Tabular Editor to modify existing refresh policies that has been set up using Power BI Desktop. Simply follow step 6-8 above in this case.

## Applying refresh policies with `EffectiveDate`

If you want to generate partitions while overriding the current date (for purposes of generating different rolling window ranges), you can use a small script in Tabular Editor to apply the refresh policy with the [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) parameter.

With the incremental refresh table selected, run the following script in Tabular Editor's "Advanced Scripting" pane, in place of step 8 above:

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![Use scripts to apply refresh policy](https://user-images.githubusercontent.com/8976200/121344362-f9633980-c923-11eb-916c-44a35cf03a36.png)


