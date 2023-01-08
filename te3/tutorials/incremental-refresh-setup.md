---
uid: incremental-refresh-setup
title: Set Up a New Refresh Policy
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# Setting up Incremental Refresh

To set up Incremental Refresh, you must configure a new Refresh Policy for the table. This is easily done by configuring the Refresh Policy properties once _EnableRefreshPolicy_ is set to `True`. A full overview of these properties is [here](docs.tabulareditor.com/te3/incremental-refresh-about.html#RefreshPolicyPropertiesOverview).

## Set up from scratch with Tabular Editor

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