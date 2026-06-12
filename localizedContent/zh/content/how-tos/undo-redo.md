---
uid: undo-redo
title: 支持撤销/重做
applies_to:
  products:
    - product: Tabular Editor 2
      full: true
    - product: Tabular Editor 3
      full: true
---

## 支持撤销/重做

你在 Tabular Editor 中所做的任何更改，都可以使用 CTRL+Z 撤销，随后可使用 CTRL+Y 重做。 可撤销的操作次数没有限制，但当你打开 Model.bim 文件或从数据库加载模型时，撤销/重做堆栈会被重置。 可撤销的操作次数没有限制，但当你打开 Model.bim 文件或从数据库加载模型时，撤销/重做堆栈会被重置。

从模型中删除对象时，所有引用该对象的翻译、透视和关系也会自动删除（而在 Visual Studio 中通常会显示错误信息，提示该对象无法删除）。 如果误删除了对象，你可以使用“撤销”功能将其恢复，同时也会恢复随之删除的任何翻译、透视或关系。 请注意，尽管 Tabular Editor 可以检测 [DAX 公式依赖项](xref:formula-fix-up-dependencies)，但如果你删除了在其他度量值或计算列的 DAX 表达式中被引用的度量值或列，Tabular Editor 并不会发出警告。 如果误删除了对象，你可以使用“撤销”功能将其恢复，同时也会恢复随之删除的任何翻译、透视或关系。 请注意，尽管 Tabular Editor 可以检测 [DAX 公式依赖项](xref:formula-fix-up-dependencies)，但如果你删除了在其他度量值或计算列的 DAX 表达式中被引用的度量值或列，Tabular Editor 并不会发出警告。