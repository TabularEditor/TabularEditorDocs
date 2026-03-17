---
uid: formula-fix-up-dependencies
title: 公式修复与公式依赖关系
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 公式修复与公式依赖关系

Tabular Editor 会持续解析模型中所有度量值、计算列和计算表格的 DAX 表达式，以构建这些对象的依赖关系树。 这个依赖关系树用于“公式修复”功能，可在“文件”>“偏好”中启用。 一旦表达式中引用的对象被重命名，“公式修复”就会自动更新相应度量值、计算列或计算表格的 DAX 表达式。

若要查看依赖关系树，请在资源管理器树中右键单击该对象，然后选择“显示依赖关系……”

![image](https://cloud.githubusercontent.com/assets/8976200/22482528/b37d27e2-e7f9-11e6-8b89-c503f9fffcac.png)