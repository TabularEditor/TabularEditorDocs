---
uid: installation-activation-basic
title: 高级安装和激活
author: Morten Lønskov
updated: 2026-10-23
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

# 高级安装和激活

## 概述

本页介绍了 Tabular Editor 3 的高级安装和激活场景：手动（离线）激活、基于注册表的许可证管理、静默部署和企业席位管理。

有关标准激活流程，请参阅@getting-started。

## 手动激活（无互联网）

如果您无法访问互联网（例如由于代理原因），Tabular Editor 会提示您进行手动激活。

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

输入您的电子邮件后，将出现一个包含激活密钥链接的对话框。复制该 URL，然后在已连接到互联网的 Web 浏览器中打开。

该 URL 返回一个 JSON 对象：

![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

复制完整的 JSON 对象并将其粘贴到对话框中。您的手动激活对话框最终将显示如下面的屏幕截图所示。

![已填写的手动激活](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

然后，您的 Tabular Editor 3 许可证将得到验证。

## 更改企业版的用户席位

要更改企业版席位，请通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/)取消该席位上现有用户的注册。订阅所有者或许可证管理员创建账户或使用现有账户登录，以管理许可证席位。

> [!NOTE]
> 仅在企业版中可以更改用户。

## 注册表详细信息

Tabular Editor 3 将每位 Windows 用户的激活详细信息存储在 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` 下。

| 值 | 类型 | 内容 |
|-------|------|---------|
| `LicenseKey` | `REG_SZ` | 许可证密钥 |
| `User` | `REG_SZ` | 许可证用户的电子邮件地址，适用于多用户许可证 |
| `ActivationKey` | `REG_SZ` | 许可服务返回的激活 |
| `Activation` | `REG_SZ` | 由旧版本 Tabular Editor 3 写入的激活。Tabular Editor 3 在下次存储激活时会将其删除 |
| `InstallationDate` | `REG_QWORD` | 此 Windows 用户首次启动 Tabular Editor 3 的时间。如果该项缺失，Tabular Editor 3 会在启动时创建它 |

要查看活动 Windows 用户的当前许可证密钥，请在 Windows 命令提示符（“开始”>“运行”>“cmd.exe”）中运行以下命令：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

您还可以使用 `regedit.exe`（Windows 注册表编辑器）并导航到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，以查看和修改值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

系统管理员还可以通过在每位用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下指定 **LicenseKey** 和 **User** 值，主动将 Tabular Editor 3 许可证分配给某台计算机。请参阅[静默安装和许可证预配置](#silent-installation-and-license-pre-provisioning)，了解完整的部署程序。

## 通过注册表更改许可证密钥

**帮助 > 关于 Tabular Editor** 中的**更改许可证密钥**选项将删除 `LicenseKey`、`User`、`ActivationKey` 和 `Activation` 值，并在许可服务上停用安装。此选项仅在未加载模型且许可证已激活或其席位预留已过期时才会显示。如果未显示（例如，由于激活失败），请通过注册表编辑器重置许可证：

1. 关闭所有 Tabular Editor 3 实例。
2. 在 Windows 中打开注册表编辑器（“开始”>“运行”>“regedit.exe”）。
3. 找到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上图）。
4. 删除 `LicenseKey`、`User`、`ActivationKey` 和 `Activation` 值。保留 `InstallationDate`。
5. 关闭注册表编辑器，然后重启 Tabular Editor 3。

或者，在 Windows 命令提示符（“开始”>“运行”>“cmd.exe”）中运行以下命令。如果命令的值不存在，则该命令会报告错误，但其余命令仍会运行：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

下次启动 Tabular Editor 3 时，系统会提示您输入许可证密钥。

> [!NOTE]
> 删除注册表值不会停用安装，请使用 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 来管理你的已激活许可证。 

## 静默安装和许可证预配置

您可以静默部署 Tabular Editor，并通过 Windows 注册表预先配置许可证。先进行安装，然后写入许可证。许可证必须在首次启动应用程序之前就位。

### 静默安装

无 UI，无需重启：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI 功能 | 在安装程序中显示为 | 描述 | 默认安装 |
|-------------|---------------------------|-------------|----------------------|
| `MainFeature` | Tabular Editor 3 | Tabular Editor 3 核心应用程序 | 是（必需） |
| `AIAssistant` | AI 功能 | @ai-assistant 和 @mcp-server | 是，从 3.27.0 开始。早期版本仅在选择时才会安装它 |

> [!IMPORTANT]
> 从 3.27.0 开始，新安装将包含**AI 功能**组件，除非您将其排除在外。如果您的组织不允许使用 AI 助手或 MCP 服务器，请排除该组件，并按以下说明设置 `DisableAi` 策略。

### 不使用 AI 功能进行部署

将 `AIAssistant` 从 `ADDLOCAL` 中排除，以安装不含 AI 功能的 Tabular Editor 3：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

使用“REMOVE”运行软件包，以从已安装该组件的计算机中将其移除：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

如果没有该组件，AI 程序集将不会位于安装文件夹中，**AI 助手**窗格和 MCP 服务器将不会出现在应用程序中，并且不会有任何请求发送到模型提供商。其他功能不受影响。

要更改单台计算机上的选择，请再次运行安装程序，然后在维护对话框中选择“修改”。

> [!NOTE]
> 使用 `ADDLOCAL` 时，请将 `MainFeature` 与任何可选功能一起列出。仅指定 `AIAssistant` 而不指定 `MainFeature` 将导致安装不完整。

### 升级和 AI 功能组件

当您在现有安装之上安装同一软件包的较新版本时，安装程序会保留该计算机已有的功能选择。这适用于交互式安装和静默安装。在 3.27.0 之前部署的未包含 AI 功能的计算机在升级后仍不包含这些功能，而选择了 AI 功能的计算机则会保留这些功能。

在这些情况下，安装程序将应用默认选择或命令行上的选择：

| 情况 | 结果 |
|--|--|
| 命令行设置 `ADDLOCAL`、`REMOVE` 或其他功能属性 | 命令行设置选择。`ADDLOCAL=MainFeature` 会从已安装 AI 功能的计算机上移除这些功能，而 `ADDLOCAL=ALL` 会在未安装这些功能的计算机上安装它们 |
| 部署在安装新版本之前卸载旧版本，例如设置为卸载的 Intune 替代 | 安装是新安装，并且包含 AI 功能，除非命令行将其排除在外 |

`DisableAi` 策略在所有情况下都会覆盖所选内容。

### 在 .NET 8 和 .NET 10 包之间切换

.NET 8 和 .NET 10 包相互替换。当您在已安装相同或更早版本的另一个版本的计算机上安装其中一个版本时，安装程序会在安装任何文件之前先卸载另一个版本，并保留该版本的Feature选择。如果一台计算机上安装了这两个版本，则在下一次安装后将只保留一个安装，并且**设置 > 应用 > 已安装的应用**中将列出一个**Tabular Editor 3**。

如果安装的另一个版本是较新版本，则安装将停止，并显示一条消息。请先卸载较新版本，然后再次运行安装程序。

### 使用 DisableAi 策略强制执行决定

运行安装程序的用户将获得默认选择，其中包含 AI 功能。将 `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` 下的 `DisableAi` @policies 设置为 `1`，以在计算机上的每次安装中都禁用 AI 功能。Tabular Editor 3 在启动时读取该策略，并关闭 AI 助手和 MCP 服务器。

从 3.27.0 版本开始，安装程序也会读取该策略：

- 新安装将省略 AI 功能组件，安装程序不会显示该组件
- 升级将从已安装该组件的计算机中将其删除
- 现有安装将保留 AI 文件，直至下一次升级。在设置策略时，Tabular Editor 3 不会加载它们。

以本地系统账户运行的部署工具不会读取计算机用户的 `HKEY_CURRENT_USER` 策略。在“HKEY_LOCAL_MACHINE”下设置策略，以便安装程序在静默部署中读取该策略。

### 组件名称和其他 MSI 选项

您还可以使用 `/package` 代替 `/i`。将“<version>”替换为实际的版本字符串。

MSI 包的命名方式为“TabularEditor.<version>.<architecture>.<runtime>.msi”，例如“TabularEditor.3.27.0.x64.Net10.msi”或“TabularEditor.3.27.0.ARM64.Net8.msi”。选择适合目标计算机的架构和运行时；请参阅@system-requirements。MSI 不会安装 .NET Desktop Runtime，因此请先部署该运行时。

有关可用 MSI 命令行选项的详细信息，请参阅 Microsoft 官方文档：
[Microsoft Standard Installer 命令行选项 - Win32 应用 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### 预先配置许可证

在应用程序*首次启动之前*，将许可证写入注册表：

```bat
REM Per-user license key (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

如果您使用的是**企业版**许可证密钥，还请设置持证用户的电子邮箱：

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**备注**

- 安装程序不接受许可证参数；许可通过上述注册表项处理。
- 密钥存储在 **HKCU**（每个用户）下。确保命令在目标用户的上下文中运行（例如通过登录脚本），以便将值写入正确的配置文件。
- 有关其他键和值，请参阅[注册表详细信息](#registry-details)。

