---
uid: auto-reload
title: 从磁盘自动重新加载
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      since: 3.27.0
      editions:
        - edition: Desktop
          none: true
          note: "桌面版无法打开或保存模型元数据文件。"
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 从磁盘自动重新加载

当你从文件或文件夹加载的模型的元数据文件在磁盘上发生变化时，Tabular Editor 会自动重新加载该模型。如果你有未保存的更改，会弹出提示，供你选择重新加载还是保留更改。外部更改的常见来源包括 AI 智能体、脚本、其他编辑器、执行 `git pull`，或同事在共享文件夹中编辑。

![图示：文件 > 保存会将 Tabular Editor 中的模型写入磁盘上的文件；另一个工具写入这些文件；自动重新加载再将已更改的文件加载回 Tabular Editor](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> 自动重新加载会监视文件，其行为不受 [工具 > 偏好 > Tabular Editor > 杂项](xref:preferences#miscellaneous) 下的 **跟踪外部模型更改** 和 **自动刷新本地 Tabular Object Model 元数据** 影响。这些设置使用 Analysis Services 跟踪来检测连接到的数据库中的更改。

## 监视的文件

| 模型加载来源                                                                               | 监视的文件                                                   |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------- |
| 一个`.bim`文件                                                                           | 该文件。同一文件夹中的其他文件会被忽略。                                    |
| 一个采用 JSON（Database.json）格式的文件夹                                       | 模型根目录下的每个 `.json` 文件，包括子文件夹中的文件。                        |
| 一个采用 [Tabular Model Definition Language (TMDL)](xref:tmdl) 格式的文件夹 | 模型根目录下的每个 `.tmdl` 文件，包括子文件夹。                            |
| 一个 Workspace 数据库                                                                     | 在[工作区模式](xref:workspace-mode)下，为模型提供支持的文件，遵循与上面各行相同的规则。 |
| 工作区模式之外的数据库或 Power BI Desktop                                                        | 无。该模型在磁盘上没有文件。                                          |
| 一个 `.pbit` 模板，或一个你从未保存过的模型                                                           | 无。                                                      |

## 有未保存更改时重新加载

如果你有未保存的更改，则会显示 **检测到外部更改** 提示。由于 Tabular Editor 不会合并这些更改，你需要选择保留哪个版本。

![“检测到外部更改”提示对话框，包含“重新加载”和“忽略”按钮，焦点位于“重新加载”](~/content/assets/images/features/external-changes-prompt.png)

- **重新加载** 会丢弃你未保存的更改，并加载磁盘上的版本。
- **忽略** 会保留你的更改。磁盘上的文件会保留这些外部更改，而你下一次保存会覆盖它们。

按 **Esc** 或关闭该提示的效果与 **忽略** 相同。

> [!WARNING]
> **重新加载** 是默认按钮，因此在提示中按 **Enter** 也会执行重新加载。重新加载会直接丢弃你未保存的更改，不会再进一步确认，而且无法撤销。

### 示例

1. 你打开一个 TMDL 文件夹模型，并重命名一个度量值。
2. 在同一文件夹中工作的 AI 代理重写了四个 `.tmdl` 文件。
3. 代理写入完成后，会出现一次 **检测到外部更改** 提示。
4. 你选择 **重新加载**，这会放弃该重命名并加载代理的更改。 TOM Explorer 会保留已展开的节点。

## 多次写入和后台更改

当某个工具重写以文件夹序列化的模型时，它会在短时间内连续更改多个文件，而 Tabular Editor 会在写入完成后统一重新加载一次。

如果文件发生更改时 Tabular Editor 不是活动窗口，则重新加载或提示会在你切换回它时出现。它处于非活动状态期间发生的所有更改都会合并为一次提示。

## 工作区模式

在[工作区模式](xref:workspace-mode)下，重新加载还会将模型重新部署到 Workspace 数据库中。

## 关闭此功能

自动重新加载默认启用。若要关闭，请在 **工具 > 偏好 > Tabular Editor > 杂项** 下取消勾选 **自动从磁盘重新加载（热重载）**。

![工具 > 偏好 > Tabular Editor > 杂项，显示“元数据同步”下的自动重新加载设置](~/content/assets/images/pref-miscellaneous.png)

如果某个持续运行的进程也会写入模型文件夹(例如文件同步客户端，或在后台刷新的 CI 检出副本)，建议将其关闭。每次更改都会触发一次重新加载；如果存在未保存的更改，则会弹出模态提示对话框。

取消选中此设置后，使用 **文件 > 从磁盘重新加载** 加载外部更改，或使用 **文件 > 保存** 用 Tabular Editor 中的模型覆盖它们。有关该页面上的其他设置，请参阅[偏好](xref:preferences#miscellaneous)。
