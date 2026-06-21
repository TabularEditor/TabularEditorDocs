---
uid: importing-tables-data-modeling
title: 导入表并进行 Data model 建模
author: Daniel Otykier
updated: 2021-10-08
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

本文介绍如何使用 Tabular Editor 3 的 [表导入向导](#table-import-wizard)，将新表添加到模型中。 此外还会介绍如何[更新现有表的表结构](#updating-table-schema)。 最后，我们将介绍如何使用[关系图工具](#working-with-diagrams)来定义并编辑表之间的关系。

<a name="table-import-wizard"></a>

## 表导入向导

[!include[importing-tables1](../features/import-tables.partial.md)]

<a name="working-with-diagrams"></a>

# 使用关系图

在 Tabular Editor 3 中，**关系图**是一种文档，可用于直观显示并编辑模型中表之间的关系。 你可以按需创建任意数量的关系图，用于可视化模型的特定区域。 图表可以另存为独立文件。 更多信息详见 <xref:supported-files#diagram-file-te3diag>。

> [!NOTE]
> 我们建议创建多个较小的关系图，而不是少量大型关系图。 当关系图包含 20 张以上的表时，很快就会变得过于复杂，难以理解。

在 Tabular Editor 3 中加载模型后，选择 **文件 > 新建 > 关系图** 菜单选项以创建新的关系图。

## 添加表

可通过以下任一方式将初始表添加到关系图中：

- 在 TOM Explorer 中(多选)选择表，然后右键单击并选择 **添加到关系图**。
- 在 TOM Explorer 中(单选或多选)表，然后将表拖到关系图上
- 使用 **关系图 > 添加表...** 菜单选项，然后在对话框中(单选或多选)要添加的表。
  ![关系图：添加表](~/content/assets/images/diagram-add-tables.png)

要向关系图添加更多表，可以再次使用上述方法；或者在关系图中右键单击现有表，并选择以下选项之一：

- **添加筛选此表的表**：将所有可能直接筛选当前选中表，或通过其他表间接筛选当前选中表的表添加到关系图中。 从事实表开始时很有用。
- **添加所有相关表**：将所有与当前选中表直接相关的表添加到关系图中。 从维度表开始时很有用。
  ![添加相关表](~/content/assets/images/add-related-tables.png)

在继续之前，先按你的偏好重新排列并调整关系图中的表大小；或者使用 **关系图 > 自动排列** 功能，让 Tabular Editor 3 自动布局这些表。

<a name="modifying-relationships-using-the-diagram"></a>

## 使用关系图修改关系

要在两张表之间添加新关系，请找到该关系中事实表（多方）上的列，并将该列拖到维度表（单方）上对应的列。 确认该关系的设置，然后单击 **确定**。

![创建关系](~/content/assets/images/create-relationship.png)

要编辑现有关系，请右键单击该关系并选择 **编辑关系**。 右键菜单还提供了反转或删除关系的快捷命令，如下图所示。

![编辑关系图](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> 你也可以不使用关系图，而是通过 TOM Explorer 创建关系。 找到应作为关系起点的列（多方/事实表一侧），右键单击并选择 **创建 > 从此列创建关系**。 在屏幕上弹出的“创建关系”对话框中指定目标列。

## 保存关系图

要保存关系图，只需使用 **文件 > 保存**（Ctrl+S）。 如果关系图有未保存的更改，而你尝试关闭文档或应用程序，Tabular Editor 3 会提示你保存关系图。

> [!TIP]
> 同一个关系图文件可以用于不同的 Data model。 关系图按表名引用表。 加载图表时，模型中不存在的任何表都会从图表中删除。

> [!NOTE]
> 每次添加或修改关系后，都需要先对 Data model 运行一次“计算”刷新，然后才能在查询模型时使用这些关系。

# 后续步骤

- @refresh-preview-query
- @creating-and-testing-dax