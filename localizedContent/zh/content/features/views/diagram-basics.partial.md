## 添加表

可通过以下任一方式将初始表添加到关系图中：

- 在 TOM Explorer 中(多选)选择表，然后右键单击并选择 **添加到关系图**。
- 在 TOM Explorer 中(单选或多选)表，然后将表拖到关系图上
- Use the **Diagram > Add tables...** menu option, and (multi-)select the tables you want to add through the dialog box.
  ![关系图：添加表](~/content/assets/images/diagram-add-tables.png)

要向关系图添加更多表，可以再次使用上述方法；或者在关系图中右键单击现有表，并选择以下选项之一：

- **添加筛选此表的表**：将所有可能直接筛选当前选中表，或通过其他表间接筛选当前选中表的表添加到关系图中。 Useful when starting from a fact table.
- **添加所有相关表**：将所有与当前选中表直接相关的表添加到关系图中。 Useful when starting from a dimension table.
  ![Add Related Tables](~/content/assets/images/add-related-tables.png)

在继续之前，先按你的偏好重新排列并调整关系图中的表大小；或者使用 **关系图 > 自动排列** 功能，让 Tabular Editor 3 自动布局这些表。

## 使用关系图修改关系

要在两张表之间添加新关系，请找到该关系中事实表（多方）上的列，并将该列拖到维度表（单方）上对应的列。 Confirm the settings for the relationship and hit **OK**.

![创建关系](~/content/assets/images/create-relationship.png)

To edit an existing relationship, right-click on it and choose **Edit relationship**. The right-click menu also contains shortcuts for reversing or deleting a relationship, as shown on the screenshot below.

![编辑关系图](~/content/assets/images/edit-relationship-diagram.png)

> [!NOTE]
> 你也可以不使用关系图，而是通过 TOM Explorer 创建关系。 Locate the column from which the relationship should start (many-side / fact-table side), right-click and choose **Create > Relationship from**. Specify the destination column in the Create Relationship dialog that appears on the screen.

## Selection and navigation

A diagram and the TOM Explorer keep the same object selected. Clicking a table, a column or a relationship in the diagram selects it in the tree, without pulling focus away from the diagram. Going the other way, selecting a table or a column in the tree highlights it in every open diagram, scrolling a column into view inside its table shape.

This works for navigation you did not perform by hand in the tree: **Go to** actions and search results highlight in your diagrams too.

A selection that does not resolve to a single table or column, whether several objects or none, clears the diagram's highlight rather than leaving a stale one behind.

> [!NOTE]
> Selecting an object in the TOM Explorer never switches the active document to a diagram. If a diagram is open in the background it updates quietly, and you keep working where you were.

Double-click a relationship to open **Edit relationship**.

## 保存关系图

To save a diagram, use the **File > Save** (**Ctrl+S**) option. Tabular Editor 3 prompts you to save the diagram if you close the document or the application while the diagram has unsaved changes.

> [!TIP]
> 同一个关系图文件可以用于不同的 Data model。 Diagrams reference tables by their names. Any tables not present in the model upon diagram load are simply removed from the diagram.

> [!NOTE]
> 每次添加或修改关系后，都需要先对 Data model 运行一次“计算”刷新，然后才能在查询模型时使用这些关系。
