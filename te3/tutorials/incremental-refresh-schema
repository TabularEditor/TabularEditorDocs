---
uid: incremental-refresh-schema
title: Add or Remove Columns in a Table with Incremental Refresh
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

When you need to add or remove columns from a table with Incremental Refresh, you must update the table schema. 

## General Protocol

5. With the table selected, in the _Expression Editor_ window, select _Source Expression_ from the top-left dropdown
6. Check whether any changes to the Power Query _Source Expression_ due to the schema changes are necessary.
7. Check for the _Polling Expression_, if configured. The _Polling Expression_ is selected from the same dropdown menu.

> [!WARNING]
> If schema changes arise from the Data Source, you may still need to apply changes to your Power Query Source Expression. For example, if you perform a 'Remove Other Columns' or 'Select Columns' step, you will need to ensure any new column names are added, or removed column names are taken out.

### Removing Columns

1. Delete the column from the model 

### Adding Columns from the Data Source

1. Right-click the table and select 'Update table schema...'
2. In the 'Apply Schema Changes' dialogue, confirm the changes you want done to your table
3. Right-click the table and select _Apply Refresh Policy_
4. Deploy the model changes
5. Select and right-click all partitions and select _Refresh > Full refresh (partition)_



### Adding Columns from Power Query