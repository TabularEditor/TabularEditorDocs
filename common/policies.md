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

|Value|When enforced...|
|--|--|
| DisableUpdates | Tabular Editor will not check if newer versions are available online. Moreover, users cannot manually check if new updates are available through the tool. |
| DisableCSharpScripts | Tabular Editor will not let users create and execute C# scripts. |
| DisableMacros | Tabular Editor will not let users save or run macros. Moreover, macros defined in the %LocalAppData% folder will not be loaded and compiled upon application startup. |
| DisableBpaDownload | Tabular Editor will not allow Best Practice Analyzer rules to be downloaded from the web. |
| DisableWebDaxFormatter | Tabular Editor will disable the DAX code formatter, which performs a webrequest to daxformatter.com. |
| DisableErrorReports | **(TE3 Only)** Tabular Editor will not allow users to send error/crash reports to the Tabular Editor 3 support team. |
| DisableTelemetry | **(TE3 Only)** Tabular Editor will not collect and send anonymous usage data to the Tabular Editor 3 support team. |

## Disabling web communications

If you want to ensure that Tabular Editor does not perform web requests, specify the `DisableUpdates`, `DisableBpaDownload`, `DisableWebDaxFormatter`, `DisableErrorReports` and `DisableTelemetry` policies.

## Disabling custom scripts

If you want to ensure that Tabular Editor does not allow users to execute arbitrary code, specify the `DisableCSharpScripts` and `DisableMacros` policies.
