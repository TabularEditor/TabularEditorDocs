---
uid: data-refresh-view
title: Data Refresh view
author: Daniel Otykier
updated: 2026-11-13
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
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Data Refresh view with a completed job expanded to its tables and partitions, each with its own duration" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Data Refresh view in Tabular Editor. Start a refresh by right-clicking a table and selecting Refresh.</figcaption>
</figure>

Refreshes run in the background while you keep editing the model, and an error message appears if a refresh fails.

Each refresh is a job row that expands to a row for each table and partition the server refreshes. For a short refresh, these rows appear a few seconds after the job completes. A row the server reports an error for stays marked as failed. If a refresh fails before it reaches the server, an error row below the job shows the reason.

## Data Refresh view columns

Each refresh operation has these columns:

- **Object**: the model object being refreshed (table, partition or model).
- **Description**: details about the refresh operation and its current state.
- **Progress**: the number of rows imported so far.
- **Start Time**: the date and time the operation began.
- **Duration**: the time the server spent on the object. While an operation runs, the column shows the time elapsed so far, updated live.

### Sorting refresh operations

Click a column header to sort by that column: once for ascending, again for descending. For example:

- sort by **Start Time**, descending, to list the latest refresh operations first
- sort by **Duration** to find long-running operations
- sort by **Object** to group refreshes by table or partition name

> [!NOTE]
> The rows, messages and durations come from the [trace events](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions) the server sends during the refresh. The server doesn't guarantee delivery of every trace event, for example when it throttles trace notifications under heavy CPU or memory load. A row whose events don't arrive is missing, and a row whose first events don't arrive shows a duration that's too short.

> [!TIP]
> If you need accurate and reliable information about refresh progress and durations, you should connect [SQL Server Profiler](https://learn.microsoft.com/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) to your SSAS instance, and collect the information manually during processing.
