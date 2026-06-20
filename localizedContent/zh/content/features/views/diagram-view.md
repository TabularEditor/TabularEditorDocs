---
uid: diagram-view
title: 图表视图
author: Morten Lønskov
updated: 2025-04-24
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

Tabular Editor 3 中的**图表视图**是语义模型的可视化呈现。 它提供直观的布局，用于查看表、表中的列，以及它们之间的关系。 它特别适合快速把握架构、创建关系，并向利益相关者展示模型。 图表可以保存为独立文件。 更多信息请参阅 <xref:supported-files#diagram-file-te3diag>。

> [!NOTE]
> 我们建议创建多个较小的图表，而不是少数几个大型图表。 当图表包含 20 张左右甚至更多的表时，很快就会显得杂乱，难以理解。

在 Tabular Editor 3 中加载模型后，选择菜单 **文件 > 新建 > 图表** 创建新图表；或在主工具栏中新建图表，然后将 TOM Explorer 中的表拖放到图表窗口中。

## 使用图表视图

## 添加表

通过以下任一方式将初始表添加到图表中：

- 在 TOM Explorer 中（多）选择表，然后右键单击并选择 **添加到图表**。
- 在 TOM Explorer 中（多）选择表，然后将表拖到图表中
- 使用 **图表 > 添加表...** 菜单选项，然后在对话框中(多选)选择要添加的表。
  ![图表 添加表](~/content/assets/images/diagram-add-tables.png)

  要向图表添加更多表，请再次使用上述方法，或在图表中的现有表上右键单击，然后选择以下选项之一：

  - **添加可筛选此表的表**：将所有可能直接或通过其他表间接筛选当前所选表的表都添加到图表中。 从事实表开始时很有用。
  - **添加所有相关表**：将与当前所选表直接相关的所有表添加到图表中。 从维度表开始时很有用。
    ![Add Related Tables](~/content/assets/images/add-related-tables.png)

  继续之前，请根据你的偏好重新排列并调整图表中各表的大小，或使用 **图表 > 自动排列** 功能，让 Tabular Editor 3 自动布局这些表。

## 使用图表修改关系

要在两张表之间添加新关系，请找到关系中事实表（多端）上的列，然后将该列拖到维度表（一端）上的对应列。 确认关系设置，然后点击 **确定**。

![创建关系](~/content/assets/images/create-relationship.png)

要编辑现有关系，请在其上右键单击，然后选择 **编辑关系**。 右键菜单还包含用于反转或删除关系的快捷方式，如下图所示。

![编辑关系图表](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> 你也可以不使用图表，而是通过 TOM Explorer 创建关系。 定位关系应从其开始的列（多端/事实表端），在该列上右键单击，然后选择 **创建 > 从此处创建关系**。 在屏幕上出现的“创建关系”对话框中指定目标列。

## 保存图表

要保存图表，只需使用 **文件 > 保存** (CTRL+S) 选项。 当图表有未保存的更改时，如果你关闭文档或应用程序，Tabular Editor 3 会提示你保存图表。

> [!TIP]
> 同一个图表文件也可以加载到不同的数据模型中。 图表通过表名来引用表。 加载图表时，模型中不存在的任何表都会从图表中移除。

> [!NOTE]
> 每次添加或修改关系后，在这些关系可用于查询模型之前，你都需要对数据模型执行一次“计算”刷新。

## 图表功能

### 用于表操作的上下文菜单

在图表视图中的任意位置右键单击，会打开一个上下文菜单，可快速访问多个选项：

![图表上下文菜单](~/content/assets/images/diagram-context-menu.png)

- **添加表...**：打开对话框，手动向图表添加更多表。
- **添加可筛选此表的表**：自动引入可筛选当前表的相关表。
- **添加所有相关表**：加载与所选表存在关系的所有表。
- **编辑关系**：打开所选关系的编辑器。 仅在选中关系时可见。 仅在选中关系时可见。
- **反转关系**：交换所选关系的“从”端和“到”端。 仅在选中关系时可见。
- **激活关系**：激活未激活的关系。 仅在选中未激活的关系时可见。 仅在选中未激活的关系时可见。
- **停用关系**：停用已激活的关系。 仅在选中已激活的关系时可见。 仅在选中已激活的关系时可见。
- **适合页面**：调整图表的缩放级别，使所有可见表都能完整显示。
- **自动排列**：自动将表排列成星型架构。
- **从图中移除**：从当前视图中隐藏所选表。
- **删除关系**：从模型中删除所选关系。 仅在选中关系时可见。 仅在选中关系时可见。

### 关系指示器

表之间的关系使用带方向的箭头来表示：

- `1 - *`：表示一对多关系。
- `* - *`：表示多对多关系。
- `➝`：表示单向关系，箭头定义了该关系的筛选方向。
- `⟷`：表示双向交叉筛选关系。

这些视觉标记可帮助你快速判断筛选方向和基数。

### 列显示切换

每个表的右上角都有一个**人字形切换按钮**。点击后可在以下选项之间切换：

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