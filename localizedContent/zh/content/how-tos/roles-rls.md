---
uid: roles-and-rls
title: 角色与行级安全性
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 角色与行级安全性

角色会显示在资源管理器树形视图中。 你可以在树形视图中右键单击，以创建新角色、删除或复制现有角色。 你可以在资源管理器树中找到该角色，然后在属性网格中转到“角色成员”属性，以查看和编辑每个角色的成员。 注意，在部署时，[Deployment Wizard](../features/deployment.md) 默认不会部署角色成员。

在 Tabular Editor 中管理角色的最大优势是：每个表对象都有一个“行级筛选器”属性，使你能够跨所有角色查看并编辑在该表上定义的筛选器：

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/RLSTableContext.png)

当然，你也可以在某个特定角色中查看所有表的筛选器，界面类似于 SSMS 或 Visual Studio：

![](https://raw.githubusercontent.com/TabularEditor/TabularEditor/master/Documentation/RLSRoleContext.png)