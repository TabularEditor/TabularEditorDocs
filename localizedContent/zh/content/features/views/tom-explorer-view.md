---
uid: tom-explorer-view
title: TOM Explorer 视图
author: Morten Lønskov
updated: 2026-09-16
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

The TOM Explorer is your main window for interacting with the objects of your data model. Objects such as tables, columns, measures, security groups etc. are all displayed in a hierarchical structure. Tabular Data model 通过所谓的 [Tabular Object Model (TOM)](https://docs.microsoft.com/en-us/analysis-services/tom/introduction-to-the-tabular-object-model-tom-in-analysis-services-amo?view=asallproducts-allversions) 来表示，而 TOM Explorer 中显示的是该 TOM 的元数据。

TOM Explorer 由两个主要区域组成：第一部分是 Data model 对象，第二部分是菜单栏，可用于筛选并更改主窗口中显示的内容。

![TOM Explorer](~/content/assets/images/user-interface/TOMExplorer.png)

## Data model 对象

You can fold out objects in the TOM Explorer to see their children and follow the hierarchy of objects downwards. And if you right click on any object you will be given a list of options to interact with that specific object. As you can see below there are several options that you can use with a table. It is with this menu that you for example can easily refresh your tables and see the status of that refresh in the @data-refresh-view

![Tom Explorer 交互](~/content/assets/images/user-interface/TomExplorerRightClick.png)

The right click menu has the following items some of which can be expanded for more actions. The menu depends on the object type chosen (Table, partition, measure, column etc.) and the list below is not exhaustive for all types of objects but contains those most used.

### 右键菜单选项

- **更新表架构...**：
  检查外部数据源中的结构更改，并相应更新表的架构。 This is useful when columns have been added, renamed, or removed in the source.

- **生成 DAX 脚本**：
  为所选表及其对象生成 DAX 脚本。 Opens a new script editor window where you can review or edit DAX definitions collectively.

- **预览数据**：
  打开数据预览窗格，显示已加载到所选表中的数据样本。 Useful for validation or debugging. Only exists when right clicking tables.

- **Refresh**:
  Expands to a selection of possible refresh operation for the selected table. This is available only if the model is connected to live model either stand alone or in workspace mode. This option is only available on tables and partitions.

- **创建**：
  展开为子菜单，可在所选对象下创建新的度量值、列、层次结构、显示文件夹或计算项。 The available options depends on the object type selected.

- **Move to group**:
  Expands to a submenu for organizing the selected tables into a Table Group for easier model navigation. The submenu lists existing Table Groups, a **(New...)** entry that creates a new group from the selected tables and opens its name editor, and a **(None)** entry that removes the Table Group assignment. This option is only available for tables.

- **Make invisible**:
  Marks the object as not visible in client tools. The table remains part of the model but is hidden from report authors. Alternative use the shortcut **Ctrl+I** to hide the object.

- **Shown in perspectives**:
  Enables or disables the table's inclusion in one or more perspectives. 透视用于限制最终用户在 Power BI 等工具中可见的内容。

- **批量重命名**：选择多个对象时，你可以使用字符串替换或正则表达式批量重命名这些对象。 The shortcut for batch rename is **F2**.

- **批量重命名子项...**：
  可使用正则表达式或字符串替换规则，对表或显示文件夹下的所有子对象进行批量重命名。 Can also be accessed with the shortcut **Shift+F2**.

- **复制**：
  创建所选表的副本，包括其所有列、度量值和分区。 Also exists for all other objects in the TOM Explorer.

- **标记为日期表格...**：
  将该表标记为日期表格，从而启用时间智能功能。 Requires that the table contains a valid date column.

- **显示依赖关系**：
  以可视化方式显示所选表与其他模型对象之间的依赖关系。 Can also be accessed via shortcut **Shift+F12**.

- **导出脚本**：
  将所选对象导出为 TMSL 或 TMDL 脚本，以用于部署或源代码管理。

- **宏菜单**：
  可将宏放入文件夹中，并对所选对象运行这些宏。 If you have created macros for the given object type, they appear as additional menu items or folders in the right-click menu.

- **Revert**:
  Puts the selected object, and everything beneath it, back to the way it was when the model was last saved, leaving all other unsaved changes in place. Only shown for objects with [unsaved changes](xref:unsaved-changes), and for tables, display folders, table groups and the **Model** node when something beneath them has changed.

- **Restore**:
  Brings back a deleted object, exactly as it was the moment before it was deleted. Only shown when right-clicking objects that were [deleted since the last save](xref:unsaved-changes#deleted-objects), which remain visible in the TOM Explorer with a struck-through name.

- **Cut / Copy / Paste / Delete**:
  Standard clipboard operations. Use these to move, duplicate, or remove model objects. Deleted objects stay visible in the TOM Explorer, struck through, until the model is saved. See @unsaved-changes.

- **Properties**:
  Opens the Properties pane for the selected object. Shortcut: **Alt+Enter**. Used to inspect and edit metadata, expressions, formatting and visibility settings.

### Copying and moving objects

Pasting an object (**Edit > Paste**, or **Ctrl+V**) selects the pasted object, gives it focus and scrolls it into view, so you can rename or edit it straight away. The original is left unselected.

Moving an object to another table by drag and drop, and duplicating one, both keep whatever error and warning indicators the object already carried. An expression that was invalid before the move is still marked as invalid afterwards, without needing to be edited again.

### Selecting a partition

Selecting a partition shows its expression in the **Expression Editor**. For a partition with no query expression of its own, such as a Direct Lake partition or one generated by an incremental refresh policy, the editor shows the **Data Coverage Definition Expression** where one is defined, and is empty otherwise.

### 显示“信息”列

TOM Explorer 支持显示或隐藏 Data model 对象的其他信息列。 This can be done with the shortcut **Ctrl+7**.
These extra info also exists in the property window, but allow for a quick view of the Object Type, Format String, Data Type, Expression and Description.
![Tom Explorer Show Hide Columns](~/content/assets/images/user-interface/TOMExplorerInfoColumns.png)

## Unsaved changes

Objects that differ from the last saved version of the model are tinted and badged: orange for edited objects, green for added objects and red for deleted objects, which also stay in the tree, struck through, until the model is saved. Tables, folders and groups that contain changed objects get a hatched fill. Deleted objects can be brought back with the right-click **Restore** option, and the **Show changes** toolbar button filters the tree down to the changed objects. See @unsaved-changes for details, including how to revert individual changes and how to adjust the indicators under **Tools > Preferences**.

![Tom Explorer Unsaved Changes](~/content/assets/images/user-interface/TOMExplorerUnsavedChanges.png)

## Keeping your place in the tree

The TOM Explorer keeps its state when the model underneath it changes. Expanded nodes stay expanded, the focused object stays focused, your selection is preserved and the tree does not scroll away from where you were looking.

This applies when you revert the model, whether it is loaded from a file, from a folder or from a server in [workspace mode](xref:workspace-mode), and when the model is reloaded because its files changed on disk. See @auto-reload.

It applies to ordinary editing too. Semantic analysis runs continuously as you edit DAX, and the tree now updates in place as it completes rather than rebuilding, so a long expression no longer costs you your position in a large model.

## TOM Explorer 工具栏

该工具栏可用于显示/隐藏不同类型的对象，切换透视和语言，并在 Data model 中搜索特定对象。
![Tom Explorer Toolbar](~/content/assets/images/user-interface/TOMExplorerToolbar.png)

1. **显示/隐藏度量值**
   切换表内度量值的可见性。
   **Shortcut:** **Ctrl+1**

2. **显示/隐藏列**
   切换表中列的可见性。
   **Shortcut:** **Ctrl+2**

3. **显示/隐藏层次结构**
   切换是否在 TOM Explorer 中显示层次结构。
   **Shortcut:** **Ctrl+3**

4. **显示/隐藏分区**
   控制是否显示表的分区。
   **Shortcut:** **Ctrl+4**

5. **显示/隐藏日历**
   控制是否显示日历。
   **Shortcut:** **Ctrl+8**

6. **显示/隐藏显示文件夹**
   启用或禁用在表中显示“显示文件夹”的文件夹组织结构。
   **Shortcut:** **Ctrl+5**

7. **按命名空间对用户自定义函数分组**
   启用后，DAX 用户自定义函数将按 [命名空间](xref:udfs#namespaces) 以层级方式分组显示，而不是以扁平列表显示。

8. **显示/隐藏隐藏对象**
   切换是否显示隐藏对象。
   **Shortcut:** **Ctrl+6**

9. **Show/Hide Info Columns**
   Shows or hides metadata columns, such as data types or object status.
   **Shortcut:** **Ctrl+7**

10. **Show/Hide Table Groups**
    Toggle the visibility of table groups in the TOM Explorer tree. This provides quick access to the same setting found in **Tools > Preferences** without leaving the explorer.

11. **Show changes**
    Filters the tree down to objects with [unsaved changes](xref:unsaved-changes), together with the tables, folders and groups needed to reach them. While the filter is active, the title of the view reads **TOM Explorer (Changed)**.

12. **Perspective Selector**
    Drop-down to choose a specific perspective. TOM Explorer 中只会显示所选透视中的对象。

13. **语言选择器**
    用于在不同语言之间切换，以本地化模型元数据。

14. **全部折叠**
    折叠 TOM Explorer 树视图中的所有节点。

15. **Search Bar**
    Provides real-time filtering and navigation within the TOM Explorer. Type to search across all visible model objects.
