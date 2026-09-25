---
uid: diagram-view
title: 图表视图
author: Morten Lønskov
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

# 图表视图

Tabular Editor 3 中的**图表视图**是语义模型的可视化呈现。 It provides an intuitive layout for viewing tables, their columns, and the relationships between them. It is particularly helpful for understanding the schema at a glance, creating relationships, and presenting models to stakeholders. A diagram can be saved as a stand alone file. See <xref:supported-files#diagram-file-te3diag> for more information.

> [!NOTE]
> 我们建议创建多个较小的图表，而不是少数几个大型图表。 When a diagram contains more than 20 or so tables, it quickly becomes overwhelming and difficult to understand.

在 Tabular Editor 3 中加载模型后，选择菜单 **文件 > 新建 > 图表** 创建新图表；或在主工具栏中新建图表，然后将 TOM Explorer 中的表拖放到图表窗口中。

## 使用图表视图

[!include[diagram-basics](diagram-basics.partial.md)]

## 图表功能

### 用于表操作的上下文菜单

在图表视图中的任意位置右键单击，会打开一个上下文菜单，可快速访问多个选项：

![图表上下文菜单](~/content/assets/images/diagram-context-menu.png)

- **添加表...**：打开对话框，手动向图表添加更多表。
- **添加可筛选此表的表**：自动引入可筛选当前表的相关表。
- **添加所有相关表**：加载与所选表存在关系的所有表。
- **编辑关系**：打开所选关系的编辑器。 Only visible when a relationship is selected.
- **Invert relationship**: Swaps the from and to sides of the selected relationship. Only visible when a relationship is selected.
- **激活关系**：激活未激活的关系。 Only visible when an inactive relationship is selected.
- **停用关系**：停用已激活的关系。 Only visible when an active relationship is selected.
- **适合页面**：调整图表的缩放级别，使所有可见表都能完整显示。
- **自动排列**：自动将表排列成星型架构。
- **从图中移除**：从当前视图中隐藏所选表。
- **删除关系**：从模型中删除所选关系。 Only visible when a relationship is selected.

### 关系指示器

表之间的关系使用带方向的箭头来表示：

- `1 - *`：表示一对多关系。
- `* - *`：表示多对多关系。
- `➝`：表示单向关系，箭头定义了该关系的筛选方向。
- `⟷`：表示双向交叉筛选关系。

这些视觉标记可帮助你快速判断筛选方向和基数。

### 列显示切换

A **chevron toggle** is available in the top-right corner of each table, by clicking it you will toggle between the following options:

![图表人字形切换按钮](~/content/assets/images/diagram-chevron-toggle.png)

- **全部列**：显示所有列。
- **仅键列**：仅显示主键和外键。
- **不显示列**：隐藏所有列，仅显示表头。

该开关有助于减少界面杂乱，尤其是在列很多的复杂模型中，让你更容易专注于关系。

### 列数据类型图标

图表中的每一列旁都会显示一个代表其数据类型的图标：

- <img src="~/content/assets/images/icons/String.svg" alt="Text Icon" width="16" height="16"> 表示字符串/文本值
- <img src="~/content/assets/images/icons/Integer.svg" alt="Integer Icon" width="16" height="16"> 表示整数
- <img src="~/content/assets/images/icons/Double.svg" alt="Double Icon" width="16" height="16"> 表示双精度/浮点小数
- <img src="~/content/assets/images/icons/Currency.svg" alt="Currency Icon" width="16" height="16"> 表示货币/定点小数
- <img src="~/content/assets/images/icons/Binary.svg" alt="Binary Icon" width="16" height="16"> 表示二进制值
- <img src="~/content/assets/images/icons/TrueFalse.svg" alt="Boolean Icon" width="16" height="16"> 表示布尔值（true/false）
- <img src="~/content/assets/images/icons/Calendar.svg" alt="Date Icon" width="16" height="16"> 用于表示日期/时间值

这份快速可视化参考支持快速数据验证，并有助于理解数据结构。