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

数据刷新视图可让你深入了解服务器上的数据是如何刷新的。
当你通过 TOM Explorer 触发一次新的刷新时，列表中会出现一条新的活动刷新记录。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="Data Refresh View" style="width: 550px;"/><figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的数据刷新视图。 可通过右键单击某个表并选择“刷新”来启动新的刷新。</figcaption>
</figure>

新的刷新将在后台运行，因此你可以继续构建数据集。如果刷新失败，Tabular Editor 会通过弹出窗口通知你。

## 数据刷新视图中的列

“数据刷新”视图会为每次刷新操作显示以下信息：

- **对象**：正在刷新的模型对象名称（表、分区或模型）
- **说明**：关于刷新操作及其当前状态的更多信息
- **进度**：显示截至目前已导入的行数。
- **开始时间**：刷新操作开始时的日期和时间。 这有助于跟踪操作的发起时间，尤其是在多个刷新任务排队等待时
- **持续时间**：从刷新操作开始到现在的已用时间；对正在运行的操作会实时更新

### 对刷新操作排序

可点击任意列标题，对刷新操作进行排序。 这在以下场景中特别有用：

- 点击 **开始时间** 列，可按时间顺序对刷新操作排序：最新的操作显示在最前（降序）或最后（升序）
- 按 **持续时间** 排序，以识别运行时间较长的操作
- 按 **对象** 排序，按表或分区名称对刷新进行分组

单击列标题一次按升序排序，再单击一次则按降序排序。 在处理多个刷新队列时，这能让你轻松识别最新的刷新操作。

> [!NOTE]
> “数据刷新”窗口中显示的所有信息和持续时间仅为估算值。 在处理过程中，Tabular Editor 会监听来自 SSAS 的[跟踪事件](https://learn.microsoft.com/en-us/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions)。 SSAS 不保证会将所有跟踪信息发送到客户端（例如，在 CPU/内存消耗达到峰值时，可能会对跟踪事件通知进行限流）。

> [!TIP]
> 如果你需要关于刷新进度和持续时间的准确且可靠的信息，你可以将 [SQL Server Profiler](https://learn.microsoft.com/en-us/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) 连接到你的 SSAS 实例，并在处理期间手动收集相关信息。