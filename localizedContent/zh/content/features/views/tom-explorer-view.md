---
uid: tom-explorer-view
title: TOM Explorer 视图
author: Morten Lønskov
updated: 2026-03-19
applies_to:
  products:
    - product: Tabular Editor 2
      partial: true
      note: "它的工作方式与本文所示不同"
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

TOM Explorer 是你与 Data model 对象交互的主窗口。 表、列、度量值、安全组等对象都会以层次结构显示。 TOM Explorer 是你与 Data model 对象交互的主窗口。 表、列、度量值、安全组等对象都会以层次结构显示。 Tabular Data model 通过所谓的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 来表示，而 TOM Explorer 中显示的是该 TOM 的元数据。

TOM Explorer 由两个主要区域组成：第一部分是 Data model 对象，第二部分是菜单栏，可用于筛选并更改主窗口中显示的内容。

![TOM Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## Data model 对象

你可以在 TOM Explorer 中展开对象以查看其子对象，并沿着对象层次结构逐级向下浏览。 此外，如果你右键单击任意对象，就会看到可对该对象执行操作的选项列表。 如下所示，针对表可使用多个选项。 例如，你可以通过此菜单轻松刷新表，并在 @data-refresh-view 中查看刷新状态

![Tom Explorer 交互](~/content/assets/images/user-interface/TomExplorerRightClick.png)

右键菜单包含以下选项，其中一些可展开以显示更多操作。 该菜单取决于所选对象的类型（表、分区、度量值、列等） 下方列表并未涵盖所有对象类型，只列出了最常用的那些类型。

### 右键菜单选项

- **更新表架构...**：
  检查外部数据源中的结构更改，并相应更新表的架构。 当源中新增、重命名或删除了列时，此功能非常有用。 当源中新增、重命名或删除了列时，此功能非常有用。

- **生成 DAX 脚本**：
  为所选表及其对象生成 DAX 脚本。 打开一个新的脚本编辑器窗口，你可以在其中集中查看或编辑 DAX 定义。 打开一个新的脚本编辑器窗口，你可以在其中集中查看或编辑 DAX 定义。

- **预览数据**：
  打开数据预览窗格，显示已加载到所选表中的数据样本。 可用于验证或调试。 仅在右键单击表时才会出现。 可用于验证或调试。 仅在右键单击表时才会出现。

- **刷新**：
  展开后会显示可对所选表执行的刷新操作列表。 仅当模型连接到实时模型时，此项才可用，无论是独立模式还是工作区模式。 此选项仅适用于表和分区。

- **创建**：
  展开为子菜单，可在所选对象下创建新的度量值、列、层次结构、显示文件夹或计算项。 可用选项取决于所选的对象类型。 可用选项取决于所选的对象类型。

- **移至组**：
  可将该表归入 TOM Explorer 中的表格组，便于浏览模型。 此选项仅适用于表。 此选项仅适用于表。

- **设为不可见**：
  将对象标记为在客户端工具中不可见。 该表仍是模型的一部分，但会对 Report 作者隐藏。 也可以使用快捷键 **Ctrl+I** 隐藏该对象。

- **在透视中显示**：
  启用或禁用该表在一个或多个透视中的显示。 **在透视中显示**：
  启用或禁用该表在一个或多个透视中的显示。 透视用于限制最终用户在 Power BI 等工具中可见的内容。

- **批量重命名**：选择多个对象时，你可以使用字符串替换或正则表达式批量重命名这些对象。 批量重命名的快捷键为 **F2**。 批量重命名的快捷键为 **F2**。

- **批量重命名子项...**：
  可使用正则表达式或字符串替换规则，对表或显示文件夹下的所有子对象进行批量重命名。 也可以使用快捷键 **Shift+F2**。 也可以使用快捷键 **Shift+F2**。

- **复制**：
  创建所选表的副本，包括其所有列、度量值和分区。 在 TOM Explorer 中，其他所有对象也都有此选项。 在 TOM Explorer 中，其他所有对象也都有此选项。

- **标记为日期表格...**：
  将该表标记为日期表格，从而启用时间智能功能。 要求该表包含有效的日期列。 要求该表包含有效的日期列。

- **显示依赖关系**：
  以可视化方式显示所选表与其他模型对象之间的依赖关系。 也可以使用快捷键 **Shift+F12**。 也可以使用快捷键 **Shift+F12**。

- **导出脚本**：
  将所选对象导出为 TMSL 或 TMDL 脚本，以用于部署或源代码管理。

- **宏菜单**：
  可将宏放入文件夹中，并对所选对象运行这些宏。 在上面的示例中，用户创建了一个“建模和分析”文件夹，用于存放适用于表对象的宏脚本。 在上面的示例中，用户创建了一个“建模和分析”文件夹，用于存放适用于表对象的宏脚本。

- **剪切 / 复制 / 粘贴 / 删除**：
  标准剪贴板操作。 使用这些选项可移动、复制或删除模型对象。

- **属性**：
  打开所选对象的“属性”窗格。 快捷键：**Alt+Enter**。 用于检查和编辑元数据、表达式、格式设置和可见性设置。

### 显示“信息”列

TOM Explorer 支持显示或隐藏 Data model 对象的其他信息列。 也可以使用快捷键 **Ctrl+7** 执行此操作。
这些额外信息在属性窗口中也可查看，但在这里可以快速查看对象类型、格式字符串、数据类型、表达式和说明。
![TOM Explorer 显示/隐藏列](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png) 也可以使用快捷键 **Ctrl+7** 执行此操作。
这些额外信息在属性窗口中也可查看，但在这里可以快速查看对象类型、格式字符串、数据类型、表达式和说明。
![TOM Explorer 显示/隐藏列](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## TOM Explorer 工具栏

该工具栏可用于显示/隐藏不同类型的对象，切换透视和语言，并在 Data model 中搜索特定对象。
![TOM Explorer 工具栏](~/content/assets/images/user-interface/TOMExplorerToolbar.png)
![TOM Explorer 工具栏](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **显示/隐藏度量值**
   切换表内度量值的可见性。
   **快捷键：** **Ctrl+1**
   **快捷键：** **Ctrl+1**

2. **显示/隐藏列**
   切换表中列的可见性。
   **快捷键：** **Ctrl+2**
   **快捷键：** **Ctrl+2**

3. **显示/隐藏层次结构**
   切换是否在 TOM Explorer 中显示层次结构。
   **快捷键：** **Ctrl+3**
   **快捷键：** **Ctrl+3**

4. **显示/隐藏分区**
   控制是否显示表的分区。
   **快捷键：** **Ctrl+4**
   **快捷键：** **Ctrl+4**

5. **显示/隐藏日历**
   控制是否显示日历。
   **快捷键：** **Ctrl+8**
   **快捷键：** **Ctrl+8**

6. **显示/隐藏显示文件夹**
   启用或禁用在表中显示“显示文件夹”的文件夹组织结构。
   **快捷键：** **Ctrl+5**
   **快捷键：** **Ctrl+5**

7. **按命名空间对用户自定义函数分组**
   启用后，DAX 用户自定义函数将按 [命名空间](xref:udfs#namespaces) 以层级方式分组显示，而不是以扁平列表显示。

8. **显示/隐藏表格组**
   切换 TOM Explorer 树中表格组的可见性。 这样无需离开资源管理器，即可快速访问 **Tools > Preferences** 中的相同设置。 这样无需离开资源管理器，即可快速访问 **Tools > Preferences** 中的相同设置。

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
    用于选择特定透视的下拉列表。 TOM Explorer 中只会显示所选透视中的对象。

12. **语言选择器**
    用于在不同语言之间切换，以本地化模型元数据。

13. **全部折叠**
    折叠 TOM Explorer 树视图中的所有节点。

14. **搜索栏**
    在 TOM Explorer 中提供实时筛选和导航功能。 输入即可搜索所有可见的模型对象。
