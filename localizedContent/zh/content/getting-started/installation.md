---
uid: installation-activation-basic
title: 安装、激活与基础配置
author: Morten Lønskov
updated: 2021-09-30
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

## 概述

本页介绍 Tabular Editor 3 的高级安装和激活场景：手动（离线）激活、基于注册表的许可证管理、静默部署，以及企业版席位管理。

如需了解标准激活流程，请参阅 @getting-started。

<a name="manual-activation-no-internet"></a>

## 手动激活（无网络）

如果你无法访问互联网，例如由于代理，Tabular Editor 会提示你进行手动激活。

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

输入邮箱后，会弹出一个对话框，其中包含指向激活密钥的链接。
复制该 URL，并在已连接互联网的网页浏览器中打开。 复制该 URL，并在可连接到互联网的 Web 浏览器中打开。

该 URL 会返回一个 JSON 对象：

![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

复制返回的完整 JSON 对象，并将其粘贴到对话框中。
你的手动激活对话框最后会像下面这样。 完成后，手动激活对话框应如下方截图所示。

![已填写的手动激活](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

这样即可验证你的 Tabular Editor 3 许可证。

## 更换企业版席位

要更换企业版席位，必须先通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 将现有用户从该席位取消注册。 要管理许可证席位，订阅所有者或许可证管理员需要创建一个账户，或使用现有账户登录。

> [!NOTE]
> 仅企业版支持更换用户。

<a name="registry-details"></a>

## 注册表详细信息

Tabular Editor 3 使用 Windows 注册表存储激活信息。

在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令，即可查看当前分配给这台计算机的许可证密钥：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

您也可以使用 `regedit.exe`（Windows 注册表编辑器），前往 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，查看并修改 **LicenseKey** 和 **User** 值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

系统管理员还可以通过在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下设置 **LicenseKey** 和 **User** 值，提前为计算机分配 Tabular Editor 3 许可证。 完整部署过程见 [静默安装和许可证预配](#silent-installation-and-license-pre-provisioning)。

## 更改许可证密钥

如果由于某种原因，你无法在 **关于 Tabular Editor** 对话框中使用标准的 **更改许可证密钥** 选项，请通过注册表编辑器重置许可证：

1. 关闭所有正在运行的 Tabular Editor 3 实例。
2. 在 Windows 中打开注册表编辑器（开始 > 运行 > regedit.msc）。
3. 定位到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上方屏幕截图）。
4. 删除该项下的所有值。
5. 关闭注册表编辑器，然后重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符中运行以下命令（开始 > 运行 > cmd.exe）：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

购买 Tabular Editor 3 的许可证后，你会收到一封电子邮件，其中包含一段 25 个字符的字符串，这就是你的许可证密钥。 出现提示时，输入许可证密钥并点击“下一步 >”以激活产品。

## 静默安装与许可证预配置

你可以以静默方式部署 Tabular Editor，并通过 Windows 注册表预先配置许可证。

1. **静默安装**（无界面、无需重启）：

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

   要包含 **AI Assistant** 功能，请在 `ADDLOCAL` 属性中指定它。 AI Assistant 默认不会安装。

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart ADDLOCAL=MainFeature,AIAssistant /l*v C:\Temp\TE3_install.log
   ```

   | MSI 功能        | 说明                                 | 默认安装  |
   | ------------- | ---------------------------------- | ----- |
   | `MainFeature` | Tabular Editor 3 核心应用程序            | 是（必需） |
   | `AIAssistant` | 用于 Tabular Editor 3 的 AI Assistant | 否     |

   > [!NOTE]> 使用 `ADDLOCAL` 时，除任何可选功能外，还必须包含 `MainFeature`。 如果仅指定 `AIAssistant` 而不包含 `MainFeature`，将导致安装不完整。

你也可以使用 `/package` 替代 `/i`。 将 `<version>` 替换为实际的版本字符串。 如适用，请使用 ARM64 版 MSI。

可用的 MSI 命令行选项详见 Microsoft 官方文档：
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. 在应用程序**首次启动前**，**将许可证写入注册表**：

   ```bat
   REM 每用户许可证密钥 (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   如果使用的是**企业版**许可证密钥，还需要设置授权用户的电子邮件地址：

   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**注意事项**

- 安装程序不接受许可证参数；许可通过上述注册表项进行处理。
- 许可证密钥存储在 **HKCU** 下（按用户）。 确保这些命令在目标用户的上下文中运行（例如通过登录脚本），这样这些值才会写入正确的用户配置文件。
- 如需其他键和值，请参阅 [注册表详细信息](#registry-details)。

