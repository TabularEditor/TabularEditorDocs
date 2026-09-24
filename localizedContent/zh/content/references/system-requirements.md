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

Tabular Editor 3 是一款 Windows 桌面应用程序。自 3.27.0 版本起，它基于两个 .NET 运行时、面向两种处理器架构，并以三种组件格式发布。

## 操作系统

- Windows 10、Windows 11、Windows Server 2016、Windows Server 2019 或更高版本

在任何时点支持哪些 Windows 版本，取决于你安装的运行时所遵循的 Microsoft .NET 受支持操作系统策略；因此，支持范围可能会随着时间推移而收窄，这与 Tabular Editor 本身无关。

## 发布内容

| 运行时                            | 架构        | 格式                            |
| ------------------------------ | --------- | ----------------------------- |
| .NET 10 _（推荐）_ | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |
| .NET 8         | x64、ARM64 | `.exe` 安装程序、`.msi`、便携式 `.zip` |

.NET 10 和 .NET 8 构建版本在功能上 _完全一致_。两者互不缺少对方的任何内容，并且可以并排安装。

自 3.23.0 版本起，ARM64 构建为原生版本。

## .NET 运行时

| 构建版本        | 需要                                                                                                                                                                                                                     |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `.exe` 安装程序 | 对应的 [.NET Desktop Runtime](https://dotnet.microsoft.com/download/dotnet)：[10](https://dotnet.microsoft.com/download/dotnet/10.0) 或 [8](https://dotnet.microsoft.com/download/dotnet/8.0)。安装程序会为你下载并安装它 |
| `.msi`      | 需预先安装匹配的 .NET Desktop Runtime。 MSI _&#x4E0D;_&#x968F;附该组件，这正是它适合无人值守部署的原因                                                                                                                              |
| 便携版 `.zip`  | 无。它是自包含的                                                                                                                                                                                                               |

必须是 _Desktop_ 运行时。 ASP.NET Core 运行时和普通 .NET 运行时都不包含该应用所需的 Windows Forms 和 WPF 库。

## 选择构建版本

除非你有明确理由选择其他版本，否则就选 **.NET 10 x64 `.exe` 安装程序**。理由如下：

- **ARM64**：你使用的是基于 ARM 的 PC
- **.NET 8**：你的组织目前还无法安装 .NET 10 桌面运行时
- **`.msi`**：你要进行集中部署。参见 [静默安装](xref:installation-activation-basic)
- **便携版 `.zip`**：你无法在这台电脑上安装软件，或者希望多个版本并存

## 可选组件

| 组件                                                                                      | 用途                                           | 说明                                                                                        |
| --------------------------------------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| [Microsoft Edge WebView2 运行时](https://developer.microsoft.com/microsoft-edge/webview2/) | 应用内的 **开始使用** 页面和 @ai-assistant | 当前 Windows 系统通常已包含。如果缺少该组件，Tabular Editor 会改用内置浏览器控件，或提供链接让你在默认浏览器中打开该页面                  |
| AI 功能                                                                                   | @ai-assistant 与 MCP 服务器         | 安装程序中的一个组件，默认选中。安装时可取消选择；另外，无论是否选择安装，管理员都可以通过 `DisableAi` @policies 禁用 AI 功能 |

## 下载位置

当前版本请参见 @downloads，旧版本请参见 @release-history。

## 后续步骤

- @downloads
- @getting-started
- @installation-activation-basic
