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

TOM Explorer 是你与 Data model 对象交互的主窗口。 表、列、度量值、安全组等对象都以分层结构显示。 表格式 Data model 由所谓的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 表示，而 TOM Explorer 中显示的是该 TOM 的元数据。

TOM Explorer 由两个主要区域组成：第一部分是数据模型对象；第二部分是菜单栏，用于筛选并更改主窗口中显示的内容。

![TOM Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## 数据模型对象

你可以在 TOM Explorer 中展开对象来查看其子级，并沿着对象层级向下浏览。 右键单击任意对象，即可看到一组用于与该对象交互的选项。 如下所示，对于表你可以使用多个选项。 例如，你可以通过此菜单轻松刷新表，并在 @data-refresh-view 中查看该刷新操作的状态

![Tom Explorer 交互](~/content/assets/images/user-interface/TomExplorerRightClick.png)

右键菜单包含以下项目，其中部分项目可展开以执行更多操作。 该菜单会根据所选对象类型而变化（表、分区、度量值、列等） 下面的列表并未涵盖所有对象类型，但包含了最常用的那些。

### 右键菜单中的选项

- **更新表架构...**：
  检查外部数据源的结构变化，并据此更新表的架构。 当源端新增、重命名或删除列时，这会很有用。

- **编写 DAX 脚本**：
  为所选表及其对象生成 DAX 脚本。 打开一个新的脚本编辑器窗口，你可以在其中集中查看或编辑 DAX 定义。

- **预览数据**：
  打开数据预览窗格，显示已加载到所选表中的数据样本。 可用于验证或进行调试。 仅在对表右键单击时才会出现。

- **刷新**：
  展开后会显示可对所选表执行的刷新操作列表。 仅当模型以独立模式或工作区模式连接到实时模型时才可用。 此选项仅适用于表及其分区。

- **创建**：
  展开为子菜单，可在所选对象下新建度量值、列、层级结构、显示文件夹或计算项。 可用选项取决于所选对象的类型。

- **移至组**：
  可在 TOM Explorer 中将该表移入某个表格组，便于浏览模型。 此选项仅对表可用。

- **设为不可见**
  将对象标记为在客户端工具中不显示。 该表仍是模型的一部分，但对 Report 作者隐藏。 也可以使用快捷键 **Ctrl+I** 来隐藏该对象。

- **在透视中显示**：
  控制该表是否包含在一个或多个透视中。 透视会限制最终用户在 Power BI 等工具中可见的内容。

- **批量重命名**：选择多个对象时，你可以通过字符串替换或正则表达式批量重命名这些对象。 批量重命名的快捷键为 **F2**。

- **批量重命名子对象...**
  允许使用正则表达式或字符串替换规则，对表或显示文件夹下的所有子对象进行批量重命名。 也可以使用快捷键 **Shift+F2** 访问。

- **复制**
  为所选表创建一个副本，包括其所有列、度量值和分区。 在 TOM Explorer 中的其他所有对象上也同样适用。

- **标记为日期表格...**：
  将该表标记为日期表格，从而启用时间智能功能。 要求该表包含一个有效的日期列。

- **显示依赖项**
  以可视化方式展示所选表与其他模型对象之间的依赖关系。 也可使用快捷键 **Shift+F12** 访问。

- **导出脚本**：
  将所选对象导出为 TMSL 或 TMDL 脚本，以便用于部署或源代码管理。

- **宏菜单**：
  可将宏放入文件夹中，并对所选对象运行。 在上面的示例中，用户为表对象上的宏脚本创建了一个名为 Modelling 和 Analysis 的文件夹。

- **剪切 / 复制 / 粘贴 / 删除**
  常规剪贴板操作。 使用这些命令可移动、复制或删除模型对象。

- **属性**
  打开所选对象的“属性”窗格。 快捷键为 **Alt+Enter**。 用于检查和编辑元数据、表达式、格式设置以及可见性设置。

### 显示信息列

TOM Explorer 允许切换显示有关数据模型对象的额外信息列。 也可通过快捷键 **Ctrl+7** 完成。
这些额外信息在属性窗口中也能查看，但在这里可以快速查看对象类型、格式字符串、数据类型、表达式和说明。
![TOM Explorer Show Hide Columns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## TOM Explorer 工具栏

工具栏可让你显示或隐藏不同类型的对象，切换透视和语言，并在 Data model 中搜索特定对象。
![TOM Explorer 工具条](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **显示/隐藏度量值**
   切换表中度量值的可见性。
   **快捷方式：** **Ctrl+1**

2. **显示/隐藏列**
   切换表格中列的显示与隐藏。
   **快捷键:** **Ctrl+2**

3. **显示/隐藏层级结构**
   切换 TOM Explorer 中层级结构是否可见。
   **快捷键:** **Ctrl+3**

4. **显示/隐藏分区**
   控制表中分区是否显示。
   **快捷键:** **Ctrl+4**

5. **显示/隐藏日历**
   控制日历是否可见。
   **快捷键:** **Ctrl+8**

6. **显示/隐藏显示文件夹**
   启用或禁用在表内按显示文件夹进行组织的显示方式。
   **快捷键:** **Ctrl+5**

7. **按命名空间对用户自定义函数分组**
   启用后，DAX 用户自定义函数会按 [命名空间](xref:udfs#namespaces) 分层分组显示，而不是以扁平列表显示。

8. **显示/隐藏表格组**
   切换 TOM Explorer 树中表格组是否可见。 无需离开资源管理器，即可快速访问 **工具 > 偏好** 中的相同设置。

9. **显示/隐藏已隐藏对象**
   切换是否显示已隐藏对象。
   **快捷键:** **Ctrl+6**

10. **显示/隐藏信息栏**
    用于显示或隐藏元数据列，例如数据类型或对象状态。
    **快捷键:** **Ctrl+7**

11. **透视选择器**
    下拉列表，用于选择特定透视。 **透视选择器**：
    用于选择特定透视的下拉列表。TOM Explorer 中仅显示所选透视中的对象。

12. **语言选择器**
    允许在不同语言之间切换，以本地化模型元数据。

13. **全部折叠**
    将 TOM Explorer 树视图中的所有节点全部折叠。

14. **搜索栏**
    在 TOM Explorer 中提供实时筛选和导航。 输入即可在所有可见的模型对象中搜索。
