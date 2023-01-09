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

<br></br>

![Incremental Refresh Visual Abstract](../../images/incremental-refresh-modify-a-refresh-policy.png)

<br></br>

__Incremental Refresh is changed by adjusting the Refresh Policy properties.__ Depending on what you want to change, you will adjust a different property. A full overview of these properties is [here](xref:incremental-refresh-about#overview-of-all-properties). 

<br></br>

## Change Incremental Refresh

Below is a general description of how you modify an existing Refresh Policy:

1. __Connect:__ Connect to the model.
2. __Select the Table:__ Select the table already configured for Incremental Refresh.
3. __Find 'Refresh Policy' properties:__ In the _Properties_ window, go to the _Refresh Policy_ section.

    <br></br>

    <img src="../../images/Incremental-refresh-properties.png" alt="Properties of Incremental Refresh" style="width:704px !important"/>

    <br></br>

4. __Change the property:__ Change the __Property__ specified in the below sections, depending on what you want to change. For an overview of all Refresh Policy properties and what they do, see [here](xref:incremental-refresh-about#overview-of-all-properties).
5. __Apply Changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.

    <br></br>

    <img src="../../images/incremental-refresh-apply-refresh-policy.png" alt="Apply Refresh Policy" style="width:450px !important"/>

    <br></br>

7. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

    <br></br>

    <img src="../../images/incremental-refresh-refresh-all-partitions.png" alt="Refresh All Partitions" style="width:450px !important"/>

    <br></br>
<br></br>


--------------------------

Below is an overview of common changes one might make to an existing Refresh Policy:

<br></br>

### Extend or Reduce the Window for Archived Data

__Purpose:__ Add or reduce the amount of data in the model.

__Property:__ <span style="color:#BC4A47">_RollingWindowPeriods_</span>. Increase it to extend the window (more data); decrease it to reduce the window (less data).

__Note:__ You can also change the <span style="color:#BC4A47">_RollingWindowGranularity_</span> to make a more fine-grain selection, i.e. from 3 Years to 36 Months.

<br></br>

------------------------------------

<br></br>

### Extend or Reduce the Window for Refreshed Data

__Purpose:__ Add or reduce the amount of data being refreshed in a scheduled refresh operation.

__Property:__ <span style="color:#455C86">_IncrementalWindowPeriods_</span>. Increase it to extend the window (more data); decrease it to reduce the window (less data).

__Note:__ You can also change the <span style="color:#455C86">_IncrementalWindowGranularity_</span> to make a more fine-grain selection, i.e. from 3 Years to 36 Months.

<br></br>

------------------------------------

<br></br>

### Only Refresh Complete Periods

__Purpose:__ Exclude partial (incomplete) periods from the <span style="color:#BC4A47">Rolling Window</span>

__Property:__ <span style="color:#455C86">_IncrementalWindowPeriodsOffset_</span>. Set the value to `-1` to offset the period by 1, excluding the current period.

__Note:__ You can further offset this window to refresh i.e. only the periods behind the most recent complete period. 

<br></br>

------------------------------------

<br></br>

### Change Incremental Refresh Mode

__Purpose:__ To change from `Import` to `Hybrid` tables, or vice-versa.

__Property:__ _Mode_

__Note:__ Follow the below process to change Incremental Refresh Mode:

5. Change _Mode_ to the desired value `Import` or `Hybrid`
6. Right-click the table and select _Apply Refresh Policy_
7. Deploy the model changes
8. Select and right-click all partitions and select _Refresh > Full refresh (partition)_

> [!NOTE]
> It is recommended to check that the Rolling Window is appropriately set for the selected _Mode_. When switching from `Import` to `Hybrid` Mode, the latest Policy Range Partition will become the DirectQuery partition. You may wish to opt for a more fine-grain window, to limit the amount of data queried with DirectQuery.

<br></br>

------------------------------------

<br></br>

### Configure 'Detect Data Changes'

__Purpose:__ To configure that archived data will refresh if the value of a date column (i.e. _LastUpdate_) changes.

__Property:__ _PollingExpression_. Add a valid M Expression which returns a maximum date value for a column. All records containing that date will be refreshed, irrespective of their partition.

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

<br></br>

------------------------------------

<br></br>

### Applying refresh policies with `EffectiveDate`

If you want to generate partitions while overriding the current date (for purposes of generating different rolling window ranges), you can use a small script in Tabular Editor to apply the refresh policy with the [EffectiveDate](https://docs.microsoft.com/en-us/analysis-services/tmsl/refresh-command-tmsl?view=asallproducts-allversions#optional-parameters) parameter.

With the incremental refresh table selected, run the following script in Tabular Editor's "Advanced Scripting" pane, in place of step 8 above:

```csharp
// Todo: replace with your effective date
var effectiveDate = new DateTime(2020, 1, 1);  
Selected.Table.ApplyRefreshPolicy(effectiveDate);
```
<br></br>

<img src="../../images/effective-date-te3.png" alt="Effective Date" style="width:700px !important"/>

<br></br>

------------------------------------

<br></br>

### Disabling Incremental Refresh

__Purpose:__ To disable a refresh policy because it is not needed or the use-case no longer fits.

__Property:__ _EnableRefreshPolicy_

__Note:__ To disable Incremental Refresh, follow the below steps:

1. __Copy the _Source Expression_:__ With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown. Copy the _Source Expression_ to a separate text editor window.
2. __Disable the Refresh Policy:__ Change _EnableRefreshPolicy_ to `False`
3. __Remove all Policy Range partitions:__ Select and delete all of the Policy Range partitions
4. __Create a new M Partition:__ Right-click the table and select _Create > New Partition_. Set the partition _kind_ property to `M`.
5. __Paste the _Source Expression_:__ Copy the _Source Expression_ from __Step 6__ into the _Expression Editor_ as the _M Expression_ when selecting the new partition. 
6. __Apply Changes:__ Deploy the model changes.
7. __Refresh the Table:__ Select and right-click the table. Select _Refresh > Full refresh (table)_. 
