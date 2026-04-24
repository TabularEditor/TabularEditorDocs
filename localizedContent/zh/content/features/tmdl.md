---
uid: tmdl
title: 表格模型定义语言（TMDL）
author: Daniel Otykier
updated: 2023-05-22
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

**TMDL** 是一种模型元数据文件格式，[微软在 2023 年四月宣布](https://powerbi.microsoft.com/en-us/blog/announcing-public-preview-of-the-tabular-model-definition-language-tmdl/)。 它旨在提供一种易于阅读的纯文本替代方案，作为基于 JSON 的 model.bim 文件格式的替代。 TMDL 的灵感来自 YAML，因此易读、易写，并且尽量减少字符串引号和转义字符的使用。 它还会将模型序列化为文件夹结构中的多个较小文件，因此更适合与版本控制集成。 它旨在提供一种易于阅读的纯文本替代方案，作为基于 JSON 的 model.bim 文件格式的替代。 TMDL 的灵感来自 YAML，因此易读、易写，并且尽量减少字符串引号和转义字符的使用。 它还会将模型序列化为文件夹结构中的多个较小文件，因此更适合与版本控制集成。

## 在 Tabular Editor 3 中启用 TMDL

要在 Tabular Editor 3 中启用 TMDL，请前往 **工具 > 偏好 > 文件格式 > 保存到文件夹**，然后在 **序列化模式** 下拉列表中选择“TMDL”。 旧版“保存到文件夹”功能将继续与 TMDL 并存，但它不是 Microsoft 支持的格式。 旧版“保存到文件夹”功能将继续与 TMDL 并存，但它不是 Microsoft 支持的格式。

完成后，当你将模型保存为文件夹（**文件 > 保存到文件夹...**）时，Tabular Editor 3 将使用 TMDL 格式。

> [!NOTE]
> 当你从旧版 Tabular Editor 文件夹结构加载模型时，使用 **文件 > 保存**（Ctrl+S）仍将以相同的格式保存。 只有在你明确使用 **文件 > 保存到文件夹...** 命令时，模型才会以新的 TMDL 格式保存。 只有在你明确使用 **文件 > 保存到文件夹...** 命令时，模型才会以新的 TMDL 格式保存。

## 新模型

首次保存新模型时，Tabular Editor (自 v. 3.7.0 起) 现在会提供将模型保存为 TMDL 的选项，即使默认序列化模式未设置为 TMDL，如上一节所述。

![新模型 Tmdl](~/content/assets/images/new-model-tmdl.png)

## TMDL 与 Microsoft Fabric Git 集成

TMDL 与 Microsoft Fabric 的 Git 集成功能完全兼容。 TMDL 与 Microsoft Fabric 的 Git 集成功能完全兼容。 在 Tabular Editor 3 中使用 **保存并包含支持文件** 选项时，TMDL 序列化格式会创建一个文件夹结构，其中包含 Fabric 的 Git 集成所需的全部元数据文件。

生成的文件夹结构包括：

- 包含元数据（显示名称、描述、逻辑 ID）的 **.platform** 文件
- 包含语义模型设置的 **definition.pbism** 文件
- 用于存放你的 TMDL 模型文件的 **definition/** 文件夹

此组合使你能够将语义模型提交到 Git repository，并使用 Fabric 内置的 Git 集成功能将其与 Microsoft Fabric Workspace 同步。 TMDL 采用人类可读的格式，尤其适合进行代码评审，并在版本控制系统中跟踪更改。 TMDL 采用人类可读的格式，尤其适合进行代码评审，并在版本控制系统中跟踪更改。

有关如何使用此功能的详细信息，请参阅[使用支持文件保存](xref:save-with-supporting-files)。

# 后续步骤

- [TMDL 概述（Microsoft Learn）](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview)。
- [TMDL 入门（Microsoft Learn）](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-how-to)
