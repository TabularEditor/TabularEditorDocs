---
uid: policies
title: Policies
author: Daniel Otykier
updated: 2022-08-11
---

# Policies

Some IT organisations may wish to limit certain features of Tabular Editor. This is possibly through the use of group policies.

Below is a listing of the policies that can be controlled.

**Registry key:** Software\Policies\Kapacity\Tabular Editor\

|Value|Description|
|--|--|
| DisableUpdates | When this is set to any value except 0, Tabular Editor will not check if newer versions are available online. Moreover, users cannot manually check if new updates are available through the tool. |
| DisableCSharpScripts | When this is set to any value except 0, Tabular Editor will not let users create and execute C# scripts. |
| DisableMacros | When this is set to any value except 0, Tabular Editor will not let users save or run macros (aka. "Custom actions"). Moreover, macros defined in the %LocalAppData% folder will not be loaded and compiled upon application startup. |
| DisableBpaDownload | When this is set to any value except 0, Tabular Editor will not allow Best Practice Analyzer rules to be downloaded from the web. |
| DisableWebDaxFormatter | When this is set to any value except 0, Tabular Editor will disable the DAX code formatter, which performs a webrequest to daxformatter.com. |