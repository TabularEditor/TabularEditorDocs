---
uid: system-requirements
title: 系统要求
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

# 系统要求

Tabular Editor 3 是一款 Windows 桌面应用程序。从 3.27.0 版本起，它将针对两种 .NET 运行时、两种处理器架构，并以三种组件格式发布。

## 操作系统

- Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本

在任何时刻支持哪些 Windows 版本，取决于你安装的运行时所遵循的 Microsoft .NET 受支持操作系统策略；因此即使 Tabular Editor 本身不变，支持范围也可能会随着时间推移而缩小。

## 发布内容

| 运行时                            | 架构        | 格式                            |
| ------------------------------ | --------- | ----------------------------- |
| .NET 10 _（推荐）_ | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |
| .NET 8         | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |

.NET 10 和 .NET 8 的构建&#x5728;_&#x529F;能上完全一致_。两者功能完全对等，没有一方有而另一方缺的内容，而且可以同时安装。

从 3.23.0 版本开始，ARM64 构建为原生版本。

## .NET 运行时

| 构建          | 所需内容                                                                                                                                                                                                                   |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.exe` 安装程序 | 对应的 [.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet)：[10](https://dotnet.microsoft.com/download/dotnet/10.0) 或 [8](https://dotnet.microsoft.com/download/dotnet/8.0)。安装程序会为你下载并安装它 |
| `.msi`      | 需要预先安装匹配的 .NET 桌面运行时。 MSI _不&#x4F1A;_&#x5C06;其一并包含，这也是它适合无人值守部署的原因                                                                                                                                     |
| 便携版 `.zip`  | 无需任何额外组件。它是自包含的                                                                                                                                                                                                        |

必须安装 _Desktop_ 运行时。 ASP.NET Core 运行时和普通的 .NET 运行时不包含此应用所需的 Windows Forms 和 WPF 库。

## 选择构建版本

除非你有明确理由，否则请选择 **.NET 10 x64 `.exe` 安装程序**。理由如下：

- **ARM64**：你使用的是基于 ARM 的 PC
- **.NET 8**：你的组织目前还无法安装 .NET 10 桌面运行时
- **`.msi`**：你正在进行集中部署。参见 [静默安装](xref:installation-activation-basic)
- **便携版 `.zip`**：你无法在这台计算机上安装软件，或者你希望同时使用多个版本

## 可选组件

| 组件                                                                                      | 用途                                           | 说明                                                                                     |
| --------------------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------------- |
| [Microsoft Edge WebView2 运行时](https://developer.microsoft.com/microsoft-edge/webview2/) | 应用内的 **开始使用** 页面和 @ai-assistant | 当前版本的 Windows 通常已预装。如果缺少该组件，Tabular Editor 会改用内置浏览器控件，或提供链接让你在默认浏览器中打开该页面              |
| AI 功能                                                                                   | @ai-assistant 与 MCP 服务器         | 默认会被选中的安装组件。安装时可取消选中；此外，无论是否选中，管理员都可以通过 @policies 中的 `DisableAi` 禁用 AI 功能 |

## 下载位置

当前版本请参见 @downloads，旧版本请参见 @release-history。

## 后续步骤

- @下载量
- @快速入门
- @installation-activation-basic
