---
uid: data-refresh-view
title: 数据刷新视图
author: Daniel Otykier
updated: 2021-09-08
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

# 数据刷新视图

The Data Refresh view allows you to investigate in detail how your data is being refreshed on the server.
A new active refresh will appear when a new refresh is triggered through the TOM Explorer.

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Data Refresh View" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的数据刷新视图。 New refresh can be started by right-clicking a table and selecting refresh </figcaption>
</figure>

新的刷新将在后台运行，因此你可以继续构建数据集。如果刷新失败，Tabular Editor 会通过弹出窗口通知你。

## 数据刷新视图中的列

“数据刷新”视图会为每次刷新操作显示以下信息：

- **对象**：正在刷新的模型对象名称（表、分区或模型）
- **说明**：关于刷新操作及其当前状态的更多信息
- **进度**：显示截至目前已导入的行数。
- **开始时间**：刷新操作开始时的日期和时间。 This is useful for tracking when operations were initiated, especially when multiple refreshes are queued
- **持续时间**：从刷新操作开始到现在的已用时间；对正在运行的操作会实时更新

### 对刷新操作排序

可点击任意列标题，对刷新操作进行排序。 This is particularly useful for:

- 点击 **开始时间** 列，可按时间顺序对刷新操作排序：最新的操作显示在最前（降序）或最后（升序）
- 按 **持续时间** 排序，以识别运行时间较长的操作
- 按 **对象** 排序，按表或分区名称对刷新进行分组

Click a column header once to sort ascending, and click again to sort descending. This makes it easy to identify the latest refresh operations when working with multiple refresh queues.

> [!NOTE]
> All the messages and durations shown in the Data Refresh window are estimates only. 在处理过程中，Tabular Editor 会监听来自 SSAS 的[跟踪事件](https://learn.microsoft.com/en-us/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions)。 SSAS is not guaranteed to send all trace messages to the client (for example it may throttle the trace event notifications during times of peak CPU/memory consumption).

> [!TIP]
> 如果你需要关于刷新进度和持续时间的准确且可靠的信息，你可以将 [SQL Server Profiler](https://learn.microsoft.com/en-us/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) 连接到你的 SSAS 实例，并在处理期间手动收集相关信息。