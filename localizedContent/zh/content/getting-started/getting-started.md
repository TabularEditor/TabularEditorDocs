---
uid: getting-started
title: 安装与激活
author: Morten Lønskov
updated: 2025-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: 桌面版
          full: true
        - edition: 商业版
          full: true
        - edition: 企业版
          full: true
---

# 快速入门

## 安装

从我们的[下载页面](xref:downloads)下载最新版本的 Tabular Editor 3。

## 先决条件

无。

## 系统要求

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **体系结构：** x64、ARM64（自 3.23.0 起提供原生支持）
- **.NET 运行时：** [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

有关各运行时当前支持的 Windows 版本，请参阅 .NET 支持的 OS 策略。

## 激活安装

Tabular Editor 3 是商业软件。 访问我们的[主页](https://tabulareditor.com)，了解定价详情和购买选项。 如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。

首次在新设备上启动 Tabular Editor 3 时，系统会提示进行产品激活。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥进行激活

购买 Tabular Editor 3 许可证后，您将收到一封电子邮件，其中包含一串 25 个字符的代码，也就是您的许可证密钥。 按提示输入许可证密钥，然后点击“下一步 >”以激活产品。

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥之外，您还需要输入电子邮件地址。 如果您输入的许可证密钥对应多用户许可证，Tabular Editor 3 会提示您输入电子邮件地址。

请注意，Tabular Editor 3 的安装是**按用户**激活的。 换句话说，如果多个用户共用同一台计算机，则每个用户都必须在各自的 Windows 用户配置文件中激活产品。

### 申请试用许可证

如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。 选择此选项时，系统会提示您输入电子邮件地址。 我们会使用该电子邮件地址来验证您是否已经激活过 Tabular Editor 3。

> [!NOTE]
> 在申请 30 天试用许可证时，Tabular Editor ApS 不会发送未经请求的电子邮件，也不会将你的电子邮件地址提供给第三方。 查看我们的 @privacy-policy 以了解更多信息。

### 更改许可证密钥

Tabular Editor 3 激活后，您可以在“帮助”菜单中选择“关于 Tabular Editor”来更改许可证密钥。

![关于 Te3](~/content/assets/images/getting-started/about-te3.png)

在对话框中，选择“更改许可证密钥”。 请注意，只有在 Tabular Editor 中未加载任何模型时，此选项才可用。 如果您已加载模型，可以通过“文件 > 关闭模型”将其关闭。 单击“更改许可证密钥”后，Tabular Editor 会询问您是否要删除当前许可证：

![图片](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

确认后，将删除当前许可证，并且您必须重新输入许可证密钥才能使用产品。

> [!IMPORTANT]
> 按上述方式删除许可证密钥后，在该计算机上的当前用户重新输入新的许可证密钥之前，将无法使用该产品。

<a name="registry-details"></a>
#### 注册表详细信息

Tabular Editor 3 使用 Windows 注册表来存储激活详细信息。

要查看分配给该计算机的当前许可证密钥，请在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

你也可以使用 `regedit.exe`（Windows 注册表编辑器），前往 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，查看并修改 **LicenseKey** 和 **User** 的值。

系统管理员也可以在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表键下指定 **LicenseKey** 和 **User** 的值，提前为某台计算机分配 Tabular Editor 3 许可证。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

### 通过注册表更改许可证密钥

如果出于任何原因，你无法按上述流程更改许可证密钥，也可以随时通过注册表编辑器重置分配给 Tabular Editor 3 的许可证：

1. 关闭所有 Tabular Editor 3 实例。
2. 在 Windows 中打开注册表编辑器（开始 > 运行 > regedit.msc）。
3. 定位到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上方截图）。
4. 删除该项下的所有值。
5. 关闭注册表编辑器，然后重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符中运行以下命令（开始 > 运行 > cmd.exe）：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

下次启动 Tabular Editor 3 时，系统会提示你输入许可证密钥，就像该工具首次安装到此计算机上时一样。

### 静默安装与许可证预配置

你可以以静默方式部署 Tabular Editor，并通过 Windows 注册表预先配置许可证。

1. **静默安装**（无 UI，不重启）：
   ```powershell
   msiexec /i TabularEditor.<version>.x64.Net8.msi /qn /norestart /l*v C:\Temp\TE3_install.log
   ```

你也可以使用 `/package` 替代 `/i`。 将 `<version>` 替换为实际的版本字符串。 如适用，请使用 ARM64 MSI。

有关可用 MSI 命令行选项的详细信息，请参阅 Microsoft 官方文档：  
[Microsoft Standard Installer command-line options - Win32 apps | Microsoft Learn](https://learn.microsoft.com/windows/win32/msi/command-line-options)

2. **在应用程序首次启动之前**，**将许可证写入注册表**：

   ```bat
   REM Per-user license key (HKCU)
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey /t REG_SZ /d YOUR-25-CHAR-KEY /f
   ```

   如果你使用的是 **企业版** 许可证密钥，还需要设置获授权用户的电子邮件：

   ```bat
   REG ADD "HKCU\Software\Kapacity\Tabular Editor 3" /v User /t REG_SZ /d user@example.com /f
   ```

**备注**

- 安装程序**不**接受许可证参数；许可证通过上述注册表项进行处理。
- 注册表项存储在 **HKCU** 下（每用户）。 请确保这些命令在目标用户的上下文中运行（例如通过登录脚本等方式），以便将值写入正确的用户配置文件。
- 有关更多键和值，请参阅[注册表详细信息](#registry-details)。

## 后续步骤

- [Tabular Editor 3 用户界面概览](xref:user-interface)