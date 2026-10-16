---
uid: installation-activation-basic
title: 高级安装与激活
author: Morten Lønskov
updated: 2026-10-14
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

# 高级安装与激活

## 概览

本页介绍 Tabular Editor 3 的高级安装和激活场景：手动（离线）激活、基于注册表的许可证管理、静默部署，以及企业版席位管理。

如需了解标准激活流程，请参阅 @getting-started。

## 手动激活（无网络连接）

如果您无法访问互联网(例如受代理限制)，Tabular Editor 会提示您进行手动激活。

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

输入邮箱后，会弹出一个对话框，其中包含指向激活密钥的链接。复制该 URL，并在可连接到互联网的 Web 浏览器中打开。

该 URL 会返回一个 JSON 对象：

![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

复制完整的 JSON 对象，并将其粘贴到对话框中。完成后，手动激活对话框应如下方截图所示。

![已填写的手动激活](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

随后将验证您的 Tabular Editor 3 许可证。

## 更换企业版席位

要更换企业版席位，必须先通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 将现有用户从该席位取消注册。要管理许可证席位，订阅所有者或许可证管理员需要创建一个账户，或使用现有账户登录。

> [!NOTE]
> 仅企业版支持更换用户。

## 注册表详细信息

Tabular Editor 3 会在 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` 下为每个 Windows 用户保存激活详细信息。

| 值                  | 类型          | 内容                                                                   |
| ------------------ | ----------- | -------------------------------------------------------------------- |
| `LicenseKey`       | `REG_SZ`    | 许可证密钥                                                                |
| `User`             | `REG_SZ`    | 多用户许可证的授权用户电子邮件地址                                                    |
| `ActivationKey`    | `REG_SZ`    | 许可服务返回的激活信息                                                          |
| `Activation`       | `REG_SZ`    | 由旧版 Tabular Editor 3 写入的激活信息。 Tabular Editor 3 会在下次存储激活信息时将其删除       |
| `InstallationDate` | `REG_QWORD` | 此 Windows 用户首次启动 Tabular Editor 3 的时间。如果缺失，Tabular Editor 3 会在启动时创建它 |

若要查看当前 Windows 用户的许可证密钥，请在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

你也可以使用 `regedit.exe`（Windows 注册表编辑器），导航到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` 以查看和修改这些值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

系统管理员还可以通过在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下设置 **LicenseKey** 和 **User** 值，提前为计算机分配 Tabular Editor 3 许可证。完整部署过程见 [静默安装和许可证预配](#silent-installation-and-license-pre-provisioning)。

## 在注册表中更改许可证密钥

在 **帮助 > 关于 Tabular Editor** 中，**更改许可证密钥** 选项会删除 `LicenseKey`、`User`、`ActivationKey` 和 `Activation` 值，并在许可服务上停用该安装。仅当未加载任何模型，且许可证已激活或其席位预留已过期时，才会显示该选项。如果未显示该选项 (例如由于激活失败)，请通过注册表编辑器重置许可证：

1. 关闭所有 Tabular Editor 3 实例。
2. 打开 Windows 注册表编辑器（开始 > 运行 > regedit.exe）。
3. 定位到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上方屏幕截图）。
4. 删除 `LicenseKey`、`User`、`ActivationKey` 和 `Activation` 值。保留 `InstallationDate` 值。
5. 关闭注册表编辑器，然后重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符 (开始 > 运行 > cmd.exe) 中运行以下命令。当某个命令的值不存在时，该命令会报告错误，其余命令仍会继续执行：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v User /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v ActivationKey /f
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /v Activation /f
```

下次启动 Tabular Editor 3 时，系统会提示你输入许可证密钥。

> [!NOTE]
> 删除这些注册表值并不会停用该安装；要管理已激活的许可证，请使用 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/)。

## 静默安装与许可证预配置

你可以以静默方式部署 Tabular Editor，并通过 Windows 注册表预先配置许可证。先安装，再写入许可证；许可证必须在应用程序首次启动前就已写入。

### 静默安装

无界面、无需重启：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI 功能        | 在安装程序中显示为        | 说明                                                    | 默认安装                                                           |
| ------------- | ---------------- | ----------------------------------------------------- | -------------------------------------------------------------- |
| `MainFeature` | Tabular Editor 3 | Tabular Editor 3 核心应用程序                               | 是（必需）                                                          |
| `AIAssistant` | AI 功能            | @ai-assistant 和 @mcp-server | 是，自 3.27.0 起。较早版本仅在选中该组件时才会安装它 |

> [!IMPORTANT]
> 从 3.27.0 开始，除非排除该组件，否则全新安装将包含 **AI 功能** 组件。如果贵组织不允许使用 AI Assistant 或 MCP 服务器，请排除此组件，并按下文所述设置 `DisableAi` 策略。

### 部署时不包含 AI 功能

如需安装不含 AI 功能的 Tabular Editor 3，请在 `ADDLOCAL` 中省略 `AIAssistant`：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

对于已安装该组件的计算机，可在运行该组件时使用 `REMOVE` 将其移除：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

如果未安装该组件，则安装目录中不会包含 AI 程序集，应用程序中也不会显示 **AI Assistant** 窗格和 MCP 服务器，并且不会向模型提供程序发送任何请求。其他功能不受影响。

如需更改单台设备上的选择，请再次运行安装程序，并在维护对话框中选择 **修改**。

> [!NOTE]
> 使用 `ADDLOCAL` 时，除了任何可选功能外，也必须包含 `MainFeature`。如果仅指定 `AIAssistant` 而不包含 `MainFeature`，将导致安装不完整。

### 升级与 AI 功能组件

在现有安装上安装同一组件的较新版本时，安装程序会保留该计算机当前的功能选择。这同样适用于交互式安装和静默安装。在 3.27.0 之前部署且不含 AI 功能的计算机，升级后仍然不含这些功能；已选择 AI 功能的计算机则会保留这些功能。

在以下情况下，安装程序会应用默认选择或命令行中的选择：

| 情况                                                                                    | 结果                                                                                           |
| ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 命令行设置了 `ADDLOCAL`、`REMOVE` 或其他功能属性                                                    | 命令行决定所选内容。 `ADDLOCAL=MainFeature` 会从已安装 AI 功能的计算机中移除这些功能，而 `ADDLOCAL=ALL` 会在未安装这些功能的计算机上安装它们 |
| 部署会先卸载旧版本，再安装新版本，例如将 Intune 的 supersedence 设置为“卸载”                                    | 该安装会被视为全新安装，除非命令行将其排除，否则会包含 AI 功能                                                            |
| 该组件针对的运行时与已安装的组件不同，例如在已安装 .NET 8 组件的计算机上部署 .NET 10 组件 | .NET 8 和 .NET 10 组件是两个独立的产品。如果是全新安装，则默认包含 AI 功能，除非通过命令行将其排除  |

无论哪种情况，`DisableAi` 策略都会覆盖该选择。

### 通过 `DisableAi` 策略强制执行此决定

运行安装程序的用户会使用默认选择，其中包含 AI 功能。要让这台计算机上的每次安装都关闭 AI 功能，请在 `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` 下将 `DisableAi` @policies 设为 `1`。 Tabular Editor 3 会在启动时读取该策略，并禁用 AI 助手和 MCP 服务器。

从 3.27.0 开始，安装程序也会读取该策略：

- 全新安装不会安装 AI 功能组件，安装程序也不会显示它
- 升级会从已安装该组件的计算机上移除它
- 现有安装会保留 AI 文件，直到下一次升级。在启用该策略期间，Tabular Editor 3 不会加载它们

以本地系统账户运行的部署工具不会读取这台计算机上用户的 `HKEY_CURRENT_USER` 策略。静默部署时，把策略设在 `HKEY_LOCAL_MACHINE` 下，这样安装程序就能读取该策略。

### 组件名称和其他 MSI 选项

你也可以使用 `/package` 替代 `/i`。将 `<version>` 替换为实际的版本字符串。

MSI 组件的命名格式为 `TabularEditor.<version>`.<architecture>.<runtime>.msi`，例如 `TabularEditor.3.27.0.x64.Net10.msi`或`TabularEditor.3.27.0.ARM64.Net8.msi\`。选择适合目标计算机的体系结构和运行时；参见 @system-requirements。 MSI 不会安装 .NET Desktop Runtime，所以先部署它。

可用的 MSI 命令行选项详见 Microsoft 官方文档：
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### 预先配置许可证

在应用程序 _首次启动之前_ 将许可证写入注册表：

```bat
REM Per-user license key (HKCU)
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
```

如果使用的是**企业版**许可证密钥，还需要设置授权用户的电子邮件地址：

```bat
REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
```

**注意事项**

- 安装程序不接受许可证参数；许可通过上述注册表项进行处理。
- 许可证密钥存储在 **HKCU** 下（按用户）。确保这些命令在目标用户的上下文中运行（例如通过登录脚本），这样这些值才会写入正确的用户配置文件。
- 如需其他键和值，请参阅 [注册表详细信息](#registry-details)。

