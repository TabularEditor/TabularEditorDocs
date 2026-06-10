---
uid: te-cli
title: Tabular Editor CLI（有限公开预览）
author: Peer Grønnerup
updated: 2026-05-12
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      none: true
    - product: Tabular Editor CLI
      full: true
---

# Tabular Editor CLI（有限公开预览）

Tabular Editor CLI (`te`) 是适用于 Power BI 和 Analysis Services 语义模型的跨平台命令行工具。 它以单个自包含的可执行文件形式在 Windows、macOS 和 Linux 上运行，并基于驱动 Tabular Editor 3 的同一基础构建。

使用 Tabular Editor CLI，你可以在终端中检查、编辑、验证、部署、刷新和测试语义模型——可针对本地 TMDL 或 BIM 文件、Power BI Desktop，或 Fabric 和 Power BI Service Workspace 中的语义模型。

与仅限 Windows 的 `TabularEditor.exe` 命令行选项（TE2）不同——后者主要用于从桌面端二进制文件自动执行 C# Script 和宏——`te` 是专为跨平台打造的 CLI，提供结构化输出、可预测的退出代码以及交互式 shell。 这让现有的 [TE2 CLI](xref:command-line-options) 难以很好覆盖的场景成为可能：在 macOS 和 Linux 上通过终端完成模型工作、由 AI 代理直接驱动模型更改，以及无缝接入任何现代 CI 运行器。

[!INCLUDE [te-cli-preview-notice](includes/te-cli-preview-notice.md)]

## 面向三类受众打造

每个命令都围绕三大设计支柱构建：

- **结构化输出** — 除默认的可读文本外，还支持 JSON、CSV、TMDL 和 TMSL。
- **非交互模式** — 全局 `--non-interactive` 标志可禁用提示并快速失败。
- **清晰的错误信息** — 写入 stderr，并使用可预测的退出代码。

这三者结合起来，让同一个二进制文件能够很好地服务于三类截然不同的用户：

- **人** — 用脚本批量编辑、在终端中探索模型，并在 shell 管道中组合命令。
- **AI 代理** — 更节省 token 的 JSON、机器可解析的错误结构，以及无需解析 stdout 就能表明成功或失败的退出代码。
- **CI/CD 管道** — 非交互式执行、GitHub Actions 和 Azure DevOps 注释，以及兼容 VSTEST 的测试结果。

