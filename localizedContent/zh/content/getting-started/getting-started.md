---
uid: getting-started
title: 安装和激活
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

# 入门

## 安装

请从我们的[下载页面](xref:downloads)下载 Tabular Editor 3 的最新版本。

我们建议在大多数情况下使用 64 位 MSI 安装程序。 下载完成后，双击 MSI 文件，并按安装向导的提示完成安装。

![安装](~/content/assets/images/getting-started/install.png)

### 先决条件

无。

### 系统要求

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **架构：** x64、ARM64（自 3.23.0 起原生支持）
- **.NET 运行时：**[.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

有关每个运行时当前支持的 Windows 版本，请参阅 .NET 支持的操作系统策略。

## 激活安装

Tabular Editor 3 是商业软件。 访问我们的[主页](https://tabulareditor.com)，了解定价详情和购买选项。 如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。

首次在新计算机上启动 Tabular Editor 3 时，系统会提示你激活产品。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥激活

购买 Tabular Editor 3 的许可证后，你会收到一封电子邮件，其中包含一段 25 个字符的字符串，这就是你的许可证密钥。 出现提示时，输入许可证密钥，然后点击 **下一步 >** 以激活产品。

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥之外，你还需要输入电子邮件地址。 当许可证密钥对应的是多用户许可证时，Tabular Editor 3 会提示你这样做。

Tabular Editor 3 的安装是按 **用户** 激活的。 如果多个用户共享同一台计算机，则每位用户都需要在各自的 Windows 用户配置文件中激活产品。

### Windows 帐户与 Power BI / Entra 帐户

安装 Tabular Editor 3 的 Windows 帐户，与用于登录 Power BI / Fabric Workspace 的 Microsoft Entra 帐户彼此独立。

- **许可证激活** 信息存储在 Windows 注册表中，即激活该产品的 Windows 用户的 `HKEY_CURRENT_USER` 下。 许可证不与任何云身份绑定。
- **Workspace 身份验证**会在连接时于 **从数据库加载语义模型** 对话框中完成。 你需要使用对该 Workspace 具有权限的 Microsoft Entra 帐户登录。

即使你使用单独的 Entra 帐户（例如未启用邮箱的管理员帐户）来管理 Power BI Workspace，也不需要仅因为这一点就通过 **以其他用户身份运行** 在其他 Windows 帐户下启动 Tabular Editor 3。 在你平常使用的 Windows 帐户下启动 Tabular Editor 3，在该帐户下使用许可证密钥激活，然后在连接对话框中提供管理员 Entra 凭据。

有关 Tabular Editor 如何对 XMLA endpoint 进行身份验证，以及如何选择正确的身份验证模式的详细信息（例如，当你的 Windows 登录与 Power BI 帐户不一致时使用 **Microsoft Entra MFA**），请参阅 @xmla-as-connectivity。

### 申请试用许可证

如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。 选择此选项时，系统会提示你输入电子邮件地址。 我们会使用该电子邮件地址来验证你是否已有 Tabular Editor 3 的激活记录。

> [!NOTE]
> 在申请 30 天试用许可证时，Tabular Editor ApS 不会发送未经请求的电子邮件，也不会将你的电子邮件地址提供给第三方。 更多信息见我们的 @privacy-policy。

### 更改许可证密钥

激活 Tabular Editor 3 后，你可以在“帮助”菜单中选择 **关于 Tabular Editor** 来更改许可证密钥。

![About Te3](~/content/assets/images/getting-started/about-te3.png)

在该对话框中，选择 **更改许可证密钥**。 此选项仅在 Tabular Editor 中未加载任何模型时可用。 如果某个模型已打开，先通过 **文件 > 关闭模型** 将其关闭。 点击 **更改许可证密钥** 后，Tabular Editor 会提示你是否要删除当前许可证：

![image](https://user-images.githubusercontent.com/8976200/146754154-e691810b-342d-4311-8278-33da240d8d08.png)

如果你确认，当前许可证将被删除，你需要重新输入许可证密钥才能使用该产品。

> [!IMPORTANT]
> 删除许可证密钥后，在该计算机上，当前用户将无法使用该产品，直到输入新的许可证密钥为止。

## 安装后配置

Tabular Editor 3 提供了许多配置选项。 默认设置已足以满足大多数开发场景，但仍建议查看以下选项。

### 启动时检查更新

默认情况下，每次启动 Tabular Editor 3 时，工具都会联机检查是否有新版本可用。 你可以在 **工具 > 偏好 > 更新和反馈** 中控制更新检查的执行方式。

> [!NOTE]
> 请始终使用最新版本的 Tabular Editor 3。 在提交 Bug Report 之前，我们的支持团队会默认你使用的是最新版本。

### 退出遥测数据收集

Tabular Editor 3 会收集匿名使用数据和遥测信息，用来帮助我们改进产品。 你可以随时启动 Tabular Editor 3，并依次前往 **工具 > 偏好 > 更新和反馈** 以选择退出。 如需退出，请取消选中 **通过收集匿名使用数据帮助改进 Tabular Editor** 复选框。

![收集遥测数据](~/content/assets/images/getting-started/collect-telemetry.png)

### 代理设置

如果你所在的网络互联网连接受限，请在 **工具 > 偏好 > 代理设置** 中指定代理服务器的地址、用户名和密码。 在 Tabular Editor 3 使用任何依赖出站 Web 请求的功能之前，必须先完成此设置。 具体包括：

- 检查更新
- 产品激活
- DAX 格式化
- 从外部 URL 下载最佳实践规则

> [!TIP]
> 代理设置有时会影响身份验证对话框或其他外部提示。 尝试在 **System** 和 **None** 之间切换代理设置，然后关闭并重新打开 Tabular Editor 3 以进行验证。

### 其他偏好设置

Tabular Editor 3 还包含许多用于控制应用程序行为的设置。 若要了解详细信息，请参阅 @preferences。

## 高级场景

有关手动（无互联网）激活、基于注册表的许可证管理、静默部署和 Enterprise 席位管理，请参阅 @installation-activation-basic。

## 后续步骤

- [Tabular Editor 3 用户界面概述](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- @installation-activation-basic
