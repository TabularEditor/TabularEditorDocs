---
uid: scripting-referencing-objects
title: 脚本编写与对象引用
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 脚本编写与对象引用

你可以使用拖放功能，通过以下方式为对象生成脚本：

- 将一个或多个对象拖到另一款 Windows 应用程序 (文本编辑器或 SSMS)
  将会生成表示所拖动对象的 JSON 代码。 拖动“模型”节点、表、角色或数据源时，会生成 CreateOrReplace 脚本。

- 将对象（度量值、列或表）拖到 DAX 表达式编辑器中，会插入该对象的完全限定 DAX 引用。

- 将对象拖到高级脚本编辑器中，会插入通过 TOM 树访问该对象所需的 C# 代码。