> [!Note]
> 当与代理配合使用 TE CLI 时，请使用面向 AI 编码代理的 TE CLI [skill](https://github.com/TabularEditor/CLI/tree/main/skill)，它对 TE CLI 进行了端到端封装。

## CLI 可以做什么

CLI 将 50 多个命令划分为 10 个类别。 每个命令族都对应语义模型生命周期中的一个具体阶段。

有关每个命令的语法、选项和示例的完整命令参考，请参阅 @te-cli-commands。 点击表中的任意示例命令，直接跳转到对应的参考条目。

| 命令族                                                  | 功能                        | 示例命令                                                                                                                                                                                  |
| ---------------------------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [模型 I/O](xref:te-cli-commands#model-io)              | 加载、保存、转换和初始化模型            | [`te load`](xref:te-cli-commands#load)、[`te save`](xref:te-cli-commands#save)、[`te init`](xref:te-cli-commands#init)                                                                  |
| [模型编辑](xref:te-cli-commands#model-editing)           | 获取/设置属性，添加/删除/移动对象        | [`te set`](xref:te-cli-commands#set)、[`te add`](xref:te-cli-commands#add)、[`te rm`](xref:te-cli-commands#rm)、[`te mv`](xref:te-cli-commands#mv)                                       |
| [检视](xref:te-cli-commands#inspection)                | 列出对象、搜索、比较差异、分析依赖关系       | [`te ls`](xref:te-cli-commands#ls)、[`te find`](xref:te-cli-commands#find)、[`te diff`](xref:te-cli-commands#diff)、[`te deps`](xref:te-cli-commands#deps)                               |
| [分析与质量](xref:te-cli-commands#analysis-and-quality)   | 验证、运行 BPA、格式化 DAX、分析存储    | [`te validate`](xref:te-cli-commands#validate)、[`te bpa run`](xref:te-cli-commands#bpa-run)、[`te format`](xref:te-cli-commands#format)、[`te vertipaq`](xref:te-cli-commands#vertipaq) |
| [执行](xref:te-cli-commands#execution)                 | 运行 DAX 查询、C# Script 和宏    | [`te query`](xref:te-cli-commands#query), [`te script`](xref:te-cli-commands#script), [`te 宏`](xref:te-cli-commands#macro)                                                            |
| [部署与刷新](xref:te-cli-commands#deployment-and-refresh) | 部署到 Workspace、触发刷新、执行增量刷新 | [`te deploy`](xref:te-cli-commands#deploy)、[`te refresh`](xref:te-cli-commands#refresh)、[`te incremental-refresh`](xref:te-cli-commands#incremental-refresh)                          |
| [测试](xref:te-cli-commands#testing)                   | 断言测试、快照、A/B 比较            | [`te test run`](xref:te-cli-commands#test-run)                                                                                                                                        |
| [连接和身份验证](xref:te-cli-commands#connection-and-auth)  | 连接到 Workspace，管理身份验证和配置文件 | [`te connect`](xref:te-cli-commands#connect), [`te auth`](xref:te-cli-commands#auth-login--status--logout), [`te profile`](xref:te-cli-commands#profile-list--show--set--remove)      |
| [配置](xref:te-cli-commands#configuration)             | 设置与许可                     | [`te config`](xref:te-cli-commands#config-show--paths--init--set)                                                                                                                     |
| [Shell](xref:te-cli-commands#shell)                  | 交互模式、Shell 自动补全           | [`te interactive`](xref:te-cli-commands#interactive), [`te completion`](xref:te-cli-commands#completion)                                                                              |

## 开始使用

1. **注册或登录**：前往 [tabulareditor.com](https://tabulareditor.com/download-tabular-editor-cli) 注册 Tabular Editor 帐户或登录。
2. **下载并安装**：Windows、macOS 和 Linux 的说明见 @te-cli-install。
3. **进行身份验证**：运行 `te auth login`，即可连接到 Power BI 或 Fabric。 见 @te-cli-auth。
4. **运行第一个命令**：`te --help` 会列出所有命令；`te <command> --help` 会显示详细选项。

初次查看实时模型只需两条命令：

```bash
te auth login
te ls -s MyWorkspace -d MyModel
```

![Tabular Editor CLI te ls 示例输出](~/content/assets/images/features/cli/cli-command-ls.png)

## 预览提示

默认情况下，每个命令都会在 stderr 中输出一个黄色的预览横幅：

![Tabular Editor CLI 预览提示横幅](~/content/assets/images/features/cli/cli-preview-notice.png)

要隐藏预览提示，只需运行：

```bash
te config set hidePreviewNotice true
```

> [!WARNING]
> 在预览结束日期（2026-09-30）前 14 天内，无论 `hidePreviewNotice` 如何设置，每次执行命令时该横幅都会再次出现。 这可确保在 CLI 停止运行之前，你能提前看到醒目的警告。

## 许可概览

在有限公开预览期间，CLI 无需许可证；你只需要一个 Tabular Editor 账户即可下载。 在正式发布 (GA) 时，CLI 将需要许可证；定价仍在最终敲定中，并会在 GA 前公布。

## 反馈与社区

在预览期间，Bug Report、功能请求和一般讨论都在 GitHub 上的公开 [TabularEditor/CLI](https://github.com/TabularEditor/CLI) repository 中进行：

- **Issues** - 用于 Report bug、提出功能请求，并跟踪已知问题。
- **Discussions** - 提问、分享反馈，并和其他早期用户交流使用技巧。

这个 repository 不托管 CLI 源代码；设立它是为了让社区在预览期间能通过一个公开渠道联系到我们。

## 后续步骤

- @te-cli-install - 下载、安装、验证。
- @te-cli-auth - 对 Power BI、Fabric 和 Azure Analysis Services 进行身份验证。
- @te-cli-commands - 完整命令参考。
- @te-cli-config - 配置文件和路径覆盖。
- @te-cli-interactive - 面向新用户的引导式 REPL 模式。
- @te-cli-automation - 结构化输出，以及适用于 Python、PowerShell 和 Bash 的脚本编写模式。
- @te-cli-cicd - GitHub Actions 和 Azure DevOps 管道示例。
- @te-cli-migrate - 从 Tabular Editor 2 命令行迁移。
