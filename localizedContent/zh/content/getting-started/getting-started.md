---
uid: getting-started
title: 安装与激活
author: Morten Lønskov
updated: 2026-09-14
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

# 安装与激活

## 安装

从我们的[下载页面](xref:downloads)下载最新版本的 Tabular Editor 3。

We recommend the 64-bit `.exe` installer on .NET 10 for most scenarios. Once downloaded, double-click it and complete the installer pages.

![Install](~/content/assets/images/getting-started/install.png)

### 先决条件

For the `.exe` installer, the matching **.NET Desktop Runtime**: [10](https://dotnet.microsoft.com/download/dotnet/10.0) for the recommended build, or [8](https://dotnet.microsoft.com/download/dotnet/8.0) for the .NET 8 build. The installer offers to download and install it for you, so in practice there is nothing to do beforehand.

The other two packages differ. The `.msi` does not bring the runtime along, so install it yourself when deploying centrally, and the portable `.zip` is self-contained and needs no runtime at all.

### 系统要求

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **架构：** x64、ARM64（自 3.23.0 起原生支持）
- **.NET Runtime:** .NET Desktop Runtime 10 or 8, matching the build you install

See @system-requirements for the full matrix and for how to choose between the builds.

## 激活安装

Tabular Editor 3 是商业软件。 Visit our [home page](https://tabulareditor.com) for pricing details and purchase options. 如果你之前未使用过 Tabular Editor 3，即可获得 30 天免费试用。

首次在新设备上启动 Tabular Editor 3 时，系统会提示进行产品激活。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥进行激活

购买 Tabular Editor 3 的许可证后，你会收到一封电子邮件，其中包含一段 25 个字符的字符串，这就是你的许可证密钥。 When prompted, enter the license key and click **Next >** to activate the product.

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥之外，你还需要输入电子邮件地址。如果该许可证密钥对应多用户许可证，Tabular Editor 3 会提示你这样做。

Tabular Editor 3 installations are activated **per user**. If multiple users share the same machine, each user activates the product on their own Windows user profile.

### Windows account vs Power BI / Entra account

The Windows account on which Tabular Editor 3 is installed is independent from the Microsoft Entra account used to authenticate against a Power BI / Fabric workspace.

- **License activation** is stored in the Windows Registry under `HKEY_CURRENT_USER` of the Windows user that activated the product. The license is not tied to any cloud identity.
- **Workspace authentication** happens at connection time in the **Load Semantic Model from Database** dialog. You sign in with the Microsoft Entra account that has permission on the workspace.

You do not need to launch Tabular Editor 3 with **Run as** under a different Windows account just because you use a separate Entra account (for example a non-mail-enabled admin account) to manage the Power BI workspace. Launch Tabular Editor 3 under your normal Windows account, activate it with your license key under that account, and provide your admin Entra credentials in the connection dialog.

For details on how Tabular Editor authenticates to the XMLA endpoint and how to pick the right authentication mode (for example **Microsoft Entra MFA** when your Windows login does not match your Power BI account), see @xmla-as-connectivity.

### 申请试用许可证

If you have not used Tabular Editor 3 before, you are eligible for a free 30-day trial. When you choose this option, you are prompted for an e-mail address. We use the e-mail address to validate whether you have an existing activation of Tabular Editor 3.

> [!NOTE]
> 在申请 30 天试用许可证时，Tabular Editor ApS 不会发送未经请求的电子邮件，也不会将你的电子邮件地址提供给第三方。 View our @privacy-policy for more information.

### 更改许可证密钥

激活 Tabular Editor 3 后，可在“帮助”菜单中选择 **关于 Tabular Editor** 来更改许可证密钥。

![关于 Te3](~/content/assets/images/getting-started/about-te3.png)

In the dialog, select **Change license key**. This option is only available when no model is loaded in Tabular Editor. If a model is open, close it under **File > Close model**. Once you click **Change license key**, Tabular Editor prompts you whether you want to remove the current license:

![image](~/content/assets/images/getting-started-01.png)

如果选择确定，当前许可证将被移除，你需要重新输入许可证密钥才能使用该产品。

> [!IMPORTANT]
> 一旦移除许可证密钥，在输入新的许可证密钥之前，当前用户将无法在该计算机上使用该产品。

## 安装后配置

Tabular Editor 3 provides many configuration options. The default settings are sufficient for most development scenarios, but review the options below.

### Check for updates on start-up

By default, whenever Tabular Editor 3 is launched, the tool checks online to see if a newer version is available. You control how this update check is performed under **Tools > Preferences > Updates and Feedback**.

> [!NOTE]
> 请始终使用最新版本的 Tabular Editor 3。 Our support team assumes you are on the latest version before submitting a bug report.

### Opting out of telemetry collection

Tabular Editor 3 会收集匿名使用数据和遥测信息，用来帮助我们改进产品。 You opt out at any time by launching Tabular Editor 3 and navigating to **Tools > Preferences > Updates and Feedback**. Uncheck the **Help improve Tabular Editor by collecting anonymous usage data** checkbox to opt out.

![Collect Telemetry](~/content/assets/images/getting-started/collect-telemetry.png)

### 代理设置

If you are on a network with limited internet connectivity, specify the address, username, and password of a proxy server under **Tools > Preferences > Proxy Settings**. This is required before Tabular Editor 3 can use any features that rely on outgoing web requests. Specifically:

- Update checks
- Product activation
- DAX Formatting
- Download of Best Practice Rules from external URLs

> [!TIP]
> The proxy settings can at times interfere with authentication dialog boxes or other external prompts. 尝试在 **System** 和 **None** 之间切换代理设置，然后关闭并重新打开 Tabular Editor 3 进行验证。

### Other preferences

Tabular Editor 3 contains many other settings for controlling application behavior. To learn more, see @preferences.

## Advanced scenarios

For manual (no-internet) activation, registry-based license management, silent deployment, and Enterprise seat administration, see @installation-activation-basic.

## 后续步骤

- [Tabular Editor 3 用户界面概览](xref:user-interface)
- @xmla-as-connectivity
- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2
- @installation-activation-basic
