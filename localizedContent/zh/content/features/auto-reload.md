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
          note: "Desktop Edition can't open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 从磁盘自动重新加载

When the metadata files of a model you loaded from a file or folder change on disk, Tabular Editor reloads the model automatically. If you have unsaved changes, a prompt appears where you choose to reload or keep your changes. Typical sources of external changes are an AI agent, a script, another editor, a `git pull` or a colleague editing a shared folder.

![Diagram: File > Save writes the model in Tabular Editor to the files on disk; another tool writes to the files; an automatic reload loads the changed files back into Tabular Editor](~/content/assets/images/features/auto-reload-sync.png)

> [!NOTE]
> Auto-reload monitors files and is independent of **Track external model changes** and **Refresh local Tabular Object Model metadata automatically** under [Tools > Preferences > Tabular Editor > Miscellaneous](xref:preferences#miscellaneous). Those settings use an Analysis Services trace to detect changes to a connected database.

## Monitored files

| 模型加载来源                                                                               | Monitored files                                                                                                            |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| 一个`.bim`文件                                                                           | That file. 同一文件夹中的其他文件会被忽略。                                                                                |
| 一个采用 JSON（Database.json）格式的文件夹                                       | 模型根目录下的每个 `.json` 文件，包括子文件夹中的文件。                                                                                           |
| 一个采用 [Tabular Model Definition Language (TMDL)](xref:tmdl) 格式的文件夹 | 模型根目录下的每个 `.tmdl` 文件，包括子文件夹。                                                                                               |
| 一个 Workspace 数据库                                                                     | The files backing the model in [workspace mode](xref:workspace-mode), by the same rules as the rows above. |
| 工作区模式之外的数据库或 Power BI Desktop                                                        | 无。 The model has no files on disk.                                                                         |
| 一个 `.pbit` 模板，或一个你从未保存过的模型                                                           | 无。                                                                                                                         |

## Reload with unsaved changes

If you have unsaved changes, the **External changes detected** prompt appears and you choose which version to keep, because Tabular Editor doesn't merge them.

![External changes detected prompt with the Reload and Ignore buttons, Reload focused](~/content/assets/images/features/external-changes-prompt.png)

- **Reload** discards your unsaved changes and loads the version on disk.
- **Ignore** keeps your changes. The files on disk keep the external changes, and your next save overwrites them.

Pressing **Esc** or closing the prompt has the same effect as **Ignore**.

> [!WARNING]
> **Reload** is the default button, so pressing **Enter** at the prompt also reloads. A reload discards your unsaved changes without further confirmation, and you can't undo it.

### 示例

1. 你打开一个 TMDL 文件夹模型，并重命名一个度量值。
2. 在同一文件夹中工作的 AI 代理重写了四个 `.tmdl` 文件。
3. After the agent's writes finish, one **External changes detected** prompt appears.
4. You choose **Reload**, which discards the rename and loads the agent's changes. The TOM Explorer keeps its expanded nodes.

## Multiple writes and background changes

When a tool rewrites a folder-serialized model, it changes many files in quick succession, and Tabular Editor reloads once, after the writes finish.

If Tabular Editor isn't the active window when the files change, the reload or prompt happens when you switch back to it. All changes made while it was inactive produce one prompt.

## 工作区模式

In [workspace mode](xref:workspace-mode), a reload also redeploys the model to the workspace database.

## 关闭此功能

Auto-reload is enabled by default, and you turn it off by clearing **Automatically reload from disk (hot reload)** under **Tools > Preferences > Tabular Editor > Miscellaneous**.

![Tools > Preferences > Tabular Editor > Miscellaneous, showing the automatic reload setting under Metadata Synchronization](~/content/assets/images/pref-miscellaneous.png)

Turn it off if a continuously running process also writes to the model folder, such as a file sync client or a CI checkout that refreshes in the background. Each change triggers a reload, or the modal prompt when you have unsaved changes.

With the setting cleared, use **File > Reload from disk** to load external changes, or **File > Save** to overwrite them with the model in Tabular Editor. See [Preferences](xref:preferences#miscellaneous) for the other settings on that page.
