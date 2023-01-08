---
uid: incremental-refresh-about
title: What is a Refresh Policy?
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# Incremental Refresh

Datasets hosted in the Power BI service can have [Incremental Refresh](https://learn.microsoft.com/en-us/power-bi/connect-data/incremental-refresh-overview) configured for one or more data tables. <span style="color:#01a99d">__The purpose of Incremental Refresh is to achieve faster, more efficient refreshes by only retrieving recent/changing data, _incrementally refreshing_ the table.__</span> To do this, the table is automatically divided into partitions, such that only recent or changing data is refreshed ("hot" partitions) or even retrieved in real-time (["Direct Query" partitions in "Hybrid Tables"](https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables)) while older, static data is archived ("cold" partitions). 

Incremental refresh can be easily configured and modified from within Tabular Editor.

<div class="NOTE">
  <h5>WHY SET UP INCREMENTAL REFRESH?</h5>
  Configuring incremental refresh has a number of benefits, particularly for larger data models:  
  <li> Reduce refresh time & resource consumption
  <li> Experience shorter and more dependable scheduled refreshes
</div>

## How is a table partitioned for Incremental Refresh?

To create the partitions, Power BI uses the `RangeStart` and `RangeEnd` _datetime_ parameters in Power Query. These parameters are used in a filter step of the table partition M Expression, filtering a table date column. 

An example is given below. Incremental Refresh is applied to a table _'Orders'_ upon the _[Order Date]_ column:

# [Filter Step Only](#tab/tabid-a)
```M
// The filter step must be able to fold back to the data source
// No steps before this should break query folding
#"Incremental Refresh Filter Step" = 
    Table.SelectRows(
        Navigation,
        each 
            [OrderDate] <= #"RangeStart" and 
            [OrderDate] > #"RangeEnd"
    )
```

# [Full M Expression](#tab/tabid-b)
```M
let
    // The data source must support Query Folding
    Source = Sql.Database(#"ServerParameter", #"DatabaseParameter"),

    Navigation = 
        Source{ 
            [ Schema="DW_fact", Item="Internet Sales" ] 
        } [Data],

    // The filter step must be able to fold back to the data source
    // No steps before this should break query folding
    #"Incremental Refresh Filter Step" = 
        Table.SelectRows(
            Navigation,
            each 
                [OrderDate] <= #"RangeStart" and 
                [OrderDate] > #"RangeEnd"
        )
in
    #"Incremental Refresh Filter Step"
```

# [RangeStart](#tab/tabid-c)
```M
// It does not matter what the initial value is for the RangeStart parameter
// RangeStart should be greater than RangeEnd
// The parameter must be of data type "datetime"
#datetime(2022, 12, 31, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```

# [RangeEnd](#tab/tabid-d)
```M
// It does not matter what the initial value is for the RangeEnd parameter
// RangeEnd should be less than RangeStart
// The parameter must be of data type "datetime"
#datetime(2022, 12, 01, 0, 0, 0) 
    meta 
        [
            IsParameterQuery = true, 
            IsParameterQueryRequired = true, 
            Type = type datetime
        ]
```
***

<div class="NOTE">
  <h5>INCREMENTAL REFRESH ONLY WORKS WITH QUERY FOLDING</h5>
  Incremental Refresh can only be configured with data sources that support <a href="https://learn.microsoft.com/en-us/power-query/power-query-folding">Power Query query folding</a>.
  Query folding must not be <a href="https://learn.microsoft.com/en-us/power-query/step-folding-indicators">broken</a> before the filter step is applied.
</div>

The number, type and refresh behavior of table partitions depends on the configured table __Refresh Policy__.

## What is a Refresh Policy?

A Refresh Policy specifies how the data should be partitioned, the partition types, and which partitions should be refreshed. These __Policy Range__ partitions are goverend by a set of Refresh Policy properties, visible in the Table object:

<div class="WARNING">
  <h5>POWER BI DESKTOP LIMITATIONS</h5>
  <p>Configuring incremental refresh when connected to a local Power BI Desktop model is not supported.
  To configure incremental refresh for a Power BI Desktop model, use the Power BI Desktop user interface.</p>
</div>

### Refresh Policy properties

#### Overview

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

<div class="table-responsive">
    <table class="table table-bordered table-striped table-condensed">
        <thead>
            <tr>
                <th class="formatting">Property Name</th>
                <th class="formatting">Power BI Desktop Equivalent</th>
                <th class="formatting">Description</th>
                <th class="formatting">Expected Value</th>
            </tr>
        </thead>
        <tbody style="font-size:80%;">
            <tr>
                <td class="formatting"><em>EnableRefreshPolicy</em></td>
                <td class="formatting">Incrementally refresh this table</td>
                <td class="formatting">Whether a refresh policy is enabled for the table. In Tabular Editor, other Refresh Policy properties will only be visible if this value is set to 'True'.</td>
                <td class="formatting"><code>True</code> or <code>False</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><em>IncrementalGranularity</em></td>
                <td class="formatting">Incremental Refresh Period</td>
                <td class="formatting">The granularity of the incremental window. Example: <em>"Refresh data in the last 30 <strong><em>days</em></strong> before refresh date."</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> or <code>Year</code>. Must be smaller than or equal to the IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><em>IncrementalPeriods</em></td>
                <td class="formatting">Number of Incremental Refresh Periods</td>
                <td class="formatting">The number of periods for the incremental window.<br /><br>Example: <em>"Refresh data in the last <strong><em>30</em></strong> days before refresh date."</em></td>
                <td class="formatting">An integer of the number of <em>IncrementalGranularity</em> periods. Must define a total period smaller than the <em>RollingWindowPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><em>IncrementalPeriodsOffset</em></td>
                <td class="formatting">Only refresh complete days</td>
                <td class="formatting">The offset to be applied to <em>IncrementalPeriods</em>.<br /><br>Example when set to -1, <em>IncrementalPeriods</em> = 30 and <em>IncrementalGranularity</em> = 'Day': <em>"Only refresh data in the last 30 days from refresh date -1 Day.</em></td>
                <td class="formatting">An integer of the number of <em>IncrementalGranularity</em> periods to shift the Incremental window.</td>
            </tr>
            <tr>
                <td class="formatting"><em>Mode</em></td>
                <td class="formatting">Get the latest data in real time with DirectQuery</td>
                <td class="formatting">Specifies whether Incremental Refresh is configured with only import partitions or also a DirectQuery partition, to result in a <a href="https://learn.microsoft.com/en-us/power-bi/connect-data/service-dataset-modes-understand#hybrid-tables"    target="_blank">"Hybrid Table"</a>.</td>
                <td class="formatting"><code>Import</code> or <code>Hybrid</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><em>PolicyType</em></td>
                <td class="formatting">N/A</td>
                <td class="formatting">Specifies the type of refresh policy.</td>
                <td class="formatting">Can only contain a single value <code>Basic</code>.</td>
            </tr>
            <tr>
                <td class="formatting"><em>PollingExpression</em></td>
                <td class="formatting">Detect Data Changes</td>
                <td class="formatting">The M Expression used to detect changes in a specific column such as <em>LastUpdateDate</em></td>.
                <td class="formatting">A valid M Expression that returns a scalar value of the latest date in a column. All records in archive partitions containing that value for the column will be refreshed.</td>
            </tr>
            <tr>
                <td class="formatting"><em>RollingWindowGranularity</em></td>
                <td class="formatting">Archive Data Period</td>
                <td class="formatting">The granularity of the rolling window.<br /><br>Example: <em>"Archive data starting 3 <strong><em>years</em></strong> before refresh date."</em></td>
                <td class="formatting"><code>Day</code>, <code>Month</code>, <code>Quarter</code> or <code>Year</code>. Must be larger than or equal to the IncrementalGranularity.</td>
            </tr>
            <tr>
                <td class="formatting"><em>RollingWindowPeriods</em></td>
                <td class="formatting">Number of Archive Data Periods</td>
                <td class="formatting">The number of periods for the rolling window.<br /><br>Example: <em>"Archive data starting <strong><em>3</em></strong> years before refresh date."</em></td>
                <td class="formatting">An integer of the number of <em>RollingWindowGranularity</em> periods. Must define a total period larger than the   <em>IncrementalPeriods</em></td>
            </tr>
            <tr>
                <td class="formatting"><em>SourceExpression</em></td>
                <td class="formatting">Power Query Source Expression</td>
                <td class="formatting">The M Expression for the table data source. This is where the original table M Expression is, and where any existing Power Query transformations would be modified.</td>
                <td class="formatting">A valid M Expression containing a filter step appropriately using <code>RangeStart</code> and <code>RangeEnd</code>.</td>
            </tr>
        </tbody>
    </table>
</div>