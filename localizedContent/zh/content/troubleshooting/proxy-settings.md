---
uid: proxy-settings
title: 代理设置
author: Daniel Otykier
updated: 2026-11-13
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 代理设置

由于 .NET Core (Tabular Editor 3 使用) 与 .NET Framework (Tabular Editor 2 和 DAX Studio 使用) 在代理处理方式上不同，当你在代理服务器后使用 Tabular Editor 3 时，可能会在连接外部服务（例如 Power BI 服务）时遇到问题。

例如，在尝试连接到 Power BI 服务时，你可能会看到以下错误信息：

![“No such host is known” 错误](~/content/assets/images/troubleshooting/proxy-error.png)

你可能会看到的典型错误信息包括：

**标题：** `Could not connect to server`

**信息：**

- `No such host is known. (login.microsoftonline.com:443)`
- `Unable to obtain authentication token using the credentials provided`
- `The requested address is not valid in its context. (login.microsoftonline.com:443)`

发生这种情况时，您首先应尝试更改 Tabular Editor 3 中的代理设置。你可以在**工具 > 首选项 > Tabular Editor > 代理设置**下找到这些设置：

![Tabular Editor 3 中的代理设置](~/content/assets/images/troubleshooting/proxy-settings.png)

在大多数情况下，把 **代理类型** 从 `None` 改成 `System` 就能解决这个问题。这个设置会让 Tabular Editor 3 使用 Windows 中配置的系统级代理设置。如果问题仍然存在，你可以尝试把 **代理类型** 设为 `Custom`，然后手动输入代理服务器地址和端口。

如果自定义代理需要用户名和密码，请取消选中**使用默认凭据**，然后在**用户名**和**密码**中输入用户名和密码。如果具有用户名和密码的自定义代理无法通过身份验证，请在**工具 > 首选项 > Tabular Editor > 代理设置**下再次输入密码，然后点击**确定**。

> [!IMPORTANT]
> 更改代理设置后，你必须重新启动 Tabular Editor 3，更改才会生效。

# .NET Core 与 .NET Framework 的代理处理差异

如果上述建议无法解决问题，您可以尝试以下替代解决方案：

创建一个名为 <a href="https://raw.githubusercontent.com/TabularEditor/TabularEditorDocs/main/content/assets/file-types/AnalysisServices.AppSettings.json" download="AnalysisServices.AppSettings.json">**AnalysisServices.AppSettings.json**</a> 的文件，并将其放入 Tabular Editor 3 的安装目录（即 TabularEditor3.exe 所在的同一目录）。将以下内容添加到该文件中：

```json
{
  "asConfiguration": {
    "authentication": {
      "msalConnectivityMode": "external"
    }
  }
}
```

如果你想为本机上的所有 .NET Core 应用启用外部 MSAL 代理支持，也可以通过设置以下环境变量来实现，而无需像上面那样使用 AppSettings 文件：

| 环境变量名称                                                               | 环境变量值 |
| -------------------------------------------------------------------- | ----- |
| MS_AS_MsalConnectivityMode | 1     |

# 启用诊断

如果尝试了上述解决方案后仍无法连接，开启高级诊断日志可能会有所帮助。你可以修改 **AnalysisServices.AppSettings.json** 文件，将其内容调整为如下所示：

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

或者，如果使用环境变量，则设置以下内容：

| 环境变量名称                                                                                         | 环境变量值                                             |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| MS_AS_AADAUTHENTICATOR_LOG      | 1                                                 |
| MS_AS_AADAUTHENTICATOR_LOGLEVEL | 4                                                 |
| MS_AS_AADAUTHENTICATOR_LOGFILE  | \<path to trace file\> |

`<path to trace file>` 必须指向现有目录中的某个文件。也就是。也就是说，如果你希望将文件写入 `c:\temp\logs\as-auth.log`，则必须确保目录 `c:\temp\logs` 已存在。

在联系 Microsoft 支持时，此跟踪文件的内容很有用。

> [!IMPORTANT]
> 更改 **AnalysisServices.AppSettings.json** 文件或修改环境变量后，你必须重启 Tabular Editor 3。