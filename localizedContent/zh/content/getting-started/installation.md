---
uid: installation-activation-basic
title: 高级安装与激活
author: Morten Lønskov
updated: 2026-09-15
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

## 概述

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

Tabular Editor 3 使用 Windows 注册表存储激活信息。

在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令，即可查看当前分配给这台计算机的许可证密钥：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

您也可以使用 `regedit.exe`（Windows 注册表编辑器），前往 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，查看并修改 **LicenseKey** 和 **User** 值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

系统管理员还可以通过在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下设置 **LicenseKey** 和 **User** 值，提前为计算机分配 Tabular Editor 3 许可证。完整部署过程见 [静默安装和许可证预配](#silent-installation-and-license-pre-provisioning)。

## 在注册表中更改许可证密钥

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

下次启动 Tabular Editor 3 时，系统会像该工具首次安装在这台电脑上时一样提示你输入许可证密钥。

## 静默安装与许可证预配置

你可以以静默方式部署 Tabular Editor，并通过 Windows 注册表预先配置许可证。先安装，再写入许可证；许可证必须在应用程序首次启动前就已写入。

### 静默安装

无界面、无需重启：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart /l*v C:\Temp\TE3_install.log
```

| MSI 功能        | 在安装程序中显示为        | 说明                                   | 默认安装                                         |
| ------------- | ---------------- | ------------------------------------ | -------------------------------------------- |
| `MainFeature` | Tabular Editor 3 | Tabular Editor 3 核心应用程序              | 是（必需）                                        |
| `AIAssistant` | AI 功能            | @ai-assistant 和 MCP 服务器 | 是，自 3.27.0 起 |

> [!IMPORTANT]
> 上述命令会安装 **AI 功能** 组件。在 3.26.x 及更早版本中，必须手动选中它，默认安装不会包含它；从 3.27.0 起，它已成为默认安装的一部分。如果贵组织不希望在用户计算机上安装 AI Assistant 或 MCP 服务器，则必须按下一节所述进行明确指定。

### 部署时不包含 AI 功能

若要避免将 AI 文件安装到计算机上，请指定需要的功能，并省略 `AIAssistant`：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

若要在已安装该组件的计算机上将其移除，请使用同一个组件并加上 `REMOVE`：

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

无论哪种方式，AI 程序集都不会写入安装文件夹；应用程序中不会出现 **AI Assistant** 窗格和 MCP 服务器；也不会向任何模型提供程序发起连接。 Tabular Editor 3 的其他所有功能都不受影响。

升级现有安装时，会保留该计算机原有的功能选择，因此，如果某台计算机在 3.27.0 之前部署时未包含 AI 功能，升级后也不会自动获得这些功能。对于全新安装，由于没有先前的选择可继承，请传入 `ADDLOCAL=MainFeature`。

> [!IMPORTANT]
> 命令行只控制 _你_ 要部署的内容，而不控制用户能安装什么：AI 功能默认包含在内，因此任何自行运行安装程序的人都会获得这些功能。要让该设置持续生效，还需要同时设置 `DisableAi` @policies。从 3.27.0 起，安装程序会读取该策略，并自动跳过 AI 组件；不管由谁运行、以何种方式运行都是如此。如果该组件已存在，该策略还会在运行时关闭 AI Assistant 和 MCP 服务器。请在整机范围内进行设置，即在 `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` 下设置，这样它会对所有用户生效，并且无法按用户进行覆盖。

> [!NOTE]
> 使用 `ADDLOCAL` 时，除了任何可选功能外，也必须包含 `MainFeature`。如果仅指定 `AIAssistant` 而不包含 `MainFeature`，将导致安装不完整。

### 组件名称和其他 MSI 选项

你也可以使用 `/package` 替代 `/i`。将 `<version>` 替换为实际的版本字符串。

MSI 组件的命名格式为 `TabularEditor.<version>`.<architecture>.<runtime>.msi`，例如 `TabularEditor.3.27.0.x64.Net10.msi`或`TabularEditor.3.27.0.ARM64.Net8.msi\`。选择适合目标计算机的体系结构和运行时；参见 @system-requirements。 MSI 不会安装 .NET Desktop Runtime，所以先部署它。

可用的 MSI 命令行选项详见 Microsoft 官方文档：
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

### 预先配置许可证

在应用程序 _首次启动之前_ 将许可证写入注册表：

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
- 许可证密钥存储在 **HKCU** 下（按用户）。确保这些命令在目标用户的上下文中运行（例如通过登录脚本），这样这些值才会写入正确的用户配置文件。
- 如需其他键和值，请参阅 [注册表详细信息](#registry-details)。

