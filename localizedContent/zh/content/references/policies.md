---
uid: policies
title: 策略
author: Daniel Otykier
updated: 2024-10-30
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 策略

某些 IT 组织可能希望限制 Tabular Editor 的部分功能。 可以通过组策略实现：在 Windows 注册表中设置特定值。

> [!NOTE]
> 此功能需要以下版本的 Tabular Editor：
>
> - Tabular Editor 2 版本 [2.17.0](https://github.com/TabularEditor/TabularEditor/releases/tag/2.17.0) 或更高版本
> - Tabular Editor 3 版本 [3.3.5](https://github.com/TabularEditor/TabularEditor3/releases/tag/3.3.5) 或更高版本。

下表列出了可控制的策略。 要强制执行其中一项或多项策略，在该注册表项下添加一个非零的 DWORD 值即可。 该值的名称用于指定要强制执行的策略。

**注册表项：** HKEY_CURRENT_USER\Software\Policies\Kapacity\Tabular Editor\

| 值                              | 启用后……                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| DisableUpdates                 | Tabular Editor 不会在线检查是否有新版本可用。 此外，用户也无法通过该工具手动检查是否有更新。                                                                    |
| DisableCSharpScripts           | Tabular Editor 不允许用户创建并执行 C# Script。                                                                                      |
| DisableMacros                  | Tabular Editor 不允许用户保存或运行宏。 此外，定义在 %LocalAppData% 文件夹中的宏也不会在应用程序启动时加载并编译。                                                 |
| DisableBpaDownload             | Tabular Editor 不允许从网络下载 Best Practice Analyzer 规则。                                                                        |
| DisableWebDaxFormatter         | Tabular Editor 将禁用 DAX 代码格式化程序，该程序会向 daxformatter.com 发起 Web 请求。 （TE3 仍允许通过内置的 DAX 格式化程序来格式化代码）           |
| DisableErrorReports            | **（仅限 TE3）** Tabular Editor 不允许用户向 Tabular Editor 3 支持团队发送错误/崩溃 Report。                                                   |
| DisableTelemetry               | **（仅限 TE3）** Tabular Editor 不会收集并向 Tabular Editor 3 支持团队发送匿名使用数据。                                                         |
| DisableDaxOptimizer            | **（仅限 TE3）** DAX优化器集成功能将不可用                                                                                               |
| DisableDaxOptimizerUpload      | **（仅限 TE3）** 用户将无法通过 DAX优化器集成功能上传 VPAX 文件。 当强制执行 `DisableDaxOptimizer` 时，会隐式强制执行此项。                                       |
| RequireDaxOptimizerObfuscation | **（仅限 TE3）** 用户将无法通过 DAX优化器集成功能上传未混淆（明文）的 VPAX 文件。 当强制执行 `DisableDaxOptimizer` 或 `DisableDaxOptimizerUpload` 时，会隐式强制执行此项。 |
| DisableDaxPackageManager       | **（仅限 TE3）** DAX 组件管理器功能将不可用。                                                                                             |

## 禁用 Web 通信

如果你想确保 Tabular Editor 不执行 Web 请求，请指定 `DisableUpdates`、`DisableBpaDownload`、`DisableWebDaxFormatter`、`DisableErrorReports`、`DisableTelemetry` 和 `DisableDaxOptimizer` 策略。

> [!NOTE]
> 即使已指定上述策略，Tabular Editor 3 仍会偶尔向 `https://api.tabulareditor.com` 发起请求，用于许可证验证。 如果 Tabular Editor 3 无法访问此端点（由于防火墙或代理），用户将不得不每 30 天对产品进行一次[手动激活](xref:installation-activation-basic#manual-activation-no-internet)。

## 禁用自定义脚本

如果你想确保 Tabular Editor 不允许用户执行任意代码，请指定 `DisableCSharpScripts` 和 `DisableMacros` 策略。