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

本文介绍如何使用 Tabular Editor 3 的 [表导入向导](#table-import-wizard)，将新表添加到模型中。 There is also a section on how to [update the table schema](#updating-table-schema) of an existing table. Lastly, we cover how to use the [diagram tool](#working-with-diagrams) to define and edit relationships between tables.

## 表导入向导

[!include[importing-tables1](../features/import-tables.partial.md)]

# 使用关系图

在 Tabular Editor 3 中，**关系图**是一种文档，可用于直观显示并编辑模型中表之间的关系。 You can create as many diagrams as you want to visualize certain areas of your model. A diagram can be saved as a standalone file. See <xref:supported-files#diagram-file-te3diag> for more information.

> [!NOTE]
> 我们建议创建多个较小的图表，而不是少数几个大型图表。 When a diagram contains more than 20 or so tables, it quickly becomes overwhelming and difficult to understand.

在 Tabular Editor 3 中加载模型后，选择 **文件 > 新建 > 关系图** 菜单选项以创建新的关系图。

[!include[diagram-basics](../features/views/diagram-basics.partial.md)]

# 后续步骤

- @刷新、预览与查询
- @creating-and-testing-dax