---
uid: data-refresh-view
title: Data Refresh view
author: Daniel Otykier
updated: 2026-10-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---
# Data Refresh View

The **Data Refresh** view shows the progress of refresh operations on the server. A refresh you start from the TOM Explorer appears in the view as an active refresh.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Data Refresh View" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Data Refresh view in Tabular Editor. Start a refresh by right-clicking a table and selecting Refresh.</figcaption>
</figure>

Refreshes run in the background while you keep editing the model, and an error message appears if a refresh fails.

## Data Refresh view columns

Each refresh operation has these columns:

- **Object**: the model object being refreshed (table, partition or model).
- **Description**: details about the refresh operation and its current state.
- **Progress**: the number of rows imported so far.
- **Start Time**: the date and time the operation began.
- **Duration**: the elapsed time since the operation began, updated live for active operations.

### Sorting refresh operations

Click a column header to sort by that column: once for ascending, again for descending. For example:

- sort by **Start Time**, descending, to list the latest refresh operations first
- sort by **Duration** to find long-running operations
- sort by **Object** to group refreshes by table or partition name

> [!NOTE]
> All the messages and durations shown in the Data Refresh window are estimates only. Tabular Editor listens to [trace events from SSAS](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions) during processing. SSAS is not guaranteed to send all trace messages to the client (for example it may throttle the trace event notifications during times of peak CPU/memory consumption). 

> [!TIP]
> If you need accurate and reliable information about refresh progress and durations, you should connect [SQL Server Profiler](https://learn.microsoft.com/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) to your SSAS instance, and collect the information manually during processing.
