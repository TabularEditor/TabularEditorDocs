---
uid: incremental-refresh-schema
title: Add or Remove Columns in a Table that uses Incremental Refresh
author: Kurt Buhler
updated: 2023-01-09
applies_to:
  editions:
    - edition: Desktop
      none: x
    - edition: Business
    - edition: Enterprise
---
# Modifying Incremental Refresh Table Schemas

<br></br>

![Incremental Refresh Workspace Mode Visual Abstract](../../images/incremental-refresh-update-schema-header.png)

<br></br>

__When adding or removing columns from a table configured with Incremental Refresh, you must update the table schema.__ Generally, this follows the same protocol as updating table schemas for single-partition tables. Tabular Editor can detect and update the schema for you, automatically: 

1. __Detect schema changes:__ Right-click the table and select _'Update table schema...'_.

  <br></br>

  <img src="../../images/incremental-refresh-update-table-schema.png" alt="Update Table Schema" style="width:450px !important"/>

  <br></br>

2. __Apply detected schema changes:__ In the _'Apply Schema Changes'_ dialogue, confirm the desired schema changes.
3. __Apply changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.

  <br></br>

  <img src="../../images/incremental-refresh-apply-refresh-policy.png" alt="Apply Refresh Policy" style="width:450px !important"/>

  <br></br>

5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

  <br></br>
  
  <img src="../../images/incremental-refresh-refresh-all-partitions.png" alt="Refresh All Partitions" style="width:450px !important"/>
  
  
  <br></br>

### Schema Update Considerations with Incremental Refresh

- For Incremental Refresh, the main consideration is that __all partitions must be refreshed__.<br />To do this, __select and right-click all partitions. Select *Refresh > Full refresh (partition)*__. 

- A second consideration is __the _Source Expression_ and _Polling Expression_ may need to be updated to reflect schema changes__. Not updating these M Expressions may result in refresh errors. Examples: 
  - `Table.TransformColumnTypes` step refers to a column that will be removed in the updated schema.
  - `Table.SelectColumns` step lists columns to be kept; the new column is not added to this list.

<div class="WARNING">
  <h5>CHECK SOURCE EXPRESSION BEFORE UPDATING SCHEMA</h5>
  <p>If schema changes arise from the Data Source, you may still need to apply changes to your Power Query <b><em>Source Expression</em></b> or <b><em>Polling Expression</em></b>. It is recommended that you carefully check these expressions before using <em>'Update table schema...'</em></p>
</div>

<br></br>

------------------------------------

<br></br>

### Removing Columns

Depending on where the column is removed, you may follow a slightly different protocol:

# [Supported Data Source](#tab/removingfromsource)

For columns removed in the __data source__ (i.e. removed from the view accessed by Power BI), follow the below steps:

1. __Detect schema changes:__ Right-click the table and select _'Update table schema...'_.
2. __Apply detected schema changes:__ In the _'Apply Schema Changes'_ dialogue, confirm the desired schema changes.
3. __Apply changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

# [Power Query](#tab/removingfrompq)

For columns removed via __Power Query__ (i.e. using `Table.RemoveColumns`), follow the below steps:

1. __Detect schema changes:__ Right-click the table and select _'Update table schema...'_.
2. __Apply detected schema changes:__ In the _'Apply Schema Changes'_ dialogue, confirm the desired schema changes.
3. __Apply changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

# [Unsupported Data Source](#tab/removingfromunsupportedsource)

If you are __unable to automatically update the table schema__ using _'Update table schema...'_ from the table context menu, follow the below steps. These steps are the same for both columns removed in the data source or in Power Query.

1. __Select the Source Expression:__ With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown.
2. __Update the Power Query Expressions:__ Check and remove any named references to the removed column, if applicable. If the column is being excluded via Power Query, you can make the appropriate changes, here.
3. __Manually update the schema:__ Delete the data column object from the table. 
4. __Apply changes:__ Deploy the model changes.
3. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

***
<div class="NOTE">
  <h5>DELETED COLUMN OBJECTS MAY STILL BE QUERIED</h5>
  <p>Deleting column objects from the model does not prevent them from being queried if they still exist in the source and are not removed in the Native Query or <b><em>Source Expression</em></b>. Columns queried but not used can have a negative impact on refresh time and resource usage. It is recommended that you remove columns from both metadata and either data sources (i.e. views) or in the <b><em>Source Expression</em></b>.</p>
</div>

<br></br>

------------------------------------

<br></br>

### Adding Columns

Depending on where the column is added, you may follow a slightly different protocol: 

# [Supported Data Source](#tab/addingfromsource)

For columns removed in the __data source__ (i.e. added to the view accessed by Power BI), follow the below steps:

1. __Detect schema changes:__ Right-click the table and select _'Update table schema...'_.
2. __Apply detected schema changes:__ In the _'Apply Schema Changes'_ dialogue, confirm the desired schema changes.
3. __Apply changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

# [Power Query](#tab/addingfrompq)

For columns removed via __Power Query__ (i.e. using `Table.AddColumns`), follow the below steps:

1. __Detect schema changes:__ Right-click the table and select _'Update table schema...'_.
2. __Apply detected schema changes:__ In the _'Apply Schema Changes'_ dialogue, confirm the desired schema changes.
3. __Apply changes:__ Deploy the model changes.
4. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
5. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

# [Unsupported Data Source](#tab/addingfromunsupportedsource)

If you are __unable to automatically update the table schema__ using _'Update table schema...'_ from the table context menu, follow the below steps. These steps are the same for both columns removed in the data source or in Power Query.

1. __Select the Source Expression:__ With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown.
2. __Update the Power Query Expressions:__ Check and remove any named references to the removed column, if applicable. If the column is being excluded via Power Query, you can make the appropriate changes, here.
3. __Manually update the schema:__ Right-click the table and select _Create > Data column_. Name the column appropriately.
4. __Configure the new column:__ Set the column's `data type` property, appropriately. Set the `Source Column` property such that it matches the source. Any additional properties can also be configured (i.e. `Format String`, `SummarizeBy`, `Data Category`...) and the column can be added to the appropriate display folder.
5. __Apply changes:__ Deploy the model changes.
6. __Apply Refresh Policy:__ Right-click the table and select _Apply Refresh Policy_.
7. __Refresh all partitions:__ Select and right-click all partitions. Select _Refresh > Full refresh (partition)_.

***