---
uid: formula-fix-up-dependencies
title: 公式修正和公式依赖关系
author: Morten Lønskov
updated: 2026-09-23
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

# 公式修正和公式依赖关系
Tabular Editor 持续解析模型中所有度量值、计算列和计算表的 DAX 表达式，并构建这些对象的依赖关系树。*公式修正*使用该树：当您重命名一个对象时，它会更新引用该对象的 DAX 表达式。在**工具 > 首选项 > Tabular Editor > 建模操作**（Tabular Editor 2 中为**文件 > 首选项**）下，通过**自动 DAX 公式修正**启用此功能。

在 TOM Explorer 中右键单击一个对象，然后选择**显示依赖项……**，以查看其依赖关系树。

![显示 measure 所依赖对象的“对象依赖关系”对话框](~/content/assets/images/formula-fixup-dependencies-01.png)