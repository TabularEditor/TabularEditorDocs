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

本页介绍 Tabular Editor 3 常见的安装和激活问题，以及相应的解决方法。 有关标准激活流程，请参见 @getting-started。 有关高级部署场景（静默安装、许可证预配置、安装后配置），请参见 @installation-activation-basic。

## 检查系统要求

在继续排查之前，先确认你的计算机满足以下要求：

- **操作系统：** Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本
- **架构：** x64、ARM64（自 3.23.0 起提供原生支持）
- **.NET Runtime：** [.NET Desktop Runtime 8.0](https://dotnet.microsoft.com/en-us/download/dotnet/8.0)

从 [下载页](xref:downloads) 下载与你的系统架构匹配的 MSI 安装包。 安装程序与系统架构不匹配，是安装失败以及首次启动时出现依赖项缺失错误的常见原因。

<a name="inspect-the-activated-license"></a>

## 检查已激活的许可证

Tabular Editor 3 会将激活信息存储在 Windows 注册表的 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3` 下。

要查看当前 Windows 登录用户的许可证密钥，在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

你也可以直接使用 `regedit.exe` 查看和编辑 **LicenseKey** 与 **User** 的值。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

## 激活对话框反复出现

Tabular Editor 3 会在启动时以及之后定期连接 `https://api.tabulareditor.com` 以验证许可证。 如果由于防火墙或代理而无法访问这个端点，应用每 30 天都需要重新激活一次。 有关所使用端点的完整列表，请参阅 @policies。

如果激活提示反复出现：

1. 确认受影响的计算机可以访问 `api.tabulareditor.com`。
2. 在 **工具 > 偏好 > 代理设置** 中配置代理。 如需进行代理相关的故障排除，请参阅 @proxy-settings，其中包括用于启用外部 MSAL 代理支持的 **AnalysisServices.AppSettings.json** 覆盖配置。
3. 如果网络阻止向激活端点发起出站流量，请使用下方的[手动激活](#manual-activation-no-internet)。

<a name="manual-activation-no-internet"></a>

## 手动激活（无网络连接）

如果运行 Tabular Editor 的计算机无法访问激活端点，激活提示会提供手动激活流程。

![Manual Activation Prompt](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

1. 输入您的电子邮件地址。 此时会弹出一个对话框，其中包含指向激活密钥的链接。

2. 复制该 URL，然后在另一台能上网的计算机上打开。 该 URL 会返回一个 JSON 对象。

   ![Manual Activation JSON Object](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

3. 复制完整的 JSON 对象，并将其粘贴到离线计算机上的对话框中。

   ![Manual Activation Filled In](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

随后，Tabular Editor 3 会验证许可证。

## 无法在 UI 中更改许可证密钥

只有在未加载任何模型时，**帮助 > 关于 Tabular Editor** 下的 **更改许可证密钥** 按钮才会启用。 如果该按钮是灰色的，先通过 **文件 > 关闭模型** 关闭当前打开的模型，然后再试一次。

如果 UI 选项还是不起作用，就通过注册表编辑器重置许可证：

1. 关闭所有正在运行的 Tabular Editor 3。
2. 打开注册表编辑器（开始 > 运行 > regedit.msc）。
3. 定位到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`。
4. 删除此键下的所有值。
5. 重新启动 Tabular Editor 3。

或者，在 Windows 命令提示符中运行以下命令：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

下次启动时，会像首次安装该应用一样提示输入许可证密钥。

> [!IMPORTANT]
> 一旦移除许可证密钥，在输入新的许可证密钥之前，该计算机上的当前 Windows 用户将无法使用该产品。

## 许可证激活在错误的 Windows 用户帐户下

Tabular Editor 3 的激活信息会 **按用户分别** 存储在 `HKEY_CURRENT_USER` 下。 如果多位用户共用一台计算机，则每位用户都需要在自己的 Windows 用户配置文件下激活该产品。 在某个 Windows 帐户下激活的许可证，对同一台计算机上的其他 Windows 帐户不可见。

若要检查哪个 Windows 帐户拥有该许可证，以该用户身份登录，并运行 [检查已激活的许可证](#inspect-the-activated-license) 中的注册表查询命令。

### Windows 帐户与 Power BI / Entra 帐户

一个常见的困惑点是：运行 Tabular Editor 3 的 Windows 帐户，与用于对 Power BI / Fabric Workspace 进行身份验证的 Microsoft Entra 帐户是相互独立的。

- **许可证激活信息** 存储在激活该产品的 Windows 用户的 `HKEY_CURRENT_USER` 下。 它不与任何云身份绑定。
- **Workspace 身份验证**会在 **从数据库加载语义模型** 对话框中建立连接时进行。 在这里使用对 Workspace 有权限的 Microsoft Entra 帐户登录。

即使你使用单独的 Entra 帐户连接到 Power BI（例如未启用邮件的管理员帐户），也无需通过 **以其他用户身份运行** 使用不同的 Windows 帐户启动 Tabular Editor 3。 在你常用的 Windows 帐户下启动，在该帐户下激活许可证，并在连接对话框中提供管理员 Entra 凭据。

关于如何选择正确的身份验证模式的详细信息（例如，当你的 Windows 登录与 Power BI 帐户不一致时使用 **Microsoft Entra MFA**），请参阅 @xmla-as-connectivity。

## 企业版席位正被另一位用户使用

企业版许可证按席位授权。 要在所有席位都已占用时为新用户激活 Tabular Editor 3，必须先通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 将现有用户从某个席位取消注册。 此操作需由订阅所有者或许可证管理员执行。

> [!NOTE]
> 仅企业版支持重新分配席位。

## 通过代理激活

Tabular Editor 3 会发起出站 Web 请求，用于产品激活、检查更新、DAX 格式化，以及下载外部最佳实践规则。 如果你在代理服务器后面：

1. 在 **工具 > 偏好 > 代理设置** 中进行配置。 将 **代理类型** 在 `System` 和 `None` 之间切换，重启 Tabular Editor 3，然后再次尝试激活。
2. 如果激活仍然失败，请参阅 @proxy-settings 进行高级代理诊断。
3. 如果对 `api.tabulareditor.com` 的出站访问被阻止，请使用 [手动激活](#manual-activation-no-internet)。

> [!TIP]
> 代理设置可能会干扰身份验证对话框和其他外部提示。 更改代理类型后，重新测试前务必先关闭并重新打开 Tabular Editor 3。

## 确认你已使用最新版本

与激活相关的问题有时会在较新的 Tabular Editor 3 版本中得到修复。 提交支持请求前，先确认你使用的是最新版本。 在 **工具 > 偏好 > 更新和反馈** 中检查更新，或从 [下载页面](xref:downloads) 下载最新安装程序。
