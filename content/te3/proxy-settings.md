---
uid: proxy-settings
title: Proxy settings
author: Daniel Otykier
updated: 2024-11-07
applies_to:
  editions:
    - edition: Desktop
    - edition: Business
    - edition: Enterprise
---

# Proxy settings

Due to different proxy behavior between .NET Core (used by Tabular Editor 3) and .NET Framework (used by Tabular Editor 2 and DAX Studio), you may experience issues with connecting to external services, such as the Power BI service, when using Tabular Editor 3 behind a proxy server.

For example, you might see the following error message when trying to connect to the Power BI service:

![No such host is known-error](~/content/assets/images/proxy-error.png)

**Title:** Could not connect to server<br/>
**Message:** No such host is known. (login.microsoftonline.com:443)

When this happens, the first thing you should try is to change the proxy settings in Tabular Editor 3. You can find these settings under **Tools > Preferences > Proxy Settings**:

![Proxy settings in Tabular Editor 3](~/content/assets/images/proxy-settings.png)

In most cases, changing the **Proxy Type** from `None` to `System` will resolve the issue. This setting tells Tabular Editor 3 to use the system-wide proxy settings configured in Windows. If you are still experiencing issues, you can try setting the **Proxy Type** to `Custom` and enter the proxy server address and port manually.

> [!IMPORTANT]
> After changing the proxy settings, you mustrestart Tabular Editor 3 for the changes to take effect.