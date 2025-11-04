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

![No such host is known-error](~/content/assets/images/troubleshooting/proxy-error.png)

Typical error messages you would see, are:

**Title:** `Could not connect to server`

**Message:**

- `No such host is known. (login.microsoftonline.com:443)`
- `Unable to obtain authentication token using the credentials provided`
- `The requested address is not valid in its context. (login.microsoftonline.com:443)`

When this happens, the first thing you should try is to change the proxy settings in Tabular Editor 3. You can find these settings under **Tools > Preferences > Proxy Settings**:

![Proxy settings in Tabular Editor 3](~/content/assets/images/troubleshooting/proxy-settings.png)

In most cases, changing the **Proxy Type** from `None` to `System` will resolve the issue. This setting tells Tabular Editor 3 to use the system-wide proxy settings configured in Windows. If you are still experiencing issues, you can try setting the **Proxy Type** to `Custom` and enter the proxy server address and port manually.

> [!IMPORTANT]
> After changing the proxy settings, you must restart Tabular Editor 3 for the changes to take effect.

# .NET Core vs. .NET Framework proxy handling

If the suggestion above does not solve the problem, starting with version 3.21.0 of Tabular Editor, you can try the following alternative solution:

> [!NOTE]
> The solutions outlined below require Tabular Editor 3.21.0 or newer, because the AS configuration options are only available in the AMO/TOM client library v. [19.94.1.1](https://www.nuget.org/packages/Microsoft.AnalysisServices/19.94.1.1). Previous versions of Tabular Editor 3 use an older version of this client library, which ignores these configuration options.

Create a file called <a href="https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/AnalysisServices.AppSettings.json" download="AnalysisServices.AppSettings.json">**AnalysisServices.AppSettings.json**</a> and put it in the installation folder for Tabular Editor 3 (i.e. the same folder that TabularEditor3.exe resides in). Add the following content to the file:

```json
{
  "asConfiguration": {
    "authentication": {
      "msalConnectivityMode": "external"
    }
  }
}
```

To turn on external MSAL proxy support for all .NET core applications on your machine, you can also set the following environment variable rather than using the AppSettings file as described above:

| Environment variable name | Environment variable value |
| --- | --- |
| MS_AS_MsalConnectivityMode | 1 |

# Enabling diagnostics

If you're still not able to connect after attempting the solutions outlined above, it may help to turn on advanced diagnostics logging. You can do that, either by modifying the **AnalysisServices.AppSettings.json** file to look like the following:

```json
{
  "asConfiguration": {
    "authentication": {
      "msalConnectivityMode": "external"
    },
    "diagnostics": {
      "authenticationTrace": {
        "isEnabled": true,
        "traceLevel": 4,
        "fileName": "<path to trace file>"
      }
    }
  }
}
```

or if using Environment Variables, by setting the following:

| Environment variable name | Environment variable value |
| --- | --- |
| MS_AS_AADAUTHENTICATOR_LOG | 1 |
| MS_AS_AADAUTHENTICATOR_LOGLEVEL | 4 |
| MS_AS_AADAUTHENTICATOR_LOGFILE | \<path to trace file\> |

`<path to trace file>` must point to a file in a directory that exists. I.e. if you want the file to be written to `c:\temp\logs\as-auth.log`, you must ensure that the directory `c:\temp\logs` exists.

The contents of this trace file is useful when contacting Microsoft support.

> [!IMPORTANT]
> You must restart Tabular Editor 3 after making changes to the **AnalysisServices.AppSettings.json** file, or after modifying environment variables.