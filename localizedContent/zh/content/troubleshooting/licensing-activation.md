---
uid: licensing-activation
title: 安装并激活 Tabular Editor 3
author: Daniel Otykier
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

# Tabular Editor 3

## 安装

请从我们的[下载页面](xref:downloads)下载 Tabular Editor 3 的最新版本。

## 先决条件

无。

## 系统要求

- **操作系统：** Windows 7、Windows 8、Windows 10、Windows Server 2016、Windows Server 2019 或更高版本
- **.NET Framework：** [4.7.2](https://dotnet.microsoft.com/download/dotnet-framework)

## 激活你的安装

Tabular Editor 3 是商业软件。 访问我们的[主页](https://tabulareditor.com)查看价格详情和购买选项。 如果你之前没有使用过 Tabular Editor 3，则可免费试用 30 天。

在新设备上首次启动 Tabular Editor 3 时，系统会提示你激活产品。

![产品激活](~/content/assets/images/getting-started/product-activation.png)

### 使用现有许可证密钥激活

购买 Tabular Editor 3 许可证后，你会收到一封电子邮件，其中包含一段 25 个字符的字符串，即你的许可证密钥。 出现提示时，输入许可证密钥，然后点击“下一步 >”激活产品。

![输入许可证密钥](~/content/assets/images/getting-started/enter-license-key.png)

> [!NOTE]
> 对于多用户许可证类型，除了许可证密钥外，还需要输入电子邮件地址。 如果你输入的许可证密钥对应多用户许可证，Tabular Editor 3 会提示你输入电子邮件地址。

#### 企业版更换席位

要更换企业版席位，必须先通过 [Tabular Editor 自助服务门户](https://tabulareditor.com/my-account/) 将现有用户从该席位取消注册。 订阅所有者或许可证管理员可以创建账号，或使用现有账号登录，以管理许可证席位。

> [!NOTE]
> 仅企业版支持更换用户。

### 申请试用许可证

如果你之前没有使用过 Tabular Editor 3，你可以免费试用 30 天。 选择此选项后，系统会提示你输入电子邮件地址。 我们会使用该电子邮件地址来验证你是否已激活过 Tabular Editor 3。

> [!NOTE]
> 注册 30 天试用许可证时，Tabular Editor ApS 不会发送未经请求的电子邮件，也不会将你的电子邮件地址转交给第三方。 更多信息请查看我们的 @privacy-policy。

### 更改许可证密钥

激活 Tabular Editor 3 后，你可以在“帮助”菜单中选择“关于 Tabular Editor”，来更换许可证密钥。

![关于 Te3](~/content/assets/images/getting-started/about-te3.png)

在对话框中，选择“更改许可证密钥”。 注意：只有在 Tabular Editor 中未加载任何模型时，此选项才可用。 如果你已经加载了模型，可以通过“文件”>“关闭模型”将其关闭。

#### 注册表信息

Tabular Editor 3 使用 Windows 注册表来存储激活详细信息。

要查看分配给此计算机的当前许可证密钥，请在 Windows 命令提示符中运行以下命令（开始 > 运行 > cmd.exe）：

```cmd
REG QUERY "HKCU\Software\Kapacity\Tabular Editor 3" /v LicenseKey
```

你也可以使用 `regedit.exe`（Windows 注册表编辑器），并导航到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`，以查看和修改 **LicenseKey** 与 **User** 值。

系统管理员也可以通过在每个用户的 `SOFTWARE\Kapacity\Tabular Editor 3` 注册表项下指定 **LicenseKey** 和 **User** 值，提前为某台机器分配 Tabular Editor 3 许可证。

![注册表编辑器](~/content/assets/images/troubleshooting/registry-editor.png)

### 通过注册表更改许可证密钥

如果由于某些原因你无法按上述流程更改许可证密钥，你也可以使用注册表编辑器重置分配给 Tabular Editor 3 的许可证：

1. 关闭所有 Tabular Editor 3 实例。
2. 在 Windows 中打开“注册表编辑器”（开始 > 运行 > regedit.msc）。
3. 找到 `HKEY_CURRENT_USER\SOFTWARE\Kapacity\Tabular Editor 3`（见上方屏幕截图）。
4. 删除此键下的所有值。
5. 关闭“注册表编辑器”，然后重新启动 Tabular Editor 3。

或者，你也可以在 Windows 命令提示符（开始 > 运行 > cmd.exe）中运行以下命令：

```cmd
REG DELETE "HKCU\Software\Kapacity\Tabular Editor 3" /va
```

下次启动 Tabular Editor 3 时，系统会像该工具首次安装到此计算机时那样，提示你输入许可证密钥。