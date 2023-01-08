---
uid: incremental-refresh-modify
title: Modify an Existing Refresh Policy
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# Modifying Incremental Refresh

To change Incremental Refresh, you adjust the Refresh Policy properties. Depending on what you want to change, you will adjust a different property. A full overview of these properties is [here](docs.tabulareditor.com/te3/incremental-refresh-about.html#RefreshPolicyPropertiesOverview). 

## Change Incremental Refresh

Below is a general description of how you modify an existing Refresh Policy:

1. Connect to the model
2. Select the table already configured for Incremental Refresh
3. In the _Properties_ window, go to the _Refresh Policy_ section.
4. Change the __Property__ specified in the below sections, depending on what you want to change
5. Right-click the table and select _Apply Refresh Policy_
6. Deploy the model changes
7. Select and right-click all partitions and select _Refresh > Full refresh (partition)_

--------------------------

Below is an overview of common changes one might make to an existing Refresh Policy:

### A. Extend or Reduce the Window for Archived Data

__Purpose:__ Add or reduce the amount of data in the model.

__Property:__ <span style="color:#BC4A47">_RollingWindowPeriods_</span>

__Note:__ You can also change the <span style="color:#BC4A47">_RollingWindowGranularity_</span> to make a more fine-grain selection, i.e. from 3 Years to 36 Months.

### B. Extend or Reduce the Window for Refreshed Data

__Purpose:__ Add or reduce the amount of data being refreshed in a scheduled refresh operation.

__Property:__ <span style="color:#455C86">_IncrementalWindowPeriods_</span>

__Note:__ You can also change the <span style="color:#455C86">_IncrementalWindowGranularity_</span> to make a more fine-grain selection, i.e. from 3 Years to 36 Months.

### C. Only Refresh Complete Periods

__Purpose:__ Exclude partial (incomplete) periods from the <span style="color:#BC4A47">Rolling Window</span>

__Property:__ <span style="color:#455C86">_IncrementalWindowPeriodsOffset_</span> = -1

__Note:__ You can further offset this window to refresh i.e. only the periods behind the most recent complete period. 

### D. Change Incremental Refresh Mode

__Purpose:__ To change from `Import` to `Hybrid` tables, or vice-versa.

__Property:__ _Mode_

__Note:__ Follow the below process to change Incremental Refresh Mode:

5. Change _Mode_ to the desired value `Import` or `Hybrid`
6. Right-click the table and select _Apply Refresh Policy_
7. Deploy the model changes
8. Select and right-click all partitions and select _Refresh > Full refresh (partition)_

> [!NOTE]
> It is recommended to check that the Rolling Window is appropriately set for the _Mode_ selected. When switching from `Import` to `Hybrid` Mode, the latest Policy Range Partition will become the DirectQuery partition. You may wish

### E. Add 'Detect Data Changes'

__Purpose:__ To configure that archived data will refresh if the value of a date column (i.e. _LastUpdate_) changes.

__Property:__ _PollingExpression_

__Note:__ Follow the below process to configure 'Detect Data Changes':

5. When the table is selected, in the _Expression Editor_ window, select _Polling Expression_ from the top-left dropdown
6. Copy in the below M Expression, replacing _LastUpdate_ with your desired column name.

```M
// Retrieves the maximum value of the column [LastUpdate]
// Replace LastUpdate with your own column name
// The data will refresh for any records where the value in this column
//    equals the maximum value in the column across the entire table
let
    #"maxLastUpdate" =
        List.max(
            // Replace the below with your column and table name
            Orders[LastUpdate] 
        ),

    accountForNu11 =
        if #"maxLastUpdate" = null
        then #datetime(1901, 01, 01, 00, 00, 00)
        else #"maxLastUpdate"
in
    accountForNu11
```

7. Right-click the table and select _Apply Refresh Policy_
8. Deploy the model changes
9. Select and right-click all partitions and select _Refresh > Full refresh (partition)_

> [!WARNING]
> Any records will update if the value equals the maximum value in the column. It does not necessarily update explicitly  because the value has changed, or if the value equals the refresh date.

### F. Applying refresh policies with `EffectiveDate`

If you want to generate partitions while overriding the current date (for purposes of generating different rolling window ranges), you can use a small script in Tabular Editor to apply the refresh policy with the [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) parameter.

With the incremental refresh table selected, run the following script in Tabular Editor's "Advanced Scripting" pane, in place of step 8 above:

```csharp
var effectiveDate = new DateTime(2020, 1, 1);  // Todo: replace with your effective date
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```

![Use scripts to apply refresh policy](https://user-images.githubusercontent.com/8976200/121344362-f9633980-c923-11eb-916c-44a35cf03a36.png)

### G. Disable Incremental Refresh

__Purpose:__ To disable a refresh policy because it is not needed or the use-case no longer fits.

__Property:__ _EnableRefreshPolicy_

__Note:__ To disable Incremental Refresh, follow the below steps:

5. With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown
6. Copy the _Source Expression_ to a separate text editor window.
7. Change _EnableRefreshPolicy_ to `False`
8. Select and delete all of the Policy Range partitions
9. Right-click the table and select _Create > New Partition_
10. Copy the _Source Expression_ from __Step 6__ into the _Expression Editor_ as the _M Expression_ when selecting the new partition. 
11. Set the partition _kind_ property to `M`

