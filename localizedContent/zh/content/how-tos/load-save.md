---
uid: load-save-model
title: 加载与保存模型元数据
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
          note: "Desktop Edition can't open or save model metadata files."
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 加载与保存模型元数据

Tabular Editor 可将模型元数据从文件、文件夹或服务器读取到内存中，并将其写回原位置或另存到新位置。

> [!NOTE]
> Metadata defines tables, measures and relationships but contains no data, and loading a model doesn't load the rows in its tables. See [Table Preview](xref:table-preview) and [Advanced refresh](xref:advanced-refresh) for working with data.

## 加载模型

![“文件”菜单，其中“打开”子菜单已展开，列出了“从文件打开模型”、“从数据库打开模型”、“从文件夹打开模型”、“文件”以及“从 Metric View YAML 导入”，并包含“保存”、“另存为”和“保存到文件夹”命令](~/content/assets/images/file-menu-open.png)

| 来源                                                                 | 命令                                                                                                                            |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `Model.bim` 或 `.bim` 文件                                            | **File > Open > Model from File...**                                          |
| 采用 JSON 或 [表格模型定义语言 (TMDL)](xref:tmdl) 格式的文件夹结构 | **File > Open > Model from Folder...**                                        |
| Analysis Services 或 Power BI XMLA 数据库                              | **文件 > 打开 > 从数据库打开模型...** (**Ctrl+Shift+O**)               |
| Power BI Desktop 的运行实例                                             | **文件 > 打开 > 从数据库打开模型...**，或从 Power BI Desktop 的 **外部工具** 功能区启动 Tabular Editor |

`.bim` 文件的兼容级别必须为 1200 或更高。更早的级别使用较旧的基于 XML 的格式，Tabular Editor 无法打开此类格式。

For everything Tabular Editor recognizes, including the supporting file types that aren't model metadata, see [Supported file types](xref:supported-files).

> [!TIP]
> **File > Recent Tabular Models** reopens a model you had open before.

## 保存模型

**文件 > 保存** (**Ctrl+S**) 会将模型保存回您加载它的位置。从文件加载的模型会写回到该文件。从文件夹加载的模型会以该文件夹当前使用的格式保存回该文件夹。从数据库加载的模型会部署回该数据库。

若要将模型写入其他位置，或改用其他格式：

- **文件 > 另存为...** 会将模型元数据保存为单个 `.bim` 文件。
- **File > Save to Folder...** saves the model metadata as a [folder structure](xref:save-to-folder), in either the JSON or the TMDL format, depending on the serialization mode under **Tools > Preferences > File Formats > Save-to-folder**.

> [!IMPORTANT]
> 从旧版 JSON 文件夹结构加载的模型，在使用 **文件 > 保存** 时会按相同格式保存，即使你的偏好中设置的是 TMDL。 The format changes only when you use **File > Save to Folder...**. 参见 [TMDL](xref:tmdl)。

## 重新加载

**File > Reload from disk** discards your changes since the last save and reloads the metadata from the source. If you have unsaved changes, a **Reload model metadata?** prompt appears first. The command label depends on the model source:

| Model source                                          | 命令                                                                                                                              |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| A file or folder                                      | **Reload from disk**                                                                                                            |
| A model in [workspace mode](xref:workspace-mode)      | **Reload from disk**. The model reloads from its files and redeploys to the workspace database. |
| Analysis Services or Power BI, outside workspace mode | **Reload from server**                                                                                                          |
| No model loaded                                       | **Reload from source**, disabled                                                                                                |

在 Tabular Editor 3.26 及更早版本，以及 Tabular Editor 2 中，该命令名为 **文件 > 还原**。

In Tabular Editor 3.27.0 and later, when an agent, a script or a `git pull` changes the metadata files of the open model, the model is reloaded, after a prompt if you have unsaved changes. 参见 [从磁盘自动重新加载](xref:auto-reload)。

> [!WARNING]
> 在让任何工具写入模型元数据之前（包括 Tabular Editor），请先备份。保存会覆盖源，重新加载无法找回你已保存的更改。

## 后续步骤

- [保存到文件夹](xref:save-to-folder)：了解文件夹格式，以及控制如何将模型拆分到多个文件中的序列化设置。
- 如果有多人共同处理这个模型，参见 [使用 Git 和保存到文件夹启用并行开发](xref:parallel-development)。
- [Deployment](xref:deployment) to write the model to an Analysis Services server.
