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

The TOM Explorer is your main window for interacting with the objects of your data model. Objects such as tables, columns, measures, security groups etc. are all displayed in a hierarchical structure. 表格数据模型由所谓的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 来表示，而在 TOM Explorer 中显示的正是该 TOM 的元数据。

TOM Explorer 由两个主要区域组成：第一部分是数据模型对象；第二部分是菜单栏，用于筛选并更改主窗口中显示的内容。

![Tom Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## 数据模型对象

你可以在 TOM Explorer 中展开对象以查看其子对象，并沿着对象层级向下浏览。 如果你在任意对象上右键单击，会看到一组用于与该对象交互的选项。 如下所示，你可以对表使用多种选项。 使用此菜单，例如，您可以轻松刷新表格，并在 @data-refresh-view 视图中查看刷新状态

![Tom Explorer Interaction](~/content/assets/images/user-interface/TomExplorerRightClick.png)

右键菜单包含以下项，其中部分可展开以查看更多操作。 菜单内容取决于所选对象类型（表、分区、度量值、列等） 下方列表并未穷尽所有对象类型，仅包含最常用的几种。

### 右键菜单中的选项

- **Update table schema...**:
  Checks for structural changes in the external data source and updates the table's schema accordingly. 当数据源中新增、重命名或删除了列时，这很有用。

- **Script DAX**:
  Generates a DAX script for the selected table and its objects. 将打开一个新的脚本编辑器窗口，便于你集中查看或编辑 DAX 定义。

- **Preview data**:
  Opens the data preview pane displaying a sample of the data loaded into the selected table. 可用于验证或调试。 仅在右键单击表时才会出现。

- **Refresh**:
  Expands to a selection of possible refresh operation for the selected table. 仅当模型在独立模式或工作区模式下连接到实时模型时才可用。 此选项仅适用于表和分区。

- **Create**:
  Expands to a submenu allowing the creation of new measures, columns, hierarchies, display folders or calculation items under the selected object. 可用的选项取决于所选对象的类型。

- **Move to group**:
  Allows you to organize the table into a Table group within the TOM Explorer for easier model navigation. 此选项仅适用于表。

- **Make invisible**:
  Marks the object as not visible in client tools. 该表仍是模型的一部分，但会对报表作者隐藏。 Alternative use the shortcut **Ctrl+I** to hide the object.

- **Shown in perspectives**:
  Enables or disables the table's inclusion in one or more perspectives. 透视会限制最终用户在 Power BI 等工具中能看到的内容。

- **批量重命名**: 选择多个对象时，你可以通过字符串替换或正则表达式批量重命名这些对象。 The shortcut for batch rename is **F2**.

- **Batch rename children...**:
  Enables bulk renaming of all child objects under the table or display folder using regex or string replacement rules. Can also be accessed with the shortcut **Shift+F2**.

- **Duplicate**:
  Creates a copy of the selected table, including all its columns, measures and partitions. TOM Explorer 中的所有其他对象也都有此功能。

- **Mark as date table...**:
  Marks the table as a date table, enabling time intelligence features. 要求该表包含有效的日期列。

- **Show dependencies**:
  Visualizes dependencies between the selected table and other model objects. Can also be accessed via shortcut **Shift+F12**.

- **Export script**:
  Exports the selected objects as a TMSL or TMDL script for use in deployment or source control.

- **Macro Menus**:
  Macros can be placed into folders and run against the selected object. 在上面的示例中，用户有一个名为“建模和分析”的文件夹，用于存放表对象的宏脚本。

- **Cut / Copy / Paste / Delete**:
  Standard clipboard operations. 可用于移动、复制或删除模型对象。

- **Properties**:
  Opens the Properties pane for the selected object. Shortcut: **Alt+Enter**. Used to inspect and edit metadata, expressions, formatting and visibility settings.

### 显示信息列

TOM Explorer 允许你切换显示有关数据模型对象的额外信息列。 This can be done with the shortcut **Ctrl+7**.
These extra info also exists in the property window, but allow for a quick view of the Object Type, Format String, Data Type, Expression and Description.
![Tom Explorer Show Hide Columns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## TOM Explorer 工具栏

The toolbar allows you to show and hide different types of objects, toggle perspectives and languages and search for specific objects in the data model.
![TOM Explorer 工具栏](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **Show/Hide Measures**
   Toggle the visibility of measures within tables.
   **Shortcut:** **Ctrl+1**

2. **Show/Hide Columns**
   Toggle the visibility of columns within tables.
   **Shortcut:** **Ctrl+2**

3. **Show/Hide Hierarchies**
   Toggle whether hierarchies are shown in the TOM Explorer.
   **Shortcut:** **Ctrl+3**

4. **Show/Hide Partitions**
   Controls whether partitions are visible for tables.
   **Shortcut:** **Ctrl+4**

5. **Show/Hide Calendars**
   Controls whether calendars are visible.
   **Shortcut:** **Ctrl+8**

6. **Show/Hide Display Folders**
   Enables or disables the display of folder organization within tables.
   **Shortcut:** **Ctrl+5**

7. **Group User-Defined Functions by Namespace**
   When enabled, DAX User-Defined Functions are grouped hierarchically by [namespace](xref:udfs#namespaces), rather than being shown as a flat list.

8. **Show/Hide Table Groups**
   Toggle the visibility of table groups in the TOM Explorer tree. This provides quick access to the same setting found in **Tools > Preferences** without leaving the explorer.

9. **Show/Hide Hidden Objects**
   Toggles whether hidden objects are shown.
   **Shortcut:** **Ctrl+6**

10. **Show/Hide Info Columns**
    Shows or hides metadata columns, such as data types or object status.
    **Shortcut:** **Ctrl+7**

11. **Perspective Selector**
    Drop-down to choose a specific perspective. TOM Explorer 中仅显示所选透视中的对象。

12. **Language Selector**
    Allows switching between different languages for model metadata localization.

13. **Collapse All**
    Collapses all nodes in the TOM Explorer tree view.

14. **Search Bar**
    Provides real-time filtering and navigation within the TOM Explorer. 输入即可搜索所有可见的模型对象。
