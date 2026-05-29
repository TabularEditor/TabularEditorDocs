---
uid: installation-activation-basic
title: 高级安装与激活
author: Morten Lønskov
updated: 2026-05-19
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

有关标准的激活流程，请参阅 @getting-started。

<a name="manual-activation-no-internet"></a>

## 手动激活（无网络）

如果你无法访问互联网，例如由于代理限制，Tabular Editor 会提示你进行手动激活。

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

输入电子邮件地址后，会弹出一个对话框，其中包含指向激活密钥的链接。 复制该 URL，并在可连接互联网的 Web 浏览器中打开它。

该 URL 会返回一个 JSON 对象：

![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

复制完整的 JSON 对象，并将其粘贴到对话框中。 完成后，手动激活对话框会像下图这样。

![已填写的手动激活信息](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

随后会验证你的 Tabular Editor 3 许可证。

## 更换企业版席位

要更换企业版席位，先通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 取消该席位上现有用户的注册。 订阅所有者或许可证管理员可以创建账户，或使用现有账户登录，以管理许可证席位。

> [!NOTE]
> 仅企业版支持更换用户。

<a name="registry-details"></a>

## 注册表详细信息

Tabular Editor 3 使用 Windows 注册表存储激活信息。

要查看当前分配给这台计算机的许可证密钥，可在 Windows 命令提示符中运行以下命令（开始 > 运行 > cmd.exe）：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

你也可以使用 `regedit.exe`（Windows 注册表编辑器），并导航到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，以查看和修改 **LicenseKey** 和 **User** 的值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

系统管理员还可以在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下指定 **LicenseKey** 和 **User** 值，从而提前为计算机分配 Tabular Editor 3 许可证。 完整部署流程请参阅 [静默安装和许可证预配](#silent-installation-and-license-pre-provisioning)。

## 通过注册表更改许可证密钥

如果由于某种原因，你无法通过 **关于 Tabular Editor** 对话框中的标准 **更改许可证密钥** 选项修改许可证密钥，请通过注册表编辑器重置许可证：

1. 关闭所有正在运行的 Tabular Editor 3 实例。
2. 在 Windows 中打开注册表编辑器（开始 > 运行 > regedit.msc）。
3. 找到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上方屏幕截图）。
4. 删除此注册表项中的所有值。
5. 关闭注册表编辑器并重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符中运行以下命令（开始 > 运行 > cmd.exe）：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

下次启动 Tabular Editor 3 时，系统会提示你输入许可证密钥，就像该工具首次安装到这台计算机上时一样。

## 静默安装和许可证预配

你可以静默部署 Tabular Editor，并通过 Windows 注册表预配许可证。

1. **静默安装**（无界面，无需重启）：

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

   要包含 **AI Assistant** 功能，请在 `ADDLOCAL` 属性中指定它。 默认不会安装 AI Assistant。

   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart ADDLOCAL=MainFeature,AIAssistant /l*v C:\Temp\TE3_install.log
   ```

   | MSI 功能        | 说明                       | 默认安装  |
   | ------------- | ------------------------ | ----- |
   | `MainFeature` | Tabular Editor 3 核心应用程序  | 是（必填） |
   | `AIAssistant` | Tabular Editor 3 的 AI 助手 | 否     |

   > [!NOTE]> 使用 `ADDLOCAL` 时，除可选功能外，还必须同时包含 `MainFeature`。 如果仅指定 `AIAssistant` 而不指定 `MainFeature`，将导致安装不完整。

你也可以使用 `/package` 替代 `/i`。 将 `<version>` 替换为实际版本字符串。 如适用，请使用 ARM64 MSI。

有关可用 MSI 命令行选项的详细信息，参见 Microsoft 官方文档：
[Microsoft Standard Installer 命令行选项 - Win32 应用 | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **在首次启动应用程序之前**，**将许可证写入注册表**：

   ```bat
   REM Per-user license key (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   如果你使用的是 **企业版** 许可证密钥，还需要设置授权用户的电子邮件地址：

   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**说明**

- 安装程序不接受许可证参数；授权通过上述注册表项完成。
- 这些键存储在 **HKCU** 下（按用户）。 确保以目标用户的身份运行这些命令（例如通过登录脚本），这样这些值会写入正确的用户配置文件。
- 有关其他键和值，请参阅 [注册表详细信息](#registry-details)。

