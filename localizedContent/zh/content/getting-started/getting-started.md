---
uid: getting-started
title: 安装与激活
author: Morten Lønskov
updated: 2026-03-27
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

# 快速入门

## 安装

从我们的[下载页面](xref:downloads)下载最新版本的 Tabular Editor 3。

我们建议在大多数情况下使用 64 位 MSI 安装程序。 下载完成后，双击 MSI 文件，并按安装向导的各步骤完成安装。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

### 先决条件

无。

### 系统要求

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **体系结构：** x64、ARM64（自 3.23.0 起提供原生支持）
- **.NET 运行时：** [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

有关各运行时当前支持的 Windows 版本，请参阅 .NET 支持的 OS 策略。

## 激活安装

Tabular Editor 3 是商业软件。 访问我们的[主页](https://tabulareditor.com)，了解定价详情和购买选项。 如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。 选择此选项时，系统会提示您输入电子邮件地址。 我们会使用该电子邮件地址来验证您是否已经激活过 Tabular Editor 3。

首次在新设备上启动 Tabular Editor 3 时，系统会提示进行产品激活。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥进行激活

购买 Tabular Editor 3 许可证后，您将收到一封电子邮件，其中包含一串 25 个字符的代码，也就是您的许可证密钥。 按提示输入许可证密钥，然后点击“下一步 >”以激活产品。 出现提示时，输入许可证密钥，然后点击 **下一步 >** 以激活产品。

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥之外，您还需要输入电子邮件地址。 如果您输入的许可证密钥对应多用户许可证，Tabular Editor 3 会提示您输入电子邮件地址。 下次启动 Tabular Editor 3 时，系统会提示你输入许可证密钥，就像该工具首次安装到此计算机上时一样。

Tabular Editor 3 的安装是按 **用户** 激活的。 如果多个用户共享同一台计算机，则每个用户都需要在各自的 Windows 用户配置文件中激活该产品。

### Windows 帐户与 Power BI / Entra 帐户

安装 Tabular Editor 3 的 Windows 帐户与用于对 Power BI / Fabric Workspace 进行身份验证的 Microsoft Entra 帐户彼此独立。

- **许可证激活** 信息存储在激活该产品的 Windows 用户的注册表 `HKEY_CURRENT_USER` 下。 许可证不绑定到任何云身份。
- **Workspace 身份验证** 会在连接时于 **从数据库加载语义模型** 对话框中进行。 你需要使用对该 Workspace 拥有权限的 Microsoft Entra 帐户登录。

即使你使用单独的 Entra 帐户（例如未启用电子邮件的管理员帐户）来管理 Power BI Workspace，也无需因此在其他 Windows 帐户下通过 **以其他用户身份运行** 启动 Tabular Editor 3。 在你平时使用的 Windows 帐户下启动 Tabular Editor 3，在该帐户下用许可证密钥激活它，并在连接对话框中输入你的管理员 Entra 凭据。

有关 Tabular Editor 连接到 XMLA endpoint 时如何进行身份验证，以及如何选择正确的身份验证模式（例如，当 Windows 登录与 Power BI 帐户不一致时使用 **Microsoft Entra MFA**），参见 @xmla-as-connectivity。

### 申请试用许可证

如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。 选择这个选项后，系统会提示你输入电子邮件地址。 我们会使用这个电子邮件地址来验证你是否已有 Tabular Editor 3 的激活记录。

> [!NOTE]
> 在申请 30 天试用许可证时，Tabular Editor ApS 不会发送未经请求的电子邮件，也不会将你的电子邮件地址提供给第三方。 查看我们的 @privacy-policy 以了解更多信息。 查看我们的 @privacy-policy 以了解更多信息。

### 更改许可证密钥

Tabular Editor 3 激活后，您可以在“帮助”菜单中选择“关于 Tabular Editor”来更改许可证密钥。

![关于 Te3](~/content/assets/images/getting-started/about-te3.png)

在对话框中，选择 **更改许可证密钥**。 只有在 Tabular Editor 中未加载任何模型时，此选项才可用。 如果模型已打开，请通过 **文件 > 关闭模型** 将其关闭。 点击 **更改许可证密钥** 后，Tabular Editor 会提示你是否要移除当前许可证：

![图片](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

确认后，将删除当前许可证，并且您必须重新输入许可证密钥才能使用产品。

> [!IMPORTANT]
> 按上述方式删除许可证密钥后，在该计算机上的当前用户重新输入新的许可证密钥之前，将无法使用该产品。

## 静默安装与许可证预配置

Tabular Editor 3 提供了许多配置选项。 默认设置已足以满足大多数开发场景，但仍建议查看以下选项。

### 启动时检查更新

默认情况下，每次启动 Tabular Editor 3 时，工具都会联机检查是否有新版本可用。 你可以在 **工具 > 偏好设置 > 更新和反馈** 中控制此更新检查的执行方式。

> 关闭所有 Tabular Editor 3 实例。 在提交 Bug Report 前，请确保你使用的是最新版本；我们的支持团队会以此为前提。

### 选择退出遥测数据收集

Tabular Editor 3 会收集匿名使用数据和遥测信息，用来帮助我们改进产品。 你可以随时启动 Tabular Editor 3，并前往 **工具 > 偏好设置 > 更新和反馈** 选择退出。 要退出，请取消选中 **通过收集匿名使用数据帮助改进 Tabular Editor** 复选框。

![收集遥测数据](~/content/assets/images/getting-started/collect-telemetry.png)

### 代理设置

如果你所在的网络互联网连接受限，请在 **工具 > 偏好设置 > 代理设置** 中指定代理服务器的地址、用户名和密码。 要让 Tabular Editor 3 使用任何依赖出站 Web 请求的功能，必须先完成此设置。 具体包括：

- 更新检查
- 产品激活
- DAX 格式设置
- 从外部 URL 下载最佳实践规则

> [!TIP]
> 代理设置有时会干扰身份验证对话框或其他外部提示。 关闭注册表编辑器，然后重新启动 Tabular Editor 3。

### 其他偏好设置

Tabular Editor 3 还提供许多其他设置，用于控制应用程序行为。 要了解更多信息，请参阅 @preferences。

## 高级场景

有关手动（无网络）激活、基于注册表的许可证管理、静默部署以及 Enterprise 席位管理，请参阅 @installation-activation-basic。

## 后续步骤

- [Tabular Editor 3 用户界面概览](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- 默认安装
