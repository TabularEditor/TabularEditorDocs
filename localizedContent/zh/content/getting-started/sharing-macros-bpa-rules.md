---
uid: sharing-macros-bpa-rules
title: 在团队中共享宏、BPA 规则和偏好
author: Just Blindbæk
updated: 2026-09-23
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

# 在团队中共享宏、BPA 规则和偏好

Tabular Editor 会从每位用户计算机上的固定位置读取多个配置文件：Tabular Editor 3 使用 `%LOCALAPPDATA%\TabularEditor3\`，Tabular Editor 2 使用 `%LOCALAPPDATA%\TabularEditor\`。其中最重要的是 [`MacroActions.json`](xref:supported-files#macroactionsjson)（用户的宏）、[`BPARules.json`](xref:supported-files#bparulesjson)（用户本地的 Best Practice Analyzer（BPA）规则）以及 `Preferences.json`（应用程序的常规偏好）。有关这些文件以及其他本地设置文件的完整说明，见[支持的文件类型](xref:supported-files#local-setting-files)。

本页介绍团队、部门或 CI 管道如何将这些固定路径下的文件与一份共享且受版本控制的副本保持同步。

![共享配置流示意图](~/content/assets/images/sharing-config-two-paths.png)

> [!NOTE]
> BPA 规则原生支持共享源，详见 [共享 BPA 规则](#sharing-bpa-rules)。本页其余内容将介绍宏和偏好。

## 从一个集中式 Git repository 开始

将共享宏以及可选的共享偏好基线 `Preferences.json` 集中存放在一个中央 Git repository 中，并将其作为唯一可信来源。无论使用哪种机制将这些文件复制到开发人员的计算机上，都应从该 repository 拉取，从而：

- 宏的更改会像语义模型的更改一样，通过拉取请求提交
- 提交历史会显示谁在何时修改了哪个宏；你也可以像回退其他任何提交一样回退一次不当更改
- 新团队成员只需克隆一个 repository，就能获得团队的宏库
- 同一个 repository 还可以存放团队的 BPA 规则集（见 [共享 BPA 规则](#sharing-bpa-rules)），把共享标准集中在一处

## 与语义模型使用同一个 repository，还是单独一个 repository？

在选择同步机制之前，先确定共享的宏和 BPA 规则放在哪里：是和语义模型放在同一个 repository 中，还是放在专用 repository 中。

优先从语义模型的 repository 开始；在这种方式下，宏和规则作为与模型并列的文件存在，并一起进行版本控制。按照 [GitHub Flow](xref:github-flow)，从 `main` 创建的功能分支会包含当时最新的宏和规则，无需额外步骤。对宏的修改也同样通过功能分支和拉取请求完成，diff 会显示它只改动了 `MacroActions.json`。

当你有多个彼此独立的语义模型 repository 时，例如每个团队或部门一个，就使用单独的专用 repository。如果不这么做，每个模型 repository 都需要各自保存一份共享宏和规则的副本，而且这些副本还得靠手动保持同步。

在这种多团队场景下，也要确认你需要的是一个统一的共享宏 repository，还是一个允许本地补充的共享基线，例如先提供一套全组织通用的宏，再叠加某个部门自己的宏。 BPA 规则集原生支持多个源（见 [共享 BPA 规则](#sharing-bpa-rules)）；关于宏，见 [合并多个宏源](#combining-multiple-macro-sources)。

如果你的团队只维护一个语义模型 repository，就使用同一 repository 的方式。如果你预计一年内会增加更多模型 repository，最好从单独的 repository 开始：以后再把共享宏从模型 repository 中迁出，工作量会更大。

下面的同步机制在这两种设置中的工作方式相同。在使用专用的宏 repository 时，它们会指向另一份克隆副本。

## 共享宏

宏的情况不同：Tabular Editor 每个用户只会从固定路径读取一个 `MacroActions.json` 文件，而宏并没有与 BPA 规则集对应的机制。有关该文件的结构，见 [宏视图参考](xref:macros-view-reference)。

> [!NOTE]
> Tabular Editor 不会从网页、GitHub repository、应用市场或任何其他远程位置下载或加载宏。宏本质上是 C# Script，因此无论采用哪种共享机制，都需要由你或你的团队自行搭建并维护。

Tabular Editor 只会读取和写入本地的 `MacroActions.json` 副本，且不提供对该文件的 Git 集成。下面每个方案都会在你的 Git repository 与固定的本地路径之间移动该文件。它们的区别在于：由什么执行这项移动、往哪个方向移动，以及由什么触发。

### 方案 A：符号链接

将固定路径中的文件替换为指向 repository 中该文件的符号链接。这样一来，Tabular Editor 读取和写入的就是你的 `MacroActions.json` 工作副本。

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

（Tabular Editor 2 请使用 `%LOCALAPPDATA%\TabularEditor\`，而不是 `%LOCALAPPDATA%\TabularEditor3\`。）

- 该链接是双向的：在 Tabular Editor UI 中所做的编辑会写入你的工作副本，便于审查和提交。
- 你仍然需要运行 `git pull` 来获取队友的更改。
- 在 Windows 上创建符号链接需要启用开发人员模式或使用提升权限的命令提示符，而在受管控的计算机上，这通常会被策略阻止。在部署 Tabular Editor 时，IT 可以集中授予该权限（通过设备策略或 `SeCreateSymbolicLinkPrivilege` 权限），开发者克隆 repository 后再运行一个小脚本创建该链接。

### 方案 B：pre-commit 钩子

一个已提交到 repository 的 [Git pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) 会在每次提交时，将 `MacroActions.json` 从 repository 复制到 `%LOCALAPPDATA%\TabularEditor3\`（Tabular Editor 2 为 `%LOCALAPPDATA%\TabularEditor\`）。

- 不需要提升权限或启用开发人员模式。源路径相对于 repository 根目录，而 `%LOCALAPPDATA%` 会按用户分别解析。无论开发者把 repository 克隆到哪里，这个 hook 都能生效。
- 这种复制是单向的，而且会在提交时执行。队友的更改会在其拉取请求合并后，于你拉取 `main` 时同步到你这里。如果你的分支长时间不拉取 `main`，可以再加一个 `post-merge` 或 `post-checkout` hook。
- 在 Tabular Editor UI 中做出的修改会一直保留在本地，直到你把这些修改复制回 repository 并提交。否则，hook 会在下一次提交时覆盖它。

### 方案 C：执行 apply 时复制文件的工具

像 [chezmoi](https://www.chezmoi.io/) 这样的 dotfiles 管理器会将文件保存在 repository 中，使用 `apply` 命令将其复制到目标位置，再用 `add` 命令将本地修改复制回 repository。不会自动回写更改。

- 和方案 B 一样，它不需要提升权限，也不依赖特定的克隆路径。两个方向都需要显式执行命令。
- 你得为这一个 JSON 文件学会使用第三方工具。如果你的团队已经用这种方式管理开发者机器上的其他配置（例如共享的 VS Code 或 Git 配置），那么宏就只是这套体系中的另一个文件。

> [!NOTE]
> 这些方案都不是官方机制，因此请选择其中一种，并在所有共享文件中统一使用。

### 合并多个宏来源

上述每种方案都只能移动一个文件，而宏本身不支持多来源。要将一组集中管理的宏与部门或个人的宏组合使用，请编写脚本，在 Tabular Editor 读取 `MacroActions.json` 之前先合并这些文件。脚本尽量保持简单，确保团队里的任何开发者都能看懂并修复。

## 共享偏好设置

与宏一样，偏好设置文件 `Preferences.json` 也使用固定路径，并且不原生支持多来源。上面的三种方案对它都适用。

## 共享 BPA 规则

Tabular Editor 原生支持从多个来源组合 Best Practice Analyzer 规则：

- **规则集**：模型会使用来自当前模型、本地用户的 `BPARules.json`、计算机级别的 `BPARules.json` 以及你添加的任何其他规则集中的规则。额外的规则集可以是磁盘上的文件、网络共享，或 HTTP/HTTPS URL。文件路径可以使用相对于模型的相对路径，这样规则文件就可以放在模型的 repository 中。规则集有优先顺序，模型级别的规则会覆盖中央共享规则。参见 [添加规则集](xref:best-practice-analyzer#adding-a-rule-collection)。
- **内置规则**（Tabular Editor 3）：应用随附一套带版本管理的最佳实践规则，会随每次发布更新，并且每条规则都链接到一篇知识库文章。它们会与你的自定义规则一同运行。参见 [内置 BPA 规则](xref:built-in-bpa-rules)。

把 repository 中的共享规则文件通过相对路径、网络共享或 URL 添加为规则集，就能满足大多数团队场景。 Tabular Editor 会直接读取该规则集，因此无需符号链接或钩子；上文关于使用同一 repository 还是独立 repository 的选择，对 BPA 规则影响也很小。

### 该用哪种规则集类型

对大多数团队来说，最好把规则文件放在语义模型的 Git repository 中，并通过相对路径引用：

- **URL**：Tabular Editor 不允许编辑从 HTTP/HTTPS URL 加载的规则集。对于按原样使用的规则集，使用 URL 很合适，例如 Microsoft 的 [标准 Analysis Services BPA 规则](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules)。对于需要由团队编辑的规则，就在其他位置维护该文件，并把这个 URL 作为只读镜像发布。
- **网络共享**：每台计算机都需要访问同一个网络位置。这适用于本地部署或单办公室环境，但不适用于远程开发者，或无法访问内部网络的云托管 CI/CD 代理。
- **相对路径**：规则文件就是 repository 中的普通文件，可像其他文件一样编辑和评审。所有克隆了该 repository 的计算机(包括 CI/CD 构建代理)都会拥有该规则文件。

只有在从磁盘加载模型时，相对路径才会生效（即“保存到文件夹”模型）。当 Tabular Editor 直接连接到 Analysis Services 或 Power BI 实例时，这些内容无法解析。使用 Git 并配合 [保存到文件夹](xref:parallel-development#what-is-save-to-folder) 进行并行开发时，模型是从磁盘加载的，因此这只会影响直接连接到实时 Workspace 的团队成员。

如果你的团队已经有一个每台计算机都可访问的共享网络位置，也可以使用网络共享。

## 总结

| 目标                       | 方式                                                                                                                                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- |
| 确定共享宏/规则应存放的位置           | 如果只维护一个语义模型 repo，就与语义模型使用同一个 repo；如果维护多个，则使用单独的专用 repo。参见[同一个 repo，还是单独的 repo？](#same-repo-as-your-semantic-model-or-a-separate-repo) |
| 在团队内共享 BPA 规则            | Git repository 中基于相对路径的文件集合。关于网络共享和 URL 集合，参见[应使用哪种集合类型](#which-collection-type-to-use)                                               |
| 无需任何设置即可获得持续维护的基线规则集     | [内置 BPA 规则](xref:built-in-bpa-rules)（Tabular Editor 3）                                                                                |
| 双向共享宏或偏好设置               | 符号链接（选项 A）。需要执行 `git pull` 获取队友的更改，并具备创建符号链接的权限                                                                                       |
| 共享宏或偏好，无需提升权限            | 预提交钩子（选项 B）。单向；在提交时同步                                                                                                                 |
| 通过明确的命令来共享宏或偏好设置         | 像 chezmoi 这样的 dotfiles 管理器（选项 C）。如果你的团队已经用它管理其他配置，那么这是最佳选择                                                                            |
| 合并多个宏来源（中心级 + 部门级 + 个人级） | 一个合并脚本，用于将这些数组合并成 Tabular Editor 读取的单个文件                                                                                              |
| 从用户无法控制的位置加载宏            | 不支持。宏是可执行代码                                                                                                                           |

## 后续步骤

- @best-practice-analyzer
- @built-in-bpa-rules
- @macros-view-reference
- @并行开发
