---
uid: tom-explorer-view
title: TOM Explorer 视图
author: Morten Lønskov
updated: 2026-03-19
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "其工作方式与本文所示不同"
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

# 在 Tabular Editor 3 中使用 TOM Explorer

TOM Explorer 是与 Data model 对象交互的主要窗口。 表、列、度量值、安全组等对象都会以层级结构显示。 TOM Explorer 是与 Data model 对象交互的主要窗口。 表、列、度量值、安全组等对象都会以层级结构显示。 表格数据模型由所谓的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 来表示，而在 TOM Explorer 中显示的正是该 TOM 的元数据。

TOM Explorer 由两个主要区域组成：第一部分是数据模型对象；第二部分是菜单栏，用于筛选并更改主窗口中显示的内容。

![Tom Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## 数据模型对象

你可以在 TOM Explorer 中展开对象以查看其子对象，并沿着对象层级向下浏览。 如果你在任意对象上右键单击，会看到一组用于与该对象交互的选项。 如下所示，你可以对表使用多种选项。 使用此菜单，例如，您可以轻松刷新表格，并在 @data-refresh-view 视图中查看刷新状态

![Tom Explorer Interaction](~/content/assets/images/user-interface/TomExplorerRightClick.png)

右键菜单包含以下项，其中部分可展开以查看更多操作。 菜单内容取决于所选对象类型（表、分区、度量值、列等） 下方列表并未穷尽所有对象类型，仅包含最常用的几种。

### 右键菜单中的选项

- **更新表架构...**：
  检查外部数据源中的结构性更改，并相应更新该表的架构。 当数据源中新增、重命名或删除了列时，这很有用。 当数据源中新增、重命名或删除了列时，这很有用。

- **生成 DAX 脚本**：
  为所选表及其对象生成 DAX 脚本。 将打开一个新的脚本编辑器窗口，便于你集中查看或编辑 DAX 定义。 将打开一个新的脚本编辑器窗口，便于你集中查看或编辑 DAX 定义。

- **预览数据**：
  打开数据预览窗格，显示加载到所选表中的数据样本。 可用于验证或调试。 仅在右键单击表时才会出现。 可用于验证或调试。 仅在右键单击表时才会出现。

- **刷新**：
  展开后会显示可对所选表执行的刷新操作选项。 仅当模型在独立模式或工作区模式下连接到实时模型时才可用。 此选项仅适用于表和分区。

- **创建**：
  展开子菜单，可在所选对象下创建新的度量值、列、层级结构、显示文件夹或计算项。 可用的选项取决于所选对象的类型。 可用的选项取决于所选对象的类型。

- **移至组**：
  允许你在 TOM Explorer 中将该表移入某个表格组，便于浏览模型。 此选项仅适用于表。 此选项仅适用于表。

- **设为不可见**：
  将对象标记为在客户端工具中不可见。 该表仍是模型的一部分，但会对报表作者隐藏。 也可以使用快捷键 **Ctrl+I** 隐藏对象。

- **在透视中显示**：
  启用或禁用该表在一个或多个透视中的显示。 **在透视中显示**：
  启用或禁用该表在一个或多个透视中的显示。 透视会限制最终用户在 Power BI 等工具中能看到的内容。

- **批量重命名**: 选择多个对象时，你可以通过字符串替换或正则表达式批量重命名这些对象。 批量重命名的快捷键是 **F2**。 批量重命名的快捷键是 **F2**。

- **批量重命名子对象...**：
  使用正则表达式或字符串替换规则，对表或显示文件夹下的所有子对象进行批量重命名。 也可通过快捷键 **Shift+F2** 访问。 也可通过快捷键 **Shift+F2** 访问。

- **复制**：
  创建所选表的副本，包括其所有列、度量值和分区。 TOM Explorer 中的所有其他对象也都有此功能。 TOM Explorer 中的所有其他对象也都有此功能。

- **标记为日期表格...**：
  将该表标记为日期表格，以启用时间智能功能。 要求该表包含有效的日期列。 要求该表包含有效的日期列。

- **显示依赖项**：
  可视化所选表与其他模型对象之间的依赖关系。 也可通过快捷键 **Shift+F12** 访问。 也可通过快捷键 **Shift+F12** 访问。

- **导出脚本**：
  将所选对象导出为 TMSL 或 TMDL 脚本，用于部署或源代码管理。

- **宏菜单**：
  可以将宏放入文件夹中，并针对所选对象运行。 在上面的示例中，用户有一个名为“建模和分析”的文件夹，用于存放表对象的宏脚本。 在上面的示例中，用户有一个名为“建模和分析”的文件夹，用于存放表对象的宏脚本。

- **剪切 / 复制 / 粘贴 / 删除**：
  标准剪贴板操作。 可用于移动、复制或删除模型对象。 可用于移动、复制或删除模型对象。

- **属性**：
  打开所选对象的“属性”窗格。 快捷键：**Alt+Enter**。 用于查看和编辑元数据、表达式、格式和可见性设置。

### 显示信息列

TOM Explorer 允许你切换显示有关数据模型对象的额外信息列。 可通过快捷键 **Ctrl+7** 实现。
这些附加信息在属性窗口中也能查看，但在这里可以快速查看对象类型、格式字符串、数据类型、表达式和说明。
![TOM Explorer 显示/隐藏列](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png) 可通过快捷键 **Ctrl+7** 实现。
这些附加信息在属性窗口中也能查看，但在这里可以快速查看对象类型、格式字符串、数据类型、表达式和说明。
![TOM Explorer 显示/隐藏列](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## TOM Explorer 工具栏

工具栏可让你显示或隐藏不同类型的对象，切换透视和语言，并可在 Data model 中搜索特定对象。
![TOM Explorer 工具栏](~/content/assets/images/user-interface/TOMExplorerToolbar.png)
![TOM Explorer 工具栏](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **显示/隐藏度量值**
   切换表内度量值的可见性。
   **快捷键：** **Ctrl+1**
   **快捷键：** **Ctrl+1**

2. **显示/隐藏列**
   切换表内列的可见性。
   **快捷键：** **Ctrl+2**
   **快捷键：** **Ctrl+2**

3. **显示/隐藏层级结构**
   切换是否在 TOM Explorer 中显示层级结构。
   **快捷键：** **Ctrl+3**
   **快捷键：** **Ctrl+3**

4. **显示/隐藏分区**
   控制表是否显示分区。
   **快捷键：** **Ctrl+4**
   **快捷键：** **Ctrl+4**

5. **显示/隐藏日历**
   控制是否显示日历。
   **快捷键：** **Ctrl+8**
   **快捷键：** **Ctrl+8**

6. **显示/隐藏显示文件夹**
   启用或禁用表内按文件夹组织的显示方式。
   **快捷键：** **Ctrl+5**
   **快捷键：** **Ctrl+5**

7. **按命名空间对用户自定义函数分组**
   启用后，DAX 用户自定义函数会按 [命名空间](xref:udfs#namespaces) 分层分组显示，而不是以扁平列表显示。

8. **显示/隐藏表格组**
   切换 TOM Explorer 树中表格组的可见性。 无需离开资源管理器，即可快速访问 **Tools > Preferences** 中的相同设置。 无需离开资源管理器，即可快速访问 **Tools > Preferences** 中的相同设置。

9. **显示/隐藏隐藏对象**
   切换是否显示隐藏对象。
   **快捷键：** **Ctrl+6**
   **快捷键：** **Ctrl+6**

10. **显示/隐藏信息列**
    显示或隐藏元数据列，例如数据类型或对象状态。
    **快捷键：** **Ctrl+7**
    **快捷键：** **Ctrl+7**

11. **透视选择器**
    用于选择特定透视的下拉列表。 **透视选择器**
    用于选择特定透视的下拉列表。 TOM Explorer 中仅显示所选透视中的对象。

12. **语言选择器**
    允许在不同语言之间切换，以本地化模型元数据。

13. **全部折叠**
    将 TOM Explorer 树视图中的所有节点全部折叠。

14. **搜索栏**
    在 TOM Explorer 中提供实时筛选与导航功能。 输入即可搜索所有可见的模型对象。
