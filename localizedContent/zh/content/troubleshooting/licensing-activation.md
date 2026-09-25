---
uid: licensing-activation
title: 安装并激活 Tabular Editor 3
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

# 安装并激活 Tabular Editor 3

This page covers common installation and activation problems for Tabular Editor 3 and how to resolve them. For the standard activation flow, see @getting-started. For advanced deployment scenarios (silent install, license pre-provisioning, post-install configuration), see @installation-activation-basic.

## 检查系统要求

Confirm the machine meets the requirements before further troubleshooting:

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **架构：** x64、ARM64（自 3.23.0 起原生支持）
- **.NET 运行时：** [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

Use the matching MSI for your architecture from the [downloads page](xref:downloads). An installer or architecture mismatch is a frequent cause of failed installs and missing-dependency errors at first launch.

## 检查已激活的许可证

Tabular Editor 3 会将激活详细信息存储在 Windows 注册表 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` 下。

若要查看当前 Windows 用户的许可证密钥，请在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

You can also inspect and edit the **LicenseKey** and **User** values directly using `regedit.exe`.

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

## Activation dialog keeps reappearing

Tabular Editor 3 contacts `https://api.tabulareditor.com` at startup and periodically to validate the license. If this endpoint is unreachable due to a firewall or proxy, the application requires re-activation every 30 days. See @policies for the full list of endpoints used.

If activation prompts persist:

1. Confirm `api.tabulareditor.com` is reachable from the affected machine.
2. Configure proxy settings under **Tools > Preferences > Proxy Settings**. See @proxy-settings for proxy-specific troubleshooting, including the **AnalysisServices.AppSettings.json** override that enables external MSAL proxy support.
3. If the network blocks outbound traffic to the activation endpoint, use [Manual activation](#manual-activation-no-internet) below.

## 手动激活（无网络连接）

If the machine running Tabular Editor cannot reach the activation endpoint, the activation prompt offers a manual flow.

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

1. Enter your e-mail. A dialog appears with a link to an activation key.

2. Copy the URL and open it on a different machine that has internet access. The URL returns a JSON object.

   ![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

3. Copy the full JSON object and paste it into the dialog on the offline machine.

   ![已填写的手动激活信息](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

然后，Tabular Editor 3 会验证许可证。

## 无法通过 UI 更改许可证密钥

The **Change license key** button under **Help > About Tabular Editor** is only enabled when no model is loaded. If the button is grayed out, close the open model under **File > Close model** and try again.

If the UI option still fails, reset the license through the Registry Editor:

1. 关闭所有 Tabular Editor 3 实例。
2. 打开注册表编辑器（开始 > 运行 > regedit.msc）。
3. 定位到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`。
4. 删除此键下的所有值。
5. 重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符中运行以下命令：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

The next launch prompts for a license key as if the application were freshly installed.

> [!IMPORTANT]
> Once a license key is removed, the product is not usable by the current Windows user on that machine until a new license key is entered.

## License is on the wrong Windows user

Tabular Editor 3 activations are stored **per user** under `HKEY_CURRENT_USER`. If multiple users share a machine, each user activates the product on their own Windows profile. A license activated under one Windows account is not visible to another Windows account on the same machine.

To check which Windows account holds the license, log in as that user and run the registry query in [Inspect the activated license](#inspect-the-activated-license).

### Windows account vs Power BI / Entra account

A common source of confusion: the Windows account that runs Tabular Editor 3 is independent from the Microsoft Entra account used to authenticate against a Power BI / Fabric workspace.

- **License activation** is stored under `HKEY_CURRENT_USER` of the Windows user that activated the product. It is not tied to any cloud identity.
- **Workspace authentication** happens at connection time in the **Load Semantic Model from Database** dialog. Sign in there with the Microsoft Entra account that has permission on the workspace.

You do not need to launch Tabular Editor 3 with **Run as** under a different Windows account just because you connect to Power BI with a separate Entra account (for example a non-mail-enabled admin account). Launch under your normal Windows account, activate the license under that account, and provide the admin Entra credentials in the connection dialog.

For details on how to choose the right authentication mode (for example **Microsoft Entra MFA** when your Windows login does not match your Power BI account), see @xmla-as-connectivity.

## Enterprise seat is in use by another user

Enterprise licenses are seat-based. To activate Tabular Editor 3 on a new user when all seats are occupied, the existing user must first be deregistered from a seat through the [Tabular Editor Self-Service portal](https://tabulareditor.com/my-account/). The subscription owner or license administrator performs this action.

> [!NOTE]
> Seat reassignment is only possible on the Enterprise Edition.

## Activation behind a proxy

Tabular Editor 3 uses outgoing web requests for product activation, update checks, DAX formatting, and downloading external Best Practice rules. If you are behind a proxy:

1. Configure **Tools > Preferences > Proxy Settings**. Switch the **Proxy Type** between `System` and `None`, restart Tabular Editor 3, and retry activation.
2. If activation still fails, see @proxy-settings for advanced proxy diagnostics.
3. If outbound access to `api.tabulareditor.com` is blocked, use [Manual activation](#manual-activation-no-internet).

> [!TIP]
> Proxy settings can interfere with authentication dialogs and other external prompts. After changing the proxy type, always close and reopen Tabular Editor 3 before retesting.

## Confirm you are on the latest version

与激活相关的问题有时会在较新的 Tabular Editor 3 版本中修复。 Confirm you are on the latest version before submitting a support request. Check for updates under **Tools > Preferences > Updates and Feedback**, or download the latest installer from the [downloads page](xref:downloads).
