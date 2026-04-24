---
uid: hierarchical-display
title: 层级显示
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      editions:
        - edition: Desktop
          full: true
        - edition: Business
          full: true
        - edition: Enterprise
          full: true
---

## 层级显示

已加载模型中的对象会显示在 TOM Explorer 树状视图中。 默认情况下，会显示所有对象类型（可见表、角色、关系等） 都会显示。 如果只想查看表、度量值、列和层级结构，请在“View”菜单中关闭“Show all object types”。

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/AllObjectTypes.png)

展开“Tables”组中的某个表后，会在该表下看到其包含的度量值、列和层级结构，默认按各自的显示文件夹显示。 这样，对象的排列方式就类似于最终用户在客户端工具中看到的效果：

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/DisplayFolders.png)

使用 Explorer Tree 正上方的按钮，可切换显示不可见对象、显示文件夹、度量值、列和层级结构，也可按名称筛选对象。 选中对象后按 F2 即可重命名。 显示文件夹也同样适用。 双击度量值或计算列，即可编辑其[DAX 表达式](dax-editor.md)。 右键单击会显示上下文菜单，提供一系列便捷的快捷操作，例如设置可见性、是否包含在透视中、将列添加到层级结构等。
