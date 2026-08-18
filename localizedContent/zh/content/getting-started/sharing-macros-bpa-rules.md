---
uid: sharing-macros-bpa-rules
title: 在团队中共享宏、BPA 规则和偏好
author: Just Blindbæk
updated: 2026-07-06
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

Tabular Editor 会从每位用户计算机上的固定位置读取多个配置文件：Tabular Editor 3 使用 `%LOCALAPPDATA%\TabularEditor3\`，Tabular Editor 2 使用 `%LOCALAPPDATA%\TabularEditor\`。 其中最重要的是 [`MacroActions.json`](xref:supported-files#macroactionsjson)（用户的宏）、[`BPARules.json`](xref:supported-files#bparulesjson)（用户本地的 Best Practice Analyzer（BPA）规则）以及 `Preferences.json`（应用程序的常规偏好）。 有关这些文件以及其他本地设置文件的完整说明，见[支持的文件类型](xref:supported-files#local-setting-files)。

这种默认方式适用于单个开发人员。 如果团队希望在整个团队、某个部门，或本地开发与 CI 之间共享一致的宏或偏好，就会遇到一个很直接的问题：如何让固定本地路径中的文件与某个受版本控制且共享的内容保持同步？

![共享配置流示意图](~/content/assets/images/sharing-config-two-paths.png)

> [!NOTE]
> 如果你要共享的是 BPA 规则，这已经有现成的解决方案。 请参阅下方的[共享 BPA 规则](#sharing-bpa-rules)。 本页其余内容将介绍宏和偏好，它们目前还没有同样的原生支持。

## 从一个集中式 Git repository 开始

无论你用什么机制把文件放到开发者的电脑上，它都应该从一个专门用于共享配置的集中式 Git repository 拉取内容：宏，以及可选的共享基线 `Preferences.json`。 将该 Git repository 视为唯一可信来源，而不是某个开发者的电脑，这样共享才真正有意义：

- 对宏的更改可以通过 Pull Request 进行审查，就像审查语义模型的更改一样。
- 你可以完整追踪是谁在什么时间修改了哪个宏，也可以像回退其他任何提交一样回退一次错误的更改。
- 新团队成员只需克隆一个 repository，就能获取整个团队的宏库，无需从同事的电脑上拷贝文件。
- 同一个 repository 还可以兼作 BPA 规则集的来源（见下文），这样团队的共享标准就集中在一个地方，而不是分散在多个同步机制中。

## 与语义模型使用同一个 repository，还是单独一个 repository？

在选择同步机制之前，先确定共享的宏和 BPA 规则放在哪里：与语义模型放在同一个 repository 中，还是放在专用的 repository 中。

和你的语义模型放在同一个 repository 是更简单的默认选择，也是合适的起点。 宏和规则作为文件与模型并列存放，并一起进行版本控制。 按照 [GitHub Flow](xref:github-flow)，从 `main` 创建功能分支时，会自动带上当时的宏和规则，无需额外步骤。 分支机制本身就能保证内容是最新的，而你本来就会为每项工作创建分支。 对宏的修改和其他任何更改一样，也是通过一个功能分支和拉取请求来完成。 审阅者从差异中就能看出它只改动了宏的 `MacroActions.json`，因此不会搞混正在审阅的内容。

当你拥有多个彼此真正独立的语义模型 repository（例如不同团队或部门各自维护一个）时，使用单独的专用 repository 才更有意义。 如果不这么做，每个模型 repository 都需要各自保存一份共享宏和规则的副本。 维护这些副本的一致性会变成一个额外的手动问题，和集中管理原本要解决的问题正好相反。

即使在这种多团队场景下，也要先确认真正需要的是一个独立的宏 repository，还是一个可供本地增补的共享基线：例如先提供全组织通用的一套宏，再叠加某个部门自己的宏。 这属于多来源的问题，而不是“同一个 repository 还是单独的 repository”的问题。 BPA 规则集原生支持这种方式（参见上文的 [共享 BPA 规则](#sharing-bpa-rules)）。 对于宏，请参见下文的 [组合多个宏来源](#combining-multiple-macro-sources)。

如果你的团队目前只维护一个语义模型 repository，那么同一 repository 的做法是最简单的选择，暂时也不存在重复副本的问题。 不过也要想想一年后是否还是这样，因为以后再把共享宏从模型 repository 中迁出，会比一开始就把它们分开存放更费工夫。

无论你怎么选，下面介绍的同步机制工作方式都是一样的。 专用的宏 repository 只是意味着它们会从第二个 repository 中获取，而不是从你已经检出的那个 repository 中获取。

## 共享宏

宏的情况不同：Tabular Editor 每个用户只会从固定路径读取一个 `MacroActions.json` 文件，并没有与 BPA 规则集系统对应的机制。 有关该文件本身的结构，请参见 [宏视图参考](xref:macros-view-reference)。

> [!NOTE]
> **为什么没有内置的远程加载功能：** 原因是宏是 C# Script。 Tabular Editor 在设计上刻意不会从用户无法控制的外部位置下载或加载宏，例如网页、GitHub repository 或公开的“marketplace”。 如果没有用户明确执行某个步骤，就从远程源加载并执行任意代码，这会带来真正的安全风险。 任何共享机制都必须由用户或团队自行搭建和配置。

团队通常用这三种方法来弥合中央 repository 与 Tabular Editor 固定本地路径之间的差距。 这三种方法都是在你的 Git repository 与该固定本地路径之间移动 `MacroActions.json`——Tabular Editor 本身始终只读写本地副本，并没有 Git 这一层概念。 这些方案的区别在于：由谁执行这项移动、移动方向，以及由什么触发：

### 方案 A：符号链接

固定路径会变成指向你 repository 的链接，因此 Tabular Editor 会直接读写你工作副本中的 `MacroActions.json`。

```powershell
New-Item -ItemType SymbolicLink -Path "$env:LOCALAPPDATA\TabularEditor3\MacroActions.json" -Target "C:\path\to\your\repo\MacroActions.json"
```

（Tabular Editor 2 请使用 `%LOCALAPPDATA%\TabularEditor\`，而不是 `%LOCALAPPDATA%\TabularEditor3\`。）

- 双向：在 Tabular Editor 图形界面中所做的编辑会直接写入你的工作副本，可以像处理其他文件更改一样进行审查和提交。
- 仍然需要显式执行 `git pull`，才能拉取队友的更改。 符号链接省掉的是手动复制这一步，而不是与远程同步的需求。
- 在 Windows 上创建符号链接需要启用开发人员模式或使用提升权限的命令提示符，而在受严格管控的计算机上，这通常会被策略阻止。 在这种情况下，IT 可以在部署 Tabular Editor 时集中授予该权限（通过设备策略或 `SeCreateSymbolicLinkPrivilege` 权限），这样开发人员就无需自行提升权限。 开发人员克隆仓库后，可以用一个单独的小脚本来创建该链接。

### 方案 B：pre-commit 钩子

将一个已提交到 repository 中的 [Git pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) 配置为在每次提交时把 `MacroActions.json` 从 repository 复制到 `%LOCALAPPDATA%\TabularEditor3\`（Tabular Editor 2 为 `%LOCALAPPDATA%\TabularEditor\`）。

- 不需要提升权限或启用开发人员模式。 只需进行一次普通的文件复制即可，而且无论开发人员把仓库克隆到哪里都能正常工作。 源路径相对于仓库根目录；目标路径 `%LOCALAPPDATA%` 会按用户自动解析。
- 单向，而且是在提交时同步，不是在拉取时同步。 你最早也要等到队友的 PR 合并并且你自己拉取之后，才能看到他们的更改，所以除非你的分支长期没有同步 `main`，否则这通常不是问题。 如果真有这个问题，加一个 `post-merge` 或 `post-checkout` 钩子就能弥补这一缺口。
- 在 Tabular Editor 图形界面里做的编辑会一直留在本地，直到你手动把它复制回仓库并提交。 否则，下次钩子运行时它会被悄无声息地覆盖。

### 方案 C：执行 apply 时复制文件的工具

像 [chezmoi](https://www.chezmoi.io/) 这样的 dotfiles 管理器，通常就是用来解决这类问题的。 将文件保存在 repository 中，使用 `apply` 命令将其复制到目标位置，再用 `add` 命令把本地修改复制回去。 不会自动建立链接，也不会自动回写。

- 与方案 B 具有相同的实际收益（无需提升权限，也不依赖特定的本地克隆路径），但两个方向都要通过显式命令完成。有些团队比起符号链接的静默回写，更喜欢这种方式。
- 代价是要学习一个有自己概念体系的第三方工具；对单个 JSON 文件来说，这通常有点大材小用。 例外情况是：团队已经用这种方式管理开发者机器上的其他配置（例如共享的 VS Code 或 Git 配置）。这样一来，宏就只是你们已采用的那套体系中的又一个文件。

> [!NOTE]
> 这些都不是“唯一的”官方机制。 它们只是针对同一个问题的不同权衡。 选定一种并始终如一地使用，不要按文件混用不同机制。

### 合并多个宏来源

上面这三种方案都不能同时合并多个来源。 它们都只是把单个文件从一个位置移到另一个位置。 如果要把中央共享的一组宏与部门级或个人级宏合并，你需要在 Tabular Editor 读取文件之前，先用脚本将它们合并。 这只是变通办法，不是原生支持的功能：与 BPA 规则不同，宏没有原生的规则集机制。 尽量保持简单，让任何开发者都能看懂并修复它。

## 共享偏好设置

`Preferences.json` 与宏一样有相同的固定路径限制，且不原生支持多来源。 上面的三种方案对它都同样适用。

## 共享 BPA 规则

Tabular Editor 原生支持组合来自多个来源的 Best Practice Analyzer 规则，无需符号链接或变通办法：

- **规则集**允许模型使用来自当前模型、本地用户的 `BPARules.json`、计算机级别的 `BPARules.json`，以及你显式添加的任意数量的其他规则集中的规则。 这些附加来源可以是磁盘上其他位置的文件（支持相对于模型的路径，因此规则文件可以放在同一 repository 中）、网络共享，或 HTTP/HTTPS URL。 规则集具有明确的优先顺序，因此在需要时，可以在模型级别覆盖中央共享规则。 有关如何添加规则集并设定其优先级，请参阅 [管理最佳实践规则](xref:best-practice-analyzer#managing-best-practice-rules)。
- **内置规则**（Tabular Editor 3）在应用中直接内置提供一套经过精选、带版本管理的最佳实践规则，并会随每次发布自动更新；每条规则都附有指向相应知识库文章的链接。 它们会与你的自定义规则并存，而不是取而代之。 参见 [内置 BPA 规则](xref:built-in-bpa-rules)。

结合这两个功能，大多数“如何在团队内共享 BPA 规则”的场景都已有原生支持。 将共享规则文件提交到 repository，并通过相对路径、网络共享或 URL 将其作为规则集引入，通常就足够了。 无需 symlink 或 hook，因为 Tabular Editor 读取规则集时是直接读取，而不是通过固定的个人路径。

> [!NOTE]
> 因为规则集可以指向相对路径、网络共享或 URL，所以上述“同一 repository 还是单独 repository”的问题，对 BPA 规则而言远没有对宏那么重要。 无论规则文件位于哪个 repository，规则集的工作方式都一样，因为无需先将任何内容复制到固定的本地路径，或在该路径上创建 symlink。 这正是 BPA 原生多源支持相较于宏当前所需文件复制机制的一个实际优势。

### 该用哪种规则集类型

在添加外部规则集的三种方式中，大多数团队默认推荐选择在 repository 中通过相对路径引用文件，因为它具备另外两种方式所不具备的优势：

- 基于 URL 的规则集是只读的。 Tabular Editor 不允许编辑从 HTTP/HTTPS URL 加载的规则集。 对于像 Microsoft 的 [标准 Analysis Services BPA 规则](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules) 这种按原样使用的内容，这个限制是合理的。 但这也意味着，URL 不适合作为你们团队会持续主动编辑的规则集的存放位置：你需要在别处维护真实文件，再把该 URL 当作只读镜像，带来的额外环节往往得不偿失。
- 网络共享的前提是每台计算机都能访问同一个网络位置。 这适合本地部署或单办公室环境，但不太适合分布式团队、远程办公的人，或者无法挂载你们内部网络的云优先 CI/CD 流水线代理。
- 把规则文件放在语义模型自己的 Git repository 里，并用相对路径引用，可以同时避免这两个问题。 它完全可编辑，本质上就是 Git 仓库中的一个普通文件，可以像其他文件一样编辑和审查，而且不依赖任何特定的网络拓扑。 只要某台机器克隆了这个 Git 仓库，就会同时拿到该规则文件，无论是开发者的笔记本电脑还是 CI/CD 构建代理。

有一个值得注意的限制：只有当模型从磁盘加载时（即“保存到文件夹”模型），相对路径才能解析；如果 Tabular Editor 直接连接到实时的 Analysis Services 或 Power BI 实例，就无法解析相对路径。 对于基于 Git 和[保存到文件夹](xref:parallel-development#what-is-save-to-folder)的并行开发，这通常不是问题，因为模型始终位于磁盘上。 但如果团队中有人改为直接连接到实时 Workspace，最好确认一下这一点。

如果你们团队已经有一个共享且可访问的网络位置，而且不想为每个 Git 仓库单独引入一个文件，那么网络共享也是可行的替代方案。 它以可移植性为代价，换取你们现有文件共享设置所带来的便利。 预留一个基于 URL 的集合，用于使用外部只读规则集（例如 Microsoft 的标准规则），而非由你们团队维护的规则集。

## 总结

| 目标                       | 方式                                                                                                                                      |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| 确定共享宏/规则应存放的位置           | 如果你只维护一个这样的 repo，就与语义模型放在同一个 repo；如果你维护多个，则单独建一个专用 repo；请参阅[同一个 repo，还是单独的 repo？](#same-repo-as-your-semantic-model-or-a-separate-repo) |
| 在团队内共享 BPA 规则            | Git repository 中的相对路径文件集合（默认推荐选项）；请参阅[使用哪种集合类型](#which-collection-type-to-use)。 也可以使用网络共享或 URL 集合；请参阅链接的章节，了解其中的权衡。                     |
| 无需设置即可获得精选并持续维护的基线规则集    | [内置 BPA 规则](xref:built-in-bpa-rules) (TE3)                                                                           |
| 双向共享宏或偏好设置               | 符号链接（选项 A）。 要获取队友的更改，你仍需执行 `git pull`；在限制较多的机器上，可能还需要 IT 授予权限                                                                           |
| 共享宏或偏好，无需提升权限            | 预提交钩子（选项 B）：单向，仅在提交时同步，而不会在拉取时同步                                                                                                        |
| 共享宏或偏好，明确且可审查            | 类似 chezmoi 的 dotfiles 管理工具（选项 C）：要学的内容更多；如果你已经用它管理其他配置，这会是最合适的选择                                                                        |
| 合并多个宏来源（中心级 + 部门级 + 个人级） | 使用合并脚本将各个数组拼接到 Tabular Editor 读取的单个文件中；这是一种变通方案，不是内置功能                                                                                  |
| 从用户无法控制的位置加载宏            | 按设计不支持：宏是可执行代码                                                                                                                          |

## 后续步骤

- @best-practice-analyzer
- @built-in-bpa-rules
- @macros-view-reference
- @并行开发
