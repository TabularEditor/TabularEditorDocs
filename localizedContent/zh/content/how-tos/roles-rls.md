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

# 角色与行级安全性

Roles are visible in the Explorer Tree. You can right-click the tree to create new roles, delete or duplicate existing roles. You can view and edit the members of each role, by locating the role in the Explorer Tree, and navigating to the "Role Members" property in the Property Grid. Note that when deploying, the [Deployment Wizard](../features/deployment.md) does not deploy role members by default.

在 Tabular Editor 中管理角色的最大优势是：每个表对象都有一个“行级筛选器”属性，使你能够跨所有角色查看并编辑在该表上定义的筛选器：

![](~/content/assets/images/roles-rls-01.png)

当然，你也可以在某个特定角色中查看所有表的筛选器，界面类似于 SSMS 或 Visual Studio：

![](~/content/assets/images/roles-rls-02.png)