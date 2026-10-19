---
uid: load-save-model
title: 加载和保存模型元数据
author: Morten Lønskov
updated: 2026-10-11
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
# 加载和保存模型元数据

Tabular Editor 从文件、文件夹或服务器将模型元数据读取到内存中，然后将其写回同一位置或新位置。

> [!NOTE]
> 元数据定义了表、度量值和关系，但不包含数据，加载模型时不会加载其表中的行。有关处理数据的信息，请参阅[表格预览](xref:table-preview)和[高级刷新](xref:advanced-refresh)。

## 加载模型

![“文件”菜单，其中“打开”子菜单已展开，列出了“从文件导入模型”、“从数据库导入模型”、“从文件夹导入模型”、“文件”和“从指标视图 YAML 导入”，以及“保存”、“另存为”和“保存到文件夹”命令](~/content/assets/images/file-menu-open.png)

| 来源 | 命令 |
|---|---|
| “Model.bim”或“.bim”文件 | **文件 > 打开 > 从文件打开模型…** |
| JSON 或 [表格模型定义语言 (TMDL)](xref:tmdl) 格式的文件夹结构 | **文件 > 打开 > 从文件夹打开模型…** |
| Analysis Services 或 Power BI XMLA 数据库 | **文件 > 打开 > 从数据库打开模型…** (**Ctrl+Shift+O**) |
| 正在运行的 Power BI Desktop 实例 | **文件 > 打开 > 从数据库打开模型…**，或从 Power BI Desktop 的**外部工具**功能区启动 Tabular Editor |

“.bim”文件的兼容级别必须为 1200 或更高。较早的级别使用较旧的基于 XML 的格式，Tabular Editor 无法打开该格式。

有关 Tabular Editor 识别的所有内容（包括并非模型元数据的支持文件类型），请参阅[支持的文件类型](xref:supported-files)。

> [!TIP]
> **文件 > 最近的表格模型**可重新打开您之前打开过的模型。

## 保存模型

**文件 > 保存** (**Ctrl+S**) 将模型写回您从中加载模型的位置。从文件加载的模型将保存回该文件。从文件夹加载的模型将以其已使用的格式保存回该文件夹。从数据库加载的模型将部署回该数据库。

要将模型写入其他位置或以其他格式写入，请执行以下操作：

- **文件 > 另存为…**将模型元数据保存为单个“.bim”文件。
- **文件 > 保存到文件夹…** 将模型元数据保存为[文件夹结构](xref:save-to-folder)，格式为 JSON 或 TMDL，具体取决于**工具 > 首选项 > 文件格式 > 保存到文件夹**下的序列化模式。

> [!IMPORTANT]
> 当您使用**文件 > 保存**时，从旧版JSON文件夹结构加载的模型将以相同的格式保存，即使您的首选项显示为TMDL。只有在使用**文件 > 保存到文件夹…**时，格式才会发生变化。请参阅[TMDL](xref:tmdl)。

## 重新加载

**文件 > 从磁盘重新加载**将放弃您自上次保存以来的更改，并从源重新加载元数据。如果您有未保存的更改，则会首先出现**重新加载模型元数据？**提示。命令标签取决于模型源：

| 模型源 | 命令 |
|---|---|
| 文件或文件夹 | **从磁盘重新加载** |
| [工作区模式](xref:workspace-mode)下的模型 | **从磁盘重新加载**。模型将从其文件重新加载，并重新部署到工作区数据库。|
| Analysis Services 或 Power BI，非工作区模式 | **从服务器重新加载** |
| 未加载模型 | **从源重新加载**，禁用 |

在 Tabular Editor 3.26 及更早版本以及 Tabular Editor 2 中，该命令称为**文件 > 还原**。

在 Tabular Editor 3.27.0 及更高版本中，当代理、脚本或“git pull”更改打开的模型的元数据文件时，系统会提示您是否存在未保存的更改，然后重新加载模型。请参阅[从磁盘自动重新加载](xref:auto-reload)。

打开的 DAX 查询和 Pivot Grid 文档在手动或自动重新加载过程中保持打开状态，并连接到重新加载的模型。

> [!WARNING]
> 在允许任何工具（包括 Tabular Editor）写入模型元数据之前，请先备份模型元数据。保存操作会覆盖源，重新加载无法恢复您已保存的更改。

## 后续步骤

- [保存到文件夹](xref:save-to-folder)，了解文件夹格式和控制模型如何在多个文件之间拆分的序列化设置。
- 如果有多人处理模型，请参阅[使用 Git 和“保存到文件夹”功能实现并行开发](xref:parallel-development)。
- [部署](xref:deployment)以将模型写入 Analysis Services 服务器。
