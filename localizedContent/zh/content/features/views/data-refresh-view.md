---
uid: data-refresh-view
title: 数据刷新视图
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
# 数据刷新视图

**数据刷新**视图显示服务器上刷新操作的进度。您从 TOM Explorer 开始的刷新将在此视图中显示为活动刷新。

<figure style="padding-top: 15px;">
  <img class="noscale" src="~/content/assets/images/data-refresh-view.png" alt="数据刷新视图" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>图 1：</strong> Tabular Editor 中的“数据刷新”视图。通过右键单击表并选择“刷新”来开始刷新。</figcaption>
</figure>

在您继续编辑模型时，刷新操作在后台运行，如果刷新失败，则会显示错误消息。

## 数据刷新视图列

每个刷新操作都有以下列：

- **对象**：正在刷新的模型对象（表格、分区或模型）。
- **说明**：有关刷新操作及其当前状态的详细信息。
- **进度**：迄今为止已导入的行数。
- **开始时间**：操作开始的日期和时间。
- **持续时间**：自操作开始以来的已过时间，对于正在进行的操作会实时更新。

### 对刷新操作进行排序

点击列标题以按该列排序：点击一次为升序，再次点击为降序。例如：

- 按**开始时间**降序排序，以便首先列出最新的刷新操作
- 按**持续时间**排序，以查找长时间运行的操作
- 按**对象**排序，以按表名或分区名对刷新进行分组

> [!NOTE]
> “数据刷新”窗口中显示的所有消息和持续时间仅为估算值。Tabular Editor 在处理过程中侦听[来自 SSAS 的跟踪事件](https://learn.microsoft.com/analysis-services/trace-events/analysis-services-trace-events?view=asallproducts-allversions)。不能保证 SSAS 会将所有跟踪消息发送给客户端（例如，在 CPU/内存消耗高峰期，它可能会限制跟踪事件通知）。 

> [!TIP]
> 如果您需要有关刷新进度和持续时间的准确可靠信息，应将 [SQL Server Profiler](https://learn.microsoft.com/sql/tools/sql-server-profiler/sql-server-profiler?view=sql-server-ver16) 连接到您的 SSAS 实例，并在处理过程中手动收集信息。
