---
uid: data-refresh-view
title: Data Refresh view
author: Daniel Otykier
updated: 2021-09-08
applies_to:
  editions:
    - edition: Desktop
      partial: TE3 Desktop Edition includes this feature, however refreshing tables through External Tools is not currently supported by Microsoft and may cause issues in Power BI Desktop.
    - edition: Business
    - edition: Enterprise
---
# Data Refresh View
The Data Refresh view allows you to investigate in detail how your data is being refreshed on the server.
A new active refresh will appear when a new refresh is triggered through the TOM Explorer. 


<figure style="padding-top: 15px;">
  <img class="noscale" src="~/assets/images/data-refresh-view.png" alt="Data Refresh View" style="width: 550px;"/>
  <figcaption style="font-size: 12px; padding-top: 10px; padding-bottom: 15px; padding-left: 75px; padding-right: 75px; color:#00766e"><strong>Figure 1:</strong> Data Refresh View in Tabular Editor. New refresh can be started by right-clicking a table and selecting refresh </figcaption>
</figure>

A new refresh will run in the background so that you can continue to build your dataset, and Tabular Editor will let you know if the refresh fails with a pop up. 

> [!WARNING]
> If you are using TE as an External Tool to Power BI and have activated _Allow Unsupported modeling operations_ do *NOT* start a refresh as this is prone to corrupt your .pbix file. 
