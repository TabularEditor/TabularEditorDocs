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

| MSI feature   | 在安装程序中显示为        | 说明                                                              | 默认安装                                                                                                                  |
| ------------- | ---------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `MainFeature` | Tabular Editor 3 | Tabular Editor 3 核心应用程序                                         | Yes (required)                                                                                     |
| `AIAssistant` | AI 功能            | The @ai-assistant and the @mcp-server | Yes, from 3.27.0. Earlier versions install it only when it's selected |

> [!IMPORTANT]
> From 3.27.0, a new installation includes the **AI features** component unless you exclude it. If your organization doesn't allow the AI Assistant or the MCP server, exclude the component and set the `DisableAi` policy as described below.

### 部署时不包含 AI 功能

Leave `AIAssistant` out of `ADDLOCAL` to install Tabular Editor 3 without the AI features:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart ADDLOCAL=MainFeature /l*v C:\Temp\TE3_install.log
```

Run the package with `REMOVE` to remove the component from machines that already have it:

```powershell
msiexec /i TabularEditor.<version>.x64.Net10.msi /qn /norestart REMOVE=AIAssistant /l*v C:\Temp\TE3_install.log
```

Without the component, the AI assemblies aren't in the installation folder, the **AI Assistant** pane and the MCP server are absent from the application and no requests go to a model provider. Other features are unaffected.

To change the selection on a single machine, run the installer again and select **Modify** in the maintenance dialog.

> [!NOTE]
> 使用 `ADDLOCAL` 时，除了任何可选功能外，也必须包含 `MainFeature`。如果仅指定 `AIAssistant` 而不包含 `MainFeature`，将导致安装不完整。

### Upgrades and the AI features component

When you install a newer version of the same package over an existing installation, the installer keeps the feature selection the machine already has. This applies to interactive and silent installations. A machine deployed without the AI features before 3.27.0 stays without them after the upgrade, and a machine where the AI features were selected keeps them.

In these cases the installer applies the default selection or the selection on the command line:

| Situation                                                                                                                                                            | 结果                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The command line sets `ADDLOCAL`, `REMOVE` or another feature property                                                                                               | The command line sets the selection. `ADDLOCAL=MainFeature` removes the AI features from machines that have them, and `ADDLOCAL=ALL` installs them on machines that don't         |
| The deployment uninstalls the earlier version before it installs the new one, for example an Intune supersedence set to uninstall                                    | The installation is new and includes the AI features unless the command line excludes them                                                                                                        |
| The package targets a different runtime than the installed one, for example the .NET 10 package on a machine with the .NET 8 package | The .NET 8 and .NET 10 packages are separate products. The installation is new and includes the AI features unless the command line excludes them |

The `DisableAi` policy overrides the selection in every case.

### Enforcing the decision with the DisableAi policy

A user who runs the installer gets the default selection, which includes the AI features. Set the `DisableAi` @policies to `1` under `HKEY_LOCAL_MACHINE\Software\Policies\Tabular Editor ApS\TE3` to keep the AI features off every installation on the machine. Tabular Editor 3 reads the policy at startup and turns off the AI Assistant and the MCP server.

From 3.27.0 the installer reads the policy as well:

- a new installation leaves out the AI features component, and the installer doesn't show it
- an upgrade removes the component from a machine that has it
- an existing installation keeps the AI files until the next upgrade. Tabular Editor 3 doesn't load them while the policy is set

A deployment tool that runs as the local system account doesn't read the `HKEY_CURRENT_USER` policies of the machine's users. Set the policy under `HKEY_LOCAL_MACHINE` for the installer to read it in a silent deployment.

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

