---
uid: installation-activation-basic
title: 安装、激活与基础配置
author: Daniel Otykier
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

## 安装

要安装 Tabular Editor 3，请从我们的 [下载页面](xref:downloads) 下载最新版本。

建议下载 64 位 MSI 安装程序，它适用于大多数场景。 下载完成后，双击 MSI 文件，然后按照安装向导的提示完成安装。

![安装](~/content/assets/images/getting-started/install.png)

## 激活此安装

当你首次在新机器上启动 Tabular Editor 3 时，系统会提示你激活产品。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥激活

购买 Tabular Editor 3 的许可证后，你会收到一封电子邮件，其中包含一段 25 个字符的字符串，这就是你的许可证密钥。 出现提示时，输入许可证密钥并点击“下一步 >”以激活产品。

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥之外，你还需要输入电子邮件地址。 如果你输入的许可证密钥对应多用户许可证，Tabular Editor 3 会提示你这样做。

<a name="manual-activation-no-internet"></a>
#### 手动激活（无网络）

如果你无法访问互联网，例如由于代理，Tabular Editor 会提示你进行手动激活。

![手动激活提示](~/content/assets/images/getting-started/Activation_manual_firstprompt.png)

输入邮箱后，会弹出一个对话框，其中包含指向激活密钥的链接。
复制该 URL，并在已连接互联网的网页浏览器中打开。

该 URL 会返回一个 JSON 对象：

![手动激活 JSON 对象](~/content/assets/images/getting-started/activation_manual_jsonobject.png)

复制返回的完整 JSON 对象，并将其粘贴到对话框中。
你的手动激活对话框最后会像下面这样。

![已填写的手动激活](~/content/assets/images/getting-started/activation_manual_dialogbox_filled.png)

这样即可验证你的 Tabular Editor 3 许可证。

### 更改许可证密钥

Tabular Editor 3 激活完成后，你可以在“帮助”菜单中选择“关于 Tabular Editor”，以更改许可证密钥。

![关于 Te3](~/content/assets/images/getting-started/about-te3.png)

在该对话框中，选择“更改许可证密钥”。 注意：只有在 Tabular Editor 中没有加载任何模型时，这个选项才可用。 如果你已经加载了模型，可以通过“文件 > 关闭模型”将其关闭。

有关管理许可证密钥的更多详细信息，请参阅[注册表详细信息](xref:getting-started#registry-details)。

## 基本配置

Tabular Editor 3 激活后，我们建议花几分钟熟悉一下[基本界面](xref:user-interface)。 此外，Tabular Editor 3 还提供了许多不同的配置选项。 默认设置足够应对大多数开发场景，但有几个重要的配置选项你最好都检查一下。

### 启动时检查更新

默认情况下，每次启动 Tabular Editor 3 时，工具都会联机检查是否有新版本可用。 你可以在 **工具 > 偏好 > 更新和反馈** 中设置更新检查的方式。

> [!NOTE]
> 我们建议始终使用最新版本的 Tabular Editor 3。 在提交 bug Report 时，我们的支持团队通常会默认你使用的是最新版本。

### 选择不参与遥测数据收集

Tabular Editor 3 会收集匿名使用数据和遥测信息，用来帮助我们改进产品。 你可以随时退出：启动 Tabular Editor 3，依次进入 **工具 > 偏好 > 更新和反馈**。 取消选中 **通过收集匿名使用数据帮助改进 Tabular Editor** 复选框即可选择退出。

![Collect Telemetry](~/content/assets/images/getting-started/collect-telemetry.png)

### 代理设置

如果你的网络连接受限，可以在 **工具 > 偏好 > 代理设置** 下指定代理服务器的地址、用户名和密码。 在 Tabular Editor 3 使用任何依赖出站 Web 请求的功能之前，必须先完成此设置。 具体包括：

- 检查更新
- 产品激活
- DAX 格式化
- 从外部 URL 下载最佳实践规则

> [!TIP]
> 代理设置有时会干扰身份验证对话框或其他外部提示。
> 尝试在“System”和“None”之间切换代理设置，关闭并重新打开 Tabular Editor 3 进行验证。

### 其他偏好设置

除上述设置外，Tabular Editor 3 还提供许多其他设置，用于控制应用程序的各种行为，让你可以更贴合自身需求地定制该工具。 要了解这些其他偏好设置的更多信息，请参阅 @preferences。

## 后续步骤

- @migrate-from-vs
- @migrate-from-desktop
- @migrate-from-te2