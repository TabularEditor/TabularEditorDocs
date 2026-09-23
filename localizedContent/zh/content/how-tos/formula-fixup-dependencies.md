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

# 公式修复与公式依赖关系

Tabular Editor 会持续解析模型中所有度量值、计算列和计算表格的 DAX 表达式，以构建这些对象的依赖关系树。 This dependency tree is used for the Formula Fix-up functionality, which may be enabled under **Tools > Preferences** (**File > Preferences** in Tabular Editor 2). 一旦表达式中引用的对象被重命名，“公式修复”就会自动更新相应度量值、计算列或计算表格的 DAX 表达式。

若要查看依赖关系树，请在资源管理器树中右键单击该对象，然后选择“显示依赖关系……”

![image](~/content/assets/images/formula-fixup-dependencies-01.png)