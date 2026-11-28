---
uid: tmdl
title: 表格模型定义语言（TMDL）
author: Daniel Otykier
updated: 2026-11-12
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          none: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 表格模型定义语言（TMDL）

**TMDL** 是一种模型元数据文件格式，[微软在 2023 年四月宣布](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-the-tabular-model-definition-language-tmdl/)。它旨在提供一种易于阅读的纯文本替代方案，作为基于 JSON 的 model.bim 文件格式的替代。 TMDL 的灵感来自 YAML，因此易读、易写，并且尽量减少字符串引号和转义字符的使用。它还会将模型序列化为文件夹结构中的多个较小文件，因此更适合与版本控制集成。

## 在 Tabular Editor 3 中将模型保存为 TMDL

如果**工具 > 首选项 > 文件格式 > 保存到文件夹**下的**保存到文件夹格式**为默认值**TMDL**，则**文件 > 保存到文件夹…**会将模型保存为 TMDL 文件夹。TMDL 格式化设置（例如缩进、编码和大写）位于**工具 > 首选项 > 文件格式 > 保存到文件夹 > TMDL 序列化**下。请参阅[偏好](xref:preferences#file-formats--save-to-folder--tmdl-serialization)。

> [!NOTE]
> 当您使用**文件 > 保存** (**Ctrl+S**) 时，从 Database.json 文件夹加载的模型将以该格式保存。使用**文件 > 保存到文件夹...**，并将**保存到文件夹格式**设置为**TMDL**，将其转换为 TMDL。

在 Tabular Editor 3 企业版中，TMDL 文件夹可以将每个列、度量值、分区和层次结构以及每个函数、共享表达式、数据源和关系存储在其各自的文件中。请参阅@tmdl-per-object-serialization。

## 新模型

**工具 > 首选项 > 文件格式 > 常规**下的**默认保存格式**设置控制首次保存新模型的方式。如果选择**始终询问**（默认），Tabular Editor 将要求您在 Model.bim 文件和 Database.json 或 TMDL 格式的文件夹之间进行选择。使用**TMDL**，新模型将保存为 TMDL 文件夹。

![新模型 Tmdl](~/content/assets/images/new-model-tmdl.png)

## TMDL 与 Microsoft Fabric Git 集成

TMDL 与 Microsoft Fabric 的 Git 集成功能完全兼容。在 Tabular Editor 3 中使用 **保存并包含支持文件** 选项时，TMDL 序列化格式会创建一个文件夹结构，其中包含 Fabric 的 Git 集成所需的全部元数据文件。

生成的文件夹结构包括：

- 包含元数据（显示名称、描述、逻辑 ID）的 **.platform** 文件
- 包含语义模型设置的 **definition.pbism** 文件
- 用于存放你的 TMDL 模型文件的 **definition/** 文件夹

此组合使你能够将语义模型提交到 Git repository，并使用 Fabric 内置的 Git 集成功能将其与 Microsoft Fabric Workspace 同步。 TMDL 采用人类可读的格式，尤其适合进行代码评审，并在版本控制系统中跟踪更改。

有关如何使用此功能的详细信息，请参阅[使用支持文件保存](xref:save-with-supporting-files)。

# 后续步骤

- [TMDL 概述（Microsoft Learn）](https://learn.microsoft.com/analysis-services/tmdl/tmdl-overview)。
- [TMDL 入门（Microsoft Learn）](https://learn.microsoft.com/analysis-services/tmdl/tmdl-how-to)
