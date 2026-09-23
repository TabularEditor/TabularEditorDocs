---
uid: importing-tables-data-modeling
title: 导入表并进行 Data model 建模
author: Daniel Otykier
updated: 2026-09-14
applies_to:
  products:
    - product: Tabular Editor 2
      none: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 导入表并进行 Data model 建模

本文介绍如何使用 Tabular Editor 3 的 [表导入向导](#table-import-wizard)，将新表添加到模型中。此外还会介绍如何[更新现有表的表结构](#updating-table-schema)。最后，我们将介绍如何使用[关系图工具](#working-with-diagrams)来定义并编辑表之间的关系。

## 表导入向导

[!include[importing-tables1](../features/import-tables.partial.md)]

# 使用关系图

在 Tabular Editor 3 中，**关系图**是一种文档，可用于直观显示并编辑模型中表之间的关系。你可以按需创建任意数量的关系图，用于可视化模型的特定区域。图表可以另存为独立文件。更多信息详见 <xref:supported-files#diagram-file-te3diag>。

> [!NOTE]
> 我们建议创建多个较小的关系图，而不是少量大型关系图。当关系图包含 20 张以上的表时，很快就会变得过于复杂，难以理解。

在 Tabular Editor 3 中加载模型后，选择 **文件 > 新建 > 关系图** 菜单选项以创建新的关系图。

[!include[diagram-basics](../features/views/diagram-basics.partial.md)]

# 后续步骤

- @refresh-preview-query
- @creating-and-testing-dax