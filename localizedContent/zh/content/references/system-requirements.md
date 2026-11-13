---
uid: system-requirements
title: 系统要求
author: Morten Lønskov
updated: 2026-10-23
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
# 系统要求

Tabular Editor 3 是一款 Windows 桌面应用程序。从 3.27.0 版本起，该产品在两个 .NET 运行时上发布，适用于两种处理器架构，并提供三种软件包格式。

## 操作系统

- Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本

在任何特定时刻，哪些 Windows 版本受支持取决于 Microsoft 对于您所安装的运行时所适用的 .NET 受支持操作系统政策，因此，受支持的 Windows 版本范围可能会随着时间的推移而缩小，这与 Tabular Editor 无关。

## 发布内容

| 运行时 | 架构 | 格式 |
|---|---|---|
| .NET 10 *(推荐)* | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |
| .NET 8 | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |

.NET 10 和 .NET 8 版本在*功能上是相同的*。一个版本中存在的功能在另一个版本中也存在。使用“`.exe`”或“`.msi`”安装程序安装一个版本会替换另一个版本。请参阅[在 .NET 8 和 .NET 10 包之间切换](xref:installation-activation-basic#switching-between-the-net-8-and-net-10-packages)。

从 3.23.0 版本起，ARM64 版本为原生版本。

## .NET 运行时

| 版本 | 需要 |
|---|---|
| `.exe` 安装程序 | 匹配的[.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet)：[10](https://dotnet.microsoft.com/download/dotnet/10.0) 或 [8](https://dotnet.microsoft.com/download/dotnet/8.0)。安装程序会为您下载并安装 |
| `.msi` | 匹配的 .NET Desktop Runtime，需事先安装。MSI *不会*随附该运行时，这正是其适合无人值守部署的原因 |
| 可移植的 `.zip` | 无。它是自包含的 |

必须是*桌面*运行时。ASP.NET Core 运行时和普通的 .NET 运行时不包含应用程序所需的 Windows Forms 和 WPF 库。

## 选择生成

请选择 **.NET 10 x64 `.exe` 安装程序**，除非你有不选的理由。理由如下：

- **ARM64**：您使用的是基于 ARM 的 PC
- **.NET 8**：您的组织尚无法安装 .NET 10 桌面运行时
- **`.msi`**：您正在进行集中部署。请参阅[静默安装](xref:installation-activation-basic)
- **可移植的 `.zip`**：您无法在计算机上安装软件，或者您希望并行安装多个版本

## 可选组件

| 组件 | 用于 | 注意事项 |
|---|---|---|
| [Microsoft Edge WebView2 运行时](https://developer.microsoft.com/microsoft-edge/webview2/) | 应用内**入门**页面和 @ai-assistant | 存在于当前的 Windows 安装中。如果缺少此组件，Tabular Editor 将回退到内置浏览器控件，或提供一个链接，以便在默认浏览器中打开该页面 |
| AI 功能 | @ai-assistant 和 MCP 服务器 | 安装程序组件，默认选中。您可以在安装过程中取消选择此组件，管理员也可以使用 `DisableAi` @policies 禁用 AI 功能。|

## 下载位置

请参阅 @downloads 以了解当前版本，参阅 @release-history 以了解以前的版本。

## 后续步骤

- @downloads
- @getting-started
- @安装-激活-基础
