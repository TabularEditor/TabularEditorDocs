---
uid: policies
title: Policies
author: Daniel Otykier
updated: 2022-08-11
---

# Policies

Some IT organisations may wish to limit certain features of Tabular Editor. This is possible through the use of group policies, by setting certain values in the Windows registry.

> [!NOTE]
> This functionality requires the following versions of Tabular Editor:
>
>   - Tabular Editor 2 version [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) or newer
>   - Tabular Editor 3 version [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) or newer.

Below is a listing of the policies that can be controlled. To enforce one or more of these policies, add a non-zero DWORD value to the registry key. The name of the value specifies which policy to enforce.

**Registry key:** Software\Policies\Kapacity\Tabular Editor\

|Value|Description|
|--|--|
| DisableUpdates | When this is set to any value except 0, Tabular Editor will not check if newer versions are available online. Moreover, users cannot manually check if new updates are available through the tool. |
| DisableCSharpScripts | When this is set to any value except 0, Tabular Editor will not let users create and execute C# scripts. |
| DisableMacros | When this is set to any value except 0, Tabular Editor will not let users save or run macros (aka. "Custom actions"). Moreover, macros defined in the %LocalAppData% folder will not be loaded and compiled upon application startup. |
| DisableBpaDownload | When this is set to any value except 0, Tabular Editor will not allow Best Practice Analyzer rules to be downloaded from the web. |
| DisableWebDaxFormatter | When this is set to any value except 0, Tabular Editor will disable the DAX code formatter, which performs a webrequest to daxformatter.com. |

## Disabling web communications

If you want to ensure that Tabular Editor does not perform web requests, specify the `DisableUpdates`, `DisableBpaDownload` and `DisableWebDaxFormatter` policies.

## Disabling custom scripts

If you want to ensure that Tabular Editor does not allow users to execute arbitrary code, specify the `DisableCSharpScripts` and `DisableMacros` policies.
